"""M01.L05 — Decision Trees: Learning by Asking Questions.

One source chapter -> one complete learner-facing lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 5: Decision Trees. Source page numbers were not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L05"

MODULE_ORDER = 1

MODULE_TITLE = "Decision Trees"

MODULE_DESCRIPTION = (
    "Learn how decision trees classify and predict by recursively splitting data, "
    "how CART chooses splits, how tree complexity is regularized, how trees perform "
    "regression, and why individual trees can be unstable despite being easy to interpret."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Decision Trees: Learning by Asking Questions",

    "slug": "machine-learning-foundations-m01-l05",

    "description": (
        "A practical and intuitive lesson on decision-tree classification and regression, "
        "Gini impurity and entropy, CART training, probability estimates, regularization, "
        "axis-aligned boundaries, and the high-variance nature of individual trees."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.75,

    "skill_tags": [
        "decision-trees",
        "classification",
        "regression",
        "cart",
        "gini-impurity",
        "entropy",
        "regularization",
        "model-interpretability",
        "bias-variance",
        "machine-learning-foundations",
        "module-01",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Decision Trees: Learning by Asking Questions",

        "content": (
            """# Decision Trees: Learning by Asking Questions

> **Course:** Applied Machine Learning with Scikit-Learn  
> **Lesson:** M01.L05  
> **Module:** Decision Trees  
> **Source alignment:** Supplied source, Chapter 5, *Decision Trees*. Source page numbers were not provided. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain how a decision tree makes a prediction by following feature-threshold questions from the root to a leaf.
- Read the main information stored in a classification-tree node: split rule, samples, class counts, predicted class, and impurity.
- Explain Gini impurity and entropy as measures of how mixed a node is.
- Describe how the CART algorithm greedily chooses splits and why this does not guarantee the globally optimal tree.
- Estimate class probabilities from the class distribution in a leaf.
- Explain why decision trees usually do not require feature scaling.
- Regularize a decision tree using `max_depth`, `min_samples_leaf`, `min_samples_split`, `max_leaf_nodes`, `max_features`, and pruning-related controls.
- Use a decision tree for regression and explain why its predictions are piecewise constant.
- Recognize overfitting in both classification and regression trees.
- Explain why trees are sensitive to axis orientation and why individual trees have high variance.
- Connect the instability of individual trees to the motivation for random forests.

---

## 1. Decision trees: a model built from questions

A decision tree is one of the easiest machine-learning models to understand because its reasoning resembles a sequence of human decisions.

Imagine that you want to identify an iris flower from its petal measurements. Instead of computing one complicated equation, the tree asks questions such as:

```text
Is petal length <= 2.45 cm?
    Yes -> predict Iris setosa
    No  -> is petal width <= 1.75 cm?
               Yes -> predict Iris versicolor
               No  -> predict Iris virginica
```

Each question splits the current set of examples into two groups. Repeating this process creates a tree.

The important vocabulary is:

- **Root node:** the first node at the top of the tree.
- **Split/internal node:** a node that asks a question and has child nodes.
- **Leaf node:** a terminal node that makes the final prediction.
- **Depth:** how many splits separate a node from the root.
- **Branch:** one path produced by answering a split question.

A simple Scikit-Learn tree can be trained like this:

```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris(as_frame=True)
X_iris = iris.data[["petal length (cm)", "petal width (cm)"]].values
y_iris = iris.target

tree_clf = DecisionTreeClassifier(max_depth=2, random_state=42)
tree_clf.fit(X_iris, y_iris)
```

The source chapter visualizes the resulting model as a compact tree. This is one of the most useful figures in the chapter because it teaches how to read the model itself.

{{image:iris-decision-tree-anatomy}}

### Why trees feel different from many other models

A linear model combines all features at once in a weighted equation. A tree instead selects **one feature at a time** and asks whether it is above or below a threshold.

This has two important consequences:

1. The model can represent nonlinear decision rules even though every individual split is simple.
2. The final reasoning can often be inspected and explained in ordinary language.

