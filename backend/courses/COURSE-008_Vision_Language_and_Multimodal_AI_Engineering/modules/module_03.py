"""M01.L03 — Vision Language Model Training.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 3, "Vision Language Model Training".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L03"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Vision and Language"

MODULE_DESCRIPTION = (
    "Learn how a simple autoregressive VLM is trained from image-text data, how "
    "loss masking and batching work, how packed multimodal sequences are built, "
    "how generation and KV caching work, and how high-resolution images are "
    "handled without overwhelming the language model with visual tokens."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Chapter 3 — page numbers not provided"


TOPIC = {
    "title": "Vision Language Model Training",

    "slug": "vision-language-m01-l03",

    "description": (
        "Build a practical mental model of VLM training: training paradigms and "
        "stages, streaming multimodal data, vision encoder + projector + LLM "
        "architecture, next-token loss, single-sample training, padding and packing, "
        "image placeholder tokens, batched multimodal training, decoding, KV cache, "
        "and high-resolution image handling."
    ),

    "order": 3,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 4.5,

    "skill_tags": [
        "vlm-training",
        "multimodal-training",
        "autoregressive-vlm",
        "cross-entropy",
        "loss-masking",
        "batching",
        "padding",
        "sequence-packing",
        "knapsack-packing",
        "image-tokens",
        "greedy-decoding",
        "kv-cache",
        "tiling",
        "pixel-shuffle",
        "hugging-face-datasets",
        "pytorch",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
    ],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Vision Language Model Training",

        "content": r"""
# Vision Language Model Training

> **Lesson:** M01.L03  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 3, *Vision Language Model Training*.  
> Page numbers were not included in the supplied source.  
> This is an instructor-authored curriculum adaptation rather than a reproduction
> of the chapter text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Separate **training paradigms** such as supervised, self-supervised, and contrastive learning from **training stages** such as pretraining and post-training.
- Explain what pretraining, midtraining, post-training, and alignment are trying to accomplish.
- Describe the structure of a simple autoregressive VLM built from a vision encoder, projector, tokenizer, and causal language model.
- Explain how image embeddings and text embeddings are combined in a simple VLM.
- Explain why next-token cross-entropy can train a multimodal autoregressive model.
- Explain why visual-token positions should usually be ignored by a text-generation loss.
- Write the logic of a single-sample training loop using forward pass, loss, backpropagation, and optimizer step.
- Explain why batch size 1 produces noisier training dynamics.
- Compare naive padding, constrained padding, naive packing, greedy knapsack packing, and balanced packing.
- Explain why packed multimodal training requires image placeholders inside the text-token sequence.
- Explain how real image embeddings replace placeholder token embeddings during the forward pass.
- Explain why image tokens and real padding must be excluded from the language-model loss.
- Distinguish a model's forward pass from autoregressive generation.
- Explain greedy decoding and the purpose of an EOS token.
- Diagnose the padding-token/EOS-token bug described in the chapter.
- Explain KV caching using prefill and decode phases.
- Explain the compute-memory trade-off introduced by KV caching.
- Explain why high-resolution images create a visual-token explosion.
- Describe tiling and pixel-shuffle-style spatial compression as two tools for high-resolution VLMs.
- Read a VLM training recipe and identify its data, architecture, loss, batching, inference, and image-resolution decisions.

---

## 1. First separate "how" from "when"

VLM training terminology becomes confusing because two different questions are
often mixed together:

### Question A — How is the model learning?

This refers to the **training paradigm**.

Examples:

- supervised learning;
- unsupervised learning;
- self-supervised learning;
- semi-supervised learning;
- contrastive learning.

### Question B — When in the model lifecycle is this happening?

This refers to the **training stage**.

Examples:

- pretraining;
- midtraining;
- post-training;
- alignment.

These are different dimensions.

For example:

```text
stage:     pretraining
paradigm:  self-supervised learning
```

or:

```text
stage:     post-training
paradigm:  supervised instruction tuning
```

or:

```text
stage:     alignment
paradigm:  preference optimization
```

That distinction is one of the most important conceptual foundations in the
chapter.

[[IMAGE_NEEDED: Training paradigms versus training stages |
Create a two-axis diagram. One axis lists HOW: supervised, unsupervised,
self-supervised, semi-supervised, contrastive. The other lists WHEN:
pretraining, midtraining, post-training, alignment. Show that a stage can use
multiple paradigms rather than implying a one-to-one mapping |
Learner should notice that "contrastive learning" and "pretraining" are not
competing terms because they answer different questions]]

---

## 2. The "how": major training paradigms

### 2.1 Supervised learning

Supervised learning uses an explicit target.

For a VLM:

```text
input:
image + instruction

target:
human-written or synthetic answer
```

Example:

```text
Image: cat sitting on a chair
Prompt: "Describe the image."
Target: "A cat is sitting on a chair."
```

The model learns to make its generated output more like the provided target.

The supplied chapter connects supervised learning to tasks such as:

- OCR;
- captioning;
- classification;
- instruction tuning.

The main trade-off is data quality versus cost.

High-quality supervised examples can be very useful, but producing them may
require:

- human annotation;
- careful synthetic generation;
- filtering;
- quality control.

### 2.2 Unsupervised learning

Unsupervised learning uses data without explicit target labels.

The chapter gives the intuition of grouping similar photos without requiring
names for those groups.

For example:

```text
mountain images → cluster A
latte-art images → cluster B
```

The system discovers structure without being told:

```text
cluster A = mountains
cluster B = latte art
```

### 2.3 Self-supervised learning

Self-supervision creates a learning target from the data itself.

Examples include:

- hide an image patch and predict it;
- hide a text token and predict it;
- predict the next token;
- use naturally paired image-caption data.

The power of self-supervision is scale.

If the labels are derived automatically from the data, enormous datasets become
usable without requiring human annotation for every example.

### 2.4 Semi-supervised learning

Semi-supervised learning combines:

```text
small amount of expensive labeled data
+
large amount of unlabeled data
```

The labeled examples help organize or improve learning from the much larger
unlabeled pool.

### 2.5 Contrastive learning

Contrastive learning teaches the model using relationships.

For multimodal learning:

```text
matching image + text
        ↓
make embeddings more similar

nonmatching image + text
        ↓
make embeddings less similar
```

This is the core idea you already saw in CLIP.

Contrastive learning is often considered a form of self-supervised learning, but
it deserves separate attention because it was so important for connecting image
and text representation spaces at scale.

### A useful comparison

| Paradigm | Where does supervision come from? | Example |
|---|---|---|
| Supervised | Explicit target labels/answers | Image + instruction → target answer |
| Unsupervised | No target labels | Group similar images |
| Self-supervised | Data generates its own target | Mask patch, predict patch |
| Semi-supervised | Small labeled + large unlabeled set | Label-guided learning over much more raw data |
| Contrastive | Pair/mismatch relationships | Pull matching image-text pairs together |

{{exercise:M01.L03.EX01}}

---

## 3. The "when": stages in a VLM lifecycle

### 3.1 Pretraining

Pretraining creates broad foundational capability.

The chapter describes this as where the model learns a rough understanding of
the world from very large datasets.

For a VLM assembled from pretrained components, pretraining may begin with:

```text
pretrained vision encoder
+
new multimodal connector
+
pretrained LLM
```

A practical strategy is:

1. freeze the large pretrained components;
2. train the connector;
3. later allow more of the vision/language backbones to update.

This protects useful pretrained knowledge while the new cross-modal connection
is initially unstable.

### 3.2 Midtraining

The chapter uses **midtraining** for a newer stage between large-scale rough
pretraining and carefully curated post-training.

The intuition is:

```text
web-scale noisy data
        ↓
    pretraining
        ↓
large synthetic / higher-quality intermediate data
        ↓
    midtraining
        ↓
smaller, higher-quality instruction/preference data
        ↓
    post-training
```

The boundaries are not universal. The terminology is evolving.

That is an important point:

> Training-stage names are useful organizational concepts, not immutable laws.

### 3.3 Post-training

