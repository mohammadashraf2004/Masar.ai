"""M01.L01 — Introducing Deep Learning and the PyTorch Library.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 1.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"
MODULE_ORDER = 1
MODULE_TITLE = "Deep Learning & PyTorch Foundations"
MODULE_DESCRIPTION = (
    "Build the mental model needed for practical deep learning with PyTorch: "
    "what deep learning changes, how training works, why PyTorch is useful, "
    "and how data, models, optimization, hardware, and deployment fit together."
)

SOURCE_CHAPTER = 1
SOURCE_PAGES = "Chapter 1 (page range not provided in source excerpt)"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Introducing Deep Learning and the PyTorch Library",
    "slug": "applied-deep-learning-m01-l01",
    "description": (
        "A practical introduction to deep learning and PyTorch that explains "
        "representation learning, training, tensors, autograd, the end-to-end "
        "project workflow, hardware choices, and the role of Jupyter."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 1.5,
    "skill_tags": [
        "deep-learning",
        "pytorch",
        "feature-learning",
        "tensors",
        "autograd",
        "training-loop",
        "data-loading",
        "deployment",
        "jupyter",
    ],
    "prerequisite_ids": [],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Introducing Deep Learning and the PyTorch Library",
        "content": (
            "# Introducing Deep Learning and the PyTorch Library\n"
            "\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** Deep Learning & PyTorch Foundations  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, "
            "Chapter 1. This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what deep learning is without confusing it with human-like thinking.\n"
            "- Distinguish manual feature engineering from representation learning.\n"
            "- Describe the basic purpose of a model, loss function, optimizer, and training loop.\n"
            "- Explain why PyTorch is useful for deep learning work.\n"
            "- Describe the roles of tensors and automatic differentiation (`autograd`).\n"
            "- Trace the path from raw data to a trained and deployed PyTorch model.\n"
            "- Decide when CPU hardware is sufficient and when a GPU becomes valuable.\n"
            "- Verify a basic PyTorch and Jupyter environment before starting a project.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. What deep learning actually is\n"
            "\n"
            "Artificial intelligence is a broad term for computer systems that perform tasks "
            "that normally require abilities we associate with human intelligence. Deep learning "
            "is one important approach inside that larger field.\n"
            "\n"
            "A useful beginner mental model is this:\n"
            "\n"
            "> **Deep learning trains large mathematical functions to map inputs to useful outputs "
            "by learning from examples.**\n"
            "\n"
            "The important phrase is **learning from examples**. Instead of a programmer writing "
            "every rule needed to recognize an image, generate text, or transform speech, a deep "
            "learning system adjusts internal numerical parameters so that its outputs increasingly "
            "match the desired behavior shown by training data.\n"
            "\n"
            "This does **not** require us to claim that the machine thinks like a person. The practical "
            "achievement is that neural networks can approximate complicated nonlinear relationships "
            "well enough to automate tasks that were once extremely difficult to program manually.\n"
            "\n"
            "### Examples of input-to-output mappings\n"
            "\n"
            "| Input | Desired output |\n"
            "|---|---|\n"
            "| A photograph | The object or class present in the image |\n"
            "| A text description | A generated image |\n"
            "| A written script | Natural-sounding speech |\n"
            "| A prompt | Generated text |\n"
            "\n"
            "These applications look very different, but the common idea is the same: learn a useful "
            "mapping from examples rather than encode every decision as a handwritten rule.\n"
            "\n"
            "One more detail matters early: generative models can produce outputs probabilistically. "
            "That means the same general request may not always produce exactly the same result.\n"
            "\n"
            "---\n"
            "\n"

            "## 2. From feature engineering to representation learning\n"
            "\n"
            "To understand why deep learning changed machine learning practice, first understand "
            "**features**.\n"
            "\n"
            "A **raw feature** is a value taken directly from the original data. In an image, raw "
            "features could simply be pixel values. Raw values often do not expose the useful pattern "
            "clearly enough for a traditional learning algorithm.\n"
            "\n"
            "### Traditional machine learning: engineer useful features\n"
            "\n"
            "In many traditional machine learning workflows, a human uses domain knowledge to design "
            "transformations that make the task easier. This is called **feature engineering**.\n"
            "\n"
            "Suppose we want to distinguish handwritten `0` digits from handwritten `1` digits. A "
            "traditional workflow might design features such as:\n"
            "\n"
            "- the directions of important edges,\n"
            "- the presence of enclosed holes,\n"
            "- shape statistics that help separate one digit from another.\n"
            "\n"
            "The classifier then learns from those engineered measurements instead of directly from "
            "the original image.\n"
            "\n"
            "### Deep learning: learn the representation too\n"
            "\n"
            "Deep learning reduces the need to manually invent all of those intermediate features. "
            "A neural network can learn useful internal representations directly from training "
            "examples. During training, the network changes its internal parameters so that the "
            "representations it builds become more useful for the task.\n"
            "\n"
            "This is often called **representation learning**.\n"
            "\n"
            "The shift can be summarized like this:\n"
            "\n"
            "```text\n"
            "Traditional ML:\n"
            "raw data -> human-designed features -> learning algorithm -> prediction\n"
            "\n"
            "Deep learning:\n"
            "raw data -> learned hierarchy of representations -> prediction\n"
            "```\n"
            "\n"
            "Deep learning does not make domain knowledge useless. We may still make choices about "
            "data preparation, model structure, objectives, or constraints. The important change is "
            "that the model can learn many of the task-specific representations automatically.\n"
            "\n"
            "[[IMAGE_NEEDED: Feature engineering versus representation learning | "
            "A two-part diagram comparing a traditional ML pipeline where a practitioner manually "
            "creates features before a learning algorithm with a deep-learning pipeline where raw "
            "data enters a neural network that learns hierarchical features automatically during "
            "training | Learner should notice that deep learning reduces manual feature design but "
            "typically increases dependence on data, training, and computation]]\n"
            "\n"
            "The practical trade-off is important: deep learning often replaces some manual feature "
            "engineering effort with greater requirements for **data**, **computation**, and "
            "**optimization**.\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 3. The training mental model: model, loss, and optimization\n"
            "\n"
            "A deep neural network starts as a mathematical function whose parameters are not yet "
            "useful for the task. Training is the process that turns this untrained function into a "
            "useful model.\n"
            "\n"
            "You can understand the core loop with four ideas:\n"
            "\n"
            "1. **Input data** is passed through the model.\n"
            "2. The model produces an **output**.\n"
            "3. A **loss function** compares that output with the desired target and produces a number.\n"
            "4. Training updates the model's parameters in a direction intended to reduce that loss.\n"
            "\n"
            "A loss function may also be called a **criterion**, **objective function**, or **cost "
            "function**. In introductory deep learning, all of these names refer to the numerical "
            "signal used to measure how far the model's behavior is from what we want.\n"
            "\n"
            "### A tiny numerical example\n"
            "\n"
            "Imagine a model should output `10`, but currently outputs `7`.\n"
            "\n"
            "```text\n"
            "desired output = 10\n"
            "model output   = 7\n"
            "difference     = 3\n"
            "```\n"
            "\n"
            "A real loss function may measure the error differently, but the purpose is the same: "
            "convert model quality into a numerical value that training can try to improve.\n"
            "\n"
            "The goal is **not** merely to drive the loss down on examples already seen during "
            "training. A useful model should also perform well on relevant data it did not see while "
            "its parameters were being updated. This is the first glimpse of the idea of "
            "**generalization**.\n"
            "\n"
            "A compact mental model is therefore:\n"
            "\n"
            "```text\n"
            "predict -> measure error -> update parameters -> repeat\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Why PyTorch is a good fit for deep learning\n"
            "\n"
            "PyTorch is a Python library designed to make numerical computing and deep learning "
            "practical. The source chapter emphasizes several reasons it works well as a first deep "
            "learning framework.\n"
            "\n"
            "### 4.1 It feels like Python\n"
            "\n"
            "PyTorch is designed to be expressive and familiar to Python programmers. You can build "
            "computations incrementally, inspect intermediate values, and debug code using normal "
            "Python workflows. If you already know NumPy, many tensor concepts will feel familiar.\n"
            "\n"
            "### 4.2 It can use GPUs\n"
            "\n"
            "Deep learning requires large amounts of numerical computation. PyTorch can execute many "
            "tensor operations on GPUs, which are designed for massive parallel numerical workloads. "
            "That can dramatically reduce training time compared with performing the same large "
            "workload only on a CPU.\n"
            "\n"
            "### 4.3 It supports automatic optimization\n"
            "\n"
            "PyTorch tracks numerical operations and can automatically compute the derivatives needed "
            "during optimization. This is what allows complex neural networks to be trained without "
            "you manually deriving and coding every gradient calculation.\n"
            "\n"
            "### 4.4 It scales beyond experiments\n"
            "\n"
            "The framework is not limited to notebook experiments. The chapter describes PyTorch "
            "support for production deployment, C++ runtimes, multiple devices, distributed training, "
            "compilation, model export, and mobile or edge deployment.\n"
            "\n"
            "### 4.5 The ecosystem is broader than one framework\n"
            "\n"
            "The deep learning ecosystem has changed over time. The chapter discusses older tools such "
            "as Theano, the continuing role of TensorFlow, the rise of JAX, and Hugging Face as a "
            "high-level ecosystem for pretrained models. The educational point is not to memorize a "
            "framework popularity timeline. It is to understand that **frameworks evolve, while core "
            "deep learning concepts transfer**.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. The two foundations you should recognize immediately: tensors and autograd\n"
            "\n"
            "Most of practical PyTorch begins with two concepts: **tensors** and **automatic "
            "differentiation**.\n"
            "\n"
            "### 5.1 Tensors\n"
            "\n"
            "A PyTorch tensor is a multidimensional array. Depending on its dimensions, it can hold:\n"
            "\n"
            "- a single number,\n"
            "- a vector,\n"
            "- a matrix,\n"
            "- or a higher-dimensional block of data.\n"
            "\n"
            "Images, batches of images, model weights, and many other deep learning values are "
            "represented as tensors.\n"
            "\n"
            "A tiny example:\n"
            "\n"
            "```python\n"
            "import torch\n"
            "\n"
            "x = torch.tensor([1.0, 2.0, 3.0])\n"
            "print(x)\n"
            "```\n"
            "\n"
            "At this stage, do not worry about every tensor operation. The key idea is that tensors "
            "are the standard numerical containers that PyTorch models operate on.\n"
            "\n"
            "### 5.2 Autograd\n"
            "\n"
            "When PyTorch performs mathematical operations on tensors participating in a learnable "
            "computation, it can keep track of the operation history. Its automatic differentiation "
            "engine, **autograd**, uses that history to determine how changes earlier in the "
            "computation would affect later outputs.\n"
            "\n"
            "That information is essential for optimization: it tells training how model parameters "
            "should be adjusted to reduce the loss.\n"
            "\n"
            "You do not need the calculus details yet. Retain this relationship:\n"
            "\n"
            "```text\n"
            "tensors -> model computation -> loss\n"
            "                         |\n"
            "                         v\n"
            "                 autograd gradients\n"
            "                         |\n"
            "                         v\n"
            "                 parameter updates\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 6. The anatomy of a PyTorch deep learning project\n"
            "\n"
            "A successful project is larger than the neural network itself. The chapter presents a "
            "high-level workflow that includes data loading, model construction, training, and "
            "deployment.\n"
            "\n"
            "[[IMAGE_NEEDED: High-level PyTorch project workflow | "
            "A left-to-right pipeline showing raw data or storage, Dataset conversion to tensors, "
            "DataLoader batching, an untrained model, the training loop with loss and optimizer, a "
            "trained model, and deployment; include optional multi-GPU or multi-machine training "
            "beneath the training stage | Learner should notice that the neural network is only one "
            "component in a complete deep learning system]]\n"
            "\n"
            "Let's walk through the pipeline.\n"
            "\n"
            "### 6.1 Get data into tensor form with `Dataset`\n"
            "\n"
            "Real data may begin as images, files, records, or another problem-specific format. "
            "PyTorch models ultimately need tensors. The `Dataset` abstraction from "
            "`torch.utils.data` provides a bridge between custom stored data and the tensor samples "
            "used by the learning system.\n"
            "\n"
            "You often implement the problem-specific part yourself because reading a medical scan, "
            "a photograph, or another dataset can require very different logic.\n"
            "\n"
            "### 6.2 Feed data efficiently with `DataLoader`\n"
            "\n"
            "Training usually processes multiple samples repeatedly. `DataLoader` helps organize "
            "samples into batches and can load data in parallel so that the training loop spends less "
            "time waiting for storage operations.\n"
            "\n"
            "### 6.3 Build the model with `torch.nn`\n"
            "\n"
            "PyTorch provides common neural-network building blocks through `torch.nn`, including "
            "layers, activation functions, and loss functions. These components are used to define "
            "the mathematical function that will become the trained model.\n"
            "\n"
            "### 6.4 Run the training loop\n"
            "\n"
            "At a high level, the loop repeats the same sequence:\n"
            "\n"
            "```text\n"
            "for each batch:\n"
            "    1. run the model on the inputs\n"
            "    2. compare outputs with targets using a loss function\n"
            "    3. compute gradients with autograd\n"
            "    4. let the optimizer update model parameters\n"
            "```\n"
            "\n"
            "PyTorch optimizers are provided through `torch.optim`.\n"
            "\n"
            "### 6.5 Scale when the problem demands it\n"
            "\n"
            "A basic project may train on a CPU or one GPU. Larger projects can distribute training "
            "across multiple GPUs or multiple machines. The chapter points to `torch.distributed` as "
            "the PyTorch area used for this kind of scaling.\n"
            "\n"
            "### 6.6 Deploy the trained model\n"
            "\n"
            "A trained model is useful only when it can perform the task where it is needed. "
            "Deployment might mean running it on a server, integrating it into a larger application, "
            "exporting it for another runtime, or targeting mobile or edge hardware.\n"
            "\n"
            "The chapter also introduces several deployment and performance tools at a high level:\n"
            "\n"
            "- `torch.compile` for optimizing PyTorch execution,\n"
            "- ONNX export for interoperable model representation,\n"
            "- ExecuTorch for supported mobile and edge scenarios.\n"
            "\n"
            "You do not need to master these tools in the first lesson. Their purpose here is to show "
            "that a deep learning project continues beyond model training.\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Hardware and software: what you actually need\n"
            "\n"
            "A common beginner mistake is to assume that deep learning cannot be learned without an "
            "expensive GPU. The chapter makes a more practical distinction.\n"
            "\n"
            "### CPU is enough for many learning tasks\n"
            "\n"
            "A recent laptop or desktop can run pretrained networks and many introductory examples. "
            "You can learn the first part of a PyTorch course, inspect tensors, experiment with model "
            "code, and perform smaller computations without specialized hardware.\n"
            "\n"
            "### GPUs matter when training becomes heavy\n"
            "\n"
            "Training performs large numerical operations repeatedly. On larger networks and datasets, "
            "a CUDA-capable GPU can reduce training time dramatically. More advanced workloads may "
            "use multiple GPUs or cloud computing resources.\n"
            "\n"
            "The source chapter's later practical examples assume stronger GPU hardware for full "
            "training runs, but the broader lesson is more useful than a specific GPU model number:\n"
            "\n"
            "> **Choose hardware according to workload size, not according to the word 'deep learning'.**\n"
            "\n"
            "### Storage can become a real engineering constraint\n"
            "\n"
            "Large projects may require significant disk capacity for raw data, extracted data, and "
            "cached training artifacts. The source chapter gives an example project whose storage "
            "requirements are much larger than the model code itself. This is a reminder that machine "
            "learning engineering includes data and infrastructure planning, not just neural networks.\n"
            "\n"
            "### Operating systems\n"
            "\n"
            "PyTorch can run on Linux, macOS, and Windows. Exact installation commands vary by "
            "platform and environment, so installation should follow the official PyTorch instructions "
            "appropriate to the machine being used.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Jupyter Notebooks and your first environment check\n"
            "\n"
            "The chapter uses Jupyter Notebooks heavily because they allow code, results, plots, and "
            "explanatory text to live together in an interactive document.\n"
            "\n"
            "### The notebook mental model\n"
            "\n"
            "A notebook contains **cells**. Code cells are sent to a running Python **kernel**. The "
            "kernel keeps variables in memory until it is restarted or terminated, so later cells can "
            "use values created by earlier cells.\n"
            "\n"
            "That statefulness is useful, but it also creates an important beginner habit:\n"
            "\n"
            "> When results seem strange, check whether your notebook's execution order and kernel "
            "state match what you think they are.\n"
            "\n"
            "### First PyTorch environment checks\n"
            "\n"
            "The chapter's exercises suggest verifying Python, PyTorch, CUDA availability, and the "
            "Jupyter environment. A simple check is:\n"
            "\n"
            "```python\n"
            "import sys\n"
            "import torch\n"
            "\n"
            "print('Python:', sys.version)\n"
            "print('PyTorch:', torch.__version__)\n"
            "print('CUDA available:', torch.cuda.is_available())\n"
            "print('PyTorch location:', torch.__file__)\n"
            "```\n"
            "\n"
            "Run a similar check inside Jupyter. If the Python version or PyTorch installation differs "
            "between your terminal and notebook, the two may be using different environments.\n"
            "\n"
            "This is not merely setup trivia. Environment mismatches are a common reason code behaves "
            "differently in a notebook than it does from a command line.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Deep learning means the computer thinks like a human\n"
            "\n"
            "> A neural network that performs a sophisticated task must possess human-like understanding.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The chapter frames deep learning more carefully: it gives us powerful algorithms for "
            "approximating complex relationships from examples. Strong task performance does not by "
            "itself establish human-like self-awareness or thought.\n"
            "\n"
            "### Misconception 2: Deep learning removes the need for all human knowledge\n"
            "\n"
            "> If the network learns features automatically, the practitioner no longer needs to make "
            "meaningful engineering decisions.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Representation learning reduces the need for some manual feature engineering, but people "
            "still make decisions about data, objectives, model architecture, evaluation, hardware, "
            "training, and deployment.\n"
            "\n"
            "### Misconception 3: A GPU is required before I can start learning PyTorch\n"
            "\n"
            "> Without a CUDA GPU, there is no point starting deep learning.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Many introductory experiments and pretrained-model workflows can run on ordinary CPUs. "
            "GPUs become especially valuable as training workloads grow.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Artificial intelligence (AI) | Broad area of building systems that perform tasks associated with intelligent behavior. |\n"
            "| Deep learning | Learning approach based on training deep neural networks from examples. |\n"
            "| Raw feature | A value taken directly from the original input data. |\n"
            "| Feature engineering | Human-designed transformation of raw data into more useful measurements. |\n"
            "| Representation learning | Learning useful internal features from data automatically. |\n"
            "| Neural network | Parameterized mathematical function used to map inputs to outputs. |\n"
            "| Loss function | Numerical measure comparing model outputs with desired targets. |\n"
            "| Training | Repeated process of adjusting model parameters to reduce the learning objective. |\n"
            "| Generalization | Ability of a trained model to perform well on relevant unseen data. |\n"
            "| Tensor | PyTorch's multidimensional numerical array. |\n"
            "| Autograd | PyTorch engine that automatically computes derivatives needed for optimization. |\n"
            "| `torch.nn` | PyTorch module containing common neural-network components and loss functions. |\n"
            "| `torch.optim` | PyTorch module providing optimizers that update parameters during training. |\n"
            "| `Dataset` | Abstraction connecting problem-specific data to samples usable by PyTorch. |\n"
            "| `DataLoader` | Utility for batching and efficiently loading samples from a dataset. |\n"
            "| Eager execution | Operations are executed as Python instructions run rather than being delayed as a separate prebuilt graph. |\n"
            "| CUDA | NVIDIA computing platform commonly used by PyTorch for GPU acceleration. |\n"
            "| Jupyter kernel | Running process that executes notebook code and keeps its state in memory. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer these without looking back:\n"
            "\n"
            "1. Why is deep learning described as learning mappings from examples rather than as human-like thinking?\n"
            "2. What is the difference between feature engineering and representation learning?\n"
            "3. What information does a loss function provide during training?\n"
            "4. Why are tensors central to PyTorch?\n"
            "5. What role does autograd play in optimization?\n"
            "6. Where do `Dataset` and `DataLoader` fit in a PyTorch project?\n"
            "7. Why is the neural network only one part of a complete deep learning system?\n"
            "8. When is a GPU especially useful?\n"
            "9. What can cause the terminal and Jupyter Notebook to use different PyTorch installations?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Deep learning learns useful representations and input-to-output mappings from examples; "
            "PyTorch gives us the tensor operations, automatic differentiation, neural-network tools, "
            "data pipeline utilities, optimization tools, and deployment path needed to turn that idea "
            "into a practical system.**\n"
        ),
        "estimated_minutes": 90,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {
                "id": "what-is-deep-learning",
                "title": "What deep learning actually is",
                "order": 1,
            },
            {
                "id": "feature-engineering-vs-representation-learning",
                "title": "From feature engineering to representation learning",
                "order": 2,
            },
            {
                "id": "training-mental-model",
                "title": "The training mental model",
                "order": 3,
            },
            {
                "id": "why-pytorch",
                "title": "Why PyTorch is a good fit for deep learning",
                "order": 4,
            },
            {
                "id": "tensors-and-autograd",
                "title": "Tensors and autograd",
                "order": 5,
            },
            {
                "id": "pytorch-project-workflow",
                "title": "The anatomy of a PyTorch deep learning project",
                "order": 6,
            },
            {
                "id": "hardware-and-software",
                "title": "Hardware and software",
                "order": 7,
            },
            {
                "id": "jupyter-and-environment-check",
                "title": "Jupyter Notebooks and environment checks",
                "order": 8,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",
            "title": "Feature Engineering or Representation Learning?",
            "lesson_code": "M01.L01",
            "section_id": "feature-engineering-vs-representation-learning",
            "placement": "after_section",
            "description": (
                "Practice distinguishing manually engineered features from representations "
                "learned automatically by a deep model."
            ),
            "instructions": (
                "For each scenario below, decide whether it mainly describes manual feature "
                "engineering or representation learning:\n"
                "1. A developer calculates the number of enclosed loops in handwritten digits "
                "before fitting a classifier.\n"
                "2. A neural network receives image pixels and learns internal filters while "
                "training on labeled examples.\n"
                "3. An engineer computes domain-specific ratios from raw measurements before "
                "training a model.\n"
                "4. A deep model receives raw examples and adjusts its intermediate features as "
                "the training loss changes.\n"
                "For each answer, explain the clue that led to your decision. Then write one "
                "sentence explaining why deep learning does not make domain knowledge irrelevant."
            ),
            "expected_output": (
                "Four classifications with short explanations, followed by one sentence describing "
                "the continuing role of domain knowledge."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "feature-engineering",
                "representation-learning",
                "conceptual-reasoning",
            ],
        },
        {
            "id": "M01.L01.EX02",
            "title": "Build the PyTorch Project Map",
            "lesson_code": "M01.L01",
            "section_id": "pytorch-project-workflow",
            "placement": "after_section",
            "description": (
                "Reconstruct the end-to-end PyTorch workflow and explain the role of each component."
            ),
            "instructions": (
                "Imagine you are building an image classifier.\n"
                "1. Put these components in a sensible order: optimizer, DataLoader, trained model, "
                "Dataset, loss function, raw data, untrained model, deployment.\n"
                "2. State which component converts problem-specific samples into PyTorch-compatible "
                "examples.\n"
                "3. State which component prepares batches for the training loop.\n"
                "4. Explain what the loss function tells the training process.\n"
                "5. Explain what autograd and the optimizer contribute.\n"
                "6. Give one reason deployment is a separate engineering stage after training."
            ),
            "expected_output": (
                "An ordered pipeline plus short explanations for Dataset, DataLoader, loss, autograd, "
                "optimizer, and deployment."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "pytorch-workflow",
                "data-pipeline",
                "training-loop",
                "deployment",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",
        "title": "Introducing Deep Learning and PyTorch — Knowledge Check",
        "lesson_code": "M01.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L01.Q01",
                "section_id": "feature-engineering-vs-representation-learning",
                "question": (
                    "Which statement best describes the major shift from traditional machine "
                    "learning toward deep learning?"
                ),
                "options": [
                    "Deep learning removes the need for data.",
                    "Deep learning learns many useful representations automatically from examples.",
                    "Traditional machine learning cannot make predictions.",
                    "Deep learning replaces optimization with handwritten rules.",
                ],
                "correct": 1,
                "explanation": (
                    "The key shift is representation learning: neural networks can learn useful "
                    "internal features from examples rather than depending entirely on manually "
                    "engineered features."
                ),
            },
            {
                "id": "M01.L01.Q02",
                "section_id": "training-mental-model",
                "question": "What is the main role of a loss function during training?",
                "options": [
                    "Store the training dataset.",
                    "Measure the mismatch between model outputs and desired targets.",
                    "Move the model from CPU to GPU.",
                    "Deploy the model to production.",
                ],
                "correct": 1,
                "explanation": (
                    "The loss converts the quality of the model's current output into a numerical "
                    "signal that the training process can try to reduce."
                ),
            },
            {
                "id": "M01.L01.Q03",
                "section_id": "tensors-and-autograd",
                "question": "Why is PyTorch autograd important for neural-network training?",
                "options": [
                    "It downloads datasets automatically.",
                    "It creates Jupyter notebooks.",
                    "It computes derivatives needed to understand how parameter changes affect the loss.",
                    "It converts every model into ONNX before training.",
                ],
                "correct": 2,
                "explanation": (
                    "Autograd tracks the relevant tensor operations and computes the derivatives "
                    "used by optimization to update learnable parameters."
                ),
            },
            {
                "id": "M01.L01.Q04",
                "section_id": "pytorch-project-workflow",
                "question": "Which pairing is correct?",
                "options": [
                    "`Dataset` defines deployment; `DataLoader` exports ONNX.",
                    "`Dataset` bridges custom data to samples; `DataLoader` organizes efficient batching/loading.",
                    "`Dataset` computes gradients; `DataLoader` updates weights.",
                    "`Dataset` is the optimizer; `DataLoader` is the loss function.",
                ],
                "correct": 1,
                "explanation": (
                    "`Dataset` represents how problem-specific data becomes usable samples, while "
                    "`DataLoader` handles iteration, batching, and efficient loading."
                ),
            },
            {
                "id": "M01.L01.Q05",
                "section_id": "hardware-and-software",
                "question": "Which hardware statement best matches the lesson?",
                "options": [
                    "A CUDA GPU is mandatory before learning PyTorch.",
                    "CPUs cannot run pretrained neural networks.",
                    "A normal computer is sufficient for many introductory tasks, while GPUs become "
                    "especially valuable for heavier training workloads.",
                    "Using a GPU removes the need for a training loop.",
                ],
                "correct": 2,
                "explanation": (
                    "Introductory work and many inference tasks can run on a CPU. GPUs become much "
                    "more important when repeated large numerical operations make training expensive."
                ),
            },
            {
                "id": "M01.L01.Q06",
                "section_id": "jupyter-and-environment-check",
                "type": "open",
                "question": (
                    "You can import PyTorch successfully from your terminal, but a Jupyter Notebook "
                    "reports a different PyTorch version. Based on this lesson, what is a likely "
                    "explanation, and what environment information would you compare?"
                ),
            },
        ],
        "passing_score": 70,
    },
}
