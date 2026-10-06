"""M01.L01 — Introduction to Vision and Language.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 1, "Introduction to Vision and Language".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Vision and Language"

MODULE_DESCRIPTION = (
    "Build the mental model needed to understand modern vision-language models: "
    "classical image processing, convolution and CNNs, language sequence models, "
    "transformers and ViTs, CLIP-style multimodal alignment, modern VLM "
    "architecture, the Hugging Face ecosystem, and image-text retrieval."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Chapter 1 — page numbers not provided"


TOPIC = {
    "title": "Introduction to Vision and Language",

    "slug": "vision-language-m01-l01",

    "description": (
        "Trace the ideas that led from handcrafted image filters and recurrent "
        "language models to vision transformers, CLIP, and modern vision-language "
        "models, then apply those ideas with Hugging Face and a text-to-image "
        "retrieval pipeline."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "computer-vision",
        "multimodal-ai",
        "cnn",
        "transformers",
        "vision-transformer",
        "clip",
        "vlm",
        "hugging-face",
        "faiss",
        "retrieval",
    ],

    "prerequisite_ids": [],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Introduction to Vision and Language",

        "content": r"""
# Introduction to Vision and Language

> **Lesson:** M01.L01  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 1, *Introduction to Vision and Language*.  
> Page numbers were not included in the supplied source.  
> This is an instructor-authored learning adaptation rather than a reproduction
> of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why vision and language became two central problems in artificial intelligence.
- Describe how Fourier, DCT, and wavelet transforms reveal useful structure in images.
- Explain kernels, convolution, padding, and feature maps using a simple numerical example.
- Explain how CNNs learn visual features instead of relying on handcrafted filters.
- Distinguish image classification, object detection, semantic segmentation, and instance segmentation.
- Explain transfer learning and the roles of a backbone, neck, and task-specific head.
- Describe the main ideas behind ResNet, MobileNet, and U-Net.
- Explain how tokenization, RNNs, LSTMs, GRUs, encoders, decoders, and attention led toward transformers.
- Distinguish the broad roles of BERT, GPT-style decoder models, and T5.
- Explain how a Vision Transformer converts an image into patch tokens.
- Describe MAE, BEiT, hierarchical ViTs, and DeiT at a high level.
- Explain CLIP's contrastive objective and shared image-text embedding space.
- Explain the common blueprint of a modern vision-language model.
- Navigate the core pieces of the Hugging Face ecosystem.
- Use `pipeline`, `AutoModel`, `AutoProcessor`, and `datasets` at a conceptual level.
- Explain how SigLIP-style embeddings and FAISS can power text-to-image search.

---

## 1. Why combine vision and language?

Humans understand the world through many senses, but two abilities are especially
important for intelligent interaction:

1. **Vision** lets us perceive objects, scenes, spatial relationships, gestures,
   text in the environment, and visual events.
2. **Language** lets us describe what we perceive, ask questions, explain
   relationships, reason with other people, and preserve knowledge beyond the
   immediate moment.

Early machine-learning systems usually specialized in only one modality. A
computer-vision model might classify an image, while a language model might
process a sentence. Modern **vision-language models (VLMs)** bring those
modalities together.

A VLM can receive visual information, language, or both, and use learned
relationships between them to solve tasks such as:

- describing an image;
- answering questions about an image;
- interpreting charts and documents;
- reading visible text;
- understanding visual content across long videos;
- matching images with natural-language descriptions;
- generating language grounded in visual input.

The important idea is not simply that one model accepts two file types. A useful
multimodal model must learn a **connection between visual representations and
linguistic representations**.

### A mental model

Think of the history in this lesson as a sequence of increasingly powerful
representations:

```text
raw pixels
   ↓
handcrafted visual features
   ↓
learned CNN features
   ↓
visual tokens and self-attention
   ↓
shared image-text embeddings
   ↓
vision encoder + language model + multimodal connector
```

At the same time, language followed its own path:

```text
words
   ↓
tokens
   ↓
recurrent hidden states
   ↓
attention
   ↓
transformers
   ↓
large pretrained language models
```

Modern VLMs appear where these two paths meet.

### Why learn the history?

The point is not memorizing dates. The history gives you reusable intuition.
When you encounter a new multimodal architecture, you can ask:

- How are images represented?
- How is text represented?
- Where do the two modalities interact?
- What objective teaches them to align?
- Which components are pretrained?
- Which components are frozen or fine-tuned?
- What output task is the final head or decoder solving?

If you can answer those questions, many apparently complicated architectures
become much easier to understand.

---

## 2. Images as signals: Fourier, DCT, and wavelets

Before deep neural networks learned features automatically, computer vision
relied heavily on **handcrafted signal-processing methods**.

A grayscale image can be viewed as a two-dimensional signal. Each location has
a numerical intensity. A color image extends this idea with several channels.

Working directly with pixels is not always the easiest way to expose structure.
Signal decomposition changes the representation so that particular properties
become easier to inspect or manipulate.

### 2.1 Fourier transform

The Fourier transform represents a signal as combinations of sine and cosine
waves at different frequencies.

For images:

- **low frequencies** correspond to slow, broad changes such as smooth shading;
- **high frequencies** correspond to rapid changes such as edges and fine
  texture.

This representation makes operations such as filtering conceptually natural.
For example, suppressing some high-frequency components can reduce noise, while
retaining important low-frequency structure.

### 2.2 Discrete cosine transform (DCT)

The DCT is closely related to Fourier analysis, but it is especially useful for
compressing natural images.

Natural photographs often contain large smooth areas. This means much of their
energy can be represented using relatively few low-frequency coefficients.

A common DCT workflow is:

```text
image
  ↓
divide into small blocks
  ↓
convert each block to frequency coefficients
  ↓
retain the important coefficients
  ↓
discard or coarsely represent small high-frequency coefficients
  ↓
reconstruct an approximation of the image
```

This is one of the central ideas behind JPEG compression.

For an 8 × 8 block, the DCT produces an 8 × 8 grid of coefficients. The
upper-left area corresponds to low spatial frequencies, while moving toward the
opposite corner represents increasingly fine patterns.

[[IMAGE_NEEDED: DCT compression intuition |
Show one image block, its DCT coefficient grid with most energy concentrated
near the low-frequency corner, a thresholded coefficient grid, and a
reconstructed block |
Learner should notice that visually important structure can often be preserved
even after many small high-frequency coefficients are removed]]

### 2.3 Wavelets

Fourier and DCT tell us about frequencies, but wavelets add stronger
**localization**.

A useful distinction is:

| Method | Main intuition |
|---|---|
| Fourier transform | Which frequencies exist in the signal? |
| DCT | Can most visual information be concentrated into a compact set of frequency coefficients? |
| Wavelets | Which frequencies exist, and where do they occur? |

Wavelets are useful when preserving local edges matters, such as in denoising
or compression where we want to keep sharp structures.

### Why this matters for modern AI

These methods introduced a lasting idea:

> An image is not merely a grid of raw numbers. It contains structure that can
> be represented in ways that expose useful patterns.

Deep learning keeps the same goal but learns many of those representations
directly from data.

---

## 3. Kernels, convolution, padding, and feature maps

Signal decomposition changes the global representation of an image. Another
important family of methods searches directly for local spatial patterns.

