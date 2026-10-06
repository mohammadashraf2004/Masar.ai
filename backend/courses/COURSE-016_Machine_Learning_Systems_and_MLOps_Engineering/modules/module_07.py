"""M07.L01 — Model Deployment and Prediction Service.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 7, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M07.L01"

MODULE_ORDER = 7

MODULE_TITLE = "Model Deployment and Prediction Service"

MODULE_DESCRIPTION = (
    "Learn how production ML models are deployed and served, how batch and online "
    "prediction differ, how batch and streaming feature pipelines interact, how "
    "models are compressed and optimized for inference, and how cloud, edge, "
    "compiler, and browser deployment choices affect system design."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Model Deployment and Prediction Service",

    "slug": "ml-systems-design-m07-l01",

    "description": (
        "A production-focused introduction to deploying ML models and building "
        "prediction services, covering deployment myths, model export, batch and "
        "online prediction, streaming features, pipeline consistency, model "
        "compression, cloud versus edge inference, intermediate representations, "
        "compiler optimization, and browser-based ML."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 4.0,

    "skill_tags": [
        "ml-deployment",
        "prediction-service",
        "model-export",
        "batch-prediction",
        "online-prediction",
        "streaming-prediction",
        "batch-features",
        "streaming-features",
        "training-serving-consistency",
        "model-compression",
        "low-rank-factorization",
        "knowledge-distillation",
        "pruning",
        "quantization",
        "cloud-inference",
        "edge-inference",
        "intermediate-representation",
        "ml-compilers",
        "model-optimization",
        "vectorization",
        "parallelization",
        "loop-tiling",
        "operator-fusion",
        "webassembly",
    ],

    "prerequisite_ids": ["M06.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Model Deployment and Prediction Service",

        "content": (
            "# Model Deployment and Prediction Service\n"
            "\n"
            "> **Lesson:** M07.L01  \n"
            "> **Module:** Model Deployment and Prediction Service  \n"
            "> **Source alignment:** Chapter 7. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what model deployment means in a production ML system.\n"
            "- Explain why production deployment is more than exposing a prediction endpoint.\n"
            "- Describe why organizations may operate many models rather than one.\n"
            "- Explain why deployed model performance can degrade over time.\n"
            "- Compare batch, online, and streaming prediction patterns.\n"
            "- Distinguish batch features, online features, and streaming features.\n"
            "- Explain why separate training and inference pipelines create bugs.\n"
            "- Compare low-rank factorization, knowledge distillation, pruning, and quantization.\n"
            "- Explain the trade-offs between cloud and edge inference.\n"
            "- Explain why intermediate representations are useful for ML compilation.\n"
            "- Distinguish local and global model optimization.\n"
            "- Explain vectorization, parallelization, loop tiling, and operator fusion.\n"
            "- Explain how ML can help optimize execution plans for ML workloads.\n"
            "- Describe the role and trade-offs of browser-based inference with WebAssembly.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Deployment means making the model runnable and accessible\n"
            "\n"
            "During development, an ML model usually runs in a development environment. "
            "Deployment moves the model out of that environment so another system or "
            "end user can actually use it.\n"
            "\n"
            "A model may first move into **staging** for testing, then into **production** "
            "for real use.\n"
            "\n"
            "The chapter emphasizes that production is a spectrum. At one end, production "
            "may mean generating useful outputs for an internal business team. At the other "
            "end, it can mean serving millions of users with millisecond latency and very high uptime.\n"
            "\n"
            "For a simple demo, deployment might look like:\n"
            "\n"
            "```text\n"
            "Client request\n"
            "      ↓\n"
            "Prediction API\n"
            "      ↓\n"
            "Loaded model\n"
            "      ↓\n"
            "Prediction response\n"
            "```\n"
            "\n"
            "But this diagram hides the hard parts of production:\n"
            "\n"
            "- scaling to many users,\n"
            "- maintaining acceptable latency,\n"
            "- keeping the service available,\n"
            "- detecting failures,\n"
            "- notifying the right people,\n"
            "- debugging failures,\n"
            "- shipping model updates safely.\n"
            "\n"
            "A small web endpoint proves that a model can be called. It does not prove "
            "that the system can operate reliably at production scale.\n"
            "\n"
            "[[IMAGE_NEEDED: Demo deployment versus production deployment | "
            "A simple model-plus-API box on the left and a production system on the "
            "right containing load balancing, monitoring, alerts, model versions, "
            "feature pipelines, and multiple clients | Learner should notice that "
            "exposing an endpoint is only one small part of production deployment]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Model export separates training from serving\n"
            "\n"
            "A deployment team may not run the model inside the same framework or "
            "environment used during development. The model may need to be **exported** "
            "into a format another application can load.\n"
            "\n"
            "The source describes two broad parts that must be represented:\n"
            "\n"
            "1. **model definition** — the model's structure,\n"
            "2. **parameter values** — the learned values inside that structure.\n"
            "\n"
            "These are usually exported together.\n"
            "\n"
            "The chapter gives examples such as TensorFlow SavedModel and ONNX export "
            "from PyTorch.\n"
            "\n"
            "This leads to an important engineering principle:\n"
            "\n"
            "> The way a model will be served should influence how it is developed.\n"
            "\n"
            "A model that cannot meet the target hardware, latency, or export constraints "
            "may be unsuitable even if its offline metric is excellent.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Four deployment myths\n"
            "\n"
            "### Myth 1: You only deploy one or two models\n"
            "\n"
            "Real applications may rely on many models.\n"
            "\n"
            "A ride-sharing system might use separate models for:\n"
            "\n"
            "- ride demand,\n"
            "- driver availability,\n"
            "- estimated arrival time,\n"
            "- dynamic pricing,\n"
            "- fraud detection,\n"
            "- churn prediction.\n"
            "\n"
            "Different countries, products, languages, or user groups can multiply "
            "the number further. Infrastructure designed only for one model may fail "
            "to support an actual production portfolio.\n"
            "\n"
            "### Myth 2: Performance stays the same if we do nothing\n"
            "\n"
            "Production data changes. A model trained on yesterday's distribution can "
            "face a different distribution later.\n"
            "\n"
            "The chapter describes this using **data distribution shift** and notes that "
            "models often perform best soon after training, then degrade as the world changes.\n"
            "\n"
            "### Myth 3: Models rarely need updates\n"
            "\n"
            "The more useful question is not simply \"How often should the model be updated?\" "
            "but \"How quickly can the organization safely update it when needed?\"\n"
            "\n"
            "Fast iteration becomes valuable when data or behavior changes quickly.\n"
            "\n"
            "### Myth 4: Most ML engineers do not need to care about scale\n"
            "\n"
            "Scale does not only mean internet-scale companies. Hundreds of queries per "
            "second, millions of users, many deployed models, or strict latency targets can "
            "all create scalability requirements.\n"
            "\n"
            "[[IMAGE_NEEDED: Model portfolio at production scale | "
            "A product with several ML-powered functions connected to many deployed "
            "models across regions or countries | Learner should notice that production "
            "ML infrastructure often manages fleets of models, not one isolated model]]\n"
            "\n"
            "{{exercise:M07.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Three prediction modes to remember\n"
            "\n"
            "The chapter acknowledges that industry terminology can be inconsistent. "
            "The most useful mental model is to remember three operating modes:\n"
            "\n"
            "1. **Batch prediction using batch features**\n"
            "2. **Online prediction using batch features**\n"
            "3. **Online prediction using both batch and streaming features**\n"
            "\n"
            "The third mode is sometimes called **streaming prediction**.\n"
            "\n"
            "This distinction matters because prediction timing and feature freshness "
            "are different design choices.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Batch prediction versus online prediction\n"
            "\n"
            "### Online prediction\n"
            "\n"
            "Online prediction generates a result as soon as a request arrives.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "User submits text\n"
            "      ↓\n"
            "Prediction request\n"
            "      ↓\n"
            "Model runs now\n"
            "      ↓\n"
            "Prediction returned immediately\n"
            "```\n"
            "\n"
            "Online prediction is also called **on-demand prediction**. When implemented "
            "through direct request-response APIs, it is often described as synchronous prediction.\n"
            "\n"
            "### Batch prediction\n"
            "\n"
            "Batch prediction generates predictions periodically or when triggered. "
            "The results are stored, then fetched later when users or applications need them.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Every 4 hours:\n"
            "Generate recommendations for many users\n"
            "      ↓\n"
            "Store recommendations\n"
            "      ↓\n"
            "User visits later\n"
            "      ↓\n"
            "Fetch stored result\n"
            "```\n"
            "\n"
            "Batch prediction is often described as asynchronous because prediction "
            "generation is not synchronized with the user request.\n"
            "\n"
            "### Main trade-off\n"
            "\n"
            "| Dimension | Batch prediction | Online prediction |\n"
            "|---|---|---|\n"
            "| When predictions are generated | Periodically / triggered | When requests arrive |\n"
            "| Main optimization target | High throughput | Low latency |\n"
            "| Good fit | Results need not reflect the latest event immediately | Result is needed immediately |\n"
            "| Responsiveness to fresh behavior | Lower | Higher |\n"
            "| Need to anticipate requests | Usually yes | No |\n"
            "\n"
            "[[IMAGE_NEEDED: Batch versus online prediction architecture | "
            "Side-by-side pipelines showing batch feature computation and periodic "
            "prediction storage versus request-time model inference through a prediction "
            "service | Learner should notice that batch prediction computes ahead of "
            "requests while online prediction computes in response to requests]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Batch features, online features, and streaming features\n"
            "\n"
            "Prediction mode and feature type are not the same thing.\n"
            "\n"
            "**Batch features** come from historical data processed periodically.\n"
            "\n"
            "Example:\n"
            "\n"
            "- a restaurant's mean preparation time over the past month.\n"
            "\n"
            "**Streaming features** are computed from incoming events in near real time.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- number of orders in the last 10 minutes,\n"
            "- number of delivery workers currently available.\n"
            "\n"
            "**Online features** are any features used for online prediction. That can "
            "include both batch features and streaming features.\n"
            "\n"
            "For example, a precomputed item embedding can be a batch feature stored "
            "for later use. If it is fetched during an online prediction request, it is "
            "an online feature but **not** a streaming feature.\n"
            "\n"
            "This gives three useful cases:\n"
            "\n"
            "```text\n"
            "Batch prediction:\n"
            "batch features → periodic inference → stored predictions\n"
            "\n"
            "Online prediction with batch features:\n"
            "stored/precomputed features → request-time inference\n"
            "\n"
            "Streaming prediction:\n"
            "batch features + fresh streaming features → request-time inference\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Feature freshness and prediction mode | "
            "Three horizontal pipelines for batch prediction, online prediction with "
            "precomputed batch features, and online prediction combining batch and "
            "streaming features | Learner should notice that 'online feature' does "
            "not necessarily mean 'streaming feature']] \n"
            "\n"
            "---\n"
            "\n"

            "## 7. Choosing between batch and online prediction\n"
            "\n"
            "Batch prediction is useful when you need many predictions and do not need "
            "them immediately.\n"
            "\n"
            "It can also hide slow inference: instead of making the user wait for a "
            "complex model, compute predictions earlier and make serving a fast lookup.\n"
            "\n"
            "But batch prediction has important limitations.\n"
            "\n"
            "### It can waste compute\n"
            "\n"
            "If only a small fraction of users visit each day, computing daily predictions "
            "for everyone wastes work on inactive users.\n"
            "\n"
            "### It can become stale\n"
            "\n"
            "A recommendation generated hours ago may not reflect what a user is doing now.\n"
            "\n"
            "### It requires predictable requests\n"
            "\n"
            "Movie recommendations can be precomputed for known users. Arbitrary translation "
            "requests cannot be fully predicted in advance.\n"
            "\n"
            "### Some applications require immediate decisions\n"
            "\n"
            "The chapter lists examples such as:\n"
            "\n"
            "- high-frequency trading,\n"
            "- autonomous vehicles,\n"
            "- voice assistants,\n"
            "- biometric unlocking,\n"
            "- fall detection,\n"
            "- fraud detection.\n"
            "\n"
            "A fraud prediction three hours after the transaction is less useful than one "
            "that can block the transaction before it completes.\n"
            "\n"
            "### Hybrid systems\n"
            "\n"
            "Batch and online prediction can coexist. You might precompute results for "
            "popular or predictable requests and run the model online for long-tail or "
            "unpredictable requests.\n"
            "\n"
            "{{exercise:M07.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 8. What online prediction requires\n"
            "\n"
            "Moving toward online prediction requires two major capabilities.\n"
            "\n"
            "### 1. A near-real-time data pipeline\n"
            "\n"
            "The system must ingest incoming data, compute any required streaming "
            "features, join them with other features, and make them available quickly.\n"
            "\n"
            "### 2. A sufficiently fast model\n"
            "\n"
            "The model must produce a prediction within the latency budget expected by "
            "the user or downstream system. For many consumer applications, that means milliseconds.\n"
            "\n"
            "A fast model with a slow feature pipeline is not a fast prediction service. "
            "Likewise, a fast streaming pipeline cannot compensate for a model whose "
            "inference time exceeds the product's latency budget.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Training-serving pipeline inconsistency\n"
            "\n"
            "An important production bug appears when training and inference compute "
            "the same feature through different code paths.\n"
            "\n"
            "Consider a route-ETA feature:\n"
            "\n"
            "> average speed of cars on the route during the last five minutes.\n"
            "\n"
            "During training, historical data may be processed in a dataframe over a "
            "large batch. During production inference, the same feature may be updated "
            "continuously using a sliding window over an event stream.\n"
            "\n"
            "Conceptually the feature is the same. Operationally, it is implemented twice.\n"
            "\n"
            "That creates a failure mode:\n"
            "\n"
            "```text\n"
            "Training pipeline changes\n"
            "         ↓\n"
            "Serving pipeline is not updated identically\n"
            "         ↓\n"
            "Training and production compute different feature values\n"
            "         ↓\n"
            "Model sees a different input definition in production\n"
            "```\n"
            "\n"
            "Separate team ownership can make the problem worse because changes must "
            "be coordinated across organizational boundaries.\n"
            "\n"
            "The chapter describes industry efforts to unify batch and stream processing "
            "and notes that feature stores can help maintain consistency between features "
            "used for training and features used for prediction.\n"
            "\n"
            "[[IMAGE_NEEDED: Training-serving skew from duplicate feature pipelines | "
            "Two paths computing the same feature: an offline batch training pipeline "
            "and an online streaming inference pipeline, first matching and then diverging "
            "after only one path changes | Learner should notice how duplicated feature "
            "logic creates inconsistent model inputs]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Model compression for faster, smaller inference\n"
            "\n"
            "If a model is too slow to serve, the chapter presents three broad directions:\n"
            "\n"
            "1. make inference execution faster,\n"
            "2. make the model smaller,\n"
            "3. use faster hardware.\n"
            "\n"
            "**Model compression** focuses on reducing model size. Smaller models often "
            "also reduce inference latency and memory requirements.\n"
            "\n"
            "The chapter highlights four major compression families:\n"
            "\n"
            "- low-rank factorization,\n"
            "- knowledge distillation,\n"
            "- pruning,\n"
            "- quantization.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Four model-compression techniques\n"
            "\n"
            "### Low-rank factorization\n"
            "\n"
            "The key idea is to replace high-dimensional tensors or expensive operations "
            "with lower-dimensional structures that approximate the same computation.\n"
            "\n"
            "The chapter uses compact convolutional filters as an example. MobileNet-style "
            "depthwise and pointwise convolutions can dramatically reduce parameter count "
            "compared with a full convolution.\n"
            "\n"
            "The trade-off is specialization: these methods often require architectural "
            "knowledge and may apply only to particular model families.\n"
            "\n"
            "### Knowledge distillation\n"
            "\n"
            "A smaller **student** model is trained to imitate a larger **teacher** model "
            "or ensemble.\n"
            "\n"
            "```text\n"
            "Large teacher model\n"
            "       ↓ teaches\n"
            "Small student model\n"
            "       ↓ deploy\n"
            "Prediction service\n"
            "```\n"
            "\n"
            "The source gives DistilBERT as an example of a smaller model designed to "
            "retain much of a larger BERT model's capability while running faster.\n"
            "\n"
            "Distillation is flexible because teacher and student do not have to use "
            "the same architecture. But it depends on having a useful teacher.\n"
            "\n"
            "### Pruning\n"
            "\n"
            "Pruning removes or disables model components that contribute little.\n"
            "\n"
            "For neural networks, this can mean:\n"
            "\n"
            "- removing entire nodes or structures, or\n"
            "- setting low-value weights to zero to create sparsity.\n"
            "\n"
            "Sparse models can need less storage and may run more efficiently when the "
            "hardware and runtime can exploit sparsity.\n"
            "\n"
            "### Quantization\n"
            "\n"
            "Quantization uses fewer bits to represent parameters and sometimes activations.\n"
            "\n"
            "Example memory intuition:\n"
            "\n"
            "```text\n"
            "100 million parameters × 32 bits ≈ 400 MB\n"
            "100 million parameters × 16 bits ≈ 200 MB\n"
            "100 million parameters ×  8 bits ≈ 100 MB\n"
            "```\n"
            "\n"
            "Lower precision can reduce memory use and increase computation speed.\n"
            "\n"
            "The trade-off is numerical error: smaller representations have less precision "
            "and a smaller representable range. Poor rounding or scaling can reduce model quality.\n"
            "\n"
            "Quantization can happen during training or after training for inference.\n"
            "\n"
            "[[IMAGE_NEEDED: Four model compression methods | "
            "Four panels showing low-rank decomposition, teacher-student distillation, "
            "weight pruning to sparse connections, and 32-bit to 8-bit quantization | "
            "Learner should notice that all four reduce deployment cost through "
            "different mechanisms]]\n"
            "\n"
            "{{exercise:M07.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Cloud versus edge inference\n"
            "\n"
            "A deployed model must run somewhere.\n"
            "\n"
            "**Cloud inference** runs most computation on remote servers.  \n"
            "**Edge inference** runs a large portion directly on user or embedded devices.\n"
            "\n"
            "Edge devices can include:\n"
            "\n"
            "- browsers,\n"
            "- phones,\n"
            "- laptops,\n"
            "- smartwatches,\n"
            "- cars,\n"
            "- cameras,\n"
            "- robots,\n"
            "- embedded devices,\n"
            "- FPGAs and ASICs.\n"
            "\n"
            "### Why cloud is attractive\n"
            "\n"
            "- easier to get started,\n"
            "- managed infrastructure is widely available,\n"
            "- server hardware can be powerful and centrally maintained.\n"
            "\n"
            "### Why edge is attractive\n"
            "\n"
            "#### Lower cloud cost\n"
            "\n"
            "More computation on the device can reduce server compute demand.\n"
            "\n"
            "#### Offline operation\n"
            "\n"
            "Edge applications can work with unreliable or absent internet connections.\n"
            "\n"
            "#### Reduced network latency\n"
            "\n"
            "The model does not need a network round trip for every prediction.\n"
            "\n"
            "#### Privacy advantages\n"
            "\n"
            "Sensitive data may remain on-device rather than being sent to centralized servers.\n"
            "\n"
            "### Edge constraints\n"
            "\n"
            "Edge devices have limited:\n"
            "\n"
            "- compute,\n"
            "- memory,\n"
            "- battery or power,\n"
            "- supported operators and runtimes.\n"
            "\n"
            "A model suitable for a server GPU may be unusable on a phone or sensor.\n"
            "\n"
            "[[IMAGE_NEEDED: Cloud versus edge inference | "
            "A mobile device sending data across a network to a cloud model versus "
            "the same device running the model locally, with callouts for cloud cost, "
            "network latency, privacy, memory, compute, and battery | Learner should "
            "notice that moving inference to the edge removes some network costs but "
            "introduces device constraints]]\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Intermediate representations bridge frameworks and hardware\n"
            "\n"
            "Different hardware backends expose different compute primitives, memory "
            "layouts, caches, and optimization opportunities.\n"
            "\n"
            "Supporting every ML framework directly on every hardware backend creates "
            "an expensive many-to-many engineering problem.\n"
            "\n"
            "A compiler can introduce an **intermediate representation (IR)**:\n"
            "\n"
            "```text\n"
            "High-level framework model\n"
            "          ↓\n"
            "High-level IR\n"
            "          ↓\n"
            "Lower-level IR(s)\n"
            "          ↓\n"
            "Hardware-native code\n"
            "```\n"
            "\n"
            "Framework developers target the IR instead of every piece of hardware. "
            "Hardware vendors support the IR and compiler path instead of every framework.\n"
            "\n"
            "This process is often called **lowering** because high-level operations "
            "are progressively converted into lower-level hardware-specific operations.\n"
            "\n"
            "At a high level, an ML model is often represented as a **computation graph** "
            "describing operators and the order in which they execute.\n"
            "\n"
            "[[IMAGE_NEEDED: Framework to hardware through intermediate representations | "
            "Several ML frameworks feeding a shared high-level IR, then lower-level IR, "
            "then branching to CPU, GPU, and accelerator machine code | Learner should "
            "notice how IRs reduce the need for every framework to directly support "
            "every hardware backend]]\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Model optimization after compilation\n"
            "\n"
            "Code can be executable on hardware without being efficient on that hardware.\n"
            "\n"
            "Optimization tries to exploit memory locality, caches, vector operations, "
            "parallel execution, and the structure of the full computation graph.\n"
            "\n"
            "The chapter separates **local** and **global** optimization.\n"
            "\n"
            "### Local optimization\n"
            "\n"
            "Optimize one operator or a small group of operators.\n"
            "\n"
            "#### Vectorization\n"
            "\n"
            "Process multiple contiguous elements together instead of one element per loop iteration.\n"
            "\n"
            "#### Parallelization\n"
            "\n"
            "Split independent work into chunks that can execute simultaneously.\n"
            "\n"
            "#### Loop tiling\n"
            "\n"
            "Reorder memory access so computation makes better use of the target "
            "hardware's memory hierarchy and cache.\n"
            "\n"
            "Because hardware layouts differ, a good access pattern for a CPU may not "
            "be good for a GPU.\n"
            "\n"
            "#### Operator fusion\n"
            "\n"
            "Combine several operators so intermediate results do not need to be "
            "written to and reread from memory repeatedly.\n"
            "\n"
            "Example intuition:\n"
            "\n"
            "```text\n"
            "Without fusion:\n"
            "read array → op A → write\n"
            "read array → op B → write\n"
            "\n"
            "With fusion:\n"
            "read array → op A + op B → write once\n"
            "```\n"
            "\n"
            "### Global optimization\n"
            "\n"
            "Instead of optimizing isolated operators, examine the computation graph "
            "end to end and reorganize larger regions of computation.\n"
            "\n"
            "[[IMAGE_NEEDED: Operator fusion reduces memory traffic | "
            "A before/after diagram where two operators each read and write an "
            "intermediate tensor versus one fused operator that keeps the intermediate "
            "result local | Learner should notice that reducing memory movement can "
            "speed inference even if the mathematical operations are unchanged]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Using ML to optimize ML execution\n"
            "\n"
            "A computation graph may have many valid execution plans.\n"
            "\n"
            "Engineers traditionally create hardware-specific heuristics for choosing "
            "fast execution strategies. These heuristics can work well but have two "
            "limitations highlighted by the chapter:\n"
            "\n"
            "- they may be nonoptimal,\n"
            "- they may not adapt well to new models or hardware.\n"
            "\n"
            "Trying every execution plan is usually impossible because the search "
            "space grows combinatorially.\n"
            "\n"
            "This creates an opportunity for ML-assisted optimization.\n"
            "\n"
            "### Autotuning idea\n"
            "\n"
            "A system can search candidate implementations, measure real execution time, "
            "and learn a **cost model** that predicts which future candidates are promising.\n"
            "\n"
            "The chapter describes autoTVM conceptually as:\n"
            "\n"
            "1. break the graph into subgraphs,\n"
            "2. estimate subgraph search difficulty or size,\n"
            "3. allocate search effort,\n"
            "4. test candidate execution plans,\n"
            "5. learn from measured runtime,\n"
            "6. combine the best subgraph implementations.\n"
            "\n"
            "This optimization can take hours or days, but it is mainly a one-time cost "
            "for a specific model and hardware target. The optimized result can then be "
            "cached and reused across many deployments on the same hardware family.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. ML in browsers and WebAssembly\n"
            "\n"
            "Browser execution offers another kind of portability: if the model can run "
            "inside a browser, it can run across many devices without directly targeting "
            "each device's native hardware interface.\n"
            "\n"
            "JavaScript can run ML logic, but the chapter describes it as limited for "
            "heavy computational workloads compared with native execution.\n"
            "\n"
            "**WebAssembly (WASM)** provides a more performant browser execution target.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Model in ML framework\n"
            "        ↓ compile\n"
            "WebAssembly executable\n"
            "        ↓\n"
            "Browser on many device types\n"
            "```\n"
            "\n"
            "The advantage is portability across devices supporting browsers.\n"
            "\n"
            "The trade-off presented in the chapter is performance: WASM can be much "
            "faster than JavaScript for some workloads but still slower than native code.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Deployment means wrapping `predict()` in an API\n"
            "\n"
            "That can create a demo, but production also requires scale, latency, "
            "availability, monitoring, alerting, debugging, and safe updates.\n"
            "\n"
            "### Misconception 2: Online prediction means all features are streaming\n"
            "\n"
            "An online request may use precomputed batch features. Streaming features "
            "specifically come from live event streams.\n"
            "\n"
            "### Misconception 3: Batch prediction is always cheaper\n"
            "\n"
            "Batch can waste compute by generating predictions for users or requests "
            "that never occur.\n"
            "\n"
            "### Misconception 4: Training and serving can implement feature logic independently\n"
            "\n"
            "Duplicated logic is a major source of training-serving inconsistency.\n"
            "\n"
            "### Misconception 5: Compression only reduces storage\n"
            "\n"
            "Compression can also reduce memory use and inference latency, though model "
            "quality and hardware support must be checked.\n"
            "\n"
            "### Misconception 6: Edge inference is automatically better than cloud inference\n"
            "\n"
            "Edge reduces network dependence and can improve privacy and latency, but "
            "device compute, memory, battery, and runtime support become constraints.\n"
            "\n"
            "### Misconception 7: If compiled code runs, it is already optimized\n"
            "\n"
            "Executable code may still waste memory bandwidth, caches, parallelism, "
            "or hardware-specific capabilities.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Deployment | Making a model runnable and accessible outside its development environment. |\n"
            "| Staging | Pre-production environment used for testing deployments. |\n"
            "| Production | Environment where a model serves real users or operational systems. |\n"
            "| Model export | Converting model structure and learned parameters into a form another application can load. |\n"
            "| Inference | Generating predictions from a trained model. |\n"
            "| Batch prediction | Generating predictions periodically or when triggered, then storing them for later use. |\n"
            "| Online prediction | Generating a prediction when a request arrives. |\n"
            "| Streaming prediction | Online prediction that incorporates streaming features. |\n"
            "| Batch feature | Feature computed from historical data, usually periodically. |\n"
            "| Streaming feature | Feature computed from incoming event streams. |\n"
            "| Online feature | Any feature used for online prediction, including batch and streaming features. |\n"
            "| Training-serving skew | Mismatch between data or feature computation during training and inference. |\n"
            "| Model compression | Reducing model size, often to lower memory use and inference latency. |\n"
            "| Low-rank factorization | Replacing expensive high-dimensional structures with lower-dimensional approximations. |\n"
            "| Knowledge distillation | Training a small student model to imitate a larger teacher. |\n"
            "| Pruning | Removing or zeroing model components judged less important. |\n"
            "| Quantization | Representing model values with fewer bits. |\n"
            "| Edge inference | Running model computation mainly on local consumer or embedded devices. |\n"
            "| Cloud inference | Running model computation mainly on remote servers. |\n"
            "| Intermediate representation (IR) | Compiler-level representation connecting high-level model code to lower-level hardware code. |\n"
            "| Lowering | Transforming high-level model operations into progressively lower-level hardware-oriented operations. |\n"
            "| Computation graph | Graph describing model operations and execution dependencies. |\n"
            "| Vectorization | Processing multiple data elements together using vector operations. |\n"
            "| Parallelization | Splitting independent work so it can run simultaneously. |\n"
            "| Loop tiling | Reordering computation to better exploit cache and memory layout. |\n"
            "| Operator fusion | Combining operations to reduce redundant intermediate memory access. |\n"
            "| Cost model | Model used to estimate execution cost for candidate optimization strategies. |\n"
            "| WebAssembly | Portable executable format designed to run efficiently in browser environments. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why is exposing a prediction endpoint not the same as production readiness?\n"
            "2. What two broad pieces of a trained model are represented when exporting it?\n"
            "3. Why might one application require hundreds of models?\n"
            "4. Why does model performance often degrade after deployment?\n"
            "5. What are the three prediction modes emphasized in this lesson?\n"
            "6. How does batch prediction differ from online prediction?\n"
            "7. What is the difference between a streaming feature and an online feature?\n"
            "8. Why can batch prediction waste compute?\n"
            "9. Why are some tasks impossible to serve purely through precomputed predictions?\n"
            "10. What two capabilities are necessary for effective online prediction?\n"
            "11. How can separate batch and streaming feature pipelines cause bugs?\n"
            "12. What are the four model-compression methods discussed?\n"
            "13. How does knowledge distillation differ from pruning?\n"
            "14. Why can quantization reduce both memory and latency?\n"
            "15. What numerical risk does quantization introduce?\n"
            "16. What are the main benefits of edge inference?\n"
            "17. What new constraints appear on edge devices?\n"
            "18. Why are intermediate representations useful to framework and hardware developers?\n"
            "19. What is the difference between local and global model optimization?\n"
            "20. How does operator fusion reduce memory traffic?\n"
            "21. Why might an ML-powered compiler use a cost model?\n"
            "22. What portability advantage does WebAssembly provide, and what performance trade-off remains?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Deployment is the beginning of a new engineering phase, not the end of "
            "an ML project. A useful production model must fit its prediction mode, "
            "feature pipeline, latency budget, hardware target, update process, and "
            "operational constraints—not merely produce good offline predictions.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "deployment-basics", "title": "Deployment means making the model runnable and accessible", "order": 1},
            {"id": "model-export", "title": "Model export separates training from serving", "order": 2},
            {"id": "deployment-myths", "title": "Four deployment myths", "order": 3},
            {"id": "prediction-modes", "title": "Three prediction modes to remember", "order": 4},
            {"id": "batch-online", "title": "Batch prediction versus online prediction", "order": 5},
            {"id": "feature-freshness", "title": "Batch features, online features, and streaming features", "order": 6},
            {"id": "choosing-mode", "title": "Choosing between batch and online prediction", "order": 7},
            {"id": "online-requirements", "title": "What online prediction requires", "order": 8},
            {"id": "pipeline-unification", "title": "Training-serving pipeline inconsistency", "order": 9},
            {"id": "compression-overview", "title": "Model compression for faster, smaller inference", "order": 10},
            {"id": "compression-techniques", "title": "Four model-compression techniques", "order": 11},
            {"id": "cloud-edge", "title": "Cloud versus edge inference", "order": 12},
            {"id": "compilers-ir", "title": "Intermediate representations bridge frameworks and hardware", "order": 13},
            {"id": "model-optimization", "title": "Model optimization after compilation", "order": 14},
            {"id": "ml-optimizing-ml", "title": "Using ML to optimize ML execution", "order": 15},
            {"id": "browser-ml", "title": "ML in browsers and WebAssembly", "order": 16},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M07.L01.EX01",

            "title": "Think beyond the prediction endpoint",

            "lesson_code": "M07.L01",

            "section_id": "deployment-myths",

            "placement": "after_section",

            "description": (
                "Identify the operational requirements hidden by a simple model API."
            ),

            "instructions": (
                "Your team has a model behind a working `/predict` endpoint. It has "
                "only been tested by five engineers. The product team now wants to "
                "serve hundreds of thousands of users.\n\n"
                "1. List at least six production concerns that are not solved merely "
                "by having the endpoint.\n"
                "2. Explain why managing only one model version is unlikely to remain "
                "sufficient over time.\n"
                "3. Explain why a model can degrade even if its code does not change.\n"
                "4. Explain why the ability to update models quickly can become an "
                "important production capability."
            ),

            "expected_output": (
                "A production-readiness checklist covering scale, latency, availability, "
                "monitoring, updates, debugging, and model lifecycle concerns."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "deployment-reasoning",
                "production-readiness",
                "model-lifecycle",
            ],
        },

        {
            "id": "M07.L01.EX02",

            "title": "Choose batch, online, or hybrid prediction",

            "lesson_code": "M07.L01",

            "section_id": "choosing-mode",

            "placement": "after_section",

            "description": (
                "Select prediction modes based on freshness, latency, volume, and query predictability."
            ),

            "instructions": (
                "Choose batch, online, or a hybrid approach for each scenario and justify your choice:\n\n"
                "1. Generate a weekly list of customers most likely to buy a new subscription.\n"
                "2. Detect a fraudulent card transaction before approval.\n"
                "3. Produce movie recommendations for millions of known users, but update "
                "a user's recommendations quickly after they begin browsing a new genre.\n"
                "4. Translate arbitrary user-entered sentences.\n"
                "5. Recommend popular search queries using precomputed results for the "
                "head of the distribution and request-time inference for uncommon queries.\n\n"
                "For at least two cases, state whether the online path needs streaming "
                "features or can rely on batch features."
            ),

            "expected_output": (
                "Five mode selections with reasoning about latency, freshness, wasted "
                "computation, predictable requests, and feature freshness."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "batch-prediction",
                "online-prediction",
                "streaming-features",
                "hybrid-serving",
            ],
        },

        {
            "id": "M07.L01.EX03",

            "title": "Choose a compression strategy",

            "lesson_code": "M07.L01",

            "section_id": "compression-techniques",

            "placement": "after_section",

            "description": (
                "Compare compression methods for deployment constraints."
            ),

            "instructions": (
                "For each scenario, choose the most relevant compression approach "
                "from low-rank factorization, knowledge distillation, pruning, and quantization:\n\n"
                "1. You have a strong large teacher model but need a smaller deployment model.\n"
                "2. You want a general method to reduce parameter precision from 32-bit "
                "floating point to lower precision for inference.\n"
                "3. You want to remove or zero parameters that contribute little.\n"
                "4. You are redesigning convolution operations into smaller factorized operations.\n\n"
                "For each choice, state one important limitation or trade-off from the lesson."
            ),

            "expected_output": (
                "Four method selections with a correct explanation of the compression "
                "mechanism and one trade-off each."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "model-compression",
                "knowledge-distillation",
                "pruning",
                "quantization",
            ],
        },

        {
            "id": "M07.L01.EX04",

            "title": "Design a prediction service under constraints",

            "lesson_code": "M07.L01",

            "section_id": "browser-ml",

            "placement": "after_section",

            "description": (
                "Combine serving mode, feature pipeline, compression, and hardware placement."
            ),

            "instructions": (
                "You are designing a fall-detection feature for a wearable device. "
                "The system should work with unreliable internet, react quickly, avoid "
                "sending raw sensor data to the cloud when possible, and preserve battery life.\n\n"
                "1. Choose cloud, edge, or hybrid inference and explain why.\n"
                "2. Choose batch or online prediction.\n"
                "3. Explain whether streaming features are likely to be useful.\n"
                "4. Choose one model-compression method to investigate.\n"
                "5. Explain why model size alone is not enough—you must also consider "
                "hardware-specific execution efficiency.\n"
                "6. Name two local compiler optimizations that could reduce latency."
            ),

            "expected_output": (
                "A coherent deployment design connecting product requirements to "
                "prediction mode, feature freshness, model compression, and hardware."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "edge-inference",
                "online-prediction",
                "model-optimization",
                "systems-tradeoffs",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M07.L01.QZ01",

        "title": "Model Deployment and Prediction Service — Knowledge Check",

        "lesson_code": "M07.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M07.L01.Q01",
                "section_id": "deployment-basics",
                "question": (
                    "Which statement best describes production deployment?"
                ),
                "options": [
                    "It only means saving model weights to disk.",
                    "It means making the model accessible while also handling operational concerns such as scale, latency, availability, monitoring, and updates.",
                    "It is identical to training the model.",
                    "It only applies to cloud-hosted models.",
                ],
                "correct": 1,
                "explanation": (
                    "A callable model is only the beginning; production requires reliable operation under real workloads."
                ),
            },

            {
                "id": "M07.L01.Q02",
                "section_id": "model-export",
                "question": (
                    "What two broad pieces of a model are normally represented when it is exported?"
                ),
                "options": [
                    "Only its accuracy and latency",
                    "Its structure/definition and its learned parameter values",
                    "Only its training dataset",
                    "Only its API endpoint",
                ],
                "correct": 1,
                "explanation": (
                    "Serving needs both the model structure and the learned values used by that structure."
                ),
            },

            {
                "id": "M07.L01.Q03",
                "section_id": "deployment-myths",
                "question": (
                    "Why can a deployed model's performance degrade even if its code does not change?"
                ),
                "options": [
                    "Model files always become corrupted with age.",
                    "Production data distributions and user behavior can change over time.",
                    "Inference automatically changes the model weights.",
                    "Deployment removes model features.",
                ],
                "correct": 1,
                "explanation": (
                    "Data distribution shift can make a previously suitable model less accurate over time."
                ),
            },

            {
                "id": "M07.L01.Q04",
                "section_id": "prediction-modes",
                "question": (
                    "Which mode describes request-time prediction using both historical batch features and freshly computed streaming features?"
                ),
                "options": [
                    "Batch prediction only",
                    "Streaming prediction",
                    "Offline evaluation",
                    "Model export",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter uses streaming prediction for online inference that incorporates streaming features."
                ),
            },

            {
                "id": "M07.L01.Q05",
                "section_id": "batch-online",
                "question": (
                    "What is the main timing difference between batch and online prediction?"
                ),
                "options": [
                    "Batch predictions are generated ahead of or independently from requests; online predictions are generated when requests arrive.",
                    "Batch is always one example at a time.",
                    "Online prediction cannot use APIs.",
                    "There is no timing difference.",
                ],
                "correct": 0,
                "explanation": (
                    "Prediction timing relative to user requests is the core distinction."
                ),
            },

            {
                "id": "M07.L01.Q06",
                "section_id": "feature-freshness",
                "question": (
                    "A product embedding is precomputed nightly but fetched during an online recommendation request. How should it be described?"
                ),
                "options": [
                    "A streaming feature only",
                    "A batch feature that is also used as an online feature",
                    "Not a feature",
                    "A model parameter",
                ],
                "correct": 1,
                "explanation": (
                    "It was computed in batch, but because it is consumed in online inference it is also an online feature."
                ),
            },

            {
                "id": "M07.L01.Q07",
                "section_id": "choosing-mode",
                "question": (
                    "Why can batch prediction waste computation?"
                ),
                "options": [
                    "It cannot process multiple inputs.",
                    "It may generate predictions for users or requests that never occur.",
                    "It always requires GPUs.",
                    "It cannot store results.",
                ],
                "correct": 1,
                "explanation": (
                    "Precomputing for an entire population wastes work when only a small fraction of those predictions are consumed."
                ),
            },

            {
                "id": "M07.L01.Q08",
                "section_id": "online-requirements",
                "question": (
                    "What two components are essential for low-latency online prediction?"
                ),
                "options": [
                    "A large test set and a notebook",
                    "A near-real-time data/feature pipeline and a model fast enough for the latency budget",
                    "Only a faster database",
                    "Only quantization",
                ],
                "correct": 1,
                "explanation": (
                    "The prediction path includes both feature availability and model inference."
                ),
            },

            {
                "id": "M07.L01.Q09",
                "section_id": "pipeline-unification",
                "question": (
                    "Why are separate training and inference feature pipelines risky?"
                ),
                "options": [
                    "They guarantee identical output.",
                    "One implementation can change without the other, causing different feature values between training and serving.",
                    "They make models smaller.",
                    "They remove the need for monitoring.",
                ],
                "correct": 1,
                "explanation": (
                    "Duplicated feature logic is a common source of training-serving inconsistency."
                ),
            },

            {
                "id": "M07.L01.Q10",
                "section_id": "compression-techniques",
                "question": (
                    "Which compression method trains a smaller student to imitate a larger teacher?"
                ),
                "options": [
                    "Pruning",
                    "Knowledge distillation",
                    "Loop tiling",
                    "Feature hashing",
                ],
                "correct": 1,
                "explanation": (
                    "Knowledge distillation transfers behavior from a teacher model into a smaller student."
                ),
            },

            {
                "id": "M07.L01.Q11",
                "section_id": "compression-techniques",
                "question": (
                    "What is the core idea of quantization?"
                ),
                "options": [
                    "Increase every parameter to 64 bits.",
                    "Use fewer bits to represent parameters and/or activations.",
                    "Remove the prediction API.",
                    "Move all inference to the cloud.",
                ],
                "correct": 1,
                "explanation": (
                    "Lower precision reduces memory footprint and can speed computation."
                ),
            },

            {
                "id": "M07.L01.Q12",
                "section_id": "compression-techniques",
                "question": (
                    "What is an important risk of aggressive quantization?"
                ),
                "options": [
                    "Numerical rounding and range limitations can reduce model quality.",
                    "It always increases memory usage.",
                    "It prevents integer inference.",
                    "It makes the model impossible to export.",
                ],
                "correct": 0,
                "explanation": (
                    "Reducing precision introduces rounding/scaling error and a smaller representable range."
                ),
            },

            {
                "id": "M07.L01.Q13",
                "section_id": "cloud-edge",
                "question": (
                    "Which is a major advantage of edge inference?"
                ),
                "options": [
                    "It guarantees unlimited compute.",
                    "It can reduce network dependence and keep more user data local.",
                    "It removes all battery constraints.",
                    "It always runs faster than every cloud system.",
                ],
                "correct": 1,
                "explanation": (
                    "Local execution can reduce network latency, support offline use, and improve some privacy properties."
                ),
            },

            {
                "id": "M07.L01.Q14",
                "section_id": "compilers-ir",
                "question": (
                    "Why are intermediate representations useful in ML compilers?"
                ),
                "options": [
                    "They allow frameworks and hardware backends to communicate through shared compiler abstractions instead of every pair requiring direct support.",
                    "They eliminate model parameters.",
                    "They replace all training data.",
                    "They are only used for browser rendering.",
                ],
                "correct": 0,
                "explanation": (
                    "IRs reduce the many-to-many integration burden between frameworks and hardware targets."
                ),
            },

            {
                "id": "M07.L01.Q15",
                "section_id": "model-optimization",
                "question": (
                    "What is operator fusion primarily trying to reduce?"
                ),
                "options": [
                    "The number of model labels",
                    "Redundant memory reads and writes between operations",
                    "The number of users",
                    "The size of the validation split",
                ],
                "correct": 1,
                "explanation": (
                    "Fusing operations can keep intermediate data local and avoid unnecessary memory movement."
                ),
            },

            {
                "id": "M07.L01.Q16",
                "section_id": "ml-optimizing-ml",
                "question": (
                    "Why might an autotuning compiler learn a cost model?"
                ),
                "options": [
                    "To predict promising execution strategies without exhaustively running every possible plan",
                    "To label training data for the deployed model",
                    "To replace model calibration",
                    "To generate business metrics",
                ],
                "correct": 0,
                "explanation": (
                    "The execution-plan search space can be too large to explore exhaustively, so a cost model can guide the search."
                ),
            },

            {
                "id": "M07.L01.Q17",
                "section_id": "browser-ml",
                "question": (
                    "What is the main appeal of compiling ML workloads to WebAssembly in the chapter?"
                ),
                "options": [
                    "It guarantees native-device performance.",
                    "It provides portable execution across many browser-capable devices.",
                    "It only works on one hardware vendor.",
                    "It removes all model optimization needs.",
                ],
                "correct": 1,
                "explanation": (
                    "Browser support provides broad portability, though WASM can still be slower than native execution."
                ),
            },

            {
                "id": "M07.L01.Q18",
                "section_id": "pipeline-unification",
                "type": "open",
                "question": (
                    "Design a serving architecture for an ETA model that uses a restaurant's "
                    "historical average preparation time plus the number of orders and available "
                    "delivery workers in the last ten minutes. Explain which features are batch "
                    "versus streaming, whether inference should be batch or online, how you would "
                    "reduce training-serving inconsistency, and what latency-related bottlenecks "
                    "you would monitor."
                ),
            },
        ],

        "passing_score": 70,
    },
}
