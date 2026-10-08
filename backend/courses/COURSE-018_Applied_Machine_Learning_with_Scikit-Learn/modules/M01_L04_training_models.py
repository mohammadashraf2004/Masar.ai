"""M01.L04 — Training Models: From Linear Regression to Softmax.

One source chapter -> one complete learner-facing lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 4: Training Models. Source page numbers were not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L04"

MODULE_ORDER = 1

MODULE_TITLE = "Training Models"

MODULE_DESCRIPTION = (
    "Open the machine-learning black box by learning how linear models are "
    "trained, optimized, regularized, diagnosed, and extended from regression "
    "to binary and multiclass classification."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Not provided in the supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Training Models: From Linear Regression to Softmax",

    "slug": "machine-learning-foundations-m01-l04",

    "description": (
        "A complete guided tour of how models learn: linear regression, closed-form "
        "solutions, gradient descent, polynomial regression, learning curves, "
        "regularization, early stopping, logistic regression, and softmax regression."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "linear-regression",
        "gradient-descent",
        "optimization",
        "polynomial-regression",
        "learning-curves",
        "regularization",
        "logistic-regression",
        "softmax-regression",
        "machine-learning-foundations",
        "module-01",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Training Models: From Linear Regression to Softmax",

        "content": (
            """# Training Models: From Linear Regression to Softmax

> **Course:** Applied Machine Learning with Scikit-Learn  
> **Lesson:** M01.L04  
> **Module:** Training Models  
> **Source alignment:** Supplied source, Chapter 4, *Training Models*. Source page numbers were not provided. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what a model parameter, prediction function, loss function, and optimization algorithm each do.
- Train linear regression conceptually using both a closed-form solution and gradient descent.
- Compare batch, stochastic, and mini-batch gradient descent and choose between them.
- Explain why feature scaling and the learning rate strongly affect gradient-descent training.
- Use polynomial features to fit nonlinear relationships while recognizing the danger of overfitting.
- Read learning curves and distinguish underfitting from overfitting.
- Explain the bias/variance trade-off.
- Compare ridge, lasso, elastic net, and early stopping as regularization strategies.
- Explain how logistic regression turns a linear score into a probability for binary classification.
- Explain how softmax regression extends the same idea to mutually exclusive multiclass problems.
- Connect log loss and cross-entropy to probability-based classification training.

---

## 1. Linear regression: what exactly is being learned?

A useful way to stop treating machine learning as a black box is to separate four ideas that are often mixed together:

1. **Model:** the rule that converts inputs into predictions.
2. **Parameters:** the numbers inside that rule that the model learns from data.
3. **Loss or cost function:** the quantity that tells us how wrong the model currently is.
4. **Training algorithm:** the procedure used to find better parameter values.

For linear regression, the model is simple. It predicts a target by taking a weighted sum of the input features and adding a bias term.

For one instance with features `x1, x2, ..., xn`:

```text
prediction = bias + weight_1*x_1 + weight_2*x_2 + ... + weight_n*x_n
```

Using the chapter's parameter notation, the same idea is:

```text
ŷ = θ₀ + θ₁x₁ + θ₂x₂ + ... + θₙxₙ
```

The bias `θ₀` shifts the prediction up or down. Each remaining parameter controls how strongly one feature affects the prediction.

### Vectorized view

Machine-learning libraries rarely compute every weighted term using separate Python statements. They represent the features and parameters as vectors and matrices, allowing the same computation to run efficiently for many features and many examples.

With a dummy feature `x₀ = 1`, the prediction can be written compactly as:

```text
ŷ = θᵀx
```

This compact notation matters because the same matrix operations appear again in gradient descent, neural networks, and modern deep-learning libraries.

### Training means minimizing error

Suppose the model predicts house prices. A set of parameters is useful only if the predictions are close to the true prices. Linear regression therefore needs a numerical measure of error.

The chapter uses **mean squared error (MSE)** during training:

```text
MSE = average((prediction - target)²)
```

Squaring has two practical effects:

- positive and negative errors do not cancel each other;
- large mistakes are penalized more heavily than small mistakes.

The chapter notes an important distinction: the metric you report to users or stakeholders does not have to be identical to the loss optimized during training. For example, you may optimize MSE because it is convenient mathematically while reporting RMSE because it is easier to interpret in the target's original units.

### Closed-form training: the normal equation

One way to train linear regression is to directly compute the parameter vector that minimizes the MSE. The chapter presents the **normal equation**:

```text
θ̂ = (XᵀX)⁻¹Xᵀy
```