A **kernel**, also called a filter, is a small matrix that slides over a signal
or image.

At each location:

1. align the kernel with a small region;
2. multiply corresponding values;
3. sum those products;
4. place the result in the output.

That slide-multiply-sum operation is the core intuition behind convolution.

### 3.1 Start with one dimension

Suppose part of a signal is:

```text
[3, 7]
```

and we use the kernel:

```text
[-1, 1]
```

The output is:

```text
(-1 × 3) + (1 × 7) = 4
```

A positive value tells us that the signal increased sharply.

If the signal instead contains:

```text
[5, 5]
```

then:

```text
(-1 × 5) + (1 × 5) = 0
```

No change was detected.

So this tiny kernel acts like a simple **change detector**.

### 3.2 Sliding the kernel

Now imagine the complete signal:

```text
[0, 0, 3, 7, 7, 7, 2, 2]
```

Sliding `[-1, 1]` over neighboring pairs produces strong outputs near the
locations where the signal changes.

The resulting sequence is a **feature map**: a transformed representation that
emphasizes the feature the kernel was designed to detect.

[[IMAGE_NEEDED: 1D convolution and feature map |
Show a step-like one-dimensional signal, the [-1, 1] kernel sliding over pairs,
and the resulting feature map with spikes at changes |
Learner should connect a spike in the feature map with a transition in the
original signal]]

### 3.3 Padding

Near the boundary, part of a kernel may extend beyond the available data.

**Padding** adds values around the signal so that convolution can still be
computed at the edges.

A common strategy is **zero padding**:

```text
original:       [3, 7, 7, 2]
zero padded: [0, 3, 7, 7, 2, 0]
```

Padding is not just implementation trivia. It affects output size and how edge
information is handled.

### 3.4 Move from 1D to 2D

A grayscale image is a two-dimensional grid, so a two-dimensional kernel can
slide over rows and columns.

A typical edge detector may use a 3 × 3 matrix.

Two classical families are:

- **Prewitt filters**
- **Sobel filters**

Both detect edges. Sobel filters place additional weight near the center,
giving them somewhat more robustness to local noise.

Different horizontal and vertical kernels respond to different edge
orientations.

[[IMAGE_NEEDED: 2D edge-detection kernels |
Show a small grayscale patch beside representative vertical and horizontal
Prewitt/Sobel kernels and the corresponding edge-response maps |
Learner should notice that kernel values determine which orientation or visual
pattern becomes strong in the feature map]]

### The bridge to deep learning

Handcrafted filters require an engineer to choose the kernel values.

The transformative question was:

> What if the model could learn the useful kernels automatically from data?

That question takes us directly to convolutional neural networks.

{{exercise:M01.L01.EX01}}

---

## 4. From handcrafted filters to convolutional neural networks

Convolutional neural networks (CNNs) apply the same basic operation you just
learned, but the filters are **learned**.

Instead of defining one edge detector manually, a CNN may begin with dozens of
random kernels. Training adjusts their values through gradient-based
optimization.

### 4.1 Why CNNs were hard at first

CNN ideas existed well before their modern success, but early systems faced
serious limitations:

- small labeled datasets;
- insufficient compute;
- difficulty training deep networks;
- vanishing-gradient problems.

Around 2012, several factors aligned:

- ImageNet provided large-scale labeled visual data;
- GPUs dramatically accelerated training;
- activations such as ReLU made deep optimization easier;
- regularization methods such as dropout improved generalization;
- AlexNet demonstrated that learned deep features could outperform
  handcrafted-feature pipelines on large-scale image classification.

### 4.2 Many kernels, many feature maps

Suppose a convolutional layer has 32 kernels.

Each kernel scans the input and produces one feature map:

```text
input image
   ├─ kernel 1  → feature map 1
   ├─ kernel 2  → feature map 2
   ├─ ...
   └─ kernel 32 → feature map 32
```

Each map responds to a different learned pattern.

[[IMAGE_NEEDED: CNN first-layer feature maps |
Show one input image, several small learned 3x3 filters, and multiple resulting
feature maps |
Learner should understand that one convolutional layer detects many different
patterns in parallel]]

### 4.3 Weight sharing

A fully connected network would use separate parameters for many spatial
locations.

A convolutional layer reuses the **same kernel weights** across the image.

This matters because a useful feature such as an edge can appear anywhere.
Weight sharing gives CNNs:

- fewer parameters than dense image processing;
- spatially reusable detectors;
- efficient local feature extraction.

### 4.4 Hierarchical visual representation

A major strength of deep CNNs is that features become more abstract with depth.

A simplified hierarchy is:

```text
pixels
  ↓
edges and color gradients
  ↓
textures and corners
  ↓
simple shapes
  ↓
object parts
  ↓
high-level object representation
```

Earlier layers may resemble classical edge filters. Deeper layers combine those
signals into richer concepts.

### 4.5 Backbone and head

The main feature extractor is often called the **backbone**.

The backbone produces a rich representation. A **task-specific head** turns
those features into the desired output.

For classification:

```text
image → backbone → classification head → class probabilities
```

The important design insight is that the backbone can often be reused.

---

## 5. Classification, detection, segmentation, and transfer learning

The same visual backbone can support several tasks.

### 5.1 Image classification

Classification answers:

> What category best describes this image?

Example:

```text
input: image of a cat
output:
cat  0.99
dog  0.01
```

The prediction applies to the whole image.

### 5.2 Object detection

Object detection asks two questions for each detected object:

1. **What is it?**
2. **Where is it?**

The output includes classes and bounding boxes.

```text
cat  → [x1, y1, x2, y2]
ball → [x1, y1, x2, y2]
```

### 5.3 Semantic segmentation

Semantic segmentation works at the pixel level.

Each pixel receives a class prediction.

If an image contains two cats, semantic segmentation usually labels the pixels
of both as the same class:

```text
CAT
```

### 5.4 Instance segmentation

Instance segmentation also works at the pixel level, but it distinguishes
separate objects:

```text
CAT #1
CAT #2
```

### Compare the tasks

| Task | Main output |
|---|---|
| Classification | One or more image-level labels |
| Object detection | Labels + bounding boxes |
| Semantic segmentation | Per-pixel semantic classes |
| Instance segmentation | Per-pixel masks separated by object instance |

[[IMAGE_NEEDED: Four visual computer-vision tasks |
Show the same scene as classification, object detection, semantic segmentation,
and instance segmentation outputs |
Learner should see that the visual backbone may be shared while the task output
and head change]]

### 5.5 Transfer learning

Training a large vision model from scratch can be expensive.

**Transfer learning** reuses knowledge learned during pretraining.

The intuition is simple:

- early and middle visual features can be broadly useful;
- the model does not need to relearn basic visual structure for every project;
- we can adapt pretrained features to a new domain or task.

A pretrained feature extractor is commonly reused as a **backbone**.

### 5.6 Backbone, neck, head

Modern computer-vision systems often use three conceptual stages:

```text
input
  ↓
backbone
  extracts visual features
  ↓
neck
  refines/combines features, often across scales
  ↓
head
  produces task-specific outputs
```

The **neck** is especially useful when the task must reason about objects at
multiple spatial scales or positions.

