"""M01.L07 — Dimensionality Reduction: Keeping the Signal, Dropping the Noise.

One source chapter -> one complete learner-facing lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 7: Dimensionality Reduction. Source page numbers were not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L07"

MODULE_ORDER = 1

MODULE_TITLE = "Dimensionality Reduction"

MODULE_DESCRIPTION = (
    "Understand why high-dimensional data is difficult to learn from, how projection "
    "and manifold learning reduce dimensionality, and how to choose among PCA, "
    "random projection, LLE, and related techniques without discarding useful signal."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Dimensionality Reduction: Keeping the Signal, Dropping the Noise",

    "slug": "machine-learning-foundations-m01-l07",

    "description": (
        "An intuitive and practical lesson on the curse of dimensionality, projection, "
        "manifold learning, PCA and its scalable variants, random projection, LLE, "
        "compression, visualization, and method selection."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.25,

    "skill_tags": [
        "dimensionality-reduction",
        "curse-of-dimensionality",
        "pca",
        "svd",
        "explained-variance",
        "random-projection",
        "lle",
        "manifold-learning",
        "data-visualization",
        "feature-compression",
        "machine-learning-foundations",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Dimensionality Reduction: Keeping the Signal, Dropping the Noise",

        "content": (
            """# Dimensionality Reduction: Keeping the Signal, Dropping the Noise

> **Course:** Applied Machine Learning with Scikit-Learn  
> **Lesson:** M01.L07  
> **Module:** Dimensionality Reduction  
> **Source alignment:** Supplied source, Chapter 7, *Dimensionality Reduction*. Source page numbers were not provided. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the **curse of dimensionality** and why distance, sparsity, generalization, and interpretability become harder in high-dimensional spaces.
- Explain when dimensionality reduction may speed up learning, improve visualization, or remove redundancy—and when it may hurt by discarding useful information.
- Distinguish **projection** from **manifold learning**.
- Explain the manifold assumption and why reducing dimensions does **not** automatically make every downstream task simpler.
- Explain PCA using variance, principal components, centering, SVD, and projection.
- Use `explained_variance_ratio_` and cumulative explained variance to choose a useful number of PCA components.
- Use PCA for compression and explain reconstruction error.
- Distinguish regular PCA, randomized PCA, and incremental PCA.
- Explain the intuition behind the Johnson–Lindenstrauss result and use random projection for very high-dimensional data.
- Explain how LLE preserves local relationships to unroll nonlinear manifolds.
- Compare PCA, random projection, LLE, MDS, Isomap, t-SNE, LDA, and UMAP at a practical level.
- Choose a dimensionality-reduction method based on dataset size, geometry, sparsity, visualization needs, and downstream model requirements.

---

## 1. Why high-dimensional data becomes difficult

A dataset may contain hundreds, thousands, or even millions of features. At first, having more features sounds helpful: more information should make learning easier, right?

Not necessarily.

The problem is that **space behaves very differently as the number of dimensions grows**. Our intuition comes from two or three dimensions, so it becomes unreliable in very high-dimensional spaces.

### The core idea

Imagine spreading the same number of points through increasingly larger spaces:

```text
1D -> points lie along a line
2D -> the same points spread across an area
3D -> they spread through a volume
1000D -> they occupy an enormous high-dimensional space
```

As dimensionality grows, the available space grows so rapidly that the data becomes **sparse**.

This creates several practical problems.

### 1. Distances become less informative

The source chapter shows that two random points can be surprisingly far apart in a high-dimensional unit hypercube. This matters because algorithms such as k-nearest neighbors rely directly on distances.

If almost every point is far from every other point, then the notion of "nearest" becomes less meaningful.

### 2. New samples are far from training samples

A model often generalizes by learning patterns near examples it has already seen. In a sparse high-dimensional space, a new example is more likely to lie far away from all training examples.

That means the model may need to extrapolate more aggressively, which can make predictions less reliable.

### 3. Noise becomes easier to fit

With many dimensions, a flexible model has many opportunities to discover accidental patterns. The model may begin treating noise as if it were useful structure.

This is one reason **regularization becomes increasingly important** as dimensionality grows.

### 4. Training can become slow or infeasible

