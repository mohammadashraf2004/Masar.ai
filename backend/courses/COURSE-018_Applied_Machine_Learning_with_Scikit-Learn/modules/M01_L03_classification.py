"""M01.L03 — Classification.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 3 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L03"

MODULE_ORDER = 1

MODULE_TITLE = "Classification Systems"

MODULE_DESCRIPTION = (
    "Learn how to build and evaluate classification systems, from binary "
    "classification and confusion matrices through precision/recall trade-offs, "
    "ROC analysis, multiclass strategies, error analysis, multilabel learning, "
    "and multioutput classification."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Classification",

    "slug": "machine-learning-foundations-m01-l03",

    "description": (
        "A practical classification lesson built around MNIST, covering binary "
        "classification, evaluation metrics, decision thresholds, PR and ROC "
        "curves, multiclass strategies, error analysis, multilabel targets, "
        "and multioutput prediction."
    ),

    "order": 3,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "machine-learning",
        "classification",
        "binary-classification",
        "precision",
        "recall",
        "f1-score",
        "roc-auc",
        "confusion-matrix",
        "multiclass",
        "multilabel",
        "multioutput",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
    ],


    # =======================================================================
    # INLINE IMAGE RULES
    # =======================================================================
    #
    # Only high-value figures from the supplied Chapter 3 are requested.
    # Each request preserves the original source figure number and includes
    # a stable key for later manual linking.
    #
    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Classification",

        "content": (
            "# Classification\n"
            "\n"
            "> **Course:** Applied Machine Learning with Scikit-Learn  \n"
            "> **Lesson:** M01.L03  \n"
            "> **Module:** Classification Systems  \n"
            "> **Source alignment:** Chapter 3, “Classification,” supplied by the course author. Page numbers were not included in the supplied extract. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the difference between binary, multiclass, multilabel, and multioutput classification.\n"
            "- Load and interpret the MNIST dataset and understand why each 28 × 28 image becomes 784 input features.\n"
            "- Train a binary classifier using `SGDClassifier`.\n"
            "- Explain why accuracy can be misleading on imbalanced datasets.\n"
            "- Read a confusion matrix and identify true positives, true negatives, false positives, and false negatives.\n"
            "- Compute and interpret precision, recall, and F1 score.\n"
            "- Explain the precision/recall trade-off and choose a decision threshold for a project requirement.\n"
            "- Use precision-recall curves and ROC curves appropriately.\n"
            "- Interpret ROC AUC and know when a PR curve is more informative than a ROC curve.\n"
            "- Compare classifiers using out-of-sample cross-validation predictions.\n"
            "- Explain one-versus-the-rest and one-versus-one multiclass strategies.\n"
            "- Analyze multiclass confusion matrices and use error analysis to improve a classifier.\n"
            "- Build simple multilabel and multioutput classification systems.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. From regression to classification\n"
            "\n"
            "In regression, the model predicts a numerical value.\n"
            "\n"
            "```text\n"
            "house price -> 245,000\n"
            "temperature -> 31.4\n"
            "revenue -> 8.2 million\n"
            "```\n"
            "\n"
            "In **classification**, the model predicts a class or category.\n"
            "\n"
            "```text\n"
            "email -> spam\n"
            "image -> digit 5\n"
            "transaction -> fraud\n"
            "document -> sports\n"
            "```\n"
            "\n"
            "The chapter uses **MNIST**, a classic dataset containing `70,000` handwritten digit images.\n"
            "\n"
            "Each image represents one digit from:\n"
            "\n"
            "```text\n"
            "0, 1, 2, 3, 4, 5, 6, 7, 8, 9\n"
            "```\n"
            "\n"
            "Each image is:\n"
            "\n"
            "```text\n"
            "28 × 28 pixels\n"
            "```\n"
            "\n"
            "So the input contains:\n"
            "\n"
            "```text\n"
            "28 × 28 = 784 features\n"
            "```\n"
            "\n"
            "Each feature stores one pixel intensity, from approximately:\n"
            "\n"
            "```text\n"
            "0   -> white\n"
            "255 -> black\n"
            "```\n"
            "\n"
            "### Load MNIST\n"
            "\n"
            "```python\n"
            "from sklearn.datasets import fetch_openml\n"
            "\n"
            "mnist = fetch_openml(\n"
            "    \"mnist_784\",\n"
            "    as_frame=False,\n"
            ")\n"
            "\n"
            "X, y = mnist.data, mnist.target\n"
            "\n"
            "print(X.shape)\n"
            "print(y.shape)\n"
            "```\n"
            "\n"
            "Expected shapes:\n"
            "\n"
            "```text\n"
            "X -> (70000, 784)\n"
            "y -> (70000,)\n"
            "```\n"
            "\n"
            "A single row of `X` is therefore not stored as a 28 × 28 image. It is stored as a vector containing 784 pixel values.\n"
            "\n"
            "To visualize one digit:\n"
            "\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "def plot_digit(image_data):\n"
            "    image = image_data.reshape(28, 28)\n"
            "    plt.imshow(image, cmap=\"binary\")\n"
            "    plt.axis(\"off\")\n"
            "\n"
            "some_digit = X[0]\n"
            "plot_digit(some_digit)\n"
            "plt.show()\n"
            "```\n"
            "\n"
            "{{image:mnist-single-digit-example}}\n"
            "\n"
            "The corresponding label is:\n"
            "\n"
            "```python\n"
            "print(y[0])\n"
            "```\n"
            "\n"
            "which is:\n"
            "\n"
            "```text\n"
            "5\n"
            "```\n"
            "\n"
            "### Protect the test set\n"
            "\n"
            "MNIST is already arranged with:\n"
            "\n"
            "```python\n"
            "X_train = X[:60000]\n"
            "X_test = X[60000:]\n"
            "\n"
            "y_train = y[:60000]\n"
            "y_test = y[60000:]\n"
            "```\n"
            "\n"
            "So:\n"
            "\n"
            "```text\n"
            "60,000 -> training images\n"
            "10,000 -> test images\n"
            "```\n"
            "\n"
            "Just as in the previous lesson, the test set should remain untouched while you develop the classifier.\n"
            "\n"
            "The training set is already shuffled, which helps cross-validation because each fold should contain a reasonable mix of digits.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. Start simple: build a binary classifier\n"
            "\n"
            "Before trying to recognize all ten digits, simplify the task.\n"
            "\n"
            "Ask only:\n"
            "\n"
            "> **Is this digit a 5 or not a 5?**\n"
            "\n"
            "This gives two classes:\n"
            "\n"
            "```text\n"
            "positive class -> 5\n"
            "negative class -> not 5\n"
            "```\n"
            "\n"
            "Create Boolean target arrays:\n"
            "\n"
            "```python\n"
            "y_train_5 = (y_train == \"5\")\n"
            "y_test_5 = (y_test == \"5\")\n"
            "```\n"
            "\n"
            "Now train a stochastic gradient descent classifier:\n"
            "\n"
            "```python\n"
            "from sklearn.linear_model import SGDClassifier\n"
            "\n"
            "sgd_clf = SGDClassifier(random_state=42)\n"
            "\n"
            "sgd_clf.fit(\n"
            "    X_train,\n"
            "    y_train_5,\n"
            ")\n"
            "```\n"
            "\n"
            "Make a prediction:\n"
            "\n"
            "```python\n"
            "sgd_clf.predict([some_digit])\n"
            "```\n"
            "\n"
            "For the example image, the model predicts:\n"
            "\n"
            "```text\n"
            "True\n"
            "```\n"
            "\n"
            "which is correct.\n"
            "\n"
            "But one correct prediction tells us almost nothing about classifier quality.\n"
            "\n"
            "We need evaluation metrics.\n"
            "\n"
            "### Accuracy with cross-validation\n"
            "\n"
            "A first attempt is cross-validation accuracy:\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import cross_val_score\n"
            "\n"
            "scores = cross_val_score(\n"
            "    sgd_clf,\n"
            "    X_train,\n"
            "    y_train_5,\n"
            "    cv=3,\n"
            "    scoring=\"accuracy\",\n"
            ")\n"
            "\n"
            "print(scores)\n"
            "```\n"
            "\n"
            "The source reports accuracies above `95%`.\n"
            "\n"
            "That sounds excellent.\n"
            "\n"
            "But now compare it with a classifier that simply predicts:\n"
            "\n"
            "```text\n"
            "not 5\n"
            "```\n"
            "\n"
            "for every image.\n"
            "\n"
            "```python\n"
            "from sklearn.dummy import DummyClassifier\n"
            "\n"
            "dummy_clf = DummyClassifier()\n"
            "\n"
            "dummy_clf.fit(\n"
            "    X_train,\n"
            "    y_train_5,\n"
            ")\n"
            "\n"
            "dummy_scores = cross_val_score(\n"
            "    dummy_clf,\n"
            "    X_train,\n"
            "    y_train_5,\n"
            "    cv=3,\n"
            "    scoring=\"accuracy\",\n"
            ")\n"
            "\n"
            "print(dummy_scores)\n"
            "```\n"
            "\n"
            "This classifier still gets roughly:\n"
            "\n"
            "```text\n"
            "90.9% accuracy\n"
            "```\n"
            "\n"
            "Why?\n"
            "\n"
            "Because only about 10% of the images are 5s.\n"
            "\n"
            "If you always predict “not 5,” you are correct most of the time.\n"
            "\n"
            "### Important lesson\n"
            "\n"
            "**Accuracy can be extremely misleading when classes are imbalanced.**\n"
            "\n"
            "Suppose a medical dataset contains:\n"
            "\n"
            "```text\n"
            "99 healthy patients\n"
            "1 sick patient\n"
            "```\n"
            "\n"
            "A classifier that always predicts:\n"
            "\n"
            "```text\n"
            "healthy\n"
            "```\n"
            "\n"
            "gets:\n"
            "\n"
            "```text\n"
            "99% accuracy\n"
            "```\n"
            "\n"
            "but it completely fails the purpose of the system.\n"
            "\n"
            "That is why classification requires richer metrics.\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Confusion matrix: understand exactly what the classifier gets wrong\n"
            "\n"
            "Instead of asking only:\n"
            "\n"
            "> “How many predictions were correct?”\n"
            "\n"
            "ask:\n"
            "\n"
            "> **“Which kinds of predictions were correct or incorrect?”**\n"
            "\n"
            "This is what a **confusion matrix** shows.\n"
            "\n"
            "To evaluate training examples without fitting and predicting on the same instance, use cross-validation predictions:\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import cross_val_predict\n"
            "\n"
            "y_train_pred = cross_val_predict(\n"
            "    sgd_clf,\n"
            "    X_train,\n"
            "    y_train_5,\n"
            "    cv=3,\n"
            ")\n"
            "```\n"
            "\n"
            "Every prediction is now **out-of-sample** within the training set: the instance was predicted by a model that did not train on that fold.\n"
            "\n"
            "Compute the confusion matrix:\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import confusion_matrix\n"
            "\n"
            "cm = confusion_matrix(\n"
            "    y_train_5,\n"
            "    y_train_pred,\n"
            ")\n"
            "\n"
            "print(cm)\n"
            "```\n"
            "\n"
            "The source obtains:\n"
            "\n"
            "```text\n"
            "[[53892,   687],\n"
            " [ 1891,  3530]]\n"
            "```\n"
            "\n"
            "Interpret it as:\n"
            "\n"
            "| Actual / Predicted | Not 5 | 5 |\n"
            "|---|---:|---:|\n"
            "| Not 5 | 53,892 | 687 |\n"
            "| 5 | 1,891 | 3,530 |\n"
            "\n"
            "Now name the four cells.\n"
            "\n"
            "### True negative\n"
            "\n"
            "```text\n"
            "Actual: not 5\n"
            "Predicted: not 5\n"
            "```\n"
            "\n"
            "Correct negative prediction.\n"
            "\n"
            "### False positive\n"
            "\n"
            "```text\n"
            "Actual: not 5\n"
            "Predicted: 5\n"
            "```\n"
            "\n"
            "The classifier raises a positive prediction incorrectly.\n"
            "\n"
            "Also called a **Type I error**.\n"
            "\n"
            "### False negative\n"
            "\n"
            "```text\n"
            "Actual: 5\n"
            "Predicted: not 5\n"
            "```\n"
            "\n"
            "The classifier misses a real positive.\n"
            "\n"
            "Also called a **Type II error**.\n"
            "\n"
            "### True positive\n"
            "\n"
            "```text\n"
            "Actual: 5\n"
            "Predicted: 5\n"
            "```\n"
            "\n"
            "Correct positive prediction.\n"
            "\n"
            "{{image:binary-confusion-matrix}}\n"
            "\n"
            "A perfect classifier would have only:\n"
            "\n"
            "```text\n"
            "true negatives\n"
            "true positives\n"
            "```\n"
            "\n"
            "and zeros in the two error cells.\n"
            "\n"
            "### Why the confusion matrix matters\n"
            "\n"
            "Two models can have similar accuracy while making very different mistakes.\n"
            "\n"
            "That difference may determine which model is acceptable.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "medical screening:\n"
            "false negatives may be especially costly\n"
            "\n"
            "automatic content moderation:\n"
            "false positives may be especially costly\n"
            "\n"
            "fraud alerts:\n"
            "both may matter, but in different ways\n"
            "```\n"
            "\n"
            "The metric must match the consequence of the error.\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Precision, recall, and F1 score\n"
            "\n"
            "The confusion matrix contains rich information, but sometimes we need smaller summary metrics.\n"
            "\n"
            "### Precision\n"
            "\n"
            "**Precision** asks:\n"
            "\n"
            "> Of the examples predicted as positive, how many were actually positive?\n"
            "\n"
            "```text\n"
            "precision = TP / (TP + FP)\n"
            "```\n"
            "\n"
            "For the source classifier:\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import precision_score\n"
            "\n"
            "precision = precision_score(\n"
            "    y_train_5,\n"
            "    y_train_pred,\n"
            ")\n"
            "\n"
            "print(precision)\n"
            "```\n"
            "\n"
            "The source obtains approximately:\n"
            "\n"
            "```text\n"
            "0.837\n"
            "```\n"
            "\n"
            "So when the classifier predicts “5,” it is correct about:\n"
            "\n"
            "```text\n"
            "83.7%\n"
            "```\n"
            "\n"
            "of the time.\n"
            "\n"
            "### Recall\n"
            "\n"
            "**Recall** asks:\n"
            "\n"
            "> Of all the actual positive examples, how many did the classifier detect?\n"
            "\n"
            "```text\n"
            "recall = TP / (TP + FN)\n"
            "```\n"
            "\n"
            "It is also called:\n"
            "\n"
            "- sensitivity,\n"
            "- true positive rate,\n"
            "- TPR.\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import recall_score\n"
            "\n"
            "recall = recall_score(\n"
            "    y_train_5,\n"
            "    y_train_pred,\n"
            ")\n"
            "\n"
            "print(recall)\n"
            "```\n"
            "\n"
            "The source obtains approximately:\n"
            "\n"
            "```text\n"
            "0.651\n"
            "```\n"
            "\n"
            "So the classifier detects only about:\n"
            "\n"
            "```text\n"
            "65.1%\n"
            "```\n"
            "\n"
            "of the actual 5s.\n"
            "\n"
            "### Precision and recall describe different risks\n"
            "\n"
            "High precision means:\n"
            "\n"
            "```text\n"
            "when I say positive,\n"
            "I am usually right\n"
            "```\n"
            "\n"
            "High recall means:\n"
            "\n"
            "```text\n"
            "when a real positive exists,\n"
            "I usually catch it\n"
            "```\n"
            "\n"
            "Consider two applications.\n"
            "\n"
            "**Child-safe video filtering**\n"
            "\n"
            "False positives may be acceptable if they mean rejecting some safe videos.\n"
            "\n"
            "But allowing unsafe videos through may be unacceptable.\n"
            "\n"
            "So high precision for the “safe” prediction can be especially important.\n"
            "\n"
            "**Medical screening**\n"
            "\n"
            "Missing a true case may be dangerous.\n"
            "\n"
            "A system may tolerate more false alarms if it achieves very high recall.\n"
            "\n"
            "The correct trade-off depends on the project.\n"
            "\n"
            "### F1 score\n"
            "\n"
            "The **F1 score** combines precision and recall using their harmonic mean.\n"
            "\n"
            "```text\n"
            "F1 = 2 × (precision × recall) / (precision + recall)\n"
            "```\n"
            "\n"
            "In Scikit-Learn:\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import f1_score\n"
            "\n"
            "f1 = f1_score(\n"
            "    y_train_5,\n"
            "    y_train_pred,\n"
            ")\n"
            "\n"
            "print(f1)\n"
            "```\n"
            "\n"
            "The source obtains approximately:\n"
            "\n"
            "```text\n"
            "0.733\n"
            "```\n"
            "\n"
            "F1 is high only when both precision and recall are reasonably high.\n"
            "\n"
            "But F1 is not always the metric you should optimize.\n"
            "\n"
            "If one kind of error is much more costly than the other, hiding precision and recall inside one number may be undesirable.\n"
            "\n"
            "### Metric selection is a business decision\n"
            "\n"
            "Do not ask:\n"
            "\n"
            "> “Which metric is mathematically best?”\n"
            "\n"
            "Ask:\n"
            "\n"
            "> **“Which mistakes matter most in this application?”**\n"
            "\n"
            "{{exercise:M01.L03.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 5. The precision/recall trade-off\n"
            "\n"
            "Many classifiers do not directly start with a Boolean decision.\n"
            "\n"
            "They first compute a **score**.\n"
            "\n"
            "Then they compare that score with a threshold:\n"
            "\n"
            "```text\n"
            "score >= threshold -> positive\n"
            "score < threshold  -> negative\n"
            "```\n"
            "\n"
            "For `SGDClassifier`, use:\n"
            "\n"
            "```python\n"
            "y_scores = sgd_clf.decision_function(\n"
            "    [some_digit]\n"
            ")\n"
            "\n"
            "print(y_scores)\n"
            "```\n"
            "\n"
            "The default decision threshold is approximately:\n"
            "\n"
            "```text\n"
            "0\n"
            "```\n"
            "\n"
            "If you manually raise the threshold:\n"
            "\n"
            "```python\n"
            "threshold = 3000\n"
            "\n"
            "prediction = (\n"
            "    y_scores > threshold\n"
            ")\n"
            "```\n"
            "\n"
            "a digit that used to be classified as positive may become negative.\n"
            "\n"
            "### What happens when the threshold increases?\n"
            "\n"
            "In general:\n"
            "\n"
            "```text\n"
            "higher threshold\n"
            "    ->\n"
            "fewer positive predictions\n"
            "    ->\n"
            "precision tends to increase\n"
            "recall tends to decrease\n"
            "```\n"
            "\n"
            "Lowering the threshold generally does the opposite.\n"
            "\n"
            "{{image:precision-recall-threshold-tradeoff}}\n"
            "\n"
            "This is the **precision/recall trade-off**.\n"
            "\n"
            "You cannot choose a threshold in isolation.\n"
            "\n"
            "You need a requirement.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "\"We need at least 90% precision.\"\n"
            "```\n"
            "\n"
            "or:\n"
            "\n"
            "```text\n"
            "\"We need at least 95% recall.\"\n"
            "```\n"
            "\n"
            "### Get cross-validated decision scores\n"
            "\n"
            "Instead of class predictions:\n"
            "\n"
            "```python\n"
            "y_scores = cross_val_predict(\n"
            "    sgd_clf,\n"
            "    X_train,\n"
            "    y_train_5,\n"
            "    cv=3,\n"
            "    method=\"decision_function\",\n"
            ")\n"
            "```\n"
            "\n"
            "Then calculate precision and recall across possible thresholds:\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import precision_recall_curve\n"
            "\n"
            "precisions, recalls, thresholds = (\n"
            "    precision_recall_curve(\n"
            "        y_train_5,\n"
            "        y_scores,\n"
            "    )\n"
            ")\n"
            "```\n"
            "\n"
            "One useful visualization is precision directly against recall.\n"
            "\n"
            "{{image:precision-recall-curve}}\n"
            "\n"
            "### Find a threshold for a target precision\n"
            "\n"
            "Suppose you need at least 90% precision.\n"
            "\n"
            "```python\n"
            "idx_for_90_precision = (\n"
            "    precisions >= 0.90\n"
            ").argmax()\n"
            "\n"
            "threshold_for_90_precision = (\n"
            "    thresholds[idx_for_90_precision]\n"
            ")\n"
            "```\n"
            "\n"
            "Then:\n"
            "\n"
            "```python\n"
            "y_train_pred_90 = (\n"
            "    y_scores >= threshold_for_90_precision\n"
            ")\n"
            "```\n"
            "\n"
            "The source gets roughly:\n"
            "\n"
            "```text\n"
            "precision = 90%\n"
            "recall    = 48%\n"
            "```\n"
            "\n"
            "This demonstrates a critical lesson:\n"
            "\n"
            "> A classifier can achieve impressive precision simply by making fewer positive predictions.\n"
            "\n"
            "That does not automatically make it useful.\n"
            "\n"
            "Whenever someone says:\n"
            "\n"
            "```text\n"
            "\"We achieved 99% precision.\"\n"
            "```\n"
            "\n"
            "the immediate question should be:\n"
            "\n"
            "```text\n"
            "\"At what recall?\"\n"
            "```\n"
            "\n"
            "### Threshold tuning tools\n"
            "\n"
            "The chapter also introduces newer Scikit-Learn tools:\n"
            "\n"
            "- `FixedThresholdClassifier`\n"
            "- `TunedThresholdClassifierCV`\n"
            "\n"
            "The first lets you choose a threshold manually.\n"
            "\n"
            "The second can tune a threshold using cross-validation for a selected metric.\n"
            "\n"
            "The important concept is not the class name—it is that **decision threshold is part of system design**, not an untouchable constant.\n"
            "\n"
            "---\n"
            "\n"
            "## 6. ROC curves, AUC, and comparing classifiers\n"
            "\n"
            "Another way to evaluate a binary classifier across thresholds is the **ROC curve**.\n"
            "\n"
            "ROC plots:\n"
            "\n"
            "```text\n"
            "y-axis -> true positive rate (TPR)\n"
            "x-axis -> false positive rate (FPR)\n"
            "```\n"
            "\n"
            "Recall that:\n"
            "\n"
            "```text\n"
            "TPR = recall\n"
            "```\n"
            "\n"
            "The false positive rate is:\n"
            "\n"
            "```text\n"
            "FPR = FP / (FP + TN)\n"
            "```\n"
            "\n"
            "The true negative rate is also called **specificity**.\n"
            "\n"
            "```text\n"
            "FPR = 1 - specificity\n"
            "```\n"
            "\n"
            "Compute the ROC points:\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import roc_curve\n"
            "\n"
            "fpr, tpr, roc_thresholds = roc_curve(\n"
            "    y_train_5,\n"
            "    y_scores,\n"
            ")\n"
            "```\n"
            "\n"
            "A random classifier lies near the diagonal.\n"
            "\n"
            "A strong classifier pushes the curve toward the top-left corner.\n"
            "\n"
            "{{image:binary-roc-curve}}\n"
            "\n"
            "### ROC AUC\n"
            "\n"
            "The **area under the ROC curve**, or ROC AUC, summarizes the entire ROC curve.\n"
            "\n"
            "```text\n"
            "perfect classifier -> AUC = 1.0\n"
            "random classifier  -> AUC = 0.5\n"
            "```\n"
            "\n"
            "Compute it with:\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import roc_auc_score\n"
            "\n"
            "roc_auc = roc_auc_score(\n"
            "    y_train_5,\n"
            "    y_scores,\n"
            ")\n"
            "\n"
            "print(roc_auc)\n"
            "```\n"
            "\n"
            "The source SGD classifier gets approximately:\n"
            "\n"
            "```text\n"
            "0.9605\n"
            "```\n"
            "\n"
            "That sounds excellent.\n"
            "\n"
            "But there is an important warning.\n"
            "\n"
            "### ROC or precision-recall curve?\n"
            "\n"
            "The chapter gives this rule of thumb:\n"
            "\n"
            "Prefer the **precision-recall curve** when:\n"
            "\n"
            "- the positive class is rare,\n"
            "- or false positives are particularly important.\n"
            "\n"
            "The 5-versus-not-5 dataset is imbalanced.\n"
            "\n"
            "Because negatives are much more common, the ROC curve can make performance appear stronger than the PR curve suggests.\n"
            "\n"
            "So metric visualization must also match the class distribution and project priorities.\n"
            "\n"
            "### Compare models with PR curves\n"
            "\n"
            "The chapter compares `SGDClassifier` with `RandomForestClassifier`.\n"
            "\n"
            "A random forest does not expose the same `decision_function()`, but it provides estimated class probabilities:\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "\n"
            "forest_clf = RandomForestClassifier(\n"
            "    random_state=42\n"
            ")\n"
            "\n"
            "y_probas_forest = cross_val_predict(\n"
            "    forest_clf,\n"
            "    X_train,\n"
            "    y_train_5,\n"
            "    cv=3,\n"
            "    method=\"predict_proba\",\n"
            ")\n"
            "\n"
            "y_scores_forest = y_probas_forest[:, 1]\n"
            "```\n"
            "\n"
            "Then:\n"
            "\n"
            "```python\n"
            "precisions_forest, recalls_forest, thresholds_forest = (\n"
            "    precision_recall_curve(\n"
            "        y_train_5,\n"
            "        y_scores_forest,\n"
            "    )\n"
            ")\n"
            "```\n"
            "\n"
            "{{image:classifier-pr-curve-comparison}}\n"
            "\n"
            "In the source example, the random forest has substantially stronger:\n"
            "\n"
            "- PR curve,\n"
            "- F1 score,\n"
            "- ROC AUC.\n"
            "\n"
            "### Estimated probability is not guaranteed to be calibrated probability\n"
            "\n"
            "If a model reports:\n"
            "\n"
            "```text\n"
            "0.80 probability\n"
            "```\n"
            "\n"
            "that does not automatically mean that among all predictions near `0.80`, about 80% are truly positive.\n"
            "\n"
            "Model probabilities may be:\n"
            "\n"
            "- overconfident,\n"
            "- underconfident.\n"
            "\n"
            "The chapter mentions `CalibratedClassifierCV` for probability calibration.\n"
            "\n"
            "Calibration is especially important when the numerical probability itself drives a decision, such as:\n"
            "\n"
            "- medical risk,\n"
            "- credit risk,\n"
            "- fraud probability.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Multiclass classification\n"
            "\n"
            "A **binary classifier** distinguishes two classes.\n"
            "\n"
            "A **multiclass classifier** distinguishes more than two.\n"
            "\n"
            "For MNIST:\n"
            "\n"
            "```text\n"
            "10 classes\n"
            "0 through 9\n"
            "```\n"
            "\n"
            "Some algorithms support multiclass problems directly.\n"
            "\n"
            "Others are fundamentally binary and can be extended using strategies.\n"
            "\n"
            "### One-versus-the-rest\n"
            "\n"
            "**One-versus-the-rest (OvR)** trains one binary classifier per class.\n"
            "\n"
            "For MNIST:\n"
            "\n"
            "```text\n"
            "0 vs rest\n"
            "1 vs rest\n"
            "2 vs rest\n"
            "...\n"
            "9 vs rest\n"
            "```\n"
            "\n"
            "That produces:\n"
            "\n"
            "```text\n"
            "10 classifiers\n"
            "```\n"
            "\n"
            "At prediction time, the system evaluates the example using all class detectors and chooses the class with the strongest score.\n"
            "\n"
            "### One-versus-one\n"
            "\n"
            "**One-versus-one (OvO)** trains one classifier for every pair of classes.\n"
            "\n"
            "For `N` classes:\n"
            "\n"
            "```text\n"
            "N × (N - 1) / 2\n"
            "```\n"
            "\n"
            "For MNIST:\n"
            "\n"
            "```text\n"
            "10 × 9 / 2 = 45 classifiers\n"
            "```\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "0 vs 1\n"
            "0 vs 2\n"
            "0 vs 3\n"
            "...\n"
            "8 vs 9\n"
            "```\n"
            "\n"
            "The predicted class is determined by the class that wins the most pairwise comparisons.\n"
            "\n"
            "### Which strategy should you use?\n"
            "\n"
            "OvO trains more models, but each model sees only examples from two classes.\n"
            "\n"
            "This can be useful for algorithms whose training cost grows badly with dataset size, such as certain support vector machines.\n"
            "\n"
            "For many other binary algorithms, OvR is usually more practical.\n"
            "\n"
            "Scikit-Learn often chooses the appropriate strategy automatically.\n"
            "\n"
            "### SVC example\n"
            "\n"
            "```python\n"
            "from sklearn.svm import SVC\n"
            "\n"
            "svm_clf = SVC(\n"
            "    random_state=42\n"
            ")\n"
            "\n"
            "svm_clf.fit(\n"
            "    X_train[:2000],\n"
            "    y_train[:2000],\n"
            ")\n"
            "\n"
            "print(\n"
            "    svm_clf.predict([some_digit])\n"
            ")\n"
            "```\n"
            "\n"
            "The source obtains:\n"
            "\n"
            "```text\n"
            "5\n"
            "```\n"
            "\n"
            "For this multiclass problem, Scikit-Learn uses an OvO strategy for `SVC`.\n"
            "\n"
            "You can inspect class scores with:\n"
            "\n"
            "```python\n"
            "some_digit_scores = (\n"
            "    svm_clf.decision_function(\n"
            "        [some_digit]\n"
            "    )\n"
            ")\n"
            "\n"
            "print(\n"
            "    some_digit_scores.round(2)\n"
            ")\n"
            "```\n"
            "\n"
            "### Force a multiclass strategy\n"
            "\n"
            "You can explicitly use:\n"
            "\n"
            "```python\n"
            "from sklearn.multiclass import OneVsRestClassifier\n"
            "\n"
            "ovr_clf = OneVsRestClassifier(\n"
            "    SVC(random_state=42)\n"
            ")\n"
            "\n"
            "ovr_clf.fit(\n"
            "    X_train[:2000],\n"
            "    y_train[:2000],\n"
            ")\n"
            "```\n"
            "\n"
            "For ten MNIST classes:\n"
            "\n"
            "```python\n"
            "len(\n"
            "    ovr_clf.estimators_\n"
            ")\n"
            "```\n"
            "\n"
            "returns:\n"
            "\n"
            "```text\n"
            "10\n"
            "```\n"
            "\n"
            "### Scaling can matter\n"
            "\n"
            "The source trains an `SGDClassifier` directly on all ten classes and obtains cross-validation accuracy around:\n"
            "\n"
            "```text\n"
            "85.8% to 87.4%\n"
            "```\n"
            "\n"
            "Then it standardizes the inputs:\n"
            "\n"
            "```python\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "\n"
            "scaler = StandardScaler()\n"
            "\n"
            "X_train_scaled = scaler.fit_transform(\n"
            "    X_train.astype(\"float64\")\n"
            ")\n"
            "```\n"
            "\n"
            "and accuracy improves to roughly:\n"
            "\n"
            "```text\n"
            "89.1% to 90.2%\n"
            "```\n"
            "\n"
            "This is an important connection to the previous lesson:\n"
            "\n"
            "> **Data preparation can matter as much as switching algorithms.**\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Error analysis: use mistakes to decide what to improve\n"
            "\n"
            "Once you have a promising model, do not only ask:\n"
            "\n"
            "```text\n"
            "\"What is the accuracy?\"\n"
            "```\n"
            "\n"
            "Ask:\n"
            "\n"
            "```text\n"
            "\"Which classes does it confuse?\"\n"
            "```\n"
            "\n"
            "For multiclass classification, a confusion matrix is extremely useful.\n"
            "\n"
            "Generate out-of-sample predictions:\n"
            "\n"
            "```python\n"
            "y_train_pred = cross_val_predict(\n"
            "    sgd_clf,\n"
            "    X_train_scaled,\n"
            "    y_train,\n"
            "    cv=3,\n"
            ")\n"
            "```\n"
            "\n"
            "Then visualize:\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import ConfusionMatrixDisplay\n"
            "\n"
            "ConfusionMatrixDisplay.from_predictions(\n"
            "    y_train,\n"
            "    y_train_pred,\n"
            ")\n"
            "\n"
            "plt.show()\n"
            "```\n"
            "\n"
            "Raw counts can be misleading if classes have different frequencies.\n"
            "\n"
            "Normalize each row:\n"
            "\n"
            "```python\n"
            "ConfusionMatrixDisplay.from_predictions(\n"
            "    y_train,\n"
            "    y_train_pred,\n"
            "    normalize=\"true\",\n"
            "    values_format=\".0%\",\n"
            ")\n"
            "\n"
            "plt.show()\n"
            "```\n"
            "\n"
            "{{image:multiclass-confusion-matrix-normalized}}\n"
            "\n"
            "The source observes that:\n"
            "\n"
            "- only about 82% of the 5s are classified correctly,\n"
            "- a noticeable portion of 5s are predicted as 8s,\n"
            "- many classes produce false 8 predictions.\n"
            "\n"
            "This suggests a concrete improvement target:\n"
            "\n"
            "```text\n"
            "reduce false 8s\n"
            "```\n"
            "\n"
            "Possible actions include:\n"
            "\n"
            "- collect more examples resembling confusing cases,\n"
            "- engineer features that separate the confusing shapes,\n"
            "- improve preprocessing,\n"
            "- choose a different model.\n"
            "\n"
            "### Look at actual misclassified examples\n"
            "\n"
            "Metrics tell you **where** an error happens.\n"
            "\n"
            "Examples can tell you **why**.\n"
            "\n"
            "The chapter compares 3s and 5s.\n"
            "\n"
            "{{image:mnist-3-vs-5-error-analysis}}\n"
            "\n"
            "The simple SGD classifier assigns weights to pixels.\n"
            "\n"
            "A small shift in a handwritten stroke changes which pixel positions are active.\n"
            "\n"
            "So a digit that looks obviously like a 3 to a human may look much closer to a 5 in the model's fixed pixel-coordinate representation.\n"
            "\n"
            "### Data augmentation\n"
            "\n"
            "One solution is to add transformed versions of training images:\n"
            "\n"
            "```text\n"
            "slightly left\n"
            "slightly right\n"
            "slightly up\n"
            "slightly down\n"
            "slightly rotated\n"
            "```\n"
            "\n"
            "This is called **data augmentation**.\n"
            "\n"
            "Instead of telling the model mathematically that small translations should not change the digit identity, you show it many examples containing those transformations.\n"
            "\n"
            "The model can then become more tolerant of them.\n"
            "\n"
            "### Error analysis creates the next experiment\n"
            "\n"
            "A good workflow is:\n"
            "\n"
            "```text\n"
            "evaluate\n"
            "   |\n"
            "find dominant errors\n"
            "   |\n"
            "inspect examples\n"
            "   |\n"
            "form a hypothesis\n"
            "   |\n"
            "change data / features / model\n"
            "   |\n"
            "evaluate again\n"
            "```\n"
            "\n"
            "This is much better than blindly trying random algorithms.\n"
            "\n"
            "{{exercise:M01.L03.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Multilabel classification\n"
            "\n"
            "So far, every example has had exactly one class.\n"
            "\n"
            "But sometimes an instance can have several labels simultaneously.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "photo contains:\n"
            "Alice = True\n"
            "Bob = False\n"
            "Charlie = True\n"
            "```\n"
            "\n"
            "This is **multilabel classification**.\n"
            "\n"
            "The chapter demonstrates it using two labels for each MNIST digit:\n"
            "\n"
            "```text\n"
            "label 1 -> is the digit large? (7, 8, or 9)\n"
            "label 2 -> is the digit odd?\n"
            "```\n"
            "\n"
            "Create the targets:\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "\n"
            "y_train_large = (\n"
            "    y_train >= \"7\"\n"
            ")\n"
            "\n"
            "y_train_odd = (\n"
            "    y_train.astype(\"int8\") % 2 == 1\n"
            ")\n"
            "\n"
            "y_multilabel = np.c_[\n"
            "    y_train_large,\n"
            "    y_train_odd,\n"
            "]\n"
            "```\n"
            "\n"
            "Train a classifier that supports multiple labels:\n"
            "\n"
            "```python\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "\n"
            "knn_clf = KNeighborsClassifier()\n"
            "\n"
            "knn_clf.fit(\n"
            "    X_train,\n"
            "    y_multilabel,\n"
            ")\n"
            "```\n"
            "\n"
            "Predict for the example digit 5:\n"
            "\n"
            "```python\n"
            "knn_clf.predict(\n"
            "    [some_digit]\n"
            ")\n"
            "```\n"
            "\n"
            "The source obtains:\n"
            "\n"
            "```text\n"
            "[False, True]\n"
            "```\n"
            "\n"
            "Correct:\n"
            "\n"
            "```text\n"
            "5 is not large\n"
            "5 is odd\n"
            "```\n"
            "\n"
            "### Evaluating multilabel systems\n"
            "\n"
            "One strategy is to compute an F1 score for each label and average them.\n"
            "\n"
            "```python\n"
            "y_train_knn_pred = cross_val_predict(\n"
            "    knn_clf,\n"
            "    X_train,\n"
            "    y_multilabel,\n"
            "    cv=3,\n"
            ")\n"
            "\n"
            "score = f1_score(\n"
            "    y_multilabel,\n"
            "    y_train_knn_pred,\n"
            "    average=\"macro\",\n"
            ")\n"
            "```\n"
            "\n"
            "`macro` gives equal importance to each label.\n"
            "\n"
            "If common labels should contribute more, you can use:\n"
            "\n"
            "```python\n"
            "average=\"weighted\"\n"
            "```\n"
            "\n"
            "which weights labels according to their support.\n"
            "\n"
            "### Label dependencies\n"
            "\n"
            "Training one independent classifier per label may ignore relationships among labels.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "large digit\n"
            "and\n"
            "odd digit\n"
            "```\n"
            "\n"
            "are statistically related.\n"
            "\n"
            "A **ClassifierChain** lets later classifiers use predictions from earlier classifiers as extra inputs.\n"
            "\n"
            "```python\n"
            "from sklearn.multioutput import ClassifierChain\n"
            "from sklearn.svm import SVC\n"
            "\n"
            "chain_clf = ClassifierChain(\n"
            "    SVC(),\n"
            "    cv=3,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "chain_clf.fit(\n"
            "    X_train[:2000],\n"
            "    y_multilabel[:2000],\n"
            ")\n"
            "```\n"
            "\n"
            "The order of labels in the chain can affect performance.\n"
            "\n"
            "---\n"
            "\n"
            "## 10. Multioutput classification\n"
            "\n"
            "**Multioutput classification** generalizes multilabel classification.\n"
            "\n"
            "In multilabel classification:\n"
            "\n"
            "```text\n"
            "each output is usually binary\n"
            "```\n"
            "\n"
            "In multioutput classification:\n"
            "\n"
            "```text\n"
            "there are multiple outputs\n"
            "and\n"
            "each output can have multiple possible values\n"
            "```\n"
            "\n"
            "The chapter demonstrates this with image denoising.\n"
            "\n"
            "### Create noisy inputs\n"
            "\n"
            "Take an MNIST image and add random noise to every pixel.\n"
            "\n"
            "```python\n"
            "rng = np.random.default_rng(\n"
            "    seed=42\n"
            ")\n"
            "\n"
            "noise_train = rng.integers(\n"
            "    0,\n"
            "    100,\n"
            "    (len(X_train), 784),\n"
            ")\n"
            "\n"
            "X_train_mod = (\n"
            "    X_train + noise_train\n"
            ")\n"
            "\n"
            "noise_test = rng.integers(\n"
            "    0,\n"
            "    100,\n"
            "    (len(X_test), 784),\n"
            ")\n"
            "\n"
            "X_test_mod = (\n"
            "    X_test + noise_test\n"
            ")\n"
            "\n"
            "y_train_mod = X_train\n"
            "y_test_mod = X_test\n"
            "```\n"
            "\n"
            "Now:\n"
            "\n"
            "```text\n"
            "input  -> noisy pixel values\n"
            "target -> clean pixel values\n"
            "```\n"
            "\n"
            "Each output pixel can take many possible intensity values.\n"
            "\n"
            "So one image prediction contains:\n"
            "\n"
            "```text\n"
            "784 output labels\n"
            "```\n"
            "\n"
            "and each label may take values from approximately:\n"
            "\n"
            "```text\n"
            "0 to 255\n"
            "```\n"
            "\n"
            "{{image:multioutput-noisy-clean-target}}\n"
            "\n"
            "Train a k-nearest-neighbors classifier:\n"
            "\n"
            "```python\n"
            "knn_clf = KNeighborsClassifier()\n"
            "\n"
            "knn_clf.fit(\n"
            "    X_train_mod,\n"
            "    y_train_mod,\n"
            ")\n"
            "\n"
            "clean_digit = knn_clf.predict(\n"
            "    [X_test_mod[0]]\n"
            ")\n"
            "```\n"
            "\n"
            "The predicted image is much cleaner.\n"
            "\n"
            "{{image:multioutput-denoised-prediction}}\n"
            "\n"
            "### Classification and regression can overlap\n"
            "\n"
            "Predicting pixel intensities could reasonably be described as regression because intensity is numerical.\n"
            "\n"
            "This is a useful reminder:\n"
            "\n"
            "> Machine learning categories are tools for framing problems, not absolute laws of nature.\n"
            "\n"
            "Some practical problems lie near the boundary between categories.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> 95% classification accuracy always means the model is excellent.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "If one class dominates the dataset, even a classifier that ignores the minority class can achieve high accuracy. Compare against a baseline and inspect confusion-matrix metrics.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Precision and recall are two names for the same idea.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Precision asks how trustworthy positive predictions are. Recall asks how many actual positives were found.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> I should always maximize F1.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "F1 balances precision and recall. Some applications intentionally value one much more than the other.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> A threshold of 0.5 or 0 is mathematically mandatory.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The threshold is a decision policy. It can be adjusted to satisfy business requirements for precision, recall, cost, or another metric.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> ROC AUC is always the best metric for imbalanced classification.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "When the positive class is rare or false positives matter strongly, a precision-recall curve often exposes weaknesses more clearly.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Multiclass and multilabel classification are the same.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Multiclass normally chooses one class from several alternatives. Multilabel classification can assign several labels to the same instance.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Classification | Predicting discrete classes or labels |\n"
            "| Binary classification | Classification with two classes |\n"
            "| Multiclass classification | Classification with more than two mutually exclusive classes |\n"
            "| Multilabel classification | Predicting multiple binary labels for one instance |\n"
            "| Multioutput classification | Predicting multiple outputs where each output may itself have multiple values |\n"
            "| Accuracy | Fraction of all predictions that are correct |\n"
            "| Class imbalance | Situation where some classes are much more frequent than others |\n"
            "| Confusion matrix | Table counting actual-versus-predicted class outcomes |\n"
            "| True positive | Positive example correctly predicted as positive |\n"
            "| True negative | Negative example correctly predicted as negative |\n"
            "| False positive | Negative example incorrectly predicted as positive |\n"
            "| False negative | Positive example incorrectly predicted as negative |\n"
            "| Precision | Fraction of positive predictions that are correct |\n"
            "| Recall | Fraction of actual positives that are detected |\n"
            "| Sensitivity | Another name for recall / true positive rate |\n"
            "| Specificity | True negative rate |\n"
            "| F1 score | Harmonic mean of precision and recall |\n"
            "| Decision threshold | Score boundary used to convert classifier scores into class decisions |\n"
            "| PR curve | Precision-recall curve across decision thresholds |\n"
            "| ROC curve | True positive rate versus false positive rate across thresholds |\n"
            "| ROC AUC | Area under the ROC curve |\n"
            "| Probability calibration | Making estimated probabilities correspond more closely to observed frequencies |\n"
            "| One-versus-the-rest | Multiclass strategy using one detector per class |\n"
            "| One-versus-one | Multiclass strategy using one classifier for every pair of classes |\n"
            "| Error analysis | Systematic study of model mistakes to guide improvements |\n"
            "| Data augmentation | Creating transformed training examples to increase robustness |\n"
            "| Classifier chain | Multilabel strategy where later classifiers use earlier label predictions |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why does each MNIST image contain 784 input features?\n"
            "2. Why can a classifier that always predicts “not 5” achieve around 90% accuracy?\n"
            "3. What do TP, TN, FP, and FN mean?\n"
            "4. What is the difference between precision and recall?\n"
            "5. Why can increasing the decision threshold improve precision but reduce recall?\n"
            "6. When is a precision-recall curve usually more informative than a ROC curve?\n"
            "7. What does ROC AUC = 0.5 represent?\n"
            "8. Why should classifier probabilities sometimes be calibrated?\n"
            "9. How do OvR and OvO differ for a ten-class problem?\n"
            "10. Why did scaling improve the SGD multiclass classifier?\n"
            "11. What information can a normalized confusion matrix reveal?\n"
            "12. How can inspecting misclassified images lead to better preprocessing or data augmentation?\n"
            "13. What is the difference between multiclass and multilabel classification?\n"
            "14. What makes image denoising an example of a multioutput problem?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**Good classification is not just about predicting the correct class as often as possible. You must understand which errors the model makes, choose metrics that reflect the real cost of those errors, tune the decision policy appropriately, evaluate out of sample, and use error analysis to decide what to improve next.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "classification-mnist",
                "title": "From regression to classification",
                "order": 1,
            },
            {
                "id": "binary-classification",
                "title": "Start simple: build a binary classifier",
                "order": 2,
            },
            {
                "id": "confusion-matrix",
                "title": "Confusion matrix: understand exactly what the classifier gets wrong",
                "order": 3,
            },
            {
                "id": "precision-recall-f1",
                "title": "Precision, recall, and F1 score",
                "order": 4,
            },
            {
                "id": "precision-recall-tradeoff",
                "title": "The precision/recall trade-off",
                "order": 5,
            },
            {
                "id": "roc-model-comparison",
                "title": "ROC curves, AUC, and comparing classifiers",
                "order": 6,
            },
            {
                "id": "multiclass",
                "title": "Multiclass classification",
                "order": 7,
            },
            {
                "id": "error-analysis",
                "title": "Error analysis: use mistakes to decide what to improve",
                "order": 8,
            },
            {
                "id": "multilabel",
                "title": "Multilabel classification",
                "order": 9,
            },
            {
                "id": "multioutput",
                "title": "Multioutput classification",
                "order": 10,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L03.EX01",

            "title": "Choose the Right Classification Metric",

            "lesson_code": "M01.L03",

            "section_id": "precision-recall-f1",

            "placement": "after_section",

            "description": (
                "Practice reading confusion-matrix outcomes and selecting a "
                "metric based on the real consequence of classification errors."
            ),

            "instructions": (
                "A medical screening classifier produces the following results:\n\n"
                "- True positives: 180\n"
                "- False positives: 60\n"
                "- False negatives: 20\n"
                "- True negatives: 740\n\n"
                "1. Compute precision.\n"
                "2. Compute recall.\n"
                "3. Compute accuracy.\n"
                "4. Explain why recall may matter more than accuracy if missing "
                "a sick patient is especially costly.\n"
                "5. If the model's decision threshold is lowered, predict the "
                "general direction in which precision and recall are likely to "
                "move."
            ),

            "expected_output": (
                "Precision = 180 / 240 = 0.75, recall = 180 / 200 = 0.90, "
                "accuracy = 920 / 1000 = 0.92, followed by a short explanation "
                "that recall directly measures how many actual positive cases "
                "are found, and that lowering the threshold generally increases "
                "recall while reducing precision."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "confusion-matrix",
                "precision",
                "recall",
                "accuracy",
                "threshold-reasoning",
            ],
        },

        {
            "id": "M01.L03.EX02",

            "title": "Diagnose and Improve a Digit Classifier",

            "lesson_code": "M01.L03",

            "section_id": "error-analysis",

            "placement": "after_section",

            "description": (
                "Use multiclass confusion patterns and example-level reasoning "
                "to design the next improvement experiment."
            ),

            "instructions": (
                "Suppose a normalized confusion matrix shows that digit 5 is "
                "frequently predicted as 8, and manual inspection shows many "
                "errors occur when digits are slightly shifted or rotated.\n\n"
                "1. Explain what the confusion matrix tells you that overall "
                "accuracy does not.\n"
                "2. Give one data-focused improvement.\n"
                "3. Give one preprocessing-focused improvement.\n"
                "4. Explain how data augmentation with shifted and rotated "
                "digits could help.\n"
                "5. State how you would evaluate whether the change really "
                "improved the model without touching the final test set."
            ),

            "expected_output": (
                "A diagnosis centered on the 5-to-8 error pattern, followed by "
                "a reasonable data collection or augmentation strategy, a "
                "preprocessing idea such as centering/rotation normalization, "
                "and validation or cross-validation as the evaluation method."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "multiclass-confusion-matrix",
                "error-analysis",
                "data-augmentation",
                "preprocessing",
                "cross-validation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L03.QZ01",

        "title": "Classification — Knowledge Check",

        "lesson_code": "M01.L03",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L03.Q01",

                "section_id": "classification-mnist",

                "question": (
                    "Why does each 28 × 28 MNIST image appear as 784 input "
                    "features?"
                ),

                "options": [
                    "There are 784 possible digit classes.",
                    "Each pixel intensity is treated as one feature, and 28 × 28 = 784.",
                    "Scikit-Learn duplicates each image 28 times.",
                    "The final 784 values are model probabilities.",
                ],

                "correct": 1,

                "explanation": (
                    "MNIST images contain 28 rows and 28 columns of pixels. "
                    "Flattening the image produces 784 pixel-intensity features."
                ),
            },

            {
                "id": "M01.L03.Q02",

                "section_id": "binary-classification",

                "question": (
                    "Why can a classifier that always predicts 'not 5' obtain "
                    "roughly 90% accuracy on the 5-versus-rest task?"
                ),

                "options": [
                    "SGD automatically corrects its mistakes.",
                    "Only about 10% of the examples are 5s, so the negative class dominates.",
                    "MNIST has no labels for digit 5.",
                    "Accuracy ignores true negatives.",
                ],

                "correct": 1,

                "explanation": (
                    "The dataset is imbalanced for this binary task. Predicting "
                    "the majority negative class is correct most of the time even "
                    "though the classifier detects no 5s."
                ),
            },

            {
                "id": "M01.L03.Q03",

                "section_id": "confusion-matrix",

                "question": (
                    "A real positive example is incorrectly predicted as "
                    "negative. What is this?"
                ),

                "options": [
                    "True positive",
                    "True negative",
                    "False positive",
                    "False negative",
                ],

                "correct": 3,

                "explanation": (
                    "The example is actually positive but the classifier missed "
                    "it, so the result is a false negative."
                ),
            },

            {
                "id": "M01.L03.Q04",

                "section_id": "precision-recall-f1",

                "question": (
                    "Which question does precision answer?"
                ),

                "options": [
                    "Of all actual positives, how many did we detect?",
                    "Of all predicted positives, how many were actually positive?",
                    "How many examples exist in the dataset?",
                    "How many negatives were correctly rejected?",
                ],

                "correct": 1,

                "explanation": (
                    "Precision measures the reliability of positive predictions: "
                    "TP / (TP + FP)."
                ),
            },

            {
                "id": "M01.L03.Q05",

                "section_id": "precision-recall-tradeoff",

                "question": (
                    "What generally happens when you raise a binary classifier's "
                    "decision threshold?"
                ),

                "options": [
                    "Recall generally rises and precision falls.",
                    "Precision generally rises and recall falls.",
                    "Both always become 100%.",
                    "The model is retrained automatically.",
                ],

                "correct": 1,

                "explanation": (
                    "A higher threshold creates fewer positive predictions. This "
                    "typically removes false positives but also misses more true "
                    "positives."
                ),
            },

            {
                "id": "M01.L03.Q06",

                "section_id": "roc-model-comparison",

                "question": (
                    "When is a precision-recall curve often preferred over a ROC "
                    "curve?"
                ),

                "options": [
                    "When the positive class is rare or false positives matter strongly.",
                    "Only when there are exactly ten classes.",
                    "Only for regression.",
                    "Whenever all classes are perfectly balanced.",
                ],

                "correct": 0,

                "explanation": (
                    "PR curves are especially informative for rare positive "
                    "classes and when the quality of positive predictions matters "
                    "strongly."
                ),
            },

            {
                "id": "M01.L03.Q07",

                "section_id": "multiclass",

                "question": (
                    "How many one-versus-one binary classifiers are required for "
                    "a problem with 10 classes?"
                ),

                "options": [
                    "10",
                    "20",
                    "45",
                    "100",
                ],

                "correct": 2,

                "explanation": (
                    "OvO requires N × (N - 1) / 2 classifiers. For N = 10, this "
                    "is 10 × 9 / 2 = 45."
                ),
            },

            {
                "id": "M01.L03.Q08",

                "section_id": "error-analysis",

                "question": (
                    "What is a primary purpose of multiclass confusion-matrix "
                    "analysis?"
                ),

                "options": [
                    "To replace the need for all validation.",
                    "To identify which specific classes are being confused so improvements can target real failure modes.",
                    "To guarantee the model is fair.",
                    "To convert a multiclass problem into regression.",
                ],

                "correct": 1,

                "explanation": (
                    "Confusion patterns reveal which classes the model mistakes "
                    "for one another, helping guide data collection, feature "
                    "engineering, preprocessing, or model changes."
                ),
            },

            {
                "id": "M01.L03.Q09",

                "section_id": "multilabel",

                "type": "open",

                "question": (
                    "Explain the difference between multiclass and multilabel "
                    "classification, and give one example of each."
                ),
            },

            {
                "id": "M01.L03.Q10",

                "section_id": "multioutput",

                "type": "open",

                "question": (
                    "Why can MNIST image denoising be framed as a multioutput "
                    "problem? Explain what the inputs and outputs represent."
                ),
            },
        ],

        "passing_score": 70,
    },
}
