"""M12.L01 — Training a Classification Model to Detect Suspected Tumors.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 13.
Instructor-authored curriculum adaptation.

Quality standard:
- balanced quiz-answer positions
- explicit train/eval/no_grad/device best practices
- realistic study-time estimate
- learning checkpoints after dense sections
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M12.L01"
MODULE_ORDER = 12
MODULE_TITLE = "3D CT Classification Training"
MODULE_DESCRIPTION = (
    "Build the first end-to-end nodule classifier for the lung-cancer project: wire "
    "LunaDataset into DataLoader, construct a 3D CNN, organize a reusable command-line "
    "training application, train and validate correctly, collect per-sample and per-class "
    "metrics, visualize progress with TensorBoard, and diagnose why extreme class imbalance "
    "makes overall accuracy dangerously misleading."
)

SOURCE_CHAPTER = 13
SOURCE_PAGES = "Chapter 13 (page range not provided in source excerpt)"


TOPIC = {
    "title": "Training a Classification Model to Detect Suspected Tumors",
    "slug": "applied-deep-learning-m12-l01",
    "description": (
        "An end-to-end lesson on training a 3D PyTorch classifier for CT nodule candidates, "
        "covering DataLoaders, application structure, Conv3d architecture, initialization, "
        "training and validation loops, per-class metrics, TensorBoard, performance bottlenecks, "
        "and the failure of overall accuracy under extreme class imbalance."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 6.0,
    "skill_tags": [
        "3d-cnn",
        "conv3d",
        "medical-imaging",
        "ct-classification",
        "dataloader",
        "training-loop",
        "validation-loop",
        "cross-entropy",
        "metrics",
        "class-imbalance",
        "false-negatives",
        "tensorboard",
        "tqdm",
        "cuda",
        "data-parallel",
        "kaiming-initialization",
        "module-12",
    ],
    "prerequisite_ids": ["M11.L01"],

    "lesson": {
        "title": "Training a Classification Model to Detect Suspected Tumors",
        "content": (
            "# Training a Classification Model to Detect Suspected Tumors\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M12.L01  \n"
            "> **Source:** *Deep Learning with PyTorch, Second Edition*, Chapter 13.  \n"
            "> **Study expectation:** about **6 hours** including code tracing, checkpoints, and exercises.\n\n"
            "The previous lesson built the data pipeline. Now we finally connect that pipeline to a trainable model.\n\n"
            "This chapter teaches two equally important lessons:\n\n"
            "1. how to build a structured end-to-end 3D classification training application,\n"
            "2. why a model reporting **99.7% accuracy can still be nearly useless**.\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "- Explain how `LunaDataset` and `DataLoader` connect the data pipeline to model training.\n"
            "- Describe a reusable training-application structure using a Python class and command-line arguments.\n"
            "- Initialize a model, device, optimizer, training loader, and validation loader cleanly.\n"
            "- Explain the expected `N × C × D × H × W` input shape for `nn.Conv3d`.\n"
            "- Explain how `batch_size`, `num_workers`, and `pin_memory` affect data feeding.\n"
            "- Build a reusable 3D convolutional block using `Conv3d`, ReLU, and `MaxPool3d`.\n"
            "- Explain tail, backbone, and head architecture terminology.\n"
            "- Trace the tensor shape through four 3D convolutional blocks.\n"
            "- Explain receptive-field growth in stacked 3D convolutions.\n"
            "- Flatten convolutional features correctly before a linear classification head.\n"
            "- Distinguish logits from softmax probabilities and use each appropriately.\n"
            "- Explain the purpose of Kaiming initialization for ReLU-based networks.\n"
            "- Implement training and validation loops with correct `train()`, `eval()`, and `no_grad()` behavior.\n"
            "- Compute per-sample cross-entropy loss for detailed metrics.\n"
            "- Record labels, probabilities, and losses without retaining gradient graphs.\n"
            "- Compute overall and per-class classification metrics with Boolean masks.\n"
            "- Use `tqdm` to monitor long-running iterations.\n"
            "- Use TensorBoard `SummaryWriter` to visualize metric trends.\n"
            "- Diagnose CPU/data-loading versus GPU-compute bottlenecks.\n"
            "- Explain why overall accuracy is misleading on highly imbalanced datasets.\n"
            "- Explain why missing nearly all positive nodules is a dangerous failure even when total accuracy looks excellent.\n\n"
            "---\n\n"

            "## 1. The first meaningful end-to-end milestone\n\n"
            "The previous chapters gave us:\n\n"
            "- CT data,\n"
            "- annotations,\n"
            "- candidate crops,\n"
            "- a custom `LunaDataset`.\n\n"
            "Now the project can finally complete a full learning cycle:\n\n"
            "```text\n"
            "Dataset\n"
            "  ↓\n"
            "DataLoader\n"
            "  ↓\n"
            "3D classifier\n"
            "  ↓\n"
            "loss\n"
            "  ↓\n"
            "backpropagation\n"
            "  ↓\n"
            "metrics\n"
            "  ↓\n"
            "validation\n"
            "```\n\n"
            '{{image:ct-classifier-training-pipeline}}'
            '\n\n'
            "Getting an imperfect but measurable end-to-end system is valuable because later experiments can be compared against a real baseline.\n\n"
            "---\n\n"

            "## 2. Why the project needs more structure now\n\n"
            "Earlier lessons could fit comfortably inside notebooks or short scripts. This project is larger.\n\n"
            "The source introduces a structured training application with:\n\n"
            "- argument parsing,\n"
            "- model initialization,\n"
            "- data-loader initialization,\n"
            "- training and validation methods,\n"
            "- metrics collection,\n"
            "- logging,\n"
            "- TensorBoard integration.\n\n"
            "The important engineering principle is balance:\n\n"
            "> **Use enough structure to make experimentation and debugging clean, but not so much infrastructure that it becomes the project itself.**\n\n"
            "The chapter explicitly warns against both extremes.\n\n"
            "---\n\n"

            "## 3. Build a reusable command-line application\n\n"
            "The training logic is wrapped in a class so it can be invoked either:\n\n"
            "- from the shell,\n"
            "- from a notebook,\n"
            "- or from another Python program.\n\n"
            "A simplified structure is:\n\n"
            "```python\n"
            "class LunaTrainingApp:\n"
            "    def __init__(self, sys_argv=None):\n"
            "        if sys_argv is None:\n"
            "            sys_argv = sys.argv[1:]\n\n"
            "        parser = argparse.ArgumentParser()\n"
            "        parser.add_argument('--num-workers', type=int, default=8)\n"
            "        # batch size, epochs, channels, comments, etc.\n\n"
            "        self.cli_args = parser.parse_args(sys_argv)\n\n"
            "    def main(self):\n"
            "        ...\n"
            "```\n\n"
            "This design separates **configuration** from **execution**, which makes experiments easier to repeat.\n\n"
            "A timestamp can also identify training runs so logs and TensorBoard outputs remain distinguishable.\n\n"
            "---\n\n"

            "## 4. Initialize device, model, then optimizer\n\n"
            "The chapter detects CUDA and constructs the model before the optimizer:\n\n"
            "```python\n"
            "self.use_cuda = torch.cuda.is_available()\n"
            "self.device = torch.device(\n"
            "    'cuda' if self.use_cuda else 'cpu'\n"
            ")\n\n"
            "self.model = self.initModel()\n"
            "self.optimizer = self.initOptimizer()\n"
            "```\n\n"
            "The model is moved onto the selected device before the optimizer is created.\n\n"
            "That ordering matters in the source design because the optimizer should reference the final parameter objects that will actually be trained.\n\n"
            "The optimizer used in the chapter is SGD with momentum:\n\n"
            "```python\n"
            "torch.optim.SGD(\n"
            "    self.model.parameters(),\n"
            "    lr=0.001,\n"
            "    momentum=0.99,\n"
            ")\n"
            "```\n\n"
            "The chapter treats these as reasonable starting values, not guaranteed optimal hyperparameters.\n\n"
            "---\n\n"

            "## 5. Multi-GPU support: simple versus scalable approaches\n\n"
            "The source uses `nn.DataParallel` when multiple GPUs are present because it is easy to wrap around an existing model.\n\n"
            "```python\n"
            "if torch.cuda.device_count() > 1:\n"
            "    model = nn.DataParallel(model)\n"
            "```\n\n"
            "The chapter also distinguishes this from `DistributedDataParallel`, which it identifies as the recommended approach for broader multi-GPU or multi-machine scaling, although setup is more involved.\n\n"
            "For this lesson, the important point is architectural awareness: scaling training across devices introduces system-level considerations beyond the model definition itself.\n\n"
            "---\n\n"

            "## 6. `DataLoader` completes the Dataset → batch bridge\n\n"
            "`LunaDataset` returns one candidate sample at a time.\n\n"
            "`DataLoader` groups those samples into batches suitable for efficient model execution.\n\n"
            "For 3D convolution, PyTorch expects:\n\n"
            "```text\n"
            "N × C × D × H × W\n"
            "```\n\n"
            "where:\n\n"
            "- `N` = batch size,\n"
            "- `C` = channels,\n"
            "- `D` = depth,\n"
            "- `H` = height,\n"
            "- `W` = width.\n\n"
            "One sample from the last chapter had shape:\n\n"
            "```text\n"
            "1 × 32 × 48 × 48\n"
            "```\n\n"
            "A batch of two becomes:\n\n"
            "```text\n"
            "2 × 1 × 32 × 48 × 48\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Candidate samples collated into a 3D batch | Several C×D×H×W candidate tensors are stacked into an "
            "N×C×D×H×W batch by DataLoader | Learner should notice that DataLoader adds the batch dimension while preserving the "
            "single CT-intensity channel]]\n\n"
            "---\n\n"

            "## 7. Keep the GPU fed: workers and pinned memory\n\n"
            "The source configures loaders with settings such as:\n\n"
            "```python\n"
            "DataLoader(\n"
            "    train_ds,\n"
            "    batch_size=batch_size,\n"
            "    num_workers=self.cli_args.num_workers,\n"
            "    pin_memory=self.use_cuda,\n"
            ")\n"
            "```\n\n"
            "### `batch_size`\n\n"
            "Controls how many samples the model processes together.\n\n"
            "### `num_workers`\n\n"
            "Lets separate worker processes prepare future batches in parallel.\n\n"
            "### `pin_memory=True`\n\n"
            "Can make CPU→GPU transfers more efficient when CUDA is used.\n\n"
            "[[IMAGE_NEEDED: DataLoader workers feeding a GPU | Multiple CPU worker processes load and prepare batches into a queue while "
            "the GPU consumes the previous batch | Learner should notice that overlapping data preparation with GPU work reduces idle time]]\n\n"
            "A fast GPU can still train slowly if the CPU/data pipeline cannot deliver the next batch in time.\n\n"

            "### Learning checkpoint 1 — Training application setup\n\n"
            "Before moving to the model, explain:\n\n"
            "1. why the model is moved to its device before optimizer construction,\n"
            "2. what shape `Conv3d` expects,\n"
            "3. what `num_workers` changes,\n"
            "4. why `pin_memory` can matter with CUDA.\n\n"
            "{{exercise:M12.L01.EX01}}\n\n"
            "---\n\n"

            "## 8. Start with a simple, credible 3D CNN\n\n"
            "The design space is enormous, so the source chooses a straightforward first-pass architecture based on ideas already learned for 2D CNNs.\n\n"
            "The model follows a common pattern:\n\n"
            "```text\n"
            "tail -> backbone -> head\n"
            "```\n\n"
            "### Tail\n\n"
            "Initial processing that adapts the raw model input.\n\n"
            "### Backbone\n\n"
            "Repeated convolutional blocks performing most feature extraction.\n\n"
            "### Head\n\n"
            "Converts the extracted representation into class predictions.\n\n"
            "[[IMAGE_NEEDED: LunaModel tail-backbone-head architecture | Input 3D crop enters BatchNorm3d tail, four repeated convolutional "
            "blocks form the backbone, then flattened features enter a linear two-class head | Learner should notice the familiar high-level "
            "vision-model organization]]\n\n"
            "The chapter emphasizes starting simple and adding complexity only when there is evidence that the architecture is the limiting factor.\n\n"
            "---\n\n"

            "## 9. `LunaBlock`: two 3D convolutions plus pooling\n\n"
            "Each repeated backbone block contains:\n\n"
            "```text\n"
            "Conv3d(3×3×3)\n"
            " -> ReLU\n"
            " -> Conv3d(3×3×3)\n"
            " -> ReLU\n"
            " -> MaxPool3d(2)\n"
            "```\n\n"
            "A simplified implementation is:\n\n"
            "```python\n"
            "class LunaBlock(nn.Module):\n"
            "    def __init__(self, in_channels, conv_channels):\n"
            "        super().__init__()\n"
            "        self.conv1 = nn.Conv3d(\n"
            "            in_channels,\n"
            "            conv_channels,\n"
            "            kernel_size=3,\n"
            "            padding=1,\n"
            "        )\n"
            "        self.relu1 = nn.ReLU(inplace=True)\n"
            "        self.conv2 = nn.Conv3d(\n"
            "            conv_channels,\n"
            "            conv_channels,\n"
            "            kernel_size=3,\n"
            "            padding=1,\n"
            "        )\n"
            "        self.relu2 = nn.ReLU(inplace=True)\n"
            "        self.maxpool = nn.MaxPool3d(2, 2)\n"
            "```\n\n"
            "The use of 3D operations is the key adaptation from ordinary 2D image classification.\n\n"
            "---\n\n"

            "## 10. Receptive fields in 3D\n\n"
            "One `3×3×3` convolution lets one output voxel depend on 27 nearby input voxels.\n\n"
            "Stack two padded `3×3×3` convolutions and the second output can depend on a larger effective region of the original input.\n\n"
            "The source describes the two stacked convolutions as having an effective `5×5×5` receptive field before pooling.\n\n"
            "Then the `2×2×2` max pool combines nearby outputs and downsamples the spatial resolution.\n\n"
            "[[IMAGE_NEEDED: Growing 3D receptive field through two convolutions | One deep output voxel traced backward through two "
            "3×3×3 convolution neighborhoods into a larger 5×5×5 source region, followed by 2×2×2 pooling | Learner should notice that "
            "small kernels compose into larger effective receptive fields]]\n\n"
            "Using stacked small kernels gives us larger context with fewer parameters than one very large convolution would require.\n\n"
            "---\n\n"

            "## 11. The full `LunaModel`\n\n"
            "The source model uses:\n\n"
            "```python\n"
            "self.tail_batchnorm = nn.BatchNorm3d(1)\n\n"
            "self.block1 = LunaBlock(1, 8)\n"
            "self.block2 = LunaBlock(8, 16)\n"
            "self.block3 = LunaBlock(16, 32)\n"
            "self.block4 = LunaBlock(32, 64)\n\n"
            "self.head_linear = nn.Linear(1152, 2)\n"
            "self.head_softmax = nn.Softmax(dim=1)\n"
            "```\n\n"
            "Each block doubles the number of channels while its max-pool halves each spatial dimension.\n\n"
            "Starting from:\n\n"
            "```text\n"
            "32 × 48 × 48\n"
            "```\n\n"
            "four `2×2×2` pooling operations reduce spatial size to:\n\n"
            "```text\n"
            "2 × 3 × 3\n"
            "```\n\n"
            "with 64 channels at the end of the backbone.\n\n"
            "Therefore:\n\n"
            "```text\n"
            "64 × 2 × 3 × 3 = 1152\n"
            "```\n\n"
            "features enter the final linear layer.\n\n"
            "{{exercise:M12.L01.EX02}}\n\n"
            "---\n\n"

            "## 12. Flatten convolutional features before classification\n\n"
            "The backbone output is still spatial:\n\n"
            "```text\n"
            "B × 64 × 2 × 3 × 3\n"
            "```\n\n"
            "A linear layer expects one feature vector per sample.\n\n"
            "So the forward pass uses:\n\n"
            "```python\n"
            "conv_flat = block_out.view(\n"
            "    block_out.size(0),\n"
            "    -1,\n"
            ")\n"
            "```\n\n"
            "The batch dimension is preserved while all remaining dimensions are flattened.\n\n"
            "Then:\n\n"
            "```python\n"
            "linear_output = self.head_linear(conv_flat)\n"
            "```\n\n"
            "produces two class logits per sample.\n\n"
            "---\n\n"

            "## 13. Return both logits and probabilities\n\n"
            "The chapter returns:\n\n"
            "```python\n"
            "return linear_output, self.head_softmax(linear_output)\n"
            "```\n\n"
            "The two outputs serve different purposes.\n\n"
            "### Logits\n\n"
            "Raw real-valued class scores. These are passed to:\n\n"
            "```python\n"
            "nn.CrossEntropyLoss()\n"
            "```\n\n"
            "during training.\n\n"
            "### Probabilities\n\n"
            "Softmax-normalized outputs between 0 and 1 that sum to 1. These are convenient for classification metrics and interpretation.\n\n"
            "The important rule remains:\n\n"
            "> **Use raw logits for `CrossEntropyLoss`; do not feed already-softmaxed probabilities into it.**\n\n"
            "---\n\n"

            "## 14. Kaiming initialization keeps signal scales usable\n\n"
            "Deep networks can become hard to train if forward activations or backward gradients rapidly explode or vanish.\n\n"
            "The source explicitly initializes convolutional and linear weights using a Kaiming-style initialization suitable for ReLU-based networks:\n\n"
            "```python\n"
            "nn.init.kaiming_normal_(\n"
            "    m.weight.data,\n"
            "    a=0,\n"
            "    mode='fan_out',\n"
            "    nonlinearity='relu',\n"
            ")\n"
            "```\n\n"
            "The lesson at this stage is not to memorize every initialization formula. It is to understand that initialization affects the scale of activations and gradients before learning has had a chance to correct anything.\n\n"

            "### Learning checkpoint 2 — Model architecture\n\n"
            "You should be able to trace:\n\n"
            "```text\n"
            "B×1×32×48×48\n"
            " -> BatchNorm3d\n"
            " -> block1\n"
            " -> block2\n"
            " -> block3\n"
            " -> block4\n"
            " -> B×64×2×3×3\n"
            " -> flatten to B×1152\n"
            " -> Linear(1152,2)\n"
            " -> logits + probabilities\n"
            "```\n\n"
            "If you cannot explain where `1152` comes from, revisit sections 9–12.\n\n"
            "---\n\n"

            "## 15. Training loop: familiar mechanics, better organization\n\n"
            "The training method starts with:\n\n"
            "```python\n"
            "self.model.train()\n"
            "```\n\n"
            "Then, for every batch:\n\n"
            "```python\n"
            "self.optimizer.zero_grad()\n"
            "loss = self.computeBatchLoss(...)\n"
            "loss.backward()\n"
            "self.optimizer.step()\n"
            "```\n\n"
            "The mathematics is familiar from earlier chapters.\n\n"
            "What changes is the engineering structure:\n\n"
            "- progress tracking is separated,\n"
            "- loss/metrics logic lives in another method,\n"
            "- detailed metrics are stored for the entire epoch,\n"
            "- the application can support future experiments without rewriting the core loop.\n\n"
            "---\n\n"

            "## 16. Compute per-sample cross-entropy loss\n\n"
            "`computeBatchLoss` unpacks the batch, moves tensors to the training device, runs the model, and computes classification loss.\n\n"
            "```python\n"
            "input_t, label_t, _series_list, _center_list = batch_tup\n\n"
            "input_g = input_t.to(\n"
            "    self.device,\n"
            "    non_blocking=True,\n"
            ")\n"
            "label_g = label_t.to(\n"
            "    self.device,\n"
            "    non_blocking=True,\n"
            ")\n\n"
            "logits_g, probability_g = self.model(input_g)\n"
            "```\n\n"
            "The loss uses:\n\n"
            "```python\n"
            "loss_func = nn.CrossEntropyLoss(reduction='none')\n"
            "loss_g = loss_func(logits_g, label_g[:, 1])\n"
            "```\n\n"
            "`reduction='none'` preserves one loss value per sample instead of immediately averaging the batch.\n\n"
            "The mean is still returned for backpropagation:\n\n"
            "```python\n"
            "return loss_g.mean()\n"
            "```\n\n"
            "Why keep individual losses? Because later we may want to compare positive and negative examples separately.\n\n"
            "---\n\n"

            "## 17. Record detailed metrics per sample\n\n"
            "The chapter records three values for every sample:\n\n"
            "```text\n"
            "true label\n"
            "predicted positive probability\n"
            "cross-entropy loss\n"
            "```\n\n"
            "It stores them in an epoch-sized metrics tensor.\n\n"
            "Importantly, the values are detached:\n\n"
            "```python\n"
            "metrics_g[...label...] = label_g[:, 1].detach()\n"
            "metrics_g[...pred...] = probability_g[:, 1].detach()\n"
            "metrics_g[...loss...] = loss_g.detach()\n"
            "```\n\n"
            "Metric logging does not need gradients, so retaining the autograd graph would waste memory.\n\n"
            "Detailed per-sample metrics also make debugging possible. We can later find the worst mistakes rather than only seeing one epoch-average number.\n\n"
            "---\n\n"

            "## 18. Validation is read-only\n\n"
            "Validation should not update the model.\n\n"
            "The source correctly combines:\n\n"
            "```python\n"
            "self.model.eval()\n"
            "```\n\n"
            "with:\n\n"
            "```python\n"
            "with torch.no_grad():\n"
            "    ...\n"
            "```\n\n"
            "and does not call the optimizer.\n\n"
            "[[IMAGE_NEEDED: Training versus validation loop | Parallel diagrams show training using train mode, forward, loss, backward, and optimizer step; "
            "validation uses eval mode, forward, metrics, and no_grad with no backward/update arrows | Learner should notice that validation must not modify weights]]\n\n"
            "`eval()` and `no_grad()` solve different problems:\n\n"
            "- `eval()` switches modules such as batch normalization into evaluation behavior,\n"
            "- `no_grad()` stops gradient-graph construction.\n\n"
            "{{exercise:M12.L01.EX03}}\n\n"
            "---\n\n"

            "## 19. Overall metrics are not enough—compute them by class\n\n"
            "The chapter creates Boolean masks for negative and positive samples.\n\n"
            "With a threshold of `0.5`:\n\n"
            "```python\n"
            "negLabel_mask = labels <= 0.5\n"
            "negPred_mask = predictions <= 0.5\n\n"
            "posLabel_mask = ~negLabel_mask\n"
            "posPred_mask = ~negPred_mask\n"
            "```\n\n"
            "Then it computes:\n\n"
            "- overall loss,\n"
            "- negative-class loss,\n"
            "- positive-class loss,\n"
            "- overall percent correct,\n"
            "- negative-class percent correct,\n"
            "- positive-class percent correct.\n\n"
            "This is the beginning of a much more informative evaluation system.\n\n"
            "[[IMAGE_NEEDED: Overall accuracy split into per-class performance | One large overall-accuracy bar is decomposed into separate "
            "non-nodule and nodule accuracy/loss panels | Learner should notice how a strong majority-class score can hide catastrophic minority-class failure]]\n\n"
            "---\n\n"

            "## 20. Boolean masks are a useful tensor-analysis tool\n\n"
            "A Boolean tensor can select only samples satisfying a condition.\n\n"
            "For example:\n\n"
            "```python\n"
            "positive_loss = losses[posLabel_mask].mean()\n"
            "```\n\n"
            "or:\n\n"
            "```python\n"
            "positive_correct = (\n"
            "    posLabel_mask & posPred_mask\n"
            ").sum()\n"
            "```\n\n"
            "This NumPy-like indexing style is a powerful general technique for analyzing model behavior across subgroups.\n\n"
            "The source also warns that its simple threshold logic relies on this being a binary, single-label classification problem.\n\n"
            "---\n\n"

            "## 21. Progress monitoring with `tqdm`\n\n"
            "Deep-learning runs can take long enough that a silent terminal becomes uncomfortable and hard to diagnose.\n\n"
            "`tqdm` wraps an iterable and reports:\n\n"
            "- percent complete,\n"
            "- completed iterations,\n"
            "- total iterations,\n"
            "- elapsed time,\n"
            "- estimated time remaining,\n"
            "- iteration rate.\n\n"
            "```python\n"
            "for batch in tqdm(train_dl, desc='Training'):\n"
            "    ...\n"
            "```\n\n"
            "Progress information is operationally useful: unexpectedly slow throughput can reveal an I/O, caching, worker, or compute problem.\n\n"
            "---\n\n"

            "## 22. Determine whether CPU/data loading or GPU compute is the bottleneck\n\n"
            "The source suggests observing CPU utilization and GPU utilization while training.\n\n"
            "A rough interpretation in this particular project is:\n\n"
            "- high CPU worker utilization with an underused GPU can indicate the input pipeline is struggling,\n"
            "- high GPU utilization indicates the accelerator is receiving enough work.\n\n"
            "Cache preparation can strongly affect the first runs.\n\n"
            "The important general lesson is not one exact percentage threshold. It is to **measure the whole pipeline** rather than assume the neural network itself is the only performance bottleneck.\n\n"
            "---\n\n"

            "## 23. Check that the expected data is actually present\n\n"
            "The source expects approximately:\n\n"
            "```text\n"
            "495,958 training samples\n"
            "55,107 validation samples\n"
            "```\n\n"
            "when the full dataset is available under the chapter's split.\n\n"
            "The lesson is broader than those exact numbers:\n\n"
            "> **Know the expected dataset size and verify it before trusting training results.**\n\n"
            "Missing files can silently change sample counts, class balance, and the meaning of every metric that follows.\n\n"
            "---\n\n"

            "## 24. Visualize metric trends with TensorBoard\n\n"
            "Per-epoch console numbers are useful, but trends are easier to understand visually.\n\n"
            "PyTorch integrates with TensorBoard through:\n\n"
            "```python\n"
            "from torch.utils.tensorboard import SummaryWriter\n"
            "```\n\n"
            "The source creates separate writers for training and validation runs.\n\n"
            "Metrics are then written as scalars:\n\n"
            "```python\n"
            "for key, value in metrics_dict.items():\n"
            "    writer.add_scalar(\n"
            "        key,\n"
            "        value,\n"
            "        self.totalTrainingSamples_count,\n"
            "    )\n"
            "```\n\n"
            "[[IMAGE_NEEDED: TensorBoard training and validation dashboard | Several time-series charts for overall loss, positive loss, "
            "negative loss, and percent correct with training and validation runs visible together | Learner should notice that trends expose "
            "problems more clearly than isolated epoch numbers]]\n\n"
            "The source uses total training samples seen as the horizontal axis so experiments with different epoch sizes can still be compared meaningfully.\n\n"
            "---\n\n"

            "## 25. Experiment logging needs hygiene too\n\n"
            "Repeated experiments can create many empty, failed, or obsolete TensorBoard runs.\n\n"
            "The source delays writer creation until metrics are actually ready to be written and recommends cleaning unimportant runs.\n\n"
            "It also points out that TensorBoard smoothing can help reveal trends, but excessive smoothing can hide meaningful variation.\n\n"
            "A dashboard is only useful when you understand what the plotted values represent and keep run names organized enough to compare experiments correctly.\n\n"
            "---\n\n"

            "## 26. The accuracy trap: 99.7% correct and still useless\n\n"
            "After one epoch, the chapter reports overall accuracy around:\n\n"
            "```text\n"
            "training   ≈ 99.7%\n"
            "validation ≈ 99.8%\n"
            "```\n\n"
            "That sounds excellent—until we separate the classes.\n\n"
            "The validation breakdown is approximately:\n\n"
            "```text\n"
            "non-nodule accuracy ≈ 100%\n"
            "nodule accuracy     ≈   0%\n"
            "```\n\n"
            "The model has learned the easiest possible strategy:\n\n"
            "> **predict non-nodule for almost everything.**\n\n"
            "[[IMAGE_NEEDED: Misleading 99.7 percent accuracy under class imbalance | A dataset graphic with roughly 99.7 percent negative "
            "samples and 0.3 percent positive samples; a classifier predicts every item negative and still receives a 99.7 percent overall "
            "accuracy badge while positive recall is zero | Learner should immediately see why the aggregate score is misleading]]\n\n"
            "Because only about `0.3%` of candidates are positive, a trivial all-negative classifier receives an impressive-looking score.\n\n"
            "---\n\n"

            "## 27. Why extreme class imbalance changes the problem\n\n"
            "The training distribution contains vastly more non-nodules than nodules.\n\n"
            "If the objective and sampling strategy let the majority class dominate every update, the optimizer can reduce average loss substantially by becoming very good at predicting the majority class while barely learning the minority class.\n\n"
            "This does **not** mean cross-entropy is mathematically broken. It means the overall training setup is allowing an easy majority-class solution to dominate the learning signal.\n\n"
            "The chapter intentionally leaves the correction for the following chapter. Here, the goal is to recognize the failure accurately.\n\n"
            "---\n\n"

            "## 28. The cost of a mistake depends on the application\n\n"
            "In this project, a missed true nodule is not equivalent in consequence to every other mistake.\n\n"
            "The source emphasizes that classifying a real tumor-like finding as innocuous can be especially dangerous because it may prevent further evaluation.\n\n"
            "This leads to a broader machine-learning principle:\n\n"
            "> **Metrics must reflect the mistakes that actually matter in the application.**\n\n"
            "Overall accuracy alone cannot capture that distinction.\n\n"
            "The next chapter will introduce better terminology and evaluation measures for this problem.\n\n"
            "---\n\n"

            "## 29. The model may still be learning even when accuracy is stuck\n\n"
            "After more epochs, the source still sees essentially zero correctly classified positive validation samples.\n\n"
            "However, positive-class loss begins to decrease.\n\n"
            "That tells us something subtle:\n\n"
            "- hard classification decisions have not improved yet,\n"
            "- but predicted probabilities may be moving in a better direction.\n\n"
            "This is why tracking **loss and class-specific behavior**, not only thresholded accuracy, is useful.\n\n"
            "A model can make progress before that progress becomes visible in a coarse 0/1 metric.\n\n"
            "{{exercise:M12.L01.EX04}}\n\n"
            "---\n\n"

            "## 30. The reusable training-system blueprint\n\n"
            "The complete chapter gives us this pattern:\n\n"
            "```text\n"
            "CONFIGURATION\n"
            "  CLI args / run identifier\n"
            "        ↓\n"
            "INITIALIZATION\n"
            "  device -> model -> optimizer\n"
            "  Dataset -> DataLoader\n"
            "        ↓\n"
            "MODEL\n"
            "  BatchNorm3d tail\n"
            "  repeated Conv3d blocks\n"
            "  flatten\n"
            "  linear classification head\n"
            "        ↓\n"
            "TRAINING\n"
            "  model.train()\n"
            "  forward -> per-sample loss -> mean\n"
            "  backward -> optimizer.step()\n"
            "        ↓\n"
            "VALIDATION\n"
            "  model.eval()\n"
            "  torch.no_grad()\n"
            "  metrics only\n"
            "        ↓\n"
            "OBSERVABILITY\n"
            "  per-class metrics\n"
            "  tqdm\n"
            "  TensorBoard\n"
            "        ↓\n"
            "DIAGNOSIS\n"
            "  detect class imbalance / misleading accuracy\n"
            "```\n\n"
            "This is no longer just a neural-network example. It is the beginning of a reusable ML training application.\n\n"
            "### Learning checkpoint 3 — Can you diagnose the system?\n\n"
            "Suppose a run reports:\n\n"
            "```text\n"
            "overall validation accuracy: 99.8%\n"
            "negative accuracy:            100%\n"
            "positive accuracy:              0%\n"
            "```\n\n"
            "You should immediately conclude that the aggregate accuracy is misleading and inspect class balance, positive loss/probabilities, sampling, and later evaluation metrics—not celebrate the 99.8% number.\n\n"
            "{{exercise:M12.L01.EX05}}\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: Once a custom Dataset exists, DataLoader adds no important functionality\n\n"
            "DataLoader provides batching, worker processes, collation, and optional pinned-memory support, all of which matter for efficient training.\n\n"
            "### Misconception 2: A 3D CT crop can go directly into `Conv2d`\n\n"
            "The source uses `Conv3d` because depth, height, and width are all spatial dimensions.\n\n"
            "### Misconception 3: Softmax probabilities should be passed into `CrossEntropyLoss`\n\n"
            "The chapter uses raw logits for cross-entropy and probabilities separately for classification metrics.\n\n"
            "### Misconception 4: `model.eval()` and `torch.no_grad()` are interchangeable\n\n"
            "`eval()` changes module behavior; `no_grad()` disables gradient tracking. Proper validation uses both.\n\n"
            "### Misconception 5: A 99.7% validation accuracy proves the classifier is excellent\n\n"
            "The dataset is so imbalanced that predicting every sample as non-nodule can achieve about that score while finding essentially no nodules.\n\n"
            "### Misconception 6: Overall loss and accuracy tell you everything needed to debug the model\n\n"
            "Per-class losses and predictions reveal behavior that aggregate metrics can hide.\n\n"
            "### Misconception 7: If hard accuracy is unchanged, the model is learning nothing\n\n"
            "Probabilities and per-class loss can improve before predictions cross the classification threshold.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Training application | Structured program coordinating configuration, data, model, optimization, validation, and logging. |\n"
            "| `DataLoader` | PyTorch utility that batches and loads dataset samples, optionally in parallel worker processes. |\n"
            "| `Conv3d` | Convolution operating across depth, height, and width. |\n"
            "| Tail | Initial network layers adapting raw input. |\n"
            "| Backbone | Main feature-extraction body of a neural network. |\n"
            "| Head | Final layers converting learned features into task outputs. |\n"
            "| Receptive field | Region of the original input capable of influencing one deeper activation. |\n"
            "| Logit | Raw class score before softmax. |\n"
            "| Softmax probability | Normalized nonnegative class score with outputs summing to 1. |\n"
            "| Kaiming initialization | Weight initialization designed for stable signal propagation in ReLU-like networks. |\n"
            "| Momentum | SGD mechanism carrying part of previous update direction into later steps. |\n"
            "| Per-sample loss | Separate loss value retained for each item before reduction. |\n"
            "| Boolean mask | True/False tensor used to select a subset of values. |\n"
            "| Class imbalance | Strongly unequal sample counts between classes. |\n"
            "| False negative | Positive sample predicted as negative. |\n"
            "| `tqdm` | Progress-bar utility for long-running iterables. |\n"
            "| TensorBoard | Visualization tool for experiment metrics and trends. |\n"
            "| `SummaryWriter` | PyTorch interface for writing TensorBoard-compatible event data. |\n"
            "| Pinned memory | CPU memory arrangement that can improve host-to-GPU transfer efficiency. |\n"
            "| DataParallel | Simple single-machine wrapper for using multiple GPUs. |\n"
            "| DistributedDataParallel | PyTorch approach intended for more scalable distributed multi-GPU training. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "1. What does the chapter classify at this stage: malignancy or nodule status?\n"
            "2. Why is an early end-to-end baseline useful even when its quality is poor?\n"
            "3. Why does this project use a structured application instead of one short notebook loop?\n"
            "4. Why is the model moved to its device before optimizer creation in the source design?\n"
            "5. What optimizer and starting hyperparameters does the chapter use?\n"
            "6. What is the difference between DataParallel and DistributedDataParallel at a high level?\n"
            "7. What five dimensions does `Conv3d` expect?\n"
            "8. Why is the CT channel dimension equal to one?\n"
            "9. What does `num_workers` change in DataLoader?\n"
            "10. Why can pinned memory help CUDA training?\n"
            "11. What layers make up one `LunaBlock`?\n"
            "12. What is the receptive field of one `3×3×3` convolution?\n"
            "13. Why do two stacked `3×3×3` convolutions see a larger region?\n"
            "14. What does `MaxPool3d(2)` do to spatial dimensions?\n"
            "15. What are tail, backbone, and head?\n"
            "16. Why does `32×48×48` become `2×3×3` after four pooling stages?\n"
            "17. Where does the number `1152` come from?\n"
            "18. Why must backbone output be flattened before the linear head?\n"
            "19. What is the difference between logits and softmax probabilities?\n"
            "20. Why are logits used with `CrossEntropyLoss`?\n"
            "21. Why does initialization matter in a deep network?\n"
            "22. What does `model.train()` do conceptually?\n"
            "23. Why does the source use `reduction='none'` in cross-entropy?\n"
            "24. Why are metric tensors detached?\n"
            "25. Why should validation use `model.eval()` and `torch.no_grad()`?\n"
            "26. How do Boolean masks enable per-class metrics?\n"
            "27. What does `tqdm` add to a long training run?\n"
            "28. How can CPU and GPU utilization help identify a bottleneck?\n"
            "29. Why should expected dataset sample counts be checked before trusting a run?\n"
            "30. What does TensorBoard add beyond console logging?\n"
            "31. Why is 99.7% accuracy misleading in this dataset?\n"
            "32. What does zero positive-class accuracy reveal about the learned classifier?\n"
            "33. Why can positive loss decrease while positive accuracy stays at zero?\n"
            "34. Why are application-specific consequences of false negatives important when choosing metrics?\n"
            "35. What is the main failure the next chapter needs to address?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**A good training system does more than update weights. It feeds data efficiently, structures experiments, validates without "
            "changing the model, records enough detail to diagnose failures, and uses metrics that reflect the real task. In an imbalanced "
            "problem, a spectacular aggregate accuracy can hide total failure on the class that matters most.**\n"
        ),

        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "chapter-goal", "title": "The first end-to-end milestone", "order": 1},
            {"id": "application-structure", "title": "Structuring a larger training project", "order": 2},
            {"id": "cli-app", "title": "Reusable command-line application", "order": 3},
            {"id": "initialize-device", "title": "Device, model, and optimizer initialization", "order": 4},
            {"id": "multi-gpu", "title": "Multi-GPU approaches", "order": 5},
            {"id": "dataloader-role", "title": "DataLoader and 3D batch shapes", "order": 6},
            {"id": "dataloader-performance", "title": "Workers and pinned memory", "order": 7},
            {"id": "architecture-overview", "title": "3D CNN architecture overview", "order": 8},
            {"id": "luna-block", "title": "The LunaBlock", "order": 9},
            {"id": "receptive-field", "title": "3D receptive fields", "order": 10},
            {"id": "full-model", "title": "The full LunaModel", "order": 11},
            {"id": "flatten-head", "title": "Flattening into the classifier head", "order": 12},
            {"id": "logits-probabilities", "title": "Logits and probabilities", "order": 13},
            {"id": "initialization", "title": "Kaiming initialization", "order": 14},
            {"id": "training-loop", "title": "Training loop", "order": 15},
            {"id": "batch-loss", "title": "Per-sample batch loss", "order": 16},
            {"id": "metrics-buffer", "title": "Detailed per-sample metrics", "order": 17},
            {"id": "validation-loop", "title": "Read-only validation", "order": 18},
            {"id": "per-class-metrics", "title": "Per-class metrics", "order": 19},
            {"id": "boolean-masking", "title": "Boolean masking", "order": 20},
            {"id": "tqdm", "title": "Progress monitoring with tqdm", "order": 21},
            {"id": "resource-monitoring", "title": "CPU and GPU bottleneck monitoring", "order": 22},
            {"id": "dataset-count-check", "title": "Dataset completeness checks", "order": 23},
            {"id": "tensorboard", "title": "TensorBoard metric visualization", "order": 24},
            {"id": "tensorboard-hygiene", "title": "Experiment-log hygiene", "order": 25},
            {"id": "accuracy-trap", "title": "The misleading 99.7% accuracy", "order": 26},
            {"id": "class-imbalance", "title": "Class imbalance", "order": 27},
            {"id": "false-negative-cost", "title": "Application cost of false negatives", "order": 28},
            {"id": "loss-signal", "title": "Loss can improve before accuracy", "order": 29},
            {"id": "chapter-blueprint", "title": "Reusable training-system blueprint", "order": 30},
        ],
    },

    "exercises": [
        {
            "id": "M12.L01.EX01",
            "title": "Inspect DataLoader Throughput and Batch Structure",
            "lesson_code": "M12.L01",
            "section_id": "dataloader-performance",
            "placement": "after_section",
            "description": "Connect Dataset samples to batched 3D tensors and measure loader behavior.",
            "instructions": (
                "Wrap a `LunaDataset` (or a synthetic replacement with the same return shapes) in DataLoaders using "
                "`num_workers=0`, `1`, and `2`. For each configuration, inspect one batch and confirm the input shape "
                "is `N×1×32×48×48`. Time a fixed number of batches. Record batch size, worker count, elapsed time, and "
                "whether CUDA pinned memory is enabled. Explain why increasing workers does not guarantee indefinite speedup."
            ),
            "expected_output": "Batch-shape verification, timing table, and a short throughput analysis.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["dataloader", "batching", "num-workers", "performance"],
        },
        {
            "id": "M12.L01.EX02",
            "title": "Trace the 3D CNN Shapes and Parameters",
            "lesson_code": "M12.L01",
            "section_id": "full-model",
            "placement": "after_section",
            "description": "Verify the dimensions flowing through LunaModel.",
            "instructions": (
                "Implement the four-block LunaModel using base channel count 8. Pass a synthetic batch shaped "
                "`(2,1,32,48,48)` through the model while printing the shape after BatchNorm3d, every block, "
                "flattening, and the final linear layer. Confirm that the final backbone tensor is "
                "`(2,64,2,3,3)` and flattening produces `(2,1152)`. Count total trainable parameters."
            ),
            "expected_output": "Working model, complete tensor-shape trace, and total parameter count.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["conv3d", "shape-reasoning", "pooling", "parameter-counting"],
        },
        {
            "id": "M12.L01.EX03",
            "title": "Prove That Validation Is Read-Only",
            "lesson_code": "M12.L01",
            "section_id": "validation-loop",
            "placement": "after_section",
            "description": "Verify correct training and validation mode behavior.",
            "instructions": (
                "Create a small model containing BatchNorm3d. Save copies of all trainable parameters before validation. "
                "Run several validation batches using `model.eval()` inside `torch.no_grad()` and do not call the optimizer. "
                "Compare parameters before and after and confirm that they are unchanged. Then explain separately what "
                "`eval()` changes and what `no_grad()` changes."
            ),
            "expected_output": "Code proving parameter stability plus a clear explanation of evaluation mode versus gradient tracking.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["validation", "eval-mode", "no-grad", "batch-normalization"],
        },
        {
            "id": "M12.L01.EX04",
            "title": "Expose the Accuracy Trap",
            "lesson_code": "M12.L01",
            "section_id": "loss-signal",
            "placement": "after_section",
            "description": "Demonstrate how extreme imbalance can make a useless classifier look excellent.",
            "instructions": (
                "Create 10,000 binary labels with 9,970 negatives and 30 positives. Predict every sample as negative. "
                "Compute overall accuracy, negative-class accuracy, and positive-class accuracy. Then create predicted "
                "positive probabilities that move from 0.01 to 0.20 for the positive samples while remaining below 0.5. "
                "Explain why thresholded positive accuracy remains zero even though positive cross-entropy loss can improve."
            ),
            "expected_output": "Metric calculations showing high overall accuracy, zero positive accuracy, and a written loss-versus-threshold explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["class-imbalance", "accuracy", "per-class-metrics", "cross-entropy"],
        },
        {
            "id": "M12.L01.EX05",
            "title": "Design an Observability Plan for Training",
            "lesson_code": "M12.L01",
            "section_id": "chapter-blueprint",
            "placement": "after_section",
            "description": "Turn the chapter's logging infrastructure into a reusable debugging plan.",
            "instructions": (
                "Design a metric/logging table for this training application. Include at least: overall loss, positive loss, "
                "negative loss, overall accuracy, positive accuracy, negative accuracy, samples processed, iteration rate, "
                "dataset sample counts, and run identifier. For each metric, state where it is collected, whether it belongs "
                "in console logs, TensorBoard, or both, and what failure it could reveal. Finally, identify which metric would "
                "have exposed the chapter's 99.7%-accuracy failure fastest."
            ),
            "expected_output": "A structured observability table and a justified diagnosis priority.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["metrics", "tensorboard", "logging", "debugging", "ml-observability"],
        },
    ],

    "quiz": {
        "id": "M12.L01.QZ01",
        "title": "Training a CT Classification Model — Knowledge Check",
        "lesson_code": "M12.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M12.L01.Q01",
                "section_id": "chapter-goal",
                "question": "What is the classifier trying to distinguish in this chapter?",
                "options": [
                    "Malignant versus benign cancer directly",
                    "Nodule versus non-nodule candidates",
                    "CT versus MRI scans",
                    "Training versus validation patients",
                ],
                "correct": 1,
                "explanation": "This chapter first classifies candidates as nodules or non-nodules; malignancy comes later.",
            },
            {
                "id": "M12.L01.Q02",
                "section_id": "dataloader-role",
                "question": "What shape convention does `nn.Conv3d` expect for batched input?",
                "options": [
                    "`N×C×D×H×W`",
                    "`N×D×H×W×C`",
                    "`C×N×H×W`",
                    "`N×F` only",
                ],
                "correct": 0,
                "explanation": "3D convolution uses batch, channel, depth, height, and width dimensions.",
            },
            {
                "id": "M12.L01.Q03",
                "section_id": "dataloader-performance",
                "question": "What does `num_workers` primarily control in a DataLoader?",
                "options": [
                    "The number of GPU layers",
                    "The number of output classes",
                    "How many worker processes can prepare/load data in parallel",
                    "The number of validation epochs",
                ],
                "correct": 2,
                "explanation": "Multiple workers can prepare batches while the model processes earlier ones.",
            },
            {
                "id": "M12.L01.Q04",
                "section_id": "architecture-overview",
                "question": "Which network component performs most of the repeated feature extraction?",
                "options": [
                    "Tail",
                    "Optimizer",
                    "Metric buffer",
                    "Backbone",
                ],
                "correct": 3,
                "explanation": "The backbone contains the repeated convolutional blocks doing most feature extraction.",
            },
            {
                "id": "M12.L01.Q05",
                "section_id": "luna-block",
                "question": "What is the order inside one LunaBlock?",
                "options": [
                    "Conv3d → ReLU → Conv3d → ReLU → MaxPool3d",
                    "Linear → Softmax → MaxPool3d",
                    "BatchNorm → CrossEntropy → SGD",
                    "Conv2d → ReLU → Flatten",
                ],
                "correct": 0,
                "explanation": "Each block uses two 3D convolutions with activations followed by 3D max pooling.",
            },
            {
                "id": "M12.L01.Q06",
                "section_id": "full-model",
                "question": "Why does the source's final backbone output flatten to 1152 features per sample?",
                "options": [
                    "There are 1152 CT scans.",
                    "`64 × 2 × 3 × 3 = 1152` after four blocks.",
                    "The batch size is fixed at 1152.",
                    "Softmax creates 1152 probabilities.",
                ],
                "correct": 1,
                "explanation": "The final tensor has 64 channels and spatial size 2×3×3.",
            },
            {
                "id": "M12.L01.Q07",
                "section_id": "logits-probabilities",
                "question": "Which model output should be passed to `nn.CrossEntropyLoss()`?",
                "options": [
                    "Thresholded class labels",
                    "Softmax probabilities",
                    "Raw logits",
                    "Series UIDs",
                ],
                "correct": 2,
                "explanation": "CrossEntropyLoss expects raw class logits.",
            },
            {
                "id": "M12.L01.Q08",
                "section_id": "initialization",
                "question": "Why does the model use Kaiming-style initialization?",
                "options": [
                    "To create validation labels",
                    "To choose the DataLoader worker count",
                    "To replace ReLU",
                    "To keep activation/gradient scales better behaved in a ReLU-based network",
                ],
                "correct": 3,
                "explanation": "Initialization helps prevent early signal scales from becoming unusably large or small.",
            },
            {
                "id": "M12.L01.Q09",
                "section_id": "training-loop",
                "question": "What should happen before `loss.backward()` on each training batch?",
                "options": [
                    "Clear previously accumulated parameter gradients",
                    "Switch the model to evaluation mode",
                    "Disable autograd",
                    "Convert logits to hard labels",
                ],
                "correct": 0,
                "explanation": "Gradients accumulate by default, so old gradients must be cleared before the new backward pass.",
            },
            {
                "id": "M12.L01.Q10",
                "section_id": "batch-loss",
                "question": "Why use `reduction='none'` for cross-entropy in this chapter?",
                "options": [
                    "To prevent all gradients",
                    "To preserve one loss value per sample for detailed metrics",
                    "To avoid moving tensors to CUDA",
                    "To create probability outputs",
                ],
                "correct": 1,
                "explanation": "Per-sample losses allow later class-specific aggregation and debugging.",
            },
            {
                "id": "M12.L01.Q11",
                "section_id": "metrics-buffer",
                "question": "Why are values detached before storing them in the metrics tensor?",
                "options": [
                    "To increase the number of classes",
                    "To move every metric to the GPU",
                    "Metrics do not need to retain the autograd graph",
                    "To change positive labels into negative labels",
                ],
                "correct": 2,
                "explanation": "Detaching prevents unnecessary graph retention for logging-only values.",
            },
            {
                "id": "M12.L01.Q12",
                "section_id": "validation-loop",
                "question": "Which combination correctly describes validation?",
                "options": [
                    "`train()` + backward + optimizer step",
                    "`eval()` + optimizer step",
                    "`no_grad()` + backward",
                    "`eval()` + `no_grad()` + no parameter update",
                ],
                "correct": 3,
                "explanation": "Validation is read-only and should neither build training graphs nor update model state through the optimizer.",
            },
            {
                "id": "M12.L01.Q13",
                "section_id": "per-class-metrics",
                "question": "Why are positive and negative metrics calculated separately?",
                "options": [
                    "Aggregate performance can hide severe failure on one class.",
                    "CrossEntropyLoss requires separate models per class.",
                    "DataLoader cannot batch different labels together.",
                    "Softmax only works on one class at a time.",
                ],
                "correct": 0,
                "explanation": "Per-class analysis reveals failures hidden by an aggregate score.",
            },
            {
                "id": "M12.L01.Q14",
                "section_id": "tensorboard",
                "question": "What is the main benefit of TensorBoard in this chapter?",
                "options": [
                    "It replaces the training loop.",
                    "It makes metric trends across training runs easier to inspect visually.",
                    "It balances the classes automatically.",
                    "It loads CT scans instead of DataLoader.",
                ],
                "correct": 1,
                "explanation": "Trend visualization makes behavior and failures easier to interpret than isolated console numbers.",
            },
            {
                "id": "M12.L01.Q15",
                "section_id": "accuracy-trap",
                "question": "Why can predicting every candidate as non-nodule still produce about 99.7% overall accuracy?",
                "options": [
                    "Softmax rounds every probability to one.",
                    "The validation set contains no positives.",
                    "Positive nodules are only a tiny fraction of the candidate dataset.",
                    "Cross-entropy ignores positive samples.",
                ],
                "correct": 2,
                "explanation": "Extreme class imbalance lets a majority-only strategy score very highly overall.",
            },
            {
                "id": "M12.L01.Q16",
                "section_id": "loss-signal",
                "question": "How can positive-class loss improve while positive-class accuracy remains zero?",
                "options": [
                    "Accuracy is always random.",
                    "Loss ignores probabilities.",
                    "Validation updates the weights after every batch.",
                    "The model's probabilities can move toward the correct class without crossing the classification threshold yet.",
                ],
                "correct": 3,
                "explanation": "Continuous probabilities can improve before the hard thresholded decision changes.",
            },
            {
                "id": "M12.L01.Q17",
                "section_id": "chapter-blueprint",
                "type": "open",
                "question": (
                    "A training run reports 99.8% validation accuracy, 100% non-nodule accuracy, and 0% nodule accuracy. "
                    "Explain why the model is failing despite the aggregate score. Then describe which parts of the chapter's "
                    "training and metrics infrastructure let you discover and investigate that failure."
                ),
            },
        ],
        "passing_score": 70,
    },
}