This is called a **closed-form solution** because it computes the answer directly rather than improving the parameters through repeated training steps.

A small NumPy implementation looks like this:

```python
import numpy as np
from sklearn.preprocessing import add_dummy_feature

rng = np.random.default_rng(seed=42)
X = 2 * rng.random((200, 1))
y = 4 + 3 * X + rng.standard_normal((200, 1))

X_b = add_dummy_feature(X)
theta_best = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
```

The `@` operator performs matrix multiplication. The recovered values will normally be close to the parameters that generated the data, but noise means they do not have to match exactly.

### Why Scikit-Learn does not simply invert `XᵀX`

The source chapter explains that `LinearRegression` relies on a least-squares/SVD-based approach rather than naively depending on the matrix inverse. The key tool is the **Moore-Penrose pseudoinverse**.

Why is that useful?

- `XᵀX` may be singular and therefore not invertible.
- Features may be redundant or strongly related.
- There may be more features than examples.
- SVD-based methods handle these edge cases more robustly.

```python
from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
lin_reg.fit(X, y)

print(lin_reg.intercept_)
print(lin_reg.coef_)
```

### Computational boundary

Closed-form/SVD approaches are attractive because they require almost no tuning, but they become expensive when the number of features becomes extremely large. Their training cost grows strongly with feature count. Once a linear model is trained, prediction itself is cheap: roughly speaking, twice as many examples or twice as many features means about twice as much prediction work.

**Mental model:** closed-form training asks, *Can I solve for the best parameters directly?* Gradient descent asks, *Can I walk toward better parameters step by step?*

---

## 2. Gradient descent: learning by taking downhill steps

Gradient descent is one of the most important ideas in machine learning because the same basic mechanism later appears in neural-network training.

Imagine standing on a mountain in dense fog. You cannot see the valley, but you can feel which direction slopes downward most steeply. You take a step downhill, measure the slope again, then repeat. Gradient descent applies this idea to a cost function.

The algorithm starts with some parameter vector `θ`, often randomly initialized. It then repeats:

1. Measure how the cost changes with respect to each parameter.
2. Combine these partial derivatives into a **gradient vector**.
3. Move in the opposite direction of the gradient.
4. Repeat until progress becomes negligible or a stopping rule is reached.

The generic update is:

```text
θ ← θ - η ∇J(θ)
```

where:

- `J(θ)` is the cost function,
- `∇J(θ)` is its gradient,
- `η` (eta) is the **learning rate**.

### Learning rate: how large should each step be?

The learning rate controls training speed and stability.

- **Too small:** training is stable but painfully slow.
- **Reasonable:** the model reaches the minimum efficiently.
- **Too large:** the algorithm can overshoot repeatedly and diverge.

{{image:gradient-descent-learning-rates}}

A practical lesson follows: optimization failures are not always caused by the model itself. Sometimes the model is appropriate, but the training hyperparameters are poor.

### Convexity and the global minimum

A general cost function can contain local minima, ridges, and plateaus. Linear regression with MSE is easier: its cost function is convex. Informally, that means it has one global basin rather than many competing local minima.

For linear regression with MSE, gradient descent can therefore approach the global minimum as long as the learning rate is not too large and training runs long enough.

### Why feature scaling matters

Suppose one feature ranges from `0` to `1` while another ranges from `0` to `100000`. The cost surface becomes stretched. Gradient descent may zigzag through a long narrow valley instead of heading efficiently toward the minimum.

That is why the chapter recommends scaling features before gradient-descent training, for example using `StandardScaler`.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

The goal is not to make the data "better" in a semantic sense. The goal is to make the optimization geometry easier.

### Stopping training

Choosing a huge fixed epoch count wastes computation after the model has effectively converged. A better stopping idea is to watch the gradient norm or another convergence signal. When the gradient becomes tiny, parameter updates become tiny too.

The threshold used for such a stopping rule is often called a **tolerance**.

---

## 3. Batch, stochastic, and mini-batch gradient descent

The three major variants differ mainly in **how much training data they use to estimate the gradient for one update**.

### 3.1 Batch gradient descent

Batch gradient descent uses the **entire training set** for every gradient computation.

For linear regression, a vectorized gradient can be written as:

```text
∇MSE(θ) = (2/m) Xᵀ(Xθ - y)
```

A simple implementation is:

```python
eta = 0.1
n_epochs = 1000
m = len(X_b)

rng = np.random.default_rng(seed=42)
theta = rng.standard_normal((2, 1))

for epoch in range(n_epochs):
    gradients = 2 / m * X_b.T @ (X_b @ theta - y)
    theta = theta - eta * gradients
```

