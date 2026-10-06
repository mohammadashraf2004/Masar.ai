"""M01.L07 — Deploying Vision-Language Models for Inference at Scale.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 7, "Deploying Models for Inference at Scale".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L07"
MODULE_ORDER = 1
MODULE_TITLE = "Foundations of Vision and Language"
MODULE_DESCRIPTION = (
    "Move a trained VLM from notebook inference to production: profile prefill and "
    "decode, reason about KV-cache memory, optimize attention and quantization, "
    "export models across runtimes, serve concurrent traffic with vLLM, and deploy "
    "to browsers, Apple Silicon, mobile, and other edge environments."
)
SOURCE_CHAPTER = 7
SOURCE_PAGES = "Chapter 7 — page numbers not provided"


TOPIC = {
    "title": "Deploying Vision-Language Models for Inference at Scale",
    "slug": "vision-language-m01-l07",
    "description": (
        "Learn how to profile and optimize VLM inference, understand prefill/decode "
        "bottlenecks and KV-cache growth, use FlashAttention and quantization, export "
        "to ONNX and TensorRT, serve efficiently with vLLM, and choose browser, "
        "server, Apple Silicon, llama.cpp, mobile, or hybrid deployment patterns."
    ),
    "order": 7,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 5.5,
    "skill_tags": [
        "vlm-inference",
        "deployment",
        "profiling",
        "ttft",
        "throughput",
        "kv-cache",
        "gqa",
        "flashattention",
        "gpu-memory",
        "quantization",
        "awq",
        "gptq",
        "gguf",
        "torchao",
        "onnx",
        "tensorrt",
        "transformers-js",
        "vllm",
        "paged-attention",
        "continuous-batching",
        "prefix-caching",
        "edge-inference",
        "mlx",
        "llama-cpp",
        "mobile-deployment",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
    ],

    "lesson": {
        "title": "Deploying Vision-Language Models for Inference at Scale",
        "content": r"""
# Deploying Vision-Language Models for Inference at Scale

> **Lesson:** M01.L07  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 7, *Deploying Models for Inference at Scale*.  
> Page numbers were not included in the supplied source.  
> This is an instructor-authored educational adaptation.

---

## Why deployment is a different problem from training

A model can work perfectly in a notebook and still fail in production.

Notebook question:

```text
Can the model answer this image question?
```

Production questions:

```text
How fast is the first token?
How many users can one GPU serve?
How much memory does one conversation consume?
What happens when 50 requests arrive together?
Can the model fit on a browser or phone?
How do we prevent one request from OOMing the server?
How do we package the model for another runtime?
```

The source frames deployment as two related challenges:

```text
1. OPTIMIZATION
   make inference fast and memory-efficient

2. PACKAGING + SERVING
   run the model reliably in the target environment
```

This lesson moves through both.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why VLM inference differs from text-only LLM inference.
- Distinguish the prefill phase from the decode phase.
- Explain why prefill is often compute-heavy while decode is often memory-bandwidth-heavy.
- Explain when large visual contexts can make prefill dominate.
- Measure time to first token (TTFT), throughput, peak memory, and memory-normalized throughput.
- Explain why GPU warmup and synchronization matter in benchmarking.
- Calculate KV-cache memory per token from model dimensions.
- Explain MHA, GQA, and MQA in terms of KV-head sharing.
- Explain why visual tokens increase long-conversation memory requirements.
- Describe the SRAM/HBM bandwidth hierarchy.
- Explain why modern inference can be memory-bound even when compute is powerful.
- Explain why FlashAttention reduces memory traffic.
- Explain why FlashAttention remains exact attention rather than an approximation.
- Explain how weight quantization targets memory bandwidth.
- Distinguish memory savings from actual latency speedup.
- Explain W4A16 weight-only quantization.
- Explain the outlier problem and block-wise quantization.
- Compare bitsandbytes, GPTQ, AWQ, GGUF, and torchao at a conceptual level.
- Explain why a VLM's LLM backbone and vision encoder may need different quantization strategies.
- Explain calibration data requirements for multimodal quantization.
- Describe what ONNX export does and why dynamic axes matter.
- Explain why VLM export often separates the vision encoder, projector, and LLM.
- Explain TensorRT's benefits and its dynamic-shape challenges for autoregressive generation.
- Describe browser deployment through ONNX Runtime Web / transformers.js.
- Explain why preprocessing parity matters after model export.
- Explain why a simple FastAPI + `model.generate()` server fails under concurrent traffic.
- Explain chunked prefill, PagedAttention, and continuous batching.
- Configure the conceptual safety boundaries of a public multimodal inference endpoint.
- Explain prefix caching and repeated-image embedding caching.
- Explain why disaggregating the vision encoder can help large deployments.
- Compare vLLM with a TensorRT-LLM + Triton style deployment.
- Explain edge constraints across laptops, phones, and embedded devices.
- Describe MLX-VLM and llama.cpp deployment flows.
- Decode the meaning of a GGUF quantization name such as `Q4_K_M`.
- Explain why mobile deployment often requires model-architecture changes in addition to quantization.
- Explain how small LoRA adapters support edge customization.
- Compare local-first, split vision/cloud language, and local-cache hybrid patterns.
- Design a deployment plan from workload requirements rather than choosing a runtime by habit.

---

## 1. The VLM inference pipeline

A text-only LLM processes text tokens.

A VLM introduces an additional front end:

```text
image
  ↓
vision processor
  ↓
vision encoder
  ↓
visual tokens
  ↓

text prompt
  ↓
text embeddings
  ↓

visual + text context
  ↓
LLM
  ↓
generated tokens
```

The vision encoder may process the image only once.

But the resulting visual tokens remain part of the model context while text is
generated.

This matters because every visual token contributes to:

- context length;
- attention work;
- KV-cache memory.

A long multimodal conversation therefore often costs more memory than a
comparable text-only chat.

---

## 2. Prefill versus decode

Transformer inference has two phases.

### 2.1 Prefill

The model processes the entire input context.

That context can include:

- visual tokens;
- system prompt;
- conversation history;
- current user prompt.

During prefill, many tokens can be processed in parallel.

The model also creates the initial KV cache.

Conceptually:

```text
all input tokens
      ↓
parallel transformer processing
      ↓
KV cache + first next-token logits
```

The source characterizes prefill as **compute-bound** because large matrix
operations can heavily use the GPU.

### 2.2 Decode

After the first output token, generation becomes autoregressive:

```text
generate one token
      ↓
append it
      ↓
generate next token
      ↓
repeat
```

The previous K/V tensors are reused from cache.

Only the new token's state needs to be computed.

However, model weights and an increasingly large KV cache must be read
repeatedly.

The source therefore characterizes decode as **memory-bound**.

### 2.3 Which phase dominates?

Large input:

```text
large image
multiple images
video
very long conversation
```

can make prefill costly.

Long output:

```text
small input
+
500-token response
```

can make decode dominate.

### Source-reported heuristic

The chapter states a crossover heuristic where input length greater than roughly
10× output length tends to favor prefill dominance.

Treat this as a source heuristic, not a universal constant.

Hardware, model architecture, kernel implementation, and batching can change
the crossover.

[[IMAGE_NEEDED: Prefill and decode timeline |
Show one large prefill block processing all image/text input tokens in parallel,
then many smaller sequential decode steps, each reading the growing KV cache |
Learner should see why prefill happens once while decode repeats]]

{{exercise:M01.L07.EX01}}

---

## 3. Metrics that matter

Deployment optimization needs measurable targets.

The chapter emphasizes two.

### Time to first token — TTFT

```text
request arrives
      ↓
first output token appears
```

TTFT strongly affects perceived responsiveness.

The source suggests:

```text
< 500 ms
```

as a desirable interactive target and notes that multi-second delays feel
sluggish.

That is a source guideline, not a universal SLA.

### Tokens per second

This measures generation speed.

Example:

```text
50 tokens / second
```

### Peak GPU memory

This determines whether:

- the request fits;
- multiple requests can run concurrently;
- a larger batch is possible.

### Memory-normalized throughput

The source proposes:

```text
tokens / second / GB
```

Why?

Model A:

```text
50 tok/s
10 GB
= 5 TPS/GB
```

Model B:

```text
40 tok/s
4 GB
= 10 TPS/GB
```

Although B is slower for one request, it can be a better server configuration
because more requests may fit on the same GPU.

This highlights a key deployment lesson:

> Lowest single-request latency and highest fleet throughput are not the same
> objective.

---

## 4. Benchmark correctly before optimizing

The source provides a benchmark function for measuring:

- TTFT;
- throughput;
- memory;
- throughput per GB.

A cleaned source-aligned pattern is:

```python
import time
import torch


def benchmark_vlm(
    model,
    processor,
    prompt="Describe.",
    max_new_tokens=100,
    warmup=3,
):
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": "IMAGE_SOURCE",
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to("cuda")

    for _ in range(warmup):
        with torch.no_grad():
            model.generate(
                **inputs,
                max_new_tokens=1,
            )

    torch.cuda.reset_peak_memory_stats()

    torch.cuda.synchronize()
    t0 = time.perf_counter()

    with torch.no_grad():
        model.generate(
            **inputs,
            max_new_tokens=1,
        )

    torch.cuda.synchronize()

    ttft_ms = (
        time.perf_counter() - t0
    ) * 1000

    torch.cuda.synchronize()
    t0 = time.perf_counter()

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
        )

    torch.cuda.synchronize()

    total_time = (
        time.perf_counter() - t0
    )

    tokens_generated = (
        outputs.shape[1]
        - inputs["input_ids"].shape[1]
    )

    throughput = (
        tokens_generated / total_time
    )

    memory_gb = (
        torch.cuda.max_memory_allocated()
        / 1e9
    )

    return {
        "ttft_ms": ttft_ms,
        "throughput": throughput,
        "memory_gb": memory_gb,
        "efficiency": (
            throughput / memory_gb
        ),
    }
```

### Why warm up?

Early runs may include:

- CUDA context initialization;
- kernel loading;
- memory allocation;
- compilation/JIT behavior.

If you benchmark the first call only, you may measure startup overhead rather
than steady-state inference.

### Why `torch.cuda.synchronize()`?

GPU operations are asynchronous.

Without synchronization, the CPU timer may stop before the GPU work actually
finishes.

### Why `time.perf_counter()`?

It is intended for precise duration measurements.

### Production benchmarking

The source recommends reporting distributions such as:

```text
P50
P95
P99
```

rather than one lucky timing result.

### Source-code note

The supplied print statement mixes formatted and nonformatted string fragments
for some metrics. The lesson presents the underlying measurements rather than
preserving that formatting typo.

---

## 5. KV cache: save compute by spending memory

Without caching, every newly generated token would require recomputing keys and
values for all earlier tokens.

KV caching avoids that.

### During prefill

Compute:

```text
K and V
```

for all context tokens.

Store them.

### During decode

For each new token:

```text
compute new token K/V
append to cache
attend over stored history
```

The cache therefore grows with sequence length.

This exchanges:

```text
memory ↑
for
repeated computation ↓
```

[[IMAGE_NEEDED: KV cache during generation |
Show prefill creating cached K/V blocks for all input tokens, then each decode
step appending one new K/V block while reusing old ones |
Learner should connect cache growth to autoregressive generation]]

---

## 6. Calculate KV-cache memory

The source gives:

```text
KV cache per token
=
2
× layers
× number of KV heads
× head dimension
× bytes per element
```

The first factor `2` represents:

```text
K + V
```

If FP16 is used:

```text
bytes per element = 2
```

### Source example: SmolVLM2 2.2B

The source uses:

```text
layers      = 24
KV heads    = 32
head dim    = 64
FP16 bytes  = 2
```

Then:

```text
2 × 24 × 32 × 64 × 2
= 196,608 bytes
≈ 192 KiB per token
```

For 1,000 tokens:

```text
≈ 187.5 MiB
```

before multiplying by batch size.

### Why VLMs are sensitive

The source states that one image can contribute hundreds to thousands of visual
tokens.

Those tokens also occupy KV cache.

For multi-turn conversations, the visual context may remain present as the text
history keeps growing.

So:

```text
visual tokens
+
conversation history
+
generated output
```

all compete for memory.

{{exercise:M01.L07.EX02}}

---

## 7. MHA, GQA, and MQA

One way to reduce KV cache is to share K/V heads.

### Multi-Head Attention — MHA

Each query head has its own corresponding K/V heads.

Conceptually:

```text
Q1 → K1,V1
Q2 → K2,V2
Q3 → K3,V3
...
```

Largest KV-cache cost among these three patterns.

### Grouped-Query Attention — GQA

Several query heads share one K/V head.

Example:

```text
4 query heads
share
1 K/V head
```

This reduces KV-cache size.

### Multi-Query Attention — MQA

All query heads share a single K/V pair per layer.

This reduces KV memory even more.

The source presents GQA as a balance between:

- efficiency;
- model quality.

---

## 8. Why inference is often memory-bound

The chapter emphasizes the GPU memory hierarchy.

Conceptually:

```text
HBM
large
slower bandwidth
stores model weights + KV cache

SRAM
tiny
very fast
close to compute units
```

The source gives illustrative figures showing a large bandwidth difference
between on-chip SRAM and off-chip HBM.

### Why this matters

Suppose model weights live in HBM.

During generation, those weights must be streamed to the compute units.

Even if tensor cores can perform the matrix multiplications extremely quickly,
they may spend time waiting for data.

This creates the **memory wall**.

### Source thought experiment

The chapter considers a very large FP16 model and divides:

```text
weight size
/
HBM bandwidth
```

to estimate a lower bound on per-token weight streaming time.

The point is not the exact number.

The point is:

> Faster arithmetic does not help if memory cannot supply weights quickly
> enough.

This explains why so many inference optimizations reduce **data movement**.

---

## 9. Three major ways to attack the memory wall

The source connects three techniques to the same bottleneck.

### Quantization

```text
smaller weights
→ less HBM data to stream
```

### FlashAttention

```text
keep intermediates on chip
→ fewer HBM round trips
```

### Batching

```text
reuse one streamed model-weight pass
across multiple requests
```

These techniques optimize different parts of the same system.

---

## 10. Why standard attention moves too much data

Standard attention:

```text
softmax(QKᵀ / √d)V
```

Naively, an implementation may:

```text
1. compute QKᵀ
2. write attention scores to HBM
3. read scores
4. softmax
5. write softmax result to HBM
6. read again
7. multiply by V
```

The expensive part is not only arithmetic.

It is repeated memory traffic.

For long sequences:

```text
N × N
```

attention matrices become huge.

A 4K sequence has:

```text
4096 × 4096
≈ 16.8 million
```

score entries per head.

This can exceed available on-chip scratch memory.

---

## 11. FlashAttention: exact attention through tiling

FlashAttention avoids materializing the full attention matrix in HBM.

Instead:

```text
split Q/K/V into tiles
      ↓
move one manageable tile into SRAM
      ↓
compute attention contribution
      ↓
update running softmax/output
      ↓
move to next tile
```

The chapter emphasizes a key point:

> FlashAttention computes exact attention; it is not an approximation.

Its advantage comes from IO-aware algorithm design.

### Memory behavior

The source describes FlashAttention as reducing attention memory from an
O(N²)-style materialized matrix to O(N)-scale working memory.

### Why it can be faster

Fewer round trips between:

```text
HBM ↔ SRAM
```

mean higher effective throughput.

---

## 12. Choosing an attention implementation

The source discusses three common Hugging Face options:

```text
eager
sdpa
flash_attention_2
```

### `eager`

Standard baseline implementation.

Useful for:

- compatibility;
- debugging;
- baseline comparison.

### `sdpa`

PyTorch's scaled-dot-product attention implementation.

### `flash_attention_2`

Optimized FlashAttention implementation when hardware/software support it.

The source reports an example A100 benchmark where FlashAttention reduced TTFT
and memory compared with eager attention.

Treat those values as source-reported results for that exact setup.

### Hardware compatibility matters

The source notes that some older GPU architectures do not support the same
FlashAttention path used by newer GPUs.

Always check:

- GPU architecture;
- CUDA version;
- package support;
- model support.

### Compilation

The source also suggests:

```python
torch.compile(
    model,
    mode="reduce-overhead",
)
```

as another possible optimization.