Post-training aims to turn a broadly capable model into one that follows useful
tasks and instructions.

Typical goals include:

- answer questions;
- follow instructions;
- behave consistently in chat;
- solve target downstream tasks.

Supervised fine-tuning often appears here.

### 3.4 Alignment

The supplied chapter discusses alignment after instruction tuning, using
preference-optimization methods such as DPO or PPO as examples.

The goal is to steer behavior toward desirable preferences.

At a high level:

```text
capable model
     ↓
instruction tuning
     ↓
preference/alignment optimization
     ↓
more useful target behavior
```

Do not confuse **alignment** with the visual-language projection layer.

Here:

- **multimodal alignment** can mean making vision and language representations compatible;
- **behavioral alignment** refers to steering model behavior/preferences.

Context matters.

---

## 4. Training data: multimodal conversations at scale

The chapter trains its example using **FineVisionMax**, a large multimodal
dataset assembled from many sources.

The samples are structured as interleaved conversations.

A conceptual sample looks like:

```text
image
user:      "What animal is shown?"
assistant: "A giraffe."

user:      "What is it standing near?"
assistant: "A tree branch."
```

That structure is useful because modern VLMs are often trained to behave as
multimodal assistants rather than simple classifiers.

### 4.1 Streaming large datasets

The source example uses:

```python
from datasets import load_dataset

dataset = load_dataset(
    "HuggingFaceM4/FineVisionMax",
    split="train",
    streaming=True,
)
```

Streaming matters because very large datasets may be too large to download or
store locally.

Conceptually:

```text
massive remote dataset
      ↓
stream samples as needed
      ↓
preprocess
      ↓
train
```

This can reduce:

- local storage requirements;
- startup time before training begins.

The source states that FineVisionMax is extremely large, so streaming is a
practical part of the training design rather than an optional convenience.

[[IMAGE_NEEDED: Streaming multimodal data pipeline |
Show a very large remote multimodal dataset feeding a stream of image-chat
samples into preprocessing and then into the GPU training loop |
Learner should notice that the full dataset does not need to exist in local
storage before training begins]]

---

## 5. Build a minimal autoregressive VLM

The chapter chooses the simpler of two broad VLM styles:

- autoregressive integration through projected visual embeddings;
- richer cross-attention-based interaction.

For the learning example, it uses the autoregressive design.

A simplified architecture is:

```text
IMAGE PATH
raw image
   ↓
vision processor
   ↓
vision encoder
   ↓
visual embeddings
   ↓
linear projector
   ↓
LLM-compatible visual embeddings


TEXT PATH
raw text
   ↓
tokenizer
   ↓
token IDs
   ↓
LLM token embedding layer
   ↓
text embeddings


COMBINE
projected visual embeddings
+
text embeddings
   ↓
concatenate into one sequence
   ↓
causal language model
   ↓
next-token logits
```

### 5.1 Why a projector is needed

Suppose the vision encoder outputs vectors of dimension:

```text
768
```

while the language model expects embeddings of dimension:

```text
576
```

They cannot be concatenated directly.

A linear projector learns:

```text
R^768 → R^576
```

so the image features enter the LLM in the same embedding width as text tokens.

### 5.2 Source-aligned minimal class

The chapter gives a compact implementation resembling:

```python
import torch
import torch.nn as nn

from transformers import (
    AutoModel,
    AutoProcessor,
    AutoTokenizer,
    AutoModelForCausalLM,
)


class VisionLanguageModel(nn.Module):
    def __init__(
        self,
        vision_ckpt,
        language_ckpt,
        modality_input_dim=768,
        modality_output_dim=576,
    ):
        super().__init__()

        self.vision_encoder = (
            AutoModel
            .from_pretrained(vision_ckpt)
            .vision_model
        )

        self.vision_processor = (
            AutoProcessor
            .from_pretrained(vision_ckpt)
        )

        self.modality_projector = nn.Linear(
            modality_input_dim,
            modality_output_dim,
            bias=False,
        )

        self.tokenizer = (
            AutoTokenizer
            .from_pretrained(language_ckpt)
        )

        self.llm = (
            AutoModelForCausalLM
            .from_pretrained(language_ckpt)
        )

    def forward(self, text, image):
        processed_img = self.vision_processor(
            images=[image],
            return_tensors="pt",
        ).to(self.llm.device)

        image_embd = self.vision_encoder(
            **processed_img
        ).last_hidden_state

        image_embd = self.modality_projector(
            image_embd
        ).to(dtype=self.llm.dtype)

        input_ids = self.tokenizer(
            text,
            return_tensors="pt",
        ).input_ids.to(self.llm.device)

        token_embd = self.llm.model.embed_tokens(
            input_ids
        )

        combined_embd = torch.cat(
            (image_embd, token_embd),
            dim=1,
        )

        logits = self.llm(
            inputs_embeds=combined_embd
        ).logits

        return logits
```

### Source note

The supplied chapter presents this as intentionally minimal teaching code.

It is useful for understanding the data flow, but it is **not** a production
training implementation.

The educational value is the architecture:

```text
pixels
→ visual embeddings
→ projected embeddings
→ concatenate with text embeddings
→ causal language model
```

[[IMAGE_NEEDED: Minimal autoregressive VLM |
Show two parallel paths: image→processor→vision encoder→projector and
text→tokenizer→embedding layer. Merge them by concatenation before a causal LLM,
then show logits |
Learner should understand exactly where the two modalities become one sequence]]

### 5.3 What are logits?

The LLM output is a tensor of raw vocabulary scores.

At every sequence position:

```text
logits[position] = score for every possible next token
```

Softmax converts these scores into probabilities.

But during training we usually pass raw logits directly into a cross-entropy
loss, which performs the appropriate normalization internally.

---

## 6. Make the VLM learn: next-token prediction

The forward pass alone does not train anything.

Training requires:

```text
prediction
+
target
+
loss
+
gradient
+
optimizer update
```

The chapter uses standard causal language modeling:

> Given previous context, predict the next text token.

### 6.1 Why not predict image tokens?

In the simple architecture, visual embeddings are continuous vectors generated
by the vision encoder.

They are not ordinary vocabulary tokens that the language model should learn to
emit.

So the source removes the positions corresponding to image embeddings from the
language-model loss.

### 6.2 Align predictions and labels

Suppose the text tokens are:

```text
[BOS, The, animal, is, a, giraffe, EOS]
```

The model learns:

```text
given BOS            → predict The
given BOS The        → predict animal
given ... animal     → predict is
...
```

This requires a one-position shift.

Conceptually:

```text
logits: [prediction at t0, prediction at t1, ..., prediction at t(n-1)]
labels: [token at t1,      token at t2,      ..., token at tn]
```

### 6.3 Source-aligned loss logic

The chapter uses logic equivalent to:

```python
shift_logits = logits[
    :,
    image_embd.size(1):-1,
    :
].contiguous()

shift_labels = input_ids[
    :,
    1:
].contiguous()

loss = nn.functional.cross_entropy(
    shift_logits.reshape(
        -1,
        shift_logits.size(-1),
    ),
    shift_labels.reshape(-1),
)
```

The main ideas are:

1. remove prediction positions corresponding to visual embeddings;
2. drop the last logit;
3. drop the first label;
4. flatten sequence and batch dimensions for cross entropy.

### 6.4 Cross entropy as "surprise"

At each text position, the model produces a distribution over vocabulary items.

If the correct next token gets probability:

```text
p(correct) = 0.90
```

the loss is small.

If:

```text
p(correct) = 0.01
```

the loss is much larger.

For one target token:

```text
loss = -log p(correct token)
```

So minimizing cross entropy encourages the model to increase the probability of
the correct continuation.

[[IMAGE_NEEDED: Cross-entropy intuition |
Show two next-token distributions for the target token "sun": one with high
probability on "sun" and low loss, one with probability spread over incorrect
tokens and high loss |
Learner should connect loss magnitude to how surprised the model is by the true
next token]]

### Important interpretation