**Strength:** smooth, stable progress.  
**Weakness:** each step touches every training example, so a single update can be expensive on a huge dataset.

### 3.2 Stochastic gradient descent (SGD)

SGD takes the opposite approach: each update is based on **one randomly selected instance**.

That makes every update cheap, but also noisy. Instead of moving smoothly to the bottom, the parameters bounce around while improving on average.

This noise is not purely bad. On irregular cost surfaces, it can help the optimizer escape shallow local minima. But the same randomness makes it difficult to settle exactly at the minimum.

The chapter introduces a **learning schedule**: start with larger steps, then gradually reduce the learning rate so training can settle.

```python
n_epochs = 50
t0, t1 = 5, 50


def learning_schedule(t):
    return t0 / (t + t1)

rng = np.random.default_rng(seed=42)
theta = rng.standard_normal((2, 1))

for epoch in range(n_epochs):
    for iteration in range(m):
        random_index = rng.integers(m)
        xi = X_b[random_index : random_index + 1]
        yi = y[random_index : random_index + 1]
        gradients = 2 * xi.T @ (xi @ theta - yi)
        eta = learning_schedule(epoch * m + iteration)
        theta = theta - eta * gradients
```

### Why shuffling matters in SGD

SGD works best when the examples behave approximately like independent and identically distributed samples. If the dataset is ordered by class, time block, or another strong pattern and you iterate through it without appropriate care, updates can be systematically biased in sequence.

Shuffling the data between epochs is a simple way to reduce this problem when the task permits it.

### 3.3 Mini-batch gradient descent

Mini-batch gradient descent uses a small group of examples per update.

It combines useful properties of both extremes:

- more stable than single-example SGD;
- much cheaper per update than full-batch gradient descent;
- efficient on GPUs and other hardware optimized for matrix operations.

This is why mini-batch training became the standard pattern for modern deep learning.

{{image:gradient-descent-variants-paths}}

### Practical comparison

| Method | Gradient uses | Large dataset | Out-of-core potential | Stability | Typical role |
|---|---|---:|---:|---|---|
| Closed-form / SVD | Whole dataset algebraically | Good if it fits memory | No | Deterministic | Small/moderate feature counts |
| Batch GD | All examples per step | Can be slow per update | Usually no | Very smooth | Teaching, some convex optimization |
| SGD | One example per step | Excellent | Yes | Noisy | Streaming or very large data |
| Mini-batch GD | Small batch per step | Excellent | Yes | Moderately smooth | Modern practical training |

Scikit-Learn exposes SGD for regression through `SGDRegressor`:

```python
from sklearn.linear_model import SGDRegressor

sgd_reg = SGDRegressor(
    max_iter=1000,
    tol=1e-5,
    penalty=None,
    eta0=0.01,
    n_iter_no_change=100,
    random_state=42,
)
sgd_reg.fit(X, y.ravel())
```

`partial_fit()` can perform incremental updates without resetting training state, while `warm_start=True` allows supported estimators to continue from previously learned parameters when `fit()` is called again.

{{exercise:M01.L04.EX01}}

---

## 4. Polynomial regression, learning curves, and the bias/variance trade-off

Linear regression produces a linear function of its input features. That does **not** mean it can only model straight-line relationships.

The trick is to transform the input first.

Suppose the true pattern looks quadratic:

```text
y ≈ 0.5x² + x + 2
```

Create a second feature `x²`, then fit ordinary linear regression on `[x, x²]`.

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

poly_features = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly_features.fit_transform(X)

