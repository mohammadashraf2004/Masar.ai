"""M06.L01 — Model Development and Offline Evaluation.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 6, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M06.L01"
MODULE_ORDER = 6
MODULE_TITLE = "Model Development and Offline Evaluation"
MODULE_DESCRIPTION = (
    "Develop, debug, scale, compare, and evaluate ML models before production, "
    "with practical guidance on model selection, ensembles, experiment tracking, "
    "distributed training, AutoML, baselines, robustness, calibration, confidence, "
    "and slice-based evaluation."
)
SOURCE_CHAPTER = 6
SOURCE_PAGES = "Not provided"


TOPIC = {
    "title": "Model Development and Offline Evaluation",
    "slug": "ml-systems-design-m06-l01",
    "description": (
        "A production-focused guide to choosing and developing models, running "
        "reproducible experiments, debugging and scaling training, using ensembles "
        "and AutoML, and evaluating models offline with meaningful baselines, "
        "robustness tests, calibration, confidence, and slice-based analysis."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 4.0,
    "skill_tags": [
        "model-selection",
        "learning-curves",
        "ensembles",
        "bagging",
        "boosting",
        "stacking",
        "experiment-tracking",
        "versioning",
        "ml-debugging",
        "distributed-training",
        "data-parallelism",
        "model-parallelism",
        "pipeline-parallelism",
        "automl",
        "hyperparameter-tuning",
        "offline-evaluation",
        "baselines",
        "perturbation-testing",
        "invariance-testing",
        "directional-expectations",
        "calibration",
        "confidence",
        "slice-evaluation",
    ],
    "prerequisite_ids": ["M05.L01"],

    "lesson": {
        "title": "Model Development and Offline Evaluation",
        "content": (
            "# Model Development and Offline Evaluation\n"
            "\n"
            "> **Lesson:** M06.L01  \n"
            "> **Module:** Model Development and Offline Evaluation  \n"
            "> **Source alignment:** Chapter 6. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored curriculum "
            "adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Select candidate model families using task fit, constraints, and trade-offs.\n"
            "- Explain why state-of-the-art performance on a benchmark does not automatically mean production suitability.\n"
            "- Use simple models and baselines to make later improvements meaningful.\n"
            "- Interpret learning curves and reason about model performance now versus later.\n"
            "- Explain the importance of model assumptions.\n"
            "- Compare bagging, boosting, and stacking.\n"
            "- Track and version experiments for comparison and reproducibility.\n"
            "- Apply practical ML debugging techniques.\n"
            "- Explain data, model, and pipeline parallelism at a high level.\n"
            "- Explain hyperparameter tuning, neural architecture search, and learned optimizers.\n"
            "- Use the four phases of model development as a progression strategy.\n"
            "- Select meaningful offline baselines.\n"
            "- Apply perturbation, invariance, and directional-expectation tests.\n"
            "- Explain model calibration and confidence thresholds.\n"
            "- Evaluate model performance on critical slices instead of relying only on aggregate metrics.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Model selection is a systems decision\n"
            "\n"
            "When you reach the modeling stage, there are usually many algorithms "
            "that could solve the same task. The challenge is not finding *an* algorithm; "
            "it is selecting a small set of candidates that fit the task and the production constraints.\n"
            "\n"
            "For a text classification problem, candidates might include logistic "
            "regression, naive Bayes, recurrent networks, or transformer-based models. "
            "For anomaly detection, candidates might include nearest-neighbor methods, "
            "isolation forests, clustering, or neural networks.\n"
            "\n"
            "The chapter emphasizes that model selection should consider more than predictive performance:\n"
            "\n"
            "| Question | Why it matters |\n"
            "|---|---|\n"
            "| How much labeled data does it need? | Some model families are much more data-hungry. |\n"
            "| How expensive is training? | Training cost affects iteration speed and budget. |\n"
            "| How fast is inference? | Latency can determine whether a model is usable online. |\n"
            "| How much hardware does it need? | A GPU-dependent model may be operationally expensive. |\n"
            "| How interpretable is it? | Some applications require explanations. |\n"
            "| How easy is deployment? | Production complexity matters. |\n"
            "\n"
            "A simple logistic regression can be inferior in accuracy to a large neural network "
            "but still be the better first production model if it is fast, cheap, explainable, "
            "and easy to deploy.\n"
            "\n"
            "[[IMAGE_NEEDED: Model selection as a multidimensional trade-off | "
            "A radar or matrix-style comparison of two model candidates across predictive "
            "quality, training cost, inference latency, data requirement, deployability, "
            "and interpretability | Learner should notice that the highest-accuracy model "
            "is not automatically the best production choice]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Six practical tips for selecting models\n"
            "\n"
            "### Tip 1: Avoid the state-of-the-art trap\n"
            "\n"
            "A model can be state of the art because it performs best on a particular "
            "static benchmark. That does not prove it will be fast enough, affordable "
            "enough, maintainable enough, or even better on your own data.\n"
            "\n"
            "If a simpler solution satisfies the real requirements, use the simpler solution.\n"
            "\n"
            "### Tip 2: Start with the simplest useful model\n"
            "\n"
            "Simple models are valuable because they:\n"
            "\n"
            "1. are easier to deploy early,\n"
            "2. are easier to understand and debug,\n"
            "3. provide a baseline for more complex models.\n"
            "\n"
            "The chapter makes an important distinction: **simple** is not always the "
            "same as **low effort**. A pretrained complex model may be easy to start with "
            "because tooling and community support are mature. It can still be worth testing "
            "simpler alternatives so you know whether the complexity is justified.\n"
            "\n"
            "### Tip 3: Avoid human bias in comparisons\n"
            "\n"
            "If an engineer runs 100 experiments on one architecture but only two on another, "
            "the comparison is not fair. Model families should be evaluated with comparable "
            "effort, data, metrics, and tuning budgets.\n"
            "\n"
            "### Tip 4: Evaluate good performance now versus later\n"
            "\n"
            "A model that wins today may lose after more data arrives.\n"
            "\n"
            "A **learning curve** plots model performance against the amount of training data. "
            "It can reveal whether additional data is likely to help.\n"
            "\n"
            "The chapter also gives an example where one recommender model initially lost "
            "offline but could update continuously, eventually outperforming the initial winner.\n"
            "\n"
            "[[IMAGE_NEEDED: Learning curves for two model families | "
            "A plot of validation performance versus number of training examples for a simple "
            "model and a higher-capacity model, where the simple model starts stronger but the "
            "higher-capacity model continues improving | Learner should notice that the best "
            "model today may not be the best model after more data arrives]]\n"
            "\n"
            "### Tip 5: Evaluate the trade-offs that matter\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- false positives versus false negatives,\n"
            "- compute versus accuracy,\n"
            "- latency versus model complexity,\n"
            "- interpretability versus predictive performance.\n"
            "\n"
            "The right trade-off depends on the application. In fingerprint unlocking, a false "
            "positive can give access to an unauthorized user. In disease screening, a false "
            "negative can miss a sick patient.\n"
            "\n"
            "### Tip 6: Understand model assumptions\n"
            "\n"
            "Every model approximates reality using assumptions. Examples discussed in the chapter include:\n"
            "\n"
            "- **prediction assumption:** `Y` can be predicted from `X`,\n"
            "- **IID:** examples are independently drawn from the same distribution,\n"
            "- **smoothness:** similar inputs tend to have similar outputs,\n"
            "- **tractability:** required probability computations are feasible,\n"
            "- **linear boundaries:** linear classifiers assume linear decision boundaries,\n"
            "- **conditional independence:** naive Bayes assumes features are independent given the class,\n"
            "- **normality:** some statistical methods assume normally distributed data.\n"
            "\n"
            "A model can fail not because it is badly implemented, but because the world violates "
            "an assumption the model depends on.\n"
            "\n"
            "{{exercise:M06.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Ensembles: combine models instead of trusting one\n"
            "\n"
            "An ensemble combines predictions from multiple **base learners**.\n"
            "\n"
            "For classification, a simple ensemble may use majority vote. For regression, "
            "it may average predictions.\n"
            "\n"
            "The source gives a useful intuition. Suppose three classifiers each have 70% "
            "accuracy and make independent errors. The ensemble is correct whenever at least "
            "two models are correct:\n"
            "\n"
            "```text\n"
            "P(all 3 correct) = 0.7³ = 0.343\n"
            "P(exactly 2 correct) = 3 × 0.7² × 0.3 = 0.441\n"
            "\n"
            "Ensemble accuracy = 0.343 + 0.441 = 0.784\n"
            "```\n"
            "\n"
            "So three independent 70%-accurate models can yield 78.4% majority-vote accuracy.\n"
            "\n"
            "The independence assumption matters. If all three models make exactly the same "
            "mistakes, ensembling gives no gain. Diversity among base learners is valuable.\n"
            "\n"
            "The trade-off is operational: ensembles are more complex to deploy and maintain.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Bagging, boosting, and stacking\n"
            "\n"
            "### Bagging\n"
            "\n"
            "**Bagging** means bootstrap aggregating.\n"
            "\n"
            "1. Create multiple bootstrap datasets by sampling with replacement.\n"
            "2. Train one learner on each bootstrap.\n"
            "3. Combine predictions by vote or averaging.\n"
            "\n"
            "Bagging can reduce variance and improve stability. Random forests are a familiar example: "
            "they combine bootstrap sampling with randomness over available features.\n"
            "\n"
            "[[IMAGE_NEEDED: Bagging workflow | "
            "One original dataset branching into several bootstrap samples, each training a model, "
            "with model outputs merged by majority vote or averaging | Learner should notice that "
            "learners are trained independently on different resampled datasets]]\n"
            "\n"
            "### Boosting\n"
            "\n"
            "Boosting trains learners iteratively. Later learners focus more heavily on examples "
            "that earlier learners handled poorly.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Train learner 1\n"
            "      ↓\n"
            "Increase weight on its mistakes\n"
            "      ↓\n"
            "Train learner 2\n"
            "      ↓\n"
            "Focus again on remaining difficult examples\n"
            "      ↓\n"
            "Combine learners into a stronger predictor\n"
            "```\n"
            "\n"
            "Gradient boosting machines are a major family, with implementations such as XGBoost "
            "and LightGBM discussed in the chapter.\n"
            "\n"
            "### Stacking\n"
            "\n"
            "Stacking trains several base learners and then uses a **meta-learner** to combine "
            "their outputs.\n"
            "\n"
            "The meta-learner can be simple voting/averaging or another learned model such as "
            "logistic regression.\n"
            "\n"
            "[[IMAGE_NEEDED: Bagging versus boosting versus stacking | "
            "A three-panel comparison: independent bootstrapped models for bagging, sequential "
            "error-focused learners for boosting, and parallel base models feeding a meta-model "
            "for stacking | Learner should notice the different way each ensemble creates and "
            "combines diversity]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Experiment tracking and versioning\n"
            "\n"
            "Model development is experimental. Two runs can differ by only one hyperparameter "
            "and still produce very different outcomes.\n"
            "\n"
            "**Experiment tracking** records what happened during a run.  \n"
            "**Versioning** records enough of the experiment definition to compare or recreate it later.\n"
            "\n"
            "Useful things to track include:\n"
            "\n"
            "- train and validation loss curves,\n"
            "- metrics such as accuracy, F1, or perplexity,\n"
            "- example inputs, predictions, and ground truth labels,\n"
            "- training speed,\n"
            "- CPU/GPU utilization and memory,\n"
            "- learning rate over time,\n"
            "- gradient norms,\n"
            "- weight norms,\n"
            "- logs and intermediate artifacts.\n"
            "\n"
            "Tracking improves observability into the learning process and helps explain why one run "
            "behaves differently from another.\n"
            "\n"
            "### Version more than code\n"
            "\n"
            "ML systems depend on **code and data**, so reproducibility requires both.\n"
            "\n"
            "Data versioning is harder than code versioning because datasets are large, may not fit "
            "on local machines, and are not naturally represented as line-by-line text diffs.\n"
            "\n"
            "Privacy regulations can make old data versions impossible to preserve indefinitely if "
            "user data must later be deleted.\n"
            "\n"
            "Even strong tracking does not guarantee exact reproducibility because hardware and ML "
            "frameworks can introduce nondeterminism.\n"
            "\n"
            "[[IMAGE_NEEDED: Reproducible experiment bundle | "
            "A central experiment ID connected to code version, data version, hyperparameters, "
            "environment, metrics, logs, and model artifacts | Learner should notice that reproducing "
            "an ML experiment requires much more than remembering the learning rate]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Debugging ML models\n"
            "\n"
            "ML debugging is unusually difficult for three reasons:\n"
            "\n"
            "1. **Failures can be silent.** Code runs and predictions are returned, but they are wrong.\n"
            "2. **Validation is slow.** A suspected fix may require retraining for hours.\n"
            "3. **Systems are cross-functional.** The fault might live in data, labels, features, "
            "model code, hyperparameters, or infrastructure.\n"
            "\n"
            "Possible failure sources include:\n"
            "\n"
            "- violated theoretical assumptions,\n"
            "- implementation bugs,\n"
            "- poor hyperparameters,\n"
            "- data or label problems,\n"
            "- outdated preprocessing statistics,\n"
            "- bad feature choices.\n"
            "\n"
            "The chapter recommends both preventive and curative debugging habits.\n"
            "\n"
            "### Debugging technique 1: start simple\n"
            "\n"
            "Build the smallest plausible version first. Add complexity one component at a time. "
            "If performance breaks after adding a component, the search space for the bug is small.\n"
            "\n"
            "### Debugging technique 2: overfit one tiny batch\n"
            "\n"
            "Take a very small set of examples and train/evaluate on the same examples. "
            "The model should be able to nearly memorize them.\n"
            "\n"
            "If an image classifier cannot reach near-perfect training accuracy on ten examples, "
            "there may be a bug in the implementation or training procedure.\n"
            "\n"
            "### Debugging technique 3: set a random seed\n"
            "\n"
            "Random initialization, dropout, and shuffling add run-to-run variation. Fixing a seed "
            "makes comparisons more controlled and makes failures easier to reproduce.\n"
            "\n"
            "{{exercise:M06.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Distributed training and memory constraints\n"
            "\n"
            "Modern models and datasets can be too large for one machine.\n"
            "\n"
            "When the dataset does not fit in memory, preprocessing, shuffling, and batching may need "
            "out-of-core and parallel techniques.\n"
            "\n"
            "Sometimes the model or even one sample is too large. The chapter discusses "
            "**gradient checkpointing**, which trades additional computation for reduced memory use.\n"
            "\n"
            "### Data parallelism\n"
            "\n"
            "Each worker stores a copy of the model, receives a different subset of data, computes "
            "gradients, and contributes to parameter updates.\n"
            "\n"
            "Two update styles are discussed:\n"
            "\n"
            "- **synchronous SGD:** wait for all workers before updating,\n"
            "- **asynchronous SGD:** update as gradients arrive.\n"
            "\n"
            "Synchronous training can suffer from **stragglers**: one slow worker delays everyone.\n"
            "\n"
            "Asynchronous training can suffer from **gradient staleness**: a gradient may have been "
            "computed using weights that have already changed.\n"
            "\n"
            "Very large distributed batch sizes also change optimization behavior. Increasing batch "
            "size can reduce the number of update steps, but eventually yields diminishing returns "
            "and may require careful learning-rate adjustment.\n"
            "\n"
            "### Model parallelism\n"
            "\n"
            "Different parts of one model live on different machines.\n"
            "\n"
            "This is useful when the model itself cannot fit on one device. But merely putting "
            "different layers on different machines does not guarantee true parallel execution if "
            "later layers must wait for earlier ones.\n"
            "\n"
            "### Pipeline parallelism\n"
            "\n"
            "Pipeline parallelism splits a mini-batch into micro-batches so different machines can "
            "work on different stages simultaneously.\n"
            "\n"
            "[[IMAGE_NEEDED: Data, model, and pipeline parallelism | "
            "Three diagrams: replicated models processing different data shards, one model split "
            "across machines, and micro-batches flowing through model stages like an assembly line "
            "| Learner should notice what is split in each strategy: data, model components, or staged computation]]\n"
            "\n"
            "Data and model parallelism can also be combined, though engineering becomes more complex.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. AutoML: automate parts of model development\n"
            "\n"
            "AutoML broadly means automating the search for model configurations that solve a task.\n"
            "\n"
            "### Soft AutoML: hyperparameter tuning\n"
            "\n"
            "Hyperparameters include choices such as:\n"
            "\n"
            "- learning rate,\n"
            "- batch size,\n"
            "- hidden-layer count,\n"
            "- hidden width,\n"
            "- dropout probability,\n"
            "- optimizer parameters,\n"
            "- numeric precision or quantization choices.\n"
            "\n"
            "Common search methods include:\n"
            "\n"
            "- grid search,\n"
            "- random search,\n"
            "- Bayesian optimization.\n"
            "\n"
            "Some hyperparameters affect performance much more strongly than others and deserve more careful search.\n"
            "\n"
            "> **Never tune hyperparameters on the test set.** Use validation performance for tuning and "
            "reserve the test split for the final estimate.\n"
            "\n"
            "### Hard AutoML: architecture search\n"
            "\n"
            "Neural architecture search treats architectural choices as variables to search over.\n"
            "\n"
            "A NAS system has three major parts:\n"
            "\n"
            "1. **search space** — possible building blocks and combinations,\n"
            "2. **performance estimation strategy** — estimate candidate quality without fully training every candidate,\n"
            "3. **search strategy** — explore candidate architectures.\n"
            "\n"
            "Search strategies can include random search, reinforcement learning, or evolutionary methods.\n"
            "\n"
            "### Learned optimizers\n"
            "\n"
            "The chapter also introduces the idea of replacing a hand-designed update rule with a learned model "
            "that decides how weights should be updated.\n"
            "\n"
            "These approaches can be extremely expensive to develop, but successful results may later be reusable "
            "across many tasks.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Four phases of model development\n"
            "\n"
            "The chapter gives a useful progression for ML adoption.\n"
            "\n"
            "### Phase 1: before machine learning\n"
            "\n"
            "Start with a heuristic or non-ML solution. It establishes a baseline and may even be good enough.\n"
            "\n"
            "Example: predict the next typed letter using the most common English letters.\n"
            "\n"
            "### Phase 2: simplest ML models\n"
            "\n"
            "Try models that are easy to inspect and deploy, such as logistic regression, nearest-neighbor methods, "
            "or gradient-boosted trees depending on the problem.\n"
            "\n"
            "The goal is to validate the end-to-end ML framework and problem framing.\n"
            "\n"
            "### Phase 3: optimize the simple models\n"
            "\n"
            "Improve with:\n"
            "\n"
            "- better objective functions,\n"
            "- hyperparameter search,\n"
            "- feature engineering,\n"
            "- more data,\n"
            "- ensembles.\n"
            "\n"
            "### Phase 4: complex models\n"
            "\n"
            "Only after simpler approaches hit their useful limit should you invest in substantially more complex models.\n"
            "\n"
            "You should also study how quickly models decay after deployment so infrastructure can support the required retraining cadence.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Offline evaluation needs context, not isolated numbers\n"
            "\n"
            "Once you have candidate models, you need to decide which one is suitable for production.\n"
            "\n"
            "A metric value by itself is often meaningless. An F1 score of 0.90 can sound impressive, but if a simple "
            "random or majority baseline gets a similar score, the model may add little value.\n"
            "\n"
            "Offline evaluation cannot perfectly predict production behavior because development environments often have "
            "labels and cleaner data that production does not.\n"
            "\n"
            "Still, good offline evaluation can eliminate weak or unsafe models before deployment.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Five useful baselines\n"
            "\n"
            "### Random baseline\n"
            "\n"
            "What happens if predictions are random?\n"
            "\n"
            "Random predictions can follow a uniform distribution or the observed label distribution.\n"
            "\n"
            "### Simple heuristic\n"
            "\n"
            "What performance can a hand-written rule achieve without ML?\n"
            "\n"
            "For a newsfeed, a simple heuristic might rank newest items first.\n"
            "\n"
            "### Zero-rule baseline\n"
            "\n"
            "Always predict the most common class or most common outcome.\n"
            "\n"
            "If recommending a user's most frequently used app already achieves 70% accuracy, a complex model should "
            "improve enough to justify its extra cost.\n"
            "\n"
            "### Human baseline\n"
            "\n"
            "If the ML system automates or assists human work, compare it with relevant human performance.\n"
            "\n"
            "### Existing solution\n"
            "\n"
            "Compare with the current business rules, third-party system, or incumbent model.\n"
            "\n"
            "A new ML model does not always need higher raw accuracy to be useful. It can still be preferable if it is "
            "cheaper, faster, or easier to operate.\n"
            "\n"
            "This motivates an important distinction:\n"
            "\n"
            "> **A good model is not automatically a useful system, and a technically imperfect model can still be useful.**\n"
            "\n"
            "{{exercise:M06.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Perturbation, invariance, and directional-expectation tests\n"
            "\n"
            "Average metrics are not enough. Production models should also behave sensibly when inputs change.\n"
            "\n"
            "### Perturbation tests\n"
            "\n"
            "Make small realistic changes to evaluation inputs and measure performance degradation.\n"
            "\n"
            "For an audio model, add background noise or slightly shift the recording. For images, change lighting or add "
            "small noise. For text, simulate typos or other plausible input variation.\n"
            "\n"
            "A model that is highly sensitive to tiny realistic changes may be difficult to maintain in production.\n"
            "\n"
            "### Invariance tests\n"
            "\n"
            "Some changes **should not change** the prediction.\n"
            "\n"
            "Examples include changing a name, gender marker, or another sensitive attribute when that attribute should "
            "not influence the decision.\n"
            "\n"
            "If the output changes when it should remain invariant, investigate bias or shortcut learning.\n"
            "\n"
            "### Directional-expectation tests\n"
            "\n"
            "Some changes **should predictably change** the output.\n"
            "\n"
            "For a housing-price model, holding everything else fixed while increasing lot size should not decrease the "
            "predicted value if domain expectations say the relationship should be monotonic.\n"
            "\n"
            "[[IMAGE_NEEDED: Three behavioral model tests | "
            "Three panels showing realistic perturbation with expected stability, a sensitive attribute swap with an "
            "unchanged expected prediction, and a meaningful feature increase with an expected directional output change "
            "| Learner should notice that evaluation can test behavior, not just aggregate accuracy]]\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Model calibration\n"
            "\n"
            "A probabilistic model is **calibrated** when predicted probabilities correspond to observed frequencies.\n"
            "\n"
            "If the model repeatedly predicts 70% probability for an event, that event should happen about 70% of the time.\n"
            "\n"
            "A model can rank items correctly while still being poorly calibrated.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Ad A predicted click probability: 10%\n"
            "Ad B predicted click probability:  8%\n"
            "```\n"
            "\n"
            "The ranking A > B might be correct even if the real click rates are 5% and 4%. But if you use these numbers "
            "to forecast total clicks or revenue, the miscalibration matters.\n"
            "\n"
            "### Calibration curve\n"
            "\n"
            "Group predictions by predicted probability and compare predicted probability with observed frequency.\n"
            "\n"
            "A perfectly calibrated model follows:\n"
            "\n"
            "```text\n"
            "predicted probability = observed frequency\n"
            "```\n"
            "\n"
            "The chapter mentions Platt scaling as one method for calibration.\n"
            "\n"
            "[[IMAGE_NEEDED: Calibration curve | "
            "A probability calibration plot with a diagonal perfect-calibration line and one model curve above/below it "
            "| Learner should notice that calibration measures whether probability values themselves are trustworthy, "
            "not merely whether ranking is correct]]\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Confidence is a per-prediction decision tool\n"
            "\n"
            "System-level metrics summarize average behavior. Confidence reasoning asks whether **this individual prediction** "
            "is trustworthy enough to act on.\n"
            "\n"
            "If a model is uncertain, possible responses include:\n"
            "\n"
            "- suppress the prediction,\n"
            "- ask the user for more information,\n"
            "- send the case to a human,\n"
            "- fall back to a safer rule-based method.\n"
            "\n"
            "This creates a practical design question:\n"
            "\n"
            "> What confidence threshold should trigger automated action?\n"
            "\n"
            "A useful system can intentionally abstain on uncertain examples instead of forcing a prediction every time.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Slice-based evaluation\n"
            "\n"
            "**Slicing** means evaluating model performance on meaningful subsets of the data.\n"
            "\n"
            "Suppose 90% of the data belongs to a majority group.\n"
            "\n"
            "| Model | Majority accuracy | Minority accuracy | Overall accuracy |\n"
            "|---|---:|---:|---:|\n"
            "| A | 98% | 80% | 96.2% |\n"
            "| B | 95% | 95% | 95% |\n"
            "\n"
            "Looking only at overall accuracy favors model A. Looking at slices reveals that model A performs much worse "
            "for the minority group.\n"
            "\n"
            "Sometimes equal performance across slices is not the goal either. Some slices are more important to the business. "
            "For churn prediction, paid users may deserve closer scrutiny than nonpaying users.\n"
            "\n"
            "### Simpson's paradox\n"
            "\n"
            "Aggregate trends can even reverse subgroup trends. The source gives an example where one model performs better "
            "inside each group, while another appears better after the groups are combined.\n"
            "\n"
            "The lesson is not that Simpson's paradox will always occur. It is that **aggregation can conceal important structure**.\n"
            "\n"
            "[[IMAGE_NEEDED: Aggregate metric versus slice metrics | "
            "A large overall accuracy bar beside separate majority/minority bars for two models, showing how the model with "
            "the best overall score can perform poorly on one subgroup | Learner should notice that aggregate metrics can hide "
            "critical weaknesses]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. How to discover critical slices\n"
            "\n"
            "The chapter describes three approaches.\n"
            "\n"
            "### Heuristics-based slicing\n"
            "\n"
            "Use domain knowledge. For web traffic, useful slices might include:\n"
            "\n"
            "- mobile versus desktop,\n"
            "- browser type,\n"
            "- geographic location.\n"
            "\n"
            "### Error analysis\n"
            "\n"
            "Manually inspect failures and search for recurring patterns.\n"
            "\n"
            "The source gives an example where poor mobile performance ultimately revealed a non-ML interface problem: "
            "a button was partially hidden on small screens.\n"
            "\n"
            "### Automated slice finding\n"
            "\n"
            "Research systems can generate candidate slices using search, clustering, or decision-based methods, then prune "
            "and rank the most interesting candidates.\n"
            "\n"
            "Whatever method you use, slice evaluation requires enough correctly labeled evaluation data for each slice. "
            "The quality of the analysis is bounded by the quality of the slice data.\n"
            "\n"
            "{{exercise:M06.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: State of the art means best for production\n"
            "\n"
            "Benchmark leadership says little about your latency, compute, cost, maintenance, or data constraints.\n"
            "\n"
            "### Misconception 2: The most complex model is the best starting point\n"
            "\n"
            "Starting simple gives you a deployable baseline and a far easier debugging path.\n"
            "\n"
            "### Misconception 3: An ensemble always improves performance\n"
            "\n"
            "Highly correlated base learners can make the same errors, eliminating the ensemble benefit.\n"
            "\n"
            "### Misconception 4: Tracking hyperparameters is enough for reproducibility\n"
            "\n"
            "You may also need code, data, environment, framework, hardware, random seed, and artifacts.\n"
            "\n"
            "### Misconception 5: A decreasing loss proves the ML system is correct\n"
            "\n"
            "ML systems can fail silently even while training appears normal.\n"
            "\n"
            "### Misconception 6: Hyperparameters should be tuned on the test set\n"
            "\n"
            "The validation split is for tuning. The test split should be reserved for the final evaluation.\n"
            "\n"
            "### Misconception 7: One high offline metric proves production readiness\n"
            "\n"
            "Models also need useful baselines, robustness checks, calibration where probabilities matter, and slice analysis.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Learning curve | Performance plotted against amount of training data. |\n"
            "| Base learner | Individual model inside an ensemble. |\n"
            "| Bagging | Train independent learners on bootstrap samples and aggregate predictions. |\n"
            "| Boosting | Train learners sequentially with greater focus on earlier mistakes. |\n"
            "| Stacking | Combine base-model outputs using a meta-learner. |\n"
            "| Experiment tracking | Recording metrics, states, artifacts, and progress of training runs. |\n"
            "| Versioning | Recording experiment definitions and dependencies for comparison or recreation. |\n"
            "| Artifact | File produced by an experiment, such as logs, curves, checkpoints, or outputs. |\n"
            "| Overfit a batch | Debugging test where a model is asked to nearly memorize a tiny training subset. |\n"
            "| Data parallelism | Replicate the model and split data across workers. |\n"
            "| Model parallelism | Split model components across workers. |\n"
            "| Pipeline parallelism | Use micro-batches to overlap computation across model stages. |\n"
            "| Straggler | Slow worker that delays synchronous distributed training. |\n"
            "| Gradient staleness | Gradient computed using older model parameters in asynchronous training. |\n"
            "| AutoML | Automation of model or hyperparameter search. |\n"
            "| NAS | Neural architecture search. |\n"
            "| Baseline | Reference solution used to interpret a model's metric. |\n"
            "| Perturbation test | Test model stability under small realistic input changes. |\n"
            "| Invariance test | Test that irrelevant or sensitive input changes do not change the output. |\n"
            "| Directional expectation | Test that an input change moves the prediction in an expected direction. |\n"
            "| Calibration | Agreement between predicted probabilities and observed event frequencies. |\n"
            "| Confidence threshold | Per-prediction threshold for deciding whether automated action is justified. |\n"
            "| Slice-based evaluation | Evaluating performance on meaningful subsets of data. |\n"
            "| Simpson's paradox | Aggregate trends differ from or reverse subgroup trends. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. Why is benchmark state-of-the-art performance not enough for model selection?\n"
            "2. What three benefits come from starting with a simple model?\n"
            "3. Why should architectures be compared with similar experimental effort?\n"
            "4. What can a learning curve tell you?\n"
            "5. How can model assumptions cause failure even when code is correct?\n"
            "6. Why does ensemble diversity matter?\n"
            "7. How do bagging, boosting, and stacking differ?\n"
            "8. What should an experiment tracker record beyond final accuracy?\n"
            "9. Why is data versioning harder than code versioning?\n"
            "10. Why is overfitting a tiny batch a useful debugging test?\n"
            "11. What is the straggler problem?\n"
            "12. What is gradient staleness?\n"
            "13. What is the difference between data and model parallelism?\n"
            "14. Why must hyperparameters be tuned on validation rather than test data?\n"
            "15. What are the three parts of a NAS setup?\n"
            "16. What are the four phases of model development described here?\n"
            "17. Why is an evaluation metric meaningless without context or a baseline?\n"
            "18. What is the difference between perturbation, invariance, and directional-expectation tests?\n"
            "19. What does it mean for a probability model to be calibrated?\n"
            "20. Why can abstention be better than forcing low-confidence predictions?\n"
            "21. How can an overall metric hide poor minority-slice performance?\n"
            "22. What are three ways to discover critical slices?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**Model development is not a contest to find the fanciest algorithm. A production candidate must be compared "
            "fairly, debugged and tracked reproducibly, evaluated against meaningful baselines, tested for sensible behavior, "
            "and inspected on the slices where failure actually matters.**\n"
        ),
        "estimated_minutes": 240,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "model-selection", "title": "Model selection is a systems decision", "order": 1},
            {"id": "six-tips", "title": "Six practical tips for selecting models", "order": 2},
            {"id": "ensembles", "title": "Ensembles: combine models instead of trusting one", "order": 3},
            {"id": "bagging-boosting-stacking", "title": "Bagging, boosting, and stacking", "order": 4},
            {"id": "tracking-versioning", "title": "Experiment tracking and versioning", "order": 5},
            {"id": "debugging", "title": "Debugging ML models", "order": 6},
            {"id": "distributed-training", "title": "Distributed training and memory constraints", "order": 7},
            {"id": "automl", "title": "AutoML: automate parts of model development", "order": 8},
            {"id": "four-phases", "title": "Four phases of model development", "order": 9},
            {"id": "offline-evaluation", "title": "Offline evaluation needs context, not isolated numbers", "order": 10},
            {"id": "baselines", "title": "Five useful baselines", "order": 11},
            {"id": "robustness-tests", "title": "Perturbation, invariance, and directional-expectation tests", "order": 12},
            {"id": "calibration", "title": "Model calibration", "order": 13},
            {"id": "confidence", "title": "Confidence is a per-prediction decision tool", "order": 14},
            {"id": "slice-evaluation", "title": "Slice-based evaluation", "order": 15},
            {"id": "finding-slices", "title": "How to discover critical slices", "order": 16},
        ],
    },

    "exercises": [
        {
            "id": "M06.L01.EX01",
            "title": "Choose the model for the system, not the leaderboard",
            "lesson_code": "M06.L01",
            "section_id": "six-tips",
            "placement": "after_section",
            "description": "Compare model candidates using production constraints and expected future growth.",
            "instructions": (
                "You need a toxic-comment classifier. Candidate A is logistic regression: F1 0.88, CPU inference "
                "under 5 ms, easy explanations, and small training cost. Candidate B is a transformer: F1 0.91, "
                "GPU inference around 70 ms, higher operating cost, and better performance as data grows.\n\n"
                "1. List at least four decision dimensions besides F1.\n"
                "2. Give one situation where A is the better production choice.\n"
                "3. Give one situation where B is the better production choice.\n"
                "4. Explain what a learning curve could tell the team.\n"
                "5. Propose a fair experiment for comparing the two architectures."
            ),
            "expected_output": "A trade-off analysis grounded in constraints rather than a metric-only winner.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["model-selection", "tradeoff-reasoning", "learning-curves"],
        },
        {
            "id": "M06.L01.EX02",
            "title": "Debug a model that refuses to learn",
            "lesson_code": "M06.L01",
            "section_id": "debugging",
            "placement": "after_section",
            "description": "Apply the chapter's debugging techniques to a failing training run.",
            "instructions": (
                "Your model trains without crashing, but validation performance is near random.\n\n"
                "Design a debugging sequence that includes:\n"
                "1. simplifying the model,\n"
                "2. overfitting a tiny batch,\n"
                "3. fixing a random seed,\n"
                "4. checking data/label alignment,\n"
                "5. checking hyperparameters and preprocessing.\n\n"
                "For each step, state what failure would tell you."
            ),
            "expected_output": "An ordered debugging procedure with a diagnostic purpose for every step.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["ml-debugging", "reproducibility", "diagnostic-reasoning"],
        },
        {
            "id": "M06.L01.EX03",
            "title": "Build meaningful evaluation baselines",
            "lesson_code": "M06.L01",
            "section_id": "baselines",
            "placement": "after_section",
            "description": "Practice interpreting a model score relative to alternative solutions.",
            "instructions": (
                "You are building a next-app recommender. A user's most frequently used app is the correct next app "
                "68% of the time. Your ML model reaches 70% accuracy.\n\n"
                "1. Name the relevant heuristic baseline.\n"
                "2. Explain why 70% accuracy alone is not impressive.\n"
                "3. Name two other baselines from the lesson you would consider.\n"
                "4. Give one operational reason the ML model could still be useful despite only a small accuracy gain.\n"
                "5. Give one operational reason it might not justify deployment."
            ),
            "expected_output": "A baseline-centered interpretation of whether the ML improvement is meaningful.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["baselines", "offline-evaluation", "production-value"],
        },
        {
            "id": "M06.L01.EX04",
            "title": "Design a production-minded offline evaluation suite",
            "lesson_code": "M06.L01",
            "section_id": "finding-slices",
            "placement": "after_section",
            "description": "Combine robustness, calibration, confidence, and slicing into one evaluation plan.",
            "instructions": (
                "You are evaluating a customer-support routing model before deployment.\n\n"
                "Design an offline evaluation plan containing:\n"
                "1. one random or heuristic baseline,\n"
                "2. one perturbation test,\n"
                "3. one invariance test,\n"
                "4. one directional-expectation test if applicable—or explain why none is appropriate,\n"
                "5. one calibration check if probabilities will be used operationally,\n"
                "6. a confidence-based fallback rule,\n"
                "7. at least four evaluation slices,\n"
                "8. one method for discovering unexpected bad slices."
            ),
            "expected_output": "A structured pre-deployment evaluation checklist tied to model behavior and risk.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["robustness-testing", "calibration", "confidence", "slice-evaluation"],
        },
    ],

    "quiz": {
        "id": "M06.L01.QZ01",
        "title": "Model Development and Offline Evaluation — Knowledge Check",
        "lesson_code": "M06.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M06.L01.Q01",
                "section_id": "model-selection",
                "question": "Which statement best reflects the chapter's model-selection philosophy?",
                "options": [
                    "Always use the architecture with the best published benchmark score.",
                    "Choose using predictive performance together with data, compute, latency, interpretability, and deployment constraints.",
                    "Classical ML should never be used if neural networks exist.",
                    "Inference latency is irrelevant before deployment.",
                ],
                "correct": 1,
                "explanation": "Production suitability is multidimensional rather than accuracy-only.",
            },
            {
                "id": "M06.L01.Q02",
                "section_id": "six-tips",
                "question": "Why is starting with a simple model valuable?",
                "options": [
                    "It guarantees the final best accuracy.",
                    "It is easier to deploy and debug and provides a baseline.",
                    "It eliminates the need for features.",
                    "It prevents all data drift.",
                ],
                "correct": 1,
                "explanation": "Simple models help validate the pipeline and provide a reference for later complexity.",
            },
            {
                "id": "M06.L01.Q03",
                "section_id": "six-tips",
                "question": "What does a learning curve plot?",
                "options": [
                    "Model performance against amount of training data.",
                    "Inference latency against GPU temperature.",
                    "Feature importance against number of classes.",
                    "Calibration against random seed.",
                ],
                "correct": 0,
                "explanation": "Learning curves help reason about whether more training data may improve performance.",
            },
            {
                "id": "M06.L01.Q04",
                "section_id": "ensembles",
                "question": "When is a simple voting ensemble least likely to improve over its members?",
                "options": [
                    "When base learners make diverse errors.",
                    "When all base learners make nearly identical errors.",
                    "When the task is classification.",
                    "When the models have different architectures.",
                ],
                "correct": 1,
                "explanation": "The ensemble benefit depends strongly on error diversity.",
            },
            {
                "id": "M06.L01.Q05",
                "section_id": "bagging-boosting-stacking",
                "question": "Which method trains later learners to focus more on mistakes made by earlier learners?",
                "options": ["Bagging", "Boosting", "Stacking", "Calibration"],
                "correct": 1,
                "explanation": "Boosting iteratively reweights or emphasizes difficult examples.",
            },
            {
                "id": "M06.L01.Q06",
                "section_id": "tracking-versioning",
                "question": "Why is data versioning usually harder than code versioning?",
                "options": [
                    "Data never changes.",
                    "Datasets can be very large and do not map naturally to line-by-line diffs and local copies.",
                    "Code cannot be versioned.",
                    "Data versions never affect model behavior.",
                ],
                "correct": 1,
                "explanation": "Large scale, storage cost, diff semantics, collaboration, and privacy complicate data versioning.",
            },
            {
                "id": "M06.L01.Q07",
                "section_id": "debugging",
                "question": "What is the purpose of trying to overfit a very small batch?",
                "options": [
                    "To estimate production traffic.",
                    "To verify the implementation can at least memorize a tiny training set.",
                    "To increase fairness.",
                    "To tune the test set.",
                ],
                "correct": 1,
                "explanation": "Failure to overfit a tiny batch is a strong sign that the implementation or training setup may be broken.",
            },
            {
                "id": "M06.L01.Q08",
                "section_id": "distributed-training",
                "question": "What is the straggler problem in synchronous data-parallel training?",
                "options": [
                    "A worker uses stale gradients.",
                    "A slow worker delays the update because all workers must synchronize.",
                    "The model cannot fit on one GPU.",
                    "A category hashes to the wrong index.",
                ],
                "correct": 1,
                "explanation": "Synchronous updates wait for all workers, so slow workers reduce overall throughput.",
            },
            {
                "id": "M06.L01.Q09",
                "section_id": "distributed-training",
                "question": "What distinguishes model parallelism from data parallelism?",
                "options": [
                    "Model parallelism splits model components; data parallelism replicates the model and splits data.",
                    "They are identical.",
                    "Data parallelism cannot use multiple workers.",
                    "Model parallelism only changes batch size.",
                ],
                "correct": 0,
                "explanation": "The object being divided differs: the model versus the data.",
            },
            {
                "id": "M06.L01.Q10",
                "section_id": "automl",
                "question": "Which split should guide hyperparameter tuning?",
                "options": ["Training only", "Validation", "Final test", "Production only"],
                "correct": 1,
                "explanation": "Validation is used for model and hyperparameter selection; test is reserved for final evaluation.",
            },
            {
                "id": "M06.L01.Q11",
                "section_id": "four-phases",
                "question": "What comes first in the chapter's four-phase development strategy?",
                "options": [
                    "Complex neural architectures",
                    "Ensembling dozens of models",
                    "A non-ML heuristic or simple existing approach",
                    "Neural architecture search",
                ],
                "correct": 2,
                "explanation": "A simple non-ML baseline establishes whether ML complexity is even needed.",
            },
            {
                "id": "M06.L01.Q12",
                "section_id": "baselines",
                "question": "What is the zero-rule baseline for classification?",
                "options": [
                    "Predict zero probability for every class.",
                    "Always predict the most common class.",
                    "Use a random neural network.",
                    "Use the human expert score.",
                ],
                "correct": 1,
                "explanation": "Zero rule is a very simple majority-class heuristic.",
            },
            {
                "id": "M06.L01.Q13",
                "section_id": "robustness-tests",
                "question": "Which test asks whether a small realistic input disturbance causes an unreasonable performance drop?",
                "options": ["Perturbation test", "Versioning test", "Bagging test", "Architecture search"],
                "correct": 0,
                "explanation": "Perturbation tests simulate realistic noise or small changes.",
            },
            {
                "id": "M06.L01.Q14",
                "section_id": "robustness-tests",
                "question": "Changing a person's name should not change a resume-screening result. What kind of check is this?",
                "options": ["Directional expectation", "Invariance test", "Boosting", "Calibration"],
                "correct": 1,
                "explanation": "The expected behavior is that the prediction remains invariant to the irrelevant change.",
            },
            {
                "id": "M06.L01.Q15",
                "section_id": "calibration",
                "question": "A model is well calibrated at 70% confidence when:",
                "options": [
                    "Every 70% prediction is correct.",
                    "Events predicted at about 70% probability occur about 70% of the time.",
                    "Its accuracy is exactly 70%.",
                    "Its threshold is fixed at 0.7.",
                ],
                "correct": 1,
                "explanation": "Calibration connects predicted probabilities to observed frequencies.",
            },
            {
                "id": "M06.L01.Q16",
                "section_id": "confidence",
                "question": "Why might a system abstain on low-confidence predictions?",
                "options": [
                    "To avoid ever making predictions.",
                    "To route uncertain cases to a safer fallback, more information, or human review.",
                    "Because confidence is the same as global accuracy.",
                    "To increase the training dataset automatically.",
                ],
                "correct": 1,
                "explanation": "Per-example uncertainty can guide whether automation is appropriate for that case.",
            },
            {
                "id": "M06.L01.Q17",
                "section_id": "slice-evaluation",
                "question": "Why can aggregate accuracy be misleading?",
                "options": [
                    "It always equals zero.",
                    "It can hide poor performance on minority or critical subgroups.",
                    "It cannot be computed for classification.",
                    "It already contains every slice metric.",
                ],
                "correct": 1,
                "explanation": "Large or easy groups can dominate the aggregate and conceal local failures.",
            },
            {
                "id": "M06.L01.Q18",
                "section_id": "finding-slices",
                "type": "open",
                "question": (
                    "A model has strong overall performance but customer complaints suggest it fails for a specific "
                    "kind of traffic. Describe how you would use heuristics-based slicing, error analysis, and one "
                    "automated slice-finding approach to investigate the problem."
                ),
            },
        ],
        "passing_score": 70,
    },
}
