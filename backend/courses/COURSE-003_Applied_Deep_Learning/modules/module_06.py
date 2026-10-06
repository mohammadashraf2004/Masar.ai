"""M06.L01 — Using a Neural Network to Fit the Data.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 6.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M06.L01"
MODULE_ORDER = 6
MODULE_TITLE = "From Linear Models to Neural Networks"
MODULE_DESCRIPTION = (
    "Move from a hand-built linear model to a real neural network using PyTorch's "
    "nn module, activation functions, batching, Sequential models, and parameter inspection."
)

SOURCE_CHAPTER = 6
SOURCE_PAGES = "Chapter 6 (page range not provided in source excerpt)"

TOPIC = {
    "title": "Using a Neural Network to Fit the Data",
    "slug": "applied-deep-learning-m06-l01",
    "description": (
        "A practical introduction to neural networks in PyTorch, focusing on why "
        "nonlinear activation functions matter, how nn.Module works, how batched "
        "inputs flow through layers, and how a simple feed-forward network is trained."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 2.5,
    "skill_tags": [
        "neural-networks", "activation-functions", "nonlinearity", "pytorch-nn",
        "nn-module", "nn-linear", "batching", "nn-sequential", "parameters",
        "regression", "overfitting", "module-06",
    ],
    "prerequisite_ids": ["M05.L01"],

    "lesson": {
        "title": "Using a Neural Network to Fit the Data",
        "content": (
            "# Using a Neural Network to Fit the Data\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M06.L01  \n"
            "> **Module:** From Linear Models to Neural Networks  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, Chapter 6. "
            "This lesson is an instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "- Explain what a neural-network neuron does mathematically.\n"
            "- Explain why stacked linear layers need nonlinear activations.\n"
            "- Compare common activation functions at a practical level.\n"
            "- Explain sensitive and saturated activation regions.\n"
            "- Describe why multilayer neural networks can approximate complex functions.\n"
            "- Use PyTorch's `nn.Module`, `nn.Parameter`, `nn.Linear`, and `nn.Sequential`.\n"
            "- Shape data correctly for batched neural-network input.\n"
            "- Inspect model parameters and gradients.\n"
            "- Train a small neural network with the same optimization loop used for a linear model.\n"
            "- Explain why extra model capacity can lead to overfitting.\n\n"
            "---\n\n"

            "## 1. From a linear model to a neural network\n\n"
            "In the previous lesson, our model was simple:\n\n"
            "```text\n"
            "prediction = weight × input + bias\n"
            "```\n\n"
            "But the surrounding learning machinery was already general: forward pass, loss, "
            "backpropagation, gradients, optimizer, training data, and validation data.\n\n"
            "That means we can replace the simple model with a more expressive differentiable model "
            "without replacing the whole learning process.\n\n"
            '{{image:same-training-loop-different-model}}'
            '\n\n'
            "This is the first major transition from machine-learning mechanics into deep learning.\n\n"
            "---\n\n"

            "## 2. The artificial neuron\n\n"
            "A practical artificial neuron is a mathematical building block. It performs:\n\n"
            "1. a linear or affine transformation,\n"
            "2. a nonlinear activation.\n\n"
            "```text\n"
            "output = f(weight × input + bias)\n"
            "```\n\n"
            "where `f` is an activation function.\n\n"
            "[[IMAGE_NEEDED: Anatomy of an artificial neuron | Input x enters a multiply-by-weight step, "
            "bias b is added, and the result passes through activation f to produce output | Learner "
            "should notice the linear transformation followed by a fixed nonlinear function]]\n\n"
            "For a layer, inputs and outputs are vectors, weights form a matrix, and biases form a vector. "
            "This lets many neurons be computed efficiently with linear algebra.\n\n"
            "---\n\n"

            "## 3. Composing layers\n\n"
            "A multilayer network feeds one layer's output into the next:\n\n"
            "```text\n"
            "x1 = f(W1 x + b1)\n"
            "x2 = f(W2 x1 + b2)\n"
            "...\n"
            "output = final_layer(...)\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Simple multilayer neural network | Input vector, two hidden layers, and "
            "an output layer connected left to right | Learner should notice that intermediate "
            "representations are passed layer to layer]]\n\n"
            "If we stack only affine linear transformations, however, the composition is still equivalent "
            "to one affine transformation. So depth alone is not enough. We need **nonlinearity**.\n\n"
            "---\n\n"

            "## 4. Why activation functions matter\n\n"
            "A linear function has one overall slope. It cannot bend differently in different regions "
            "of its input space. A nonlinear activation changes that.\n\n"
            "By combining linear transformations with nonlinear activations, different units can "
            "respond differently to different input regions. Stacking such units lets the network "
            "approximate much more complicated relationships.\n\n"
            "### Example: `tanh`\n\n"
            "`tanh` maps values into approximately `[-1, 1]`:\n\n"
            "```python\n"
            "import math\n"
            "print(math.tanh(-2.2))\n"
            "print(math.tanh(0.1))\n"
            "print(math.tanh(2.5))\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Tanh sensitive and saturated regions | A tanh curve with the center marked "
            "as sensitive and the flat tails marked as saturated | Learner should notice that changes "
            "near zero affect output more strongly than changes in the tails]]\n\n"
            "---\n\n"

            "## 5. Common activation functions\n\n"
            "The chapter introduces several useful activations:\n\n"
            "- **Tanh** — smooth, nonlinear, bounded approximately in `[-1, 1]`.\n"
            "- **Sigmoid** — smooth and approximately in `[0, 1]`; useful when that output range matters.\n"
            "- **ReLU** — conceptually `max(0, x)`; simple and widely used.\n"
            "- **LeakyReLU** — like ReLU but keeps a small negative-side slope.\n"
            "- **Hardtanh** — explicitly clamps output to a bounded range.\n\n"
            "[[IMAGE_NEEDED: Activation function comparison | A grid of Tanh, Sigmoid, ReLU, "
            "LeakyReLU, and Hardtanh curves on common axes | Learner should notice differences in "
            "range, slope, and saturated/flat regions]]\n\n"
            "The most important broad requirements from this chapter are **nonlinearity** and the "
            "ability to propagate useful derivatives for gradient-based learning.\n\n"
            "---\n\n"

            "## 6. Sensitive and saturated regions\n\n"
            "A **sensitive region** is where small input changes produce meaningful output changes. "
            "That usually gives backpropagation a useful gradient.\n\n"
            "A **saturated region** is nearly flat. Small input changes produce little output change, "
            "so the derivative can be close to zero and less learning signal flows backward.\n\n"
            "Different neurons can operate in different response regions for the same input, allowing "
            "different subsets of the network to specialize.\n\n"
            "{{exercise:M06.L01.EX01}}\n\n"
            "---\n\n"

            "## 7. Why simple neurons can form complex functions\n\n"
            "Individual activated neurons are simple, but their weights and biases can shift and scale "
            "where they respond. Combining many such neurons produces richer curves, and composing those "
            "combinations through more layers produces even richer behavior.\n\n"
            "[[IMAGE_NEEDED: Combining nonlinear neurons | Several shifted and scaled activation curves "
            "shown individually and then combined into a more complicated nonlinear curve | Learner "
            "should notice that simple units can compose into functions much richer than any one unit]]\n\n"
            "This provides intuition for why neural networks are flexible function approximators. "
            "Instead of manually choosing a quadratic or piecewise polynomial, we choose a network "
            "family and learn its parameters from examples.\n\n"
            "The trade-off is that individual weights usually lose the direct interpretation that "
            "parameters in a simple scientific model may have.\n\n"
            "---\n\n"

            "## 8. The PyTorch `nn` module\n\n"
            "`torch.nn` contains standard neural-network building blocks.\n\n"
            "The central abstraction is `nn.Module`. A module may contain:\n\n"
            "- learnable `nn.Parameter` tensors,\n"
            "- other modules as submodules,\n"
            "- a forward computation describing how inputs become outputs.\n\n"
            "Registered submodules are tracked recursively, so their parameters can be discovered by "
            "the parent model. When storing collections of modules, PyTorch provides `nn.ModuleList` "
            "and `nn.ModuleDict` for proper registration.\n\n"
            "---\n\n"

            "## 9. Call the module, not `.forward()` directly\n\n"
            "Normal user code should execute a module like this:\n\n"
            "```python\n"
            "y = model(x)\n"
            "```\n\n"
            "The module's call machinery then invokes `forward()` internally and can also run hooks "
            "or other framework logic.\n\n"
            "Avoid directly writing:\n\n"
            "```python\n"
            "y = model.forward(x)\n"
            "```\n\n"
            "because that bypasses the normal module call path.\n\n"
            "---\n\n"

            "## 10. Replace the handwritten linear model with `nn.Linear`\n\n"
            "PyTorch already provides the affine model from the previous chapter:\n\n"
            "```python\n"
            "import torch.nn as nn\n"
            "linear_model = nn.Linear(1, 1)\n"
            "```\n\n"
            "The arguments mean one input feature and one output feature.\n\n"
            "The module owns trainable parameters:\n\n"
            "```python\n"
            "print(linear_model.weight)\n"
            "print(linear_model.bias)\n"
            "```\n\n"
            "If each sample had two input features and one output, we could use:\n\n"
            "```python\n"
            "nn.Linear(2, 1)\n"
            "```\n\n"
            "---\n\n"

            "## 11. Batching inputs\n\n"
            "Neural-network modules are designed to process multiple samples together. For a linear "
            "layer, the input commonly has shape:\n\n"
            "```text\n"
            "B × N_in\n"
            "```\n\n"
            "where `B` is batch size and `N_in` is the number of input features.\n\n"
            "For 10 one-feature samples:\n\n"
            "```python\n"
            "x = torch.ones(10, 1)\n"
            "output = linear_model(x)\n"
            "```\n\n"
            "The output shape becomes `B × N_out`.\n\n"
            "[[IMAGE_NEEDED: Batched neural-network inputs and outputs | Several samples enter the "
            "same model in parallel, labeled B×N_in, with B×N_out at the output | Learner should "
            "notice that dimension 0 carries independent samples through the same learned function]]\n\n"
            "The thermometer vectors were previously shaped `(B,)`. To make the feature dimension "
            "explicit for `nn.Linear(1,1)`, use:\n\n"
            "```python\n"
            "t_c = torch.tensor(t_c).unsqueeze(1)\n"
            "t_u = torch.tensor(t_u).unsqueeze(1)\n"
            "```\n\n"
            "For 11 samples, the shape becomes `(11, 1)`.\n\n"
            "{{exercise:M06.L01.EX02}}\n\n"
            "---\n\n"

            "## 12. Let the module own its parameters\n\n"
            "Instead of manually creating parameter tensors, we ask the model for them:\n\n"
            "```python\n"
            "linear_model = nn.Linear(1, 1)\n"
            "optimizer = torch.optim.SGD(\n"
            "    linear_model.parameters(),\n"
            "    lr=1e-2,\n"
            ")\n"
            "```\n\n"
            "`model.parameters()` recursively returns registered learnable parameters. After "
            "`loss.backward()`, those parameter tensors contain gradients. Then `optimizer.step()` "
            "updates them.\n\n"
            "The math is the same as before; `nn.Module` is organizing it for us.\n\n"
            "---\n\n"

            "## 13. Use `nn.MSELoss`\n\n"
            "Our handwritten mean squared error:\n\n"
            "```python\n"
            "def loss_fn(t_p, t_c):\n"
            "    return ((t_p - t_c) ** 2).mean()\n"
            "```\n\n"
            "can be replaced by:\n\n"
            "```python\n"
            "loss_fn = nn.MSELoss()\n"
            "loss = loss_fn(predictions, targets)\n"
            "```\n\n"
            "`nn.MSELoss` is itself an `nn.Module`, giving PyTorch a consistent interface across "
            "models, layers, activations, and many loss functions.\n\n"
            "---\n\n"

            "## 14. A reusable training loop\n\n"
            "Once the model owns its parameters, the training loop no longer needs to know the individual "
            "weights and biases:\n\n"
            "```python\n"
            "def training_loop(n_epochs, optimizer, model, loss_fn,\n"
            "                  t_u_train, t_u_val, t_c_train, t_c_val):\n"
            "    for epoch in range(1, n_epochs + 1):\n"
            "        t_p_train = model(t_u_train)\n"
            "        loss_train = loss_fn(t_p_train, t_c_train)\n\n"
            "        t_p_val = model(t_u_val)\n"
            "        loss_val = loss_fn(t_p_val, t_c_val)\n\n"
            "        optimizer.zero_grad()\n"
            "        loss_train.backward()\n"
            "        optimizer.step()\n\n"
            "    return model\n"
            "```\n\n"
            "The exact architecture is no longer hardcoded into the loop. This is what makes the same "
            "optimization structure reusable across many differentiable models.\n\n"
            "---\n\n"

            "## 15. Build the first actual neural network\n\n"
            "The chapter's simplest neural network uses:\n\n"
            "```text\n"
            "Linear -> Tanh -> Linear\n"
            "```\n\n"
            "In PyTorch:\n\n"
            "```python\n"
            "seq_model = nn.Sequential(\n"
            "    nn.Linear(1, 13),\n"
            "    nn.Tanh(),\n"
            "    nn.Linear(13, 1),\n"
            ")\n"
            "```\n\n"
            "The first layer expands one input feature into 13 hidden features. `Tanh` introduces "
            "nonlinearity. The final linear layer combines those 13 values into one output.\n\n"
            "[[IMAGE_NEEDED: Linear-Tanh-Linear neural network | Two depictions of the same network: "
            "a node-and-arrow view and a block view labeled Linear(1,13), Tanh, Linear(13,1) | Learner "
            "should notice that both diagrams represent the same computation at different abstraction levels]]\n\n"
            "The value `13` is a design choice that affects model capacity; it is not dictated by the "
            "thermometer problem itself.\n\n"
            "---\n\n"

            "## 16. `nn.Sequential`\n\n"
            "`nn.Sequential` is ideal when computation is simply one module after another:\n\n"
            "```text\n"
            "input -> module A -> module B -> module C -> output\n"
            "```\n\n"
            "We can also name the modules:\n\n"
            "```python\n"
            "from collections import OrderedDict\n\n"
            "seq_model = nn.Sequential(OrderedDict([\n"
            "    ('hidden_linear', nn.Linear(1, 8)),\n"
            "    ('hidden_activation', nn.Tanh()),\n"
            "    ('output_linear', nn.Linear(8, 1)),\n"
            "]))\n"
            "```\n\n"
            "Then a component can be accessed directly:\n\n"
            "```python\n"
            "print(seq_model.output_linear.bias)\n"
            "```\n\n"
            "More complicated data flow eventually requires custom subclasses of `nn.Module`, but "
            "`Sequential` is perfect for this simple feed-forward chain.\n\n"
            "---\n\n"

            "## 17. Inspect parameters and gradients\n\n"
            "For:\n\n"
            "```text\n"
            "Linear(1,13) -> Tanh -> Linear(13,1)\n"
            "```\n\n"
            "the parameter shapes are conceptually:\n\n"
            "```text\n"
            "first weights:  [13, 1]\n"
            "first bias:     [13]\n"
            "second weights: [1, 13]\n"
            "second bias:    [1]\n"
            "```\n\n"
            "Inspect them with:\n\n"
            "```python\n"
            "for name, param in seq_model.named_parameters():\n"
            "    print(name, param.shape)\n"
            "```\n\n"
            "`nn.Tanh()` does not appear because it has no trainable parameters.\n\n"
            "You can inspect gradients too:\n\n"
            "```python\n"
            "print(seq_model.hidden_linear.weight.grad)\n"
            "```\n\n"
            "This directly connects the convenient module API with the gradient mechanics learned in "
            "the previous lesson.\n\n"
            "{{exercise:M06.L01.EX03}}\n\n"
            "---\n\n"

            "## 18. Train the neural network\n\n"
            "The network uses the same training recipe:\n\n"
            "```python\n"
            "optimizer = torch.optim.SGD(seq_model.parameters(), lr=1e-3)\n\n"
            "training_loop(\n"
            "    n_epochs=5000,\n"
            "    optimizer=optimizer,\n"
            "    model=seq_model,\n"
            "    loss_fn=nn.MSELoss(),\n"
            "    t_u_train=t_un_train,\n"
            "    t_u_val=t_un_val,\n"
            "    t_c_train=t_c_train,\n"
            "    t_c_val=t_c_val,\n"
            ")\n"
            "```\n\n"
            "The optimizer simply has more parameters to update. The logic remains:\n\n"
            "```text\n"
            "forward -> loss -> zero gradients -> backward -> optimizer step\n"
            "```\n\n"
            "---\n\n"

            "## 19. Compare the neural network with the linear model\n\n"
            "The thermometer problem is fundamentally linear, so a neural network is more flexible "
            "than necessary.\n\n"
            "The chapter shows that the trained network can curve toward noisy measurements instead of "
            "remaining perfectly linear.\n\n"
            "[[IMAGE_NEEDED: Linear fit versus neural-network fit | Thermometer scatter points with a "
            "straight linear fit and a slightly curved neural-network fit following some noisy samples | "
            "Learner should notice that greater capacity can fit noise even when the true process is simple]]\n\n"
            "This is a practical demonstration of **model capacity** and **overfitting**.\n\n"
            "More capacity means a model can represent richer functions, but richer is not automatically "
            "better. Generalization on unseen data remains the important criterion.\n\n"
            "{{exercise:M06.L01.EX04}}\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: More linear layers automatically create a nonlinear model\n\n"
            "A stack of affine transformations without nonlinear activations can still collapse into one "
            "affine transformation. Activation functions provide the essential nonlinearity.\n\n"
            "### Misconception 2: Activation layers have trainable weights\n\n"
            "`nn.Tanh()` is a fixed mathematical function. It affects both forward computation and "
            "backpropagation but owns no learnable weights or biases.\n\n"
            "### Misconception 3: Calling `.forward()` directly is normal user code\n\n"
            "Call `model(x)` so PyTorch's full module machinery is preserved.\n\n"
            "### Misconception 4: Lower training loss always means the more complex model is better\n\n"
            "Extra capacity can fit noise. Validation behavior is needed to judge generalization.\n\n"
            "### Misconception 5: Every hidden parameter has an obvious human meaning\n\n"
            "Neural-network parameters generally work collectively; different internal parameter "
            "settings can produce similarly good outputs.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Neuron | Affine transformation followed by an activation function. |\n"
            "| Layer | Collection of neurons operating together. |\n"
            "| Activation function | Fixed nonlinear transform applied to layer output. |\n"
            "| Nonlinearity | Property that allows a network to go beyond one affine mapping. |\n"
            "| Sensitive region | Activation region with meaningful output response to input change. |\n"
            "| Saturated region | Nearly flat activation region with small derivative. |\n"
            "| Hidden layer | Intermediate layer not directly exposed as final output. |\n"
            "| Model capacity | Flexibility of a model to represent different functions. |\n"
            "| `nn.Module` | Base abstraction for PyTorch neural-network components. |\n"
            "| `nn.Parameter` | Registered learnable tensor owned by a module. |\n"
            "| `nn.Linear` | Affine linear layer. |\n"
            "| Batch | Group of samples processed together. |\n"
            "| `nn.MSELoss` | PyTorch mean squared error loss module. |\n"
            "| `nn.Sequential` | Container that applies modules in order. |\n"
            "| `.parameters()` | Iterator over registered learnable parameters. |\n"
            "| `.named_parameters()` | Iterator yielding parameter names and tensors. |\n"
            "| Overfitting | Fitting training-specific details that fail to generalize. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "1. What changes when the linear model is replaced by a neural network?\n"
            "2. What two operations make up a basic neuron?\n"
            "3. Why are activation functions necessary between linear layers?\n"
            "4. What is a saturated activation region?\n"
            "5. Why can saturation weaken gradient flow?\n"
            "6. What does `nn.Module` organize?\n"
            "7. What is an `nn.Parameter`?\n"
            "8. Why call `model(x)` instead of `model.forward(x)`?\n"
            "9. What do the arguments of `nn.Linear(1, 13)` mean?\n"
            "10. What shape should 11 one-feature samples have?\n"
            "11. Why is batching useful?\n"
            "12. Why can the optimizer simply receive `model.parameters()`?\n"
            "13. Why does `nn.Tanh()` have no entries in `.named_parameters()`?\n"
            "14. What does `nn.Sequential` do?\n"
            "15. Why can the same training loop work for a linear model and a multilayer network?\n"
            "16. Why can the neural network overfit the thermometer data more easily?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**A neural network is built by composing parameterized linear transformations with fixed "
            "nonlinear activations. PyTorch's `nn.Module` system organizes those layers and their "
            "parameters, while the same autograd and optimizer mechanics learned for a simple linear "
            "model scale naturally to multilayer neural networks.**\n"
        ),
        "estimated_minutes": 150,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "from-linear-to-neural", "title": "From a linear model to a neural network", "order": 1},
            {"id": "artificial-neuron", "title": "The artificial neuron", "order": 2},
            {"id": "multilayer-composition", "title": "Composing layers", "order": 3},
            {"id": "why-activation-functions", "title": "Why activation functions matter", "order": 4},
            {"id": "activation-functions", "title": "Common activation functions", "order": 5},
            {"id": "sensitive-and-saturated", "title": "Sensitive and saturated regions", "order": 6},
            {"id": "universal-approximation-intuition", "title": "Why simple neurons form complex functions", "order": 7},
            {"id": "nn-module", "title": "The PyTorch nn module", "order": 8},
            {"id": "callable-module", "title": "Calling modules correctly", "order": 9},
            {"id": "nn-linear", "title": "Using nn.Linear", "order": 10},
            {"id": "batching", "title": "Batching inputs", "order": 11},
            {"id": "module-parameters", "title": "Module-owned parameters", "order": 12},
            {"id": "nn-loss", "title": "Using nn.MSELoss", "order": 13},
            {"id": "generic-training-loop", "title": "A reusable training loop", "order": 14},
            {"id": "first-neural-network", "title": "Building the first neural network", "order": 15},
            {"id": "sequential", "title": "Using nn.Sequential", "order": 16},
            {"id": "inspect-parameters", "title": "Inspecting parameters and gradients", "order": 17},
            {"id": "train-neural-network", "title": "Training the neural network", "order": 18},
            {"id": "linear-vs-neural", "title": "Linear versus neural-network fit", "order": 19},
        ],
    },

    "exercises": [
        {
            "id": "M06.L01.EX01",
            "title": "Explore Activation Functions",
            "lesson_code": "M06.L01",
            "section_id": "sensitive-and-saturated",
            "placement": "after_section",
            "description": "Build intuition for activation response and saturation.",
            "instructions": (
                "Create `x = torch.linspace(-5, 5, 21)` and compute `torch.tanh(x)`, "
                "`torch.sigmoid(x)`, and `torch.relu(x)`. Print the values side by side. "
                "Identify saturated regions for tanh and sigmoid, describe ReLU on negative and "
                "positive inputs, and explain why nonlinearity is needed between linear layers."
            ),
            "expected_output": "PyTorch code plus a concise comparison of the three activations.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["activation-functions", "tanh", "sigmoid", "relu", "nonlinearity"],
        },
        {
            "id": "M06.L01.EX02",
            "title": "Reason About Batch Shapes",
            "lesson_code": "M06.L01",
            "section_id": "batching",
            "placement": "after_section",
            "description": "Practice matching tensor shapes to nn.Linear.",
            "instructions": (
                "Predict and verify input/output shapes for: `nn.Linear(1,1)` with 32 samples, "
                "`nn.Linear(5,2)` with 64 samples, and `nn.Linear(20,10)` with one batched sample. "
                "Explain why `(32,1)` is clearer and correct for 32 one-feature samples."
            ),
            "expected_output": "Shape predictions, verification code, and explanations.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["batching", "shape-reasoning", "nn-linear"],
        },
        {
            "id": "M06.L01.EX03",
            "title": "Inspect a Sequential Network",
            "lesson_code": "M06.L01",
            "section_id": "inspect-parameters",
            "placement": "after_section",
            "description": "Connect architecture to parameter tensors.",
            "instructions": (
                "Build `nn.Sequential(nn.Linear(2,4), nn.Tanh(), nn.Linear(4,1))`. "
                "Print the model, list names and shapes using `.named_parameters()`, count total "
                "trainable scalar parameters, pass a batch of 8 samples with 2 features, verify "
                "the output shape, and explain why Tanh has no trainable parameters."
            ),
            "expected_output": "Model code, parameter table/count, output shape, and explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["nn-sequential", "parameters", "parameter-counting", "model-inspection"],
        },
        {
            "id": "M06.L01.EX04",
            "title": "Capacity and Overfitting Experiment",
            "lesson_code": "M06.L01",
            "section_id": "linear-vs-neural",
            "placement": "after_section",
            "description": "Explore how hidden width changes capacity and generalization.",
            "instructions": (
                "Train three models on the thermometer task: `nn.Linear(1,1)`, "
                "`Linear(1,2)->Tanh->Linear(2,1)`, and `Linear(1,32)->Tanh->Linear(32,1)`. "
                "Record final training and validation losses, inspect predictions over a smooth "
                "temperature range, and explain whether greater capacity improved validation performance "
                "or mainly made the fit more nonlinear."
            ),
            "expected_output": "Three trained models, loss comparison, prediction comparison, and interpretation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["model-capacity", "overfitting", "validation", "hidden-layers"],
        },
    ],

    "quiz": {
        "id": "M06.L01.QZ01",
        "title": "Using a Neural Network to Fit the Data — Knowledge Check",
        "lesson_code": "M06.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M06.L01.Q01",
                "section_id": "artificial-neuron",
                "question": "Which expression best represents a basic artificial neuron?",
                "options": ["`f(w * x + b)`", "`x / epoch`", "`loss + optimizer`", "`validation - training`"],
                "correct": 0,
                "explanation": "A basic neuron applies an affine transformation and then an activation.",
            },
            {
                "id": "M06.L01.Q02",
                "section_id": "why-activation-functions",
                "question": "Why are nonlinear activations important between linear layers?",
                "options": [
                    "Without them, stacked linear layers still reduce to an overall affine transformation.",
                    "They create training samples automatically.",
                    "They remove all model parameters.",
                    "They guarantee zero validation loss.",
                ],
                "correct": 0,
                "explanation": "Nonlinearity allows the network to represent genuinely nonlinear mappings.",
            },
            {
                "id": "M06.L01.Q03",
                "section_id": "sensitive-and-saturated",
                "question": "What characterizes a saturated activation region?",
                "options": [
                    "Output changes very little when input changes.",
                    "The layer contains more parameters.",
                    "The batch dimension disappears.",
                    "Loss is always zero.",
                ],
                "correct": 0,
                "explanation": "Saturated regions are relatively flat and commonly have small derivatives.",
            },
            {
                "id": "M06.L01.Q04",
                "section_id": "nn-module",
                "question": "What is an `nn.Parameter`?",
                "options": [
                    "A tensor registered by an `nn.Module` as a learnable parameter.",
                    "A validation dataset.",
                    "A fixed activation function.",
                    "An optimizer class.",
                ],
                "correct": 0,
                "explanation": "Parameters are registered trainable tensors tracked by a module.",
            },
            {
                "id": "M06.L01.Q05",
                "section_id": "callable-module",
                "question": "How should user code normally execute a module?",
                "options": ["`model(x)`", "`model.forward(x)` only", "`model.backward(x)`", "`model.parameters(x)`"],
                "correct": 0,
                "explanation": "Calling the module itself preserves PyTorch's full module call machinery.",
            },
            {
                "id": "M06.L01.Q06",
                "section_id": "nn-linear",
                "question": "What does `nn.Linear(5, 2)` mean?",
                "options": [
                    "Five input features and two output features.",
                    "Five batches and two epochs.",
                    "Five hidden layers and two optimizers.",
                    "A five-by-two validation split.",
                ],
                "correct": 0,
                "explanation": "The arguments specify input and output feature dimensions.",
            },
            {
                "id": "M06.L01.Q07",
                "section_id": "batching",
                "question": "What input shape represents 32 samples with 5 features for `nn.Linear(5,2)`?",
                "options": ["`(32, 5)`", "`(5, 32)`", "`(32,)`", "`(5, 2)`"],
                "correct": 0,
                "explanation": "Dimension 0 is the batch; the final dimension contains the five features.",
            },
            {
                "id": "M06.L01.Q08",
                "section_id": "module-parameters",
                "question": "Why is `model.parameters()` useful for an optimizer?",
                "options": [
                    "It provides the registered learnable tensors to update.",
                    "It returns the training dataset.",
                    "It selects the validation loss.",
                    "It disables autograd.",
                ],
                "correct": 0,
                "explanation": "Optimizers need references to learnable parameters and their gradients.",
            },
            {
                "id": "M06.L01.Q09",
                "section_id": "first-neural-network",
                "question": "What does `13` represent in `Linear(1,13) -> Tanh -> Linear(13,1)`?",
                "options": [
                    "The hidden representation has 13 features.",
                    "The model must train for 13 epochs.",
                    "The batch size is always 13.",
                    "The learning rate is 13.",
                ],
                "correct": 0,
                "explanation": "The first layer expands one input feature into 13 hidden features.",
            },
            {
                "id": "M06.L01.Q10",
                "section_id": "inspect-parameters",
                "question": "Why does `nn.Tanh()` not appear in `.named_parameters()`?",
                "options": [
                    "It is a fixed activation with no learnable parameter tensors.",
                    "It is not part of the forward pass.",
                    "PyTorch ignores activation functions.",
                    "It only runs during validation.",
                ],
                "correct": 0,
                "explanation": "Tanh transforms values but owns no trainable weights or biases.",
            },
            {
                "id": "M06.L01.Q11",
                "section_id": "linear-vs-neural",
                "question": "Why can the neural network overfit the thermometer data more easily?",
                "options": [
                    "It has greater capacity and can bend toward noisy samples.",
                    "It cannot use gradients.",
                    "It has no parameters.",
                    "It always receives more data.",
                ],
                "correct": 0,
                "explanation": "The hidden units and nonlinear activation allow a richer family of curves.",
            },
            {
                "id": "M06.L01.Q12",
                "section_id": "generic-training-loop",
                "type": "open",
                "question": (
                    "Explain why the same high-level training loop can train both `nn.Linear(1,1)` "
                    "and `Linear -> Tanh -> Linear` even though they have different numbers of parameters."
                ),
            },
        ],
        "passing_score": 70,
    },
}