lin_reg = LinearRegression()
lin_reg.fit(X_poly, y)
```

The model is still **linear in its parameters**, even though its prediction curve is nonlinear in the original input.

### Interactions appear automatically

With multiple original features, `PolynomialFeatures` can create not only powers such as `a²` and `b³`, but also interaction terms such as `ab`, `a²b`, and `ab²`.

This is powerful, but the number of generated features can explode combinatorially as degree and feature count increase. High-degree polynomial models can therefore become expensive and prone to overfitting.

### Underfitting versus overfitting

Increasing model flexibility can move you through three regimes:

- **Underfitting:** the model is too simple to represent the real pattern.
- **Good fit:** the model captures the important structure without chasing noise.
- **Overfitting:** the model bends itself around training examples and noise, hurting generalization.

{{image:polynomial-model-complexity}}

### Learning curves

A learning curve compares training error and validation error as the amount of training data or the training progress changes.

A typical **underfitting** pattern is:

- training error is fairly high;
- validation error is also high;
- both curves become close to each other.

When this happens, simply adding more examples usually does not solve the core problem. The model or feature representation is too weak.

{{image:learning-curves-underfitting}}

A typical **overfitting** pattern is different:

- training error is low;
- validation error is noticeably higher;
- a persistent gap separates the curves.

More training data can sometimes reduce that gap, because it becomes harder for the model to memorize peculiarities of a small sample.

{{image:learning-curves-overfitting}}

### The bias/variance trade-off

Generalization error can be understood through three sources:

**Bias**  
Error caused by assumptions that are too restrictive. A high-bias model misses important structure and tends to underfit.

**Variance**  
Error caused by excessive sensitivity to the particular training sample. A high-variance model changes too much when the data changes slightly and tends to overfit.

**Irreducible error**  
Noise that cannot be eliminated simply by choosing a better model. Reducing it requires improving the data-generating or data-cleaning process.

Increasing model complexity usually lowers bias but raises variance. Stronger regularization usually does the reverse.

{{image:bias-variance-tradeoff}}

---

## 5. Regularization: controlling model flexibility

Regularization deliberately constrains a model so that it is less tempted to fit noise.

For polynomial regression, reducing the polynomial degree is one simple form of regularization. For linear models, the chapter focuses on constraining the learned weights.

Before comparing methods, remember one practical rule:

> **Scale your features before most regularized linear models.**

Without scaling, the penalty can affect features unfairly simply because their numerical units differ.

### 5.1 Ridge regression: shrink weights with an ℓ2 penalty

Ridge regression adds a penalty based on the squared ℓ2 norm of the feature weights.

Conceptually:

```text
training objective = MSE + α × squared_weight_size
```

The bias term is not regularized.

The hyperparameter `α` controls regularization strength:

- `α = 0` behaves like unregularized linear regression;
- larger `α` pushes weights closer to zero;
- excessive `α` can make the model too simple and increase bias.

```python
from sklearn.linear_model import Ridge

ridge_reg = Ridge(alpha=0.1, solver="cholesky")
ridge_reg.fit(X, y)
```

Ridge is a strong default when you want a stable linear model and expect many features to contribute somewhat.

### 5.2 Lasso regression: encourage sparse solutions with an ℓ1 penalty

Lasso adds a penalty based on the ℓ1 norm of the feature weights.

Its most distinctive behavior is that some coefficients can become **exactly zero**. That means lasso can perform a form of automatic feature selection.

```python
from sklearn.linear_model import Lasso

lasso_reg = Lasso(alpha=0.1)
lasso_reg.fit(X, y)
```

This sparsity is useful when you suspect that only a subset of features should matter. But very strong lasso regularization can remove useful signal too.

### Why ridge shrinks while lasso can eliminate

The geometry of the ℓ1 and ℓ2 penalties differs. Lasso's ℓ1 geometry makes solutions on parameter axes common, which corresponds to exact zeros. Ridge's smooth ℓ2 geometry tends to shrink parameters continuously toward zero without usually setting them exactly to zero.

{{image:lasso-vs-ridge-geometry}}

### 5.3 Elastic net: combine ridge and lasso

Elastic net mixes the two penalties. A mix ratio controls how lasso-like or ridge-like the penalty becomes.

- mix ratio `0` → ridge-like;
- mix ratio `1` → lasso-like;
- values between them blend both behaviors.

```python
from sklearn.linear_model import ElasticNet

elastic_net = ElasticNet(alpha=0.1, l1_ratio=0.5)
elastic_net.fit(X, y)
```

The chapter's practical guidance is:

- some regularization is usually preferable to none;
- ridge is a good default;
- lasso is useful when many features may be irrelevant;
- elastic net is often safer than pure lasso when features are strongly correlated or when there are more features than training instances.

### 5.4 Early stopping: regularize by stopping at the right time

Regularization does not always need an explicit penalty term. For iterative models, another strategy is to track validation performance and stop when it stops improving.

Typical pattern:

1. training error keeps decreasing;
2. validation error decreases at first;
3. validation error reaches a minimum;
4. validation error begins to increase as overfitting grows.

The model from the minimum-validation-error point is the one you want to keep.

{{image:early-stopping-validation-error}}

With noisy stochastic or mini-batch training, do not react to one tiny upward fluctuation. A common practical approach is to allow a patience period and then restore the best checkpoint seen so far.

```python
from copy import deepcopy
from sklearn.metrics import root_mean_squared_error