### Very little preprocessing is required

A major advantage highlighted in the chapter is that ordinary decision-tree training does **not** require features to be centered or standardized.

Why? A split such as:

```text
petal width <= 1.75
```

only depends on the ordering of values. If every petal width were multiplied by 100, the useful threshold would also be multiplied by 100, but the ordering of the training examples would remain the same.

This is very different from algorithms such as gradient descent, k-nearest neighbors, or models based on distance and geometry, where feature scale may directly affect optimization or comparison.

---

## 2. Reading a tree: samples, values, impurity, and probability

A trained tree stores more than just split conditions. To understand what the model has learned, you should know what the common node statistics mean.

### `samples`

The `samples` value tells you how many training examples reached that node.

If 100 flowers reach a node, then every statistic displayed there is calculated from those 100 examples.

### `value`

For a classification tree, `value` describes how many examples from each class reached the node.

For example:

```text
value = [0, 49, 5]
```

means that the node contains:

- 0 examples of class 0,
- 49 examples of class 1,
- 5 examples of class 2.

The tree normally predicts the class with the largest count.

### Gini impurity

A node is **pure** when all examples reaching it belong to the same class. In that case its Gini impurity is `0`.

The chapter's Gini idea can be written as:

```text
Gini = 1 - sum(class_probability²)
```

Suppose a node contains 54 flowers:

```text
0 setosa
49 versicolor
5 virginica
```

Then most examples belong to one class, so the node has low impurity. If the classes were distributed much more evenly, impurity would be higher.

**Mental model:** impurity asks, *How mixed are the labels inside this node?*

### From leaves to class probabilities

A classification tree can return probabilities as well as hard predictions. It first sends an instance to a leaf, then uses the class proportions among the training examples in that leaf.

For the chapter's example, a leaf containing `[0, 49, 5]` produces approximately:

```text
P(setosa)     = 0 / 54  = 0.000
P(versicolor) = 49 / 54 = 0.907
P(virginica)  = 5 / 54  = 0.093
```

In Scikit-Learn:

```python
print(tree_clf.predict_proba([[5, 1.5]]).round(3))
print(tree_clf.predict([[5, 1.5]]))
```

The important limitation is subtle: **every point that reaches the same leaf gets the same probability distribution**. The probability estimate does not gradually change as you move around inside that leaf's region.

### Decision regions

Every split cuts the feature space with a threshold. In a two-feature problem, these cuts form rectangular decision regions because standard tree splits are parallel to one of the feature axes.

{{image:decision-tree-boundaries-by-depth}}

This connection is essential: the diagram of the tree and the plot of its decision boundaries are two views of the **same model**.

---

## 3. Why decision trees are called white-box models

Decision trees are often described as **white-box models** because their decisions can usually be inspected directly.

For a shallow tree, you can explain a prediction as a short rule:

```text
petal length > 2.45
AND petal width <= 1.75
-> Iris versicolor
```

This is valuable when a human needs to review the model's reasoning.

Examples mentioned by the chapter include domains such as:

- healthcare, where a clinician may need to inspect a diagnosis;
- finance, where analysts may need to understand a risk decision;
- judicial settings, where humans must retain final responsibility;
- human resources, where decision rules may need to be checked for problematic bias.

By contrast, large neural networks and many ensembles are harder to summarize as a few simple rules, even when their predictions are excellent.

### Interpretability has a practical limit

Do not turn “trees are interpretable” into “every tree is easy to interpret.”

A tree with hundreds or thousands of nodes can be technically inspectable but practically overwhelming. This is another reason why limiting tree complexity can be useful: regularization can improve both **generalization** and **human readability**.

---

## 4. How CART grows a decision tree

Scikit-Learn trains decision trees using the **Classification and Regression Tree (CART)** algorithm.

The central problem at every node is:

> Which feature and threshold should I use to split these examples into two better groups?

