"""M08.L01 — Using Convolutions to Generalize.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 8.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M08.L01"
MODULE_ORDER = 8
MODULE_TITLE = "Convolutional Neural Networks"
MODULE_DESCRIPTION = (
    "Learn why convolution is a better architectural fit for images than fully connected "
    "layers, then build, train, regularize, save, and scale a convolutional neural network "
    "using PyTorch."
)

SOURCE_CHAPTER = 8
SOURCE_PAGES = "Chapter 8 (page range not provided in source excerpt)"


TOPIC = {
    "title": "Using Convolutions to Generalize",
    "slug": "applied-deep-learning-m08-l01",
    "description": (
        "A complete introduction to convolutional neural networks in PyTorch: locality, "
        "translation-aware feature reuse, kernels, padding, pooling, receptive fields, "
        "custom nn.Module models, functional APIs, GPU training, regularization, "
        "batch normalization, residual connections, and architecture design."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 4.0,
    "skill_tags": [
        "computer-vision",
        "convolution",
        "cnn",
        "conv2d",
        "padding",
        "feature-maps",
        "pooling",
        "receptive-field",
        "custom-nn-module",
        "functional-api",
        "gpu-training",
        "state-dict",
        "regularization",
        "weight-decay",
        "dropout",
        "batch-normalization",
        "residual-networks",
        "skip-connections",
        "model-capacity",
        "module-08",
    ],
    "prerequisite_ids": ["M07.L01"],

    "lesson": {
        "title": "Using Convolutions to Generalize",
        "content": (
            "# Using Convolutions to Generalize\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M08.L01  \n"
            "> **Module:** Convolutional Neural Networks  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, Chapter 8. "
            "This lesson is an instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "- Explain why fully connected image classifiers use too many parameters and ignore locality.\n"
            "- Explain convolution as a small learned kernel reused across image locations.\n"
            "- Describe how convolution provides local feature extraction and position-independent feature reuse.\n"
            "- Predict `Conv2d` weight and output tensor shapes.\n"
            "- Explain padding and why it is useful.\n"
            "- Describe handcrafted blur and edge-detection kernels and connect them to learned filters.\n"
            "- Explain pooling, downsampling, and receptive fields.\n"
            "- Build a complete convolutional classifier for CIFAR-sized images.\n"
            "- Implement a custom model by subclassing `nn.Module`.\n"
            "- Explain automatic registration of submodules and parameters.\n"
            "- Distinguish PyTorch's module-based and functional APIs.\n"
            "- Train and validate a CNN using minibatches.\n"
            "- Save and restore model parameters with `state_dict()`.\n"
            "- Move models and minibatches consistently between CPU and GPU.\n"
            "- Explain width and depth as two dimensions of network capacity.\n"
            "- Explain L2 regularization/weight decay, dropout, and batch normalization.\n"
            "- Use `model.train()` and `model.eval()` correctly for stateful training-time behavior.\n"
            "- Explain vanishing gradients and how residual skip connections help deep networks train.\n"
            "- Build reusable residual blocks programmatically.\n"
            "- Recognize overgeneralization as a deployment problem for closed-set classifiers.\n\n"
            "---\n\n"

            "## 1. Why the fully connected image model was the wrong architectural fit\n\n"
            "Chapter 7 proved that a fully connected network *can* classify flattened images. But it also "
            "revealed two serious problems:\n\n"
            "1. the first dense layer requires enormous numbers of parameters,\n"
            "2. flattening removes the image's explicit spatial organization.\n\n"
            "For vision, nearby pixels usually matter together. A small edge, corner, texture, or color "
            "transition is a **local pattern**. A dense layer does not encode that prior knowledge; every "
            "hidden unit independently learns a connection to every pixel.\n\n"
            "We also want a feature detector to be useful wherever the feature appears. An airplane wing "
            "should still look like a wing if it moves a few pixels across the image.\n\n"
            "Convolution addresses these needs through:\n\n"
            "- **local connectivity**,\n"
            "- **weight sharing across spatial locations**,\n"
            "- dramatically fewer parameters than equivalent dense image processing.\n\n"
            "[[IMAGE_NEEDED: Fully connected image processing versus convolution | Left side shows a flattened "
            "image densely connected to hidden units; right side shows a small kernel applied locally at many "
            "positions | Learner should notice that convolution reuses the same small set of weights instead "
            "of learning independent weights for every pixel-location relationship]]\n\n"
            "---\n\n"

            "## 2. What a convolution does\n\n"
            "A 2D convolution uses a small matrix of learnable weights called a **kernel** or **filter**.\n\n"
            "For a `3 × 3` kernel, the operation examines one local `3 × 3` neighborhood of the input, "
            "multiplies corresponding values by kernel weights, sums the products, and produces one output value.\n\n"
            "Then the same kernel is moved to another spatial position and used again.\n\n"
            "For a one-channel image, one output location conceptually looks like:\n\n"
            "```text\n"
            "output =\n"
            "    i00*w00 + i01*w01 + i02*w02\n"
            "  + i10*w10 + i11*w11 + i12*w12\n"
            "  + i20*w20 + i21*w21 + i22*w22\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Sliding 3x3 convolution kernel | A small 3×3 kernel overlaying one neighborhood "
            "of an image, with corresponding cells multiplied and summed to produce one output pixel, then "
            "the kernel shown sliding to the next position | Learner should notice that the identical kernel "
            "weights are reused at every location]]\n\n"
            "For RGB input, one filter includes weights for all three input channels. A `3 × 3` filter over "
            "RGB therefore contains `3 × 3 × 3 = 27` learned weights, plus an optional bias for the output channel.\n\n"
            "The important idea is **weight sharing**: one learned pattern detector is reused throughout the image.\n\n"
            "---\n\n"

            "## 3. Locality, weight sharing, and translation-aware feature detection\n\n"
            "A dense layer can theoretically reproduce a local operation, but it would need a huge sparse "
            "matrix whose weights are carefully tied together across positions.\n\n"
            "Convolution gives us that structure directly.\n\n"
            "### Locality\n\n"
            "An output value depends only on a nearby neighborhood rather than every pixel in the image.\n\n"
            "### Shared detectors\n\n"
            "The same filter is applied everywhere, so if the filter learns to respond to a vertical edge, "
            "that detector can fire near the left edge, center, or right side of the image.\n\n"
            "### Parameter efficiency\n\n"
            "The number of convolution weights depends mainly on:\n\n"
            "```text\n"
            "output channels × input channels × kernel height × kernel width\n"
            "```\n\n"
            "It does **not** grow directly with image width and height in the way the first dense layer does.\n\n"
            "This architectural prior is why convolution often generalizes better on images with fewer parameters.\n\n"
            "---\n\n"

            "## 4. `nn.Conv2d` in PyTorch\n\n"
            "For RGB CIFAR images, a first convolutional layer might be:\n\n"
            "```python\n"
            "import torch.nn as nn\n\n"
            "conv = nn.Conv2d(\n"
            "    in_channels=3,\n"
            "    out_channels=16,\n"
            "    kernel_size=3,\n"
            ")\n"
            "```\n\n"
            "This means:\n\n"
            "- the input has 3 channels,\n"
            "- the layer learns 16 different output feature channels,\n"
            "- every filter uses a `3 × 3` spatial neighborhood.\n\n"
            "The weight shape is:\n\n"
            "```text\n"
            "[16, 3, 3, 3]\n"
            "```\n\n"
            "or:\n\n"
            "```text\n"
            "[out_channels, in_channels, kernel_height, kernel_width]\n"
            "```\n\n"
            "The bias shape is:\n\n"
            "```text\n"
            "[16]\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Conv2d channel transformation | Three RGB input channels feeding several 3×3 "
            "kernels and producing 16 output feature maps | Learner should notice that one output channel "
            "combines information from all input channels using its own learned kernel bank]]\n\n"
            "### Batch shape\n\n"
            "`nn.Conv2d` expects:\n\n"
            "```text\n"
            "B × C × H × W\n"
            "```\n\n"
            "For one image:\n\n"
            "```python\n"
            "output = conv(img.unsqueeze(0))\n"
            "```\n\n"
            "Without padding, a `32 × 32` image processed with a `3 × 3` kernel and stride 1 becomes `30 × 30` spatially.\n\n"
            "{{exercise:M08.L01.EX01}}\n\n"
            "---\n\n"

            "## 5. Padding the image boundary\n\n"
            "Why did `32 × 32` become `30 × 30`?\n\n"
            "Near a border, a `3 × 3` kernel cannot be centered on a pixel unless values exist outside the image. "
            "With no padding, PyTorch only uses kernel positions that fit completely inside the input.\n\n"
            "For stride 1 and no dilation, a useful output-size formula for one spatial dimension is:\n\n"
            "```text\n"
            "output = floor((input + 2*padding - kernel_size) / stride) + 1\n"
            "```\n\n"
            "For `input=32`, `kernel=3`, `padding=0`, `stride=1`:\n\n"
            "```text\n"
            "output = 30\n"
            "```\n\n"
            "Using one layer of zero padding around the image:\n\n"
            "```python\n"
            "conv = nn.Conv2d(3, 16, kernel_size=3, padding=1)\n"
            "```\n\n"
            "preserves the `32 × 32` spatial size.\n\n"
            "[[IMAGE_NEEDED: Zero padding around a 2D input | A small image grid surrounded by one border "
            "of zero-valued ghost pixels, with a 3×3 kernel centered over an original corner pixel | Learner "
            "should notice that padding lets the kernel produce outputs at boundary locations]]\n\n"
            "Padding is especially useful when later architecture components need compatible tensor sizes, "
            "such as residual additions or encoder-decoder skip connections.\n\n"
            "---\n\n"

            "## 6. Handcrafted kernels reveal what convolution can learn\n\n"
            "Although CNN kernels are normally learned through backpropagation, assigning weights manually "
            "helps us understand their behavior.\n\n"
            "### Blur / local averaging\n\n"
            "If every weight in a `3 × 3` kernel is `1/9`, each output pixel becomes an average of its neighborhood.\n\n"
            "```python\n"
            "with torch.no_grad():\n"
            "    conv.bias.zero_()\n"
            "    conv.weight.fill_(1.0 / 9.0)\n"
            "```\n\n"
            "The result is a smoother, blurred image.\n\n"
            "### Vertical-edge detector\n\n"
            "A kernel similar to:\n\n"
            "```text\n"
            "[-1, 0, 1]\n"
            "[-1, 0, 1]\n"
            "[-1, 0, 1]\n"
            "```\n\n"
            "compares intensity on the right side with intensity on the left side. Uniform regions produce "
            "small responses, while strong vertical boundaries produce larger magnitudes.\n\n"
            "[[IMAGE_NEEDED: Blur kernel and vertical-edge kernel effects | Show the same simple image passed "
            "through a local averaging kernel and a vertical-edge detector, alongside the two 3×3 kernels | "
            "Learner should notice that different local weight patterns emphasize different visual features]]\n\n"
            "Historically, vision systems relied heavily on human-designed filters. Deep learning instead lets "
            "gradient descent discover filter weights that are useful for the end task.\n\n"
            "A CNN therefore learns **banks of feature detectors**, where different output channels may respond "
            "to different patterns.\n\n"
            "---\n\n"

            "## 7. Pooling: reduce spatial resolution while preserving strong responses\n\n"
            "Small convolution kernels give us excellent locality, but objects are larger than `3 × 3` pixels. "
            "We need deeper layers to gradually incorporate larger regions of the image.\n\n"
            "A common strategy is to alternate convolutions with **downsampling**.\n\n"
            "Possible downsampling approaches include:\n\n"
            "- average pooling,\n"
            "- max pooling,\n"
            "- strided convolutions.\n\n"
            "This chapter focuses on max pooling.\n\n"
            "```python\n"
            "pool = nn.MaxPool2d(2)\n"
            "output = pool(img.unsqueeze(0))\n"
            "```\n\n"
            "For a `32 × 32` input, a non-overlapping `2 × 2` max pool reduces the spatial shape to `16 × 16`.\n\n"
            "[[IMAGE_NEEDED: Max pooling over 2x2 regions | A small activation map divided into non-overlapping "
            "2×2 cells, with the maximum value from each cell copied into a smaller output map | Learner should "
            "notice that strong feature responses survive while spatial resolution is halved]]\n\n"
            "The intuition is that convolutional feature maps often contain large positive responses where a learned "
            "feature is detected. Max pooling keeps the strongest local response while shrinking the map.\n\n"
            "---\n\n"

            "## 8. Receptive fields: how small kernels learn about large structures\n\n"
            "A deeper convolution does not operate directly on raw pixels. It operates on feature maps produced by earlier layers.\n\n"
            "When convolution is combined with downsampling, one value in a deeper layer can depend on an increasingly large "
            "region of the original image. That region is the neuron's **receptive field**.\n\n"
            "[[IMAGE_NEEDED: Receptive field growing with depth | A sequence Conv3x3 -> MaxPool2x2 -> Conv3x3 "
            "with arrows tracing one deep output value back to a much larger area of the original image | Learner "
            "should notice that small kernels can indirectly see large input regions when layers are stacked]]\n\n"
            "This creates a hierarchy:\n\n"
            "```text\n"
            "early layers  -> local low-level patterns\n"
            "middle layers -> combinations of those patterns\n"
            "deeper layers -> wider, higher-level structures\n"
            "```\n\n"
            "This hierarchical feature composition is one of the key strengths of deep convolutional networks.\n\n"
            "---\n\n"

            "## 9. Assemble the bird-versus-airplane CNN\n\n"
            "The chapter builds:\n\n"
            "```text\n"
            "RGB image\n"
            " -> Conv2d(3,16,3)\n"
            " -> Tanh\n"
            " -> MaxPool2d(2)\n"
            " -> Conv2d(16,8,3)\n"
            " -> Tanh\n"
            " -> MaxPool2d(2)\n"
            " -> flatten\n"
            " -> Linear(512,32)\n"
            " -> Tanh\n"
            " -> Linear(32,2)\n"
            "```\n\n"
            "With padding preserving convolution size:\n\n"
            "```text\n"
            "B×3×32×32\n"
            " -> B×16×32×32\n"
            " -> B×16×16×16\n"
            " -> B×8×16×16\n"
            " -> B×8×8×8\n"
            " -> B×512\n"
            " -> B×32\n"
            " -> B×2\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Complete baseline CNN with tensor shapes | A block diagram of two convolution/"
            "activation/pooling stages followed by flatten and two fully connected layers, annotated with the "
            "tensor shape after each stage | Learner should practice tracing channels and spatial dimensions]]\n\n"
            "The model contains only about **18 thousand parameters**, dramatically fewer than the millions used by "
            "the dense classifier from Chapter 7.\n\n"
            "But there is a problem if we try to express the entire model with a simple `nn.Sequential`: we need an "
            "explicit reshape between the convolutional part and the first linear layer.\n\n"
            "That motivates writing our own module.\n\n"
            "---\n\n"

            "## 10. Subclass `nn.Module` when the forward computation needs custom logic\n\n"
            "A custom model inherits from `nn.Module`.\n\n"
            "Two pieces are central:\n\n"
            "### `__init__`\n\n"
            "Create and register stateful layers here.\n\n"
            "### `forward`\n\n"
            "Describe how tensors flow through the model.\n\n"
            "```python\n"
            "class Net(nn.Module):\n"
            "    def __init__(self):\n"
            "        super().__init__()\n"
            "        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)\n"
            "        self.act1 = nn.Tanh()\n"
            "        self.pool1 = nn.MaxPool2d(2)\n"
            "        self.conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)\n"
            "        self.act2 = nn.Tanh()\n"
            "        self.pool2 = nn.MaxPool2d(2)\n"
            "        self.fc1 = nn.Linear(8 * 8 * 8, 32)\n"
            "        self.act3 = nn.Tanh()\n"
            "        self.fc2 = nn.Linear(32, 2)\n\n"
            "    def forward(self, x):\n"
            "        out = self.pool1(self.act1(self.conv1(x)))\n"
            "        out = self.pool2(self.act2(self.conv2(out)))\n"
            "        out = out.view(-1, 8 * 8 * 8)\n"
            "        out = self.act3(self.fc1(out))\n"
            "        out = self.fc2(out)\n"
            "        return out\n"
            "```\n\n"
            "There is no custom `backward()` method. Autograd builds the backward computation automatically from the tensor "
            "operations executed during `forward()`.\n\n"
            "The `-1` in `view(-1, 8*8*8)` lets PyTorch infer the batch size.\n\n"
            "{{exercise:M08.L01.EX02}}\n\n"
            "---\n\n"

            "## 11. How `nn.Module` tracks submodules and parameters\n\n"
            "When an `nn.Module` instance is assigned to an attribute of another module, PyTorch registers it as a child submodule.\n\n"
            "That means:\n\n"
            "```python\n"
            "model.parameters()\n"
            "```\n\n"
            "can recursively discover the parameters of `conv1`, `conv2`, `fc1`, and `fc2` without us manually collecting them.\n\n"
            "The optimizer therefore works normally:\n\n"
            "```python\n"
            "optimizer = torch.optim.SGD(model.parameters(), lr=1e-2)\n"
            "```\n\n"
            "If collections of submodules are needed, use containers such as `nn.ModuleList` or `nn.ModuleDict` rather than hiding "
            "plain module objects in ordinary Python lists or dictionaries where automatic registration may be lost.\n\n"
            "---\n\n"

            "## 12. Module API versus functional API\n\n"
            "Not every operation needs a stateful module object.\n\n"
            "PyTorch therefore provides `torch.nn.functional`, commonly imported as `F`.\n\n"
            "| Module style | Functional style |\n"
            "|---|---|\n"
            "| `nn.Linear(...)` | `F.linear(input, weight, bias)` |\n"
            "| Stores parameters internally | Parameters are explicit arguments |\n"
            "| Registered as model state | Function itself has no persistent state |\n"
            "| Natural for trainable layers | Natural for stateless activations/pooling |\n\n"
            "A cleaner network can keep parameter-owning layers as modules and use functions for stateless operations:\n\n"
            "```python\n"
            "import torch.nn.functional as F\n\n"
            "class Net(nn.Module):\n"
            "    def __init__(self):\n"
            "        super().__init__()\n"
            "        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)\n"
            "        self.conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)\n"
            "        self.fc1 = nn.Linear(8 * 8 * 8, 32)\n"
            "        self.fc2 = nn.Linear(32, 2)\n\n"
            "    def forward(self, x):\n"
            "        out = F.max_pool2d(torch.tanh(self.conv1(x)), 2)\n"
            "        out = F.max_pool2d(torch.tanh(self.conv2(out)), 2)\n"
            "        out = out.view(-1, 8 * 8 * 8)\n"
            "        out = torch.tanh(self.fc1(out))\n"
            "        return self.fc2(out)\n"
            "```\n\n"
            "The underlying principle is simple:\n\n"
            "> **Use modules when you need state/parameters to be owned and registered; functions are convenient for stateless operations.**\n\n"
            "---\n\n"

            "## 13. Train the convolutional classifier\n\n"
            "The training loop has not fundamentally changed:\n\n"
            "```python\n"
            "def training_loop(n_epochs, optimizer, model, loss_fn, train_loader):\n"
            "    for epoch in range(1, n_epochs + 1):\n"
            "        loss_train = 0.0\n\n"
            "        for imgs, labels in train_loader:\n"
            "            outputs = model(imgs)\n"
            "            loss = loss_fn(outputs, labels)\n\n"
            "            optimizer.zero_grad()\n"
            "            loss.backward()\n"
            "            optimizer.step()\n\n"
            "            loss_train += loss.item()\n\n"
            "        average_loss = loss_train / len(train_loader)\n"
            "```\n\n"
            "The major architecture change from Chapter 7 is inside the model, not inside the basic optimization recipe.\n\n"
            "Using `.item()` turns the loss into an ordinary Python value for logging rather than retaining unnecessary computation-graph history.\n\n"
            "---\n\n"

            "## 14. Evaluate the CNN and compare architectures\n\n"
            "Validation still uses classification accuracy:\n\n"
            "```python\n"
            "with torch.no_grad():\n"
            "    for imgs, labels in val_loader:\n"
            "        outputs = model(imgs)\n"
            "        _, predicted = torch.max(outputs, dim=1)\n"
            "```\n\n"
            "The source's baseline convolutional model achieves roughly:\n\n"
            "```text\n"
            "training accuracy   ≈ 0.95\n"
            "validation accuracy ≈ 0.90\n"
            "```\n\n"
            "This is much better validation performance than the fully connected model from Chapter 7, despite using dramatically fewer parameters.\n\n"
            "That gives us an important engineering lesson:\n\n"
            "> **A model architecture that matches the structure of the data can outperform a much larger generic architecture.**\n\n"
            "---\n\n"

            "## 15. Save and reload learned model state\n\n"
            "Once the model is trained, save its parameter state:\n\n"
            "```python\n"
            "torch.save(\n"
            "    model.state_dict(),\n"
            "    data_path + 'birds_vs_airplanes.pt',\n"
            ")\n"
            "```\n\n"
            "`state_dict()` contains learned state such as weights and biases. It does **not** by itself define the Python model architecture.\n\n"
            "To restore:\n\n"
            "```python\n"
            "loaded_model = Net()\n"
            "loaded_model.load_state_dict(\n"
            "    torch.load(data_path + 'birds_vs_airplanes.pt')\n"
            ")\n"
            "```\n\n"
            "This means the model definition must remain compatible with the saved parameter names and shapes.\n\n"
            "---\n\n"

            "## 16. Train the model on a GPU\n\n"
            "Choose a device:\n\n"
            "```python\n"
            "device = (\n"
            "    torch.device('cuda')\n"
            "    if torch.cuda.is_available()\n"
            "    else torch.device('cpu')\n"
            ")\n"
            "```\n\n"
            "Move the model:\n\n"
            "```python\n"
            "model = Net().to(device=device)\n"
            "```\n\n"
            "and move every minibatch before the forward pass:\n\n"
            "```python\n"
            "imgs = imgs.to(device=device)\n"
            "labels = labels.to(device=device)\n"
            "```\n\n"
            "[[IMAGE_NEEDED: CPU DataLoader to GPU model pipeline | DataLoader yields CPU minibatches, image and label "
            "tensors are transferred to GPU memory, the CNN runs on GPU, then scalar logging values return to Python | "
            "Learner should notice that model parameters and input tensors must be on the same device]]\n\n"
            "A useful nuance from the chapter:\n\n"
            "- `Module.to(...)` modifies the module in place,\n"
            "- `Tensor.to(...)` returns a tensor on the requested device and should normally be assigned.\n\n"
            "Create the optimizer **after** placing the model on the intended device so the optimizer references the final parameter tensors.\n\n"
            "When loading saved weights onto a chosen device, use `map_location` when appropriate:\n\n"
            "```python\n"
            "state = torch.load(path, map_location=device)\n"
            "model.load_state_dict(state)\n"
            "```\n\n"
            "---\n\n"

            "## 17. Model design dimension #1: width\n\n"
            "**Width** refers to the number of neurons in a fully connected layer or channels in a convolutional layer.\n\n"
            "Increasing output channels gives the network more learned feature maps and therefore greater representational capacity.\n\n"
            "A parameterized model might begin:\n\n"
            "```python\n"
            "class NetWidth(nn.Module):\n"
            "    def __init__(self, n_chans1=32):\n"
            "        super().__init__()\n"
            "        self.n_chans1 = n_chans1\n"
            "        self.conv1 = nn.Conv2d(3, n_chans1, 3, padding=1)\n"
            "        self.conv2 = nn.Conv2d(n_chans1, n_chans1 // 2, 3, padding=1)\n"
            "        self.fc1 = nn.Linear(8 * 8 * n_chans1 // 2, 32)\n"
            "        self.fc2 = nn.Linear(32, 2)\n"
            "```\n\n"
            "More width generally means more parameters and capacity. That can help with genuinely complex input variability, but it also increases the model's ability to memorize irrelevant training detail.\n\n"
            "---\n\n"

            "## 18. Regularization: improve generalization, not just training fit\n\n"
            "Training has two goals that must be kept distinct:\n\n"
            "1. **optimization** — reduce loss on training data,\n"
            "2. **generalization** — perform well on unseen data.\n\n"
            "Regularization refers broadly to techniques that help control overfitting and improve generalization.\n\n"
            "The chapter explores three important approaches:\n\n"
            "- weight penalties / weight decay,\n"
            "- dropout,\n"
            "- batch normalization.\n\n"
            "---\n\n"

            "## 19. Weight penalties and weight decay\n\n"
            "One way to discourage overly specialized solutions is to penalize very large parameter values.\n\n"
            "### L2 regularization\n\n"
            "Add a term based on squared parameters:\n\n"
            "```python\n"
            "l2_lambda = 0.001\n"
            "l2_norm = sum(\n"
            "    p.pow(2.0).sum()\n"
            "    for p in model.parameters()\n"
            ")\n"
            "loss = task_loss + l2_lambda * l2_norm\n"
            "```\n\n"
            "### L1 regularization\n\n"
            "Uses absolute parameter magnitudes instead and can encourage sparse weights.\n\n"
            "For SGD, PyTorch provides a convenient `weight_decay` optimizer argument for the L2-style effect:\n\n"
            "```python\n"
            "optimizer = torch.optim.SGD(\n"
            "    model.parameters(),\n"
            "    lr=learning_rate,\n"
            "    weight_decay=weight_decay,\n"
            ")\n"
            "```\n\n"
            "The strength is a hyperparameter: too little may have negligible effect, while too much can prevent the model from fitting useful structure.\n\n"
            "---\n\n"

            "## 20. Dropout: prevent units from relying too heavily on one another\n\n"
            "During training, dropout randomly zeros some activations. The random mask changes on different iterations.\n\n"
            "This means the network cannot always rely on the same exact combination of active units, which can reduce coordinated memorization.\n\n"
            "For convolutional feature maps, the chapter uses `nn.Dropout2d`, which can zero entire channels:\n\n"
            "```python\n"
            "self.conv1_dropout = nn.Dropout2d(p=0.4)\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Dropout during training versus evaluation | A feature map stack where random channels/activations "
            "are crossed out during training, beside the same network with all features active during evaluation | Learner "
            "should notice that dropout deliberately injects randomness only while training]]\n\n"
            "### `train()` and `eval()` matter\n\n"
            "Dropout behaves differently depending on model mode:\n\n"
            "```python\n"
            "model.train()  # dropout active\n"
            "model.eval()   # dropout disabled for ordinary inference\n"
            "```\n\n"
            "Forgetting `model.eval()` during inference can silently degrade predictions.\n\n"
            "---\n\n"

            "## 21. Batch normalization\n\n"
            "Batch normalization rescales intermediate activations using minibatch statistics, then applies learned scaling and shifting.\n\n"
            "Its practical goals in this chapter include keeping activation inputs in useful numerical regimes, helping optimization, "
            "reducing sensitivity to initialization, and sometimes adding a regularizing effect.\n\n"
            "For 2D convolutional feature maps:\n\n"
            "```python\n"
            "self.bn1 = nn.BatchNorm2d(num_features=n_channels)\n"
            "```\n\n"
            "A typical order used in the source model is:\n\n"
            "```text\n"
            "Conv2d -> BatchNorm2d -> activation -> pooling\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Batch normalization over a minibatch | Several samples with the same feature/channel shown together, "
            "with mean and standard deviation computed across the minibatch and values rescaled before activation | Learner should "
            "notice that normalization statistics come from the batch during training]]\n\n"
            "Batch normalization also behaves differently during training and inference.\n\n"
            "During training, it uses current minibatch statistics and updates running estimates. During evaluation, those running estimates "
            "are frozen and used so a sample's output does not depend unpredictably on whichever other samples happen to share its inference batch.\n\n"
            "Therefore:\n\n"
            "```python\n"
            "model.train()\n"
            "```\n\n"
            "and:\n\n"
            "```python\n"
            "model.eval()\n"
            "```\n\n"
            "are critical whenever dropout or batch normalization is present.\n\n"
            "{{exercise:M08.L01.EX03}}\n\n"
            "---\n\n"

            "## 22. Model design dimension #2: depth\n\n"
            "**Depth** is the number of successive learned transformations.\n\n"
            "Greater depth allows hierarchical computation. In vision, a conceptual hierarchy might look like:\n\n"
            "```text\n"
            "edges\n"
            " -> corners/textures\n"
            " -> parts\n"
            " -> larger structures\n"
            " -> object-level evidence\n"
            "```\n\n"
            "Depth also increases the length of the computation performed on the input.\n\n"
            "But simply adding more layers creates an optimization challenge: backpropagated gradients pass through long chains of derivatives.\n\n"
            "---\n\n"

            "## 23. Why very deep networks can be difficult to train\n\n"
            "Backpropagation uses the chain rule. In a very deep model, a gradient reaching early layers may contain a long product of derivatives.\n\n"
            "If many factors are smaller than 1, repeated multiplication can drive the gradient toward zero. Early layers then receive almost no useful update signal.\n\n"
            "This is one form of the **vanishing gradient problem**.\n\n"
            "Large factors can create different numerical problems, but the general message is the same: deeper networks can be harder to optimize even though they have greater representational capacity.\n\n"
            "---\n\n"

            "## 24. Skip connections and residual learning\n\n"
            "Residual networks introduced a simple but powerful idea: allow information to bypass a block of layers through a shortcut.\n\n"
            "Instead of only computing:\n\n"
            "```text\n"
            "y = F(x)\n"
            "```\n\n"
            "a residual block computes:\n\n"
            "```text\n"
            "y = F(x) + x\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Residual block with skip connection | Input x splits into a learned convolutional path F(x) "
            "and an identity shortcut; the two paths are added before continuing | Learner should notice that the shortcut "
            "provides a direct route for information and gradients around the learned block]]\n\n"
            "A simple forward fragment looks like:\n\n"
            "```python\n"
            "out1 = out\n"
            "out = torch.relu(self.conv3(out)) + out1\n"
            "```\n\n"
            "The shortcut creates a more direct gradient path from later layers back toward earlier representations, helping very deep networks converge.\n\n"
            "Residual connections also tend to make the optimization landscape easier to navigate compared with equally deep plain feed-forward stacks.\n\n"
            "---\n\n"

            "## 25. Build reusable residual blocks\n\n"
            "Instead of manually writing dozens of layers, define a block once and compose many copies.\n\n"
            "A simplified residual block from the chapter is:\n\n"
            "```python\n"
            "class ResBlock(nn.Module):\n"
            "    def __init__(self, n_chans):\n"
            "        super().__init__()\n"
            "        self.conv = nn.Conv2d(\n"
            "            n_chans,\n"
            "            n_chans,\n"
            "            kernel_size=3,\n"
            "            padding=1,\n"
            "            bias=False,\n"
            "        )\n"
            "        self.batch_norm = nn.BatchNorm2d(n_chans)\n\n"
            "    def forward(self, x):\n"
            "        out = self.conv(x)\n"
            "        out = self.batch_norm(out)\n"
            "        out = torch.relu(out)\n"
            "        return out + x\n"
            "```\n\n"
            "Then a deeper network can hold many blocks inside a registered container such as `nn.Sequential`.\n\n"
            "This is a major software-engineering pattern in deep learning:\n\n"
            "> **Define reusable architectural blocks, parameterize how many you need, and compose them programmatically.**\n\n"
            "{{exercise:M08.L01.EX04}}\n\n"
            "---\n\n"

            "## 26. Initialization matters more as networks become deeper\n\n"
            "The values used to initialize weights influence early activation and gradient scales.\n\n"
            "The chapter's residual example uses a Kaiming-style initialization for a ReLU convolution:\n\n"
            "```python\n"
            "torch.nn.init.kaiming_normal_(\n"
            "    self.conv.weight,\n"
            "    nonlinearity='relu',\n"
            ")\n"
            "```\n\n"
            "and explicit batch-normalization initialization.\n\n"
            "You do not need to master initialization theory at this stage. The important lesson is that deep optimization can be sensitive "
            "to initialization, activation choice, normalization, learning rate, and architecture. When a deep model does not converge, "
            "the problem is not necessarily that the idea is fundamentally impossible; training dynamics may need attention.\n\n"
            "---\n\n"

            "## 27. Compare architectural modifications carefully\n\n"
            "The chapter compares wider models, weight decay, dropout, batch normalization, and deeper/residual variants.\n\n"
            "The exact numerical differences should not be overinterpreted because:\n\n"
            "- the dataset is small,\n"
            "- random initialization changes results,\n"
            "- hyperparameters were not exhaustively tuned,\n"
            "- design choices can interact when combined.\n\n"
            "The more durable conceptual distinction is:\n\n"
            "- **width/depth** primarily increase capacity,\n"
            "- **weight decay/dropout** directly target overfitting/generalization,\n"
            "- **batch normalization** strongly helps optimization and can also have regularizing effects,\n"
            "- **skip connections** make deeper networks easier to optimize.\n\n"
            "---\n\n"

            "## 28. A working classifier still has production limitations\n\n"
            "Our model solves a *closed-set* problem: among the two classes it knows, choose airplane or bird.\n\n"
            "But what if the camera sees a cat?\n\n"
            "The classifier still has only two outputs. It may confidently assign the image to one of them even though neither is correct.\n\n"
            "The chapter calls attention to this **overgeneralization** problem: neural classifiers can be very confident on inputs far from their training distribution.\n\n"
            "[[IMAGE_NEEDED: Closed-set classifier on an unknown class | A bird and airplane classifier receives three inputs: bird, "
            "airplane, and cat; the first two are classified appropriately while the cat is still forced into one known class with high "
            "confidence | Learner should notice that high confidence does not imply the input belongs to the model's known distribution]]\n\n"
            "This is a crucial deployment lesson. Accuracy on a held-out set drawn from the same task distribution is important, but it does not "
            "guarantee safe or sensible behavior on arbitrary real-world inputs.\n\n"
            "The model also does not localize objects inside a large image; classification and object detection are different tasks.\n\n"
            "---\n\n"

            "## 29. The reusable CNN engineering blueprint\n\n"
            "The chapter gives us a general workflow for image-learning systems:\n\n"
            "```text\n"
            "image batch B×C×H×W\n"
            "   |\n"
            "   v\n"
            "local learned convolutional features\n"
            "   |\n"
            "   v\n"
            "activation / normalization / regularization\n"
            "   |\n"
            "   v\n"
            "spatial downsampling\n"
            "   |\n"
            "   v\n"
            "deeper features with larger receptive fields\n"
            "   |\n"
            "   v\n"
            "flatten or aggregate\n"
            "   |\n"
            "   v\n"
            "classification logits\n"
            "   |\n"
            "   v\n"
            "cross-entropy loss during training\n"
            "```\n\n"
            "Around that model we need:\n\n"
            "- `Dataset` and `DataLoader`,\n"
            "- optimizer and training loop,\n"
            "- validation metrics,\n"
            "- correct `train()` / `eval()` mode,\n"
            "- device management,\n"
            "- model-state saving/loading,\n"
            "- capacity and regularization decisions.\n\n"
            "This is the first complete convolutional deep-learning system in the course.\n\n"
            "{{exercise:M08.L01.EX05}}\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: Convolution means the kernel weights are handcrafted\n\n"
            "Handwritten blur and edge filters are only teaching examples. In CNN training, kernel weights are ordinary learnable parameters updated by backpropagation.\n\n"
            "### Misconception 2: More channels or more layers always improve generalization\n\n"
            "Width and depth increase capacity. They can improve representation power, but they can also make overfitting or optimization problems worse.\n\n"
            "### Misconception 3: Pooling is the only way to downsample\n\n"
            "Average pooling, max pooling, and strided convolution are all possible approaches. This chapter focuses mainly on max pooling.\n\n"
            "### Misconception 4: `nn.Sequential` can express every architecture cleanly\n\n"
            "Sequential is convenient for straight chains, but custom `nn.Module` subclasses are better when the forward pass requires reshaping, branching, skip connections, or other explicit tensor logic.\n\n"
            "### Misconception 5: `model.eval()` disables gradients\n\n"
            "`eval()` changes behavior of modules such as dropout and batch normalization. Gradient recording is a separate concern controlled by tools such as `torch.no_grad()`.\n\n"
            "### Misconception 6: Saving `state_dict()` saves the complete Python architecture\n\n"
            "`state_dict()` stores learned state. Compatible model code is still needed to construct the architecture before loading those parameters.\n\n"
            "### Misconception 7: A 99% class confidence means the image truly belongs to that class\n\n"
            "A closed-set classifier can be confidently wrong on out-of-distribution inputs because it is still forced to distribute evidence among the classes it knows.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Convolution | Local linear operation that reuses kernel weights across spatial positions. |\n"
            "| Kernel / filter | Small learned weight tensor applied repeatedly to local neighborhoods. |\n"
            "| Feature map | Spatial output channel produced by a convolutional filter. |\n"
            "| Locality | Architectural focus on nearby values rather than arbitrary global connections. |\n"
            "| Weight sharing | Reusing the same kernel parameters at many locations. |\n"
            "| Translation invariance / position independence | Desired ability for a feature to remain useful when its location changes. |\n"
            "| `nn.Conv2d` | PyTorch module implementing learnable 2D convolution. |\n"
            "| Padding | Values added around an input boundary so kernels can operate near edges or preserve size. |\n"
            "| Pooling | Downsampling operation that reduces spatial resolution. |\n"
            "| Max pooling | Downsampling by retaining the maximum value in each local window. |\n"
            "| Receptive field | Region of the original input that can influence one deeper activation. |\n"
            "| `nn.Module` subclass | Custom PyTorch model/component with registered state and a forward computation. |\n"
            "| Functional API | Stateless operations available through `torch.nn.functional` and related tensor functions. |\n"
            "| `state_dict` | Mapping containing a module's learned/stateful tensors for serialization. |\n"
            "| Width | Number of units/channels in layers. |\n"
            "| Depth | Number of successive learned transformations. |\n"
            "| Regularization | Techniques intended to reduce overfitting or improve generalization. |\n"
            "| L2 regularization | Penalty based on squared parameter magnitudes. |\n"
            "| Weight decay | Optimizer-level shrinking of parameters associated with L2-style regularization. |\n"
            "| Dropout | Random removal of activations during training. |\n"
            "| Batch normalization | Normalization of intermediate activations with learned scaling/shifting and running statistics. |\n"
            "| Vanishing gradient | Backpropagated gradient becoming too small to train earlier layers effectively. |\n"
            "| Skip connection | Shortcut path that bypasses one or more transformations. |\n"
            "| Residual block | Block learning a residual transformation and adding the input back to the result. |\n"
            "| Overgeneralization | Confident prediction on inputs outside the task/training distribution. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "1. Why does a fully connected image layer use far more parameters than a small convolution?\n"
            "2. What does a `3×3` convolution kernel compute at one output location?\n"
            "3. Why is weight sharing important for image recognition?\n"
            "4. What is the weight shape of `nn.Conv2d(3, 16, 3)`?\n"
            "5. Why does an unpadded `3×3` convolution reduce `32×32` to `30×30`?\n"
            "6. How does `padding=1` affect a stride-1 `3×3` convolution?\n"
            "7. What visual operation does an all-`1/9` kernel approximate?\n"
            "8. Why does the `[-1,0,1]` style kernel respond strongly to vertical edges?\n"
            "9. What does `MaxPool2d(2)` do to spatial dimensions?\n"
            "10. What is a receptive field?\n"
            "11. Why can receptive fields grow even when every convolution uses only `3×3` kernels?\n"
            "12. Trace the tensor shapes through the baseline CNN from `3×32×32` to the final two logits.\n"
            "13. Why did the `nn.Sequential` attempt fail before adding a flattening operation?\n"
            "14. What are the minimum pieces required to define a custom `nn.Module`?\n"
            "15. Why does a custom model normally not implement its own `backward()`?\n"
            "16. How does assigning a module to `self.conv1` help parameter discovery?\n"
            "17. When is the functional API especially convenient?\n"
            "18. Why does the CNN generalize better than the much larger dense classifier in this example?\n"
            "19. What exactly is stored by `state_dict()`?\n"
            "20. Why should model and input tensors be on the same device?\n"
            "21. What is the practical difference between `Module.to()` and `Tensor.to()` highlighted in the chapter?\n"
            "22. How does increasing width affect capacity?\n"
            "23. What is the purpose of L2 regularization or weight decay?\n"
            "24. How does dropout differ between training and evaluation?\n"
            "25. Why does batch normalization maintain running statistics?\n"
            "26. What is the vanishing gradient problem?\n"
            "27. How does a skip connection create a shorter path for gradients?\n"
            "28. Why are reusable residual blocks helpful when building very deep networks?\n"
            "29. Why can initialization matter more for very deep networks?\n"
            "30. Why can a bird-vs-airplane classifier confidently classify a cat as one of those two classes?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**Convolution improves image learning not merely by adding another layer type, but by encoding useful structure into the model: "
            "local neighborhoods matter, the same detector should be reusable across positions, and deeper feature hierarchies should gradually "
            "combine local evidence into larger patterns. PyTorch then lets us turn those ideas into trainable systems with custom modules, "
            "functional operations, regularization, residual connections, serialization, and accelerator support.**\n"
        ),

        "estimated_minutes": 240,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "why-convolution", "title": "Why convolution", "order": 1},
            {"id": "convolution-intuition", "title": "What convolution does", "order": 2},
            {"id": "locality-and-translation", "title": "Locality and translation-aware feature detection", "order": 3},
            {"id": "conv2d", "title": "nn.Conv2d", "order": 4},
            {"id": "padding", "title": "Padding", "order": 5},
            {"id": "handcrafted-filters", "title": "Handcrafted filters and learned kernels", "order": 6},
            {"id": "pooling", "title": "Pooling and downsampling", "order": 7},
            {"id": "receptive-field", "title": "Receptive fields", "order": 8},
            {"id": "baseline-cnn", "title": "The baseline convolutional classifier", "order": 9},
            {"id": "custom-module", "title": "Subclassing nn.Module", "order": 10},
            {"id": "module-registration", "title": "Submodule and parameter registration", "order": 11},
            {"id": "functional-api", "title": "Module versus functional APIs", "order": 12},
            {"id": "training-cnn", "title": "Training the CNN", "order": 13},
            {"id": "cnn-accuracy", "title": "Evaluating the CNN", "order": 14},
            {"id": "save-load", "title": "Saving and loading model state", "order": 15},
            {"id": "gpu-training", "title": "GPU training", "order": 16},
            {"id": "network-width", "title": "Model width", "order": 17},
            {"id": "regularization", "title": "Regularization", "order": 18},
            {"id": "weight-decay", "title": "Weight penalties and weight decay", "order": 19},
            {"id": "dropout", "title": "Dropout", "order": 20},
            {"id": "batchnorm", "title": "Batch normalization", "order": 21},
            {"id": "network-depth", "title": "Model depth", "order": 22},
            {"id": "vanishing-gradients", "title": "Vanishing gradients", "order": 23},
            {"id": "skip-connections", "title": "Skip connections and residual learning", "order": 24},
            {"id": "residual-blocks", "title": "Reusable residual blocks", "order": 25},
            {"id": "initialization", "title": "Weight initialization", "order": 26},
            {"id": "design-comparison", "title": "Comparing model-design choices", "order": 27},
            {"id": "production-limitations", "title": "Production limitations and overgeneralization", "order": 28},
            {"id": "chapter-blueprint", "title": "Reusable CNN engineering blueprint", "order": 29},
        ],
    },

    "exercises": [
        {
            "id": "M08.L01.EX01",
            "title": "Predict Convolution Shapes and Parameter Counts",
            "lesson_code": "M08.L01",
            "section_id": "conv2d",
            "placement": "after_section",
            "description": "Practice reasoning about Conv2d channels, kernels, parameters, and spatial outputs.",
            "instructions": (
                "For `nn.Conv2d(3, 16, kernel_size=3, padding=1)`, predict the weight shape, bias shape, "
                "trainable parameter count, and output shape for an input batch `(64,3,32,32)`. "
                "Then repeat the output-shape calculation with `padding=0`. Verify all predictions in PyTorch. "
                "Finally, compare the convolution parameter count with `nn.Linear(3072,512)` and explain the difference."
            ),
            "expected_output": (
                "Predictions, executable verification code, exact parameter counts, and a short explanation "
                "of why convolution is more parameter-efficient."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["conv2d", "shape-reasoning", "parameter-counting", "padding"],
        },
        {
            "id": "M08.L01.EX02",
            "title": "Trace a CNN Forward Pass",
            "lesson_code": "M08.L01",
            "section_id": "custom-module",
            "placement": "after_section",
            "description": "Build the baseline CNN and verify every intermediate tensor shape.",
            "instructions": (
                "Implement the chapter's baseline CNN as a custom `nn.Module`. In `forward`, temporarily print "
                "the shape after conv1, pool1, conv2, pool2, flatten, fc1, and fc2. Pass a batch of four "
                "`3×32×32` images. Confirm that the final output is `(4,2)`. Then intentionally remove the "
                "flattening step, observe the failure, and explain why the first linear layer requires a `B×512` tensor."
            ),
            "expected_output": "Working custom module, shape trace, observed failure, and explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["custom-nn-module", "forward-pass", "view", "cnn-shapes"],
        },
        {
            "id": "M08.L01.EX03",
            "title": "Compare Regularization Modes",
            "lesson_code": "M08.L01",
            "section_id": "batchnorm",
            "placement": "after_section",
            "description": "Observe how dropout and batch normalization depend on training/evaluation mode.",
            "instructions": (
                "Create a tiny model containing `nn.Dropout2d` or `nn.Dropout` and a batch-normalization layer. "
                "Run the same input multiple times with `model.train()` and then multiple times with `model.eval()`. "
                "Record what changes. Inspect the batch-normalization running statistics before and after several "
                "training forwards. Explain separately what `model.eval()` changes and what `torch.no_grad()` changes."
            ),
            "expected_output": (
                "Code and observations demonstrating stochastic dropout, batch-normalization running statistics, "
                "evaluation behavior, and the distinction between model mode and autograd."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["dropout", "batch-normalization", "train-mode", "eval-mode", "no-grad"],
        },
        {
            "id": "M08.L01.EX04",
            "title": "Build and Inspect a Residual Block",
            "lesson_code": "M08.L01",
            "section_id": "residual-blocks",
            "placement": "after_section",
            "description": "Practice implementing an identity skip connection with matching tensor shapes.",
            "instructions": (
                "Implement a residual block with `Conv2d(n,n,3,padding=1)`, `BatchNorm2d(n)`, ReLU, and `return out + x`. "
                "Pass a tensor shaped `(8,16,20,20)` through it and verify that input and output shapes match. "
                "Explain why shape compatibility is required for the addition. Then stack five blocks and verify that "
                "backpropagation reaches the first block by calling `.backward()` on a scalar loss and inspecting an early gradient."
            ),
            "expected_output": (
                "Residual-block code, shape checks, a five-block stack, and evidence that early parameters receive gradients."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["residual-block", "skip-connections", "batchnorm", "backpropagation"],
        },
        {
            "id": "M08.L01.EX05",
            "title": "Kernel Size and Unknown-Input Investigation",
            "lesson_code": "M08.L01",
            "section_id": "chapter-blueprint",
            "placement": "after_section",
            "description": "Explore two of the chapter's final design questions: kernel size and closed-set confidence.",
            "instructions": (
                "Part A: change the baseline model's convolution kernels from `3×3` to `5×5`, adjusting padding "
                "when needed to preserve spatial size. Compare parameter counts and training/validation behavior. "
                "Part B: after training a bird-vs-airplane classifier, pass an image that is clearly neither class. "
                "Inspect logits, softmax probabilities, and the predicted class. Explain why a high softmax value does "
                "not prove that the unknown image belongs to one of the training classes."
            ),
            "expected_output": (
                "A parameter-count comparison, training/validation observations, and an analysis of classifier "
                "overgeneralization on an out-of-distribution image."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["kernel-size", "capacity", "generalization", "out-of-distribution", "softmax"],
        },
    ],

    "quiz": {
        "id": "M08.L01.QZ01",
        "title": "Using Convolutions to Generalize — Knowledge Check",
        "lesson_code": "M08.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M08.L01.Q01",
                "section_id": "convolution-intuition",
                "question": "What is the central computational idea of a 2D convolution?",
                "options": [
                    "Reuse a small kernel to compute weighted sums over local neighborhoods.",
                    "Connect every pixel to every hidden unit with unrelated weights.",
                    "Sort pixel values before every layer.",
                    "Convert the image to a class label without parameters.",
                ],
                "correct": 0,
                "explanation": "Convolution repeatedly applies the same local kernel across spatial positions.",
            },
            {
                "id": "M08.L01.Q02",
                "section_id": "conv2d",
                "question": "What is the weight shape of `nn.Conv2d(3,16,kernel_size=3)`?",
                "options": ["`[16,3,3,3]`", "`[3,16,32,32]`", "`[16,32,32]`", "`[3,3,3]`"],
                "correct": 0,
                "explanation": "Conv2d weights are `[out_channels, in_channels, kernel_height, kernel_width]`.",
            },
            {
                "id": "M08.L01.Q03",
                "section_id": "padding",
                "question": "Why use `padding=1` with a stride-1 `3×3` convolution?",
                "options": [
                    "To preserve the input height and width.",
                    "To double the number of channels.",
                    "To remove the batch dimension.",
                    "To disable the convolution bias.",
                ],
                "correct": 0,
                "explanation": "One pixel of padding on each side compensates for the spatial shrinkage from a 3×3 kernel.",
            },
            {
                "id": "M08.L01.Q04",
                "section_id": "pooling",
                "question": "What does `nn.MaxPool2d(2)` usually do to a feature map?",
                "options": [
                    "Halves each spatial dimension by keeping local maxima.",
                    "Doubles channel count.",
                    "Turns logits into probabilities.",
                    "Adds learnable convolution weights.",
                ],
                "correct": 0,
                "explanation": "A non-overlapping 2×2 max pool keeps one maximum value for each local 2×2 region.",
            },
            {
                "id": "M08.L01.Q05",
                "section_id": "receptive-field",
                "question": "Why can deeper CNN features represent larger structures even with small kernels?",
                "options": [
                    "Stacking convolution and downsampling causes deeper activations to depend on larger regions of the original input.",
                    "Every kernel silently grows to the full image size.",
                    "The batch dimension becomes spatial.",
                    "Softmax expands the receptive field.",
                ],
                "correct": 0,
                "explanation": "Each deeper layer combines features whose own values already summarize local neighborhoods.",
            },
            {
                "id": "M08.L01.Q06",
                "section_id": "custom-module",
                "question": "Why subclass `nn.Module` instead of using only `nn.Sequential` in the baseline CNN?",
                "options": [
                    "The forward path needs explicit tensor reshaping between convolutional and linear stages.",
                    "Sequential cannot contain Conv2d.",
                    "Custom modules disable autograd.",
                    "Sequential cannot be optimized.",
                ],
                "correct": 0,
                "explanation": "A custom forward makes reshaping and other arbitrary tensor logic easy to express.",
            },
            {
                "id": "M08.L01.Q07",
                "section_id": "functional-api",
                "question": "When is the functional API especially natural?",
                "options": [
                    "For stateless operations such as activations or pooling inside a custom forward.",
                    "Only when saving a state_dict.",
                    "Only for GPU tensors.",
                    "When automatic differentiation must be disabled.",
                ],
                "correct": 0,
                "explanation": "Stateless functions need no persistent registered parameters.",
            },
            {
                "id": "M08.L01.Q08",
                "section_id": "save-load",
                "question": "What does `model.state_dict()` primarily contain?",
                "options": [
                    "The model's registered learned/stateful tensors.",
                    "The complete Python source code for the model class.",
                    "The entire training dataset.",
                    "Only validation accuracy.",
                ],
                "correct": 0,
                "explanation": "The architecture code must still be available to construct a compatible model before loading state.",
            },
            {
                "id": "M08.L01.Q09",
                "section_id": "dropout",
                "question": "What happens to ordinary dropout when `model.eval()` is used?",
                "options": [
                    "Its random dropping behavior is disabled for evaluation.",
                    "All weights are deleted.",
                    "Gradients are automatically enabled.",
                    "All channels are set to zero.",
                ],
                "correct": 0,
                "explanation": "Dropout behaves stochastically during training and is bypassed in normal evaluation mode.",
            },
            {
                "id": "M08.L01.Q10",
                "section_id": "batchnorm",
                "question": "Why does batch normalization maintain running statistics?",
                "options": [
                    "So evaluation can normalize consistently without depending on the other samples in the current inference batch.",
                    "To count optimizer steps.",
                    "To replace convolution kernels.",
                    "To store class labels.",
                ],
                "correct": 0,
                "explanation": "During evaluation, BatchNorm uses accumulated running estimates rather than current minibatch statistics.",
            },
            {
                "id": "M08.L01.Q11",
                "section_id": "skip-connections",
                "question": "How can a residual skip connection help very deep networks train?",
                "options": [
                    "It creates shorter paths for information and gradients around blocks of transformations.",
                    "It removes every convolution from the model.",
                    "It converts the task into regression.",
                    "It guarantees that loss is convex.",
                ],
                "correct": 0,
                "explanation": "The identity shortcut provides a more direct path that reduces dependence on a long chain of derivative multiplications.",
            },
            {
                "id": "M08.L01.Q12",
                "section_id": "production-limitations",
                "question": "Why can a bird-vs-airplane classifier assign high confidence to a cat image?",
                "options": [
                    "The model is a closed-set classifier and still distributes its output among the classes it knows.",
                    "Softmax checks whether an image belongs to CIFAR automatically.",
                    "Cross-entropy rejects all unknown classes.",
                    "Convolution requires every image to contain a bird.",
                ],
                "correct": 0,
                "explanation": "High relative confidence among known classes is not the same as evidence that the input is in distribution.",
            },
            {
                "id": "M08.L01.Q13",
                "section_id": "weight-decay",
                "question": "What is the purpose of weight decay in this chapter?",
                "options": [
                    "Discourage excessively large parameter values as a regularization strategy.",
                    "Increase image width after convolution.",
                    "Create additional dataset labels.",
                    "Turn evaluation mode on automatically.",
                ],
                "correct": 0,
                "explanation": "Weight decay applies pressure toward smaller weights and can help reduce overfitting.",
            },
            {
                "id": "M08.L01.Q14",
                "section_id": "chapter-blueprint",
                "type": "open",
                "question": (
                    "Explain why the convolutional model can outperform a much larger fully connected image classifier "
                    "with far fewer parameters. Your answer should discuss locality, weight sharing, spatial structure, "
                    "pooling/receptive fields, and generalization."
                ),
            },
        ],
        "passing_score": 70,
    },
}