best_valid_rmse = float("inf")
best_model = None

for epoch in range(500):
    sgd_reg.partial_fit(X_train_prep, y_train)
    y_valid_pred = sgd_reg.predict(X_valid_prep)
    valid_rmse = root_mean_squared_error(y_valid, y_valid_pred)

    if valid_rmse < best_valid_rmse:
        best_valid_rmse = valid_rmse
        best_model = deepcopy(sgd_reg)
```

---

## 6. Logistic regression: turning a linear score into a probability

Despite its name, logistic regression is primarily used for **classification**.

For a binary problem, such as spam versus not spam, logistic regression first computes the familiar linear score:

```text
t = θᵀx
```

Instead of returning `t` directly, it passes the score through the **logistic sigmoid**:

```text
σ(t) = 1 / (1 + e⁻ᵗ)
```

The output is between `0` and `1`, so it can be interpreted as an estimated probability for the positive class.

### From probability to class

With the default 50% threshold:

```text
if estimated_probability >= 0.5:
    predict positive class
else:
    predict negative class
```

Because the sigmoid reaches `0.5` when the linear score is zero, this corresponds to predicting the positive class when `θᵀx >= 0`.

The raw linear score is often called a **logit**. The logit can also be viewed as the log-odds of the positive class.

### Training with log loss

The training objective should strongly penalize confident wrong probabilities.

If the true class is positive, predicting a probability near `0` should be very expensive. If the true class is negative, predicting a probability near `1` should be very expensive. **Log loss** has exactly this behavior.

For the whole dataset, logistic regression minimizes the average negative log-likelihood of the correct labels.

Unlike linear regression's normal equation, logistic regression does not have a direct closed-form solution for the optimal parameters. However, its log-loss objective is convex, so gradient-based optimization can find the global minimum under suitable optimization settings.

### Decision boundaries

A logistic classifier can produce probabilities everywhere, but a class prediction requires a threshold. The set of feature values where the model is exactly at the threshold forms the **decision boundary**.

For ordinary logistic regression, that boundary is linear in the feature space.

The chapter demonstrates this with the Iris dataset, first using only petal width and then using petal width plus petal length.

{{image:logistic-probability-decision-boundary}}

A minimal Scikit-Learn example is:

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

iris = load_iris(as_frame=True)
X = iris.data[["petal width (cm)"]].values
y = iris.target_names[iris.target] == "virginica"

X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42
)

log_reg = LogisticRegression(random_state=42)
log_reg.fit(X_train, y_train)

print(log_reg.predict_proba([[1.7]]))
print(log_reg.predict([[1.7]]))
```

### Regularization in `LogisticRegression`

Scikit-Learn regularizes logistic regression by default. One naming detail is easy to get wrong:

- many linear models expose strength through `alpha`;
- `LogisticRegression` uses `C`, which acts inversely.

So:

```text
larger C  -> weaker regularization
smaller C -> stronger regularization
```

Logistic regression can use ℓ1 or ℓ2 penalties depending on the chosen solver and configuration.

---

## 7. Softmax regression: multiclass classification in one model

Binary logistic regression asks, "How likely is class 1?"

Softmax regression, also called **multinomial logistic regression**, extends the idea to multiple **mutually exclusive** classes.

For an input `x`, the model computes one linear score for each class:

```text
score_class_1 = θ₁ᵀx
score_class_2 = θ₂ᵀx
...
score_class_K = θ_Kᵀx
```

Each class therefore has its own parameter vector.

### Softmax converts scores into probabilities

The raw class scores are not probabilities. Softmax exponentiates and normalizes them so that:

- every class probability is between `0` and `1`;
- all class probabilities sum to `1`.

Conceptually:

```text
probability(class k) = exp(score_k) / sum(exp(all class scores))
```

The model predicts the class with the highest estimated probability using `argmax`.

A subtle but important point: the winning class does **not** need probability above 50%. With three classes, probabilities such as `0.40`, `0.35`, and `0.25` still produce a clear winner.

### Softmax is multiclass, not multioutput

Use softmax when exactly one class should be selected from mutually exclusive alternatives, such as three flower species.

Do **not** use one softmax output when several labels may all be true at the same time. For example, an image could be both "outdoor" and "nighttime"; those are two independent binary targets, not mutually exclusive classes.

### Cross-entropy loss

To train softmax regression, the chapter introduces **cross entropy**. It penalizes the model when it assigns low probability to the correct class.

For one-hot targets, the loss focuses on the probability assigned to the true class:

```text
cross-entropy = -log(probability assigned to the correct class)
```

Across the full dataset, these losses are averaged.

When there are exactly two classes, this reduces to the same log-loss idea used by binary logistic regression.

The chapter also connects cross entropy to information theory: if your predicted probability distribution disagrees strongly with the true distribution, the coding cost becomes larger.

### Iris example

Scikit-Learn's `LogisticRegression` can train a multiclass softmax model when given more than two target classes with a suitable solver.

```python
X = iris.data[["petal length (cm)", "petal width (cm)"]].values
y = iris["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42
)

softmax_reg = LogisticRegression(C=30, random_state=42)
softmax_reg.fit(X_train, y_train)

print(softmax_reg.predict([[5, 2]]))
print(softmax_reg.predict_proba([[5, 2]]).round(2))
```

The source example predicts Iris virginica for a flower with petals roughly 5 cm long and 2 cm wide, with the model assigning the overwhelming majority of probability to that class.

{{image:softmax-multiclass-decision-boundaries}}

{{exercise:M01.L04.EX02}}

---

## 8. Putting the chapter together: how to choose what to try

The chapter is easier to remember if you view it as a sequence of engineering decisions.

### If the target is continuous

Start with a regression model.

- Relationship roughly linear and feature count manageable → `LinearRegression` is a useful baseline.
- Huge feature space or streaming/very large data → gradient-based training becomes attractive.
- Clear nonlinear curvature → consider polynomial features, but control complexity.

### If optimization is slow or unstable

Check:

1. Are the features on very different scales?
2. Is the learning rate too small?
3. Is the learning rate so large that the loss diverges?
4. Is full-batch training too expensive for the dataset size?
5. Would mini-batches or SGD fit the hardware/data setting better?

### If training error and validation error are both high

Think **underfitting / high bias**.

Possible responses:

- use a more expressive model;
- engineer better features;
- reduce excessive regularization.

Adding more data alone is unlikely to fix a model that cannot even fit its training set adequately.

### If training error is low but validation error is much higher

Think **overfitting / high variance**.

Possible responses:

- collect more training data;
- simplify the model;
- increase regularization;
- use early stopping for iterative learners.

### Choosing a linear regularizer

| Method | Main effect | Best mental model |
|---|---|---|
| Ridge | Shrinks all weights | "Keep the model stable and moderate" |
| Lasso | Can set weights exactly to zero | "Prefer a sparse set of useful features" |
| Elastic net | Mixes ridge and lasso | "Get sparsity with more stability under correlated features" |
| Early stopping | Limits how long fitting continues | "Stop before validation performance starts degrading" |

### If the target is categorical

- Two mutually exclusive classes → logistic regression.
- More than two mutually exclusive classes → softmax regression.
- Multiple independent labels can be true together → separate binary outputs/classifiers rather than one softmax choice.

### The deepest connection in the chapter

Linear regression, logistic regression, and softmax regression may look like different algorithms, but they share a common architecture:

```text
features
   ↓
linear scores from learned parameters
   ↓
possibly transform scores into probabilities
   ↓
compute a differentiable loss
   ↓
optimize parameters
```

That pattern prepares you for neural networks. A neural network changes the function that creates the scores, but training still revolves around parameters, differentiable losses, gradients, learning rates, mini-batches, regularization, and validation.

---

## Important misconceptions

### Misconception 1

> "Gradient descent is the model."

### Why this is wrong

Gradient descent is a **training algorithm**. Linear regression, logistic regression, and neural networks are models. The same model can sometimes be trained by different algorithms.

### Misconception 2

> "Lower training error always means a better model."

### Why this is wrong

A model can achieve extremely low training error by fitting noise. Validation performance and learning curves help determine whether the model generalizes.

### Misconception 3

> "Logistic regression predicts a class directly."

### Why this is wrong

It first estimates a probability using the sigmoid function. A decision threshold then converts that probability into a class.

### Misconception 4

> "Softmax is the right choice whenever a task has several labels."

### Why this is wrong

Softmax assumes one mutually exclusive class is selected. Multi-label problems require a different output formulation, commonly independent sigmoid outputs or binary classifiers.

---

## Key terminology

