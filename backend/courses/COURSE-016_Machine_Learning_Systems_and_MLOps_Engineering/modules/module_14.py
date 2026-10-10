"""M13.L01 — MLOps for AWS.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 7, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M13.L01"

MODULE_ORDER = 13

MODULE_TITLE = "MLOps for AWS"

MODULE_DESCRIPTION = (
    "Learn how to build and operate practical MLOps systems on AWS by choosing "
    "the right service abstraction, using managed AI APIs, serverless functions, "
    "containers, continuous delivery, reusable ML project scaffolding, CLI and "
    "Flask interfaces, AWS SAM, and service patterns matched to organizational needs."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "MLOps for AWS",

    "slug": "practical-mlops-m13-l01-aws",

    "description": (
        "A practical AWS MLOps lesson covering service abstraction levels, managed AI "
        "services, S3 and CodeBuild, Cloud9, AWS Lambda and Step Functions, Fargate, "
        "ECR, App Runner, Elastic Beanstalk, reusable MLOps project structure, CLI and "
        "Flask interfaces, GitHub Actions, AWS SAM, deployment patterns, business metrics, "
        "automation, monitoring, security, and service-selection strategy."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 6.5,

    "skill_tags": [
        "aws",
        "mlops",
        "cloud-ml",
        "managed-ai-services",
        "amazon-comprehend",
        "amazon-s3",
        "aws-codebuild",
        "aws-cloud9",
        "serverless",
        "aws-lambda",
        "aws-step-functions",
        "amazon-rekognition",
        "containers",
        "amazon-ecr",
        "aws-fargate",
        "aws-app-runner",
        "elastic-beanstalk",
        "continuous-delivery",
        "flask",
        "cli-tools",
        "click",
        "github-actions",
        "aws-sam",
        "api-gateway",
        "infrastructure-as-code",
        "sagemaker",
        "monitoring",
        "automation",
        "security",
        "product-metrics",
    ],

    "prerequisite_ids": ["M12.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "MLOps for AWS",

        "content": (
            "# MLOps for AWS\n"
            "\n"
            "> **Lesson:** M13.L01  \n"
            "> **Module:** MLOps for AWS  \n"
            "> **Source alignment:** Chapter 7. Page numbers were not included in the supplied source. "
            "The AWS interfaces and command examples in the chapter reflect the source's timeframe, and the source itself "
            "recommends checking current AWS documentation because cloud services change quickly. This lesson preserves the "
            "chapter's concepts and workflows rather than claiming that every historical command or UI remains unchanged.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the chapter's service-abstraction view of AWS.\n"
            "- Choose between high-level managed services and lower-level building blocks based on organizational maturity and opportunity cost.\n"
            "- Explain when a managed AI API such as Amazon Comprehend can be preferable to building a model from scratch.\n"
            "- Describe a simple S3 static-site continuous-delivery workflow.\n"
            "- Explain why cloud development environments can reduce environment mismatch.\n"
            "- Define serverless computing using the chapter's function-centered mental model.\n"
            "- Explain Lambda invocation through manual calls, schedules, and events.\n"
            "- Describe an event-driven S3-to-Rekognition Lambda workflow.\n"
            "- Explain how AWS Step Functions compose multiple Lambda functions.\n"
            "- Explain the value of container-as-a-service for MLOps.\n"
            "- Describe the role of ECR, Fargate, and App Runner in containerized deployment.\n"
            "- Explain the chapter's computer-vision prototyping pattern with DeepLens and MQTT.\n"
            "- Explain why operationalizing a reasonable model can be more valuable than indefinitely optimizing offline accuracy.\n"
            "- Describe a continuous-delivery workflow using Cloud9, source control, CodeBuild, and Elastic Beanstalk.\n"
            "- Identify the reusable artifacts in the chapter's MLOps Cookbook project.\n"
            "- Explain why command-line interfaces are useful MLOps tools.\n"
            "- Explain the separation between ML library logic, CLI interfaces, and web-service interfaces.\n"
            "- Containerize and locally test a Flask ML microservice conceptually.\n"
            "- Explain automated container build and registry publishing with GitHub Actions.\n"
            "- Describe how App Runner simplifies source-to-service deployment.\n"
            "- Explain the role of AWS SAM in serverless development and deployment.\n"
            "- Distinguish direct Lambda invocation from API Gateway invocation payloads.\n"
            "- Explain how SAM templates act as infrastructure as code.\n"
            "- Match App Runner/CaaS, SageMaker, and Lambda + AI APIs to different organizational patterns described by the source.\n"
            "- Connect product metrics and recommendation quality in the sports-social-network case study.\n"
            "- Explain why MLOps should inherit software-engineering practices such as versioning, testing, automation, documentation, monitoring, and security.\n"
            "- Explain why understanding the business problem should guide cloud-service and model decisions.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. AWS MLOps is about choosing from many levels of abstraction\n"
            "\n"
            "The chapter presents AWS as a very large platform with many ways to solve the same broad problem.\n"
            "\n"
            "Because the platform is too large to cover completely, the chapter focuses on practical patterns and relatively high-level services such as:\n"
            "\n"
            "- AWS Lambda,\n"
            "- AWS App Runner,\n"
            "- container services,\n"
            "- managed AI APIs,\n"
            "- continuous-delivery services.\n"
            "\n"
            "More comprehensive platforms such as SageMaker appear as one part of the wider AWS MLOps landscape rather than the only possible starting point.\n"
            "\n"
            "The main lesson is:\n"
            "\n"
            "> **AWS gives you many abstraction levels. Your job is to choose the level that fits the problem, team, and stage of the organization.**\n"
            "\n"
            "[[IMAGE_NEEDED: AWS MLOps abstraction ladder | "
            "A ladder from raw infrastructure/building blocks through containers and serverless to managed AI APIs and full ML platforms | "
            "Learner should notice that higher levels remove more operational work while lower levels provide more control]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. The chapter's Costco analogy: raw ingredients versus prepared services\n"
            "\n"
            "The source compares AWS to a wholesale store with different preparation levels.\n"
            "\n"
            "One customer may buy a prepared meal because speed and convenience matter most.\n"
            "\n"
            "Another may buy raw ingredients because they have the staff and expertise to create something more customized.\n"
            "\n"
            "The AWS version of this trade-off is:\n"
            "\n"
            "```text\n"
            "More managed service\n"
            "    ↑ less operational work\n"
            "    ↑ faster start\n"
            "    ↑ usually less low-level control\n"
            "\n"
            "More raw infrastructure\n"
            "    ↑ more customization\n"
            "    ↑ more engineering responsibility\n"
            "```\n"
            "\n"
            "The source also invokes **comparative advantage**: do not compare only the direct vendor price with the cost of doing a task yourself. "
            "Compare the opportunity cost of spending your own people and time recreating infrastructure instead of building customer value.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Managed AI APIs can provide a fast first solution\n"
            "\n"
            "The chapter uses Amazon Comprehend as a high-level NLP example.\n"
            "\n"
            "Capabilities named in the source include:\n"
            "\n"
            "- entity detection,\n"
            "- key phrase detection,\n"
            "- personally identifiable information detection,\n"
            "- language detection,\n"
            "- sentiment analysis.\n"
            "\n"
            "Instead of hiring a team and spending months building a custom NLP stack, an organization may first use a managed API.\n"
            "\n"
            "This is especially attractive when the capability is useful to the product but not the company's core differentiator.\n"
            "\n"
            "The correct question is not simply:\n"
            "\n"
            "> Which option has the lower sticker price?\n"
            "\n"
            "It is:\n"
            "\n"
            "> Which option lets the organization create useful customer value with the best total trade-off in time, engineering effort, control, and cost?\n"
            "\n"
            "{{exercise:M13.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Learn continuous delivery first with a simple S3-hosted project\n"
            "\n"
            "Before deploying machine-learning services, the chapter demonstrates a simpler continuous-delivery project: a Hugo static website hosted on S3.\n"
            "\n"
            "The repository is treated as the source of truth and contains text-based project artifacts such as:\n"
            "\n"
            "- Markdown content,\n"
            "- templates,\n"
            "- build instructions.\n"
            "\n"
            "The build flow is conceptually:\n"
            "\n"
            "```text\n"
            "Source repository\n"
            "      ↓\n"
            "AWS build service\n"
            "      ↓\n"
            "Install Hugo\n"
            "      ↓\n"
            "Generate static files\n"
            "      ↓\n"
            "Sync output to S3\n"
            "      ↓\n"
            "Hosted website\n"
            "```\n"
            "\n"
            "The educational point is more important than Hugo itself: first understand the mechanics of automated build and deployment on a small system.\n"
            "\n"
            "[[IMAGE_NEEDED: Simple S3 continuous-delivery pipeline | "
            "Source repository flowing to an automated build step, static-site generation, and S3 website deployment | "
            "Learner should notice the source-of-truth and repeatable-deployment pattern]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. A build configuration is an executable recipe\n"
            "\n"
            "The source's `buildspec.yml` installs the build tool, generates the site, and synchronizes output to S3.\n"
            "\n"
            "A simplified structure is:\n"
            "\n"
            "```yaml\n"
            "phases:\n"
            "  install:\n"
            "    commands:\n"
            "      - install build tool\n"
            "  build:\n"
            "    commands:\n"
            "      - generate output\n"
            "  post_build:\n"
            "    commands:\n"
            "      - sync output to deployment target\n"
            "```\n"
            "\n"
            "This is infrastructure/process knowledge captured as code.\n"
            "\n"
            "Anyone who can access the repository can inspect the recipe rather than depending on one person's memory.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Cloud development environments reduce distance between development and deployment\n"
            "\n"
            "The chapter favors AWS Cloud9 because development happens close to the cloud resources being used.\n"
            "\n"
            "The workflow becomes:\n"
            "\n"
            "```text\n"
            "Check out source in cloud environment\n"
            "      ↓\n"
            "Run/test using cloud-connected tools\n"
            "      ↓\n"
            "Use the same cloud ecosystem for deployment\n"
            "```\n"
            "\n"
            "This can make it easier to test permissions, service integrations, and deployment commands in an environment that resembles the target platform.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Serverless starts with the function as the unit of work\n"
            "\n"
            "The chapter explains serverless using a function-centered mental model.\n"
            "\n"
            "A Python function performs a task when given input.\n"
            "\n"
            "Serverless provides the execution environment without requiring the developer to manage the underlying server directly.\n"
            "\n"
            "```text\n"
            "Event / request\n"
            "      ↓\n"
            "Function\n"
            "      ↓\n"
            "Result / side effect\n"
            "```\n"
            "\n"
            "The phrase 'serverless' does not mean physical servers cease to exist. It means server management is abstracted away from the developer's main workflow.\n"
            "\n"
            "[[IMAGE_NEEDED: Serverless function mental model | "
            "Events from API, schedule, and S3 all invoking a cloud function, with server infrastructure hidden beneath the function abstraction | "
            "Learner should notice that serverless removes server-management responsibility rather than physical servers]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Lambda functions can react to many types of triggers\n"
            "\n"
            "The source uses a simple Marco/Polo function to show the Lambda programming model.\n"
            "\n"
            "A simplified handler is:\n"
            "\n"
            "```python\n"
            "def lambda_handler(event, context):\n"
            "    if event[\"name\"] == \"Marco\":\n"
            "        return \"Polo\"\n"
            "    return \"No!\"\n"
            "```\n"
            "\n"
            "The same function can conceptually be triggered by:\n"
            "\n"
            "- manual invocation,\n"
            "- command line or SDK calls,\n"
            "- scheduled events,\n"
            "- service events such as a new S3 object.\n"
            "\n"
            "This event-driven model is valuable for MLOps because data and model workflows naturally contain many events.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Event-driven ML example: S3 upload → Lambda → image labels\n"
            "\n"
            "The chapter gives a computer-vision example where an image arriving in S3 triggers a Lambda function.\n"
            "\n"
            "The function extracts the bucket and object key, calls Amazon Rekognition, and returns detected labels.\n"
            "\n"
            "```text\n"
            "Image uploaded to S3\n"
            "      ↓ event\n"
            "Lambda handler\n"
            "      ↓\n"
            "Read bucket + key\n"
            "      ↓\n"
            "Call Rekognition\n"
            "      ↓\n"
            "Return / process labels\n"
            "```\n"
            "\n"
            "The lesson is architectural: managed event sources and managed AI APIs can be composed into useful ML systems with very little custom infrastructure.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Step Functions compose serverless tasks into workflows\n"
            "\n"
            "A single Lambda performs one task well.\n"
            "\n"
            "More complex workflows can require multiple functions in sequence.\n"
            "\n"
            "The source demonstrates a Step Functions state machine that executes one Lambda and then another before reaching a final state.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "State A / Lambda A\n"
            "       ↓\n"
            "State B / Lambda B\n"
            "       ↓\n"
            "Finish\n"
            "```\n"
            "\n"
            "This provides a managed orchestration layer for event-driven tasks.\n"
            "\n"
            "{{exercise:M13.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Container as a Service gives portability without managing the entire platform\n"
            "\n"
            "The chapter presents AWS Fargate as a container-as-a-service option.\n"
            "\n"
            "The developer packages the microservice into a container.\n"
            "\n"
            "The cloud platform then handles more of the deployment infrastructure.\n"
            "\n"
            "The source emphasizes several container benefits:\n"
            "\n"
            "- reproduce the production runtime locally,\n"
            "- distribute software through registries,\n"
            "- keep runtime/deployment information alongside project source,\n"
            "- deploy to managed container services.\n"
            "\n"
            "[[IMAGE_NEEDED: Container portability for AWS MLOps | "
            "One container image running locally, stored in ECR, then deployed to Fargate/App Runner or another target | "
            "Learner should notice that the same packaged runtime can move across environments]]\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Fargate workflow: build locally, publish to ECR, deploy as a service\n"
            "\n"
            "The chapter's Flask 'make change' example follows a practical sequence:\n"
            "\n"
            "1. set up the application environment,\n"
            "2. test the application locally,\n"
            "3. call it with an HTTP request,\n"
            "4. create an ECR repository,\n"
            "5. build the container,\n"
            "6. push the image,\n"
            "7. run the container locally,\n"
            "8. deploy to Fargate,\n"
            "9. test the public service.\n"
            "\n"
            "This is a strong MLOps pattern because the same service is tested before and after packaging and then deployed from a versioned image.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. App Runner trades control for simpler source-to-service deployment\n"
            "\n"
            "The source describes AWS App Runner as an even higher-level container/application service.\n"
            "\n"
            "It can deploy from source code or from an existing container image.\n"
            "\n"
            "A simple source-based setup needs information such as:\n"
            "\n"
            "- how to install dependencies,\n"
            "- how to start the app,\n"
            "- which port the service listens on.\n"
            "\n"
            "The platform handles much of the surrounding deployment complexity and exposes a secure service URL.\n"
            "\n"
            "The design trade-off is the same abstraction lesson from earlier: less low-level work in exchange for using a more opinionated managed service.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. High-level hardware and services can shorten the computer-vision feedback loop\n"
            "\n"
            "The chapter discusses AWS DeepLens as a rapid computer-vision prototyping device.\n"
            "\n"
            "The key value is not the specific hardware itself. It is that a difficult integration problem—capturing video, running vision logic, and sending results—can be packaged into a higher-level developer experience.\n"
            "\n"
            "The example separates a project stream with real-time annotation and sends detected-object information through MQTT, a publish-subscribe protocol.\n"
            "\n"
            "This illustrates the chapter's repeated preference for tools that reduce setup friction and let teams focus on the problem.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. In production, operations deserves equal status with accuracy and explainability\n"
            "\n"
            "The chapter asks readers to consider three constraints:\n"
            "\n"
            "- prediction accuracy,\n"
            "- explainability,\n"
            "- operations.\n"
            "\n"
            "Academic workflows often prioritize accuracy first.\n"
            "\n"
            "The source argues for taking operationalization seriously because a reasonable model that can be deployed, monitored, and improved may create more value than a slightly better model that never becomes a reliable service.\n"
            "\n"
            "This is closely connected to Kaizen/continuous improvement:\n"
            "\n"
            "```text\n"
            "Reasonable model\n"
            "      ↓\n"
            "Operationalize\n"
            "      ↓\n"
            "Measure\n"
            "      ↓\n"
            "Improve data/model/software\n"
            "      ↺\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Accuracy explainability operations triangle | "
            "A triangle with prediction accuracy, explainability, and operations at the corners, with continuous improvement in the center | "
            "Learner should notice that production success is a systems trade-off rather than accuracy alone]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Learn continuous delivery with a simple application before adding ML complexity\n"
            "\n"
            "The source demonstrates a Flask application continuously deployed to Elastic Beanstalk.\n"
            "\n"
            "The high-level path is:\n"
            "\n"
            "```text\n"
            "Cloud9 development\n"
            "      ↓\n"
            "Git repository\n"
            "      ↓ change\n"
            "AWS CodeBuild\n"
            "      ↓\n"
            "install + lint + tests/build\n"
            "      ↓\n"
            "Elastic Beanstalk deployment\n"
            "```\n"
            "\n"
            "The chapter explicitly recommends getting a hello-world continuous-deployment project working before attempting a more complex ML service.\n"
            "\n"
            "That isolates cloud/deployment learning from model-specific complexity.\n"
            "\n"
            "{{exercise:M13.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 17. A reusable MLOps cookbook separates concerns\n"
            "\n"
            "The chapter introduces an intentionally small ML project that predicts baseball-player height from weight.\n"
            "\n"
            "Its purpose is not model sophistication. Its purpose is reusable deployment structure.\n"
            "\n"
            "The project includes artifacts such as:\n"
            "\n"
            "- `Makefile` — repeatable commands/recipes,\n"
            "- `requirements.txt` — pinned dependencies,\n"
            "- `cli.py` — direct prediction interface,\n"
            "- `utilscli.py` — utility/retraining/remote-endpoint interface,\n"
            "- `app.py` — Flask prediction microservice,\n"
            "- `mlib.py` — shared model logic,\n"
            "- dataset/scaling data,\n"
            "- serialized model,\n"
            "- `Dockerfile`,\n"
            "- Jupyter notebook explaining model creation.\n"
            "\n"
            "The central architectural insight is **separation of concerns**: core ML logic should be reusable by several interfaces and deployment targets.\n"
            "\n"
            "[[IMAGE_NEEDED: MLOps cookbook project structure | "
            "A central mlib.py/model layer connected to CLI, utility CLI, Flask API, notebook, Dockerfile, requirements, and deployment targets | "
            "Learner should notice that interfaces reuse the same model logic rather than duplicating it]]\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Makefiles and pinned dependencies turn common actions into repeatable commands\n"
            "\n"
            "The chapter treats a Makefile as both a recipe collection and an execution interface.\n"
            "\n"
            "Typical commands can include:\n"
            "\n"
            "- install,\n"
            "- lint,\n"
            "- test,\n"
            "- build,\n"
            "- deploy.\n"
            "\n"
            "Pinned dependencies in `requirements.txt` reduce surprise from unexpected library-version changes.\n"
            "\n"
            "Together, these files make local and automated workflows easier to reproduce.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Put model behavior in a reusable library, not inside every interface\n"
            "\n"
            "The source's `mlib.py` handles the model-oriented work:\n"
            "\n"
            "- load the model,\n"
            "- load data,\n"
            "- retrain,\n"
            "- format/scale input,\n"
            "- run prediction,\n"
            "- inverse-transform outputs,\n"
            "- return human-readable results,\n"
            "- emit debug information.\n"
            "\n"
            "Then the CLI and Flask service call this shared library.\n"
            "\n"
            "This reduces duplicated preprocessing and prediction logic across interfaces.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. CLI tools are fast interfaces for testing and operating ML code\n"
            "\n"
            "The chapter uses the Click framework to expose model prediction from the terminal.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```bash\n"
            "./cli.py --weight 180\n"
            "```\n"
            "\n"
            "The CLI calls the shared ML library and formats the result for the user.\n"
            "\n"
            "Why is this valuable?\n"
            "\n"
            "- fast to build,\n"
            "- easy to script,\n"
            "- easy to test repeatedly,\n"
            "- useful before a graphical interface exists,\n"
            "- useful for developers and automation systems.\n"
            "\n"
            "The chapter treats command-line tooling as a first-class MLOps interface rather than merely a development convenience.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. A utility CLI can handle retraining and remote endpoint testing\n"
            "\n"
            "The source's second CLI can perform tasks such as:\n"
            "\n"
            "- retrain the model with a specified test size,\n"
            "- call a local or remote prediction endpoint,\n"
            "- change the target host from the command line.\n"
            "\n"
            "This is a useful pattern:\n"
            "\n"
            "```text\n"
            "Developer/operator CLI\n"
            "   ├── retrain → shared ML library\n"
            "   └── predict → local/cloud HTTP endpoint\n"
            "```\n"
            "\n"
            "The CLI becomes an operational tool for both model-development and deployment verification.\n"
            "\n"
            "{{exercise:M13.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 22. CLI tools can be containerized and delivered like any other software\n"
            "\n"
            "The chapter also containerizes a small Click application.\n"
            "\n"
            "A Makefile can install dependencies and lint the Dockerfile.\n"
            "\n"
            "A Dockerfile packages the runtime and command-line application.\n"
            "\n"
            "The resulting image can be built and pushed to a registry.\n"
            "\n"
            "This means a CLI-based ML tool can have the same reproducibility and delivery discipline as a web microservice.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. The Flask layer should be thin\n"
            "\n"
            "The source's Flask application does very little ML work itself.\n"
            "\n"
            "The `/predict` route:\n"
            "\n"
            "1. reads a JSON payload,\n"
            "2. logs the payload,\n"
            "3. calls `mlib.predict(...)`,\n"
            "4. returns JSON.\n"
            "\n"
            "A simplified structure is:\n"
            "\n"
            "```python\n"
            "@app.route(\"/predict\", methods=[\"POST\"])\n"
            "def predict():\n"
            "    payload = request.json\n"
            "    prediction = mlib.predict(payload[\"Weight\"])\n"
            "    return jsonify({\"prediction\": prediction})\n"
            "```\n"
            "\n"
            "Keeping the HTTP layer thin makes the core model logic easier to test and reuse elsewhere.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Test the HTTP contract locally before cloud deployment\n"
            "\n"
            "The source runs the Flask app locally and calls it with a small shell script using `curl`.\n"
            "\n"
            "That script hides repetitive HTTP syntax and reduces manual mistakes.\n"
            "\n"
            "A good local test verifies:\n"
            "\n"
            "- service starts,\n"
            "- expected port is open,\n"
            "- `/predict` accepts the expected JSON,\n"
            "- returned JSON has the expected schema,\n"
            "- preprocessing and model loading work together.\n"
            "\n"
            "Only after this should cloud-specific debugging be added to the problem.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Containerizing the Flask service expands deployment choices\n"
            "\n"
            "The source builds the Flask application into a container and runs it locally with a port mapping.\n"
            "\n"
            "Once the application is containerized, it can be shared with teammates and moved to multiple deployment platforms.\n"
            "\n"
            "This is why containers function as a portability boundary in the chapter's MLOps cookbook.\n"
            "\n"
            "[[IMAGE_NEEDED: One Flask model service, multiple deployment targets | "
            "A containerized Flask prediction service branching to local Docker, Fargate, App Runner, Elastic Beanstalk, and other compatible targets | "
            "Learner should notice how containerization separates application packaging from deployment destination]]\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Build and publish containers automatically\n"
            "\n"
            "The chapter uses GitHub Actions to automate container creation and publishing.\n"
            "\n"
            "The workflow conceptually performs:\n"
            "\n"
            "```text\n"
            "Checkout source\n"
            "      ↓\n"
            "Authenticate to registry\n"
            "      ↓\n"
            "Build container\n"
            "      ↓\n"
            "Push image\n"
            "```\n"
            "\n"
            "The source uses GitHub Container Registry in the example but notes that similar services can be substituted, such as AWS ECR.\n"
            "\n"
            "A successful automated build also acts as a test that the container recipe still works.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. App Runner can connect source control directly to a deployed ML microservice\n"
            "\n"
            "The MLOps Cookbook service can be connected to App Runner so changes in the source repository trigger deployment.\n"
            "\n"
            "After deployment, the utility CLI can query the public endpoint.\n"
            "\n"
            "This creates a compact development loop:\n"
            "\n"
            "```text\n"
            "Change code\n"
            "   ↓\n"
            "Push to source control\n"
            "   ↓\n"
            "Managed build/deploy\n"
            "   ↓\n"
            "Secure endpoint\n"
            "   ↓\n"
            "CLI smoke test\n"
            "```\n"
            "\n"
            "The appeal is that less effort is spent on the underlying DevOps mechanics.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. AWS SAM packages serverless development, infrastructure, and local testing\n"
            "\n"
            "The chapter presents the AWS Serverless Application Model (SAM) as a recommended way to build production Lambda applications.\n"
            "\n"
            "Benefits named in the source include:\n"
            "\n"
            "- one deployment configuration,\n"
            "- CloudFormation integration,\n"
            "- built-in best practices,\n"
            "- local debugging/testing,\n"
            "- development-tool integration.\n"
            "\n"
            "A basic workflow begins with:\n"
            "\n"
            "```text\n"
            "sam init\n"
            "sam local invoke\n"
            "```\n"
            "\n"
            "A project contains artifacts such as:\n"
            "\n"
            "- `app.py`,\n"
            "- `requirements.txt`,\n"
            "- `template.yaml`,\n"
            "- unit tests.\n"
            "\n"
            "[[IMAGE_NEEDED: AWS SAM development loop | "
            "SAM project files feeding local container-based invocation, then build and guided deployment to Lambda/API Gateway | "
            "Learner should notice that serverless infrastructure and application logic are developed together]]\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Lambda input shape depends on how the function is invoked\n"
            "\n"
            "The source highlights an important Lambda integration detail.\n"
            "\n"
            "A function invoked directly may receive a payload like:\n"
            "\n"
            "```json\n"
            "{\"Weight\": 200}\n"
            "```\n"
            "\n"
            "When invoked through API Gateway, the useful payload may be encoded inside the event's `body` field.\n"
            "\n"
            "Therefore the handler can need logic such as:\n"
            "\n"
            "```python\n"
            "if \"body\" in event:\n"
            "    event = json.loads(event[\"body\"])\n"
            "```\n"
            "\n"
            "This is a general integration lesson: the model may be identical while the surrounding event contract changes across invocation mechanisms.\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Containerized Lambda packages small models with their runtime\n"
            "\n"
            "In the source's SAM ML example, a Docker image can contain:\n"
            "\n"
            "- serialized model,\n"
            "- ML library,\n"
            "- supporting dataset/scaling information,\n"
            "- Lambda handler,\n"
            "- Python dependencies.\n"
            "\n"
            "The image is stored in ECR and used by Lambda.\n"
            "\n"
            "This can be practical for relatively small model artifacts that fit the serverless deployment pattern.\n"
            "\n"
            "---\n"
            "\n"

            "## 31. `template.yaml` is the infrastructure-as-code layer\n"
            "\n"
            "The SAM template describes resources and event bindings.\n"
            "\n"
            "In the source example it defines a serverless function packaged as an image and exposes it through an API route.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```yaml\n"
            "Function:\n"
            "  package: container image\n"
            "  event:\n"
            "    type: API\n"
            "    path: /predict\n"
            "    method: POST\n"
            "```\n"
            "\n"
            "This means deployment infrastructure is versionable and repeatable rather than being a sequence of undocumented console clicks.\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Test locally before guided deployment\n"
            "\n"
            "The source's SAM workflow uses:\n"
            "\n"
            "```text\n"
            "sam build\n"
            "      ↓\n"
            "sam local invoke -e payload.json\n"
            "      ↓\n"
            "verify prediction locally\n"
            "      ↓\n"
            "sam deploy --guided\n"
            "```\n"
            "\n"
            "Local invocation is valuable because it detects packaging, dependency, handler, and payload errors before the remote deployment step.\n"
            "\n"
            "After deployment, the service can be tested through the Lambda console, development shell, API clients, or other HTTP tooling.\n"
            "\n"
            "{{exercise:M13.L01.EX05}}\n"
            "\n"
            "---\n"
            "\n"

            "## 33. Match AWS service patterns to organizational needs\n"
            "\n"
            "The source gives three broad patterns rather than one universal recommendation.\n"
            "\n"
            "### CaaS / App Runner\n"
            "\n"
            "A useful starting point for organizations that want to get a containerized prediction service running quickly.\n"
            "\n"
            "### SageMaker\n"
            "\n"
            "A stronger fit in the source's framing for larger organizations with multiple teams, large data, more complex training/deployment needs, and finer-grained security requirements.\n"
            "\n"
            "### Serverless + managed AI APIs\n"
            "\n"
            "A strong initial option for a small team/startup that needs to move quickly and can reuse pretrained capabilities.\n"
            "\n"
            "The meta-principle is:\n"
            "\n"
            "> **Pick services based on the problem and organizational context, not because one AWS service must be used for every ML project.**\n"
            "\n"
            "[[IMAGE_NEEDED: AWS MLOps service-selection matrix | "
            "Three columns for small/fast serverless+AI API, containerized App Runner/CaaS, and larger enterprise SageMaker workflows, compared by control, speed, and operational scope | "
            "Learner should notice that service choice depends on organizational needs]]\n"
            "\n"
            "---\n"
            "\n"

            "## 34. Case study: recommendation quality must connect to a product KPI\n"
            "\n"
            "The sports-social-network case study centers on **monthly active users (MAU)** as a key product metric.\n"
            "\n"
            "The platform needed more than a large number of signups. It needed acquisition, retention, and viral growth to work together.\n"
            "\n"
            "A major early problem was weak fan retention.\n"
            "\n"
            "Users had difficulty discovering relevant athletes and teams, received insufficient content, and often became inactive after the first month.\n"
            "\n"
            "The recommendation engine was part of the solution, but early iterations suffered from insufficient data and poor recommendations.\n"
            "\n"
            "As data and the algorithm improved, the team observed the desired retention improvement using cohort analysis.\n"
            "\n"
            "This connects MLOps to product management:\n"
            "\n"
            "```text\n"
            "Better data/model\n"
            "     ↓\n"
            "Better feed recommendations\n"
            "     ↓\n"
            "Higher user retention\n"
            "     ↓\n"
            "Healthier MAU growth\n"
            "     ↓\n"
            "Supports revenue strategy\n"
            "```\n"
            "\n"
            "A technically strong model matters because of the product outcome it improves.\n"
            "\n"
            "{{exercise:M13.L01.EX06}}\n"
            "\n"
            "---\n"
            "\n"

            "## 35. Case study lesson: machine learning is software engineering too\n"
            "\n"
            "The second interview in the chapter makes a direct argument: ML workflows should inherit mature software-engineering practices.\n"
            "\n"
            "The source specifically emphasizes:\n"
            "\n"
            "- traceability,\n"
            "- versioning,\n"
            "- testing,\n"
            "- automation,\n"
            "- documentation,\n"
            "- safe deployment strategies,\n"
            "- monitoring,\n"
            "- scaling.\n"
            "\n"
            "From an MLOps perspective, code, data, and models are all production artifacts that need controlled lifecycle management.\n"
            "\n"
            "---\n"
            "\n"

            "## 36. Career and systems advice: understand the business problem first\n"
            "\n"
            "The source's career advice prioritizes deep understanding of the business problem over technology for technology's sake.\n"
            "\n"
            "Questions to ask include:\n"
            "\n"
            "- What do users actually care about?\n"
            "- Which metrics reveal success or failure?\n"
            "- What is the right cost/performance/time-to-market trade-off?\n"
            "- Which parts should be automated?\n"
            "- Which quality gates must block bad models?\n"
            "\n"
            "This reinforces the earlier service-selection lesson: a technically impressive AWS architecture is not valuable if it solves the wrong problem.\n"
            "\n"
            "---\n"
            "\n"

            "## 37. Automation and security are scale requirements\n"
            "\n"
            "The interview advice emphasizes automation because manual processes do not scale well.\n"
            "\n"
            "Data-science teams should ideally be able to train, test, and deploy within established quality gates without requiring operations engineers for every development action.\n"
            "\n"
            "At the same time, the source stresses security practices such as:\n"
            "\n"
            "- least privilege,\n"
            "- encryption,\n"
            "- auditing,\n"
            "- appropriate access policies.\n"
            "\n"
            "Automation without security can scale risk as quickly as it scales productivity.\n"
            "\n"
            "---\n"
            "\n"

            "## 38. The chapter's AWS strategy: get quick wins, then deepen the platform\n"
            "\n"
            "The chapter's conclusion recommends a staged approach.\n"
            "\n"
            "The source encourages organizations to:\n"
            "\n"
            "- get quick wins with high-level AI APIs and managed deployment services,\n"
            "- automate as much of the lifecycle as practical,\n"
            "- invest in team AWS knowledge,\n"
            "- use more comprehensive platforms such as SageMaker for longer-term or more complex needs.\n"
            "\n"
            "The exact AWS services and interfaces evolve, but the architectural strategy is durable:\n"
            "\n"
            "```text\n"
            "Start simple\n"
            "   ↓\n"
            "Deliver something useful\n"
            "   ↓\n"
            "Automate it\n"
            "   ↓\n"
            "Measure it\n"
            "   ↓\n"
            "Add platform sophistication only when the problem needs it\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Progressive AWS MLOps adoption | "
            "A maturity path from managed API/serverless quick win to containerized service, automated delivery, monitoring, and fuller ML platform adoption | "
            "Learner should notice that platform complexity grows with actual needs]]\n"
            "\n"
            "{{exercise:M13.L01.EX07}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Every AWS ML project should start with the most comprehensive ML platform\n"
            "\n"
            "The chapter presents multiple paths, including managed APIs, serverless functions, containers, PaaS, and SageMaker.\n"
            "\n"
            "### Misconception 2: Building the capability yourself is automatically cheaper\n"
            "\n"
            "The source emphasizes opportunity cost and comparative advantage, not only direct service price.\n"
            "\n"
            "### Misconception 3: Serverless means there are literally no servers\n"
            "\n"
            "Servers are abstracted away from the developer's operational responsibility.\n"
            "\n"
            "### Misconception 4: Lambda is only for HTTP APIs\n"
            "\n"
            "The source shows manual, scheduled, S3-event, CLI/SDK, and API-driven invocation patterns.\n"
            "\n"
            "### Misconception 5: Containerizing the model is the end of MLOps\n"
            "\n"
            "A container is a portable deployment unit, but delivery automation, tests, monitoring, and product outcomes still matter.\n"
            "\n"
            "### Misconception 6: The Flask route should contain all preprocessing and ML code\n"
            "\n"
            "The source centralizes heavy ML logic in a reusable library and keeps interfaces thin.\n"
            "\n"
            "### Misconception 7: CLI tools are only for toy projects\n"
            "\n"
            "The chapter treats CLIs as fast, scriptable operational interfaces for prediction, retraining, and endpoint testing.\n"
            "\n"
            "### Misconception 8: Better offline accuracy automatically means a better production system\n"
            "\n"
            "The source repeatedly emphasizes operations, business impact, safe deployment, monitoring, and continuous improvement.\n"
            "\n"
            "### Misconception 9: One product KPI can always be interpreted without supporting metrics\n"
            "\n"
            "The sports-network case shows that a steady MAU number can hide retention problems or changing user composition.\n"
            "\n"
            "### Misconception 10: ML engineering can ignore ordinary software-engineering practices\n"
            "\n"
            "The source explicitly argues for versioning, testing, traceability, documentation, automation, monitoring, and safe deployment.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Managed AI API | High-level cloud service exposing pretrained AI capabilities through an API. |\n"
            "| Opportunity cost | Value of what an organization gives up when it spends its own resources building one capability instead of another. |\n"
            "| Serverless | Execution model where developers focus on functions/events while the provider abstracts server management. |\n"
            "| AWS Lambda | AWS serverless function service used throughout the chapter. |\n"
            "| Event-driven architecture | System where events such as uploads, schedules, or requests trigger computation. |\n"
            "| AWS Step Functions | Managed state-machine/workflow service used to compose tasks such as Lambda functions. |\n"
            "| Container as a Service (CaaS) | Managed deployment pattern for containerized applications without managing all underlying infrastructure directly. |\n"
            "| Amazon ECR | AWS container registry used to store container images. |\n"
            "| AWS Fargate | Managed container execution option presented in the chapter. |\n"
            "| AWS App Runner | High-level service that can deploy an application from source or container image. |\n"
            "| Elastic Beanstalk | AWS platform-as-a-service deployment option used in the chapter's continuous-delivery example. |\n"
            "| MLOps Cookbook | Reusable project scaffold in the source combining model library, CLI, API, container, dependencies, and model artifacts. |\n"
            "| CLI | Command-line interface used to invoke prediction, retraining, or remote-service operations. |\n"
            "| AWS SAM | Serverless Application Model toolkit/template approach for developing and deploying Lambda-based applications. |\n"
            "| API Gateway | AWS service pattern used to expose Lambda functions through HTTP APIs. |\n"
            "| Infrastructure as code | Versioned description of infrastructure and deployment resources such as SAM templates. |\n"
            "| Quality gate | Automated or manual criterion a model/service must satisfy before progressing toward production. |\n"
            "| MAU | Monthly active users, used as the key product metric in the sports-social-network case study. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. Why does the chapter focus on AWS service patterns rather than every AWS product?\n"
            "2. What does the Costco analogy teach about cloud-service abstraction levels?\n"
            "3. Why should opportunity cost influence build-versus-managed-service decisions?\n"
            "4. Which NLP capabilities are named for Amazon Comprehend?\n"
            "5. When might a managed AI API be a strong first solution?\n"
            "6. Why does the chapter start continuous-delivery learning with a static site?\n"
            "7. What role does a build configuration play in deployment reproducibility?\n"
            "8. Why can a cloud development environment be useful?\n"
            "9. What does serverless abstract away?\n"
            "10. Which kinds of events can invoke Lambda in the source examples?\n"
            "11. How does the S3 → Lambda → Rekognition workflow operate?\n"
            "12. What problem do Step Functions solve?\n"
            "13. What benefits of containers does the chapter emphasize?\n"
            "14. What role does ECR play in a Fargate workflow?\n"
            "15. What steps make up the chapter's Fargate deployment sequence?\n"
            "16. How does App Runner simplify deployment further?\n"
            "17. What systems lesson does the DeepLens example illustrate?\n"
            "18. Why does the chapter place operations alongside accuracy and explainability?\n"
            "19. Why should you learn CD with a simple app before adding ML complexity?\n"
            "20. What role does CodeBuild play in the Elastic Beanstalk example?\n"
            "21. Name at least six artifacts in the MLOps Cookbook project.\n"
            "22. Why is `mlib.py` separated from the CLI and Flask layers?\n"
            "23. Why are pinned dependencies useful?\n"
            "24. What advantages do CLI tools provide for MLOps?\n"
            "25. What can the utility CLI do beyond local prediction?\n"
            "26. Why can a CLI itself be containerized?\n"
            "27. Why should the Flask route remain thin?\n"
            "28. What should a local HTTP smoke test verify?\n"
            "29. How does containerization widen deployment choices?\n"
            "30. What does automated container publishing verify in addition to distributing the image?\n"
            "31. How can App Runner connect source control to a deployed endpoint?\n"
            "32. What benefits of SAM are listed in the source?\n"
            "33. Why can direct Lambda and API Gateway invocations require different payload handling?\n"
            "34. What role does `template.yaml` play in SAM?\n"
            "35. Why is `sam local invoke` useful before deployment?\n"
            "36. When does the source recommend CaaS/App Runner?\n"
            "37. When does the source recommend SageMaker?\n"
            "38. When does the source recommend serverless + AI APIs?\n"
            "39. Why was MAU alone insufficient to understand the sports network's health?\n"
            "40. How did recommendation quality connect to retention in the case study?\n"
            "41. Which software-engineering practices does the interview recommend for ML systems?\n"
            "42. Why should the business problem guide technology selection?\n"
            "43. Why are automation and quality gates both necessary?\n"
            "44. Which security principles are emphasized in the interview?\n"
            "45. What is the chapter's overall strategy for progressively adopting AWS MLOps capabilities?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**AWS MLOps is not about memorizing the largest number of AWS services. It is about choosing the simplest useful abstraction, "
            "building a reproducible ML core, exposing it through reusable interfaces, automating delivery and testing, measuring the product outcome, "
            "and adding infrastructure sophistication only when the real problem requires it.**\n"
        ),

        "estimated_minutes": 390,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "aws-chapter-framing", "title": "AWS MLOps is about choosing from many levels of abstraction", "order": 1},
            {"id": "service-spectrum", "title": "The chapter's Costco analogy: raw ingredients versus prepared services", "order": 2},
            {"id": "managed-ai-comprehend", "title": "Managed AI APIs can provide a fast first solution", "order": 3},
            {"id": "s3-hugo", "title": "Learn continuous delivery first with a simple S3-hosted project", "order": 4},
            {"id": "buildspec-recipe", "title": "A build configuration is an executable recipe", "order": 5},
            {"id": "cloud9", "title": "Cloud development environments reduce distance between development and deployment", "order": 6},
            {"id": "serverless-model", "title": "Serverless starts with the function as the unit of work", "order": 7},
            {"id": "lambda-triggers", "title": "Lambda functions can react to many types of triggers", "order": 8},
            {"id": "lambda-rekognition", "title": "Event-driven ML example: S3 upload → Lambda → image labels", "order": 9},
            {"id": "step-functions", "title": "Step Functions compose serverless tasks into workflows", "order": 10},
            {"id": "caas", "title": "Container as a Service gives portability without managing the entire platform", "order": 11},
            {"id": "fargate-workflow", "title": "Fargate workflow: build locally, publish to ECR, deploy as a service", "order": 12},
            {"id": "app-runner", "title": "App Runner trades control for simpler source-to-service deployment", "order": 13},
            {"id": "computer-vision-prototype", "title": "High-level hardware and services can shorten the computer-vision feedback loop", "order": 14},
            {"id": "accuracy-explainability-operations", "title": "In production, operations deserves equal status with accuracy and explainability", "order": 15},
            {"id": "elastic-beanstalk-cd", "title": "Learn continuous delivery with a simple application before adding ML complexity", "order": 16},
            {"id": "mlops-cookbook", "title": "A reusable MLOps cookbook separates concerns", "order": 17},
            {"id": "makefile-dependencies", "title": "Makefiles and pinned dependencies turn common actions into repeatable commands", "order": 18},
            {"id": "ml-library", "title": "Put model behavior in a reusable library, not inside every interface", "order": 19},
            {"id": "cli-tools", "title": "CLI tools are fast interfaces for testing and operating ML code", "order": 20},
            {"id": "utility-cli", "title": "A utility CLI can handle retraining and remote endpoint testing", "order": 21},
            {"id": "cli-container", "title": "CLI tools can be containerized and delivered like any other software", "order": 22},
            {"id": "flask-api", "title": "The Flask layer should be thin", "order": 23},
            {"id": "flask-local-test", "title": "Test the HTTP contract locally before cloud deployment", "order": 24},
            {"id": "flask-container", "title": "Containerizing the Flask service expands deployment choices", "order": 25},
            {"id": "github-actions-container", "title": "Build and publish containers automatically", "order": 26},
            {"id": "app-runner-ml", "title": "App Runner can connect source control directly to a deployed ML microservice", "order": 27},
            {"id": "sam", "title": "AWS SAM packages serverless development, infrastructure, and local testing", "order": 28},
            {"id": "lambda-event-shapes", "title": "Lambda input shape depends on how the function is invoked", "order": 29},
            {"id": "sam-container", "title": "Containerized Lambda packages small models with their runtime", "order": 30},
            {"id": "sam-iac", "title": "template.yaml is the infrastructure-as-code layer", "order": 31},
            {"id": "sam-build-deploy", "title": "Test locally before guided deployment", "order": 32},
            {"id": "service-selection-patterns", "title": "Match AWS service patterns to organizational needs", "order": 33},
            {"id": "sports-case", "title": "Case study: recommendation quality must connect to a product KPI", "order": 34},
            {"id": "ml-is-software", "title": "Case study lesson: machine learning is software engineering too", "order": 35},
            {"id": "business-first", "title": "Career and systems advice: understand the business problem first", "order": 36},
            {"id": "automation-security", "title": "Automation and security are scale requirements", "order": 37},
            {"id": "aws-takeaways", "title": "The chapter's AWS strategy: get quick wins, then deepen the platform", "order": 38},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M13.L01.EX01",
            "title": "Choose the AWS abstraction level",
            "lesson_code": "M13.L01",
            "section_id": "managed-ai-comprehend",
            "placement": "after_section",
            "description": (
                "Practice deciding when to use managed AI capabilities versus building more infrastructure yourself."
            ),
            "instructions": (
                "Choose a reasonable source-aligned AWS approach for each scenario and justify it:\n\n"
                "1. A two-person startup needs sentiment analysis in a customer-support tool within days.\n"
                "2. A team has a specialized prediction model and needs a portable HTTP service.\n"
                "3. A larger organization needs shared training/deployment controls across multiple teams.\n"
                "4. A one-off file-upload workflow should label incoming images automatically.\n\n"
                "For each scenario discuss opportunity cost, speed, control, and operational burden."
            ),
            "expected_output": (
                "Four service-pattern choices grounded in managed APIs, containers/CaaS, SageMaker, and Lambda/event-driven design."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "aws-service-selection",
                "opportunity-cost",
                "managed-ai-services",
                "cloud-architecture",
            ],
        },

        {
            "id": "M13.L01.EX02",
            "title": "Design an event-driven ML workflow",
            "lesson_code": "M13.L01",
            "section_id": "step-functions",
            "placement": "after_section",
            "description": (
                "Combine Lambda events, managed AI APIs, and workflow orchestration."
            ),
            "instructions": (
                "Design a serverless image-processing workflow where a new file arrives in S3.\n\n"
                "Include:\n"
                "1. the event that starts the workflow,\n"
                "2. a Lambda that extracts bucket/key information,\n"
                "3. a call to an image-labeling service,\n"
                "4. a second processing step,\n"
                "5. how Step Functions could order the tasks,\n"
                "6. what information you would log for debugging."
            ),
            "expected_output": (
                "A clear event-driven architecture from upload through labels to a second task."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "aws-lambda",
                "event-driven-architecture",
                "step-functions",
                "managed-ai-api",
            ],
        },

        {
            "id": "M13.L01.EX03",
            "title": "Build a learning-first continuous-delivery path",
            "lesson_code": "M13.L01",
            "section_id": "elastic-beanstalk-cd",
            "placement": "after_section",
            "description": (
                "Separate cloud/deployment learning from model complexity."
            ),
            "instructions": (
                ('1. You are learning AWS deployment for the first time and eventually want to deploy an ML API.\n'
                 '2. Design two stages:\n'
                 '3. Stage A: a hello-world Flask application using source control, linting, CodeBuild, and Elastic Beanstalk.\n'
                 '4. Stage B: replace the simple endpoint with a model-backed endpoint.\n'
                 '5. Explain which failures Stage A helps you isolate before ML is introduced.')
            ),
            "expected_output": (
                "A two-stage learning/deployment plan that reduces debugging complexity."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "continuous-delivery",
                "elastic-beanstalk",
                "codebuild",
                "debugging-strategy",
            ],
        },

        {
            "id": "M13.L01.EX04",
            "title": "Design the interfaces around one ML core",
            "lesson_code": "M13.L01",
            "section_id": "utility-cli",
            "placement": "after_section",
            "description": (
                "Practice separating reusable model logic from CLI and HTTP interfaces."
            ),
            "instructions": (
                "Design a small prediction project with one shared ML library.\n\n"
                "Specify responsibilities for:\n"
                "1. `mlib.py`,\n"
                "2. `cli.py`,\n"
                "3. `utilscli.py`,\n"
                "4. `app.py`,\n"
                "5. `Dockerfile`,\n"
                "6. `Makefile`,\n"
                "7. model artifact and supporting data.\n\n"
                "Then explain why preprocessing should not be independently reimplemented inside all three interfaces."
            ),
            "expected_output": (
                "A project structure that centralizes model logic and exposes it through multiple thin interfaces."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "ml-project-structure",
                "cli",
                "flask",
                "separation-of-concerns",
            ],
        },

        {
            "id": "M13.L01.EX05",
            "title": "Design a SAM ML deployment",
            "lesson_code": "M13.L01",
            "section_id": "sam-build-deploy",
            "placement": "after_section",
            "description": (
                "Connect Lambda handler logic, container packaging, IaC, local testing, and API deployment."
            ),
            "instructions": (
                "Design a small Lambda-based prediction service using the source's SAM pattern.\n\n"
                "Include:\n"
                "1. files placed in the container,\n"
                "2. handler behavior for direct invocation,\n"
                "3. handler behavior for API Gateway invocation,\n"
                "4. what `template.yaml` defines,\n"
                "5. how you test with `sam local invoke`,\n"
                "6. what `sam build` and guided deployment accomplish,\n"
                "7. where ECR fits."
            ),
            "expected_output": (
                "A complete serverless ML deployment flow from local project to deployed API."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "aws-sam",
                "aws-lambda",
                "api-gateway",
                "infrastructure-as-code",
            ],
        },

        {
            "id": "M13.L01.EX06",
            "title": "Connect model quality to product retention",
            "lesson_code": "M13.L01",
            "section_id": "sports-case",
            "placement": "after_section",
            "description": (
                "Practice reasoning from ML changes to business outcomes instead of stopping at model metrics."
            ),
            "instructions": (
                "A social platform reports stable monthly active users, but many users disappear after their first month.\n\n"
                "1. Explain why MAU alone may hide the problem.\n"
                "2. Define at least three supporting metrics related to acquisition, retention, or recommendation quality.\n"
                "3. Explain how insufficient recommendation data can affect retention.\n"
                "4. Design one cohort analysis you would monitor after improving the recommendation system.\n"
                "5. Explain how a better recommendation metric should ultimately connect to a product KPI."
            ),
            "expected_output": (
                "A product-aware ML measurement plan linking recommendation improvements to user retention."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "product-metrics",
                "recommendation-systems",
                "cohort-analysis",
                "business-ml-alignment",
            ],
        },

        {
            "id": "M13.L01.EX07",
            "title": "Create an AWS MLOps adoption roadmap",
            "lesson_code": "M13.L01",
            "section_id": "aws-takeaways",
            "placement": "after_section",
            "description": (
                "Build a staged AWS plan without starting with unnecessary complexity."
            ),
            "instructions": (
                "A ten-person company has one useful ML idea but no production ML infrastructure.\n\n"
                "Design three stages:\n"
                "1. a quick-win MVP,\n"
                "2. a repeatable production service,\n"
                "3. a later scalable MLOps platform.\n\n"
                "For each stage choose source-supported AWS patterns, list the automation you would add, "
                "state one quality gate, one monitoring concern, and one security concern."
            ),
            "expected_output": (
                "A progressive AWS MLOps roadmap that increases sophistication only as needs grow."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "aws-architecture",
                "mlops-roadmap",
                "automation",
                "security",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M13.L01.QZ01",

        "title": "MLOps for AWS — Knowledge Check",

        "lesson_code": "M13.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M13.L01.Q01",
                "section_id": "aws-chapter-framing",
                "question": "What is the main architectural lesson of the chapter's broad AWS service catalog?",
                "options": [
                    "Every project should use the same AWS service.",
                    "Choose an abstraction level that fits the problem, team, and organizational maturity.",
                    "Always build from EC2 directly.",
                    "Avoid managed services.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter presents several different AWS approaches rather than one universal stack."
                ),
            },

            {
                "id": "M13.L01.Q02",
                "section_id": "service-spectrum",
                "question": "What does the Costco analogy represent?",
                "options": [
                    "AWS regions are grocery stores.",
                    "Cloud services come at different preparation/abstraction levels with different cost and responsibility trade-offs.",
                    "Containers store food.",
                    "Only low-level services are valuable.",
                ],
                "correct": 1,
                "explanation": (
                    "The analogy compares prepared services with raw building blocks."
                ),
            },

            {
                "id": "M13.L01.Q03",
                "section_id": "managed-ai-comprehend",
                "question": "When can a service like Amazon Comprehend be attractive?",
                "options": [
                    "When a team wants fast access to common NLP capabilities without first building the entire modeling stack.",
                    "Only after building a custom NLP model.",
                    "Only for container orchestration.",
                    "Only for storing datasets.",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents managed NLP as a high-level fast-start option."
                ),
            },

            {
                "id": "M13.L01.Q04",
                "section_id": "s3-hugo",
                "question": "Why does the chapter teach an S3-hosted static-site deployment before complex ML deployment?",
                "options": [
                    "To learn continuous-delivery mechanics in a simpler system first.",
                    "Because ML models cannot use AWS.",
                    "Because S3 trains models.",
                    "To avoid source control.",
                ],
                "correct": 0,
                "explanation": (
                    "A small example separates deployment learning from ML-specific complexity."
                ),
            },

            {
                "id": "M13.L01.Q05",
                "section_id": "buildspec-recipe",
                "question": "What is a useful mental model for a build configuration file?",
                "options": [
                    "An executable recipe describing repeatable build/deployment actions.",
                    "A model accuracy report.",
                    "A database table.",
                    "A monitoring alert.",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly treats the build configuration as a recipe."
                ),
            },

            {
                "id": "M13.L01.Q06",
                "section_id": "serverless-model",
                "question": "What does 'serverless' mean in the chapter's practical framing?",
                "options": [
                    "No physical servers exist.",
                    "The provider abstracts server management so developers focus on functions and events.",
                    "Only browser code can run.",
                    "Containers are forbidden.",
                ],
                "correct": 1,
                "explanation": (
                    "The execution infrastructure still exists; it is simply managed for the developer."
                ),
            },

            {
                "id": "M13.L01.Q07",
                "section_id": "lambda-triggers",
                "question": "Which can trigger a Lambda in the source examples?",
                "options": [
                    "Manual/CLI invocation",
                    "S3 events",
                    "Schedules",
                    "All of the above",
                ],
                "correct": 3,
                "explanation": (
                    "The source uses all three as examples of Lambda invocation patterns."
                ),
            },

            {
                "id": "M13.L01.Q08",
                "section_id": "lambda-rekognition",
                "question": "What happens in the S3 computer-vision trigger example?",
                "options": [
                    "An image upload triggers Lambda, which calls Rekognition to detect labels.",
                    "Rekognition deploys an S3 bucket.",
                    "Lambda trains a new operating system.",
                    "The image is ignored.",
                ],
                "correct": 0,
                "explanation": (
                    "The example demonstrates event-driven composition of storage, Lambda, and a managed AI service."
                ),
            },

            {
                "id": "M13.L01.Q09",
                "section_id": "step-functions",
                "question": "Why use Step Functions in the chapter's serverless examples?",
                "options": [
                    "To sequence multiple tasks/functions in a managed workflow.",
                    "To store Docker images.",
                    "To replace Python.",
                    "To train every ML model.",
                ],
                "correct": 0,
                "explanation": (
                    "Step Functions provide state-machine orchestration across tasks."
                ),
            },

            {
                "id": "M13.L01.Q10",
                "section_id": "caas",
                "question": "What is one advantage of containers for MLOps emphasized by the source?",
                "options": [
                    "They help reproduce a runtime locally and deploy the same packaged software elsewhere.",
                    "They guarantee model accuracy.",
                    "They remove the need for source code.",
                    "They cannot use registries.",
                ],
                "correct": 0,
                "explanation": (
                    "Runtime portability is one of the source's key container benefits."
                ),
            },

            {
                "id": "M13.L01.Q11",
                "section_id": "fargate-workflow",
                "question": "What role does ECR play in the Fargate workflow?",
                "options": [
                    "It stores the container image used for deployment.",
                    "It labels images with Rekognition.",
                    "It replaces Flask.",
                    "It provides a Jupyter notebook.",
                ],
                "correct": 0,
                "explanation": (
                    "ECR is the container registry in the chapter's AWS container workflow."
                ),
            },

            {
                "id": "M13.L01.Q12",
                "section_id": "app-runner",
                "question": "Why is App Runner attractive in the source's framing?",
                "options": [
                    "It removes much of the deployment plumbing and can deploy from source or a container.",
                    "It requires more low-level orchestration than Fargate.",
                    "It is only a storage service.",
                    "It cannot expose a URL.",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents App Runner as a high-level deployment abstraction."
                ),
            },

            {
                "id": "M13.L01.Q13",
                "section_id": "accuracy-explainability-operations",
                "question": "What production lesson does the chapter make about accuracy?",
                "options": [
                    "Accuracy is the only important constraint.",
                    "A reasonable model that can be operationalized and continuously improved may be more useful than an undeployable higher-accuracy model.",
                    "Explainability and operations do not matter.",
                    "Model quality cannot improve after deployment.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter emphasizes operational delivery and continuous improvement."
                ),
            },

            {
                "id": "M13.L01.Q14",
                "section_id": "elastic-beanstalk-cd",
                "question": "What is the main learning strategy behind the Elastic Beanstalk hello-world example?",
                "options": [
                    "Master a simple continuous-delivery path before adding model complexity.",
                    "Never deploy ML models.",
                    "Only use manual deployment.",
                    "Avoid linting and testing.",
                ],
                "correct": 0,
                "explanation": (
                    "The source recommends isolating deployment learning from ML complexity."
                ),
            },

            {
                "id": "M13.L01.Q15",
                "section_id": "mlops-cookbook",
                "question": "What is the main purpose of the MLOps Cookbook project structure?",
                "options": [
                    "Provide a reusable, intentionally simple scaffold for deploying ML logic through multiple interfaces and targets.",
                    "Maximize model complexity.",
                    "Replace all cloud services.",
                    "Store only a notebook.",
                ],
                "correct": 0,
                "explanation": (
                    "The cookbook focuses on deployment patterns rather than sophisticated modeling."
                ),
            },

            {
                "id": "M13.L01.Q16",
                "section_id": "ml-library",
                "question": "Why centralize preprocessing and prediction in `mlib.py`?",
                "options": [
                    "So CLI and web interfaces can reuse the same model behavior instead of duplicating logic.",
                    "So Flask cannot call the model.",
                    "To avoid testing.",
                    "To hide model output.",
                ],
                "correct": 0,
                "explanation": (
                    "Shared ML logic reduces divergence across interfaces."
                ),
            },

            {
                "id": "M13.L01.Q17",
                "section_id": "cli-tools",
                "question": "Why does the chapter value CLI tools?",
                "options": [
                    "They are fast to develop, scriptable, and useful for repeated prediction/testing workflows.",
                    "They are required for every end user.",
                    "They replace containers.",
                    "They cannot call remote APIs.",
                ],
                "correct": 0,
                "explanation": (
                    "The source repeatedly presents CLI tooling as a high-speed operational interface."
                ),
            },

            {
                "id": "M13.L01.Q18",
                "section_id": "flask-api",
                "question": "What should the Flask prediction route primarily do?",
                "options": [
                    "Parse the request, call shared ML logic, and return a response.",
                    "Reimplement all training logic.",
                    "Manually scale servers.",
                    "Replace the model file.",
                ],
                "correct": 0,
                "explanation": (
                    "The source keeps most model behavior in the library layer."
                ),
            },

            {
                "id": "M13.L01.Q19",
                "section_id": "github-actions-container",
                "question": "What does an automated container-build workflow provide?",
                "options": [
                    "A repeatable check that the image can be built plus automatic publication to a registry.",
                    "Guaranteed business success.",
                    "Automatic model retraining in every case.",
                    "Removal of all credentials.",
                ],
                "correct": 0,
                "explanation": (
                    "The source uses the workflow both as build validation and delivery."
                ),
            },

            {
                "id": "M13.L01.Q20",
                "section_id": "sam",
                "question": "Which capability does the source associate with AWS SAM?",
                "options": [
                    "Local testing/debugging plus versioned serverless deployment configuration.",
                    "Only data visualization.",
                    "Only model training.",
                    "Only container registry storage.",
                ],
                "correct": 0,
                "explanation": (
                    "SAM combines development tooling and deployment/infrastructure definition."
                ),
            },

            {
                "id": "M13.L01.Q21",
                "section_id": "lambda-event-shapes",
                "question": "Why might a Lambda handler check for a `body` field?",
                "options": [
                    "API Gateway can wrap the HTTP payload inside the event body.",
                    "Direct Lambda calls never contain data.",
                    "The model requires HTML.",
                    "SAM removes all event fields.",
                ],
                "correct": 0,
                "explanation": (
                    "The source shows different payload shapes for direct function calls versus API Gateway requests."
                ),
            },

            {
                "id": "M13.L01.Q22",
                "section_id": "sam-iac",
                "question": "What role does `template.yaml` play in the SAM example?",
                "options": [
                    "It defines serverless resources and event/API configuration as infrastructure as code.",
                    "It stores training examples.",
                    "It replaces Python dependencies.",
                    "It is only a README file.",
                ],
                "correct": 0,
                "explanation": (
                    "The template is the deployable infrastructure definition."
                ),
            },

            {
                "id": "M13.L01.Q23",
                "section_id": "service-selection-patterns",
                "question": "Which pairing best matches the source's service-selection examples?",
                "options": [
                    "Small fast-moving team → serverless + AI API; larger multi-team environment → SageMaker",
                    "Small team → always SageMaker; large enterprise → only curl",
                    "Every team → only Fargate",
                    "Every team → only EC2",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly presents different service patterns for different organizational needs."
                ),
            },

            {
                "id": "M13.L01.Q24",
                "section_id": "sports-case",
                "question": "Why could stable MAU still hide a product problem?",
                "options": [
                    "New users could be replacing churned users, masking poor retention.",
                    "MAU always measures retention perfectly.",
                    "Recommendation quality cannot affect activity.",
                    "Monthly metrics never change.",
                ],
                "correct": 0,
                "explanation": (
                    "The case study explains why supporting acquisition/retention analysis is needed."
                ),
            },

            {
                "id": "M13.L01.Q25",
                "section_id": "sports-case",
                "question": "What improved as recommendation data and algorithms improved in the sports-network case?",
                "options": [
                    "Fan retention",
                    "Container build time only",
                    "S3 storage price",
                    "Lambda cold-start configuration",
                ],
                "correct": 0,
                "explanation": (
                    "The case study links better recommendations with the desired retention improvement."
                ),
            },

            {
                "id": "M13.L01.Q26",
                "section_id": "ml-is-software",
                "question": "Which practice does the source argue should apply to ML like other software engineering?",
                "options": [
                    "Versioning and testing",
                    "Safe deployment",
                    "Monitoring and automation",
                    "All of the above",
                ],
                "correct": 3,
                "explanation": (
                    "The interview explicitly lists these as nonoptional engineering practices."
                ),
            },

            {
                "id": "M13.L01.Q27",
                "section_id": "business-first",
                "question": "What is the chapter's career advice before choosing technology?",
                "options": [
                    "Understand the business problem, users, metrics, and trade-offs deeply.",
                    "Choose the largest service first.",
                    "Optimize the résumé before the product.",
                    "Ignore time-to-market.",
                ],
                "correct": 0,
                "explanation": (
                    "The interview emphasizes problem understanding over technology for its own sake."
                ),
            },

            {
                "id": "M13.L01.Q28",
                "section_id": "automation-security",
                "question": "Why are quality gates still necessary in highly automated MLOps?",
                "options": [
                    "Automation should accelerate good changes without allowing bad models to flow unchecked into production.",
                    "Automation eliminates all failures.",
                    "Quality gates are only for manual systems.",
                    "They are only used for billing.",
                ],
                "correct": 0,
                "explanation": (
                    "The source recommends extensive automation together with appropriate gates."
                ),
            },

            {
                "id": "M13.L01.Q29",
                "section_id": "automation-security",
                "question": "Which security principle is explicitly emphasized in the chapter's career advice?",
                "options": [
                    "Least privilege",
                    "Share every credential",
                    "Disable auditing",
                    "Avoid encryption",
                ],
                "correct": 0,
                "explanation": (
                    "The source also mentions encryption and auditing among the relevant security practices."
                ),
            },

            {
                "id": "M13.L01.Q30",
                "section_id": "aws-takeaways",
                "type": "open",
                "question": (
                    "Design an AWS MLOps architecture for a small company launching its first prediction product. "
                    "Start with the simplest useful AWS abstraction and show how the system could evolve toward stronger "
                    "containerization, automated delivery, monitoring, quality gates, and—only if the organizational need grows—"
                    "a broader platform such as SageMaker. Explain the business metric you would track and the security practices you would apply."
                ),
            },
        ],

        "passing_score": 70,
    },
}
