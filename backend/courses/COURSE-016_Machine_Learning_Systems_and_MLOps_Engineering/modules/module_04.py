"""M04.L01 — Training Data.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 4, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"

MODULE_ORDER = 4

MODULE_TITLE = "Training Data for Machine Learning Systems"

MODULE_DESCRIPTION = (
    "Learn how to create useful training data through careful sampling, labeling, "
    "label-scarcity strategies, class-imbalance handling, and data augmentation."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Training Data",

    "slug": "ml-systems-design-m04-l01",

    "description": (
        "A practical guide to creating and improving training data for production "
        "machine learning systems, covering sampling, labels and feedback loops, "
        "weak and semi-supervision, transfer and active learning, class imbalance, "
        "evaluation metrics, resampling, cost-sensitive losses, and data augmentation."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "training-data",
        "sampling",
        "stratified-sampling",
        "weighted-sampling",
        "reservoir-sampling",
        "importance-sampling",
        "labeling",
        "data-lineage",
        "natural-labels",
        "feedback-loops",
        "weak-supervision",
        "semi-supervised-learning",
        "transfer-learning",
        "active-learning",
        "class-imbalance",
        "precision",
        "recall",
        "f1",
        "roc",
        "precision-recall",
        "resampling",
        "cost-sensitive-learning",
        "focal-loss",
        "data-augmentation",
    ],

    "prerequisite_ids": ["M03.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Training Data",

        "content": (
            "# Training Data\n"
            "\n"
            "> **Lesson:** M04.L01  \n"
            "> **Module:** Training Data for Machine Learning Systems  \n"
            "> **Source alignment:** Chapter 4. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why training data evolves throughout an ML project lifecycle.\n"
            "- Compare nonprobability, simple random, stratified, weighted, "
            "reservoir, and importance sampling.\n"
            "- Explain the risks of hand labeling and the problem of conflicting labels.\n"
            "- Explain data lineage and why it is useful for debugging training data.\n"
            "- Distinguish natural, behavioral, implicit, and explicit labels.\n"
            "- Explain feedback loop length and how it affects iteration speed.\n"
            "- Compare weak supervision, semi-supervision, transfer learning, and "
            "active learning as strategies for limited labels.\n"
            "- Explain why class imbalance can make accuracy misleading.\n"
            "- Compute and interpret precision, recall, and F1 at a conceptual level.\n"
            "- Explain ROC and precision-recall curves at a high level.\n"
            "- Compare oversampling, undersampling, SMOTE, and algorithm-level "
            "class-imbalance methods.\n"
            "- Explain cost-sensitive learning, class-balanced loss, and focal loss.\n"
            "- Describe label-preserving augmentation, perturbation, and data synthesis.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Training data is part of the system, not a one-time file\n"
            "\n"
            "Many ML courses spend most of their time on models. In production, "
            "however, poor data can ruin even a strong modeling approach.\n"
            "\n"
            "This chapter uses **training data** broadly to mean the data used "
            "during model development, including training, validation, and test "
            "splits.\n"
            "\n"
            "The wording matters. A fixed \"dataset\" sounds finite and stationary, "
            "but production data is usually neither. New examples arrive, behavior "
            "changes, labels change, and model requirements evolve.\n"
            "\n"
            "So creating training data is an **iterative process**:\n"
            "\n"
            "```text\n"
            "Collect / sample\n"
            "      ↓\n"
            "Label\n"
            "      ↓\n"
            "Train / evaluate\n"
            "      ↓\n"
            "Discover data problems\n"
            "      ↓\n"
            "Resample / relabel / augment / collect more\n"
            "      ↺\n"
            "```\n"
            "\n"
            "The chapter also gives an important warning: data can contain biases "
            "from collection, sampling, labeling, or historical human decisions. "
            "A model trained on biased data can reproduce those biases.\n"
            "\n"
            "[[IMAGE_NEEDED: Iterative training-data lifecycle | "
            "A cycle showing sampling, labeling, training, evaluation, discovering "
            "data issues, and updating the data before looping back | Learner should "
            "notice that training-data creation continues as the model and environment evolve]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Why sampling matters\n"
            "\n"
            "Sampling appears throughout ML:\n"
            "\n"
            "- selecting a subset of real-world data for training,\n"
            "- splitting data into train/validation/test sets,\n"
            "- selecting events for monitoring,\n"
            "- running a cheap experiment on a small subset before scaling up.\n"
            "\n"
            "Sampling is necessary when you cannot access all possible real-world "
            "data or cannot afford to process everything you have.\n"
            "\n"
            "A sampling method affects what the model gets to see. If the sample "
            "does not represent important parts of reality, the model may fail "
            "even if its training procedure is correct.\n"
            "\n"
            "The chapter groups sampling methods into two broad families:\n"
            "\n"
            "1. **Nonprobability sampling** — selection is not based on probability.\n"
            "2. **Random/probability-based sampling** — selection uses probabilistic rules.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Nonprobability sampling and selection bias\n"
            "\n"
            "Nonprobability sampling selects examples without a probability-based "
            "mechanism.\n"
            "\n"
            "### Convenience sampling\n"
            "\n"
            "Use whatever data is easiest to obtain.\n"
            "\n"
            "This is common because it is fast and cheap, but convenience does not "
            "guarantee representativeness.\n"
            "\n"
            "### Snowball sampling\n"
            "\n"
            "Start with some examples and use them to discover more examples.\n"
            "\n"
            "Example: begin with a few social-media accounts, collect the accounts "
            "they follow, then continue outward.\n"
            "\n"
            "### Judgment sampling\n"
            "\n"
            "Experts decide which examples should be included.\n"
            "\n"
            "### Quota sampling\n"
            "\n"
            "Choose fixed numbers from selected groups without randomizing within "
            "those groups.\n"
            "\n"
            "Example: collect exactly 100 responses from each age group even if "
            "those groups are not equally common in the real population.\n"
            "\n"
            "### Why this is risky\n"
            "\n"
            "These methods can produce **selection bias** because the sample is not "
            "guaranteed to reflect the real-world population.\n"
            "\n"
            "The chapter gives several examples:\n"
            "\n"
            "- language models trained on easily available web sources rather than "
            "all possible language,\n"
            "- sentiment datasets built from online reviews, which represent people "
            "willing and able to leave reviews,\n"
            "- early self-driving datasets collected heavily in sunny locations, "
            "leaving rain and snow less represented.\n"
            "\n"
            "Nonprobability sampling can still be useful for getting an early "
            "project started, but it should not be mistaken for an unbiased sample.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Simple random, stratified, and weighted sampling\n"
            "\n"
            "### Simple random sampling\n"
            "\n"
            "Every example receives the same probability of being selected.\n"
            "\n"
            "Example: randomly sample 10% of the population, so every member has "
            "a 10% chance of inclusion.\n"
            "\n"
            "The advantage is simplicity. The disadvantage is that **rare classes "
            "can disappear from the sample**.\n"
            "\n"
            "Suppose a rare class represents only 0.01% of the population and you "
            "take a small random subset. You may sample none of that class at all.\n"
            "\n"
            "### Stratified sampling\n"
            "\n"
            "First divide the population into groups, called **strata**, then sample "
            "from each group separately.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Class A → sample 1%\n"
            "Class B → sample 1%\n"
            "```\n"
            "\n"
            "This guarantees that both classes can appear even when one is rare.\n"
            "\n"
            "The challenge is that clean strata may not exist, especially in "
            "multilabel tasks where one example can belong to several groups.\n"
            "\n"
            "### Weighted sampling\n"
            "\n"
            "Each example gets a weight controlling how likely it is to be selected.\n"
            "\n"
            "This is useful when domain knowledge says that some examples are more "
            "valuable—for example, more recent data—or when your collected data has "
            "a different distribution from the real world.\n"
            "\n"
            "Python example adapted from the chapter:\n"
            "\n"
            "```python\n"
            "import random\n"
            "\n"
            "samples = random.choices(\n"
            "    population=[1, 2, 3, 4, 100, 1000],\n"
            "    weights=[0.2, 0.2, 0.2, 0.2, 0.1, 0.1],\n"
            "    k=2,\n"
            ")\n"
            "print(samples)\n"
            "```\n"
            "\n"
            "Do not confuse **weighted sampling** with **sample weights**:\n"
            "\n"
            "- weighted sampling changes which examples are selected,\n"
            "- sample weights change how strongly selected examples influence the loss.\n"
            "\n"
            "[[IMAGE_NEEDED: Sampling strategies comparison | "
            "One imbalanced population shown with three selection outcomes: simple "
            "random sampling, stratified sampling preserving each class, and weighted "
            "sampling favoring selected examples | Learner should notice that the "
            "selection mechanism changes what information reaches training]]\n"
            "\n"
            "{{exercise:M04.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Reservoir sampling and importance sampling\n"
            "\n"
            "### Reservoir sampling\n"
            "\n"
            "Reservoir sampling is useful for a stream whose total size is unknown "
            "and too large to keep in memory.\n"
            "\n"
            "Suppose tweets arrive continuously and you want to maintain a uniform "
            "sample of `k` tweets.\n"
            "\n"
            "The algorithm described in the chapter is:\n"
            "\n"
            "1. Put the first `k` elements into a reservoir.\n"
            "2. For the `n`th incoming item, draw a random integer `i` from 1 to `n`.\n"
            "3. If `i <= k`, replace the `i`th reservoir element with the new item.\n"
            "4. Otherwise, keep the reservoir unchanged.\n"
            "\n"
            "The important property is that every observed item has an equal chance "
            "of being represented in the reservoir, and the algorithm can be stopped "
            "at any time.\n"
            "\n"
            "[[IMAGE_NEEDED: Reservoir sampling over a stream | "
            "A stream of numbered items entering a fixed-size reservoir, with later "
            "items sometimes replacing earlier items | Learner should notice that "
            "memory stays bounded while all observed items retain equal sampling chance]]\n"
            "\n"
            "### Importance sampling\n"
            "\n"
            "Importance sampling is useful when the distribution you want to sample "
            "from is difficult or expensive, but another distribution is easier.\n"
            "\n"
            "If the target distribution is `P(x)` and the easier proposal distribution "
            "is `Q(x)`, you sample from `Q(x)` and reweight the sample to account for "
            "the difference between `P` and `Q`.\n"
            "\n"
            "The proposal must give nonzero probability wherever the target "
            "distribution can produce data.\n"
            "\n"
            "The chapter gives reinforcement learning as an example, where outcomes "
            "from an older policy can be reweighted when estimating behavior under "
            "a newer, sufficiently related policy.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Labels: why hand labeling is difficult\n"
            "\n"
            "Most production ML systems discussed in the chapter are supervised, "
            "which means they require labels.\n"
            "\n"
            "Hand labeling creates several major challenges.\n"
            "\n"
            "### Cost\n"
            "\n"
            "Some labels can be created by general annotators. Others require scarce "
            "domain experts. Labeling medical images, for example, may require "
            "qualified specialists rather than generic crowdsourcing workers.\n"
            "\n"
            "### Privacy\n"
            "\n"
            "Human labeling means people must inspect data. Sensitive records may "
            "not be allowed to leave an organization and may require controlled "
            "on-premises annotation.\n"
            "\n"
            "### Speed\n"
            "\n"
            "High-quality labeling can be extremely slow. Slow labeling means slow "
            "model iteration, which reduces adaptability when requirements or data change.\n"
            "\n"
            "Imagine a sentiment system changing from two classes—POSITIVE and "
            "NEGATIVE—to three classes by adding ANGRY. Old examples may need "
            "relabeling, and new ANGRY examples may need to be collected.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Label multiplicity and data lineage\n"
            "\n"
            "Different annotators frequently disagree.\n"
            "\n"
            "This creates **label multiplicity** or label ambiguity: one example "
            "may receive several conflicting labels.\n"
            "\n"
            "The problem gets worse when tasks require more expertise or when the "
            "labeling rules are vague.\n"
            "\n"
            "### Improve the labeling definition first\n"
            "\n"
            "Before blaming annotators, define the task clearly. The chapter's "
            "entity-recognition example shows that rules such as \"choose the "
            "longest matching entity span\" can remove some disagreements.\n"
            "\n"
            "The rules must then be incorporated into annotator training.\n"
            "\n"
            "### Data lineage\n"
            "\n"
            "**Data lineage** means tracking where every example and label came from.\n"
            "\n"
            "Why is this important?\n"
            "\n"
            "Suppose a model trained on 100,000 examples works reasonably well. You "
            "then buy one million newly labeled examples and performance gets worse. "
            "If you kept lineage, you can check whether errors concentrate in the "
            "newly acquired data and investigate that labeling process.\n"
            "\n"
            "Without lineage, low-quality data can be mixed permanently into the "
            "training pool, making failures difficult to explain.\n"
            "\n"
            "[[IMAGE_NEEDED: Data lineage for labeled examples | "
            "A training-data table with provenance fields pointing to source, "
            "collection date, annotator or labeling process, and label version | "
            "Learner should notice how provenance enables debugging when a subset "
            "of data causes model degradation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Natural labels, behavioral labels, and feedback loops\n"
            "\n"
            "Not every task needs human annotation.\n"
            "\n"
            "A task has **natural labels** when the system can later observe the "
            "real outcome and use it to evaluate the prediction.\n"
            "\n"
            "Examples from the chapter include:\n"
            "\n"
            "- predicted travel time versus actual travel time,\n"
            "- predicted stock price versus observed future price,\n"
            "- recommendations versus later clicks.\n"
            "\n"
            "Labels inferred from user behavior are also called **behavioral labels**.\n"
            "\n"
            "### Implicit versus explicit labels\n"
            "\n"
            "An **explicit label** comes from direct feedback, such as a rating or "
            "downvote.\n"
            "\n"
            "An **implicit label** is inferred. If a recommendation receives no "
            "click within a chosen time window, a system might treat it as NEGATIVE.\n"
            "\n"
            "That inference can be wrong: the user may click later.\n"
            "\n"
            "### Feedback loop length\n"
            "\n"
            "**Feedback loop length** is the time from serving a prediction until "
            "its natural label becomes available.\n"
            "\n"
            "Short-loop examples:\n"
            "\n"
            "- product recommendation clicks,\n"
            "- people-to-follow recommendations.\n"
            "\n"
            "Long-loop examples:\n"
            "\n"
            "- clothing recommendations that require delivery and trying the item,\n"
            "- fraud labels that may depend on disputes filed weeks or months later.\n"
            "\n"
            "A shorter feedback loop helps teams detect problems faster. A longer "
            "loop may provide a stronger or more reliable signal but slows adaptation.\n"
            "\n"
            "### Feedback signals differ in strength\n"
            "\n"
            "In ecommerce, signals might include:\n"
            "\n"
            "```text\n"
            "click → add to cart → purchase → rating/review → return\n"
            "```\n"
            "\n"
            "Clicks are plentiful and fast but weaker. Purchases are rarer and "
            "slower but usually provide a stronger signal of preference and business value.\n"
            "\n"
            "Choosing the feedback target is therefore a product and ML decision, "
            "not merely a modeling choice.\n"
            "\n"
            "[[IMAGE_NEEDED: Feedback loop signal strength versus delay | "
            "A user journey from impression to click, cart, purchase, review, and "
            "return, annotated with increasing feedback delay and changing signal "
            "strength | Learner should notice the trade-off between fast abundant "
            "feedback and slower stronger feedback]]\n"
            "\n"
            "{{exercise:M04.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Four strategies when labels are scarce\n"
            "\n"
            "The chapter presents four major approaches:\n"
            "\n"
            "| Method | Main idea | Initial ground truth labels? |\n"
            "|---|---|---|\n"
            "| Weak supervision | Use noisy heuristics to create labels | Not strictly, though a small labeled set is recommended |\n"
            "| Semi-supervision | Use structure and a small labeled seed set to infer more labels | Yes |\n"
            "| Transfer learning | Reuse a model trained on another task | Not always; fine-tuning usually uses some labels |\n"
            "| Active learning | Spend annotation effort on examples most useful to the model | Yes |\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Weak supervision and programmatic labeling\n"
            "\n"
            "Weak supervision uses **heuristics** to generate noisy labels.\n"
            "\n"
            "The chapter discusses **labeling functions (LFs)**: functions that "
            "encode expert rules.\n"
            "\n"
            "Example:\n"
            "\n"
            "```python\n"
            "def labeling_function(note):\n"
            '    if "pneumonia" in note:\n'
            '        return "EMERGENT"\n'
            "```\n"
            "\n"
            "Labeling functions can use:\n"
            "\n"
            "- keywords,\n"
            "- regular expressions,\n"
            "- database lookups,\n"
            "- outputs of existing models.\n"
            "\n"
            "Because heuristics are imperfect, several LFs may conflict or have "
            "different accuracies. Their outputs need to be combined, denoised, "
            "and reweighted to create useful probabilistic labels.\n"
            "\n"
            "A small hand-labeled set is valuable for judging and improving the LFs.\n"
            "\n"
            "### Why programmatic labeling is attractive\n"
            "\n"
            "- Expert knowledge can be versioned.\n"
            "- Rules can be shared and reused.\n"
            "- The same rules can be reapplied when data changes.\n"
            "- Privacy exposure can be reduced because experts may only need a "
            "cleared subset to develop rules.\n"
            "- Scaling rules to many examples can be faster than labeling each "
            "example manually.\n"
            "\n"
            "Weak supervision does not guarantee useful labels. If the heuristics "
            "are too noisy, performance may still be poor. But it can provide a "
            "low-cost starting point.\n"
            "\n"
            "[[IMAGE_NEEDED: Weak supervision with labeling functions | "
            "Several labeling functions applying noisy votes to unlabeled examples, "
            "followed by a combination/denoising stage that produces probabilistic "
            "training labels | Learner should notice that programmatic labels can "
            "conflict and must be combined rather than blindly trusted]]\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Semi-supervision, transfer learning, and active learning\n"
            "\n"
            "### Semi-supervision\n"
            "\n"
            "Semi-supervised learning starts with a small labeled set and a larger "
            "unlabeled set.\n"
            "\n"
            "One classic approach is **self-training**:\n"
            "\n"
            "1. Train on the labeled examples.\n"
            "2. Predict labels for unlabeled examples.\n"
            "3. Keep high-confidence predicted labels.\n"
            "4. Add them to training data.\n"
            "5. Train again.\n"
            "\n"
            "Another idea assumes that similar examples should have similar labels. "
            "Similarity can come from co-occurrence, clustering, or nearest-neighbor "
            "relationships.\n"
            "\n"
            "A third family uses **perturbation consistency**: a small change to an "
            "example should not change its label.\n"
            "\n"
            "### Transfer learning\n"
            "\n"
            "Transfer learning reuses a model learned for a base task as a starting "
            "point for a downstream task.\n"
            "\n"
            "A pretrained language model, for example, can later be adapted for "
            "sentiment analysis, intent detection, or question answering.\n"
            "\n"
            "Adaptation may be:\n"
            "\n"
            "- zero-shot use,\n"
            "- prompting with an appropriate input format,\n"
            "- fine-tuning on a smaller task-specific labeled set.\n"
            "\n"
            "Transfer learning is valuable because it reduces the need to train "
            "every task from scratch and can lower labeling requirements.\n"
            "\n"
            "### Active learning\n"
            "\n"
            "Active learning asks:\n"
            "\n"
            "> If humans can label only a limited number of examples, which examples "
            "should they label?\n"
            "\n"
            "A straightforward strategy is **uncertainty sampling**: choose examples "
            "the current model is least certain about.\n"
            "\n"
            "Another strategy is **query-by-committee**. Several candidate models "
            "vote, and examples with the strongest disagreement are sent for labeling.\n"
            "\n"
            "The goal is to gain more useful information per annotation instead of "
            "spending labels randomly.\n"
            "\n"
            "[[IMAGE_NEEDED: Active learning loop | "
            "An unlabeled pool or data stream feeding a model, the model selecting "
            "high-uncertainty examples for human annotation, and the new labels "
            "returning to training | Learner should notice that the model helps "
            "decide where scarce labeling effort should be spent]]\n"
            "\n"
            "{{exercise:M04.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Why class imbalance is difficult\n"
            "\n"
            "**Class imbalance** means that some labels occur much more often than others.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "NORMAL lung scans: 99.99%\n"
            "CANCER scans:      0.01%\n"
            "```\n"
            "\n"
            "This is common in real-world ML because important events are often rare:\n"
            "\n"
            "- fraud,\n"
            "- disease,\n"
            "- churn,\n"
            "- successful job candidates,\n"
            "- positive object-detection boxes.\n"
            "\n"
            "The chapter highlights three major problems.\n"
            "\n"
            "### 1. Too little signal from the minority class\n"
            "\n"
            "The model may see too few rare examples to learn a useful pattern.\n"
            "\n"
            "### 2. Easy majority-class shortcuts\n"
            "\n"
            "A model can obtain extremely high accuracy by always predicting the "
            "majority class.\n"
            "\n"
            "If 99.99% of examples are NORMAL, always predicting NORMAL gives "
            "99.99% accuracy while detecting zero cancer cases.\n"
            "\n"
            "### 3. Error costs are asymmetric\n"
            "\n"
            "Missing a rare cancer case can be much more costly than incorrectly "
            "flagging a normal scan.\n"
            "\n"
            "The imbalance itself may be inherent in reality, but it can also come "
            "from biased sampling or labeling errors. Before applying a technical "
            "fix, investigate why the imbalance exists.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Evaluate imbalanced problems with the right metrics\n"
            "\n"
            "Overall accuracy can hide failure on the class you care about.\n"
            "\n"
            "The chapter compares two cancer classifiers with the same 90% accuracy:\n"
            "\n"
            "- one detects only 10 out of 100 cancer cases,\n"
            "- the other detects 90 out of 100.\n"
            "\n"
            "The second model is clearly more useful for detecting cancer, even "
            "though overall accuracy is identical.\n"
            "\n"
            "### Confusion-matrix terms\n"
            "\n"
            "| Actual / prediction | Meaning |\n"
            "|---|---|\n"
            "| True Positive (TP) | Positive example correctly predicted positive |\n"
            "| False Positive (FP) | Negative example incorrectly predicted positive |\n"
            "| False Negative (FN) | Positive example incorrectly predicted negative |\n"
            "| True Negative (TN) | Negative example correctly predicted negative |\n"
            "\n"
            "### Precision\n"
            "\n"
            "```text\n"
            "Precision = TP / (TP + FP)\n"
            "```\n"
            "\n"
            "Of the examples predicted positive, how many were actually positive?\n"
            "\n"
            "### Recall\n"
            "\n"
            "```text\n"
            "Recall = TP / (TP + FN)\n"
            "```\n"
            "\n"
            "Of the actual positive examples, how many did the model find?\n"
            "\n"
            "### F1\n"
            "\n"
            "```text\n"
            "F1 = 2 × Precision × Recall / (Precision + Recall)\n"
            "```\n"
            "\n"
            "F1 balances precision and recall through their harmonic mean.\n"
            "\n"
            "Precision, recall, and F1 depend on which class is treated as positive.\n"
            "\n"
            "### Thresholds and ROC\n"
            "\n"
            "Many classifiers output a score or probability. Changing the threshold "
            "changes the trade-off between true positives and false positives.\n"
            "\n"
            "The **ROC curve** plots true-positive rate against false-positive rate "
            "across thresholds. **AUC** summarizes the area under that curve.\n"
            "\n"
            "### Precision-recall curve\n"
            "\n"
            "The chapter notes that for heavily imbalanced tasks, plotting precision "
            "against recall can provide a more informative view of performance than "
            "ROC alone.\n"
            "\n"
            "[[IMAGE_NEEDED: Accuracy can hide minority-class failure | "
            "Two confusion matrices with equal overall accuracy but dramatically "
            "different cancer recall, followed by a small precision-recall concept "
            "diagram | Learner should notice why class-specific metrics matter in "
            "imbalanced problems]]\n"
            "\n"
            "{{exercise:M04.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Data-level methods: resampling\n"
            "\n"
            "Data-level methods change the training distribution.\n"
            "\n"
            "### Undersampling\n"
            "\n"
            "Remove examples from the majority class.\n"
            "\n"
            "Benefit: makes the training distribution less dominated by the majority.\n"
            "\n"
            "Risk: throws away potentially useful information.\n"
            "\n"
            "### Oversampling\n"
            "\n"
            "Add more minority examples, often by duplicating or synthesizing them.\n"
            "\n"
            "Benefit: increases minority exposure.\n"
            "\n"
            "Risk: repeated copies can cause overfitting.\n"
            "\n"
            "### Tomek links\n"
            "\n"
            "For low-dimensional data, Tomek links identify close pairs from "
            "opposite classes and remove the majority-class member. This can make "
            "the decision boundary cleaner, though it can also remove useful boundary detail.\n"
            "\n"
            "### SMOTE\n"
            "\n"
            "SMOTE creates synthetic minority examples by combining nearby minority "
            "points in feature space.\n"
            "\n"
            "The chapter cautions that techniques such as SMOTE and Tomek links "
            "have mainly been shown effective for low-dimensional settings, while "
            "distance-based resampling can become difficult in high-dimensional spaces.\n"
            "\n"
            "### Critical evaluation rule\n"
            "\n"
            "> **Never evaluate on the resampled training distribution.**\n"
            "\n"
            "Evaluation should reflect the intended real-world distribution rather "
            "than the artificial distribution used to make training easier.\n"
            "\n"
            "The chapter also discusses two-phase learning and dynamic sampling as "
            "ways to balance learning without relying only on one fixed resampled set.\n"
            "\n"
            "[[IMAGE_NEEDED: Oversampling versus undersampling | "
            "An imbalanced two-class scatterplot shown before and after undersampling "
            "the majority class and oversampling the minority class | Learner should "
            "notice that resampling changes the training distribution, not reality]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Algorithm-level methods for class imbalance\n"
            "\n"
            "Instead of changing the data distribution, algorithm-level methods "
            "change how the learning algorithm values mistakes.\n"
            "\n"
            "### Cost-sensitive learning\n"
            "\n"
            "Different mistakes can receive different costs.\n"
            "\n"
            "If predicting NEGATIVE for a truly POSITIVE case is twice as costly "
            "as the opposite error, the loss can reflect that difference.\n"
            "\n"
            "A challenge is that the cost matrix must be specified for the problem.\n"
            "\n"
            "### Class-balanced loss\n"
            "\n"
            "One approach gives rare classes larger loss weights, for example by "
            "making class weight inversely related to class frequency.\n"
            "\n"
            "This encourages the model to pay more attention to underrepresented classes.\n"
            "\n"
            "### Focal loss\n"
            "\n"
            "Focal loss gives less emphasis to examples the model already classifies "
            "easily and more emphasis to hard examples.\n"
            "\n"
            "The intuition is:\n"
            "\n"
            "> Don't spend most of the learning signal on examples the model has "
            "already mastered; focus more on difficult ones.\n"
            "\n"
            "[[IMAGE_NEEDED: Class-imbalance intervention layers | "
            "A three-layer diagram showing metric choice, data-level resampling, "
            "and algorithm-level loss weighting as different intervention points | "
            "Learner should notice that imbalance can be addressed at evaluation, "
            "data, and learning-algorithm levels]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Data augmentation\n"
            "\n"
            "Data augmentation increases or diversifies training data. The chapter "
            "groups augmentation into three broad categories.\n"
            "\n"
            "### 1. Simple label-preserving transformations\n"
            "\n"
            "For images, examples include:\n"
            "\n"
            "- crop,\n"
            "- flip,\n"
            "- rotate,\n"
            "- erase part of the image,\n"
            "- invert orientation where appropriate.\n"
            "\n"
            "The key assumption is that the transformation should not change the label.\n"
            "\n"
            "For text, the chapter gives examples such as replacing a word with a "
            "similar word while trying to preserve meaning and sentiment.\n"
            "\n"
            "### 2. Perturbation\n"
            "\n"
            "Neural networks can be sensitive to small changes. Adversarial attacks "
            "intentionally exploit this weakness by modifying an input enough to "
            "cause a wrong prediction while keeping the input perceptually similar.\n"
            "\n"
            "Adding carefully chosen noisy examples to training can expose weak "
            "parts of the decision boundary and improve robustness. The chapter "
            "calls this **adversarial augmentation**.\n"
            "\n"
            "Perturbation also appears in NLP, though random character or word "
            "changes can more easily destroy meaning than small pixel changes in images.\n"
            "\n"
            "### 3. Data synthesis\n"
            "\n"
            "Synthetic data can bootstrap a task when real collection is expensive "
            "or limited.\n"
            "\n"
            "For conversational systems, templates can generate many queries:\n"
            "\n"
            "```text\n"
            "Find me a [CUISINE] restaurant within [NUMBER] miles of [LOCATION].\n"
            "```\n"
            "\n"
            "Filling slots with many values creates large numbers of examples.\n"
            "\n"
            "### Mixup\n"
            "\n"
            "The chapter also introduces **mixup**, where two examples and their "
            "labels are combined to create an intermediate synthetic training example.\n"
            "\n"
            "The goal is not merely to make the dataset larger. Augmentation can "
            "also improve generalization and robustness.\n"
            "\n"
            "[[IMAGE_NEEDED: Three families of data augmentation | "
            "Three panels showing label-preserving transformation, noisy/perturbed "
            "input, and synthesized/mixed examples | Learner should notice that "
            "augmentation can create diversity by transformation, perturbation, "
            "or generating new examples]]\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Random sampling always represents rare classes well\n"
            "\n"
            "Rare classes can disappear from small random samples. Stratified or "
            "weighted strategies may be needed when those slices are important.\n"
            "\n"
            "### Misconception 2: More labels automatically mean a better model\n"
            "\n"
            "A large amount of low-quality or inconsistent labeling can reduce "
            "performance. Label quality and lineage matter.\n"
            "\n"
            "### Misconception 3: Natural labels are immediately available\n"
            "\n"
            "Some natural labels arrive within seconds; others arrive weeks or "
            "months later. Feedback loop length strongly affects iteration speed.\n"
            "\n"
            "### Misconception 4: Weak supervision means perfectly reliable rules\n"
            "\n"
            "Weak supervision assumes heuristics are noisy. The method must combine "
            "and reason about conflicting labeling functions.\n"
            "\n"
            "### Misconception 5: High accuracy proves success on an imbalanced task\n"
            "\n"
            "A model can obtain excellent accuracy by predicting the majority class "
            "while completely failing on the rare class.\n"
            "\n"
            "### Misconception 6: Resampled data should also be used for evaluation\n"
            "\n"
            "Evaluation on the resampled distribution can give misleading results. "
            "The evaluation distribution should reflect the intended real setting.\n"
            "\n"
            "### Misconception 7: Augmentation is only for tiny datasets\n"
            "\n"
            "The chapter notes that augmentation can improve robustness and "
            "generalization even when substantial training data already exists.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Sampling | Selecting a subset of data for training, evaluation, monitoring, or experimentation. |\n"
            "| Convenience sampling | Selecting examples because they are easy to obtain. |\n"
            "| Stratified sampling | Sampling separately within predefined groups or strata. |\n"
            "| Weighted sampling | Assigning different selection probabilities to examples. |\n"
            "| Reservoir sampling | Maintaining a uniform fixed-size sample from a stream of unknown total length. |\n"
            "| Importance sampling | Sampling from an easier proposal distribution and reweighting toward a target distribution. |\n"
            "| Label multiplicity | Multiple conflicting labels for the same example. |\n"
            "| Data lineage | Tracking the origin and labeling history of data examples. |\n"
            "| Natural label | Ground truth that becomes observable from the system or later real-world outcome. |\n"
            "| Behavioral label | Label inferred from user behavior such as a click or purchase. |\n"
            "| Implicit label | Label inferred from behavior or absence of behavior rather than explicitly provided. |\n"
            "| Feedback loop length | Time between serving a prediction and receiving its label or feedback. |\n"
            "| Weak supervision | Using noisy heuristics or labeling functions to generate labels. |\n"
            "| Semi-supervision | Using a small labeled set plus unlabeled data and structural assumptions. |\n"
            "| Transfer learning | Reusing a model learned for one task as the starting point for another. |\n"
            "| Active learning | Selecting the most useful examples for annotation. |\n"
            "| Class imbalance | Large differences in the number or importance of examples across classes. |\n"
            "| Precision | Fraction of predicted positives that are actually positive. |\n"
            "| Recall | Fraction of actual positives that the model correctly identifies. |\n"
            "| F1 | Harmonic mean of precision and recall. |\n"
            "| ROC curve | True-positive rate versus false-positive rate across thresholds. |\n"
            "| Precision-recall curve | Precision versus recall across thresholds. |\n"
            "| Oversampling | Increasing minority-class representation in training data. |\n"
            "| Undersampling | Reducing majority-class representation in training data. |\n"
            "| SMOTE | Synthesizing minority examples from nearby minority points. |\n"
            "| Cost-sensitive learning | Giving different prediction errors different costs. |\n"
            "| Class-balanced loss | Weighting classes so rare classes have greater influence. |\n"
            "| Focal loss | Reducing emphasis on easy examples and focusing learning on difficult examples. |\n"
            "| Data augmentation | Creating additional or altered training examples while preserving useful learning signal. |\n"
            "| Adversarial augmentation | Training with deliberately perturbed examples to improve robustness. |\n"
            "| Mixup | Creating synthetic examples by combining existing examples and their labels. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why does the chapter prefer the term training data over training dataset?\n"
            "2. What is the main danger of convenience sampling?\n"
            "3. Why can simple random sampling miss rare classes?\n"
            "4. How does stratified sampling address that problem?\n"
            "5. What is the difference between weighted sampling and sample weights?\n"
            "6. Why is reservoir sampling useful for production streams?\n"
            "7. What is label multiplicity?\n"
            "8. How can data lineage help debug a model?\n"
            "9. What is the difference between implicit and explicit labels?\n"
            "10. Why does feedback loop length affect model adaptability?\n"
            "11. How is weak supervision different from semi-supervision?\n"
            "12. Why can transfer learning reduce labeling requirements?\n"
            "13. What does active learning try to optimize?\n"
            "14. Why is accuracy often misleading under strong class imbalance?\n"
            "15. What do precision and recall measure?\n"
            "16. Why must resampled data not be used as the evaluation distribution?\n"
            "17. How do cost-sensitive learning and focal loss differ conceptually?\n"
            "18. Name the three augmentation families discussed in this lesson.\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A production model can only learn from the evidence you give it. "
            "Good ML therefore depends on deliberately sampling, labeling, tracing, "
            "balancing, and augmenting training data so that the evidence reflects "
            "the problem you actually need the model to solve.**\n"
        ),

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "training-data-foundation", "title": "Training data is part of the system, not a one-time file", "order": 1},
            {"id": "sampling-overview", "title": "Why sampling matters", "order": 2},
            {"id": "nonprobability-sampling", "title": "Nonprobability sampling and selection bias", "order": 3},
            {"id": "probability-sampling", "title": "Simple random, stratified, and weighted sampling", "order": 4},
            {"id": "stream-special-sampling", "title": "Reservoir sampling and importance sampling", "order": 5},
            {"id": "hand-labeling", "title": "Labels: why hand labeling is difficult", "order": 6},
            {"id": "label-multiplicity-lineage", "title": "Label multiplicity and data lineage", "order": 7},
            {"id": "natural-labels", "title": "Natural labels, behavioral labels, and feedback loops", "order": 8},
            {"id": "label-scarcity", "title": "Four strategies when labels are scarce", "order": 9},
            {"id": "weak-supervision", "title": "Weak supervision and programmatic labeling", "order": 10},
            {"id": "semi-transfer-active", "title": "Semi-supervision, transfer learning, and active learning", "order": 11},
            {"id": "class-imbalance", "title": "Why class imbalance is difficult", "order": 12},
            {"id": "imbalance-metrics", "title": "Evaluate imbalanced problems with the right metrics", "order": 13},
            {"id": "resampling", "title": "Data-level methods: resampling", "order": 14},
            {"id": "algorithm-level-imbalance", "title": "Algorithm-level methods for class imbalance", "order": 15},
            {"id": "data-augmentation", "title": "Data augmentation", "order": 16},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M04.L01.EX01",
            "title": "Choose the right sampling strategy",
            "lesson_code": "M04.L01",
            "section_id": "probability-sampling",
            "placement": "after_section",
            "description": (
                "Practice choosing sampling methods based on rarity, stream size, "
                "and distribution mismatch."
            ),
            "instructions": (
                "Choose the most suitable sampling method discussed in the lesson "
                "for each situation and explain your reasoning:\n\n"
                "1. A fraud class represents only 0.05% of transactions, and you "
                "must ensure both fraud and non-fraud examples appear in a sample.\n"
                "2. You are consuming an endless event stream and can keep only "
                "10,000 examples in memory while giving every observed event an "
                "equal chance of inclusion.\n"
                "3. Recent customer behavior is more valuable than old behavior, "
                "so recent records should be selected more often.\n"
                "4. You need a quick prototype and only have access to the easiest "
                "data source, but you must also state the main statistical risk."
            ),
            "expected_output": (
                "Four sampling choices with one- to three-sentence justifications "
                "and the important bias or trade-off for each."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "sampling-strategy",
                "stratified-sampling",
                "weighted-sampling",
                "reservoir-sampling",
            ],
        },

        {
            "id": "M04.L01.EX02",
            "title": "Design a useful feedback label",
            "lesson_code": "M04.L01",
            "section_id": "natural-labels",
            "placement": "after_section",
            "description": (
                "Reason about natural labels, feedback strength, and feedback delay."
            ),
            "instructions": (
                "You are designing an ecommerce recommender. Possible feedback "
                "signals are impression, click, add-to-cart, purchase, review, and return.\n\n"
                "1. Choose one fast, high-volume signal.\n"
                "2. Choose one slower but stronger signal.\n"
                "3. Explain what an implicit negative label might look like.\n"
                "4. Explain how choosing a very short feedback window could create "
                "premature negative labels.\n"
                "5. State which business or product discussion must happen before "
                "choosing the final target."
            ),
            "expected_output": (
                "A short comparison of candidate labels, including signal strength, "
                "feedback loop length, and one risk of premature labeling."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "natural-labels",
                "feedback-loop",
                "implicit-labels",
            ],
        },

        {
            "id": "M04.L01.EX03",
            "title": "Choose a strategy for limited labels",
            "lesson_code": "M04.L01",
            "section_id": "semi-transfer-active",
            "placement": "after_section",
            "description": (
                "Compare weak supervision, semi-supervision, transfer learning, "
                "and active learning."
            ),
            "instructions": (
                "For each scenario, choose the most suitable method from weak "
                "supervision, semi-supervision, transfer learning, or active learning:\n\n"
                "1. Experts can write reliable domain heuristics, but cannot label "
                "millions of records manually.\n"
                "2. You have a small labeled set and a very large unlabeled pool, "
                "and nearby examples often share labels.\n"
                "3. A strong pretrained model already exists for a related task.\n"
                "4. Human annotators are expensive, so you want the model to choose "
                "which examples they should label next.\n\n"
                "Explain one important limitation or requirement for each choice."
            ),
            "expected_output": (
                "Four method selections with concise justifications and one "
                "limitation or dependency for each."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "weak-supervision",
                "semi-supervision",
                "transfer-learning",
                "active-learning",
            ],
        },

        {
            "id": "M04.L01.EX04",
            "title": "Evaluate an imbalanced classifier",
            "lesson_code": "M04.L01",
            "section_id": "imbalance-metrics",
            "placement": "after_section",
            "description": (
                "Practice interpreting confusion-matrix metrics when the minority "
                "class matters."
            ),
            "instructions": (
                "A disease classifier produces:\n"
                "- TP = 80\n"
                "- FP = 20\n"
                "- FN = 20\n"
                "- TN = 880\n\n"
                "1. Compute precision.\n"
                "2. Compute recall.\n"
                "3. Compute F1 using the formula in the lesson.\n"
                "4. Explain why overall accuracy alone would not be enough to "
                "evaluate this task.\n"
                "5. Explain what might happen to recall and false positives if you "
                "lower the decision threshold."
            ),
            "expected_output": (
                "Precision, recall, and F1 calculations plus a short interpretation "
                "of threshold trade-offs and class imbalance."
            ),
            "type": "code",
            "language": "python",
            "starter_code": (
                "tp = 80\n"
                "fp = 20\n"
                "fn = 20\n"
                "tn = 880\n\n"
                "# TODO: calculate all three minority-class metrics.\n"
                "precision = None\n"
                "recall = None\n"
                "f1 = None\n"
            ),
            "solution_code": (
                "tp = 80\n"
                "fp = 20\n"
                "fn = 20\n"
                "tn = 880\n\n"
                "precision = tp / (tp + fp)\n"
                "recall = tp / (tp + fn)\n"
                "f1 = 2 * precision * recall / (precision + recall)\n"
            ),
            "hint": "Use TP / (TP + FP), TP / (TP + FN), then the harmonic mean of precision and recall.",
            "success_message": "Correct! Precision, recall, and F1 are all 0.8 for this confusion matrix.",
            "tests": [
                {
                    "id": "precision_is_numeric",
                    "type": "type_equals",
                    "variable": "precision",
                    "expected": "float",
                    "feedback": {
                        "en": "Calculate `precision` as a numeric value.",
                        "ar": "احسب `precision` كقيمة رقمية.",
                    },
                },
                {
                    "id": "precision_value",
                    "type": "value_approx",
                    "variable": "precision",
                    "expected": 0.8,
                    "feedback": {
                        "en": "Check the precision denominator: TP + FP.",
                        "ar": "راجع مقام precision: ‏TP + FP.",
                    },
                },
                {
                    "id": "recall_value",
                    "type": "value_approx",
                    "variable": "recall",
                    "expected": 0.8,
                    "feedback": {
                        "en": "Check the recall denominator: TP + FN.",
                        "ar": "راجع مقام recall: ‏TP + FN.",
                    },
                },
                {
                    "id": "f1_value",
                    "type": "value_approx",
                    "variable": "f1",
                    "expected": 0.8,
                    "feedback": {
                        "en": "Calculate F1 as the harmonic mean of precision and recall.",
                        "ar": "احسب F1 بوصفه المتوسط التوافقي لـ precision وrecall.",
                    },
                },
            ],
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "precision",
                "recall",
                "f1",
                "class-imbalance-evaluation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M04.L01.QZ01",

        "title": "Training Data — Knowledge Check",

        "lesson_code": "M04.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M04.L01.Q01",
                "section_id": "training-data-foundation",
                "question": (
                    "Why does the chapter prefer the term 'training data' over "
                    "'training dataset'?"
                ),
                "options": [
                    "Because training data never includes validation data.",
                    "Because production data is not necessarily finite or stationary.",
                    "Because datasets cannot contain labels.",
                    "Because only streaming systems use training data.",
                ],
                "correct": 1,
                "explanation": (
                    "Production data changes and grows, so treating it as one fixed, "
                    "stationary set can be misleading."
                ),
            },

            {
                "id": "M04.L01.Q02",
                "section_id": "nonprobability-sampling",
                "question": (
                    "What is the main statistical risk of convenience sampling?"
                ),
                "options": [
                    "It always costs more than random sampling.",
                    "It can create selection bias because available data may not represent reality.",
                    "It can only be used with images.",
                    "It guarantees rare classes are oversampled.",
                ],
                "correct": 1,
                "explanation": (
                    "Easy-to-obtain examples can differ systematically from the "
                    "population the model will face."
                ),
            },

            {
                "id": "M04.L01.Q03",
                "section_id": "probability-sampling",
                "question": (
                    "Why might stratified sampling be preferred over simple random "
                    "sampling when one class is very rare?"
                ),
                "options": [
                    "It guarantees every example is selected.",
                    "It samples separately within groups so rare classes can be represented.",
                    "It removes the need for labels.",
                    "It works only for regression.",
                ],
                "correct": 1,
                "explanation": (
                    "Sampling inside each stratum prevents an important rare group "
                    "from disappearing simply by chance."
                ),
            },

            {
                "id": "M04.L01.Q04",
                "section_id": "stream-special-sampling",
                "question": (
                    "Which method is designed to maintain a fixed-size uniform "
                    "sample from a stream whose total length is unknown?"
                ),
                "options": [
                    "Quota sampling",
                    "Reservoir sampling",
                    "Judgment sampling",
                    "SMOTE",
                ],
                "correct": 1,
                "explanation": (
                    "Reservoir sampling keeps bounded memory while preserving equal "
                    "selection probability among observed items."
                ),
            },

            {
                "id": "M04.L01.Q05",
                "section_id": "label-multiplicity-lineage",
                "question": "What does data lineage provide?",
                "options": [
                    "Automatic model architecture search",
                    "A record of where examples and labels came from",
                    "A replacement for validation data",
                    "Guaranteed perfect annotations",
                ],
                "correct": 1,
                "explanation": (
                    "Lineage preserves provenance so teams can connect failures to "
                    "specific data sources or labeling processes."
                ),
            },

            {
                "id": "M04.L01.Q06",
                "section_id": "natural-labels",
                "question": (
                    "What is feedback loop length?"
                ),
                "options": [
                    "The number of hidden layers in a model",
                    "The time from a served prediction until its feedback or natural label arrives",
                    "The amount of time required to train one epoch",
                    "The number of annotators used for one example",
                ],
                "correct": 1,
                "explanation": (
                    "Feedback loop length measures how long the system waits before "
                    "the real outcome becomes observable."
                ),
            },

            {
                "id": "M04.L01.Q07",
                "section_id": "weak-supervision",
                "question": (
                    "What is a labeling function in weak supervision?"
                ),
                "options": [
                    "A perfectly accurate human annotation",
                    "A function that encodes a heuristic for assigning labels",
                    "A model evaluation metric",
                    "A sampling probability",
                ],
                "correct": 1,
                "explanation": (
                    "Labeling functions encode noisy domain heuristics that can be "
                    "applied programmatically across many examples."
                ),
            },

            {
                "id": "M04.L01.Q08",
                "section_id": "semi-transfer-active",
                "question": (
                    "Which method explicitly asks the model to select the examples "
                    "that are most useful to send for human labeling?"
                ),
                "options": [
                    "Transfer learning",
                    "Active learning",
                    "Convenience sampling",
                    "Simple random sampling",
                ],
                "correct": 1,
                "explanation": (
                    "Active learning tries to use annotation budget efficiently by "
                    "selecting informative examples such as uncertain cases."
                ),
            },

            {
                "id": "M04.L01.Q09",
                "section_id": "class-imbalance",
                "question": (
                    "A dataset is 99.99% NORMAL and 0.01% CANCER. A model always "
                    "predicts NORMAL. What is the main lesson?"
                ),
                "options": [
                    "The model is excellent because accuracy is 99.99%.",
                    "High overall accuracy can hide complete failure on the minority class.",
                    "The dataset must be perfectly balanced before any training.",
                    "Recall and precision are identical to accuracy.",
                ],
                "correct": 1,
                "explanation": (
                    "Majority-class dominance can make accuracy look excellent even "
                    "when the model fails at the actual rare-event detection task."
                ),
            },

            {
                "id": "M04.L01.Q10",
                "section_id": "imbalance-metrics",
                "question": (
                    "Which metric answers: 'Of all actual positive examples, what "
                    "fraction did the model correctly identify?'"
                ),
                "options": [
                    "Precision",
                    "Recall",
                    "Specificity only",
                    "Overall accuracy",
                ],
                "correct": 1,
                "explanation": (
                    "Recall is TP / (TP + FN), so it measures how many actual "
                    "positives were recovered."
                ),
            },

            {
                "id": "M04.L01.Q11",
                "section_id": "resampling",
                "question": (
                    "Why should a model not be evaluated on the resampled training distribution?"
                ),
                "options": [
                    "Because resampling can create an artificial class distribution.",
                    "Because validation data can never contain minority examples.",
                    "Because oversampling prevents model training.",
                    "Because evaluation requires only unlabeled data.",
                ],
                "correct": 0,
                "explanation": (
                    "The resampled distribution is a training intervention and may "
                    "not reflect the real environment in which performance matters."
                ),
            },

            {
                "id": "M04.L01.Q12",
                "section_id": "algorithm-level-imbalance",
                "question": (
                    "What is the core intuition behind focal loss?"
                ),
                "options": [
                    "Remove all difficult examples.",
                    "Give less emphasis to easy examples and more to hard examples.",
                    "Force every class to have the same sample count.",
                    "Always maximize accuracy on the majority class.",
                ],
                "correct": 1,
                "explanation": (
                    "Focal loss reduces the contribution of already-easy examples "
                    "so training focuses more on examples the model still finds difficult."
                ),
            },

            {
                "id": "M04.L01.Q13",
                "section_id": "data-augmentation",
                "question": (
                    "Which statement best describes label-preserving augmentation?"
                ),
                "options": [
                    "It intentionally changes the target class.",
                    "It modifies an example while assuming the correct label remains valid.",
                    "It deletes all rare examples.",
                    "It requires human relabeling of every transformed sample.",
                ],
                "correct": 1,
                "explanation": (
                    "A valid label-preserving transformation changes the input while "
                    "keeping the underlying target unchanged."
                ),
            },

            {
                "id": "M04.L01.Q14",
                "section_id": "semi-transfer-active",
                "type": "open",
                "question": (
                    "You have 5,000 manually labeled examples, 2 million unlabeled "
                    "examples, a related pretrained model, and a limited annotation "
                    "budget. Describe how at least two of the chapter's strategies "
                    "for label scarcity could be combined, and state one risk or "
                    "assumption for each strategy you choose."
                ),
            },
        ],

        "passing_score": 70,
    },
}
