"""M03.L01 — Introduction to TensorFlow, PyTorch, JAX, and Keras.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 3, pages not provided in the supplied extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"

MODULE_ORDER = 3

MODULE_TITLE = "Introduction to Deep Learning Frameworks"

MODULE_DESCRIPTION = (
    "Learn how TensorFlow, PyTorch, JAX, and Keras express the shared building "
    "blocks of practical deep learning: tensors, trainable state, gradients, "
    "compilation, model construction, training, validation, and inference."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Not provided in supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Introduction to TensorFlow, PyTorch, JAX, and Keras",

    "slug": "deep-learning-foundations-m03-l01",

    "description": (
        "A practical introduction to the major deep learning frameworks and the "
        "shared ideas behind tensors, automatic differentiation, training loops, "
        "Keras model building, validation, and inference."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.0,

    "skill_tags": [
        "deep-learning",
        "tensorflow",
        "pytorch",
        "jax",
        "keras",
        "automatic-differentiation",
        "training-loops",
        "module-03",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Introduction to TensorFlow, PyTorch, JAX, and Keras",

        "content": (
            '# Introduction to TensorFlow, PyTorch, JAX, and Keras\n'
            '\n'
            '> **Course:** Deep Learning Foundations  \n'
            '> **Lesson:** M03.L01  \n'
            '> **Module:** Introduction to Deep Learning Frameworks  \n'
            '> **Source alignment:** BOOK-002, Chapter 3. The supplied chapter extract does not include page numbers. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n'
            '\n'
            '---\n'
            '\n'
            '## Learning outcomes\n'
            '\n'
            'By the end of this lesson, you should be able to:\n'
            '\n'
            '- Explain the roles of TensorFlow, PyTorch, JAX, and Keras in modern deep learning.\n'
            '- Identify the three low-level capabilities shared by modern deep learning frameworks.\n'
            '- Create and manipulate tensors and trainable state in TensorFlow, PyTorch, and JAX.\n'
            '- Explain how automatic differentiation is exposed differently by the three low-level frameworks.\n'
            '- Compare eager execution, compilation, state handling, and gradient APIs across frameworks.\n'
            '- Explain how a linear classifier is trained with gradient descent in each framework.\n'
            '- Build the mental model behind Keras layers, models, `compile()`, `fit()`, validation, and inference.\n'
            '- Choose the right level of abstraction for a deep learning workflow.\n'
            '\n'
            '---\n'
            '\n'
            '## 1. The modern deep learning framework landscape\n'
            '\n'
            'In practice, deep learning engineers almost never implement every tensor operation, gradient rule, and device-management feature from scratch. They use frameworks.\n'
            '\n'
            'The chapter introduces four major tools:\n'
            '\n'
            '```text\n'
            'TensorFlow\n'
            'PyTorch\n'
            'JAX\n'
            'Keras\n'
            '```\n'
            '\n'
            'They are related, but they do not all serve the same role.\n'
            '\n'
            'A useful mental model is:\n'
            '\n'
            '```text\n'
            'High-level model-building API\n'
            '          Keras\n'
            '            │\n'
            '            ▼\n'
            'Low-level numerical / autodiff backends\n'
            ' ┌────────────┬────────────┬────────────┐\n'
            ' │ TensorFlow │  PyTorch   │    JAX     │\n'
            ' └────────────┴────────────┴────────────┘\n'
            '            │\n'
            '            ▼\n'
            '       CPU / GPU / TPU\n'
            '```\n'
            '\n'
            'TensorFlow, PyTorch, and JAX provide the lower-level numerical machinery needed for deep learning. Keras provides a higher-level interface for defining and training neural networks.\n'
            '\n'
            '### A short historical view\n'
            '\n'
            'The chapter presents modern frameworks as the result of several developments coming together:\n'
            '\n'
            '- scientific Python became widely used,\n'
            '- GPUs became accessible for general-purpose computation,\n'
            '- automatic differentiation became practical,\n'
            '- distributed training became important,\n'
            '- frameworks packaged these capabilities into reusable tools.\n'
            '\n'
            'Earlier systems such as Theano, Torch 7, and Caffe helped establish ideas that later appeared in modern frameworks.\n'
            '\n'
            "You do not need to memorize the full history. The important engineering lesson is that today's frameworks exist to solve recurring infrastructure problems that deep learning developers should not need to reimplement for every project.\n"
            '\n'
            '### Three capabilities that unlock modern deep learning\n'
            '\n'
            'The chapter highlights three capabilities shared by modern deep learning frameworks:\n'
            '\n'
            '1. **Automatic differentiation** — compute gradients of differentiable computations.\n'
            '2. **Accelerated tensor computation** — run numerical operations on CPUs, GPUs, and specialized hardware.\n'
            '3. **Distributed computation** — scale work across multiple devices or machines.\n'
            '\n'
            'These capabilities connect directly to the training loop you learned earlier:\n'
            '\n'
            '```text\n'
            'forward computation\n'
            '       ↓\n'
            'loss\n'
            '       ↓\n'
            'gradients\n'
            '       ↓\n'
            'parameter update\n'
            '```\n'
            '\n'
            'The frameworks differ mainly in **how they expose these ideas to the programmer**.\n'
            '\n'
            '---\n'
            '\n'
            '## 2. Shared core concepts across frameworks\n'
            '\n'
            'Although the APIs look different, the same concepts appear again and again.\n'
            '\n'
            '### Tensors\n'
            '\n'
            'A tensor is the central numerical data structure.\n'
            '\n'
            'You can think of tensors as generalized arrays:\n'
            '\n'
            '```text\n'
            'scalar       -> rank 0\n'
            'vector       -> rank 1\n'
            'matrix       -> rank 2\n'
            'image batch  -> often rank 4\n'
            '```\n'
            '\n'
            'Deep learning models transform tensors into other tensors.\n'
            '\n'
            '### Trainable state\n'
            '\n'
            'A model contains values that change during training, such as weights and biases.\n'
            '\n'
            'Each framework has its own way to represent this trainable state:\n'
            '\n'
            '| Framework | Typical trainable state |\n'
            '|---|---|\n'
            '| TensorFlow | `tf.Variable` |\n'
            '| PyTorch | `torch.nn.Parameter` or tensors with gradients enabled |\n'
            '| JAX | ordinary arrays passed explicitly as state |\n'
            '| Keras | weights owned by `Layer` objects |\n'
            '\n'
            "The difference is not merely naming. It reflects each framework's programming philosophy.\n"
            '\n'
            '### Tensor operations\n'
            '\n'
            'The same mathematical operations appear everywhere:\n'
            '\n'
            '```text\n'
            'addition\n'
            'multiplication\n'
            'matrix multiplication\n'
            'square / square root\n'
            'concatenation\n'
            'activation functions\n'
            'reductions such as mean\n'
            '```\n'
            '\n'
            'A dense transformation can be expressed conceptually as:\n'
            '\n'
            '```text\n'
            'output = activation(inputs @ W + b)\n'
            '```\n'
            '\n'
            'where:\n'
            '\n'
            '- `inputs` is the input tensor,\n'
            '- `W` is a weight matrix,\n'
            '- `b` is a bias vector,\n'
            '- `@` represents matrix multiplication.\n'
            '\n'
            '### Automatic differentiation\n'
            '\n'
            'Training requires gradients.\n'
            '\n'
            'The frameworks expose gradient computation differently:\n'
            '\n'
            '| Framework | Gradient style |\n'
            '|---|---|\n'
            '| TensorFlow | record operations with `GradientTape` |\n'
            '| PyTorch | build an implicit computation graph and call `.backward()` |\n'
            '| JAX | transform a function with `jax.grad()` or `jax.value_and_grad()` |\n'
            '\n'
            'The mathematical goal is the same:\n'
            '\n'
            '> compute how the loss changes with respect to the trainable parameters.\n'
            '\n'
            '### Compilation\n'
            '\n'
            'Python is convenient, but Python-level execution can become a performance bottleneck.\n'
            '\n'
            'Each framework has a way to move important computation into a compiled form:\n'
            '\n'
            '```text\n'
            'TensorFlow -> tf.function / XLA\n'
            'PyTorch    -> torch.compile()\n'
            'JAX        -> jax.jit\n'
            '```\n'
            '\n'
            'Compilation can improve performance, but it can also make debugging harder because the executed program is no longer a simple line-by-line Python interpretation.\n'
            '\n'
            '### High-level training concepts\n'
            '\n'
            'At a higher level, neural-network training still needs:\n'
            '\n'
            '```text\n'
            'model\n'
            'loss\n'
            'optimizer\n'
            'metrics\n'
            'training loop\n'
            'validation\n'
            'inference\n'
            '```\n'
            '\n'
            'Keras packages these concepts into a consistent API.\n'
            '\n'
            '{{exercise:M03.L01.EX01}}\n'
            '\n'
            '---\n'
            '\n'
            '## 3. TensorFlow: variables, GradientTape, and compiled functions\n'
            '\n'
            'TensorFlow is a Python-based machine-learning framework with a broad ecosystem for research and production.\n'
            '\n'
            'The chapter emphasizes that TensorFlow is more than tensor math. Its ecosystem includes tooling for production workflows, serving, optimization, and deployment.\n'
            '\n'
            '### Creating tensors\n'
            '\n'
            'Typical creation operations include:\n'
            '\n'
            '```python\n'
            'import tensorflow as tf\n'
            '\n'
            'a = tf.ones((2, 2))\n'
            'b = tf.zeros((2, 2))\n'
            'c = tf.constant([1, 2, 3], dtype=tf.float32)\n'
            '```\n'
            '\n'
            'These tensors behave similarly to NumPy arrays for many numerical operations.\n'
            '\n'
            '### Tensors versus variables\n'
            '\n'
            'A key distinction is that ordinary TensorFlow tensors are not intended to be changed in place.\n'
            '\n'
            'Trainable state is stored with `tf.Variable`:\n'
            '\n'
            '```python\n'
            'w = tf.Variable(tf.random.normal((3, 1)))\n'
            'w.assign(tf.ones((3, 1)))\n'
            '```\n'
            '\n'
            'You can also update variables incrementally:\n'
            '\n'
            '```python\n'
            'w.assign_add(tf.ones((3, 1)))\n'
            'w.assign_sub(tf.ones((3, 1)))\n'
            '```\n'
            '\n'
            'This distinction matters because model parameters must change during training.\n'
            '\n'
            '### Tensor operations\n'
            '\n'
            'TensorFlow provides mathematical operations such as:\n'
            '\n'
            '```python\n'
            'x = tf.ones((2, 2))\n'
            '\n'
            'squared = tf.square(x)\n'
            'root = tf.sqrt(x)\n'
            'product = tf.matmul(x, x)\n'
            'joined = tf.concat([x, x], axis=0)\n'
            '```\n'
            '\n'
            'A small dense transformation can be written as:\n'
            '\n'
            '```python\n'
            'def dense(inputs, W, b):\n'
            '    return tf.nn.relu(tf.matmul(inputs, W) + b)\n'
            '```\n'
            '\n'
            '### Computing gradients with GradientTape\n'
            '\n'
            'TensorFlow exposes automatic differentiation through `tf.GradientTape`.\n'
            '\n'
            'Example:\n'
            '\n'
            '```python\n'
            'x = tf.Variable(3.0)\n'
            '\n'
            'with tf.GradientTape() as tape:\n'
            '    y = x ** 2\n'
            '\n'
            'dy_dx = tape.gradient(y, x)\n'
            '```\n'
            '\n'
            'Since:\n'
            '\n'
            '```text\n'
            'y = x²\n'
            'dy/dx = 2x\n'
            '```\n'
            '\n'
            'at `x = 3`, the gradient is `6`.\n'
            '\n'
            'For model training, the common pattern is:\n'
            '\n'
            '```python\n'
            'with tf.GradientTape() as tape:\n'
            '    predictions = model(inputs)\n'
            '    loss = loss_function(targets, predictions)\n'
            '\n'
            'gradients = tape.gradient(loss, model_weights)\n'
            '```\n'
            '\n'
            'The tape tracks trainable variables automatically. If you want a gradient with respect to a constant tensor, it must be watched explicitly.\n'
            '\n'
            '### Higher-order gradients\n'
            '\n'
            'Gradient tapes can be nested.\n'
            '\n'
            'That makes it possible to compute a gradient of a gradient, such as:\n'
            '\n'
            '```text\n'
            'position -> velocity -> acceleration\n'
            '```\n'
            '\n'
            'You do not need to master higher-order differentiation yet, but it is useful to see that automatic differentiation is more general than only training neural networks.\n'
            '\n'
            '### Compilation in TensorFlow\n'
            '\n'
            'TensorFlow normally supports eager execution, which is convenient for debugging.\n'
            '\n'
            'A function can be compiled using:\n'
            '\n'
            '```python\n'
            '@tf.function\n'
            'def dense(inputs, W, b):\n'
            '    return tf.nn.relu(tf.matmul(inputs, W) + b)\n'
            '```\n'
            '\n'
            'For XLA compilation:\n'
            '\n'
            '```python\n'
            '@tf.function(jit_compile=True)\n'
            'def dense(inputs, W, b):\n'
            '    return tf.nn.relu(tf.matmul(inputs, W) + b)\n'
            '```\n'
            '\n'
            'A useful rule is:\n'
            '\n'
            '> Debug first, compile later.\n'
            '\n'
            'Compilation can make repeated computation faster, but the first call may take longer because the function has to be compiled.\n'
            '\n'
            '### Linear classifier: the TensorFlow training idea\n'
            '\n'
            'The chapter builds a classifier for two groups of 2D points.\n'
            '\n'
            'The model is:\n'
            '\n'
            '```text\n'
            'prediction = input @ W + b\n'
            '```\n'
            '\n'
            'For a point `[x, y]`, this is equivalent to:\n'
            '\n'
            '```text\n'
            'prediction = w1*x + w2*y + b\n'
            '```\n'
            '\n'
            'The model is trained by:\n'
            '\n'
            '1. producing predictions,\n'
            '2. computing mean squared error,\n'
            '3. using `GradientTape` to get gradients,\n'
            '4. subtracting a learning-rate-scaled gradient from `W` and `b`,\n'
            '5. repeating the process.\n'
            '\n'
            'A conceptual training step is:\n'
            '\n'
            '```python\n'
            'with tf.GradientTape() as tape:\n'
            '    predictions = model(inputs, W, b)\n'
            '    loss = mean_squared_error(targets, predictions)\n'
            '\n'
            'grad_W, grad_b = tape.gradient(loss, [W, b])\n'
            '\n'
            'W.assign_sub(learning_rate * grad_W)\n'
            'b.assign_sub(learning_rate * grad_b)\n'
            '```\n'
            '\n'
            'The classifier learns a linear decision boundary.\n'
            '\n'
            'In two dimensions, that boundary is a line. In higher-dimensional spaces, the same idea becomes a hyperplane.\n'
            '\n'
            "### TensorFlow's practical character\n"
            '\n'
            'The chapter presents TensorFlow as especially strong in:\n'
            '\n'
            '- a mature production ecosystem,\n'
            '- compilation support,\n'
            '- data-processing tooling,\n'
            '- deployment to multiple environments.\n'
            '\n'
            'It also notes that the API is broad and can feel more complex than smaller frameworks.\n'
            '\n'
            '---\n'
            '\n'
            '## 4. PyTorch: eager programming, backward(), Modules, and optimizers\n'
            '\n'
            'PyTorch is a Python-based machine-learning framework that is especially prominent in research and the pretrained-model ecosystem.\n'
            '\n'
            'The package is imported as:\n'
            '\n'
            '```python\n'
            'import torch\n'
            '```\n'
            '\n'
            'not as `pytorch`.\n'
            '\n'
            '### Creating tensors\n'
            '\n'
            'Examples:\n'
            '\n'
            '```python\n'
            'a = torch.ones((2, 2))\n'
            'b = torch.zeros((2, 2))\n'
            'c = torch.tensor([1, 2, 3], dtype=torch.float32)\n'
            '```\n'
            '\n'
            'Unlike ordinary TensorFlow tensors, PyTorch tensors can be modified in place.\n'
            '\n'
            '### Parameters\n'
            '\n'
            'Trainable state can be represented by a `Parameter`:\n'
            '\n'
            '```python\n'
            'p = torch.nn.Parameter(torch.zeros((2, 1)))\n'
            '```\n'
            '\n'
            'A `Parameter` is a tensor with a special role: it tells PyTorch that the value belongs to the trainable state of a model.\n'
            '\n'
            '### Tensor operations\n'
            '\n'
            'The mathematical operations remain familiar:\n'
            '\n'
            '```python\n'
            'a = torch.ones((2, 2))\n'
            '\n'
            'b = torch.square(a)\n'
            'c = torch.sqrt(a)\n'
            'd = torch.matmul(a, b)\n'
            'e = torch.cat((a, b), dim=0)\n'
            '```\n'
            '\n'
            'A dense transformation looks like:\n'
            '\n'
            '```python\n'
            'def dense(inputs, W, b):\n'
            '    return torch.nn.relu(torch.matmul(inputs, W) + b)\n'
            '```\n'
            '\n'
            '### Computing gradients with backward()\n'
            '\n'
            'PyTorch does not require the user to open an explicit gradient-tape context.\n'
            '\n'
            'Instead, operations create the information needed for backpropagation behind the scenes.\n'
            '\n'
            'Example:\n'
            '\n'
            '```python\n'
            'x = torch.tensor(3.0, requires_grad=True)\n'
            '\n'
            'y = x ** 2\n'
            'y.backward()\n'
            '\n'
            'print(x.grad)\n'
            '```\n'
            '\n'
            'The result is the gradient of `x²` at `x = 3`, which is `6`.\n'
            '\n'
            '### Gradient accumulation\n'
            '\n'
            'One very important PyTorch behavior is that gradients accumulate.\n'
            '\n'
            'If you call `.backward()` again without resetting the gradient, the new gradient is added to the old one.\n'
            '\n'
            'That means a training loop must clear gradients between updates.\n'
            '\n'
            'A common pattern is:\n'
            '\n'
            '```text\n'
            'loss.backward()\n'
            'optimizer.step()\n'
            'model.zero_grad()\n'
            '```\n'
            '\n'
            'or with optimizer-managed clearing:\n'
            '\n'
            '```text\n'
            'optimizer.zero_grad()\n'
            'loss.backward()\n'
            'optimizer.step()\n'
            '```\n'
            '\n'
            'The exact ordering depends on the code style, but the important rule is:\n'
            '\n'
            '> Do not accidentally reuse gradients from previous training steps.\n'
            '\n'
            '### Updating parameters manually\n'
            '\n'
            'A low-level training step might look conceptually like:\n'
            '\n'
            '```python\n'
            'loss.backward()\n'
            '\n'
            'with torch.no_grad():\n'
            '    W -= learning_rate * W.grad\n'
            '    b -= learning_rate * b.grad\n'
            '\n'
            'W.grad = None\n'
            'b.grad = None\n'
            '```\n'
            '\n'
            'The `torch.no_grad()` context prevents the parameter-update operations themselves from becoming part of the computation graph.\n'
            '\n'
            '### Packaging models with Module\n'
            '\n'
            "PyTorch's `torch.nn.Module` packages trainable parameters and the forward computation.\n"
            '\n'
            'Example:\n'
            '\n'
            '```python\n'
            'class LinearModel(torch.nn.Module):\n'
            '    def __init__(self):\n'
            '        super().__init__()\n'
            '        self.W = torch.nn.Parameter(torch.rand(2, 1))\n'
            '        self.b = torch.nn.Parameter(torch.zeros(1))\n'
            '\n'
            '    def forward(self, inputs):\n'
            '        return torch.matmul(inputs, self.W) + self.b\n'
            '```\n'
            '\n'
            'You usually call the model itself:\n'
            '\n'
            '```python\n'
            'outputs = model(inputs)\n'
            '```\n'
            '\n'
            'rather than directly calling `forward()`.\n'
            '\n'
            '### Optimizers\n'
            '\n'
            'Instead of writing parameter-update code manually, you can use an optimizer:\n'
            '\n'
            '```python\n'
            'optimizer = torch.optim.SGD(model.parameters(), lr=0.1)\n'
            '```\n'
            '\n'
            'Then the core training sequence becomes:\n'
            '\n'
            '```python\n'
            'predictions = model(inputs)\n'
            'loss = loss_function(targets, predictions)\n'
            '\n'
            'loss.backward()\n'
            'optimizer.step()\n'
            'model.zero_grad()\n'
            '```\n'
            '\n'
            'This is one of the most important PyTorch patterns to remember.\n'
            '\n'
            '### Compilation\n'
            '\n'
            'PyTorch also offers:\n'
            '\n'
            '```python\n'
            'compiled_model = torch.compile(model)\n'
            '```\n'
            '\n'
            "The goal is to speed up forward and backward computation while preserving the model's behavior.\n"
            '\n'
            "The chapter contrasts PyTorch's strong eager-execution culture with frameworks such as JAX, where compilation is more central to the typical workflow.\n"
            '\n'
            "### PyTorch's practical character\n"
            '\n'
            'The chapter emphasizes two major strengths:\n'
            '\n'
            '- an easy-to-debug eager programming style,\n'
            '- strong support in the pretrained-model ecosystem.\n'
            '\n'
            'A practical cost is that its API contains some naming inconsistencies, and performance optimization through compilation may require extra care.\n'
            '\n'
            '---\n'
            '\n'
            '## 5. JAX: NumPy-style code, stateless functions, grad(), and jit\n'
            '\n'
            'JAX takes a more functional and stateless approach.\n'
            '\n'
            'Its numerical API intentionally resembles NumPy:\n'
            '\n'
            '```python\n'
            'from jax import numpy as jnp\n'
            '\n'
            'a = jnp.ones((2, 2))\n'
            'b = jnp.zeros((2, 2))\n'
            'c = jnp.array([1, 2, 3], dtype="float32")\n'
            '```\n'
            '\n'
            "This familiarity is one of JAX's major attractions.\n"
            '\n'
            '### Stateless programming\n'
            '\n'
            'The central idea is:\n'
            '\n'
            '> a function should not secretly modify persistent state.\n'
            '\n'
            'Instead of hiding changing state inside objects or global variables, state is passed into functions and updated state is returned.\n'
            '\n'
            'This design makes computation easier to transform, compile, parallelize, and distribute.\n'
            '\n'
            '### Randomness is explicit\n'
            '\n'
            "Random-number generation reveals JAX's stateless philosophy clearly.\n"
            '\n'
            'In many libraries, random functions rely on hidden global state.\n'
            '\n'
            'JAX instead uses explicit random keys:\n'
            '\n'
            '```python\n'
            'import jax\n'
            '\n'
            'key = jax.random.key(123)\n'
            'values = jax.random.normal(key, shape=(3,))\n'
            '```\n'
            '\n'
            'If you reuse exactly the same key, you get the same random values.\n'
            '\n'
            'To obtain a new stream of randomness, you split the key:\n'
            '\n'
            '```python\n'
            'key, new_key = jax.random.split(key)\n'
            '```\n'
            '\n'
            'This is more explicit than global random state and supports deterministic, parallel computation.\n'
            '\n'
            '### Arrays are not modified in place\n'
            '\n'
            'JAX arrays follow a functional style.\n'
            '\n'
            'Instead of:\n'
            '\n'
            '```text\n'
            'change x directly\n'
            '```\n'
            '\n'
            'you create an updated array:\n'
            '\n'
            '```python\n'
            'x = jnp.array([1, 2, 3])\n'
            'new_x = x.at[0].set(10)\n'
            '```\n'
            '\n'
            '`x` remains conceptually unchanged; `new_x` represents the updated result.\n'
            '\n'
            '### Tensor operations\n'
            '\n'
            'Because JAX mirrors NumPy closely, common operations look familiar:\n'
            '\n'
            '```python\n'
            'a = jnp.ones((2, 2))\n'
            '\n'
            'b = jnp.square(a)\n'
            'c = jnp.sqrt(a)\n'
            'd = jnp.matmul(a, b)\n'
            '```\n'
            '\n'
            'A dense transformation is:\n'
            '\n'
            '```python\n'
            'def dense(inputs, W, b):\n'
            '    return jax.nn.relu(jnp.matmul(inputs, W) + b)\n'
            '```\n'
            '\n'
            '### Gradients with function transformations\n'
            '\n'
            'JAX exposes differentiation as a function transformation.\n'
            '\n'
            'Suppose:\n'
            '\n'
            '```python\n'
            'def compute_loss(x):\n'
            '    return x ** 2\n'
            '```\n'
            '\n'
            'You can create a new function that computes its gradient:\n'
            '\n'
            '```python\n'
            'grad_fn = jax.grad(compute_loss)\n'
            'gradient = grad_fn(3.0)\n'
            '```\n'
            '\n'
            'Instead of asking a tensor to backpropagate, you transform one function into another function.\n'
            '\n'
            '### value_and_grad()\n'
            '\n'
            'Training usually needs both:\n'
            '\n'
            '- the loss value,\n'
            '- the gradients.\n'
            '\n'
            'JAX provides:\n'
            '\n'
            '```python\n'
            'value_and_grad_fn = jax.value_and_grad(compute_loss)\n'
            'loss, gradients = value_and_grad_fn(state)\n'
            '```\n'
            '\n'
            'When model state contains many arrays, JAX can preserve the same nested structure in the gradient result.\n'
            '\n'
            '### JIT compilation\n'
            '\n'
            'JAX commonly uses:\n'
            '\n'
            '```python\n'
            '@jax.jit\n'
            'def training_step(...):\n'
            '    ...\n'
            '```\n'
            '\n'
            'This compiles the stateless function with XLA.\n'
            '\n'
            'The stateless restriction matters: updated values must be returned rather than silently changed inside the function.\n'
            '\n'
            '### Linear classifier: the JAX training idea\n'
            '\n'
            'The same classifier can be trained in JAX.\n'
            '\n'
            'The main difference is explicit state flow:\n'
            '\n'
            '```text\n'
            'old W, b\n'
            '   ↓\n'
            'training_step(...)\n'
            '   ↓\n'
            'loss, new W, new b\n'
            '```\n'
            '\n'
            'A conceptual update is:\n'
            '\n'
            '```python\n'
            'def compute_loss(state, inputs, targets):\n'
            '    W, b = state\n'
            '    predictions = inputs @ W + b\n'
            '    return jnp.mean((targets - predictions) ** 2)\n'
            '\n'
            'grad_fn = jax.value_and_grad(compute_loss)\n'
            '\n'
            '@jax.jit\n'
            'def training_step(state, inputs, targets):\n'
            '    loss, grads = grad_fn(state, inputs, targets)\n'
            '    W, b = state\n'
            '    grad_W, grad_b = grads\n'
            '\n'
            '    W = W - learning_rate * grad_W\n'
            '    b = b - learning_rate * grad_b\n'
            '\n'
            '    return loss, (W, b)\n'
            '```\n'
            '\n'
            'The mathematics is the same as TensorFlow and PyTorch. The programming style is different.\n'
            '\n'
            "### JAX's practical character\n"
            '\n'
            'The chapter presents JAX as especially attractive for:\n'
            '\n'
            '- high-performance compiled numerical work,\n'
            '- NumPy-like syntax,\n'
            '- TPU-oriented workloads,\n'
            '- large-scale parallel and distributed computation.\n'
            '\n'
            'The tradeoff is that functional programming, metaprogramming, and compiled execution may require a different mental model and can make debugging harder.\n'
            '\n'
            '---\n'
            '\n'
            '## 6. Keras: from layers to training and inference\n'
            '\n'
            'Keras sits at a higher level of abstraction.\n'
            '\n'
            'Instead of focusing first on low-level tensor mechanics, Keras focuses on the objects and workflows used to build neural networks.\n'
            '\n'
            '### Keras backends\n'
            '\n'
            'Keras can use:\n'
            '\n'
            '```text\n'
            'TensorFlow\n'
            'PyTorch\n'
            'JAX\n'
            '```\n'
            '\n'
            'as backend engines.\n'
            '\n'
            'This means Keras code can describe the model while the backend performs the low-level tensor operations, gradient computation, and hardware execution.\n'
            '\n'
            'A useful analogy is:\n'
            '\n'
            '```text\n'
            'Keras        -> building system / high-level interface\n'
            'Backend      -> numerical engine and low-level machinery\n'
            'Hardware     -> CPU / GPU / TPU\n'
            '```\n'
            '\n'
            'The backend must be configured before Keras is imported if you want to override the default environment configuration.\n'
            '\n'
            '### Layers are the main building blocks\n'
            '\n'
            'A Keras `Layer` combines:\n'
            '\n'
            '```text\n'
            'state + computation\n'
            '```\n'
            '\n'
            'The state usually means trainable weights.\n'
            '\n'
            'The computation is the forward pass.\n'
            '\n'
            'Different data types naturally use different layer families:\n'
            '\n'
            '```text\n'
            'vector/tabular data -> Dense\n'
            'sequence data       -> recurrent or 1D convolution layers\n'
            'image data          -> 2D convolution layers\n'
            '```\n'
            '\n'
            'A useful mental model is to treat layers like compatible building blocks that transform tensors.\n'
            '\n'
            '### build() and call()\n'
            '\n'
            'A custom layer typically separates:\n'
            '\n'
            '- `build()` — create state after the input shape is known,\n'
            '- `call()` — define the forward computation.\n'
            '\n'
            'Example:\n'
            '\n'
            '```python\n'
            'import keras\n'
            '\n'
            'class SimpleDense(keras.Layer):\n'
            '    def __init__(self, units, activation=None):\n'
            '        super().__init__()\n'
            '        self.units = units\n'
            '        self.activation = activation\n'
            '\n'
            '    def build(self, input_shape):\n'
            '        input_dim = input_shape[-1]\n'
            '        self.W = self.add_weight(\n'
            '            shape=(input_dim, self.units),\n'
            '            initializer="random_normal",\n'
            '        )\n'
            '        self.b = self.add_weight(\n'
            '            shape=(self.units,),\n'
            '            initializer="zeros",\n'
            '        )\n'
            '\n'
            '    def call(self, inputs):\n'
            '        outputs = keras.ops.matmul(inputs, self.W) + self.b\n'
            '        if self.activation is not None:\n'
            '            outputs = self.activation(outputs)\n'
            '        return outputs\n'
            '```\n'
            '\n'
            'The useful design idea is **lazy building**.\n'
            '\n'
            'The layer can wait until it sees its first input before creating weights with the correct input dimension.\n'
            '\n'
            'That means Keras often infers shapes automatically.\n'
            '\n'
            '### From layers to models\n'
            '\n'
            'A model is a graph of layers.\n'
            '\n'
            'The simplest form is a sequential stack:\n'
            '\n'
            '```python\n'
            'model = keras.Sequential(\n'
            '    [\n'
            '        keras.layers.Dense(32, activation="relu"),\n'
            '        keras.layers.Dense(32, activation="relu"),\n'
            '        keras.layers.Dense(1),\n'
            '    ]\n'
            ')\n'
            '```\n'
            '\n'
            'More advanced networks can branch, merge, create multiple outputs, or include residual connections.\n'
            '\n'
            'The model architecture defines the **hypothesis space**.\n'
            '\n'
            'Choosing an architecture therefore encodes assumptions about what kinds of relationships the model can learn.\n'
            '\n'
            '### compile(): configure learning\n'
            '\n'
            'After choosing the architecture, training still needs three major choices:\n'
            '\n'
            '```text\n'
            'loss\n'
            'optimizer\n'
            'metrics\n'
            '```\n'
            '\n'
            'Example:\n'
            '\n'
            '```python\n'
            'model.compile(\n'
            '    optimizer=keras.optimizers.RMSprop(learning_rate=1e-4),\n'
            '    loss=keras.losses.MeanSquaredError(),\n'
            '    metrics=[keras.metrics.BinaryAccuracy()],\n'
            ')\n'
            '```\n'
            '\n'
            '#### Loss\n'
            '\n'
            'The loss is the quantity training tries to minimize.\n'
            '\n'
            'The chapter stresses that choosing the right loss matters because the model will optimize the objective you define, not the intention you forgot to encode.\n'
            '\n'
            'Typical examples include:\n'
            '\n'
            '```text\n'
            'binary classification      -> BinaryCrossentropy\n'
            'multiclass classification  -> CategoricalCrossentropy\n'
            'regression                 -> MeanSquaredError\n'
            '```\n'
            '\n'
            'The exact correct choice depends on the task and target representation.\n'
            '\n'
            '#### Optimizer\n'
            '\n'
            'The optimizer controls how parameter updates are performed.\n'
            '\n'
            'Common examples include:\n'
            '\n'
            '```text\n'
            'SGD\n'
            'RMSprop\n'
            'Adam\n'
            '```\n'
            '\n'
            '#### Metrics\n'
            '\n'
            'Metrics are values you want to monitor, such as:\n'
            '\n'
            '```text\n'
            'accuracy\n'
            'precision\n'
            'recall\n'
            'AUC\n'
            '```\n'
            '\n'
            'The optimizer does not necessarily optimize metrics directly.\n'
            '\n'
            'This distinction is important:\n'
            '\n'
            '```text\n'
            'loss    -> drives parameter updates\n'
            'metrics -> help humans monitor performance\n'
            '```\n'
            '\n'
            '### fit(): run the training loop\n'
            '\n'
            'Keras provides `fit()` as a high-level training loop.\n'
            '\n'
            'Example:\n'
            '\n'
            '```python\n'
            'history = model.fit(\n'
            '    inputs,\n'
            '    targets,\n'
            '    epochs=5,\n'
            '    batch_size=128,\n'
            ')\n'
            '```\n'
            '\n'
            'Two core terms:\n'
            '\n'
            '**Epoch**  \n'
            'One full pass over the training data.\n'
            '\n'
            '**Batch size**  \n'
            'The number of training examples used to compute one parameter update.\n'
            '\n'
            'If there are 10,000 training samples and the batch size is 100, then roughly 100 batches are processed per epoch.\n'
            '\n'
            '`fit()` returns a history of loss and metric values, which lets you inspect how training changed over epochs.\n'
            '\n'
            '### Validation data\n'
            '\n'
            'Good performance on training examples is not enough.\n'
            '\n'
            'The goal is to perform well on new examples.\n'
            '\n'
            'That is why part of the available data is often reserved as **validation data**.\n'
            '\n'
            'Validation data:\n'
            '\n'
            '- is not used to update weights,\n'
            '- is used to monitor loss and metrics on unseen examples.\n'
            '\n'
            'Example:\n'
            '\n'
            '```python\n'
            'model.fit(\n'
            '    training_inputs,\n'
            '    training_targets,\n'
            '    epochs=5,\n'
            '    batch_size=32,\n'
            '    validation_data=(validation_inputs, validation_targets),\n'
            ')\n'
            '```\n'
            '\n'
            'A critical rule is:\n'
            '\n'
            '> training and validation data must remain separate.\n'
            '\n'
            'If validation examples leak into training, validation measurements become unreliable.\n'
            '\n'
            'After training, you can evaluate explicitly:\n'
            '\n'
            '```python\n'
            'results = model.evaluate(validation_inputs, validation_targets)\n'
            '```\n'
            '\n'
            '### Inference with predict()\n'
            '\n'
            "Training changes the model's weights.\n"
            '\n'
            'Inference uses the trained model to produce outputs for new data.\n'
            '\n'
            'Keras provides:\n'
            '\n'
            '```python\n'
            'predictions = model.predict(new_inputs, batch_size=128)\n'
            '```\n'
            '\n'
            'Using `predict()` is useful because large inputs can be processed in manageable batches instead of forcing all examples through the model at once.\n'
            '\n'
            '### The complete Keras workflow\n'
            '\n'
            'The entire workflow can be remembered as:\n'
            '\n'
            '```text\n'
            '1. Choose backend\n'
            '2. Build layers\n'
            '3. Assemble model\n'
            '4. Choose loss\n'
            '5. Choose optimizer\n'
            '6. Choose metrics\n'
            '7. compile()\n'
            '8. fit()\n'
            '9. validate / evaluate()\n'
            '10. predict()\n'
            '```\n'
            '\n'
            'This higher-level workflow is why Keras can be much more productive than writing every gradient update manually.\n'
            '\n'
            '{{exercise:M03.L01.EX02}}\n'
            '\n'
            '---\n'
            '\n'
            '## Important misconception\n'
            '\n'
            '### Misconception\n'
            '\n'
            '> "TensorFlow, PyTorch, JAX, and Keras are four interchangeable libraries that differ only in syntax."\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'They overlap, but their abstractions and programming philosophies differ.\n'
            '\n'
            '- TensorFlow emphasizes a broad ecosystem and compiled/production workflows.\n'
            '- PyTorch emphasizes an eager, object-oriented workflow with strong research and pretrained-model adoption.\n'
            '- JAX emphasizes functional, stateless transformations and compilation.\n'
            '- Keras is a higher-level neural-network API that can use TensorFlow, PyTorch, or JAX as a backend.\n'
            '\n'
            'The same mathematics appears in all of them, but the developer experience and abstraction level differ.\n'
            '\n'
            '---\n'
            '\n'
            '## Key terminology\n'
            '\n'
            '| Term | Meaning |\n'
            '|---|---|\n'
            '| Tensor | A multidimensional numerical array used as the basic data structure in deep learning |\n'
            '| Automatic differentiation | Automatic computation of gradients through differentiable operations |\n'
            '| Trainable state | Model values, such as weights, that change during training |\n'
            '| `tf.Variable` | TensorFlow object for modifiable model state |\n'
            '| `torch.nn.Parameter` | PyTorch tensor type used to mark trainable model state |\n'
            '| Stateless function | A function whose result depends only on explicit inputs and which does not hide mutable state |\n'
            '| `GradientTape` | TensorFlow mechanism for recording operations and computing gradients |\n'
            '| `.backward()` | PyTorch operation that runs backpropagation through the recorded computation |\n'
            '| `jax.grad()` | JAX transformation that creates a gradient-computing function |\n'
            '| JIT compilation | Compilation of a function just before execution to improve performance |\n'
            '| Layer | A reusable tensor transformation that may own trainable weights |\n'
            '| Model | A graph or composition of layers |\n'
            '| Loss | The training objective minimized by the optimizer |\n'
            '| Optimizer | The rule that updates parameters using gradients |\n'
            '| Metric | A monitored measurement of performance |\n'
            '| Epoch | One full pass over the training dataset |\n'
            '| Batch | A subset of examples used for one training update |\n'
            '| Validation data | Held-out data used to monitor performance without updating weights |\n'
            '| Inference | Using a trained model to generate predictions on new inputs |\n'
            '| Backend | The low-level framework Keras uses for numerical computation and differentiation |\n'
            '\n'
            '---\n'
            '\n'
            '## Framework comparison\n'
            '\n'
            '| Concept | TensorFlow | PyTorch | JAX | Keras |\n'
            '|---|---|---|---|---|\n'
            '| Main role | Low-level ML framework/platform | Low-level + some high-level ML framework | Differentiable numerical-computing library | High-level deep-learning API |\n'
            '| Core array | `tf.Tensor` | `torch.Tensor` | JAX array | Backend tensor through `keras.ops` |\n'
            '| Trainable state | `tf.Variable` | `Parameter` / grad-enabled tensor | Explicit arrays in state | Layer weights |\n'
            '| Gradients | `GradientTape` | `.backward()` | `grad()` / `value_and_grad()` | Usually handled by `fit()` |\n'
            '| Typical state style | Mutable variables | Mutable module parameters | Explicit, functional state | Encapsulated in layers/models |\n'
            '| Compilation | `tf.function`, XLA | `torch.compile()` | `jax.jit` | Depends on backend |\n'
            '| High-level model API | Available | Available | Usually external libraries | Central purpose |\n'
            '| Common strength | Production ecosystem | Eager workflow and model ecosystem | Speed, NumPy style, scaling | Productivity and backend portability |\n'
            '\n'
            '---\n'
            '\n'
            '## Self-check\n'
            '\n'
            'Before continuing, make sure you can answer:\n'
            '\n'
            '1. What three low-level capabilities do modern deep learning frameworks need?\n'
            '2. How does trainable state differ between TensorFlow, PyTorch, and JAX?\n'
            '3. What is the conceptual difference among `GradientTape`, `.backward()`, and `jax.grad()`?\n'
            '4. Why must PyTorch gradients usually be cleared between training steps?\n'
            '5. Why does JAX make randomness explicit?\n'
            '6. What does `jax.jit` do?\n'
            '7. What do `build()` and `call()` mean in a Keras layer?\n'
            '8. What is the difference between loss and metrics?\n'
            '9. What do epochs and batch size control?\n'
            '10. Why must validation data remain separate from training data?\n'
            '11. What is the difference between training and inference?\n'
            '12. Why can Keras be used without committing permanently to one backend?\n'
            '\n'
            '---\n'
            '\n'
            '## Retain this idea\n'
            '\n'
            '**TensorFlow, PyTorch, and JAX provide different low-level ways to express tensors, state, gradients, and compilation; Keras sits above them to provide a productive model-building, training, validation, and inference workflow.**\n'
        ),

        "estimated_minutes": 120,

        "has_code_examples": True,

        "sections": [
            {
                "id": 'framework-landscape',
                "title": 'The modern deep learning framework landscape',
                "order": 1,
            },
            {
                "id": 'shared-core-concepts',
                "title": 'Shared core concepts across frameworks',
                "order": 2,
            },
            {
                "id": 'tensorflow-basics',
                "title": 'TensorFlow: variables, GradientTape, and compiled functions',
                "order": 3,
            },
            {
                "id": 'pytorch-basics',
                "title": 'PyTorch: eager programming, backward(), Modules, and optimizers',
                "order": 4,
            },
            {
                "id": 'jax-basics',
                "title": 'JAX: NumPy-style code, stateless functions, grad(), and jit',
                "order": 5,
            },
            {
                "id": 'keras-workflow',
                "title": 'Keras: from layers to training and inference',
                "order": 6,
            }
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": 'M03.L01.EX01',
            "title": 'Map the Same Training Step Across Frameworks',
            "lesson_code": 'M03.L01',
            "section_id": 'shared-core-concepts',
            "placement": 'after_section',
            "description": 'Connect the same mathematical training process to the different APIs used by TensorFlow, PyTorch, and JAX.',
            "instructions": '1. Start with the common sequence: forward pass -> loss -> gradients -> parameter update.\n2. For TensorFlow, name the API used to record and compute gradients.\n3. For PyTorch, name the method used to start backpropagation and explain where gradients are stored.\n4. For JAX, name the function transformation used to compute gradients.\n5. Explain in two or three sentences why the mathematics is the same even though the APIs look different.',
            "expected_output": 'A three-row comparison table for TensorFlow, PyTorch, and JAX plus a short explanation of the shared training logic.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'framework-comparison',
                'automatic-differentiation',
                'training-loop',
            ],
        },

        {
            "id": 'M03.L01.EX02',
            "title": 'Design a Keras Training Workflow',
            "lesson_code": 'M03.L01',
            "section_id": 'keras-workflow',
            "placement": 'after_section',
            "description": 'Apply the Keras workflow to a simple binary classification task.',
            "instructions": '1. Assume you have numeric training inputs and binary targets 0/1.\n2. Sketch a small Sequential model with at least one hidden Dense layer and one output layer.\n3. Choose a reasonable loss, optimizer, and metric based on the lesson.\n4. Write a model.compile(...) call and a model.fit(...) call with epochs, batch_size, and validation_data.\n5. Show how you would generate predictions for new inputs.\n6. Explain why the validation set must not be used for parameter updates.',
            "expected_output": 'A short Keras code sketch containing model construction, compile, fit, validation, and predict, followed by a brief explanation.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'keras',
                'model-training',
                'validation',
                'inference',
            ],
        }
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M03.L01.QZ01",

        "title": "Introduction to TensorFlow, PyTorch, JAX, and Keras — Knowledge Check",

        "lesson_code": "M03.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": 'M03.L01.Q01',
                "section_id": 'framework-landscape',
                "question": 'Which three capabilities does the chapter identify as central to modern low-level deep learning frameworks?',
                "options": [
                    'Automatic differentiation, accelerated tensor computation, and distributed computation',
                    'Only data visualization, SQL, and web serving',
                    'Only image augmentation, tokenization, and plotting',
                    'Manual gradients, CPU-only execution, and single-device training',
                ],
                "correct": 0,
                "explanation": 'The chapter emphasizes automatic differentiation, hardware-accelerated tensor computation, and distribution across devices or machines.',
            },

            {
                "id": 'M03.L01.Q02',
                "section_id": 'shared-core-concepts',
                "question": 'Which mapping of framework to gradient API is correct?',
                "options": [
                    'TensorFlow -> backward(), PyTorch -> GradientTape, JAX -> fit()',
                    'TensorFlow -> GradientTape, PyTorch -> backward(), JAX -> grad()/value_and_grad()',
                    'TensorFlow -> predict(), PyTorch -> compile(), JAX -> Module',
                    'All three use exactly the same gradient API',
                ],
                "correct": 1,
                "explanation": 'All three compute gradients automatically, but TensorFlow uses GradientTape, PyTorch commonly uses backward(), and JAX transforms functions with grad or value_and_grad.',
            },

            {
                "id": 'M03.L01.Q03',
                "section_id": 'tensorflow-basics',
                "question": 'Why is tf.Variable important in TensorFlow training?',
                "options": [
                    'It stores modifiable state such as model parameters',
                    'It prevents all gradient computation',
                    'It is only used for strings',
                    'It permanently compiles Python code',
                ],
                "correct": 0,
                "explanation": 'Ordinary TensorFlow tensors are not used as mutable parameter state; tf.Variable is designed for values such as weights that must be updated.',
            },

            {
                "id": 'M03.L01.Q04',
                "section_id": 'pytorch-basics',
                "question": 'What common bug can occur if PyTorch gradients are not reset between training steps?',
                "options": [
                    'The dataset is automatically deleted',
                    'Gradients accumulate across backward passes',
                    'The model changes to TensorFlow',
                    'All tensors become immutable',
                ],
                "correct": 1,
                "explanation": 'PyTorch accumulates gradients in .grad by default, so training code must clear them between updates unless accumulation is intentional.',
            },

            {
                "id": 'M03.L01.Q05',
                "section_id": 'jax-basics',
                "question": 'Why does JAX use explicit random keys?',
                "options": [
                    'Because JAX cannot generate random numbers',
                    'To support its stateless and deterministic functional design',
                    'Only to make code longer',
                    'Because NumPy has no random-number API',
                ],
                "correct": 1,
                "explanation": 'JAX avoids hidden global random state. Explicit keys make randomness reproducible and compatible with functional transformation and parallelization.',
            },

            {
                "id": 'M03.L01.Q06',
                "section_id": 'keras-workflow',
                "question": 'What is the main difference between a training loss and a metric in Keras?',
                "options": [
                    'Metrics update weights, while loss is ignored',
                    'The loss drives optimization; metrics are primarily monitored',
                    'They are always mathematically identical',
                    'Metrics can only be used during inference',
                ],
                "correct": 1,
                "explanation": 'The optimizer updates parameters to minimize the loss. Metrics are useful measurements to monitor but are not necessarily the direct optimization objective.',
            },

            {
                "id": 'M03.L01.Q07',
                "section_id": 'keras-workflow',
                "question": 'Why should validation data remain separate from training data?',
                "options": [
                    'So it can provide a more honest measurement on examples not used for weight updates',
                    'Because validation examples cannot be represented as tensors',
                    'Because validation data is always unlabeled',
                    'So the optimizer can update validation targets',
                ],
                "correct": 0,
                "explanation": 'Validation is intended to estimate how learning transfers beyond the training examples. Leakage from training makes that estimate unreliable.',
            },

            {
                "id": 'M03.L01.Q08',
                "section_id": 'keras-workflow',
                "type": "open",
                "question": 'You must train the same conceptual linear classifier in TensorFlow, PyTorch, and JAX. Explain what stays mathematically the same and what changes in the programming style, then explain how Keras could hide most of these low-level differences.',
            }
        ],

        "passing_score": 70,
    },
}