[[IMAGE_NEEDED: Backbone-neck-head pipeline |
Show an input image flowing through a generic backbone, feature-refinement neck,
and task head into an output |
Learner should understand that transfer learning commonly reuses the backbone
while neck/head design can be task specific]]

---

## 6. Three influential visual architectures

Different backbones solve different engineering problems. There is no universal
best backbone for every use case.

### 6.1 ResNet: making very deep networks trainable

As networks became deeper, gradients could become unstable.

ResNet introduced the highly influential **residual connection**.

Instead of learning only:

```text
x → transformations → output
```

a residual block also gives the input a shortcut:

```text
x ─────────────────────┐
│                      ↓
└→ transformations → add → activation
```

Conceptually, if the transformed path learns `F(x)`, the block can produce:

```text
F(x) + x
```

That direct path improves gradient flow and makes very deep networks easier to
optimize.

#### Projection shortcuts

Sometimes `x` and `F(x)` have incompatible shapes.

A 1 × 1 convolution can project the shortcut into a matching shape before the
addition.

#### Bottleneck blocks

A common bottleneck pattern is:

```text
1×1 convolution → reduce dimensions
3×3 convolution → process spatial information
1×1 convolution → expand dimensions
```

This reduces the cost of the expensive spatial convolution.

#### Batch normalization

ResNet also uses batch normalization to stabilize training by normalizing
intermediate activations.

[[IMAGE_NEEDED: ResNet residual and bottleneck block |
Show both a simple residual block and a bottleneck 1x1 → 3x3 → 1x1 block with
the shortcut path |
Learner should notice that the shortcut bypasses several transformations and is
added back to the processed signal]]

### 6.2 MobileNet: efficiency first

MobileNet focuses on resource-constrained inference.

Its central idea is **depthwise separable convolution**.

A standard convolution mixes spatial processing and cross-channel mixing in one
operation. MobileNet separates them:

1. **depthwise convolution** — one spatial filter per input channel;
2. **pointwise convolution** — a 1 × 1 convolution that mixes channels.

This can greatly reduce computation while retaining useful accuracy, making the
architecture practical for phones and embedded systems.

### 6.3 U-Net: precise localization

U-Net was designed for image segmentation.

Its shape is approximately symmetric:

```text
contracting path                expanding path
(high resolution)             (recover resolution)
      \                              /
       \________ skip links _______/
```

The contracting side captures context. The expanding side restores spatial
resolution.

Skip connections transfer fine spatial details from earlier high-resolution
features to corresponding decoding stages.

This architecture became influential in:

- biomedical segmentation;
- semantic segmentation;
- satellite imaging;
- robotics;
- later diffusion-based image generation systems.

### What to remember

| Architecture | Core problem it addresses | Signature idea |
|---|---|---|
| ResNet | Training very deep CNNs | Residual shortcuts |
| MobileNet | Efficient inference | Depthwise separable convolution |
| U-Net | Pixel-precise output | Encoder-decoder shape + skip connections |

{{exercise:M01.L01.EX02}}

---

## 7. The language path: tokens, RNNs, LSTMs, GRUs, encoders, and decoders

Vision is only half of a VLM. We also need a model that can understand and
generate language.

### 7.1 Tokenization

Text is first divided into units called **tokens**.

Early systems often used whole words, but subword tokenization became important
because it handles vocabulary more flexibly.

A **tokenizer** performs this conversion.

Conceptually:

```text
"multimodal models are useful"
            ↓
["multi", "modal", " models", " are", " useful"]
            ↓
token IDs
```

The exact segmentation depends on the tokenizer.

### 7.2 Recurrent neural networks

An RNN processes a sequence step by step.

At time step `t`, it receives:

- the current token representation;
- a hidden state carrying information from previous steps.

A simplified recurrence is:

```text
h_t = RNN(x_t, h_(t-1))
```

The hidden state is the model's evolving representation of what it has seen.

[[IMAGE_NEEDED: Unrolled RNN |
Show tokens x1, x2, x3, x4 entering sequential RNN cells with hidden states
h1, h2, h3, h4 flowing forward |
Learner should see that later computation depends on a chain of earlier hidden
states]]

### 7.3 Why recurrence becomes difficult

Long sequences create two important problems.

First, early information must travel through many recurrent steps.

Second, gradients can become very small or very large during training.

This makes long-range learning difficult.

### 7.4 LSTM and GRU

**LSTM** networks introduced gates that control how information is retained,
added, updated, or removed.

**GRU** networks use a simplified gated design.

Both aim to preserve useful information across longer spans than a basic RNN.

### 7.5 Encoders and decoders

An **encoder** converts an input sequence into a representation.

A **decoder** generates an output sequence from a representation.

For translation:

```text
English sentence
      ↓
   encoder
      ↓
representation
      ↓
   decoder
      ↓
French sentence
```

A major weakness of early encoder-decoder RNN systems was compression:
representing a long input sequence through a limited recurrent state becomes a
bottleneck.

### 7.6 Attention changes the picture

Attention lets the decoder focus selectively on different encoder states rather
than depending only on one compressed representation.

That idea became foundational to the transformer family.

The deeper attention mechanics come later; for now, remember the purpose:

> Attention gives the model a direct mechanism for deciding which parts of an
> input are most relevant to another part of the computation.

---

## 8. The transformer boom in language

Transformers made it much easier to learn relationships across a sequence.

Three influential model patterns help organize the landscape.

### 8.1 BERT: encoder-focused understanding

BERT became a highly influential transformer encoder.

Its pretraining uses masked language modeling:

```text
"The cat sat on the [MASK]."
                    ↓
                predict "mat"
```

Because the training target can be produced from ordinary text itself, large
unlabeled corpora become useful for pretraining.

After pretraining, the encoder can be adapted to downstream tasks using
task-specific heads.

{{image:bert-pretraining-finetuning}}

This mirrors transfer learning in computer vision:

```text
pretrained representation + new task head
```

### 8.2 GPT-style decoder models: autoregressive generation

A decoder-only language model learns to predict the next token.

Example:

```text
input:  "The bee landed on the"
target: "flower"
```

Training repeatedly shifts that prediction target through text.

This is **autoregressive next-token prediction**.

During generation, predicted tokens become part of the context for later
predictions.

### 8.3 T5: text-to-text encoder-decoder

T5 popularized a unified text-to-text approach.

Different tasks can be expressed using text input and text output:

```text
translate: English → French
summarize: long text → short text
classify sentiment: review → positive
```

The architecture uses an encoder-decoder transformer.

### Three useful categories

| Family | Main structure | Typical strength |
|---|---|---|
| BERT-style | Encoder | Understanding/representation |
| GPT-style | Decoder-only | Autoregressive generation |
| T5-style | Encoder-decoder | Input-to-output sequence transformation |

This classification is a mental model, not a claim that any family can perform
only one kind of task.

---

## 9. Vision Transformers: treating image patches like tokens

CNNs build understanding mainly from local neighborhoods.

Self-attention offers another possibility:

> Any token can directly interact with any other token in the same attention
> computation.

The Vision Transformer (ViT) adapts this idea to images.

### 9.1 Turn an image into patch tokens

Suppose the image is:

```text
224 × 224 pixels
```

and patches are:

```text
16 × 16 pixels
```

The number of patches along each dimension is:

```text
224 / 16 = 14
```

So the total number of patches is:

```text
14 × 14 = 196
```

