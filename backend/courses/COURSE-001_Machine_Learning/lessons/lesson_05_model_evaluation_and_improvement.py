"""M05.L01 — Model Evaluation and Improvement.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-001, Chapter 5, pages not provided in extracted source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M05.L01"

MODULE_ORDER = 5

MODULE_TITLE = "Model Evaluation and Improvement"

MODULE_DESCRIPTION = (
    "Learn how to evaluate generalization reliably, use cross-validation, tune "
    "hyperparameters without leaking test information, and choose evaluation "
    "metrics that match the real objective of a supervised learning problem."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Not provided in extracted source text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Model Evaluation and Improvement",

    "slug": "ml-foundations-m05-l01",

    "description": (
        "Build a reliable model-evaluation workflow using cross-validation, "
        "validation sets, grid search, confusion matrices, precision, recall, "
        "F1, precision-recall curves, ROC-AUC, and task-appropriate scoring."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "machine-learning",
        "model-evaluation",
        "generalization",
        "cross-validation",
        "grid-search",
        "hyperparameter-tuning",
        "classification-metrics",
        "confusion-matrix",
        "precision",
        "recall",
        "f1-score",
        "roc-auc",
        "imbalanced-data",
        "module-05",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Model Evaluation and Improvement",

        "content": (
            "# Model Evaluation and Improvement\n"
            "\n"
            "> **Course:** Machine Learning Foundations  \n"
            "> **Lesson:** M05.L01  \n"
            "> **Module:** Model Evaluation and Improvement  \n"
            "> **Source alignment:** BOOK-001, Chapter 5. The extracted source "
            "text does not provide page numbers. This lesson is an "
            "instructor-authored curriculum adaptation rather than a "
            "reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Learning outcomes
            # ----------------------------------------------------------------

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why model evaluation is about performance on unseen data.\n"
            "- Use k-fold cross-validation to obtain a more stable estimate of generalization.\n"
            "- Distinguish standard, stratified, group-aware, leave-one-out, and shuffle-split validation strategies.\n"
            "- Explain why test data must not be used to choose hyperparameters.\n"
            "- Use a validation set or GridSearchCV for model selection.\n"
            "- Interpret a binary confusion matrix using TP, TN, FP, and FN.\n"
            "- Compute and interpret precision, recall, and F1 score.\n"
            "- Explain why accuracy can be misleading on imbalanced datasets.\n"
            "- Interpret precision-recall curves and ROC-AUC at a conceptual level.\n"
            "- Select evaluation metrics that better reflect the real objective of a classification or regression problem.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Evaluation is really about generalization\n"
            "\n"
            "A machine learning model is useful because we want it to work on "
            "new data, not because it memorizes the data it was trained on.\n"
            "\n"
            "A basic supervised-learning workflow is:\n"
            "\n"
            "```text\n"
            "full dataset\n"
            "    |\n"
            "    +--> training set --> fit the model\n"
            "    |\n"
            "    `--> test set -----> evaluate on unseen data\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, random_state=0\n"
            ")\n"
            "\n"
            "model = LogisticRegression()\n"
            "model.fit(X_train, y_train)\n"
            "\n"
            "test_score = model.score(X_test, y_test)\n"
            "```\n"
            "\n"
            "The important question is not:\n"
            "\n"
            "> How well does the model reproduce examples it has already seen?\n"
            "\n"
            "It is:\n"
            "\n"
            "> How well will the model perform on new observations drawn from "
            "the problem we care about?\n"
            "\n"
            "A single train/test split is a useful starting point, but its result "
            "can depend heavily on which observations happen to land in each set. "
            "This motivates cross-validation.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Cross-validation\n"
            "\n"
            "Cross-validation evaluates the same learning algorithm on several "
            "different train/test splits instead of relying on only one split.\n"
            "\n"
            "### Five-fold cross-validation\n"
            "\n"
            "In five-fold cross-validation, the dataset is divided into five "
            "approximately equal parts called folds.\n"
            "\n"
            "```text\n"
            "Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5\n"
            "```\n"
            "\n"
            "The algorithm is trained five times:\n"
            "\n"
            "```text\n"
            "Run 1: test = Fold 1, train = Folds 2-5\n"
            "Run 2: test = Fold 2, train = Folds 1,3,4,5\n"
            "Run 3: test = Fold 3, train = Folds 1,2,4,5\n"
            "Run 4: test = Fold 4, train = Folds 1,2,3,5\n"
            "Run 5: test = Fold 5, train = Folds 1-4\n"
            "```\n"
            "\n"
            "Every observation is used for testing exactly once and for training "
            "in the other runs.\n"
            "\n"
            "Instead of obtaining one score, we obtain several scores:\n"
            "\n"
            "```text\n"
            "0.97, 0.93, 0.90, 1.00, 0.97\n"
            "```\n"
            "\n"
            "The mean gives a useful summary, while the spread tells us something "
            "about how sensitive performance is to the particular training data.\n"
            "\n"
            "### scikit-learn example\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import cross_val_score\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "\n"
            "model = LogisticRegression()\n"
            "\n"
            "scores = cross_val_score(model, X, y, cv=5)\n"
            "\n"
            "print(scores)\n"
            "print(scores.mean())\n"
            "```\n"
            "\n"
            "The chapter's iris example produces five scores and then averages "
            "them to estimate typical generalization performance.\n"
            "\n"
            "### Why cross-validation is useful\n"
            "\n"
            "A single random split can be unusually easy or unusually difficult. "
            "Cross-validation reduces our dependence on one lucky or unlucky split.\n"
            "\n"
            "It also uses the available data efficiently. With five folds, each "
            "model is trained on about 80% of the data. With ten folds, each model "
            "is trained on about 90%.\n"
            "\n"
            "The trade-off is computational cost. Five-fold cross-validation "
            "requires training roughly five models instead of one; ten-fold "
            "cross-validation requires roughly ten.\n"
            "\n"
            "### What cross-validation does not do\n"
            "\n"
            "Cross-validation is an evaluation procedure. Calling "
            "`cross_val_score` does not give you one final model ready for future "
            "predictions. It internally trains multiple models in order to "
            "estimate how the algorithm generalizes.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Choosing the right cross-validation strategy\n"
            "\n"
            "The way we create folds matters. A splitting strategy should reflect "
            "the structure of the real prediction problem.\n"
            "\n"
            "### Stratified k-fold for classification\n"
            "\n"
            "Suppose a classification dataset contains:\n"
            "\n"
            "```text\n"
            "90% class A\n"
            "10% class B\n"
            "```\n"
            "\n"
            "With careless splitting, one fold might contain almost no examples "
            "of class B. That fold would provide a poor evaluation of the "
            "classifier's ability to recognize the minority class.\n"
            "\n"
            "Stratified k-fold tries to preserve approximately the same class "
            "proportions in every fold as in the full dataset.\n"
            "\n"
            "This is why stratified cross-validation is usually preferred for "
            "classification.\n"
            "\n"
            "### Standard k-fold\n"
            "\n"
            "Standard k-fold simply divides the samples into folds. It is commonly "
            "used for regression, where there are no discrete class proportions "
            "to preserve in the same way.\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import KFold, cross_val_score\n"
            "\n"
            "kfold = KFold(n_splits=5, shuffle=True, random_state=0)\n"
            "scores = cross_val_score(model, X, y, cv=kfold)\n"
            "```\n"
            "\n"
            "Shuffling can be important when the dataset has an ordering that "
            "would otherwise create unrepresentative folds.\n"
            "\n"
            "### Leave-one-out cross-validation\n"
            "\n"
            "Leave-one-out can be viewed as k-fold cross-validation where every "
            "fold contains exactly one sample.\n"
            "\n"
            "If the dataset has 150 observations, the model is trained 150 times.\n"
            "\n"
            "This can be useful on small datasets but becomes expensive quickly.\n"
            "\n"
            "### Shuffle-split\n"
            "\n"
            "Shuffle-split repeatedly creates random, disjoint training and test "
            "subsets. It lets you control the number of repetitions separately "
            "from the sizes of the training and test sets.\n"
            "\n"
            "This can be useful when experimenting on large datasets or when you "
            "want repeated randomized splits.\n"
            "\n"
            "### Group-aware cross-validation\n"
            "\n"
            "Sometimes several rows belong to the same real-world entity.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- several medical measurements from one patient,\n"
            "- several face images from one person,\n"
            "- several speech recordings from one speaker.\n"
            "\n"
            "If rows from the same person appear in both training and test data, "
            "evaluation may become unrealistically easy.\n"
            "\n"
            "`GroupKFold` keeps each group entirely in the training side or "
            "entirely in the test side for a split.\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import GroupKFold, cross_val_score\n"
            "\n"
            "group_cv = GroupKFold(n_splits=3)\n"
            "\n"
            "scores = cross_val_score(\n"
            "    model,\n"
            "    X,\n"
            "    y,\n"
            "    groups=groups,\n"
            "    cv=group_cv,\n"
            ")\n"
            "```\n"
            "\n"
            "The key rule is simple: your validation split should represent the "
            "kind of new data the deployed model will actually face.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Hyperparameter tuning, validation data, and grid search\n"
            "\n"
            "Machine learning algorithms often have settings that must be chosen "
            "before fitting. These are commonly called hyperparameters.\n"
            "\n"
            "For an RBF-kernel SVM, two important examples are `C` and `gamma`.\n"
            "\n"
            "Grid search tries a set of possible values for each selected "
            "hyperparameter and evaluates all requested combinations.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "C values:     0.001, 0.01, 0.1, 1, 10, 100\n"
            "gamma values: 0.001, 0.01, 0.1, 1, 10, 100\n"
            "\n"
            "6 x 6 = 36 parameter combinations\n"
            "```\n"
            "\n"
            "### The dangerous approach\n"
            "\n"
            "A tempting workflow is:\n"
            "\n"
            "```text\n"
            "1. Train many parameter combinations.\n"
            "2. Evaluate every combination on the test set.\n"
            "3. Choose whichever one performs best on the test set.\n"
            "4. Report that test score as final performance.\n"
            "```\n"
            "\n"
            "This is wrong because the test set influenced model selection.\n"
            "\n"
            "Once we repeatedly inspect test performance and use it to choose "
            "settings, information from the test set has leaked into the "
            "development process. The test set is no longer an independent "
            "measure of future performance.\n"
            "\n"
            "### Training, validation, and test sets\n"
            "\n"
            "One solution is to create three roles:\n"
            "\n"
            "```text\n"
            "training set   -> fit model parameters\n"
            "validation set -> choose model/hyperparameters\n"
            "test set       -> final unbiased evaluation\n"
            "```\n"
            "\n"
            "After choosing the hyperparameters with validation data, the model "
            "can be rebuilt using the combined training and validation data and "
            "then evaluated once on the untouched test set.\n"
            "\n"
            "### Grid search with cross-validation\n"
            "\n"
            "Instead of depending on one validation split, we can evaluate every "
            "parameter combination using cross-validation on the training data.\n"
            "\n"
            "If we test 36 parameter combinations with five-fold cross-validation:\n"
            "\n"
            "```text\n"
            "36 combinations x 5 folds = 180 model fits\n"
            "```\n"
            "\n"
            "For each parameter combination, we calculate the mean validation "
            "score across the folds. The combination with the best mean score is "
            "selected.\n"
            "\n"
            "### GridSearchCV\n"
            "\n"
            "scikit-learn packages this workflow in `GridSearchCV`.\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import GridSearchCV, train_test_split\n"
            "from sklearn.svm import SVC\n"
            "\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, random_state=0\n"
            ")\n"
            "\n"
            "param_grid = {\n"
            "    'C': [0.001, 0.01, 0.1, 1, 10, 100],\n"
            "    'gamma': [0.001, 0.01, 0.1, 1, 10, 100],\n"
            "}\n"
            "\n"
            "grid = GridSearchCV(SVC(), param_grid, cv=5)\n"
            "grid.fit(X_train, y_train)\n"
            "\n"
            "print(grid.best_params_)\n"
            "print(grid.best_score_)\n"
            "print(grid.score(X_test, y_test))\n"
            "```\n"
            "\n"
            "`best_score_` is the best mean cross-validation score obtained "
            "inside the training data. It is not the final test-set score.\n"
            "\n"
            "### Inspecting the search\n"
            "\n"
            "`cv_results_` contains the scores and details for all tried parameter "
            "settings. Inspecting these results can reveal that:\n"
            "\n"
            "- one parameter matters more than another,\n"
            "- the search range is too narrow,\n"
            "- the best value sits on the edge and the grid may need expanding,\n"
            "- large parts of the grid perform similarly poorly.\n"
            "\n"
            "Changing the parameter grid based on cross-validation results is "
            "part of model development. Changing it repeatedly based on the final "
            "test set would contaminate the final evaluation.\n"
            "\n"
            "### Nested cross-validation\n"
            "\n"
            "Nested cross-validation adds an outer cross-validation loop around "
            "the model-selection process. The inner loop chooses hyperparameters; "
            "the outer loop evaluates the complete selection procedure.\n"
            "\n"
            "It produces evaluation scores rather than one final trained model, "
            "and it can be computationally expensive.\n"
            "\n"

            "{{exercise:M05.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 5
            # ----------------------------------------------------------------

            "## 5. Choose metrics based on the real goal\n"
            "\n"
            "A model metric is useful only when it reflects what matters in the "
            "application.\n"
            "\n"
            "Accuracy answers:\n"
            "\n"
            "> What fraction of predictions were correct?\n"
            "\n"
            "That can be useful, but it does not tell us whether different kinds "
            "of mistakes have different consequences.\n"
            "\n"
            "### False positives and false negatives\n"
            "\n"
            "In binary classification, we usually designate one class as the "
            "positive class.\n"
            "\n"
            "Consider a medical screening example:\n"
            "\n"
            "- **False positive:** a healthy patient is predicted positive and "
            "receives unnecessary follow-up testing.\n"
            "- **False negative:** a sick patient is predicted negative and may "
            "miss further diagnosis or treatment.\n"
            "\n"
            "Both are errors, but their consequences can be very different.\n"
            "\n"
            "The right metric should reflect which errors matter most for the "
            "problem.\n"
            "\n"
            "### Imbalanced datasets\n"
            "\n"
            "Suppose only 1% of users click an advertisement:\n"
            "\n"
            "```text\n"
            "99% no click\n"
            " 1% click\n"
            "```\n"
            "\n"
            "A trivial classifier that always predicts `no click` achieves 99% "
            "accuracy without learning how to identify clicks at all.\n"
            "\n"
            "This is why high accuracy alone can be misleading when classes are "
            "strongly imbalanced.\n"
            "\n"
            "A useful baseline is a simple dummy classifier. If a sophisticated "
            "model barely beats a trivial baseline, the apparently high accuracy "
            "may not be meaningful.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 6
            # ----------------------------------------------------------------

            "## 6. Confusion matrix, precision, recall, and F1\n"
            "\n"
            "A confusion matrix gives a more detailed view of binary "
            "classification results.\n"
            "\n"
            "```text\n"
            "                    Predicted negative   Predicted positive\n"
            "Actual negative            TN                   FP\n"
            "Actual positive            FN                   TP\n"
            "```\n"
            "\n"
            "- **TP — true positive:** positive example correctly predicted positive.\n"
            "- **TN — true negative:** negative example correctly predicted negative.\n"
            "- **FP — false positive:** negative example incorrectly predicted positive.\n"
            "- **FN — false negative:** positive example incorrectly predicted negative.\n"
            "\n"
            "### Accuracy\n"
            "\n"
            "Accuracy measures all correct predictions divided by all predictions:\n"
            "\n"
            "```text\n"
            "accuracy = (TP + TN) / (TP + TN + FP + FN)\n"
            "```\n"
            "\n"
            "### Precision\n"
            "\n"
            "Precision asks:\n"
            "\n"
            "> Of everything the model predicted as positive, how much was "
            "actually positive?\n"
            "\n"
            "```text\n"
            "precision = TP / (TP + FP)\n"
            "```\n"
            "\n"
            "High precision is especially important when false positives are "
            "costly.\n"
            "\n"
            "### Recall\n"
            "\n"
            "Recall asks:\n"
            "\n"
            "> Of all the truly positive examples, how many did the model find?\n"
            "\n"
            "```text\n"
            "recall = TP / (TP + FN)\n"
            "```\n"
            "\n"
            "Recall is also called sensitivity or true positive rate. High recall "
            "is especially important when missing a positive case is costly.\n"
            "\n"
            "### Precision-recall trade-off\n"
            "\n"
            "You can obtain perfect recall by predicting every observation as "
            "positive, but precision will usually become poor because of many "
            "false positives.\n"
            "\n"
            "You can obtain very high precision by predicting positive only when "
            "the model is extremely confident, but then many real positives may "
            "be missed and recall will fall.\n"
            "\n"
            "Neither precision nor recall tells the whole story by itself.\n"
            "\n"
            "### F1 score\n"
            "\n"
            "F1 combines precision and recall using their harmonic mean:\n"
            "\n"
            "```text\n"
            "F1 = 2 * precision * recall / (precision + recall)\n"
            "```\n"
            "\n"
            "F1 is often more informative than raw accuracy for imbalanced binary "
            "classification when both precision and recall matter.\n"
            "\n"
            "### scikit-learn report\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import confusion_matrix, classification_report\n"
            "\n"
            "pred = model.predict(X_test)\n"
            "\n"
            "print(confusion_matrix(y_test, pred))\n"
            "print(classification_report(y_test, pred))\n"
            "```\n"
            "\n"
            "`classification_report` shows precision, recall, F1, and support "
            "for each class, together with useful averages.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 7
            # ----------------------------------------------------------------

            "## 7. Decision thresholds, precision-recall curves, ROC, and AUC\n"
            "\n"
            "A classifier often produces more information than a final class "
            "label. It may produce a decision score or probability.\n"
            "\n"
            "The final prediction is created by comparing that score with a "
            "threshold.\n"
            "\n"
            "Changing the threshold changes the trade-off between different "
            "errors.\n"
            "\n"
            "### Threshold intuition\n"
            "\n"
            "If we make it easier to predict the positive class:\n"
            "\n"
            "```text\n"
            "more predicted positives\n"
            "-> usually higher recall\n"
            "-> usually more false positives\n"
            "-> often lower precision\n"
            "```\n"
            "\n"
            "If we demand stronger evidence before predicting positive:\n"
            "\n"
            "```text\n"
            "fewer predicted positives\n"
            "-> usually fewer false positives\n"
            "-> often higher precision\n"
            "-> usually lower recall\n"
            "```\n"
            "\n"
            "A threshold should be chosen using development/validation data, not "
            "by searching for the best result on the final test set.\n"
            "\n"
            "### Precision-recall curve\n"
            "\n"
            "A precision-recall curve shows the precision and recall obtained "
            "across many possible thresholds.\n"
            "\n"
            "A good curve stays toward the high-precision, high-recall region.\n"
            "\n"
            "Different models may be better in different parts of the curve. A "
            "single F1 score describes one operating point, while the full curve "
            "shows the broader trade-off.\n"
            "\n"
            "Average precision summarizes the precision-recall behavior across "
            "thresholds in one number.\n"
            "\n"
            "### ROC curve\n"
            "\n"
            "A receiver operating characteristic curve plots:\n"
            "\n"
            "```text\n"
            "true positive rate (recall)\n"
            "against\n"
            "false positive rate\n"
            "```\n"
            "\n"
            "A strong ROC curve lies near the upper-left region: high true "
            "positive rate with low false positive rate.\n"
            "\n"
            "### AUC\n"
            "\n"
            "AUC is the area under the ROC curve.\n"
            "\n"
            "The chapter highlights an important property:\n"
            "\n"
            "```text\n"
            "random ranking -> AUC around 0.5\n"
            "better ranking -> AUC closer to 1.0\n"
            "```\n"
            "\n"
            "AUC can reveal large differences between classifiers even when "
            "their default-threshold accuracy is the same. This is particularly "
            "valuable for imbalanced classification.\n"
            "\n"
            "A high AUC does not automatically mean the default classification "
            "threshold is appropriate. The operating threshold still needs to "
            "match the application.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 8
            # ----------------------------------------------------------------

            "## 8. Multiclass metrics, regression, and scoring during model selection\n"
            "\n"
            "### Multiclass classification\n"
            "\n"
            "For multiclass classification, accuracy is still the fraction of "
            "correct predictions, and a confusion matrix can show which classes "
            "are confused with one another.\n"
            "\n"
            "Precision, recall, and F1 can also be computed class by class by "
            "treating one class as positive and all remaining classes as negative.\n"
            "\n"
            "The per-class results can then be averaged.\n"
            "\n"
            "#### Macro average\n"
            "\n"
            "```text\n"
            "Compute the metric for every class.\n"
            "Average the class scores equally.\n"
            "```\n"
            "\n"
            "Macro averaging gives every class equal importance, regardless of "
            "how many samples that class contains.\n"
            "\n"
            "#### Weighted average\n"
            "\n"
            "Weighted averaging gives larger classes more influence according to "
            "their support, meaning the number of true samples in each class.\n"
            "\n"
            "#### Micro average\n"
            "\n"
            "Micro averaging first totals the true positives, false positives, "
            "and false negatives across classes and then computes the metric.\n"
            "\n"
            "The chapter's practical guidance is:\n"
            "\n"
            "- use micro averaging when each sample should contribute equally,\n"
            "- use macro averaging when each class should contribute equally.\n"
            "\n"
            "### Regression metrics\n"
            "\n"
            "For regression, the chapter notes that `R2` is often a useful "
            "default summary, while mean squared error and mean absolute error "
            "can also be appropriate when those error quantities better match "
            "the practical objective.\n"
            "\n"
            "The correct choice depends on what kind of prediction error matters "
            "for the application.\n"
            "\n"
            "### The metric used for tuning matters\n"
            "\n"
            "Model selection optimizes whatever score you ask it to optimize.\n"
            "\n"
            "If you tune hyperparameters for accuracy, you may select different "
            "settings than if you tune them for average precision or ROC-AUC.\n"
            "\n"
            "scikit-learn allows this through the `scoring` argument:\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import cross_val_score\n"
            "\n"
            "accuracy_scores = cross_val_score(\n"
            "    model, X, y, cv=5, scoring='accuracy'\n"
            ")\n"
            "\n"
            "ap_scores = cross_val_score(\n"
            "    model, X, y, cv=5, scoring='average_precision'\n"
            ")\n"
            "```\n"
            "\n"
            "You can also compute multiple metrics with `cross_validate`:\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import cross_validate\n"
            "\n"
            "results = cross_validate(\n"
            "    model,\n"
            "    X,\n"
            "    y,\n"
            "    cv=5,\n"
            "    scoring=['accuracy', 'average_precision', 'recall_macro'],\n"
            ")\n"
            "```\n"
            "\n"
            "The same idea applies to `GridSearchCV`: the scoring function "
            "determines which parameter setting is considered best.\n"
            "\n"
            "### The central model-selection workflow\n"
            "\n"
            "Put the chapter together as one sequence:\n"
            "\n"
            "```text\n"
            "1. Define the real prediction goal.\n"
            "2. Choose an evaluation metric that reflects that goal.\n"
            "3. Reserve independent test data.\n"
            "4. Use training data plus cross-validation for development.\n"
            "5. Tune hyperparameters with the chosen metric.\n"
            "6. Select the model without consulting the test result.\n"
            "7. Evaluate the finished choice on the untouched test set.\n"
            "```\n"
            "\n"

            "{{exercise:M05.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> A model with 99% accuracy must be excellent.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "On a highly imbalanced dataset, a trivial classifier may achieve "
            "very high accuracy by predicting only the majority class. Always "
            "compare accuracy with the class distribution and the costs of "
            "different errors.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> It is fine to keep trying hyperparameters on the test set because "
            "the model is never directly trained on those test rows.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The moment test performance affects which model or parameters you "
            "choose, information from the test set has entered model development. "
            "The final test score is then optimistically biased.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Cross-validation trains the final model that should be deployed.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Cross-validation is primarily an evaluation procedure. It repeatedly "
            "trains models to estimate generalization. After model selection, a "
            "final model still needs to be fitted on the appropriate development "
            "data.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> The best metric is always accuracy.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The best metric depends on the application. If false positives and "
            "false negatives have different consequences, or if classes are "
            "imbalanced, precision, recall, F1, average precision, AUC, or another "
            "metric may better represent the real objective.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Key terminology
            # ----------------------------------------------------------------

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Generalization | Performance on new data not used to fit the model |\n"
            "| Cross-validation | Repeated splitting and evaluation used to estimate generalization |\n"
            "| Fold | One partition used during k-fold cross-validation |\n"
            "| Stratification | Preserving class proportions across folds |\n"
            "| GroupKFold | Cross-validation that keeps related observations in the same group side of a split |\n"
            "| Hyperparameter | Model setting chosen before fitting, such as `C` or `gamma` |\n"
            "| Validation set | Development data used for model or hyperparameter selection |\n"
            "| Test set | Data reserved for final evaluation after model selection |\n"
            "| Grid search | Evaluating combinations of hyperparameter values |\n"
            "| Data leakage | Information from evaluation data improperly influencing model development |\n"
            "| Confusion matrix | Table counting true and predicted class combinations |\n"
            "| Precision | Fraction of predicted positives that are actually positive |\n"
            "| Recall | Fraction of actual positives that are successfully identified |\n"
            "| F1 score | Harmonic mean of precision and recall |\n"
            "| Support | Number of true examples belonging to a class |\n"
            "| ROC curve | Plot of true positive rate against false positive rate across thresholds |\n"
            "| AUC | Area under the ROC curve |\n"
            "| Macro average | Equal-weight average of per-class metric values |\n"
            "| Micro average | Metric computed from counts accumulated across classes |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why can a single train/test split give a misleading impression of performance?\n"
            "2. In five-fold cross-validation, how many times is each sample used as test data?\n"
            "3. Why is stratified cross-validation usually preferred for classification?\n"
            "4. When would GroupKFold be more appropriate than ordinary KFold?\n"
            "5. Why must the final test set remain untouched during hyperparameter tuning?\n"
            "6. What information does a confusion matrix provide that accuracy hides?\n"
            "7. When would recall matter more than precision?\n"
            "8. Why can two models have the same accuracy but very different AUC values?\n"
            "9. What is the difference between macro and micro averaging?\n"
            "10. Why can changing `scoring` in GridSearchCV change the chosen hyperparameters?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**Reliable machine learning evaluation requires two disciplines: "
            "protect truly unseen test data from model-selection decisions, and "
            "optimize a metric that actually reflects the errors and outcomes "
            "that matter for the real problem.**\n"
        ),

        "estimated_minutes": 210,

        "has_code_examples": True,

        "sections": [
            {
                "id": "generalization-evaluation",
                "title": "Evaluation is really about generalization",
                "order": 1,
            },
            {
                "id": "cross-validation",
                "title": "Cross-validation",
                "order": 2,
            },
            {
                "id": "cv-strategies",
                "title": "Choosing the right cross-validation strategy",
                "order": 3,
            },
            {
                "id": "grid-search",
                "title": "Hyperparameter tuning, validation data, and grid search",
                "order": 4,
            },
            {
                "id": "metrics-goal-imbalance",
                "title": "Choose metrics based on the real goal",
                "order": 5,
            },
            {
                "id": "confusion-precision-recall",
                "title": "Confusion matrix, precision, recall, and F1",
                "order": 6,
            },
            {
                "id": "threshold-curves",
                "title": "Decision thresholds, precision-recall curves, ROC, and AUC",
                "order": 7,
            },
            {
                "id": "multiclass-regression-scoring",
                "title": "Multiclass metrics, regression, and scoring during model selection",
                "order": 8,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M05.L01.EX01",

            "title": "Design a Leakage-Free Model Selection Workflow",

            "lesson_code": "M05.L01",

            "section_id": "grid-search",

            "placement": "after_section",

            "description": (
                "Practice separating model development from final evaluation "
                "using cross-validation and GridSearchCV."
            ),

            "instructions": (
                "1. Load a small classification dataset such as Iris.\n"
                "2. Split it once into training and test sets.\n"
                "3. Define at least two values for `C` and two values for `gamma` "
                "for an RBF SVC.\n"
                "4. Run GridSearchCV with five-fold cross-validation using only "
                "the training set.\n"
                "5. Record `best_params_` and `best_score_`.\n"
                "6. Evaluate the fitted grid search object once on the test set.\n"
                "7. Explain why repeatedly choosing parameter ranges based on "
                "the test score would make the final evaluation unreliable."
            ),

            "expected_output": (
                "A Python notebook or script containing the split, parameter grid, "
                "GridSearchCV result, final test score, and a short written "
                "explanation of why the test set must remain independent."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "cross-validation",
                "grid-search",
                "hyperparameter-tuning",
                "data-leakage",
                "model-evaluation",
            ],
        },

        {
            "id": "M05.L01.EX02",

            "title": "Choose Metrics for Different Classification Goals",

            "lesson_code": "M05.L01",

            "section_id": "multiclass-regression-scoring",

            "placement": "after_section",

            "description": (
                "Practice choosing evaluation metrics based on class imbalance "
                "and the consequences of false positives and false negatives."
            ),

            "instructions": (
                "For each scenario, choose the most informative metric or set of "
                "metrics from accuracy, precision, recall, F1, ROC-AUC, and a "
                "confusion matrix. Justify your choice.\n"
                "1. A rare medical condition where missing a real case is very costly.\n"
                "2. An expensive follow-up process where false alarms should be minimized.\n"
                "3. A 99-to-1 imbalanced binary classification problem where you want "
                "to compare ranking quality across thresholds.\n"
                "4. A ten-class classification problem where some classes are commonly "
                "confused with particular others.\n"
                "5. Explain how your chosen model-selection metric should be passed "
                "to cross-validation or GridSearchCV using the `scoring` argument."
            ),

            "expected_output": (
                "A table with one row per scenario showing the metric choice, "
                "the error type it emphasizes, and a short justification. Include "
                "one example `scoring=` value for model selection."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "classification-metrics",
                "precision-recall",
                "imbalanced-data",
                "metric-selection",
                "reasoning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M05.L01.QZ01",

        "title": "Model Evaluation and Improvement — Knowledge Check",

        "lesson_code": "M05.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M05.L01.Q01",

                "section_id": "cross-validation",

                "question": (
                    "What is the main reason to use k-fold cross-validation "
                    "instead of relying only on one train/test split?"
                ),

                "options": [
                    "It guarantees that the model will never overfit",
                    "It evaluates the algorithm across several splits and reduces dependence on one lucky or unlucky split",
                    "It automatically chooses the best features",
                    "It permanently combines all fitted models into one deployment model",
                ],

                "correct": 1,

                "explanation": (
                    "Cross-validation evaluates the learning procedure across "
                    "multiple train/test partitions, producing a more thorough "
                    "estimate of generalization than one arbitrary split."
                ),
            },

            {
                "id": "M05.L01.Q02",

                "section_id": "grid-search",

                "question": (
                    "Why should the final test set not be used to choose "
                    "hyperparameters?"
                ),

                "options": [
                    "Because test data cannot contain labels",
                    "Because hyperparameters work only on training data",
                    "Because using test performance to make model-selection decisions leaks information and biases the final evaluation",
                    "Because GridSearchCV cannot score a test set",
                ],

                "correct": 2,

                "explanation": (
                    "The test set should represent untouched future data. If its "
                    "performance affects model choice, it is no longer an "
                    "independent estimate of generalization."
                ),
            },

            {
                "id": "M05.L01.Q03",

                "section_id": "confusion-precision-recall",

                "question": (
                    "A task places very high cost on missing real positive cases. "
                    "Which metric should receive particular attention?"
                ),

                "options": [
                    "Recall",
                    "Precision only",
                    "Training accuracy",
                    "Number of model parameters",
                ],

                "correct": 0,

                "explanation": (
                    "Recall measures the fraction of actual positive examples "
                    "that the classifier successfully finds. Low recall means "
                    "many false negatives."
                ),
            },

            {
                "id": "M05.L01.Q04",

                "section_id": "threshold-curves",

                "question": (
                    "Why can ROC-AUC be more informative than accuracy on an "
                    "imbalanced binary classification problem?"
                ),

                "options": [
                    "AUC uses only the majority class",
                    "AUC always equals the F1 score",
                    "AUC removes the need for a test set",
                    "AUC evaluates ranking behavior across thresholds and is not tied to one default class threshold",
                ],

                "correct": 3,

                "explanation": (
                    "Accuracy may look high simply because the majority class is "
                    "common. ROC-AUC examines true-positive versus false-positive "
                    "behavior across thresholds and can distinguish models with "
                    "the same default-threshold accuracy."
                ),
            },

            {
                "id": "M05.L01.Q05",

                "section_id": "multiclass-regression-scoring",

                "type": "open",

                "question": (
                    "You are tuning a classifier on a highly imbalanced dataset. "
                    "Accuracy is high, but the minority class is the class you care "
                    "about most. Describe how you would change both the evaluation "
                    "metric and the model-selection workflow so that the selected "
                    "hyperparameters better reflect the real objective."
                ),
            },
        ],

        "passing_score": 70,
    },
}
