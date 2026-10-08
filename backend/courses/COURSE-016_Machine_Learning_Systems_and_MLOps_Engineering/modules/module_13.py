"""M12.L01 — Monitoring and Logging for MLOps.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 6, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M12.L01"

MODULE_ORDER = 12

MODULE_TITLE = "Monitoring and Logging for MLOps"

MODULE_DESCRIPTION = (
    "Learn how observability, logging, metrics, baselines, and drift monitoring "
    "make production ML systems understandable and safer to operate. Practice "
    "Python logging, metric design, AWS SageMaker Model Monitor patterns, and "
    "Azure ML data-drift monitoring."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Monitoring and Logging for MLOps",

    "slug": "practical-mlops-m12-l01-monitoring-and-logging",

    "description": (
        "A production-focused lesson on observability for cloud MLOps, meaningful "
        "logging, Python log levels and logger hierarchy, model and business metrics, "
        "baselines, target datasets, data capture, scheduled drift monitoring, and "
        "cloud-based drift workflows with AWS SageMaker and Azure ML."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 5.0,

    "skill_tags": [
        "mlops",
        "observability",
        "logging",
        "monitoring",
        "metrics",
        "python-logging",
        "log-levels",
        "logger-hierarchy",
        "cloud-observability",
        "business-metrics",
        "model-monitoring",
        "counters",
        "timers",
        "values",
        "baseline-dataset",
        "target-dataset",
        "data-capture",
        "data-drift",
        "sagemaker-model-monitor",
        "cloudwatch",
        "azure-monitor",
        "azure-ml-drift",
        "application-insights",
        "automation",
    ],

    "prerequisite_ids": ["M11.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Monitoring and Logging for MLOps",

        "content": (
            "# Monitoring and Logging for MLOps\n"
            "\n"
            "> **Lesson:** M12.L01  \n"
            "> **Module:** Monitoring and Logging for MLOps  \n"
            "> **Source alignment:** Chapter 6. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why logging and monitoring are foundational DevOps/MLOps capabilities.\n"
            "- Distinguish useful observability from noisy or cryptic output.\n"
            "- Explain why infrastructure metrics alone can miss critical product failures.\n"
            "- Describe the role of cloud observability services in collecting logs, metrics, alerts, and autoscaling signals.\n"
            "- Explain the difference between logs, metrics, monitoring, and observability in the chapter's framing.\n"
            "- Use Python's logging system instead of ad hoc print statements.\n"
            "- Explain why `logger.exception()` is useful during error handling.\n"
            "- Order the five common log levels by verbosity/severity.\n"
            "- Explain why log verbosity should change over an application's lifecycle.\n"
            "- Explain logger hierarchy and how third-party libraries can produce unwanted noise.\n"
            "- Configure separate logger behavior for application code and dependencies.\n"
            "- Explain why monitoring should tell a meaningful operational story.\n"
            "- Define counters, timers, and value metrics.\n"
            "- Select useful metrics for data processing, model serving, and business behavior.\n"
            "- Explain the roles of baseline and target datasets in drift monitoring.\n"
            "- Describe the AWS SageMaker data-capture and Model Monitor workflow.\n"
            "- Explain why monitored serving data must preserve expected feature order/type assumptions.\n"
            "- Interpret baseline constraints and drift violations at a high level.\n"
            "- Explain how scheduled monitoring compares new traffic against a baseline.\n"
            "- Describe Azure ML's baseline/target/monitor pattern for data drift.\n"
            "- Explain how seasonality can complicate drift interpretation.\n"
            "- Explain why automation should make logs, metrics, and drift reports continuously available.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Logging and monitoring are not optional production extras\n"
            "\n"
            "The chapter starts from a simple problem: engineers often prefer writing the main application code "
            "and postpone work such as testing, documentation, logging, and monitoring.\n"
            "\n"
            "That is dangerous in production ML because a model can fail in ways that are difficult to reconstruct after the fact.\n"
            "\n"
            "Logging and monitoring provide evidence about what the system was doing before and during a problem.\n"
            "\n"
            "A useful observability strategy should help answer questions like:\n"
            "\n"
            "- What happened?\n"
            "- When did it happen?\n"
            "- Which component was involved?\n"
            "- Was the problem infrastructure, software, data, or model behavior?\n"
            "- Is the situation getting better or worse?\n"
            "\n"
            "The key goal is not to produce the most output. It is to produce information that helps people understand the system's state.\n"
            "\n"
            "[[IMAGE_NEEDED: Observability questions around a production ML system | "
            "A deployed ML service surrounded by logs, metrics, alerts, model-quality signals, and data-drift signals | "
            "Learner should notice that observability exists to explain system state, not merely collect data]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. A log line should tell a story, not create another puzzle\n"
            "\n"
            "The source gives an example of a cryptic low-level log entry that an experienced user could not interpret.\n"
            "\n"
            "Its real meaning was simple: one machine could not contact another service at a particular address.\n"
            "\n"
            "This illustrates an important design rule:\n"
            "\n"
            "> **Observability output should help the consumer understand what happened without requiring them to decode implementation trivia.**\n"
            "\n"
            "A good operational message might include:\n"
            "\n"
            "- component name,\n"
            "- severity,\n"
            "- what operation failed,\n"
            "- the resource or endpoint involved,\n"
            "- enough context to begin debugging.\n"
            "\n"
            "Bad logging is not harmless. Useless output consumes storage and attention while still failing to support diagnosis.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. CPU and disk metrics cannot tell you whether the product still works\n"
            "\n"
            "The chapter describes a content-management system whose operations team already monitored server health such as disk and memory.\n"
            "\n"
            "But imagine the website's most important **subscribe** button breaks after a JavaScript deployment.\n"
            "\n"
            "Disk usage can remain normal.\n"
            "\n"
            "Memory usage can remain normal.\n"
            "\n"
            "The business-critical action can still be completely broken.\n"
            "\n"
            "A more useful metric might track the button's click-through or conversion behavior over time.\n"
            "\n"
            "This creates an important monitoring hierarchy:\n"
            "\n"
            "```text\n"
            "Infrastructure health\n"
            "CPU, memory, disk, network\n"
            "\n"
            "Application health\n"
            "errors, latency, successful requests\n"
            "\n"
            "ML health\n"
            "accuracy / quality, drift, feature validity\n"
            "\n"
            "Business/product health\n"
            "conversion, engagement, revenue-related actions\n"
            "```\n"
            "\n"
            "A healthy server does not prove a healthy product.\n"
            "\n"
            "[[IMAGE_NEEDED: Four monitoring layers | "
            "A stack showing infrastructure health, application health, ML/model health, and business/product health | "
            "Learner should notice that lower layers can look healthy while higher-level outcomes fail]]\n"
            "\n"
            "{{exercise:M12.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. MLOps adds data and model signals to ordinary software observability\n"
            "\n"
            "Traditional cloud software already needs logs, metrics, dashboards, and alerts.\n"
            "\n"
            "MLOps adds new observability targets such as:\n"
            "\n"
            "- training metadata,\n"
            "- endpoint predictions,\n"
            "- model performance over time,\n"
            "- captured serving data,\n"
            "- drift indicators,\n"
            "- dataset constraints and violations.\n"
            "\n"
            "The chapter stresses that a model with a significant drop in accuracy should not quietly reach or remain in production.\n"
            "\n"
            "The earlier such problems are detected, the cheaper they are to fix.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Cloud observability systems centralize logs, metrics, alerts, and reactions\n"
            "\n"
            "The source names several cloud observability services:\n"
            "\n"
            "- Amazon CloudWatch,\n"
            "- Google Cloud operations suite,\n"
            "- Azure Monitor.\n"
            "\n"
            "At a high level, cloud components send operational information into a central system.\n"
            "\n"
            "That information can then feed:\n"
            "\n"
            "- dashboards,\n"
            "- alerts,\n"
            "- human investigation,\n"
            "- automated scaling or other actions.\n"
            "\n"
            "For example, a production endpoint could scale if CPU or memory exceeds a threshold.\n"
            "\n"
            "The MLOps difference is that model-specific data and metadata also enter this observability ecosystem.\n"
            "\n"
            "[[IMAGE_NEEDED: Cloud MLOps observability hub | "
            "Servers, training jobs, application logs, and model endpoints all sending logs/metrics to a central observability service, "
            "which feeds dashboards, alerts, autoscaling, and human analysis | Learner should notice the many-to-one collection pattern]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Logging separates normal events from errors through levels and structure\n"
            "\n"
            "The source uses Nginx access and error logs to introduce logging.\n"
            "\n"
            "An access log can record ordinary requests such as:\n"
            "\n"
            "- client address,\n"
            "- timestamp,\n"
            "- HTTP method/path,\n"
            "- user-agent information.\n"
            "\n"
            "An error log can record a failure such as a permission error while opening a file.\n"
            "\n"
            "The important idea is **severity**: log consumers should be able to distinguish routine activity from warning/error conditions.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. `print()` is not a production logging strategy\n"
            "\n"
            "Developers often debug by inserting `print()` statements.\n"
            "\n"
            "That can be useful temporarily, but it becomes difficult to maintain because:\n"
            "\n"
            "- statements must be added and removed manually,\n"
            "- verbosity is hard to control,\n"
            "- output lacks standardized severity,\n"
            "- routing output to multiple destinations becomes awkward,\n"
            "- useful traceback/context handling must be reinvented.\n"
            "\n"
            "A logging framework solves these problems systematically.\n"
            "\n"
            "The chapter's Python examples use the standard `logging` module.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Add context before the failure happens\n"
            "\n"
            "The source starts with a brittle CSV-processing script.\n"
            "\n"
            "A simplified version is:\n"
            "\n"
            "```python\n"
            "import sys\n"
            "import pandas as pd\n"
            "\n"
            "argument = sys.argv[-1]\n"
            "df = pd.read_csv(argument)\n"
            "print(df.describe())\n"
            "```\n"
            "\n"
            "If the path is wrong, Pandas raises an exception.\n"
            "\n"
            "A poor error handler can make things worse:\n"
            "\n"
            "```python\n"
            "try:\n"
            "    df = pd.read_csv(argument)\n"
            "except Exception:\n"
            "    print(\"Had a problem trying to read the CSV file\")\n"
            "```\n"
            "\n"
            "That message hides the useful context.\n"
            "\n"
            "A logger can record what input the application was attempting to process before the exception occurs.\n"
            "\n"
            "```python\n"
            "import logging\n"
            "\n"
            "logging.basicConfig()\n"
            "logger = logging.getLogger(\"describe\")\n"
            "logger.setLevel(logging.DEBUG)\n"
            "\n"
            "logger.debug(\"processing input file: %s\", argument)\n"
            "```\n"
            "\n"
            "That single line can save substantial debugging time in a remote pipeline.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Preserve the traceback with `logger.exception()`\n"
            "\n"
            "Catching an exception without recording the traceback removes the evidence needed to understand the real cause.\n"
            "\n"
            "The chapter improves the example with:\n"
            "\n"
            "```python\n"
            "try:\n"
            "    df = pd.read_csv(argument)\n"
            "except Exception:\n"
            "    logger.exception(\"Had a problem trying to read the CSV file\")\n"
            "```\n"
            "\n"
            "`logger.exception()` records an error-level message together with traceback information while allowing the program "
            "to continue if the surrounding code is designed to continue.\n"
            "\n"
            "This is more useful than a generic message such as 'something went wrong.'\n"
            "\n"
            "[[IMAGE_NEEDED: Context-rich exception logging | "
            "A remote job failure where a structured error message includes operation context and a traceback, contrasted with a generic one-line print message | "
            "Learner should notice how preserved context makes diagnosis much easier]]\n"
            "\n"
            "{{exercise:M12.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Log levels control how much operational detail you see\n"
            "\n"
            "The source presents five common Python logging levels.\n"
            "\n"
            "From **most verbose** to **least verbose / most severe**:\n"
            "\n"
            "```text\n"
            "DEBUG\n"
            "INFO\n"
            "WARNING\n"
            "ERROR\n"
            "CRITICAL\n"
            "```\n"
            "\n"
            "A DEBUG configuration includes lower-severity operational detail as well as warnings/errors.\n"
            "\n"
            "A higher threshold such as ERROR suppresses routine debug and informational messages.\n"
            "\n"
            "This allows the same logging statements to remain in the program while operators change what is actually emitted.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Useful verbosity changes as software matures\n"
            "\n"
            "The source recommends expecting more surprises in newly deployed software.\n"
            "\n"
            "High verbosity such as DEBUG can therefore be useful early in a deployment lifecycle.\n"
            "\n"
            "After the system becomes stable, the same volume may become noise.\n"
            "\n"
            "At that point, the team can tighten normal logging toward INFO or ERROR while preserving the ability to increase verbosity during investigation.\n"
            "\n"
            "The principle is:\n"
            "\n"
            "> **Logging configuration should adapt to operational needs rather than remain permanently maximal or minimal.**\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Logger hierarchy lets you control your code and dependencies separately\n"
            "\n"
            "Python applications often depend on libraries that have their own loggers.\n"
            "\n"
            "The source demonstrates this with `requests` / `urllib3`.\n"
            "\n"
            "When the root logger is set to DEBUG, both the application's messages and lower-level dependency messages may appear.\n"
            "\n"
            "That can be noisy.\n"
            "\n"
            "You can fine-tune one dependency separately:\n"
            "\n"
            "```python\n"
            "import logging\n"
            "\n"
            "root_logger = logging.getLogger()\n"
            "root_logger.setLevel(logging.DEBUG)\n"
            "\n"
            "urllib_logger = logging.getLogger(\"urllib3\")\n"
            "urllib_logger.setLevel(logging.ERROR)\n"
            "```\n"
            "\n"
            "Now the application can remain verbose while routine HTTP connection details from the dependency are suppressed.\n"
            "\n"
            "[[IMAGE_NEEDED: Python logger hierarchy | "
            "A root logger above application logger and library loggers, with different severity thresholds on each branch | "
            "Learner should notice that one noisy dependency can be tuned without silencing the whole application]]\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Different audiences may need different log destinations\n"
            "\n"
            "The chapter describes using multiple loggers/destinations for the same application.\n"
            "\n"
            "One destination can show concise user-friendly output.\n"
            "\n"
            "Another can store detailed developer-oriented diagnostics and tracebacks.\n"
            "\n"
            "This is useful because the best output for an operator, an end user, and a developer is not always the same.\n"
            "\n"
            "The broader design question is:\n"
            "\n"
            "> Who consumes this information, and what do they need to make a decision?\n"
            "\n"
            "---\n"
            "\n"

            "## 14. If you can measure, you can compare; if you can compare, you can improve\n"
            "\n"
            "The chapter uses an athletic training journal as an analogy for monitoring.\n"
            "\n"
            "The journal recorded:\n"
            "\n"
            "- planned workout,\n"
            "- actual results,\n"
            "- how the athlete felt,\n"
            "- other relevant information such as pain or illness.\n"
            "\n"
            "A single entry may not seem valuable.\n"
            "\n"
            "Over time, the history becomes a basis for comparison and planning.\n"
            "\n"
            "Production ML is similar: when a new model version is released, you need historical signals to determine whether it is better, worse, or simply different.\n"
            "\n"
            "Monitoring is therefore not just alerting. It is also preserving comparable operational history.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Metrics and automation reduce dependence on one person\n"
            "\n"
            "The source criticizes workflows where one employee manually receives data, 'runs some numbers,' and returns a report.\n"
            "\n"
            "That process does not scale and fails the **bus test**: if that person suddenly becomes unavailable, the workflow should still be understandable and operable.\n"
            "\n"
            "Automated metrics and reports help convert personal knowledge into shared system behavior.\n"
            "\n"
            "This is another reason observability matters: information should be continuously available without depending on one engineer remembering how to produce it.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Model monitoring covers the whole path to production\n"
            "\n"
            "The chapter defines ML monitoring broadly.\n"
            "\n"
            "It includes signals from:\n"
            "\n"
            "- data collection and cleaning,\n"
            "- training jobs,\n"
            "- deployment services,\n"
            "- hosted inference,\n"
            "- model performance,\n"
            "- production data.\n"
            "\n"
            "There is no single universal set of metrics because the important signal depends on the step.\n"
            "\n"
            "For a data-cleaning job, useful metrics might include:\n"
            "\n"
            "- number of empty values per column,\n"
            "- processing duration.\n"
            "\n"
            "For a hosted model, useful metrics might include:\n"
            "\n"
            "- request latency,\n"
            "- prediction error rate,\n"
            "- drift indicators.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Three basic metric types: counter, timer, value\n"
            "\n"
            "The source identifies three common metric patterns.\n"
            "\n"
            "### Counter\n"
            "\n"
            "Counts occurrences.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- empty cells,\n"
            "- failed requests,\n"
            "- processed records.\n"
            "\n"
            "### Timer\n"
            "\n"
            "Measures elapsed time.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- preprocessing time,\n"
            "- model inference latency,\n"
            "- pipeline-stage duration.\n"
            "\n"
            "### Value\n"
            "\n"
            "Stores an observed measurement that is not naturally a count or duration.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- resulting database size,\n"
            "- current accuracy,\n"
            "- a drift magnitude.\n"
            "\n"
            "[[IMAGE_NEEDED: Counter timer value metric types | "
            "Three cards showing a count of missing values, a timer for prediction latency, and a numeric value such as database size or model score | "
            "Learner should notice how different operational questions map to different metric types]]\n"
            "\n"
            "{{exercise:M12.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Drift monitoring needs a reference and something new to compare\n"
            "\n"
            "The chapter introduces two important concepts.\n"
            "\n"
            "### Baseline\n"
            "\n"
            "A reference describing acceptable or expected data characteristics.\n"
            "\n"
            "### Target data\n"
            "\n"
            "The newer data being monitored and compared against the baseline.\n"
            "\n"
            "The terminology can be confusing because the dataset used to create the baseline may also be called a baseline dataset, "
            "and the same training dataset can sometimes serve as the initial reference dataset.\n"
            "\n"
            "A simple mental model is:\n"
            "\n"
            "```text\n"
            "Reference dataset\n"
            "      ↓\n"
            "Create statistics + constraints\n"
            "      ↓\n"
            "Baseline\n"
            "\n"
            "New production data\n"
            "      ↓\n"
            "Compare with baseline\n"
            "      ↓\n"
            "Violation / drift report\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Baseline versus target monitoring | "
            "A reference dataset generating baseline statistics/constraints, then new serving data being compared against them to produce violations | "
            "Learner should notice the difference between the reference and the data being monitored]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. AWS SageMaker workflow step 1: capture production data\n"
            "\n"
            "The source's SageMaker example enables data capture when deploying the model.\n"
            "\n"
            "A simplified source-aligned configuration is:\n"
            "\n"
            "```python\n"
            "from sagemaker.model_monitor import DataCaptureConfig\n"
            "\n"
            "data_capture_config = DataCaptureConfig(\n"
            "    enable_capture=True,\n"
            "    sampling_percentage=100,\n"
            "    destination_s3_uri=\"s3://.../capture\",\n"
            ")\n"
            "```\n"
            "\n"
            "The capture configuration is then attached to the deployed endpoint.\n"
            "\n"
            "As requests arrive, SageMaker saves request-related information to storage so monitoring jobs can analyze it later.\n"
            "\n"
            "The chapter's example stores captured data in S3.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Monitoring data must still respect the model's expected input contract\n"
            "\n"
            "The chapter repeatedly stresses that monitored data should have the expected features and order.\n"
            "\n"
            "Why?\n"
            "\n"
            "A drift system cannot meaningfully compare inputs if today's field positions/types no longer correspond to the model's training schema.\n"
            "\n"
            "Examples of problematic change include:\n"
            "\n"
            "- a feature changing from one numeric unit to another,\n"
            "- null/empty values appearing unexpectedly,\n"
            "- a type changing from integer-like to another representation,\n"
            "- feature order changing.\n"
            "\n"
            "These may be data-quality failures rather than meaningful real-world behavior change.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. AWS workflow step 2: generate baseline statistics and constraints\n"
            "\n"
            "The source creates a `DefaultModelMonitor` and asks it to suggest a baseline from a reference dataset.\n"
            "\n"
            "A simplified source-aligned shape is:\n"
            "\n"
            "```python\n"
            "from sagemaker.model_monitor import DefaultModelMonitor\n"
            "from sagemaker.model_monitor.dataset_format import DatasetFormat\n"
            "\n"
            "monitor = DefaultModelMonitor(\n"
            "    role=role,\n"
            "    instance_count=1,\n"
            "    instance_type=\"ml.m5.xlarge\",\n"
            ")\n"
            "\n"
            "monitor.suggest_baseline(\n"
            "    baseline_dataset=\"s3://.../training-dataset.csv\",\n"
            "    dataset_format=DatasetFormat.csv(header=True),\n"
            "    output_s3_uri=\"s3://.../baseline/\",\n"
            "    wait=True,\n"
            ")\n"
            "```\n"
            "\n"
            "The baseline job creates statistics and constraints that describe expected data properties.\n"
            "\n"
            "Examples shown in the chapter include inferred types, completeness, and non-negative-value constraints.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. AWS workflow step 3: schedule repeated comparisons\n"
            "\n"
            "After a baseline exists, the source creates a monitoring schedule.\n"
            "\n"
            "The scheduled job repeatedly compares captured endpoint traffic against the baseline.\n"
            "\n"
            "A simplified source-aligned shape is:\n"
            "\n"
            "```python\n"
            "from sagemaker.model_monitor import CronExpressionGenerator\n"
            "\n"
            "monitor.create_monitoring_schedule(\n"
            "    monitor_schedule_name=\"model-monitor-schedule\",\n"
            "    endpoint_input=predictor.endpoint_name,\n"
            "    statistics=monitor.baseline_statistics(),\n"
            "    constraints=monitor.suggested_constraints(),\n"
            "    schedule_cron_expression=CronExpressionGenerator.hourly(),\n"
            "    enable_cloudwatch_metrics=True,\n"
            ")\n"
            "```\n"
            "\n"
            "This turns drift monitoring from a one-time notebook experiment into a recurring operational process.\n"
            "\n"
            "[[IMAGE_NEEDED: SageMaker drift monitoring lifecycle | "
            "Endpoint traffic being captured to S3, a reference dataset creating baseline statistics and constraints, then an hourly monitor comparing traffic and sending metrics/reports | "
            "Learner should notice the three phases: capture, baseline, scheduled comparison]]\n"
            "\n"
            "{{exercise:M12.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 23. A violation is a signal to investigate, not automatically proof of model failure\n"
            "\n"
            "The source shows constraint-violation reports.\n"
            "\n"
            "One feature expected 100% integer-like values but observed roughly 99.7%.\n"
            "\n"
            "Another showed 0% where 100% was expected—a much more critical situation.\n"
            "\n"
            "This demonstrates two ideas:\n"
            "\n"
            "1. monitoring thresholds may need tuning so small harmless deviations do not create constant noise,\n"
            "2. severe violations can reveal broken data contracts quickly.\n"
            "\n"
            "Monitoring output requires interpretation.\n"
            "\n"
            "A threshold is not useful merely because it exists; it should distinguish actionable abnormal behavior from acceptable variation.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Azure ML uses the same baseline-target-monitor pattern\n"
            "\n"
            "The source presents Azure ML drift monitoring as conceptually similar to SageMaker.\n"
            "\n"
            "It requires:\n"
            "\n"
            "- a baseline dataset,\n"
            "- a target dataset,\n"
            "- a monitor configuration.\n"
            "\n"
            "The monitor compares newer data with the reference and can expose drift metrics and alerts.\n"
            "\n"
            "Azure's time-series dataset support allows the system to reason about how data changes across time windows.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Not every distribution change is a defect\n"
            "\n"
            "The chapter uses a swimsuit-sales example to make this point.\n"
            "\n"
            "If sales suddenly fall toward zero, that could indicate bad data.\n"
            "\n"
            "Or it could simply be winter.\n"
            "\n"
            "Likewise, Christmas-tree sales in August should not necessarily be compared with December as though the two periods were equivalent.\n"
            "\n"
            "Therefore drift interpretation requires domain knowledge.\n"
            "\n"
            "Potential causes named in the source include:\n"
            "\n"
            "- changes in value type/unit,\n"
            "- null or empty values,\n"
            "- legitimate seasonal shifts.\n"
            "\n"
            "A drift detector tells you that the data changed. It does not automatically tell you whether the change is bad.\n"
            "\n"
            "[[IMAGE_NEEDED: Harmful drift versus seasonal change | "
            "Two time-series examples: one showing a sudden schema/unit anomaly and one showing an expected seasonal sales cycle | "
            "Learner should notice that domain context determines whether distribution change is alarming]]\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Time-aware datasets make drift comparisons more useful\n"
            "\n"
            "The source describes configuring an Azure target dataset as a time series.\n"
            "\n"
            "The timestamp can come from:\n"
            "\n"
            "- an explicit timestamp column,\n"
            "- or a virtual column inferred from the storage path using a partition convention.\n"
            "\n"
            "For example, a path convention such as:\n"
            "\n"
            "```text\n"
            "/2021/10/14/dataset.csv\n"
            "```\n"
            "\n"
            "can encode the dataset date without requiring another physical column.\n"
            "\n"
            "The chapter calls this **configuration by convention**: when reliable structure can be inferred, reduce manual configuration.\n"
            "\n"
            "Less repeated configuration means less operational overhead.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Azure monitor configuration brings reference, target, schedule, and threshold together\n"
            "\n"
            "Once the target dataset is time-aware, the monitor can combine:\n"
            "\n"
            "- target dataset,\n"
            "- baseline dataset,\n"
            "- selected feature/time settings,\n"
            "- acceptable drift threshold,\n"
            "- monitoring schedule.\n"
            "\n"
            "The resulting monitoring interface can surface drift magnitude and identify which features changed most.\n"
            "\n"
            "For deeper operational analysis, the source points to Application Insights for logs and metrics associated with monitored systems.\n"
            "\n"
            "{{exercise:M12.L01.EX05}}\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Automation binds logging, monitoring, and MLOps together\n"
            "\n"
            "The final conclusion of the chapter is broader than any one cloud service.\n"
            "\n"
            "Logging and monitoring are only useful at scale if the information is captured reliably and made available without repeated manual effort.\n"
            "\n"
            "Automation should make it routine to:\n"
            "\n"
            "- emit useful logs,\n"
            "- capture key metrics,\n"
            "- collect serving data,\n"
            "- compare against baselines,\n"
            "- generate reports,\n"
            "- surface alerts,\n"
            "- support reproducible decisions.\n"
            "\n"
            "The strong foundation may not be the most exciting part of ML engineering, but it is what makes exceptional results repeatable.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: More logs automatically mean better observability\n"
            "\n"
            "Unclear or excessively noisy output can make diagnosis harder rather than easier.\n"
            "\n"
            "### Misconception 2: Infrastructure metrics are enough for ML systems\n"
            "\n"
            "CPU, memory, and disk can look healthy while product behavior, data quality, or model quality is failing.\n"
            "\n"
            "### Misconception 3: `print()` is equivalent to structured logging\n"
            "\n"
            "Logging provides severity levels, hierarchy, traceback support, routing, and configurable verbosity.\n"
            "\n"
            "### Misconception 4: Catching every exception with a generic message improves reliability\n"
            "\n"
            "It can hide the real failure context and make remote debugging much harder.\n"
            "\n"
            "### Misconception 5: DEBUG should always be enabled forever\n"
            "\n"
            "High verbosity is useful during early operation and investigation but can become noisy as systems mature.\n"
            "\n"
            "### Misconception 6: Drift means the model is definitely broken\n"
            "\n"
            "Distribution change can be legitimate, including seasonality. The signal needs domain interpretation.\n"
            "\n"
            "### Misconception 7: A baseline is the same thing as all future target data\n"
            "\n"
            "The baseline is the reference; target data is what is compared against it over time.\n"
            "\n"
            "### Misconception 8: A tiny constraint violation and a complete schema failure deserve the same response\n"
            "\n"
            "Thresholds and severity need tuning so monitoring remains actionable.\n"
            "\n"
            "### Misconception 9: Monitoring is only about dashboards for humans\n"
            "\n"
            "Observability signals can also feed automated alerts and infrastructure reactions such as scaling.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Logging | Emitting structured event information that helps explain application behavior. |\n"
            "| Monitoring | Repeatedly measuring system/model behavior so changes and problems can be detected. |\n"
            "| Observability | Broader ability to understand system state using logs, metrics, traces/signals, dashboards, and related evidence. |\n"
            "| Log level | Severity/verbosity category used to control which log messages are emitted. |\n"
            "| DEBUG | Most verbose common logging level in the chapter's ordering. |\n"
            "| INFO | Routine informational events. |\n"
            "| WARNING | Potential problem or unusual condition. |\n"
            "| ERROR | Failed operation or significant error condition. |\n"
            "| CRITICAL | Most severe common logging level in the chapter's ordering. |\n"
            "| Root logger | Parent logger whose configuration can affect loggers across an application and its libraries. |\n"
            "| Counter | Metric representing a count of events/items. |\n"
            "| Timer | Metric representing duration. |\n"
            "| Value | Metric representing an observed numeric/state measurement. |\n"
            "| Baseline | Reference statistics/constraints describing expected data behavior. |\n"
            "| Target data | Newer data being monitored and compared with the baseline. |\n"
            "| Data capture | Recording production endpoint inputs/outputs or related serving information for later analysis. |\n"
            "| Data drift | Change in data distribution or characteristics over time. |\n"
            "| Constraint violation | Monitored property falling outside the baseline expectation/threshold. |\n"
            "| Configuration by convention | Reducing explicit configuration by inferring reliable information from established structure such as paths. |\n"
            "| Bus test | Whether a process can continue if the person who usually performs it is suddenly unavailable. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. Why are logging and monitoring foundational to production ML?\n"
            "2. What makes a log message operationally useful?\n"
            "3. Why can infrastructure health remain normal while a critical product feature is broken?\n"
            "4. What new observability signals does MLOps add beyond ordinary software systems?\n"
            "5. What role does a cloud observability service such as CloudWatch play?\n"
            "6. What is the difference between an access log and an error log in the chapter's Nginx example?\n"
            "7. Why is `print()` difficult to use as a long-term logging strategy?\n"
            "8. What context did the CSV example add before reading the file?\n"
            "9. Why is a generic caught-exception message often harmful?\n"
            "10. What does `logger.exception()` preserve?\n"
            "11. List DEBUG, INFO, WARNING, ERROR, CRITICAL from most to least verbose.\n"
            "12. Why might new production code use a more verbose level initially?\n"
            "13. Why might a stable system later reduce verbosity?\n"
            "14. What is the root logger?\n"
            "15. Why can setting the root logger to DEBUG create noise?\n"
            "16. How can you suppress one noisy dependency without silencing your application?\n"
            "17. Why might one application send logs to more than one destination?\n"
            "18. What does the athletic-journal analogy teach about monitoring?\n"
            "19. What is the bus test?\n"
            "20. Why does monitoring need automation to pass the bus test?\n"
            "21. What does a counter measure?\n"
            "22. What does a timer measure?\n"
            "23. When is a value metric useful?\n"
            "24. Give one useful metric for data preparation.\n"
            "25. Give one useful metric for hosted inference.\n"
            "26. What is the difference between a baseline and target data?\n"
            "27. Why does serving-data capture matter for drift monitoring?\n"
            "28. Why must feature order/type expectations remain consistent?\n"
            "29. What does SageMaker's baseline-generation step produce conceptually?\n"
            "30. What is the purpose of a recurring monitoring schedule?\n"
            "31. Why do thresholds need tuning?\n"
            "32. Why is a 0% type match more alarming than a small deviation from 100%?\n"
            "33. What three core pieces appear in the Azure drift-monitoring pattern?\n"
            "34. Why can seasonality look like drift?\n"
            "35. What is configuration by convention in the Azure example?\n"
            "36. How can a time-series dataset improve drift analysis?\n"
            "37. Why is Application Insights useful in the Azure discussion?\n"
            "38. How does automation connect logging, monitoring, and drift detection?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A production ML system is only as trustworthy as its ability to explain what it is doing. "
            "Useful logs provide context, metrics make behavior comparable, monitoring turns those signals into ongoing evidence, "
            "and drift detection helps reveal when production data no longer matches the assumptions behind the model.**\n"
        ),

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-observability", "title": "Logging and monitoring are not optional production extras", "order": 1},
            {"id": "meaningful-logs", "title": "A log line should tell a story, not create another puzzle", "order": 2},
            {"id": "business-vs-system", "title": "CPU and disk metrics cannot tell you whether the product still works", "order": 3},
            {"id": "ml-specific-observability", "title": "MLOps adds data and model signals to ordinary software observability", "order": 4},
            {"id": "cloud-observability", "title": "Cloud observability systems centralize logs, metrics, alerts, and reactions", "order": 5},
            {"id": "logging-basics", "title": "Logging separates normal events from errors through levels and structure", "order": 6},
            {"id": "print-vs-logging", "title": "print() is not a production logging strategy", "order": 7},
            {"id": "python-logging-start", "title": "Add context before the failure happens", "order": 8},
            {"id": "logger-exception", "title": "Preserve the traceback with logger.exception()", "order": 9},
            {"id": "log-levels", "title": "Log levels control how much operational detail you see", "order": 10},
            {"id": "verbosity-lifecycle", "title": "Useful verbosity changes as software matures", "order": 11},
            {"id": "logger-hierarchy", "title": "Logger hierarchy lets you control your code and dependencies separately", "order": 12},
            {"id": "multiple-log-destinations", "title": "Different audiences may need different log destinations", "order": 13},
            {"id": "monitoring-journal", "title": "If you can measure, you can compare; if you can compare, you can improve", "order": 14},
            {"id": "bus-test", "title": "Metrics and automation reduce dependence on one person", "order": 15},
            {"id": "monitoring-scope", "title": "Model monitoring covers the whole path to production", "order": 16},
            {"id": "metric-types", "title": "Three basic metric types: counter, timer, value", "order": 17},
            {"id": "baseline-target", "title": "Drift monitoring needs a reference and something new to compare", "order": 18},
            {"id": "sagemaker-data-capture", "title": "AWS SageMaker workflow step 1: capture production data", "order": 19},
            {"id": "capture-contract", "title": "Monitoring data must still respect the model's expected input contract", "order": 20},
            {"id": "sagemaker-baseline", "title": "AWS workflow step 2: generate baseline statistics and constraints", "order": 21},
            {"id": "sagemaker-schedule", "title": "AWS workflow step 3: schedule repeated comparisons", "order": 22},
            {"id": "violations", "title": "A violation is a signal to investigate, not automatically proof of model failure", "order": 23},
            {"id": "azure-drift", "title": "Azure ML uses the same baseline-target-monitor pattern", "order": 24},
            {"id": "seasonality", "title": "Not every distribution change is a defect", "order": 25},
            {"id": "azure-time-series", "title": "Time-aware datasets make drift comparisons more useful", "order": 26},
            {"id": "azure-monitor", "title": "Azure monitor configuration brings reference, target, schedule, and threshold together", "order": 27},
            {"id": "automation-binds", "title": "Automation binds logging, monitoring, and MLOps together", "order": 28},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M12.L01.EX01",
            "title": "Design metrics across four monitoring layers",
            "lesson_code": "M12.L01",
            "section_id": "business-vs-system",
            "placement": "after_section",
            "description": (
                "Practice distinguishing infrastructure, application, ML, and business signals."
            ),
            "instructions": (
                "You operate a subscription website whose recommendation model promotes paid plans.\n\n"
                "Propose at least two metrics for each layer:\n"
                "1. infrastructure health,\n"
                "2. application health,\n"
                "3. ML/model health,\n"
                "4. business/product health.\n\n"
                "Then describe one failure where CPU and memory look normal but the product is still broken."
            ),
            "expected_output": (
                "Eight or more metrics organized by monitoring layer plus one cross-layer failure scenario."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "monitoring-design",
                "business-metrics",
                "model-monitoring",
                "observability",
            ],
        },

        {
            "id": "M12.L01.EX02",
            "title": "Replace brittle prints with useful Python logging",
            "lesson_code": "M12.L01",
            "section_id": "logger-exception",
            "placement": "after_section",
            "description": (
                "Convert a fragile data-processing script into a more diagnosable one."
            ),
            "instructions": (
                "A script loads a CSV file and currently uses `print()` for every message.\n\n"
                "Design a logging approach that includes:\n"
                "1. a named application logger,\n"
                "2. DEBUG output showing which file is being processed,\n"
                "3. INFO output for normal completion,\n"
                "4. `logger.exception()` when Pandas fails,\n"
                "5. a readable log format,\n"
                "6. an explanation of why this is better for a remote pipeline than a generic `print('failed')`."
            ),
            "expected_output": "A short Python logging design plus operational reasoning.",
            "type": "code",
            "language": "python",
            "starter_code": (
                "import logging\n\n"
                "logger = logging.getLogger(\"csv_processor\")\n\n"
                "def process_csv(path):\n"
                "    # TODO: log the path at DEBUG, successful completion at INFO,\n"
                "    # and preserve the traceback with logger.exception on failure.\n"
                "    pass\n"
            ),
            "solution_code": (
                "import logging\n\n"
                "logging.basicConfig(\n"
                "    level=logging.INFO,\n"
                "    format=\"%(asctime)s %(levelname)s %(name)s %(message)s\",\n"
                ")\n"
                "logger = logging.getLogger(\"csv_processor\")\n\n"
                "def process_csv(path):\n"
                "    logger.debug(\"Processing CSV file: %s\", path)\n"
                "    try:\n"
                "        rows = load_csv(path)\n"
                "        logger.info(\"Processed %s rows from %s\", len(rows), path)\n"
                "        return rows\n"
                "    except Exception:\n"
                "        logger.exception(\"Failed to process CSV file: %s\", path)\n"
                "        raise\n"
            ),
            "hint": "Use a named logger and put logger.exception() inside the except block.",
            "success_message": "Correct! The logger records context, normal completion, and the original failure traceback.",
            "tests": [
                {
                    "id": "process_function",
                    "type": "function_exists",
                    "function": "process_csv",
                    "static": True,
                    "feedback": {
                        "en": "Define a function named `process_csv`.",
                        "ar": "عرّف دالة باسم `process_csv`.",
                    },
                },
                {
                    "id": "debug_log",
                    "type": "function_called",
                    "function": "logger.debug",
                    "static": True,
                    "feedback": {
                        "en": "Log the file being processed with `logger.debug()`.",
                        "ar": "سجّل الملف الجاري معالجته باستخدام `logger.debug()`.",
                    },
                },
                {
                    "id": "info_log",
                    "type": "function_called",
                    "function": "logger.info",
                    "static": True,
                    "feedback": {
                        "en": "Use `logger.info()` for normal completion.",
                        "ar": "استخدم `logger.info()` عند اكتمال المعالجة بنجاح.",
                    },
                },
                {
                    "id": "exception_log",
                    "type": "function_called",
                    "function": "logger.exception",
                    "static": True,
                    "feedback": {
                        "en": "Use `logger.exception()` so the traceback is retained.",
                        "ar": "استخدم `logger.exception()` للاحتفاظ بتتبّع الخطأ.",
                    },
                },
                {
                    "id": "no_print",
                    "type": "function_not_called",
                    "function": "print",
                    "static": True,
                    "feedback": {
                        "en": "Replace generic `print()` calls with the named logger.",
                        "ar": "استبدل استدعاءات `print()` العامة بالـ logger المسمّى.",
                    },
                },
            ],
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "python-logging",
                "error-handling",
                "logger-exception",
                "diagnostics",
            ],
        },

        {
            "id": "M12.L01.EX03",
            "title": "Classify operational measurements",
            "lesson_code": "M12.L01",
            "section_id": "metric-types",
            "placement": "after_section",
            "description": (
                "Choose counter, timer, or value for real MLOps measurements."
            ),
            "instructions": (
                "Classify each measurement as primarily a counter, timer, or value and justify your answer:\n"
                "1. number of null records in a batch,\n"
                "2. time to preprocess one dataset,\n"
                "3. current database size in GB,\n"
                "4. number of HTTP 500 responses,\n"
                "5. model inference latency,\n"
                "6. current observed drift magnitude.\n\n"
                "Then add one metric of your own for model training."
            ),
            "expected_output": "Seven metric classifications with justification.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "metrics",
                "counters",
                "timers",
                "values",
            ],
        },

        {
            "id": "M12.L01.EX04",
            "title": "Design an AWS drift-monitoring workflow",
            "lesson_code": "M12.L01",
            "section_id": "sagemaker-schedule",
            "placement": "after_section",
            "description": (
                "Connect data capture, baseline generation, and scheduled monitoring."
            ),
            "instructions": (
                "Design the monitoring flow for a deployed churn endpoint.\n\n"
                "Include:\n"
                "1. where request data is captured,\n"
                "2. which dataset is used to create the baseline,\n"
                "3. what statistics/constraints represent,\n"
                "4. how often comparisons run,\n"
                "5. where reports/metrics are stored or surfaced,\n"
                "6. one small violation you might tolerate,\n"
                "7. one severe violation that should trigger immediate investigation."
            ),
            "expected_output": (
                "An end-to-end baseline-versus-production monitoring design consistent with the SageMaker example."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "sagemaker-model-monitor",
                "data-capture",
                "baseline",
                "drift-monitoring",
            ],
        },

        {
            "id": "M12.L01.EX05",
            "title": "Interpret drift with seasonality",
            "lesson_code": "M12.L01",
            "section_id": "azure-monitor",
            "placement": "after_section",
            "description": (
                "Separate real data-quality failures from expected distribution change."
            ),
            "instructions": (
                "An online retail dataset shows three changes:\n"
                "1. swimsuit sales fall sharply in winter,\n"
                "2. a temperature feature suddenly changes from values around 70–90 to values around 20–30,\n"
                "3. 15% of a previously complete customer-age column becomes null.\n\n"
                "For each change:\n"
                "- decide whether it might be natural drift or likely a data-quality issue,\n"
                "- explain what domain or schema context you need,\n"
                "- state whether you would compare against last month, the same season last year, or another baseline.\n\n"
                "Then explain why a time-aware Azure dataset helps."
            ),
            "expected_output": (
                "A contextual drift analysis that does not treat every distribution change as equally harmful."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "data-drift",
                "seasonality",
                "azure-ml",
                "monitoring-interpretation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M12.L01.QZ01",

        "title": "Monitoring and Logging for MLOps — Knowledge Check",

        "lesson_code": "M12.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M12.L01.Q01",
                "section_id": "why-observability",
                "question": "What is the most important purpose of useful logging and monitoring?",
                "options": [
                    "Produce as much output as possible.",
                    "Help people and systems understand the operational state and diagnose change or failure.",
                    "Replace model evaluation.",
                    "Eliminate all debugging.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter emphasizes understandable information that tells a story about system state."
                ),
            },

            {
                "id": "M12.L01.Q02",
                "section_id": "meaningful-logs",
                "question": "What was wrong with the cryptic log-message example in the source?",
                "options": [
                    "It contained too few hexadecimal characters.",
                    "It hid a simple operational meaning behind output that even an experienced user could not understand.",
                    "It had no IP address.",
                    "It was too short.",
                ],
                "correct": 1,
                "explanation": (
                    "A good log should make the failure easier to understand rather than require decoding."
                ),
            },

            {
                "id": "M12.L01.Q03",
                "section_id": "business-vs-system",
                "question": "Why can server CPU and memory metrics fail to detect a critical product outage?",
                "options": [
                    "Business functionality can break while infrastructure usage remains normal.",
                    "CPU metrics are always inaccurate.",
                    "Memory has no relationship to software.",
                    "Product failures always cause disk failure first.",
                ],
                "correct": 0,
                "explanation": (
                    "The subscribe-button example shows why business/application metrics are needed in addition to infrastructure metrics."
                ),
            },

            {
                "id": "M12.L01.Q04",
                "section_id": "cloud-observability",
                "question": "What is a central role of a cloud observability service such as CloudWatch?",
                "options": [
                    "Collect metrics/logs and feed dashboards, alerts, analysis, and automated actions.",
                    "Only store model weights.",
                    "Only train models.",
                    "Replace the application database.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter describes a central collection and action hub for cloud operational signals."
                ),
            },

            {
                "id": "M12.L01.Q05",
                "section_id": "logging-basics",
                "question": "Why are log levels useful?",
                "options": [
                    "They communicate severity/verbosity and let consumers filter operational information.",
                    "They encrypt log files.",
                    "They replace timestamps.",
                    "They guarantee no error can occur.",
                ],
                "correct": 0,
                "explanation": (
                    "The Nginx and Python examples use levels to distinguish routine information from errors."
                ),
            },

            {
                "id": "M12.L01.Q06",
                "section_id": "print-vs-logging",
                "question": "Which is an advantage of logging over ad hoc print statements?",
                "options": [
                    "Configurable severity and routing",
                    "Ability to preserve traceback information",
                    "Control over verbosity",
                    "All of the above",
                ],
                "correct": 3,
                "explanation": (
                    "The chapter demonstrates all of these capabilities."
                ),
            },

            {
                "id": "M12.L01.Q07",
                "section_id": "logger-exception",
                "question": "What does `logger.exception()` add in the CSV example?",
                "options": [
                    "Only a success message",
                    "An error message together with traceback information",
                    "A new CSV parser",
                    "Automatic data correction",
                ],
                "correct": 1,
                "explanation": (
                    "The traceback preserves the actual error context for later diagnosis."
                ),
            },

            {
                "id": "M12.L01.Q08",
                "section_id": "log-levels",
                "question": "Which ordering is correct from most verbose to least verbose / most severe?",
                "options": [
                    "DEBUG → INFO → WARNING → ERROR → CRITICAL",
                    "CRITICAL → ERROR → WARNING → INFO → DEBUG",
                    "INFO → DEBUG → ERROR → WARNING → CRITICAL",
                    "DEBUG → CRITICAL → INFO → ERROR → WARNING",
                ],
                "correct": 0,
                "explanation": (
                    "This is the ordering explicitly described in the source."
                ),
            },

            {
                "id": "M12.L01.Q09",
                "section_id": "verbosity-lifecycle",
                "question": "Why might a team reduce logging verbosity after a system matures?",
                "options": [
                    "Stable systems can generate excessive routine noise at DEBUG level.",
                    "Errors can no longer happen.",
                    "Logging is no longer useful.",
                    "Mature systems cannot change configuration.",
                ],
                "correct": 0,
                "explanation": (
                    "The source recommends adapting verbosity to the application's lifecycle."
                ),
            },

            {
                "id": "M12.L01.Q10",
                "section_id": "logger-hierarchy",
                "question": "What can happen when the root logger is set to DEBUG?",
                "options": [
                    "Third-party libraries may also emit detailed debug messages.",
                    "Only the application's custom logger changes.",
                    "All logging is disabled.",
                    "Python deletes dependency logs.",
                ],
                "correct": 0,
                "explanation": (
                    "The source's urllib3 example demonstrates this logger-hierarchy effect."
                ),
            },

            {
                "id": "M12.L01.Q11",
                "section_id": "multiple-log-destinations",
                "question": "Why might one application use multiple logging destinations?",
                "options": [
                    "Different audiences may need concise user-facing output versus detailed developer diagnostics.",
                    "Python only permits one message per destination.",
                    "It guarantees lower latency.",
                    "It prevents exceptions.",
                ],
                "correct": 0,
                "explanation": (
                    "The source gives terminal-versus-file logging as an example."
                ),
            },

            {
                "id": "M12.L01.Q12",
                "section_id": "monitoring-journal",
                "question": "What does the athletic-journal analogy teach?",
                "options": [
                    "Historical measurements make comparison and improvement possible.",
                    "Monitoring should only happen once.",
                    "Qualitative context is never useful.",
                    "Production systems should avoid history.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter's core idea is that measurable history supports comparison and planning."
                ),
            },

            {
                "id": "M12.L01.Q13",
                "section_id": "metric-types",
                "question": "Which metric type is most natural for the number of null values in a dataset?",
                "options": [
                    "Counter",
                    "Timer",
                    "Value only",
                    "Logger",
                ],
                "correct": 0,
                "explanation": (
                    "A counter records how many occurrences are observed."
                ),
            },

            {
                "id": "M12.L01.Q14",
                "section_id": "metric-types",
                "question": "Which metric type is most natural for HTTP prediction latency?",
                "options": [
                    "Counter",
                    "Timer",
                    "Only a log level",
                    "Baseline dataset",
                ],
                "correct": 1,
                "explanation": (
                    "A timer measures elapsed duration."
                ),
            },

            {
                "id": "M12.L01.Q15",
                "section_id": "baseline-target",
                "question": "What is the role of the baseline in drift monitoring?",
                "options": [
                    "Provide expected/reference statistics or constraints for comparison.",
                    "Replace all production data.",
                    "Train every future model automatically.",
                    "Store only logs.",
                ],
                "correct": 0,
                "explanation": (
                    "New target data is compared against the baseline reference."
                ),
            },

            {
                "id": "M12.L01.Q16",
                "section_id": "sagemaker-data-capture",
                "question": "Why enable data capture on a deployed SageMaker endpoint?",
                "options": [
                    "To preserve serving data that monitoring jobs can later analyze.",
                    "To prevent all predictions.",
                    "To replace the model registry.",
                    "To remove the need for a baseline.",
                ],
                "correct": 0,
                "explanation": (
                    "Captured traffic becomes the target data used by monitoring."
                ),
            },

            {
                "id": "M12.L01.Q17",
                "section_id": "capture-contract",
                "question": "Why must monitored data preserve expected feature order and schema?",
                "options": [
                    "Otherwise drift checks may compare the wrong meanings or detect a broken contract rather than meaningful behavior change.",
                    "Feature order never matters.",
                    "Monitoring systems ignore schema.",
                    "It only affects dashboards.",
                ],
                "correct": 0,
                "explanation": (
                    "A meaningful comparison depends on consistent feature interpretation."
                ),
            },

            {
                "id": "M12.L01.Q18",
                "section_id": "sagemaker-baseline",
                "question": "What does the baseline-generation step conceptually create?",
                "options": [
                    "Statistics and constraints representing expected data properties",
                    "A new user interface",
                    "A container image",
                    "A source-code linter",
                ],
                "correct": 0,
                "explanation": (
                    "The source shows files containing baseline statistics and constraints."
                ),
            },

            {
                "id": "M12.L01.Q19",
                "section_id": "sagemaker-schedule",
                "question": "What is the purpose of the monitoring schedule?",
                "options": [
                    "Repeatedly compare new captured data with the baseline.",
                    "Train the same model every minute.",
                    "Delete all reports.",
                    "Change feature order automatically.",
                ],
                "correct": 0,
                "explanation": (
                    "The schedule turns drift analysis into an ongoing operational process."
                ),
            },

            {
                "id": "M12.L01.Q20",
                "section_id": "violations",
                "question": "Why do monitoring thresholds need tuning?",
                "options": [
                    "Very small harmless deviations can otherwise create noisy violations.",
                    "Thresholds must always be zero.",
                    "Every deviation is catastrophic.",
                    "Monitoring cannot report severe problems.",
                ],
                "correct": 0,
                "explanation": (
                    "The source contrasts small deviations with a severe 0% match example."
                ),
            },

            {
                "id": "M12.L01.Q21",
                "section_id": "azure-drift",
                "question": "Which three components are central to the Azure drift workflow described?",
                "options": [
                    "Baseline dataset, target dataset, and monitor",
                    "Dockerfile, registry, and linter",
                    "GPU, CPU, and RAM",
                    "Only logs, no datasets",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly describes those three pieces working together."
                ),
            },

            {
                "id": "M12.L01.Q22",
                "section_id": "seasonality",
                "question": "Why is a distribution change in swimsuit sales not automatically evidence of bad data?",
                "options": [
                    "Seasonality can legitimately change the distribution.",
                    "Sales data can never drift.",
                    "Monitoring ignores time.",
                    "Drift only occurs in image data.",
                ],
                "correct": 0,
                "explanation": (
                    "The source uses seasonality to show why domain context matters."
                ),
            },

            {
                "id": "M12.L01.Q23",
                "section_id": "azure-time-series",
                "question": "What is configuration by convention in the Azure example?",
                "options": [
                    "Inferring timestamp information from a structured storage path rather than requiring extra manual configuration.",
                    "Removing all timestamps.",
                    "Using random path names.",
                    "Manually typing the same date twice.",
                ],
                "correct": 0,
                "explanation": (
                    "The source praises using partition-path structure to infer time information."
                ),
            },

            {
                "id": "M12.L01.Q24",
                "section_id": "automation-binds",
                "type": "open",
                "question": (
                    "Design an observability plan for a production classification endpoint. "
                    "Include meaningful application logs, log levels, at least one counter/timer/value metric, "
                    "infrastructure metrics, one business metric, serving-data capture, baseline creation, "
                    "a drift-monitoring schedule, alert interpretation, and how you would distinguish "
                    "natural seasonal change from a broken data pipeline."
                ),
            },
        ],

        "passing_score": 70,
    },
}