| Term | Meaning |
|---|---|
| Parameter | A value learned from training data, such as a weight or bias |
| Hyperparameter | A setting chosen outside the learned parameters, such as learning rate or regularization strength |
| Cost function | A scalar quantity the training algorithm tries to minimize |
| MSE | Mean squared error, a common regression training objective |
| Gradient | Vector of partial derivatives showing how the cost changes with each parameter |
| Learning rate | Step-size control used by gradient-based optimization |
| Epoch | One training pass or conventional round over the dataset |
| Batch GD | Gradient descent using the entire training set per update |
| SGD | Gradient descent using one example per update |
| Mini-batch GD | Gradient descent using a small subset per update |
| Learning schedule | Rule that changes the learning rate during training |
| Polynomial features | Powers and interactions of original features used to model nonlinear relationships |
| Learning curve | Plot comparing training and validation behavior as training data or training progress changes |
| Bias | Error caused by an overly restrictive model or assumptions |
| Variance | Error caused by excessive sensitivity to the training sample |
| Regularization | Constraint that reduces model flexibility to improve generalization |
| Ridge | Linear model with an ℓ2 penalty |
| Lasso | Linear model with an ℓ1 penalty that can create sparse coefficients |
| Elastic net | Regularization that combines ℓ1 and ℓ2 penalties |
| Early stopping | Keeping the model from the point of best validation performance |
| Sigmoid | S-shaped function mapping a real score into the range 0 to 1 |
| Logit | Linear score / log-odds used by logistic regression |
| Decision boundary | Feature-space boundary where predicted class changes |
| Softmax | Function that converts multiple class scores into probabilities summing to 1 |
| Cross entropy | Classification loss that penalizes low probability on the correct class |

---

## Self-check

Before continuing, make sure you can answer:

1. What is the difference between a model, a parameter, a loss function, and a training algorithm?
2. Why can minimizing MSE and minimizing RMSE lead to the same best linear-regression parameters?
3. Why does feature scaling often make gradient descent converge faster?
4. What is the main computational difference between batch GD, SGD, and mini-batch GD?
5. What learning-curve pattern suggests underfitting? What pattern suggests overfitting?
6. Why can lasso set coefficients to zero while ridge usually only shrinks them?
7. Why should early stopping be based on validation performance rather than training loss alone?
8. How does logistic regression turn a linear score into a probability?
9. Why can softmax predict a class with less than 50% probability?
10. When would separate binary classifiers be more appropriate than one softmax classifier?

---

## Retain this idea

