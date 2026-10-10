"""M01.L08 — Unsupervised Learning Techniques.

One source chapter -> one complete learner-facing lesson + inline Images +
inline Exercises + lesson Quiz.

Source alignment: Chapter 8 supplied by the course author.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L08"

MODULE_ORDER = 1

MODULE_TITLE = "Unsupervised Learning Techniques"

MODULE_DESCRIPTION = (
    "Learn how to discover useful structure in unlabeled data using k-means, "
    "DBSCAN, Gaussian mixture models, density estimation, semi-supervised "
    "labeling strategies, and anomaly detection."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Unsupervised Learning Techniques",

    "slug": "machine-learning-foundations-m01-l08",

    "description": (
        "A practical lesson covering clustering, k-means, cluster selection, "
        "semi-supervised learning, active learning, DBSCAN, Gaussian mixture "
        "models, density estimation, anomaly detection, and unsupervised model "
        "selection."
    ),

    "order": 8,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 5.0,

    "skill_tags": [
        "machine-learning",
        "unsupervised-learning",
        "clustering",
        "k-means",
        "dbscan",
        "gaussian-mixtures",
        "anomaly-detection",
        "semi-supervised-learning",
        "active-learning",
        "density-estimation",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L07",
    ],


    # =======================================================================
    # INLINE IMAGE RULES
    # =======================================================================
    #
    # Only high-value source figures are requested below. Each request
    # preserves the original source figure number and includes a stable key.
    #
    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Unsupervised Learning Techniques",

        "content": (
            "# Unsupervised Learning Techniques\n"
            "\n"
            "> **Course:** Applied Machine Learning with Scikit-Learn  \n"
            "> **Lesson:** M01.L08  \n"
            "> **Module:** Unsupervised Learning Techniques  \n"
            "> **Source alignment:** Chapter 8, “Unsupervised Learning Techniques,” supplied by the course author. Page numbers were not included in the supplied extract. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain how unsupervised learning differs from supervised learning.\n"
            "- Describe clustering, anomaly detection, novelty detection, and density estimation.\n"
            "- Explain how k-means assigns instances to centroids and how the algorithm iteratively updates them.\n"
            "- Distinguish hard clustering from soft cluster representations.\n"
            "- Explain why centroid initialization matters and how k-means++ reduces poor initializations.\n"
            "- Use inertia, the elbow method, silhouette score, and silhouette diagrams to reason about the number of clusters.\n"
            "- Recognize when k-means is a poor fit because clusters are nonspherical, differently sized, or differently dense.\n"
            "- Use clustering for image segmentation and semi-supervised label selection/propagation.\n"
            "- Explain active learning and uncertainty sampling.\n"
            "- Explain how DBSCAN identifies clusters using local density, core instances, neighborhoods, and anomalies.\n"
            "- Describe Gaussian mixture models as probabilistic soft-clustering and density-estimation models.\n"
            "- Explain the expectation-maximization intuition behind Gaussian mixtures.\n"
            "- Use Gaussian mixtures for anomaly detection.\n"
            "- Choose the number of Gaussian components using AIC or BIC.\n"
            "- Distinguish anomaly detection from novelty detection and identify alternative algorithms for each.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. Learning from data without labels\n"
            "\n"
            "Most real-world data is not labeled.\n"
            "\n"
            "You may have:\n"
            "\n"
            "```text\n"
            "X = input features\n"
            "```\n"
            "\n"
            "without:\n"
            "\n"
            "```text\n"
            "y = target labels\n"
            "```\n"
            "\n"
            "This makes **unsupervised learning** valuable.\n"
            "\n"
            "Instead of learning a direct mapping:\n"
            "\n"
            "```text\n"
            "X -> y\n"
            "```\n"
            "\n"
            "the algorithm tries to discover structure in:\n"
            "\n"
            "```text\n"
            "X\n"
            "```\n"
            "\n"
            "itself.\n"
            "\n"
            "The chapter focuses on three major tasks.\n"
            "\n"
            "### Clustering\n"
            "\n"
            "Group similar instances together.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- customer segmentation,\n"
            "- grouping similar documents or images,\n"
            "- search and recommendation,\n"
            "- data exploration,\n"
            "- feature engineering.\n"
            "\n"
            "### Anomaly detection\n"
            "\n"
            "Learn what normal data looks like and identify unusual examples.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- fraud,\n"
            "- defective products,\n"
            "- suspicious network activity,\n"
            "- strange sensor readings,\n"
            "- outlier removal before model training.\n"
            "\n"
            "Normal examples are often called:\n"
            "\n"
            "```text\n"
            "inliers\n"
            "```\n"
            "\n"
            "Unusual examples are:\n"
            "\n"
            "```text\n"
            "anomalies\n"
            "or\n"
            "outliers\n"
            "```\n"
            "\n"
            "### Density estimation\n"
            "\n"
            "Estimate how densely data is distributed throughout feature space.\n"
            "\n"
            "High-density regions:\n"
            "\n"
            "```text\n"
            "many plausible observations\n"
            "```\n"
            "\n"
            "Low-density regions:\n"
            "\n"
            "```text\n"
            "rare / unusual observations\n"
            "```\n"
            "\n"
            "Density estimation naturally connects to anomaly detection.\n"
            "\n"
            "### Classification versus clustering\n"
            "\n"
            "Classification has labeled targets.\n"
            "\n"
            "Clustering does not.\n"
            "\n"
            "{{image:classification-vs-clustering}}\n"
            "\n"
            "A cluster is not a universal mathematical object.\n"
            "\n"
            "Different algorithms define clusters differently:\n"
            "\n"
            "```text\n"
            "k-means:\n"
            "points near a centroid\n"
            "\n"
            "DBSCAN:\n"
            "connected regions of high density\n"
            "\n"
            "Gaussian mixture:\n"
            "points likely generated by the same probability distribution\n"
            "```\n"
            "\n"
            "So the “best” clustering algorithm depends on what structure you expect the data to contain.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. k-means: clustering around centroids\n"
            "\n"
            "**k-means** is one of the most widely used clustering algorithms.\n"
            "\n"
            "You must choose the number of clusters:\n"
            "\n"
            "```text\n"
            "k\n"
            "```\n"
            "\n"
            "The model then learns:\n"
            "\n"
            "```text\n"
            "k centroids\n"
            "```\n"
            "\n"
            "and assigns each instance to its nearest centroid.\n"
            "\n"
            "### Basic Scikit-Learn usage\n"
            "\n"
            "```python\n"
            "from sklearn.cluster import KMeans\n"
            "from sklearn.datasets import make_blobs\n"
            "\n"
            "X, _ = make_blobs(\n"
            "    n_samples=1000,\n"
            "    centers=5,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "kmeans = KMeans(\n"
            "    n_clusters=5,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "y_pred = kmeans.fit_predict(X)\n"
            "```\n"
            "\n"
            "The cluster assignments are also stored in:\n"
            "\n"
            "```python\n"
            "kmeans.labels_\n"
            "```\n"
            "\n"
            "The learned centroids are:\n"
            "\n"
            "```python\n"
            "kmeans.cluster_centers_\n"
            "```\n"
            "\n"
            "### Predict clusters for new instances\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "\n"
            "X_new = np.array([\n"
            "    [0, 2],\n"
            "    [3, 2],\n"
            "    [-3, 3],\n"
            "    [-3, 2.5],\n"
            "])\n"
            "\n"
            "kmeans.predict(X_new)\n"
            "```\n"
            "\n"
            "Each new instance is assigned to the nearest centroid.\n"
            "\n"
            "### Hard clustering\n"
            "\n"
            "A standard `predict()` call produces one cluster index:\n"
            "\n"
            "```text\n"
            "instance -> cluster 2\n"
            "```\n"
            "\n"
            "This is **hard clustering**.\n"
            "\n"
            "### Soft cluster representation\n"
            "\n"
            "Sometimes one cluster ID throws away useful information.\n"
            "\n"
            "Instead, measure each instance’s distance to every centroid:\n"
            "\n"
            "```python\n"
            "kmeans.transform(X_new)\n"
            "```\n"
            "\n"
            "An instance can then be represented as:\n"
            "\n"
            "```text\n"
            "distance to cluster 1\n"
            "distance to cluster 2\n"
            "distance to cluster 3\n"
            "...\n"
            "```\n"
            "\n"
            "This is useful for:\n"
            "\n"
            "- feature engineering,\n"
            "- nonlinear dimensionality reduction,\n"
            "- downstream supervised learning.\n"
            "\n"
            "It gives a richer representation than one hard cluster label.\n"
            "\n"
            "---\n"
            "\n"
            "## 3. How k-means actually learns\n"
            "\n"
            "Suppose the centroids were already known.\n"
            "\n"
            "Then assigning every instance is easy:\n"
            "\n"
            "```text\n"
            "assign each point to nearest centroid\n"
            "```\n"
            "\n"
            "Suppose instead the cluster memberships were known.\n"
            "\n"
            "Then finding each centroid is easy:\n"
            "\n"
            "```text\n"
            "centroid = mean of all points in that cluster\n"
            "```\n"
            "\n"
            "But initially, neither is known.\n"
            "\n"
            "k-means solves this by alternating between these two easy steps.\n"
            "\n"
            "### k-means algorithm\n"
            "\n"
            "1. Choose `k` initial centroids.\n"
            "2. Assign every instance to its nearest centroid.\n"
            "3. Recompute each centroid as the mean of its assigned instances.\n"
            "4. Reassign all instances.\n"
            "5. Update centroids again.\n"
            "6. Repeat until the centroids stop moving.\n"
            "\n"
            "{{image:kmeans-iterative-algorithm}}\n"
            "\n"
            "The objective improves at every iteration because the total squared distance to the closest centroids cannot keep increasing.\n"
            "\n"
            "Eventually the algorithm converges.\n"
            "\n"
            "### Convergence does not guarantee the best solution\n"
            "\n"
            "The initial centroids matter.\n"
            "\n"
            "Different random starting positions can lead to different final clusters.\n"
            "\n"
            "{{image:kmeans-initialization-local-optima}}\n"
            "\n"
            "### Inertia\n"
            "\n"
            "k-means evaluates a solution using **inertia**:\n"
            "\n"
            "```text\n"
            "sum of squared distances\n"
            "from every instance\n"
            "to its nearest centroid\n"
            "```\n"
            "\n"
            "In Scikit-Learn:\n"
            "\n"
            "```python\n"
            "kmeans.inertia_\n"
            "```\n"
            "\n"
            "Lower inertia means clusters are tighter around their centroids.\n"
            "\n"
            "But inertia should not be interpreted in isolation.\n"
            "\n"
            "### Multiple initializations\n"
            "\n"
            "One strategy is:\n"
            "\n"
            "```text\n"
            "run k-means several times\n"
            "with different initial centroids\n"
            "keep the solution with lowest inertia\n"
            "```\n"
            "\n"
            "Scikit-Learn manages this using initialization behavior and `n_init`.\n"
            "\n"
            "### k-means++\n"
            "\n"
            "A better strategy is **k-means++**.\n"
            "\n"
            "Instead of choosing all initial centroids completely at random, it spreads them out.\n"
            "\n"
            "Points far from already selected centroids are more likely to become new initial centroids.\n"
            "\n"
            "This makes it much more likely that distinct cluster regions receive their own starting centroid.\n"
            "\n"
            "In Scikit-Learn:\n"
            "\n"
            "```python\n"
            "KMeans(\n"
            "    n_clusters=5,\n"
            "    init=\"k-means++\",\n"
            ")\n"
            "```\n"
            "\n"
            "is the standard choice.\n"
            "\n"
            "### Mini-batch k-means\n"
            "\n"
            "For large datasets, use:\n"
            "\n"
            "```python\n"
            "from sklearn.cluster import MiniBatchKMeans\n"
            "\n"
            "minibatch_kmeans = MiniBatchKMeans(\n"
            "    n_clusters=5,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "minibatch_kmeans.fit(X)\n"
            "```\n"
            "\n"
            "Instead of processing the full dataset on every update, it uses mini-batches.\n"
            "\n"
            "Benefits:\n"
            "\n"
            "- faster updates,\n"
            "- lower memory requirements,\n"
            "- practical for very large datasets.\n"
            "\n"
            "The trade-off is that the final solution may be slightly less precise than full batch k-means.\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Choosing the number of clusters\n"
            "\n"
            "k-means requires:\n"
            "\n"
            "```text\n"
            "k = number of clusters\n"
            "```\n"
            "\n"
            "But real datasets rarely tell you the correct value.\n"
            "\n"
            "Choosing too few clusters merges distinct groups.\n"
            "\n"
            "Choosing too many clusters splits meaningful groups.\n"
            "\n"
            "### Why minimum inertia is not enough\n"
            "\n"
            "As `k` increases:\n"
            "\n"
            "```text\n"
            "centroids become more numerous\n"
            "points become closer to some centroid\n"
            "inertia decreases\n"
            "```\n"
            "\n"
            "So simply choosing the `k` with the smallest inertia would push you toward more and more clusters.\n"
            "\n"
            "That does not solve the problem.\n"
            "\n"
            "### Elbow method\n"
            "\n"
            "Plot:\n"
            "\n"
            "```text\n"
            "k\n"
            "against\n"
            "inertia\n"
            "```\n"
            "\n"
            "Often the curve drops quickly, then starts flattening.\n"
            "\n"
            "The transition resembles an elbow.\n"
            "\n"
            "{{image:kmeans-elbow-method}}\n"
            "\n"
            "The elbow is a reasonable candidate for `k`.\n"
            "\n"
            "But it can be subjective.\n"
            "\n"
            "### Silhouette coefficient\n"
            "\n"
            "A more informative metric is the **silhouette coefficient**.\n"
            "\n"
            "For one instance:\n"
            "\n"
            "```text\n"
            "a = average distance to instances in its own cluster\n"
            "b = average distance to instances in the nearest other cluster\n"
            "```\n"
            "\n"
            "Then:\n"
            "\n"
            "```text\n"
            "silhouette = (b - a) / max(a, b)\n"
            "```\n"
            "\n"
            "Interpretation:\n"
            "\n"
            "```text\n"
            "close to +1\n"
            "-> well inside its own cluster\n"
            "\n"
            "close to 0\n"
            "-> near a cluster boundary\n"
            "\n"
            "close to -1\n"
            "-> possibly assigned to wrong cluster\n"
            "```\n"
            "\n"
            "Compute the mean score:\n"
            "\n"
            "```python\n"
            "from sklearn.metrics import silhouette_score\n"
            "\n"
            "score = silhouette_score(\n"
            "    X,\n"
            "    kmeans.labels_,\n"
            ")\n"
            "\n"
            "print(score)\n"
            "```\n"
            "\n"
            "### Silhouette diagrams\n"
            "\n"
            "A single mean score still hides cluster-specific problems.\n"
            "\n"
            "A silhouette diagram shows the distribution of silhouette coefficients for every cluster.\n"
            "\n"
            "{{image:silhouette-diagram-cluster-selection}}\n"
            "\n"
            "This can reveal:\n"
            "\n"
            "- clusters that are poorly separated,\n"
            "- imbalanced cluster sizes,\n"
            "- many borderline points,\n"
            "- a value of `k` that is statistically good but practically awkward.\n"
            "\n"
            "### No metric replaces domain meaning\n"
            "\n"
            "A cluster should be useful for the task.\n"
            "\n"
            "For customer segmentation, for example:\n"
            "\n"
            "```text\n"
            "k = 20\n"
            "```\n"
            "\n"
            "might produce a slightly better mathematical score but be too many segments for a marketing team to act on.\n"
            "\n"
            "Always combine metrics with use-case requirements.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Limits and practical applications of k-means\n"
            "\n"
            "k-means is:\n"
            "\n"
            "- fast,\n"
            "- scalable,\n"
            "- simple,\n"
            "- effective for compact centroid-shaped clusters.\n"
            "\n"
            "But it has assumptions.\n"
            "\n"
            "### Where k-means struggles\n"
            "\n"
            "k-means can perform poorly when clusters have:\n"
            "\n"
            "- different sizes,\n"
            "- different densities,\n"
            "- elongated shapes,\n"
            "- curved or irregular shapes.\n"
            "\n"
            "{{image:kmeans-nonspherical-cluster-failure}}\n"
            "\n"
            "Another important requirement:\n"
            "\n"
            "> Scale numerical features before k-means when their numeric ranges are very different.\n"
            "\n"
            "Distance drives k-means.\n"
            "\n"
            "If one feature ranges from:\n"
            "\n"
            "```text\n"
            "0 to 100,000\n"
            "```\n"
            "\n"
            "and another from:\n"
            "\n"
            "```text\n"
            "0 to 1\n"
            "```\n"
            "\n"
            "the large-scale feature can dominate Euclidean distance.\n"
            "\n"
            "### Application: image color segmentation\n"
            "\n"
            "An RGB image can be reshaped so every pixel becomes:\n"
            "\n"
            "```text\n"
            "[R, G, B]\n"
            "```\n"
            "\n"
            "Then cluster these colors.\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "import PIL\n"
            "from sklearn.cluster import KMeans\n"
            "\n"
            "image = np.asarray(\n"
            "    PIL.Image.open(filepath)\n"
            ")\n"
            "\n"
            "X_pixels = image.reshape(-1, 3)\n"
            "\n"
            "kmeans = KMeans(\n"
            "    n_clusters=8,\n"
            "    random_state=42,\n"
            ").fit(X_pixels)\n"
            "\n"
            "segmented_img = (\n"
            "    kmeans.cluster_centers_[\n"
            "        kmeans.labels_\n"
            "    ]\n"
            ")\n"
            "\n"
            "segmented_img = segmented_img.reshape(\n"
            "    image.shape\n"
            ")\n"
            "```\n"
            "\n"
            "Every original pixel is replaced by its cluster’s mean color.\n"
            "\n"
            "{{image:kmeans-color-segmentation}}\n"
            "\n"
            "This demonstrates that clustering can transform data, not only label it.\n"
            "\n"
            "---\n"
            "\n"
            "## 6. Clustering for semi-supervised and active learning\n"
            "\n"
            "Clustering can reduce the cost of labeling data.\n"
            "\n"
            "Suppose you have:\n"
            "\n"
            "```text\n"
            "many unlabeled examples\n"
            "few labels\n"
            "```\n"
            "\n"
            "Instead of randomly choosing examples for manual labeling, find representative examples.\n"
            "\n"
            "### Label representative instances\n"
            "\n"
            "The chapter clusters a digits dataset into 50 clusters.\n"
            "\n"
            "```python\n"
            "from sklearn.cluster import KMeans\n"
            "\n"
            "k = 50\n"
            "\n"
            "kmeans = KMeans(\n"
            "    n_clusters=k,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "X_digits_dist = kmeans.fit_transform(\n"
            "    X_train\n"
            ")\n"
            "\n"
            "representative_idx = (\n"
            "    X_digits_dist.argmin(axis=0)\n"
            ")\n"
            "\n"
            "X_representative = (\n"
            "    X_train[representative_idx]\n"
            ")\n"
            "```\n"
            "\n"
            "Each selected image is the training instance closest to one centroid.\n"
            "\n"
            "{{image:cluster-representative-labeling}}\n"
            "\n"
            "The source result illustrates the value:\n"
            "\n"
            "```text\n"
            "50 random labeled instances\n"
            "-> about 75.8% classifier accuracy\n"
            "\n"
            "50 representative labeled instances\n"
            "-> about 83.4%\n"
            "```\n"
            "\n"
            "Same labeling budget.\n"
            "\n"
            "Better label selection.\n"
            "\n"
            "### Label propagation\n"
            "\n"
            "After manually labeling the representative instance from each cluster, propagate that label to the other instances in that cluster.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "cluster centroid example labeled \"7\"\n"
            "        |\n"
            "propagate label\n"
            "        |\n"
            "nearby members also receive \"7\"\n"
            "```\n"
            "\n"
            "This creates many more pseudo-labeled examples.\n"
            "\n"
            "The source reports another accuracy increase.\n"
            "\n"
            "### Partial label propagation\n"
            "\n"
            "Do not blindly trust every cluster member.\n"
            "\n"
            "Instances far from the centroid may be:\n"
            "\n"
            "- borderline cases,\n"
            "- outliers,\n"
            "- poorly represented by the cluster.\n"
            "\n"
            "One strategy is to propagate labels only to the closest fraction of instances.\n"
            "\n"
            "The source keeps only the closest 50% within each cluster and gets still better performance.\n"
            "\n"
            "### Active learning\n"
            "\n"
            "**Active learning** takes this one step further.\n"
            "\n"
            "Instead of humans labeling random examples, the model asks for labels on examples that are especially informative.\n"
            "\n"
            "A common strategy is **uncertainty sampling**:\n"
            "\n"
            "1. train on currently labeled instances,\n"
            "2. predict on unlabeled instances,\n"
            "3. find the examples where the model is least confident,\n"
            "4. ask an expert to label them,\n"
            "5. retrain,\n"
            "6. repeat until additional labeling is no longer worth the effort.\n"
            "\n"
            "This focuses human attention where labels are most valuable.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. DBSCAN: find clusters using density\n"
            "\n"
            "k-means defines clusters around centroids.\n"
            "\n"
            "**DBSCAN** takes a completely different approach:\n"
            "\n"
            "> A cluster is a connected region of high local density.\n"
            "\n"
            "DBSCAN uses two key hyperparameters:\n"
            "\n"
            "```text\n"
            "eps\n"
            "min_samples\n"
            "```\n"
            "\n"
            "### Epsilon neighborhood\n"
            "\n"
            "For each instance, consider all points within distance:\n"
            "\n"
            "```text\n"
            "eps\n"
            "```\n"
            "\n"
            "This region is the instance’s **epsilon neighborhood**.\n"
            "\n"
            "### Core instance\n"
            "\n"
            "An instance is a **core instance** if its epsilon neighborhood contains at least:\n"
            "\n"
            "```text\n"
            "min_samples\n"
            "```\n"
            "\n"
            "instances, including itself.\n"
            "\n"
            "Core instances represent dense regions.\n"
            "\n"
            "### Expand connected dense regions\n"
            "\n"
            "If one core instance is near another core instance, they become part of the same cluster.\n"
            "\n"
            "Long chains of connected core points can produce:\n"
            "\n"
            "- curved clusters,\n"
            "- irregular clusters,\n"
            "- non-centroid-shaped clusters.\n"
            "\n"
            "### Anomalies\n"
            "\n"
            "An instance that:\n"
            "\n"
            "```text\n"
            "is not a core instance\n"
            "and\n"
            "is not close enough to a core instance\n"
            "```\n"
            "\n"
            "is labeled as an anomaly.\n"
            "\n"
            "In Scikit-Learn, anomalies receive:\n"
            "\n"
            "```text\n"
            "-1\n"
            "```\n"
            "\n"
            "### Example\n"
            "\n"
            "```python\n"
            "from sklearn.cluster import DBSCAN\n"
            "from sklearn.datasets import make_moons\n"
            "\n"
            "X, _ = make_moons(\n"
            "    n_samples=1000,\n"
            "    noise=0.05,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "dbscan = DBSCAN(\n"
            "    eps=0.2,\n"
            "    min_samples=5,\n"
            ")\n"
            "\n"
            "dbscan.fit(X)\n"
            "```\n"
            "\n"
            "{{image:dbscan-eps-comparison}}\n"
            "\n"
            "### Why DBSCAN is powerful\n"
            "\n"
            "It can discover:\n"
            "\n"
            "- arbitrary cluster shapes,\n"
            "- the number of clusters automatically,\n"
            "- anomalies naturally.\n"
            "\n"
            "Unlike k-means, it does not need:\n"
            "\n"
            "```text\n"
            "k\n"
            "```\n"
            "\n"
            "in advance.\n"
            "\n"
            "### Where DBSCAN struggles\n"
            "\n"
            "DBSCAN has problems when:\n"
            "\n"
            "- cluster densities differ significantly,\n"
            "- low-density gaps between clusters are weak,\n"
            "- the dataset is very large.\n"
            "\n"
            "Its performance also depends heavily on choosing meaningful:\n"
            "\n"
            "```text\n"
            "eps\n"
            "and\n"
            "min_samples\n"
            "```\n"
            "\n"
            "### Predicting new instances\n"
            "\n"
            "Scikit-Learn’s `DBSCAN` does not provide a standard `predict()` method.\n"
            "\n"
            "One practical solution is to train another classifier, such as k-NN, on the learned core instances.\n"
            "\n"
            "This emphasizes an important distinction:\n"
            "\n"
            "> Clustering the training data and assigning future data are not always the same algorithmic task.\n"
            "\n"
            "---\n"
            "\n"
            "## 8. Gaussian mixtures: soft probabilistic clustering\n"
            "\n"
            "k-means assumes each instance belongs to the closest centroid.\n"
            "\n"
            "But real clusters may have:\n"
            "\n"
            "- different sizes,\n"
            "- different orientations,\n"
            "- different covariance structures,\n"
            "- overlapping regions.\n"
            "\n"
            "A **Gaussian mixture model (GMM)** assumes data was generated from a mixture of several Gaussian distributions.\n"
            "\n"
            "Each component has:\n"
            "\n"
            "- a mean,\n"
            "- a covariance matrix,\n"
            "- a mixture weight.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "choose Gaussian component\n"
            "        |\n"
            "sample a point from that Gaussian\n"
            "        |\n"
            "observed instance\n"
            "```\n"
            "\n"
            "The component index is hidden.\n"
            "\n"
            "The model must infer it.\n"
            "\n"
            "### Fit a Gaussian mixture\n"
            "\n"
            "```python\n"
            "from sklearn.mixture import GaussianMixture\n"
            "\n"
            "gm = GaussianMixture(\n"
            "    n_components=3,\n"
            "    n_init=10,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "gm.fit(X)\n"
            "```\n"
            "\n"
            "Learned values include:\n"
            "\n"
            "```python\n"
            "gm.weights_\n"
            "gm.means_\n"
            "gm.covariances_\n"
            "```\n"
            "\n"
            "### Hard clustering\n"
            "\n"
            "```python\n"
            "gm.predict(X)\n"
            "```\n"
            "\n"
            "assigns each instance to its most likely component.\n"
            "\n"
            "### Soft clustering\n"
            "\n"
            "```python\n"
            "gm.predict_proba(X)\n"
            "```\n"
            "\n"
            "returns:\n"
            "\n"
            "```text\n"
            "P(cluster 1 | x)\n"
            "P(cluster 2 | x)\n"
            "P(cluster 3 | x)\n"
            "...\n"
            "```\n"
            "\n"
            "This is richer than one cluster ID.\n"
            "\n"
            "{{image:gaussian-mixture-density-contours}}\n"
            "\n"
            "### Expectation-maximization intuition\n"
            "\n"
            "Gaussian mixtures are fitted using **expectation-maximization (EM)**.\n"
            "\n"
            "It alternates between two steps.\n"
            "\n"
            "#### Expectation step\n"
            "\n"
            "Estimate:\n"
            "\n"
            "```text\n"
            "how likely is each instance\n"
            "to belong to each Gaussian component?\n"
            "```\n"
            "\n"
            "These probabilities are often called **responsibilities**.\n"
            "\n"
            "#### Maximization step\n"
            "\n"
            "Update each component using the data, weighted by those responsibilities.\n"
            "\n"
            "Then repeat.\n"
            "\n"
            "This resembles k-means:\n"
            "\n"
            "```text\n"
            "k-means:\n"
            "assign points\n"
            "update centroids\n"
            "\n"
            "EM:\n"
            "estimate soft memberships\n"
            "update distribution parameters\n"
            "```\n"
            "\n"
            "But EM learns much more:\n"
            "\n"
            "- means,\n"
            "- covariance,\n"
            "- mixture weights.\n"
            "\n"
            "### EM can also get stuck\n"
            "\n"
            "Like k-means, EM can converge to poor local solutions.\n"
            "\n"
            "That is why multiple initializations may help:\n"
            "\n"
            "```python\n"
            "GaussianMixture(\n"
            "    n_components=3,\n"
            "    n_init=10,\n"
            ")\n"
            "```\n"
            "\n"
            "### Covariance types\n"
            "\n"
            "Scikit-Learn can constrain cluster shape using:\n"
            "\n"
            "```text\n"
            "spherical\n"
            "diag\n"
            "tied\n"
            "full\n"
            "```\n"
            "\n"
            "These trade flexibility against computation and statistical complexity.\n"
            "\n"
            "The default:\n"
            "\n"
            "```text\n"
            "full\n"
            "```\n"
            "\n"
            "lets every component learn its own full covariance matrix.\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Density estimation and anomaly detection\n"
            "\n"
            "A Gaussian mixture is more than a clustering algorithm.\n"
            "\n"
            "It is also a **density model**.\n"
            "\n"
            "It can estimate how plausible each location is under the learned distribution.\n"
            "\n"
            "```python\n"
            "log_densities = gm.score_samples(X)\n"
            "```\n"
            "\n"
            "Higher values correspond to denser, more typical regions.\n"
            "\n"
            "Lower density suggests unusual instances.\n"
            "\n"
            "### Detect anomalies using a density threshold\n"
            "\n"
            "Suppose you want to flag approximately the lowest-density 2%.\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "\n"
            "densities = gm.score_samples(X)\n"
            "\n"
            "density_threshold = np.percentile(\n"
            "    densities,\n"
            "    2,\n"
            ")\n"
            "\n"
            "anomalies = X[\n"
            "    densities < density_threshold\n"
            "]\n"
            "```\n"
            "\n"
            "{{image:gaussian-mixture-anomaly-detection}}\n"
            "\n"
            "### Threshold choice creates a trade-off\n"
            "\n"
            "Raise the anomaly threshold:\n"
            "\n"
            "```text\n"
            "flag more points\n"
            "-> catch more real anomalies\n"
            "-> produce more false positives\n"
            "```\n"
            "\n"
            "Lower the threshold:\n"
            "\n"
            "```text\n"
            "flag fewer points\n"
            "-> fewer false alarms\n"
            "-> risk missing more anomalies\n"
            "```\n"
            "\n"
            "This connects directly to the precision/recall trade-off from classification.\n"
            "\n"
            "### Anomaly detection versus novelty detection\n"
            "\n"
            "These terms are related but not identical.\n"
            "\n"
            "**Anomaly detection**\n"
            "\n"
            "Training data may already contain outliers.\n"
            "\n"
            "Goal:\n"
            "\n"
            "```text\n"
            "find unusual examples\n"
            "within possibly contaminated data\n"
            "```\n"
            "\n"
            "**Novelty detection**\n"
            "\n"
            "Training data is assumed to be clean.\n"
            "\n"
            "Goal:\n"
            "\n"
            "```text\n"
            "detect future examples\n"
            "that do not resemble known-normal data\n"
            "```\n"
            "\n"
            "This distinction matters because training contamination can change the learned definition of normality.\n"
            "\n"
            "### Alternative methods\n"
            "\n"
            "The chapter also introduces several alternatives.\n"
            "\n"
            "**Isolation Forest**\n"
            "\n"
            "Randomly partitions feature space.\n"
            "\n"
            "Anomalies tend to become isolated in fewer splits than ordinary points.\n"
            "\n"
            "Useful for high-dimensional outlier detection.\n"
            "\n"
            "**Local Outlier Factor (LOF)**\n"
            "\n"
            "Compares local density around one point with the density around its neighbors.\n"
            "\n"
            "A point may be anomalous if it is much more isolated than nearby points.\n"
            "\n"
            "**One-Class SVM**\n"
            "\n"
            "Learns a region enclosing normal training examples.\n"
            "\n"
            "Especially useful for novelty detection, but does not scale well to very large datasets.\n"
            "\n"
            "**Robust covariance / EllipticEnvelope**\n"
            "\n"
            "Fits a robust Gaussian-like envelope while reducing the influence of outliers.\n"
            "\n"
            "Useful when normal data roughly follows one Gaussian distribution.\n"
            "\n"
            "**Reconstruction-error methods**\n"
            "\n"
            "Dimensionality-reduction models can reconstruct normal examples well.\n"
            "\n"
            "Anomalies often have much larger reconstruction error.\n"
            "\n"
            "---\n"
            "\n"
            "## 10. Choosing the number of Gaussian components\n"
            "\n"
            "Like k-means, a standard Gaussian mixture requires:\n"
            "\n"
            "```text\n"
            "n_components\n"
            "```\n"
            "\n"
            "But inertia and silhouette score are less reliable for GMMs when clusters:\n"
            "\n"
            "- are nonspherical,\n"
            "- differ in size,\n"
            "- overlap.\n"
            "\n"
            "Instead, use model-selection criteria.\n"
            "\n"
            "### AIC and BIC\n"
            "\n"
            "Two common criteria are:\n"
            "\n"
            "- **Akaike Information Criterion (AIC)**\n"
            "- **Bayesian Information Criterion (BIC)**\n"
            "\n"
            "Both balance:\n"
            "\n"
            "```text\n"
            "goodness of fit\n"
            "against\n"
            "model complexity\n"
            "```\n"
            "\n"
            "A model with more Gaussian components may fit the training data better.\n"
            "\n"
            "But it also has more parameters.\n"
            "\n"
            "AIC and BIC penalize this complexity.\n"
            "\n"
            "In Scikit-Learn:\n"
            "\n"
            "```python\n"
            "gm.aic(X)\n"
            "gm.bic(X)\n"
            "```\n"
            "\n"
            "Lower is better.\n"
            "\n"
            "{{image:gmm-aic-bic-selection}}\n"
            "\n"
            "### Why BIC may select simpler models\n"
            "\n"
            "BIC typically penalizes model complexity more strongly than AIC, especially as dataset size increases.\n"
            "\n"
            "So when the two disagree:\n"
            "\n"
            "```text\n"
            "BIC often chooses fewer components\n"
            "```\n"
            "\n"
            "### Bayesian Gaussian mixture\n"
            "\n"
            "Another strategy is:\n"
            "\n"
            "```python\n"
            "from sklearn.mixture import BayesianGaussianMixture\n"
            "\n"
            "bgm = BayesianGaussianMixture(\n"
            "    n_components=10,\n"
            "    n_init=10,\n"
            "    max_iter=500,\n"
            "    random_state=42,\n"
            ")\n"
            "\n"
            "bgm.fit(X)\n"
            "```\n"
            "\n"
            "Choose an upper bound that is reasonably larger than the expected true number of clusters.\n"
            "\n"
            "The model can assign near-zero weights to unnecessary components.\n"
            "\n"
            "This lets the effective number of clusters emerge from the fit.\n"
            "\n"
            "### But GMMs also have assumptions\n"
            "\n"
            "Gaussian mixtures work especially well for:\n"
            "\n"
            "```text\n"
            "ellipsoidal Gaussian-like clusters\n"
            "```\n"
            "\n"
            "They are not ideal for every geometry.\n"
            "\n"
            "For strongly curved structures such as moon-shaped clusters, a density-connected algorithm like DBSCAN may be a much better match.\n"
            "\n"
            "---\n"
            "\n"
            "## 11. A practical decision guide\n"
            "\n"
            "The techniques in this chapter become easier to choose when organized by assumptions.\n"
            "\n"
            "| Method | Main idea | Strong when | Weak when |\n"
            "|---|---|---|---|\n"
            "| k-means | nearest centroid | compact, roughly spherical clusters; large datasets | irregular shapes, varying density/size |\n"
            "| MiniBatchKMeans | approximate k-means with mini-batches | very large datasets | slightly less precise solutions |\n"
            "| DBSCAN | connected high-density regions | arbitrary shapes, anomaly identification | strongly varying densities, large-scale computation |\n"
            "| Gaussian mixture | probabilistic Gaussian components | overlapping ellipsoidal clusters, density estimation | strongly non-Gaussian geometry |\n"
            "| Isolation Forest | isolate rare points quickly | high-dimensional anomaly detection | not a clustering method |\n"
            "| LOF | compare local densities | local-density anomalies | can be expensive / sensitive to neighborhoods |\n"
            "| One-Class SVM | learn boundary around normal data | novelty detection, high-dimensional data | poor scaling to large datasets |\n"
            "\n"
            "### Ask these questions\n"
            "\n"
            "When choosing an unsupervised method:\n"
            "\n"
            "```text\n"
            "Do I know the number of clusters?\n"
            "Are clusters centroid-like?\n"
            "Are clusters density-connected?\n"
            "Do cluster shapes overlap?\n"
            "Do I need probabilities?\n"
            "Do I need anomaly scores?\n"
            "Does the dataset fit in memory?\n"
            "Will I need to assign future instances?\n"
            "```\n"
            "\n"
            "The answer usually points you toward the right family of algorithms.\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> A cluster label is the same thing as a class label.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Class labels are known targets provided during supervised learning. Cluster IDs are discovered by an unsupervised algorithm and have no inherent semantic meaning until a human interprets them.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> k-means always finds the correct solution once it converges.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "k-means may converge to a poor local solution depending on centroid initialization.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> The clustering with the lowest inertia always has the best number of clusters.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Inertia normally decreases as `k` increases. Use the elbow method, silhouette analysis, and domain usefulness instead of minimizing inertia blindly.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> k-means can model any cluster shape if you add enough clusters.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "k-means fundamentally groups points by nearest-centroid geometry and is poorly matched to many irregular or differently scaled cluster shapes.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> DBSCAN needs the number of clusters in advance.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "DBSCAN discovers connected dense regions from `eps` and `min_samples`; the number of clusters emerges from the data.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Gaussian mixtures perform hard clustering just like k-means.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A GMM naturally produces membership probabilities, so it supports soft probabilistic cluster assignments.\n"
            "\n"
            "### Misconception 7\n"
            "\n"
            "> Anomaly detection and novelty detection are identical.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Novelty detection assumes the training data is clean, while anomaly detection may be trained on data already containing some outliers.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Unsupervised learning | Learning structure from data without target labels |\n"
            "| Clustering | Grouping similar instances |\n"
            "| Cluster | Group of instances considered similar under an algorithm’s definition |\n"
            "| Centroid | Mean location representing a k-means cluster |\n"
            "| Hard clustering | Assigning each instance to one cluster |\n"
            "| Soft clustering | Representing degrees of membership or affinity to multiple clusters |\n"
            "| Inertia | Sum of squared distances from instances to their closest k-means centroids |\n"
            "| k-means++ | Smarter centroid initialization that spreads starting centroids apart |\n"
            "| Mini-batch k-means | Scalable k-means variant that updates from mini-batches |\n"
            "| Elbow method | Choosing k from the point where inertia improvement starts flattening |\n"
            "| Silhouette coefficient | Cluster-quality score comparing within-cluster and nearest-cluster distances |\n"
            "| Label propagation | Extending labels from representative labeled instances to similar unlabeled ones |\n"
            "| Active learning | Iterative labeling where the model requests especially informative labels |\n"
            "| DBSCAN | Density-based clustering algorithm that finds connected high-density regions |\n"
            "| Epsilon neighborhood | Region within distance `eps` of an instance in DBSCAN |\n"
            "| Core instance | DBSCAN instance with at least `min_samples` points in its epsilon neighborhood |\n"
            "| Gaussian mixture model | Probabilistic model representing data as a mixture of Gaussian components |\n"
            "| EM | Expectation-maximization algorithm used to fit latent-variable probabilistic models |\n"
            "| Responsibility | Estimated probability that a Gaussian component generated an instance |\n"
            "| Density estimation | Estimating how probable different regions of feature space are |\n"
            "| Anomaly | Unusually low-density or atypical instance |\n"
            "| Novelty detection | Detecting new examples unlike clean normal training data |\n"
            "| AIC | Information criterion balancing likelihood and model complexity |\n"
            "| BIC | Information criterion similar to AIC, typically penalizing complexity more strongly |\n"
            "| Isolation Forest | Anomaly detector based on how quickly random partitions isolate instances |\n"
            "| Local Outlier Factor | Anomaly method comparing local density with neighboring density |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What is the difference between classification and clustering?\n"
            "2. What do k-means centroids represent?\n"
            "3. What is the difference between hard clustering and soft cluster features?\n"
            "4. What are the two alternating steps in k-means?\n"
            "5. Why can k-means converge to a bad result?\n"
            "6. What does k-means++ improve?\n"
            "7. Why can’t you select `k` merely by minimizing inertia?\n"
            "8. How do you interpret silhouette values near +1, 0, and -1?\n"
            "9. Why does feature scaling matter for k-means?\n"
            "10. How can clustering reduce labeling cost in semi-supervised learning?\n"
            "11. What is uncertainty sampling in active learning?\n"
            "12. What makes a point a core instance in DBSCAN?\n"
            "13. Why can DBSCAN capture moon-shaped clusters that k-means struggles with?\n"
            "14. What does a Gaussian mixture learn beyond cluster centers?\n"
            "15. How does EM differ from k-means conceptually?\n"
            "16. How can a GMM be used for anomaly detection?\n"
            "17. What is the difference between anomaly and novelty detection?\n"
            "18. Why are AIC and BIC useful for Gaussian mixtures?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**Unsupervised learning is about discovering useful structure when labels are absent. k-means represents groups through centroids, DBSCAN discovers connected dense regions, and Gaussian mixtures model overlapping probabilistic distributions. The right method depends on the geometry, density, scale, and purpose of the data—and unsupervised learning becomes especially powerful when its discovered structure is reused for feature engineering, label selection, anomaly detection, or downstream supervised learning.**\n"
        ),

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "unsupervised-overview",
                "title": "Learning from data without labels",
                "order": 1,
            },
            {
                "id": "kmeans-basics",
                "title": "k-means: clustering around centroids",
                "order": 2,
            },
            {
                "id": "kmeans-algorithm",
                "title": "How k-means actually learns",
                "order": 3,
            },
            {
                "id": "select-k",
                "title": "Choosing the number of clusters",
                "order": 4,
            },
            {
                "id": "kmeans-applications",
                "title": "Limits and practical applications of k-means",
                "order": 5,
            },
            {
                "id": "semi-supervised",
                "title": "Clustering for semi-supervised and active learning",
                "order": 6,
            },
            {
                "id": "dbscan",
                "title": "DBSCAN: find clusters using density",
                "order": 7,
            },
            {
                "id": "gmm",
                "title": "Gaussian mixtures: soft probabilistic clustering",
                "order": 8,
            },
            {
                "id": "anomaly-detection",
                "title": "Density estimation and anomaly detection",
                "order": 9,
            },
            {
                "id": "gmm-model-selection",
                "title": "Choosing the number of Gaussian components",
                "order": 10,
            },
            {
                "id": "decision-guide",
                "title": "A practical decision guide",
                "order": 11,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L08.EX01",

            "title": "Select and Diagnose a k-means Solution",

            "lesson_code": "M01.L08",

            "section_id": "select-k",

            "placement": "after_section",

            "description": (
                "Practice selecting k and diagnosing whether centroid-based "
                "clustering is appropriate for the dataset."
            ),

            "instructions": (
                "You run k-means for k = 2 through 8. Inertia falls sharply until "
                "k = 4, then improves only slowly. The silhouette scores are:\n\n"
                "k=3: 0.48\n"
                "k=4: 0.62\n"
                "k=5: 0.60\n"
                "k=6: 0.43\n\n"
                "The k=4 solution has one very large cluster, while k=5 produces "
                "five similarly sized groups that are easier for the business to "
                "interpret.\n\n"
                "1. Why should you not select k using minimum inertia alone?\n"
                "2. What does the elbow suggest?\n"
                "3. What do the silhouette scores suggest?\n"
                "4. Could k=5 still be reasonable? Explain.\n"
                "5. If the clusters are long curved shapes, would you still trust "
                "k-means? Which algorithm from this lesson might be more suitable?"
            ),

            "expected_output": (
                "An explanation that inertia monotonically improves as k grows, "
                "recognition that k=4 is strongly supported statistically, a "
                "reasonable business justification for k=5, and DBSCAN as a "
                "candidate for irregular density-connected shapes."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "k-means",
                "inertia",
                "elbow-method",
                "silhouette-score",
                "algorithm-selection",
            ],
        },

        {
            "id": "M01.L08.EX02",

            "title": "Choose an Unsupervised Learning Strategy",

            "lesson_code": "M01.L08",

            "section_id": "decision-guide",

            "placement": "after_section",

            "description": (
                "Choose between centroid, density-based, probabilistic, and "
                "anomaly-detection methods for realistic scenarios."
            ),

            "instructions": (
                "Choose a reasonable method for each scenario and justify it:\n\n"
                "1. You need five compact customer segments from standardized "
                "tabular data and training speed matters.\n"
                "2. Your 2D data forms two moon-shaped regions plus scattered "
                "noise, and you do not know the number of clusters.\n"
                "3. Your clusters overlap and have different ellipsoidal shapes, "
                "and you want membership probabilities.\n"
                "4. You have a huge high-dimensional dataset and want an efficient "
                "outlier detector.\n"
                "5. You have thousands of unlabeled images but can afford to "
                "manually label only 50. Explain how clustering could make those "
                "50 labels more useful."
            ),

            "expected_output": (
                "A mapping such as k-means for scenario 1, DBSCAN for scenario 2, "
                "Gaussian mixture for scenario 3, Isolation Forest for scenario "
                "4, and representative-instance labeling plus optional label "
                "propagation for scenario 5."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "algorithm-selection",
                "dbscan",
                "gaussian-mixtures",
                "anomaly-detection",
                "semi-supervised-learning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L08.QZ01",

        "title": "Unsupervised Learning Techniques — Knowledge Check",

        "lesson_code": "M01.L08",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L08.Q01",

                "section_id": "unsupervised-overview",

                "question": (
                    "What distinguishes clustering from supervised classification?"
                ),

                "options": [
                    "Clustering always uses neural networks.",
                    "Clustering discovers groups without target labels.",
                    "Classification cannot use numerical features.",
                    "Clustering requires a test label for every instance.",
                ],

                "correct": 1,

                "explanation": (
                    "Clustering is unsupervised: the training data does not provide "
                    "class labels for the algorithm to imitate."
                ),
            },

            {
                "id": "M01.L08.Q02",

                "section_id": "kmeans-basics",

                "question": (
                    "How does standard k-means assign a new instance to a cluster?"
                ),

                "options": [
                    "To the cluster with the highest class probability.",
                    "To the cluster whose centroid is closest.",
                    "To every cluster equally.",
                    "To the least dense cluster.",
                ],

                "correct": 1,

                "explanation": (
                    "k-means uses nearest-centroid geometry for hard cluster "
                    "assignment."
                ),
            },

            {
                "id": "M01.L08.Q03",

                "section_id": "kmeans-algorithm",

                "question": (
                    "Why can different k-means initializations produce different "
                    "final solutions?"
                ),

                "options": [
                    "k-means never converges.",
                    "The optimization can converge to different local solutions depending on starting centroids.",
                    "Cluster centers are fixed before training.",
                    "Inertia is random after training.",
                ],

                "correct": 1,

                "explanation": (
                    "k-means is guaranteed to converge, but the converged solution "
                    "may depend on the initial centroids."
                ),
            },

            {
                "id": "M01.L08.Q04",

                "section_id": "select-k",

                "question": (
                    "Why is the clustering with the lowest inertia not necessarily "
                    "the best choice of k?"
                ),

                "options": [
                    "Inertia tends to decrease whenever more clusters are added.",
                    "Inertia can only be computed for DBSCAN.",
                    "Lower inertia means worse clustering.",
                    "Inertia ignores centroid distance.",
                ],

                "correct": 0,

                "explanation": (
                    "More centroids generally reduce distances, so inertia keeps "
                    "falling as k increases. The question is whether the added "
                    "clusters produce meaningful improvement."
                ),
            },

            {
                "id": "M01.L08.Q05",

                "section_id": "semi-supervised",

                "question": (
                    "Why can labeling instances nearest to cluster centroids be "
                    "better than labeling the same number of random instances?"
                ),

                "options": [
                    "Centroid-near instances tend to be representative of diverse regions of the dataset.",
                    "They guarantee 100% label accuracy.",
                    "They remove the need for a classifier.",
                    "They automatically convert unsupervised learning into regression.",
                ],

                "correct": 0,

                "explanation": (
                    "Cluster representatives can cover distinct regions of the "
                    "data, making a limited labeling budget more informative."
                ),
            },

            {
                "id": "M01.L08.Q06",

                "section_id": "dbscan",

                "question": (
                    "What is a DBSCAN core instance?"
                ),

                "options": [
                    "The point closest to a global centroid.",
                    "An instance with at least min_samples points in its eps-neighborhood, including itself.",
                    "Any point labeled -1.",
                    "The first point processed by the algorithm.",
                ],

                "correct": 1,

                "explanation": (
                    "Core instances lie in sufficiently dense regions according "
                    "to the eps and min_samples settings."
                ),
            },

            {
                "id": "M01.L08.Q07",

                "section_id": "gmm",

                "question": (
                    "What does GaussianMixture.predict_proba() provide?"
                ),

                "options": [
                    "Distances to every k-means centroid.",
                    "Estimated membership probabilities for each Gaussian component.",
                    "Only one hard cluster ID.",
                    "The optimal number of components.",
                ],

                "correct": 1,

                "explanation": (
                    "A Gaussian mixture is probabilistic and naturally supports "
                    "soft cluster assignments."
                ),
            },

            {
                "id": "M01.L08.Q08",

                "section_id": "anomaly-detection",

                "question": (
                    "How can a fitted Gaussian mixture identify anomalies?"
                ),

                "options": [
                    "By selecting instances in very low-density regions.",
                    "By selecting instances nearest to component means.",
                    "By maximizing their silhouette score.",
                    "By forcing all points into one cluster.",
                ],

                "correct": 0,

                "explanation": (
                    "A GMM estimates probability density; unusually low-density "
                    "instances can be flagged as anomalies."
                ),
            },

            {
                "id": "M01.L08.Q09",

                "section_id": "gmm-model-selection",

                "type": "open",

                "question": (
                    "Explain why AIC or BIC can be useful when selecting the "
                    "number of Gaussian mixture components."
                ),
            },

            {
                "id": "M01.L08.Q10",

                "section_id": "decision-guide",

                "type": "open",

                "question": (
                    "Compare k-means, DBSCAN, and Gaussian mixture models in terms "
                    "of the cluster structures they assume or detect."
                ),
            },
        ],

        "passing_score": 70,
    },
}