A decreasing loss tells us that the model is fitting the training objective
better.

It does **not** automatically prove:

- high-quality generation;
- correct grounding;
- no hallucination;
- good generalization.

We still need inference-time evaluation.

{{exercise:M01.L03.EX02}}

---

## 7. The first training loop: one sample at a time

The simplest training step is:

```text
sample
  ↓
forward pass
  ↓
loss
  ↓
backward pass
  ↓
optimizer step
```

A source-aligned loop is:

```python
import torch.optim as optim

optimizer = optim.AdamW(
    vlm.parameters(),
    lr=1e-5,
)

step = 0

for sample in dataset:
    text = apply_chat_template_to_sample(sample)

    if len(text) > 3000:
        continue

    if len(sample["images"]) != 1:
        continue

    image = sample["images"][0].convert("RGB")

    optimizer.zero_grad()

    logits, loss = vlm(
        text,
        image,
    )

    loss.backward()

    optimizer.step()

    step += 1

    print(
        f"step {step} | "
        f"loss {loss.item():.4f}"
    )
```

### 7.1 The four operations you must understand

#### `optimizer.zero_grad()`

Clears gradients from the previous step.

PyTorch accumulates gradients by default.

#### `loss.backward()`

Uses backpropagation to compute gradients.

#### `optimizer.step()`

Updates parameters based on those gradients.

#### `loss.item()`

Extracts a Python scalar for logging.

### 7.2 Why filter samples?

The chapter filters:

- overly long text;
- samples with zero or multiple images.

That is not a universal VLM limitation.

It is a limitation of this **minimal teaching implementation**.

More advanced code can support:

- multiple images;
- variable visual token counts;
- much longer sequences.

### 7.3 Reading the loss curve

With batch size 1, loss is often noisy.

That happens because every optimizer step depends on one individual example.

One example may be:

- short;
- easy;
- difficult;
- noisy;
- domain-specific.

So the gradient direction varies strongly from step to step.

[[IMAGE_NEEDED: Batch-size-1 loss curve |
Show a raw noisy loss curve over training steps plus a smoothed downward trend |
Learner should understand that noisy individual steps can coexist with overall
learning progress]]

---

## 8. Why batching multimodal samples is difficult

Larger batches usually provide:

- better GPU utilization;
- less noisy gradient estimates;
- more examples per optimizer update.

But sequences have different lengths.

Example:

```text
sample 1 → 150 tokens
sample 2 → 2800 tokens
sample 3 → 310 tokens
sample 4 → 940 tokens
```

A tensor batch must be rectangular.

We cannot directly stack:

```text
[150]
[2800]
[310]
[940]
```

into one ordinary dense tensor.

We need a batching strategy.

---

## 9. Naive padding and constrained padding

### 9.1 Naive padding

Suppose the longest sequence has 2800 tokens.

Naive padding makes every sample length 2800.

```text
sample 1: 150 real + 2650 padding
sample 2: 2800 real
sample 3: 310 real + 2490 padding
sample 4: 940 real + 1860 padding
```

This is easy to implement, but expensive.

The model still performs attention and other computation over many padded
positions even though they carry no learning signal.

The supplied chapter reports that a simple real implementation could waste a
large share of compute this way.

### 9.2 Ignore padding in the loss

Padding should not become a prediction target.

A common convention is:

```text
ignore_index = -100
```

because PyTorch cross entropy supports that value naturally.

The source also discusses another option:

```text
use an actual padding token ID
+
tell the loss to ignore that ID
```

The critical rule is:

> Padding positions must not contribute to the training objective.

### 9.3 Constrained padding

A different approach sets a maximum sample length:

```text
max_length = 512
```

Then:

- shorter samples are padded to 512;
- longer samples are discarded.

This reduces padding waste.

But it throws away long examples.

### 9.4 Why truncation can be dangerous

In chat-style training, truncating the end can remove part of the assistant
response.

That may remove the exact target content we want the model to learn.

Therefore, the supplied chapter focuses on discarding overlong samples rather
than blindly truncating them.

{{image:naive-padding}}
{{image:constrained-padding-512}}

---

## 10. Packing: think in token budgets, not individual samples

Packing changes the unit of thinking.

Instead of:

```text
one training row = one sample
```

we use:

```text
one training row = token budget containing several samples
```

For example:

```text
max_length = 2048
```

Then a packed row might contain:

```text
sample A: 300 tokens
sample B: 700 tokens
sample C: 500 tokens
sample D: 430 tokens
padding: 118 tokens
```

Total:

```text
2048 tokens
```

Much denser.

### 10.1 Naive packing

A simple algorithm:

1. read a sample;
2. tokenize it;
3. if it fits in the current row, append it;
4. otherwise start a new row.

A source-aligned version:

```python
max_length = 2048
curr_sample = []
batch = []
max_batch_size = 8

for sample in dataset:
    tokens = tokenize_sample(sample)

    if len(tokens) > max_length:
        continue

    if len(curr_sample) + len(tokens) < max_length:
        curr_sample.extend(tokens)

    else:
        if len(batch) == max_batch_size:
            break

        batch.append(curr_sample)

        curr_sample = tokens
```

This reduces padding significantly compared with naive sample-by-sample padding.

But it is not optimal because sample order affects how well the rows fill.

### 10.2 The bin-packing intuition

Packing is similar to this problem:

```text
boxes have capacity 2048
items have different sizes
place items into boxes
minimize empty space
```

That is why knapsack/bin-packing ideas appear.

---

## 11. Greedy and balanced packing

### 11.1 Greedy packing

The chapter proposes:

1. collect a pool of samples;
2. sort them longest to shortest;
3. place each sample into an existing row if it fits;
4. otherwise create a new row.

Conceptually:

```text
pool:
[900, 800, 700, 650, 500, 400, 300, 200]

capacity:
2048

possible rows:
[900 + 700 + 400]
[800 + 650 + 500]
[300 + 200 + ...]
```

This can reduce unused space dramatically.

### 11.2 Why sorting helps

Long samples are hard to place later.

By placing them first, the algorithm can use shorter samples to fill the
remaining gaps.

### 11.3 Balanced packing

Pure greedy packing can create:

- several dense rows;
- one badly padded final row;
- uneven numbers of samples/images per row.

The chapter describes a balanced strategy that tries to place the next sample
into the currently shortest row that can hold it.

This aims for more even row lengths.

### 11.4 Multimodal balance is not only about text tokens

For VLMs, images have computation cost too.

Imagine distributed training:

```text
GPU 1 row: 8 images
GPU 2 row: 2 images
GPU 3 row: 1 image
GPU 4 row: 1 image
```

Even if text lengths are similar, GPU 1 may finish vision encoding much later.

So advanced packing can track:

- token count;
- image count.

This is a distinctly multimodal systems problem.

{{image:naive-packing}}
{{image:greedy-knapsack-packing}}
{{image:balanced-knapsack-packing}}

{{exercise:M01.L03.EX03}}

---

## 12. The multimodal packing problem: where do the images go?

Single-sample training is simple:

```text
[all image embeddings][all text embeddings]
```

But after packing, one row can contain multiple conversations.

Example:

```text
sample A:
image of South America
question/answer about capitals

sample B:
image of a molecule
question/answer about chemistry
```

If we put all visual embeddings at the beginning:

```text
[image A][image B][text A][text B]
```

the association becomes ambiguous.

We want:

```text
[image A placeholders][text A]
[image B placeholders][text B]
```

inside the same packed sequence.

That motivates **placeholder image tokens**.

---

## 13. Placeholder image tokens

The chapter introduces a special token:

```text
<|image|>
```

The token acts as a reserved location.

### 13.1 Step 1 — Add the image token to the tokenizer

Conceptually:

```python
image_token = {
    "image_token": "<|image|>"
}

tokenizer = AutoTokenizer.from_pretrained(
    smollm_checkpoint,
    extra_special_tokens=image_token,
)
```

### 13.2 Step 2 — Reserve enough placeholder positions

If one image becomes 256 visual tokens, the text representation begins with
something conceptually like:

```text
<|image|><|image|><|image|> ... 256 times ...
What do you see?
```

After tokenization, the packed sequence now knows exactly where the image should
appear.

### 13.3 Step 3 — Resize the LLM embedding table

Adding a new vocabulary token changes tokenizer size.

So the LLM embedding matrix must expand:

```python
self.llm.resize_token_embeddings(
    len(self.tokenizer)
)
```

### 13.4 Step 4 — Replace fake token embeddings with real visual embeddings

First, the entire sequence goes through the normal token embedding layer.

Then locate:

```text
input_ids == image_token_id
```

and replace those positions with real projected image features.

A source-aligned helper looks like:

```python
def _replace_img_tokens_with_embd(
    self,
    input_ids,
    token_embd,
    image_embd,
):
    updated = token_embd.clone()

    mask = (
        input_ids
        == self.tokenizer.image_token_id
    )

    updated[mask] = image_embd.view(
        -1,
        image_embd.size(-1),
    ).to(updated.dtype)

    return updated
```

### Critical shape requirement

This replacement works only when:

```text
number of placeholder positions
=
number of real visual embedding vectors
```

If the tokenizer contains 256 placeholder positions but the vision pipeline
produces 196 visual vectors, direct replacement fails.

So a production implementation must know exactly how many visual tokens each
image produces after:

- resizing;
- patching;
- special tokens;
- pooling/compression.

### 13.5 Why this approach is elegant

Packing logic manipulates token IDs.

Vision encoding happens later.

The placeholders form a bridge between those two processes.

[[IMAGE_NEEDED: Image placeholder replacement |
Show a packed token sequence containing <|image|> placeholders in two different
conversation positions. Then show two encoded images producing visual vectors
that replace those placeholder embeddings before entering the LLM |
Learner should understand how multiple images remain aligned with their own
text inside one packed sequence]]

---

## 14. Loss masking in packed multimodal training

In the first simple model, visual tokens were all at the beginning.

So we could ignore:

```text
first N prediction positions
```

Packed training breaks that assumption.

Image tokens can appear anywhere.

We need a position-level loss mask.

### 14.1 Build labels from token IDs

Start with:

```python
labels = input_ids.clone()
```

Then mark visual positions as ignored.

The source illustrates this by replacing image-token labels with a token ID that
the loss ignores.

### Important source-specific caution

The chapter later reveals that the selected padding token in the example can
coincide with the EOS token for the language model.

That means using:

```text
pad_token_id
```

as the ignore index can accidentally suppress learning on valid EOS targets.

Therefore, the safer conceptual rule is:

> Use a dedicated ignore value such as `-100`, or ensure PAD and EOS are
> distinct before using PAD as the ignore index.

A robust educational version is:

```python
IGNORE_INDEX = -100

labels = input_ids.clone()

labels[
    labels == tokenizer.image_token_id
] = IGNORE_INDEX

labels[
    labels == tokenizer.pad_token_id
] = IGNORE_INDEX

shift_logits = (
    logits[..., :-1, :]
    .contiguous()
)

shift_labels = (
    labels[..., 1:]
    .contiguous()
)

loss = nn.functional.cross_entropy(
    shift_logits.reshape(
        -1,
        shift_logits.size(-1),
    ),
    shift_labels.reshape(-1),
    ignore_index=IGNORE_INDEX,
)
```

### Why the lesson uses `-100`

This is a deliberate instructional correction prompted by the exact bug the
chapter later diagnoses.

The source's conceptual goal is unchanged:

- learn text;
- ignore visual placeholders;
- ignore real padding;
- **do not accidentally ignore EOS**.

---

## 15. Training with real packed batches

Once preprocessing moves outside the model, the data pipeline becomes:

```text
raw sample
  ↓
chat formatting
  ↓
insert image placeholders
  ↓
tokenize
  ↓
pack several samples
  ↓
pad packed rows
  ↓
stack rows into a tensor batch
  ↓
collect corresponding images
  ↓
model forward
```

The chapter's example uses:

```text
max_length = 2048
batch size = 4
```

### 15.1 Why preprocessing moves outside `forward`

The model should receive a consistent tensor structure.

If tokenization, packing, and padding occur inside `forward`, the model becomes
responsible for data-pipeline logic.

Instead, advanced training usually separates:

```text
dataset / collator / batch builder
```

from:

```text
model forward
```

This improves:

- clarity;
- reusability;
- performance;
- distributed training compatibility.

### 15.2 Packed rows still need padding

Even after packing:

```text
row A = 2012 tokens
row B = 1988 tokens
row C = 2041 tokens
row D = 2004 tokens
```

we still need a rectangular tensor.

So each row may finally be padded to:

```text
2048
```

The important difference is that this final padding is small.

### 15.3 Why the loss curve becomes smoother

Batch size 1 uses one example's gradient.

Batch size 4 averages signal over more data.

Conceptually:

```text
g_batch =
(g1 + g2 + g3 + g4) / 4
```

The average tends to reduce example-specific noise.

The source observes a smoother loss curve in the packed batch experiment.

{{image:packed-training-loss}}

---

## 16. Training is not inference

During training, the model sees known target sequences.

During inference, we provide:

```text
image + prompt
```

and the model must generate unknown continuation tokens.

The forward pass gives us:

```text
logits
```

but not a complete answer.

We need a decoding loop.

### 16.1 Greedy decoding

Greedy decoding chooses:

```text
argmax probability
```

at every step.

Algorithm:

```text
prompt
  ↓
model
  ↓
choose highest-probability next token
  ↓
append token
  ↓
model again
  ↓
repeat
```

Stop when:

- the model emits EOS;
- maximum generation length is reached.

### 16.2 Source-aligned generation logic

The supplied chapter uses a minimal routine conceptually like:

```python
def generate(
    trained_vlm,
    tokenizer,
    input_text,
    image,
    max_new_tokens,
):
    messages = [
        {
            "role": "user",
            "content": (
                tokenizer.image_token * 256
                + input_text
            ),
        }
    ]

    text_str = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=False,
    )

    input_tokens = tokenizer(
        text_str,
        return_tensors="pt",
    ).input_ids.cuda()

    output = []

    while len(output) < max_new_tokens:
        prediction = trained_vlm(
            input_tokens,
            image,
        )[0]

        next_token = torch.argmax(
            prediction[:, -1, :],
            dim=-1,
        )

        if next_token.item() == tokenizer.eos_token_id:
            break

        output.append(
            next_token.item()
        )

        input_tokens = torch.cat(
            [
                input_tokens,
                next_token[:, None],
            ],
            dim=1,
        )

    return tokenizer.decode(output)
```

### Source note

The chapter's code is intentionally simple and demonstrates the algorithm.

The version above makes a few mechanical details explicit, such as extracting a
scalar token ID for comparison and decoding integer IDs at the end.

Those are implementation clarifications, not changes to the learning concept.

---

## 17. Why qualitative generation checks matter

The chapter trains a very small VLM for a limited number of steps.

When tested qualitatively, it shows two common problems:

### Hallucination

The model describes objects that are not present.

Example pattern:

```text
image: mountain landscape
model: mentions trees that are not actually there
```

### Repetition

The model may repeat:

```text
"It is a mountain.
 It is a mountain.
 It is a mountain..."
```

That repetition exposed a deeper training bug.

### 17.1 The PAD/EOS bug

The chapter explains that, for the selected language model configuration:

```text
pad token
=
end-of-sentence token
```

The training loss ignored the pad token.

Therefore, it also ignored EOS.

That means the model was never rewarded for learning:

```text
"this is where the answer should stop"
```

So it could continue indefinitely.

### The fix

Use distinct semantics:

```text
PAD → ignored by loss
EOS → valid prediction target
```

One safe implementation is:

```text
padding label = -100
EOS label = eos_token_id
```

Then cross entropy uses:

```python
ignore_index=-100
```

### Why this story matters

The main lesson is bigger than EOS.

A decreasing training loss can coexist with a serious behavioral defect.

Qualitative inspection can reveal:

