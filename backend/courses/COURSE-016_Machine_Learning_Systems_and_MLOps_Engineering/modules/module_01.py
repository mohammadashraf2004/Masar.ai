"""M01.L01 — Overview of Machine Learning Systems.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 1, pages not provided in the supplied source extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"
MODULE_ORDER = 1
MODULE_TITLE = "Overview of Machine Learning Systems"
MODULE_DESCRIPTION = (
    "Understand machine learning as a production system rather than only a model, "
    "decide when ML is appropriate, and recognize the engineering constraints that "
    "separate research prototypes from reliable production systems."
)
SOURCE_CHAPTER = 1
SOURCE_PAGES = "Not provided in the supplied source extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Overview of Machine Learning Systems",
    "slug": "ml-systems-m01-l01-overview",
    "description": (
        "A practical introduction to production machine learning: what an ML system "
        "contains, when ML is a good fit, common use cases, and why production ML "
        "differs from both research ML and traditional software."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 1.75,
    "skill_tags": [
        "machine-learning-systems",
        "ml-production",
        "mlops",
        "system-design",
        "latency",
        "throughput",
        "data-quality",
        "fairness",
        "interpretability",
    ],
    "prerequisite_ids": [],

    "lesson": {
        "title": "Overview of Machine Learning Systems",
        "content": (
            "# Overview of Machine Learning Systems\n"
            "\n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** Overview of Machine Learning Systems  \n"
            "> **Source alignment:** BOOK-XXX, Chapter 1. Page numbers were not included "
            "in the supplied source extract. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why a production ML system is much more than an ML algorithm.\n"
            "- Distinguish ML systems design from the narrower idea of model training.\n"
            "- Decide whether a problem is a reasonable candidate for machine learning.\n"
            "- Identify situations where a simpler non-ML solution is preferable.\n"
            "- Recognize common consumer and enterprise ML use cases.\n"
            "- Explain the major differences between ML research and ML in production.\n"
            "- Reason about latency, throughput, batching, and latency percentiles.\n"
            "- Explain why production data, fairness, and interpretability require special attention.\n"
            "- Describe how ML systems differ from traditional software systems.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. An ML system is bigger than the model\n"
            "\n"
            "When people first learn machine learning, it is natural to focus on algorithms: "
            "logistic regression, decision trees, neural networks, transformers, and so on. "
            "In production, however, the algorithm is only one component of a much larger system.\n"
            "\n"
            "A production ML system begins with a **business or product requirement**. It then "
            "needs an interface through which users or other services interact with it, a data "
            "stack that collects and transforms information, model-development logic, deployment "
            "infrastructure, monitoring, maintenance, and a process for updating the model when "
            "the world or the data changes.\n"
            "\n"
            "A useful mental model is:\n"
            "\n"
            "```text\n"
            "Problem / objective\n"
            "       ↓\n"
            "Data → Model development → Deployment → Prediction service\n"
            "  ↘          ↓                ↓             ↙\n"
            "   Data quality      Monitoring / maintenance\n"
            "             ↘        ↓        ↙\n"
            "             Updates and iteration\n"
            "```\n"
            "\n"
            "The important idea is that a highly accurate model can still fail as a product if "
            "its data pipeline breaks, its predictions arrive too slowly, the system cannot scale, "
            "or nobody notices when its behavior degrades.\n"
            "\n"
            "[[IMAGE_NEEDED: Components of a production ML system | A clean systems diagram showing business requirements, user or API interface, data stack, model development, deployment infrastructure, prediction serving, monitoring, and model/data updates as connected components | Learner should notice that the ML algorithm is only one component inside a larger feedback-driven system]]\n"
            "\n"
            "### MLOps and ML systems design\n"
            "\n"
            "The chapter describes **MLOps** as tools and best practices for bringing ML into "
            "production, including deployment, monitoring, and maintenance. **ML systems design** "
            "takes a broader system view: it asks how all components and stakeholders work together "
            "to satisfy the system's objectives and requirements.\n"
            "\n"
            "So, rather than asking only *Which model should I train?*, systems thinking also asks:\n"
            "\n"
            "- What problem are we solving?\n"
            "- What data do we have, and how will it change?\n"
            "- Who depends on the predictions?\n"
            "- How fast must the answer arrive?\n"
            "- What happens when the model is wrong?\n"
            "- How will we detect degradation?\n"
            "- How will we update the system safely?\n"
            "\n"
            "---\n"
            "\n"
            "## 2. When is machine learning a good fit?\n"
            "\n"
            "Machine learning is powerful, but the chapter strongly warns against treating it as "
            "a universal solution. A useful first question is not *Can ML solve this?* but rather "
            "*Is ML necessary and cost-effective for this problem?*\n"
            "\n"
            "The chapter gives a compact framing:\n"
            "\n"
            "> Machine learning learns complex patterns from existing data and uses those patterns "
            "to make predictions on unseen data.\n"
            "\n"
            "Each part of that sentence imposes a requirement.\n"
            "\n"
            "### 2.1 The system must be able to learn\n"
            "\n"
            "A lookup table is not an ML system because the relationship is explicitly written by "
            "a programmer. An ML system instead infers a relationship from examples.\n"
            "\n"
            "For supervised learning, those examples usually contain inputs together with desired "
            "outputs. If you want to predict the rental price of a property, the input might include "
            "size, room count, neighborhood, amenities, and rating, while the output is the observed "
            "rental price. The system learns a mapping from those examples and applies it to a new listing.\n"
            "\n"
            "### 2.2 There must be a pattern, and it should be complex enough to justify ML\n"
            "\n"
            "If there is no learnable pattern, ML cannot create one. Predicting the next result of a "
            "fair die is not useful because the sequence itself contains no exploitable pattern.\n"
            "\n"
            "At the other extreme, if the pattern is simple and known, ML may be unnecessary. If a "
            "zip code maps deterministically to a known state, a lookup table is simpler, cheaper, and "
            "easier to verify than training a model.\n"
            "\n"
            "ML becomes more attractive when the relationship is too complicated to specify manually. "
            "For example, the relationship between a rental price and many property characteristics "
            "may be difficult to encode as a hand-written formula.\n"
            "\n"
            "[[IMAGE_NEEDED: Hand-written rules versus learned patterns | A side-by-side diagram where traditional software receives explicit rules plus inputs to produce outputs, while ML receives example inputs and outputs during training and learns a model used for future inputs | Learner should notice that ML replaces hand-specified decision logic with patterns learned from examples]]\n"
            "\n"
            "### 2.3 Data must exist, or it must be possible to collect it\n"
            "\n"
            "Because ML learns from data, a project needs something to learn from. A model for a tax-related "
            "prediction cannot be trained if the relevant tax and income information is unavailable.\n"
            "\n"
            "The chapter also points out two subtleties:\n"
            "\n"
            "- **Zero-shot learning** can perform a task without task-specific training examples, but the "
            "  model still learned from data during earlier training.\n"
            "- **Continual learning** can allow a model to learn from incoming production data, but deploying "
            "  an insufficiently trained model can create poor user experiences and other risks.\n"
            "\n"
            "When organizations do not yet have enough data, some begin with human-generated decisions and "
            "use the resulting interactions to collect training data for a later ML system.\n"
            "\n"
            "### 2.4 The problem must be expressible as a prediction\n"
            "\n"
            "An ML model produces an estimate. The estimate does not have to describe the future. A system can "
            "predict a class, a value, an action, a ranking, or the likely output of a computational process.\n"
            "\n"
            "This is why some expensive computational tasks can be reframed as approximation problems: instead "
            "of calculating an exact result, a model predicts an answer that is good enough for the application.\n"
            "\n"
            "### 2.5 Unseen data should share useful patterns with training data\n"
            "\n"
            "Learning only helps when the future inputs resemble the conditions represented in training. A model "
            "trained on behavior from a very different era or environment may fail because the relationship between "
            "inputs and outputs has changed.\n"
            "\n"
            "In technical language, the chapter says training and unseen data should come from similar distributions. "
            "We cannot know the future distribution with certainty, so production ML relies on assumptions and then "
            "uses monitoring to discover when those assumptions stop holding.\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Additional signals that make ML attractive\n"
            "\n"
            "The previous five ideas describe the basic shape of an ML problem. The chapter adds four practical "
            "characteristics that often make ML especially useful.\n"
            "\n"
            "### 3.1 The task is repetitive\n"
            "\n"
            "Many ML algorithms need many examples. Repetitive tasks naturally generate repeated examples of the same "
            "types of patterns, which makes learning easier and creates more opportunities to reuse the model.\n"
            "\n"
            "### 3.2 Wrong predictions are affordable, or their expected benefit justifies the risk\n"
            "\n"
            "Meaningful models will make mistakes. Recommendation systems are a classic forgiving setting: a poor "
            "recommendation may simply be ignored. In higher-stakes systems, a model might still be considered only if "
            "the expected benefit is large enough and the system is designed around the cost of errors.\n"
            "\n"
            "The key design question is therefore not just *How accurate is the model?* but also:\n"
            "\n"
            "> **What does one wrong prediction cost, and who bears that cost?**\n"
            "\n"
            "### 3.3 The task operates at scale\n"
            "\n"
            "ML usually requires meaningful up-front investment in data, compute, infrastructure, and specialized work. "
            "That investment is easier to justify when the system will make many predictions—for example, routing large "
            "volumes of support tickets or filtering very large numbers of messages.\n"
            "\n"
            "Scale also tends to create more data, which can support continued model development.\n"
            "\n"
            "### 3.4 The patterns change over time\n"
            "\n"
            "Hard-coded rules can become expensive to maintain when language, user behavior, fraud strategies, or other "
            "patterns evolve. ML can be updated with new data, making it suitable for changing environments—provided the "
            "system has monitoring and update processes to detect and respond to change.\n"
            "\n"
            "### When should you avoid ML?\n"
            "\n"
            "The chapter identifies three broad warning signs:\n"
            "\n"
            "1. **The use would be unethical.** A technically possible prediction is not automatically an acceptable product.\n"
            "2. **A simpler solution already works.** Start by considering non-ML baselines, rules, or lookup logic.\n"
            "3. **The economics do not make sense.** The value of the predictions must justify data, infrastructure, compute, "
            "   development, and maintenance costs.\n"
            "\n"
            "A useful compromise is decomposition. A problem that is too broad for ML may contain smaller predictive pieces. "
            "For instance, instead of building a system that answers every possible customer question, ML could first predict "
            "whether a question matches a known FAQ and route only unmatched cases to a human.\n"
            "\n"
            "---\n"
            "\n"
            "## 4. What ML systems are used for\n"
            "\n"
            "The chapter separates familiar consumer applications from a large set of enterprise uses. The exact products "
            "change over time, but the underlying problem types are durable.\n"
            "\n"
            "### Consumer-facing examples\n"
            "\n"
            "Common examples in the chapter include:\n"
            "\n"
            "- search and recommendation,\n"
            "- predictive typing,\n"
            "- photo enhancement,\n"
            "- fingerprint or face matching,\n"
            "- machine translation,\n"
            "- smart assistants,\n"
            "- home monitoring and event detection.\n"
            "\n"
            "### Enterprise examples\n"
            "\n"
            "Enterprise systems often use ML to improve internal processes or business decisions. Examples include:\n"
            "\n"
            "| Use case | What the model predicts or detects | Why it matters |\n"
            "|---|---|---|\n"
            "| Fraud detection | Whether a transaction appears fraudulent | Reduce financial loss and manual review |\n"
            "| Price optimization | A useful price under current conditions | Improve a chosen objective such as margin or revenue |\n"
            "| Demand forecasting | Future demand | Plan inventory, budgets, staffing, and pricing |\n"
            "| Customer targeting | Which people are likely to respond | Reduce acquisition cost and improve outreach |\n"
            "| Churn prediction | Which customers may leave | Support retention actions |\n"
            "| Support-ticket classification | Where a request should be routed | Shorten response time |\n"
            "| Brand monitoring | Mentions and sentiment | Detect reputation changes |\n"
            "| Health-care assistance | Patterns relevant to diagnosis or monitoring | Assist qualified professionals under strict requirements |\n"
            "\n"
            "A production engineer should notice that each use case implies different costs of errors, different latency needs, "
            "different privacy constraints, and different requirements for human oversight.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. ML research and ML production optimize for different things\n"
            "\n"
            "A model that looks excellent in a paper or competition is not automatically the best model to deploy. The chapter "
            "highlights five major differences.\n"
            "\n"
            "| Dimension | Research emphasis | Production emphasis |\n"
            "|---|---|---|\n"
            "| Requirements | Strong benchmark performance | Multiple stakeholder requirements |\n"
            "| Computation | Fast training / high throughput | Fast inference / low latency |\n"
            "| Data | Often static and curated | Noisy, incomplete, changing |\n"
            "| Fairness | May receive less attention | Must be considered as a system requirement |\n"
            "| Interpretability | May receive less attention | Often needed by users and developers |\n"
            "\n"
            "### Stakeholders can want different things\n"
            "\n"
            "The chapter uses a restaurant-recommendation example. Different teams might optimize for different goals:\n"
            "\n"
            "- ML engineers may want recommendations users are most likely to order.\n"
            "- Sales may prefer recommendations that create higher service fees.\n"
            "- Product may require recommendations to arrive in under a strict latency target.\n"
            "- Platform engineers may prioritize reliability and scalability over frequent model changes.\n"
            "- Management may care most about overall margin.\n"
            "\n"
            "These are not merely technical disagreements. They are different definitions of success. Before model selection, "
            "the team must determine which requirements are **must-have constraints** and which are **nice-to-have preferences**.\n"
            "\n"
            "A model that is slightly more accurate but violates a hard latency requirement is not a valid production candidate.\n"
            "Likewise, a technique such as ensembling may improve predictive performance while also increasing serving cost, "
            "latency, operational complexity, and difficulty of interpretation.\n"
            "\n"
            "### Why leaderboard success can be misleading\n"
            "\n"
            "Benchmarks are useful, but they simplify the environment. Data preparation, deployment, scaling, monitoring, and "
            "product trade-offs may already be removed from the competition. Repeated experimentation against the same test set "
            "can also make leaderboard differences less meaningful than they first appear.\n"
            "\n"
            "The engineering lesson is simple: **optimize for the real system objective, not for a metric in isolation.**\n"
            "\n"
            "[[IMAGE_NEEDED: Research ML versus production ML | A two-column visual contrasting benchmark performance, static data, training throughput, and limited stakeholder constraints with production requirements, changing data, inference latency, fairness, interpretability, monitoring, and reliability | Learner should see that deployment introduces objectives and constraints that are absent from many research settings]]\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Computational priorities: latency, throughput, and batching\n"
            "\n"
            "During experimentation, training is often the bottleneck because you may train many models over the same data. "
            "After deployment, inference becomes the repeating workload because the system must answer user or service requests.\n"
            "\n"
            "That shift changes what you optimize.\n"
            "\n"
            "### Latency\n"
            "\n"
            "In the terminology used by the chapter, **latency** is the time from sending a request until receiving its response.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "User presses Translate\n"
            "        ↓\n"
            "request sent → model/service works → result returned\n"
            "<---------------- latency ---------------->\n"
            "```\n"
            "\n"
            "### Throughput\n"
            "\n"
            "**Throughput** is how many requests are processed during a unit of time.\n"
            "\n"
            "If one request takes 10 ms and the system processes only one at a time:\n"
            "\n"
            "```text\n"
            "1 second = 1000 ms\n"
            "1000 / 10 = 100 requests per second\n"
            "```\n"
            "\n"
            "If each request instead takes 100 ms, the same one-at-a-time system handles only about 10 requests per second.\n"
            "\n"
            "### Batching changes the trade-off\n"
            "\n"
            "Modern systems can process several requests together. Suppose a batch of 10 requests takes 10 ms. The latency for "
            "that batch is still about 10 ms, but throughput becomes about 1,000 requests per second. If a batch of 50 takes 20 ms, "
            "latency has increased, yet throughput becomes about 2,500 requests per second.\n"
            "\n"
            "This is why higher latency does **not** always imply lower throughput in a batched or concurrent system.\n"
            "\n"
            "[[IMAGE_NEEDED: Latency and throughput with batching | Two timelines: one processing requests sequentially and one processing requests in batches, annotated with per-request latency and total requests per second | Learner should notice that batching can increase throughput even when latency per batch also increases]]\n"
            "\n"
            "Online batching introduces another issue: the service may need to wait for enough requests to form a batch, and that "
            "waiting time adds to latency.\n"
            "\n"
            "### Latency is a distribution, not one number\n"
            "\n"
            "An average can hide important behavior. Consider these ten request latencies from the chapter:\n"
            "\n"
            "```text\n"
            "90, 95, 99, 100, 100, 100, 102, 104, 110, 3000 ms\n"
            "```\n"
            "\n"
            "Most requests are around 100 ms, but one extremely slow request pulls the arithmetic mean upward. Looking only at the "
            "mean can therefore give a misleading picture.\n"
            "\n"
            "Production teams often inspect percentiles:\n"
            "\n"
            "- **p50**: the median; half of requests are faster and half are slower.\n"
            "- **p90**: 90% of requests are at or below this value.\n"
            "- **p95 / p99**: useful for seeing the slow tail of the distribution.\n"
            "\n"
            "High-percentile latency matters because rare slow requests can reveal failures or disproportionately affect important users.\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Production data, fairness, and interpretability\n"
            "\n"
            "### 7.1 Production data is messy and continuously changing\n"
            "\n"
            "Research datasets are often cleaned, formatted, documented, and intentionally kept static so that experiments are comparable. "
            "Production data is more difficult. It may be noisy, unstructured, biased in unknown ways, incomplete, incorrectly labeled, or "
            "generated continuously by users and external systems.\n"
            "\n"
            "Changing business requirements can also change what labels mean. If user data is involved, privacy and regulatory requirements "
            "become part of the system design.\n"
            "\n"
            "[[IMAGE_NEEDED: Research data versus production data | A side-by-side data-flow illustration showing a clean static benchmark dataset on the research side and noisy, streaming, changing, partially labeled data with privacy checks on the production side | Learner should notice that production data is an evolving system dependency rather than a fixed file]]\n"
            "\n"
            "### 7.2 Fairness cannot be postponed until after deployment\n"
            "\n"
            "A model learns from historical data, and historical data can contain existing inequalities or biases. If the model reproduces those "
            "patterns at scale, a problem that affected a small number of decisions can become automated across a very large population.\n"
            "\n"
            "The chapter's key warning is that fairness is not a cosmetic check added after optimizing accuracy. It must be considered while choosing "
            "data, objectives, evaluation metrics, and deployment safeguards. Aggregate accuracy can also hide poor performance on smaller groups.\n"
            "\n"
            "### 7.3 Interpretability serves both users and developers\n"
            "\n"
            "Interpretability matters for at least two reasons described in the chapter:\n"
            "\n"
            "1. **Users and decision makers** may need to understand why a result was produced so they can trust, challenge, or audit it.\n"
            "2. **Developers** need clues about model behavior so they can debug failures and improve the system.\n"
            "\n"
            "The higher the consequence of a prediction, the harder it becomes to treat explanation as an optional feature.\n"
            "\n"
            "---\n"
            "\n"
            "## 8. ML systems versus traditional software\n"
            "\n"
            "Machine learning is still software engineering, so many traditional engineering practices remain valuable. The difference is that an ML "
            "application adds new moving parts.\n"
            "\n"
            "Traditional software often treats code and data as separate concerns. In an ML system, behavior emerges from:\n"
            "\n"
            "```text\n"
            "code + data + learned model artifacts\n"
            "```\n"
            "\n"
            "That means teams must test and version more than source code. Data changes can change model behavior even when application code stays identical.\n"
            "\n"
            "### Data itself becomes an engineering dependency\n"
            "\n"
            "Not all training samples are equally valuable. If a dataset already contains many examples of one common class and very few examples of a rare "
            "but important class, another rare example may be much more informative than another common one. Blindly accepting data can also introduce poor "
            "samples or maliciously constructed examples.\n"
            "\n"
            "### Model size and serving constraints matter\n"
            "\n"
            "Large models can require substantial memory and compute. A model that cannot fit the target hardware or answer quickly enough may be unusable even "
            "if its offline accuracy is excellent. This is especially challenging on edge devices with limited resources.\n"
            "\n"
            "### Monitoring and debugging are harder\n"
            "\n"
            "Traditional software failures often have explicit exceptions or reproducible bugs. ML failures can be gradual and statistical: input distributions "
            "shift, data quality changes, or predictions become less useful without the program crashing. Production systems therefore need monitoring that looks "
            "at model behavior and data behavior, not only service uptime.\n"
            "\n"
            "The chapter's broader message is that ML engineering requires a **holistic system approach**. Good model code is necessary, but it is not sufficient.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: The best offline model is automatically the best production model\n"
            "\n"
            "> If Model A has the highest benchmark score, we should deploy Model A.\n"
            "\n"
            "**Why this is wrong:** production selection also depends on latency, cost, scalability, interpretability, fairness, reliability, and stakeholder objectives.\n"
            "\n"
            "### Misconception 2: ML is appropriate whenever a problem involves data\n"
            "\n"
            "> We have a lot of data, so we should use ML.\n"
            "\n"
            "**Why this is wrong:** the problem also needs a useful learnable pattern, a predictive framing, sufficiently relevant data, and economics that justify the system.\n"
            "\n"
            "### Misconception 3: Lower latency always means lower throughput\n"
            "\n"
            "> If each request takes longer, the system must always process fewer requests per second.\n"
            "\n"
            "**Why this is wrong:** batching and concurrency can increase total throughput even while per-request or per-batch latency increases.\n"
            "\n"
            "### Misconception 4: If the service is running, the ML system is healthy\n"
            "\n"
            "> No errors in the server logs means the model is fine.\n"
            "\n"
            "**Why this is wrong:** an ML system can remain technically available while data or prediction quality silently degrades.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| ML system | The complete production system around an ML model, including data, infrastructure, serving, monitoring, maintenance, and requirements |\n"
            "| MLOps | Tools and practices for operationalizing ML through deployment, monitoring, and maintenance |\n"
            "| ML systems design | A holistic approach to making all ML system components and stakeholders satisfy defined objectives and requirements |\n"
            "| Prediction | An estimated output produced by a model for an input |\n"
            "| Unseen data | Inputs not used to train the model |\n"
            "| Data distribution | The statistical pattern describing how data values occur |\n"
            "| Latency | Time from sending a request to receiving the result, using the chapter's terminology |\n"
            "| Throughput | Number of requests processed per unit of time |\n"
            "| Batching | Processing several requests together |\n"
            "| p50 | Median latency: half of requests are faster and half are slower |\n"
            "| p90 / p95 / p99 | High-percentile latency measurements used to inspect the slow tail |\n"
            "| Fairness | Concern that model behavior and impacts should not systematically disadvantage groups |\n"
            "| Interpretability | Ability to understand or explain factors behind model behavior or outputs |\n"
            "| Continual learning | Updating or learning from newly arriving data over time |\n"
            "| Data poisoning | Harm caused when malicious or harmful training data is introduced into the learning process |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why is an ML algorithm only one part of a production ML system?\n"
            "2. What five ideas are contained in the framing 'learn complex patterns from existing data and make predictions on unseen data'?\n"
            "3. Give one example where a lookup table is better than ML.\n"
            "4. Why does repetitive, high-scale work often favor ML?\n"
            "5. Why can a research winner still be a poor production model?\n"
            "6. What is the difference between latency and throughput?\n"
            "7. Why can batching raise both latency and throughput?\n"
            "8. Why are p95 or p99 useful in addition to average latency?\n"
            "9. How is production data different from a static research dataset?\n"
            "10. Why must fairness and interpretability be considered during system design rather than after deployment?\n"
            "11. What must be versioned or monitored in ML systems beyond application code?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**A production ML system succeeds only when the model, data, infrastructure, stakeholders, and operational process work together. "
            "Choosing an algorithm is only one small part of engineering the complete system.**\n"
        ),
        "estimated_minutes": 105,
        "has_code_examples": False,
        "has_manual_image_requests": True,
        "sections": [
            {
                "id": "ml-system-bigger-than-model",
                "title": "An ML system is bigger than the model",
                "order": 1,
            },
            {
                "id": "when-to-use-ml",
                "title": "When is machine learning a good fit?",
                "order": 2,
            },
            {
                "id": "additional-fit-signals",
                "title": "Additional signals that make ML attractive",
                "order": 3,
            },
            {
                "id": "ml-use-cases",
                "title": "What ML systems are used for",
                "order": 4,
            },
            {
                "id": "research-vs-production",
                "title": "ML research and ML production optimize for different things",
                "order": 5,
            },
            {
                "id": "latency-throughput",
                "title": "Computational priorities: latency, throughput, and batching",
                "order": 6,
            },
            {
                "id": "production-data-responsibility",
                "title": "Production data, fairness, and interpretability",
                "order": 7,
            },
            {
                "id": "ml-vs-software",
                "title": "ML systems versus traditional software",
                "order": 8,
            },
        ],
    },

    "exercises": [
        {
            "id": "M01.L01.EX01",
            "title": "Should This Problem Use Machine Learning?",
            "lesson_code": "M01.L01",
            "section_id": "when-to-use-ml",
            "placement": "after_section",
            "description": (
                "Practice deciding whether a problem has the properties that make ML useful."
            ),
            "instructions": (
                "For each scenario below, decide whether you would begin with ML or a simpler solution. "
                "Use the chapter's criteria: learnability, pattern complexity, data availability, predictive framing, "
                "and similarity between training and unseen data.\n\n"
                "A. Convert a US zip code to its known state.\n"
                "B. Estimate the rental price of a property from location, size, rooms, amenities, and ratings.\n"
                "C. Predict the next outcome of a fair six-sided die.\n"
                "D. Route thousands of daily support tickets to departments from their text.\n\n"
                "For every scenario:\n"
                "1. State ML / non-ML / uncertain.\n"
                "2. Give the main reason.\n"
                "3. Identify the data you would need if ML is used.\n"
                "4. Name one assumption that could fail after deployment."
            ),
            "expected_output": (
                "A four-row decision table with a recommendation, justification, required data, and one production assumption for each scenario."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "ml-problem-framing",
                "solution-selection",
                "data-requirements",
                "distribution-assumptions",
            ],
        },
        {
            "id": "M01.L01.EX02",
            "title": "Analyze a Production Latency Profile",
            "lesson_code": "M01.L01",
            "section_id": "latency-throughput",
            "placement": "after_section",
            "description": (
                "Practice reasoning about mean latency, percentiles, throughput, and batching."
            ),
            "instructions": (
                "Use this set of request latencies in milliseconds:\n"
                "90, 95, 99, 100, 100, 100, 102, 104, 110, 3000\n\n"
                "1. Explain why the arithmetic mean alone gives a misleading impression.\n"
                "2. Identify the p50 value from the sorted list using the simple median interpretation taught in the lesson.\n"
                "3. Explain what the very slow request tells you operationally.\n"
                "4. If a system handles one request at a time and each takes 10 ms, compute approximate throughput.\n"
                "5. If it processes batches of 50 in 20 ms, compute approximate throughput.\n"
                "6. Explain why the second configuration has higher latency but can still have higher throughput."
            ),
            "expected_output": (
                "A short analysis containing the latency interpretation, percentile reasoning, two throughput calculations, and a batching explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "latency-analysis",
                "throughput-calculation",
                "percentile-interpretation",
                "batching-tradeoffs",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L01.QZ01",
        "title": "Overview of Machine Learning Systems — Knowledge Check",
        "lesson_code": "M01.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L01.Q01",
                "section_id": "ml-system-bigger-than-model",
                "question": "Which statement best describes a production ML system?",
                "options": [
                    "It is mainly the trained model file.",
                    "It is the model plus the surrounding data, infrastructure, interfaces, monitoring, maintenance, and requirements.",
                    "It is any application that uses a neural network.",
                    "It is a database that stores model predictions.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter's central systems view is that the algorithm is only one component. Production success depends on the surrounding data and operational system as well."
                ),
            },
            {
                "id": "M01.L01.Q02",
                "section_id": "when-to-use-ml",
                "question": "Which problem is the strongest example of using a simpler non-ML solution?",
                "options": [
                    "Predicting rental price from many interacting property characteristics",
                    "Classifying support tickets from free-form text",
                    "Mapping a known zip code to its known state",
                    "Detecting suspicious transactions from historical behavior",
                ],
                "correct": 2,
                "explanation": (
                    "A known zip-code-to-state mapping is a simple deterministic relationship, so a lookup table is more appropriate than learning the mapping with ML."
                ),
            },
            {
                "id": "M01.L01.Q03",
                "section_id": "additional-fit-signals",
                "question": "Why are repetitive, high-volume tasks often good ML candidates?",
                "options": [
                    "They guarantee perfect predictions.",
                    "They create repeated examples and allow the up-front ML investment to be reused many times.",
                    "They remove the need for training data.",
                    "They make monitoring unnecessary.",
                ],
                "correct": 1,
                "explanation": (
                    "Repetition provides many examples of recurring patterns, while scale helps justify the cost of data, compute, infrastructure, and engineering."
                ),
            },
            {
                "id": "M01.L01.Q04",
                "section_id": "research-vs-production",
                "question": "Why might the highest-scoring research model be rejected for production?",
                "options": [
                    "Production systems never care about predictive quality.",
                    "Research models cannot use real data.",
                    "The model may violate latency, cost, interpretability, scalability, or stakeholder requirements.",
                    "A production model must always be simpler than every research model.",
                ],
                "correct": 2,
                "explanation": (
                    "Production model selection is multi-objective. Benchmark performance is only one requirement among several technical and stakeholder constraints."
                ),
            },
            {
                "id": "M01.L01.Q05",
                "section_id": "latency-throughput",
                "question": "Which statement about batching is correct?",
                "options": [
                    "Batching can increase throughput even if latency also increases.",
                    "Batching always reduces both latency and throughput.",
                    "Batching matters only during model training.",
                    "Batching guarantees every request has identical latency.",
                ],
                "correct": 0,
                "explanation": (
                    "Processing many requests together can increase requests per second. Waiting for or processing a batch can still increase latency, so both values may rise."
                ),
            },
            {
                "id": "M01.L01.Q06",
                "section_id": "latency-throughput",
                "question": "Why are p95 and p99 latency useful in production?",
                "options": [
                    "They show how fast the training loop converges.",
                    "They reveal the slow tail that an average may hide.",
                    "They replace all need for monitoring.",
                    "They measure model accuracy on 95% or 99% of samples.",
                ],
                "correct": 1,
                "explanation": (
                    "High-percentile latency exposes unusually slow requests and helps teams define performance requirements for the tail of the distribution."
                ),
            },
            {
                "id": "M01.L01.Q07",
                "section_id": "production-data-responsibility",
                "question": "What is a major difference between research data and production data?",
                "options": [
                    "Production data is always fully labeled.",
                    "Research data changes faster than production data.",
                    "Production data is often noisy, changing, partially labeled, and tied to privacy or regulatory concerns.",
                    "Research data can never contain bias.",
                ],
                "correct": 2,
                "explanation": (
                    "The chapter emphasizes that production data is an evolving system input and is often much messier than static benchmark datasets."
                ),
            },
            {
                "id": "M01.L01.Q08",
                "section_id": "ml-vs-software",
                "type": "open",
                "question": (
                    "A model's API is healthy and no application exceptions are occurring, but prediction quality has slowly become worse over several weeks. "
                    "Using the lesson, explain why this can happen and name at least three parts of the system you would investigate."
                ),
            },
        ],
        "passing_score": 70,
    },
}