For an RGB image, each patch contains:

```text
16 × 16 × 3 = 768
```

raw values before projection.

Each patch is flattened and mapped into an embedding.

A simplified ViT pipeline is:

```text
image
  ↓
split into patches
  ↓
flatten + linear projection
  ↓
patch embeddings
  ↓
add positional information
  ↓
transformer encoder
  ↓
task representation
  ↓
classification head
```

A special classification token may be added to aggregate information for image
classification.

{{image:vision-transformer-vit}}

### 9.2 Why position matters

If patches were treated as an unordered set, the model would lose important
spatial structure.

Positional information tells the transformer where each patch came from.

### 9.3 Try a pretrained ViT

The chapter introduces the Hugging Face `pipeline` abstraction:

```bash
pip install transformers
```

```python
from transformers import pipeline

pipe = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224",
)

result = pipe(
    "https://huggingface.co/datasets/vlmbook/images/resolve/main/bee.jpg"
)

print(result[:3])
```

The key lesson is not the exact score. It is the workflow:

```text
pretrained model + processor abstraction + image
                ↓
             predictions
```

### 9.4 ViT variations

Several important variations change how the model learns or organizes visual
tokens.

#### Masked Autoencoder (MAE)

MAE removes some image patches and trains the system to reconstruct missing
visual content.

This creates a self-supervised learning signal.

```text
image patches
  ↓
mask many patches
  ↓
encode visible patches
  ↓
reconstruct missing information
```

{{image:masked-autoencoder}}

#### BEiT

BEiT uses an approach conceptually similar to masked language modeling, but with
visual tokens.

#### Hierarchical ViTs

Hierarchical models progressively change spatial resolution and feature
structure across stages.

This is valuable for dense tasks such as segmentation or object localization.

#### DeiT

DeiT focuses on data-efficient transformer training and makes use of
distillation from a larger teacher model.

### The important shift

CNNs encode a strong local inductive structure through convolution.

ViTs make global interaction through attention a central mechanism.

Modern systems often combine ideas from both families rather than treating them
as mutually exclusive.

---

## 10. CLIP: learning a shared language for images and text

So far, we have a strong visual encoder and strong text models.

But how can a model learn that an image of a dog and the sentence:

```text
"a happy dog"
```

belong together?

CLIP addresses this by learning a **shared embedding space**.

### 10.1 Two encoders

CLIP contains:

- an image encoder;
- a text encoder.

Each converts its input into a vector.

```text
image → image encoder → image embedding
text  → text encoder  → text embedding
```

### 10.2 Contrastive learning

Suppose a training batch contains `N` matching image-text pairs.

After encoding, we have:

```text
I1, I2, ..., IN
T1, T2, ..., TN
```

Compute similarity between every image and every text:

```text
          T1    T2    T3   ...   TN
I1       s11   s12   s13   ...  s1N
I2       s21   s22   s23   ...  s2N
...
IN       sN1   sN2   sN3   ...  sNN
```

The correct pairs sit on the diagonal:

```text
I1 ↔ T1
I2 ↔ T2
...
IN ↔ TN
```

Training tries to:

- increase similarity for matching pairs;
- decrease similarity for mismatched pairs.

[[IMAGE_NEEDED: CLIP similarity matrix |
Show N image embeddings on rows, N text embeddings on columns, with the
matching diagonal highlighted and off-diagonal mismatches suppressed |
Learner should understand that contrastive learning rewards aligned image-text
pairs rather than requiring a fixed category label]]

### 10.3 Symmetric alignment

The training objective considers both directions:

- image → text;
- text → image.

That encourages one shared space that supports cross-modal comparison.

### 10.4 Why this enables zero-shot classification

Suppose we have an image and three candidate descriptions:

```text
"bee on a flower"
"bee in the hive"
"bee in the sky"
```

CLIP can encode:

- the image once;
- each candidate text;

then compare similarities.

The highest-scoring text becomes the best match.

No new classifier head must be trained for those exact labels.

This is the intuition behind **zero-shot image classification**.

### 10.5 CLIP inference with Hugging Face

```python
from transformers import pipeline

model_id = "openai/clip-vit-large-patch14"

pipe = pipeline(
    "zero-shot-image-classification",
    model=model_id,
)

labels = [
    "bee on a flower",
    "bee in the hive",
    "bee in the sky",
]

result = pipe(
    image="https://oreil.ly/ne2UQ",
    candidate_labels=labels,
)

print(result)
```

### 10.6 What CLIP can and cannot do

CLIP-style models are excellent at **matching** representations.

A classic CLIP system does not itself behave like a conversational language
generator that produces long new answers from visual input.

This limitation motivates the next step: combine strong visual encoders with
generative language models.

{{exercise:M01.L01.EX03}}

---

## 11. The blueprint of a modern vision-language model

A common modern VLM contains three conceptual components:

```text
image
  ↓
vision encoder
  ↓
visual features/tokens
  ↓
multimodal projection or connector
  ↓
language-model-compatible representations
  ↓
text decoder / language model
  ↓
generated response
```

### 11.1 Vision encoder

The image encoder is often a ViT-like model.

Its job is to turn pixels into useful visual tokens or feature vectors.

### 11.2 Projection layer

The vision encoder and language model usually do not naturally produce and
consume identically shaped representations.

A projection layer maps visual features into the representation space expected
by the text model.

A simplified linear mapping is:

```text
visual feature dimension
          ↓
      projection
          ↓
language-model embedding dimension
```

The projected visual tokens can then be combined with text embeddings.

{{image:vlm-multimodal-projector}}

### 11.3 Text decoder

A transformer-based language model receives the multimodal representation and
generates text.

This allows tasks such as:

```text
image + "What animal is shown?"
              ↓
          "A turtle."
```

### 11.4 Training stages

A common training strategy described in the chapter is:

1. start from pretrained visual and language components;
2. freeze major pretrained components while training the multimodal projection;
3. teach the connector to map visual features into a language-compatible space;
4. later train or fine-tune additional parts of the whole system;
5. use multimodal instruction data for tasks involving images, instructions,
   and responses.

{{image:vlm-pretraining-finetuning}}

### 11.5 Minimal inference example

The chapter uses an image-text-to-text pipeline.

```python
from transformers import pipeline

pipe = pipeline(
    "image-text-to-text",
    model="OpenGVLab/InternVL3-1B-hf",
)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "url": "https://oreil.ly/jlwF2",
            },
            {
                "type": "text",
                "text": "What animal is on the candy?",
            },
        ],
    }
]

result = pipe(
    text=messages,
    return_full_text=False,
)

print(result[0]["generated_text"])
```

The practical lesson is that a VLM is not magic. At a high level, it combines
well-understood components:

```text
visual representation
+
cross-modal connector
+
language generation
```

---

## 12. Hugging Face: models, datasets, processors, and reusable workflows

Training a large multimodal model from scratch is usually expensive.

The Hugging Face ecosystem makes pretrained models and datasets easier to
discover and reuse.

### 12.1 Hugging Face Hub

The Hub hosts model repositories, datasets, and demos.

A model repository typically contains several useful areas.

#### Model card

A model card can include:

- intended task;
- library/framework;
- license;
- inputs and outputs;
- usage examples;
- training details;
- evaluation metrics;
- hardware information;
- limitations.