- repeated text;
- grounding failures;
- hallucinations;
- malformed output;
- bad stopping behavior;
- prompt-template bugs.

So practical training should iterate:

```text
train a little
   ↓
inspect samples
   ↓
diagnose weird behavior
   ↓
fix pipeline/model
   ↓
train again
```

{{exercise:M01.L03.EX04}}

---

## 18. Why autoregressive generation is slow

Suppose the prompt contains 1000 tokens.

To generate token 1001 without caching, the transformer processes all 1000
existing tokens.

Then to generate token 1002, a naive implementation processes:

```text
1001 tokens again
```

Most of the key/value computations for previous tokens are repeated.

That is wasteful.

### 18.1 Attention recap

Transformer attention uses:

- queries;
- keys;
- values.

During autoregressive decoding:

- old tokens' keys and values do not change;
- only the new token contributes new key/value tensors.

So we can cache the old ones.

---

## 19. KV cache: prefill once, decode efficiently

The **key-value cache** stores the past keys and values for each transformer
layer.

### Phase 1 — Prefill

Run the entire prompt once:

```text
image + prompt tokens
       ↓
transformer
       ↓
logits + cached K/V tensors
```

### Phase 2 — Decode

For each new token:

1. compute its query/key/value;
2. append new K/V to the cache;
3. attend over cached history;
4. predict the next token.

Conceptual pseudocode from the chapter:

```python
hidden, kv_cache = vlm(
    input_ids=prefill_tokens,
    images=image,
    kv_cache=None,
    start_pos=0,
)

for step in range(max_new_tokens):
    logits, kv_cache = vlm(
        input_ids=next_token.unsqueeze(0),
        images=image,
        kv_cache=kv_cache,
        start_pos=(
            prefill_tokens.size(1)
            + step
        ),
    )

    next_token = greedy_sample(logits)
```

### 19.1 What is inside the cache?

For every transformer layer, cache:

```text
keys
values
```

The sequence dimension grows as generation proceeds.

### 19.2 Why it is faster

Without cache:

```text
recompute previous K/V every step
```

With cache:

```text
reuse previous K/V
compute only new step's K/V
```

The supplied chapter reports a noticeable generation speedup in its NanoVLM
experiments.

The exact speedup depends on:

- model size;
- prompt length;
- output length;
- hardware;
- implementation.

### 19.3 Trade-off: compute vs memory

KV cache saves computation but consumes memory.

Memory grows with factors such as:

- number of layers;
- sequence length;
- number of attention heads;
- head dimension;
- batch size;
- precision.

So the trade-off is:

```text
more cache memory
        ↔
less repeated attention computation
```

[[IMAGE_NEEDED: Prefill versus decode with KV cache |
Show the full prompt processed once during prefill, creating per-layer K/V
cache. Then show each generated token computing only new Q/K/V while attending
to cached K/V |
Learner should understand that history is still available even though most old
attention projections are not recomputed]]

{{exercise:M01.L03.EX05}}

---

## 20. High-resolution images create a token-budget problem

Small inputs such as:

```text
256 × 256
```

may be enough for:

- large objects;
- coarse scenes;
- simple photographs.

But they can destroy information in:

- screenshots;
- documents;
- charts;
- small text;
- dense diagrams.

Downscaling a paper screenshot to 256 × 256 may make the text unreadable.

So we need more visual resolution.

---

## 21. Tiling: more pixels without redesigning the encoder

One simple strategy is **tiling**.

Suppose a high-resolution image is split into:

```text
5 columns × 3 rows = 15 tiles
```

If every tile is:

```text
256 × 256
```

the vision encoder can still process its familiar input size.

Conceptually:

```text
high-resolution image
      ↓
split into tiles
      ↓
encode each tile
      ↓
combine visual tokens
```

This preserves local detail.

### 21.1 The cost: visual-token explosion

Suppose one 256 × 256 tile produces:

```text
256 visual tokens
```

Then 15 tiles produce:

```text
15 × 256 = 3840 visual tokens
```

That can consume a huge fraction of the language model's context window.

It also makes attention much more expensive.

### Attention cost intuition

Self-attention scales approximately with:

```text
O(n²)
```

in sequence length `n`.

If visual tokens double:

```text
n → 2n
```

attention work can grow roughly:

```text
n² → 4n²
```

So preserving resolution by blindly adding visual tokens can be extremely
expensive.

[[IMAGE_NEEDED: High-resolution tiling |
Show one dense screenshot first downscaled to 256x256 with unreadable details,
then divided into a grid of multiple 256x256 tiles with readable local details |
Learner should see why tiling improves visibility but multiplies visual-token
count]]

---

## 22. Pixel shuffle: compress spatial tokens into channels

The chapter introduces pixel shuffle as a way to reduce the number of visual
tokens passed into the LLM.

The important idea is:

```text
more spatial positions
        ↓
rearrange
        ↓
fewer spatial positions
+
more channel depth
```

No conceptual information is meant to be thrown away by the rearrangement
itself; it is reorganized.

### 22.1 Before compression

Imagine a feature grid:

```text
H × W × C
```

There are:

```text
H × W
```

spatial token positions.

### 22.2 After spatial compression

A shuffle operation can trade:

```text
spatial resolution
```

for:

```text
channel width
```

So the language model sees fewer visual sequence positions.

The projector becomes wider because each compressed token contains more channel
information.

### 22.3 Why this is useful

Attention is expensive in **sequence length**.

A wider linear projector scales more gently than exploding the number of
attention tokens.

So the system prefers:

```text
fewer, richer visual tokens
```

over:

```text
thousands of fine-grained visual tokens
```

when possible.

### 22.4 Tiling plus compression

These ideas are complementary.

A modern high-resolution pipeline may conceptually do:

```text
large image
  ↓
adaptive tiling / resizing
  ↓
vision encoder
  ↓
spatial compression
  ↓
projector
  ↓
manageable number of visual tokens
  ↓
LLM
```

[[IMAGE_NEEDED: Pixel-shuffle token compression |
Show a 2D grid of visual tokens before compression and a smaller grid after
compression where each remaining token has a deeper channel representation |
Learner should understand the spatial-token versus channel-width trade-off]]

### Important nuance

The source describes the rearrangement as preserving information.

In practice, the usefulness of aggressive compression still depends on:

- how the vision features were produced;
- compression ratio;
- downstream projector capacity;
- training.

So even if the rearrangement operation itself is information-preserving,
representational quality can degrade if the overall system compresses too
aggressively for the task.

---

## 23. Put the complete training system together

A useful mental model for the whole chapter is:

```text
1. DATA
large multimodal conversation dataset
        ↓
stream examples

2. PREPROCESSING
chat template
        ↓
insert image placeholders
        ↓
tokenize
        ↓
pack samples
        ↓
pad packed rows

3. VISION
images
        ↓
vision processor
        ↓
vision encoder
        ↓
optional spatial compression
        ↓
projector

4. FUSION
find image placeholder positions
        ↓
replace placeholder embeddings
        ↓
multimodal embedding sequence

5. LANGUAGE MODEL
causal transformer
        ↓
next-token logits

6. LOSS
shift labels
        ↓
ignore visual positions
        ↓
ignore padding
        ↓
keep EOS trainable
        ↓
cross entropy

7. OPTIMIZATION
zero gradients
        ↓
backward
        ↓
optimizer step

8. CHECK
loss curve
+
qualitative generations

9. INFERENCE
prefill
        ↓
KV cache
        ↓
autoregressive decode
```

This is the training chapter in one diagram.

---

## 24. Practical engineering lessons hidden inside the chapter

The source repeatedly emphasizes that successful VLM training is not just about
choosing a model architecture.

Many failures come from pipeline details.

### 24.1 Data quality matters

A large dataset does not guarantee a good model.

Training can only learn from the quality and diversity of the available
examples.

### 24.2 Shape assumptions must be explicit

You must know:

- visual embedding width;
- LLM embedding width;
- number of visual tokens;
- max sequence length;
- batch shape.