Some algorithms scale poorly with the number of features. Even if the model is statistically capable of learning from the data, the computation or memory requirements may become unacceptable.

### 5. Interpretation becomes harder

It is much easier to reason about relationships between 5 features than between 50,000 features.

### Why not simply collect more data?

More training examples can increase data density, but the number of examples needed to maintain the same density grows extremely quickly with dimensionality.

This is the heart of the **curse of dimensionality**:

> As the number of dimensions increases, the space grows so quickly that available data becomes increasingly sparse.

### Dimensionality reduction is not automatically beneficial

Reducing features can:

- speed up training,
- reduce storage and memory use,
- remove redundant or noisy directions,
- sometimes improve generalization,
- make 2D or 3D visualization possible.

But reduction can also discard useful signal.

Think of it like lossy image compression: a smaller representation is convenient, but compressing too aggressively removes detail.

Some models, especially neural networks, may also learn their own compact internal representations. So dimensionality reduction should be treated as a tool, not a mandatory preprocessing step.

---

## 2. Projection versus manifold learning

Most real datasets are not distributed uniformly across every available dimension.

Some features barely vary. Others are strongly correlated. As a result, the data may actually live close to a lower-dimensional structure hidden inside the original feature space.

There are two main ways to exploit this: **projection** and **manifold learning**.

### Projection: find a useful lower-dimensional subspace

Imagine a cloud of points in 3D that lies almost flat on a plane.

Although every sample has three coordinates, most of the meaningful variation happens along the plane. We can therefore project the points onto that plane and describe them using only two new coordinates.

```text
Original representation: (x1, x2, x3)
                         |
                         v
Lower-dimensional plane: (z1, z2)
```

The new features `z1` and `z2` are not necessarily copies of the original features. They are coordinates in the new lower-dimensional representation.

[[IMAGE_NEEDED: Projection from a 3D space to a 2D subspace — Source Figures 7-2 and 7-3 — key: projection-3d-to-2d-subspace | Recreate or combine the source view of 3D points lying close to a plane and the resulting 2D projected dataset with new axes z1 and z2 | Learner should notice that dimensionality can be reduced because the points vary mostly along a lower-dimensional subspace]]

Projection is the central idea behind PCA and random projection.

### Manifold learning: unfold nonlinear structure

Projection works well when the useful structure is approximately flat. But what if the structure bends or twists?

The classic example is the **Swiss roll**: a 2D sheet rolled through 3D space.

If you simply flatten it by dropping one coordinate, different layers of the roll overlap. Points that were far apart along the sheet may be placed on top of each other.

What we really want is to **unroll** the sheet.

{{image:projection-vs-manifold-unrolling}}

A **manifold** is a lower-dimensional structure embedded inside a higher-dimensional space.

For example:

```text
Swiss roll:
Intrinsic dimension = 2
Observed dimension  = 3
```

Locally, a small part of the Swiss roll looks almost like an ordinary 2D plane, even though the whole structure is bent in 3D.

### The manifold assumption

Many dimensionality-reduction algorithms rely on the idea that real high-dimensional datasets often lie close to much lower-dimensional manifolds.

Handwritten digits are a good example. A 28 x 28 image has 784 pixel features, but valid handwritten digits occupy only a tiny fraction of all possible 784-dimensional pixel combinations.

Real digits obey many constraints:

- strokes tend to connect,
- borders are often blank,
- shapes occupy a limited region,
- only certain structures look like valid digits.

So the true degrees of freedom may be much smaller than 784.

### Important: lower dimension does not guarantee an easier task

A common misconception is:

```text
fewer dimensions -> simpler decision boundary -> better model
```

This is not guaranteed.

Sometimes unrolling a manifold makes the classification boundary much simpler. In other cases, a simple boundary in the original space may become fragmented after dimensionality reduction.

{{image:manifold-decision-boundary-caveat}}

So evaluate dimensionality reduction according to the **actual downstream task**, not just the geometry of the embedding.

---

## 3. PCA: preserve the directions with the most variance

**Principal Component Analysis (PCA)** is the most widely used dimensionality-reduction technique in the chapter.

Its basic idea is simple:

> Find the directions along which the data varies the most, then represent the data using only the most important of those directions.

### Why preserve variance?

Suppose a 2D cloud of points is long and narrow.

There are many possible 1D axes onto which you could project the points. If you choose the long direction, the projected points remain well spread out. If you choose the short direction, many different points collapse into nearly the same location.

The long direction therefore preserves more information.

{{image:pca-maximum-variance-projection}}

Another equivalent way to understand PCA is that it chooses the projection that minimizes the average squared distance between the original points and their projected versions.

### Principal components

The most important direction is the **first principal component (PC1)**.

Then PCA finds a second direction that:

1. is perpendicular to PC1, and
2. preserves as much of the remaining variance as possible.

It continues this process for additional components.

```text
PC1 -> most variance
PC2 -> most remaining variance, orthogonal to PC1
PC3 -> most remaining variance, orthogonal to PC1 and PC2
...
```

Each principal component is represented by a unit vector.

### PCA and SVD

The source connects PCA to **Singular Value Decomposition (SVD)**.

If the centered data matrix is `X`, SVD decomposes it conceptually as:

```text
X = U @ Sigma @ V.T
```

The rows of `V.T` identify the principal directions.

A small NumPy example is:

```python
import numpy as np

X = [...]  # small dataset
X_centered = X - X.mean(axis=0)
U, s, Vt = np.linalg.svd(X_centered)

c1 = Vt[0]
c2 = Vt[1]
```

### Centering matters

PCA assumes that the data is centered around the origin.

That means subtracting the mean of each feature:

```text
centered value = original value - feature mean
```

Scikit-Learn's `PCA` centers the data automatically.

If you implement PCA manually, forgetting to center the data changes the geometry and therefore changes the resulting components.

### Projecting to fewer dimensions

Once the principal components are known, choose the first `d` components and project the dataset onto them.

If `W_d` contains those components, the reduced representation is conceptually:

```text
X_reduced = X_centered @ W_d
```

In Scikit-Learn:

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)
```

After fitting:

```python
pca.components_
```

contains the learned principal directions.

### Principal-component direction is not a semantic label

Do not assume that `PC1` means something like "size" and `PC2` means "shape" unless you inspect the component weights and data carefully.

Also, the sign of a principal component may flip if PCA is refit. A vector and its negative represent the same axis.

That is why, if PCA is part of a production preprocessing pipeline and you refit PCA, you should retrain the downstream model using the new representation as well.

---

## 4. Choosing dimensions, compression, and scalable PCA

The most important practical PCA question is often not *how* to run PCA, but:

> How many components should I keep?

### Explained variance ratio

Scikit-Learn exposes:

```python
pca.explained_variance_ratio_
```

Suppose the first three components explain:

```text
PC1 = 82%
PC2 = 11%
PC3 = 7%
```

Then the first two components preserve about 93% of the dataset's variance.

The **explained variance ratio** tells us how much of the total variance is retained by each component.

### Choosing a target such as 95%

Instead of saying "keep exactly 100 components", you can ask PCA to preserve a target fraction of the variance:

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=0.95)
X_reduced = pca.fit_transform(X_train)
```

Scikit-Learn then chooses the number of components automatically.

In the chapter's MNIST example, keeping 95% of the variance reduces the representation from 784 original pixel features to 154 principal components.

### The explained-variance elbow

Another useful strategy is to plot cumulative explained variance against the number of components.

At first, every additional component may add substantial information. Eventually the curve begins to flatten. The bend is often called the **elbow**.

{{image:pca-explained-variance-elbow}}

This is a heuristic, not a rule. The best number of dimensions depends on the downstream goal.

### Tune PCA as part of the complete ML pipeline

If dimensionality reduction is preprocessing for classification or regression, the strongest approach is often to tune the number of components together with the model hyperparameters.

For example:

```python
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import make_pipeline
import numpy as np

clf = make_pipeline(
    PCA(random_state=42),
    RandomForestClassifier(random_state=42),
)

param_distrib = {
    "pca__n_components": np.arange(10, 80),
    "randomforestclassifier__n_estimators": np.arange(50, 500),
}

rnd_search = RandomizedSearchCV(
    clf,
    param_distrib,
    n_iter=10,
    cv=3,
    random_state=42,
)
```