Compilation itself can introduce startup/recompilation costs, so benchmark your
actual workload.

---

## 13. Quantization for inference

Quantization stores model values with fewer bits.

Example:

```text
FP16
→ INT8
→ INT4
```

The benefit:

```text
less memory
less data movement
```

The cost:

```text
reduced numerical precision
possible quality loss
possible conversion/dequantization overhead
```

This is crucial:

> Smaller weights do not automatically mean lower latency.

If the runtime must:

```text
load INT4
dequantize separately
then multiply in FP16
```

the extra conversion can erase speed gains.

Quantization only becomes a latency win when the runtime and kernels are
optimized for it.

---

## 14. W4A16: weight-only quantization

The source describes the common pattern:

```text
weights     → 4-bit
activations → 16-bit
```

This is often called:

```text
W4A16
```

Why keep activations higher precision?

Weights are static.

They can be quantized offline carefully.

Activations change for every input.

Quantizing them dynamically can add:

- overhead;
- extra error.

So weight-only quantization gets substantial memory savings without quantizing
every intermediate value.

---

## 15. Scale and zero-point intuition

Linear/affine quantization maps floating-point values to a smaller integer set.

Conceptually:

```text
float weight
   ↓
scale + zero point
   ↓
integer q
```

At inference:

```text
integer q
   ↓
reconstruct approximate float
```

A simplified relationship is:

```text
w_hat ≈ scale × (q - zero_point)
```

Different blocks of weights can receive different scales.

This becomes important because weight distributions are not uniform.

---

## 16. The outlier problem

Neural-network weights can contain unusually large values.

Suppose most values lie near:

```text
-2 to +2
```

but a few are near:

```text
-60 to +60
```

If one quantization scale must represent the entire range, the normal values
receive very coarse bins.

This harms precision.

### Block-wise quantization

Instead of one scale for the entire tensor:

```text
split tensor into blocks
      ↓
compute one scale per block
```

Then one outlier affects only its local block.

The source connects this principle to modern quantization approaches such as:

- GPTQ;
- AWQ;
- GGUF k-quants.

---

## 17. bitsandbytes: easy memory savings

The source uses bitsandbytes as the easiest path to 4-bit loading.

Conceptually:

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4",
)
```

The source reports an example where 4-bit loading:

- reduced memory dramatically;
- increased TTFT;
- improved throughput per GB.

That demonstrates an important deployment distinction:

```text
single-request latency
vs
memory efficiency / concurrency
```

bitsandbytes may be excellent when:

- fitting the model is the problem;
- serving more concurrent requests is valuable.

It may be less attractive when:

- minimum single-request latency is the top priority.

---

## 18. GPTQ, AWQ, and GGUF

The source contrasts production-oriented methods.

### GPTQ

Key source framing:

```text
quantization with error compensation
```

Often paired with optimized CUDA kernels.

### AWQ

Key source framing:

```text
protect high-activation / important weights
```

The source notes that AWQ often preserves instruction-following quality well.

### GGUF

Designed for broad runtime portability, especially:

- CPU;
- Apple Silicon;
- llama.cpp-compatible backends.

The important systems lesson is:

> The kernel/runtime matters as much as the quantization format.

Two 4-bit models can have very different latency if one uses fused kernels and
the other performs slow standalone dequantization.

---

## 19. Calibration: quantize using representative data

Some quantization schemes use calibration examples.

The calibration dataset lets the algorithm observe:

- activation ranges;
- important channels;
- outliers;
- representative input patterns.

For VLMs, the source recommends multimodal calibration data.

Why?

A text-only calibration set may not exercise:

- visual connector behavior;
- image-conditioned activations;
- cross-modal layers.

So:

```text
quantizing a VLM
→ calibrate with image-text examples
```

when the chosen method requires calibration.

---

## 20. Quantize VLM components differently

A VLM is not one homogeneous block.

Typical structure:

```text
vision encoder
+
connector/projector
+
LLM backbone
```

The source recommends asymmetric treatment.

### LLM backbone

Usually the largest component.

The source suggests quantizing it aggressively because this produces the largest
memory savings.

### Vision encoder

Smaller, but potentially more sensitive to quantization.

The source recommends keeping it at higher precision in many workloads.

### Connector

Tiny relative to the LLM.

Little benefit from aggressively quantizing it.

### Task sensitivity

The source states that coarse caption/VQA workloads may tolerate aggressive
quantization better than tasks such as:

- OCR;
- fine text reading;
- counting.

Treat the exact reported quality-drop percentages as source-specific examples,
not universal guarantees.

[[IMAGE_NEEDED: Component-wise VLM quantization |
Show vision encoder and projector kept high precision while large LLM backbone
is quantized to lower bit width |
Learner should understand why optimizing the largest component yields most of
the memory savings]]

{{exercise:M01.L07.EX03}}

---

## 21. torchao

The source also introduces `torchao`.

It supports several forms of quantization, including:

- weight-only;
- weight + activation;
- layer-level strategies;
- KV-cache quantization;
- custom kernels;
- `torch.compile` integration.

The chapter's larger lesson is not to memorize one API.

It is to understand that quantization choices depend on:

```text
hardware
runtime
data type
batch size
model architecture
```

The source explicitly notes that APIs may evolve.

---

## 22. Why export a model?

PyTorch executes a dynamic computational graph.

That flexibility is excellent for research.

Deployment runtimes often prefer a more explicit graph because they can:

- fuse operations;
- optimize memory;
- select specialized kernels;
- remove unsupported Python dependencies.

Export also improves portability.

Think:

```text
training framework
      ↓
portable graph
      ↓
different optimized runtimes
```

---

## 23. ONNX: portable computational graphs

ONNX is presented as an interchange format.

Conceptual flow:

```text
PyTorch model
   ↓
ONNX export
   ↓
.onnx graph + weights
   ↓
ONNX Runtime / TensorRT / browser / other backend
```

The source shows:

```python
torch.onnx.export(
    model,
    (
        dummy_image,
        dummy_input_ids,
    ),
    "model.onnx",
    input_names=[
        "pixel_values",
        "input_ids",
    ],
    output_names=[
        "logits",
    ],
    dynamic_axes={
        "pixel_values": {
            0: "batch"
        },
        "input_ids": {
            0: "batch",
            1: "sequence",
        },
        "logits": {
            0: "batch",
            1: "sequence",
        },
    },
    opset_version=17,
)
```

### Why dummy inputs?

The exporter needs example shapes to trace/model the forward graph.

### Why dynamic axes?

Without them, the exported graph may become tied to:

```text
batch = 1
sequence length = 128
```

Dynamic axes declare which dimensions can vary.

---

## 24. Why VLM export is harder than classifier export

Possible ONNX problems include:

### Unsupported operations

Custom kernels or newer framework operations may lack an ONNX equivalent.

### Dynamic control flow

Input-dependent branching can be difficult to represent through simple tracing.

### Preprocessing outside the graph

VLMs need:

- resize;
- normalization;
- patch/tile extraction;
- tokenization;
- image placeholders.

These steps often remain outside the ONNX graph.

### Multi-component architecture

The source notes that practitioners often export separately:

```text
vision encoder
projector
language model
```

and reconnect them in deployment code.

This is important:

> Exporting the neural network is not the same as exporting the entire
> application behavior.

---

## 25. TensorRT: optimize for NVIDIA hardware

The source positions TensorRT as:

```text
less portable
more hardware-specific
higher performance potential
```

TensorRT can optimize through:

- layer fusion;
- kernel auto-tuning;
- memory planning;
- precision optimization.

A typical flow:

```text
ONNX
  ↓
TensorRT builder
  ↓
