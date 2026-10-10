"""M11.L01 — Continuous Delivery, AutoML, and KaizenML.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapters 4–5, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M11.L01"

MODULE_ORDER = 11

MODULE_TITLE = "Continuous Delivery, AutoML, and KaizenML"

MODULE_DESCRIPTION = (
    "Learn how to package and continuously deliver ML models with automated tests "
    "and controlled rollouts, then extend that automation mindset into AutoML and "
    "KaizenML: continuous improvement of data, features, software, models, "
    "deployment, explainability, and feedback."
)

SOURCE_CHAPTER = 4
SOURCE_CHAPTERS = [4, 5]
SOURCE_PAGES = "Not provided"


TOPIC = {
    "title": "Continuous Delivery, AutoML, and KaizenML",
    "slug": "practical-mlops-m11-l01-continuous-delivery-automl-kaizenml",
    "description": (
        "A combined production-focused lesson covering model packaging, CI/CD, "
        "infrastructure as code, cloud ML pipelines, controlled rollout, automated "
        "deployment tests, AutoML, feature stores, managed and open-source AutoML "
        "platforms, explainability, and KaizenML as continuous improvement across "
        "the entire machine-learning system."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 6.0,
    "skill_tags": [
        "continuous-integration",
        "continuous-delivery",
        "model-packaging",
        "containers",
        "onnx",
        "flask",
        "github-actions",
        "infrastructure-as-code",
        "container-registry",
        "cloud-pipelines",
        "sagemaker-pipelines",
        "blue-green-deployment",
        "canary-deployment",
        "rollback",
        "automated-testing",
        "linting",
        "shift-left",
        "continuous-improvement",
        "automl",
        "kaizenml",
        "data-centric-ml",
        "feature-store",
        "create-ml",
        "core-ml",
        "vertex-ai",
        "azure-automl",
        "sagemaker-autopilot",
        "ludwig",
        "flaml",
        "model-explainability",
        "shap",
        "eli5",
    ],
    "prerequisite_ids": ["M10.L01"],

    "lesson": {
        "title": "Continuous Delivery, AutoML, and KaizenML",
        "content": (
            "# Continuous Delivery, AutoML, and KaizenML\n"
            "\n"
            "> **Lesson:** M11.L01  \n"
            "> **Module:** Continuous Delivery, AutoML, and KaizenML  \n"
            "> **Source alignment:** Chapters 4–5. Page numbers were not included "
            "in the supplied sources. This lesson is an instructor-authored curriculum "
            "adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why CI/CD is fundamentally a feedback-and-automation discipline.\n"
            "- Package a model together with its runtime and prediction service in a container.\n"
            "- Explain the benefits of containerized model packaging for portability, sharing, and deployment.\n"
            "- Explain why model binaries should not be treated like ordinary source-code files.\n"
            "- Describe an infrastructure-as-code workflow that retrieves, packages, and publishes a registered model.\n"
            "- Explain why CI/CD jobs should be broken into small, single-responsibility steps.\n"
            "- Explain how secrets are used in automated delivery workflows.\n"
            "- Explain the role of a container registry in model delivery.\n"
            "- Distinguish generic CI/CD pipelines from ML-specific cloud pipelines.\n"
            "- Design pipelines with data preparation, training, evaluation, registration, and deployment stages.\n"
            "- Compare blue-green and canary deployment strategies.\n"
            "- Explain rollback and production-health gating during model rollout.\n"
            "- Design automated functional and API-contract checks for model services.\n"
            "- Explain why linting and early validation support a shift-left strategy.\n"
            "- Define AutoML and explain what it does—and does not—automate.\n"
            "- Define KaizenML as continuous improvement across the whole ML system.\n"
            "- Explain why AutoML is only one part of MLOps automation.\n"
            "- Explain the role of feature stores in reuse and automation.\n"
            "- Describe the high-level AutoML workflows presented for Apple, Google, Azure, AWS, Ludwig, and FLAML.\n"
            "- Explain when using a pretrained model may be more efficient than training a new one.\n"
            "- Explain the importance of model explainability in automated ML workflows.\n"
            "- Distinguish SHAP-style explanations from permutation-importance-style explanations at a conceptual level.\n"
            "- Connect continuous delivery and AutoML through a single KaizenML mindset: automate, evaluate, improve, repeat.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Continuous delivery begins with continuous evaluation\n"
            "\n"
            "The first source chapter uses an injury-recovery analogy to explain the central idea of CI/CD: "
            "evaluate continuously, react to feedback, change the strategy when needed, and keep improving the process.\n"
            "\n"
            "A manual release process built around emails, memory, and human confirmation is slow and inconsistent.\n"
            "\n"
            "A robust CI/CD process replaces that with explicit, repeatable checks:\n"
            "\n"
            "```text\n"
            "Change\n"
            "  ↓\n"
            "Build\n"
            "  ↓\n"
            "Verify\n"
            "  ↓\n"
            "Package\n"
            "  ↓\n"
            "Release / Deploy\n"
            "  ↓\n"
            "Observe result\n"
            "  ↓\n"
            "Improve the process\n"
            "```\n"
            "\n"
            "The important word is **continuous**: not 'deploy every minute,' but maintain a recurring feedback process "
            "that steadily reduces risk and manual work.\n"
            "\n"
            "[[IMAGE_NEEDED: Continuous delivery feedback loop | "
            "A circular process from code/model change to build, test, package, deploy, observe, and improve | "
            "Learner should notice that feedback and improvement are built into the release process]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Packaging an ML model means packaging the environment around it\n"
            "\n"
            "In the source, **packaging an ML model** means placing the model and the software required to serve it "
            "inside a container.\n"
            "\n"
            "Why is that useful?\n"
            "\n"
            "1. A container can be run locally wherever a compatible container runtime exists.\n"
            "2. Cloud providers can deploy and scale containers.\n"
            "3. Other people can pull and try the same packaged system with far less setup ambiguity.\n"
            "\n"
            "The result is a more portable and debuggable unit than a loose collection of scripts, package instructions, "
            "and model files.\n"
            "\n"
            "[[IMAGE_NEEDED: What a packaged ML model contains | "
            "A container boundary around prediction-service code, exact dependencies, tokenizer/preprocessing logic, "
            "runtime library, and serialized model | Learner should notice that packaging includes the inference environment, not only weights]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Example: ONNX model behind a Flask prediction endpoint\n"
            "\n"
            "The source packages a RoBERTa sequence-classification model exported to ONNX and serves it through Flask.\n"
            "\n"
            "The project contains four important pieces:\n"
            "\n"
            "```text\n"
            "Dockerfile\n"
            "requirements.txt\n"
            "model.onnx\n"
            "webapp/app.py\n"
            "```\n"
            "\n"
            "The prediction path is conceptually:\n"
            "\n"
            "```text\n"
            "JSON request\n"
            "   ↓\n"
            "Tokenizer\n"
            "   ↓\n"
            "Tensor / NumPy conversion\n"
            "   ↓\n"
            "ONNX Runtime\n"
            "   ↓\n"
            "Class prediction\n"
            "   ↓\n"
            "JSON response\n"
            "```\n"
            "\n"
            "A simplified source-aligned serving skeleton is:\n"
            "\n"
            "```python\n"
            "from flask import Flask, request, jsonify\n"
            "import onnxruntime\n"
            "\n"
            "app = Flask(__name__)\n"
            "session = onnxruntime.InferenceSession(\"model.onnx\")\n"
            "\n"
            "@app.route(\"/predict\", methods=[\"POST\"])\n"
            "def predict():\n"
            "    # tokenize / convert request\n"
            "    # run model\n"
            "    # return JSON prediction\n"
            "    return jsonify({\"positive\": True})\n"
            "```\n"
            "\n"
            "The educational point is the shape of the production unit: prediction code, runtime, dependencies, and model "
            "must all agree on paths, input schema, and output schema.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Test locally before automating delivery\n"
            "\n"
            "The chapter validates the application in two stages:\n"
            "\n"
            "### Stage 1: run the application directly\n"
            "\n"
            "Create an environment, install dependencies, launch the Flask app, and call `/predict` using an HTTP request.\n"
            "\n"
            "### Stage 2: run the packaged container\n"
            "\n"
            "Build the image and expose the service port:\n"
            "\n"
            "```bash\n"
            "docker build -t my-model-service .\n"
            "docker run -it -p 5000:5000 --rm my-model-service\n"
            "```\n"
            "\n"
            "Then call the same endpoint again.\n"
            "\n"
            "Why repeat the test? Because the container adds another layer where missing files, dependency problems, incorrect "
            "working directories, or port configuration can break the service even when local Python execution succeeds.\n"
            "\n"
            "{{exercise:M11.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Infrastructure as code makes model delivery reproducible\n"
            "\n"
            "The chapter presents a failure mode: a container image exists in a registry, but nobody has the source files "
            "needed to recreate it.\n"
            "\n"
            "The correct response is not to reverse engineer the image every time. The better solution is to define the build "
            "process in version-controlled automation.\n"
            "\n"
            "A reproducible delivery process can specify:\n"
            "\n"
            "- where the source code comes from,\n"
            "- where the registered model comes from,\n"
            "- how authentication works,\n"
            "- how the image is built,\n"
            "- which tests run,\n"
            "- which registry receives the result.\n"
            "\n"
            "This is infrastructure-as-code thinking: **the process that creates the deployable artifact should itself be reproducible.**\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Keep large model artifacts separate from ordinary source control\n"
            "\n"
            "The source warns against treating large model binaries like normal Git-managed text files.\n"
            "\n"
            "Two practical issues are emphasized:\n"
            "\n"
            "- hosted Git systems can impose large-file limits,\n"
            "- Git's normal history model is not designed for repeatedly versioning large binary model files.\n"
            "\n"
            "A better pattern is:\n"
            "\n"
            "```text\n"
            "Git repository\n"
            "  ├── source code\n"
            "  ├── Dockerfile\n"
            "  ├── workflow definition\n"
            "  └── tests\n"
            "\n"
            "Model registry / ML platform\n"
            "  └── versioned model artifact\n"
            "```\n"
            "\n"
            "The delivery workflow retrieves the correct registered model during the build.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Automate model packaging with a CI/CD workflow\n"
            "\n"
            "The source uses GitHub Actions as the automation platform.\n"
            "\n"
            "The workflow is triggered by a change to the main branch or manually.\n"
            "\n"
            "Its high-level steps are:\n"
            "\n"
            "1. check out the repository,\n"
            "2. authenticate to the cloud platform,\n"
            "3. attach/configure the ML workspace,\n"
            "4. retrieve the registered model,\n"
            "5. build the prediction-service container,\n"
            "6. authenticate to a container registry,\n"
            "7. publish the image.\n"
            "\n"
            "A simplified YAML shape is:\n"
            "\n"
            "```yaml\n"
            "on:\n"
            "  push:\n"
            "    branches: [main]\n"
            "\n"
            "jobs:\n"
            "  build:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - checkout source\n"
            "      - authenticate cloud\n"
            "      - download registered model\n"
            "      - build container\n"
            "      - run checks\n"
            "      - push container\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: CI/CD model packaging workflow | "
            "Git push triggering source checkout, cloud authentication, model-registry download, container build, checks, and registry publish | "
            "Learner should notice how the model artifact and source code are reunited automatically during delivery]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Small CI/CD steps create smaller failure domains\n"
            "\n"
            "The chapter warns against **greedy steps**—pipeline steps that try to do too much.\n"
            "\n"
            "Compare:\n"
            "\n"
            "```text\n"
            "One giant step:\n"
            "download + validate + train + package + publish\n"
            "```\n"
            "\n"
            "with:\n"
            "\n"
            "```text\n"
            "Step 1: download\n"
            "Step 2: validate\n"
            "Step 3: train\n"
            "Step 4: package\n"
            "Step 5: publish\n"
            "```\n"
            "\n"
            "When a pipeline fails, small responsibilities make the failure easier to locate and debug.\n"
            "\n"
            "This is a recurring theme across both chapters: automation should simplify the system, not merely hide a giant manual script inside a CI runner.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Secrets and registries complete the delivery path\n"
            "\n"
            "Automated workflows need credentials to access model registries, cloud workspaces, and container registries.\n"
            "\n"
            "Those credentials should be stored as CI/CD secrets rather than hard-coded in the workflow file.\n"
            "\n"
            "The chapter demonstrates this with cloud credentials and registry tokens.\n"
            "\n"
            "A **container registry** then becomes the distribution point for the built image.\n"
            "\n"
            "```text\n"
            "CI runner\n"
            "  ↓ authenticate\n"
            "Container registry\n"
            "  ↓ pull\n"
            "Staging / production environment\n"
            "```\n"
            "\n"
            "The main operational benefit is that the same versioned packaged artifact can be consumed repeatedly by downstream systems.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Cloud ML pipelines organize multi-step model workflows\n"
            "\n"
            "A pipeline is simply a sequence or graph of steps that achieves an objective.\n"
            "\n"
            "Common pipeline elements include:\n"
            "\n"
            "- build,\n"
            "- test,\n"
            "- release,\n"
            "- deploy,\n"
            "- validate.\n"
            "\n"
            "ML workflows often add:\n"
            "\n"
            "- extract data,\n"
            "- preprocess data,\n"
            "- train,\n"
            "- evaluate,\n"
            "- register model.\n"
            "\n"
            "The source emphasizes that the exact steps should match the workflow; there is no requirement that every pipeline use the same fixed template.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Generic CI/CD and ML-specific pipeline systems solve overlapping problems\n"
            "\n"
            "GitHub Actions or Jenkins are general automation systems.\n"
            "\n"
            "An ML-specific platform such as the SageMaker pipeline example in the source can provide more direct support for:\n"
            "\n"
            "- data preparation,\n"
            "- specialized training compute,\n"
            "- model evaluation,\n"
            "- model registration,\n"
            "- later deployment.\n"
            "\n"
            "ML-specific pipeline systems can also make GPU-intensive training resources easier to provision than a generic build runner.\n"
            "\n"
            "The chapter's broader point is not that one class of tool always replaces the other. Use the tool whose abstractions fit the job.\n"
            "\n"
            "[[IMAGE_NEEDED: Generic CI/CD versus ML-specific pipeline | "
            "A comparison of generic source/build/test automation and an ML pipeline with data prep, GPU training, evaluation, model registry, and deployment | "
            "Learner should notice the shared automation concept but different domain-specific capabilities]]\n"
            "\n"
            "{{exercise:M11.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Blue-green deployment: prepare the full replacement before switching traffic\n"
            "\n"
            "A blue-green strategy keeps the old production version and the new version separate.\n"
            "\n"
            "The new version is deployed into an environment intended to match production closely, then tested before traffic is switched.\n"
            "\n"
            "```text\n"
            "Current traffic → Green v1\n"
            "\n"
            "Blue v2 deployed separately\n"
            "      ↓\n"
            "verify\n"
            "      ↓\n"
            "switch traffic to Blue\n"
            "```\n"
            "\n"
            "The main strength is isolation before cutover.\n"
            "\n"
            "The practical challenge is faithfully maintaining two production-like versions/environments.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Canary deployment: increase traffic only while the candidate remains healthy\n"
            "\n"
            "A canary sends a small share of production traffic to the new model while the previous version continues serving the rest.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "90% → current model\n"
            "10% → candidate model\n"
            "```\n"
            "\n"
            "If the candidate remains healthy, the percentage can rise toward 100%.\n"
            "\n"
            "If errors increase, traffic can be returned to the old version. That reversal is a **rollback**.\n"
            "\n"
            "The source's dependency-error example is useful: a candidate can have better model accuracy and still fail as a software service.\n"
            "\n"
            "Therefore canary health gates must include operational metrics as well as model metrics.\n"
            "\n"
            "[[IMAGE_NEEDED: Blue-green versus canary deployment | "
            "Blue-green shows separate old/new environments and one traffic switch; canary shows progressive traffic percentages with rollback | "
            "Learner should notice that both reduce release risk in different ways]]\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Test every layer of the prediction service contract\n"
            "\n"
            "The chapter decomposes one model request into testable layers:\n"
            "\n"
            "1. the client sends the expected JSON schema,\n"
            "2. the correct port and route exist,\n"
            "3. Flask parses the payload correctly,\n"
            "4. the runtime receives correctly shaped model input,\n"
            "5. the service produces the expected JSON response and HTTP status.\n"
            "\n"
            "This is a crucial MLOps insight:\n"
            "\n"
            "> **Good offline accuracy does not prove that the deployed software contract is correct.**\n"
            "\n"
            "For example, these two outputs look similar to a human:\n"
            "\n"
            "```json\n"
            "{\"positive\": false}\n"
            "```\n"
            "\n"
            "and:\n"
            "\n"
            "```json\n"
            "{\"positive\": \"false\"}\n"
            "```\n"
            "\n"
            "But one uses a boolean and the other a string. A client expecting a boolean may break even though the model itself is healthy.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Automated checks belong inside the pipeline\n"
            "\n"
            "The source argues that verification should be automated rather than relying on last-minute manual inspection.\n"
            "\n"
            "Useful checks include:\n"
            "\n"
            "- container build succeeds,\n"
            "- service starts,\n"
            "- endpoint exists,\n"
            "- valid inputs return expected schema,\n"
            "- invalid inputs return controlled errors,\n"
            "- dependency versions are compatible,\n"
            "- linters catch code mistakes,\n"
            "- model/runtime integration works.\n"
            "\n"
            "The goal is not merely automation for speed. It is repeatable confidence.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Shift left: find problems when they are cheapest to fix\n"
            "\n"
            "The source uses linting as a simple example.\n"
            "\n"
            "An undefined import found by a linter takes seconds to fix during development.\n"
            "\n"
            "The same problem discovered only after a production rollout can require incident response and rollback.\n"
            "\n"
            "```text\n"
            "Developer → CI → staging → canary → production\n"
            "   ↑ cheaper detection                ↑ expensive detection\n"
            "```\n"
            "\n"
            "This 'shift-left' principle applies to syntax, API contracts, dependencies, security checks, data validation, and model integration.\n"
            "\n"
            "{{exercise:M11.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Continuous delivery naturally leads to continuous improvement\n"
            "\n"
            "The source tells a release story where a seemingly harmless one-line change broke the released software.\n"
            "\n"
            "The important lesson is not 'never make small changes.' It is:\n"
            "\n"
            "> **If a failure occurs, improve the process so that class of failure becomes cheaper or impossible next time.**\n"
            "\n"
            "That idea forms a bridge into the second chapter.\n"
            "\n"
            "Continuous delivery improves how artifacts are shipped. KaizenML extends continuous improvement across the whole ML system.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. AutoML automates model creation from prepared data\n"
            "\n"
            "The second source defines **AutoML** narrowly: automation of tasks involved in training a model from clean data.\n"
            "\n"
            "That can include combinations of:\n"
            "\n"
            "- algorithm/model selection,\n"
            "- hyperparameter search,\n"
            "- preprocessing choices,\n"
            "- training,\n"
            "- evaluation,\n"
            "- model export.\n"
            "\n"
            "The author's central argument is that teams should use automation where it reduces manual complexity.\n"
            "\n"
            "AutoML is therefore best understood as a technique for automating the modeling portion of an ML workflow.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. KaizenML automates and improves the whole ML system\n"
            "\n"
            "**Kaizen** means continuous improvement in the framing used by the source.\n"
            "\n"
            "The chapter defines **KaizenML** more broadly than AutoML.\n"
            "\n"
            "It includes continuous improvement of:\n"
            "\n"
            "- data quality,\n"
            "- feature quality,\n"
            "- software quality,\n"
            "- model quality,\n"
            "- deployment automation,\n"
            "- production feedback.\n"
            "\n"
            "A useful relationship from the source is:\n"
            "\n"
            "```text\n"
            "AutoML = automation of model creation\n"
            "\n"
            "KaizenML = continuous improvement of the end-to-end ML system\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: AutoML inside KaizenML | "
            "A small AutoML circle inside a much larger KaizenML system containing data, features, software, testing, deployment, monitoring, and feedback | "
            "Learner should notice that automated modeling is only one part of system-wide automation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Automation should move effort from repetitive mechanics toward execution\n"
            "\n"
            "The source repeatedly contrasts research or manual tuning with the goal of turning useful ideas into working systems.\n"
            "\n"
            "The practical engineering takeaway is:\n"
            "\n"
            "- do not write custom code merely to prove you can,\n"
            "- use high-level tools when they solve the problem correctly,\n"
            "- reserve human attention for decisions that actually require judgment.\n"
            "\n"
            "This does not mean humans disappear from ML.\n"
            "\n"
            "The chapter explicitly presents AutoML as a technique within a larger human-directed MLOps process.\n"
            "\n"
            "The engineer still chooses the problem, data, quality requirements, deployment target, and whether the automated result is useful.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. KaizenML treats data, software, and models as equal improvement targets\n"
            "\n"
            "A model-centric workflow can spend enormous effort squeezing incremental gains from hyperparameters while ignoring poor data or fragile software.\n"
            "\n"
            "The source advocates a broader data-centric and systems-centric view:\n"
            "\n"
            "```text\n"
            "Data quality\n"
            "   +\n"
            "Software quality\n"
            "   +\n"
            "Model quality\n"
            "   +\n"
            "Feedback loop quality\n"
            "   =\n"
            "Production ML quality\n"
            "```\n"
            "\n"
            "This is the strongest connection between the two chapters: Chapter 4 automates delivery quality; Chapter 5 says to apply the same thinking everywhere.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Feature stores are one KaizenML mechanism\n"
            "\n"
            "The source describes a feature store as a shared mechanism for high-quality ML inputs.\n"
            "\n"
            "Two practical capabilities are emphasized:\n"
            "\n"
            "1. users can add reusable features to a shared store,\n"
            "2. stored features become easier to reuse in training and prediction.\n"
            "\n"
            "Feature stores support the automation mindset because repeated feature engineering work can move from bespoke project code into shared infrastructure.\n"
            "\n"
            "The source contrasts a data warehouse and a feature store at a high level:\n"
            "\n"
            "- a warehouse commonly supports analytics/business-intelligence workloads,\n"
            "- a feature store organizes inputs used by ML systems.\n"
            "\n"
            "Feature stores therefore connect data engineering with model automation.\n"
            "\n"
            "[[IMAGE_NEEDED: Data warehouse and feature store roles | "
            "Raw data flowing to a warehouse for analytics and to a feature pipeline/store that supplies reusable batch/online ML features | "
            "Learner should notice that feature stores specialize repeated data preparation for ML use]]\n"
            "\n"
            "{{exercise:M11.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Apple ecosystem: AutoML plus on-device deployment\n"
            "\n"
            "The source presents Apple's ecosystem as an example of vertically integrated ML tooling.\n"
            "\n"
            "Three workflows are highlighted:\n"
            "\n"
            "1. train with Create ML,\n"
            "2. use a pretrained model,\n"
            "3. train elsewhere and convert the model to Core ML.\n"
            "\n"
            "Create ML exposes high-level automated training through a GUI and supports several data domains.\n"
            "\n"
            "The important lesson is not the specific interface. It is the reduction of friction from data to a deployable on-device model.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Sometimes the best automation is not training at all\n"
            "\n"
            "The Core ML example makes a valuable point: if a strong pretrained model already exists, it may be cheaper and faster to reuse or convert it "
            "than to train another model from scratch.\n"
            "\n"
            "The workflow becomes:\n"
            "\n"
            "```text\n"
            "Find pretrained model\n"
            "      ↓\n"
            "Convert to deployment format\n"
            "      ↓\n"
            "Add metadata / labels / input contract\n"
            "      ↓\n"
            "Validate\n"
            "      ↓\n"
            "Deploy\n"
            "```\n"
            "\n"
            "KaizenML is about reducing unnecessary work, not maximizing the number of custom training jobs.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Google AutoML: high-level training connected to cloud and edge deployment\n"
            "\n"
            "The source's Google workflow includes:\n"
            "\n"
            "- enabling the AutoML service,\n"
            "- uploading labeled training data,\n"
            "- visually inspecting and correcting the data,\n"
            "- training,\n"
            "- evaluating,\n"
            "- deploying online or exporting for edge targets.\n"
            "\n"
            "The notable systems lesson is that an integrated platform can shorten the path from prepared data to multiple deployment targets.\n"
            "\n"
            "[[IMAGE_NEEDED: Managed AutoML lifecycle | "
            "Prepared labeled data flowing through inspection, automated training, evaluation, and either hosted endpoint or edge-model export | "
            "Learner should notice how one platform can integrate modeling with deployment destinations]]\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Azure AutoML: GUI and programmatic automation\n"
            "\n"
            "The source highlights two access patterns for Azure AutoML:\n"
            "\n"
            "- a visual ML Studio workflow,\n"
            "- a Python SDK workflow.\n"
            "\n"
            "The platform can automate tasks such as classification, regression, and forecasting workflows and can expose explanation capabilities after training.\n"
            "\n"
            "A source-aligned SDK shape is:\n"
            "\n"
            "```python\n"
            "automl_config = AutoMLConfig(\n"
            "    task=\"regression\",\n"
            "    training_data=x_train,\n"
            "    label_column_name=\"target\",\n"
            "    **automl_settings,\n"
            ")\n"
            "```\n"
            "\n"
            "The conceptual point is that AutoML can be used interactively or embedded into repeatable code-driven workflows.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. SageMaker Autopilot: AutoML inside a broader ML platform\n"
            "\n"
            "The source's SageMaker example follows a full managed workflow:\n"
            "\n"
            "```text\n"
            "Upload dataset\n"
            "   ↓\n"
            "Select target\n"
            "   ↓\n"
            "Automated preprocessing + model tuning\n"
            "   ↓\n"
            "Compare candidate models\n"
            "   ↓\n"
            "Inspect metrics / explainability\n"
            "   ↓\n"
            "Deploy selected model\n"
            "```\n"
            "\n"
            "This is significant because AutoML is connected to the wider MLOps lifecycle rather than existing as an isolated model-search script.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Open-source AutoML lowers the cost of automation\n"
            "\n"
            "The chapter also discusses open-source AutoML systems.\n"
            "\n"
            "### Ludwig\n"
            "\n"
            "Ludwig lets users configure and run model training at a high level instead of writing a custom training loop for every project.\n"
            "\n"
            "A simplified source-aligned CLI shape is:\n"
            "\n"
            "```bash\n"
            "ludwig experiment --dataset data.csv --config_file config.yaml\n"
            "```\n"
            "\n"
            "### FLAML\n"
            "\n"
            "FLAML is presented as a cost-aware automated model-selection and hyperparameter-optimization tool.\n"
            "\n"
            "A minimal usage pattern is:\n"
            "\n"
            "```python\n"
            "from flaml import AutoML\n"
            "\n"
            "automl = AutoML()\n"
            "automl.fit(X_train, y_train, task=\"classification\")\n"
            "```\n"
            "\n"
            "The broader lesson is that powerful automation is not limited to large managed cloud products.\n"
            "\n"
            "{{exercise:M11.L01.EX05}}\n"
            "\n"
            "---\n"
            "\n"

            "## 29. AutoML still needs human constraints and judgment\n"
            "\n"
            "Automation does not decide everything for you.\n"
            "\n"
            "Humans still define or validate:\n"
            "\n"
            "- the problem to solve,\n"
            "- the target label,\n"
            "- whether the data is appropriate,\n"
            "- the evaluation metric,\n"
            "- compute/time budgets,\n"
            "- deployment constraints,\n"
            "- whether the final behavior creates useful value.\n"
            "\n"
            "An automated system can efficiently optimize the wrong metric if the human framing is wrong.\n"
            "\n"
            "This is why AutoML is a component of MLOps rather than a replacement for ML systems engineering.\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Explainability should be automated alongside modeling\n"
            "\n"
            "The source argues that an MLOps team should inspect explanation information in the same spirit that software teams inspect CPU or memory dashboards.\n"
            "\n"
            "Managed platforms may provide built-in explainability, while open-source libraries can provide similar capabilities.\n"
            "\n"
            "Two tools discussed are:\n"
            "\n"
            "- **SHAP** — explains feature contributions using a game-theoretic framework and provides local/global visualizations,\n"
            "- **ELI5** — provides model inspection tools including permutation importance for supported models.\n"
            "\n"
            "The purpose is not to make every model perfectly interpretable. It is to make automated model creation less opaque to engineers and stakeholders.\n"
            "\n"
            "[[IMAGE_NEEDED: Explainability as an MLOps dashboard | "
            "An ML operations dashboard combining infrastructure health with global feature importance and one local prediction explanation | "
            "Learner should notice that model behavior can be monitored alongside software behavior]]\n"
            "\n"
            "---\n"
            "\n"

            "## 31. SHAP: explain how features push a prediction\n"
            "\n"
            "In the source example, SHAP is applied to an XGBoost model.\n"
            "\n"
            "A local explanation can show which features push a prediction upward or downward.\n"
            "\n"
            "A global summary can show which features contribute most strongly across many predictions.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Prediction\n"
            "  ↑ pushed by feature A\n"
            "  ↑ pushed by feature B\n"
            "  ↓ pushed by feature C\n"
            "```\n"
            "\n"
            "This gives engineers a structured way to investigate whether the model is relying on sensible inputs.\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Permutation importance: measure performance loss when a feature is disrupted\n"
            "\n"
            "The source uses ELI5's permutation-importance tooling on a logistic-regression model.\n"
            "\n"
            "The core idea is:\n"
            "\n"
            "1. measure normal model performance,\n"
            "2. disrupt one feature's information,\n"
            "3. measure how much performance decreases,\n"
            "4. larger decreases suggest greater model dependence on that feature.\n"
            "\n"
            "Different model families can produce different feature-importance patterns even on similar data.\n"
            "\n"
            "Explainability should therefore be interpreted as evidence about a particular model, not universal truth about the world.\n"
            "\n"
            "{{exercise:M11.L01.EX06}}\n"
            "\n"
            "---\n"
            "\n"

            "## 33. Continuous delivery and AutoML are one automation story\n"
            "\n"
            "The two chapters fit naturally together.\n"
            "\n"
            "Chapter 4 asks:\n"
            "\n"
            "> How can we repeatedly ship a known model safely?\n"
            "\n"
            "Chapter 5 asks:\n"
            "\n"
            "> How can we automate more of model creation and continuously improve the whole ML system?\n"
            "\n"
            "Together:\n"
            "\n"
            "```text\n"
            "Data\n"
            " ↓\n"
            "Reusable features\n"
            " ↓\n"
            "AutoML / model creation\n"
            " ↓\n"
            "Evaluation + explainability\n"
            " ↓\n"
            "Registered model\n"
            " ↓\n"
            "Automated packaging\n"
            " ↓\n"
            "CI/CD tests\n"
            " ↓\n"
            "Controlled rollout\n"
            " ↓\n"
            "Production feedback\n"
            " ↺ continuous improvement\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: End-to-end KaizenML automation loop | "
            "A full loop from data and feature store through AutoML, evaluation, registry, CI/CD packaging, canary deployment, and production feedback | "
            "Learner should notice how both source chapters combine into one continuous-improvement system]]\n"
            "\n"
            "---\n"
            "\n"

            "## 34. What should be automated first?\n"
            "\n"
            "The strongest practical rule across the sources is to automate recurring sources of friction and failure.\n"
            "\n"
            "Good early candidates include:\n"
            "\n"
            "- environment/package construction,\n"
            "- container builds,\n"
            "- service-contract tests,\n"
            "- linting,\n"
            "- model retrieval and packaging,\n"
            "- image publishing,\n"
            "- model registration,\n"
            "- repeated feature preparation,\n"
            "- repetitive model search,\n"
            "- explanation/report generation.\n"
            "\n"
            "Automation is most valuable when it makes the next failure easier to understand and the next release easier to trust.\n"
            "\n"
            "{{exercise:M11.L01.EX07}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: CI/CD means deploying continuously with no controls\n"
            "\n"
            "The chapter's focus is continuous feedback, verification, and safer delivery—not removing quality gates.\n"
            "\n"
            "### Misconception 2: Packaging a model means only copying the model file\n"
            "\n"
            "The serving code, runtime, dependencies, preprocessing, and API contract are part of the deployable unit.\n"
            "\n"
            "### Misconception 3: High model accuracy proves the deployed service works\n"
            "\n"
            "The API, dependency versions, input/output types, routes, and runtime can fail independently of model quality.\n"
            "\n"
            "### Misconception 4: One large pipeline step is simpler\n"
            "\n"
            "It may be shorter to write, but it creates a much larger failure domain and is harder to debug.\n"
            "\n"
            "### Misconception 5: Canary rollout only needs model metrics\n"
            "\n"
            "Operational errors such as HTTP failures or dependency breakage can make a high-accuracy model unusable.\n"
            "\n"
            "### Misconception 6: AutoML automates the entire ML lifecycle\n"
            "\n"
            "The source defines AutoML mainly around model creation from clean data. KaizenML is the broader system-improvement concept.\n"
            "\n"
            "### Misconception 7: AutoML eliminates the need for ML engineers\n"
            "\n"
            "Humans still choose objectives, data, constraints, metrics, integration, deployment, and product decisions.\n"
            "\n"
            "### Misconception 8: Training a model yourself is always more 'real' than using a pretrained model\n"
            "\n"
            "The source explicitly treats model reuse and conversion as valid, often more efficient workflows.\n"
            "\n"
            "### Misconception 9: Feature stores and AutoML solve the same problem\n"
            "\n"
            "Feature stores improve reusable ML inputs; AutoML automates parts of model creation.\n"
            "\n"
            "### Misconception 10: Explainability is only for research reports\n"
            "\n"
            "The source treats explanation information as an operational signal that can be part of MLOps workflows.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Continuous integration (CI) | Repeated automated integration and verification of changes. |\n"
            "| Continuous delivery (CD) | Automated, repeatable process for preparing artifacts for safe release/deployment. |\n"
            "| Model packaging | Bundling a model with the runtime and software needed to execute it. |\n"
            "| Container registry | Repository used to store and distribute container images. |\n"
            "| Infrastructure as code | Defining infrastructure/build/deployment processes in versioned, reproducible configuration/code. |\n"
            "| Pipeline | Ordered or dependency-aware set of steps used to accomplish an automation goal. |\n"
            "| Failure domain | Scope within which a failure can occur or must be diagnosed. |\n"
            "| Blue-green deployment | Deploy new version separately, validate it, then switch traffic from old to new. |\n"
            "| Canary deployment | Send a growing fraction of live traffic to a candidate while monitoring health. |\n"
            "| Rollback | Return traffic or deployment state to a previously working version. |\n"
            "| Shift left | Move error detection earlier in the software/model delivery lifecycle. |\n"
            "| AutoML | Automation of model-training/model-selection tasks from prepared data. |\n"
            "| KaizenML | Continuous improvement and automation across data, software, features, models, deployment, and feedback. |\n"
            "| Data-centric ML | Emphasis on improving data quality and data processes, not only model architecture. |\n"
            "| Feature store | Shared system for reusable features used in model training and/or prediction. |\n"
            "| Pretrained model | Model trained previously and reused or adapted instead of training from scratch. |\n"
            "| Explainability | Methods for inspecting why a model produced its predictions. |\n"
            "| SHAP | Explanation framework discussed in the source for local and global feature contributions. |\n"
            "| Permutation importance | Importance estimate based on model-performance degradation when feature information is disrupted. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. What is the core feedback idea behind CI/CD?\n"
            "2. What does packaging an ML model into a container actually include?\n"
            "3. Why does containerization improve sharing and debugging?\n"
            "4. What components exist in the chapter's ONNX + Flask example?\n"
            "5. Why should you test both local Python execution and container execution?\n"
            "6. Why should a deployable image be reproducible from version-controlled instructions?\n"
            "7. Why are large model binaries awkward to manage in ordinary Git repositories?\n"
            "8. What are the main stages in the source's GitHub Actions packaging workflow?\n"
            "9. Why should CI/CD credentials live in secrets rather than source files?\n"
            "10. What is a greedy pipeline step?\n"
            "11. Why do smaller pipeline steps improve debugging?\n"
            "12. What is the purpose of a container registry?\n"
            "13. How does an ML-specific cloud pipeline differ from a generic CI/CD runner?\n"
            "14. Which steps might appear in a training-and-registration pipeline?\n"
            "15. What is the difference between blue-green and canary deployment?\n"
            "16. What is rollback?\n"
            "17. Why must canary health include software-service metrics?\n"
            "18. What layers of a prediction HTTP request should be tested?\n"
            "19. Why is a boolean/string response mismatch dangerous even if the model is accurate?\n"
            "20. What is shift-left validation?\n"
            "21. How does continuous improvement connect Chapter 4 to Chapter 5?\n"
            "22. How does the source define AutoML?\n"
            "23. How does KaizenML differ from AutoML?\n"
            "24. Why does the chapter argue that modeling automation is only one part of MLOps?\n"
            "25. What does a data-centric improvement mindset add to model-centric development?\n"
            "26. What two feature-store capabilities are emphasized in the source?\n"
            "27. How is a feature store different from a general data warehouse in the chapter's framing?\n"
            "28. What three Apple ML workflows are described?\n"
            "29. When can reusing a pretrained model be more efficient than training one?\n"
            "30. What steps make up the high-level Google AutoML workflow?\n"
            "31. What two Azure AutoML access patterns are discussed?\n"
            "32. Why is SageMaker Autopilot an example of AutoML embedded in a larger MLOps platform?\n"
            "33. What problem do Ludwig and FLAML try to simplify?\n"
            "34. Which important choices remain human responsibilities even with AutoML?\n"
            "35. Why does the source consider explainability part of MLOps automation?\n"
            "36. What is the difference between a local SHAP explanation and a global feature summary?\n"
            "37. What does permutation importance measure?\n"
            "38. Why can two different models assign different importance to the same feature?\n"
            "39. How do continuous delivery and AutoML form one end-to-end automation loop?\n"
            "40. Which repetitive tasks in your own ML workflow would you automate first, and why?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Reliable MLOps is not one automation tool. Continuous delivery makes model releases repeatable and testable; "
            "AutoML reduces repetitive modeling work; KaizenML connects them into a culture of continuously improving data, "
            "features, software, models, deployment, explanations, and production feedback.**\n"
        ),
        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "feedback-first", "title": "Continuous delivery begins with continuous evaluation", "order": 1},
            {"id": "package-model", "title": "Packaging an ML model means packaging the environment around it", "order": 2},
            {"id": "onnx-flask-example", "title": "Example: ONNX model behind a Flask prediction endpoint", "order": 3},
            {"id": "docker-build-test", "title": "Test locally before automating delivery", "order": 4},
            {"id": "iac-cd", "title": "Infrastructure as code makes model delivery reproducible", "order": 5},
            {"id": "model-binaries", "title": "Keep large model artifacts separate from ordinary source control", "order": 6},
            {"id": "github-actions-flow", "title": "Automate model packaging with a CI/CD workflow", "order": 7},
            {"id": "small-steps", "title": "Small CI/CD steps create smaller failure domains", "order": 8},
            {"id": "secrets-registry", "title": "Secrets and registries complete the delivery path", "order": 9},
            {"id": "cloud-pipelines", "title": "Cloud ML pipelines organize multi-step model workflows", "order": 10},
            {"id": "generic-vs-ml-pipeline", "title": "Generic CI/CD and ML-specific pipeline systems solve overlapping problems", "order": 11},
            {"id": "blue-green", "title": "Blue-green deployment: prepare the full replacement before switching traffic", "order": 12},
            {"id": "canary", "title": "Canary deployment: increase traffic only while the candidate remains healthy", "order": 13},
            {"id": "test-service-contract", "title": "Test every layer of the prediction service contract", "order": 14},
            {"id": "automated-checks", "title": "Automated checks belong inside the pipeline", "order": 15},
            {"id": "shift-left", "title": "Shift left: find problems when they are cheapest to fix", "order": 16},
            {"id": "chapter4-kaizen", "title": "Continuous delivery naturally leads to continuous improvement", "order": 17},
            {"id": "automl-definition", "title": "AutoML automates model creation from prepared data", "order": 18},
            {"id": "kaizenml-definition", "title": "KaizenML automates and improves the whole ML system", "order": 19},
            {"id": "automation-execution", "title": "Automation should move effort from repetitive mechanics toward execution", "order": 20},
            {"id": "data-centric-kaizen", "title": "KaizenML treats data, software, and models as equal improvement targets", "order": 21},
            {"id": "feature-stores", "title": "Feature stores are one KaizenML mechanism", "order": 22},
            {"id": "apple-ecosystem", "title": "Apple ecosystem: AutoML plus on-device deployment", "order": 23},
            {"id": "pretrained-models", "title": "Sometimes the best automation is not training at all", "order": 24},
            {"id": "google-automl", "title": "Google AutoML: high-level training connected to cloud and edge deployment", "order": 25},
            {"id": "azure-automl", "title": "Azure AutoML: GUI and programmatic automation", "order": 26},
            {"id": "aws-autopilot", "title": "SageMaker Autopilot: AutoML inside a broader ML platform", "order": 27},
            {"id": "open-source-automl", "title": "Open-source AutoML lowers the cost of automation", "order": 28},
            {"id": "automl-constraints", "title": "AutoML still needs human constraints and judgment", "order": 29},
            {"id": "explainability", "title": "Explainability should be automated alongside modeling", "order": 30},
            {"id": "shap", "title": "SHAP: explain how features push a prediction", "order": 31},
            {"id": "permutation-importance", "title": "Permutation importance: measure performance loss when a feature is disrupted", "order": 32},
            {"id": "one-automation-story", "title": "Continuous delivery and AutoML are one automation story", "order": 33},
            {"id": "automation-priorities", "title": "What should be automated first?", "order": 34},
        ],
    },

    "exercises": [
        {
            "id": "M11.L01.EX01",
            "title": "Package and verify a prediction service",
            "lesson_code": "M11.L01",
            "section_id": "docker-build-test",
            "placement": "after_section",
            "description": "Design the minimum reproducible containerized prediction service from source-supported components.",
            "instructions": (
                "You have a serialized model, preprocessing code, a Flask prediction route, and a requirements file.\n\n"
                "1. List what the container must contain.\n"
                "2. Write the high-level Docker build/run sequence.\n"
                "3. Define one valid request and expected response schema.\n"
                "4. Explain why you test outside the container first and then test again inside it.\n"
                "5. Identify two packaging failures that would not be revealed by offline model accuracy."
            ),
            "expected_output": "A reproducible packaging checklist plus an API-contract test plan.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["model-packaging", "containers", "prediction-api", "integration-testing"],
        },

        {
            "id": "M11.L01.EX02",
            "title": "Design an ML delivery pipeline",
            "lesson_code": "M11.L01",
            "section_id": "generic-vs-ml-pipeline",
            "placement": "after_section",
            "description": "Separate CI/CD responsibilities into clear, debuggable steps.",
            "instructions": (
                ('1. Design a pipeline that starts with source code and a registered model and ends with a published image.\n'
                 '2. Include steps for:\n'
                 '   - source checkout,\n'
                 '   - cloud/model-registry authentication,\n'
                 '   - model retrieval,\n'
                 '   - container build,\n'
                 '   - functional tests,\n'
                 '   - linting,\n'
                 '   - registry authentication,\n'
                 '   - publishing.\n'
                 '3. Then explain which parts fit a generic CI/CD tool and which might benefit from an ML-specific pipeline service.')
            ),
            "expected_output": "A step-by-step pipeline with small failure domains and tool-selection reasoning.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["ci-cd", "infrastructure-as-code", "pipeline-design", "model-registry"],
        },

        {
            "id": "M11.L01.EX03",
            "title": "Create a safe rollout and rollback plan",
            "lesson_code": "M11.L01",
            "section_id": "shift-left",
            "placement": "after_section",
            "description": "Combine pre-release tests with controlled production rollout.",
            "instructions": (
                "A candidate model has higher offline accuracy than production, but it also uses a newly upgraded runtime dependency.\n\n"
                "1. Choose blue-green or canary rollout and justify your choice.\n"
                "2. Define at least four health checks before increasing traffic.\n"
                "3. Define a rollback condition.\n"
                "4. Add three automated checks that should run earlier in CI so the rollout is less likely to fail.\n"
                "5. Explain how this demonstrates shift-left thinking."
            ),
            "expected_output": "A risk-controlled deployment plan that includes software health, model health, and rollback.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["canary-deployment", "blue-green-deployment", "rollback", "shift-left"],
        },

        {
            "id": "M11.L01.EX04",
            "title": "Place AutoML inside a KaizenML system",
            "lesson_code": "M11.L01",
            "section_id": "feature-stores",
            "placement": "after_section",
            "description": "Distinguish modeling automation from system-wide continuous improvement.",
            "instructions": (
                "You are building a churn system with repeated data cleaning, shared features, manual hyperparameter search, "
                "manual deployment, and no automated explanation reports.\n\n"
                "Classify each improvement as primarily AutoML, feature-store/data automation, CI/CD, explainability, or broader KaizenML:\n"
                "1. automate algorithm and hyperparameter search,\n"
                "2. register reusable customer features,\n"
                "3. automatically package and deploy approved models,\n"
                "4. generate feature-importance reports,\n"
                "5. continuously improve all of these components together.\n\n"
                "Explain why AutoML alone would leave major manual bottlenecks."
            ),
            "expected_output": "A correct mapping of automation responsibilities and a system-level KaizenML explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["automl", "kaizenml", "feature-store", "continuous-delivery"],
        },

        {
            "id": "M11.L01.EX05",
            "title": "Choose an AutoML path",
            "lesson_code": "M11.L01",
            "section_id": "open-source-automl",
            "placement": "after_section",
            "description": "Select between managed, open-source, and pretrained-model workflows.",
            "instructions": (
                "Choose a sensible path for each scenario based only on patterns discussed in the lesson:\n\n"
                "1. An iOS developer wants a simple on-device image classifier with minimal code.\n"
                "2. A cloud team wants managed automated training and later hosted deployment.\n"
                "3. A Python team wants open-source cost-aware automated model selection.\n"
                "4. A team already has access to a strong pretrained vision model and mostly needs deployment conversion.\n"
                "5. A team wants an open-source high-level framework driven by dataset + configuration.\n\n"
                "Name an example source tool/workflow for each and explain the reasoning."
            ),
            "expected_output": "Five tool/workflow choices grounded in the source's Apple, cloud, FLAML, pretrained, and Ludwig examples.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["automl-tools", "pretrained-models", "managed-ml", "open-source-automl"],
        },

        {
            "id": "M11.L01.EX06",
            "title": "Explain an automated model",
            "lesson_code": "M11.L01",
            "section_id": "permutation-importance",
            "placement": "after_section",
            "description": "Reason about local explanation and global feature importance.",
            "instructions": (
                "An AutoML system selects a strong tree model.\n\n"
                "1. Explain what a local SHAP-style explanation tries to show for one prediction.\n"
                "2. Explain what a global SHAP-style summary tries to show across many predictions.\n"
                "3. Explain permutation importance in plain language.\n"
                "4. Explain why two model families may produce different feature-importance rankings.\n"
                "5. State one way explanation reports could be incorporated into an MLOps pipeline."
            ),
            "expected_output": "A comparison of local/global explanations and permutation importance without treating importance as causal truth.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["explainability", "shap", "permutation-importance", "mlops-reporting"],
        },

        {
            "id": "M11.L01.EX07",
            "title": "Build a KaizenML improvement backlog",
            "lesson_code": "M11.L01",
            "section_id": "automation-priorities",
            "placement": "after_section",
            "description": "Prioritize automation by recurring friction and failure risk.",
            "instructions": (
                ('1. A team currently does the following manually:\n'
                 '   - copies model files into Docker build folders,\n'
                 '   - runs one curl request by hand,\n'
                 '   - emails another team for release approval,\n'
                 '   - recreates the same features in three projects,\n'
                 '   - manually tries ten model configurations,\n'
                 '   - creates explainability plots only after incidents.\n'
                 '2. Prioritize these six problems from first to last for automation. There is no single correct ordering, but every choice must be justified using failure risk, repetition, debugging cost, and production value.')
            ),
            "expected_output": "A prioritized continuous-improvement backlog with explicit reasoning.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["kaizenml", "automation-prioritization", "continuous-improvement", "systems-thinking"],
        },
    ],

    "quiz": {
        "id": "M11.L01.QZ01",
        "title": "Continuous Delivery, AutoML, and KaizenML — Knowledge Check",
        "lesson_code": "M11.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M11.L01.Q01",
                "section_id": "feedback-first",
                "question": "What is the central role of feedback in CI/CD as framed by the source?",
                "options": [
                    "It replaces testing.",
                    "It lets teams continuously evaluate, adapt, and improve the release process.",
                    "It guarantees no release will fail.",
                    "It only measures model accuracy.",
                ],
                "correct": 1,
                "explanation": "Continuous evaluation and process improvement are core themes of the chapter.",
            },
            {
                "id": "M11.L01.Q02",
                "section_id": "package-model",
                "question": "What does model packaging mean in the source?",
                "options": [
                    "Saving only model weights.",
                    "Putting the model into a container with the software environment needed to serve it.",
                    "Compressing the model into ZIP format.",
                    "Uploading source code to Git.",
                ],
                "correct": 1,
                "explanation": "The chapter treats containerization as the mechanism for packaging models for sharing and deployment.",
            },
            {
                "id": "M11.L01.Q03",
                "section_id": "docker-build-test",
                "question": "Why should the service be tested again after it is containerized?",
                "options": [
                    "Container packaging can introduce missing-file, path, dependency, and port errors.",
                    "The model changes its labels automatically.",
                    "Containers cannot run HTTP services.",
                    "Local testing has no value.",
                ],
                "correct": 0,
                "explanation": "The container is a separate executable environment with its own possible integration failures.",
            },
            {
                "id": "M11.L01.Q04",
                "section_id": "model-binaries",
                "question": "Why does the source avoid keeping the large ONNX model directly in the Git repository?",
                "options": [
                    "Git is intended primarily for source history, and hosted repositories may impose large binary-file limits.",
                    "ONNX cannot be versioned anywhere.",
                    "Model files contain no useful information.",
                    "Containers cannot copy model files.",
                ],
                "correct": 0,
                "explanation": "The model is retrieved from an ML platform/registry during the build instead.",
            },
            {
                "id": "M11.L01.Q05",
                "section_id": "github-actions-flow",
                "question": "Which workflow ordering is most consistent with the source?",
                "options": [
                    "Publish → retrieve model → test → checkout",
                    "Checkout → authenticate → retrieve model → build → publish",
                    "Deploy → train → delete source",
                    "Only build; no other automation is needed",
                ],
                "correct": 1,
                "explanation": "The source decomposes delivery into explicit source, authentication, retrieval, build, and publish steps.",
            },
            {
                "id": "M11.L01.Q06",
                "section_id": "small-steps",
                "question": "Why should a CI/CD pipeline avoid greedy steps?",
                "options": [
                    "Small steps make failures easier to localize and understand.",
                    "Cloud systems forbid multi-command steps.",
                    "Small steps guarantee free compute.",
                    "Greedy steps reduce security automatically.",
                ],
                "correct": 0,
                "explanation": "Single-responsibility steps create smaller and clearer failure domains.",
            },
            {
                "id": "M11.L01.Q07",
                "section_id": "secrets-registry",
                "question": "Where should cloud and registry credentials be placed?",
                "options": [
                    "Hard-coded into the public YAML file",
                    "Stored as CI/CD secrets and referenced by the workflow",
                    "Inside the model weights",
                    "Inside the API response",
                ],
                "correct": 1,
                "explanation": "The source demonstrates repository secrets for cloud and registry authentication.",
            },
            {
                "id": "M11.L01.Q08",
                "section_id": "cloud-pipelines",
                "question": "Which step can legitimately appear in an ML pipeline?",
                "options": [
                    "Data preprocessing",
                    "Model training",
                    "Evaluation",
                    "All of the above",
                ],
                "correct": 3,
                "explanation": "The source explicitly treats pipeline elements as composable based on the workflow's real needs.",
            },
            {
                "id": "M11.L01.Q09",
                "section_id": "generic-vs-ml-pipeline",
                "question": "Why can an ML-specific pipeline platform be useful compared with a generic CI/CD service?",
                "options": [
                    "It can offer model-oriented steps and specialized training resources directly.",
                    "Generic CI/CD cannot execute any code.",
                    "ML pipelines never need tests.",
                    "Only ML pipelines can use YAML.",
                ],
                "correct": 0,
                "explanation": "The source points to data/training/registry abstractions and specialized compute as ML-specific advantages.",
            },
            {
                "id": "M11.L01.Q10",
                "section_id": "blue-green",
                "question": "What is the defining idea of blue-green deployment?",
                "options": [
                    "Train two models on blue and green datasets.",
                    "Prepare a separate new version, verify it, then switch traffic from the old version.",
                    "Send random traffic to every historical model forever.",
                    "Never use staging.",
                ],
                "correct": 1,
                "explanation": "Blue-green isolates the candidate before cutover.",
            },
            {
                "id": "M11.L01.Q11",
                "section_id": "canary",
                "question": "What is the defining idea of a canary deployment?",
                "options": [
                    "Gradually expose a candidate to a fraction of production traffic while monitoring health.",
                    "Delete the previous model immediately.",
                    "Use only offline data.",
                    "Deploy without rollback capability.",
                ],
                "correct": 0,
                "explanation": "The chapter's example progressively routes traffic and rolls back if health degrades.",
            },
            {
                "id": "M11.L01.Q12",
                "section_id": "test-service-contract",
                "question": "Why is `{ \"positive\": \"false\" }` potentially a serious service bug?",
                "options": [
                    "It uses a string instead of the expected boolean type.",
                    "JSON does not permit keys.",
                    "The endpoint cannot return negative sentiment.",
                    "Strings are always faster than booleans.",
                ],
                "correct": 0,
                "explanation": "A schema/type mismatch can break downstream clients without obvious HTTP failures.",
            },
            {
                "id": "M11.L01.Q13",
                "section_id": "shift-left",
                "question": "What does shift-left mean in this lesson?",
                "options": [
                    "Move error detection earlier in the delivery lifecycle.",
                    "Send more traffic to the leftmost model.",
                    "Use only local development.",
                    "Delay testing until after production.",
                ],
                "correct": 0,
                "explanation": "Earlier detection is generally cheaper and faster to fix.",
            },
            {
                "id": "M11.L01.Q14",
                "section_id": "automl-definition",
                "question": "How does the source define AutoML?",
                "options": [
                    "Automation of tasks related to training a model on clean data.",
                    "Full automation of every business decision.",
                    "Only automated data labeling.",
                    "Only container deployment.",
                ],
                "correct": 0,
                "explanation": "The chapter uses a relatively narrow modeling-focused definition.",
            },
            {
                "id": "M11.L01.Q15",
                "section_id": "kaizenml-definition",
                "question": "How is KaizenML broader than AutoML?",
                "options": [
                    "It includes continuous improvement of data, software, models, deployment, and feedback.",
                    "It only changes the learning rate.",
                    "It excludes automation.",
                    "It is another name for one AutoML library.",
                ],
                "correct": 0,
                "explanation": "KaizenML is the source's system-wide continuous-improvement idea.",
            },
            {
                "id": "M11.L01.Q16",
                "section_id": "data-centric-kaizen",
                "question": "Which set best reflects KaizenML's improvement targets?",
                "options": [
                    "Only model architecture",
                    "Data quality, software quality, model quality, and feedback-loop quality",
                    "Only GPU utilization",
                    "Only feature count",
                ],
                "correct": 1,
                "explanation": "The source explicitly expands improvement beyond the model itself.",
            },
            {
                "id": "M11.L01.Q17",
                "section_id": "feature-stores",
                "question": "Which feature-store capability is emphasized in the source?",
                "options": [
                    "Sharing features so they are easier to reuse in training and prediction",
                    "Replacing every database",
                    "Running only model explanations",
                    "Deleting all raw data",
                ],
                "correct": 0,
                "explanation": "Feature sharing/reuse is one of the source's central feature-store functions.",
            },
            {
                "id": "M11.L01.Q18",
                "section_id": "pretrained-models",
                "question": "What systems lesson comes from the Core ML conversion example?",
                "options": [
                    "A strong pretrained model may sometimes be more efficient than training a new model from scratch.",
                    "Every model must be trained on-device.",
                    "Converted models cannot be deployed.",
                    "Pretrained models are incompatible with MLOps.",
                ],
                "correct": 0,
                "explanation": "The source explicitly argues that model reuse can be easier than new training in some cases.",
            },
            {
                "id": "M11.L01.Q19",
                "section_id": "google-automl",
                "question": "What is one advantage of an integrated managed AutoML platform?",
                "options": [
                    "It can connect prepared data, automated training, evaluation, and deployment/export in one workflow.",
                    "It eliminates the need to inspect data.",
                    "It guarantees the model is correct.",
                    "It cannot deploy to edge devices.",
                ],
                "correct": 0,
                "explanation": "The source presents an integrated path from uploaded data to hosted or edge deployment.",
            },
            {
                "id": "M11.L01.Q20",
                "section_id": "azure-automl",
                "question": "Which two Azure AutoML access styles are discussed?",
                "options": [
                    "GUI and Python SDK",
                    "Only shell scripts and C++",
                    "Only mobile and browser",
                    "Only Docker and Kubernetes",
                ],
                "correct": 0,
                "explanation": "The chapter presents both Azure ML Studio and programmatic access.",
            },
            {
                "id": "M11.L01.Q21",
                "section_id": "aws-autopilot",
                "question": "What happens after a SageMaker Autopilot experiment finishes in the source example?",
                "options": [
                    "Candidate models can be inspected and a selected model can be deployed.",
                    "All models are automatically deleted.",
                    "The data must be relabeled manually before any metrics are shown.",
                    "The system cannot expose explainability information.",
                ],
                "correct": 0,
                "explanation": "The example includes candidate comparison, metrics/explainability, and deployment.",
            },
            {
                "id": "M11.L01.Q22",
                "section_id": "open-source-automl",
                "question": "What does the minimal FLAML example demonstrate?",
                "options": [
                    "Automated model selection can be invoked through a small amount of Python code.",
                    "AutoML requires a graphical user interface.",
                    "FLAML is a container registry.",
                    "FLAML only performs model deployment.",
                ],
                "correct": 0,
                "explanation": "The source highlights a compact API for automated model selection/tuning.",
            },
            {
                "id": "M11.L01.Q23",
                "section_id": "automl-constraints",
                "question": "Which responsibility still belongs to humans even when AutoML is used?",
                "options": [
                    "Defining the problem and deciding whether the chosen metric and result are useful",
                    "None; AutoML decides the business objective automatically",
                    "Only naming the model file",
                    "Only choosing the container color",
                ],
                "correct": 0,
                "explanation": "Automated optimization still depends on human framing and judgment.",
            },
            {
                "id": "M11.L01.Q24",
                "section_id": "explainability",
                "question": "Why does the source treat explainability as an MLOps capability?",
                "options": [
                    "It helps teams inspect model behavior as part of operational workflows.",
                    "It replaces all software monitoring.",
                    "It guarantees causality.",
                    "It is only useful before training.",
                ],
                "correct": 0,
                "explanation": "Explanation reports can be operationalized alongside other model and system signals.",
            },
            {
                "id": "M11.L01.Q25",
                "section_id": "shap",
                "question": "What does a local SHAP-style explanation focus on?",
                "options": [
                    "Feature contributions to one prediction",
                    "Container build time",
                    "All historical Git commits",
                    "Only training-data size",
                ],
                "correct": 0,
                "explanation": "The source's force-plot example explains one model output using feature contributions.",
            },
            {
                "id": "M11.L01.Q26",
                "section_id": "permutation-importance",
                "question": "What is the core idea behind permutation importance?",
                "options": [
                    "Measure performance degradation when information from a feature is disrupted.",
                    "Sort features alphabetically.",
                    "Measure container size.",
                    "Train one model per feature automatically.",
                ],
                "correct": 0,
                "explanation": "The source describes importance through change in accuracy when feature information is disturbed.",
            },
            {
                "id": "M11.L01.Q27",
                "section_id": "one-automation-story",
                "question": "Which sequence best captures the combined lesson?",
                "options": [
                    "Data/features → automated model creation → evaluation → packaging/tests → controlled deployment → feedback",
                    "Deployment → delete data → no evaluation",
                    "Manual tuning only → manual release only",
                    "Feature store → no model → no production",
                ],
                "correct": 0,
                "explanation": "The two source chapters combine naturally into one end-to-end automation loop.",
            },
            {
                "id": "M11.L01.Q28",
                "section_id": "automation-priorities",
                "question": "What type of task is a strong candidate for early automation?",
                "options": [
                    "A repetitive manual step that frequently causes release errors",
                    "A one-time creative decision with no repetition",
                    "Every task regardless of cost",
                    "Only hyperparameter tuning",
                ],
                "correct": 0,
                "explanation": "The sources repeatedly emphasize automating recurring friction and failure points.",
            },
            {
                "id": "M11.L01.Q29",
                "section_id": "chapter4-kaizen",
                "question": "What should a team do after discovering a costly release failure?",
                "options": [
                    "Improve the process so the same class of failure is detected earlier next time.",
                    "Avoid documenting it.",
                    "Add more manual email approvals only.",
                    "Stop using tests.",
                ],
                "correct": 0,
                "explanation": "Continuous improvement means converting failures into stronger automated process controls.",
            },
            {
                "id": "M11.L01.Q30",
                "section_id": "one-automation-story",
                "type": "open",
                "question": (
                    "Design an end-to-end KaizenML workflow for a classification system. Include reusable features, "
                    "AutoML or automated model search, explanation/evaluation checks, a model registry, container packaging, "
                    "CI/CD tests, one controlled rollout strategy, production feedback, and one rule for improving the pipeline "
                    "after a failure."
                ),
            },
        ],
        "passing_score": 70,
    },
}