For classification, CART searches candidate feature-threshold pairs and favors a split that produces child nodes with low impurity, while taking their sizes into account.

A simplified mental model is:

```text
for each candidate feature:
    for each candidate threshold:
        split the node into left and right groups
        measure the weighted impurity after the split
choose the split with the lowest cost
repeat recursively on the children
```

### CART makes binary trees

Scikit-Learn's CART implementation creates **binary splits**. Every internal node has two outcomes:

```text
feature <= threshold
```

or

```text
feature > threshold
```

Other tree algorithms can allow more than two children, but CART repeatedly uses yes/no decisions.

### When does recursion stop?

Growth can stop because:

- the maximum depth has been reached;
- the node cannot be split in a way that sufficiently improves the objective;
- a minimum sample requirement prevents further splitting;
- a maximum leaf limit has been reached;
- another regularization rule blocks further growth.

### CART is greedy

This is one of the most important ideas in the chapter.

CART chooses a good split **now**. It does not explore every possible future tree and ask which first split would eventually produce the globally best structure several levels later.

That makes CART a **greedy algorithm**.

Greedy optimization is computationally practical and usually produces useful trees, but it does not guarantee the globally optimal tree.

The chapter notes why this compromise is necessary: searching for the optimal tree is computationally intractable in general. So real tree-training algorithms settle for a good solution that can actually be found.

### Training versus prediction cost

After training, a prediction only needs to follow one path from the root to a leaf. In a roughly balanced tree, the number of visited nodes grows slowly with the number of training examples, so prediction is typically very fast.

Training is more expensive because CART must evaluate many possible split choices while growing the tree.

---

## 5. Gini impurity or entropy?

`DecisionTreeClassifier` uses **Gini impurity** by default, but Scikit-Learn also supports **entropy** as the split criterion.

Both try to answer essentially the same question:

> How mixed are the classes in this node?

For entropy, a pure node also has impurity `0`. The chapter's example uses the class proportions in a node and the familiar information-theory expression based on `-p log₂(p)`.

### Should you worry about choosing the perfect criterion?

Usually, no.

The chapter emphasizes that Gini impurity and entropy commonly produce similar trees. Gini is slightly faster to compute, which makes it a sensible default.

When they differ, their tendencies can differ slightly:

- Gini often isolates the most frequent class into its own branch.
- Entropy may produce somewhat more balanced trees.

But in most practical workflows, hyperparameters controlling **tree complexity** matter much more than obsessing over Gini versus entropy.

{{exercise:M01.L05.EX01}}

---

## 6. Controlling overfitting with tree regularization

Decision trees are extremely flexible. If you give a tree enough freedom, it can keep creating tiny regions until it matches the training data very closely.

That sounds attractive, but it is exactly how overfitting happens.

A tree is described as **nonparametric** because its structure is not fixed to a predetermined number of parameters before training. The tree can grow more nodes and branches as needed to fit the data.

To improve generalization, we restrict this freedom.

### `max_depth`

This is the simplest and often the first hyperparameter to tune.

```python
tree_clf = DecisionTreeClassifier(max_depth=4, random_state=42)
```

Smaller `max_depth`:

- reduces the number of successive decisions;
- makes the model simpler;
- generally increases bias;
- generally decreases variance;
- often improves interpretability.

### `min_samples_split`

A node must contain at least this many samples before it may be split.

Increasing it prevents the tree from creating decisions based on very small groups.

### `min_samples_leaf`

Every newly created leaf must contain at least this many samples.

This is especially useful for small or noisy datasets because it prevents tiny leaves that memorize a handful of examples.

### `max_leaf_nodes`

This directly caps how many terminal regions the tree may create.

### `max_features`

This limits how many features are considered when searching for a split at each node. It can speed up training on high-dimensional data and also inject useful randomness into tree-based methods.

### `min_impurity_decrease`

A split is accepted only if it improves impurity by at least the specified amount.

### `ccp_alpha`

This controls **minimal cost-complexity pruning**. A larger value encourages more pruning and therefore a smaller tree.