GPU-specific engine
```

### GPU-specific engines

The source notes that an engine optimized for one GPU class may not run on a
different one.

This can create operational overhead:

```text
A100 engine
L4 engine
T4 engine
...
```

---

## 26. Why autoregressive generation complicates static runtimes

Image classifiers often use fixed shapes:

```text
batch × 3 × 224 × 224
```

Autoregressive generation is dynamic.

The KV cache grows:

```text
10 tokens
→ 11
→ 12
...
→ 500
```

This creates variable shapes.

A static runtime may need to:

- preallocate a large maximum cache;
- support dynamic memory;
- use a specialized LLM runtime.

The source therefore recommends using specialized systems such as:

- vLLM;
- TensorRT-LLM;

rather than implementing complex cache management from scratch.

---

## 27. Browser deployment with transformers.js

The source describes a browser path using:

```text
transformers.js
+
ONNX Runtime Web
```

Two browser compute backends are highlighted.

### WebAssembly

CPU-based.

Broad compatibility.

### WebGPU

GPU acceleration.

More suitable for practical VLM inference.

The source emphasizes browser constraints:

- limited memory;
- model download size;
- user startup latency.

This makes small and quantized models particularly important.

---

## 28. Export preprocessing with the same care as weights

The model graph is not enough.

You must reproduce training-time preprocessing exactly.

For images:

- resize;
- crop;
- normalize;
- tile;
- patch.

For text:

- tokenizer;
- image special tokens;
- chat template.

For output:

- sampling;
- stop conditions;
- decoding.

A subtle normalization mismatch can reduce quality without crashing.

This type of bug is dangerous because:

```text
system runs
but predictions quietly get worse
```

Some teams export preprocessing.

Others rewrite it in:

- JavaScript;
- C++;
- Swift;
- Kotlin.

Either way, behavior must match.

{{exercise:M01.L07.EX04}}

---

## 29. The naive web server

The chapter shows the natural first deployment:

```text
FastAPI
+
Transformers model
+
model.generate()
+
Docker
```

Conceptually:

```python
@app.post("/generate")
async def generate(req):
    image = load_image(req.image_url)

    inputs = processor(
        text=req.prompt,
        images=image,
        return_tensors="pt",
    ).to(device)

    output = model.generate(
        **inputs,
        max_new_tokens=200,
    )

    return decode(output)
```

This is enough to prove the service works.

But it is not a high-throughput inference engine.

---

## 30. Why naive serving breaks under traffic

The source identifies several problems.

### One `generate()` call per request

This creates small independent GPU jobs.

GPUs prefer larger, more regular workloads.

### KV-cache competition

Multiple long requests can consume large amounts of memory simultaneously.

Without scheduling, concurrent requests may cause OOM.

### No streaming

Users see nothing until the full response is done.

### Missing production behavior

You eventually need:

- queueing;
- cancellation;
- timeouts;
- health checks;
- graceful shutdown;
- scheduling.

### Naive batching is not enough

Request A may be decoding.

Request B may be in prefill.

Request C may finish after 20 tokens.

Request D may generate 1,000 tokens.

The batch is constantly changing.

This motivates a dedicated serving scheduler.

---

## 31. vLLM: a serving engine, not just a model loader

The source introduces vLLM as a solution for:

- batching;
- scheduling;
- KV-cache management;
- OpenAI-compatible serving;
- multimodal requests.

Three ideas are central.

```text
1. chunked prefill
2. PagedAttention
3. continuous batching
```

---

## 32. Chunked prefill

A very long prompt can monopolize the GPU if prefilled in one giant operation.

Chunked prefill splits it.

Conceptually:

```text
request B long prompt:
[prefill chunk 1]
[prefill chunk 2]
[prefill chunk 3]

interleaved with:

request A decode token
request C decode token
```

The source says the scheduler prioritizes decode responsiveness while using
remaining compute budget for prefill.

Goal:

```text
lower TTFT interference
+
better GPU utilization
```

---

## 33. PagedAttention

A naive server might reserve a maximum KV-cache block for every request.

That wastes memory.

PagedAttention treats cache storage more like virtual memory.

Instead of one large contiguous reservation:

```text
request A → cache blocks
request B → cache blocks
request C → cache blocks
```

blocks are allocated as needed.

Benefits:

- less fragmentation;
- less over-allocation;
- larger effective batch sizes.

[[IMAGE_NEEDED: PagedAttention memory layout |
Compare fixed maximum KV-cache allocations with many unused spaces against
small cache pages allocated only as each request grows |
Learner should see how paging reduces memory waste and fragmentation]]

---

## 34. Continuous batching

Traditional batch:

```text
start 8 requests together
wait for all 8 to finish
then start next batch
```

Problem:

One long sequence makes everyone wait.

Continuous batching:

```text
request finishes
      ↓
slot immediately reused
      ↓
new request joins active batch
```

The batch evolves continuously.

This matches autoregressive serving better than fixed batch boundaries.

---

## 35. Running a VLM server

The source shows a simple CLI:

```bash
vllm serve Qwen/Qwen2.5-VL-3B-Instruct
```

and a Docker deployment.

Key conceptual flags include:

### Maximum model length

Limits context capacity.

### Multimodal input limit

The source shows a limit such as:

```text
maximum two images per prompt
```

This is important for public systems.

Without a limit, a user could submit many high-resolution images and exhaust GPU
memory.

### Shared memory

Multi-GPU PyTorch workloads may need sufficient `/dev/shm`.

Container settings such as host IPC or explicit shared-memory sizing prevent
certain multiprocessing failures.

---

## 36. Multimodal endpoints introduce media-fetch security risk

If the server accepts arbitrary image URLs, it may fetch:

```text
https://user-provided-url
```

That introduces **server-side request forgery (SSRF)** risk.

A malicious request may point to:

- internal metadata endpoints;
- private network services;
- redirect chains.

The source highlights controls such as:

- allowed media domains;
- disabling unsafe redirects;
- fetch timeouts.

General lesson:

> Model security is not only prompt safety. The media-ingestion layer is part
> of your attack surface.

---

## 37. Prefix caching

Many requests share the same beginning.

Example:

```text
500-token system prompt
+
few-shot examples
+
user-specific question
```

Without caching:

```text
prefill common prefix
again
and again
and again
```

Prefix caching reuses previously computed KV states.

This can reduce TTFT for repeated prefixes.

---

## 38. Cache repeated image processing

A user may ask several questions about one image.

Without caching:

```text
question 1 → vision encoder(image)
question 2 → vision encoder(image)
question 3 → vision encoder(image)
```

The source describes assigning a stable identifier to the image so the server
can reuse its processed visual representation.

Conceptually:

```text
image UUID
      ↓
cached vision embedding
      ↓
reuse across follow-up questions
```

### Cache-miss design

A cache can be:

- evicted;
- cleared on restart.

So clients should handle a missing cached media object by resending the image.

This is a good general caching principle:

> A cache hit should improve performance, not be required for correctness.

---

## 39. Disaggregate the vision encoder at large scale

Most VLM requests perform:

```text
vision encode once
then many LLM decode steps
```

The resource profile of these stages differs.

At large scale, you may separate:

```text
vision workers
and
decoder workers
```

Benefits can include:

- independently scale image preprocessing;
- cache shared image features;
- keep expensive LLM GPUs focused on decode.

The source positions this as useful in large multi-GPU deployments rather than
small services.

---

## 40. Triton + TensorRT-LLM

The source presents a more complex high-performance option:

```text
TensorRT engines
+
Triton Inference Server
+
TensorRT-LLM
```

Potential benefit:

- highly optimized NVIDIA GPU throughput.

Cost:

- engine compilation;
- runtime-specific setup;
- version management;
- model repository configuration.

A practical progression is:

```text
simple Transformers
→ vLLM
→ TensorRT-LLM/Triton
```

only when scale justifies the extra complexity.

---

## 41. Edge deployment changes the priorities

"Edge" includes:

- laptops;
- desktops;
- phones;
- embedded devices.

At the edge, dominant constraints often become:

```text
memory
power
thermal budget
download size
hardware support
```

The source emphasizes that a real device can behave very differently from a
simulator because of:

- memory pressure;
- thermal throttling;
- shared memory;
- background OS usage.

So production testing should include real target devices.

---

## 42. MLX and MLX-VLM on Apple Silicon

MLX is presented as an array/ML framework for Apple Silicon.

A key hardware characteristic is unified memory:

```text
CPU + GPU
share one memory pool
```

MLX-VLM builds VLM support on top of MLX.

The source shows that supported architectures can be:

- converted;
- quantized;
- generated from through CLI;
- used from Python.

### Important limitation

The architecture must be supported by the runtime.

A checkpoint alone is not enough.

The runtime must know how the model's:

- vision encoder;
- projector;
- language model;
- multimodal prompt format;

fit together.

---

## 43. llama.cpp and GGUF

The source presents `llama.cpp` as a C++ inference ecosystem supporting several
backends.

Models are commonly converted to:

```text
GGUF
```

For a VLM, conversion may include separate multimodal projector handling.

The source illustrates:

```text
convert model
→ GGUF
→ quantize
→ run CLI or server
```

This route is attractive when you want portability across:

- CPU;
- Apple Silicon;
- CUDA;
- other supported accelerators.

---

## 44. Reading `Q4_K_M`

The source explains a GGUF quantization label.

```text
Q4_K_M
```

Breakdown:

### `Q`

Quantized.

### `4`

Approximately 4-bit weight quantization.

### `_K`

K-quant block/group quantization family.

### `_M`

Balanced quality preset in the source explanation.

The source gives a spectrum:

```text
S → smaller/faster, more quality loss
M → balanced
L → larger/higher quality
```

The exact storage bits per weight can exceed the headline `4` because:

- scales;
- block metadata;

also consume space.

---

## 45. Mobile deployment

On phones, reducing model size is not optional.

The source gives the intuition:

```text
500M parameters
× 4 bits
≈ 250 MB raw weight storage
```

before:

- activations;
- KV cache;
- runtime memory.

That is already substantial for a mobile application.

Mobile optimization therefore combines:

- quantization;
- smaller model architecture;
- fewer visual tokens;
- hardware-native execution.

---

## 46. Device-native runtimes

The source describes exporting models into mobile-native execution paths such
as:

```text
Core ML
NNAPI / TFLite-style paths
```

The reason is hardware access.

Native runtimes can better target:

- NPU;
- GPU;
- device-specific kernels.

Generic execution may leave performance on the table.

---

## 47. Optimize architecture, not only precision

The chapter uses FastVLM/FastViT as an example of an architecture designed to
reduce visual-token cost.

The key principle is:

```text
reduce image representation earlier
      ↓
