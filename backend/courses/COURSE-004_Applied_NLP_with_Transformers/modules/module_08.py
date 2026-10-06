"""M01.L06 — Making Transformers Efficient in Production.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 8.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L06"
MODULE_ORDER = 1
MODULE_TITLE = "Transformer Foundations"
MODULE_DESCRIPTION = (
    "Learn how to make transformer models practical for production by measuring "
    "quality, latency, and memory, then applying distillation, quantization, ONNX "
    "Runtime optimization, and pruning."
)

SOURCE_CHAPTER = 8
SOURCE_PAGES = "Chapter 8"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Making Transformers Efficient in Production",
    "slug": "applied-nlp-transformers-m01-l06-efficient-transformers-production",
    "description": (
        "Optimize transformer inference systematically by benchmarking accuracy, latency, "
        "and model size, then applying knowledge distillation, quantization, ONNX Runtime, "
        "and pruning while measuring the trade-offs."
    ),
    "order": 6,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 2.0,
    "skill_tags": [
        "transformer-optimization",
        "production-inference",
        "knowledge-distillation",
        "quantization",
        "onnx",
        "onnx-runtime",
        "pruning",
        "latency",
        "model-compression",
        "benchmarking",
        "module-01",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
    ],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Making Transformers Efficient in Production",

        "content": (
            "# Making Transformers Efficient in Production\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L06  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 8. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why accuracy alone is not enough for production ML.\n"
            "- Benchmark a transformer on model quality, latency, and memory footprint.\n"
            "- Explain why repeated latency measurements are more useful than one timing run.\n"
            "- Explain teacher-student knowledge distillation and soft targets.\n"
            "- Describe the roles of temperature, KL divergence, and the mixing coefficient "
            "in a distillation loss.\n"
            "- Explain why DistilBERT is a sensible student for a BERT teacher.\n"
            "- Use hyperparameter search to tune distillation settings.\n"
            "- Explain FP32-to-INT8 quantization intuitively.\n"
            "- Distinguish dynamic, static, and quantization-aware training approaches.\n"
            "- Explain how ONNX and ONNX Runtime can optimize inference graphs.\n"
            "- Explain magnitude pruning and movement pruning.\n"
            "- Compare optimization techniques using measured production trade-offs.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. A great model can still be a bad production model\n"
            "\n"
            "During model development, it is tempting to optimize only for the task metric: "
            "accuracy, F1, ROUGE, BLEU, or another quality score.\n"
            "\n"
            "Production adds other constraints.\n"
            "\n"
            "A model can be highly accurate and still be unusable if:\n"
            "\n"
            "- every prediction is too slow,\n"
            "- the model consumes too much RAM,\n"
            "- the model file is too large for the target device,\n"
            "- serving costs become too high,\n"
            "- the application must respond in real time.\n"
            "\n"
            "The chapter focuses on four complementary techniques:\n"
            "\n"
            "1. **Knowledge distillation**\n"
            "2. **Quantization**\n"
            "3. **ONNX / ONNX Runtime graph optimization**\n"
            "4. **Pruning**\n"
            "\n"
            "These methods do not all solve the same problem in the same way.\n"
            "\n"
            "| Technique | Main idea |\n"
            "|---|---|\n"
            "| Distillation | Train a smaller model to imitate a larger model |\n"
            "| Quantization | Use lower-precision numerical representations |\n"
            "| ONNX Runtime | Optimize and execute a standardized computation graph efficiently |\n"
            "| Pruning | Remove less important weights/connections to create sparsity |\n"
            "\n"
            "[[IMAGE_NEEDED: Transformer production optimization overview | "
            "A large accurate transformer on the left and four optimization paths labeled "
            "distillation, quantization, ONNX Runtime, and pruning leading toward a smaller/"
            "faster deployment model | "
            "Learner should notice that several techniques can be combined rather than treated "
            "as mutually exclusive choices]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Case study: intent detection for a real-time assistant\n"
            "\n"
            "The chapter uses an intent classifier as the running production example.\n"
            "\n"
            "A customer might write:\n"
            "\n"
            "```text\n"
            "I'd like to rent a vehicle in Paris for two weeks.\n"
            "```\n"
            "\n"
            "The system should map the query to an intent such as:\n"
            "\n"
            "```text\n"
            "car_rental\n"
            "```\n"
            "\n"
            "It must also recognize **out-of-scope** requests that do not match any supported "
            "intent, rather than confidently returning an unrelated action.\n"
            "\n"
            "The benchmark uses the CLINC150 dataset, which contains many intent classes plus "
            "an out-of-scope class.\n"
            "\n"
            "The chapter begins with a fine-tuned BERT-base classifier as the production-quality "
            "reference model.\n"
            "\n"
            "This case study is useful because a conversational assistant cares strongly about "
            "latency: a correct answer that arrives too slowly still creates a poor user experience.\n"
            "\n"
            "[[IMAGE_NEEDED: In-scope versus out-of-scope intent detection | "
            "Three small chat examples: one correctly routed in-scope query, one out-of-scope "
            "query incorrectly forced into a known intent, and one out-of-scope query correctly "
            "sent to a fallback response | "
            "Learner should notice that production classification includes safe handling of "
            "unknown requests, not only predicting known intents]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Benchmark before optimizing anything\n"
            "\n"
            "Optimization without a benchmark is guesswork.\n"
            "\n"
            "The chapter tracks three core quantities:\n"
            "\n"
            "### 1. Model performance\n"
            "\n"
            "How well does the model solve the actual task on a representative test set?\n"
            "\n"
            "### 2. Latency\n"
            "\n"
            "How long does one prediction take under the deployment conditions we care about?\n"
            "\n"
            "### 3. Memory / model size\n"
            "\n"
            "How much storage and memory does the model require?\n"
            "\n"
            "These form the central production trade-off:\n"
            "\n"
            "```text\n"
            "quality\n"
            "  ▲\n"
            "  │\n"
            "  │      useful operating region\n"
            "  │\n"
            "  └────────────────────────► speed / compactness\n"
            "```\n"
            "\n"
            "A simple benchmark class can collect the same measurements for every model:\n"
            "\n"
            "```python\n"
            "class PerformanceBenchmark:\n"
            "    def __init__(self, pipeline, dataset, optim_type='baseline'):\n"
            "        self.pipeline = pipeline\n"
            "        self.dataset = dataset\n"
            "        self.optim_type = optim_type\n"
            "\n"
            "    def compute_accuracy(self):\n"
            "        ...\n"
            "\n"
            "    def compute_size(self):\n"
            "        ...\n"
            "\n"
            "    def time_pipeline(self):\n"
            "        ...\n"
            "\n"
            "    def run_benchmark(self):\n"
            "        metrics = {}\n"
            "        metrics.update(self.compute_size())\n"
            "        metrics.update(self.time_pipeline())\n"
            "        metrics.update(self.compute_accuracy())\n"
            "        return metrics\n"
            "```\n"
            "\n"
            "The exact API is less important than the discipline: **every optimization must be "
            "measured using the same benchmark.**\n"
            "\n"
            "{{exercise:M01.L06.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Measure latency correctly\n"
            "\n"
            "One timing measurement is unreliable.\n"
            "\n"
            "System scheduling, CPU state, cache behavior, and other background effects can "
            "make individual timings noisy.\n"
            "\n"
            "The chapter therefore:\n"
            "\n"
            "1. performs warm-up predictions,\n"
            "2. measures many inference runs,\n"
            "3. reports the mean latency,\n"
            "4. reports the standard deviation.\n"
            "\n"
            "```python\n"
            "from time import perf_counter\n"
            "import numpy as np\n"
            "\n"
            "def measure_latency(pipe, query):\n"
            "    latencies = []\n"
            "\n"
            "    for _ in range(10):\n"
            "        _ = pipe(query)\n"
            "\n"
            "    for _ in range(100):\n"
            "        start = perf_counter()\n"
            "        _ = pipe(query)\n"
            "        latencies.append(perf_counter() - start)\n"
            "\n"
            "    return {\n"
            "        'mean_ms': 1000 * np.mean(latencies),\n"
            "        'std_ms': 1000 * np.std(latencies),\n"
            "    }\n"
            "```\n"
            "\n"
            "The chapter also warns that latency is hardware-dependent and depends on input "
            "length. The most useful comparison is therefore often **relative performance on "
            "the same hardware using representative production inputs**.\n"
            "\n"
            "### Baseline result from the chapter\n"
            "\n"
            "| Model | Size | Avg. latency | Test accuracy |\n"
            "|---|---:|---:|---:|\n"
            "| BERT baseline | 418.16 MB | 54.20 ms | 0.867 |\n"
            "\n"
            "Now we have something concrete to beat.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 5
            # ----------------------------------------------------------------

            "## 5. Knowledge distillation: teacher and student\n"
            "\n"
            "Knowledge distillation trains a smaller **student** model to imitate a larger, "
            "better-performing **teacher** model.\n"
            "\n"
            "The obvious information available to the student is the ground-truth label.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "true label = car_rental\n"
            "```\n"
            "\n"
            "But the teacher can provide richer information:\n"
            "\n"
            "```text\n"
            "car_rental       0.70\n"
            "travel_booking   0.18\n"
            "car_payment      0.07\n"
            "other            0.05\n"
            "```\n"
            "\n"
            "The secondary probabilities reveal relationships learned by the teacher. "
            "The chapter calls this hidden information **dark knowledge**.\n"
            "\n"
            "A student can therefore learn from two signals:\n"
            "\n"
            "```text\n"
            "ground-truth labels\n"
            "       +\n"
            "teacher probability distribution\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Teacher-student knowledge distillation | "
            "One input branching into a large teacher and smaller student; teacher produces "
            "soft class probabilities, student produces its own probabilities, and the final "
            "student loss combines label loss with teacher-student distribution matching | "
            "Learner should notice that the teacher guides training but is not needed for "
            "student inference after training]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 6
            # ----------------------------------------------------------------

            "## 6. Temperature, KL divergence, and the distillation loss\n"
            "\n"
            "A confident teacher may produce a probability distribution that is almost one-hot. "
            "That hides useful relationships among the less probable classes.\n"
            "\n"
            "Distillation therefore uses a **temperature** `T` to soften the distributions.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "soft_probs = softmax(logits / T)\n"
            "```\n"
            "\n"
            "When `T` increases, the distribution becomes softer and exposes more information "
            "about the teacher's relative preference among classes.\n"
            "\n"
            "We then compare teacher and student distributions with **KL divergence**.\n"
            "\n"
            "The overall student objective combines:\n"
            "\n"
            "- normal cross-entropy against the true labels,\n"
            "- distillation loss against the teacher distribution.\n"
            "\n"
            "A simplified view is:\n"
            "\n"
            "```text\n"
            "student_loss\n"
            "=\n"
            "alpha × label_loss\n"
            "+\n"
            "(1 - alpha) × distillation_loss\n"
            "```\n"
            "\n"
            "`alpha` controls how much the student trusts the ordinary labels versus the "
            "teacher signal.\n"
            "\n"
            "[[IMAGE_NEEDED: Hard labels versus soft teacher probabilities | "
            "Three side-by-side bar charts: one-hot hard label, normal teacher softmax, and "
            "temperature-softened teacher probabilities | "
            "Learner should notice that higher temperature reveals relative probabilities "
            "among non-winning classes]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 7
            # ----------------------------------------------------------------

            "## 7. Implement a custom distillation trainer\n"
            "\n"
            "The chapter extends the standard training loop by computing both teacher and "
            "student outputs for each training batch.\n"
            "\n"
            "A simplified version is:\n"
            "\n"
            "```python\n"
            "import torch\n"
            "import torch.nn as nn\n"
            "import torch.nn.functional as F\n"
            "from transformers import Trainer\n"
            "\n"
            "class DistillationTrainer(Trainer):\n"
            "    def __init__(self, *args, teacher_model=None, **kwargs):\n"
            "        super().__init__(*args, **kwargs)\n"
            "        self.teacher_model = teacher_model\n"
            "\n"
            "    def compute_loss(self, model, inputs, return_outputs=False):\n"
            "        student_outputs = model(**inputs)\n"
            "        student_logits = student_outputs.logits\n"
            "        label_loss = student_outputs.loss\n"
            "\n"
            "        with torch.no_grad():\n"
            "            teacher_logits = self.teacher_model(**inputs).logits\n"
            "\n"
            "        T = self.args.temperature\n"
            "\n"
            "        kd_loss = nn.KLDivLoss(reduction='batchmean')(\n"
            "            F.log_softmax(student_logits / T, dim=-1),\n"
            "            F.softmax(teacher_logits / T, dim=-1),\n"
            "        ) * (T ** 2)\n"
            "\n"
            "        loss = (\n"
            "            self.args.alpha * label_loss\n"
            "            + (1 - self.args.alpha) * kd_loss\n"
            "        )\n"
            "\n"
            "        return (loss, student_outputs) if return_outputs else loss\n"
            "```\n"
            "\n"
            "The teacher forward pass does not need gradients, so it is wrapped in "
            "`torch.no_grad()`.\n"
            "\n"
            "### Choosing the student\n"
            "\n"
            "The chapter recommends choosing a smaller model of a similar architecture when "
            "possible. With a BERT teacher, **DistilBERT** is a natural student.\n"
            "\n"
            "A student fine-tuned without teacher distillation already gives a strong speed/"
            "size improvement in the chapter:\n"
            "\n"
            "| Model | Size | Avg. latency | Test accuracy |\n"
            "|---|---:|---:|---:|\n"
            "| BERT baseline | 418.16 MB | 54.20 ms | 0.867 |\n"
            "| DistilBERT | 255.89 MB | 27.53 ms | 0.858 |\n"
            "\n"
            "That is roughly half the latency for only a modest accuracy reduction.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 8
            # ----------------------------------------------------------------

            "## 8. Tune distillation instead of guessing\n"
            "\n"
            "Distillation introduces important hyperparameters such as:\n"
            "\n"
            "- `alpha`,\n"
            "- temperature,\n"
            "- number of training epochs.\n"
            "\n"
            "Rather than choosing them manually, the chapter uses **Optuna** to search for "
            "a better combination.\n"
            "\n"
            "```python\n"
            "def hp_space(trial):\n"
            "    return {\n"
            "        'num_train_epochs': trial.suggest_int(\n"
            "            'num_train_epochs', 5, 10\n"
            "        ),\n"
            "        'alpha': trial.suggest_float('alpha', 0, 1),\n"
            "        'temperature': trial.suggest_int('temperature', 2, 20),\n"
            "    }\n"
            "```\n"
            "\n"
            "In the chapter's search, a strong run uses approximately:\n"
            "\n"
            "```text\n"
            "epochs      = 10\n"
            "alpha       = 0.125\n"
            "temperature = 7\n"
            "```\n"
            "\n"
            "After training with the distillation signal, the resulting student benchmark is:\n"
            "\n"
            "| Model | Size | Avg. latency | Test accuracy |\n"
            "|---|---:|---:|---:|\n"
            "| Distilled DistilBERT | 255.89 MB | 25.96 ms | 0.868 |\n"
            "\n"
            "The student now matches the chapter's BERT baseline test accuracy while remaining "
            "much smaller and faster.\n"
            "\n"
            "This is the first major lesson of the chapter:\n"
            "\n"
            "> **A smaller model does not necessarily have to accept a large quality loss if "
            "it is trained carefully.**\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 9
            # ----------------------------------------------------------------

            "## 9. Quantization: use fewer bits for the numbers\n"
            "\n"
            "Distillation changes the model architecture/size. Quantization attacks a different "
            "source of cost: **numerical precision**.\n"
            "\n"
            "A typical model stores many weights as 32-bit floating-point values (`FP32`).\n"
            "\n"
            "Quantization maps those values into a lower-precision representation such as "
            "8-bit integers (`INT8`).\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "FP32 weight values\n"
            "   ↓ map using scale + zero point\n"
            "INT8 integer levels\n"
            "```\n"
            "\n"
            "Why can this help?\n"
            "\n"
            "- INT8 uses fewer bits per value.\n"
            "- Weight storage can become much smaller.\n"
            "- Integer arithmetic can be faster on supported hardware.\n"
            "- Less data may need to move through memory.\n"
            "\n"
            "The trade-off is that many floating-point values must map to the same integer "
            "level, introducing quantization error.\n"
            "\n"
            "[[IMAGE_NEEDED: FP32 to INT8 quantization | "
            "A continuous number line of floating-point weight values mapped onto a smaller "
            "set of discrete INT8 levels using a scale and zero point | "
            "Learner should notice that quantization saves precision by grouping nearby "
            "floating-point values into shared integer levels]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 10
            # ----------------------------------------------------------------

            "## 10. Dynamic, static, and quantization-aware approaches\n"
            "\n"
            "The chapter describes three common quantization strategies.\n"
            "\n"
            "### Dynamic quantization\n"
            "\n"
            "- model weights are quantized ahead of inference,\n"
            "- activations are quantized dynamically during inference,\n"
            "- simplest of the three approaches in the chapter,\n"
            "- useful for transformer inference on CPUs.\n"
            "\n"
            "### Static quantization\n"
            "\n"
            "- uses representative data to estimate activation ranges ahead of deployment,\n"
            "- stores a fixed quantization scheme,\n"
            "- avoids some runtime conversion overhead,\n"
            "- requires an extra calibration stage.\n"
            "\n"
            "### Quantization-aware training\n"
            "\n"
            "- simulates quantization effects during training,\n"
            "- lets the model adapt to the reduced precision,\n"
            "- can better preserve quality when quantization error matters.\n"
            "\n"
            "For the NLP transformer case study, the chapter focuses on **dynamic quantization**.\n"
            "\n"
            "In PyTorch, the idea is concise:\n"
            "\n"
            "```python\n"
            "from torch.quantization import quantize_dynamic\n"
            "from torch import nn\n"
            "\n"
            "model_quantized = quantize_dynamic(\n"
            "    model,\n"
            "    {nn.Linear},\n"
            "    dtype=torch.qint8,\n"
            ")\n"
            "```\n"
            "\n"
            "The chapter's benchmark becomes:\n"
            "\n"
            "| Model | Size | Avg. latency | Test accuracy |\n"
            "|---|---:|---:|---:|\n"
            "| Distilled model | 255.89 MB | 25.96 ms | 0.868 |\n"
            "| Distillation + PyTorch quantization | 132.40 MB | 12.54 ms | 0.876 |\n"
            "\n"
            "The key practice is not to assume that quantization is safe—**measure the task "
            "metric after quantizing.**\n"
            "\n"
            "{{exercise:M01.L06.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 11
            # ----------------------------------------------------------------

            "## 11. ONNX: represent the model as a standardized graph\n"
            "\n"
            "**ONNX** is an open model representation format built around standardized "
            "operators and a computational graph.\n"
            "\n"
            "Instead of thinking only in terms of a Python model class, ONNX represents "
            "inference as nodes such as:\n"
            "\n"
            "```text\n"
            "Input\n"
            "  ↓\n"
            "MatMul\n"
            "  ↓\n"
            "Add\n"
            "  ↓\n"
            "Activation\n"
            "  ↓\n"
            "...\n"
            "```\n"
            "\n"
            "This intermediate representation helps separate model execution from the original "
            "training framework.\n"
            "\n"
            "[[IMAGE_NEEDED: Simplified ONNX computational graph | "
            "A small directed graph of model operators such as input, MatMul, Add, LayerNorm, "
            "and output, shown as connected nodes | "
            "Learner should notice that ONNX describes the inference computation as a graph "
            "of standardized operations rather than a high-level Python model class]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 12
            # ----------------------------------------------------------------

            "## 12. ONNX Runtime: optimize and execute the graph\n"
            "\n"
            "ONNX Runtime (ORT) is an inference engine for ONNX graphs.\n"
            "\n"
            "The chapter highlights graph optimizations such as:\n"
            "\n"
            "- **operator fusion** — combine operations so intermediate results do not need "
            "to be moved around unnecessarily,\n"
            "- **constant folding** — evaluate constant expressions ahead of runtime,\n"
            "- optimized execution providers for specific hardware.\n"
            "\n"
            "A useful mental model is:\n"
            "\n"
            "```text\n"
            "trained PyTorch model\n"
            "       ↓ export\n"
            "ONNX graph\n"
            "       ↓ optimize\n"
            "ONNX Runtime\n"
            "       ↓\n"
            "faster inference backend\n"
            "```\n"
            "\n"
            "The chapter's distilled ONNX model benchmark is:\n"
            "\n"
            "| Model | Size | Avg. latency | Test accuracy |\n"
            "|---|---:|---:|---:|\n"
            "| Distillation + ORT | 255.88 MB | 21.02 ms | 0.868 |\n"
            "\n"
            "The model size stays almost the same, but graph/runtime optimization improves "
            "latency relative to the ordinary distilled model.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 13
            # ----------------------------------------------------------------

            "## 13. Combine ONNX Runtime and quantization\n"
            "\n"
            "Production optimizations can be stacked.\n"
            "\n"
            "The chapter dynamically quantizes the exported ONNX model:\n"
            "\n"
            "```python\n"
            "from onnxruntime.quantization import quantize_dynamic, QuantType\n"
            "\n"
            "quantize_dynamic(\n"
            "    'onnx/model.onnx',\n"
            "    'onnx/model.quant.onnx',\n"
            "    weight_type=QuantType.QInt8,\n"
            ")\n"
            "```\n"
            "\n"
            "The resulting benchmark in the chapter is:\n"
            "\n"
            "| Model | Size | Avg. latency | Test accuracy |\n"
            "|---|---:|---:|---:|\n"
            "| BERT baseline | 418.16 MB | 54.20 ms | 0.867 |\n"
            "| Distillation | 255.89 MB | 25.96 ms | 0.868 |\n"
            "| Distillation + PyTorch quantization | 132.40 MB | 12.54 ms | 0.876 |\n"
            "| Distillation + ORT | 255.88 MB | 21.02 ms | 0.868 |\n"
            "| Distillation + ORT quantization | 64.20 MB | 9.24 ms | 0.877 |\n"
            "\n"
            "The chapter's best measured configuration is dramatically smaller and faster "
            "than the starting BERT baseline while retaining similar task quality.\n"
            "\n"
            "[[IMAGE_NEEDED: Production optimization benchmark trade-off | "
            "A scatter plot with average latency on the x-axis and accuracy on the y-axis, "
            "bubble size representing model size, containing the BERT baseline, distilled "
            "model, quantized model, ORT model, and ORT-quantized model using the chapter's "
            "benchmark values | "
            "Learner should notice that the optimized models move toward lower latency and "
            "smaller size without a large accuracy penalty]]\n"
            "\n"
            "The exact latency numbers are hardware-specific. The important result is the "
            "relative movement under a consistent benchmark.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 14
            # ----------------------------------------------------------------

            "## 14. Pruning: make the network sparse\n"
            "\n"
            "Quantization keeps the same basic network but stores numbers with fewer bits.\n"
            "\n"
            "Pruning tries to remove some connections entirely.\n"
            "\n"
            "The result is a **sparse model** with many zero-valued weights.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "dense weights\n"
            "● ● ● ● ●\n"
            "● ● ● ● ●\n"
            "● ● ● ● ●\n"
            "\n"
            "after pruning\n"
            "● · · ● ·\n"
            "· ● · · ●\n"
            "● · · · ·\n"
            "```\n"
            "\n"
            "A pruning method needs some definition of **importance** so it can decide which "
            "weights to keep and which to mask.\n"
            "\n"
            "[[IMAGE_NEEDED: Dense network versus pruned sparse network | "
            "Two small neural network diagrams side by side, one with dense connections and "
            "one with many connections removed | "
            "Learner should notice that pruning reduces the number of active nonzero "
            "connections rather than merely reducing numerical precision]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 15
            # ----------------------------------------------------------------

            "## 15. Magnitude pruning versus movement pruning\n"
            "\n"
            "### Magnitude pruning\n"
            "\n"
            "Magnitude pruning treats small-magnitude weights as less important.\n"
            "\n"
            "A common process is:\n"
            "\n"
            "```text\n"
            "train model\n"
            "   ↓\n"
            "remove low-magnitude weights\n"
            "   ↓\n"
            "retrain\n"
            "   ↓\n"
            "prune more\n"
            "```\n"
            "\n"
            "The chapter discusses gradually increasing sparsity rather than removing a huge "
            "fraction of weights at once.\n"
            "\n"
            "A limitation in transfer learning is that weight magnitude primarily reflects "
            "what happened during pretraining; a small weight is not guaranteed to be "
            "unimportant for the downstream task.\n"
            "\n"
            "### Movement pruning\n"
            "\n"
            "Movement pruning instead learns importance scores during fine-tuning.\n"
            "\n"
            "Its intuition is to preserve weights whose training movement indicates they are "
            "becoming important for the downstream task.\n"
            "\n"
            "This makes the importance criterion more closely tied to fine-tuning behavior "
            "instead of only the current absolute weight size.\n"
            "\n"
            "[[IMAGE_NEEDED: Magnitude versus movement pruning | "
            "A side-by-side conceptual comparison where magnitude pruning ranks weights by "
            "absolute size and movement pruning ranks them using learned movement/importance "
            "scores during fine-tuning | "
            "Learner should understand that the two methods answer 'which weights matter?' "
            "using different signals]]\n"
            "\n"
            "### Important practical limitation\n"
            "\n"
            "A sparse model is not automatically faster on real hardware. The chapter notes "
            "that hardware support for sparse matrix operations can limit the practical speed "
            "benefit even when storage is reduced.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 16
            # ----------------------------------------------------------------

            "## 16. A practical production optimization workflow\n"
            "\n"
            "The chapter can be turned into one repeatable engineering loop:\n"
            "\n"
            "```text\n"
            "1. Define the product requirements\n"
            "       ↓\n"
            "2. Benchmark the full model\n"
            "   quality + latency + memory\n"
            "       ↓\n"
            "3. Try a smaller student / distillation\n"
            "       ↓\n"
            "4. Re-benchmark\n"
            "       ↓\n"
            "5. Apply quantization\n"
            "       ↓\n"
            "6. Re-benchmark\n"
            "       ↓\n"
            "7. Export / optimize with ONNX Runtime\n"
            "       ↓\n"
            "8. Re-benchmark\n"
            "       ↓\n"
            "9. Consider pruning if storage/sparsity matters\n"
            "       ↓\n"
            "10. Validate on realistic production hardware and inputs\n"
            "```\n"
            "\n"
            "The most important habit is the repeated **re-benchmark** step.\n"
            "\n"
            "An optimization is only valuable when it improves the constraints that actually "
            "matter without degrading quality beyond an acceptable level.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: The most accurate model is automatically the best production model\n"
            "\n"
            "> If a model wins on the test metric, deployment concerns are secondary.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Latency, memory, cost, and hardware constraints can make a highly accurate model "
            "impractical. Production choices require several metrics.\n"
            "\n"
            "### Misconception 2: Distillation means copying the teacher's final class only\n"
            "\n"
            "> The student simply trains on the teacher's argmax prediction.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The soft probability distribution can reveal relationships among classes that "
            "the hard label alone does not contain.\n"
            "\n"
            "### Misconception 3: Quantization always reduces accuracy significantly\n"
            "\n"
            "> INT8 necessarily destroys model quality.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The actual impact must be measured. In the chapter's intent-classification "
            "experiment, INT8 quantization preserves the task metric very well.\n"
            "\n"
            "### Misconception 4: Exporting to ONNX automatically makes a model smaller\n"
            "\n"
            "> ONNX conversion itself is the same thing as compression.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "ONNX primarily provides a standardized graph representation. Runtime graph "
            "optimization can improve execution speed, while quantization or pruning are "
            "separate mechanisms for reducing numerical/storage cost.\n"
            "\n"
            "### Misconception 5: Sparse always means fast\n"
            "\n"
            "> Removing weights guarantees proportional latency improvement.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Speed depends on whether the target hardware/runtime can efficiently exploit "
            "sparse operations.\n"
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
            "| Latency | Time required to produce a prediction |\n"
            "| Throughput | Number of predictions a system can process in a period of time |\n"
            "| Model footprint | Storage/RAM cost associated with a model |\n"
            "| Benchmark | Consistent procedure for comparing production-relevant metrics |\n"
            "| Knowledge distillation | Training a smaller student using guidance from a larger teacher |\n"
            "| Teacher | Larger model that supplies soft predictions during distillation |\n"
            "| Student | Smaller model trained to imitate the teacher |\n"
            "| Soft target | Probability distribution over classes rather than one hard class label |\n"
            "| Temperature | Parameter used to soften class probability distributions |\n"
            "| KL divergence | Measure used to compare teacher and student probability distributions |\n"
            "| Quantization | Mapping model values to lower-precision numerical representations |\n"
            "| FP32 | 32-bit floating-point representation |\n"
            "| INT8 | 8-bit integer representation commonly used for quantized inference |\n"
            "| Dynamic quantization | Quantization where activations are handled dynamically during inference |\n"
            "| Static quantization | Quantization calibrated using representative activation data beforehand |\n"
            "| Quantization-aware training | Training while simulating reduced precision |\n"
            "| ONNX | Standard format for representing ML computation graphs |\n"
            "| ONNX Runtime | Inference engine that optimizes and executes ONNX graphs |\n"
            "| Operator fusion | Combining compatible graph operations for more efficient execution |\n"
            "| Constant folding | Precomputing constant graph expressions before runtime |\n"
            "| Pruning | Removing less important model weights/connections |\n"
            "| Sparsity | Fraction of weights that are zero or inactive |\n"
            "| Magnitude pruning | Pruning based largely on absolute weight magnitude |\n"
            "| Movement pruning | Pruning based on learned importance/movement during fine-tuning |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why is accuracy alone insufficient when selecting a production model?\n"
            "2. Why should latency be measured over many runs with warm-up?\n"
            "3. What extra information can a teacher's soft distribution provide?\n"
            "4. What do temperature and alpha control in knowledge distillation?\n"
            "5. Why is DistilBERT a sensible student for a BERT teacher?\n"
            "6. How does quantization differ from distillation?\n"
            "7. What is the difference between dynamic and static quantization?\n"
            "8. What does ONNX represent?\n"
            "9. What can ONNX Runtime optimize?\n"
            "10. Why can combining distillation, ORT, and quantization be useful?\n"
            "11. How do magnitude and movement pruning define importance differently?\n"
            "12. Why might a highly sparse model fail to achieve the expected speedup?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**Production optimization is a measured trade-off, not a single compression "
            "trick. Benchmark quality, latency, and memory first; then apply techniques such "
            "as distillation, quantization, ONNX Runtime optimization, and pruning one by one "
            "or in combination, re-measuring after every change on realistic hardware.**\n"
        ),

        "estimated_minutes": 120,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "production-problem", "title": "A great model can still be a bad production model", "order": 1},
            {"id": "case-study", "title": "Intent detection case study", "order": 2},
            {"id": "benchmark", "title": "Benchmark before optimizing", "order": 3},
            {"id": "latency", "title": "Measure latency correctly", "order": 4},
            {"id": "distillation", "title": "Knowledge distillation", "order": 5},
            {"id": "soft-targets", "title": "Temperature and distillation loss", "order": 6},
            {"id": "distillation-trainer", "title": "Custom distillation trainer", "order": 7},
            {"id": "hyperparameter-search", "title": "Tune distillation", "order": 8},
            {"id": "quantization", "title": "Quantization", "order": 9},
            {"id": "quantization-types", "title": "Quantization strategies", "order": 10},
            {"id": "onnx", "title": "ONNX computational graphs", "order": 11},
            {"id": "ort", "title": "ONNX Runtime", "order": 12},
            {"id": "ort-quantization", "title": "Combine ORT and quantization", "order": 13},
            {"id": "pruning", "title": "Pruning and sparsity", "order": 14},
            {"id": "pruning-methods", "title": "Magnitude vs movement pruning", "order": 15},
            {"id": "workflow", "title": "Production optimization workflow", "order": 16},
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L06.EX01",
            "title": "Design a Production Benchmark",
            "lesson_code": "M01.L06",
            "section_id": "benchmark",
            "placement": "after_section",
            "description": (
                "Practice defining an evaluation setup that measures more than model accuracy."
            ),
            "instructions": (
                "1. Imagine you are deploying an intent classifier for a customer-support chatbot.\n"
                "2. Define one model-quality metric.\n"
                "3. Define how you will measure latency, including warm-up and repeated runs.\n"
                "4. Define how you will measure model size or memory footprint.\n"
                "5. Choose one representative production query and explain why it is representative.\n"
                "6. State what would make an optimized model unacceptable even if it is faster."
            ),
            "expected_output": (
                "A compact benchmark specification including model quality, latency methodology, "
                "memory/model size, representative input selection, and an acceptable quality-loss "
                "constraint."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "production-benchmarking",
                "latency-measurement",
                "model-evaluation",
                "deployment-tradeoffs",
            ],
        },

        {
            "id": "M01.L06.EX02",
            "title": "Choose the Right Optimization",
            "lesson_code": "M01.L06",
            "section_id": "quantization-types",
            "placement": "after_section",
            "description": (
                "Practice matching production constraints to compression and inference techniques."
            ),
            "instructions": (
                "For each scenario, choose a reasonable first optimization and explain why:\n"
                "1. The model is accurate but twice too slow and much larger than needed.\n"
                "2. You already have a smaller student but CPU inference is still too slow.\n"
                "3. You need a standardized inference graph and optimized CPU runtime.\n"
                "4. Storage is the main constraint and you are willing to investigate sparsity.\n"
                "5. After every choice, state which three benchmark quantities you must re-measure."
            ),
            "expected_output": (
                "A table mapping scenarios to distillation, quantization, ONNX Runtime, or pruning, "
                "with a short rationale and repeated measurement of quality, latency, and size/memory."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "knowledge-distillation",
                "quantization",
                "onnx-runtime",
                "pruning",
                "production-reasoning",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L06.QZ01",
        "title": "Making Transformers Efficient in Production — Knowledge Check",
        "lesson_code": "M01.L06",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L06.Q01",
                "section_id": "benchmark",
                "question": (
                    "Which set best represents the core production trade-off emphasized "
                    "in this lesson?"
                ),
                "options": [
                    "Accuracy, latency, and memory/model size.",
                    "Learning rate, tokenizer name, and random seed.",
                    "Number of notebooks, plots, and epochs.",
                    "Vocabulary size, file name, and operating system.",
                ],
                "correct": 0,
                "explanation": (
                    "A production model must meet task-quality requirements while also "
                    "satisfying latency and memory/storage constraints."
                ),
            },

            {
                "id": "M01.L06.Q02",
                "section_id": "soft-targets",
                "question": (
                    "Why is temperature used during knowledge distillation?"
                ),
                "options": [
                    "To increase the physical temperature of the GPU.",
                    "To soften class probabilities so the teacher reveals more information "
                    "about relationships among classes.",
                    "To reduce the tokenizer vocabulary.",
                    "To remove all incorrect teacher predictions.",
                ],
                "correct": 1,
                "explanation": (
                    "Dividing logits by a larger temperature before softmax produces a softer "
                    "distribution, exposing relative probabilities that hard labels hide."
                ),
            },

            {
                "id": "M01.L06.Q03",
                "section_id": "quantization",
                "question": (
                    "What is the main idea behind INT8 quantization?"
                ),
                "options": [
                    "Delete the transformer attention layers.",
                    "Represent weights/activations with lower-precision integer values to reduce "
                    "storage and accelerate supported operations.",
                    "Train only on eight examples.",
                    "Replace the model with a rule-based system.",
                ],
                "correct": 1,
                "explanation": (
                    "Quantization reduces numerical precision, for example from FP32 to INT8, "
                    "so values require fewer bits and integer operations can be more efficient."
                ),
            },

            {
                "id": "M01.L06.Q04",
                "section_id": "pruning-methods",
                "question": (
                    "How does movement pruning differ conceptually from magnitude pruning?"
                ),
                "options": [
                    "Movement pruning learns task-related importance scores during fine-tuning, "
                    "while magnitude pruning primarily ranks weights by absolute size.",
                    "Movement pruning only works on tokenizers.",
                    "Magnitude pruning increases every weight magnitude.",
                    "They are exactly the same algorithm with different names.",
                ],
                "correct": 0,
                "explanation": (
                    "Magnitude pruning uses weight magnitude as its importance signal. Movement "
                    "pruning learns importance scores during fine-tuning, making the criterion "
                    "more adaptive to the downstream task."
                ),
            },

            {
                "id": "M01.L06.Q05",
                "section_id": "workflow",
                "type": "open",
                "question": (
                    "You have a BERT classifier that is accurate enough but too slow and too "
                    "large for a CPU-only deployment. Propose an optimization sequence using "
                    "techniques from this lesson. Explain what you would benchmark after each "
                    "step and what trade-off would make you stop optimizing."
                ),
            },
        ],

        "passing_score": 70,
    },
}
