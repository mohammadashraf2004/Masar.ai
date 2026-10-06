"""M02.L01 — Mathematical Building Blocks of Neural Networks.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 2, page range not provided in supplied source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"

MODULE_ORDER = 2

MODULE_TITLE = "Mathematical Building Blocks of Neural Networks"

MODULE_DESCRIPTION = (
    "Build an intuitive understanding of how neural networks represent data "
    "with tensors, transform that data through layers, measure errors with "
    "loss functions, and learn by updating trainable parameters using "
    "gradient descent and backpropagation."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Chapter 2 — page range not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "How Neural Networks Represent Data and Learn",

    "slug": "deep-learning-foundations-m02-l01",

    "description": (
        "Understand the fundamental mechanics behind neural-network training: "
        "tensors, tensor shapes, Dense layers, activation functions, loss, "
        "gradients, gradient descent, and backpropagation."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 1.5,

    "skill_tags": [
        "deep-learning",
        "neural-networks",
        "tensors",
        "tensor-operations",
        "gradient-descent",
        "backpropagation",
        "optimization",
        "module-02",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "How Neural Networks Represent Data and Learn",

        "content": (
            "# How Neural Networks Represent Data and Learn\n"
            "\n"
            "> **Course:** Deep Learning Foundations  \n"
            "> **Lesson:** M02.L01  \n"
            "> **Module:** Mathematical Building Blocks of Neural Networks  \n"
            "> **Source alignment:** BOOK-002, Chapter 2. "
            "The supplied source did not specify a page range. "
            "This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
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
            "- Explain the basic workflow used to train a neural network.\n"
            "- Distinguish training data from test data.\n"
            "- Explain tensors, rank, shape and data type.\n"
            "- Recognize common tensor shapes used for tables, sequences, "
            "images and videos.\n"
            "- Explain what a Dense layer does at a conceptual level.\n"
            "- Interpret matrix multiplication, broadcasting and reshaping.\n"
            "- Explain why activation functions such as ReLU are necessary.\n"
            "- Distinguish loss, gradients and optimizers.\n"
            "- Explain gradient descent using an intuitive mental model.\n"
            "- Distinguish the forward pass from the backward pass.\n"
            "- Explain the purpose of backpropagation.\n"
            "- Describe the complete neural-network training loop.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Your First Mental Model of a Neural Network\n"
            "\n"
            "Before studying tensors or gradients, start with the overall "
            "idea.\n"
            "\n"
            "A neural network receives numbers, transforms those numbers, "
            "produces a prediction, measures how wrong that prediction is, "
            "and then changes itself slightly so that future predictions can "
            "be better.\n"
            "\n"
            "The whole process can be pictured as:\n"
            "\n"
            "```text\n"
            "Input data\n"
            "    ↓\n"
            "Neural network\n"
            "    ↓\n"
            "Prediction\n"
            "    ↓\n"
            "Compare prediction with correct answer\n"
            "    ↓\n"
            "Loss\n"
            "    ↓\n"
            "Calculate how parameters affected the loss\n"
            "    ↓\n"
            "Update parameters\n"
            "    ↓\n"
            "Repeat\n"
            "```\n"
            "\n"
            "Everything in this lesson helps explain one part of this loop.\n"
            "\n"
            "### A concrete problem: handwritten digit recognition\n"
            "\n"
            "Suppose we want a neural network to look at a small grayscale "
            "image containing a handwritten digit and decide whether the "
            "image represents 0, 1, 2, and so on up to 9.\n"
            "\n"
            "The MNIST dataset is a classic dataset for this task. Each image "
            "has a size of 28 × 28 pixels, and there are ten possible output "
            "classes.\n"
            "\n"
            "Three terms are important here:\n"
            "\n"
            "- A **sample** is one example, such as one digit image.\n"
            "- A **class** is one possible category, such as digit 7.\n"
            "- A **label** is the correct class attached to one sample.\n"
            "\n"
            "If an image contains a handwritten 7:\n"
            "\n"
            "```text\n"
            "sample = the image\n"
            "class  = digit 7\n"
            "label  = 7\n"
            "```\n"
            "\n"
            "### Training data and test data\n"
            "\n"
            "Machine-learning datasets are normally separated so that the "
            "model is evaluated on examples it did not use to learn.\n"
            "\n"
            "The MNIST example contains:\n"
            "\n"
            "```text\n"
            "60,000 training images\n"
            "10,000 test images\n"
            "```\n"
            "\n"
            "The **training set** is used to learn the model's parameters.\n"
            "\n"
            "The **test set** is used later to check whether the trained "
            "model can perform well on unseen examples.\n"
            "\n"
            "This distinction matters because simply memorizing training "
            "examples is not enough. We want the model to generalize to new "
            "examples.\n"
            "\n"
            "### Building the network\n"
            "\n"
            "A simple digit classifier can be represented conceptually as:\n"
            "\n"
            "```text\n"
            "784 pixel values\n"
            "      ↓\n"
            "Dense layer\n"
            "512 units\n"
            "      ↓\n"
            "ReLU\n"
            "      ↓\n"
            "Dense layer\n"
            "10 units\n"
            "      ↓\n"
            "Softmax\n"
            "      ↓\n"
            "10 class probabilities\n"
            "```\n"
            "\n"
            "The 784 values come from flattening a 28 × 28 image:\n"
            "\n"
            "```text\n"
            "28 × 28 = 784\n"
            "```\n"
            "\n"
            "The final layer has ten outputs because there are ten possible "
            "digit classes.\n"
            "\n"
            "### What softmax gives us\n"
            "\n"
            "The final classification layer can produce scores such as:\n"
            "\n"
            "```text\n"
            "Digit 0 → 0.001\n"
            "Digit 1 → 0.002\n"
            "Digit 2 → 0.001\n"
            "Digit 3 → 0.010\n"
            "Digit 4 → 0.001\n"
            "Digit 5 → 0.002\n"
            "Digit 6 → 0.001\n"
            "Digit 7 → 0.978\n"
            "Digit 8 → 0.003\n"
            "Digit 9 → 0.001\n"
            "```\n"
            "\n"
            "The values can be interpreted as class probabilities and sum "
            "to approximately 1. The largest probability belongs to digit 7, "
            "so the model predicts 7.\n"
            "\n"
            "### Loss, optimizer and accuracy\n"
            "\n"
            "Before training, three ideas need to be separated clearly.\n"
            "\n"
            "**Loss** answers:\n"
            "\n"
            "> How wrong is the model?\n"
            "\n"
            "A smaller loss generally means that the model's predictions are "
            "closer to the expected targets.\n"
            "\n"
            "**The optimizer** answers:\n"
            "\n"
            "> How should the trainable parameters be changed to reduce the "
            "loss?\n"
            "\n"
            "**Accuracy** answers:\n"
            "\n"
            "> What fraction of predictions were classified correctly?\n"
            "\n"
            "For example, 980 correct predictions out of 1,000 examples "
            "corresponds to 98% accuracy.\n"
            "\n"
            "Loss and accuracy are related to performance, but they are not "
            "the same thing. Loss is the quantity used to guide learning, "
            "whereas accuracy is a human-readable performance metric for this "
            "classification problem.\n"
            "\n"
            "### Preparing image values\n"
            "\n"
            "A 28 × 28 image can be reshaped into one vector containing 784 "
            "values.\n"
            "\n"
            "Pixel values may originally be integers between 0 and 255. They "
            "can be converted to floating-point values between 0 and 1 by "
            "dividing by 255.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "image_vector = image.reshape(28 * 28)\n"
            "image_vector = image_vector.astype('float32') / 255\n"
            "```\n"
            "\n"
            "The goal is not to change what the image means. We are simply "
            "putting the data into a numerical form and scale that works "
            "conveniently with the model.\n"
            "\n"
            "### Epochs and batches\n"
            "\n"
            "An **epoch** means one complete pass through the training "
            "dataset.\n"
            "\n"
            "If training uses five epochs, the model goes through the entire "
            "training set five times.\n"
            "\n"
            "Models normally do not process the entire dataset in a single "
            "operation. They use smaller groups called **batches**.\n"
            "\n"
            "For a batch size of 128:\n"
            "\n"
            "```text\n"
            "128 samples → model update\n"
            "next 128     → model update\n"
            "next 128     → model update\n"
            "...\n"
            "```\n"
            "\n"
            "### Training accuracy versus test accuracy\n"
            "\n"
            "A model may perform better on its training data than on unseen "
            "test data.\n"
            "\n"
            "This introduces the idea of **overfitting**.\n"
            "\n"
            "Overfitting happens when a model adapts too specifically to the "
            "training data and therefore performs worse on new examples.\n"
            "\n"
            "A useful analogy is memorizing practice-exam answers instead of "
            "learning the underlying concepts. You might score extremely "
            "well on familiar questions but struggle when the real exam "
            "contains new ones.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Tensors: How Neural Networks Store Data\n"
            "\n"
            "Neural networks work with numerical data stored in **tensors**.\n"
            "\n"
            "The simplest useful definition is:\n"
            "\n"
            "> A tensor is a container for numbers.\n"
            "\n"
            "A single number can be a tensor. A vector can be a tensor. A "
            "matrix can be a tensor. Collections of images and videos can "
            "also be represented as tensors.\n"
            "\n"
            "### Scalar: rank 0\n"
            "\n"
            "A scalar contains one value:\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "\n"
            "x = np.array(12)\n"
            "print(x.ndim)\n"
            "# 0\n"
            "```\n"
            "\n"
            "It has no axes, so it is called a **rank-0 tensor**.\n"
            "\n"
            "### Vector: rank 1\n"
            "\n"
            "A vector is an ordered sequence of values:\n"
            "\n"
            "```python\n"
            "x = np.array([12, 3, 6, 14, 7])\n"
            "print(x.ndim)\n"
            "# 1\n"
            "```\n"
            "\n"
            "It has one axis, so it is a **rank-1 tensor**.\n"
            "\n"
            "Be careful with the word *dimension*.\n"
            "\n"
            "A vector containing five values may be called a five-dimensional "
            "vector, but it still has only one tensor axis.\n"
            "\n"
            "```text\n"
            "5-dimensional vector:\n"
            "shape = (5,)\n"
            "rank  = 1\n"
            "```\n"
            "\n"
            "That is different from a rank-5 tensor, which has five axes.\n"
            "\n"
            "### Matrix: rank 2\n"
            "\n"
            "A matrix has rows and columns:\n"
            "\n"
            "```python\n"
            "x = np.array([\n"
            "    [5, 78, 2],\n"
            "    [6, 79, 3],\n"
            "    [7, 80, 4],\n"
            "])\n"
            "\n"
            "print(x.ndim)\n"
            "# 2\n"
            "```\n"
            "\n"
            "Because the matrix has two axes, it is a **rank-2 tensor**.\n"
            "\n"
            "### Rank-3 tensors\n"
            "\n"
            "If you stack several matrices together, you obtain another "
            "axis and therefore a rank-3 tensor.\n"
            "\n"
            "The MNIST training images can be represented with shape:\n"
            "\n"
            "```text\n"
            "(60000, 28, 28)\n"
            "```\n"
            "\n"
            "Interpret each axis separately:\n"
            "\n"
            "```text\n"
            "axis 0 → which image\n"
            "axis 1 → row within the image\n"
            "axis 2 → column within the image\n"
            "```\n"
            "\n"
            "### Three tensor properties you should always inspect\n"
            "\n"
            "When working with a tensor, ask three questions.\n"
            "\n"
            "#### 1. What is its rank?\n"
            "\n"
            "Rank tells you the number of axes.\n"
            "\n"
            "In NumPy this is available through:\n"
            "\n"
            "```python\n"
            "x.ndim\n"
            "```\n"
            "\n"
            "#### 2. What is its shape?\n"
            "\n"
            "Shape tells you how many values exist along each axis.\n"
            "\n"
            "```python\n"
            "x.shape\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "(60000, 28, 28)\n"
            "```\n"
            "\n"
            "means there are 60,000 items along the first axis, 28 along the "
            "second and 28 along the third.\n"
            "\n"
            "#### 3. What is its data type?\n"
            "\n"
            "The data type tells you what kind of values are stored.\n"
            "\n"
            "```python\n"
            "x.dtype\n"
            "```\n"
            "\n"
            "Common examples include:\n"
            "\n"
            "```text\n"
            "uint8\n"
            "float16\n"
            "float32\n"
            "float64\n"
            "bool\n"
            "```\n"
            "\n"
            "### Common machine-learning tensor shapes\n"
            "\n"
            "Understanding shapes becomes much easier when you connect each "
            "axis to something meaningful in the real world.\n"
            "\n"
            "#### Tabular or vector data\n"
            "\n"
            "A typical shape is:\n"
            "\n"
            "```text\n"
            "(samples, features)\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "(100000, 3)\n"
            "```\n"
            "\n"
            "could represent 100,000 people, each described by three numerical "
            "features.\n"
            "\n"
            "#### Sequence or time-series data\n"
            "\n"
            "A common shape is:\n"
            "\n"
            "```text\n"
            "(samples, timesteps, features)\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "(250, 390, 3)\n"
            "```\n"
            "\n"
            "could represent 250 trading days, 390 time steps per day and "
            "three measurements at each time step.\n"
            "\n"
            "#### Image data\n"
            "\n"
            "Using a channels-last convention, a batch of images can have "
            "shape:\n"
            "\n"
            "```text\n"
            "(samples, height, width, channels)\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "(128, 256, 256, 3)\n"
            "```\n"
            "\n"
            "means:\n"
            "\n"
            "```text\n"
            "128 images\n"
            "256 pixels high\n"
            "256 pixels wide\n"
            "3 color channels\n"
            "```\n"
            "\n"
            "Some frameworks may use channels first instead:\n"
            "\n"
            "```text\n"
            "(samples, channels, height, width)\n"
            "```\n"
            "\n"
            "The important skill is not memorizing one library's convention. "
            "It is learning to inspect and interpret the shape.\n"
            "\n"
            "#### Video data\n"
            "\n"
            "A video is a sequence of images, so another axis is needed:\n"
            "\n"
            "```text\n"
            "(samples, frames, height, width, channels)\n"
            "```\n"
            "\n"
            "This usually produces a rank-5 tensor.\n"
            "\n"
            "### Tensor slicing\n"
            "\n"
            "You do not always need the entire tensor. You can select parts "
            "of it using slicing.\n"
            "\n"
            "For example:\n"
            "\n"
            "```python\n"
            "first_batch = train_images[:128]\n"
            "```\n"
            "\n"
            "selects the first 128 samples.\n"
            "\n"
            "If `train_images` has shape `(60000, 28, 28)`, then:\n"
            "\n"
            "```python\n"
            "subset = train_images[10:100]\n"
            "```\n"
            "\n"
            "has shape:\n"
            "\n"
            "```text\n"
            "(90, 28, 28)\n"
            "```\n"
            "\n"
            "because index 100 is not included.\n"
            "\n"

            # Exercise EX01 is rendered here by the frontend.
            "{{exercise:M02.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Tensor Operations and Neural-Network Layers\n"
            "\n"
            "A neural network does not simply store tensors. It repeatedly "
            "transforms them.\n"
            "\n"
            "A Dense layer can be understood with the expression:\n"
            "\n"
            "```python\n"
            "output = relu(input @ W + b)\n"
            "```\n"
            "\n"
            "You do not need to memorize this immediately. Read it as a "
            "sequence of operations:\n"
            "\n"
            "```text\n"
            "input\n"
            "  ↓\n"
            "multiply by W\n"
            "  ↓\n"
            "add b\n"
            "  ↓\n"
            "apply ReLU\n"
            "  ↓\n"
            "output\n"
            "```\n"
            "\n"
            "`W` and `b` are trainable parameters. Their values change during "
            "training.\n"
            "\n"
            "### Element-wise operations\n"
            "\n"
            "Some operations act independently on every value of a tensor.\n"
            "\n"
            "For example, addition can be element-wise:\n"
            "\n"
            "```python\n"
            "x = np.array([1, 2, 3])\n"
            "y = np.array([10, 20, 30])\n"
            "\n"
            "z = x + y\n"
            "print(z)\n"
            "# [11 22 33]\n"
            "```\n"
            "\n"
            "Each value is combined with the value in the corresponding "
            "position.\n"
            "\n"
            "### ReLU\n"
            "\n"
            "ReLU is also applied element by element.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "relu(x) = max(x, 0)\n"
            "```\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "-5 → 0\n"
            "-2 → 0\n"
            " 0 → 0\n"
            " 3 → 3\n"
            " 8 → 8\n"
            "```\n"
            "\n"
            "For a vector:\n"
            "\n"
            "```text\n"
            "[-4, 3, -2, 7]\n"
            "       ↓ ReLU\n"
            "[ 0, 3,  0, 7]\n"
            "```\n"
            "\n"
            "Although the operation is simple, its role is extremely "
            "important: it introduces **nonlinearity**.\n"
            "\n"
            "Without nonlinear activation functions, stacking many Dense "
            "layers would still behave like a single linear or affine "
            "transformation. Adding nonlinear activations allows neural "
            "networks to represent much more complicated relationships.\n"
            "\n"
            "### Broadcasting\n"
            "\n"
            "Sometimes two tensors involved in an operation do not have "
            "identical shapes.\n"
            "\n"
            "Suppose:\n"
            "\n"
            "```text\n"
            "X shape = (32, 10)\n"
            "y shape = (10,)\n"
            "```\n"
            "\n"
            "When computing:\n"
            "\n"
            "```python\n"
            "X + y\n"
            "```\n"
            "\n"
            "the vector `y` can conceptually be treated as though it were "
            "repeated for each row of `X`.\n"
            "\n"
            "```text\n"
            "y\n"
            "y\n"
            "y\n"
            "...\n"
            "32 times\n"
            "```\n"
            "\n"
            "This behavior is called **broadcasting**.\n"
            "\n"
            "The repeated copies do not necessarily have to be physically "
            "created in memory. Repetition is a useful mental model for "
            "understanding what the operation means.\n"
            "\n"
            "Broadcasting explains how a bias vector `b` can be added across "
            "many samples in a Dense layer.\n"
            "\n"
            "### Matrix multiplication\n"
            "\n"
            "One of the most important tensor operations in neural networks "
            "is matrix multiplication.\n"
            "\n"
            "In Python you will often see:\n"
            "\n"
            "```python\n"
            "result = x @ y\n"
            "```\n"
            "\n"
            "or an equivalent matrix-multiplication function.\n"
            "\n"
            "For two matrices:\n"
            "\n"
            "```text\n"
            "(a, b) @ (b, c) → (a, c)\n"
            "```\n"
            "\n"
            "The two inner dimensions must match.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "(32, 784) @ (784, 512)\n"
            "               ↑\n"
            "       matching dimension\n"
            "\n"
            "result → (32, 512)\n"
            "```\n"
            "\n"
            "Interpret this as 32 samples, each represented by 784 values, "
            "being transformed into 32 new representations, each containing "
            "512 values.\n"
            "\n"
            "### Reshaping\n"
            "\n"
            "Reshaping changes how tensor values are organized without "
            "changing the total number of values.\n"
            "\n"
            "For example:\n"
            "\n"
            "```python\n"
            "x = np.array([\n"
            "    [0, 1],\n"
            "    [2, 3],\n"
            "    [4, 5],\n"
            "])\n"
            "\n"
            "print(x.shape)\n"
            "# (3, 2)\n"
            "\n"
            "x = x.reshape((2, 3))\n"
            "\n"
            "print(x)\n"
            "# [[0 1 2]\n"
            "#  [3 4 5]]\n"
            "```\n"
            "\n"
            "Both shapes contain six values:\n"
            "\n"
            "```text\n"
            "3 × 2 = 6\n"
            "2 × 3 = 6\n"
            "```\n"
            "\n"
            "That is why this reshape is possible.\n"
            "\n"
            "Flattening an MNIST image follows the same idea:\n"
            "\n"
            "```text\n"
            "(28, 28)\n"
            "    ↓ reshape\n"
            "(784,)\n"
            "```\n"
            "\n"
            "### Geometric intuition\n"
            "\n"
            "Tensor operations can also be understood as geometric "
            "transformations.\n"
            "\n"
            "Adding a vector can move points through space. Matrix "
            "multiplication can rotate, scale or otherwise transform their "
            "coordinates.\n"
            "\n"
            "A Dense layer without an activation performs an affine "
            "transformation:\n"
            "\n"
            "```text\n"
            "input @ W + b\n"
            "```\n"
            "\n"
            "A nonlinear activation such as ReLU then bends the representation "
            "in a way that cannot be reproduced by simply stacking linear "
            "transformations.\n"
            "\n"
            "One useful mental image is to imagine data from two classes as "
            "two sheets of paper crumpled together into one complicated ball. "
            "Each neural-network layer performs another transformation that "
            "helps untangle the data until the classes become easier to "
            "separate.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. How Neural Networks Learn: Gradients and Backpropagation\n"
            "\n"
            "Now we reach the central question:\n"
            "\n"
            "> How does the network learn useful values for `W` and `b`?\n"
            "\n"
            "These tensors are the layer's **trainable parameters**, often "
            "called its weights.\n"
            "\n"
            "At the beginning of training, the parameters start from initial "
            "values that have not yet learned the task. The resulting "
            "predictions are therefore not expected to be useful yet.\n"
            "\n"
            "Training repeatedly adjusts these parameters so that the model's "
            "loss decreases.\n"
            "\n"
            "### The basic training loop\n"
            "\n"
            "The process is:\n"
            "\n"
            "```text\n"
            "1. Select a batch of inputs and correct targets.\n"
            "2. Run the model to produce predictions.\n"
            "3. Calculate the loss.\n"
            "4. Calculate how the parameters affected that loss.\n"
            "5. Adjust the parameters to reduce the loss.\n"
            "6. Repeat.\n"
            "```\n"
            "\n"
            "Steps 2 and 3 are straightforward once the model and loss "
            "function have been defined.\n"
            "\n"
            "The interesting question is step 4:\n"
            "\n"
            "> How do we know which parameter should increase, which should "
            "decrease, and by how much?\n"
            "\n"
            "The answer begins with derivatives.\n"
            "\n"
            "### Derivative intuition\n"
            "\n"
            "Imagine standing on a hill.\n"
            "\n"
            "At your current position, you want to know:\n"
            "\n"
            "- Which direction goes uphill?\n"
            "- Which direction goes downhill?\n"
            "- How steep is the slope?\n"
            "\n"
            "A derivative provides this kind of local information for a "
            "function with one input variable.\n"
            "\n"
            "If the derivative is positive, increasing the input slightly "
            "causes the function value to increase locally.\n"
            "\n"
            "If the derivative is negative, increasing the input slightly "
            "causes the function value to decrease locally.\n"
            "\n"
            "The magnitude tells us how strongly the output changes.\n"
            "\n"
            "This is useful because training is an optimization problem: we "
            "want parameter values that produce a smaller loss.\n"
            "\n"
            "### From derivatives to gradients\n"
            "\n"
            "A real neural network does not contain only one adjustable "
            "number. It may contain thousands, millions or more parameters.\n"
            "\n"
            "The multidimensional generalization of the derivative is the "
            "**gradient**.\n"
            "\n"
            "You can think of a gradient as a collection of local directions "
            "describing how changes to the model's parameters would affect "
            "the loss.\n"
            "\n"
            "For example, conceptually:\n"
            "\n"
            "```text\n"
            "parameter 1 gradient → +0.80\n"
            "parameter 2 gradient → -0.20\n"
            "parameter 3 gradient → +0.03\n"
            "...\n"
            "```\n"
            "\n"
            "The gradient therefore gives us the information needed to decide "
            "how the parameters should move.\n"
            "\n"
            "### Gradient descent\n"
            "\n"
            "If the gradient tells us the direction in which loss increases, "
            "then reducing loss means moving in the opposite direction.\n"
            "\n"
            "The essential update rule is:\n"
            "\n"
            "```python\n"
            "new_weight = old_weight - learning_rate * gradient\n"
            "```\n"
            "\n"
            "This is the core intuition behind **gradient descent**.\n"
            "\n"
            "You can imagine the loss as a landscape and the model's current "
            "parameters as your current position on that landscape.\n"
            "\n"
            "Training repeatedly looks at the local slope and takes a small "
            "step downhill.\n"
            "\n"
            "### Learning rate\n"
            "\n"
            "The **learning rate** controls the size of the update.\n"
            "\n"
            "If the learning rate is too small:\n"
            "\n"
            "```text\n"
            "The model takes tiny steps.\n"
            "Training may progress very slowly.\n"
            "```\n"
            "\n"
            "If it is too large:\n"
            "\n"
            "```text\n"
            "The model may jump over useful regions.\n"
            "Training may become unstable.\n"
            "```\n"
            "\n"
            "The goal is therefore to use updates that are useful without "
            "being excessively large.\n"
            "\n"
            "### Mini-batch stochastic gradient descent\n"
            "\n"
            "Rather than calculate every update using the full training "
            "dataset, neural networks commonly train on small batches.\n"
            "\n"
            "For every batch:\n"
            "\n"
            "```text\n"
            "batch\n"
            "  ↓\n"
            "forward pass\n"
            "  ↓\n"
            "predictions\n"
            "  ↓\n"
            "loss\n"
            "  ↓\n"
            "backward pass\n"
            "  ↓\n"
            "gradients\n"
            "  ↓\n"
            "parameter update\n"
            "```\n"
            "\n"
            "This is the basic idea behind mini-batch stochastic gradient "
            "descent.\n"
            "\n"
            "### Forward pass\n"
            "\n"
            "During the **forward pass**, data moves through the network to "
            "produce a prediction.\n"
            "\n"
            "```text\n"
            "Input\n"
            "  ↓\n"
            "Layer 1\n"
            "  ↓\n"
            "Layer 2\n"
            "  ↓\n"
            "Prediction\n"
            "  ↓\n"
            "Loss\n"
            "```\n"
            "\n"
            "### The problem solved by backpropagation\n"
            "\n"
            "Suppose a neural network contains many operations and many "
            "parameters.\n"
            "\n"
            "After computing the final loss, we need to answer:\n"
            "\n"
            "> How did every trainable parameter contribute to this result?\n"
            "\n"
            "This is the role of **backpropagation**.\n"
            "\n"
            "Backpropagation works backward through the sequence of operations "
            "used during the forward pass.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Loss\n"
            " ↑\n"
            "Output layer\n"
            " ↑\n"
            "Hidden layer\n"
            " ↑\n"
            "Earlier layer\n"
            "```\n"
            "\n"
            "It uses the derivatives of simple operations to calculate "
            "gradients through the entire network.\n"
            "\n"
            "### The chain rule\n"
            "\n"
            "A neural network is a chain of functions.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "input\n"
            " → matrix multiplication\n"
            " → addition\n"
            " → ReLU\n"
            " → matrix multiplication\n"
            " → softmax\n"
            " → loss\n"
            "```\n"
            "\n"
            "The mathematical chain rule allows derivatives of these simple "
            "operations to be combined so that we can determine how an early "
            "parameter ultimately affects the final loss.\n"
            "\n"
            "That is the mathematical foundation of backpropagation.\n"
            "\n"
            "Modern deep-learning frameworks perform this gradient calculation "
            "automatically. This capability is generally called automatic "
            "differentiation.\n"
            "\n"
            "### Backward pass\n"
            "\n"
            "The backward pass calculates gradients.\n"
            "\n"
            "A useful distinction is:\n"
            "\n"
            "```text\n"
            "Forward pass:\n"
            "input → prediction → loss\n"
            "\n"
            "Backward pass:\n"
            "loss → gradients for parameters\n"
            "```\n"
            "\n"
            "After the gradients are known, the optimizer uses them to update "
            "the parameters.\n"
            "\n"
            "### Loss versus gradient versus optimizer\n"
            "\n"
            "These concepts are easy to mix up, so keep their responsibilities "
            "separate.\n"
            "\n"
            "```text\n"
            "Loss\n"
            "→ How wrong is the model?\n"
            "\n"
            "Gradient\n"
            "→ How does the loss locally change with the parameters?\n"
            "\n"
            "Optimizer\n"
            "→ How should those gradients be used to update the parameters?\n"
            "```\n"
            "\n"
            "### The complete learning process\n"
            "\n"
            "Putting everything together:\n"
            "\n"
            "```text\n"
            "Training data\n"
            "     ↓\n"
            "Neural network\n"
            "     ↓\n"
            "Prediction\n"
            "     ↓\n"
            "Loss\n"
            "     ↓\n"
            "Backpropagation\n"
            "     ↓\n"
            "Gradients\n"
            "     ↓\n"
            "Optimizer\n"
            "     ↓\n"
            "Updated parameters\n"
            "     ↓\n"
            "Repeat\n"
            "```\n"
            "\n"
            "A simplified training loop could be imagined as:\n"
            "\n"
            "```python\n"
            "for epoch in range(epochs):\n"
            "    for batch in training_data:\n"
            "        predictions = model(batch.inputs)\n"
            "        loss = loss_function(predictions, batch.targets)\n"
            "        gradients = calculate_gradients(loss)\n"
            "        update_parameters(gradients)\n"
            "```\n"
            "\n"
            "Deep-learning frameworks automate most of these details, but "
            "understanding this loop lets you understand what those convenient "
            "training functions are actually doing.\n"
            "\n"
            "### Where is the model's learned knowledge?\n"
            "\n"
            "For the simple Dense layers discussed here, learned information "
            "is contained in the trainable parameter tensors such as `W` and "
            "`b`.\n"
            "\n"
            "Training is therefore not the process of adding new handwritten "
            "rules to the program. It is the process of adjusting many "
            "numerical parameter values so that the network's transformations "
            "produce increasingly useful predictions.\n"
            "\n"

            # Exercise EX02 is rendered here by the frontend.
            "{{exercise:M02.L01.EX02}}\n"
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
            "> A tensor's rank is the total number of values stored inside it.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Rank means the number of axes, not the total number of values.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "shape = (60000, 28, 28)\n"
            "rank  = 3\n"
            "```\n"
            "\n"
            "The tensor contains millions of numerical values but still has "
            "only three axes.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> A five-dimensional vector is automatically a rank-5 tensor.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A vector containing five values has shape `(5,)` and therefore "
            "only one axis. It is rank 1.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Loss and accuracy mean the same thing.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Accuracy measures the fraction of correct classifications. Loss "
            "provides the numerical optimization signal used to guide learning. "
            "Two models can even have the same accuracy while having different "
            "loss values.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> Backpropagation itself updates the model's parameters.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Backpropagation is used to calculate gradients. The optimizer "
            "uses those gradients to perform parameter updates.\n"
            "\n"
            "A useful separation is:\n"
            "\n"
            "```text\n"
            "backpropagation → gradients\n"
            "optimizer       → parameter update\n"
            "```\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> More Dense layers always make a network powerful, even without "
            "activation functions.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Repeated affine transformations without nonlinear activations can "
            "collapse into another affine transformation. Nonlinear activation "
            "functions such as ReLU allow the network to model substantially "
            "more complex relationships.\n"
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
            "| Sample | One individual data example |\n"
            "| Class | One possible category in a classification problem |\n"
            "| Label | The correct class associated with a sample |\n"
            "| Training set | Data used to learn model parameters |\n"
            "| Test set | Separate data used to evaluate performance on unseen examples |\n"
            "| Tensor | Numerical data container used throughout deep learning |\n"
            "| Rank | Number of axes in a tensor |\n"
            "| Shape | Number of values along each tensor axis |\n"
            "| dtype | Type of numerical values stored in a tensor |\n"
            "| Batch | Small group of samples processed together |\n"
            "| Epoch | One complete pass through the training dataset |\n"
            "| Dense layer | Layer in which outputs are formed from learned combinations of inputs |\n"
            "| Weight | Trainable numerical parameter of a model |\n"
            "| Bias | Trainable value added during a layer transformation |\n"
            "| ReLU | Nonlinear activation defined conceptually as `max(x, 0)` |\n"
            "| Softmax | Transformation that produces normalized scores suitable for class probabilities |\n"
            "| Broadcasting | Applying operations between compatible tensors of different shapes |\n"
            "| Matrix multiplication | Tensor operation commonly written with `@` in Python |\n"
            "| Reshaping | Changing tensor organization while preserving its number of values |\n"
            "| Loss | Quantity measuring the mismatch between predictions and targets |\n"
            "| Gradient | Local information describing how loss changes with model parameters |\n"
            "| Gradient descent | Optimization approach that moves parameters toward lower loss |\n"
            "| Learning rate | Factor controlling the size of parameter updates |\n"
            "| Forward pass | Computing predictions and loss from inputs |\n"
            "| Backward pass | Computing gradients from the loss back through the model |\n"
            "| Backpropagation | Algorithm for propagating derivative information through chained operations |\n"
            "| Optimizer | Procedure that uses gradients to update trainable parameters |\n"
            "| Overfitting | Performing better on training data than on unseen data because the model has adapted too specifically to training examples |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer these questions "
            "without looking back at the lesson:\n"
            "\n"
            "1. What is the difference between a tensor's rank and shape?\n"
            "2. What does `(60000, 28, 28)` mean for the MNIST training data?\n"
            "3. Why is a five-element vector still a rank-1 tensor?\n"
            "4. What does broadcasting allow us to do?\n"
            "5. For `(32, 784) @ (784, 512)`, what is the output shape?\n"
            "6. Why is an activation function such as ReLU important?\n"
            "7. What is the difference between loss and accuracy?\n"
            "8. What information does a gradient provide?\n"
            "9. Why does gradient descent move opposite the gradient?\n"
            "10. What does the learning rate control?\n"
            "11. What happens during a forward pass?\n"
            "12. What happens during a backward pass?\n"
            "13. What is the purpose of backpropagation?\n"
            "14. What is the optimizer responsible for?\n"
            "15. Where is the learned information of the model represented?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**A neural network learns by transforming tensor data with "
            "trainable parameters, measuring its prediction error with a loss "
            "function, computing gradients through backpropagation, and using "
            "an optimizer to repeatedly adjust those parameters toward lower "
            "loss.**\n"
            "\n"
            "Keep this chain in your head:\n"
            "\n"
            "```text\n"
            "Data\n"
            " → Tensors\n"
            " → Layers\n"
            " → Prediction\n"
            " → Loss\n"
            " → Backpropagation\n"
            " → Gradients\n"
            " → Optimizer\n"
            " → Updated parameters\n"
            " → Better predictions\n"
            "```\n"
        ),

        "estimated_minutes": 90,

        "has_code_examples": True,

        "sections": [
            {
                "id": "first-neural-network",
                "title": "Your First Mental Model of a Neural Network",
                "order": 1,
            },
            {
                "id": "tensors",
                "title": "Tensors: How Neural Networks Store Data",
                "order": 2,
            },
            {
                "id": "tensor-operations",
                "title": "Tensor Operations and Neural-Network Layers",
                "order": 3,
            },
            {
                "id": "learning-with-gradients",
                "title": "How Neural Networks Learn: Gradients and Backpropagation",
                "order": 4,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M02.L01.EX01",

            "title": "Read and Interpret Tensor Shapes",

            "lesson_code": "M02.L01",

            "section_id": "tensors",

            "placement": "after_section",

            "description": (
                "Practice identifying tensor rank, axes and the real-world "
                "meaning of common machine-learning tensor shapes."
            ),

            "instructions": (
                "For each tensor below, identify its rank and explain what "
                "each axis could represent.\n\n"
                "1. `(5000, 12)` — a table of customer data.\n"
                "2. `(128, 256, 256, 3)` — a batch of RGB images.\n"
                "3. `(32, 100, 64)` — a batch of sequences.\n"
                "4. `(4, 240, 144, 256, 3)` — a batch of videos.\n\n"
                "Then answer:\n"
                "5. What is the difference between rank and shape?\n"
                "6. A vector has shape `(5,)`. Is it rank 1 or rank 5? "
                "Explain why.\n"
                "7. If `images` has shape `(60000, 28, 28)`, what shape "
                "would `images[:128]` have?"
            ),

            "expected_output": (
                "A short table or written answer showing the rank of each "
                "tensor, the meaning of its axes, and clear explanations for "
                "the rank-versus-shape questions."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tensor-rank",
                "tensor-shape",
                "axis-interpretation",
                "tensor-slicing",
            ],
        },

        {
            "id": "M02.L01.EX02",

            "title": "Trace One Neural-Network Training Step",

            "lesson_code": "M02.L01",

            "section_id": "learning-with-gradients",

            "placement": "after_section",

            "description": (
                "Connect the forward pass, loss, gradients, backpropagation "
                "and optimizer into one coherent model-training step."
            ),

            "instructions": (
                "Suppose a neural network receives a batch of digit images.\n\n"
                "1. Put these operations in the correct order: parameter "
                "update, prediction, gradient calculation, input batch, loss "
                "calculation.\n"
                "2. Label which operations belong to the forward pass.\n"
                "3. Label which operation belongs to the backward pass.\n"
                "4. Explain what the loss tells us.\n"
                "5. Explain what the gradient tells us.\n"
                "6. Explain what the optimizer does.\n"
                "7. Given the conceptual update "
                "`new_weight = old_weight - learning_rate * gradient`, "
                "explain the purpose of the minus sign.\n"
                "8. Describe what could happen if the learning rate were "
                "extremely large."
            ),

            "expected_output": (
                "An ordered training pipeline plus short explanations of loss, "
                "gradient, backpropagation, optimizer and learning rate."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "training-loop",
                "forward-pass",
                "backpropagation",
                "gradient-descent",
                "optimization",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M02.L01.QZ01",

        "title": "How Neural Networks Represent Data and Learn — Knowledge Check",

        "lesson_code": "M02.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M02.L01.Q01",

                "section_id": "first-neural-network",

                "question": (
                    "Why is a separate test set used after training a neural "
                    "network?"
                ),

                "options": [
                    "To provide additional examples for updating the model's weights",
                    "To make each training batch larger",
                    "To evaluate how well the model performs on data it did not train on",
                    "To convert images into tensors",
                ],

                "correct": 2,

                "explanation": (
                    "The training set is used to learn parameters. The test set "
                    "is kept separate so that it can estimate performance on "
                    "unseen examples. Using the test examples for parameter "
                    "updates would undermine this purpose."
                ),
            },

            {
                "id": "M02.L01.Q02",

                "section_id": "tensors",

                "question": (
                    "A tensor has shape `(128, 256, 256, 3)`. What is its rank?"
                ),

                "options": [
                    "3",
                    "4",
                    "128",
                    "256",
                ],

                "correct": 1,

                "explanation": (
                    "Rank is the number of axes. The shape contains four axis "
                    "sizes—128, 256, 256 and 3—so the tensor is rank 4."
                ),
            },

            {
                "id": "M02.L01.Q03",

                "section_id": "tensor-operations",

                "question": (
                    "What is the resulting shape of "
                    "`(32, 784) @ (784, 512)`?"
                ),

                "options": [
                    "(32, 512)",
                    "(784, 784)",
                    "(512, 32)",
                    "(32, 784, 512)",
                ],

                "correct": 0,

                "explanation": (
                    "For matrix multiplication `(a, b) @ (b, c)`, the inner "
                    "dimensions must match and the resulting shape is `(a, c)`. "
                    "Therefore `(32, 784) @ (784, 512)` produces `(32, 512)`."
                ),
            },

            {
                "id": "M02.L01.Q04",

                "section_id": "learning-with-gradients",

                "question": (
                    "Why does a basic gradient-descent update subtract the "
                    "gradient from the current parameter value?"
                ),

                "options": [
                    "Because gradients always contain negative numbers",
                    "Because subtraction converts tensors into scalars",
                    "Because the model must make every parameter smaller",
                    "Because moving opposite the local gradient is intended to reduce the loss",
                ],

                "correct": 3,

                "explanation": (
                    "The gradient describes the local direction of increasing "
                    "loss. Gradient descent therefore takes a step in the "
                    "opposite direction, scaled by the learning rate, with the "
                    "goal of reducing the loss."
                ),
            },

            {
                "id": "M02.L01.Q05",

                "section_id": "learning-with-gradients",

                "type": "open",

                "question": (
                    "A model receives a batch of images, produces predictions, "
                    "calculates a loss, performs backpropagation and then uses "
                    "an optimizer. Explain what happens at each stage and how "
                    "these stages together allow the model to learn."
                ),
            },
        ],

        "passing_score": 70,
    },
}