fewer visual tokens
      ↓
smaller context
      ↓
less attention + KV-cache work
```

The source reports large token-count and speed improvements for that example.

Treat those factors as source-reported for its model/setup.

The general lesson is robust:

> On-device optimization can require redesigning the model, not merely
> quantizing the same server architecture.

---

## 48. PEFT adapters as downloadable customizations

LoRA has another deployment benefit.

Instead of shipping several full models:

```text
general model
medical model
caption model
industrial model
```

ship:

```text
one quantized base model
+
small adapter A
+
small adapter B
+
small adapter C
```

The source gives an example of:

```text
base model: hundreds of MB
adapter: single-digit MB
```

This allows:

- lower download size;
- user-selectable specialization;
- one shared base.

[[IMAGE_NEEDED: Base model plus edge adapters |
Show one quantized base VLM stored on-device with several tiny interchangeable
LoRA adapters for different tasks |
Learner should understand why PEFT helps distribution as well as training]]

---

## 49. Hybrid edge/cloud patterns

Deployment does not have to be:

```text
100% local
or
100% cloud
```

The source presents several hybrid strategies.

### Local-first with cloud fallback

```text
easy query
→ small local VLM

hard/uncertain query
→ cloud VLM
```

Benefits:

- lower average latency;
- lower cloud cost;
- offline capability for simple cases.

Challenge:

- reliable escalation logic.

### Vision on device, language in cloud

```text
raw image
→ local vision encoder
→ embedding
→ cloud language system
```

Potential benefit:

- less raw media transmitted.

The source frames this as improving privacy/bandwidth, but remember that
embeddings can still be sensitive application data.

### Local response cache

Reuse results for repeated inputs/questions.

Useful when request patterns repeat.

---

## 50. Choose deployment from workload requirements

Do not begin with:

```text
"We should use vLLM."
```

Begin with requirements.

### Workload

- one user or thousands?
- interactive chat or batch jobs?
- one image or many images?
- short answers or long generation?
- repeated images?
- repeated system prompts?

### Hardware

- NVIDIA GPU?
- Apple Silicon?
- CPU only?
- mobile NPU?
- browser WebGPU?

### Product requirements

- offline?
- privacy-sensitive?
- low TTFT?
- maximum throughput?
- lowest cost?
- portable runtime?

### Model requirements

- size?
- visual token count?
- quantization tolerance?
- supported export path?

Then choose:

```text
Transformers
vLLM
TensorRT-LLM
ONNX Runtime
transformers.js
MLX-VLM
llama.cpp
mobile-native runtime
hybrid architecture
```

---

## 51. Source-specific caveats and implementation notes

The supplied chapter contains several details that are best treated carefully.

### Source benchmarks are configuration-specific

Numbers reported for:

- A100 TTFT;
- FlashAttention speedup;
- bitsandbytes memory/latency;
- edge model speed;
- quantization quality;

belong to the source's stated setup.

Do not assume they transfer directly to another:

- GPU;
- model;
- batch size;
- sequence length;
- software version.

### Heuristics are not physical laws

The source's prefill/decode crossover rule is useful intuition but not a
guarantee.

### API/runtime support changes

Libraries such as:

- vLLM;
- torchao;
- transformers.js;
- MLX-VLM;
- llama.cpp;

change quickly.

This lesson preserves the source's conceptual workflow rather than claiming
that every command is permanently current.

### Internal chapter references are inconsistent

The source sometimes refers to earlier topics by chapter number in a way that
does not perfectly match the supplied chapter sequence.

The lesson preserves the concepts rather than depending on those cross-reference
numbers.

### Code examples are educational

Some snippets in the raw source have formatting artifacts from the pasted text,
including split imports and shell dash characters.

The lesson normalizes only mechanical presentation issues while preserving the
intended workflow.

---

## 52. The complete deployment mental model

The entire chapter can be reduced to this pipeline:

```text
TRAINED VLM
    ↓
PROFILE
TTFT / TPS / memory / P95
    ↓
IDENTIFY BOTTLENECK
prefill?
decode?
KV cache?
memory bandwidth?
    ↓
OPTIMIZE
FlashAttention
quantization
compile
token reduction
    ↓
PACKAGE
PyTorch
ONNX
TensorRT
GGUF
MLX
    ↓
SERVE
simple server
or
vLLM
or
Triton/TensorRT-LLM
    ↓
SCHEDULE
chunked prefill
PagedAttention
continuous batching
    ↓
CACHE
prefixes
images
vision embeddings
    ↓
PROTECT
input limits
media-domain restrictions
timeouts
    ↓
DEPLOY TARGET
cloud
browser
Apple Silicon
mobile
embedded
hybrid
    ↓