Why is joint tuning useful?

Because the ideal compressed representation depends partly on the model that consumes it.

A powerful nonlinear model may work well with fewer components, while a simpler model may need more retained information.

### PCA as compression

PCA can also compress data.

If MNIST goes from 784 features to 154 components, the reduced dataset occupies much less space.

The reduced representation can be approximately reconstructed with:

```python
X_recovered = pca.inverse_transform(X_reduced)
```

The reconstruction will not be identical to the original data because the discarded components are gone.

The mean squared distance between the original and reconstructed data is called the **reconstruction error**.

{{image:pca-mnist-compression-reconstruction}}

### Regular PCA, randomized PCA, and incremental PCA

The chapter introduces three important PCA execution modes.

| Method | Best fit | Main idea |
|---|---|---|
| Regular PCA | Dataset fits in memory and ordinary SVD is affordable | Compute principal components using standard decomposition |
| Randomized PCA | You need only a relatively small number of components from a larger feature space | Approximate the leading components faster using a randomized algorithm |
| Incremental PCA | The full training set does not fit comfortably in memory or arrives in chunks | Learn PCA gradually from mini-batches |

Randomized PCA can be requested with:

```python
from sklearn.decomposition import PCA

rnd_pca = PCA(
    n_components=154,
    svd_solver="randomized",
    random_state=42,
)
X_reduced = rnd_pca.fit_transform(X_train)
```

Incremental PCA uses repeated mini-batches:

```python
from sklearn.decomposition import IncrementalPCA
import numpy as np

n_batches = 100
inc_pca = IncrementalPCA(n_components=154)

for X_batch in np.array_split(X_train, n_batches):
    inc_pca.partial_fit(X_batch)

X_reduced = inc_pca.transform(X_train)
```

The source also describes `np.memmap` as a way to work with an array stored on disk while loading only required pieces into memory.

### Practical trade-off

The smallest representation is not automatically the best representation.

You are balancing at least three goals:

```text
fewer dimensions
    -> smaller model/data
    -> potentially faster training/inference
    -> but more information loss
```

The correct choice is the one that gives an acceptable balance of **performance, memory, and speed** for your application.

{{exercise:M01.L07.EX01}}

---

## 5. Random projection: surprisingly useful randomness

PCA learns projection directions from the data. **Random projection** does something that sounds almost unreasonable at first: it projects the data using a random matrix.

Why would that work?

Because a famous result called the **Johnson–Lindenstrauss lemma** shows that a sufficiently large random projection can preserve pairwise distances approximately, with high probability.

So if two examples are similar before the projection, they are likely to remain relatively close afterward. If two examples are very different, they are likely to remain far apart.

### The intuition

Suppose you start with:

```text
20,000 features
```

and reduce the representation to a few thousand dimensions.

The exact coordinates change dramatically, but the geometry can remain useful enough for downstream learning.

### Choosing the projected dimensionality

The source emphasizes an interesting fact: the Johnson–Lindenstrauss bound depends on:

- `m`: the number of samples,
- `epsilon`: the tolerated distance distortion,

but not directly on the original feature count `n`.

Scikit-Learn provides:

```python
from sklearn.random_projection import johnson_lindenstrauss_min_dim

m = 5_000
eps = 0.1

d = johnson_lindenstrauss_min_dim(m, eps=eps)
print(d)
```

In the source example, this yields `7300` dimensions for 5,000 samples with a 10% tolerance.

### Gaussian random projection

A Gaussian projection matrix can be generated conceptually as:

```python
import numpy as np

n = 20_000
rng = np.random.default_rng(seed=42)
P = rng.standard_normal((d, n)) / np.sqrt(d)

X_reduced = X @ P.T
```

Scikit-Learn wraps this process:

```python
from sklearn.random_projection import GaussianRandomProjection

gaussian_rnd_proj = GaussianRandomProjection(
    eps=0.1,
    random_state=42,
)
X_reduced = gaussian_rnd_proj.fit_transform(X)
```

### Why random projection is attractive

It is particularly useful when:

- the original feature space is enormous,
- the data is sparse,
- fitting PCA would be too slow or memory intensive,
- approximate distance preservation is good enough.

The projection matrix can be generated without learning detailed structure from the training values; the algorithm mainly needs the dimensionality information.

### Sparse random projection

`SparseRandomProjection` uses a sparse projection matrix.

This can dramatically reduce memory use and speed up transformation, especially for sparse input data. The source notes that it often offers comparable quality to Gaussian random projection and is usually preferable for very large or sparse datasets.

### Trade-off versus PCA

A useful mental model is:

```text
PCA
  + data-aware projection
  + usually preserves more signal
  - training can be expensive

Random projection
  + extremely simple and fast
  + works well for huge/sparse spaces
  - usually loses somewhat more signal
```

Random projection is therefore not "random guessing". The randomness is carefully structured, and high-dimensional geometry makes the result useful with high probability.

---

## 6. LLE: preserve local relationships instead of projecting globally

**Locally Linear Embedding (LLE)** is a nonlinear dimensionality-reduction method.

Unlike PCA and random projection, it is not based on projecting everything onto one global linear subspace.

Instead, it tries to preserve the **local neighborhood structure** of the data.

### Step 1: describe each point using its neighbors

For each training sample, LLE finds its `k` nearest neighbors.

It then asks:

> Can this point be approximately reconstructed as a weighted combination of its nearby points?

This creates a set of local reconstruction weights.

### Step 2: find low-dimensional points with the same local relationships

Now LLE searches for a lower-dimensional representation in which those same reconstruction relationships are preserved as closely as possible.

The important idea is:

```text
original space:
point ~= weighted combination of neighbors

lower-dimensional space:
embedded point ~= same weighted combination of embedded neighbors
```

Because LLE preserves local structure, it can handle curved manifolds that global linear projection methods struggle with.

### Swiss roll example

```python
from sklearn.datasets import make_swiss_roll
from sklearn.manifold import LocallyLinearEmbedding

X_swiss, t = make_swiss_roll(
    n_samples=1000,
    noise=0.2,
    random_state=42,
)

lle = LocallyLinearEmbedding(
    n_components=2,
    n_neighbors=10,
    random_state=42,
)

X_unrolled = lle.fit_transform(X_swiss)
```

{{image:lle-unrolled-swiss-roll}}

LLE does a good job of unrolling the manifold locally, but the source points out an important limitation: global distances may still be distorted.

### Scaling limitation

LLE can be computationally expensive, especially as the number of samples grows. The source specifically highlights a quadratic dependency on the number of samples in part of the computation.

So LLE is most appropriate for **small or medium-sized datasets** where nonlinear geometry matters.

---

## 7. Other dimensionality-reduction methods and how to choose

The chapter closes by comparing several additional techniques.

### MDS — preserve pairwise distances

**Multidimensional Scaling (MDS)** tries to reduce dimensions while keeping distances between samples as faithful as possible.

It can be useful when the distance relationships themselves are what you care about.

### Isomap — preserve geodesic distances

**Isomap** first creates a neighborhood graph and then tries to preserve **geodesic distances**: distances measured along the manifold rather than straight through the ambient space.

It works especially well when the data lies on a smooth, low-dimensional manifold with a coherent global structure.

### t-SNE — visualization of local clusters

**t-SNE** tries to keep similar samples close and dissimilar samples apart.

It is especially popular for 2D or 3D visualization of high-dimensional datasets and can make clusters visually clear.

The source gives an important warning:

> t-SNE is mainly a visualization method here; it is not intended as a normal preprocessing stage for an ML model.

### LDA — supervised dimensionality reduction

**Linear Discriminant Analysis (LDA)** is different because it uses class labels.

During training, it looks for axes that separate the classes as strongly as possible. Those axes can then be used as a lower-dimensional representation before another classifier.

This makes LDA a **supervised** dimensionality-reduction technique.

### UMAP — local and global visualization structure

The source also discusses **UMAP** as a popular visualization technique.

Its practical goal is to preserve both local and global structure better than methods that focus primarily on one scale, and it generally scales better than t-SNE to larger datasets.

In the source, UMAP is not part of Scikit-Learn itself and is available through the `umap-learn` package.

