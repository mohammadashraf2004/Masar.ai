"""M05.L01 — The Mechanics of Learning.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 5.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M05.L01"
MODULE_ORDER = 5
MODULE_TITLE = "The Mechanics of Learning"
MODULE_DESCRIPTION = (
    "Understand learning as parameter estimation: define a model and loss, compute "
    "gradients, update parameters with gradient descent, use PyTorch autograd and "
    "optimizers, and evaluate generalization with training, validation, and test data."
)

SOURCE_CHAPTER = 5
SOURCE_PAGES = "Chapter 5 (page range not provided in source excerpt)"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "The Mechanics of Learning",
    "slug": "applied-deep-learning-m05-l01",
    "description": (
        "A first-principles explanation of how models learn from data through loss "
        "minimization, differentiation, gradient descent, autograd, optimization, "
        "normalization, and validation."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 3.0,
    "skill_tags": [
        "machine-learning",
        "parameter-estimation",
        "regression",
        "loss-functions",
        "gradient-descent",
        "derivatives",
        "backpropagation",
        "autograd",
        "optimizers",
        "normalization",
        "validation",
        "overfitting",
        "module-05",
    ],
    "prerequisite_ids": ["M04.L01"],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "The Mechanics of Learning",
        "content": (
            "# The Mechanics of Learning\n"
            "\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M05.L01  \n"
            "> **Module:** The Mechanics of Learning  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, "
            "Chapter 5. This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain learning as estimating model parameters from paired input/output data.\n"
            "- Distinguish a model, its parameters, a loss function, and an optimizer.\n"
            "- Build and fit a simple linear regression model in PyTorch.\n"
            "- Explain why mean squared error can be used as a loss for continuous predictions.\n"
            "- Describe gradient descent intuitively and mathematically.\n"
            "- Explain the roles of derivatives, partial derivatives, gradients, and the chain rule.\n"
            "- Implement a basic training loop.\n"
            "- Distinguish an epoch from a training iteration or step.\n"
            "- Explain how learning rate affects convergence and divergence.\n"
            "- Explain why input normalization can improve optimization.\n"
            "- Use `requires_grad`, `.backward()`, and `.grad` with PyTorch autograd.\n"
            "- Explain why gradients must normally be cleared between optimization steps.\n"
            "- Use `torch.optim.SGD` and understand the purpose of `optimizer.zero_grad()` and `optimizer.step()`.\n"
            "- Explain the high-level difference between SGD and an adaptive optimizer such as Adam.\n"
            "- Separate training, validation, and test sets and explain their different roles.\n"
            "- Recognize underfitting, overfitting, and data leakage.\n"
            "- Use `torch.no_grad()` when gradients are not needed.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Learning is model fitting\n"
            "\n"
            "A learning algorithm receives examples of inputs together with desired outputs. Its goal "
            "is to adjust a model so that the model can produce useful outputs not only for the examples "
            "used during training, but also for sufficiently similar new inputs.\n"
            "\n"
            "The chapter connects this idea with a much older scientific workflow: collect observations, "
            "choose a model, estimate its unknown parameters, check the model against observations that "
            "were not used to fit it, and revise if necessary.\n"
            "\n"
            "This is the core idea behind modern supervised learning too.\n"
            "\n"
            "A **model** is a function with unknown parameters. Learning consists of estimating those "
            "parameters from data.\n"
            "\n"
            "A useful high-level picture is:\n"
            "\n"
            "```text\n"
            "input data + desired output\n"
            "          |\n"
            "          v\n"
            "      model(params)\n"
            "          |\n"
            "          v\n"
            "       prediction\n"
            "          |\n"
            "          v\n"
            "compare with desired output\n"
            "          |\n"
            "          v\n"
            "         loss\n"
            "          |\n"
            "          v\n"
            "compute gradient\n"
            "          |\n"
            "          v\n"
            "update parameters\n"
            "          |\n"
            "        repeat\n"
            "```\n"
            "\n"
            '{{image:mental-model-of-learning}}'
            '\n'
            "\n"
            "Deep neural networks are much larger and more flexible than the simple model in this lesson, "
            "but the same training logic remains.\n"
            "\n"
            "---\n"
            "\n"

            "## 2. A simple regression problem\n"
            "\n"
            "To expose every moving part clearly, the chapter uses a deliberately small problem: an "
            "unlabeled thermometer produces readings in unknown units, and we also have corresponding "
            "temperatures measured in Celsius.\n"
            "\n"
            "The paired data is:\n"
            "\n"
            "```python\n"
            "import torch\n"
            "\n"
            "t_c = torch.tensor([\n"
            "    0.5, 14.0, 15.0, 28.0, 11.0, 8.0,\n"
            "    3.0, -4.0, 6.0, 13.0, 21.0,\n"
            "])\n"
            "\n"
            "t_u = torch.tensor([\n"
            "    35.7, 55.9, 58.2, 81.9, 56.3, 48.9,\n"
            "    33.9, 21.8, 48.4, 60.4, 68.4,\n"
            "])\n"
            "```\n"
            "\n"
            "`t_u` is the input measurement and `t_c` is the desired Celsius output.\n"
            "\n"
            "The problem is **regression** because the model predicts a continuous numerical value.\n"
            "\n"
            "A plot suggests that the relationship may be approximately linear.\n"
            "\n"
            "[[IMAGE_NEEDED: Noisy thermometer measurements | "
            "A scatter plot with unknown thermometer reading on the horizontal axis and Celsius "
            "temperature on the vertical axis, showing an approximately linear trend with some noise | "
            "Learner should notice that a straight line appears to be a reasonable first model even "
            "though the points are not perfectly aligned]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Choose the model and its parameters\n"
            "\n"
            "We begin with the simplest reasonable assumption: a linear relationship.\n"
            "\n"
            "```text\n"
            "t_p = w * t_u + b\n"
            "```\n"
            "\n"
            "where:\n"
            "\n"
            "- `t_p` is the predicted Celsius temperature,\n"
            "- `w` is the **weight** or scaling parameter,\n"
            "- `b` is the **bias** or additive offset.\n"
            "\n"
            "In PyTorch:\n"
            "\n"
            "```python\n"
            "def model(t_u, w, b):\n"
            "    return w * t_u + b\n"
            "```\n"
            "\n"
            "The weight and bias are the values we want learning to discover.\n"
            "\n"
            "This distinction matters:\n"
            "\n"
            "| Item | Meaning |\n"
            "|---|---|\n"
            "| Model structure | The formula `w * t_u + b` |\n"
            "| Parameters | `w` and `b`, which are learned |\n"
            "| Data | Observed `t_u` and `t_c` pairs |\n"
            "| Prediction | Output produced by the current parameters |\n"
            "\n"
            "A neural network uses far more parameters and a more complicated function, but training "
            "still means finding parameter values that reduce prediction error.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Loss: turn prediction error into a number to minimize\n"
            "\n"
            "To improve the model, we first need a numerical measure of how badly it is performing.\n"
            "\n"
            "That measure is the **loss function**.\n"
            "\n"
            "For each prediction we can compute:\n"
            "\n"
            "```text\n"
            "prediction error = predicted value - true value\n"
            "```\n"
            "\n"
            "But simply averaging signed errors could let positive and negative mistakes cancel each "
            "other. We therefore need a loss that penalizes errors regardless of direction.\n"
            "\n"
            "Two simple possibilities are:\n"
            "\n"
            "```text\n"
            "|prediction - target|\n"
            "```\n"
            "\n"
            "and:\n"
            "\n"
            "```text\n"
            "(prediction - target)^2\n"
            "```\n"
            "\n"
            "The chapter chooses squared differences because the curve is smooth around its minimum "
            "and because larger errors receive stronger penalties.\n"
            "\n"
            "[[IMAGE_NEEDED: Absolute error versus squared error | "
            "Two simple loss curves centered at zero error: a V-shaped absolute-error curve and a "
            "smooth U-shaped squared-error curve | Learner should notice that both are minimized at "
            "zero but squared error is smooth and grows more strongly for large errors]]\n"
            "\n"
            "A mean squared loss is:\n"
            "\n"
            "```python\n"
            "def loss_fn(t_p, t_c):\n"
            "    squared_diffs = (t_p - t_c) ** 2\n"
            "    return squared_diffs.mean()\n"
            "```\n"
            "\n"
            "For initial values:\n"
            "\n"
            "```python\n"
            "w = torch.ones(())\n"
            "b = torch.zeros(())\n"
            "\n"
            "t_p = model(t_u, w, b)\n"
            "loss = loss_fn(t_p, t_c)\n"
            "```\n"
            "\n"
            "The job of learning is now well defined:\n"
            "\n"
            "> **Find values of `w` and `b` that make the loss as small as possible.**\n"
            "\n"
            "{{exercise:M05.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Gradient descent: which way should the parameters move?\n"
            "\n"
            "Imagine a machine with two knobs, `w` and `b`, and a display showing the current loss.\n"
            "\n"
            "If turning a knob slightly one way makes the loss decrease, that is a useful direction. "
            "If it makes the loss increase, move the knob the other way.\n"
            "\n"
            "Gradient descent formalizes this process.\n"
            "\n"
            "[[IMAGE_NEEDED: Gradient descent as parameter knobs | "
            "A conceptual machine with two knobs labeled w and b and a loss display, with arrows "
            "showing adjustments toward lower loss | Learner should notice that each parameter is "
            "adjusted according to how changing it affects the loss]]\n"
            "\n"
            "The central update rule is:\n"
            "\n"
            "```text\n"
            "new_parameter = old_parameter - learning_rate * gradient\n"
            "```\n"
            "\n"
            "The **gradient** describes how the loss changes when the parameters change.\n"
            "\n"
            "The **learning rate** controls how large each update is.\n"
            "\n"
            "If a gradient is positive, increasing that parameter would locally increase loss, so the "
            "subtraction moves it in the opposite direction. If the gradient is negative, the update "
            "moves the parameter upward.\n"
            "\n"
            "### Numerical approximation\n"
            "\n"
            "Before using calculus, we can estimate the rate of change around a parameter by evaluating "
            "the loss slightly on both sides:\n"
            "\n"
            "```python\n"
            "delta = 0.1\n"
            "\n"
            "loss_rate_of_change_w = (\n"
            "    loss_fn(model(t_u, w + delta, b), t_c)\n"
            "    - loss_fn(model(t_u, w - delta, b), t_c)\n"
            ") / (2.0 * delta)\n"
            "```\n"
            "\n"
            "Then:\n"
            "\n"
            "```python\n"
            "learning_rate = 1e-2\n"
            "w = w - learning_rate * loss_rate_of_change_w\n"
            "```\n"
            "\n"
            "This captures the core idea, but repeatedly probing every parameter this way becomes "
            "impractical for models with large numbers of parameters.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Derivatives, gradients, and the chain rule\n"
            "\n"
            "Instead of estimating a slope using nearby points, calculus gives us the exact local rate "
            "of change through a **derivative**.\n"
            "\n"
            "For multiple parameters, we compute one partial derivative per parameter and collect them "
            "into a **gradient**.\n"
            "\n"
            "[[IMAGE_NEEDED: Numerical versus analytical gradient | "
            "A curve with one slope estimated from two nearby points and another tangent slope drawn "
            "exactly at a point | Learner should notice that finite differences approximate local change "
            "whereas differentiation gives the local derivative directly]]\n"
            "\n"
            "Our prediction is produced by a model, and the prediction is then passed into a loss. "
            "Therefore the effect of `w` on the loss passes through more than one function.\n"
            "\n"
            "The **chain rule** lets us combine those effects:\n"
            "\n"
            "```text\n"
            "d loss / d w\n"
            "=\n"
            "(d loss / d prediction)\n"
            "×\n"
            "(d prediction / d w)\n"
            "```\n"
            "\n"
            "For the mean squared loss, the chapter derives:\n"
            "\n"
            "```python\n"
            "def dloss_fn(t_p, t_c):\n"
            "    return 2 * (t_p - t_c) / t_p.size(0)\n"
            "```\n"
            "\n"
            "For the linear model:\n"
            "\n"
            "```python\n"
            "def dmodel_dw(t_u, w, b):\n"
            "    return t_u\n"
            "\n"
            "def dmodel_db(t_u, w, b):\n"
            "    return 1.0\n"
            "```\n"
            "\n"
            "Putting them together:\n"
            "\n"
            "```python\n"
            "def grad_fn(t_u, t_c, t_p, w, b):\n"
            "    dloss_dtp = dloss_fn(t_p, t_c)\n"
            "    dloss_dw = dloss_dtp * dmodel_dw(t_u, w, b)\n"
            "    dloss_db = dloss_dtp * dmodel_db(t_u, w, b)\n"
            "    return torch.stack([\n"
            "        dloss_dw.sum(),\n"
            "        dloss_db.sum(),\n"
            "    ])\n"
            "```\n"
            "\n"
            "This is backpropagation in a tiny example: start from the loss and propagate derivatives "
            "back through the operations that produced it.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Build the training loop\n"
            "\n"
            "Once we can compute predictions, loss, and gradients, training is a repetition of four "
            "basic stages:\n"
            "\n"
            "```text\n"
            "1. forward pass\n"
            "2. calculate loss\n"
            "3. backward pass / gradients\n"
            "4. update parameters\n"
            "```\n"
            "\n"
            "A manual loop looks like:\n"
            "\n"
            "```python\n"
            "def training_loop(n_epochs, learning_rate, params, t_u, t_c):\n"
            "    for epoch in range(1, n_epochs + 1):\n"
            "        w, b = params\n"
            "\n"
            "        t_p = model(t_u, w, b)\n"
            "        loss = loss_fn(t_p, t_c)\n"
            "        grad = grad_fn(t_u, t_c, t_p, w, b)\n"
            "\n"
            "        params = params - learning_rate * grad\n"
            "\n"
            "    return params\n"
            "```\n"
            "\n"
            "### Epoch versus step\n"
            "\n"
            "An **epoch** is one complete pass through the entire training dataset.\n"
            "\n"
            "A **training step/iteration** normally processes one batch and updates parameters once.\n"
            "\n"
            "In this tiny example, the whole dataset is used at once, so one step is also one epoch. "
            "For large datasets split into minibatches, many steps are required to complete one epoch.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Learning rate: too large, too small, or useful\n"
            "\n"
            "The chapter deliberately shows training fail when the learning rate is too large.\n"
            "\n"
            "With a large update, the parameters overshoot the minimum. The next update overshoots back "
            "the other way, often by an even larger amount. The loss can explode until numerical values "
            "become infinite.\n"
            "\n"
            "[[IMAGE_NEEDED: Converging versus diverging gradient descent | "
            "Two bowl-shaped loss plots: one with steps jumping back and forth farther away from the "
            "minimum, and another with smaller steps approaching the minimum | Learner should notice "
            "that the learning rate controls update size and can determine whether optimization "
            "converges or diverges]]\n"
            "\n"
            "A smaller learning rate stabilizes the updates, but if it becomes too small, learning can "
            "be painfully slow.\n"
            "\n"
            "The learning rate is a **hyperparameter**: it affects how learning proceeds, but it is not "
            "one of the model parameters being learned by this gradient descent process.\n"
            "\n"
            "Other examples of hyperparameters include the number of epochs and choices related to the "
            "optimizer.\n"
            "\n"
            "The practical lesson is not that one learning rate is universally correct. It is that "
            "unstable or stagnant optimization often requires us to inspect the update scale.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Why input normalization helps optimization\n"
            "\n"
            "In the initial thermometer problem, the gradient for `w` is much larger than the gradient "
            "for `b`. This creates an awkward optimization problem: one learning rate may be too large "
            "for one parameter but too small for the other.\n"
            "\n"
            "The chapter improves the situation by rescaling the input:\n"
            "\n"
            "```python\n"
            "t_un = 0.1 * t_u\n"
            "```\n"
            "\n"
            "This simple transformation brings the effective scales closer together. With normalized "
            "input, the same learning rate can update both parameters more sensibly.\n"
            "\n"
            "This is why data normalization is not merely cosmetic preprocessing. It can directly "
            "change the geometry of the optimization problem and make gradient descent more stable.\n"
            "\n"
            "After sufficient training, the example obtains parameters close to the real Fahrenheit-to-"
            "Celsius conversion relationship once the earlier input scaling is taken into account.\n"
            "\n"
            "The loss does not need to reach exactly zero because real or simulated measurements can "
            "contain noise and may not lie perfectly on the chosen model function.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. PyTorch autograd: stop deriving every gradient by hand\n"
            "\n"
            "Hand-derived gradients are useful for understanding the mechanics, but they do not scale "
            "to deep networks containing millions of parameters and long compositions of operations.\n"
            "\n"
            "PyTorch solves this using **autograd**.\n"
            "\n"
            "Start by marking parameters for gradient tracking:\n"
            "\n"
            "```python\n"
            "params = torch.tensor(\n"
            "    [1.0, 0.0],\n"
            "    requires_grad=True,\n"
            ")\n"
            "```\n"
            "\n"
            "Then compute the forward path normally:\n"
            "\n"
            "```python\n"
            "loss = loss_fn(model(t_u, *params), t_c)\n"
            "```\n"
            "\n"
            "Because `params` requires gradients, PyTorch tracks the relevant operations in a "
            "**computation graph**.\n"
            "\n"
            "Now call:\n"
            "\n"
            "```python\n"
            "loss.backward()\n"
            "```\n"
            "\n"
            "and inspect:\n"
            "\n"
            "```python\n"
            "print(params.grad)\n"
            "```\n"
            "\n"
            "The gradient of the loss with respect to each parameter is now available automatically.\n"
            "\n"
            "[[IMAGE_NEEDED: Autograd forward and backward computation graph | "
            "A small graph showing parameters feeding a linear model, prediction feeding a loss node, "
            "then backward arrows from loss through the model to parameter gradients | Learner should "
            "notice that the forward pass records dependencies and backward traverses them in reverse "
            "to apply the chain rule]]\n"
            "\n"
            "### The critical gradient-accumulation rule\n"
            "\n"
            "PyTorch **accumulates** gradients in leaf tensors. It does not automatically replace the "
            "previous gradient every time `.backward()` is called.\n"
            "\n"
            "Therefore, before computing gradients for the next training step, the old gradient "
            "normally needs to be cleared:\n"
            "\n"
            "```python\n"
            "if params.grad is not None:\n"
            "    params.grad.zero_()\n"
            "```\n"
            "\n"
            "If you forget this, gradients from different steps are added together and the update no "
            "longer represents just the current loss.\n"
            "\n"
            "{{exercise:M05.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Updating parameters safely with autograd\n"
            "\n"
            "Autograd should track the forward computation that produces the loss, but we generally do "
            "not want the parameter-update arithmetic itself added to the new forward graph.\n"
            "\n"
            "The chapter therefore performs the manual update inside `torch.no_grad()`:\n"
            "\n"
            "```python\n"
            "with torch.no_grad():\n"
            "    params -= learning_rate * params.grad\n"
            "```\n"
            "\n"
            "A complete autograd-driven loop is:\n"
            "\n"
            "```python\n"
            "def training_loop(n_epochs, learning_rate, params, t_u, t_c):\n"
            "    for epoch in range(1, n_epochs + 1):\n"
            "        if params.grad is not None:\n"
            "            params.grad.zero_()\n"
            "\n"
            "        t_p = model(t_u, *params)\n"
            "        loss = loss_fn(t_p, t_c)\n"
            "        loss.backward()\n"
            "\n"
            "        with torch.no_grad():\n"
            "            params -= learning_rate * params.grad\n"
            "\n"
            "    return params\n"
            "```\n"
            "\n"
            "At this point, PyTorch has replaced our hand-written derivative functions, but the "
            "underlying mathematical logic is unchanged.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Let optimizers handle the update rule\n"
            "\n"
            "PyTorch provides the `torch.optim` module so that we do not need to manually implement "
            "parameter updates for every model.\n"
            "\n"
            "### SGD\n"
            "\n"
            "```python\n"
            "import torch.optim as optim\n"
            "\n"
            "params = torch.tensor([1.0, 0.0], requires_grad=True)\n"
            "optimizer = optim.SGD([params], lr=1e-2)\n"
            "```\n"
            "\n"
            "The optimizer stores references to the parameters it is responsible for updating.\n"
            "\n"
            "A standard step becomes:\n"
            "\n"
            "```python\n"
            "t_p = model(t_un, *params)\n"
            "loss = loss_fn(t_p, t_c)\n"
            "\n"
            "optimizer.zero_grad()\n"
            "loss.backward()\n"
            "optimizer.step()\n"
            "```\n"
            "\n"
            "Three operations are worth memorizing conceptually:\n"
            "\n"
            "```text\n"
            "optimizer.zero_grad() -> clear old accumulated parameter gradients\n"
            "loss.backward()       -> compute current gradients\n"
            "optimizer.step()      -> update parameters using those gradients\n"
            "```\n"
            "\n"
            "The training loop becomes reusable because the exact update strategy is delegated to the "
            "optimizer object.\n"
            "\n"
            "### Why the name stochastic gradient descent?\n"
            "\n"
            "The chapter notes that the same basic update can use gradients computed from the whole "
            "dataset or from a randomly selected subset called a **minibatch**. The optimizer itself "
            "does not know which was used to compute the gradients.\n"
            "\n"
            "### Adam\n"
            "\n"
            "Changing optimization strategy can require only changing the optimizer object:\n"
            "\n"
            "```python\n"
            "optimizer = optim.Adam([params], lr=1e-1)\n"
            "```\n"
            "\n"
            "The source introduces Adam as a more sophisticated optimizer with adaptive behavior and "
            "shows that it can handle the original unnormalized thermometer input more robustly in this "
            "example. The point here is not to master Adam yet; it is to see that the training loop can "
            "stay almost unchanged while the optimization strategy changes.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Training and validation: fitting is not enough\n"
            "\n"
            "A flexible model can drive training loss downward by fitting the samples it sees. But low "
            "training loss alone does not prove that the learned function works on unseen data.\n"
            "\n"
            "This motivates a **validation set**.\n"
            "\n"
            "We fit the model using the training set while independently evaluating it on validation "
            "samples that are not used to compute parameter updates.\n"
            "\n"
            "[[IMAGE_NEEDED: Training and validation split | "
            "A dataset divided into a larger training subset and a held-out validation subset, with "
            "parameter updates driven only by training data and validation data flowing only to an "
            "evaluation loss | Learner should notice that validation observations are deliberately "
            "kept out of gradient-based fitting]]\n"
            "\n"
            "### Underfitting\n"
            "\n"
            "If training loss does not meaningfully decrease, two possibilities discussed in the source "
            "are:\n"
            "\n"
            "- the model does not have enough capacity for the relationship,\n"
            "- the available input does not contain the information needed to predict the target.\n"
            "\n"
            "A model that cannot fit the training data sufficiently is **underfitting**.\n"
            "\n"
            "### Overfitting\n"
            "\n"
            "If training loss continues improving while validation loss gets worse or fails to improve "
            "with it, the model is fitting the training examples without learning a relationship that "
            "generalizes well.\n"
            "\n"
            "That is **overfitting**.\n"
            "\n"
            "[[IMAGE_NEEDED: Training and validation loss scenarios | "
            "Four small plots showing: neither loss decreasing; training decreasing while validation "
            "worsens; both decreasing together; and both decreasing with a stable gap | Learner should "
            "identify no learning, overfitting, ideal generalization trend, and acceptable generalization "
            "with different absolute losses]]\n"
            "\n"
            "The chapter mentions several broad ways to fight overfitting:\n"
            "\n"
            "- collect enough representative data,\n"
            "- reduce unnecessary model complexity,\n"
            "- use regularization such as penalties on large parameter values,\n"
            "- use data augmentation/noise when appropriate.\n"
            "\n"
            "For now, the most important diagnostic habit is to monitor both training and validation "
            "loss rather than training loss alone.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Split a dataset correctly\n"
            "\n"
            "The chapter creates a random permutation of sample indices:\n"
            "\n"
            "```python\n"
            "n_samples = t_u.shape[0]\n"
            "n_val = int(0.2 * n_samples)\n"
            "\n"
            "shuffled_indices = torch.randperm(n_samples)\n"
            "\n"
            "train_indices = shuffled_indices[:-n_val]\n"
            "val_indices = shuffled_indices[-n_val:]\n"
            "```\n"
            "\n"
            "Then both inputs and corresponding targets are indexed using the same split:\n"
            "\n"
            "```python\n"
            "train_t_u = t_u[train_indices]\n"
            "train_t_c = t_c[train_indices]\n"
            "\n"
            "val_t_u = t_u[val_indices]\n"
            "val_t_c = t_c[val_indices]\n"
            "```\n"
            "\n"
            "This preserves each input/target pairing.\n"
            "\n"
            "### Only training loss drives gradients\n"
            "\n"
            "A training/validation loop evaluates both losses, but calls `.backward()` only on the "
            "training loss:\n"
            "\n"
            "```python\n"
            "train_t_p = model(train_t_u, *params)\n"
            "train_loss = loss_fn(train_t_p, train_t_c)\n"
            "\n"
            "val_t_p = model(val_t_u, *params)\n"
            "val_loss = loss_fn(val_t_p, val_t_c)\n"
            "\n"
            "optimizer.zero_grad()\n"
            "train_loss.backward()\n"
            "optimizer.step()\n"
            "```\n"
            "\n"
            "Calling backward on validation loss would contaminate the independence of validation by "
            "using validation examples to influence the learned parameters.\n"
            "\n"
            "{{exercise:M05.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Test set and data leakage\n"
            "\n"
            "The chapter goes one step beyond the training/validation split and introduces the "
            "**test set**.\n"
            "\n"
            "The roles are different:\n"
            "\n"
            "| Split | Primary role |\n"
            "|---|---|\n"
            "| Training set | Fit model parameters |\n"
            "| Validation set | Evaluate during development and guide model/hyperparameter choices |\n"
            "| Test set | Final independent evaluation after development decisions are complete |\n"
            "\n"
            "Repeatedly choosing models and hyperparameters based on validation performance means we can "
            "indirectly adapt to the validation set. The test set is therefore held aside to provide a "
            "more independent final estimate.\n"
            "\n"
            "### Data leakage\n"
            "\n"
            "**Data leakage** occurs when information that should not be available to the training "
            "process influences it anyway.\n"
            "\n"
            "Examples described in the chapter include:\n"
            "\n"
            "- overlap between training, validation, or test samples,\n"
            "- training with information from the future that would not be available when the model is "
            "used for real predictions.\n"
            "\n"
            "Leakage can make evaluation look much better than true real-world performance.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Turn autograd off when you do not need gradients\n"
            "\n"
            "Validation requires predictions and loss values, but it does not require parameter "
            "gradients because validation should not train the model.\n"
            "\n"
            "Building an autograd computation graph anyway consumes unnecessary resources, especially "
            "for large models.\n"
            "\n"
            "Use:\n"
            "\n"
            "```python\n"
            "with torch.no_grad():\n"
            "    val_t_p = model(val_t_u, *params)\n"
            "    val_loss = loss_fn(val_t_p, val_t_c)\n"
            "```\n"
            "\n"
            "A cleaner training loop is therefore:\n"
            "\n"
            "```python\n"
            "def training_loop(\n"
            "    n_epochs,\n"
            "    optimizer,\n"
            "    params,\n"
            "    train_t_u,\n"
            "    val_t_u,\n"
            "    train_t_c,\n"
            "    val_t_c,\n"
            "):\n"
            "    for epoch in range(1, n_epochs + 1):\n"
            "        train_t_p = model(train_t_u, *params)\n"
            "        train_loss = loss_fn(train_t_p, train_t_c)\n"
            "\n"
            "        with torch.no_grad():\n"
            "            val_t_p = model(val_t_u, *params)\n"
            "            val_loss = loss_fn(val_t_p, val_t_c)\n"
            "\n"
            "        optimizer.zero_grad()\n"
            "        train_loss.backward()\n"
            "        optimizer.step()\n"
            "\n"
            "    return params\n"
            "```\n"
            "\n"
            "The related context `torch.set_grad_enabled(is_train)` can enable or disable gradient "
            "tracking conditionally depending on whether code is running in a training context.\n"
            "\n"
            "### Important nuance\n"
            "\n"
            "The source notes that `torch.no_grad()` controls gradient tracking, while `detach()` is "
            "useful when you specifically need a tensor detached from its computation history.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. The complete learning recipe\n"
            "\n"
            "We can now compress the whole chapter into one reusable mental model.\n"
            "\n"
            "### Before training\n"
            "\n"
            "1. Collect input/target examples.\n"
            "2. Understand and visualize the data.\n"
            "3. Split data into training and validation sets; reserve a test set when appropriate.\n"
            "4. Normalize inputs when scale differences make optimization difficult.\n"
            "5. Define a model with learnable parameters.\n"
            "6. Define a loss function that represents the error you want to reduce.\n"
            "7. Choose an optimizer and learning rate.\n"
            "\n"
            "### During every training step\n"
            "\n"
            "```text\n"
            "forward pass\n"
            "    -> calculate training loss\n"
            "    -> clear old gradients\n"
            "    -> backward pass\n"
            "    -> optimizer step\n"
            "```\n"
            "\n"
            "### During evaluation\n"
            "\n"
            "```text\n"
            "forward pass on validation data\n"
            "    -> calculate validation loss\n"
            "    -> do NOT call backward\n"
            "    -> preferably disable gradient tracking\n"
            "```\n"
            "\n"
            "### What to watch\n"
            "\n"
            "- exploding/diverging loss -> update scale may be unstable,\n"
            "- very slow improvement -> update scale or representation may be poor,\n"
            "- training loss not improving -> possible underfitting or insufficient signal,\n"
            "- training improves while validation degrades -> overfitting,\n"
            "- suspiciously excellent evaluation -> check for leakage.\n"
            "\n"
            "This cycle is the foundation for the much larger neural networks that follow in the next "
            "chapter.\n"
            "\n"
            "{{exercise:M05.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Learning means the model discovers the correct formula automatically\n"
            "\n"
            "> If training succeeds, the model must have discovered the true underlying law.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Training finds parameters that reduce loss for the chosen model family and observed data. "
            "A model can fit observations without representing the true causal process.\n"
            "\n"
            "### Misconception 2: Lower training loss always means a better model\n"
            "\n"
            "> If training loss keeps decreasing, we should always keep training the same model.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A model can improve on training samples while getting worse on unseen validation data. "
            "That is the classic overfitting signal.\n"
            "\n"
            "### Misconception 3: `.backward()` replaces the previous gradients\n"
            "\n"
            "> Calling backward automatically clears earlier gradients.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Gradients accumulate on leaf tensors. Normal training loops clear them explicitly using "
            "`optimizer.zero_grad()` or an equivalent operation before the next backward pass.\n"
            "\n"
            "### Misconception 4: Validation loss should participate in backpropagation\n"
            "\n"
            "> Since validation loss measures model quality, we should call `val_loss.backward()` too.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "That would use validation samples to update parameters, destroying their role as held-out "
            "evaluation data.\n"
            "\n"
            "### Misconception 5: More model capacity always improves generalization\n"
            "\n"
            "> A larger model can fit more patterns, so it must perform better on unseen data.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Excess capacity can let a model fit details specific to the training set rather than a "
            "generalizable relationship.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Model | Parameterized function mapping inputs to predictions. |\n"
            "| Parameter | Value learned from data, such as a weight or bias. |\n"
            "| Weight | Parameter controlling how strongly an input contributes to an output. |\n"
            "| Bias | Additive model parameter. |\n"
            "| Regression | Prediction of continuous numerical values. |\n"
            "| Loss function | Scalar measure of model error to be minimized. |\n"
            "| Mean squared error | Average squared difference between prediction and target. |\n"
            "| Derivative | Local rate of change of one quantity with respect to another. |\n"
            "| Gradient | Collection of partial derivatives with respect to model parameters. |\n"
            "| Chain rule | Rule for combining derivatives through composed functions. |\n"
            "| Gradient descent | Parameter-update method that moves opposite the gradient. |\n"
            "| Learning rate | Hyperparameter scaling the size of each parameter update. |\n"
            "| Hyperparameter | Training/design setting not learned as a normal model parameter. |\n"
            "| Forward pass | Computation from inputs through the model to predictions/loss. |\n"
            "| Backward pass | Propagation of derivatives backward through the computation. |\n"
            "| Backpropagation | Efficient application of the chain rule through the computation graph. |\n"
            "| Epoch | One complete pass through the training dataset. |\n"
            "| Minibatch | Subset of training samples used for one or more parameter updates. |\n"
            "| Autograd | PyTorch system that automatically computes derivatives. |\n"
            "| `requires_grad` | Flag telling PyTorch to track operations needed for gradients. |\n"
            "| Computation graph | Recorded dependency structure linking tensor operations. |\n"
            "| Optimizer | Object that updates parameters using their gradients. |\n"
            "| SGD | Gradient-descent optimizer commonly applied using minibatch gradients. |\n"
            "| Adam | Adaptive optimizer introduced as an alternative to basic SGD. |\n"
            "| Training set | Data used to fit model parameters. |\n"
            "| Validation set | Held-out data used during model development to assess generalization. |\n"
            "| Test set | Independent data reserved for final evaluation. |\n"
            "| Underfitting | Model fails to fit important structure even in training data. |\n"
            "| Overfitting | Model fits training data but generalizes poorly to unseen data. |\n"
            "| Regularization | Techniques that discourage overly complex fitted behavior. |\n"
            "| Data leakage | Improper access to information that should be unavailable during training. |\n"
            "| `torch.no_grad()` | Context disabling normal autograd graph construction where gradients are unnecessary. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why can supervised learning be described as parameter estimation?\n"
            "2. What are `w` and `b` in the thermometer model?\n"
            "3. Why do we need a loss function instead of only looking at predictions?\n"
            "4. Why does squared error penalize large errors more strongly than absolute error?\n"
            "5. What information does the sign of a gradient provide?\n"
            "6. What role does the learning rate play in a parameter update?\n"
            "7. Why can an excessively large learning rate make loss explode?\n"
            "8. What is the difference between a derivative and a gradient?\n"
            "9. Why is the chain rule important for model training?\n"
            "10. What are the four fundamental stages of a training step?\n"
            "11. What is the difference between an epoch and a step when using minibatches?\n"
            "12. Why did rescaling `t_u` help the thermometer optimization?\n"
            "13. What does `requires_grad=True` tell PyTorch?\n"
            "14. What does `loss.backward()` produce for tracked leaf parameters?\n"
            "15. Why must gradients normally be cleared before the next step?\n"
            "16. What do `optimizer.zero_grad()` and `optimizer.step()` each do?\n"
            "17. What observation indicates underfitting?\n"
            "18. What relationship between training and validation losses suggests overfitting?\n"
            "19. Why should validation loss not call `.backward()`?\n"
            "20. What is the purpose of a separate test set?\n"
            "21. Give one example of data leakage from the lesson.\n"
            "22. Why use `torch.no_grad()` during validation?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Learning is an optimization loop: a model makes predictions, a loss measures their "
            "error, backpropagation computes how each parameter contributed to that error, and an "
            "optimizer updates the parameters in a direction that should reduce future loss. Training "
            "loss tells us how well we fit known examples; validation and test data tell us whether the "
            "learned relationship generalizes beyond them.**\n"
        ),

        "estimated_minutes": 180,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "learning-as-model-fitting", "title": "Learning is model fitting", "order": 1},
            {"id": "thermometer-regression", "title": "A simple regression problem", "order": 2},
            {"id": "linear-model", "title": "Choose the model and its parameters", "order": 3},
            {"id": "loss-function", "title": "Loss functions", "order": 4},
            {"id": "gradient-descent", "title": "Gradient descent", "order": 5},
            {"id": "derivatives-and-chain-rule", "title": "Derivatives, gradients, and the chain rule", "order": 6},
            {"id": "training-loop", "title": "Build the training loop", "order": 7},
            {"id": "learning-rate", "title": "Learning rate and convergence", "order": 8},
            {"id": "input-normalization", "title": "Input normalization", "order": 9},
            {"id": "autograd", "title": "PyTorch autograd", "order": 10},
            {"id": "manual-autograd-update", "title": "Updating parameters safely with autograd", "order": 11},
            {"id": "optimizers", "title": "PyTorch optimizers", "order": 12},
            {"id": "training-validation-overfitting", "title": "Training, validation, and overfitting", "order": 13},
            {"id": "split-data", "title": "Splitting data correctly", "order": 14},
            {"id": "test-set-and-data-leakage", "title": "Test set and data leakage", "order": 15},
            {"id": "disable-autograd-validation", "title": "Disabling autograd during validation", "order": 16},
            {"id": "complete-training-recipe", "title": "The complete learning recipe", "order": 17},
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M05.L01.EX01",
            "title": "Compute the Model and Loss by Hand",
            "lesson_code": "M05.L01",
            "section_id": "loss-function",
            "placement": "after_section",
            "description": (
                "Build intuition for a linear model and mean squared error before using gradients."
            ),
            "instructions": (
                "Use `t_u = torch.tensor([1.0, 2.0, 3.0])` and "
                "`t_c = torch.tensor([3.0, 5.0, 7.0])`.\n"
                "1. Define `model(t_u, w, b) = w * t_u + b`.\n"
                "2. Start with `w=1.0` and `b=0.0`.\n"
                "3. Compute all predictions.\n"
                "4. Compute each prediction error.\n"
                "5. Square each error and calculate the mean squared loss.\n"
                "6. Try `w=2.0` and `b=1.0` and compare the new loss.\n"
                "7. Explain what the lower loss tells you about the parameter values."
            ),
            "expected_output": (
                "PyTorch code, both prediction vectors, both MSE values, and a short explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "linear-model",
                "parameters",
                "mean-squared-error",
                "loss-interpretation",
            ],
        },
        {
            "id": "M05.L01.EX02",
            "title": "Verify Autograd Against an Analytical Gradient",
            "lesson_code": "M05.L01",
            "section_id": "autograd",
            "placement": "after_section",
            "description": (
                "Connect the hand-derived gradient idea with PyTorch's automatic differentiation."
            ),
            "instructions": (
                "Using a small linear-regression tensor:\n"
                "1. Create parameters with `requires_grad=True`.\n"
                "2. Compute predictions and mean squared loss.\n"
                "3. Call `loss.backward()` and record `params.grad`.\n"
                "4. Independently compute the gradient using the derivative formulas from the lesson.\n"
                "5. Compare the two gradient tensors.\n"
                "6. Call backward again without clearing gradients and observe what changes.\n"
                "7. Clear the gradients and explain why normal training loops do this every step."
            ),
            "expected_output": (
                "A short script showing autograd and manual gradient values, accumulation behavior, "
                "and an explanation of why gradients are cleared."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "autograd",
                "backward",
                "gradient",
                "gradient-accumulation",
            ],
        },
        {
            "id": "M05.L01.EX03",
            "title": "Diagnose Training and Validation Curves",
            "lesson_code": "M05.L01",
            "section_id": "split-data",
            "placement": "after_section",
            "description": (
                "Practice distinguishing healthy learning, underfitting, and overfitting from loss trends."
            ),
            "instructions": (
                "For each case, diagnose the most likely situation and explain why:\n"
                "1. Training loss stays high and validation loss stays high.\n"
                "2. Training loss falls steadily while validation loss rises after an initial improvement.\n"
                "3. Training and validation losses both fall and stay reasonably close.\n"
                "4. Training loss is slightly lower than validation loss, but both continue declining "
                "with similar trends.\n"
                "Then explain why calling `val_loss.backward()` would invalidate the purpose of the "
                "validation set."
            ),
            "expected_output": (
                "Four diagnoses with reasoning plus a short explanation of why validation does not "
                "participate in parameter updates."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "validation",
                "underfitting",
                "overfitting",
                "generalization",
            ],
        },
        {
            "id": "M05.L01.EX04",
            "title": "Replace the Linear Model with a Quadratic Model",
            "lesson_code": "M05.L01",
            "section_id": "complete-training-recipe",
            "placement": "after_section",
            "description": (
                "Identify which training components depend on the model formula and which remain reusable."
            ),
            "instructions": (
                "Redefine the model as:\n"
                "`t_p = w2 * t_u**2 + w1 * t_u + b`.\n"
                "1. Determine how many learnable parameters are now needed.\n"
                "2. Implement the model using PyTorch autograd.\n"
                "3. Reuse the same mean squared loss.\n"
                "4. Reuse an optimizer-based training loop.\n"
                "5. Train it on the thermometer data.\n"
                "6. Compare training and validation losses with the linear model.\n"
                "7. Explain which parts of the pipeline changed because the model changed and which "
                "parts stayed exactly the same.\n"
                "8. Explain why a lower training loss would not automatically prove the quadratic "
                "model is better."
            ),
            "expected_output": (
                "Working quadratic-model training code plus a comparison explaining model-specific "
                "versus model-agnostic parts of the training pipeline."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "model-design",
                "autograd",
                "optimizer",
                "generalization",
                "training-loop",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M05.L01.QZ01",
        "title": "The Mechanics of Learning — Knowledge Check",
        "lesson_code": "M05.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M05.L01.Q01",
                "section_id": "linear-model",
                "question": "In `t_p = w * t_u + b`, what are `w` and `b`?",
                "options": [
                    "Training examples",
                    "Learnable model parameters",
                    "Validation losses",
                    "Optimizers",
                ],
                "correct": 1,
                "explanation": (
                    "`w` and `b` are the values adjusted during fitting so that model predictions "
                    "better match the target data."
                ),
            },
            {
                "id": "M05.L01.Q02",
                "section_id": "loss-function",
                "question": "What is the purpose of a loss function?",
                "options": [
                    "Produce a scalar measure of prediction error for optimization.",
                    "Randomly initialize all model parameters after every epoch.",
                    "Split the dataset into training and validation sets.",
                    "Move data to the GPU.",
                ],
                "correct": 0,
                "explanation": (
                    "Loss gives optimization a numerical objective: parameter updates should make "
                    "that value smaller."
                ),
            },
            {
                "id": "M05.L01.Q03",
                "section_id": "gradient-descent",
                "question": "Why does gradient descent subtract the gradient multiplied by the learning rate?",
                "options": [
                    "The gradient points in the local direction of increasing loss, so subtraction moves toward decreasing loss.",
                    "Gradients contain target labels.",
                    "Subtraction automatically normalizes the input.",
                    "The learning rate is a model parameter.",
                ],
                "correct": 0,
                "explanation": (
                    "The gradient describes local loss increase. Moving in the negative-gradient "
                    "direction aims to reduce the loss."
                ),
            },
            {
                "id": "M05.L01.Q04",
                "section_id": "learning-rate",
                "question": "What can happen if the learning rate is much too large?",
                "options": [
                    "Updates can overshoot the minimum and optimization can diverge.",
                    "The loss is guaranteed to become exactly zero.",
                    "The model automatically switches to Adam.",
                    "Autograd stops creating gradients permanently.",
                ],
                "correct": 0,
                "explanation": (
                    "Oversized parameter steps can jump across the minimum repeatedly and grow rather "
                    "than shrink, causing exploding loss."
                ),
            },
            {
                "id": "M05.L01.Q05",
                "section_id": "input-normalization",
                "question": "Why did rescaling the thermometer input help the SGD example?",
                "options": [
                    "It made parameter-gradient scales more compatible for a shared learning rate.",
                    "It added more training samples.",
                    "It changed the regression task into classification.",
                    "It removed the need for a loss function.",
                ],
                "correct": 0,
                "explanation": (
                    "The original parameter gradients had very different magnitudes. Rescaling the "
                    "input made optimization better conditioned for one shared learning rate."
                ),
            },
            {
                "id": "M05.L01.Q06",
                "section_id": "autograd",
                "question": "What does `requires_grad=True` do for a parameter tensor?",
                "options": [
                    "Tells PyTorch to track relevant operations so gradients can be computed.",
                    "Automatically chooses a validation set.",
                    "Freezes the tensor so it cannot change.",
                    "Converts the tensor into a NumPy array.",
                ],
                "correct": 0,
                "explanation": (
                    "Gradient tracking records the computation dependencies needed for autograd to "
                    "calculate derivatives during backward."
                ),
            },
            {
                "id": "M05.L01.Q07",
                "section_id": "autograd",
                "question": "Why is `optimizer.zero_grad()` normally called during every training step?",
                "options": [
                    "Because PyTorch accumulates gradients across backward calls.",
                    "Because optimizer parameters become zero otherwise.",
                    "Because it sets training loss to zero.",
                    "Because it disables the computation graph.",
                ],
                "correct": 0,
                "explanation": (
                    "Without clearing, a new backward pass adds its gradient to gradients already "
                    "stored on the parameters."
                ),
            },
            {
                "id": "M05.L01.Q08",
                "section_id": "optimizers",
                "question": "What does `optimizer.step()` do?",
                "options": [
                    "Updates the optimizer's parameters using their computed gradients.",
                    "Computes the validation loss.",
                    "Clears the entire dataset.",
                    "Creates the computation graph.",
                ],
                "correct": 0,
                "explanation": (
                    "After gradients are populated, `step()` applies the optimizer's update strategy "
                    "to the parameter values."
                ),
            },
            {
                "id": "M05.L01.Q09",
                "section_id": "training-validation-overfitting",
                "question": "Which pattern most strongly suggests overfitting?",
                "options": [
                    "Training loss decreases while validation loss worsens.",
                    "Both losses decrease together.",
                    "Both losses remain high from the first epoch.",
                    "The optimizer has a `step` method.",
                ],
                "correct": 0,
                "explanation": (
                    "The model is improving on examples used for fitting but losing performance on "
                    "held-out examples, indicating poor generalization."
                ),
            },
            {
                "id": "M05.L01.Q10",
                "section_id": "test-set-and-data-leakage",
                "question": "What is the main purpose of the test set?",
                "options": [
                    "Provide a final independent evaluation after model-development decisions are complete.",
                    "Update model parameters every epoch.",
                    "Replace the loss function.",
                    "Tune the learning rate continuously.",
                ],
                "correct": 0,
                "explanation": (
                    "The test set is kept independent from training and routine validation-driven "
                    "development to provide a less biased final evaluation."
                ),
            },
            {
                "id": "M05.L01.Q11",
                "section_id": "disable-autograd-validation",
                "question": "Why use `torch.no_grad()` during validation?",
                "options": [
                    "Validation needs outputs and losses but not a gradient computation graph.",
                    "It forces validation loss to equal training loss.",
                    "It makes validation data participate in optimization.",
                    "It permanently removes `requires_grad` from all parameters.",
                ],
                "correct": 0,
                "explanation": (
                    "Validation is evaluation-only, so skipping normal gradient tracking avoids "
                    "unnecessary graph construction and resource use."
                ),
            },
            {
                "id": "M05.L01.Q12",
                "section_id": "complete-training-recipe",
                "type": "open",
                "question": (
                    "Describe one complete training step in the correct order and explain why validation "
                    "evaluation is kept separate from the parameter update."
                ),
            },
        ],
        "passing_score": 70,
    },
}