A good habit is:

> Read the model card before copying code from an old tutorial.

APIs, preprocessing requirements, licenses, and recommended inference settings
can change.

#### Files and versions

This section contains model weights, configuration files, tokenizer or
processor assets, and version history.

#### Community

Discussions and pull requests can reveal:

- known issues;
- implementation details;
- fixes;
- usage questions;
- model-owner recommendations.

### 12.2 Access tokens

The chapter distinguishes:

- fine-grained tokens;
- read tokens;
- write tokens.

For security, use the smallest permission set needed for the task.

Avoid placing secret tokens directly in notebooks or source code.

[[IMAGE_NEEDED: Hugging Face model repository anatomy |
Show a generic model repository page with model card, files/versions, and
community areas called out |
Learner should know where to look for usage instructions, weights/configs, and
community troubleshooting]]

---

## 13. Core Hugging Face abstractions

Several abstractions appear repeatedly in multimodal workflows.

### 13.1 `AutoModel`

A task-specific `AutoModel...` class loads model weights and selects the
appropriate implementation for the repository.

For example, the chapter uses a zero-shot image-classification model class.

### 13.2 `AutoProcessor`

A multimodal model needs preprocessing for different input types.

The processor may combine:

- a text tokenizer;
- an image processor.

So instead of manually implementing every resizing, normalization, and
tokenization step, the model's processor packages the expected preprocessing.

### 13.3 Model + processor example

```python
from PIL import Image
import requests

from transformers import (
    AutoModelForZeroShotImageClassification,
    AutoProcessor,
)

model_id = "openai/clip-vit-large-patch14"

model = (
    AutoModelForZeroShotImageClassification
    .from_pretrained(model_id)
    .to("cuda")
)

processor = AutoProcessor.from_pretrained(model_id)

url = (
    "https://huggingface.co/datasets/vlmbook/images/"
    "resolve/main/bee.jpg"
)

image = Image.open(
    requests.get(url, stream=True).raw
)

inputs = processor(
    text=[
        "a bee on a flower",
        "a bee in a hive",
    ],
    images=image,
    return_tensors="pt",
    padding=True,
).to("cuda")

outputs = model(**inputs)

probs = outputs.logits_per_image.softmax(dim=1)

print(probs)
```

The sequence is:

```text
raw image + raw text
        ↓
     processor
        ↓
model-ready tensors
        ↓
       model
        ↓
      logits
        ↓
interpretation / probabilities
```

### 13.4 `pipeline`

`pipeline` packages preprocessing, model inference, and postprocessing.

It is ideal when:

- you want to test a model quickly;
- the task is supported directly;
- you do not need low-level control.

```python
from transformers import pipeline

classifier = pipeline(
    task="zero-shot-image-classification",
    model="openai/clip-vit-large-patch14",
)
```

{{image:huggingface-inference-pipeline}}

### 13.5 `Trainer`

`Trainer` abstracts common training-loop responsibilities such as:

- dataset iteration;
- loss handling;
- optimization;
- gradient accumulation;
- gradient checkpointing;
- evaluation.

It is useful when you want to fine-tune rather than only infer.

### 13.6 `Accelerate`

Large-model training may involve:

- mixed precision;
- multiple GPUs;
- distributed processes;
- different hardware setups.

`Accelerate` helps run similar PyTorch code across these configurations.

### Choosing the abstraction

| Goal | Useful abstraction |
|---|---|
| Fast inference prototype | `pipeline` |
| More control over inference | `AutoModel` + `AutoProcessor` |
| Reusable fine-tuning loop | `Trainer` |
| Hardware/distributed simplification | `Accelerate` |

---

## 14. Hugging Face Datasets

Multimodal datasets can be large and memory-intensive.

The `datasets` library provides tools for loading, streaming, transforming, and
working with datasets without manually implementing the entire data pipeline.

Install it with:

```bash
pip install datasets
```

### 14.1 Load a dataset

```python
from datasets import load_dataset

ds = load_dataset("merve/vqav2-small")

print(ds)
```

A returned `DatasetDict` can contain multiple splits.

The chapter's example has a validation split with fields such as:

```text
question
image
multiple_choice_answer
```

### 14.2 Access an example

```python
example = ds["validation"][0]

print(example["question"])
print(example["multiple_choice_answer"])
print(example["image"])
```

### 14.3 Transform examples with `map`

```python
def preprocess(example):
    example["question"] = example["question"].lower()
    return example

ds["validation"] = ds["validation"].map(preprocess)
```

The key idea:

> Dataset transformations can be expressed as reusable functions rather than
> hand-written loops scattered through training code.

---

## 15. Build the first multimodal application: text-to-image retrieval

Now we combine the chapter's central ideas into an application.

The goal is:

> Given a natural-language query, retrieve the images whose embeddings are
> closest to the query embedding.

The source uses a SigLIP-family model and FAISS.

### 15.1 System design

There are two phases.

#### Offline phase: image indexing

```text
images
  ↓
SigLIP image encoder
  ↓
image embeddings
  ↓
normalize
  ↓
FAISS index
```

#### Online phase: text search

```text
text query
  ↓
SigLIP text encoder
  ↓
text embedding
  ↓
normalize
  ↓
nearest-neighbor search in FAISS
  ↓
matching images
```

{{image:siglip-image-text-retrieval}}

### 15.2 Why a shared embedding space works

SigLIP is CLIP-like.

Its image tower and text tower produce embeddings that can be compared.

That means semantically related text and images should occupy nearby regions of
the learned representation space.

Example:

```text
query: "a woman"
          ↓
text embedding
          ↓
nearest image vectors
          ↓
artworks visually associated with the query
```

### 15.3 Install the tools

The chapter uses:

```bash
pip install datasets transformers sentencepiece
```

and a FAISS build appropriate for the environment.

For a CUDA 12.x GPU environment, the source specifically points to:

```bash
pip install faiss-gpu-cu12
```

Your actual FAISS package must match your runtime.

### 15.4 Load SigLIP

```python
import torch

from transformers import (
    AutoModel,
    AutoProcessor,
    AutoTokenizer,
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model_id = "google/siglip-base-patch16-224"

model = AutoModel.from_pretrained(
    model_id,
    device_map="auto",
).eval()

processor = AutoProcessor.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)
```

### 15.5 Create an image-embedding helper

```python
def embed_siglip(image):
    with torch.no_grad():
        inputs = processor(
            images=image,
            return_tensors="pt",
        ).to(device)

        image_features = model.get_image_features(**inputs)

        return image_features.pooler_output
```

The flow is:

```text
PIL image
   ↓
processor
   ↓
pixel tensors
   ↓
image tower
   ↓
embedding vector
```

### 15.6 Add vectors to FAISS

```python
import numpy as np
import faiss


def add_vector(embedding, index):
    vector = embedding.detach().cpu().numpy()
    vector = np.float32(vector)

    faiss.normalize_L2(vector)

    index.add(vector)
```

Normalization matters because retrieval is based on comparing vector geometry.

### 15.7 Important implementation check: embedding dimension

The supplied chapter contains an internal implementation inconsistency worth
catching before you run the code.

Its narrative states one SigLIP embedding dimensionality, while the example
creates a FAISS index with a different dimension.

Do not hard-code the dimension until you inspect the actual model output.