MEASURE AGAIN
```

The final step is always:

```text
measure again
```

Optimization without measurement is guesswork.

{{exercise:M01.L07.EX05}}

---

## Important misconceptions

### Misconception 1: "If the model is accurate, deployment is solved."

No.

Production adds latency, concurrency, memory, scheduling, security, and cost.

### Misconception 2: "Vision encoding is the only VLM overhead."

Visual tokens also stay in the LLM context and KV cache.

### Misconception 3: "Decode is parallel over output tokens."

Autoregressive output generation is sequential across generated tokens.

### Misconception 4: "A lower-bit model must be faster."

Not necessarily.

Slow dequantization kernels can make a quantized model slower despite using less
memory.

### Misconception 5: "FlashAttention approximates attention."

The source presents it as exact attention with a more IO-efficient algorithm.

### Misconception 6: "KV cache reduces memory."

It reduces repeated computation by **using more memory**.

### Misconception 7: "If a model fits once, it can serve many users."

Concurrency multiplies KV-cache and activation pressure.

### Misconception 8: "Naive fixed batching is enough."

Autoregressive requests enter, leave, prefill, and decode at different times.

### Misconception 9: "ONNX export includes every preprocessing step automatically."

Often it does not.

Image preprocessing and tokenization may remain application code.

### Misconception 10: "TensorRT is automatically portable."

TensorRT engines are often hardware-specific.

### Misconception 11: "Quantize every VLM component equally."

The source argues that the large LLM backbone and smaller vision components can
have different precision trade-offs.

### Misconception 12: "A browser deployment is just a smaller cloud deployment."

Browser memory, download size, WebGPU support, and client preprocessing matter.

### Misconception 13: "Caching can be required for correctness."

A robust cache should be optional.

If the cache misses, the system should be able to recompute.

### Misconception 14: "Public image URLs are harmless inputs."

Fetching user-controlled URLs creates SSRF and availability risks.

### Misconception 15: "Mobile deployment only requires quantization."

Architecture, visual-token count, runtime choice, thermal limits, and memory also
matter.

---

## Key terminology

| Term | Meaning |
|---|---|
| Inference | Running a trained model to produce outputs |
| Prefill | Processing all input/context tokens and building the initial KV cache |
| Decode | Sequential generation of new output tokens |
| TTFT | Time to first generated token |
| Throughput | Generated tokens per unit time |
| TPS/GB | Throughput normalized by memory usage |
| Warmup | Untimed initial runs to remove startup effects |
| KV cache | Stored attention keys/values from prior tokens |
| MHA | Multi-head attention with separate K/V heads |
| GQA | Grouped-query attention sharing K/V heads across query groups |
| MQA | Multi-query attention using one shared K/V set |
| HBM | Large off-chip GPU memory |
| SRAM | Small fast on-chip memory |
| Memory-bound | Performance limited by data movement rather than arithmetic |
| FlashAttention | IO-aware exact attention implementation using tiling |
| Weight-only quantization | Low-bit weights with higher-precision activations |
| W4A16 | 4-bit weights and 16-bit activations |
| Calibration | Using representative examples to guide quantization |
| GPTQ | Quantization family using error-aware post-training methods |
| AWQ | Activation-aware weight quantization |
| GGUF | File/quantization ecosystem commonly used by llama.cpp |
| ONNX | Portable neural-network graph interchange format |
| Dynamic axes | Export dimensions allowed to vary at runtime |
| TensorRT | NVIDIA inference optimization/runtime system |
| WebGPU | Browser GPU-compute API |
| PagedAttention | Block/page-based KV-cache memory management |
| Continuous batching | Dynamically adding/removing active requests from a batch |
| Chunked prefill | Splitting large prompt prefills so they can be scheduled with decode |
| Prefix caching | Reusing KV states for repeated prompt prefixes |
| Vision embedding cache | Reusing image-encoder outputs for repeated media |
| Disaggregated vision | Running/scaling the vision encoder separately from the decoder |
| MLX | Apple Silicon-focused ML array/runtime framework |
| MLX-VLM | VLM tooling on top of MLX |
| llama.cpp | Portable C/C++ LLM/VLM inference runtime |
| Q4_K_M | GGUF-style 4-bit K-quant balanced preset naming |
| Edge inference | Running models on user-adjacent hardware |
| Hybrid inference | Splitting workload between local and cloud systems |

---

## Self-check

Before moving on, make sure you can answer:

1. Why does a VLM conversation often use more context memory than text-only chat?
2. What happens during prefill?
3. What happens during decode?
4. Why can a high-resolution or multi-image prompt make prefill expensive?
5. What is TTFT?
6. Why can TPS/GB be more useful than raw TPS for capacity planning?
7. Why should you warm up the GPU before benchmarking?
8. Why is CUDA synchronization needed around timing?
9. What does KV cache store?
10. Why does KV cache grow with context length?
11. How do you calculate approximate KV-cache bytes per token?
12. How does GQA reduce KV-cache memory?
13. What is the difference between HBM and SRAM?
14. Why can inference be memory-bound?
15. What memory traffic does FlashAttention avoid?
16. Why is FlashAttention not simply approximate attention?
17. Why might INT4 use less memory but have worse TTFT?
18. What is W4A16?
19. Why are outliers a problem for naive quantization?
20. Why do block-wise scales help?
21. Why does kernel implementation matter for GPTQ/AWQ performance?
22. Why should VLM calibration data include images?
23. Why might you keep the vision encoder at higher precision?
24. What does ONNX export?
25. Why are dynamic axes important?
26. Why might a VLM be exported in multiple components?
27. Why is autoregressive decoding difficult for fixed-shape runtimes?
28. What are the main browser deployment constraints?
29. Why must preprocessing match training exactly?
30. Why does a simple FastAPI `generate()` endpoint scale poorly?
31. What problem does chunked prefill solve?
32. What problem does PagedAttention solve?
33. What problem does continuous batching solve?
34. Why should a public VLM endpoint limit images per request?
35. What is SSRF in the context of user-provided image URLs?
36. When does prefix caching help?
37. Why cache image embeddings across follow-up questions?
38. Why should the client be able to recover from an image-cache miss?
39. Why disaggregate the vision encoder?
40. When might TensorRT-LLM/Triton be worth the extra complexity?
41. Why is edge memory usually a primary constraint?
42. What is MLX-VLM?
43. Why does llama.cpp use GGUF?
44. What does `Q4_K_M` communicate?
45. Why is a 4-bit 500M model still nontrivial on a phone?
46. Why can fewer visual tokens improve mobile inference?
47. How can LoRA adapters help edge distribution?
48. What is local-first cloud fallback?
49. What privacy and system trade-offs exist when sending vision embeddings to the cloud?
50. Why must every optimization be benchmarked on the actual workload?

---

## Retain this idea

**VLM deployment is a systems problem. The model is only one component. Real
performance depends on context length, visual-token count, KV-cache memory,
memory bandwidth, attention kernels, quantization kernels, scheduling, caching,
runtime compatibility, security boundaries, and target hardware. Profile first,
optimize the actual bottleneck, and measure again.**
""",

        "estimated_minutes": 330,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "inference-pipeline", "title": "The VLM inference pipeline", "order": 1},
            {"id": "prefill-decode", "title": "Prefill versus decode", "order": 2},
            {"id": "metrics", "title": "Inference metrics", "order": 3},
            {"id": "benchmarking", "title": "Correct benchmarking", "order": 4},
            {"id": "kv-cache", "title": "KV cache", "order": 5},
            {"id": "kv-memory", "title": "KV-cache memory calculation", "order": 6},
            {"id": "mha-gqa-mqa", "title": "MHA, GQA, and MQA", "order": 7},
            {"id": "memory-bound", "title": "Why inference is memory-bound", "order": 8},
            {"id": "optimization-map", "title": "Optimization map", "order": 9},
            {"id": "flashattention", "title": "The attention memory bottleneck", "order": 10},
            {"id": "flashattention-tiling", "title": "FlashAttention tiling", "order": 11},
            {"id": "optimized-attention", "title": "Optimized attention implementations", "order": 12},
            {"id": "quantization-intuition", "title": "Quantization intuition", "order": 13},
            {"id": "weight-only", "title": "W4A16 weight-only quantization", "order": 14},
            {"id": "quantization-mapping", "title": "Affine quantization", "order": 15},
            {"id": "outliers", "title": "The outlier problem", "order": 16},
            {"id": "bnb", "title": "bitsandbytes", "order": 17},
            {"id": "production-quantization", "title": "GPTQ, AWQ, and GGUF", "order": 18},
            {"id": "calibration", "title": "Calibration", "order": 19},
            {"id": "vlm-quant-asymmetry", "title": "Component-wise VLM quantization", "order": 20},
            {"id": "torchao", "title": "torchao", "order": 21},
            {"id": "export", "title": "Why export models", "order": 22},
            {"id": "onnx", "title": "ONNX", "order": 23},
            {"id": "onnx-friction", "title": "VLM export friction", "order": 24},
            {"id": "tensorrt", "title": "TensorRT", "order": 25},
            {"id": "dynamic-generation", "title": "Dynamic autoregressive generation", "order": 26},
            {"id": "browser", "title": "Browser deployment", "order": 27},
            {"id": "browser-preprocessing", "title": "Preprocessing parity", "order": 28},
            {"id": "naive-server", "title": "The naive web server", "order": 29},
            {"id": "naive-failures", "title": "Why naive serving fails", "order": 30},
            {"id": "vllm", "title": "vLLM", "order": 31},
            {"id": "chunked-prefill", "title": "Chunked prefill", "order": 32},
            {"id": "pagedattention", "title": "PagedAttention", "order": 33},
            {"id": "continuous-batching", "title": "Continuous batching", "order": 34},
            {"id": "vllm-deploy", "title": "Running a VLM server", "order": 35},
            {"id": "media-security", "title": "Media security", "order": 36},
            {"id": "prefix-cache", "title": "Prefix caching", "order": 37},
            {"id": "image-cache", "title": "Image embedding caching", "order": 38},
            {"id": "disaggregated-vision", "title": "Disaggregated vision encoder", "order": 39},
            {"id": "triton", "title": "Triton and TensorRT-LLM", "order": 40},
            {"id": "edge-landscape", "title": "The edge landscape", "order": 41},
            {"id": "mlx", "title": "MLX and MLX-VLM", "order": 42},
            {"id": "llamacpp", "title": "llama.cpp and GGUF", "order": 43},
            {"id": "q4km", "title": "Reading Q4_K_M", "order": 44},
            {"id": "mobile", "title": "Mobile deployment", "order": 45},
            {"id": "device-native", "title": "Device-native runtimes", "order": 46},
            {"id": "architecture-for-edge", "title": "Architecture for edge", "order": 47},
            {"id": "edge-adapters", "title": "PEFT adapters on edge", "order": 48},
            {"id": "hybrid", "title": "Hybrid edge/cloud patterns", "order": 49},
            {"id": "deployment-decision", "title": "Deployment decision framework", "order": 50},
            {"id": "source-notes", "title": "Source-specific caveats", "order": 51},
            {"id": "complete-pipeline", "title": "Complete deployment mental model", "order": 52},
        ],
    },

    "exercises": [
        {
            "id": "M01.L07.EX01",
            "title": "Identify the inference bottleneck",
            "lesson_code": "M01.L07",
            "section_id": "prefill-decode",
            "placement": "after_section",
            "description": (
                "Decide whether prefill or decode is likely to dominate several VLM workloads."
            ),
            "instructions": (
                "For each workload, classify the likely dominant phase and explain why:\n"
                "A. 24K visual/text input tokens, 80-token answer.\n"
                "B. 700-token image+prompt context, 1,000-token answer.\n"
                "C. 8-image prompt producing a 20-token classification answer.\n"
                "D. 500-token prompt producing a 10-token response.\n"
                "Use the source's prefill/decode intuition but state that the real crossover "
                "must be benchmarked."
            ),
            "expected_output": (
                "A four-row table with input length, output length, predicted dominant phase, "
                "and explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "prefill",
                "decode",
                "performance-analysis",
            ],
        },
        {
            "id": "M01.L07.EX02",
            "title": "Calculate KV-cache pressure",
            "lesson_code": "M01.L07",
            "section_id": "kv-memory",
            "placement": "after_section",
            "description": (
                "Quantify the memory cost of autoregressive context."
            ),
            "instructions": (
                "A model has 32 layers, 8 KV heads, head_dim=128, and stores K/V in FP16.\n"
                "1. Compute KV-cache bytes per token using 2×layers×KV_heads×head_dim×2 bytes.\n"
                "2. Convert to KiB per token.\n"
                "3. Compute approximate MiB for 4,096 tokens.\n"
                "4. Compute the cache for batch size 8.\n"
                "5. Explain why adding several thousand visual tokens has a major serving impact."
            ),
            "expected_output": (
                "Step-by-step memory calculations plus one capacity-planning interpretation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "kv-cache",
                "memory-planning",
                "gqa",
            ],
        },
        {
            "id": "M01.L07.EX03",
            "title": "Choose a quantization strategy",
            "lesson_code": "M01.L07",
            "section_id": "vlm-quant-asymmetry",
            "placement": "after_section",
            "description": (
                "Apply component-wise precision reasoning to a production VLM."
            ),
            "instructions": (
                "You have a 7B VLM composed of a 0.4B vision encoder, small projector, and "
                "large LLM backbone. The target task is document OCR.\n"
                "Propose precisions for each component and choose between an easy "
                "bitsandbytes path and a production AWQ/GPTQ-style path.\n"
                "Explain your choice in terms of memory, latency, kernel support, and task sensitivity."
            ),
            "expected_output": (
                "A component/precision table and a short runtime recommendation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "quantization",
                "awq",
                "gptq",
                "vlm-components",
            ],
        },
        {
            "id": "M01.L07.EX04",
            "title": "Plan a browser export",
            "lesson_code": "M01.L07",
            "section_id": "browser-preprocessing",
            "placement": "after_section",
            "description": (
                "Design a complete ONNX/browser path including non-model preprocessing."
            ),
            "instructions": (
                "You want to deploy a 300M VLM in a WebGPU-capable browser.\n"
                "List the artifacts/code you must ship for:\n"
                "1. vision encoder,\n"
                "2. projector/decoder,\n"
                "3. tokenizer,\n"
                "4. image preprocessing,\n"
                "5. image placeholder handling,\n"
                "6. generation/stop logic.\n"
                "Then identify two ways a preprocessing mismatch could silently hurt quality."
            ),
            "expected_output": (
                "A deployment manifest and two failure examples."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "onnx",
                "browser-deployment",
                "preprocessing",
            ],
        },
        {
            "id": "M01.L07.EX05",
            "title": "Design a production VLM service",
            "lesson_code": "M01.L07",
            "section_id": "complete-pipeline",
            "placement": "after_section",
            "description": (
                "Synthesize profiling, serving, caching, and security into one production design."
            ),
            "instructions": (
                "Design a service for 1,000 active users who repeatedly ask questions about "
                "the same uploaded images. Requirements: low TTFT, two images max per request, "
                "streaming output, and protection against unsafe arbitrary URL fetching.\n"
                "Choose a serving engine and specify:\n"
                "- scheduler strategy,\n"
                "- KV-cache management,\n"
                "- prefix caching,\n"
                "- image embedding caching,\n"
                "- multimodal input limits,\n"
                "- URL-fetch security,\n"
                "- metrics to monitor."
            ),
            "expected_output": (
                "An architecture diagram or structured production plan covering all seven areas."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "vllm",
                "paged-attention",
                "continuous-batching",
                "security",
                "caching",
            ],
        },
        {
            "id": "M01.L07.EX06",
            "title": "Choose cloud, edge, or hybrid",
            "lesson_code": "M01.L07",
            "section_id": "hybrid",
            "placement": "after_section",
            "description": (
                "Compare deployment architectures for a privacy-sensitive mobile VLM product."
            ),
            "instructions": (
                "A mobile assistant must work offline for simple camera questions but can use "
                "the cloud for difficult requests. Device memory is limited and images are sensitive.\n"
                "Design a hybrid strategy including:\n"
                "- local model size/quantization,\n"
                "- local versus cloud responsibilities,\n"
                "- when escalation occurs,\n"
                "- whether raw images or embeddings leave the phone,\n"
                "- adapter customization,\n"
                "- cache behavior.\n"
                "Explain the privacy, latency, and quality trade-offs."
            ),
            "expected_output": (
                "A local/cloud decision flow plus trade-off table."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "edge-inference",
                "hybrid-deployment",
                "quantization",
                "peft",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L07.QZ01",
        "title": "Deploying VLMs for Inference at Scale — Knowledge Check",
        "lesson_code": "M01.L07",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L07.Q01",
                "section_id": "prefill-decode",
                "question": "What happens during prefill?",
                "options": [
                    "The model processes the input context and builds initial KV-cache states.",
                    "The model generates every future token in parallel.",
                    "The model quantizes itself.",
                    "The vision encoder is permanently removed.",
                ],
                "correct": 0,
                "explanation": (
                    "Prefill processes existing context tokens and creates cached attention states."
                ),
            },
            {
                "id": "M01.L07.Q02",
                "section_id": "prefill-decode",
                "question": "Why is decode often memory-bound?",
                "options": [
                    "Each token requires repeated movement of model weights and a growing KV cache.",
                    "No memory is used during decode.",
                    "Every output token is generated in parallel.",
                    "The GPU never performs matrix multiplication.",
                ],
                "correct": 0,
                "explanation": (
                    "Per-token arithmetic can be small relative to the data that must be read from memory."
                ),
            },
            {
                "id": "M01.L07.Q03",
                "section_id": "metrics",
                "question": "What does TTFT measure?",
                "options": [
                    "Delay from request arrival until the first generated token",
                    "Total training time",
                    "Number of images in a batch",
                    "Weight quantization error",
                ],
                "correct": 0,
                "explanation": (
                    "TTFT is an interactive-latency metric for how quickly output begins."
                ),
            },
            {
                "id": "M01.L07.Q04",
                "section_id": "benchmarking",
                "question": "Why call torch.cuda.synchronize() around GPU timings?",
                "options": [
                    "GPU work is asynchronous, so the CPU timer could otherwise finish before the GPU.",
                    "It increases model accuracy.",
                    "It reduces sequence length.",
                    "It converts FP16 to INT4.",
                ],
                "correct": 0,
                "explanation": (
                    "Synchronization makes the timing interval include the actual GPU execution."
                ),
            },
            {
                "id": "M01.L07.Q05",
                "section_id": "kv-cache",
                "question": "What trade-off does KV caching make?",
                "options": [
                    "More memory in exchange for less repeated computation",
                    "More computation in exchange for no memory",
                    "Lower accuracy for more training data",
                    "More visual tokens for fewer parameters",
                ],
                "correct": 0,
                "explanation": (
                    "Cached K/V projections avoid recomputation but consume memory proportional to context."
                ),
            },
            {
                "id": "M01.L07.Q06",
                "section_id": "mha-gqa-mqa",
                "question": "How does GQA reduce KV-cache usage?",
                "options": [
                    "Several query heads share fewer K/V heads.",
                    "It removes all query heads.",
                    "It disables attention.",
                    "It stores each K/V head twice.",
                ],
                "correct": 0,
                "explanation": (
                    "Sharing K/V heads reduces the amount of cached key/value state."
                ),
            },
            {
                "id": "M01.L07.Q07",
                "section_id": "memory-bound",
                "question": "What does memory-bound inference mean?",
                "options": [
                    "Performance is limited primarily by moving data rather than arithmetic throughput.",
                    "The model cannot perform multiplication.",
                    "The GPU has no HBM.",
                    "Only CPU memory matters.",
                ],
                "correct": 0,
                "explanation": (
                    "Compute units may wait for weights/cache to arrive from memory."
                ),
            },
            {
                "id": "M01.L07.Q08",
                "section_id": "flashattention-tiling",
                "question": "What is FlashAttention's key optimization idea in the source?",
                "options": [
                    "Process attention in SRAM-sized tiles and avoid materializing the full NxN matrix in HBM.",
                    "Delete the softmax.",
                    "Approximate attention using random scores.",
                    "Use only one attention head.",
                ],
                "correct": 0,
                "explanation": (
                    "Tiling reduces slow memory traffic while preserving exact attention."
                ),
            },
            {
                "id": "M01.L07.Q09",
                "section_id": "quantization-intuition",
                "question": "Why can a quantized model still be slower than BF16?",
                "options": [
                    "Dequantization overhead and poorly optimized kernels can outweigh bandwidth savings.",
                    "Lower-bit weights always require more HBM.",
                    "Quantization increases parameter count.",
                    "BF16 cannot use GPU kernels.",
                ],
                "correct": 0,
                "explanation": (
                    "Memory savings do not automatically translate into latency without efficient kernels."
                ),
            },
            {
                "id": "M01.L07.Q10",
                "section_id": "weight-only",
                "question": "What does W4A16 mean?",
                "options": [
                    "4-bit weights and 16-bit activations",
                    "4-bit activations and 16-bit weights",
                    "4 layers and 16 attention heads",
                    "4 images and 16 text tokens",
                ],
                "correct": 0,
                "explanation": (
                    "Weight-only quantization stores weights in low precision while activations remain higher precision."
                ),
            },
            {
                "id": "M01.L07.Q11",
                "section_id": "outliers",
                "question": "Why does block-wise quantization help with outliers?",
                "options": [
                    "A large outlier only affects the scale of its local block rather than the entire tensor.",
                    "It removes every outlier from the model.",
                    "It increases all weights to FP32.",
                    "It eliminates calibration.",
                ],
                "correct": 0,
                "explanation": (
                    "Local scales preserve resolution for normal-valued blocks."
                ),
            },
            {
                "id": "M01.L07.Q12",
                "section_id": "vlm-quant-asymmetry",
                "question": "Which VLM component usually offers the largest memory-saving opportunity?",
                "options": [
                    "The LLM backbone",
                    "The tiny connector only",
                    "The tokenizer file",
                    "The image URL",
                ],
                "correct": 0,
                "explanation": (
                    "The LLM typically contains the overwhelming majority of VLM parameters."
                ),
            },
            {
                "id": "M01.L07.Q13",
                "section_id": "onnx",
                "question": "Why are dynamic axes important in ONNX export?",
                "options": [
                    "They allow dimensions such as batch size or sequence length to vary at runtime.",
                    "They increase LoRA rank.",
                    "They disable tokenization.",
                    "They force every image to 224x224.",
                ],
                "correct": 0,
                "explanation": (
                    "Without dynamic dimensions, the graph may be tied to export-time shapes."
                ),
            },
            {
                "id": "M01.L07.Q14",
                "section_id": "browser-preprocessing",
                "question": "Why must deployment preprocessing match training preprocessing?",
                "options": [
                    "Small normalization/tokenization differences can silently degrade model behavior.",
                    "Preprocessing affects only file names.",
                    "ONNX automatically fixes every mismatch.",
                    "The model ignores image pixels.",
                ],
                "correct": 0,
                "explanation": (
                    "The model learned under a specific input representation and expects the same one at inference."
                ),
            },
            {
                "id": "M01.L07.Q15",
                "section_id": "pagedattention",
                "question": "What problem does PagedAttention address?",
                "options": [
                    "KV-cache allocation waste and fragmentation",
                    "Image caption quality",
                    "Tokenizer vocabulary size",
                    "Model training loss",
                ],
                "correct": 0,
                "explanation": (
                    "Paged cache blocks allow memory to be allocated more flexibly as requests grow."
                ),
            },
            {
                "id": "M01.L07.Q16",
                "section_id": "continuous-batching",
                "question": "What is continuous batching?",
                "options": [
                    "Requests can join and leave the active batch dynamically as sequences finish.",
                    "All requests must start and end together.",
                    "Only one request is allowed.",
                    "Batches are used only during training.",
                ],
                "correct": 0,
                "explanation": (
                    "Dynamic admission keeps GPU capacity occupied despite different sequence lengths."
                ),
            },
            {
                "id": "M01.L07.Q17",
                "section_id": "media-security",
                "question": "Why are arbitrary user-provided image URLs a security concern?",
                "options": [
                    "They can enable SSRF against internal or restricted network resources.",
                    "They always lower model accuracy.",
                    "They prevent tokenization.",
                    "They disable GPU memory.",
                ],
                "correct": 0,
                "explanation": (
                    "A server fetching attacker-controlled URLs can be abused to access unintended resources."
                ),
            },
            {
                "id": "M01.L07.Q18",
                "section_id": "image-cache",
                "question": "What is the benefit of caching vision embeddings for the same image?",
                "options": [
                    "Follow-up questions can reuse vision-encoder work.",
                    "The model no longer needs text prompts.",
                    "KV cache becomes zero size.",
                    "The image can never be evicted.",
                ],
                "correct": 0,
                "explanation": (
                    "Repeated image encoding is unnecessary when the same visual representation can be reused."
                ),
            },
            {
                "id": "M01.L07.Q19",
                "section_id": "edge-adapters",
                "question": "Why are LoRA adapters useful for edge distribution?",
                "options": [
                    "One shared base model can support multiple small downloadable task-specific adapters.",
                    "They make the base model larger than full fine-tuning.",
                    "They eliminate all device memory limits.",
                    "They replace quantization.",
                ],
                "correct": 0,
                "explanation": (
                    "Adapters let applications distribute small specializations instead of multiple full model copies."
                ),
            },
            {
                "id": "M01.L07.Q20",
                "section_id": "complete-pipeline",
                "type": "open",
                "question": (
                    "You must deploy a VLM that receives one image and a short prompt, streams "
                    "200-token answers to thousands of users, and runs on NVIDIA GPUs. Design "
                    "a production path covering profiling metrics, attention implementation, "
                    "quantization choice, KV-cache strategy, serving/scheduling engine, caching, "
                    "media-security limits, and the measurements you would use to validate the result."
                ),
            },
        ],
        "passing_score": 70,
    },
}