A useful rule from the chapter is:

```text
To regularize more:
- decrease max_* limits
- increase min_* requirements
- increase ccp_alpha
```

### Regularization in action

The chapter compares two classifiers on the noisy `make_moons()` dataset: one unrestricted tree and one using `min_samples_leaf=5`.

```python
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier

X_moons, y_moons = make_moons(
    n_samples=150,
    noise=0.2,
    random_state=42,
)

tree_clf1 = DecisionTreeClassifier(random_state=42)
tree_clf2 = DecisionTreeClassifier(min_samples_leaf=5, random_state=42)

tree_clf1.fit(X_moons, y_moons)
tree_clf2.fit(X_moons, y_moons)
```

{{image:regularized-vs-unregularized-tree-boundaries}}

The source's test-set comparison illustrates the point: the regularized tree performs better on new examples even though the unrestricted tree can fit the training data more aggressively.

### Pre-pruning and post-pruning

Scikit-Learn commonly regularizes while the tree is being grown using limits such as `max_depth` or `min_samples_leaf`.

Another family of methods first grows a large tree and then **prunes** branches that do not provide enough useful improvement. The chapter discusses statistical-significance-based pruning in other algorithms and also exposes `ccp_alpha` for cost-complexity pruning.

The common idea is the same:

> A branch should survive only if the extra complexity earns enough predictive value.

---

## 7. Decision trees for regression

Decision trees are not limited to classification. A `DecisionTreeRegressor` uses the same recursive splitting idea but predicts a **number** instead of a class.

The source trains a regression tree on a noisy quadratic dataset:

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(seed=42)
X_quad = rng.random((200, 1)) - 0.5
y_quad = X_quad ** 2 + 0.025 * rng.standard_normal((200, 1))

tree_reg = DecisionTreeRegressor(max_depth=2, random_state=42)
tree_reg.fit(X_quad, y_quad)
```

### What does a regression leaf predict?

For classification, a leaf chooses a class from the class distribution.

For regression, a leaf predicts the **average target value** of the training examples that reached that leaf.

Suppose a leaf contains many training examples and their average target is `0.038`. Every new example routed to that leaf receives approximately the same prediction:

```text
prediction = 0.038
```

That explains the characteristic shape of tree regression.

### Piecewise-constant predictions

A tree partitions the input space into regions. Within each region, the prediction is constant. Increasing the depth creates more, smaller regions, allowing a more detailed fit.

{{image:decision-tree-regression-depth-comparison}}

### How CART changes for regression

The overall recursive algorithm is the same, but the split objective changes.

Instead of asking:

```text
Which split makes the child nodes purer?
```

regression asks:

```text
Which split makes the target values within the child regions more similar?
```

The chapter expresses this using an MSE-based CART objective.

### Regression trees can overfit too

An unrestricted regression tree may create tiny regions around individual training examples and produce a jagged prediction function.

The same regularization tools apply. For example:

```python
DecisionTreeRegressor(min_samples_leaf=10, random_state=42)
```

forces each leaf to represent a larger group of examples, usually producing a smoother and more generalizable model.

---

## 8. Important limitation: trees prefer axis-aligned splits

Standard decision trees ask one-feature threshold questions, such as:

```text
x1 <= 2.7
```

or:

```text
x2 <= 1.4
```

In two dimensions, these produce vertical or horizontal boundaries. This makes decision trees naturally good at creating rectangular regions, but it also creates a weakness: the model may represent a diagonal pattern very inefficiently.

Imagine a dataset that can be separated with one diagonal line. A tree cannot directly draw that diagonal line. Instead, it may approximate the diagonal using many small staircase-like horizontal and vertical splits.

{{image:decision-tree-axis-orientation-sensitivity}}

### Can PCA help?

The chapter shows that scaling the data and then applying PCA can rotate the feature space. In some cases this reduces feature correlation and makes the important structure easier for a tree to capture with a small number of axis-aligned splits.

```python
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pca_pipeline = make_pipeline(StandardScaler(), PCA())
X_iris_rotated = pca_pipeline.fit_transform(X_iris)