A safer pattern is:

```python
sample_embedding = embed_siglip(sample_image)

embedding_dim = sample_embedding.shape[-1]

index = faiss.IndexFlatL2(embedding_dim)
```

This is a useful engineering habit beyond this example:

> Let the actual model output define the vector-index dimension.

If the FAISS index dimension and embedding dimension disagree, indexing will
fail.

### 15.8 Index the images

Conceptually:

```python
for image in dataset:
    embedding = embed_siglip(image)
    add_vector(embedding, index)
```

In the source example, image URLs are obtained from a small subset of an art
dataset and then encoded one by one.

### 15.9 Save and reload the index

```python
faiss.write_index(
    index,
    "./siglip_artworks.index",
)

index = faiss.read_index(
    "./siglip_artworks.index",
)
```

This separates expensive offline indexing from later queries.

### 15.10 Encode a text query

```python
prompt = "a woman"

text_token = processor.tokenizer(
    [prompt],
    return_tensors="pt",
).to(device)

text_features = model.get_text_features(
    **text_token
)

text_features = (
    text_features
    .detach()
    .cpu()
    .numpy()
)

text_features = np.float32(text_features)

faiss.normalize_L2(text_features)
```

Now the text has been placed into the same kind of representation space used
for retrieval.

### 15.11 Search

```python
distances, indices = index.search(
    text_features,
    2,
)

print(indices)
print(distances)
```

The returned indices tell you which stored images are nearest to the query.

The result can be mapped back to dataset rows.

### 15.12 What you have actually built

This small application contains the same core architecture found in much larger
systems:

```text
unstructured content
      ↓
embedding model
      ↓
vector database / vector index
      ↓
query embedding
      ↓
nearest-neighbor retrieval
      ↓
relevant results
```

Only the modality has changed.

The exact same pattern appears in:

- semantic text search;
- image search;
- recommendation;
- multimodal retrieval;
- retrieval-augmented systems.

{{exercise:M01.L01.EX04}}

---

## 16. Connect the whole chapter into one mental model

The chapter contains many architectures, but they form one coherent story.

### Stage 1 — Engineer visual features

```text
pixels
  ↓
Fourier / DCT / wavelets
  ↓
handcrafted kernels
```

Humans decide which transformation exposes useful structure.

### Stage 2 — Learn visual features

```text
pixels
  ↓
CNN
  ↓
learned hierarchy of features
```

The model learns filters through optimization.

### Stage 3 — Build reusable backbones

```text
pretrained backbone
  ↓
classification / detection / segmentation head
```

Transfer learning makes learned representations reusable.

### Stage 4 — Improve sequence modeling

```text
tokens
  ↓
RNN → LSTM/GRU
  ↓
attention
  ↓
transformers
```

Language models become better at representing and generating long sequences.

### Stage 5 — Bring transformers to images

```text
image
  ↓
patch tokens
  ↓
ViT
```

Images become sequences of visual tokens.

### Stage 6 — Align images and text

```text
image encoder ─┐
               ├→ shared embedding space
text encoder ──┘
```

CLIP-style contrastive learning connects semantics across modalities.

### Stage 7 — Make vision conversational

```text
vision encoder
     ↓
multimodal projector
     ↓
language model
     ↓
generated answer
```

Now the model can not only compare images and text but generate language
grounded in visual information.

### Stage 8 — Turn the ideas into applications

Hugging Face provides reusable model and data abstractions.

Vector search tools such as FAISS make embedding-based retrieval practical.

That leads directly to multimodal applications such as:

- text-to-image search;
- image-to-text matching;
- visual question answering;
- document understanding;
- multimodal assistants.

---

## Important misconceptions

### Misconception 1: "A CNN is just a large collection of manually designed edge filters."

That misses the central idea.

CNN filters are learned during training. Some early filters may resemble
classical edge detectors because edges are useful low-level features, but the
network is not restricted to a fixed handcrafted filter bank.

### Misconception 2: "A backbone already solves the entire application."

A backbone mainly extracts representations.

The head, and often a neck, turns those representations into task-specific
predictions.

### Misconception 3: "A Vision Transformer reads pixels exactly like a language model reads words."

The analogy is useful but incomplete.

ViT first converts image patches into learned embeddings and adds spatial
position information. Patches are visual input units, not linguistic words.

### Misconception 4: "CLIP is the same thing as a conversational VLM."

CLIP-style models align image and text representations and score similarity.

A modern generative VLM adds a language-generation component so the system can
produce free-form text responses.

### Misconception 5: "Zero-shot means the model has never learned anything related to the task."

Zero-shot means no additional task-specific training is provided for the new
prediction setup. The model still relies on knowledge learned during its large
pretraining process.

### Misconception 6: "Using a pretrained model removes the need to understand preprocessing."

Preprocessing still matters.

The practical advantage of abstractions such as `AutoProcessor` and `pipeline`
is that they package model-compatible preprocessing so you are less likely to
implement it incorrectly.

---

## Key terminology

| Term | Meaning |
|---|---|
| Modality | A type of input or information, such as text, image, audio, or video |
| VLM | A vision-language model that connects visual and linguistic information |
| Frequency | How quickly a signal changes across space or time |
| Fourier transform | A representation based on sinusoidal frequency components |
| DCT | A cosine-based transform widely used for compact image representation and JPEG compression |
| Wavelet | A localized signal representation useful for examining frequency and position |
| Kernel / filter | A small matrix that scans a signal or image to detect a pattern |
| Convolution | Slide-multiply-sum operation used to create feature maps |
| Padding | Added boundary values that control convolution behavior near edges |
| Feature map | Output highlighting where a learned or designed feature occurs |
| CNN | Neural network that learns convolutional filters for spatial data |
| Backbone | Main pretrained feature extractor |
| Neck | Intermediate feature-refinement stage between backbone and head |
| Head | Task-specific output component |
| Transfer learning | Reusing knowledge from a pretrained model for a new task |
| Residual connection | Shortcut that adds an earlier activation to a later transformed output |
| Depthwise separable convolution | Efficient convolution split into depthwise and pointwise stages |
| U-Net | Encoder-decoder segmentation architecture with skip connections |
| Token | Numerical unit produced from a piece of text |
| Tokenizer | Component that splits/encodes text into model input tokens |
| Hidden state | Recurrent representation carrying sequence information forward |
| RNN | Sequential neural network with recurrent hidden state |
| LSTM | Gated recurrent network designed to preserve useful long-range information |
| GRU | Simplified gated recurrent architecture |
| Encoder | Component that turns input into a representation |
| Decoder | Component that generates an output sequence |
| Attention | Mechanism for weighting relationships among different input positions |
| Transformer | Architecture built around attention-based sequence processing |
| ViT | Vision Transformer that represents images as patch tokens |
| Patch embedding | Vector representation of an image patch |
| Positional information | Encoding that tells a transformer where a token or patch belongs |
| MAE | Masked Autoencoder trained by reconstructing missing image content |
| BEiT | Transformer approach that learns from masked visual tokens |
| DeiT | Data-efficient vision transformer approach using distillation |
| Contrastive learning | Training that pulls matching pairs together and pushes mismatches apart |
| CLIP | Dual-encoder image-text model trained with contrastive alignment |
| Embedding | Dense vector representing semantic information |
| Zero-shot classification | Classification using new natural-language labels without additional task-specific training |
| Projection layer | Connector that maps features from one representation dimension/space to another |
| AutoModel | Hugging Face abstraction that loads an appropriate model implementation |
| AutoProcessor | Preprocessing abstraction combining model-compatible image/text processing |
| Pipeline | High-level Hugging Face interface for preprocessing, inference, and postprocessing |
| Trainer | Hugging Face abstraction for common model-training loops |
| Accelerate | Library that simplifies multi-device and distributed PyTorch execution |
| FAISS | Vector indexing/search library for nearest-neighbor retrieval |
| Vector search | Retrieval based on distances or similarities between embeddings |

