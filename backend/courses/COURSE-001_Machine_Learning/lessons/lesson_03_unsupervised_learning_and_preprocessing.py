"""M03.L01 — Unsupervised Learning and Preprocessing.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-001, Chapter 3, pages not provided in extracted source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"

MODULE_ORDER = 3

MODULE_TITLE = "Unsupervised Learning and Preprocessing"

MODULE_DESCRIPTION = (
    "Learn how machine learning can discover structure without target labels, "
    "prepare features with scaling, reduce dimensionality, visualize complex "
    "data, and discover groups with clustering."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Not provided in extracted source text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Unsupervised Learning and Preprocessing",

    "slug": "ml-foundations-m03-l01",

    "description": (
        "Understand the main ideas of unsupervised learning, feature scaling, "
        "PCA, NMF, t-SNE, and clustering algorithms such as k-means, "
        "agglomerative clustering, and DBSCAN."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.5,

    "skill_tags": [
        "machine-learning",
        "unsupervised-learning",
        "preprocessing",
        "feature-scaling",
        "dimensionality-reduction",
        "pca",
        "nmf",
        "tsne",
        "clustering",
        "k-means",
        "dbscan",
        "module-03",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Unsupervised Learning and Preprocessing",

        "content": (
            "# Unsupervised Learning and Preprocessing\n"
            "\n"
            "> **Course:** Machine Learning Foundations  \n"
            "> **Lesson:** M03.L01  \n"
            "> **Module:** Unsupervised Learning and Preprocessing  \n"
            "> **Source alignment:** BOOK-001, Chapter 3. The extracted source "
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
            "- Explain how unsupervised learning differs from supervised learning.\n"
            "- Explain why feature scaling can be important before training some models.\n"
            "- Apply the training-set-first rule when fitting a scaler.\n"
            "- Explain the main idea behind PCA, NMF, and t-SNE.\n"
            "- Describe how k-means, agglomerative clustering, and DBSCAN form clusters.\n"
            "- Choose a reasonable unsupervised technique for a simple practical problem.\n"
            "- Explain why evaluating unsupervised learning is often difficult.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. What is unsupervised learning?\n"
            "\n"
            "In supervised learning, the training data includes both the inputs "
            "and the correct outputs. If we are predicting house prices, for "
            "example, the model receives information about each house together "
            "with its known price.\n"
            "\n"
            "Unsupervised learning is different. The algorithm receives the "
            "input data, but there is no known target value telling it what the "
            "correct answer should be.\n"
            "\n"
            "A useful mental model is:\n"
            "\n"
            "```text\n"
            "Supervised learning:\n"
            "X + y -> learn how to predict y\n"
            "\n"
            "Unsupervised learning:\n"
            "X only -> discover useful structure in X\n"
            "```\n"
            "\n"
            "The goal is therefore not necessarily to predict a label. Instead, "
            "we might want to find groups, discover patterns, create a more useful "
            "representation, compress the data, or visualize a high-dimensional "
            "dataset.\n"
            "\n"
            "### Example\n"
            "\n"
            "Imagine an online store with information about 100,000 customers:\n"
            "\n"
            "```text\n"
            "age\n"
            "amount spent\n"
            "number of purchases\n"
            "products viewed\n"
            "time on website\n"
            "```\n"
            "\n"
            "There may be no labels such as `premium customer`, `casual customer`, "
            "or `discount shopper`. A clustering algorithm can still try to find "
            "natural groups of customers based only on their behavior.\n"
            "\n"
            "### Two broad tasks in this chapter\n"
            "\n"
            "The chapter focuses on two broad families of unsupervised methods:\n"
            "\n"
            "```text\n"
            "Unsupervised learning\n"
            "|\n"
            "|-- Transformations\n"
            "|   |-- Scaling\n"
            "|   |-- PCA\n"
            "|   |-- NMF\n"
            "|   `-- t-SNE\n"
            "|\n"
            "`-- Clustering\n"
            "    |-- k-Means\n"
            "    |-- Agglomerative clustering\n"
            "    `-- DBSCAN\n"
            "```\n"
            "\n"
            "Transformations change how the data is represented. Clustering "
            "divides observations into groups of similar items.\n"
            "\n"
            "### Why evaluation is difficult\n"
            "\n"
            "Suppose you ask an algorithm to group face photographs. You hoped "
            "it would group photographs by person, but it instead groups them by "
            "whether the face is looking forward or sideways. The algorithm did "
            "discover structure, but it was not the structure you wanted.\n"
            "\n"
            "This is one of the central difficulties of unsupervised learning: "
            "there is often no single known correct answer against which the "
            "result can be compared.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Preprocessing and feature scaling\n"
            "\n"
            "Many machine learning algorithms are sensitive to the numerical "
            "scale of their input features. Consider a dataset containing age "
            "and annual salary:\n"
            "\n"
            "```text\n"
            "Age:     18 to 70\n"
            "Salary:  3,000 to 300,000\n"
            "```\n"
            "\n"
            "The salary feature contains much larger numbers. For algorithms "
            "that rely heavily on distances or numerical magnitudes, that "
            "difference can cause salary to dominate the calculation even when "
            "age is also important.\n"
            "\n"
            "Scaling changes the numerical representation so that features are "
            "on more comparable scales.\n"
            "\n"
            "### StandardScaler\n"
            "\n"
            "`StandardScaler` changes each feature so that its mean is zero and "
            "its variance is one. The exact transformed values depend on the "
            "training data, but the result is that features with very different "
            "original magnitudes become more comparable.\n"
            "\n"
            "```python\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "\n"
            "scaler = StandardScaler()\n"
            "X_train_scaled = scaler.fit_transform(X_train)\n"
            "X_test_scaled = scaler.transform(X_test)\n"
            "```\n"
            "\n"
            "### MinMaxScaler\n"
            "\n"
            "`MinMaxScaler` uses the minimum and maximum of each training "
            "feature. With the default feature range, training values are mapped "
            "between 0 and 1.\n"
            "\n"
            "For one value `x`, the basic idea is:\n"
            "\n"
            "```text\n"
            "scaled_x = (x - minimum) / (maximum - minimum)\n"
            "```\n"
            "\n"
            "If the minimum age is 20 and the maximum is 60, then age 40 becomes:\n"
            "\n"
            "```text\n"
            "(40 - 20) / (60 - 20) = 0.5\n"
            "```\n"
            "\n"
            "### RobustScaler\n"
            "\n"
            "`RobustScaler` uses the median and quartiles instead of statistics "
            "that are more strongly affected by extreme values. It is therefore "
            "useful when outliers are an important concern.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "3000, 3500, 4000, 4200, 4500, 1000000\n"
            "```\n"
            "\n"
            "The value `1000000` is very different from the rest. A robust "
            "scaling strategy is less influenced by such an extreme observation.\n"
            "\n"
            "### Normalizer\n"
            "\n"
            "`Normalizer` behaves differently from the previous scalers. It "
            "normalizes each individual sample so that its feature vector has "
            "length 1.\n"
            "\n"
            "For the vector `[3, 4]`, the Euclidean length is 5, so normalization "
            "produces:\n"
            "\n"
            "```text\n"
            "[3/5, 4/5] = [0.6, 0.8]\n"
            "```\n"
            "\n"
            "This is useful when the direction of a vector matters more than its "
            "magnitude.\n"
            "\n"
            "### The training-set-first rule\n"
            "\n"
            "This is one of the most important practical rules in preprocessing:\n"
            "\n"
            "```text\n"
            "Training data: fit + transform\n"
            "Test data:     transform only\n"
            "```\n"
            "\n"
            "Correct:\n"
            "\n"
            "```python\n"
            "scaler.fit(X_train)\n"
            "X_train_scaled = scaler.transform(X_train)\n"
            "X_test_scaled = scaler.transform(X_test)\n"
            "```\n"
            "\n"
            "Incorrect:\n"
            "\n"
            "```python\n"
            "train_scaler.fit(X_train)\n"
            "test_scaler.fit(X_test)  # Do not do this.\n"
            "```\n"
            "\n"
            "The test data must be transformed using exactly the same rule that "
            "was learned from the training data. Otherwise, the training and test "
            "sets would effectively use different coordinate systems.\n"
            "\n"
            "A test value can legitimately end up below 0 or above 1 after a "
            "`MinMaxScaler` transformation. That simply means the test value is "
            "outside the range observed in the training data.\n"
            "\n"
            "### Why scaling can matter\n"
            "\n"
            "In the chapter's breast-cancer SVM example, the unscaled model "
            "achieved a test accuracy of 0.63. After MinMax scaling, the test "
            "accuracy increased to 0.97. The lesson is not that scaling always "
            "creates exactly this improvement, but that some algorithms can be "
            "highly sensitive to feature scale.\n"
            "\n"

            "{{exercise:M03.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Dimensionality reduction and feature extraction\n"
            "\n"
            "Each input feature can be thought of as one dimension. A dataset "
            "with 500 features is therefore a 500-dimensional dataset.\n"
            "\n"
            "Humans cannot directly visualize 500 dimensions, and some of those "
            "features may contain overlapping or less useful information. "
            "Dimensionality reduction tries to create a smaller representation "
            "while preserving important structure.\n"
            "\n"
            "Common reasons include:\n"
            "\n"
            "- visualization,\n"
            "- data compression,\n"
            "- removing less useful variation,\n"
            "- and creating a representation that may be more useful for later processing.\n"
            "\n"
            "The chapter introduces PCA, NMF, and t-SNE as three important ways "
            "to transform high-dimensional data.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Principal Component Analysis (PCA)\n"
            "\n"
            "PCA finds new directions in the data called principal components. "
            "The first component captures the direction of greatest variance. "
            "The next component captures as much remaining variance as possible "
            "while being orthogonal to the previous component.\n"
            "\n"
            "### Intuition\n"
            "\n"
            "Imagine two-dimensional data arranged roughly along a diagonal:\n"
            "\n"
            "```text\n"
            "          *\n"
            "        *\n"
            "      *\n"
            "    *\n"
            "  *\n"
            "*\n"
            "```\n"
            "\n"
            "Although the data has an x-coordinate and a y-coordinate, most of "
            "its variation follows one diagonal direction. PCA can discover that "
            "direction and use it as the first principal component.\n"
            "\n"
            "If we keep only that component, we have reduced the data from two "
            "dimensions to one dimension while trying to retain the most "
            "important variation.\n"
            "\n"
            "### Principal components are combinations of original features\n"
            "\n"
            "A principal component is usually not one original feature. It is a "
            "weighted combination of several original features.\n"
            "\n"
            "For example, with four academic features, a component might look "
            "conceptually like:\n"
            "\n"
            "```text\n"
            "PC1 =\n"
            "0.50 * math\n"
            "+ 0.60 * physics\n"
            "+ 0.45 * chemistry\n"
            "+ 0.55 * engineering\n"
            "```\n"
            "\n"
            "The weights here are only an intuition example. PCA learns the real "
            "weights from the data.\n"
            "\n"
            "### PCA is unsupervised\n"
            "\n"
            "If `X` contains tumor measurements and `y` says whether each tumor "
            "is benign or malignant, PCA learns its components from `X`. It does "
            "not use `y` to decide the directions.\n"
            "\n"
            "Labels can later be used to color a visualization, but they were not "
            "used to learn the PCA transformation.\n"
            "\n"
            "### Example with scikit-learn\n"
            "\n"
            "```python\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.decomposition import PCA\n"
            "\n"
            "scaler = StandardScaler()\n"
            "X_scaled = scaler.fit_transform(X)\n"
            "\n"
            "pca = PCA(n_components=2)\n"
            "X_pca = pca.fit_transform(X_scaled)\n"
            "\n"
            "print(X.shape)\n"
            "print(X_pca.shape)\n"
            "```\n"
            "\n"
            "In the chapter's breast-cancer example, the representation changes "
            "from 569 samples with 30 features to 569 samples with 2 principal "
            "components. The number of samples stays the same; only the feature "
            "representation changes.\n"
            "\n"
            "### PCA for images\n"
            "\n"
            "An 87 by 65 grayscale image contains 5,655 pixel values. PCA can "
            "replace those raw pixel features with a smaller number of principal "
            "components. Keeping more components preserves more image detail; "
            "keeping fewer components produces a rougher reconstruction.\n"
            "\n"
            "This provides another useful mental model for PCA:\n"
            "\n"
            "```text\n"
            "Original high-dimensional data\n"
            "        |\n"
            "        v\n"
            "PCA representation\n"
            "        |\n"
            "        v\n"
            "Approximate reconstruction\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 5
            # ----------------------------------------------------------------

            "## 5. NMF and t-SNE\n"
            "\n"
            "PCA is not the only way to transform data. The chapter also "
            "introduces Non-Negative Matrix Factorization and t-SNE.\n"
            "\n"
            "### Non-Negative Matrix Factorization (NMF)\n"
            "\n"
            "NMF tries to represent each data point as a weighted combination of "
            "components, but it imposes an important restriction: the components "
            "and coefficients are non-negative.\n"
            "\n"
            "That means NMF is intended for data whose features are non-negative.\n"
            "\n"
            "A useful intuition is a mixed audio signal. Imagine hearing:\n"
            "\n"
            "```text\n"
            "vocals + guitar + drums\n"
            "```\n"
            "\n"
            "The observed signal is a combination of several sources. NMF can be "
            "useful when the data has this kind of additive structure and we want "
            "to discover components that make up the observations.\n"
            "\n"
            "Compared with PCA, NMF components can sometimes be easier to "
            "interpret because they do not rely on positive and negative "
            "components cancelling each other.\n"
            "\n"
            "### t-SNE\n"
            "\n"
            "t-SNE is mainly a visualization technique. It tries to create a "
            "low-dimensional representation, commonly two dimensions, in which "
            "points that were neighbors in the original feature space remain "
            "close to one another.\n"
            "\n"
            "It places more emphasis on preserving local neighborhoods than on "
            "perfectly preserving distances between far-away points.\n"
            "\n"
            "```python\n"
            "from sklearn.manifold import TSNE\n"
            "\n"
            "tsne = TSNE(random_state=42)\n"
            "X_tsne = tsne.fit_transform(X)\n"
            "```\n"
            "\n"
            "In the chapter's handwritten-digits example, a two-dimensional PCA "
            "representation contains substantial overlap between digit classes, "
            "while t-SNE produces much more clearly separated groups.\n"
            "\n"
            "However, the chapter emphasizes an important limitation: the "
            "discussed t-SNE workflow does not provide a normal `transform` method "
            "for unseen test data. It is mainly useful for exploratory "
            "visualization rather than as a general preprocessing transform for "
            "new observations.\n"
            "\n"
            "### PCA vs NMF vs t-SNE\n"
            "\n"
            "| Method | Main idea | Typical use |\n"
            "|---|---|---|\n"
            "| PCA | Keep important variance directions | Compression, preprocessing, visualization |\n"
            "| NMF | Find non-negative additive components | Interpretable component extraction |\n"
            "| t-SNE | Preserve local neighborhoods in a low-dimensional map | Visualization and exploration |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 6
            # ----------------------------------------------------------------

            "## 6. Clustering: discovering groups in data\n"
            "\n"
            "Clustering divides observations into groups called clusters. The "
            "general goal is for points within the same cluster to be similar "
            "and points in different clusters to be different.\n"
            "\n"
            "Cluster labels such as `0`, `1`, and `2` are identifiers only. "
            "Cluster 2 is not automatically better or larger than cluster 0.\n"
            "\n"
            "### k-Means clustering\n"
            "\n"
            "k-means is one of the simplest and most common clustering methods.\n"
            "\n"
            "The algorithm repeatedly performs two main steps:\n"
            "\n"
            "1. Assign every point to its closest cluster center.\n"
            "2. Move each center to the mean of the points assigned to it.\n"
            "\n"
            "The process repeats until the assignments stop changing.\n"
            "\n"
            "```python\n"
            "from sklearn.cluster import KMeans\n"
            "\n"
            "kmeans = KMeans(n_clusters=3, random_state=0)\n"
            "kmeans.fit(X)\n"
            "\n"
            "labels = kmeans.labels_\n"
            "```\n"
            "\n"
            "A strength of k-means is that every cluster has a meaningful center: "
            "the mean of the observations assigned to it.\n"
            "\n"
            "Important limitations include the need to choose the number of "
            "clusters and assumptions that work best for relatively simple "
            "cluster shapes. The result can also depend on initialization.\n"
            "\n"
            "### Agglomerative clustering\n"
            "\n"
            "Agglomerative clustering starts with every point as its own cluster. "
            "It repeatedly merges the two most similar clusters until the desired "
            "number of clusters remains.\n"
            "\n"
            "A simplified progression looks like:\n"
            "\n"
            "```text\n"
            "[A] [B] [C] [D] [E] [F]\n"
            "        |\n"
            "        v\n"
            "[AB] [C] [D] [EF]\n"
            "        |\n"
            "        v\n"
            "[ABC] [D] [EF]\n"
            "```\n"
            "\n"
            "This naturally creates a hierarchy of possible groupings. A "
            "dendrogram can visualize that hierarchy and show how clusters were "
            "merged.\n"
            "\n"
            "The chapter discusses several linkage criteria, including `ward`, "
            "`average`, and `complete`, which differ in how similarity between "
            "clusters is measured.\n"
            "\n"
            "One practical limitation is that the agglomerative workflow "
            "described in the chapter does not provide a `predict` method for "
            "assigning arbitrary new observations after fitting. Instead, "
            "`fit_predict` is used to obtain memberships for the fitted data.\n"
            "\n"
            "### DBSCAN\n"
            "\n"
            "DBSCAN is based on density. It looks for crowded regions of feature "
            "space separated by relatively empty regions.\n"
            "\n"
            "Its two central parameters are:\n"
            "\n"
            "- `eps`: the neighborhood radius.\n"
            "- `min_samples`: how many nearby samples are required for a point "
            "to count as a core point.\n"
            "\n"
            "DBSCAN distinguishes three conceptual kinds of points:\n"
            "\n"
            "```text\n"
            "core point     -> inside a dense region\n"
            "boundary point -> near a core point\n"
            "noise point    -> not assigned to a cluster\n"
            "```\n"
            "\n"
            "Major advantages are that the number of clusters does not need to be "
            "set directly, complex cluster shapes can be discovered, and unusual "
            "points can be labeled as noise.\n"
            "\n"
            "The value of `eps` strongly affects the result. A value that is too "
            "small may split the data into many clusters and noise points, while "
            "a value that is too large may merge distinct groups into one cluster.\n"
            "\n"
            "### Comparing the three methods\n"
            "\n"
            "| Algorithm | Mental model | Main strength | Important limitation |\n"
            "|---|---|---|---|\n"
            "| k-Means | Find centers | Simple, scalable, interpretable centers | Must choose `k`; limited cluster shapes |\n"
            "| Agglomerative | Repeatedly merge groups | Hierarchical structure | No normal prediction of new points in the described workflow |\n"
            "| DBSCAN | Find dense regions | Complex shapes and noise detection | Sensitive to density parameters |\n"
            "\n"

            "{{exercise:M03.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 7
            # ----------------------------------------------------------------

            "## 7. Evaluating clustering results\n"
            "\n"
            "Evaluating clustering is difficult because we often do not know the "
            "correct grouping in advance.\n"
            "\n"
            "When ground-truth grouping is available, the chapter discusses "
            "metrics such as the Adjusted Rand Index (ARI) and Normalized Mutual "
            "Information (NMI). These compare the discovered clustering with a "
            "known grouping without requiring the numeric cluster identifiers to "
            "match exactly.\n"
            "\n"
            "This matters because these two outputs can represent the same grouping:\n"
            "\n"
            "```text\n"
            "Ground truth:    [0, 0, 1, 1]\n"
            "Cluster output:  [1, 1, 0, 0]\n"
            "```\n"
            "\n"
            "The label numbers are swapped, but the partition is identical.\n"
            "\n"
            "When no ground truth exists, evaluation becomes more qualitative. "
            "The usefulness of the clusters often depends on whether the "
            "discovered structure helps us understand the real problem.\n"
            "\n"
            "This is why unsupervised learning is especially valuable during "
            "exploratory data analysis: it helps us inspect structure that may "
            "not have been obvious beforehand.\n"
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
            "> Unsupervised learning automatically discovers the one true grouping "
            "of the data.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A dataset can contain several valid kinds of structure. Faces could "
            "be grouped by identity, lighting, orientation, expression, or other "
            "properties. The algorithm can discover mathematically meaningful "
            "structure that is not useful for your goal.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> The test set should be fitted with its own scaler so that it also "
            "falls perfectly into the desired range.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Training and test data must use the same transformation. Fit the "
            "scaler on the training set and only transform the test set.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> PCA simply chooses the most important original columns.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "PCA creates new axes that are usually combinations of many original "
            "features. A principal component is generally not identical to one "
            "input feature.\n"
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
            "| Unsupervised learning | Learning structure from input data without known target labels |\n"
            "| Scaling | Changing numerical feature ranges or statistical scale |\n"
            "| Outlier | An observation that is unusually different from most of the data |\n"
            "| Dimensionality | The number of features used to represent each observation |\n"
            "| Principal component | A new PCA direction formed from the original features |\n"
            "| NMF | A decomposition using non-negative components and coefficients |\n"
            "| t-SNE | A nonlinear method mainly used to visualize local neighborhood structure |\n"
            "| Cluster | A group of observations considered similar by a clustering algorithm |\n"
            "| Cluster center | Representative mean used by k-means |\n"
            "| Dendrogram | Tree-like visualization of hierarchical cluster merging |\n"
            "| Core point | A DBSCAN point lying in a sufficiently dense neighborhood |\n"
            "| Noise point | A DBSCAN observation that is not assigned to a cluster |\n"
            "| ARI | Adjusted Rand Index, a metric for comparing clusterings when reference labels exist |\n"
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
            "1. What is missing from an unsupervised learning dataset compared "
            "with a typical supervised learning dataset?\n"
            "2. Why should a scaler be fitted on `X_train` but not separately on "
            "`X_test`?\n"
            "3. What information does the first principal component try to capture?\n"
            "4. Why is t-SNE used mainly for visualization in this chapter?\n"
            "5. How does k-means update its cluster centers?\n"
            "6. What is the main difference between k-means and DBSCAN when "
            "handling noise points?\n"
            "7. Why can a clustering result be mathematically reasonable but "
            "still unhelpful for the real problem?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**Unsupervised learning does not receive the correct target answer. "
            "Its job is to reveal useful structure or create a better "
            "representation of the data, so the value of the result depends on "
            "whether that discovered structure helps us understand or solve the "
            "problem.**\n"
        ),

        "estimated_minutes": 150,

        "has_code_examples": True,

        "sections": [
            {
                "id": "unsupervised-learning",
                "title": "What is unsupervised learning?",
                "order": 1,
            },
            {
                "id": "preprocessing-scaling",
                "title": "Preprocessing and feature scaling",
                "order": 2,
            },
            {
                "id": "dimensionality-reduction",
                "title": "Dimensionality reduction and feature extraction",
                "order": 3,
            },
            {
                "id": "pca",
                "title": "Principal Component Analysis (PCA)",
                "order": 4,
            },
            {
                "id": "nmf-tsne",
                "title": "NMF and t-SNE",
                "order": 5,
            },
            {
                "id": "clustering",
                "title": "Clustering: discovering groups in data",
                "order": 6,
            },
            {
                "id": "evaluating-clustering",
                "title": "Evaluating clustering results",
                "order": 7,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M03.L01.EX01",

            "title": "Scale Training and Test Data Correctly",

            "lesson_code": "M03.L01",

            "section_id": "preprocessing-scaling",

            "placement": "after_section",

            "description": (
                "Practice the correct train-first preprocessing workflow and "
                "interpret why the same fitted scaler must be reused on test data."
            ),

            "instructions": (
                "1. Create a small dataset with two features whose numerical "
                "ranges are very different.\n"
                "2. Split the dataset into training and test sets.\n"
                "3. Fit a StandardScaler or MinMaxScaler on X_train only.\n"
                "4. Transform both X_train and X_test using that fitted scaler.\n"
                "5. Print the feature ranges before and after scaling.\n"
                "6. Explain why fitting another scaler separately on X_test would "
                "make the evaluation inconsistent."
            ),

            "expected_output": (
                "A short Python notebook or script showing the original and "
                "scaled feature values, followed by a written explanation of "
                "why the scaler is fitted only on training data."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "feature-scaling",
                "train-test-preprocessing",
                "interpretation",
            ],
        },

        {
            "id": "M03.L01.EX02",

            "title": "Choose the Right Unsupervised Technique",

            "lesson_code": "M03.L01",

            "section_id": "clustering",

            "placement": "after_section",

            "description": (
                "Practice selecting between PCA, t-SNE, k-means, agglomerative "
                "clustering, and DBSCAN for different practical goals."
            ),

            "instructions": (
                "For each scenario below, choose one technique from PCA, t-SNE, "
                "k-means, agglomerative clustering, or DBSCAN, then justify your "
                "choice.\n"
                "1. Reduce 200 features to 20 features before another model.\n"
                "2. Visualize a complicated 64-dimensional handwritten-digit dataset.\n"
                "3. Group customers into exactly five segments with representative centers.\n"
                "4. Find irregularly shaped geographic groups while allowing isolated "
                "points to remain unclustered.\n"
                "5. Explore a hierarchy of possible cluster groupings using a dendrogram."
            ),

            "expected_output": (
                "A five-row table containing the scenario, selected technique, "
                "and a one- or two-sentence justification for each choice."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "algorithm-selection",
                "dimensionality-reduction",
                "clustering",
                "reasoning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M03.L01.QZ01",

        "title": "Unsupervised Learning and Preprocessing — Knowledge Check",

        "lesson_code": "M03.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M03.L01.Q01",

                "section_id": "unsupervised-learning",

                "question": (
                    "What most directly distinguishes the unsupervised learning "
                    "setting introduced in this lesson?"
                ),

                "options": [
                    "The model receives input features but no known target labels",
                    "The model is not allowed to use numerical data",
                    "The model always predicts continuous values",
                    "The model must contain neural-network layers",
                ],

                "correct": 0,

                "explanation": (
                    "Unsupervised learning receives the input data without a "
                    "known target output telling the algorithm the correct answer."
                ),
            },

            {
                "id": "M03.L01.Q02",

                "section_id": "preprocessing-scaling",

                "question": (
                    "Which preprocessing workflow correctly handles training "
                    "and test data?"
                ),

                "options": [
                    "Fit one scaler on X_train and another scaler on X_test",
                    "Fit the scaler on the full dataset before splitting",
                    "Fit the scaler on X_train, then transform both X_train and X_test with it",
                    "Scale only X_test because training data should remain unchanged",
                ],

                "correct": 2,

                "explanation": (
                    "The transformation must be learned from the training data. "
                    "The same fitted scaler is then applied to both training and "
                    "test inputs."
                ),
            },

            {
                "id": "M03.L01.Q03",

                "section_id": "pca",

                "question": (
                    "What does the first principal component primarily represent?"
                ),

                "options": [
                    "A new direction that captures the greatest variance in the data",
                    "The original feature with the largest numerical values",
                    "The target label with the highest frequency",
                    "The cluster containing the most observations",
                ],

                "correct": 0,

                "explanation": (
                    "PCA creates new directions from combinations of the original "
                    "features. The first principal component captures the "
                    "direction of greatest variance."
                ),
            },

            {
                "id": "M03.L01.Q04",

                "section_id": "clustering",

                "question": (
                    "Which property is a major advantage of DBSCAN compared with "
                    "k-means in the chapter?"
                ),

                "options": [
                    "It always creates equally sized clusters",
                    "It requires the exact number of clusters in advance",
                    "It always produces a meaningful cluster center",
                    "It can discover complex cluster shapes and label some points as noise",
                ],

                "correct": 3,

                "explanation": (
                    "DBSCAN groups points by density. It can follow irregular "
                    "cluster shapes and can leave isolated points unassigned as "
                    "noise rather than forcing every point into a cluster."
                ),
            },

            {
                "id": "M03.L01.Q05",

                "section_id": "evaluating-clustering",

                "type": "open",

                "question": (
                    "A clustering algorithm groups a collection of face images "
                    "mainly by lighting and head orientation, but your goal was "
                    "to group the images by person. Explain why the clustering "
                    "may still be mathematically meaningful and why it is not "
                    "useful for your intended task."
                ),
            },
        ],

        "passing_score": 70,
    },
}