**Training a model means choosing parameters that minimize a useful objective, while good machine-learning engineering also controls optimization, model complexity, and generalization—not just training error.**
"""
        ),

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "linear-regression",
                "title": "Linear regression: what exactly is being learned?",
                "order": 1,
            },
            {
                "id": "gradient-descent",
                "title": "Gradient descent: learning by taking downhill steps",
                "order": 2,
            },
            {
                "id": "gradient-descent-variants",
                "title": "Batch, stochastic, and mini-batch gradient descent",
                "order": 3,
            },
            {
                "id": "polynomial-regression",
                "title": "Polynomial regression, learning curves, and the bias/variance trade-off",
                "order": 4,
            },
            {
                "id": "regularization",
                "title": "Regularization: controlling model flexibility",
                "order": 5,
            },
            {
                "id": "logistic-regression",
                "title": "Logistic regression: turning a linear score into a probability",
                "order": 6,
            },
            {
                "id": "softmax-regression",
                "title": "Softmax regression: multiclass classification in one model",
                "order": 7,
            },
            {
                "id": "model-selection",
                "title": "Putting the chapter together: how to choose what to try",
                "order": 8,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L04.EX01",

            "title": "Diagnose and Compare Gradient Descent Strategies",

            "lesson_code": "M01.L04",

            "section_id": "gradient-descent-variants",

            "placement": "after_section",

            "description": (
                "Practice reasoning about learning rate, feature scaling, and the "
                "trade-offs among batch, stochastic, and mini-batch gradient descent."
            ),

            "instructions": (
                "1. Imagine a regression dataset with 5 million rows and 50 numeric features. "
                "Explain why full-batch gradient descent may be inconvenient.\n"
                "2. Choose either SGD or mini-batch GD for this setting and justify the choice.\n"
                "3. Suppose training loss oscillates but trends downward. Explain why this is not "
                "automatically a failure for SGD or mini-batch training.\n"
                "4. Suppose one feature ranges from 0 to 1 and another from 0 to 1,000,000. "
                "State what preprocessing you would apply and why.\n"
                "5. Finally, explain what you would expect if the learning rate were far too high."
            ),

            "expected_output": (
                "A short technical analysis that selects an optimizer, explains the expected "
                "training behavior, identifies the need for scaling, and diagnoses a too-high "
                "learning rate."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "gradient-descent-selection",
                "learning-rate-diagnosis",
                "feature-scaling",
                "optimization-reasoning",
            ],
        },

        {
            "id": "M01.L04.EX02",

            "title": "Choose the Right Linear Model and Regularization Strategy",

            "lesson_code": "M01.L04",

            "section_id": "softmax-regression",

            "placement": "after_section",

            "description": (
                "Apply learning-curve, regularization, logistic-regression, and softmax concepts "
                "to realistic model-selection scenarios."
            ),

            "instructions": (
                "1. A polynomial model has very low training RMSE but much higher validation RMSE. "
                "Diagnose the problem and give two fixes.\n"
                "2. A ridge model has high and nearly equal training and validation error. Decide "
                "whether this is mainly high bias or high variance and state how you would adjust "
                "regularization.\n"
                "3. Choose ridge, lasso, or elastic net when you have many strongly correlated "
                "features but expect only some to be useful, and explain the choice.\n"
                "4. For classifying one flower into exactly one of three species, choose binary "
                "logistic classifiers or softmax regression and justify the answer.\n"
                "5. For an image that may independently be both 'outdoor' and 'nighttime', explain "
                "why one softmax output is inappropriate."
            ),

            "expected_output": (
                "A scenario-by-scenario model-selection explanation that correctly identifies "
                "overfitting versus underfitting, chooses regularization, and distinguishes "
                "binary, multiclass, and multi-label classification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "learning-curve-interpretation",
                "regularization-selection",
                "logistic-regression",
                "softmax-regression",
                "classification-framing",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L04.QZ01",

        "title": "Training Models: From Linear Regression to Softmax — Knowledge Check",

        "lesson_code": "M01.L04",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L04.Q01",

                "section_id": "linear-regression",

                "question": (
                    "Why can linear regression minimize MSE during training even if RMSE is the "
                    "reported regression metric?"
                ),

                "options": [
                    "MSE and RMSE are always numerically equal",
                    "They reach their minimum at the same parameter values because square root is monotonic for positive errors",
                    "RMSE cannot be computed on training data",
                    "MSE automatically regularizes the coefficients",
                ],

                "correct": 1,

                "explanation": (
                    "RMSE is the square root of MSE. Since square root increases monotonically for "
                    "nonnegative values, the parameters that minimize MSE also minimize RMSE."
                ),
            },

            {
                "id": "M01.L04.Q02",

                "section_id": "gradient-descent-variants",

                "question": (
                    "Which statement best describes mini-batch gradient descent?"
                ),

                "options": [
                    "It computes one update from the entire training set and never repeats",
                    "It computes each update from exactly one training example",
                    "It computes updates from small subsets, balancing noisy SGD updates with efficient matrix operations",
                    "It solves the normal equation on a random subset",
                ],

                "correct": 2,

                "explanation": (
                    "Mini-batch GD estimates the gradient using small batches. This is usually more "
                    "hardware-efficient than one-example SGD while much cheaper per update than full-batch GD."
                ),
            },

            {
                "id": "M01.L04.Q03",

                "section_id": "polynomial-regression",

                "question": (
                    "A model has low training error but substantially higher validation error. What is the most likely diagnosis?"
                ),

                "options": [
                    "Overfitting / high variance",
                    "Underfitting / high bias",
                    "The model has already reached perfect generalization",
                    "The target must be categorical",
                ],

                "correct": 0,

                "explanation": (
                    "A persistent gap where training performance is much better than validation "
                    "performance is a classic sign of overfitting and high variance."
                ),
            },

            {
                "id": "M01.L04.Q04",

                "section_id": "regularization",

                "question": (
                    "Which property most clearly distinguishes lasso from ridge regression?"
                ),

                "options": [
                    "Lasso cannot be used with numeric features",
                    "Lasso never requires feature scaling",
                    "Lasso always has lower validation error",
                    "Lasso can drive some feature weights exactly to zero and therefore create sparse models",
                ],

                "correct": 3,

                "explanation": (
                    "The ℓ1 penalty used by lasso can produce exact zero coefficients. Ridge's ℓ2 "
                    "penalty generally shrinks coefficients toward zero without eliminating them."
                ),
            },

            {
                "id": "M01.L04.Q05",

                "section_id": "softmax-regression",

                "type": "open",

                "question": (
                    "You are designing two vision tasks. Task A assigns each image to exactly one "
                    "of three animal species. Task B independently predicts whether an image is "
                    "outdoor and whether it is nighttime. Explain which task is naturally suited "
                    "to softmax regression and how you would frame the other task."
                ),
            },
        ],

        "passing_score": 70,
    },
}