---

## Self-check

Before continuing, make sure you can answer these without looking back:

1. Why are low-frequency DCT coefficients often important in natural images?
2. What does the kernel `[-1, 1]` detect in a 1D signal?
3. What is the difference between a handcrafted kernel and a CNN kernel?
4. Why does weight sharing make sense for image features?
5. How do classification and object detection outputs differ?
6. What are the roles of backbone, neck, and head?
7. Why do residual connections help deep networks?
8. What problem do LSTMs and GRUs address relative to basic RNNs?
9. What is the difference between an encoder and a decoder?
10. How does next-token prediction differ from masked-token prediction?
11. How does ViT turn an image into transformer input?
12. Why does ViT need positional information?
13. In CLIP training, what should happen to matching versus mismatching pairs?
14. Why can CLIP perform zero-shot image classification?
15. What additional component lets a modern VLM generate language from visual features?
16. When would you prefer `pipeline` over `AutoModel` + `AutoProcessor`?
17. What is stored in FAISS in the chapter's retrieval application?
18. Why should the FAISS dimension be derived from the model output rather than assumed?

---

## Retain this idea

**Modern vision-language models are the result of several reusable ideas joining
together: learned visual representations, attention-based sequence modeling,
shared multimodal embedding spaces, transfer learning, and a connector that
allows visual information to become usable by a language model.**