### Different methods preserve different things

The same Swiss roll can look very different after MDS, Isomap, or t-SNE because each algorithm optimizes a different geometric objective.

{{image:dimensionality-reduction-methods-comparison}}

### A practical decision guide

Use this as a starting point rather than a rigid rule:

| Situation | Good first method to consider | Why |
|---|---|---|
| General linear dimensionality reduction | PCA | Strong default; preserves maximum variance |
| Need only leading components from a large matrix | Randomized PCA | Faster approximate PCA |
| Dataset does not fit comfortably in memory | Incremental PCA | Mini-batch learning |
| Extremely high-dimensional or sparse data | Random projection | Very fast and memory efficient |
| Nonlinear manifold, small/medium dataset | LLE or Isomap | Preserves local/manifold geometry |
| 2D/3D cluster visualization | t-SNE or UMAP | Designed for informative embeddings |
| Need class-aware linear compression | LDA | Uses labels to preserve discrimination |

### How should you evaluate dimensionality reduction?

There is no single universal score.

Evaluation depends on your goal.

If reduction is preprocessing for a supervised model, evaluate the **whole pipeline**:

```text
raw data
  -> dimensionality reduction
  -> classifier/regressor
  -> validation metric
```

If the downstream model performs better, trains faster, or uses less memory while staying within acceptable quality limits, the reduction is helping.

For reconstruction-based methods such as PCA, reconstruction error can also be informative.

For visualization methods, inspect whether meaningful neighborhoods and patterns are represented—but avoid assuming that every visual cluster is automatically a true class or causal structure.

### Can dimensionality-reduction methods be chained?

Yes, when there is a reason.

For example, a very high-dimensional dataset may first be compressed rapidly using PCA or random projection and then passed to a more expensive nonlinear visualization algorithm.

The first stage reduces computational burden; the second stage focuses on geometry.

The important rule is to validate the combined pipeline instead of assuming that more preprocessing is automatically better.

{{exercise:M01.L07.EX02}}

---

## Important misconceptions

### Misconception 1

> Dimensionality reduction always improves model accuracy.

### Why this is wrong

Reduction always throws away or transforms information. It may remove noise and redundancy, but it can also remove useful predictive signal. Judge it using the downstream objective.

### Misconception 2

> PCA simply keeps the original features with the highest variance.

### Why this is wrong

PCA creates **new axes** that are linear combinations of the original features. Principal components are directions in feature space, not merely selected original columns.

### Misconception 3

> PCA can correctly unroll any nonlinear manifold.

### Why this is wrong

PCA is a global **linear projection** technique. Strongly curved manifolds may require nonlinear techniques such as LLE or Isomap.

### Misconception 4

> A beautiful 2D t-SNE plot proves that the classes are naturally separated.

### Why this is wrong

Visualization methods deliberately distort some geometry to emphasize other relationships. The embedding is useful for exploration, but it should not be treated as proof of class separability or causal structure.

### Misconception 5

> Fewer dimensions are always better once accuracy is acceptable.

### Why this is wrong

The correct dimensionality is a trade-off among predictive quality, training speed, inference speed, storage, robustness, and interpretability.

---

## Key terminology

| Term | Meaning |
|---|---|
| Curse of dimensionality | Problems caused by rapidly expanding, sparse feature space as dimensionality grows |
| Dimensionality reduction | Transforming data into a representation with fewer dimensions |
| Projection | Mapping data onto a lower-dimensional subspace |
| Manifold | A lower-dimensional structure embedded in a higher-dimensional space |
| Manifold assumption | The idea that real high-dimensional data often lies near a much lower-dimensional manifold |
| Principal component | An orthogonal direction found by PCA that captures as much remaining variance as possible |
| Explained variance ratio | Fraction of total dataset variance associated with a principal component |
| SVD | Matrix factorization used to obtain PCA directions |
| Reconstruction error | Difference between original data and its approximation after reducing and reversing the representation |
| Randomized PCA | Approximate PCA method optimized for efficiently finding leading components |
| Incremental PCA | PCA trained gradually from mini-batches |
| Random projection | Lower-dimensional mapping using a random matrix designed to approximately preserve distances |
| Johnson–Lindenstrauss lemma | Result showing that random projections can preserve pairwise distances approximately in fewer dimensions |
| LLE | Nonlinear manifold-learning method that preserves local linear neighbor relationships |
| Geodesic distance | Distance measured along a graph or manifold rather than straight through ambient space |
| t-SNE | Nonlinear dimensionality-reduction method primarily used for visualization of local structure and clusters |
| LDA | Supervised linear technique that finds directions that separate classes |
| UMAP | Nonlinear embedding method often used for scalable visualization while preserving local and some global structure |

