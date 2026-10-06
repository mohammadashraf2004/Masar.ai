"""M09.L01 — Continual Learning and Test in Production.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 9, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M09.L01"

MODULE_ORDER = 9

MODULE_TITLE = "Continual Learning and Test in Production"

MODULE_DESCRIPTION = (
    "Learn how production ML systems can continually adapt to changing data, "
    "how stateful and stateless retraining differ, what infrastructure continual "
    "learning requires, how to decide retraining frequency, and how to evaluate "
    "updated models safely with live production traffic."
)

SOURCE_CHAPTER = 9

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Continual Learning and Test in Production",

    "slug": "ml-systems-design-m09-l01",

    "description": (
        "A production-focused lesson on continual learning, stateful versus stateless "
        "training, fresh-data and evaluation challenges, four stages of continual-learning "
        "maturity, retraining frequency, data freshness, shadow deployment, A/B testing, "
        "canary releases, interleaving, multi-armed bandits, contextual bandits, and "
        "automated model-evaluation pipelines."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 4.25,

    "skill_tags": [
        "continual-learning",
        "stateful-training",
        "stateless-retraining",
        "micro-batch-training",
        "champion-challenger",
        "data-iteration",
        "model-iteration",
        "fresh-data",
        "label-computation",
        "stream-processing",
        "model-lineage",
        "retraining-frequency",
        "data-freshness",
        "backtesting",
        "shadow-deployment",
        "ab-testing",
        "canary-release",
        "interleaving",
        "multi-armed-bandits",
        "epsilon-greedy",
        "thompson-sampling",
        "ucb",
        "contextual-bandits",
        "test-in-production",
        "evaluation-pipeline",
    ],

    "prerequisite_ids": ["M08.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Continual Learning and Test in Production",

        "content": (
            "# Continual Learning and Test in Production\n"
            "\n"
            "> **Lesson:** M09.L01  \n"
            "> **Module:** Continual Learning and Test in Production  \n"
            "> **Source alignment:** Chapter 9. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what continual learning means in production ML.\n"
            "- Explain why continual learning usually uses micro-batches rather than one-example-at-a-time updates.\n"
            "- Describe the champion-challenger pattern for safe model updates.\n"
            "- Distinguish stateless retraining from stateful training.\n"
            "- Distinguish model iteration from data iteration.\n"
            "- Explain why continual learning can help with drift, rare events, and continuous cold start.\n"
            "- Identify the fresh-data, evaluation, and algorithmic challenges of continual learning.\n"
            "- Explain label computation from behavioral logs.\n"
            "- Describe the four infrastructure stages toward continual learning.\n"
            "- Explain the role of schedulers, data access, model stores, lineage, and monitoring.\n"
            "- Explain the log-and-wait approach for feature reuse.\n"
            "- Choose among time-, performance-, volume-, and drift-based retraining triggers.\n"
            "- Estimate the value of data freshness experimentally.\n"
            "- Distinguish data iteration from model iteration when allocating engineering effort.\n"
            "- Explain why static test sets and backtests are both useful but insufficient alone.\n"
            "- Compare shadow deployment, A/B testing, canary release, and interleaving experiments.\n"
            "- Explain the exploration-exploitation trade-off in multi-armed bandits.\n"
            "- Explain epsilon-greedy, Thompson Sampling, and UCB at a conceptual level.\n"
            "- Distinguish model-selection bandits from contextual bandits.\n"
            "- Explain why production evaluation should be standardized and automated.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Continual learning is an infrastructure capability\n"
            "\n"
            "Chapter 8 focused on why models degrade in production and how monitoring "
            "can detect the problem. Chapter 9 asks the next question:\n"
            "\n"
            "> **How do we adapt the model after the world changes?**\n"
            "\n"
            "The chapter's answer is **continual learning**: build the infrastructure "
            "needed to update models whenever updates are needed, then evaluate and "
            "deploy those updates safely.\n"
            "\n"
            "Continual learning is therefore not just a training algorithm. It connects:\n"
            "\n"
            "- fresh data access,\n"
            "- label generation,\n"
            "- training,\n"
            "- model storage and lineage,\n"
            "- evaluation,\n"
            "- deployment,\n"
            "- monitoring.\n"
            "\n"
            "The complete loop looks like:\n"
            "\n"
            "```text\n"
            "Production data\n"
            "      ↓\n"
            "Fresh examples + labels\n"
            "      ↓\n"
            "Update candidate model\n"
            "      ↓\n"
            "Evaluate offline / online\n"
            "      ↓\n"
            "Promote if satisfactory\n"
            "      ↓\n"
            "Monitor production\n"
            "      ↺\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Continual-learning production loop | "
            "A circular production pipeline showing fresh data and feedback feeding "
            "candidate training, evaluation, promotion, deployment, and monitoring | "
            "Learner should notice that continual learning requires an end-to-end "
            "update system, not merely a training function]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Continual learning does not mean learning from every single event\n"
            "\n"
            "A common misunderstanding is that continual learning means updating a "
            "model immediately after every incoming sample.\n"
            "\n"
            "The chapter says this is uncommon in real production systems.\n"
            "\n"
            "There are two reasons.\n"
            "\n"
            "### Catastrophic forgetting\n"
            "\n"
            "A neural network trained aggressively on new data can abruptly forget "
            "previously learned information.\n"
            "\n"
            "### Hardware efficiency\n"
            "\n"
            "Modern training hardware is optimized for batches and parallel computation. "
            "Training on one example at a time wastes compute and limits data parallelism.\n"
            "\n"
            "A more practical production pattern is **micro-batch updating**.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Collect 512 new examples\n"
            "        ↓\n"
            "Update candidate model\n"
            "        ↓\n"
            "Collect next micro-batch\n"
            "```\n"
            "\n"
            "The right micro-batch size depends on the task and infrastructure.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Never update the live model blindly: champion and challenger\n"
            "\n"
            "The currently deployed model is the **champion**.\n"
            "\n"
            "Instead of modifying it directly, create a copy and update that copy. "
            "The updated copy is the **challenger**.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Champion v1.4\n"
            "    │\n"
            "    └── copy → train on fresh data → Challenger v1.5\n"
            "                                      ↓\n"
            "                                   Evaluate\n"
            "                                 /          \\\n"
            "                           passes            fails\n"
            "                              ↓                ↓\n"
            "                        Promote v1.5       Keep v1.4\n"
            "```\n"
            "\n"
            "The key safety rule is:\n"
            "\n"
            "> **An updated model should not replace the live model until the update has been evaluated.**\n"
            "\n"
            "Real systems can maintain multiple challengers simultaneously and use "
            "more sophisticated promotion and rollback rules than this simplified diagram.\n"
            "\n"
            "[[IMAGE_NEEDED: Champion-challenger model update | "
            "A deployed champion copied into one or more challengers, with fresh-data "
            "training and an evaluation gate before promotion | Learner should notice "
            "that training and deployment are separated by a quality gate]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Stateless retraining versus stateful training\n"
            "\n"
            "Continual learning is more about **how** a model is updated than exactly "
            "how frequently it is updated.\n"
            "\n"
            "### Stateless retraining\n"
            "\n"
            "Train the model from scratch during every update.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Update 1: initialize → train on recent 3 months → model A\n"
            "Update 2: initialize → train on recent 3 months → model B\n"
            "```\n"
            "\n"
            "### Stateful training\n"
            "\n"
            "Continue training from the previous model checkpoint using fresh data.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Model v1.0\n"
            "   + today's data\n"
            "        ↓\n"
            "Model v1.1\n"
            "   + tomorrow's data\n"
            "        ↓\n"
            "Model v1.2\n"
            "```\n"
            "\n"
            "Stateful training is also referred to as **fine-tuning** or "
            "**incremental learning** in the source.\n"
            "\n"
            "### Why stateful training can be attractive\n"
            "\n"
            "- It may require much less fresh data per update.\n"
            "- It can converge faster.\n"
            "- It can reduce compute cost.\n"
            "- It can make more frequent updates practical.\n"
            "\n"
            "The chapter gives a production example where switching from daily "
            "stateless retraining to daily stateful training greatly reduced compute "
            "cost while improving a business metric.\n"
            "\n"
            "### Privacy-related benefit\n"
            "\n"
            "Traditional stateless retraining often requires storing old training data "
            "so it can be reused. Stateful training can, in principle, use a fresh data "
            "sample once and then discard it, reducing the need for permanent storage.\n"
            "\n"
            "This does **not** mean companies never retrain from scratch. The source notes "
            "that teams using stateful training may still periodically retrain on a large "
            "dataset to recalibrate the system.\n"
            "\n"
            "[[IMAGE_NEEDED: Stateless versus stateful training | "
            "Two parallel timelines: stateless updates repeatedly initialize from scratch "
            "using large historical windows, while stateful updates continue from the "
            "previous checkpoint using smaller fresh-data windows | Learner should notice "
            "the difference in reused model state and data requirements]]\n"
            "\n"
            "{{exercise:M09.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Data iteration versus model iteration\n"
            "\n"
            "The chapter separates two types of updates.\n"
            "\n"
            "### Data iteration\n"
            "\n"
            "The architecture and feature set stay the same. You refresh the model "
            "using new data.\n"
            "\n"
            "This is where stateful training is most naturally applied today.\n"
            "\n"
            "### Model iteration\n"
            "\n"
            "You change the model itself—for example:\n"
            "\n"
            "- add a feature,\n"
            "- remove a feature,\n"
            "- add or change a layer,\n"
            "- change the architecture.\n"
            "\n"
            "Such changes often require training from scratch because the new model "
            "structure is no longer identical to the previous one.\n"
            "\n"
            "This distinction becomes important later when deciding where to invest "
            "engineering and compute resources.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Why continual learning can matter\n"
            "\n"
            "### Adapt to sudden distribution shifts\n"
            "\n"
            "A ride-pricing model may have learned that demand is usually low on a "
            "particular Thursday evening. A large local event can suddenly invalidate "
            "that expectation.\n"
            "\n"
            "If the model adapts too slowly, the predicted price may remain too low, "
            "fewer drivers may become available, and riders may experience long waits.\n"
            "\n"
            "### Adapt during rare events\n"
            "\n"
            "Black Friday or Singles Day happens infrequently. Historical data may not "
            "fully represent the current year's event.\n"
            "\n"
            "Learning from fresh behavior during the event can improve recommendations "
            "or predictions while the event is still happening.\n"
            "\n"
            "### Reduce continuous cold start\n"
            "\n"
            "Cold start is not only about brand-new users.\n"
            "\n"
            "An existing user can effectively become cold when:\n"
            "\n"
            "- they switch devices,\n"
            "- they are not logged in,\n"
            "- they visit so rarely that old history is stale.\n"
            "\n"
            "If the model can adapt inside the user's current session, it can become "
            "relevant much sooner.\n"
            "\n"
            "The core idea is:\n"
            "\n"
            "> Continual learning expands what is possible when recent behavior matters.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Challenge 1: getting fresh data and fresh labels\n"
            "\n"
            "If you want to update a model every hour, you need useful new training "
            "data every hour.\n"
            "\n"
            "Many organizations build training data from a warehouse. That introduces "
            "delay because data from applications must first be moved and processed "
            "before it becomes queryable.\n"
            "\n"
            "A faster approach is to consume data directly from real-time transports "
            "before it reaches the warehouse.\n"
            "\n"
            "```text\n"
            "Application events\n"
            "       ↓\n"
            "Real-time transport\n"
            "   ↙             ↘\n"
            "Fresh training   Data warehouse\n"
            "pipeline\n"
            "```\n"
            "\n"
            "But raw events are not enough if the model requires supervised labels.\n"
            "\n"
            "The ideal continual-learning tasks often have **natural labels with short "
            "feedback loops**, such as:\n"
            "\n"
            "- dynamic pricing,\n"
            "- ETA prediction,\n"
            "- click-through prediction,\n"
            "- online content recommendation.\n"
            "\n"
            "[[IMAGE_NEEDED: Fresh-data paths for continual learning | "
            "Application events entering a real-time transport, with one path going "
            "directly to fresh training/label extraction and another slower path through "
            "a warehouse | Learner should notice how bypassing warehouse delay can make "
            "training data fresher]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Label computation from behavioral logs\n"
            "\n"
            "Natural labels are often not stored as ready-made labels.\n"
            "\n"
            "Suppose a user clicks product `32345` at 10:33 p.m. That click becomes "
            "useful only if the system can connect it to the earlier recommendation "
            "that caused the exposure.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Recommendation log\n"
            "user A + query Q → product 32345 shown\n"
            "\n"
            "Later click log\n"
            "user A → clicked product 32345\n"
            "\n"
            "Join the events\n"
            "      ↓\n"
            "Label recommendation(Q, 32345) as positive\n"
            "```\n"
            "\n"
            "The process of extracting labels from behavioral history is called "
            "**label computation**.\n"
            "\n"
            "It can be implemented in batch after logs reach a warehouse, but that "
            "adds delay. Stream processing can create labels more quickly from real-time events.\n"
            "\n"
            "The chapter also mentions programmatic and crowdsourced labeling as possible "
            "ways to speed up labeling when natural labels are not enough.\n"
            "\n"
            "[[IMAGE_NEEDED: Label computation from recommendation and click logs | "
            "A recommendation event and a later click event joined by user/item/context "
            "identifiers to create a supervised label | Learner should notice that user "
            "behavior must be matched back to the prediction that generated the opportunity]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Challenge 2: evaluating every update safely\n"
            "\n"
            "Writing a script that trains frequently is not the hardest part.\n"
            "\n"
            "The hard part is proving that each update is safe and useful enough to deploy.\n"
            "\n"
            "More frequent updates create more opportunities for failure.\n"
            "\n"
            "They also create more exposure to manipulation because malicious or "
            "coordinated user behavior can enter the training stream more quickly.\n"
            "\n"
            "The chapter uses the Tay chatbot incident as an example of the danger of "
            "learning rapidly from hostile public input.\n"
            "\n"
            "Evaluation itself can become the bottleneck.\n"
            "\n"
            "For rare-event tasks such as fraud detection, enough positive examples "
            "may take days or weeks to appear. A model could technically train every "
            "hour but still be impossible to validate reliably that quickly.\n"
            "\n"
            "Therefore:\n"
            "\n"
            "> **Maximum retraining frequency is bounded not only by training speed, "
            "but also by how fast trustworthy evaluation evidence becomes available.**\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Challenge 3: some algorithms are easier to update incrementally\n"
            "\n"
            "A neural network can be updated using a small new data batch.\n"
            "\n"
            "Some matrix-based methods are less natural for partial-data updates because "
            "their representation depends on the full dataset.\n"
            "\n"
            "The source uses collaborative filtering with a user-item matrix as an example. "
            "Rebuilding and refactorizing the whole matrix for every tiny change can be "
            "too expensive for very frequent updates.\n"
            "\n"
            "Tree methods also require special incremental algorithms if they are to learn "
            "continuously from partial data.\n"
            "\n"
            "### Feature transformations must also become incremental\n"
            "\n"
            "It is not enough for the model to support partial updates.\n"
            "\n"
            "Suppose feature scaling depends on global statistics such as:\n"
            "\n"
            "- min,\n"
            "- max,\n"
            "- mean,\n"
            "- variance,\n"
            "- quantiles.\n"
            "\n"
            "Recomputing these from each tiny micro-batch can make preprocessing statistics "
            "fluctuate heavily.\n"
            "\n"
            "A continual-learning pipeline may therefore need **running statistics** that "
            "update incrementally as new data arrives.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Four stages toward continual learning\n"
            "\n"
            "The chapter presents continual learning as an infrastructure maturity path.\n"
            "\n"
            "| Stage | Training style | Trigger / process |\n"
            "|---|---|---|\n"
            "| 1 | Manual, stateless retraining | Human-driven, ad hoc |\n"
            "| 2 | Automated, stateless retraining | Scripted, usually schedule-based |\n"
            "| 3 | Automated, stateful training | Script loads previous checkpoint |\n"
            "| 4 | Continual learning | Update trigger responds to time, performance, volume, or drift |\n"
            "\n"
            "[[IMAGE_NEEDED: Four stages of continual-learning maturity | "
            "A staircase from manual stateless retraining to automated stateless, "
            "automated stateful, and finally trigger-driven continual learning | "
            "Learner should notice that the progression is mostly about infrastructure "
            "automation, state management, monitoring, and evaluation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Stage 1: manual, stateless retraining\n"
            "\n"
            "At the beginning, teams often prioritize building new ML applications rather "
            "than maintaining existing ones.\n"
            "\n"
            "A model update may happen only when:\n"
            "\n"
            "1. performance becomes bad enough to matter, and\n"
            "2. someone has time to fix it.\n"
            "\n"
            "The update process is manual:\n"
            "\n"
            "```text\n"
            "Query new data\n"
            "   ↓\n"
            "Clean data\n"
            "   ↓\n"
            "Extract features\n"
            "   ↓\n"
            "Retrain from scratch\n"
            "   ↓\n"
            "Export model\n"
            "   ↓\n"
            "Deploy manually\n"
            "```\n"
            "\n"
            "This process creates opportunities for inconsistency when training code "
            "changes but production logic is not updated in the same way.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Stage 2: automated stateless retraining\n"
            "\n"
            "At this stage, the manual sequence becomes an automated script or workflow.\n"
            "\n"
            "The pipeline can automatically:\n"
            "\n"
            "- pull data,\n"
            "- resample if necessary,\n"
            "- extract features,\n"
            "- generate/process labels,\n"
            "- train,\n"
            "- evaluate,\n"
            "- deploy.\n"
            "\n"
            "The model is still trained from scratch each time.\n"
            "\n"
            "### Different models need different schedules\n"
            "\n"
            "A recommender may use:\n"
            "\n"
            "- a product embedding model that changes slowly,\n"
            "- a ranking model that changes quickly.\n"
            "\n"
            "The embedding model might update weekly while the ranker updates daily.\n"
            "\n"
            "Dependencies matter too: if the embedding model changes, the dependent ranking "
            "model may also need an update.\n"
            "\n"
            "### Three infrastructure factors\n"
            "\n"
            "The chapter highlights:\n"
            "\n"
            "1. **scheduler** — runs tasks in the right order and at the right time,\n"
            "2. **data availability** — determines how difficult fresh training-data creation is,\n"
            "3. **model store** — stores and versions model artifacts.\n"
            "\n"
            "A model store should make it possible to find the model artifact and enough "
            "metadata to reproduce or understand it later.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Feature reuse with log and wait\n"
            "\n"
            "Fresh production examples have already passed through the prediction pipeline.\n"
            "\n"
            "That pipeline already computed the model's features.\n"
            "\n"
            "Instead of computing them again for retraining, some systems **log the "
            "serving-time features and wait for the label**.\n"
            "\n"
            "```text\n"
            "Prediction request\n"
            "      ↓\n"
            "Serving feature extraction\n"
            "      ↓\n"
            "Log features + prediction metadata\n"
            "      ↓\n"
            "Wait for feedback / label\n"
            "      ↓\n"
            "Join label with logged features\n"
            "      ↓\n"
            "New training example\n"
            "```\n"
            "\n"
            "This can:\n"
            "\n"
            "- save feature-computation cost,\n"
            "- increase consistency between serving and training,\n"
            "- reduce train-serving skew.\n"
            "\n"
            "[[IMAGE_NEEDED: Log-and-wait feature reuse | "
            "A production inference request whose computed features are logged, "
            "then later joined with delayed feedback to create a training example | "
            "Learner should notice that retraining can reuse the exact features "
            "seen by the live model]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Stage 3: automated stateful training\n"
            "\n"
            "Stage 3 changes the automatic update process so it does not start from scratch.\n"
            "\n"
            "The pipeline first finds and loads the previous checkpoint, then continues "
            "training from that state using fresh data.\n"
            "\n"
            "```text\n"
            "Find previous checkpoint\n"
            "       ↓\n"
            "Load model state\n"
            "       ↓\n"
            "Train on fresh data\n"
            "       ↓\n"
            "Evaluate new version\n"
            "       ↓\n"
            "Store version + lineage\n"
            "```\n"
            "\n"
            "### Lineage becomes essential\n"
            "\n"
            "Imagine these model branches:\n"
            "\n"
            "```text\n"
            "1.0 → 1.1 → 1.2 → ... → 1.64\n"
            "2.0 → 2.1 → ... → 2.11\n"
            "3.0 → ... → 3.32\n"
            "```\n"
            "\n"
            "For each version, you may need to know:\n"
            "\n"
            "- which model was its parent,\n"
            "- which data updated it,\n"
            "- which feature version was used,\n"
            "- which code produced it,\n"
            "- what evaluation it passed.\n"
            "\n"
            "Without lineage, reproducing and debugging stateful evolution becomes very difficult.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Stage 4: trigger-driven continual learning\n"
            "\n"
            "At Stage 3, updates are automated but still often happen on a fixed schedule.\n"
            "\n"
            "Stage 4 makes the update schedule adaptive.\n"
            "\n"
            "The chapter gives four possible triggers:\n"
            "\n"
            "### Time-based\n"
            "\n"
            "```text\n"
            "Update every 5 minutes / hour / day\n"
            "```\n"
            "\n"
            "### Performance-based\n"
            "\n"
            "```text\n"
            "Update when model performance falls below a threshold\n"
            "```\n"
            "\n"
            "### Volume-based\n"
            "\n"
            "```text\n"
            "Update when newly labeled data increases by 5%\n"
            "```\n"
            "\n"
            "### Drift-based\n"
            "\n"
            "```text\n"
            "Update when a significant distribution shift is detected\n"
            "```\n"
            "\n"
            "This stage requires a strong monitoring system. If drift detection produces "
            "many false alarms, the training system can retrain far more often than necessary.\n"
            "\n"
            "It also requires an evaluation pipeline strong enough to reject bad updates automatically.\n"
            "\n"
            "[[IMAGE_NEEDED: Trigger-driven continual-learning pipeline | "
            "Four trigger sources—time, performance, data volume, drift—feeding an "
            "update pipeline with training, evaluation gate, model store, and deployment | "
            "Learner should notice that retraining triggers depend on trustworthy monitoring]]\n"
            "\n"
            "{{exercise:M09.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 17. How often should you update? Measure the value of data freshness\n"
            "\n"
            "There is no universal answer to \"How often should this model retrain?\"\n"
            "\n"
            "The right question is:\n"
            "\n"
            "> **How much performance gain does fresher data provide?**\n"
            "\n"
            "The chapter proposes an experiment.\n"
            "\n"
            "Suppose you want to predict December behavior using historical data.\n"
            "\n"
            "Train several model versions:\n"
            "\n"
            "```text\n"
            "Model A: train Jan–Jun  → test December\n"
            "Model B: train Apr–Sep  → test December\n"
            "Model C: train Jun–Nov  → test December\n"
            "```\n"
            "\n"
            "If the model trained on the freshest window is meaningfully better, recent "
            "data has high value and frequent retraining may be justified.\n"
            "\n"
            "If performance barely changes, frequent updates may add infrastructure cost "
            "without enough benefit.\n"
            "\n"
            "This experiment can be performed at finer scales—months, weeks, days, hours, "
            "or even minutes depending on the task.\n"
            "\n"
            "[[IMAGE_NEEDED: Measuring the value of data freshness | "
            "Several training windows ending progressively closer to a fixed modern test "
            "window, with model performance increasing or flattening as training data "
            "becomes fresher | Learner should notice that update frequency should be "
            "supported by measured performance gain rather than intuition]]\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Spend effort on model iteration or data iteration?\n"
            "\n"
            "You have limited engineering and compute resources.\n"
            "\n"
            "Suppose:\n"
            "\n"
            "- a new architecture costs 100× more to train and improves performance 1%,\n"
            "- refreshing the existing model on the latest three hours of data costs 1× "
            "and also improves performance 1%.\n"
            "\n"
            "The source argues that the second option may be the better use of resources.\n"
            "\n"
            "On the other hand, if data refreshes add little value, resources may be better "
            "spent improving the model or features.\n"
            "\n"
            "This is an empirical decision. Run experiments rather than assuming model "
            "iteration or data iteration is always superior.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Why offline evaluation alone is not enough\n"
            "\n"
            "Updated models should still pass offline evaluation, but two offline methods "
            "have important limitations.\n"
            "\n"
            "### Static test set\n"
            "\n"
            "A static test set is valuable because all model versions are compared against "
            "the same trusted benchmark.\n"
            "\n"
            "But if the production distribution has shifted, the static test set may represent "
            "yesterday's world rather than today's.\n"
            "\n"
            "### Backtest\n"
            "\n"
            "A **backtest** evaluates the model on data from a recent historical period.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Train/update on data through yesterday\n"
            "Test on the most recent hour not used in training\n"
            "```\n"
            "\n"
            "This better reflects current conditions, but recent data can itself be corrupted "
            "by a pipeline incident.\n"
            "\n"
            "Therefore the chapter recommends using both:\n"
            "\n"
            "- a trusted static test set as a sanity check,\n"
            "- a recent backtest for freshness.\n"
            "\n"
            "Even this does not guarantee future production performance. The final environment "
            "is production itself.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Test in production complements monitoring\n"
            "\n"
            "The source draws a useful distinction:\n"
            "\n"
            "- **Monitoring** passively observes whichever model is already serving.\n"
            "- **Test in production** actively decides which model should produce outputs "
            "so the models can be evaluated under live conditions.\n"
            "\n"
            "The goal is not reckless deployment. The chapter presents several techniques "
            "for reducing risk:\n"
            "\n"
            "1. shadow deployment,\n"
            "2. A/B testing,\n"
            "3. canary release,\n"
            "4. interleaving experiments,\n"
            "5. bandits.\n"
            "\n"
            "[[IMAGE_NEEDED: Monitoring versus test in production | "
            "A split diagram where monitoring observes one production model, while test "
            "in production deliberately routes or duplicates live traffic among candidate "
            "models for comparison | Learner should notice the passive versus proactive distinction]]\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Shadow deployment: evaluate live traffic without changing user output\n"
            "\n"
            "Shadow deployment is one of the lowest-risk ways to test a candidate model.\n"
            "\n"
            "Process:\n"
            "\n"
            "1. deploy the candidate alongside the champion,\n"
            "2. send each incoming request to both,\n"
            "3. serve only the champion's prediction,\n"
            "4. log the candidate's prediction,\n"
            "5. compare the results,\n"
            "6. promote only if satisfactory.\n"
            "\n"
            "```text\n"
            "Incoming request\n"
            "      ├────────→ Champion → user\n"
            "      │\n"
            "      └────────→ Challenger → logs only\n"
            "```\n"
            "\n"
            "The candidate cannot directly harm users because its output is not served.\n"
            "\n"
            "The main cost is compute: both models run for the same traffic, potentially "
            "doubling inference workload.\n"
            "\n"
            "[[IMAGE_NEEDED: Shadow deployment | "
            "One production request duplicated to champion and challenger, with only "
            "champion output returned to the user and challenger output stored for analysis | "
            "Learner should notice that the candidate sees real traffic without affecting users]]\n"
            "\n"
            "---\n"
            "\n"

            "## 22. A/B testing: randomized live comparison\n"
            "\n"
            "A/B testing routes different portions of real traffic to different variants.\n"
            "\n"
            "For model evaluation:\n"
            "\n"
            "- A = existing model,\n"
            "- B = candidate model.\n"
            "\n"
            "Process:\n"
            "\n"
            "```text\n"
            "Production traffic\n"
            "      ↓ random assignment\n"
            "  ┌─────────────┐\n"
            "  ↓             ↓\n"
            "Model A       Model B\n"
            "  ↓             ↓\n"
            "User feedback + metrics\n"
            "      ↓\n"
            "Statistical comparison\n"
            "```\n"
            "\n"
            "Two requirements emphasized in the chapter are critical.\n"
            "\n"
            "### Randomized assignment\n"
            "\n"
            "If mobile users mostly get A and desktop users mostly get B, the models are "
            "confounded with device type. You cannot know whether the model or the audience "
            "caused the difference.\n"
            "\n"
            "### Sufficient sample size\n"
            "\n"
            "The experiment must run long enough to gather enough evidence for the target metric.\n"
            "\n"
            "A statistically significant result suggests enough evidence exists to distinguish "
            "the variants, but significance is not infallible. Repeating the experiment can "
            "occasionally produce a different winner.\n"
            "\n"
            "A non-significant result also does not necessarily mean the experiment failed. "
            "With enough data, it may indicate the two models are practically very similar.\n"
            "\n"
            "A/B testing can also extend beyond two variants: A/B/C, A/B/C/D, and so on.\n"
            "\n"
            "{{exercise:M09.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Canary release: increase traffic gradually\n"
            "\n"
            "A **canary** is a candidate model introduced to a small portion of production traffic.\n"
            "\n"
            "If it performs well, increase its share.\n"
            "\n"
            "If important metrics degrade, abort the rollout and return traffic to the champion.\n"
            "\n"
            "```text\n"
            "5% traffic → candidate looks good\n"
            "        ↓\n"
            "20% traffic → still good\n"
            "        ↓\n"
            "50% traffic → still good\n"
            "        ↓\n"
            "100% → candidate becomes champion\n"
            "```\n"
            "\n"
            "or:\n"
            "\n"
            "```text\n"
            "5% traffic → critical metric degrades\n"
            "        ↓\n"
            "Abort canary\n"
            "        ↓\n"
            "100% traffic back to existing model\n"
            "```\n"
            "\n"
            "Canary rollout resembles A/B infrastructure, but random traffic assignment is "
            "not always required. For example, a team might first release to a less critical market.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Interleaving: compare ranking models inside one user experience\n"
            "\n"
            "Suppose two ranking systems each produce ten recommendations.\n"
            "\n"
            "A/B testing exposes one user to one model.\n"
            "\n"
            "**Interleaving** combines recommendations from both models into one displayed list "
            "and uses user preference to determine which system contributed better items.\n"
            "\n"
            "This can require fewer samples than ordinary A/B tests for ranking problems.\n"
            "\n"
            "But position matters. Top-ranked items naturally receive more clicks.\n"
            "\n"
            "For a valid comparison, an item appearing at a given position should be equally "
            "likely to come from either ranking system.\n"
            "\n"
            "The chapter describes **team-draft interleaving**:\n"
            "\n"
            "1. choose A or B randomly for the next slot,\n"
            "2. that model contributes its highest-ranked item not already chosen,\n"
            "3. repeat until the mixed list is complete.\n"
            "\n"
            "[[IMAGE_NEEDED: A/B testing versus interleaving | "
            "A/B side shows separate users receiving full lists from A or B; interleaving "
            "side shows one list composed of alternating/random contributions from A and B | "
            "Learner should notice that interleaving compares ranking preferences within the "
            "same user experience]]\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Multi-armed bandits: evaluate while favoring better models\n"
            "\n"
            "A/B testing allocates traffic according to a fixed experiment design.\n"
            "\n"
            "A **multi-armed bandit** changes allocation based on what has been learned so far.\n"
            "\n"
            "Imagine each candidate model is a slot machine with an unknown payout.\n"
            "\n"
            "You want to answer two questions at once:\n"
            "\n"
            "1. Which model is best?\n"
            "2. How can we avoid wasting too much traffic on models that already appear worse?\n"
            "\n"
            "This creates the classic **exploration-exploitation trade-off**:\n"
            "\n"
            "- **exploit:** send traffic to the current best model,\n"
            "- **explore:** still test uncertain alternatives in case one is actually better.\n"
            "\n"
            "Bandit-based model evaluation requires:\n"
            "\n"
            "- online prediction,\n"
            "- preferably short feedback loops,\n"
            "- a feedback-collection mechanism,\n"
            "- continuous payoff/performance tracking,\n"
            "- dynamic request routing.\n"
            "\n"
            "The source notes that bandits can be far more data-efficient than A/B tests, "
            "but they are also harder to implement.\n"
            "\n"
            "[[IMAGE_NEEDED: Exploration versus exploitation for model traffic | "
            "Three candidate models with estimated rewards, most traffic going to the "
            "current best while a smaller amount explores uncertain alternatives | "
            "Learner should notice that bandit allocation adapts as evidence changes]]\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Epsilon-greedy, Thompson Sampling, and UCB\n"
            "\n"
            "### Epsilon-greedy\n"
            "\n"
            "Most of the time, route to the current best model. Sometimes explore another model.\n"
            "\n"
            "Example from the source's convention:\n"
            "\n"
            "```text\n"
            "90% → current best model\n"
            "10% → random alternative\n"
            "```\n"
            "\n"
            "The exact notation for epsilon can differ by convention; the important lesson "
            "here is the exploitation/exploration split described in the chapter.\n"
            "\n"
            "### Thompson Sampling\n"
            "\n"
            "Select a model according to the probability that it is optimal under current knowledge.\n"
            "\n"
            "A model with strong evidence receives more traffic, but uncertain alternatives continue "
            "to receive opportunities.\n"
            "\n"
            "### Upper Confidence Bound (UCB)\n"
            "\n"
            "Choose the candidate with the highest optimistic upper confidence estimate.\n"
            "\n"
            "Uncertain candidates receive an **exploration bonus**, which encourages the system "
            "to gather more evidence about them.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Contextual bandits: explore actions, not just model versions\n"
            "\n"
            "The chapter uses a specific terminology distinction.\n"
            "\n"
            "A **bandit for model evaluation** chooses which model should serve a request.\n"
            "\n"
            "A **contextual bandit** chooses which action or item to show based on context.\n"
            "\n"
            "Suppose a recommender has 1,000 possible items but can display only 10.\n"
            "\n"
            "The system receives feedback only for displayed items. It does not know how the "
            "user would have reacted to the 990 unseen items.\n"
            "\n"
            "This is the **partial feedback** or **bandit feedback** problem.\n"
            "\n"
            "If the system always displays only the currently highest-valued items, unseen items "
            "may never receive enough exposure to reveal whether they are actually good.\n"
            "\n"
            "Contextual bandits balance:\n"
            "\n"
            "- showing items already believed to be relevant,\n"
            "- showing uncertain items to learn more about them.\n"
            "\n"
            "Unlike general reinforcement learning, contextual bandits receive feedback after "
            "one action rather than needing a long sequence of actions before reward appears.\n"
            "\n"
            "The chapter notes that contextual bandits can be powerful but are harder to generalize "
            "across use cases because the exploration strategy can depend on the model architecture.\n"
            "\n"
            "{{exercise:M09.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Standardize and automate model evaluation\n"
            "\n"
            "A strong evaluation system is not only about **which tests** exist.\n"
            "\n"
            "It is also about **who runs them, in what order, with what thresholds, and "
            "what happens when one fails**.\n"
            "\n"
            "Ad hoc evaluation by each model author creates problems:\n"
            "\n"
            "- developers have more context than ordinary users,\n"
            "- different engineers may run different tests,\n"
            "- thresholds may change informally,\n"
            "- promotion decisions become inconsistent.\n"
            "\n"
            "The chapter recommends a pipeline similar in spirit to CI/CD:\n"
            "\n"
            "```text\n"
            "New model update\n"
            "      ↓\n"
            "Static offline tests\n"
            "      ↓\n"
            "Recent backtests\n"
            "      ↓\n"
            "Production-safety test\n"
            "      ↓\n"
            "Promotion threshold passed?\n"
            "   /             \\\n"
            " yes             no\n"
            "  ↓               ↓\n"
            "promote         reject / investigate\n"
            "```\n"
            "\n"
            "The exact tests depend on the application, but the process should be explicit, "
            "repeatable, reviewable, and as automated as practical.\n"
            "\n"
            "[[IMAGE_NEEDED: Automated model promotion pipeline | "
            "A gated pipeline from new model artifact through offline tests, backtest, "
            "shadow/A-B/canary or another production test, then promotion or rejection | "
            "Learner should notice that model updates move through standardized quality gates]]\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Continual learning means updating on every incoming sample\n"
            "\n"
            "Production systems often use micro-batches because per-sample updates are inefficient "
            "and can increase problems such as catastrophic forgetting.\n"
            "\n"
            "### Misconception 2: Continual learning means retraining as frequently as possible\n"
            "\n"
            "Frequency should be justified by the value of fresh data and bounded by evaluation capacity.\n"
            "\n"
            "### Misconception 3: Stateful training means you never train from scratch again\n"
            "\n"
            "Teams may periodically retrain from scratch for recalibration or model changes.\n"
            "\n"
            "### Misconception 4: Fast training guarantees fast iteration\n"
            "\n"
            "Fresh data, label computation, and trustworthy evaluation may be slower than training itself.\n"
            "\n"
            "### Misconception 5: Monitoring and test in production are the same thing\n"
            "\n"
            "Monitoring observes what is already serving; test in production actively routes or duplicates traffic to evaluate candidates.\n"
            "\n"
            "### Misconception 6: A recent backtest can replace the static test set\n"
            "\n"
            "Recent data can itself be corrupted. A trusted static benchmark remains a useful sanity check.\n"
            "\n"
            "### Misconception 7: Shadow deployment and A/B testing expose users to the candidate in the same way\n"
            "\n"
            "Shadow deployment does not serve challenger outputs to users; A/B testing does.\n"
            "\n"
            "### Misconception 8: A/B testing only requires splitting traffic\n"
            "\n"
            "Valid A/B experiments require appropriate randomization, adequate sample size, and meaningful metrics.\n"
            "\n"
            "### Misconception 9: Bandits are just faster A/B tests\n"
            "\n"
            "Bandits dynamically change routing according to observed performance and explicitly balance exploration with exploitation.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Continual learning | Infrastructure and training approach that enables models to be updated whenever needed as new data arrives. |\n"
            "| Continuous learning | Ambiguous term the source distinguishes from continual learning; often implies per-sample continuous updates or continuous delivery. |\n"
            "| Micro-batch | Small batch of recent examples used for an incremental model update. |\n"
            "| Catastrophic forgetting | Neural-network tendency to forget older learned information when learning new information abruptly. |\n"
            "| Champion | Current deployed model. |\n"
            "| Challenger | Candidate update evaluated against the champion. |\n"
            "| Stateless retraining | Training a new model from scratch for each update. |\n"
            "| Stateful training | Continuing training from a previous checkpoint. |\n"
            "| Data iteration | Updating an unchanged model and feature definition using newer data. |\n"
            "| Model iteration | Changing features or model architecture. |\n"
            "| Continuous cold start | Repeated cold-start-like situations caused by new context, device, stale history, or infrequent visits. |\n"
            "| Label computation | Converting behavioral events and prediction logs into supervised labels. |\n"
            "| Running statistics | Statistics updated incrementally as new data arrives. |\n"
            "| Scheduler | System that triggers and coordinates training workflow tasks. |\n"
            "| Model store | Store for model artifacts, versions, and associated metadata. |\n"
            "| Model lineage | Record of parent models, data, code, and transformations that produced a model version. |\n"
            "| Log and wait | Reuse serving-time features by logging them and joining them later with delayed labels. |\n"
            "| Data freshness | How recent the data used to update a model is. |\n"
            "| Backtest | Evaluation on a specific recent historical time period. |\n"
            "| Test in production | Evaluate candidate behavior with live production data under controlled exposure. |\n"
            "| Shadow deployment | Run champion and challenger on the same traffic but serve only champion output. |\n"
            "| A/B testing | Randomized experiment comparing variants on live traffic. |\n"
            "| Canary release | Gradual rollout of a candidate to increasing portions of traffic. |\n"
            "| Interleaving | Combine outputs from competing ranking models into one list to compare user preference. |\n"
            "| Multi-armed bandit | Adaptive traffic-allocation method balancing exploration and exploitation. |\n"
            "| Exploration | Gathering information about uncertain alternatives. |\n"
            "| Exploitation | Favoring the option currently believed to be best. |\n"
            "| Thompson Sampling | Bandit strategy that samples actions according to their probability of being optimal. |\n"
            "| UCB | Upper Confidence Bound strategy that adds an exploration bonus to uncertain alternatives. |\n"
            "| Contextual bandit | Bandit problem where context informs which action/item to choose and only chosen actions receive feedback. |\n"
            "| Partial feedback | Observing reward only for selected/displayed actions. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why is continual learning mainly an infrastructure problem in this chapter?\n"
            "2. Why do production systems often use micro-batches instead of per-sample updates?\n"
            "3. What is catastrophic forgetting?\n"
            "4. What are champion and challenger models?\n"
            "5. Why must a challenger be evaluated before replacing the champion?\n"
            "6. How does stateless retraining differ from stateful training?\n"
            "7. Why can stateful training require less data and compute?\n"
            "8. Why might stateful training reduce the need to permanently store training data?\n"
            "9. What is the difference between data iteration and model iteration?\n"
            "10. How can continual learning help with sudden distribution shifts?\n"
            "11. What is continuous cold start?\n"
            "12. Why is fresh data access difficult when training data comes from warehouses?\n"
            "13. What is label computation?\n"
            "14. Why are natural labels with short feedback loops useful for continual learning?\n"
            "15. Why can evaluation become the bottleneck even if training is fast?\n"
            "16. Why are some matrix-based models harder to update incrementally?\n"
            "17. Why do feature preprocessing statistics also need incremental treatment?\n"
            "18. What are the four continual-learning maturity stages?\n"
            "19. What three infrastructure factors are highlighted for automated retraining?\n"
            "20. How does log and wait reduce train-serving skew?\n"
            "21. Why does stateful training increase the importance of model lineage?\n"
            "22. What four trigger types can start a Stage-4 update?\n"
            "23. How can noisy monitoring create unnecessary retraining?\n"
            "24. How do you experimentally estimate the value of data freshness?\n"
            "25. When might data iteration be more cost-effective than model iteration?\n"
            "26. Why should a recent backtest not completely replace a trusted static test set?\n"
            "27. How does test in production differ from monitoring?\n"
            "28. Why is shadow deployment low risk but compute expensive?\n"
            "29. What two requirements are especially important for valid A/B testing?\n"
            "30. How does canary release reduce rollout risk?\n"
            "31. Why can interleaving require fewer samples for ranking comparisons?\n"
            "32. Why must interleaving account for position bias?\n"
            "33. What is the exploration-exploitation trade-off?\n"
            "34. What infrastructure does model-evaluation bandit routing require?\n"
            "35. How do epsilon-greedy, Thompson Sampling, and UCB differ conceptually?\n"
            "36. What is the partial-feedback problem in contextual bandits?\n"
            "37. Why should model evaluation pipelines be standardized rather than ad hoc?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A maintainable ML system must be able not only to detect change, but also "
            "to update itself safely. Continual learning provides the update capability, "
            "while test in production provides the evidence needed to decide whether a "
            "new model deserves to become the new champion.**\n"
        ),

        "estimated_minutes": 255,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "continual-learning-intro", "title": "Continual learning is an infrastructure capability", "order": 1},
            {"id": "micro-batches", "title": "Continual learning does not mean learning from every single event", "order": 2},
            {"id": "champion-challenger", "title": "Never update the live model blindly: champion and challenger", "order": 3},
            {"id": "stateful-stateless", "title": "Stateless retraining versus stateful training", "order": 4},
            {"id": "data-model-iteration", "title": "Data iteration versus model iteration", "order": 5},
            {"id": "why-continual", "title": "Why continual learning can matter", "order": 6},
            {"id": "fresh-data-challenge", "title": "Challenge 1: getting fresh data and fresh labels", "order": 7},
            {"id": "label-computation", "title": "Label computation from behavioral logs", "order": 8},
            {"id": "evaluation-challenge", "title": "Challenge 2: evaluating every update safely", "order": 9},
            {"id": "algorithm-challenge", "title": "Challenge 3: some algorithms are easier to update incrementally", "order": 10},
            {"id": "four-stages", "title": "Four stages toward continual learning", "order": 11},
            {"id": "stage-one", "title": "Stage 1: manual, stateless retraining", "order": 12},
            {"id": "stage-two", "title": "Stage 2: automated stateless retraining", "order": 13},
            {"id": "log-and-wait", "title": "Feature reuse with log and wait", "order": 14},
            {"id": "stage-three", "title": "Stage 3: automated stateful training", "order": 15},
            {"id": "stage-four", "title": "Stage 4: trigger-driven continual learning", "order": 16},
            {"id": "data-freshness", "title": "How often should you update? Measure the value of data freshness", "order": 17},
            {"id": "iteration-tradeoff", "title": "Spend effort on model iteration or data iteration?", "order": 18},
            {"id": "offline-before-production", "title": "Why offline evaluation alone is not enough", "order": 19},
            {"id": "test-in-production", "title": "Test in production complements monitoring", "order": 20},
            {"id": "shadow", "title": "Shadow deployment: evaluate live traffic without changing user output", "order": 21},
            {"id": "ab-testing", "title": "A/B testing: randomized live comparison", "order": 22},
            {"id": "canary", "title": "Canary release: increase traffic gradually", "order": 23},
            {"id": "interleaving", "title": "Interleaving: compare ranking models inside one user experience", "order": 24},
            {"id": "bandits", "title": "Multi-armed bandits: evaluate while favoring better models", "order": 25},
            {"id": "bandit-algorithms", "title": "Epsilon-greedy, Thompson Sampling, and UCB", "order": 26},
            {"id": "contextual-bandits", "title": "Contextual bandits: explore actions, not just model versions", "order": 27},
            {"id": "evaluation-pipeline", "title": "Standardize and automate model evaluation", "order": 28},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M09.L01.EX01",

            "title": "Choose stateful or stateless updating",

            "lesson_code": "M09.L01",

            "section_id": "stateful-stateless",

            "placement": "after_section",

            "description": (
                "Practice choosing between training from scratch and continuing from "
                "an existing checkpoint."
            ),

            "instructions": (
                "For each scenario, choose stateful training, stateless retraining, "
                "or a combination, and explain your reasoning:\n\n"
                "1. A ranking model keeps the same features and architecture but receives "
                "fresh click data every day.\n"
                "2. The team adds three new features and changes the output layer.\n"
                "3. A mature production model is fine-tuned daily, but the team wants "
                "periodic recalibration on a large historical dataset.\n"
                "4. User data must not be kept in permanent storage after it has been used.\n\n"
                "For each case, state one infrastructure requirement."
            ),

            "expected_output": (
                "Four update choices with justification and one required infrastructure "
                "capability such as checkpoint loading, lineage, data access, or full retraining."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "stateful-training",
                "stateless-retraining",
                "model-iteration",
                "data-iteration",
            ],
        },

        {
            "id": "M09.L01.EX02",

            "title": "Design a Stage-4 update trigger",

            "lesson_code": "M09.L01",

            "section_id": "stage-four",

            "placement": "after_section",

            "description": (
                "Use monitoring, fresh data, evaluation, and model lineage to design "
                "a safe trigger-driven continual-learning workflow."
            ),

            "instructions": (
                "You operate an online ranking model whose behavior changes rapidly "
                "during major shopping events.\n\n"
                "Design a continual-learning trigger system that includes:\n"
                "1. one time-based trigger,\n"
                "2. one performance-based trigger,\n"
                "3. one volume-based trigger,\n"
                "4. one drift-based trigger,\n"
                "5. rules to prevent repeated retraining from noisy alerts,\n"
                "6. how the challenger is evaluated before promotion,\n"
                "7. what lineage information you store for each update."
            ),

            "expected_output": (
                "A trigger-to-training-to-evaluation-to-promotion workflow with "
                "guardrails against noisy monitoring and bad model updates."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "continual-learning",
                "retraining-triggers",
                "monitoring",
                "model-lineage",
            ],
        },

        {
            "id": "M09.L01.EX03",

            "title": "Choose a safe production test",

            "lesson_code": "M09.L01",

            "section_id": "ab-testing",

            "placement": "after_section",

            "description": (
                "Compare shadow deployment, A/B testing, and canary release for "
                "different risk profiles."
            ),

            "instructions": (
                "Choose the most appropriate technique for each scenario and justify it:\n\n"
                "1. A new fraud model must see real traffic, but its decisions must not "
                "affect users yet.\n"
                "2. Two recommendation models need a randomized comparison on engagement.\n"
                "3. A candidate model should first receive 5% of traffic, then more only "
                "if key metrics remain healthy.\n"
                "4. A ranking team wants to compare two result lists using fewer users "
                "than a traditional A/B test might require.\n\n"
                "For the A/B case, explain why random assignment and adequate sample size matter."
            ),

            "expected_output": (
                "Four technique selections using shadow, A/B, canary, or interleaving, "
                "plus the statistical requirements of the A/B experiment."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "shadow-deployment",
                "ab-testing",
                "canary-release",
                "interleaving",
            ],
        },

        {
            "id": "M09.L01.EX04",

            "title": "Reason about exploration and exploitation",

            "lesson_code": "M09.L01",

            "section_id": "contextual-bandits",

            "placement": "after_section",

            "description": (
                "Compare fixed experiments with adaptive bandit strategies."
            ),

            "instructions": (
                "You have three recommendation models and short feedback loops from clicks.\n\n"
                "1. Explain why a bandit can use traffic more efficiently than a fixed "
                "A/B/C split.\n"
                "2. Describe exploitation and exploration in this setting.\n"
                "3. Describe an epsilon-greedy strategy.\n"
                "4. Explain the intuition behind Thompson Sampling.\n"
                "5. Explain the intuition behind UCB's uncertainty bonus.\n"
                "6. Then switch from model selection to item recommendation and explain "
                "why recommending only the current top items creates a partial-feedback problem.\n"
                "7. Explain how a contextual bandit addresses that problem."
            ),

            "expected_output": (
                "A concise comparison of adaptive model routing and contextual item "
                "exploration, including the exploration-exploitation trade-off."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "multi-armed-bandits",
                "exploration-exploitation",
                "thompson-sampling",
                "ucb",
                "contextual-bandits",
            ],
        },

        {
            "id": "M09.L01.EX05",

            "title": "Measure whether fresher data is worth the cost",

            "lesson_code": "M09.L01",

            "section_id": "data-freshness",

            "placement": "after_section",

            "description": (
                "Design a freshness experiment instead of choosing retraining frequency by intuition."
            ),

            "instructions": (
                "You have one year of timestamped training data and want to decide "
                "between monthly, weekly, and daily updates.\n\n"
                "1. Design at least three training windows with different freshness levels.\n"
                "2. Choose one common recent evaluation period that is excluded from all training windows.\n"
                "3. State which model-quality metric you would compare.\n"
                "4. State one compute or operational cost you would compare alongside quality.\n"
                "5. Explain what result would justify daily retraining.\n"
                "6. Explain what result would suggest that model iteration may deserve "
                "more effort than data iteration."
            ),

            "expected_output": (
                "A controlled data-freshness experiment that connects measured quality "
                "gain to update cost."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "data-freshness",
                "retraining-frequency",
                "experimental-design",
                "data-iteration",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M09.L01.QZ01",

        "title": "Continual Learning and Test in Production — Knowledge Check",

        "lesson_code": "M09.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M09.L01.Q01",
                "section_id": "continual-learning-intro",
                "question": (
                    "Which statement best captures continual learning as presented in the chapter?"
                ),
                "options": [
                    "A model must update after every individual sample.",
                    "The system is designed so models can be updated safely whenever updates are needed.",
                    "The model must be retrained from scratch every five minutes.",
                    "Only the optimizer changes over time.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter emphasizes update capability and infrastructure rather "
                    "than one mandatory update frequency."
                ),
            },

            {
                "id": "M09.L01.Q02",
                "section_id": "micro-batches",
                "question": (
                    "Why are micro-batches commonly preferred over one-example-at-a-time training?"
                ),
                "options": [
                    "Micro-batches avoid all evaluation.",
                    "They better use batch-oriented hardware and reduce the inefficiency of single-sample updates.",
                    "A neural network cannot train on one example.",
                    "Micro-batches eliminate distribution shift.",
                ],
                "correct": 1,
                "explanation": (
                    "Modern hardware is optimized for batch computation, and per-sample "
                    "training can waste compute."
                ),
            },

            {
                "id": "M09.L01.Q03",
                "section_id": "champion-challenger",
                "question": (
                    "What is the purpose of the champion-challenger pattern?"
                ),
                "options": [
                    "Modify the live model directly without evaluation.",
                    "Evaluate an updated replica before replacing the deployed model.",
                    "Remove the need for model versioning.",
                    "Make every model stateful.",
                ],
                "correct": 1,
                "explanation": (
                    "The challenger provides a safe candidate that can be rejected if evaluation fails."
                ),
            },

            {
                "id": "M09.L01.Q04",
                "section_id": "stateful-stateless",
                "question": (
                    "What distinguishes stateful training from stateless retraining?"
                ),
                "options": [
                    "Stateful training continues from a previous checkpoint; stateless retraining starts from scratch.",
                    "Stateful training never uses new data.",
                    "Stateless retraining cannot use historical data.",
                    "There is no difference.",
                ],
                "correct": 0,
                "explanation": (
                    "The defining difference is whether previous model state is reused."
                ),
            },

            {
                "id": "M09.L01.Q05",
                "section_id": "data-model-iteration",
                "question": (
                    "Which is an example of data iteration?"
                ),
                "options": [
                    "Adding a new feature to the model.",
                    "Changing the model architecture.",
                    "Refreshing the same model and feature definition with newer data.",
                    "Replacing the output layer with a different number of classes.",
                ],
                "correct": 2,
                "explanation": (
                    "Data iteration changes the data while holding the feature and model definition fixed."
                ),
            },

            {
                "id": "M09.L01.Q06",
                "section_id": "why-continual",
                "question": (
                    "What is continuous cold start?"
                ),
                "options": [
                    "Only the first prediction for a brand-new user.",
                    "Repeated cold-start-like situations caused by new contexts, devices, missing login, or stale history.",
                    "A model that cannot load its checkpoint.",
                    "A training job that runs out of memory.",
                ],
                "correct": 1,
                "explanation": (
                    "Existing users can effectively become cold when historical context "
                    "is absent, stale, or inappropriate."
                ),
            },

            {
                "id": "M09.L01.Q07",
                "section_id": "label-computation",
                "question": (
                    "What is label computation?"
                ),
                "options": [
                    "Choosing the number of classes manually.",
                    "Matching behavioral feedback back to prior predictions to construct training labels.",
                    "Compressing the model's output layer.",
                    "Selecting a batch size.",
                ],
                "correct": 1,
                "explanation": (
                    "Behavioral events must often be joined with earlier prediction logs "
                    "before they can serve as supervised labels."
                ),
            },

            {
                "id": "M09.L01.Q08",
                "section_id": "evaluation-challenge",
                "question": (
                    "Why can evaluation limit how frequently a model is updated?"
                ),
                "options": [
                    "Evaluation is always instantaneous.",
                    "Enough trustworthy feedback or rare positive examples may take time to accumulate.",
                    "Evaluation only happens before the first deployment.",
                    "Frequent updates eliminate the need for labels.",
                ],
                "correct": 1,
                "explanation": (
                    "The team cannot safely promote updates faster than it can gather "
                    "reliable evidence that they are good."
                ),
            },

            {
                "id": "M09.L01.Q09",
                "section_id": "algorithm-challenge",
                "question": (
                    "Why can incremental feature scaling be difficult?"
                ),
                "options": [
                    "Scaling requires no statistics.",
                    "Statistics computed independently on tiny batches may fluctuate too much between updates.",
                    "Running statistics cannot be computed.",
                    "Models do not use numerical features.",
                ],
                "correct": 1,
                "explanation": (
                    "Continual systems may need stable running estimates rather than "
                    "independent micro-batch statistics."
                ),
            },

            {
                "id": "M09.L01.Q10",
                "section_id": "four-stages",
                "question": (
                    "Which stage first introduces automated stateful training?"
                ),
                "options": [
                    "Stage 1",
                    "Stage 2",
                    "Stage 3",
                    "Stage 4 only",
                ],
                "correct": 2,
                "explanation": (
                    "Stage 3 loads the previous checkpoint and continues training automatically."
                ),
            },

            {
                "id": "M09.L01.Q11",
                "section_id": "stage-two",
                "question": (
                    "Which three infrastructure factors does the chapter highlight for automated retraining?"
                ),
                "options": [
                    "Scheduler, data accessibility, and model store",
                    "GPU brand, IDE, and programming language",
                    "Only batch size, optimizer, and loss",
                    "Browser, mobile phone, and database schema",
                ],
                "correct": 0,
                "explanation": (
                    "Those three factors strongly affect whether the retraining workflow "
                    "can be automated reliably."
                ),
            },

            {
                "id": "M09.L01.Q12",
                "section_id": "log-and-wait",
                "question": (
                    "What is a main advantage of log and wait?"
                ),
                "options": [
                    "It uses the exact serving-time features later for retraining, improving training-serving consistency.",
                    "It eliminates all logs.",
                    "It prevents any label delay.",
                    "It requires retraining from scratch.",
                ],
                "correct": 0,
                "explanation": (
                    "Reusing already-computed serving features reduces redundant "
                    "computation and can reduce train-serving skew."
                ),
            },

            {
                "id": "M09.L01.Q13",
                "section_id": "stage-three",
                "question": (
                    "Why is lineage especially important for stateful training?"
                ),
                "options": [
                    "Model versions form chains or branches that depend on previous checkpoints and specific update data.",
                    "Stateful models have no versions.",
                    "Lineage is only needed for dashboards.",
                    "It replaces evaluation.",
                ],
                "correct": 0,
                "explanation": (
                    "Debugging or reproducing a stateful model requires knowing its parent "
                    "model and the data and code used for each update."
                ),
            },

            {
                "id": "M09.L01.Q14",
                "section_id": "stage-four",
                "question": (
                    "Which is NOT one of the trigger categories listed for continual learning?"
                ),
                "options": [
                    "Time-based",
                    "Performance-based",
                    "Volume-based",
                    "Random architecture replacement",
                ],
                "correct": 3,
                "explanation": (
                    "The chapter lists time-, performance-, volume-, and drift-based triggers."
                ),
            },

            {
                "id": "M09.L01.Q15",
                "section_id": "data-freshness",
                "question": (
                    "How does the chapter recommend deciding whether to retrain more frequently?"
                ),
                "options": [
                    "Choose the shortest interval your scheduler supports.",
                    "Measure performance gain from models trained on data windows with different freshness levels.",
                    "Always retrain daily.",
                    "Always wait for visible production failure.",
                ],
                "correct": 1,
                "explanation": (
                    "Retraining frequency should be informed by experiments measuring "
                    "the value of fresher data."
                ),
            },

            {
                "id": "M09.L01.Q16",
                "section_id": "offline-before-production",
                "question": (
                    "Why should recent backtests and a trusted static test set both be used?"
                ),
                "options": [
                    "Recent data reflects current conditions, while the static test set provides a stable sanity check.",
                    "They are identical.",
                    "Static tests are always fresher.",
                    "Backtests eliminate the need for production evaluation.",
                ],
                "correct": 0,
                "explanation": (
                    "Each catches weaknesses the other may miss."
                ),
            },

            {
                "id": "M09.L01.Q17",
                "section_id": "shadow",
                "question": (
                    "What makes shadow deployment relatively safe?"
                ),
                "options": [
                    "The candidate model never runs.",
                    "The candidate sees real requests, but its predictions are not served to users.",
                    "It requires no compute.",
                    "It immediately replaces the champion.",
                ],
                "correct": 1,
                "explanation": (
                    "The candidate can be evaluated on live inputs without changing user-facing decisions."
                ),
            },

            {
                "id": "M09.L01.Q18",
                "section_id": "ab-testing",
                "question": (
                    "Why must traffic assignment in an A/B test be randomized?"
                ),
                "options": [
                    "To prevent systematic differences between user groups from confounding the model comparison.",
                    "To reduce inference cost to zero.",
                    "To avoid collecting feedback.",
                    "To turn the experiment into a shadow deployment.",
                ],
                "correct": 0,
                "explanation": (
                    "Without randomization, differences in audience composition can be mistaken for model effects."
                ),
            },

            {
                "id": "M09.L01.Q19",
                "section_id": "canary",
                "question": (
                    "What is the defining idea of a canary release?"
                ),
                "options": [
                    "Run the candidate only offline.",
                    "Gradually increase candidate traffic if metrics remain healthy, otherwise roll back.",
                    "Always send 50% traffic to every model.",
                    "Combine recommendations from two models into one list.",
                ],
                "correct": 1,
                "explanation": (
                    "A canary limits initial exposure and expands only after the candidate proves healthy."
                ),
            },

            {
                "id": "M09.L01.Q20",
                "section_id": "interleaving",
                "question": (
                    "Why must interleaving account for recommendation position?"
                ),
                "options": [
                    "Items at higher positions naturally receive more exposure and clicks.",
                    "Position never affects user behavior.",
                    "Interleaving uses no user feedback.",
                    "Position only matters during training.",
                ],
                "correct": 0,
                "explanation": (
                    "Without controlling position, one model may appear better simply "
                    "because its items were shown in more favorable slots."
                ),
            },

            {
                "id": "M09.L01.Q21",
                "section_id": "bandits",
                "question": (
                    "What is the exploration-exploitation trade-off?"
                ),
                "options": [
                    "Balance using the current best option against gathering evidence about uncertain alternatives.",
                    "Choose between training and deployment.",
                    "Choose between CPU and GPU.",
                    "Balance precision and recall.",
                ],
                "correct": 0,
                "explanation": (
                    "Bandits must gain reward now while still learning whether another option could be better."
                ),
            },

            {
                "id": "M09.L01.Q22",
                "section_id": "bandit-algorithms",
                "question": (
                    "What is the core intuition behind UCB?"
                ),
                "options": [
                    "Always choose the option with the lowest mean.",
                    "Favor high estimated reward while giving uncertain options an exploration bonus.",
                    "Never explore once a leader exists.",
                    "Assign traffic randomly forever.",
                ],
                "correct": 1,
                "explanation": (
                    "UCB is optimistic under uncertainty and uses confidence bounds to encourage exploration."
                ),
            },

            {
                "id": "M09.L01.Q23",
                "section_id": "contextual-bandits",
                "question": (
                    "What is the partial-feedback problem in recommendations?"
                ),
                "options": [
                    "You observe feedback only for the items you actually show.",
                    "You receive labels for every possible item.",
                    "The model receives no context.",
                    "Only the champion can make predictions.",
                ],
                "correct": 0,
                "explanation": (
                    "Unshown actions do not reveal their reward, so the system must deliberately explore to learn about them."
                ),
            },

            {
                "id": "M09.L01.Q24",
                "section_id": "evaluation-pipeline",
                "type": "open",
                "question": (
                    "Design an automated promotion pipeline for a continually updated recommender model. "
                    "Include the fresh-data source, label computation, champion/challenger creation, "
                    "offline tests, recent backtest, one test-in-production method, promotion/rollback "
                    "rules, and the model-lineage information that should be stored."
                ),
            },
        ],

        "passing_score": 70,
    },
}