tree_clf_pca = DecisionTreeClassifier(max_depth=2, random_state=42)
tree_clf_pca.fit(X_iris_rotated, y_iris)
```

This does **not** mean you should automatically apply PCA before every tree. The point is to understand that the coordinate system can affect how efficiently a tree represents a pattern.

### A useful implementation detail

The source also notes that Scikit-Learn's `DecisionTreeClassifier` and `DecisionTreeRegressor` support missing values natively, so an imputer is not always required before these estimators.

{{exercise:M01.L05.EX02}}

---

## 9. The bigger limitation: decision trees have high variance

The most important weakness of a single decision tree is not that it cannot fit complicated data. It often can.

The bigger problem is **instability**.

A small change in the training data, a small change in hyperparameters, or a different random choice during training can produce a very different tree.

This is what we mean when we say that decision trees have **high variance**.

{{image:decision-tree-high-variance}}

### Why `random_state` matters

If the algorithm has multiple equally good or nearly equal split choices, randomness can influence the tree that is selected.

Setting:

```python
random_state=42
```

makes the training process reproducible for experiments, debugging, and teaching.

But reproducibility does not remove the underlying statistical instability of the model. It only makes the same random choices repeatable.

### The bridge to random forests

The chapter ends with an important insight:

> If one tree has high variance, combine many different trees and average or vote over their predictions.

Individual trees may disagree strongly, but averaging many of them can cancel part of their instability. This idea leads directly to **random forests**, the next major topic.

---

## Important misconceptions

### Misconception 1: “A tree that perfectly fits the training data must be excellent.”

A perfect training fit may simply mean the tree memorized noise. Decision trees are flexible enough to overfit aggressively when left unrestricted.

### Misconception 2: “Feature scaling is required before a decision tree.”

Ordinary tree splits depend on thresholds and ordering, not Euclidean distance or gradient-descent geometry. Trees generally do not need scaling for the same reason many other algorithms do.

### Misconception 3: “Every child node must have lower impurity than its parent.”

CART minimizes a **weighted split objective**. The combined split should improve the objective, but an individual child is not guaranteed to be purer than the parent in every possible split.

### Misconception 4: “Decision trees are always easy to explain.”

A small tree is highly interpretable. A huge tree may contain so many branches that manual interpretation becomes impractical.

### Misconception 5: “If I rotate or rescale my features, the learned tree must stay the same.”

Rescaling individual features preserves their ordering and usually does not change the essential threshold structure. Rotating the coordinate system is different: it changes which patterns can be expressed with simple axis-aligned splits.

---

## Choosing tree settings: a practical guide

| Situation | Useful action | Why |
|---|---|---|
| Training accuracy is extremely high but validation accuracy is worse | Reduce `max_depth` | Makes the tree less flexible |
| Leaves contain only a handful of examples | Increase `min_samples_leaf` | Prevents tiny memorizing regions |
| The tree has too many terminal regions | Reduce `max_leaf_nodes` | Caps model complexity directly |
| Training is expensive with many features | Reduce `max_features` | Evaluates fewer candidate features per split |
| Small impurity improvements keep creating branches | Increase `min_impurity_decrease` | Requires splits to earn their complexity |
| A large fitted tree should be simplified afterward | Increase `ccp_alpha` | Encourages cost-complexity pruning |
| Results change across repeated runs | Set `random_state` for reproducibility | Makes stochastic choices repeatable |
| The problem has strongly diagonal geometry | Consider feature engineering or a rotation such as PCA | Axis-aligned splits may otherwise require many regions |

---

## Key terminology

| Term | Meaning |
|---|---|
| Decision tree | A model that recursively partitions data using feature-threshold questions |
| Root node | The first node in the tree |
| Split node | A node that asks a question and sends examples to child nodes |
| Leaf node | A terminal node that produces the prediction |
| Depth | Number of split levels from the root to a node |
| Gini impurity | A measure of how mixed the classes are inside a node |
| Entropy | An information-theoretic impurity measure used as an alternative to Gini |
| CART | Classification and Regression Tree algorithm used by Scikit-Learn to grow binary trees |
| Greedy algorithm | An algorithm that chooses a locally good action without exhaustively optimizing all future decisions |
| Nonparametric model | A model whose effective structure and number of parameters are not fixed in advance |
| Regularization | Restricting model flexibility to reduce overfitting |
| Pruning | Removing branches whose added complexity is not worthwhile |
| Piecewise constant | A prediction function that outputs one fixed value within each region |
| Axis-aligned split | A boundary perpendicular to one feature axis |
| High variance | Strong sensitivity of the fitted model to changes in the training data or training process |

---

## Self-check

Before continuing, make sure you can answer:

1. How does a decision tree turn a feature vector into a prediction?
2. What is the difference between a split node and a leaf node?
3. What does Gini impurity measure, and what does `gini = 0` mean?
4. How does a leaf produce class probabilities?
5. Why is CART described as greedy?
6. Why does an unrestricted decision tree tend to overfit?
7. Which hyperparameters can make a tree less complex?
8. How does a regression tree choose its prediction within a leaf?
9. Why can rotating a dataset make a decision tree much more complicated?
10. What does high variance mean for an individual tree, and how does it motivate random forests?

---

## Retain this idea

**A decision tree learns by repeatedly asking simple threshold questions. Its power comes from combining many simple splits into complex regions; its main danger is that this flexibility makes an unrestricted tree unstable and prone to overfitting, so controlling tree growth is just as important as growing the tree itself.**
"""
        ),

        "estimated_minutes": 165,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "tree-intuition",
                "title": "Decision trees: a model built from questions",
                "order": 1,
            },
            {
                "id": "reading-tree",
                "title": "Reading a tree: samples, values, impurity, and probability",
                "order": 2,
            },
            {
                "id": "interpretability",
                "title": "Why decision trees are called white-box models",
                "order": 3,
            },
            {
                "id": "cart",
                "title": "How CART grows a decision tree",
                "order": 4,
            },
            {
                "id": "gini-entropy",
                "title": "Gini impurity or entropy?",
                "order": 5,
            },
            {
                "id": "regularization",
                "title": "Controlling overfitting with tree regularization",
                "order": 6,
            },
            {
                "id": "regression",
                "title": "Decision trees for regression",
                "order": 7,
            },
            {
                "id": "limitations",
                "title": "Important limitation: trees prefer axis-aligned splits",
                "order": 8,
            },
            {
                "id": "variance",
                "title": "The bigger limitation: decision trees have high variance",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L05.EX01",

            "title": "Read and Diagnose a Classification Tree",

            "lesson_code": "M01.L05",

            "section_id": "gini-entropy",

            "placement": "after_section",

            "description": (
                "Practice reading leaf statistics, turning class counts into probabilities, "
                "and reasoning about impurity and tree predictions."
            ),

            "instructions": (
                "A leaf contains 80 training examples with class counts [8, 60, 12].\n"
                "1. Compute the estimated probability of each class for a new example that reaches this leaf.\n"
                "2. State which class the tree will predict.\n"
                "3. Decide whether this leaf is pure or impure and explain why.\n"
                "4. Explain why another example that reaches the same leaf receives the same probability distribution even if its feature values are different.\n"
                "5. Briefly explain what would happen to impurity if almost all 80 examples belonged to the same class."
            ),

            "expected_output": (
                "Three class probabilities, the predicted class, and a short explanation "
                "of leaf impurity and leaf-based probability estimation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tree-interpretation",
                "class-probabilities",
                "gini-impurity",
            ],
        },

        {
            "id": "M01.L05.EX02",

            "title": "Regularize an Overfitting Tree",

            "lesson_code": "M01.L05",

            "section_id": "limitations",

            "placement": "after_section",

            "description": (
                "Apply decision-tree regularization to a noisy classification problem and "
                "interpret the difference between memorizing the training set and generalizing."
            ),

            "instructions": (
                "1. Generate a noisy moons dataset with `make_moons(n_samples=1000, noise=0.3, random_state=42)`.\n"
                "2. Split the data into training and test sets.\n"
                "3. Train one unrestricted `DecisionTreeClassifier`.\n"
                "4. Train a second tree with at least one regularization control such as `max_depth`, `min_samples_leaf`, or `max_leaf_nodes`.\n"
                "5. Compare training and test accuracy for both trees.\n"
                "6. Explain which model appears to generalize better and identify the evidence for overfitting or underfitting.\n"
                "7. Change one regularization hyperparameter once more and explain how the bias/variance trade-off changed."
            ),

            "expected_output": (
                "Working Scikit-Learn code, a small comparison table containing training and "
                "test accuracy, and a short interpretation of the regularization effect."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "decision-tree-training",
                "regularization",
                "overfitting-diagnosis",
                "model-evaluation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L05.QZ01",

        "title": "Decision Trees: Learning by Asking Questions — Knowledge Check",

        "lesson_code": "M01.L05",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L05.Q01",

                "section_id": "reading-tree",

                "question": (
                    "A classification-tree leaf has `value = [0, 49, 5]`. "
                    "Approximately what probability does it assign to class 1?"
                ),

                "options": [
                    "0%",
                    "9.3%",
                    "50%",
                    "90.7%",
                ],

                "correct": 3,

                "explanation": (
                    "The leaf probability is the class count divided by the total count. "
                    "Class 1 therefore gets 49 / 54, which is about 90.7%."
                ),
            },

            {
                "id": "M01.L05.Q02",

                "section_id": "cart",

                "question": "Why is CART described as a greedy training algorithm?",

                "options": [
                    "It always chooses the feature with the largest numerical values.",
                    "It chooses a good split at the current node without exhaustively searching every possible future tree.",
                    "It trains only on a random subset of the training set.",
                    "It always grows the deepest possible tree first and then restarts.",
                ],

                "correct": 1,

                "explanation": (
                    "CART optimizes each split locally. It recursively repeats this process "
                    "instead of globally exploring all possible tree structures."
                ),
            },

            {
                "id": "M01.L05.Q03",

                "section_id": "regularization",

                "question": (
                    "A decision tree has nearly perfect training accuracy but much worse validation accuracy. "
                    "Which change is most likely to help?"
                ),

                "options": [
                    "Increase `max_depth` substantially.",
                    "Decrease `min_samples_leaf` to 1.",
                    "Reduce tree complexity, for example by decreasing `max_depth` or increasing `min_samples_leaf`.",
                    "Standardize every feature because unscaled features are the primary cause of tree overfitting.",
                ],

                "correct": 2,

                "explanation": (
                    "The pattern indicates overfitting. Restricting tree growth reduces variance "
                    "and can improve generalization. Standard scaling is not the standard remedy for this problem."
                ),
            },

            {
                "id": "M01.L05.Q04",

                "section_id": "regression",

                "question": "What does a standard regression-tree leaf normally predict?",

                "options": [
                    "The median feature value that reached the leaf.",
                    "A probability distribution over classes.",
                    "The average target value of the training examples associated with that leaf.",
                    "A globally fitted polynomial equation shared by every leaf.",
                ],

                "correct": 2,

                "explanation": (
                    "Regression trees partition the input space into regions and predict the "
                    "average target value of the training examples in each leaf region."
                ),
            },

            {
                "id": "M01.L05.Q05",

                "section_id": "variance",

                "type": "open",

                "question": (
                    "Two decision trees trained on almost identical datasets produce very different structures. "
                    "Explain which property of decision trees this demonstrates, give one way to regularize an "
                    "individual tree, and explain why combining many trees can help."
                ),
            },
        ],

        "passing_score": 70,
    },
}
