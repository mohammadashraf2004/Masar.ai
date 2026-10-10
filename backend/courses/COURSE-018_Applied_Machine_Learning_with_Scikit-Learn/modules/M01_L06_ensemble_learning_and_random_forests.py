"""M01.L06 — Ensemble Learning and Random Forests.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 6 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L06"

MODULE_ORDER = 1

MODULE_TITLE = "Ensemble Learning and Random Forests"

MODULE_DESCRIPTION = (
    "Learn how to combine predictors into stronger systems using voting, "
    "bagging, random forests, extra-trees, boosting, histogram-based gradient "
    "boosting, and stacking, with emphasis on diversity, bias/variance tradeoffs, "
    "evaluation, and practical model selection."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Ensemble Learning and Random Forests",

    "slug": "machine-learning-foundations-m01-l06",

    "description": (
        "A practical lesson on the main ensemble-learning strategies: voting, "
        "bagging and OOB evaluation, random forests and extra-trees, AdaBoost, "
        "gradient boosting, histogram-based gradient boosting, and stacking."
    ),

    "order": 6,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 4.0,

    "skill_tags": [
        "machine-learning",
        "ensemble-learning",
        "voting",
        "bagging",
        "random-forest",
        "extra-trees",
        "adaboost",
        "gradient-boosting",
        "hist-gradient-boosting",
        "stacking",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
    ],


    # =======================================================================
    # INLINE IMAGE RULES
    # =======================================================================
    #
    # Only high-value source figures are requested. Each request includes the
    # original source figure number and a stable key for later manual linking.
    #
    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Ensemble Learning and Random Forests",

        "content": (
            "# Ensemble Learning and Random Forests\n"
            "\n"
            "> **Course:** Applied Machine Learning with Scikit-Learn  \n"
            "> **Lesson:** M01.L06  \n"
            "> **Module:** Ensemble Learning and Random Forests  \n"
            "> **Source alignment:** Chapter 6, “Ensemble Learning and Random Forests,” supplied by the course author. Page numbers were not included in the supplied extract. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why combining diverse predictors can outperform a strong individual predictor.\n"
            "- Distinguish hard voting from soft voting and explain when probability calibration matters.\n"
            "- Explain bagging and pasting, including sampling with and without replacement.\n"
            "- Describe why aggregation can reduce variance and why diversity between predictors matters.\n"
            "- Use out-of-bag evaluation to estimate a bagging model’s performance.\n"
            "- Explain random patches and random subspaces.\n"
            "- Describe how random forests add randomness beyond ordinary bagged decision trees.\n"
            "- Distinguish random forests from extra-trees and interpret feature importance.\n"
            "- Explain how AdaBoost focuses progressively on hard training examples.\n"
            "- Explain gradient boosting as sequentially fitting residual errors.\n"
            "- Describe shrinkage, early stopping, stochastic gradient boosting, and histogram-based gradient boosting.\n"
            "- Explain stacking and why out-of-sample base-model predictions are required to train a blender safely.\n"
            "- Choose an ensemble method based on the dataset, model behavior, and computational constraints.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. Why ensembles work\n"
            "\n"
            "An **ensemble** is a group of predictors whose outputs are combined to produce a final prediction.\n"
            "\n"
            "The basic idea is similar to the **wisdom of the crowd**:\n"
            "\n"
            "```text\n"
            "many imperfect opinions\n"
            "        |\n"
            "aggregate them\n"
            "        |\n"
            "often obtain a better answer\n"
            "```\n"
            "\n"
            "In machine learning:\n"
            "\n"
            "```text\n"
            "model 1 prediction\n"
            "model 2 prediction\n"
            "model 3 prediction\n"
            "...\n"
            "        |\n"
            "aggregation\n"
            "        |\n"
            "ensemble prediction\n"
            "```\n"
            "\n"
            "The most important condition is not simply having many models.\n"
            "\n"
            "The models should be **useful and diverse**.\n"
            "\n"
            "If every model makes the same mistake, combining them will not help.\n"
            "\n"
            "### Weak learners can form a strong learner\n"
            "\n"
            "A **weak learner** is a model that performs only slightly better than random guessing.\n"
            "\n"
            "If many weak learners make sufficiently independent errors, their majority decision can be much stronger than any individual learner.\n"
            "\n"
            "The chapter uses a biased-coin analogy:\n"
            "\n"
            "```text\n"
            "single event:\n"
            "51% chance of heads\n"
            "\n"
            "many independent tosses:\n"
            "the overall proportion tends toward 51%\n"
            "```\n"
            "\n"
            "Similarly, a large collection of classifiers that are each slightly better than random can produce a much more reliable majority vote.\n"
            "\n"
            "But independence matters.\n"
            "\n"
            "Models trained:\n"
            "\n"
            "- with the same algorithm,\n"
            "- on the same data,\n"
            "- with the same assumptions,\n"
            "\n"
            "may make correlated errors.\n"
            "\n"
            "That is why ensemble design often tries to increase diversity by:\n"
            "\n"
            "- using different algorithms,\n"
            "- changing hyperparameters,\n"
            "- training on different samples,\n"
            "- training on different feature subsets.\n"
            "\n"
            "### Ensembles have costs\n"
            "\n"
            "Ensembles often improve predictive performance, but they may also require:\n"
            "\n"
            "- more training compute,\n"
            "- more inference compute,\n"
            "- more memory,\n"
            "- more deployment complexity,\n"
            "- more difficult debugging,\n"
            "- less interpretability.\n"
            "\n"
            "So the question is not:\n"
            "\n"
            "> “Are ensembles powerful?”\n"
            "\n"
            "They are.\n"
            "\n"
            "The practical question is:\n"
            "\n"
            "> **“Is the performance gain worth the extra operational cost?”**\n"
            "\n"
            "---\n"
            "\n"
            "## 2. Voting classifiers: combine different models\n"
            "\n"
            "Suppose you train several classifiers:\n"
            "\n"
            "```text\n"
            "Logistic Regression\n"
            "SVM\n"
            "Random Forest\n"
            "k-NN\n"
            "```\n"
            "\n"
            "Each model sees the same problem differently.\n"
            "\n"
            "Their errors may therefore differ.\n"
            "\n"
            "### Hard voting\n"
            "\n"
            "A **hard voting classifier** chooses the class receiving the most individual model votes.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Logistic Regression -> class 1\n"
            "Random Forest       -> class 1\n"
            "SVM                 -> class 0\n"
            "\n"
            "majority vote       -> class 1\n"
            "```\n"
            "\n"
            "{{image:hard-voting-ensemble}}\n"
            "\n"
            "Scikit-Learn provides `VotingClassifier`:\n"
            "\n"
            "```python\n"
            "from sklearn.datasets import make_moons\n"
            "from sklearn.ensemble import RandomForestClassifier, VotingClassifier\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.svm import SVC\n"
            "\n"
            "X, y = make_moons(\n"
            "    n_samples=500,\n"
            "    noise=0.30,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X,\n"
            "    y,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "voting_clf = VotingClassifier(\n"
            "    estimators=[\n"
            "        (\"lr\", LogisticRegression(random_state=42)),\n"
            "        (\"rf\", RandomForestClassifier(random_state=42)),\n"
            "        (\"svc\", SVC(random_state=42)),\n"
            "    ]\n"
            ")\n"
            "\n"
            "voting_clf.fit(\n"
            "    X_train,\n"
            "    y_train,\n"
            ")\n"
            "```\n"
            "\n"
            "In the source example, the individual models reach approximately:\n"
            "\n"
            "```text\n"
            "Logistic Regression -> 86.4%\n"
            "Random Forest       -> 89.6%\n"
            "SVC                 -> 89.6%\n"
            "```\n"
            "\n"
            "while hard voting reaches about:\n"
            "\n"
            "```text\n"
            "91.2%\n"
            "```\n"
            "\n"
            "The ensemble is better than every individual member.\n"
            "\n"
            "### Soft voting\n"
            "\n"
            "If all classifiers estimate class probabilities, the ensemble can average those probabilities instead of counting labels.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Model A:\n"
            "P(class 1) = 0.90\n"
            "\n"
            "Model B:\n"
            "P(class 1) = 0.55\n"
            "\n"
            "Model C:\n"
            "P(class 1) = 0.60\n"
            "```\n"
            "\n"
            "Soft voting considers the confidence values, not just three equal votes.\n"
            "\n"
            "With Scikit-Learn:\n"
            "\n"
            "```python\n"
            "voting_clf.voting = \"soft\"\n"
            "\n"
            "voting_clf.named_estimators[\n"
            "    \"svc\"\n"
            "].probability = True\n"
            "\n"
            "voting_clf.fit(\n"
            "    X_train,\n"
            "    y_train,\n"
            ")\n"
            "\n"
            "print(\n"
            "    voting_clf.score(\n"
            "        X_test,\n"
            "        y_test,\n"
            "    )\n"
            ")\n"
            "```\n"
            "\n"
            "The source reaches approximately:\n"
            "\n"
            "```text\n"
            "92%\n"
            "```\n"
            "\n"
            "### When soft voting is meaningful\n"
            "\n"
            "Soft voting works best when model probabilities are reasonably **calibrated**.\n"
            "\n"
            "If one model routinely says:\n"
            "\n"
            "```text\n"
            "99% confidence\n"
            "```\n"
            "\n"
            "when it is correct only 70% of the time, its probability estimates can dominate the average unfairly.\n"
            "\n"
            "Probability calibration helps ensure that confidence scores better match observed frequencies.\n"
            "\n"
            "### Hard versus soft voting\n"
            "\n"
            "Use the mental model:\n"
            "\n"
            "```text\n"
            "hard voting:\n"
            "\"What class did each model choose?\"\n"
            "\n"
            "soft voting:\n"
            "\"How much probability did each model assign to each class?\"\n"
            "```\n"
            "\n"
            "Soft voting often performs better when good probability estimates are available.\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Bagging and pasting: diversify the data instead of the algorithm\n"
            "\n"
            "Voting used different algorithms.\n"
            "\n"
            "Another way to build diversity is:\n"
            "\n"
            "> **Use the same learning algorithm many times, but train each copy on a different random subset of the data.**\n"
            "\n"
            "This produces two closely related methods.\n"
            "\n"
            "### Bagging\n"
            "\n"
            "**Bagging** means **bootstrap aggregating**.\n"
            "\n"
            "Each predictor receives a random sample of the training set **with replacement**.\n"
            "\n"
            "With replacement means the same training instance can appear more than once inside one predictor’s sample.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "original IDs:\n"
            "1 2 3 4 5\n"
            "\n"
            "possible bagging sample:\n"
            "2 2 5 1 5\n"
            "```\n"
            "\n"
            "### Pasting\n"
            "\n"
            "**Pasting** samples **without replacement**.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "original IDs:\n"
            "1 2 3 4 5\n"
            "\n"
            "possible pasting sample:\n"
            "2 5 1\n"
            "```\n"
            "\n"
            "No training instance is repeated within that predictor’s sample.\n"
            "\n"
            "{{image:bagging-pasting-sampling}}\n"
            "\n"
            "### Aggregate predictions\n"
            "\n"
            "After training:\n"
            "\n"
            "```text\n"
            "classification -> majority vote / class probability aggregation\n"
            "regression     -> average predictions\n"
            "```\n"
            "\n"
            "Each individual predictor may have somewhat higher bias because it trains on only part of the available information.\n"
            "\n"
            "But aggregation can reduce variance.\n"
            "\n"
            "This is especially valuable for models such as deep decision trees, which naturally have:\n"
            "\n"
            "```text\n"
            "low bias\n"
            "high variance\n"
            "```\n"
            "\n"
            "### Why averaging reduces variance\n"
            "\n"
            "Imagine two independent regressors.\n"
            "\n"
            "Their individual predictions fluctuate around the true answer.\n"
            "\n"
            "If their errors are not perfectly correlated, averaging can make the positive and negative deviations partially cancel.\n"
            "\n"
            "That is the statistical reason ensembles often produce smoother, more stable predictions.\n"
            "\n"
            "### Bagging versus pasting\n"
            "\n"
            "Bagging introduces extra randomness because repeated samples are allowed.\n"
            "\n"
            "That can increase predictor diversity and reduce correlation.\n"
            "\n"
            "In many practical cases:\n"
            "\n"
            "```text\n"
            "bagging -> slightly more bias\n"
            "          but lower variance\n"
            "```\n"
            "\n"
            "which can improve overall generalization.\n"
            "\n"
            "Pasting can be more computationally efficient because it avoids duplicate examples inside a predictor’s sample.\n"
            "\n"
            "### Parallelization\n"
            "\n"
            "Bagging and pasting are naturally parallel.\n"
            "\n"
            "Each predictor can usually be trained independently:\n"
            "\n"
            "```text\n"
            "CPU 1 -> predictor 1\n"
            "CPU 2 -> predictor 2\n"
            "CPU 3 -> predictor 3\n"
            "...\n"
            "```\n"
            "\n"
            "Predictions can also be parallelized.\n"
            "\n"
            "This is a major scalability advantage compared with sequential boosting methods.\n"
            "\n"
            "### Scikit-Learn example\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import BaggingClassifier\n"
            "from sklearn.tree import DecisionTreeClassifier\n"
            "\n"
            "bag_clf = BaggingClassifier(\n"
            "    DecisionTreeClassifier(),\n"
            "    n_estimators=500,\n"
            "    max_samples=100,\n"
            "    n_jobs=-1,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "bag_clf.fit(\n"
            "    X_train,\n"
            "    y_train,\n"
            ")\n"
            "```\n"
            "\n"
            "To use pasting instead:\n"
            "\n"
            "```python\n"
            "BaggingClassifier(\n"
            "    DecisionTreeClassifier(),\n"
            "    bootstrap=False,\n"
            ")\n"
            "```\n"
            "\n"
            "### Why bagging can improve a tree\n"
            "\n"
            "A single decision tree may produce an irregular decision boundary because it follows small training-set details.\n"
            "\n"
            "A bagging ensemble averages many differently trained trees.\n"
            "\n"
            "{{image:single-tree-vs-bagging}}\n"
            "\n"
            "This is an important general pattern:\n"
            "\n"
            "> **The individual members can be unstable while the ensemble is stable.**\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Out-of-bag evaluation and feature sampling\n"
            "\n"
            "Bagging creates a useful side effect.\n"
            "\n"
            "Because each predictor samples training instances with replacement, some instances are not selected for that predictor at all.\n"
            "\n"
            "These are called **out-of-bag (OOB) instances**.\n"
            "\n"
            "### Why about 37% are OOB\n"
            "\n"
            "When the bootstrap sample contains the same number of draws as the training-set size, only about:\n"
            "\n"
            "```text\n"
            "63%\n"
            "```\n"
            "\n"
            "of unique training instances are included on average.\n"
            "\n"
            "So approximately:\n"
            "\n"
            "```text\n"
            "37%\n"
            "```\n"
            "\n"
            "are left out for that predictor.\n"
            "\n"
            "The exact OOB examples differ from one predictor to another.\n"
            "\n"
            "### OOB evaluation\n"
            "\n"
            "For a particular training instance:\n"
            "\n"
            "```text\n"
            "predictor A -> may have trained on it\n"
            "predictor B -> may not have trained on it\n"
            "predictor C -> may not have trained on it\n"
            "...\n"
            "```\n"
            "\n"
            "The predictors that did **not** train on that example can make an out-of-sample prediction for it.\n"
            "\n"
            "Across many predictors, we can aggregate these OOB predictions and estimate ensemble performance without creating a separate validation set.\n"
            "\n"
            "```python\n"
            "bag_clf = BaggingClassifier(\n"
            "    DecisionTreeClassifier(),\n"
            "    n_estimators=500,\n"
            "    oob_score=True,\n"
            "    n_jobs=-1,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "bag_clf.fit(\n"
            "    X_train,\n"
            "    y_train,\n"
            ")\n"
            "\n"
            "print(\n"
            "    bag_clf.oob_score_\n"
            ")\n"
            "```\n"
            "\n"
            "The source obtains:\n"
            "\n"
            "```text\n"
            "OOB accuracy ≈ 89.6%\n"
            "test accuracy ≈ 92.0%\n"
            "```\n"
            "\n"
            "OOB evaluation is not magical or always exact, but it provides a useful built-in estimate.\n"
            "\n"
            "### OOB class probabilities\n"
            "\n"
            "If the base estimator supports probabilities:\n"
            "\n"
            "```python\n"
            "bag_clf.oob_decision_function_\n"
            "```\n"
            "\n"
            "contains OOB class-probability estimates for training instances.\n"
            "\n"
            "### Random patches\n"
            "\n"
            "Bagging can also sample **features**.\n"
            "\n"
            "If you randomly sample both:\n"
            "\n"
            "```text\n"
            "training instances\n"
            "+\n"
            "input features\n"
            "```\n"
            "\n"
            "the method is called **random patches**.\n"
            "\n"
            "### Random subspaces\n"
            "\n"
            "If you keep all training instances but randomly sample features:\n"
            "\n"
            "```text\n"
            "all rows\n"
            "+\n"
            "random subset of columns\n"
            "```\n"
            "\n"
            "this is called the **random subspaces** method.\n"
            "\n"
            "Feature sampling is useful for high-dimensional data because it can:\n"
            "\n"
            "- reduce computation,\n"
            "- create more diverse predictors,\n"
            "- reduce correlation among predictors,\n"
            "- trade a little more bias for lower variance.\n"
            "\n"
            "{{exercise:M01.L06.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Random forests, extra-trees, and feature importance\n"
            "\n"
            "A **random forest** is an ensemble of decision trees, usually trained using bagging.\n"
            "\n"
            "However, it introduces another important source of randomness.\n"
            "\n"
            "### Random feature selection at each split\n"
            "\n"
            "A regular decision tree considers all available features when looking for the best split.\n"
            "\n"
            "A random forest considers only a random subset of features at each node.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "tree 1:\n"
            "random data sample\n"
            "+\n"
            "random candidate features at every split\n"
            "\n"
            "tree 2:\n"
            "different random data sample\n"
            "+\n"
            "different random candidate features\n"
            "\n"
            "...\n"
            "```\n"
            "\n"
            "This makes the trees less similar to one another.\n"
            "\n"
            "Again, the trade-off is:\n"
            "\n"
            "```text\n"
            "more randomness\n"
            "-> slightly higher bias\n"
            "-> lower correlation\n"
            "-> lower ensemble variance\n"
            "```\n"
            "\n"
            "### Scikit-Learn random forest\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "\n"
            "rnd_clf = RandomForestClassifier(\n"
            "    n_estimators=500,\n"
            "    max_leaf_nodes=16,\n"
            "    n_jobs=-1,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "rnd_clf.fit(\n"
            "    X_train,\n"
            "    y_train,\n"
            ")\n"
            "\n"
            "y_pred_rf = rnd_clf.predict(\n"
            "    X_test\n"
            ")\n"
            "```\n"
            "\n"
            "A random forest exposes:\n"
            "\n"
            "- tree-growth hyperparameters,\n"
            "- ensemble hyperparameters.\n"
            "\n"
            "This lets you control both:\n"
            "\n"
            "```text\n"
            "how each tree learns\n"
            "and\n"
            "how the forest is constructed\n"
            "```\n"
            "\n"
            "### Extra-trees\n"
            "\n"
            "An **extremely randomized trees** ensemble, or **extra-trees**, adds still more randomness.\n"
            "\n"
            "Random forests:\n"
            "\n"
            "```text\n"
            "sample candidate features\n"
            "then search for the best split threshold\n"
            "```\n"
            "\n"
            "Extra-trees:\n"
            "\n"
            "```text\n"
            "sample candidate features\n"
            "and use random split thresholds\n"
            "```\n"
            "\n"
            "This makes training faster because searching for the optimal threshold is expensive.\n"
            "\n"
            "It may also reduce variance further.\n"
            "\n"
            "Trade-off:\n"
            "\n"
            "```text\n"
            "extra randomness\n"
            "-> potentially more bias\n"
            "-> potentially less variance\n"
            "```\n"
            "\n"
            "Extra-trees may be especially useful when:\n"
            "\n"
            "- the dataset is noisy,\n"
            "- dimensionality is high,\n"
            "- random forests are overfitting,\n"
            "- training speed matters.\n"
            "\n"
            "Scikit-Learn provides:\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import ExtraTreesClassifier\n"
            "```\n"
            "\n"
            "### Feature importance\n"
            "\n"
            "Random forests can estimate how important each feature is.\n"
            "\n"
            "The basic idea is to measure how much tree splits using a feature reduce impurity across the forest.\n"
            "\n"
            "Scikit-Learn stores normalized values in:\n"
            "\n"
            "```python\n"
            "rnd_clf.feature_importances_\n"
            "```\n"
            "\n"
            "For the Iris example in the chapter, petal length and width receive much higher importance than the sepal measurements.\n"
            "\n"
            "Feature importance can help with:\n"
            "\n"
            "- quick interpretation,\n"
            "- feature selection,\n"
            "- discovering which inputs dominate predictions.\n"
            "\n"
            "The chapter also demonstrates pixel importance on MNIST.\n"
            "\n"
            "{{image:random-forest-mnist-feature-importance}}\n"
            "\n"
            "### Important caution\n"
            "\n"
            "Feature importance is evidence from a model, not absolute truth about the world.\n"
            "\n"
            "A feature may appear unimportant because:\n"
            "\n"
            "- another correlated feature carries similar information,\n"
            "- the model cannot exploit it well,\n"
            "- preprocessing changed its representation.\n"
            "\n"
            "Use importance as a diagnostic tool, not as unquestionable causal proof.\n"
            "\n"
            "---\n"
            "\n"
            "## 6. AdaBoost: make each learner focus on previous mistakes\n"
            "\n"
            "**Boosting** combines weak learners sequentially.\n"
            "\n"
            "Unlike bagging:\n"
            "\n"
            "```text\n"
            "bagging:\n"
            "models can train independently\n"
            "\n"
            "boosting:\n"
            "model 2 depends on model 1\n"
            "model 3 depends on model 2\n"
            "...\n"
            "```\n"
            "\n"
            "This means boosting cannot be parallelized in the same way.\n"
            "\n"
            "### AdaBoost intuition\n"
            "\n"
            "**AdaBoost** begins by giving all training examples equal importance.\n"
            "\n"
            "Then:\n"
            "\n"
            "1. train a weak predictor,\n"
            "2. find which training examples it misclassified,\n"
            "3. increase the weights of those difficult examples,\n"
            "4. train the next predictor using the new weights,\n"
            "5. repeat.\n"
            "\n"
            "{{image:adaboost-sequential-reweighting}}\n"
            "\n"
            "The sequence is:\n"
            "\n"
            "```text\n"
            "initial equal weights\n"
            "        |\n"
            "predictor 1\n"
            "        |\n"
            "increase weight of mistakes\n"
            "        |\n"
            "predictor 2\n"
            "        |\n"
            "increase weight of remaining mistakes\n"
            "        |\n"
            "predictor 3\n"
            "        |\n"
            "...\n"
            "```\n"
            "\n"
            "### Predictor weights\n"
            "\n"
            "AdaBoost also gives each predictor its own vote strength.\n"
            "\n"
            "A more accurate predictor receives a larger weight in the final ensemble.\n"
            "\n"
            "A predictor near random guessing gets very little influence.\n"
            "\n"
            "### Learning rate\n"
            "\n"
            "The **learning rate** controls how aggressively the algorithm updates instance weights and adds new predictors.\n"
            "\n"
            "A smaller learning rate means each stage makes a smaller correction.\n"
            "\n"
            "As with other iterative methods:\n"
            "\n"
            "```text\n"
            "large learning rate:\n"
            "faster / more aggressive changes\n"
            "\n"
            "small learning rate:\n"
            "slower / more conservative changes\n"
            "```\n"
            "\n"
            "### Decision stumps\n"
            "\n"
            "A common AdaBoost base learner is a **decision stump**:\n"
            "\n"
            "```text\n"
            "decision tree with max_depth = 1\n"
            "```\n"
            "\n"
            "This is a very weak learner.\n"
            "\n"
            "Scikit-Learn example:\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import AdaBoostClassifier\n"
            "from sklearn.tree import DecisionTreeClassifier\n"
            "\n"
            "ada_clf = AdaBoostClassifier(\n"
            "    DecisionTreeClassifier(\n"
            "        max_depth=1\n"
            "    ),\n"
            "    n_estimators=30,\n"
            "    learning_rate=0.5,\n"
            "    random_state=42,\n"
            "    algorithm=\"SAMME\",\n"
            ")\n"
            "\n"
            "ada_clf.fit(\n"
            "    X_train,\n"
            "    y_train,\n"
            ")\n"
            "```\n"
            "\n"
            "### If AdaBoost overfits\n"
            "\n"
            "Possible remedies include:\n"
            "\n"
            "- reduce the number of estimators,\n"
            "- regularize the base estimator more strongly.\n"
            "\n"
            "The broader lesson is that boosting is powerful because later learners actively correct earlier weaknesses—but that same power can overfit.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Gradient boosting: learn the residual errors\n"
            "\n"
            "**Gradient boosting** also builds predictors sequentially.\n"
            "\n"
            "But instead of changing training-instance weights like AdaBoost, it trains each new predictor to model the **residual errors** of the current ensemble.\n"
            "\n"
            "Suppose the first model predicts:\n"
            "\n"
            "```text\n"
            "ŷ1\n"
            "```\n"
            "\n"
            "Then residuals are:\n"
            "\n"
            "```text\n"
            "residual = y - ŷ1\n"
            "```\n"
            "\n"
            "The second model tries to predict those residuals.\n"
            "\n"
            "Then:\n"
            "\n"
            "```text\n"
            "ensemble prediction\n"
            "=\n"
            "first prediction\n"
            "+\n"
            "second correction\n"
            "```\n"
            "\n"
            "The third model learns what is still wrong after the first two, and so on.\n"
            "\n"
            "### Build it manually\n"
            "\n"
            "The source demonstrates a simple regression example.\n"
            "\n"
            "First tree:\n"
            "\n"
            "```python\n"
            "from sklearn.tree import DecisionTreeRegressor\n"
            "\n"
            "tree_reg1 = DecisionTreeRegressor(\n"
            "    max_depth=2,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "tree_reg1.fit(\n"
            "    X,\n"
            "    y,\n"
            ")\n"
            "```\n"
            "\n"
            "Residual targets:\n"
            "\n"
            "```python\n"
            "y2 = y - tree_reg1.predict(X)\n"
            "```\n"
            "\n"
            "Second tree:\n"
            "\n"
            "```python\n"
            "tree_reg2 = DecisionTreeRegressor(\n"
            "    max_depth=2,\n"
            "    random_state=43,\n"
            ")\n"
            "\n"
            "tree_reg2.fit(\n"
            "    X,\n"
            "    y2,\n"
            ")\n"
            "```\n"
            "\n"
            "Then:\n"
            "\n"
            "```python\n"
            "y3 = y2 - tree_reg2.predict(X)\n"
            "```\n"
            "\n"
            "Train a third tree on what remains.\n"
            "\n"
            "The final prediction is the sum:\n"
            "\n"
            "```python\n"
            "prediction = (\n"
            "    tree_reg1.predict(X_new)\n"
            "    + tree_reg2.predict(X_new)\n"
            "    + tree_reg3.predict(X_new)\n"
            ")\n"
            "```\n"
            "\n"
            "{{image:gradient-boosting-residual-correction}}\n"
            "\n"
            "### Scikit-Learn implementation\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import GradientBoostingRegressor\n"
            "\n"
            "gbrt = GradientBoostingRegressor(\n"
            "    max_depth=2,\n"
            "    n_estimators=3,\n"
            "    learning_rate=1.0,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "gbrt.fit(\n"
            "    X,\n"
            "    y,\n"
            ")\n"
            "```\n"
            "\n"
            "### Learning rate and shrinkage\n"
            "\n"
            "The `learning_rate` scales how much each new tree contributes.\n"
            "\n"
            "A smaller value means:\n"
            "\n"
            "```text\n"
            "each tree makes a smaller correction\n"
            "```\n"
            "\n"
            "so more trees are usually needed.\n"
            "\n"
            "This is called **shrinkage**.\n"
            "\n"
            "It often improves generalization.\n"
            "\n"
            "But there is a balance.\n"
            "\n"
            "```text\n"
            "too few trees\n"
            "-> underfitting\n"
            "\n"
            "appropriate number\n"
            "-> good fit\n"
            "\n"
            "too many trees\n"
            "-> possible overfitting\n"
            "```\n"
            "\n"
            "{{image:gbrt-number-of-predictors}}\n"
            "\n"
            "### Early stopping\n"
            "\n"
            "Instead of guessing the ideal number of trees, monitor validation performance and stop when new trees no longer improve it.\n"
            "\n"
            "```python\n"
            "gbrt_best = GradientBoostingRegressor(\n"
            "    max_depth=2,\n"
            "    learning_rate=0.05,\n"
            "    n_estimators=500,\n"
            "    n_iter_no_change=10,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "gbrt_best.fit(\n"
            "    X,\n"
            "    y,\n"
            ")\n"
            "```\n"
            "\n"
            "The source stops after only:\n"
            "\n"
            "```text\n"
            "53 estimators\n"
            "```\n"
            "\n"
            "even though the maximum was set to 500.\n"
            "\n"
            "This is **early stopping**.\n"
            "\n"
            "The model has permission to keep learning but stops once extra capacity stops helping validation performance.\n"
            "\n"
            "### Stochastic gradient boosting\n"
            "\n"
            "`GradientBoostingRegressor` can train each tree on a random fraction of the training instances:\n"
            "\n"
            "```python\n"
            "subsample=0.25\n"
            "```\n"
            "\n"
            "This creates **stochastic gradient boosting**.\n"
            "\n"
            "It:\n"
            "\n"
            "- speeds training,\n"
            "- increases randomness,\n"
            "- increases bias,\n"
            "- may reduce variance.\n"
            "\n"
            "Again, ensemble design repeatedly uses the same principle:\n"
            "\n"
            "> **Add useful randomness to reduce correlation and overfitting.**\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Histogram-based gradient boosting\n"
            "\n"
            "Traditional gradient boosting can be expensive on large datasets because every tree must evaluate many possible split thresholds.\n"
            "\n"
            "**Histogram-based gradient boosting (HGB)** speeds this up by **binning** continuous feature values.\n"
            "\n"
            "Instead of treating a feature as thousands of distinct floating-point values:\n"
            "\n"
            "```text\n"
            "2.134\n"
            "2.141\n"
            "2.149\n"
            "2.153\n"
            "...\n"
            "```\n"
            "\n"
            "HGB maps values into a limited number of integer bins:\n"
            "\n"
            "```text\n"
            "bin 0\n"
            "bin 1\n"
            "bin 2\n"
            "...\n"
            "```\n"
            "\n"
            "This dramatically reduces the number of thresholds the training algorithm must evaluate.\n"
            "\n"
            "### Why HGB can be much faster\n"
            "\n"
            "The chapter contrasts the computational behavior of standard GBRT and HGB.\n"
            "\n"
            "The practical message is:\n"
            "\n"
            "```text\n"
            "fewer candidate thresholds\n"
            "+\n"
            "integer-based representation\n"
            "+\n"
            "no repeated full sorting\n"
            "=\n"
            "much faster training on large datasets\n"
            "```\n"
            "\n"
            "### Binning is also a form of regularization\n"
            "\n"
            "Binning loses some numerical precision.\n"
            "\n"
            "That can:\n"
            "\n"
            "```text\n"
            "reduce overfitting\n"
            "```\n"
            "\n"
            "or, if too much information is lost:\n"
            "\n"
            "```text\n"
            "cause underfitting\n"
            "```\n"
            "\n"
            "So speed is not the only consequence.\n"
            "\n"
            "### Convenient handling of real tabular data\n"
            "\n"
            "Scikit-Learn provides:\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import (\n"
            "    HistGradientBoostingClassifier,\n"
            "    HistGradientBoostingRegressor,\n"
            ")\n"
            "```\n"
            "\n"
            "The HGB estimators can handle:\n"
            "\n"
            "- missing numerical values,\n"
            "- categorical features represented appropriately,\n"
            "- early stopping.\n"
            "\n"
            "This can reduce preprocessing work dramatically.\n"
            "\n"
            "For example, the chapter shows a compact California housing pipeline:\n"
            "\n"
            "```python\n"
            "from sklearn.pipeline import make_pipeline\n"
            "from sklearn.compose import make_column_transformer\n"
            "from sklearn.ensemble import HistGradientBoostingRegressor\n"
            "from sklearn.preprocessing import OrdinalEncoder\n"
            "\n"
            "hgb_reg = make_pipeline(\n"
            "    make_column_transformer(\n"
            "        (\n"
            "            OrdinalEncoder(),\n"
            "            [\"ocean_proximity\"],\n"
            "        ),\n"
            "        remainder=\"passthrough\",\n"
            "        force_int_remainder_cols=False,\n"
            "    ),\n"
            "    HistGradientBoostingRegressor(\n"
            "        categorical_features=[0],\n"
            "        random_state=42,\n"
            "    ),\n"
            ")\n"
            "\n"
            "hgb_reg.fit(\n"
            "    housing,\n"
            "    housing_labels,\n"
            ")\n"
            "```\n"
            "\n"
            "No explicit:\n"
            "\n"
            "```text\n"
            "imputer\n"
            "standard scaler\n"
            "one-hot encoder\n"
            "```\n"
            "\n"
            "is required for this example.\n"
            "\n"
            "### When HGB is attractive\n"
            "\n"
            "HGB is especially useful when:\n"
            "\n"
            "- the dataset is large,\n"
            "- the data is tabular,\n"
            "- training speed matters,\n"
            "- missing values are present,\n"
            "- categorical features are present,\n"
            "- you want a strong baseline with limited preprocessing.\n"
            "\n"
            "The chapter also mentions specialized gradient-boosting ecosystems such as:\n"
            "\n"
            "- XGBoost,\n"
            "- CatBoost,\n"
            "- LightGBM.\n"
            "\n"
            "The important lesson here is not to memorize every library yet.\n"
            "\n"
            "It is to recognize histogram-based gradient boosting as a major tool for modern tabular machine learning.\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Stacking: train a model to combine models\n"
            "\n"
            "Voting uses a fixed aggregation rule:\n"
            "\n"
            "```text\n"
            "majority vote\n"
            "or\n"
            "average probability\n"
            "```\n"
            "\n"
            "**Stacking** asks:\n"
            "\n"
            "> Why choose the aggregation rule manually?\n"
            "\n"
            "Instead, train another model to learn how to combine the base models.\n"
            "\n"
            "This final model is often called:\n"
            "\n"
            "- a **blender**,\n"
            "- a **meta-learner**,\n"
            "- a **final estimator**.\n"
            "\n"
            "### Prediction-time idea\n"
            "\n"
            "Suppose three regressors predict:\n"
            "\n"
            "```text\n"
            "model 1 -> 3.1\n"
            "model 2 -> 2.7\n"
            "model 3 -> 2.9\n"
            "```\n"
            "\n"
            "The blender receives:\n"
            "\n"
            "```text\n"
            "[3.1, 2.7, 2.9]\n"
            "```\n"
            "\n"
            "as its features and predicts:\n"
            "\n"
            "```text\n"
            "3.0\n"
            "```\n"
            "\n"
            "{{image:stacking-blender-prediction}}\n"
            "\n"
            "### The dangerous wrong way to train the blender\n"
            "\n"
            "Do not:\n"
            "\n"
            "```text\n"
            "train base models on training data\n"
            "predict that same training data\n"
            "train blender on those predictions\n"
            "```\n"
            "\n"
            "The base predictions may be unrealistically good because each base model has already seen those examples.\n"
            "\n"
            "That would leak information into the blender.\n"
            "\n"
            "### Use out-of-sample base predictions\n"
            "\n"
            "Instead:\n"
            "\n"
            "1. use cross-validation on each base predictor,\n"
            "2. obtain out-of-sample predictions for every training instance,\n"
            "3. use those predictions as features for the blender,\n"
            "4. use the original targets as the blender targets,\n"
            "5. finally retrain the base models on the full training set.\n"
            "\n"
            "{{image:stacking-training-process}}\n"
            "\n"
            "If there are three base predictors, the blender’s training matrix contains:\n"
            "\n"
            "```text\n"
            "feature 1 -> prediction from model 1\n"
            "feature 2 -> prediction from model 2\n"
            "feature 3 -> prediction from model 3\n"
            "```\n"
            "\n"
            "regardless of how many features existed in the original dataset.\n"
            "\n"
            "### Scikit-Learn stacking\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import StackingClassifier\n"
            "\n"
            "stacking_clf = StackingClassifier(\n"
            "    estimators=[\n"
            "        (\n"
            "            \"lr\",\n"
            "            LogisticRegression(\n"
            "                random_state=42\n"
            "            ),\n"
            "        ),\n"
            "        (\n"
            "            \"rf\",\n"
            "            RandomForestClassifier(\n"
            "                random_state=42\n"
            "            ),\n"
            "        ),\n"
            "        (\n"
            "            \"svc\",\n"
            "            SVC(\n"
            "                probability=True,\n"
            "                random_state=42,\n"
            "            ),\n"
            "        ),\n"
            "    ],\n"
            "    final_estimator=RandomForestClassifier(\n"
            "        random_state=43\n"
            "    ),\n"
            "    cv=5,\n"
            ")\n"
            "\n"
            "stacking_clf.fit(\n"
            "    X_train,\n"
            "    y_train,\n"
            ")\n"
            "```\n"
            "\n"
            "The source reports roughly:\n"
            "\n"
            "```text\n"
            "soft voting accuracy -> 92.0%\n"
            "stacking accuracy    -> 92.8%\n"
            "```\n"
            "\n"
            "That is an improvement.\n"
            "\n"
            "But ask:\n"
            "\n"
            "```text\n"
            "Is +0.8 percentage point worth:\n"
            "- another model?\n"
            "- more training?\n"
            "- more inference cost?\n"
            "- more deployment complexity?\n"
            "```\n"
            "\n"
            "The best production architecture is not always the architecture with the highest benchmark score.\n"
            "\n"
            "{{exercise:M01.L06.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## 10. Choosing an ensemble method\n"
            "\n"
            "The chapter covers many methods, but they are easier to remember when organized by the problem each one solves.\n"
            "\n"
            "| Method | Main idea | Good fit |\n"
            "|---|---|---|\n"
            "| Hard voting | Majority vote across diverse models | Several strong classifiers with different errors |\n"
            "| Soft voting | Average class probabilities | Probabilistic classifiers with well-calibrated confidence |\n"
            "| Bagging | Same learner on bootstrap samples | High-variance / overfitting-prone models |\n"
            "| Pasting | Same learner on samples without replacement | Similar goal to bagging with less sampling redundancy |\n"
            "| Random forest | Bagged trees + random features at splits | Strong general-purpose tabular baseline |\n"
            "| Extra-trees | Random features + random thresholds | Faster, more randomized tree ensemble |\n"
            "| AdaBoost | Reweight difficult training examples sequentially | Small/medium structured data with weak learners |\n"
            "| Gradient boosting | Fit residual errors sequentially | High-performance structured-data prediction |\n"
            "| HGB | Gradient boosting with binned features | Large tabular datasets and faster training |\n"
            "| Stacking | Train a model to combine base-model predictions | Maximum predictive performance from diverse models |\n"
            "\n"
            "### A practical starting strategy\n"
            "\n"
            "For a tabular project, a reasonable experiment plan is:\n"
            "\n"
            "```text\n"
            "1. establish a simple baseline\n"
            "2. try random forest / extra-trees\n"
            "3. try gradient boosting or HGB\n"
            "4. tune the strongest candidates\n"
            "5. consider voting or stacking only if multiple strong diverse models remain\n"
            "```\n"
            "\n"
            "Do not begin with the most complicated ensemble possible.\n"
            "\n"
            "Complexity should earn its place through validated improvement.\n"
            "\n"
            "### Bias, variance, diversity, and compute\n"
            "\n"
            "Most ensemble decisions can be understood through four questions:\n"
            "\n"
            "```text\n"
            "1. Does my base model have high variance?\n"
            "2. Can I create predictors with less-correlated errors?\n"
            "3. Can models train independently or must they be sequential?\n"
            "4. Is the expected accuracy gain worth the compute and deployment cost?\n"
            "```\n"
            "\n"
            "If you can answer those questions, the chapter stops feeling like a list of unrelated algorithms.\n"
            "\n"
            "It becomes a set of strategies for controlling model error.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> Adding more models automatically makes an ensemble better.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "If the models are weak in the same way and make highly correlated errors, aggregation may add cost without adding useful diversity.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Soft voting is always better than hard voting.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Soft voting relies on probability estimates. Poorly calibrated probabilities can make confidence-weighted aggregation misleading.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Bagging reduces overfitting because every tree is simpler.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Individual bagged trees may still be very complex. The main benefit comes from aggregating diverse high-variance predictors so their fluctuations partially cancel.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> OOB evaluation means the model never needs a final test set.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "OOB estimates are useful during development, but a final untouched test set is still the strongest way to estimate final generalization before launch.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> AdaBoost and gradient boosting correct earlier models in the same way.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "AdaBoost changes the importance of training examples, emphasizing previous mistakes. Gradient boosting fits new predictors to residual errors or, more generally, to directions that improve the ensemble objective.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Stacking can train the blender using predictions made by base models on the same examples they were fitted on.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Those predictions are optimistically biased. The blender should be trained from out-of-sample predictions, typically generated with cross-validation.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Ensemble | Group of predictors whose outputs are combined |\n"
            "| Ensemble learning | Learning approach based on combining multiple predictors |\n"
            "| Weak learner | Predictor that performs only slightly better than random |\n"
            "| Strong learner | Predictor with substantially useful predictive performance |\n"
            "| Diversity | Degree to which ensemble members make different errors |\n"
            "| Hard voting | Predicting the class receiving the most model votes |\n"
            "| Soft voting | Predicting from averaged model class probabilities |\n"
            "| Bagging | Training predictors on random bootstrap samples with replacement |\n"
            "| Pasting | Training predictors on random samples without replacement |\n"
            "| Bootstrap sample | Random sample drawn with replacement |\n"
            "| OOB instance | Training instance not selected for a particular bootstrap sample |\n"
            "| OOB evaluation | Estimating ensemble performance using predictors for which each training instance was out of bag |\n"
            "| Random patches | Sampling both instances and features |\n"
            "| Random subspaces | Keeping instances while sampling subsets of features |\n"
            "| Random forest | Ensemble of randomized decision trees, typically trained with bagging |\n"
            "| Extra-trees | Tree ensemble using extra randomness in split thresholds |\n"
            "| Feature importance | Model-derived score estimating how much features contribute to predictive decisions |\n"
            "| Boosting | Sequential ensemble approach where new learners correct weaknesses of the current ensemble |\n"
            "| AdaBoost | Boosting method that increases focus on misclassified training instances |\n"
            "| Decision stump | Decision tree with a single decision node (`max_depth=1`) |\n"
            "| Gradient boosting | Sequential ensemble method that fits new learners to residual errors / objective corrections |\n"
            "| Residual | Difference between the true target and current prediction |\n"
            "| Shrinkage | Using a small learning rate to reduce each boosting stage’s contribution |\n"
            "| Early stopping | Ending training when validation performance stops improving |\n"
            "| Stochastic gradient boosting | Gradient boosting where each tree trains on a random fraction of instances |\n"
            "| Histogram-based gradient boosting | Fast boosting approach that bins continuous feature values |\n"
            "| Stacking | Training a meta-model to combine predictions from base models |\n"
            "| Blender / meta-learner | Final stacking model trained on base-model predictions |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why does ensemble diversity matter?\n"
            "2. What is the difference between hard and soft voting?\n"
            "3. Why can poorly calibrated probabilities hurt soft voting?\n"
            "4. What is the difference between bagging and pasting?\n"
            "5. Why is bagging particularly useful for high-variance models such as deep trees?\n"
            "6. What is an OOB instance, and how can it be used for evaluation?\n"
            "7. What is the difference between random patches and random subspaces?\n"
            "8. How does a random forest add randomness beyond ordinary bagging?\n"
            "9. How are extra-trees more random than random forests?\n"
            "10. What does random-forest feature importance measure?\n"
            "11. How does AdaBoost decide what the next learner should focus on?\n"
            "12. How does gradient boosting differ from AdaBoost?\n"
            "13. Why can a low learning rate require more boosting estimators?\n"
            "14. What problem does early stopping solve?\n"
            "15. Why can HGB train much faster on large tabular datasets?\n"
            "16. Why must stacking use out-of-sample predictions to train the blender?\n"
            "17. When might a small stacking improvement not be worth deploying?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**Ensemble learning works by turning multiple imperfect predictors into a stronger system. The central tools are diversity, aggregation, and controlled sequential correction: voting combines different models, bagging and random forests reduce variance through randomness, boosting corrects errors stage by stage, and stacking learns how to combine models. The strongest ensemble is not simply the largest one—it is the one whose members contribute useful, sufficiently different information at an acceptable computational and operational cost.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "ensemble-intuition",
                "title": "Why ensembles work",
                "order": 1,
            },
            {
                "id": "voting",
                "title": "Voting classifiers: combine different models",
                "order": 2,
            },
            {
                "id": "bagging-pasting",
                "title": "Bagging and pasting: diversify the data instead of the algorithm",
                "order": 3,
            },
            {
                "id": "oob-feature-sampling",
                "title": "Out-of-bag evaluation and feature sampling",
                "order": 4,
            },
            {
                "id": "random-forests",
                "title": "Random forests, extra-trees, and feature importance",
                "order": 5,
            },
            {
                "id": "adaboost",
                "title": "AdaBoost: make each learner focus on previous mistakes",
                "order": 6,
            },
            {
                "id": "gradient-boosting",
                "title": "Gradient boosting: learn the residual errors",
                "order": 7,
            },
            {
                "id": "hgb",
                "title": "Histogram-based gradient boosting",
                "order": 8,
            },
            {
                "id": "stacking",
                "title": "Stacking: train a model to combine models",
                "order": 9,
            },
            {
                "id": "choose-ensemble",
                "title": "Choosing an ensemble method",
                "order": 10,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L06.EX01",

            "title": "Design a Bagging Ensemble",

            "lesson_code": "M01.L06",

            "section_id": "oob-feature-sampling",

            "placement": "after_section",

            "description": (
                "Practice choosing between bagging, pasting, OOB evaluation, "
                "and feature sampling for an overfitting base learner."
            ),

            "instructions": (
                "You have a deep decision tree that performs extremely well on "
                "the training set but poorly on validation data. The dataset is "
                "moderately noisy and contains 200 input features.\n\n"
                "1. Would bagging or pasting be your first choice? Explain why.\n"
                "2. Explain how training many trees on different samples can "
                "reduce variance even if the individual trees remain complex.\n"
                "3. What does oob_score=True allow you to estimate?\n"
                "4. Explain how random feature sampling could create additional "
                "diversity.\n"
                "5. Write a short BaggingClassifier configuration using at least "
                "200 trees, all CPU cores, and OOB evaluation."
            ),

            "expected_output": (
                "A recommendation favoring bagging for the noisy, overfitting "
                "tree; a variance-reduction explanation; a correct description "
                "of OOB evaluation; a feature-sampling explanation; and valid "
                "Scikit-Learn code using BaggingClassifier with oob_score=True."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "bagging",
                "bias-variance",
                "oob-evaluation",
                "feature-sampling",
                "scikit-learn",
            ],
        },

        {
            "id": "M01.L06.EX02",

            "title": "Choose the Right Ensemble Strategy",

            "lesson_code": "M01.L06",

            "section_id": "choose-ensemble",

            "placement": "after_section",

            "description": (
                "Compare voting, random forests, boosting, HGB, and stacking "
                "using practical modeling and deployment constraints."
            ),

            "instructions": (
                "For each scenario, choose a reasonable ensemble strategy and "
                "justify it in one or two sentences:\n\n"
                "1. Three already-strong but very different classifiers expose "
                "well-calibrated class probabilities.\n"
                "2. A deep decision tree badly overfits a noisy tabular dataset.\n"
                "3. You need a powerful model for a large tabular dataset with "
                "missing values and categorical features, and training speed "
                "matters.\n"
                "4. You have several strong diverse models and want to squeeze "
                "out a final performance gain, accepting extra complexity.\n"
                "5. A gradient boosting model keeps improving training error but "
                "validation performance stops improving. What training control "
                "should you use?"
            ),

            "expected_output": (
                "A mapping such as soft voting for scenario 1, bagging/random "
                "forest for scenario 2, HGB for scenario 3, stacking for "
                "scenario 4, and early stopping for scenario 5, with reasoning "
                "grounded in diversity, variance, scalability, and validation."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "ensemble-selection",
                "voting",
                "random-forests",
                "boosting",
                "hist-gradient-boosting",
                "stacking",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L06.QZ01",

        "title": "Ensemble Learning and Random Forests — Knowledge Check",

        "lesson_code": "M01.L06",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L06.Q01",

                "section_id": "ensemble-intuition",

                "question": (
                    "Why is predictor diversity important in an ensemble?"
                ),

                "options": [
                    "It guarantees every model has zero bias.",
                    "Different error patterns make aggregation more likely to cancel individual mistakes.",
                    "It ensures every model uses the same decision boundary.",
                    "It removes the need for validation.",
                ],

                "correct": 1,

                "explanation": (
                    "Ensembles benefit when members make different errors. "
                    "Highly correlated mistakes are difficult for aggregation "
                    "to correct."
                ),
            },

            {
                "id": "M01.L06.Q02",

                "section_id": "voting",

                "question": (
                    "What is the key difference between hard and soft voting?"
                ),

                "options": [
                    "Hard voting averages probabilities; soft voting counts labels.",
                    "Hard voting counts class predictions; soft voting aggregates estimated class probabilities.",
                    "Soft voting works only for regression.",
                    "Hard voting requires calibrated probabilities.",
                ],

                "correct": 1,

                "explanation": (
                    "Hard voting aggregates final class labels, while soft voting "
                    "uses the models' class-probability estimates."
                ),
            },

            {
                "id": "M01.L06.Q03",

                "section_id": "bagging-pasting",

                "question": (
                    "What distinguishes bagging from pasting?"
                ),

                "options": [
                    "Bagging samples with replacement; pasting samples without replacement.",
                    "Pasting uses trees and bagging cannot.",
                    "Bagging is sequential while pasting is parallel.",
                    "Pasting samples features while bagging samples only labels.",
                ],

                "correct": 0,

                "explanation": (
                    "Both train predictors on random subsets of instances, but "
                    "bagging uses bootstrap sampling with replacement."
                ),
            },

            {
                "id": "M01.L06.Q04",

                "section_id": "oob-feature-sampling",

                "question": (
                    "What is an out-of-bag instance for one predictor in a "
                    "bagging ensemble?"
                ),

                "options": [
                    "An example removed permanently from the dataset.",
                    "A training example not selected in that predictor's bootstrap sample.",
                    "A test-set example with an incorrect label.",
                    "A feature not used by the ensemble.",
                ],

                "correct": 1,

                "explanation": (
                    "Because bootstrap sampling does not select every training "
                    "instance, examples left out for a predictor can be used to "
                    "obtain out-of-sample predictions from that predictor."
                ),
            },

            {
                "id": "M01.L06.Q05",

                "section_id": "random-forests",

                "question": (
                    "How does a random forest add diversity beyond ordinary "
                    "bagging of decision trees?"
                ),

                "options": [
                    "It removes randomness from training.",
                    "At each split it considers only a random subset of features.",
                    "It trains all trees on the exact same bootstrap sample.",
                    "It forces every tree to have depth 1.",
                ],

                "correct": 1,

                "explanation": (
                    "Random forests randomly restrict the candidate features "
                    "available at each node, reducing correlation among trees."
                ),
            },

            {
                "id": "M01.L06.Q06",

                "section_id": "adaboost",

                "question": (
                    "What does AdaBoost do after a predictor misclassifies some "
                    "training instances?"
                ),

                "options": [
                    "Deletes the misclassified instances.",
                    "Raises their relative weights so later predictors focus more on them.",
                    "Converts them into validation data.",
                    "Always increases the tree depth.",
                ],

                "correct": 1,

                "explanation": (
                    "AdaBoost progressively emphasizes hard examples by "
                    "increasing the weights of instances that earlier learners "
                    "misclassified."
                ),
            },

            {
                "id": "M01.L06.Q07",

                "section_id": "gradient-boosting",

                "question": (
                    "In the regression example, what does the next gradient "
                    "boosting tree learn?"
                ),

                "options": [
                    "A completely unrelated target.",
                    "Only the most important feature.",
                    "The residual errors left by the current ensemble.",
                    "The test-set labels.",
                ],

                "correct": 2,

                "explanation": (
                    "Each new learner models the errors remaining after the "
                    "current ensemble, so its prediction acts as a correction."
                ),
            },

            {
                "id": "M01.L06.Q08",

                "section_id": "hgb",

                "question": (
                    "Why can histogram-based gradient boosting train much faster "
                    "on large datasets?"
                ),

                "options": [
                    "It removes the target column.",
                    "It bins feature values, greatly reducing the number of split thresholds that must be evaluated.",
                    "It never builds decision trees.",
                    "It requires all features to be binary.",
                ],

                "correct": 1,

                "explanation": (
                    "Binning compresses many distinct numeric values into a "
                    "limited number of integer bins, reducing split-search cost "
                    "and enabling efficient data structures."
                ),
            },

            {
                "id": "M01.L06.Q09",

                "section_id": "stacking",

                "type": "open",

                "question": (
                    "Why should a stacking blender be trained on cross-validated "
                    "out-of-sample predictions instead of predictions made by "
                    "base models on the same examples they were trained on?"
                ),
            },

            {
                "id": "M01.L06.Q10",

                "section_id": "choose-ensemble",

                "type": "open",

                "question": (
                    "Compare bagging and boosting in terms of training order, "
                    "parallelization, and the type of problem each is trying to "
                    "solve."
                ),
            },
        ],

        "passing_score": 70,
    },
}
