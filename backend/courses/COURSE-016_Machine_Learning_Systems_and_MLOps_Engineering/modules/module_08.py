"""M08.L01 — Data Distribution Shifts and Monitoring.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 8, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M08.L01"

MODULE_ORDER = 8

MODULE_TITLE = "Data Distribution Shifts and Monitoring"

MODULE_DESCRIPTION = (
    "Learn why ML systems fail after deployment, how production data drifts away "
    "from training data, how edge cases and degenerate feedback loops emerge, and "
    "how monitoring and observability help detect and diagnose production problems."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Data Distribution Shifts and Monitoring",

    "slug": "ml-systems-design-m08-l01",

    "description": (
        "A production-focused lesson on ML system failures, data distribution "
        "shifts, edge cases, degenerate feedback loops, statistical drift "
        "detection, monitoring windows, model adaptation, operational and ML-specific "
        "metrics, logs, dashboards, alerts, and observability."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 4.0,

    "skill_tags": [
        "ml-monitoring",
        "production-failures",
        "silent-failure",
        "data-distribution-shift",
        "covariate-shift",
        "label-shift",
        "concept-drift",
        "edge-cases",
        "degenerate-feedback-loops",
        "train-serving-skew",
        "drift-detection",
        "two-sample-tests",
        "ks-test",
        "time-windows",
        "feature-monitoring",
        "prediction-monitoring",
        "observability",
        "logging",
        "distributed-tracing",
        "dashboards",
        "alerts",
        "telemetry",
        "slos",
        "slas",
    ],

    "prerequisite_ids": ["M07.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Data Distribution Shifts and Monitoring",

        "content": (
            "# Data Distribution Shifts and Monitoring\n"
            "\n"
            "> **Lesson:** M08.L01  \n"
            "> **Module:** Data Distribution Shifts and Monitoring  \n"
            "> **Source alignment:** Chapter 8. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why deployment is not the end of an ML system's lifecycle.\n"
            "- Distinguish operational failures from ML-performance failures.\n"
            "- Explain why ML systems can fail silently.\n"
            "- Identify common software-system and ML-specific failure modes.\n"
            "- Distinguish edge cases from statistical outliers.\n"
            "- Explain degenerate feedback loops and popularity/exposure bias.\n"
            "- Define source and target distributions.\n"
            "- Distinguish covariate shift, label shift, and concept drift.\n"
            "- Recognize feature and label-schema changes as additional production shifts.\n"
            "- Explain how summary statistics and two-sample tests can help detect drift.\n"
            "- Reason about sliding versus cumulative monitoring windows.\n"
            "- Explain several ways organizations respond to shifted distributions.\n"
            "- Distinguish monitoring, observability, instrumentation, and telemetry.\n"
            "- Choose useful operational and ML-specific monitoring metrics.\n"
            "- Explain the strengths and limitations of monitoring predictions, features, and raw inputs.\n"
            "- Design useful logs, dashboards, and alerts while avoiding alert fatigue.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. A deployed model can become wrong without breaking\n"
            "\n"
            "The chapter begins with an inventory forecasting system that worked well "
            "when deployed but became less useful over time. It began overestimating "
            "some products and underestimating others, causing expired inventory and "
            "lost sales.\n"
            "\n"
            "The lesson is fundamental:\n"
            "\n"
            "> **Deployment is not the end of the ML lifecycle.**\n"
            "\n"
            "A model exists inside a changing environment. User behavior, markets, "
            "products, application interfaces, data pipelines, and business processes "
            "can all change after training.\n"
            "\n"
            "Therefore a production system needs an ongoing loop:\n"
            "\n"
            "```text\n"
            "Deploy\n"
            "  ↓\n"
            "Monitor\n"
            "  ↓\n"
            "Detect degradation or anomalies\n"
            "  ↓\n"
            "Investigate root cause\n"
            "  ↓\n"
            "Update / retrain / fix system\n"
            "  ↓\n"
            "Deploy again\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Post-deployment ML lifecycle | "
            "A circular flow from deployment to monitoring, detection, diagnosis, "
            "correction/retraining, and redeployment | Learner should notice that "
            "production ML is a continuing feedback process rather than a final release]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. What counts as an ML system failure?\n"
            "\n"
            "A failure occurs when the system violates one or more expectations.\n"
            "\n"
            "For traditional software, expectations are often operational:\n"
            "\n"
            "- latency,\n"
            "- throughput,\n"
            "- availability,\n"
            "- successful responses,\n"
            "- resource usage.\n"
            "\n"
            "ML systems have these **plus predictive expectations**.\n"
            "\n"
            "Imagine an English-to-French translation service.\n"
            "\n"
            "Operational expectation:\n"
            "\n"
            "```text\n"
            "Return a response within 1 second.\n"
            "```\n"
            "\n"
            "ML-performance expectation:\n"
            "\n"
            "```text\n"
            "Return an accurate translation at the required quality level.\n"
            "```\n"
            "\n"
            "If the service times out, the failure is obvious. If it returns a fluent "
            "but incorrect translation, the service may appear healthy even though the "
            "ML behavior is wrong.\n"
            "\n"
            "This is why the chapter says ML systems often **fail silently**.\n"
            "\n"
            "[[IMAGE_NEEDED: Operational failure versus silent ML failure | "
            "Two examples: one request timing out with an obvious error, and one "
            "request returning a normal-looking but incorrect prediction | Learner "
            "should notice that ML failure can occur while software health looks normal]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Software failures versus ML-specific failures\n"
            "\n"
            "### Software-system failures\n"
            "\n"
            "These could happen in any software system:\n"
            "\n"
            "- dependency failure,\n"
            "- deployment of the wrong binary or model version,\n"
            "- permission errors,\n"
            "- hardware failures,\n"
            "- server downtime,\n"
            "- orchestration failures,\n"
            "- data-pipeline bugs.\n"
            "\n"
            "The chapter notes that many real ML pipeline failures come from ordinary "
            "software and distributed-system problems rather than the learning algorithm itself.\n"
            "\n"
            "### ML-specific failures\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- poor or changed data collection,\n"
            "- label problems,\n"
            "- unsuitable hyperparameters,\n"
            "- training-serving inconsistencies,\n"
            "- data distribution shifts,\n"
            "- edge cases,\n"
            "- degenerate feedback loops.\n"
            "\n"
            "The distinction matters because different failures require different debugging skills.\n"
            "\n"
            "{{exercise:M08.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Why production data differs from training data\n"
            "\n"
            "A model learns patterns from its training distribution and is expected "
            "to generalize to unseen production data.\n"
            "\n"
            "This assumes training and unseen data are sufficiently similar.\n"
            "\n"
            "In reality, this assumption often breaks for two reasons.\n"
            "\n"
            "### Reason 1: training data never perfectly represents reality\n"
            "\n"
            "Training data is finite. Real-world data is much broader and changes "
            "across users, devices, regions, encodings, behaviors, and contexts.\n"
            "\n"
            "Sampling and selection biases can therefore create a mismatch from the start.\n"
            "\n"
            "A development model can perform well on held-out test data yet fail after "
            "deployment because the real production population differs. The chapter "
            "uses **train-serving skew** for this kind of development-to-production mismatch.\n"
            "\n"
            "### Reason 2: the real world is not stationary\n"
            "\n"
            "Even if training data represented deployment well at launch, the environment "
            "can later change.\n"
            "\n"
            "Shifts can be:\n"
            "\n"
            "- sudden,\n"
            "- gradual,\n"
            "- seasonal or cyclic.\n"
            "\n"
            "Examples include pricing changes by competitors, launching in a new region, "
            "a celebrity driving unexpected traffic, gradual language changes, and seasonal "
            "changes in ride demand.\n"
            "\n"
            "### Not every apparent drift is real-world drift\n"
            "\n"
            "A monitoring dashboard may look as though data shifted when the actual cause is internal:\n"
            "\n"
            "- a broken preprocessing pipeline,\n"
            "- a feature becoming missing or NaN,\n"
            "- mismatched training and inference feature logic,\n"
            "- wrong standardization statistics,\n"
            "- the wrong model version,\n"
            "- an application-interface bug changing user behavior.\n"
            "\n"
            "So detecting a shift is only the first step. Root-cause analysis still matters.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Edge cases are performance failures, not merely unusual data\n"
            "\n"
            "The chapter makes a useful distinction between **outliers** and **edge cases**.\n"
            "\n"
            "**Outlier:** an example that differs significantly from other data points.  \n"
            "**Edge case:** an example on which the model performs significantly worse than normal.\n"
            "\n"
            "An outlier can be an edge case, but it does not have to be.\n"
            "\n"
            "Example:\n"
            "\n"
            "A pedestrian walking on a highway is unusual. If an autonomous vehicle "
            "detects and responds correctly, it is an outlier but not a model edge case.\n"
            "\n"
            "Edge cases matter most when their consequences are severe. A system with "
            "99.99% average success may still be unusable if the remaining 0.01% contains "
            "catastrophic failures.\n"
            "\n"
            "This principle applies to safety-critical systems such as medical or vehicle "
            "applications, but also to brand-sensitive systems such as chatbots that may "
            "occasionally produce highly offensive outputs.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Degenerate feedback loops\n"
            "\n"
            "A **degenerate feedback loop** occurs when a system's output changes the "
            "future data that will later train or evaluate the same system.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Model prediction\n"
            "      ↓\n"
            "Changes what users see\n"
            "      ↓\n"
            "Changes what users click / buy / interact with\n"
            "      ↓\n"
            "Those interactions become new training data\n"
            "      ↓\n"
            "Future model reinforces the original prediction pattern\n"
            "```\n"
            "\n"
            "### Recommendation example\n"
            "\n"
            "Suppose songs A and B are initially almost equally relevant, but A is ranked "
            "slightly higher. Because A appears first, users see and click it more. Those "
            "clicks become evidence that A is better, so future versions rank it even higher.\n"
            "\n"
            "Over time, a tiny initial difference can become a large popularity gap.\n"
            "\n"
            "Related ideas include:\n"
            "\n"
            "- exposure bias,\n"
            "- popularity bias,\n"
            "- filter bubbles,\n"
            "- echo chambers.\n"
            "\n"
            "### Hiring example\n"
            "\n"
            "If a resume model favors a feature and recruiters only interview recommended "
            "candidates, future training data may contain disproportionately more successful "
            "candidates with that feature. The model can then reinforce the original preference.\n"
            "\n"
            "[[IMAGE_NEEDED: Degenerate recommendation feedback loop | "
            "Two items begin with nearly equal scores, one is ranked slightly higher, "
            "receives more exposure and clicks, then receives a larger future score | "
            "Learner should notice how model outputs can change future training data]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Detecting and correcting degenerate feedback loops\n"
            "\n"
            "### Detect popularity concentration\n"
            "\n"
            "For recommenders, measure how diverse the outputs are across popular and "
            "long-tail items.\n"
            "\n"
            "If recommendations become increasingly concentrated on already-popular items, "
            "the system may be reinforcing its own exposure patterns.\n"
            "\n"
            "One approach described in the chapter is to bucket items by historical popularity "
            "and compare recommendation quality across those buckets. If performance is much "
            "better for popular items, popularity bias may be present.\n"
            "\n"
            "### Correction method 1: randomization\n"
            "\n"
            "Expose users to some randomly chosen items so the system can gather less-biased "
            "feedback about items it would not normally rank highly.\n"
            "\n"
            "The trade-off is user experience: too much random exploration can reduce relevance.\n"
            "\n"
            "### Correction method 2: positional features\n"
            "\n"
            "User feedback depends on where an item is shown. The first result may receive "
            "more clicks simply because it is first.\n"
            "\n"
            "Adding position as a feature helps the model separate **item quality** from "
            "**exposure advantage**.\n"
            "\n"
            "The chapter also describes a more sophisticated two-model idea:\n"
            "\n"
            "1. model the probability that the user actually sees/considers the item,\n"
            "2. model the probability of clicking given that the user saw it.\n"
            "\n"
            "This separates position-driven exposure from user preference.\n"
            "\n"
            "[[IMAGE_NEEDED: Position bias correction | "
            "A ranked recommendation list where top position affects probability of "
            "being seen, followed by a two-stage model separating 'seen/considered' "
            "from 'clicked given seen' | Learner should notice that clicks combine "
            "item preference with exposure position]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Source and target distributions\n"
            "\n"
            "The distribution used for training is the **source distribution**.  \n"
            "The distribution encountered during inference is the **target distribution**.\n"
            "\n"
            "In supervised learning, let:\n"
            "\n"
            "- `X` be model inputs,\n"
            "- `Y` be outputs or labels.\n"
            "\n"
            "The joint distribution can be decomposed as:\n"
            "\n"
            "```text\n"
            "P(X, Y) = P(Y|X) P(X)\n"
            "```\n"
            "\n"
            "or:\n"
            "\n"
            "```text\n"
            "P(X, Y) = P(X|Y) P(Y)\n"
            "```\n"
            "\n"
            "These decompositions help define three shift types:\n"
            "\n"
            "| Shift | What changes? | What stays fixed in the definition? |\n"
            "|---|---|---|\n"
            "| Covariate shift | `P(X)` | `P(Y|X)` |\n"
            "| Label shift | `P(Y)` | `P(X|Y)` |\n"
            "| Concept drift | `P(Y|X)` | `P(X)` |\n"
            "\n"
            "[[IMAGE_NEEDED: Covariate shift, label shift, and concept drift | "
            "Three panels showing changes to P(X), P(Y), and P(Y|X), with the "
            "unchanged conditional or marginal distribution noted in each case | "
            "Learner should notice that 'data drift' is not one single mathematical phenomenon]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Covariate shift: the input distribution changes\n"
            "\n"
            "Covariate shift occurs when:\n"
            "\n"
            "```text\n"
            "P(X) changes\n"
            "P(Y|X) stays the same\n"
            "```\n"
            "\n"
            "Example from the chapter:\n"
            "\n"
            "A breast-cancer dataset may contain more women over 40 than the deployment "
            "population. The age distribution changes between training and production, "
            "but for a given age group, the probability relationship between age and "
            "cancer is assumed unchanged.\n"
            "\n"
            "Covariate shift can arise from:\n"
            "\n"
            "- sample-selection bias,\n"
            "- deliberately oversampling rare classes,\n"
            "- active learning changing which inputs are selected,\n"
            "- a product attracting a new user population,\n"
            "- environmental changes.\n"
            "\n"
            "If the target input distribution were known in advance, training examples "
            "could be reweighted using a density ratio. In production, however, future "
            "shifts are usually not known in advance.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Label shift: the output distribution changes\n"
            "\n"
            "Label shift occurs when:\n"
            "\n"
            "```text\n"
            "P(Y) changes\n"
            "P(X|Y) stays the same\n"
            "```\n"
            "\n"
            "It is also called prior shift, prior-probability shift, or target shift.\n"
            "\n"
            "For example, the overall rate of a positive diagnosis may change between "
            "training and deployment even if the feature distribution among people with "
            "that diagnosis remains similar.\n"
            "\n"
            "The chapter also points out that covariate and label shift can happen together. "
            "Real production shifts do not need to fit neatly into exactly one category.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Concept drift: the relationship changes\n"
            "\n"
            "Concept drift occurs when:\n"
            "\n"
            "```text\n"
            "P(Y|X) changes\n"
            "P(X) stays the same\n"
            "```\n"
            "\n"
            "Think of this as:\n"
            "\n"
            "> **same kind of input, different expected output.**\n"
            "\n"
            "The source uses housing prices as an example. The physical features of an "
            "apartment may remain the same, but a market disruption can change the expected "
            "price associated with those features.\n"
            "\n"
            "Concept drift may also be cyclic or seasonal. Ride prices and travel demand, "
            "for example, can behave differently on weekdays, weekends, or holidays.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Other important production shifts\n"
            "\n"
            "Not every harmful production change fits perfectly into the three classical categories.\n"
            "\n"
            "### Feature changes\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- adding a new feature,\n"
            "- removing an old feature,\n"
            "- changing units,\n"
            "- changing allowed values,\n"
            "- a pipeline bug converting a feature to NaN.\n"
            "\n"
            "A feature changing from age in years to age in months dramatically changes "
            "its numerical distribution even if the semantic idea is similar.\n"
            "\n"
            "### Label-schema changes\n"
            "\n"
            "The structure or set of possible labels can change.\n"
            "\n"
            "Regression example:\n"
            "\n"
            "- old credit-score range: 300–850,\n"
            "- new score range: 250–900.\n"
            "\n"
            "Classification example:\n"
            "\n"
            "```text\n"
            "Old sentiment labels:\n"
            "POSITIVE / NEGATIVE / NEUTRAL\n"
            "\n"
            "New labels:\n"
            "POSITIVE / SAD / ANGRY / NEUTRAL\n"
            "```\n"
            "\n"
            "A label-schema change can require relabeling data and changing the model's output structure.\n"
            "\n"
            "{{exercise:M08.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Detecting distribution shifts\n"
            "\n"
            "The most direct signal of harmful shift is a change in the model's real performance.\n"
            "\n"
            "If ground-truth labels arrive quickly enough, monitor metrics such as:\n"
            "\n"
            "- accuracy,\n"
            "- F1,\n"
            "- recall,\n"
            "- AUC-ROC,\n"
            "- task-specific business or quality metrics.\n"
            "\n"
            "A decrease should trigger investigation. Unexpected increases or unusual fluctuations "
            "can also be worth investigating.\n"
            "\n"
            "The main production difficulty is that labels may be unavailable or delayed.\n"
            "\n"
            "When labels are not available, teams often monitor quantities that do not require them, "
            "especially the input-feature distribution `P(X)` and the prediction distribution.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Statistical methods for drift detection\n"
            "\n"
            "### Summary statistics\n"
            "\n"
            "Compare source and target statistics such as:\n"
            "\n"
            "- minimum,\n"
            "- maximum,\n"
            "- mean,\n"
            "- median,\n"
            "- variance,\n"
            "- quantiles,\n"
            "- skewness,\n"
            "- kurtosis.\n"
            "\n"
            "These are easy to compute and useful as a first check.\n"
            "\n"
            "However:\n"
            "\n"
            "> Similar summary statistics do **not** prove two distributions are the same.\n"
            "\n"
            "### Two-sample tests\n"
            "\n"
            "A two-sample hypothesis test asks whether two data samples are likely to have "
            "come from the same underlying distribution.\n"
            "\n"
            "A statistically significant difference suggests the observed difference is unlikely "
            "to be explained only by ordinary sampling variation.\n"
            "\n"
            "But statistical significance is not identical to practical importance. With huge "
            "sample sizes, very small differences can become statistically detectable.\n"
            "\n"
            "### Kolmogorov-Smirnov test\n"
            "\n"
            "The chapter describes the KS test as a nonparametric two-sample test that does not "
            "assume a particular underlying distribution.\n"
            "\n"
            "Its major limitation here is dimensionality: it is designed for one-dimensional data.\n"
            "\n"
            "Predictions or scalar labels can fit this setting. High-dimensional feature vectors do not.\n"
            "\n"
            "The source also mentions methods such as Least-Squares Density Difference and Maximum "
            "Mean Discrepancy (MMD), while noting that research techniques are not always widely "
            "adopted in production.\n"
            "\n"
            "Because many statistical tests work better in lower-dimensional spaces, dimensionality "
            "reduction may be useful before testing high-dimensional data.\n"
            "\n"
            "[[IMAGE_NEEDED: Drift detection from source to target distributions | "
            "Two overlaid feature distributions with summary-statistic comparison and "
            "a two-sample test indicator | Learner should notice the difference between "
            "simple summary monitoring and a formal statistical comparison]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Time windows change what drift you can see\n"
            "\n"
            "Temporal drift detection depends strongly on the comparison window.\n"
            "\n"
            "If data follows a weekly cycle, comparing only a short window can make normal "
            "seasonality look like drift.\n"
            "\n"
            "The shorter the monitoring window:\n"
            "\n"
            "- the faster changes can be detected,\n"
            "- but the more sensitive the system becomes to noise and false alarms.\n"
            "\n"
            "The longer the monitoring window:\n"
            "\n"
            "- the smoother and more stable the estimates,\n"
            "- but the easier it is to hide a short-lived failure.\n"
            "\n"
            "### Sliding statistics\n"
            "\n"
            "Computed only over a recent fixed window, such as the last hour.\n"
            "\n"
            "### Cumulative statistics\n"
            "\n"
            "Aggregate all data seen so far.\n"
            "\n"
            "Cumulative metrics can hide sharp recent failures because earlier healthy history "
            "dominates the aggregate.\n"
            "\n"
            "[[IMAGE_NEEDED: Sliding versus cumulative monitoring metrics | "
            "A time series with a sudden performance drop, alongside a responsive sliding "
            "metric and a smoother cumulative metric that barely moves | Learner should notice "
            "how cumulative statistics can hide recent incidents]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. How systems respond to data shifts\n"
            "\n"
            "Detecting drift does not automatically fix it.\n"
            "\n"
            "The chapter describes three broad approaches.\n"
            "\n"
            "### Approach 1: train on very broad data\n"
            "\n"
            "Use a large and diverse training distribution in the hope that future production "
            "examples still fall within patterns the model has learned.\n"
            "\n"
            "### Approach 2: adapt without target labels\n"
            "\n"
            "Research methods attempt unsupervised or weakly supervised domain adaptation. "
            "The chapter notes that such approaches have had limited industry adoption.\n"
            "\n"
            "### Approach 3: retrain using target-distribution data\n"
            "\n"
            "This is the common industry response when reliable new labels can be obtained.\n"
            "\n"
            "Retraining choices include:\n"
            "\n"
            "- train from scratch on old + new data,\n"
            "- continue training from the previous checkpoint,\n"
            "- use recent data only,\n"
            "- use data since the shift began,\n"
            "- use a longer historical window.\n"
            "\n"
            "The best strategy is empirical and depends on the application.\n"
            "\n"
            "### Design for stability\n"
            "\n"
            "Some features drift faster than others. A rapidly changing high-accuracy feature "
            "may force frequent retraining, while a coarser but more stable feature can reduce "
            "maintenance cost.\n"
            "\n"
            "System decomposition can also help. If one market changes quickly and another slowly, "
            "separate models can allow independent update schedules.\n"
            "\n"
            "And remember: if the apparent degradation comes from a software or human error, the "
            "solution is to fix that error—not to apply an ML adaptation technique.\n"
            "\n"
            "{{exercise:M08.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Monitoring, observability, instrumentation, and telemetry\n"
            "\n"
            "**Monitoring** is the act of measuring, tracking, and logging signals that help "
            "you determine whether something is wrong.\n"
            "\n"
            "**Observability** is the system property that gives you enough visibility to "
            "investigate *what* went wrong and *why*.\n"
            "\n"
            "**Instrumentation** is the work of adding the signals that make the system observable.\n"
            "\n"
            "Examples of instrumentation include:\n"
            "\n"
            "- timing functions,\n"
            "- counting NaN values,\n"
            "- tracking how inputs change across processing stages,\n"
            "- recording unusually long inputs,\n"
            "- attaching IDs and metadata to requests.\n"
            "\n"
            "**Telemetry** is runtime data collected from components, including remote services "
            "or user devices.\n"
            "\n"
            "A useful way to remember the relationship is:\n"
            "\n"
            "```text\n"
            "Instrumentation creates telemetry\n"
            "Telemetry feeds monitoring\n"
            "Good telemetry + structure create observability\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Monitor operational health first\n"
            "\n"
            "ML systems are still software systems, so ordinary production metrics remain essential.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- request latency,\n"
            "- throughput,\n"
            "- prediction request count,\n"
            "- HTTP success rate,\n"
            "- CPU/GPU utilization,\n"
            "- memory utilization,\n"
            "- service availability.\n"
            "\n"
            "### SLOs and SLAs\n"
            "\n"
            "A service can define what 'healthy' means using service-level objectives or agreements.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Median latency < 200 ms\n"
            "99th percentile latency < 2 seconds\n"
            "```\n"
            "\n"
            "An uptime target such as 99.99% leaves only a few minutes of allowable downtime per month.\n"
            "\n"
            "But uptime is not enough for ML:\n"
            "\n"
            "> A prediction service can be fully available and still return useless predictions.\n"
            "\n"
            "So operational monitoring must be complemented by ML-specific monitoring.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Four ML artifacts to monitor\n"
            "\n"
            "The chapter groups ML-specific monitoring into four artifacts:\n"
            "\n"
            "1. accuracy-related metrics,\n"
            "2. predictions,\n"
            "3. features,\n"
            "4. raw inputs.\n"
            "\n"
            "These lie at different depths of the ML pipeline.\n"
            "\n"
            "Raw inputs are closest to reality but can be messy and difficult to monitor. "
            "Predictions are highly structured and easy to inspect but provide less direct "
            "information about where upstream problems began.\n"
            "\n"
            "[[IMAGE_NEEDED: Four monitoring layers in an ML pipeline | "
            "A pipeline from raw inputs to transformed features to predictions to "
            "accuracy/feedback metrics, with monitoring attached at each layer | "
            "Learner should notice the trade-off between upstream root-cause visibility "
            "and downstream monitoring simplicity]]\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Monitoring accuracy-related metrics and user feedback\n"
            "\n"
            "If production feedback can provide natural labels, log it.\n"
            "\n"
            "Useful signals may include:\n"
            "\n"
            "- clicks,\n"
            "- purchases,\n"
            "- hides,\n"
            "- upvotes/downvotes,\n"
            "- favorites,\n"
            "- shares,\n"
            "- completion rate,\n"
            "- explicit corrections.\n"
            "\n"
            "When those signals can approximate ground truth, they can be used to calculate "
            "production performance metrics.\n"
            "\n"
            "Even when feedback is not a direct label, changes can reveal degradation.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Click-through rate: stable\n"
            "Video completion rate: falling\n"
            "```\n"
            "\n"
            "The recommendation system may still attract clicks while recommending less satisfying content.\n"
            "\n"
            "Systems can also deliberately collect feedback—for example, letting users upvote or downvote an output.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Monitoring prediction distributions\n"
            "\n"
            "Predictions are one of the easiest artifacts to monitor because they are often low-dimensional.\n"
            "\n"
            "For regression, a prediction is usually a scalar. For classification, it may be a class "
            "or a small probability vector.\n"
            "\n"
            "Useful checks include:\n"
            "\n"
            "- mean/median predicted value,\n"
            "- class frequency,\n"
            "- score quantiles,\n"
            "- unusual runs such as many identical outputs,\n"
            "- two-sample tests between historical and recent predictions.\n"
            "\n"
            "If the model parameters are unchanged, a shift in prediction distribution can act as a proxy "
            "for a shift in the inputs.\n"
            "\n"
            "Prediction monitoring is especially valuable when real labels arrive slowly. A model predicting "
            "only `False` for ten minutes can be detected immediately, long before enough labels arrive to compute accuracy.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Monitoring features and schema validity\n"
            "\n"
            "Features are structured enough to support strong validation rules.\n"
            "\n"
            "Possible checks include:\n"
            "\n"
            "- min/max/median within an acceptable range,\n"
            "- values matching a required regular expression,\n"
            "- categories belonging to an approved set,\n"
            "- cross-feature relationships remaining valid,\n"
            "- missing-value and NaN rates,\n"
            "- distribution comparisons over time.\n"
            "\n"
            "Feature validation is sometimes described as **table testing** or **unit testing for data**.\n"
            "\n"
            "### Four practical challenges\n"
            "\n"
            "#### 1. Monitoring cost\n"
            "\n"
            "Hundreds of models multiplied by hundreds or thousands of features produces an enormous number "
            "of statistics to compute and store.\n"
            "\n"
            "#### 2. Alert fatigue\n"
            "\n"
            "Features drift frequently, and many changes do not hurt model performance. Alerting on every minor "
            "shift creates false positives until people stop paying attention.\n"
            "\n"
            "#### 3. Root-cause ambiguity\n"
            "\n"
            "A feature may change because the real input changed—or because a preprocessing step broke.\n"
            "\n"
            "#### 4. Schema evolution\n"
            "\n"
            "If schemas change over time without versioning, monitoring can mistake an expected schema migration "
            "for an unexpected distribution shift.\n"
            "\n"
            "[[IMAGE_NEEDED: Feature monitoring with schema and drift checks | "
            "A tabular feature set with range checks, category checks, missing-value checks, "
            "and distribution comparisons, followed by alerts filtered by model impact | "
            "Learner should notice that feature drift alone does not prove model degradation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Monitoring raw inputs\n"
            "\n"
            "Monitoring raw inputs can help distinguish true world changes from errors introduced by preprocessing.\n"
            "\n"
            "But raw input monitoring is difficult because raw data may:\n"
            "\n"
            "- come from many sources,\n"
            "- use different formats,\n"
            "- have little shared structure,\n"
            "- be controlled by a separate data-platform team,\n"
            "- be unavailable directly to ML engineers.\n"
            "\n"
            "The chapter therefore treats raw-input monitoring as an important but often organizationally separate concern.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Logs and distributed tracing\n"
            "\n"
            "Logs record runtime events that may later matter for diagnosis.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- container start and stop events,\n"
            "- function calls,\n"
            "- execution duration,\n"
            "- inputs and outputs,\n"
            "- crashes,\n"
            "- stack traces,\n"
            "- resource usage,\n"
            "- error codes.\n"
            "\n"
            "Modern systems may contain many services, so identifying *where* an error happened can be harder than "
            "knowing that an error happened.\n"
            "\n"
            "### Distributed tracing\n"
            "\n"
            "Give a request or process a unique identifier and propagate it through the system. Log metadata such as:\n"
            "\n"
            "- timestamp,\n"
            "- service,\n"
            "- function,\n"
            "- user or request identity where appropriate,\n"
            "- upstream/downstream calls.\n"
            "\n"
            "When a failure occurs, the identifier lets engineers reconstruct the request's path across services.\n"
            "\n"
            "### Batch versus streaming log analysis\n"
            "\n"
            "Logs can be processed periodically for high throughput, but that delays problem detection.\n"
            "\n"
            "For near-real-time anomaly detection, logs can flow through real-time transports and stream-processing systems.\n"
            "\n"
            "[[IMAGE_NEEDED: Distributed tracing across microservices | "
            "One request ID traveling through several services with timestamps and logs at each hop | "
            "Learner should notice how a shared trace identifier reconstructs the path of one request]]\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Dashboards and alerts\n"
            "\n"
            "### Dashboards\n"
            "\n"
            "Dashboards make numerical trends easier to inspect and make monitoring accessible to both engineers "
            "and nonengineering stakeholders.\n"
            "\n"
            "But a graph does not explain itself. Statistical understanding and domain context are still needed.\n"
            "\n"
            "Too many graphs also create **dashboard rot**: the dashboard becomes cluttered with low-value metrics "
            "that nobody uses.\n"
            "\n"
            "### Alerts\n"
            "\n"
            "A useful alert has three parts.\n"
            "\n"
            "#### 1. Alert policy\n"
            "\n"
            "The condition that triggers the alert.\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "Model accuracy below 90%\n"
            "```\n"
            "\n"
            "or:\n"
            "\n"
            "```text\n"
            "HTTP latency > 1 second for at least 10 minutes\n"
            "```\n"
            "\n"
            "#### 2. Notification channel\n"
            "\n"
            "Who should receive it and through which system?\n"
            "\n"
            "#### 3. Description and action\n"
            "\n"
            "The alert should explain what happened, where, when, and ideally link to a **runbook** describing routine "
            "mitigation and diagnostic steps.\n"
            "\n"
            "### Alert fatigue\n"
            "\n"
            "Too many low-value alerts train people to ignore the system. Alert policies should focus attention on signals "
            "that require human action.\n"
            "\n"
            "{{exercise:M08.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Observability: make the system explainable at runtime\n"
            "\n"
            "Monitoring tells you **that** something suspicious happened.\n"
            "\n"
            "Observability aims to give you enough runtime information to investigate **why**.\n"
            "\n"
            "In a well-instrumented system, engineers should be able to ask detailed questions such as:\n"
            "\n"
            "- Which users received incorrect predictions in the last hour?\n"
            "- Which regions or device types are affected?\n"
            "- Which requests were outliers in the last ten minutes?\n"
            "- What intermediate feature values did one problematic request produce?\n"
            "- Which feature contributed most to recent incorrect predictions?\n"
            "\n"
            "Answering these questions requires logs and metrics with useful metadata and tags so they can be sliced "
            "across time, users, services, features, and model versions.\n"
            "\n"
            "The chapter connects observability with model interpretability:\n"
            "\n"
            "- **interpretability** helps explain what the model is doing,\n"
            "- **observability** helps explain what the entire ML system is doing.\n"
            "\n"
            "Monitoring is powerful but passive. It detects and helps diagnose a problem; it does not itself adapt the model.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: If the API is up, the ML system is healthy\n"
            "\n"
            "Operational availability does not guarantee prediction quality.\n"
            "\n"
            "### Misconception 2: Every feature shift is a model failure\n"
            "\n"
            "Many feature changes are benign. Drift matters when it meaningfully affects system behavior or indicates another problem.\n"
            "\n"
            "### Misconception 3: Any unusual input is an edge case\n"
            "\n"
            "An outlier is unusual data; an edge case is an input on which model performance is unusually poor.\n"
            "\n"
            "### Misconception 4: Feedback data is unbiased ground truth\n"
            "\n"
            "Model outputs influence what users see, which can influence the feedback later used as training data.\n"
            "\n"
            "### Misconception 5: Summary statistics can prove that no drift occurred\n"
            "\n"
            "Similar mean, variance, or quantiles do not guarantee identical distributions.\n"
            "\n"
            "### Misconception 6: Statistical significance means operational importance\n"
            "\n"
            "A very small difference can become statistically significant with enough data while still being irrelevant to model quality.\n"
            "\n"
            "### Misconception 7: Cumulative metrics are always safer than sliding metrics\n"
            "\n"
            "Cumulative history can hide recent degradation.\n"
            "\n"
            "### Misconception 8: Monitoring fixes drift\n"
            "\n"
            "Monitoring detects signals and supports diagnosis. Fixing the system may require software repair, retraining, adaptation, "
            "data collection, or another intervention.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Silent failure | ML-quality failure that occurs while the software continues to return normal-looking outputs. |\n"
            "| Train-serving skew | Mismatch between development/training conditions and production serving conditions. |\n"
            "| Outlier | Data example that differs significantly from other examples. |\n"
            "| Edge case | Example on which model performance is significantly worse than normal. |\n"
            "| Degenerate feedback loop | Loop where model outputs influence future inputs or training data and reinforce themselves. |\n"
            "| Exposure bias | Bias caused by some items receiving more opportunity to be seen than others. |\n"
            "| Source distribution | Distribution from which training data is drawn. |\n"
            "| Target distribution | Distribution encountered during inference. |\n"
            "| Covariate shift | Change in `P(X)` while `P(Y|X)` remains fixed by definition. |\n"
            "| Label shift | Change in `P(Y)` while `P(X|Y)` remains fixed by definition. |\n"
            "| Concept drift | Change in `P(Y|X)` while `P(X)` remains fixed by definition. |\n"
            "| Label-schema change | Change in the allowed structure, range, or classes of labels. |\n"
            "| Two-sample test | Statistical test for whether two samples likely come from the same distribution. |\n"
            "| KS test | Nonparametric one-dimensional two-sample test discussed in the chapter. |\n"
            "| Sliding statistic | Metric computed only over a recent fixed-size time window. |\n"
            "| Cumulative statistic | Metric aggregated over all observations collected so far. |\n"
            "| Monitoring | Measuring, tracking, and logging signals to detect problems. |\n"
            "| Observability | Ability to infer and investigate internal system behavior from runtime outputs. |\n"
            "| Instrumentation | Adding the measurements and metadata needed for runtime visibility. |\n"
            "| Telemetry | Runtime measurements collected from components or remote systems. |\n"
            "| SLO | Service-level objective defining a target level of service health. |\n"
            "| SLA | Service-level agreement that may include explicit guarantees and consequences. |\n"
            "| Distributed tracing | Tracking one request across multiple services using shared identifiers and metadata. |\n"
            "| Alert fatigue | Desensitization caused by too many low-value or false-positive alerts. |\n"
            "| Runbook | Documented routine steps for diagnosing or mitigating an operational incident. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. Why does deployment not mark the end of an ML system's lifecycle?\n"
            "2. What is the difference between an operational failure and an ML-performance failure?\n"
            "3. Why are ML systems described as failing silently?\n"
            "4. Name four ordinary software failures that can break an ML system.\n"
            "5. How can training-serving skew arise before the real world even changes?\n"
            "6. What is the difference between an outlier and an edge case?\n"
            "7. How can a recommender create a degenerate feedback loop?\n"
            "8. How can randomization help break popularity bias?\n"
            "9. Why can position itself become a useful feature when modeling clicks?\n"
            "10. What are source and target distributions?\n"
            "11. Define covariate shift mathematically.\n"
            "12. Define label shift mathematically.\n"
            "13. Define concept drift mathematically.\n"
            "14. What is a label-schema change?\n"
            "15. Why are ground-truth labels especially valuable for drift monitoring?\n"
            "16. Why are summary statistics an incomplete drift detector?\n"
            "17. What limitation does the KS test have for typical feature spaces?\n"
            "18. Why does time-window size affect drift detection?\n"
            "19. How can cumulative metrics hide incidents?\n"
            "20. What are three broad responses to shifted distributions?\n"
            "21. Why might feature stability matter when choosing production features?\n"
            "22. How does monitoring differ from observability?\n"
            "23. What is instrumentation?\n"
            "24. Why must operational metrics be monitored even for an excellent ML model?\n"
            "25. What four ML artifacts does the chapter recommend monitoring?\n"
            "26. Why are predictions easier to monitor than raw inputs?\n"
            "27. Why can feature monitoring create alert fatigue?\n"
            "28. How does distributed tracing help debug a multi-service request?\n"
            "29. What three components make up a useful alert?\n"
            "30. Why does observability require well-tagged fine-grained telemetry?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A production ML system is healthy only when both the software and the "
            "model remain healthy. Because the world, data, pipelines, and user behavior "
            "change, you need monitoring to detect degradation and observability to trace "
            "that degradation back to a cause before deciding how to fix it.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-monitor", "title": "A deployed model can become wrong without breaking", "order": 1},
            {"id": "failure-definition", "title": "What counts as an ML system failure?", "order": 2},
            {"id": "failure-types", "title": "Software failures versus ML-specific failures", "order": 3},
            {"id": "train-production-gap", "title": "Why production data differs from training data", "order": 4},
            {"id": "edge-cases", "title": "Edge cases are performance failures, not merely unusual data", "order": 5},
            {"id": "feedback-loops", "title": "Degenerate feedback loops", "order": 6},
            {"id": "feedback-detection-correction", "title": "Detecting and correcting degenerate feedback loops", "order": 7},
            {"id": "distribution-shifts", "title": "Source and target distributions", "order": 8},
            {"id": "covariate-shift", "title": "Covariate shift: the input distribution changes", "order": 9},
            {"id": "label-shift", "title": "Label shift: the output distribution changes", "order": 10},
            {"id": "concept-drift", "title": "Concept drift: the relationship changes", "order": 11},
            {"id": "general-shifts", "title": "Other important production shifts", "order": 12},
            {"id": "detecting-shifts", "title": "Detecting distribution shifts", "order": 13},
            {"id": "statistical-drift", "title": "Statistical methods for drift detection", "order": 14},
            {"id": "time-windows", "title": "Time windows change what drift you can see", "order": 15},
            {"id": "addressing-shifts", "title": "How systems respond to data shifts", "order": 16},
            {"id": "monitoring-observability", "title": "Monitoring, observability, instrumentation, and telemetry", "order": 17},
            {"id": "operational-metrics", "title": "Monitor operational health first", "order": 18},
            {"id": "ml-specific-monitoring", "title": "Four ML artifacts to monitor", "order": 19},
            {"id": "monitor-performance", "title": "Monitoring accuracy-related metrics and user feedback", "order": 20},
            {"id": "monitor-predictions", "title": "Monitoring prediction distributions", "order": 21},
            {"id": "monitor-features", "title": "Monitoring features and schema validity", "order": 22},
            {"id": "monitor-raw", "title": "Monitoring raw inputs", "order": 23},
            {"id": "logs", "title": "Logs and distributed tracing", "order": 24},
            {"id": "dashboards-alerts", "title": "Dashboards and alerts", "order": 25},
            {"id": "observability", "title": "Observability: make the system explainable at runtime", "order": 26},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M08.L01.EX01",

            "title": "Classify production failures",

            "lesson_code": "M08.L01",

            "section_id": "failure-types",

            "placement": "after_section",

            "description": (
                "Distinguish ordinary software failures from ML-specific failures "
                "and identify why silent failures are especially difficult."
            ),

            "instructions": (
                "Classify each incident as mainly a software-system failure, ML-specific "
                "failure, or a case requiring more investigation:\n\n"
                "1. The prediction API returns HTTP 500 because a dependency service is down.\n"
                "2. The service returns predictions normally, but accuracy has fallen sharply "
                "for users in a newly launched region.\n"
                "3. A preprocessing bug turns one important numerical feature into NaN.\n"
                "4. An older model artifact is deployed by mistake.\n"
                "5. Latency remains normal, but the model begins predicting the same class for "
                "almost every request.\n\n"
                "For each, state one signal that could help detect it."
            ),

            "expected_output": (
                "A five-row classification with one detection signal and a short explanation "
                "of why the failure belongs in that category."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "failure-classification",
                "monitoring-design",
                "silent-failure-reasoning",
            ],
        },

        {
            "id": "M08.L01.EX02",

            "title": "Identify the shift",

            "lesson_code": "M08.L01",

            "section_id": "general-shifts",

            "placement": "after_section",

            "description": (
                "Practice distinguishing covariate shift, label shift, concept drift, "
                "and schema changes."
            ),

            "instructions": (
                "Identify the most relevant shift type for each scenario and justify it:\n\n"
                "1. A marketing campaign attracts a wealthier population, but conversion "
                "probability for a given income level stays the same.\n"
                "2. The same type of apartment now sells for substantially less after a "
                "major market disruption.\n"
                "3. A sentiment system changes from POSITIVE/NEGATIVE/NEUTRAL to "
                "POSITIVE/SAD/ANGRY/NEUTRAL.\n"
                "4. A feature that used to store age in years now stores age in months.\n"
                "5. The overall rate of one class changes while the feature distribution "
                "within that class remains stable."
            ),

            "expected_output": (
                "Five shift labels using covariate shift, concept drift, label shift, "
                "feature change, or label-schema change, each with a concise reason."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "covariate-shift",
                "label-shift",
                "concept-drift",
                "schema-change",
            ],
        },

        {
            "id": "M08.L01.EX03",

            "title": "Design a drift-detection strategy",

            "lesson_code": "M08.L01",

            "section_id": "addressing-shifts",

            "placement": "after_section",

            "description": (
                "Combine delayed labels, prediction monitoring, feature monitoring, "
                "and time-window design."
            ),

            "instructions": (
                "You operate a fraud model. Ground-truth fraud labels arrive about 30 days "
                "after transactions, but transaction features and predictions are available immediately.\n\n"
                "Design a monitoring strategy that includes:\n"
                "1. what you would monitor immediately,\n"
                "2. what you would monitor once labels arrive,\n"
                "3. at least three feature summary statistics,\n"
                "4. one use for a two-sample test,\n"
                "5. one short sliding window and one longer comparison window,\n"
                "6. how you would avoid treating every feature change as a critical incident,\n"
                "7. what evidence you would gather before deciding to retrain."
            ),

            "expected_output": (
                "A layered drift-monitoring plan that distinguishes early proxy signals "
                "from delayed direct performance measurements."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "drift-detection",
                "prediction-monitoring",
                "feature-monitoring",
                "time-window-design",
            ],
        },

        {
            "id": "M08.L01.EX04",

            "title": "Build an actionable monitoring and observability plan",

            "lesson_code": "M08.L01",

            "section_id": "dashboards-alerts",

            "placement": "after_section",

            "description": (
                "Design monitoring that detects incidents without overwhelming operators."
            ),

            "instructions": (
                "You maintain a recommendation service with multiple microservices.\n\n"
                "Create a compact monitoring plan containing:\n"
                "1. four operational metrics,\n"
                "2. two model-quality or user-feedback metrics,\n"
                "3. two prediction-distribution checks,\n"
                "4. three feature-validation checks,\n"
                "5. one distributed-tracing field or identifier,\n"
                "6. one dashboard view,\n"
                "7. one alert policy with a duration condition,\n"
                "8. a notification target,\n"
                "9. the information that should appear in the alert description/runbook,\n"
                "10. one step to reduce alert fatigue."
            ),

            "expected_output": (
                "A production monitoring specification connecting metrics, logs, tracing, "
                "dashboards, alerts, and incident response."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "monitoring",
                "observability",
                "distributed-tracing",
                "alert-design",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M08.L01.QZ01",

        "title": "Data Distribution Shifts and Monitoring — Knowledge Check",

        "lesson_code": "M08.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M08.L01.Q01",
                "section_id": "failure-definition",
                "question": (
                    "Why are ML-performance failures often harder to detect than ordinary service failures?"
                ),
                "options": [
                    "ML services never produce logs.",
                    "The service can keep returning normal-looking outputs even when the predictions are wrong.",
                    "Operational failures never happen in ML.",
                    "Models cannot be monitored.",
                ],
                "correct": 1,
                "explanation": (
                    "A model can silently return incorrect predictions while latency, uptime, and request handling look healthy."
                ),
            },

            {
                "id": "M08.L01.Q02",
                "section_id": "failure-types",
                "question": (
                    "Which is primarily an ordinary software-system failure?"
                ),
                "options": [
                    "Concept drift",
                    "A third-party dependency becomes unavailable",
                    "Popularity bias",
                    "Covariate shift",
                ],
                "correct": 1,
                "explanation": (
                    "Dependency failures also occur in non-ML software systems."
                ),
            },

            {
                "id": "M08.L01.Q03",
                "section_id": "edge-cases",
                "question": (
                    "What is the lesson's distinction between an outlier and an edge case?"
                ),
                "options": [
                    "They mean exactly the same thing.",
                    "An outlier is unusual data; an edge case is an example where model performance is unusually bad.",
                    "Outliers only occur in training.",
                    "Edge cases always come from a different distribution.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter defines outliers in terms of data and edge cases in terms of model performance."
                ),
            },

            {
                "id": "M08.L01.Q04",
                "section_id": "feedback-loops",
                "question": (
                    "What creates a degenerate feedback loop?"
                ),
                "options": [
                    "Model outputs influence future user behavior or data, which then influences future versions of the model.",
                    "The model has too few parameters.",
                    "The API has high latency.",
                    "The training dataset is shuffled.",
                ],
                "correct": 0,
                "explanation": (
                    "The system's own outputs alter the future inputs or labels used by the same system."
                ),
            },

            {
                "id": "M08.L01.Q05",
                "section_id": "feedback-detection-correction",
                "question": (
                    "Why can random exploration help a recommender suffering from popularity bias?"
                ),
                "options": [
                    "It guarantees every recommendation is relevant.",
                    "It collects feedback for items that the current ranking would otherwise rarely expose.",
                    "It removes the need for users.",
                    "It makes all item scores equal.",
                ],
                "correct": 1,
                "explanation": (
                    "Random exposure provides less-biased evidence about items hidden by the existing ranking."
                ),
            },

            {
                "id": "M08.L01.Q06",
                "section_id": "distribution-shifts",
                "question": (
                    "What is covariate shift?"
                ),
                "options": [
                    "P(X) changes while P(Y|X) remains the same.",
                    "P(Y|X) changes while P(X) remains the same.",
                    "The label schema changes.",
                    "The model API goes offline.",
                ],
                "correct": 0,
                "explanation": (
                    "Covariate shift is defined as a change in the input distribution with the conditional output relationship fixed."
                ),
            },

            {
                "id": "M08.L01.Q07",
                "section_id": "label-shift",
                "question": (
                    "What is label shift?"
                ),
                "options": [
                    "P(Y) changes while P(X|Y) remains the same.",
                    "Only the model version changes.",
                    "P(X) changes while all labels disappear.",
                    "A feature becomes NaN.",
                ],
                "correct": 0,
                "explanation": (
                    "Label shift changes the output prior distribution while keeping the conditional input distribution fixed by definition."
                ),
            },

            {
                "id": "M08.L01.Q08",
                "section_id": "concept-drift",
                "question": (
                    "Which statement best describes concept drift?"
                ),
                "options": [
                    "The same kind of input can now correspond to a different output relationship.",
                    "Only the number of servers changes.",
                    "The input distribution changes but P(Y|X) remains fixed.",
                    "The labels are delayed.",
                ],
                "correct": 0,
                "explanation": (
                    "Concept drift means P(Y|X) changes."
                ),
            },

            {
                "id": "M08.L01.Q09",
                "section_id": "general-shifts",
                "question": (
                    "Changing a classifier from three possible labels to four is primarily what kind of production change?"
                ),
                "options": [
                    "Label-schema change",
                    "Only covariate shift",
                    "Hardware failure",
                    "Distributed tracing",
                ],
                "correct": 0,
                "explanation": (
                    "The structure and possible values of Y changed."
                ),
            },

            {
                "id": "M08.L01.Q10",
                "section_id": "statistical-drift",
                "question": (
                    "Why are matching mean and variance insufficient to prove that two data distributions are unchanged?"
                ),
                "options": [
                    "Different distributions can share the same summary statistics.",
                    "Mean and variance can never be calculated.",
                    "They require ground-truth labels.",
                    "They only work for images.",
                ],
                "correct": 0,
                "explanation": (
                    "Summary statistics compress information and can look similar even when full distributions differ."
                ),
            },

            {
                "id": "M08.L01.Q11",
                "section_id": "statistical-drift",
                "question": (
                    "What is a key limitation of the KS test in this chapter's monitoring context?"
                ),
                "options": [
                    "It only works for one-dimensional data.",
                    "It requires neural networks.",
                    "It cannot compare samples.",
                    "It requires a GPU.",
                ],
                "correct": 0,
                "explanation": (
                    "The standard KS test is one-dimensional, while feature spaces are often high-dimensional."
                ),
            },

            {
                "id": "M08.L01.Q12",
                "section_id": "time-windows",
                "question": (
                    "Why can cumulative accuracy hide a recent incident?"
                ),
                "options": [
                    "Old healthy data can dominate the aggregate and dilute a short recent drop.",
                    "Cumulative metrics contain no history.",
                    "Sliding metrics cannot show recent data.",
                    "Accuracy cannot be monitored over time.",
                ],
                "correct": 0,
                "explanation": (
                    "The cumulative statistic mixes the incident with a much larger amount of older normal behavior."
                ),
            },

            {
                "id": "M08.L01.Q13",
                "section_id": "monitoring-observability",
                "question": (
                    "What best distinguishes observability from basic monitoring?"
                ),
                "options": [
                    "Monitoring detects signals; observability aims to provide enough runtime detail to investigate internal causes.",
                    "Observability only measures uptime.",
                    "Monitoring requires no metrics.",
                    "They are unrelated concepts.",
                ],
                "correct": 0,
                "explanation": (
                    "Observability emphasizes the ability to explain internal behavior from collected runtime signals."
                ),
            },

            {
                "id": "M08.L01.Q14",
                "section_id": "operational-metrics",
                "question": (
                    "Why are operational metrics still necessary for an ML system with an excellent model?"
                ),
                "options": [
                    "A high-quality model provides no value if the service is unavailable or too slow.",
                    "Operational metrics replace model evaluation.",
                    "Models do not use hardware.",
                    "They are only useful during training.",
                ],
                "correct": 0,
                "explanation": (
                    "Production usefulness requires both software health and predictive quality."
                ),
            },

            {
                "id": "M08.L01.Q15",
                "section_id": "ml-specific-monitoring",
                "question": (
                    "Which list contains the four ML artifacts emphasized for monitoring?"
                ),
                "options": [
                    "Accuracy-related metrics, predictions, features, and raw inputs",
                    "Only CPU, GPU, memory, and disk",
                    "Code, comments, branches, and commits",
                    "Training, validation, test, and staging",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter organizes ML-specific monitoring around those four pipeline artifacts."
                ),
            },

            {
                "id": "M08.L01.Q16",
                "section_id": "monitor-predictions",
                "question": (
                    "Why can prediction monitoring be useful when labels arrive slowly?"
                ),
                "options": [
                    "Prediction anomalies can be detected immediately even before ground truth becomes available.",
                    "Predictions always reveal exact accuracy.",
                    "It eliminates the need for labels permanently.",
                    "Prediction distributions never change.",
                ],
                "correct": 0,
                "explanation": (
                    "Patterns such as all-one-class outputs can reveal problems much earlier than delayed accuracy metrics."
                ),
            },

            {
                "id": "M08.L01.Q17",
                "section_id": "monitor-features",
                "question": (
                    "What is alert fatigue?"
                ),
                "options": [
                    "Operators stop paying attention because alerts are too frequent or low value.",
                    "The monitoring server runs out of battery.",
                    "A model becomes overfit to alert labels.",
                    "A dashboard loads slowly.",
                ],
                "correct": 0,
                "explanation": (
                    "Excessive false-positive or trivial alerts desensitize operators to important incidents."
                ),
            },

            {
                "id": "M08.L01.Q18",
                "section_id": "logs",
                "question": (
                    "What is a major purpose of a shared trace or request ID in a distributed system?"
                ),
                "options": [
                    "To connect logs from the same request across multiple services.",
                    "To replace model parameters.",
                    "To compute label shift.",
                    "To choose a neural architecture.",
                ],
                "correct": 0,
                "explanation": (
                    "A trace identifier lets engineers reconstruct one request's path through a multi-service system."
                ),
            },

            {
                "id": "M08.L01.Q19",
                "section_id": "dashboards-alerts",
                "question": (
                    "Which combination best describes a useful alert?"
                ),
                "options": [
                    "A triggering policy, notification channel, and descriptive/actionable context",
                    "Only a graph",
                    "Only a threshold with no owner",
                    "A model checkpoint and training seed",
                ],
                "correct": 0,
                "explanation": (
                    "An alert should define when to fire, who should receive it, and enough information to act."
                ),
            },

            {
                "id": "M08.L01.Q20",
                "section_id": "observability",
                "type": "open",
                "question": (
                    "A model's prediction quality falls for one hour while latency and uptime remain normal. "
                    "Describe how you would use prediction monitoring, feature monitoring, logs/traces, "
                    "time-window analysis, and observability metadata to determine whether the cause is "
                    "real-world distribution shift, a preprocessing bug, a model-version problem, or another system error."
                ),
            },
        ],

        "passing_score": 70,
    },
}