Silent shape mismatches quickly become runtime errors.

### 24.3 Token semantics matter

`PAD`, `EOS`, and `<|image|>` have different meanings.

Treating them as interchangeable can corrupt the objective.

### 24.4 Compute efficiency is part of model quality

Wasteful padding does not only cost money.

It can limit:

- effective batch size;
- sequence length;
- number of experiments;
- model scale.

Data packing is therefore an important training technique.

### 24.5 Loss is necessary but insufficient

A falling loss can coexist with:

- hallucinations;
- repetition;
- poor stopping behavior;
- weak grounding.

Always inspect generated samples.

### 24.6 Inference architecture matters too

Training a model is only part of the system.

Interactive deployment also needs:

- efficient decoding;
- caching;
- memory management.

### 24.7 Visual resolution is part of the token budget

More pixels often mean more visual tokens.

The LLM context window is therefore a shared budget among:

- visual content;
- prompt text;
- conversation history;
- generated response.

This trade-off is central to multimodal system design.

---

## Important misconceptions

### Misconception 1: "Pretraining is a learning paradigm."

Pretraining is a **stage**.

It can use self-supervised, contrastive, supervised, or mixed objectives.

### Misconception 2: "The projector converts the image directly into words."

The projector maps visual feature vectors into an embedding space compatible
with the LLM.

The LLM still performs language prediction.

### Misconception 3: "If visual embeddings are concatenated with text embeddings, the model automatically understands images."

Concatenation only provides the information.

Training must teach the model how visual positions relate to language targets.

### Misconception 4: "A falling training loss proves the VLM works."

No.

It proves the model is improving on the optimization objective.

Qualitative behavior and held-out evaluation are still required.

### Misconception 5: "Padding does not matter because it is ignored by the loss."

Padding can still waste substantial forward/backward compute.

Ignoring it in the loss prevents it from becoming a target, but does not make
the computation free.

### Misconception 6: "Packing is just padding with a different name."

Packing fills each fixed-length row with several real samples before adding
final padding.

Its purpose is to increase useful-token density.

### Misconception 7: "All image embeddings can stay at the beginning after packing."

No.

With multiple samples and images, visual features must remain aligned with the
text they belong to.

### Misconception 8: "It is safe to ignore `pad_token_id` without checking token configuration."

Not always.

If PAD and EOS share an ID, ignoring PAD may also prevent the model from
learning EOS.

### Misconception 9: "Greedy decoding is training."

Greedy decoding is an inference strategy.

Training uses a loss and gradients.

### Misconception 10: "KV cache changes what the model attends to."

KV cache is primarily an efficiency optimization.

The model can still attend to prior history; cached K/V tensors prevent
recomputing most of it.

### Misconception 11: "High resolution is free if the vision encoder supports it."

Higher resolution often creates many more visual tokens and therefore much more
LLM attention cost.

### Misconception 12: "Pixel shuffle simply deletes image information."

The operation described in the chapter rearranges spatial information into
channels to reduce sequence length. The larger system can still lose useful
detail if compression becomes too aggressive, but the operation is not simply
throwing away arbitrary tokens.

---

## Key terminology

| Term | Meaning |
|---|---|
| Training paradigm | The method by which supervision is constructed |
| Training stage | Where a training process occurs in the model lifecycle |
| Supervised learning | Learning from explicit input-target pairs |
| Unsupervised learning | Learning structure without explicit labels |
| Self-supervised learning | Creating supervision from the data itself |
| Semi-supervised learning | Combining a small labeled set with a large unlabeled set |
| Contrastive learning | Pull matching representations together and push mismatches apart |
| Pretraining | Large-scale foundational training stage |
| Midtraining | Intermediate stage using large higher-quality/synthetic datasets |
| Post-training | Task/instruction-focused adaptation after broad pretraining |
| Alignment | Preference/behavior steering stage |
| Streaming dataset | Dataset read incrementally instead of downloaded entirely first |
| Vision encoder | Network that converts images into visual representations |
| Projector | Layer mapping visual embedding dimensions into the LLM-compatible space |
| Causal LM | Language model trained to predict future/next tokens from prior context |
| Logits | Raw unnormalized vocabulary scores produced by the model |
| Cross entropy | Standard classification/language-modeling loss |
| Loss masking | Excluding selected token positions from the objective |
| Padding | Filler positions added to equalize sequence lengths |
| Packing | Combining multiple real samples into a fixed token-budget row |
| Greedy knapsack | Heuristic that fits variable-length samples into rows with low waste |
| Balanced packing | Packing strategy that tries to equalize row utilization |
| Image placeholder | Special token position reserved for real visual embeddings |
| Image token | A sequence position representing visual information for the LLM |
| EOS | End-of-sequence token that teaches the model when to stop |
| Greedy decoding | Choosing the highest-scoring next token at each inference step |
| KV cache | Stored transformer keys/values reused across autoregressive decoding steps |
| Prefill | First inference phase processing the full prompt and creating the cache |
| Decode | Repeated next-token generation phase using cached history |
| Tiling | Splitting a high-resolution image into smaller encoder-sized pieces |
| Pixel shuffle | Spatial/channel rearrangement used here to reduce visual token count |
| Context budget | Maximum multimodal sequence space available to the language model |

---

## Self-check

Before continuing, make sure you can answer:

1. What is the difference between a training paradigm and a training stage?
2. Why is contrastive learning important in multimodal pretraining?
3. What role does the multimodal projector play?
4. Why are visual embedding positions excluded from the simple next-token loss?
5. Why do we shift logits and labels by one position?
6. What exactly happens during `loss.backward()`?
7. Why is batch-size-1 training noisy?
8. Why is naive padding computationally wasteful?
9. What trade-off does constrained padding introduce?
10. Why does packing improve useful-token density?
11. Why do greedy/knapsack strategies sort or arrange samples by length?
12. Why can image-count imbalance matter in distributed VLM training?
13. Why are `<|image|>` placeholders necessary in packed multimodal sequences?
14. What shape equality must hold when replacing placeholder embeddings?
15. Why is using PAD as an ignore index dangerous when PAD and EOS share an ID?
16. How does greedy decoding generate an answer?
17. What bug caused the chapter's model to repeat instead of stopping?
18. What is the difference between prefill and decode?
19. What does the KV cache store?
20. Why does KV cache trade memory for speed?
21. Why does tiling increase visual-token count?
22. Why is visual-token count expensive for the LLM?
23. What is pixel shuffle trying to reduce?
24. Why should qualitative generations be inspected before a long expensive training run?

---

## Retain this idea