If you understand how each representation is created and how the components are
connected, the architecture of new multimodal systems becomes far less
mysterious.
""",

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-vision-language",
                "title": "Why combine vision and language?",
                "order": 1,
            },
            {
                "id": "signal-decomposition",
                "title": "Images as signals: Fourier, DCT, and wavelets",
                "order": 2,
            },
            {
                "id": "kernels-convolution",
                "title": "Kernels, convolution, padding, and feature maps",
                "order": 3,
            },
            {
                "id": "cnn-revolution",
                "title": "From handcrafted filters to convolutional neural networks",
                "order": 4,
            },
            {
                "id": "vision-tasks-transfer",
                "title": "Classification, detection, segmentation, and transfer learning",
                "order": 5,
            },
            {
                "id": "backbones",
                "title": "Three influential visual architectures",
                "order": 6,
            },
            {
                "id": "language-before-transformers",
                "title": "The language path",
                "order": 7,
            },
            {
                "id": "transformer-language",
                "title": "The transformer boom in language",
                "order": 8,
            },
            {
                "id": "vision-transformers",
                "title": "Vision Transformers",
                "order": 9,
            },
            {
                "id": "clip",
                "title": "CLIP and shared image-text embeddings",
                "order": 10,
            },
            {
                "id": "modern-vlm",
                "title": "The blueprint of a modern vision-language model",
                "order": 11,
            },
            {
                "id": "hugging-face",
                "title": "The Hugging Face ecosystem",
                "order": 12,
            },
            {
                "id": "hf-abstractions",
                "title": "Core Hugging Face abstractions",
                "order": 13,
            },
            {
                "id": "datasets",
                "title": "Hugging Face Datasets",
                "order": 14,
            },
            {
                "id": "retrieval-app",
                "title": "Text-to-image retrieval with SigLIP and FAISS",
                "order": 15,
            },
            {
                "id": "full-mental-model",
                "title": "Connect the whole chapter into one mental model",
                "order": 16,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Manually compute a 1D convolution",

            "lesson_code": "M01.L01",

            "section_id": "kernels-convolution",

            "placement": "after_section",

            "description": (
                "Practice the slide-multiply-sum operation and interpret the "
                "result as a change-detection feature map."
            ),

            "instructions": (
                "Use the signal [2, 2, 5, 5, 1] and the kernel [-1, 1].\n"
                "1. Compute the convolution over each adjacent pair without padding.\n"
                "2. Write the resulting feature map.\n"
                "3. Identify where the strongest positive and negative changes occur.\n"
                "4. Explain what the sign of each non-zero response means."
            ),

            "expected_output": (
                "A short calculation table showing each adjacent pair, its "
                "convolution result, the final feature map, and a written "
                "interpretation of the positive and negative transitions."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "convolution",
                "kernel-interpretation",
                "feature-maps",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Choose an architecture for the constraint",

            "lesson_code": "M01.L01",

            "section_id": "backbones",

            "placement": "after_section",

            "description": (
                "Match ResNet, MobileNet, and U-Net to practical vision-system "
                "requirements."
            ),

            "instructions": (
                "For each scenario, choose ResNet, MobileNet, or U-Net and justify your answer:\n"
                "1. Pixel-precise segmentation of medical scans.\n"
                "2. Real-time image recognition on a low-power mobile device.\n"
                "3. A deep general-purpose CNN backbone where stable optimization is important.\n"
                "For each choice, name the architectural idea that supports your decision."
            ),

            "expected_output": (
                "A three-row table containing the scenario, chosen architecture, "
                "signature architectural idea, and a two-to-three sentence justification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "architecture-selection",
                "resnet",
                "mobilenet",
                "unet",
            ],
        },

        {
            "id": "M01.L01.EX03",

            "title": "Reason through a CLIP similarity matrix",

            "lesson_code": "M01.L01",

            "section_id": "clip",

            "placement": "after_section",

            "description": (
                "Use a small similarity matrix to understand contrastive image-text "
                "alignment."
            ),

            "instructions": (
                "Assume a batch contains three correct image-text pairs: "
                "(cat image, 'a cat'), (dog image, 'a dog'), and "
                "(bee image, 'a bee on a flower').\n"
                "1. Draw a 3x3 similarity matrix.\n"
                "2. Mark the cells that should become large during contrastive training.\n"
                "3. Mark two off-diagonal cells that should become small.\n"
                "4. Explain why the same representation can later support zero-shot labels."
            ),

            "expected_output": (
                "A labeled 3x3 matrix with the diagonal identified as positive pairs "
                "and a short explanation of the contrastive objective and zero-shot use."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "contrastive-learning",
                "clip",
                "multimodal-embeddings",
                "zero-shot-learning",
            ],
        },

        {
            "id": "M01.L01.EX04",

            "title": "Design a safe embedding-index pipeline",

            "lesson_code": "M01.L01",

            "section_id": "retrieval-app",

            "placement": "after_section",

            "description": (
                "Turn the chapter's SigLIP/FAISS example into a robust retrieval plan."
            ),

            "instructions": (
                "Design pseudocode for a text-to-image retrieval system.\n"
                "Your solution must:\n"
                "1. Load a pretrained image-text model and processor.\n"
                "2. Compute one sample image embedding first.\n"
                "3. Derive the FAISS index dimension from that embedding.\n"
                "4. Normalize and index all image embeddings.\n"
                "5. Encode and normalize a text query.\n"
                "6. Retrieve the top 5 nearest images.\n"
                "7. Explain why the vector dimension check prevents a failure."
            ),

            "expected_output": (
                "Pseudocode or Python-like code plus a concise explanation of the "
                "offline indexing stage, online query stage, and embedding-dimension check."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "siglip",
                "faiss",
                "vector-search",
                "retrieval-system-design",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "Introduction to Vision and Language — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",
                "section_id": "signal-decomposition",
                "question": (
                    "Which statement best captures the difference between a "
                    "global frequency transform and a wavelet representation?"
                ),
                "options": [
                    "Wavelets remove all spatial information from an image.",
                    "Wavelets can represent frequency information together with stronger spatial localization.",
                    "Fourier transforms operate only on text tokens.",
                    "DCT cannot represent smooth image regions.",
                ],
                "correct": 1,
                "explanation": (
                    "Wavelets are useful because they provide information about "
                    "both frequency content and where that content occurs."
                ),
            },
            {
                "id": "M01.L01.Q02",
                "section_id": "kernels-convolution",
                "question": (
                    "What does the 1D kernel [-1, 1] respond strongly to?"
                ),
                "options": [
                    "A difference between neighboring values",
                    "The total length of the signal",
                    "Only the first value in the signal",
                    "The average of all values in the signal",
                ],
                "correct": 0,
                "explanation": (
                    "The output is -x_t + x_(t+1), so the kernel measures a local "
                    "change between adjacent values."
                ),
            },
            {
                "id": "M01.L01.Q03",
                "section_id": "cnn-revolution",
                "question": (
                    "What is the most important difference between classical "
                    "handcrafted filters and CNN filters?"
                ),
                "options": [
                    "CNN filters cannot detect edges.",
                    "CNN filters are learned from data during training.",
                    "Classical filters always have more parameters.",
                    "CNN filters can be applied only once per image.",
                ],
                "correct": 1,
                "explanation": (
                    "CNN kernels begin as trainable parameters and are optimized "
                    "from data rather than fixed entirely by an engineer."
                ),
            },
            {
                "id": "M01.L01.Q04",
                "section_id": "vision-tasks-transfer",
                "question": (
                    "Which task must predict both object category and object location?"
                ),
                "options": [
                    "Whole-image classification",
                    "Object detection",
                    "Language modeling",
                    "DCT compression",
                ],
                "correct": 1,
                "explanation": (
                    "Object detection predicts classes together with bounding-box "
                    "coordinates for one or more objects."
                ),
            },
            {
                "id": "M01.L01.Q05",
                "section_id": "backbones",
                "question": (
                    "What is the defining idea of a ResNet residual block?"
                ),
                "options": [
                    "Removing all nonlinear activations",
                    "Adding a shortcut path that bypasses one or more transformations",
                    "Replacing images with text tokens",
                    "Using only 1x1 convolutions everywhere",
                ],
                "correct": 1,
                "explanation": (
                    "Residual connections let the input travel through a shortcut "
                    "and be added to the transformed path, improving deep-network training."
                ),
            },
            {
                "id": "M01.L01.Q06",
                "section_id": "language-before-transformers",
                "question": (
                    "Why were LSTMs and GRUs introduced?"
                ),
                "options": [
                    "To convert images into JPEG files",
                    "To improve recurrent handling of longer-range sequence information",
                    "To replace all tokenizers",
                    "To perform vector search in FAISS",
                ],
                "correct": 1,
                "explanation": (
                    "Their gating mechanisms help preserve and update useful state "
                    "over longer sequences than a basic RNN."
                ),
            },
            {
                "id": "M01.L01.Q07",
                "section_id": "transformer-language",
                "question": (
                    "Which training description best matches an autoregressive "
                    "decoder-style language model?"
                ),
                "options": [
                    "Predict a future/next token from prior context",
                    "Predict a bounding box around every noun",
                    "Compress an image using DCT",
                    "Match only identical images",
                ],
                "correct": 0,
                "explanation": (
                    "Autoregressive language modeling repeatedly predicts the next "
                    "token given previous context."
                ),
            },
            {
                "id": "M01.L01.Q08",
                "section_id": "vision-transformers",
                "question": (
                    "How does a standard Vision Transformer prepare an image for "
                    "transformer processing?"
                ),
                "options": [
                    "It converts the whole image into one scalar.",
                    "It splits the image into patches and maps them to embeddings.",
                    "It uses only manually designed Sobel filters.",
                    "It converts pixels directly into spoken audio.",
                ],
                "correct": 1,
                "explanation": (
                    "ViT divides an image into patches, projects those patches into "
                    "embeddings, adds position information, and applies a transformer."
                ),
            },
            {
                "id": "M01.L01.Q09",
                "section_id": "clip",
                "question": (
                    "During CLIP-style contrastive training, what should happen to "
                    "matching image-text pairs?"
                ),
                "options": [
                    "Their similarity should be reduced.",
                    "Their embeddings should be deleted.",
                    "Their similarity should increase relative to mismatched pairs.",
                    "They should be sent through unrelated decoders.",
                ],
                "correct": 2,
                "explanation": (
                    "The contrastive objective rewards correct image-text alignment "
                    "and penalizes mismatched pairings."
                ),
            },
            {
                "id": "M01.L01.Q10",
                "section_id": "modern-vlm",
                "question": (
                    "Why is a projection/connector layer useful in a modern VLM?"
                ),
                "options": [
                    "It converts all text into JPEG.",
                    "It maps visual representations into a form compatible with the language model.",
                    "It replaces the image encoder with FAISS.",
                    "It prevents the model from receiving text.",
                ],
                "correct": 1,
                "explanation": (
                    "The visual encoder and language model may use different "
                    "representation dimensions/spaces, so the connector aligns them."
                ),
            },
            {
                "id": "M01.L01.Q11",
                "section_id": "hf-abstractions",
                "question": (
                    "Which Hugging Face abstraction is most suitable for a quick "
                    "supported inference workflow with preprocessing and postprocessing bundled?"
                ),
                "options": [
                    "pipeline",
                    "FAISS IndexFlatL2",
                    "NumPy only",
                    "A residual block",
                ],
                "correct": 0,
                "explanation": (
                    "`pipeline` is the high-level abstraction that packages model "
                    "loading, preprocessing, inference, and output postprocessing."
                ),
            },
            {
                "id": "M01.L01.Q12",
                "section_id": "retrieval-app",
                "question": (
                    "What should determine the dimension passed to a FAISS index in "
                    "the SigLIP retrieval application?"
                ),
                "options": [
                    "The number of dataset rows",
                    "The text-query length",
                    "The actual embedding dimension produced by the model",
                    "The number of image files on disk",
                ],
                "correct": 2,
                "explanation": (
                    "FAISS vectors must match the index dimensionality exactly, so "
                    "the safest choice is to inspect the model's real embedding shape."
                ),
            },
            {
                "id": "M01.L01.Q13",
                "section_id": "full-mental-model",
                "type": "open",
                "question": (
                    "Explain the complete path from an input image to a generated "
                    "natural-language answer in a modern VLM. Name the major components "
                    "and describe the role of each."
                ),
            },
        ],

        "passing_score": 70,
    },
}
