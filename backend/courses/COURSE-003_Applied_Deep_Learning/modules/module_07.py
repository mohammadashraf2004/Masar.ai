"""M07.L01 — Telling Birds from Airplanes: Learning from Images.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 7.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M07.L01"
MODULE_ORDER = 7
MODULE_TITLE = "Image Classification Foundations"
MODULE_DESCRIPTION = (
    "Build a complete image-classification pipeline with PyTorch: load CIFAR-10, "
    "transform and normalize images, create a two-class dataset, train a fully "
    "connected classifier with minibatches, use classification loss correctly, "
    "evaluate accuracy, diagnose overfitting, and understand the limits of flattening images."
)

SOURCE_CHAPTER = 7
SOURCE_PAGES = "Chapter 7 (page range not provided in source excerpt)"


TOPIC = {
    "title": "Telling Birds from Airplanes: Learning from Images",
    "slug": "applied-deep-learning-m07-l01",
    "description": (
        "An end-to-end introduction to supervised image classification using CIFAR-10, "
        "TorchVision datasets and transforms, DataLoader minibatches, softmax/logits, "
        "negative log-likelihood and cross-entropy loss, validation accuracy, and the "
        "limitations of fully connected image classifiers."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 3.25,
    "skill_tags": [
        "computer-vision",
        "cifar10",
        "torchvision",
        "dataset",
        "dataloader",
        "image-transforms",
        "normalization",
        "classification",
        "softmax",
        "logits",
        "cross-entropy",
        "minibatches",
        "sgd",
        "accuracy",
        "overfitting",
        "parameter-counting",
        "translation-invariance",
        "module-07",
    ],
    "prerequisite_ids": ["M06.L01"],

    "lesson": {
        "title": "Telling Birds from Airplanes: Learning from Images",
        "content": (
            "# Telling Birds from Airplanes: Learning from Images\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M07.L01  \n"
            "> **Module:** Image Classification Foundations  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, Chapter 7. "
            "This lesson is an instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "- Explain the structure and labels of CIFAR-10.\n"
            "- Describe the `Dataset` interface using `__len__` and `__getitem__`.\n"
            "- Use TorchVision transforms to convert PIL images into tensors.\n"
            "- Explain why `ToTensor()` changes image layout and value range.\n"
            "- Normalize image channels using training-set mean and standard deviation.\n"
            "- Filter CIFAR-10 into a two-class bird-versus-airplane dataset.\n"
            "- Flatten image tensors for a fully connected classifier.\n"
            "- Explain the difference between regression outputs and categorical classification outputs.\n"
            "- Explain logits, softmax probabilities, `argmax`, NLL loss, and cross-entropy loss.\n"
            "- Use `DataLoader` to create shuffled minibatches.\n"
            "- Explain why minibatch gradients are stochastic estimates of the full-dataset gradient.\n"
            "- Evaluate classification accuracy on a validation set with `torch.no_grad()`.\n"
            "- Diagnose overfitting by comparing training and validation performance.\n"
            "- Count trainable parameters and explain why fully connected image models scale poorly.\n"
            "- Explain why flattening an image discards useful spatial structure.\n"
            "- Explain why lack of translation invariance motivates convolutional networks.\n\n"
            "---\n\n"

            "## 1. From a neural network to an image classifier\n\n"
            "In the previous lesson, we learned how to build and train a small neural network for "
            "regression. The training mechanics do not fundamentally change when the input becomes an image.\n\n"
            "What *does* change is the problem structure:\n\n"
            "- the inputs are now image tensors,\n"
            "- the outputs are categorical rather than continuous,\n"
            "- the dataset is much larger,\n"
            "- we need minibatches,\n"
            "- and the model must somehow use visual information to separate classes.\n\n"
            "The chapter builds a complete classification pipeline for two classes: **airplane** and **bird**.\n\n"
            '{{image:bird-vs-airplane-classifier}}'
            '\n\n'
            "---\n\n"

            "## 2. CIFAR-10: a small image-classification dataset\n\n"
            "CIFAR-10 contains **60,000 RGB images**, each only `32 × 32` pixels, divided among 10 classes.\n\n"
            "| Label | Class |\n"
            "|---:|---|\n"
            "| 0 | airplane |\n"
            "| 1 | automobile |\n"
            "| 2 | bird |\n"
            "| 3 | cat |\n"
            "| 4 | deer |\n"
            "| 5 | dog |\n"
            "| 6 | frog |\n"
            "| 7 | horse |\n"
            "| 8 | ship |\n"
            "| 9 | truck |\n\n"
            "The dataset is simple by modern research standards, but that makes it useful for learning "
            "the mechanics of image classification without being overwhelmed by data size or model complexity.\n\n"
            "[[IMAGE_NEEDED: CIFAR-10 class samples | A small grid with one or more example 32×32 RGB "
            "images from each of the ten CIFAR-10 classes | Learner should notice the tiny image size, "
            "the visual ambiguity, and that each sample belongs to one discrete class]]\n\n"
            "TorchVision can download the training and validation/test portions directly:\n\n"
            "```python\n"
            "from torchvision import datasets\n"
            "import os\n\n"
            "data_path = '../data-unversioned/p1ch7/'\n"
            "os.makedirs(data_path, exist_ok=True)\n\n"
            "cifar10 = datasets.CIFAR10(\n"
            "    data_path,\n"
            "    train=True,\n"
            "    download=True,\n"
            ")\n\n"
            "cifar10_val = datasets.CIFAR10(\n"
            "    data_path,\n"
            "    train=False,\n"
            "    download=True,\n"
            ")\n"
            "```\n\n"
            "---\n\n"

            "## 3. The `Dataset` abstraction\n\n"
            "A PyTorch `Dataset` gives code a uniform way to access samples.\n\n"
            "The core interface is conceptually built around two methods:\n\n"
            "```text\n"
            "__len__()      -> how many items exist?\n"
            "__getitem__(i) -> what is sample i?\n"
            "```\n\n"
            "For supervised image classification, one item is usually:\n\n"
            "```text\n"
            "(sample, label)\n"
            "```\n\n"
            "[[IMAGE_NEEDED: PyTorch Dataset interface | A dataset box exposing __len__ and __getitem__, "
            "with __getitem__(i) returning an image and an integer label | Learner should notice that a "
            "Dataset provides an access interface and does not necessarily need to hold every transformed "
            "sample permanently in memory]]\n\n"
            "That means normal Python operations work:\n\n"
            "```python\n"
            "print(len(cifar10))\n"
            "img, label = cifar10[99]\n"
            "```\n\n"
            "Before applying a transform, CIFAR-10 returns the image as a PIL image and the target as an integer class index.\n\n"
            "The abstraction is intentionally general. A dataset can return images, text, audio, tables, "
            "or any other sample representation that a model pipeline needs.\n\n"
            "---\n\n"

            "## 4. Convert images to tensors with TorchVision transforms\n\n"
            "Neural networks need tensors rather than PIL image objects. TorchVision's `transforms` "
            "module provides composable preprocessing operations.\n\n"
            "A central transform is:\n\n"
            "```python\n"
            "from torchvision import transforms\n\n"
            "to_tensor = transforms.ToTensor()\n"
            "img_t = to_tensor(img)\n"
            "```\n\n"
            "For a CIFAR-10 RGB image, the tensor shape becomes:\n\n"
            "```text\n"
            "3 × 32 × 32\n"
            "```\n\n"
            "or:\n\n"
            "```text\n"
            "C × H × W\n"
            "```\n\n"
            "`ToTensor()` also converts ordinary 8-bit image values from approximately `0..255` into "
            "`float32` values scaled to approximately `0..1`.\n\n"
            "This is important because models generally work with floating-point tensors rather than "
            "raw byte-valued image arrays.\n\n"
            "### Attach the transform directly to the dataset\n\n"
            "```python\n"
            "tensor_cifar10 = datasets.CIFAR10(\n"
            "    data_path,\n"
            "    train=True,\n"
            "    download=False,\n"
            "    transform=transforms.ToTensor(),\n"
            ")\n"
            "```\n\n"
            "Now each call to `__getitem__` returns a transformed tensor automatically.\n\n"
            "### Visualizing channel-first tensors\n\n"
            "Matplotlib commonly expects `H × W × C`, so we can temporarily reorder dimensions for plotting:\n\n"
            "```python\n"
            "plt.imshow(img_t.permute(1, 2, 0))\n"
            "```\n\n"
            "This does not mean the model should use that layout. It is only for the plotting tool.\n\n"
            "---\n\n"

            "## 5. Normalize image channels\n\n"
            "The chapter normalizes each color channel so that its distribution is centered roughly "
            "around zero with unit standard deviation.\n\n"
            "Why? From the previous lessons, we know that optimization often behaves better when input "
            "scales are reasonably controlled. Activations are also more likely to operate in useful "
            "response ranges instead of being pushed immediately into saturation.\n\n"
            "### Compute training-set statistics\n\n"
            "For this small dataset, the chapter stacks all transformed images and computes per-channel statistics:\n\n"
            "```python\n"
            "imgs = torch.stack(\n"
            "    [img_t for img_t, _ in tensor_cifar10],\n"
            "    dim=3,\n"
            ")\n\n"
            "mean = imgs.view(3, -1).mean(dim=1)\n"
            "std = imgs.view(3, -1).std(dim=1)\n"
            "```\n\n"
            "The source obtains approximately:\n\n"
            "```text\n"
            "mean = [0.4914, 0.4822, 0.4465]\n"
            "std  = [0.2470, 0.2435, 0.2616]\n"
            "```\n\n"
            "### Compose preprocessing\n\n"
            "```python\n"
            "transform = transforms.Compose([\n"
            "    transforms.ToTensor(),\n"
            "    transforms.Normalize(mean=mean, std=std),\n"
            "])\n"
            "```\n\n"
            "[[IMAGE_NEEDED: CIFAR image before and after normalization | The same image shown conceptually "
            "before normalization and after channel standardization, with a note that the normalized tensor "
            "can contain values outside 0..1 even though no information was intentionally removed | Learner "
            "should notice that normalized data may look visually strange while still being useful to the model]]\n\n"
            "After normalization, directly plotting the tensor may look wrong because plotting software "
            "expects normal display ranges. The numerical representation is for learning, not for human viewing.\n\n"
            "{{exercise:M07.L01.EX01}}\n\n"
            "---\n\n"

            "## 6. Build the bird-versus-airplane dataset\n\n"
            "We now simplify the 10-class problem into two classes:\n\n"
            "```text\n"
            "airplane -> 0\n"
            "bird     -> 1\n"
            "```\n\n"
            "The chapter filters CIFAR-10 and remaps the labels:\n\n"
            "```python\n"
            "label_map = {0: 0, 2: 1}\n"
            "class_names = ['airplane', 'bird']\n\n"
            "cifar2 = [\n"
            "    (img, label_map[label])\n"
            "    for img, label in cifar10\n"
            "    if label in [0, 2]\n"
            "]\n\n"
            "cifar2_val = [\n"
            "    (img, label_map[label])\n"
            "    for img, label in cifar10_val\n"
            "    if label in [0, 2]\n"
            "]\n"
            "```\n\n"
            "The chapter points out that a Python list is enough here because it supports `len()` and indexing. "
            "For more complex or larger pipelines, a proper `Dataset` subclass is usually cleaner and more flexible.\n\n"
            "PyTorch also provides helpers such as `Subset`, `ConcatDataset`, and `ChainDataset` for other dataset-composition patterns.\n\n"
            "---\n\n"

            "## 7. First attempt: flatten the image and use a fully connected network\n\n"
            "Each CIFAR image has:\n\n"
            "```text\n"
            "3 × 32 × 32 = 3072\n"
            "```\n\n"
            "scalar pixel values.\n\n"
            "A fully connected network can treat those 3,072 numbers as ordinary input features by flattening the image.\n\n"
            "[[IMAGE_NEEDED: Flattening an image into a feature vector | A 3×32×32 RGB image tensor being "
            "reshaped into one long 3072-element vector before entering a fully connected neural network | "
            "Learner should notice that flattening preserves numerical values but removes the explicit 2D spatial layout]]\n\n"
            "A first classifier is:\n\n"
            "```python\n"
            "import torch.nn as nn\n\n"
            "model = nn.Sequential(\n"
            "    nn.Linear(3072, 512),\n"
            "    nn.Tanh(),\n"
            "    nn.Linear(512, 2),\n"
            ")\n"
            "```\n\n"
            "The model maps 3,072 input features to a hidden representation of 512 values and then to "
            "two class-related output values.\n\n"
            "But those final two outputs need a classification interpretation. That brings us to logits and probabilities.\n\n"
            "---\n\n"

            "## 8. Classification outputs are not regression targets\n\n"
            "In regression, a prediction such as `21.4°C` has direct quantitative meaning.\n\n"
            "A class ID such as `0` for airplane and `1` for bird is different. The numerical distance "
            "between IDs is not what we want the model to learn.\n\n"
            "The real goal is categorical:\n\n"
            "```text\n"
            "airplane OR bird\n"
            "```\n\n"
            "A useful two-class representation is conceptually:\n\n"
            "```text\n"
            "airplane -> [1, 0]\n"
            "bird     -> [0, 1]\n"
            "```\n\n"
            "The model can produce one score per class. The class with the strongest score becomes the prediction.\n\n"
            "For binary classification there are also one-output formulations using sigmoid-based losses, "
            "but this chapter develops the two-output multiclass formulation because it generalizes naturally "
            "to more than two classes.\n\n"
            "---\n\n"

            "## 9. Softmax: turn class scores into a probability distribution\n\n"
            "Suppose the final layer produces a vector of arbitrary real-valued class scores. These raw scores "
            "are often called **logits**.\n\n"
            "Softmax transforms the vector so that:\n\n"
            "- every output lies between 0 and 1,\n"
            "- all outputs sum to 1,\n"
            "- higher logits still correspond to higher probabilities.\n\n"
            "A simple implementation is:\n\n"
            "```python\n"
            "def softmax(x):\n"
            "    return torch.exp(x) / torch.exp(x).sum()\n"
            "```\n\n"
            "For batched class vectors, PyTorch must know which dimension contains classes:\n\n"
            "```python\n"
            "softmax = nn.Softmax(dim=1)\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Logits to probabilities with softmax | A vector of raw class scores entering "
            "softmax and producing nonnegative probabilities that sum to 1, with the highest logit remaining "
            "the highest probability | Learner should notice that softmax changes scale but preserves ranking]]\n\n"
            "A model could therefore end with:\n\n"
            "```python\n"
            "model = nn.Sequential(\n"
            "    nn.Linear(3072, 512),\n"
            "    nn.Tanh(),\n"
            "    nn.Linear(512, 2),\n"
            "    nn.Softmax(dim=1),\n"
            ")\n"
            "```\n\n"
            "### Flatten and batch one image\n\n"
            "```python\n"
            "img_batch = img.view(-1).unsqueeze(0)\n"
            "print(img_batch.shape)  # [1, 3072]\n"
            "out = model(img_batch)\n"
            "```\n\n"
            "Before training, these probabilities are meaningless because the model parameters are still random.\n\n"
            "### Choose a predicted class\n\n"
            "```python\n"
            "_, index = torch.max(out, dim=1)\n"
            "```\n\n"
            "This is effectively an `argmax`: choose the class index with the largest output value.\n\n"
            "---\n\n"

            "## 10. A loss function designed for classification\n\n"
            "Mean squared error worked well for continuous regression. Classification needs a loss that "
            "rewards assigning high score/probability to the correct class and strongly penalizes assigning "
            "it very little probability.\n\n"
            "The chapter introduces **negative log likelihood (NLL)**.\n\n"
            "For each sample, conceptually:\n\n"
            "1. produce class scores,\n"
            "2. convert them to probabilities,\n"
            "3. select the probability of the correct class,\n"
            "4. take its logarithm,\n"
            "5. negate it.\n\n"
            "If the correct class receives a tiny probability, the loss becomes large.\n\n"
            "[[IMAGE_NEEDED: Negative log-likelihood curve | A curve of -log(p) for correct-class "
            "probability p from near 0 to 1 | Learner should notice that assigning very small probability "
            "to the true class receives a very large penalty while loss approaches zero as p approaches 1]]\n\n"
            "### `LogSoftmax` + `NLLLoss`\n\n"
            "PyTorch's `nn.NLLLoss()` expects **log probabilities**, not ordinary probabilities. "
            "So instead of applying `Softmax` and then manually taking logarithms, use:\n\n"
            "```python\n"
            "model = nn.Sequential(\n"
            "    nn.Linear(3072, 512),\n"
            "    nn.Tanh(),\n"
            "    nn.Linear(512, 2),\n"
            "    nn.LogSoftmax(dim=1),\n"
            ")\n\n"
            "loss_fn = nn.NLLLoss()\n"
            "```\n\n"
            "`LogSoftmax` performs the calculation in a numerically stable way.\n\n"
            "### `CrossEntropyLoss`: the common shortcut\n\n"
            "PyTorch combines the raw-logit-to-log-probability calculation and NLL behavior in:\n\n"
            "```python\n"
            "loss_fn = nn.CrossEntropyLoss()\n"
            "```\n\n"
            "When using `CrossEntropyLoss`, remove the final `LogSoftmax` layer:\n\n"
            "```python\n"
            "model = nn.Sequential(\n"
            "    nn.Linear(3072, 512),\n"
            "    nn.Tanh(),\n"
            "    nn.Linear(512, 2),\n"
            ")\n"
            "```\n\n"
            "The model now returns **logits**. `CrossEntropyLoss` handles the appropriate transformation internally.\n\n"
            "> **Practical rule:** for ordinary multiclass classification, raw logits + `nn.CrossEntropyLoss()` "
            "is usually the simplest formulation.\n\n"
            "{{exercise:M07.L01.EX02}}\n\n"
            "---\n\n"

            "## 11. Train the classifier one sample at a time\n\n"
            "The first image-classification loop processes one sample per update:\n\n"
            "```python\n"
            "optimizer = torch.optim.SGD(model.parameters(), lr=1e-2)\n"
            "loss_fn = nn.NLLLoss()\n\n"
            "for epoch in range(n_epochs):\n"
            "    for img, label in cifar2:\n"
            "        img_tensor = img.view(-1).unsqueeze(0)\n"
            "        label_tensor = torch.tensor([label])\n\n"
            "        out = model(img_tensor)\n"
            "        loss = loss_fn(out, label_tensor)\n\n"
            "        optimizer.zero_grad()\n"
            "        loss.backward()\n"
            "        optimizer.step()\n"
            "```\n\n"
            "This is already stochastic gradient descent in spirit because each update uses only one randomly ordered "
            "sample rather than the exact gradient averaged across the whole dataset.\n\n"
            "But one-sample batches are usually not the best use of modern hardware. We want minibatches.\n\n"
            "---\n\n"

            "## 12. Full-batch, single-sample, and minibatch training\n\n"
            "There are three useful mental models:\n\n"
            "### Full-batch gradient descent\n\n"
            "Use all training samples to estimate one gradient before updating parameters.\n\n"
            "### Single-sample stochastic updates\n\n"
            "Use one sample to estimate the gradient and update immediately.\n\n"
            "### Minibatch stochastic gradient descent\n\n"
            "Use a small group of samples—such as 32, 64, or 128—to estimate the gradient before each update.\n\n"
            "[[IMAGE_NEEDED: Full batch vs sample-wise vs minibatch optimization | Three diagrams showing "
            "one update after all samples, one update after each individual sample, and one update after each "
            "small batch | Learner should notice the trade-off between gradient stability and update frequency]]\n\n"
            "A minibatch gradient is only an estimate of the full-dataset gradient, so its direction contains noise. "
            "That stochasticity is not purely a disadvantage; the source explains that it can help optimization move "
            "through complicated error surfaces rather than following one exact deterministic path.\n\n"
            "Batch size is therefore a **hyperparameter**.\n\n"
            "---\n\n"

            "## 13. Use `DataLoader` to shuffle and batch data\n\n"
            "`torch.utils.data.DataLoader` automates the common job of selecting dataset items, grouping them "
            "into batches, and optionally shuffling the dataset at the start of each epoch.\n\n"
            "```python\n"
            "train_loader = torch.utils.data.DataLoader(\n"
            "    cifar2,\n"
            "    batch_size=64,\n"
            "    shuffle=True,\n"
            ")\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Dataset and DataLoader relationship | A Dataset exposing indexed samples, a shuffled "
            "index order, and a DataLoader grouping those indices into minibatches before yielding image/label tensors | "
            "Learner should notice that Dataset defines access to individual items while DataLoader controls batching "
            "and sampling order]]\n\n"
            "Now training becomes:\n\n"
            "```python\n"
            "for epoch in range(n_epochs):\n"
            "    for imgs, labels in train_loader:\n"
            "        batch_size = imgs.shape[0]\n"
            "        img_tensor = imgs.view(batch_size, -1)\n\n"
            "        out = model(img_tensor)\n"
            "        loss = loss_fn(out, labels)\n\n"
            "        optimizer.zero_grad()\n"
            "        loss.backward()\n"
            "        optimizer.step()\n"
            "```\n\n"
            "For `batch_size=64`, the raw image batch has shape:\n\n"
            "```text\n"
            "64 × 3 × 32 × 32\n"
            "```\n\n"
            "and flattening produces:\n\n"
            "```text\n"
            "64 × 3072\n"
            "```\n\n"
            "The labels tensor has one class index per sample.\n\n"
            "{{exercise:M07.L01.EX03}}\n\n"
            "---\n\n"

            "## 14. Evaluate accuracy on held-out data\n\n"
            "Loss is useful for optimization, but the task itself is classification. A direct metric is **accuracy**:\n\n"
            "```text\n"
            "accuracy = correct predictions / total predictions\n"
            "```\n\n"
            "Create a validation loader without shuffling:\n\n"
            "```python\n"
            "val_loader = torch.utils.data.DataLoader(\n"
            "    cifar2_val,\n"
            "    batch_size=64,\n"
            "    shuffle=False,\n"
            ")\n"
            "```\n\n"
            "Then evaluate without building gradient graphs:\n\n"
            "```python\n"
            "correct = 0\n"
            "total = 0\n\n"
            "with torch.no_grad():\n"
            "    for imgs, labels in val_loader:\n"
            "        batch_size = imgs.shape[0]\n"
            "        outputs = model(imgs.view(batch_size, -1))\n"
            "        _, predicted = torch.max(outputs, dim=1)\n\n"
            "        total += labels.shape[0]\n"
            "        correct += int((predicted == labels).sum())\n\n"
            "accuracy = correct / total\n"
            "```\n\n"
            "The source reports validation accuracy around `0.811` for the shallow fully connected classifier.\n\n"
            "That is much better than random guessing for a balanced two-class problem, but still leaves substantial room for improvement.\n\n"
            "---\n\n"

            "## 15. A deeper model does not automatically solve the problem\n\n"
            "The chapter tries a deeper fully connected network:\n\n"
            "```python\n"
            "model = nn.Sequential(\n"
            "    nn.Linear(3072, 1024),\n"
            "    nn.Tanh(),\n"
            "    nn.Linear(1024, 512),\n"
            "    nn.Tanh(),\n"
            "    nn.Linear(512, 128),\n"
            "    nn.Tanh(),\n"
            "    nn.Linear(128, 2),\n"
            ")\n\n"
            "loss_fn = nn.CrossEntropyLoss()\n"
            "```\n\n"
            "Training accuracy can reach essentially `1.0`, while validation accuracy improves only slightly "
            "to around `0.813` in the source example.\n\n"
            "That is a strong overfitting signal:\n\n"
            "```text\n"
            "training accuracy -> almost perfect\n"
            "validation accuracy -> much lower\n"
            "```\n\n"
            "The model has enough capacity to memorize or exploit training-specific patterns without learning a "
            "representation that generalizes much better to new images.\n\n"
            "This is a practical reminder that **more layers and more parameters do not automatically fix a bad architectural match**.\n\n"
            "---\n\n"

            "## 16. Count parameters and see why fully connected image models grow so fast\n\n"
            "A useful way to understand model size is to count trainable scalar parameters:\n\n"
            "```python\n"
            "numel_list = [\n"
            "    p.numel()\n"
            "    for p in model.parameters()\n"
            "    if p.requires_grad\n"
            "]\n\n"
            "total_params = sum(numel_list)\n"
            "```\n\n"
            "For a linear layer:\n\n"
            "```python\n"
            "nn.Linear(3072, 1024)\n"
            "```\n\n"
            "the weight tensor has shape:\n\n"
            "```text\n"
            "[1024, 3072]\n"
            "```\n\n"
            "and the bias has shape:\n\n"
            "```text\n"
            "[1024]\n"
            "```\n\n"
            "So the layer alone contains:\n\n"
            "```text\n"
            "1024 × 3072 + 1024 = 3,146,752 parameters\n"
            "```\n\n"
            "The chapter's deeper fully connected model has roughly **3.7 million trainable parameters**.\n\n"
            "[[IMAGE_NEEDED: Parameter explosion in a fully connected image layer | A flattened 3072-value image "
            "fully connected to 1024 hidden units, with an annotation showing a 1024×3072 weight matrix and over "
            "3 million parameters | Learner should notice that every hidden unit needs a separate connection to every input pixel]]\n\n"
            "If the image resolution becomes much larger, the first fully connected layer becomes enormous. "
            "This is one major reason image models need architectures that exploit spatial structure more efficiently.\n\n"
            "---\n\n"

            "## 17. Flattening images throws away spatial structure\n\n"
            "A flattened image preserves the pixel values, but it no longer makes locality explicit.\n\n"
            "The model sees:\n\n"
            "```text\n"
            "feature 0, feature 1, feature 2, ... feature 3071\n"
            "```\n\n"
            "It does **not** inherently know that two particular features came from neighboring pixels.\n\n"
            "A fully connected layer allows every input value to interact with every hidden unit, but it treats "
            "the image as a generic vector instead of exploiting the fact that nearby pixels are often strongly related.\n\n"
            "[[IMAGE_NEEDED: Fully connected treatment of an image | A 2D image flattened into a long vector with "
            "dense connections from every pixel value to every hidden unit | Learner should notice that the network "
            "uses many connections but has no built-in notion of local neighborhoods]]\n\n"
            "That mismatch wastes parameters and makes learning visual patterns less efficient.\n\n"
            "---\n\n"

            "## 18. The translation problem\n\n"
            "Suppose the model learns that a dark airplane-like shape appearing at one exact pixel location is useful evidence.\n\n"
            "If the same airplane shifts several pixels to the right, the flattened feature positions change. A fully connected "
            "network does not automatically recognize that this is the same local pattern in a different location.\n\n"
            "This is the translation problem emphasized by the chapter.\n\n"
            "[[IMAGE_NEEDED: Same airplane shifted to a new image position | Two small images containing the same airplane-like "
            "pattern at different coordinates, plus a flattened-vector view showing that different feature positions become active | "
            "Learner should notice why a fully connected classifier must relearn similar patterns at different locations]]\n\n"
            "The source describes this as a lack of **translation invariance**: the model's response is not naturally preserved when "
            "the object moves in the image.\n\n"
            "### Data augmentation helps, but does not fix the architecture\n\n"
            "We can show the model translated examples using random crops or shifts. This is **data augmentation**.\n\n"
            "Augmentation helps the model see more positional variation, but a fully connected architecture still needs enough "
            "parameters to learn many translated versions of similar patterns.\n\n"
            "A better solution is to use a model architecture that is designed around local spatial structure and reuses learned "
            "patterns across locations.\n\n"
            "That is exactly the motivation for **convolutional layers**, introduced in the next chapter.\n\n"
            "{{exercise:M07.L01.EX04}}\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: A `Dataset` must keep every sample as a ready-made tensor in memory\n\n"
            "A dataset is primarily an access abstraction. `__getitem__` can load or transform an item when it is requested.\n\n"
            "### Misconception 2: Softmax is required inside the model whenever we use cross-entropy\n\n"
            "`nn.CrossEntropyLoss()` expects raw logits and internally performs the needed log-softmax/NLL-style computation. "
            "Adding a normal softmax before it is unnecessary and changes the intended numerical path.\n\n"
            "### Misconception 3: Class labels such as 0 and 1 should be treated like regression values\n\n"
            "The labels are category indices, not measurements on a continuous number line. Classification losses are designed "
            "around relative class scores rather than numeric distance between class IDs.\n\n"
            "### Misconception 4: A model with perfect training accuracy must be an excellent classifier\n\n"
            "Perfect training accuracy with much worse validation accuracy is evidence of overfitting, not proof of good generalization.\n\n"
            "### Misconception 5: Flattening preserves everything important about an image\n\n"
            "It preserves raw values but discards explicit spatial organization. The model has no built-in awareness of local neighborhoods "
            "or that the same visual pattern can appear at different positions.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| CIFAR-10 | Dataset of 60,000 small 32×32 RGB images from 10 classes. |\n"
            "| `Dataset` | Abstraction providing indexed access to samples, commonly through `__len__` and `__getitem__`. |\n"
            "| Transform | Preprocessing operation applied to a sample before it is returned. |\n"
            "| `ToTensor` | TorchVision transform converting supported image data to channel-first float tensors. |\n"
            "| Normalization | Rescaling using statistics such as channel mean and standard deviation. |\n"
            "| Classification | Predicting a discrete class rather than a continuous value. |\n"
            "| Logit | Raw, unnormalized class score produced by a model. |\n"
            "| Softmax | Transformation turning class scores into nonnegative values that sum to 1. |\n"
            "| `argmax` | Index of the largest output value; commonly used to choose a predicted class. |\n"
            "| Likelihood | In this lesson, the model-assigned probability/log-probability associated with the observed target class. |\n"
            "| NLL | Negative log likelihood loss. |\n"
            "| Cross-entropy loss | Standard multiclass classification loss; in PyTorch commonly applied directly to logits. |\n"
            "| Minibatch | Small group of samples used to estimate a gradient before one parameter update. |\n"
            "| SGD | Stochastic gradient descent, using gradients estimated from samples or minibatches. |\n"
            "| `DataLoader` | Utility that batches, samples, and optionally shuffles dataset items. |\n"
            "| Accuracy | Fraction of samples assigned the correct class. |\n"
            "| Overfitting | Strong training performance with weaker performance on unseen data. |\n"
            "| Trainable parameter | Learned scalar stored in a parameter tensor with gradients enabled. |\n"
            "| Fully connected layer | Layer in which each output unit has a learned connection to every input feature. |\n"
            "| Spatial structure | Relative arrangement of values in dimensions such as image height and width. |\n"
            "| Translation invariance | Desired property that recognition remains stable when an object shifts position. |\n"
            "| Data augmentation | Creating transformed training examples to expose the model to useful variation. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "1. How many classes and images are in CIFAR-10?\n"
            "2. What do `__len__` and `__getitem__` provide in a `Dataset`?\n"
            "3. What shape does `ToTensor()` produce for a CIFAR RGB image?\n"
            "4. What happens to the image value range when `ToTensor()` converts an 8-bit image?\n"
            "5. Why normalize each color channel?\n"
            "6. Why can a normalized image look wrong when plotted directly?\n"
            "7. Why are bird and airplane labels remapped to contiguous values 0 and 1?\n"
            "8. How many scalar input features are produced when a 3×32×32 image is flattened?\n"
            "9. Why is classification conceptually different from predicting a continuous value?\n"
            "10. What is a logit?\n"
            "11. What two constraints does softmax impose on its outputs?\n"
            "12. Why is `argmax` useful for classification?\n"
            "13. Why is NLL large when the true class gets very small probability?\n"
            "14. What is the relationship between `LogSoftmax + NLLLoss` and `CrossEntropyLoss`?\n"
            "15. Why does `CrossEntropyLoss` normally receive raw logits?\n"
            "16. What is the difference between full-batch and minibatch gradient descent?\n"
            "17. What does `DataLoader(..., shuffle=True)` do for training?\n"
            "18. Why use `torch.no_grad()` during validation accuracy calculation?\n"
            "19. What does training accuracy near 100% with much lower validation accuracy suggest?\n"
            "20. Why does `Linear(3072, 1024)` contain more than three million parameters?\n"
            "21. What important image property is lost when we flatten height and width into one vector?\n"
            "22. Why does a fully connected image classifier struggle when the same object moves to a new position?\n"
            "23. How can data augmentation help with position changes?\n"
            "24. Why does the chapter naturally lead next to convolutional layers?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**An image classifier is more than a neural network: it needs a dataset interface, consistent transforms, "
            "normalization, minibatch sampling, a classification-aware loss, and independent evaluation. A fully connected "
            "network can learn from flattened images, but it uses huge numbers of parameters and ignores local spatial structure, "
            "which is why image recognition quickly motivates convolutional architectures.**\n"
        ),
        "estimated_minutes": 195,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "classification-pipeline", "title": "From a neural network to an image classifier", "order": 1},
            {"id": "cifar10", "title": "CIFAR-10", "order": 2},
            {"id": "dataset-abstraction", "title": "The Dataset abstraction", "order": 3},
            {"id": "torchvision-transforms", "title": "TorchVision transforms", "order": 4},
            {"id": "normalizing-cifar", "title": "Normalizing CIFAR-10", "order": 5},
            {"id": "binary-dataset", "title": "Building the bird-vs-airplane dataset", "order": 6},
            {"id": "flattened-classifier", "title": "A fully connected image classifier", "order": 7},
            {"id": "classification-output", "title": "Classification outputs", "order": 8},
            {"id": "softmax", "title": "Softmax and class probabilities", "order": 9},
            {"id": "classification-loss", "title": "Classification loss", "order": 10},
            {"id": "first-training-loop", "title": "Sample-wise classifier training", "order": 11},
            {"id": "minibatches", "title": "Minibatch stochastic gradient descent", "order": 12},
            {"id": "dataloader", "title": "Using DataLoader", "order": 13},
            {"id": "validation-accuracy", "title": "Validation accuracy", "order": 14},
            {"id": "deeper-model-overfitting", "title": "Deeper models and overfitting", "order": 15},
            {"id": "parameter-counting", "title": "Counting parameters", "order": 16},
            {"id": "spatial-structure", "title": "Why flattening loses spatial structure", "order": 17},
            {"id": "translation-invariance", "title": "Translation invariance and the path to convolutions", "order": 18},
        ],
    },

    "exercises": [
        {
            "id": "M07.L01.EX01",
            "title": "Inspect and Normalize CIFAR-10",
            "lesson_code": "M07.L01",
            "section_id": "normalizing-cifar",
            "placement": "after_section",
            "description": (
                "Practice the complete image preprocessing path from raw dataset sample to normalized tensor."
            ),
            "instructions": (
                "Load CIFAR-10 with `transforms.ToTensor()`. Inspect one sample's type, shape, dtype, minimum, "
                "and maximum. Compute or use training-set channel mean/std, build a `Compose` transform with "
                "`ToTensor` and `Normalize`, reload the dataset, and inspect the normalized sample. Explain why "
                "the normalized tensor may contain values below 0 or above 1."
            ),
            "expected_output": (
                "Working PyTorch/TorchVision code plus a comparison of raw tensor statistics and normalized statistics."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "torchvision",
                "dataset",
                "totensor",
                "normalization",
                "tensor-statistics",
            ],
        },
        {
            "id": "M07.L01.EX02",
            "title": "Logits, Softmax, and Cross-Entropy",
            "lesson_code": "M07.L01",
            "section_id": "classification-loss",
            "placement": "after_section",
            "description": (
                "Connect raw class scores with probabilities, predictions, and classification loss."
            ),
            "instructions": (
                "Create logits for three two-class samples, for example `[[2.0, 0.5], [-1.0, 2.5], [0.2, 0.1]]`, "
                "with target labels `[0, 1, 1]`. Compute softmax probabilities, predicted classes with `argmax`, "
                "and `nn.CrossEntropyLoss()` directly from the logits. Then compute `LogSoftmax(dim=1)` followed by "
                "`nn.NLLLoss()` and verify the losses are equivalent up to normal floating-point precision. Explain "
                "why ordinary `Softmax` should not be inserted before `CrossEntropyLoss`."
            ),
            "expected_output": (
                "Code showing probabilities, predictions, both loss calculations, and a short explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "logits",
                "softmax",
                "argmax",
                "cross-entropy",
                "nll-loss",
            ],
        },
        {
            "id": "M07.L01.EX03",
            "title": "Build a Minibatch Training Step",
            "lesson_code": "M07.L01",
            "section_id": "dataloader",
            "placement": "after_section",
            "description": (
                "Practice using DataLoader batches with a fully connected classifier."
            ),
            "instructions": (
                "Create a `DataLoader` for the two-class dataset with `batch_size=64` and `shuffle=True`. "
                "Take one minibatch and print the image and label shapes. Flatten the image batch from "
                "`B×3×32×32` to `B×3072`, run it through a classifier, compute cross-entropy loss, call "
                "`zero_grad`, `backward`, and `step`, and print the resulting loss. Explain why the batch "
                "dimension must be preserved during flattening."
            ),
            "expected_output": (
                "One complete executable minibatch optimization step plus shape explanations."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "dataloader",
                "minibatches",
                "flattening",
                "training-step",
                "sgd",
            ],
        },
        {
            "id": "M07.L01.EX04",
            "title": "Measure the Cost of Fully Connected Vision",
            "lesson_code": "M07.L01",
            "section_id": "translation-invariance",
            "placement": "after_section",
            "description": (
                "Quantify why flattening images into dense layers scales poorly and reason about translation."
            ),
            "instructions": (
                "1. Compute the number of trainable parameters in `nn.Linear(3072, 512)`.\n"
                "2. Compute the number in `nn.Linear(3072, 1024)`.\n"
                "3. Estimate the weight count for a 1024×1024 RGB image connected to 1024 hidden units.\n"
                "4. Explain why shifting an object by several pixels changes which flattened features are active.\n"
                "5. Explain how random crops/translations can help.\n"
                "6. Explain why an architecture that reuses local pattern detectors across positions would be more efficient."
            ),
            "expected_output": (
                "Parameter calculations and a written explanation connecting dense connectivity, image translation, "
                "augmentation, and the motivation for convolution."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "parameter-counting",
                "fully-connected-networks",
                "spatial-structure",
                "translation-invariance",
                "data-augmentation",
            ],
        },
    ],

    "quiz": {
        "id": "M07.L01.QZ01",
        "title": "Learning from Images — Knowledge Check",
        "lesson_code": "M07.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M07.L01.Q01",
                "section_id": "cifar10",
                "question": "What is the shape of one CIFAR-10 RGB image after `transforms.ToTensor()`?",
                "options": ["`3×32×32`", "`32×32×3`", "`3072×3`", "`1×32×32`"],
                "correct": 0,
                "explanation": "`ToTensor()` returns the image in channel-first `C×H×W` format.",
            },
            {
                "id": "M07.L01.Q02",
                "section_id": "dataset-abstraction",
                "question": "Which two methods capture the core indexed Dataset interface discussed in the lesson?",
                "options": [
                    "`__len__` and `__getitem__`",
                    "`forward` and `backward`",
                    "`step` and `zero_grad`",
                    "`softmax` and `argmax`",
                ],
                "correct": 0,
                "explanation": "`__len__` reports dataset size and `__getitem__` returns an indexed item.",
            },
            {
                "id": "M07.L01.Q03",
                "section_id": "normalizing-cifar",
                "question": "Why normalize image channels before training?",
                "options": [
                    "To place channel values on better-controlled scales for optimization.",
                    "To convert classification into regression.",
                    "To remove the need for a loss function.",
                    "To make every image visually brighter.",
                ],
                "correct": 0,
                "explanation": "Controlled input scale can improve optimization and activation behavior.",
            },
            {
                "id": "M07.L01.Q04",
                "section_id": "flattened-classifier",
                "question": "How many scalar features are in a flattened `3×32×32` image?",
                "options": ["3072", "1024", "96", "32"],
                "correct": 0,
                "explanation": "`3 × 32 × 32 = 3072`.",
            },
            {
                "id": "M07.L01.Q05",
                "section_id": "softmax",
                "question": "What does softmax do to a vector of class scores?",
                "options": [
                    "Produces nonnegative values summing to 1 while preserving score ranking.",
                    "Turns images into tensors.",
                    "Clears parameter gradients.",
                    "Makes every class equally likely.",
                ],
                "correct": 0,
                "explanation": "Softmax maps logits to a probability-like distribution over classes.",
            },
            {
                "id": "M07.L01.Q06",
                "section_id": "classification-loss",
                "question": "What input does `nn.CrossEntropyLoss()` normally expect from a multiclass classifier?",
                "options": [
                    "Raw logits",
                    "Already-softmaxed probabilities",
                    "PIL images",
                    "Boolean predictions only",
                ],
                "correct": 0,
                "explanation": "CrossEntropyLoss combines the numerically stable log-softmax/NLL calculation internally.",
            },
            {
                "id": "M07.L01.Q07",
                "section_id": "classification-loss",
                "question": "Which combination is equivalent in purpose to `nn.CrossEntropyLoss()` in this lesson?",
                "options": [
                    "`nn.LogSoftmax(dim=1)` + `nn.NLLLoss()`",
                    "`nn.ReLU()` + `nn.MSELoss()`",
                    "`nn.Sigmoid()` + `torch.max()`",
                    "`nn.Linear()` + `Dataset()`",
                ],
                "correct": 0,
                "explanation": "LogSoftmax followed by NLLLoss corresponds to the same classification objective.",
            },
            {
                "id": "M07.L01.Q08",
                "section_id": "dataloader",
                "question": "What is the main role of a `DataLoader`?",
                "options": [
                    "Sample, batch, and optionally shuffle dataset items.",
                    "Define neural-network weights.",
                    "Replace the validation set.",
                    "Convert logits into probabilities.",
                ],
                "correct": 0,
                "explanation": "DataLoader controls iteration over dataset samples, including batching and shuffle behavior.",
            },
            {
                "id": "M07.L01.Q09",
                "section_id": "validation-accuracy",
                "question": "Why is `torch.no_grad()` appropriate during validation accuracy calculation?",
                "options": [
                    "Validation needs predictions but does not need gradient graphs or parameter updates.",
                    "It guarantees correct predictions.",
                    "It converts the model to a Dataset.",
                    "It increases batch size automatically.",
                ],
                "correct": 0,
                "explanation": "No backward pass is needed for evaluation, so gradient tracking is unnecessary.",
            },
            {
                "id": "M07.L01.Q10",
                "section_id": "deeper-model-overfitting",
                "question": "Training accuracy is 100% but validation accuracy remains much lower. What does this most strongly suggest?",
                "options": ["Overfitting", "Underflow", "Perfect generalization", "Missing labels"],
                "correct": 0,
                "explanation": "The model fits the training set much better than unseen validation data.",
            },
            {
                "id": "M07.L01.Q11",
                "section_id": "parameter-counting",
                "question": "Why does the first fully connected image layer contain so many parameters?",
                "options": [
                    "Every hidden unit has a separate learned weight for every flattened input pixel value.",
                    "Softmax duplicates every parameter.",
                    "DataLoader stores a parameter for each image.",
                    "Validation requires a second copy of the network.",
                ],
                "correct": 0,
                "explanation": "Dense connectivity produces a weight matrix of `out_features × in_features`.",
            },
            {
                "id": "M07.L01.Q12",
                "section_id": "translation-invariance",
                "type": "open",
                "question": (
                    "Explain why flattening an image before a fully connected classifier makes recognizing the same "
                    "object at different positions inefficient, and why this motivates convolutional layers."
                ),
            },
        ],
        "passing_score": 70,
    },
}