---

## Self-check

Before continuing, make sure you can answer:

1. Why do distances become less useful as dimensionality grows?
2. What is the difference between projection and manifold learning?
3. Why does PCA maximize variance, and why must the input be centered?
4. What does `explained_variance_ratio_` tell you?
5. When would incremental PCA be preferable to ordinary PCA?
6. Why can random projection work even though its matrix is random?
7. Why is LLE better suited than PCA to some curved manifolds?
8. Why should t-SNE normally be treated as a visualization technique rather than a standard preprocessing step?
9. How would you evaluate whether dimensionality reduction helps a classifier?
10. Why can reducing dimensions sometimes make a decision boundary more complicated rather than simpler?

---

## Retain this idea

**Dimensionality reduction is not about deleting features blindly. It is about finding a smaller representation that preserves the structure needed for your goal: PCA preserves dominant variance, random projection preserves distances approximately at massive scale, and manifold methods preserve nonlinear neighborhood structure. The best representation is the smallest one that still preserves what the downstream task actually needs.**
"""
        ),

        "estimated_minutes": 195,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "curse-of-dimensionality",
                "title": "Why high-dimensional data becomes difficult",
                "order": 1,
            },
            {
                "id": "projection-and-manifolds",
                "title": "Projection versus manifold learning",
                "order": 2,
            },
            {
                "id": "pca",
                "title": "PCA: preserve the directions with the most variance",
                "order": 3,
            },
            {
                "id": "choosing-pca-size",
                "title": "Choosing dimensions, compression, and scalable PCA",
                "order": 4,
            },
            {
                "id": "random-projection",
                "title": "Random projection: surprisingly useful randomness",
                "order": 5,
            },
            {
                "id": "lle",
                "title": "LLE: preserve local relationships instead of projecting globally",
                "order": 6,
            },
            {
                "id": "other-methods",
                "title": "Other dimensionality-reduction methods and how to choose",
                "order": 7,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L07.EX01",

            "title": "Choose and Inspect a PCA Representation",

            "lesson_code": "M01.L07",

            "section_id": "choosing-pca-size",

            "placement": "after_section",

            "description": (
                "Practice selecting a PCA dimensionality using explained variance and "
                "reason about the trade-off between compression and information retention."
            ),

            "instructions": (
                "1. Load a numeric dataset with at least several features, or use a prepared course dataset.\n"
                "2. Fit `PCA()` without fixing `n_components` and inspect `explained_variance_ratio_`.\n"
                "3. Compute cumulative explained variance and identify the smallest number of components that preserves at least 95% of the variance.\n"
                "4. Fit PCA again using that target and transform the dataset.\n"
                "5. Report the original feature count, reduced feature count, and compression ratio.\n"
                "6. Use `inverse_transform()` on a small sample and explain what reconstruction error means.\n"
                "7. Explain whether you would automatically choose the 95% representation for a downstream classifier, and why validation is still necessary."
            ),

            "expected_output": (
                "A short notebook or code submission containing the explained-variance "
                "analysis, selected dimensionality, transformed-data shape, one reconstruction "
                "example, and a written interpretation of the speed-versus-signal trade-off."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "pca",
                "explained-variance",
                "dimensionality-selection",
                "reconstruction-error",
                "model-reasoning",
            ],
        },

        {
            "id": "M01.L07.EX02",

            "title": "Select the Right Dimensionality-Reduction Method",

            "lesson_code": "M01.L07",

            "section_id": "other-methods",

            "placement": "after_section",

            "description": (
                "Choose appropriate dimensionality-reduction techniques for realistic "
                "datasets by matching each method to geometry, scale, and downstream goals."
            ),

            "instructions": (
                "For each scenario, choose a primary method and justify your choice:\n"
                "1. A sparse text matrix with one million features where training PCA is too expensive.\n"
                "2. A medium-sized nonlinear dataset shaped like a twisted manifold that must be visualized in 2D.\n"
                "3. A large dense dataset that does not fit in memory, where a linear compressed representation is needed for a classifier.\n"
                "4. A labeled classification dataset where you specifically want a linear projection that separates classes.\n"
                "5. A high-dimensional dataset where you need an exploratory 2D cluster visualization, not a preprocessing transform for production inference.\n"
                "For every answer, name one important limitation or validation check."
            ),

            "expected_output": (
                "A five-row decision table naming the chosen technique, the reason it fits "
                "the scenario, and one limitation or validation step for each choice."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "method-selection",
                "random-projection",
                "incremental-pca",
                "manifold-learning",
                "visualization",
                "supervised-dimensionality-reduction",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L07.QZ01",

        "title": "Dimensionality Reduction — Knowledge Check",

        "lesson_code": "M01.L07",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L07.Q01",

                "section_id": "curse-of-dimensionality",

                "question": (
                    "What best describes the curse of dimensionality in machine learning?"
                ),

                "options": [
                    "Every extra feature always increases model accuracy",
                    "High-dimensional space grows so rapidly that finite data becomes sparse and distances become less informative",
                    "Models cannot perform matrix multiplication when there are many features",
                    "Dimensionality reduction is mathematically impossible above three dimensions",
                ],

                "correct": 1,

                "explanation": (
                    "As dimensionality grows, the available space expands rapidly. With a finite "
                    "training set, examples become sparse and often far apart, which can hurt "
                    "distance-based reasoning, generalization, computation, and interpretability."
                ),
            },

            {
                "id": "M01.L07.Q02",

                "section_id": "projection-and-manifolds",

                "question": (
                    "Why can ordinary projection fail on a Swiss-roll-shaped dataset?"
                ),

                "options": [
                    "Projection requires class labels",
                    "Projection always increases the number of dimensions",
                    "Flattening the roll can place different layers on top of each other and destroy manifold structure",
                    "Projection cannot be applied to numeric features",
                ],

                "correct": 2,

                "explanation": (
                    "A Swiss roll is a curved 2D manifold embedded in 3D. A simple linear projection "
                    "may squash separated parts together, while manifold learning tries to preserve "
                    "the structure along the surface."
                ),
            },

            {
                "id": "M01.L07.Q03",

                "section_id": "pca",

                "question": (
                    "What does PCA choose for its first principal component?"
                ),

                "options": [
                    "The original feature with the largest mean",
                    "The direction that preserves the largest amount of variance",
                    "The feature with the smallest standard deviation",
                    "A randomly selected projection direction",
                ],

                "correct": 1,

                "explanation": (
                    "PC1 is the direction along which the centered training data has maximum "
                    "variance. Later components are orthogonal and preserve as much of the remaining "
                    "variance as possible."
                ),
            },

            {
                "id": "M01.L07.Q04",

                "section_id": "random-projection",

                "question": (
                    "Why can random projection be useful for extremely high-dimensional data?"
                ),

                "options": [
                    "It guarantees perfect reconstruction of every feature",
                    "It approximately preserves pairwise distances with high probability while being very fast and memory efficient",
                    "It always finds more informative axes than PCA",
                    "It requires the target labels to construct the projection matrix",
                ],

                "correct": 1,

                "explanation": (
                    "The Johnson–Lindenstrauss result explains why sufficiently large random "
                    "projections can approximately preserve pairwise distances. This makes the method "
                    "especially attractive when PCA would be too expensive."
                ),
            },

            {
                "id": "M01.L07.Q05",

                "section_id": "other-methods",

                "type": "open",

                "question": (
                    "You have a high-dimensional dataset and want to reduce it before classification. "
                    "Describe how you would decide whether PCA, random projection, or a nonlinear "
                    "manifold method is appropriate, and explain how you would verify that your choice helps."
                ),
            },
        ],

        "passing_score": 70,
    },
}