**Training a VLM is an end-to-end engineering problem, not just a neural-network
architecture problem. The model learns only when data formatting, visual-token
placement, loss masking, batching, padding, stopping tokens, inference caching,
and image resolution all agree with one another.**
""",

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "training-map",
                "title": 'First separate "how" from "when"',
                "order": 1,
            },
            {
                "id": "training-paradigms",
                "title": "Major training paradigms",
                "order": 2,
            },
            {
                "id": "training-stages",
                "title": "Stages in a VLM lifecycle",
                "order": 3,
            },
            {
                "id": "training-data",
                "title": "Training data and streaming",
                "order": 4,
            },
            {
                "id": "basic-vlm",
                "title": "Build a minimal autoregressive VLM",
                "order": 5,
            },
            {
                "id": "next-token-loss",
                "title": "Next-token prediction and cross-entropy loss",
                "order": 6,
            },
            {
                "id": "single-sample-training",
                "title": "Single-sample training",
                "order": 7,
            },
            {
                "id": "batching-problem",
                "title": "Why multimodal batching is difficult",
                "order": 8,
            },
            {
                "id": "padding",
                "title": "Naive and constrained padding",
                "order": 9,
            },
            {
                "id": "packing",
                "title": "Sequence packing",
                "order": 10,
            },
            {
                "id": "knapsack",
                "title": "Greedy and balanced packing",
                "order": 11,
            },
            {
                "id": "multimodal-packing",
                "title": "The multimodal packing problem",
                "order": 12,
            },
            {
                "id": "image-placeholders",
                "title": "Placeholder image tokens",
                "order": 13,
            },
            {
                "id": "loss-masking",
                "title": "Loss masking in packed multimodal training",
                "order": 14,
            },
            {
                "id": "real-batches",
                "title": "Training with real packed batches",
                "order": 15,
            },
            {
                "id": "inference",
                "title": "Training is not inference",
                "order": 16,
            },
            {
                "id": "vibe-testing-bug",
                "title": "Qualitative testing and the PAD/EOS bug",
                "order": 17,
            },
            {
                "id": "kv-cache",
                "title": "Why autoregressive generation is slow",
                "order": 18,
            },
            {
                "id": "kv-prefill-decode",
                "title": "KV cache: prefill and decode",
                "order": 19,
            },
            {
                "id": "high-resolution",
                "title": "High-resolution images and token budgets",
                "order": 20,
            },
            {
                "id": "tiling",
                "title": "Tiling",
                "order": 21,
            },
            {
                "id": "pixel-shuffle",
                "title": "Pixel shuffle",
                "order": 22,
            },
            {
                "id": "full-training-loop",
                "title": "The complete training system",
                "order": 23,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L03.EX01",

            "title": "Classify the training recipe",

            "lesson_code": "M01.L03",

            "section_id": "training-paradigms",

            "placement": "after_section",

            "description": (
                "Separate training paradigms from training stages using short VLM "
                "training scenarios."
            ),

            "instructions": (
                "For each scenario, identify the training paradigm and likely stage.\n"
                "A. Train an image-text encoder on millions of naturally paired web images "
                "and captions by increasing matching similarity.\n"
                "B. Fine-tune a VLM on curated image-question-answer examples.\n"
                "C. Mask image patches and train the visual encoder to reconstruct them.\n"
                "D. Optimize a previously instruction-tuned model using preference pairs.\n"
                "For each scenario, explain which word answers HOW and which answers WHEN."
            ),

            "expected_output": (
                "A four-row table with columns: scenario, training paradigm, training "
                "stage, and justification."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "training-paradigms",
                "training-stages",
                "contrastive-learning",
                "alignment",
            ],
        },

        {
            "id": "M01.L03.EX02",

            "title": "Align next-token logits and labels",

            "lesson_code": "M01.L03",

            "section_id": "next-token-loss",

            "placement": "after_section",

            "description": (
                "Practice causal next-token shifting and visual-position masking."
            ),

            "instructions": (
                "Assume an input contains 3 image embeddings followed by text token IDs "
                "[10, 20, 30, 40].\n"
                "1. State which model positions should be excluded because they correspond "
                "to image embeddings.\n"
                "2. Write the text input-label prediction pairs for next-token learning.\n"
                "3. Explain why the final text-position logit has no next-token label inside "
                "this example.\n"
                "4. Explain why image embeddings should influence the prediction even though "
                "their positions are not themselves prediction targets."
            ),

            "expected_output": (
                "A small position table showing context position, target token, whether "
                "the position contributes to loss, and a short explanation."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "next-token-prediction",
                "loss-shifting",
                "loss-masking",
                "multimodal-conditioning",
            ],
        },

        {
            "id": "M01.L03.EX03",

            "title": "Pack variable-length samples",

            "lesson_code": "M01.L03",

            "section_id": "knapsack",

            "placement": "after_section",

            "description": (
                "Compare padding waste with a simple packing solution."
            ),

            "instructions": (
                "You have token lengths [900, 700, 620, 400, 260, 100] and "
                "max_length=1024.\n"
                "1. Compute the padding required if every sample is padded individually "
                "to 1024.\n"
                "2. Propose a valid greedy packing into 1024-token rows.\n"
                "3. Compute the final padding for your packed rows.\n"
                "4. Calculate the percentage reduction in padding tokens.\n"
                "5. Explain why image count might still make two equally full rows have "
                "different compute costs."
            ),

            "expected_output": (
                "Individual-padding total, a valid packed-row arrangement, packed-padding "
                "total, percentage reduction, and a short multimodal compute explanation."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "padding",
                "packing",
                "token-efficiency",
                "multimodal-batching",
            ],
        },

        {
            "id": "M01.L03.EX04",

            "title": "Diagnose a model that never stops",

            "lesson_code": "M01.L03",

            "section_id": "vibe-testing-bug",

            "placement": "after_section",

            "description": (
                "Use observed generation behavior to trace a bug back to the loss mask."
            ),

            "instructions": (
                "A newly trained VLM produces sensible beginnings but repeats sentences "
                "until max_new_tokens is reached.\n"
                "You discover pad_token_id == eos_token_id and cross entropy uses "
                "ignore_index=pad_token_id.\n"
                "1. Explain why the model is not trained to produce EOS.\n"
                "2. Propose a safe label-masking strategy.\n"
                "3. State what qualitative test you would run after retraining.\n"
                "4. Explain why the training loss could still have looked healthy."
            ),

            "expected_output": (
                "A concise root-cause analysis plus corrected masking logic and a "
                "post-fix inference test."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "debugging",
                "pad-token",
                "eos-token",
                "loss-masking",
                "qualitative-evaluation",
            ],
        },

        {
            "id": "M01.L03.EX05",

            "title": "Reason about KV-cache trade-offs",

            "lesson_code": "M01.L03",

            "section_id": "kv-prefill-decode",

            "placement": "after_section",

            "description": (
                "Compare naive autoregressive recomputation with cached decoding."
            ),

            "instructions": (
                "Assume a 1000-token prompt and an output of 100 new tokens.\n"
                "1. Describe what is repeatedly recomputed without KV cache.\n"
                "2. Describe what is computed during prefill with KV cache.\n"
                "3. Describe what is computed for each later decode token.\n"
                "4. State the main memory cost introduced by caching.\n"
                "5. Explain why long output generation benefits strongly from caching."
            ),

            "expected_output": (
                "A comparison table for no-cache versus KV-cache decoding, plus a short "
                "compute-memory trade-off explanation."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "kv-cache",
                "prefill",
                "decode",
                "inference-efficiency",
            ],
        },

        {
            "id": "M01.L03.EX06",

            "title": "Budget high-resolution visual tokens",

            "lesson_code": "M01.L03",

            "section_id": "pixel-shuffle",

            "placement": "after_section",

            "description": (
                "Quantify why tiling can overwhelm a language model context and how "
                "spatial compression changes the budget."
            ),

            "instructions": (
                "A 256x256 tile produces 256 visual tokens.\n"
                "A high-resolution image is divided into 16 tiles.\n"
                "1. Compute the total visual-token count before compression.\n"
                "2. If a spatial compression method reduces the number of visual positions "
                "by a factor of 4, compute the new token count.\n"
                "3. For an 8192-token context window, compute the percentage occupied by "
                "visual tokens before and after compression.\n"
                "4. Explain why this matters for prompt text and generated output."
            ),

            "expected_output": (
                "The before/after token counts, percentages of context consumed, and a "
                "short explanation of the multimodal context-budget trade-off."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "high-resolution-vlm",
                "visual-token-budget",
                "tiling",
                "pixel-shuffle",
                "context-window",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L03.QZ01",

        "title": "Vision Language Model Training — Knowledge Check",

        "lesson_code": "M01.L03",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L03.Q01",
                "section_id": "training-map",
                "question": (
                    "Which pair correctly separates a training paradigm from a "
                    "training stage?"
                ),
                "options": [
                    "Contrastive learning = paradigm; pretraining = stage",
                    "Pretraining = paradigm; contrastive learning = stage",
                    "Padding = paradigm; batching = stage",
                    "KV cache = paradigm; generation = stage",
                ],
                "correct": 0,
                "explanation": (
                    "Contrastive learning describes how supervision works, while "
                    "pretraining describes when in the lifecycle the training occurs."
                ),
            },
            {
                "id": "M01.L03.Q02",
                "section_id": "training-paradigms",
                "question": (
                    "What best describes self-supervised learning?"
                ),
                "options": [
                    "Humans manually label every example.",
                    "The training signal is constructed from the data itself.",
                    "The model is never optimized.",
                    "Only preference data can be used.",
                ],
                "correct": 1,
                "explanation": (
                    "Self-supervision creates targets such as masked patches or next "
                    "tokens directly from raw data."
                ),
            },
            {
                "id": "M01.L03.Q03",
                "section_id": "basic-vlm",
                "question": (
                    "Why is a modality projector used in the minimal autoregressive VLM?"
                ),
                "options": [
                    "To map visual features into the embedding dimension expected by the LLM",
                    "To convert text into JPEG files",
                    "To replace the tokenizer",
                    "To compute the optimizer learning rate",
                ],
                "correct": 0,
                "explanation": (
                    "The visual encoder and LLM may use different hidden dimensions, so "
                    "the projector creates compatible visual embeddings."
                ),
            },
            {
                "id": "M01.L03.Q04",
                "section_id": "next-token-loss",
                "question": (
                    "Why are the initial visual positions removed from the simple "
                    "language-model loss?"
                ),
                "options": [
                    "The image is irrelevant to text prediction.",
                    "The model should condition on visual embeddings but not predict them as vocabulary tokens.",
                    "Cross entropy works only on images.",
                    "Visual embeddings are always padding.",
                ],
                "correct": 1,
                "explanation": (
                    "The visual embeddings provide context, while the training target in "
                    "this setup is next-text-token prediction."
                ),
            },
            {
                "id": "M01.L03.Q05",
                "section_id": "single-sample-training",
                "question": (
                    "Which operation actually updates the model parameters after gradients "
                    "have been computed?"
                ),
                "options": [
                    "optimizer.zero_grad()",
                    "loss.item()",
                    "optimizer.step()",
                    "tokenizer.decode()",
                ],
                "correct": 2,
                "explanation": (
                    "`loss.backward()` computes gradients, while `optimizer.step()` "
                    "applies an update to trainable parameters."
                ),
            },
            {
                "id": "M01.L03.Q06",
                "section_id": "padding",
                "question": (
                    "Why can naive padding waste substantial GPU compute?"
                ),
                "options": [
                    "Padding changes images into audio.",
                    "Short samples are expanded to the longest sequence and many padded "
                    "positions still pass through model computation.",
                    "Padding prevents batching entirely.",
                    "Padding always increases the amount of training data.",
                ],
                "correct": 1,
                "explanation": (
                    "Ignoring padding in the loss does not eliminate the compute spent "
                    "processing those sequence positions."
                ),
            },
            {
                "id": "M01.L03.Q07",
                "section_id": "packing",
                "question": (
                    "What is the central idea behind sequence packing?"
                ),
                "options": [
                    "Store every sample in a separate GPU.",
                    "Fill a fixed token-budget row with several real samples before adding padding.",
                    "Remove all long samples from the dataset.",
                    "Force every sample to contain one token.",
                ],
                "correct": 1,
                "explanation": (
                    "Packing increases the fraction of useful tokens by placing multiple "
                    "samples into the same fixed-length row."
                ),
            },
            {
                "id": "M01.L03.Q08",
                "section_id": "image-placeholders",
                "question": (
                    "Why are image placeholder tokens useful in packed multimodal sequences?"
                ),
                "options": [
                    "They mark the exact sequence positions where real image embeddings belong.",
                    "They permanently replace the vision encoder.",
                    "They make every image the same color.",
                    "They are used only for optimizer state.",
                ],
                "correct": 0,
                "explanation": (
                    "Placeholders preserve alignment between each image and its associated "
                    "conversation position inside a packed token sequence."
                ),
            },
            {
                "id": "M01.L03.Q09",
                "section_id": "loss-masking",
                "question": (
                    "Why is it dangerous to use `pad_token_id` as `ignore_index` when "
                    "`pad_token_id == eos_token_id`?"
                ),
                "options": [
                    "The model may never learn to predict the EOS stopping token.",
                    "The vision encoder becomes frozen automatically.",
                    "The batch size doubles.",
                    "The tokenizer loses all vocabulary.",
                ],
                "correct": 0,
                "explanation": (
                    "If PAD and EOS share an ID, ignoring PAD also masks genuine EOS "
                    "training targets."
                ),
            },
            {
                "id": "M01.L03.Q10",
                "section_id": "inference",
                "question": (
                    "What does greedy decoding do at each generation step?"
                ),
                "options": [
                    "Samples a random training image.",
                    "Chooses the token with the highest current score/probability.",
                    "Updates model weights.",
                    "Re-packs the dataset.",
                ],
                "correct": 1,
                "explanation": (
                    "Greedy decoding selects the highest-scoring next token and appends it "
                    "to the generated sequence."
                ),
            },
            {
                "id": "M01.L03.Q11",
                "section_id": "vibe-testing-bug",
                "question": (
                    "What behavior in the chapter revealed that the EOS target had been "
                    "accidentally ignored?"
                ),
                "options": [
                    "The model generated perfectly calibrated confidence scores.",
                    "The model repeated text and failed to stop naturally.",
                    "The model could not tokenize images.",
                    "The optimizer refused to initialize.",
                ],
                "correct": 1,
                "explanation": (
                    "Repeated output continuing until the maximum generation length was a "
                    "clue that the model had not learned a reliable stopping behavior."
                ),
            },
            {
                "id": "M01.L03.Q12",
                "section_id": "kv-prefill-decode",
                "question": (
                    "What is cached during KV-cache decoding?"
                ),
                "options": [
                    "Only the training loss",
                    "Past transformer keys and values for each layer",
                    "The complete dataset",
                    "Only image filenames",
                ],
                "correct": 1,
                "explanation": (
                    "Past attention keys and values are reused so they do not need to be "
                    "recomputed for every new generated token."
                ),
            },
            {
                "id": "M01.L03.Q13",
                "section_id": "kv-prefill-decode",
                "question": (
                    "What is the main cost introduced by KV caching?"
                ),
                "options": [
                    "More memory usage for cached attention states",
                    "The model loses access to prior context",
                    "Training labels become unavailable",
                    "Images must be converted to text",
                ],
                "correct": 0,
                "explanation": (
                    "KV cache exchanges additional memory consumption for reduced repeated "
                    "attention computation."
                ),
            },
            {
                "id": "M01.L03.Q14",
                "section_id": "tiling",
                "question": (
                    "Why can high-resolution tiling become expensive for an autoregressive VLM?"
                ),
                "options": [
                    "Tiling always reduces the number of image tokens.",
                    "Many tiles can produce thousands of visual tokens, increasing sequence "
                    "length and attention cost.",
                    "The tokenizer cannot contain text after an image.",
                    "Tiling disables the vision encoder.",
                ],
                "correct": 1,
                "explanation": (
                    "Each tile generates visual tokens, and long multimodal sequences make "
                    "LLM self-attention expensive."
                ),
            },
            {
                "id": "M01.L03.Q15",
                "section_id": "pixel-shuffle",
                "question": (
                    "What is the main goal of the pixel-shuffle-style compression "
                    "described in the chapter?"
                ),
                "options": [
                    "Increase the number of spatial visual tokens indefinitely",
                    "Trade spatial positions for channel depth so fewer visual tokens enter the LLM",
                    "Delete all image features",
                    "Replace cross entropy with contrastive loss",
                ],
                "correct": 1,
                "explanation": (
                    "The technique reorganizes spatial feature information into channels, "
                    "reducing the visual sequence length seen by the language model."
                ),
            },
            {
                "id": "M01.L03.Q16",
                "section_id": "full-training-loop",
                "type": "open",
                "question": (
                    "Describe the complete training path for one packed multimodal batch: "
                    "from raw image-text samples through tokenization and image placeholders, "
                    "vision encoding, embedding replacement, causal-language-model forward "
                    "pass, loss masking, backpropagation, and optimizer update. Then explain "
                    "one qualitative test you would run before committing to a long training run."
                ),
            },
        ],

        "passing_score": 70,
    },
}
