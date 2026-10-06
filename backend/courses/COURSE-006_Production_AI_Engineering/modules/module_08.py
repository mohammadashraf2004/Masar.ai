"""M09.L01 — Inference Optimization.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 9, "Inference Optimization".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M09.L01"
MODULE_ORDER = 9
MODULE_TITLE = "Inference Optimization"
MODULE_DESCRIPTION = (
    "Learn how to make foundation-model inference faster and cheaper by "
    "understanding bottlenecks, latency/throughput/utilization metrics, accelerators, "
    "model compression, decoding optimization, attention/KV-cache optimization, "
    "kernels/compilers, batching, caching, prefill/decode disaggregation, and parallelism."
)
SOURCE_CHAPTER = 9
SOURCE_PAGES = "Page range not provided in the supplied chapter text"


TOPIC = {
    "title": "Inference Optimization",
    "slug": "ai-engineering-m09-l01-inference-optimization",
    "description": (
        "A complete learner-facing guide to inference optimization for foundation models, "
        "covering computational bottlenecks, TTFT/TPOT/goodput, hardware efficiency, "
        "quantization/distillation/pruning, speculative and parallel decoding, KV-cache "
        "optimization, FlashAttention, kernels and compilers, batching, prompt caching, "
        "prefill/decode disaggregation, and model/service parallelism."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 6.0,
    "skill_tags": [
        "inference-optimization",
        "latency",
        "throughput",
        "goodput",
        "gpu-utilization",
        "mfu",
        "mbu",
        "accelerators",
        "speculative-decoding",
        "kv-cache",
        "attention-optimization",
        "kernels",
        "compilers",
        "batching",
        "prompt-caching",
        "parallelism",
    ],
    "prerequisite_ids": [],

    "lesson": {
        "title": "Inference Optimization",
        "content": (
            "# Inference Optimization\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M09.L01  \n"
            "> **Module:** Inference Optimization  \n"
            "> **Source alignment:** Chapter 9, *Inference Optimization*. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why inference latency and cost directly affect model usability.\n"
            "- Distinguish model-level, hardware-level, and service-level optimization.\n"
            "- Explain what an inference server and inference service do.\n"
            "- Distinguish compute-bound from memory-bandwidth-bound workloads.\n"
            "- Explain arithmetic intensity and the intuition behind roofline analysis.\n"
            "- Explain why LLM prefill is usually compute-bound while decoding is often bandwidth-bound.\n"
            "- Distinguish online APIs from batch APIs and explain the latency/cost tradeoff.\n"
            "- Explain streaming and its benefits and risks.\n"
            "- Measure latency using TTFT, TPOT, TBT/ITL, total latency, and percentiles.\n"
            "- Measure capacity using throughput, RPM/RPS, and goodput.\n"
            "- Explain utilization, GPU utilization, MFU, and MBU.\n"
            "- Explain how model size, precision, tokens/s, and memory bandwidth interact.\n"
            "- Compare CPU and GPU architecture at a high level.\n"
            "- Explain accelerator FLOP/s, memory size, bandwidth, and power considerations.\n"
            "- Choose hardware according to compute-bound versus memory-bound workloads.\n"
            "- Explain model compression through quantization, distillation, and pruning.\n"
            "- Explain speculative decoding, inference with reference, and parallel decoding.\n"
            "- Explain the purpose and memory cost of the KV cache.\n"
            "- Calculate approximate KV-cache memory from batch size, sequence length, layers, hidden dimension, and bytes/value.\n"
            "- Compare local attention, multi-query attention, grouped-query attention, and cross-layer attention.\n"
            "- Explain PagedAttention, KV-cache quantization, compression, and selective caching.\n"
            "- Explain FlashAttention and why hardware-aware kernels matter.\n"
            "- Explain vectorization, parallelization, loop tiling, and operator fusion.\n"
            "- Explain the role of compilers such as torch.compile/XLA-style systems in lowering models to hardware.\n"
            "- Compare static, dynamic, and continuous batching.\n"
            "- Explain prefill/decode disaggregation.\n"
            "- Explain prompt/prefix caching and when it provides large gains.\n"
            "- Compare replica, tensor, pipeline, context, and sequence parallelism.\n"
            "- Design an optimization plan around workload characteristics instead of applying every technique blindly.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why inference optimization matters\n"
            "\n"
            "A model can be highly accurate and still fail as a product if it is too "
            "slow or too expensive to use.\n"
            "\n"
            "The chapter frames inference optimization around two practical goals:\n"
            "\n"
            "- **Faster:** reduce response latency.\n"
            "- **Cheaper:** use hardware and model capacity more efficiently.\n"
            "\n"
            "Optimization can happen at three levels:\n"
            "\n"
            "1. **Model level** — change the model or its computation.\n"
            "2. **Hardware level** — use hardware better suited to the workload.\n"
            "3. **Service level** — allocate resources and schedule requests more efficiently.\n"
            "\n"
            "These levels interact. A quantized model may fit on cheaper hardware. A "
            "better serving scheduler may increase utilization without changing model weights.\n"
            "\n"
            '{{image:inference-optimization-levels}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. What an inference service does\n"
            "\n"
            "**Training** builds or updates a model. **Inference** uses a trained model "
            "to compute outputs from inputs.\n"
            "\n"
            "In production, an **inference server** hosts models and runs their forward passes "
            "on available hardware.\n"
            "\n"
            "A broader **inference service** can also:\n"
            "\n"
            "- Receive requests.\n"
            "- Route requests to models or servers.\n"
            "- Preprocess inputs.\n"
            "- Schedule work.\n"
            "- Stream outputs.\n"
            "- Track resource usage.\n"
            "\n"
            "Commercial model APIs are inference services. If you self-host a model, "
            "you inherit much more responsibility for this layer.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Start by identifying the bottleneck\n"
            "\n"
            "Optimization should target the part of the system that is actually limiting performance.\n"
            "\n"
            "The chapter introduces two main computational bottlenecks.\n"
            "\n"
            "### Compute-bound\n"
            "\n"
            "Runtime is limited mainly by the amount of arithmetic the hardware can perform.\n"
            "\n"
            "Useful responses include:\n"
            "\n"
            "- More compute units.\n"
            "- Faster accelerators.\n"
            "- More parallelism.\n"
            "- Better kernels.\n"
            "\n"
            "### Memory-bandwidth-bound\n"
            "\n"
            "Runtime is limited mainly by how fast data can move between memory and compute units.\n"
            "\n"
            "Useful responses include:\n"
            "\n"
            "- Higher-bandwidth hardware.\n"
            "- Smaller models / lower precision.\n"
            "- Better caching.\n"
            "- Better memory layout.\n"
            "- Fewer repeated memory transfers.\n"
            "\n"
            "The word **memory-bound** is sometimes used ambiguously to mean either "
            "bandwidth-limited or capacity-limited. The chapter emphasizes that even "
            "capacity problems often turn into bandwidth problems when data must be moved "
            "between CPU and GPU memory.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Arithmetic intensity and the roofline intuition\n"
            "\n"
            "**Arithmetic intensity** roughly means:\n"
            "\n"
            "```text\n"
            "arithmetic operations / bytes of memory accessed\n"
            "```\n"
            "\n"
            "Low arithmetic intensity means the hardware spends much of its time moving "
            "data relative to doing math. High arithmetic intensity means more computation "
            "is performed per byte loaded.\n"
            "\n"
            "A **roofline chart** helps determine whether a workload is limited by "
            "compute or memory bandwidth.\n"
            "\n"
            "This matters because a faster arithmetic unit does little for a workload "
            "that is waiting on memory, and extra bandwidth may do little for a workload "
            "already dominated by arithmetic.\n"
            "\n"
            "[[IMAGE_NEEDED: Roofline model intuition | A simplified roofline graph with "
            "a bandwidth-limited rising region and compute-limited flat region | Learner "
            "should notice that optimization depends on which side of the bottleneck the "
            "workload occupies]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. LLM inference has two very different phases\n"
            "\n"
            "Transformer-based autoregressive language-model inference is commonly divided into:\n"
            "\n"
            "### Prefill\n"
            "\n"
            "The model processes input tokens largely in parallel and initializes the "
            "attention state used for generation.\n"
            "\n"
            "Prefill is typically **compute-bound**.\n"
            "\n"
            "### Decode\n"
            "\n"
            "The model generates output tokens one at a time.\n"
            "\n"
            "At each step, large model weights and attention state must be accessed. "
            "Decode is therefore commonly **memory-bandwidth-bound**.\n"
            "\n"
            "This distinction explains many later techniques, including:\n"
            "\n"
            "- Separate prefill/decode servers.\n"
            "- TTFT versus TPOT optimization.\n"
            "- Speculative decoding.\n"
            "- KV-cache optimization.\n"
            "\n"
            "[[IMAGE_NEEDED: Prefill versus decode | A two-phase LLM inference diagram "
            "showing parallel input processing during prefill and one-token-at-a-time "
            "generation during decode | Learner should notice the different compute profiles]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Online APIs versus batch APIs\n"
            "\n"
            "Inference systems often expose two broad service modes.\n"
            "\n"
            "### Online inference\n"
            "\n"
            "Optimizes for low latency. Requests are processed as soon as practical.\n"
            "\n"
            "Typical use cases:\n"
            "\n"
            "- Chatbots.\n"
            "- Interactive coding assistants.\n"
            "- Real-time user-facing generation.\n"
            "\n"
            "### Batch inference\n"
            "\n"
            "Optimizes for cost and throughput. Requests can wait so the service can use "
            "larger batches, cheaper hardware, or more relaxed scheduling.\n"
            "\n"
            "Typical use cases:\n"
            "\n"
            "- Synthetic data generation.\n"
            "- Periodic reports.\n"
            "- Large document reprocessing.\n"
            "- Customer onboarding pipelines.\n"
            "- Recommendation/newsletter generation.\n"
            "- Knowledge-base reindexing.\n"
            "\n"
            "The important distinction is the optimization objective: **online -> latency; "
            "batch -> throughput/cost**.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Streaming changes perceived latency\n"
            "\n"
            "Autoregressive generation can take a long time to complete. Streaming lets "
            "the application return tokens as they are produced instead of waiting for the "
            "entire response.\n"
            "\n"
            "Benefits:\n"
            "\n"
            "- The user sees progress sooner.\n"
            "- Perceived responsiveness improves.\n"
            "\n"
            "Tradeoff:\n"
            "\n"
            "- The full response cannot be scored or screened before the first tokens "
            "are shown.\n"
            "\n"
            "Streaming therefore improves responsiveness but can complicate safety or "
            "post-generation validation.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Latency metrics: TTFT, TPOT, and total latency\n"
            "\n"
            "For autoregressive models, total latency can be decomposed into useful pieces.\n"
            "\n"
            "### Time to first token (TTFT)\n"
            "\n"
            "Time from request arrival until the first generated token appears.\n"
            "\n"
            "TTFT is heavily influenced by prefill and therefore by input length.\n"
            "\n"
            "### Time per output token (TPOT)\n"
            "\n"
            "Average generation time for each token after the first token.\n"
            "\n"
            "### Time between tokens / inter-token latency\n"
            "\n"
            "Measures gaps between streamed tokens.\n"
            "\n"
            "A simple latency approximation is:\n"
            "\n"
            "```text\n"
            "total latency ≈ TTFT + TPOT × number_of_output_tokens\n"
            "```\n"
            "\n"
            "Two systems with the same total latency can feel different: one may start "
            "instantly but generate slowly; another may wait longer and then generate quickly.\n"
            "\n"
            "[[IMAGE_NEEDED: TTFT and TPOT timeline | A request timeline marking request "
            "arrival, first token, subsequent tokens, and completion | Learner should "
            "notice how first-token delay and per-token generation contribute differently "
            "to total latency]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Model latency is not always user-visible latency\n"
            "\n"
            "Agentic applications may generate plans, tool calls, or hidden intermediate "
            "tokens before producing anything visible to the user.\n"
            "\n"
            "From the model's perspective, token generation has already started. From the "
            "user's perspective, nothing has appeared yet.\n"
            "\n"
            "This is why some teams track a metric such as **time to publish**: time until "
            "the first user-visible output appears.\n"
            "\n"
            "Measure the experience your user sees, not only the internal model timings.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Measure latency as a distribution\n"
            "\n"
            "Average latency can hide serious outliers.\n"
            "\n"
            "Useful percentiles include:\n"
            "\n"
            "- **p50** — median.\n"
            "- **p90** — 90% of requests are faster than this value.\n"
            "- **p95**.\n"
            "- **p99** — exposes tail-latency problems.\n"
            "\n"
            "Also plot latency against workload variables such as input length. A long prompt "
            "may produce a legitimate high TTFT, while a network problem may produce an "
            "unexpected outlier.\n"
            "\n"
            "Production optimization should care about the tail, not only the average.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Throughput and request capacity\n"
            "\n"
            "**Throughput** measures the amount of work completed per unit time.\n"
            "\n"
            "Common measures include:\n"
            "\n"
            "- Output tokens per second (TPS).\n"
            "- Input tokens per second.\n"
            "- Tokens/s/user.\n"
            "- Requests per second (RPS).\n"
            "- Completed requests per minute (RPM).\n"
            "\n"
            "Input and output throughput should often be tracked separately because "
            "prefill and decode have different bottlenecks.\n"
            "\n"
            "Throughput is tightly linked to cost. If the same hardware produces more useful "
            "tokens per second, cost per token or request usually falls.\n"
            "\n"
            "However, higher throughput can increase request waiting and hurt latency.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Goodput: throughput that actually meets the SLO\n"
            "\n"
            "A service can report impressive throughput while giving users poor latency.\n"
            "\n"
            "**Goodput** counts only requests that meet a defined service-level objective (SLO).\n"
            "\n"
            "Example SLO:\n"
            "\n"
            "```text\n"
            "TTFT <= 200 ms\n"
            "TPOT <= 100 ms\n"
            "```\n"
            "\n"
            "If the service completes 100 requests/minute but only 30 satisfy both targets:\n"
            "\n"
            "```text\n"
            "throughput = 100 requests/min\n"
            "goodput    = 30 requests/min\n"
            "```\n"
            "\n"
            "Goodput forces the system to optimize capacity **and** user experience together.\n"
            "\n"
            "[[IMAGE_NEEDED: Throughput versus goodput | A bar of all completed requests "
            "with only the SLO-satisfying portion highlighted as goodput | Learner should "
            "notice that raw throughput can overstate useful serving capacity]]\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Utilization is not one number\n"
            "\n"
            "Utilization measures how efficiently hardware capacity is being used, but "
            "different metrics mean different things.\n"
            "\n"
            "A common GPU utilization metric reports how often the GPU is active, not how "
            "close it is to peak arithmetic efficiency.\n"
            "\n"
            "A GPU can therefore appear highly 'utilized' while performing far below its "
            "theoretical compute capacity.\n"
            "\n"
            "Two more informative metrics are:\n"
            "\n"
            "- **MFU** — Model FLOP/s Utilization.\n"
            "- **MBU** — Model Bandwidth Utilization.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. MFU: Model FLOP/s Utilization\n"
            "\n"
            "MFU compares observed computational throughput with the hardware's theoretical "
            "maximum for the workload/model.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "MFU = observed model FLOP/s / theoretical peak model FLOP/s\n"
            "```\n"
            "\n"
            "Compute-bound workloads tend to care strongly about MFU.\n"
            "\n"
            "Prefill often shows higher MFU than decode because decode frequently waits on "
            "memory movement instead of saturating arithmetic units.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. MBU: Model Bandwidth Utilization\n"
            "\n"
            "MBU measures how much of the achievable memory bandwidth the workload uses.\n"
            "\n"
            "The chapter provides the useful approximation:\n"
            "\n"
            "```text\n"
            "bandwidth_used ≈ parameter_count × bytes_per_parameter × tokens_per_second\n"
            "\n"
            "MBU = bandwidth_used / theoretical_memory_bandwidth\n"
            "```\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "7B parameters\n"
            "× 2 bytes/parameter\n"
            "× 100 tokens/s\n"
            "= 1400 GB/s\n"
            "```\n"
            "\n"
            "The key insight is that **quantization reduces bytes per parameter**, which "
            "can directly reduce bandwidth pressure during decoding.\n"
            "\n"
            "Do not optimize utilization for its own sake. The real goal remains better "
            "latency and cost for the workload.\n"
            "\n"
            "{{exercise:M09.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 16. AI accelerators\n"
            "\n"
            "An **accelerator** is a chip specialized for a computational workload. GPUs "
            "became central to deep learning because neural-network operations—especially "
            "matrix multiplication—parallelize well.\n"
            "\n"
            "### CPU intuition\n"
            "\n"
            "- Fewer powerful cores.\n"
            "- Strong at sequential/control-heavy work.\n"
            "- Good general-purpose behavior and I/O orchestration.\n"
            "\n"
            "### GPU intuition\n"
            "\n"
            "- Many smaller cores.\n"
            "- Designed for massive parallelism.\n"
            "- Strong for matrix/tensor operations.\n"
            "\n"
            "Other AI accelerators exist, and some specialize further toward inference or "
            "particular model operations.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. What to compare in an accelerator\n"
            "\n"
            "The chapter highlights three major capability dimensions plus power.\n"
            "\n"
            "### Compute capability\n"
            "\n"
            "Often represented as FLOP/s for different numerical formats.\n"
            "\n"
            "Lower precision can allow much higher operations/second on compatible hardware.\n"
            "\n"
            "### Memory size\n"
            "\n"
            "Determines whether model weights, caches, and batches fit.\n"
            "\n"
            "### Memory bandwidth\n"
            "\n"
            "Determines how quickly data can move between memory and compute units.\n"
            "\n"
            "### Power consumption\n"
            "\n"
            "Affects infrastructure cost, cooling, and environmental impact.\n"
            "\n"
            "A useful hardware-selection test is:\n"
            "\n"
            "1. Can it run the workload?\n"
            "2. How long does the workload take?\n"
            "3. How much does it cost?\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Accelerator memory hierarchy\n"
            "\n"
            "AI accelerators interact with multiple memory levels.\n"
            "\n"
            "### CPU/system memory\n"
            "\n"
            "- Large capacity.\n"
            "- Lower bandwidth.\n"
            "- Farther from GPU compute.\n"
            "\n"
            "### GPU high-bandwidth memory (HBM)\n"
            "\n"
            "- Much faster.\n"
            "- Smaller and more expensive.\n"
            "- Stores model weights and active inference state.\n"
            "\n"
            "### On-chip SRAM/cache/registers\n"
            "\n"
            "- Extremely fast.\n"
            "- Very small.\n"
            "- Useful for repeatedly accessed data.\n"
            "\n"
            "Much GPU optimization is fundamentally about minimizing expensive data movement "
            "through this hierarchy.\n"
            "\n"
            "[[IMAGE_NEEDED: Accelerator memory hierarchy | A memory pyramid showing CPU "
            "DRAM at large/slow bottom, GPU HBM in the middle, and small/fast on-chip "
            "SRAM/registers at the top | Learner should notice the capacity-versus-bandwidth "
            "tradeoff across memory levels]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Select hardware for the actual workload\n"
            "\n"
            "If the workload is compute-bound, more FLOP/s can help.\n"
            "\n"
            "If it is bandwidth-bound, memory bandwidth and model size/precision may matter "
            "more than advertised peak compute.\n"
            "\n"
            "Do not buy hardware from a single headline number. Measure the exact model, "
            "precision, sequence lengths, batch sizes, and traffic pattern you expect to serve.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Model-level optimization: compression\n"
            "\n"
            "Model compression reduces the amount of computation or storage required for inference.\n"
            "\n"
            "The chapter discusses three important families.\n"
            "\n"
            "### Quantization\n"
            "\n"
            "Represent weights using fewer bits.\n"
            "\n"
            "- Lower memory footprint.\n"
            "- Lower bandwidth pressure.\n"
            "- Often higher throughput.\n"
            "- Possible quality loss.\n"
            "\n"
            "### Distillation\n"
            "\n"
            "Train a smaller student model to imitate a larger teacher.\n"
            "\n"
            "### Pruning\n"
            "\n"
            "Remove network components or set low-value parameters to zero, creating a "
            "smaller or sparser model.\n"
            "\n"
            "Pruning is attractive in theory but can be harder to exploit in practice "
            "because hardware must efficiently support the resulting sparsity.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. The autoregressive decoding bottleneck\n"
            "\n"
            "An autoregressive language model normally produces one token at a time:\n"
            "\n"
            "```text\n"
            "token 1 -> token 2 -> token 3 -> ...\n"
            "```\n"
            "\n"
            "Each new token depends on the previous context. This sequential dependency makes "
            "output generation expensive and slow.\n"
            "\n"
            "Output tokens can be particularly costly because decoding repeatedly accesses the "
            "full model while generating only one new token per step.\n"
            "\n"
            "This bottleneck motivates techniques that try to verify several tokens at once or "
            "generate multiple future-token candidates in parallel.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Speculative decoding\n"
            "\n"
            "Speculative decoding uses two models:\n"
            "\n"
            "- **Draft model:** fast and weaker.\n"
            "- **Target model:** slower and stronger; its behavior is the one you want.\n"
            "\n"
            "Basic loop:\n"
            "\n"
            "1. Draft model proposes `K` tokens.\n"
            "2. Target model verifies those tokens in parallel.\n"
            "3. Accept the longest prefix that the target agrees with.\n"
            "4. Target produces one additional token.\n"
            "5. Repeat.\n"
            "\n"
            "This helps because verification of multiple proposed tokens can be more parallel "
            "than generating them sequentially.\n"
            "\n"
            "It works best when the draft model has a high acceptance rate. Structured text "
            "such as code can be especially friendly to this method.\n"
            "\n"
            "[[IMAGE_NEEDED: Speculative decoding | A draft model proposing K tokens and a "
            "target model accepting the longest valid prefix in one verification pass | "
            "Learner should notice how verification parallelizes work that would otherwise "
            "be sequential]]\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Inference with reference\n"
            "\n"
            "Sometimes much of the output already appears in the input.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Editing code while keeping most lines unchanged.\n"
            "- Quoting from a retrieved document.\n"
            "- Continuing a conversation with repeated context.\n"
            "\n"
            "Instead of asking another model to draft tokens, **inference with reference** "
            "tries to reuse candidate token spans directly from the input.\n"
            "\n"
            "It avoids an extra draft model but is useful mainly when input/output overlap is high.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Parallel decoding\n"
            "\n"
            "Parallel-decoding methods try to predict several future tokens simultaneously, "
            "reducing strict one-token-at-a-time dependence.\n"
            "\n"
            "Examples in the chapter include:\n"
            "\n"
            "- Lookahead/Jacobi-style decoding.\n"
            "- Medusa-style extra decoding heads.\n"
            "\n"
            "Because future tokens are predicted without knowing all preceding generated tokens, "
            "a verification step is required.\n"
            "\n"
            "The general pattern is:\n"
            "\n"
            "```text\n"
            "predict several future tokens\n"
            " -> verify consistency\n"
            " -> keep valid tokens\n"
            " -> repair/recompute invalid tokens\n"
            "```\n"
            "\n"
            "These techniques can provide speedups but are more complex to implement than "
            "ordinary autoregressive decoding.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. The KV cache\n"
            "\n"
            "Transformer attention repeatedly needs key and value vectors from previous tokens.\n"
            "\n"
            "Without caching, the model would recompute them again and again during decoding.\n"
            "\n"
            "The **KV cache** stores previous key/value vectors so that each generation step "
            "only needs to compute new vectors for the newest token.\n"
            "\n"
            "KV caching speeds decoding but creates a memory problem:\n"
            "\n"
            "- Longer context -> larger cache.\n"
            "- Larger batches -> larger cache.\n"
            "- More layers -> larger cache.\n"
            "- Larger hidden dimension -> larger cache.\n"
            "\n"
            "KV cache is an inference concern; training knows the full sequence and does not "
            "use this same sequential inference cache.\n"
            "\n"
            "[[IMAGE_NEEDED: KV-cache reuse | Several decoding steps where old K/V vectors "
            "remain cached and only the newest token's K/V is added | Learner should notice "
            "that caching removes recomputation but grows memory over the sequence]]\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Calculate KV-cache memory\n"
            "\n"
            "The chapter gives the unoptimized approximation:\n"
            "\n"
            "```text\n"
            "KV cache bytes = 2 × B × S × L × H × M\n"
            "```\n"
            "\n"
            "where:\n"
            "\n"
            "- `B` = batch size.\n"
            "- `S` = sequence length.\n"
            "- `L` = number of transformer layers.\n"
            "- `H` = model/hidden dimension.\n"
            "- `M` = bytes per cached value.\n"
            "- factor `2` represents keys and values.\n"
            "\n"
            "This equation makes the scaling problem visible. Doubling batch size or context "
            "length doubles KV-cache memory.\n"
            "\n"
            "For long-context serving, KV-cache memory can become as important as—or even "
            "larger than—the model weights themselves.\n"
            "\n"
            "{{exercise:M09.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Redesigning attention to reduce KV cost\n"
            "\n"
            "Some optimizations change the model architecture and therefore generally must be "
            "introduced during training or finetuning.\n"
            "\n"
            "### Local/windowed attention\n"
            "\n"
            "Attend only to a fixed nearby window instead of the entire history.\n"
            "\n"
            "### Multi-query attention (MQA)\n"
            "\n"
            "Share key/value vectors across query heads.\n"
            "\n"
            "### Grouped-query attention (GQA)\n"
            "\n"
            "Group query heads and share key/value pairs inside each group, balancing memory "
            "savings with representational flexibility.\n"
            "\n"
            "### Cross-layer attention\n"
            "\n"
            "Share key/value representations across adjacent layers.\n"
            "\n"
            "All these methods attack the same problem: reduce the number or lifetime of "
            "key/value states required during inference.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. KV-cache management and PagedAttention\n"
            "\n"
            "Even without redesigning attention, the serving system can manage KV memory more efficiently.\n"
            "\n"
            "### PagedAttention\n"
            "\n"
            "Split KV-cache memory into non-contiguous blocks instead of requiring one large "
            "contiguous allocation per sequence.\n"
            "\n"
            "Benefits include:\n"
            "\n"
            "- Less fragmentation.\n"
            "- Better memory sharing.\n"
            "- More flexible allocation as sequences grow and finish.\n"
            "\n"
            "Other approaches mentioned include:\n"
            "\n"
            "- KV-cache quantization.\n"
            "- Adaptive KV-cache compression.\n"
            "- Selective KV caching.\n"
            "\n"
            "The goal is to fit more concurrent useful work into limited accelerator memory.\n"
            "\n"
            "[[IMAGE_NEEDED: Paged KV cache | A comparison between fragmented contiguous "
            "KV allocations and page/block-based allocations packed flexibly into GPU memory | "
            "Learner should notice how paging reduces wasted memory space]]\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Attention kernels and FlashAttention\n"
            "\n"
            "Another optimization path keeps the attention algorithm conceptually similar but "
            "changes **how the computation is executed on hardware**.\n"
            "\n"
            "FlashAttention is a well-known example of a hardware-aware attention kernel. "
            "It reduces unnecessary memory movement and fuses operations so attention can run "
            "more efficiently on modern accelerators.\n"
            "\n"
            "This illustrates a broad systems principle:\n"
            "\n"
            "> Equivalent mathematics can run at very different speeds depending on memory "
            "layout, operation ordering, and hardware-specific implementation.\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Kernels: optimized code close to the hardware\n"
            "\n"
            "A **kernel** is specialized code optimized for an accelerator and a repeated "
            "computational operation.\n"
            "\n"
            "Common ML kernels include:\n"
            "\n"
            "- Matrix multiplication.\n"
            "- Attention.\n"
            "- Convolution.\n"
            "\n"
            "Kernel optimization requires understanding the hardware memory hierarchy, "
            "threading, and movement of data between registers, caches, shared memory, and "
            "global memory.\n"
            "\n"
            "Languages/tools mentioned by the chapter include low-level GPU ecosystems such "
            "as CUDA, Triton, and ROCm.\n"
            "\n"
            "---\n"
            "\n"

            "## 31. Four common kernel-optimization techniques\n"
            "\n"
            "### Vectorization\n"
            "\n"
            "Process multiple nearby data values per instruction/operation rather than one "
            "element at a time.\n"
            "\n"
            "### Parallelization\n"
            "\n"
            "Split independent pieces of work across threads/cores.\n"
            "\n"
            "### Loop tiling\n"
            "\n"
            "Reorder and block computation so frequently used data stays in faster memory/cache.\n"
            "\n"
            "### Operator fusion\n"
            "\n"
            "Combine several operators into one hardware pass so intermediate values do not "
            "need to be repeatedly written to and reloaded from slower memory.\n"
            "\n"
            "These techniques often target **data movement** as much as arithmetic.\n"
            "\n"
            "[[IMAGE_NEEDED: Operator fusion | A before/after diagram where operator A writes "
            "an intermediate tensor to memory and operator B reloads it, versus a fused kernel "
            "keeping the intermediate on-chip | Learner should notice the avoided memory traffic]]\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Compilers connect model graphs to hardware\n"
            "\n"
            "A model is expressed as operations. Hardware executes lower-level instructions.\n"
            "\n"
            "**Lowering** is the process of converting high-level model operations into code "
            "that a target hardware architecture can execute efficiently.\n"
            "\n"
            "A compiler can:\n"
            "\n"
            "- Rewrite graphs.\n"
            "- Fuse operators.\n"
            "- Select optimized kernels.\n"
            "- Specialize execution for shapes and devices.\n"
            "\n"
            "The chapter mentions standalone and integrated compiler systems, including "
            "torch.compile-style compilation, XLA/OpenXLA, TensorRT-related compilation, "
            "TVM, and MLIR-style infrastructure.\n"
            "\n"
            "Compilers matter because hand-optimizing every model/hardware combination does "
            "not scale.\n"
            "\n"
            "---\n"
            "\n"

            "## 33. Service-level optimization\n"
            "\n"
            "Service-level optimization focuses on how requests are scheduled onto fixed "
            "compute and memory resources.\n"
            "\n"
            "Unlike model-level techniques, service-level methods generally leave model "
            "weights and behavior unchanged.\n"
            "\n"
            "Important service-level techniques in the chapter include:\n"
            "\n"
            "- Batching.\n"
            "- Prefill/decode disaggregation.\n"
            "- Prompt caching.\n"
            "- Parallelism.\n"
            "\n"
            "---\n"
            "\n"

            "## 34. Batching: share hardware across requests\n"
            "\n"
            "Batching processes several requests together, increasing hardware efficiency.\n"
            "\n"
            "The tradeoff is familiar:\n"
            "\n"
            "- Larger/more efficient batches -> higher throughput/lower cost.\n"
            "- Waiting to form batches -> potentially higher latency.\n"
            "\n"
            "The chapter discusses three important batching strategies.\n"
            "\n"
            "---\n"
            "\n"

            "## 35. Static and dynamic batching\n"
            "\n"
            "### Static batching\n"
            "\n"
            "Wait until a fixed batch size is full.\n"
            "\n"
            "Advantage:\n"
            "\n"
            "- Predictable full batches.\n"
            "\n"
            "Disadvantage:\n"
            "\n"
            "- Early requests can wait a long time for later arrivals.\n"
            "\n"
            "### Dynamic batching\n"
            "\n"
            "Process when either:\n"
            "\n"
            "- Batch is full, or\n"
            "- A maximum waiting window expires.\n"
            "\n"
            "This bounds queueing latency but sometimes runs partially filled batches.\n"
            "\n"
            "[[IMAGE_NEEDED: Static versus dynamic batching | A timeline of arriving requests "
            "where static waits for a full batch and dynamic launches when full or timeout "
            "occurs | Learner should notice the throughput-versus-queueing-latency tradeoff]]\n"
            "\n"
            "---\n"
            "\n"

            "## 36. Continuous batching\n"
            "\n"
            "Naive batching can make short generations wait for long generations in the same batch.\n"
            "\n"
            "**Continuous batching** allows completed requests to leave immediately and new "
            "requests to enter available batch slots while other requests continue decoding.\n"
            "\n"
            "This improves occupancy without forcing every request to have the same output length.\n"
            "\n"
            "It is especially important for LLM serving because response lengths vary dramatically.\n"
            "\n"
            "[[IMAGE_NEEDED: Continuous batching | A batch-slot timeline where one request "
            "finishes early and is immediately replaced by a new request while longer requests "
            "continue | Learner should notice why variable-length workloads benefit from in-flight batching]]\n"
            "\n"
            "---\n"
            "\n"

            "## 37. Decouple prefill and decode\n"
            "\n"
            "Prefill and decode compete for different resources:\n"
            "\n"
            "- Prefill wants compute.\n"
            "- Decode wants memory bandwidth.\n"
            "\n"
            "Running them on the same saturated GPU can cause interference.\n"
            "\n"
            "A disaggregated serving architecture uses separate instances for the two phases:\n"
            "\n"
            "```text\n"
            "request -> prefill workers -> transfer intermediate state -> decode workers\n"
            "```\n"
            "\n"
            "The correct ratio of prefill workers to decode workers depends on input length, "
            "output length, and whether the product prioritizes TTFT or TPOT.\n"
            "\n"
            "This is an example of optimizing the service around the model's computational profile.\n"
            "\n"
            "---\n"
            "\n"

            "## 38. Prompt caching\n"
            "\n"
            "Many requests share large prompt prefixes:\n"
            "\n"
            "- System prompts.\n"
            "- The same long document.\n"
            "- Earlier messages in a long conversation.\n"
            "- Shared few-shot examples.\n"
            "\n"
            "A **prompt cache** or **prefix/context cache** stores processed state for these "
            "segments so the service does not recompute them for every request.\n"
            "\n"
            "Prompt caching can significantly reduce input-processing latency and cost for "
            "applications with long, repeated prefixes.\n"
            "\n"
            "The tradeoff is memory/storage: cached context itself consumes resources and must "
            "be managed.\n"
            "\n"
            "[[IMAGE_NEEDED: Prompt caching | Two requests sharing a long system prompt where "
            "the first request computes/caches the prefix and the second reuses it while only "
            "processing the new user suffix | Learner should notice which computation is avoided]]\n"
            "\n"
            "---\n"
            "\n"

            "## 39. Replica parallelism\n"
            "\n"
            "The simplest parallelism strategy is to create several complete copies of a model.\n"
            "\n"
            "Each replica serves different requests.\n"
            "\n"
            "Benefits:\n"
            "\n"
            "- More concurrent requests.\n"
            "- Simple mental model.\n"
            "- Can reduce queueing and latency if extra hardware is available.\n"
            "\n"
            "Cost:\n"
            "\n"
            "- Every replica consumes memory and hardware.\n"
            "\n"
            "When many models and GPU sizes coexist, deciding which replicas go on which devices "
            "becomes a resource-placement / bin-packing problem.\n"
            "\n"
            "---\n"
            "\n"

            "## 40. Tensor parallelism\n"
            "\n"
            "If one model does not fit on one device—or you want lower latency—you can split "
            "individual tensor operations across several devices.\n"
            "\n"
            "For a matrix multiplication, one matrix can be divided by columns or rows so "
            "different devices compute pieces in parallel.\n"
            "\n"
            "Benefits:\n"
            "\n"
            "- Serve models larger than one device's memory.\n"
            "- Potentially reduce operation latency.\n"
            "\n"
            "Cost:\n"
            "\n"
            "- Devices must exchange intermediate data.\n"
            "- Communication can erase some speedup.\n"
            "\n"
            "---\n"
            "\n"

            "## 41. Pipeline parallelism\n"
            "\n"
            "Pipeline parallelism divides the model into sequential stages placed on different devices.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "microbatch -> layers 1..N/4 -> device 1\n"
            "           -> layers ...   -> device 2\n"
            "           -> layers ...   -> device 3\n"
            "           -> final layers -> device 4\n"
            "```\n"
            "\n"
            "Different microbatches can occupy different stages simultaneously.\n"
            "\n"
            "Pipeline parallelism helps fit large models and can increase throughput, but extra "
            "stage-to-stage communication increases per-request latency. The chapter therefore "
            "notes that it is often less attractive for strict-latency inference than other strategies.\n"
            "\n"
            "---\n"
            "\n"

            "## 42. Context and sequence parallelism\n"
            "\n"
            "These techniques target long input sequences.\n"
            "\n"
            "### Context parallelism\n"
            "\n"
            "Split different portions of the input sequence across devices.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "first half of context  -> device 1\n"
            "second half of context -> device 2\n"
            "```\n"
            "\n"
            "### Sequence parallelism\n"
            "\n"
            "Split operations associated with sequence processing across devices. The chapter "
            "uses the intuition of assigning different whole-input operators, such as attention "
            "and feedforward work, to different machines.\n"
            "\n"
            "Both approaches illustrate that long-context inference can be parallelized not only "
            "across model weights, but also across the sequence-processing dimension.\n"
            "\n"
            "[[IMAGE_NEEDED: Parallelism families | A comparison of replica parallelism "
            "(full copies), tensor parallelism (split operator tensors), pipeline parallelism "
            "(split layers), and context parallelism (split sequence) | Learner should notice "
            "what dimension each strategy partitions]]\n"
            "\n"
            "{{exercise:M09.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> The GPU with the highest FLOP/s is always the fastest choice.\n"
            "\n"
            "**Why this is wrong:** bandwidth-bound workloads can spend most of their time "
            "moving data rather than performing arithmetic.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> GPU utilization at 100% means the GPU is being used efficiently.\n"
            "\n"
            "**Why this is wrong:** activity percentage does not show how close the workload "
            "is to peak compute or memory-bandwidth efficiency.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Maximizing throughput automatically gives the best product experience.\n"
            "\n"
            "**Why this is wrong:** batching can increase throughput while making TTFT/TPOT worse. "
            "Goodput is often more meaningful.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> Quantization only reduces storage size.\n"
            "\n"
            "**Why this is wrong:** fewer bytes per parameter can also reduce bandwidth pressure "
            "and increase throughput.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Speculative decoding makes the target model unnecessary.\n"
            "\n"
            "**Why this is wrong:** the target model still verifies draft tokens and determines "
            "the accepted output behavior.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> KV caching solves the long-context problem completely.\n"
            "\n"
            "**Why this is wrong:** KV caching avoids recomputation but its memory grows with "
            "sequence length, batch size, layers, and hidden dimension.\n"
            "\n"
            "### Misconception 7\n"
            "\n"
            "> Model-level optimization and service-level optimization are interchangeable.\n"
            "\n"
            "**Why this is wrong:** model-level methods can change model behavior; service-level "
            "methods generally change scheduling/execution while keeping the model intact.\n"
            "\n"
            "### Misconception 8\n"
            "\n"
            "> Larger batches are always better.\n"
            "\n"
            "**Why this is wrong:** they can improve throughput but increase queueing, memory use, "
            "and latency.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Inference | Using a trained model to compute outputs from inputs. |\n"
            "| Inference server | Component that hosts models and executes inference. |\n"
            "| Inference service | Broader system for routing, scheduling, preprocessing, serving, and returning model results. |\n"
            "| Compute-bound | Runtime limited mainly by arithmetic throughput. |\n"
            "| Memory-bandwidth-bound | Runtime limited mainly by data-transfer speed. |\n"
            "| Arithmetic intensity | Arithmetic operations performed per byte of memory access. |\n"
            "| Roofline model | Framework for analyzing compute versus memory-bandwidth limitations. |\n"
            "| Prefill | Input-processing phase of LLM inference. |\n"
            "| Decode | Sequential token-generation phase of LLM inference. |\n"
            "| TTFT | Time to first token. |\n"
            "| TPOT | Time per output token. |\n"
            "| TBT / ITL | Time between output tokens / inter-token latency. |\n"
            "| Throughput | Total amount of inference work completed per unit time. |\n"
            "| Goodput | Work completed per unit time while satisfying an SLO. |\n"
            "| MFU | Model FLOP/s Utilization. |\n"
            "| MBU | Model Bandwidth Utilization. |\n"
            "| Accelerator | Specialized chip optimized for a class of workloads. |\n"
            "| HBM | High-bandwidth memory located close to accelerator compute. |\n"
            "| Pruning | Removing or zeroing parameters/components to create a smaller/sparser model. |\n"
            "| Speculative decoding | Draft-model proposal plus target-model verification for faster decoding. |\n"
            "| Inference with reference | Reusing candidate output spans from the input/context. |\n"
            "| Parallel decoding | Predicting multiple future-token candidates simultaneously, followed by verification. |\n"
            "| KV cache | Stored key/value vectors reused across autoregressive decoding steps. |\n"
            "| MQA | Multi-query attention; query heads share key/value representations. |\n"
            "| GQA | Grouped-query attention; groups of query heads share key/value representations. |\n"
            "| PagedAttention | Block/page-based KV-cache management that reduces fragmentation. |\n"
            "| Kernel | Hardware-optimized implementation of a repeated low-level operation. |\n"
            "| Operator fusion | Combine multiple operations into one pass to reduce memory traffic. |\n"
            "| Lowering | Converting high-level model operations into hardware-executable operations/kernels. |\n"
            "| Static batching | Wait for a fixed-size batch before execution. |\n"
            "| Dynamic batching | Execute when the batch fills or a wait timeout expires. |\n"
            "| Continuous batching | Replace completed requests in a running batch with new requests. |\n"
            "| Prompt cache | Cached processing/state for repeated prompt prefixes. |\n"
            "| Replica parallelism | Multiple full copies of a model serve different requests. |\n"
            "| Tensor parallelism | Split tensor operations across devices. |\n"
            "| Pipeline parallelism | Split sequential model stages across devices. |\n"
            "| Context parallelism | Split portions of a long input sequence across devices. |\n"
            "| Sequence parallelism | Split sequence-processing operations across devices. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What are the three levels of inference optimization?\n"
            "2. What is the difference between an inference server and inference service?\n"
            "3. What is a compute-bound workload?\n"
            "4. What is a memory-bandwidth-bound workload?\n"
            "5. Why can moving a model between CPU and GPU become a bandwidth problem?\n"
            "6. What is arithmetic intensity?\n"
            "7. Why is prefill usually compute-bound?\n"
            "8. Why is decode often bandwidth-bound?\n"
            "9. How do online and batch APIs differ in optimization goals?\n"
            "10. What is the main user-experience benefit of streaming?\n"
            "11. What safety/evaluation complication does streaming create?\n"
            "12. Define TTFT and TPOT.\n"
            "13. How can two systems have equal total latency but different user experience?\n"
            "14. Why should p95/p99 latency be monitored?\n"
            "15. What is throughput?\n"
            "16. Why should input and output throughput often be separated?\n"
            "17. What is goodput?\n"
            "18. Why can high throughput coexist with low goodput?\n"
            "19. Why is nvidia-smi-style GPU utilization not enough?\n"
            "20. What is MFU?\n"
            "21. What is MBU?\n"
            "22. How does quantization reduce bandwidth pressure?\n"
            "23. Why are GPUs suited to neural-network workloads?\n"
            "24. What accelerator properties matter besides FLOP/s?\n"
            "25. Describe the accelerator memory hierarchy.\n"
            "26. When should you prioritize memory bandwidth over peak compute?\n"
            "27. Compare quantization, distillation, and pruning.\n"
            "28. What makes autoregressive decoding inherently sequential?\n"
            "29. How does speculative decoding work?\n"
            "30. When is inference with reference useful?\n"
            "31. Why do parallel-decoding methods still require verification?\n"
            "32. What problem does the KV cache solve?\n"
            "33. Which variables increase KV-cache size?\n"
            "34. How do MQA and GQA reduce KV state?\n"
            "35. What does PagedAttention improve?\n"
            "36. Why can hardware-aware attention kernels be much faster with identical high-level math?\n"
            "37. What is operator fusion?\n"
            "38. What is lowering in a compiler?\n"
            "39. Compare static and dynamic batching.\n"
            "40. Why is continuous batching particularly valuable for LLMs?\n"
            "41. Why can separating prefill and decode improve service efficiency?\n"
            "42. When is prompt caching most useful?\n"
            "43. What is the difference between replica and tensor parallelism?\n"
            "44. Why can tensor parallelism reduce latency but introduce communication overhead?\n"
            "45. Why is pipeline parallelism often less attractive for strict-latency inference?\n"
            "46. What does context parallelism partition?\n"
            "47. Why should the workload determine the optimization technique?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Inference optimization is bottleneck engineering. Measure the workload first, "
            "then apply the technique that attacks the limiting resource. Faster and cheaper "
            "serving comes from coordinating model representation, memory movement, hardware, "
            "decoding algorithms, caches, batching, and parallelism—not from one universal trick.**\n"
        ),
        "estimated_minutes": 360,
        "has_code_examples": False,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "why-optimize", "title": "Why inference optimization matters", "order": 1},
            {"id": "inference-overview", "title": "Inference service overview", "order": 2},
            {"id": "bottlenecks", "title": "Computational bottlenecks", "order": 3},
            {"id": "roofline", "title": "Arithmetic intensity and roofline", "order": 4},
            {"id": "prefill-decode", "title": "Prefill and decode", "order": 5},
            {"id": "online-batch", "title": "Online and batch APIs", "order": 6},
            {"id": "streaming", "title": "Streaming", "order": 7},
            {"id": "latency-metrics", "title": "Latency metrics", "order": 8},
            {"id": "user-visible-latency", "title": "User-visible latency", "order": 9},
            {"id": "latency-percentiles", "title": "Latency percentiles", "order": 10},
            {"id": "throughput", "title": "Throughput", "order": 11},
            {"id": "goodput", "title": "Goodput", "order": 12},
            {"id": "utilization", "title": "Utilization", "order": 13},
            {"id": "mfu", "title": "MFU", "order": 14},
            {"id": "mbu", "title": "MBU", "order": 15},
            {"id": "accelerators", "title": "AI accelerators", "order": 16},
            {"id": "accelerator-metrics", "title": "Accelerator metrics", "order": 17},
            {"id": "memory-hierarchy", "title": "Accelerator memory hierarchy", "order": 18},
            {"id": "select-hardware", "title": "Selecting accelerators", "order": 19},
            {"id": "model-compression", "title": "Model compression", "order": 20},
            {"id": "autoregressive-bottleneck", "title": "Autoregressive bottleneck", "order": 21},
            {"id": "speculative-decoding", "title": "Speculative decoding", "order": 22},
            {"id": "reference-decoding", "title": "Inference with reference", "order": 23},
            {"id": "parallel-decoding", "title": "Parallel decoding", "order": 24},
            {"id": "kv-cache", "title": "KV cache", "order": 25},
            {"id": "kv-cache-math", "title": "KV cache calculation", "order": 26},
            {"id": "attention-redesign", "title": "Attention redesign", "order": 27},
            {"id": "kv-cache-optimization", "title": "KV-cache optimization", "order": 28},
            {"id": "flash-attention", "title": "FlashAttention", "order": 29},
            {"id": "kernels", "title": "Kernels", "order": 30},
            {"id": "kernel-techniques", "title": "Kernel optimization techniques", "order": 31},
            {"id": "compilers", "title": "Compilers and lowering", "order": 32},
            {"id": "service-optimization", "title": "Service-level optimization", "order": 33},
            {"id": "batching", "title": "Batching", "order": 34},
            {"id": "static-dynamic", "title": "Static and dynamic batching", "order": 35},
            {"id": "continuous-batching", "title": "Continuous batching", "order": 36},
            {"id": "disaggregation", "title": "Prefill/decode disaggregation", "order": 37},
            {"id": "prompt-caching", "title": "Prompt caching", "order": 38},
            {"id": "replica-parallelism", "title": "Replica parallelism", "order": 39},
            {"id": "tensor-parallelism", "title": "Tensor parallelism", "order": 40},
            {"id": "pipeline-parallelism", "title": "Pipeline parallelism", "order": 41},
            {"id": "context-sequence-parallelism", "title": "Context and sequence parallelism", "order": 42},
        ],
    },

    "exercises": [
        {
            "id": "M09.L01.EX01",
            "title": "Diagnose an Inference Bottleneck",
            "lesson_code": "M09.L01",
            "section_id": "mbu",
            "placement": "after_section",
            "description": (
                "Use latency, throughput, MFU, and MBU signals to identify likely "
                "serving bottlenecks instead of applying optimization blindly."
            ),
            "instructions": (
                "You operate a chat model with the following observations:\n\n"
                "- TTFT rises sharply as input length grows.\n"
                "- TPOT stays almost constant.\n"
                "- Prefill MFU is high.\n"
                "- Decode MFU is low but MBU is high.\n"
                "- GPU activity is near 100%.\n"
                "- Increasing batch size improves tokens/s but worsens TTFT.\n\n"
                "1. Identify the likely bottleneck during prefill.\n"
                "2. Identify the likely bottleneck during decode.\n"
                "3. Explain why GPU activity alone is insufficient.\n"
                "4. Propose two prefill optimizations.\n"
                "5. Propose two decode optimizations.\n"
                "6. Explain how quantization may help decode.\n"
                "7. Define an SLO using TTFT and TPOT.\n"
                "8. Explain why goodput is a better target than raw throughput.\n"
                "9. Define which p50/p95/p99 metrics you would monitor.\n"
                "10. Explain what experiment would show whether more batching is worth the latency cost."
            ),
            "expected_output": (
                "A bottleneck diagnosis linking observed metrics to concrete optimization "
                "choices and an SLO-aware measurement plan."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "bottleneck-analysis",
                "latency",
                "throughput",
                "mfu",
                "mbu",
                "goodput",
            ],
        },

        {
            "id": "M09.L01.EX02",
            "title": "Calculate and Reduce KV-Cache Memory",
            "lesson_code": "M09.L01",
            "section_id": "kv-cache-math",
            "placement": "after_section",
            "description": (
                "Practice the KV-cache formula and reason about long-context serving tradeoffs."
            ),
            "instructions": (
                "Use the formula `2 × B × S × L × H × M`.\n\n"
                "Assume:\n"
                "- batch size B = 8\n"
                "- sequence length S = 4096\n"
                "- layers L = 32\n"
                "- hidden dimension H = 4096\n"
                "- bytes/value M = 2\n\n"
                "1. Calculate the approximate KV-cache bytes.\n"
                "2. Convert the result to GB approximately.\n"
                "3. Recalculate if sequence length doubles.\n"
                "4. Recalculate if cache precision drops from 2 bytes to 1 byte.\n"
                "5. Explain what happens if batch size doubles.\n"
                "6. Explain how MQA/GQA could reduce cache memory conceptually.\n"
                "7. Explain how PagedAttention helps even if it does not change the "
                "raw theoretical number of K/V values.\n"
                "8. Define a serving experiment comparing maximum concurrent users "
                "before and after KV-cache optimization."
            ),
            "expected_output": (
                "A calculation sheet plus an engineering explanation of which techniques "
                "change cache size and which mainly improve memory management."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "kv-cache",
                "memory-estimation",
                "attention-optimization",
                "paged-attention",
            ],
        },

        {
            "id": "M09.L01.EX03",
            "title": "Design an Optimized LLM Inference Service",
            "lesson_code": "M09.L01",
            "section_id": "context-sequence-parallelism",
            "placement": "after_section",
            "description": (
                "Combine service-level techniques according to workload rather than "
                "treating optimization techniques as independent tricks."
            ),
            "instructions": (
                "Design serving for an enterprise assistant with these properties:\n\n"
                "- Long system prompt reused across requests.\n"
                "- Some queries contain very long documents.\n"
                "- Output lengths vary from 20 to 2,000 tokens.\n"
                "- Interactive users care about low TTFT.\n"
                "- Nightly jobs can wait hours.\n"
                "- The model is too large for one GPU.\n\n"
                "1. Separate workloads into online and batch paths.\n"
                "2. Choose static, dynamic, or continuous batching for the online path.\n"
                "3. Explain whether prompt caching should be used.\n"
                "4. Explain whether prefill/decode should be disaggregated.\n"
                "5. Choose replica, tensor, pipeline, context, or a combination of parallelism strategies.\n"
                "6. Explain why variable output lengths affect batching choice.\n"
                "7. Define TTFT, TPOT, p99 latency, throughput, and goodput targets.\n"
                "8. Explain where quantization could help.\n"
                "9. Explain one situation where speculative decoding is attractive.\n"
                "10. Define how you will verify that optimization did not degrade model quality."
            ),
            "expected_output": (
                "A production inference architecture with workload routing, caching, batching, "
                "parallelism, metrics, and model-quality validation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "inference-service-design",
                "batching",
                "prompt-caching",
                "prefill-decode",
                "parallelism",
                "slo-design",
            ],
        },
    ],

    "quiz": {
        "id": "M09.L01.QZ01",
        "title": "Inference Optimization — Knowledge Check",
        "lesson_code": "M09.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M09.L01.Q01",
                "section_id": "bottlenecks",
                "question": "What characterizes a memory-bandwidth-bound workload?",
                "options": [
                    "Runtime is limited mainly by how quickly data can move through memory",
                    "Runtime is limited only by the number of parameters",
                    "The model has no cache",
                    "The workload cannot use a GPU",
                ],
                "correct": 0,
                "explanation": (
                    "Bandwidth-bound workloads spend substantial time waiting for data movement "
                    "rather than arithmetic execution."
                ),
            },
            {
                "id": "M09.L01.Q02",
                "section_id": "prefill-decode",
                "question": "Which phase of LLM inference is typically compute-bound?",
                "options": [
                    "Prefill",
                    "Decode",
                    "Prompt caching",
                    "Streaming only",
                ],
                "correct": 0,
                "explanation": (
                    "Input tokens can be processed in parallel during prefill, making arithmetic "
                    "capacity a primary constraint."
                ),
            },
            {
                "id": "M09.L01.Q03",
                "section_id": "latency-metrics",
                "question": "What does TTFT measure?",
                "options": [
                    "Time from request arrival to the first generated token",
                    "Average time for all output tokens after completion",
                    "Number of output tokens per second across all users",
                    "GPU memory capacity",
                ],
                "correct": 0,
                "explanation": (
                    "TTFT captures how quickly generation begins from the request's perspective."
                ),
            },
            {
                "id": "M09.L01.Q04",
                "section_id": "goodput",
                "question": "What is goodput?",
                "options": [
                    "Throughput counting only requests that satisfy the defined SLO",
                    "Maximum theoretical GPU FLOP/s",
                    "The number of cached prompts",
                    "Model accuracy after quantization",
                ],
                "correct": 0,
                "explanation": (
                    "Goodput combines capacity with latency/service-quality requirements."
                ),
            },
            {
                "id": "M09.L01.Q05",
                "section_id": "utilization",
                "question": (
                    "Why can 100% GPU activity still represent poor efficiency?"
                ),
                "options": [
                    "The GPU may be active while using only a small fraction of its potential compute",
                    "GPUs cannot measure activity",
                    "100% activity means the model is too small",
                    "Activity directly equals MFU",
                ],
                "correct": 0,
                "explanation": (
                    "Activity time says little about how much useful arithmetic or bandwidth "
                    "capacity is actually being exploited."
                ),
            },
            {
                "id": "M09.L01.Q06",
                "section_id": "mbu",
                "question": (
                    "How can lower-precision weights help a bandwidth-bound decoder?"
                ),
                "options": [
                    "Fewer bytes must be transferred per parameter",
                    "They always increase model parameter count",
                    "They eliminate KV cache",
                    "They make decoding parallel automatically",
                ],
                "correct": 0,
                "explanation": (
                    "Quantization reduces memory traffic per weight, which can improve throughput "
                    "when memory bandwidth is the bottleneck."
                ),
            },
            {
                "id": "M09.L01.Q07",
                "section_id": "accelerator-metrics",
                "question": "Which set contains the main accelerator characteristics emphasized in the chapter?",
                "options": [
                    "Compute capability, memory size, memory bandwidth, and power",
                    "Tokenizer size, prompt length, and top-p",
                    "BLEU, ROUGE, and MRR",
                    "Only core count",
                ],
                "correct": 0,
                "explanation": (
                    "These hardware characteristics determine whether a workload fits, how fast it "
                    "runs, and part of its operating cost."
                ),
            },
            {
                "id": "M09.L01.Q08",
                "section_id": "model-compression",
                "question": "What does pruning attempt to do?",
                "options": [
                    "Remove or zero less-useful model components/parameters",
                    "Cache prompt prefixes",
                    "Split requests into batches",
                    "Separate prefill and decode servers",
                ],
                "correct": 0,
                "explanation": (
                    "Pruning reduces model complexity or sparsifies the model by eliminating "
                    "less-useful computation."
                ),
            },
            {
                "id": "M09.L01.Q09",
                "section_id": "speculative-decoding",
                "question": "What is the draft model's role in speculative decoding?",
                "options": [
                    "Propose tokens quickly for the target model to verify",
                    "Replace the target model permanently",
                    "Compute only embeddings",
                    "Manage prompt caching",
                ],
                "correct": 0,
                "explanation": (
                    "The draft model cheaply proposes candidate tokens while the target model "
                    "retains control through verification."
                ),
            },
            {
                "id": "M09.L01.Q10",
                "section_id": "reference-decoding",
                "question": "When is inference with reference most useful?",
                "options": [
                    "When outputs significantly reuse text from the input/context",
                    "When input and output are completely unrelated",
                    "When no context is provided",
                    "Only during training",
                ],
                "correct": 0,
                "explanation": (
                    "Reference-based acceleration reuses candidate spans already present in the input."
                ),
            },
            {
                "id": "M09.L01.Q11",
                "section_id": "kv-cache",
                "question": "What problem does the KV cache solve?",
                "options": [
                    "It avoids recomputing previous key/value vectors during decoding",
                    "It stores training gradients",
                    "It converts FP16 to INT4",
                    "It schedules batch requests",
                ],
                "correct": 0,
                "explanation": (
                    "Previously computed K/V states are reused for later decoding steps."
                ),
            },
            {
                "id": "M09.L01.Q12",
                "section_id": "kv-cache-math",
                "question": "What happens to KV-cache memory if sequence length doubles?",
                "options": [
                    "It approximately doubles, all else equal",
                    "It halves",
                    "It stays constant",
                    "It grows only with parameter count",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter's KV-cache formula is linear in sequence length."
                ),
            },
            {
                "id": "M09.L01.Q13",
                "section_id": "attention-redesign",
                "question": "What is the key idea behind grouped-query attention?",
                "options": [
                    "Groups of query heads share key/value representations",
                    "Every token gets a separate model replica",
                    "Queries are processed only on CPUs",
                    "All attention is removed",
                ],
                "correct": 0,
                "explanation": (
                    "GQA reduces KV state by sharing it within groups of query heads."
                ),
            },
            {
                "id": "M09.L01.Q14",
                "section_id": "kv-cache-optimization",
                "question": "What is a core benefit of PagedAttention?",
                "options": [
                    "More flexible KV-cache allocation with less fragmentation",
                    "It eliminates all attention computation",
                    "It trains a smaller student model",
                    "It makes every request the same length",
                ],
                "correct": 0,
                "explanation": (
                    "Paged memory management lets variable-length KV state use GPU memory more efficiently."
                ),
            },
            {
                "id": "M09.L01.Q15",
                "section_id": "kernel-techniques",
                "question": "Why does operator fusion improve performance?",
                "options": [
                    "It reduces repeated reads/writes of intermediate data",
                    "It increases the number of model parameters",
                    "It always improves model quality",
                    "It removes the need for a compiler",
                ],
                "correct": 0,
                "explanation": (
                    "Fusing operations can keep intermediate data closer to compute and avoid memory traffic."
                ),
            },
            {
                "id": "M09.L01.Q16",
                "section_id": "continuous-batching",
                "question": "Why is continuous batching well suited to LLM serving?",
                "options": [
                    "Requests with different output lengths can leave and enter batch slots independently",
                    "Every LLM response has identical length",
                    "It disables streaming",
                    "It requires no scheduler",
                ],
                "correct": 0,
                "explanation": (
                    "Continuous batching avoids forcing short generations to wait for much longer ones."
                ),
            },
            {
                "id": "M09.L01.Q17",
                "section_id": "disaggregation",
                "question": "Why separate prefill and decode onto different resources?",
                "options": [
                    "They have different compute/memory-bandwidth profiles and can interfere",
                    "They use different tokenizers",
                    "Decode cannot run on GPUs",
                    "Prefill changes model weights",
                ],
                "correct": 0,
                "explanation": (
                    "Disaggregation lets each phase use resources optimized for its distinct bottleneck."
                ),
            },
            {
                "id": "M09.L01.Q18",
                "section_id": "prompt-caching",
                "question": "Which workload benefits most directly from prompt caching?",
                "options": [
                    "Many requests sharing a long repeated prefix/system prompt",
                    "Completely unrelated one-token prompts",
                    "Training from scratch",
                    "Image-only inference with no shared context",
                ],
                "correct": 0,
                "explanation": (
                    "Caching saves repeated processing only when substantial prompt segments recur."
                ),
            },
            {
                "id": "M09.L01.Q19",
                "section_id": "tensor-parallelism",
                "question": "What does tensor parallelism split?",
                "options": [
                    "Individual tensor operations across multiple devices",
                    "Only incoming HTTP requests",
                    "The training dataset",
                    "Prompt cache entries by user",
                ],
                "correct": 0,
                "explanation": (
                    "Tensor parallelism partitions the computation of operators such as matrix multiplications."
                ),
            },
            {
                "id": "M09.L01.Q20",
                "section_id": "context-sequence-parallelism",
                "type": "open",
                "question": (
                    "You must serve a large long-context model with low interactive latency but "
                    "limited GPU memory. Design an inference-optimization plan using the chapter's "
                    "concepts. Diagnose likely bottlenecks, define TTFT/TPOT/goodput metrics, choose "
                    "model-level and service-level optimizations, explain batching/caching/KV-cache "
                    "choices, choose a parallelism strategy, and state how you would verify that "
                    "optimization did not meaningfully degrade model quality."
                ),
            },
        ],
        "passing_score": 70,
    },
}
