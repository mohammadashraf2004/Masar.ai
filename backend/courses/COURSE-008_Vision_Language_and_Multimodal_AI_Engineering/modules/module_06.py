"""M01.L06 — Core Architectures of Vision-Language Models.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 6, "Core Architectures of Vision Language Models".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L06"
MODULE_ORDER = 1
MODULE_TITLE = "Foundations of Vision and Language"
MODULE_DESCRIPTION = (
    "Understand the architectural core of modern VLMs: scaled dot-product "
    "attention, self-attention, cross-attention, perceiver resampling, gated "
    "visual adapters, unified visual-text token sequences, fusion strategies, "
    "and the encoder-decoder pattern."
)
SOURCE_CHAPTER = 6
SOURCE_PAGES = "Chapter 6 — page numbers not provided"


TOPIC = {
    "title": "Core Architectures of Vision-Language Models",
    "slug": "vision-language-m01-l06",
    "description": (
        "Learn how visual and textual information are connected inside modern "
        "VLMs. Build intuition for Q/K/V attention, compare self-attention and "
        "cross-attention, study Flamingo-style adapters and SmolVLM-style unified "
        "sequences, analyze frozen versus trainable backbones, and place modern "
        "designs on the early/intermediate/late fusion spectrum."
    ),
    "order": 6,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 4.5,
    "skill_tags": [
        "vlm-architecture",
        "attention",
        "self-attention",
        "cross-attention",
        "query-key-value",
        "perceiver-resampler",
        "gated-cross-attention",
        "unified-sequence-vlm",
        "visual-tokens",
        "modality-projector",
        "early-fusion",
        "intermediate-fusion",
        "late-fusion",
        "encoder-decoder",
        "flamingo",
        "smolvlm",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
    ],

    "lesson": {
        "title": "Core Architectures of Vision-Language Models",
        "content": r"""
# Core Architectures of Vision-Language Models

> **Lesson:** M01.L06  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 6, *Core Architectures of Vision Language Models*.  
> Page numbers were not included in the supplied source.  
> This lesson is an instructor-authored educational adaptation.

---

## Why architecture matters

By this point, you already know that a VLM can:

- encode an image;
- process text;
- generate language;
- learn from multimodal training data.

The architectural question is more specific:

> **How should the visual information enter the language model?**

Modern VLMs often begin with two strong pretrained components:

```text
vision encoder
+
language model
```

The difficult part is the bridge between them.

This chapter focuses on two dominant design patterns:

```text
1. CROSS-ATTENTION ADAPTER
   vision encoder
        ↓
   compressed visual tokens
        ↓
   dedicated cross-attention layers
        ↓
   language model

2. UNIFIED SEQUENCE
   vision encoder
        ↓
   linear projection
        ↓
   visual tokens inserted beside text tokens
        ↓
   ordinary LLM self-attention
```

To understand why these architectures work, we first need to understand
attention itself.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the roles of query, key, and value vectors.
- Derive the high-level steps of scaled dot-product attention.
- Explain why the dot product is scaled before softmax.
- Interpret an attention matrix row as a probability distribution over keys.
- Distinguish self-attention from cross-attention.
- Explain how one sequence can attend internally with self-attention.
- Explain how text queries can retrieve information from visual keys and values.
- Describe how cross-attention can also compress a large visual sequence.
- Explain why modern VLMs commonly reuse pretrained vision encoders and LLMs.
- Describe the Flamingo-style adapter architecture.
- Explain how a perceiver resampler turns many image tokens into a fixed number of visual tokens.
- Explain why zero-initialized gates protect a pretrained LLM at the beginning of adapter training.
- Describe the SmolVLM-style unified sequence architecture.
- Explain why a modality projector is needed.
- Explain how image-placeholder embeddings are replaced with projected visual tokens.
- Compare architectural complexity between interleaved cross-attention and a unified sequence.
- Explain why visual-token compression matters for attention cost.
- Interpret the source's frozen-backbone versus fine-tuned-backbone comparison.
- Explain why token-budget mismatches can make architecture comparisons unfair.
- Distinguish early, intermediate, and late fusion.
- Explain the classic encoder-decoder VLM pattern.
- Compare Show and Tell, Flamingo, and SmolVLM conceptually.
- Choose an architecture based on backbone freezing, simplicity, modularity, and compute constraints.

---

## 1. Attention: deciding what matters

Imagine the sentence:

```text
"The AI community building the future."
```

When processing the word:

```text
AI
```

not every other word is equally useful.

The model might care more about:

```text
community
future
```

than about:

```text
the
```

Attention gives the model a learnable mechanism for deciding:

> Which other elements should influence the representation of this element?

The same idea works for:

- words attending to words;
- image patches attending to image patches;
- text attending to image regions;
- visual and textual tokens attending in one combined sequence.

[[IMAGE_NEEDED: Attention intuition |
Show the words in "The AI community building the future" with stronger arrows
from AI to future and community and weaker arrows to less relevant words |
Learner should see attention as weighted information gathering rather than a
hard one-to-one lookup]]

---

## 2. Query, Key, and Value

Every sequence element is transformed into three learned vectors.

### Query — Q

Think:

```text
"What information am I looking for?"
```

### Key — K

Think:

```text
"What kind of information do I contain?"
```

### Value — V

Think:

```text
"What information should I contribute if selected?"
```

If the input embedding matrix is:

```text
X
```

then learned matrices produce:

```text
Q = XW_q
K = XW_k
V = XW_v
```

The source emphasizes that every word or image patch can produce its own:

- query;
- key;
- value.

For a six-token sequence, you therefore get:

```text
6 queries
6 keys
6 values
```

### A useful mental model

For one token:

```text
query
  ↓
compare against all keys
  ↓
produce relevance scores
  ↓
use scores to mix all values
  ↓
new contextual representation
```

---

## 3. Scaled dot-product attention step by step

The chapter's code implements standard scaled dot-product attention.

The full operation is:

```text
Attention(Q, K, V)
=
softmax(QKᵀ / √d_k) V
```

where:

```text
d_k = key/query feature dimension
```

Let's unpack it.

### Step 1 — Compare queries and keys

Compute:

```text
QKᵀ
```

If the sequence contains 6 elements, this produces:

```text
6 × 6
```

scores.

Each row answers:

> For this query, how relevant is every key?

### Step 2 — Scale

The code divides by:

```text
√d_k
```

Conceptually:

```python
scale = K.size(-1) ** 0.5
scores = Q @ K.transpose(-2, -1) / scale
```

Why scale?

As vector dimensionality grows, raw dot products can become large.

Large logits can make softmax extremely sharp.

Scaling keeps the score magnitudes more manageable before softmax.

### Step 3 — Softmax

Apply:

```python
weights = torch.softmax(
    scores,
    dim=-1,
)
```

Each query row becomes a distribution over keys.

For example:

```text
AI query:

The        0.00
AI         0.60
community  0.10
building   0.00
the        0.00
future     0.30
```

The weights add to:

```text
1.0
```

### Step 4 — Mix the values

Finally:

```text
weights × V
```

creates the new representation.

For intuition:

```text
new AI representation
≈
0.60 × AI value
+
0.10 × community value
+
0.30 × future value
```

This is how an element absorbs context from other elements.

[[IMAGE_NEEDED: Scaled dot-product attention pipeline |
Show Q and K multiplied to form score matrix, divide by sqrt(d_k), softmax to
attention weights, then multiply by V to produce contextualized outputs |
Learner should connect the formula to the four conceptual steps]]

{{exercise:M01.L06.EX01}}

---

## 4. Reading an attention matrix

The source presents an example matrix for six words.

Interpretation:

```text
rows    = queries
columns = keys
```

So if:

```text
row = AI
column = future
weight = 0.30
```

then the current `AI` representation is receiving a meaningful contribution
from the `future` value vector.

### Diagonal weights

The source's example gives many words large self-attention weights.

That means the token keeps a strong contribution from its own content.

### Off-diagonal weights

The interesting relationships are often off the diagonal.

Those show contextual dependencies such as:

```text
AI → future
community → building
future → AI
```

### Important caution

An attention matrix is useful for understanding computation, but one individual
head or layer should not automatically be treated as a complete explanation of
a model's reasoning.

For this lesson, use it as:

```text
a weighted interaction matrix
```

not as a perfect causal explanation.

---

## 5. Self-attention: one sequence talks to itself

In self-attention:

```text
Q comes from sequence X
K comes from sequence X
V comes from sequence X
```

The source provides:

```python
def self_attention(
    x,
    W_q,
    W_k,
    W_v,
):
    Q = x @ W_q
    K = x @ W_k
    V = x @ W_v

    scale = K.size(-1) ** 0.5

    scores = (
        Q @ K.transpose(-2, -1)
        / scale
    )

    weights = torch.softmax(
        scores,
        dim=-1,
    )

    return weights @ V
```

This mechanism is central to:

- text transformers;
- Vision Transformers;
- unified-sequence VLMs.

### Why self-attention can become multimodal

Suppose one sequence contains:

```text
[image_1]
[image_2]
[image_3]
[text_1]
[text_2]
[text_3]
```

Self-attention does not inherently care whether an embedding came from:

- an image patch;
- a word.

If they exist in a compatible embedding space, the attention mechanism can
learn cross-modal relationships inside that one sequence.

This is the central idea behind the unified-sequence architecture later in the
lesson.

---

## 6. Cross-attention: one sequence asks another

Cross-attention changes only one key idea:

```text
queries come from one sequence
keys and values come from another
```

For example:

```text
Q = text features
K = image features
V = image features
```

Source-aligned code:

```python
def cross_attention(
    text_features,
    image_features,
    W_q,
    W_k,
    W_v,
):
    Q = text_features @ W_q
    K = image_features @ W_k
    V = image_features @ W_v

    scale = K.size(-1) ** 0.5

    scores = (
        Q @ K.transpose(-2, -1)
        / scale
    )

    weights = torch.softmax(
        scores,
        dim=-1,
    )

    return weights @ V
```

### The "interview" intuition

Text asks:

```text
"Which visual information do I need?"
```

Image features answer through their keys and values.

Example:

```text
text query:
"What color is the car?"

cross-attention:
focus strongly on visual tokens representing the car
```

[[IMAGE_NEEDED: Self-attention versus cross-attention |
Left: one mixed sequence generates Q/K/V internally.
Right: text generates Q while image features generate K and V |
Learner should see the exact source difference between the two attention types]]

---

## 7. Cross-attention can also compress information

A useful property is:

```text
number of queries
does not need to equal
number of keys/values
```

Suppose the vision encoder outputs:

```text
256 image tokens
```

We can create:

```text
64 learned queries
```

and let them attend over all 256 visual tokens.

The result is:

```text
64 output visual tokens
```

So cross-attention performs two jobs:

```text
1. retrieve useful visual information
2. compress a long visual sequence
```

This leads directly to the Flamingo-style perceiver resampler.

---

## 8. The modern VLM blueprint

The chapter emphasizes a major practical shift.

Instead of training one giant vision-language network from scratch, use:

```text
powerful pretrained vision encoder
+
powerful pretrained LLM
```

and teach them to communicate.

Why?

The vision encoder already knows useful visual structure.

The LLM already knows useful language structure.

The new architectural question becomes:

> How should we connect them?

The source presents two major answers.

### Architecture A

```text
Adapter / cross-attention approach
```

### Architecture B

```text
Unified sequence / self-attention approach
```

---

## 9. Flamingo-style adapter architecture

The adapter-style design keeps major pretrained components frozen.

A simplified flow is:

```text
IMAGE
  ↓
frozen vision encoder
  ↓
perceiver resampler
  ↓
compact visual tokens
  ↓
gated cross-attention blocks
  ↓
frozen LLM layers
  ↓
text output
```

The source highlights two important trainable components:

```text
1. perceiver resampler
2. gated cross-attention layers
```

The goal is to add visual capability without heavily modifying the pretrained
language model.

{{image:flamingo-architecture}}

---

## 10. Perceiver resampler: fixed-size visual summary

Suppose a vision encoder produces one token per patch.

The source example:

```text
image = 256 × 256
patch = 16 × 16

patch grid:
16 × 16

visual tokens:
256
```

Sending all 256 tokens into repeated cross-attention layers is expensive.

The perceiver resampler uses a fixed set of learned queries.

Example:

```text
64 learned queries
```

Each query attends over all 256 vision features.

Result:

```text
256 visual features
       ↓
cross-attention
       ↓
64 compact visual tokens
```

### Source-aligned implementation

```python
class PerceiverResampler(nn.Module):
    def __init__(
        self,
        num_queries=64,
        vision_dim=768,
        llm_dim=576,
        num_heads=8,
    ):
        super().__init__()

        self.learned_queries = nn.Parameter(
            torch.randn(
                1,
                num_queries,
                vision_dim,
            )
        )

        self.cross_attn = nn.MultiheadAttention(
            embed_dim=vision_dim,
            num_heads=num_heads,
            batch_first=True,
        )

        self.proj = nn.Linear(
            vision_dim,
            llm_dim,
        )

    def forward(
        self,
        vision_features,
    ):
        batch_size = vision_features.size(0)

        queries = self.learned_queries.expand(
            batch_size,
            -1,
            -1,
        )

        summary, _ = self.cross_attn(
            query=queries,
            key=vision_features,
            value=vision_features,
        )

        return self.proj(summary)
```

### Why fixed query count is useful

The output length can remain:

```text
64
```

even if the raw visual sequence is much longer.

That gives the LLM a predictable visual interface.

### Compression trade-off

Compression saves compute.

But the compact tokens must preserve the visual information required by the
task.

More compression is not automatically better.

{{exercise:M01.L06.EX02}}

---

## 11. Gated cross-attention: inject vision gradually

After obtaining compact visual tokens, the LLM needs to use them.

At a cross-attention layer:

```text
Q = current LLM hidden states
K = compact image tokens
V = compact image tokens
```

This lets the current text state retrieve relevant visual content.

### Why a gate?

New cross-attention layers begin with random weights.

If they immediately inject strong random activations into a pretrained LLM,
they can disrupt its useful language representations.

The source uses learned gates initialized to zero.

Conceptually:

```text
text_hidden
+
gate × visual_cross_attention
```

At initialization:

```text
gate ≈ 0
```

so:

```text
output ≈ original text_hidden
```

As training progresses, the model learns to open the gate.

### Source-aligned layer

```python
class GatedCrossAttentionLayer(nn.Module):
    def __init__(
        self,
        hidden_dim,
        num_heads=8,
    ):
        super().__init__()

        self.attn_norm = nn.LayerNorm(
            hidden_dim
        )

        self.ffn_norm = nn.LayerNorm(
            hidden_dim
        )

        self.cross_attn = nn.MultiheadAttention(
            embed_dim=hidden_dim,
            num_heads=num_heads,
            batch_first=True,
        )

        self.ffn = nn.Sequential(
            nn.Linear(
                hidden_dim,
                hidden_dim * 4,
            ),
            nn.GELU(),
            nn.Linear(
                hidden_dim * 4,
                hidden_dim,
            ),
        )

        self.attn_gate = nn.Parameter(
            torch.zeros(1)
        )

        self.ffn_gate = nn.Parameter(
            torch.zeros(1)
        )

    def forward(
        self,
        text_hidden,
        image_features,
    ):
        attn_in = self.attn_norm(
            text_hidden
        )

        attn_out, _ = self.cross_attn(
            query=attn_in,
            key=image_features,
            value=image_features,
        )

        text_hidden = (
            text_hidden
            + self.attn_gate.tanh()
            * attn_out
        )

        ffn_in = self.ffn_norm(
            text_hidden
        )

        ffn_out = self.ffn(
            ffn_in
        )

        text_hidden = (
            text_hidden
            + self.ffn_gate.tanh()
            * ffn_out
        )

        return text_hidden
```

{{image:gated-cross-attention}}

---

## 12. Unified sequence: make images look like tokens

The second architecture asks:

> What if image features simply become part of the LLM input sequence?

The pipeline is:

```text
image
  ↓
vision encoder
  ↓
visual embeddings
  ↓
modality projector
  ↓
LLM-sized visual tokens

text
  ↓
token embedding layer
  ↓
text tokens

then:

[visual tokens][text tokens]
        ↓
ordinary LLM self-attention
```

There is no dedicated cross-attention adapter.

The LLM's existing self-attention performs the fusion.

### Why a projection layer is needed

If the vision encoder produces:

```text
768-dimensional vectors
```

but the LLM expects:

```text
576-dimensional embeddings
```

the visual tokens must be projected:

```text
768 → 576
```

Then both modalities can exist inside the same sequence.

{{image:smolvlm-unified-sequence}}

---

## 13. Unified-sequence implementation

The source provides a compact design.

A source-aligned educational version:

```python
class UnifiedSequenceVLM(nn.Module):
    def __init__(
        self,
        vision_encoder_ckpt,
        language_model_ckpt,
        tokenizer,
        modality_input_dim=768,
        modality_output_dim=576,
    ):
        super().__init__()

        self.vision_encoder = (
            AutoModel
            .from_pretrained(
                vision_encoder_ckpt
            )
            .vision_model
        )

        self.modality_projector = nn.Linear(
            modality_input_dim,
            modality_output_dim,
            bias=False,
        )

        self.tokenizer = tokenizer

        self.llm = (
            AutoModelForCausalLM
            .from_pretrained(
                language_model_ckpt
            )
        )

        self.llm.resize_token_embeddings(
            len(self.tokenizer)
        )

    def forward(
        self,
        input_ids,
        pixel_values,
    ):
        image_embd = self.vision_encoder(
            pixel_values
        ).last_hidden_state

        image_tokens = self.modality_projector(
            image_embd
        )

        token_embd = self.llm.model.embed_tokens(
            input_ids
        )

        mask = (
            input_ids
            == self.tokenizer.image_token_id
        )

        token_embd[mask] = image_tokens.view(
            -1,
            image_tokens.size(-1),
        )

        return self.llm(
            inputs_embeds=token_embd
        ).logits
```

### The elegant part

The bridge is nearly just:

```text
linear projection
+
placeholder replacement
```

After that:

```text
self.llm(inputs_embeds=...)
```

handles the rest.

### Critical requirement

As learned previously:

```text
number of image placeholders
=
number of projected visual tokens
```

must hold for direct mask replacement.

---

## 14. Unified architectures still need visual-token compression

A simple unified sequence can become very long.

High-resolution images may produce hundreds or thousands of visual tokens.

Because LLM self-attention becomes expensive as sequence length grows, modern
systems often compress visual tokens.

The source points back to **pixel shuffle**.

Conceptually:

```text
many spatial positions
      ↓
rearrange spatial information into channels
      ↓
fewer visual token positions
      ↓
linear projection
      ↓
LLM
```

So both major architectures need a token-budget solution:

```text
cross-attention approach
→ perceiver resampling

unified sequence approach
→ pixel shuffle / pooling / other compression
```

The mechanisms differ, but the engineering problem is the same:

> Visual information can overwhelm the LLM sequence if left uncompressed.

---

## 15. Cross-attention versus unified self-attention

The source compares the two designs conceptually and empirically.

### Cross-attention adapter

Strengths:

- strong when major backbones remain frozen;
- preserves pretrained language behavior cleanly;
- provides dedicated visual fusion layers;
- perceiver gives fixed-size visual interface.

Costs:

- more trainable fusion parameters;
- more complex forward pass;
- explicit layer-by-layer interleaving;
- must manage masks/positions/cache carefully.

### Unified sequence

Strengths:

- simple architecture;
- fewer new fusion parameters;
- uses ordinary LLM self-attention;
- much simpler forward integration.

Costs:

- often benefits from allowing backbones to adapt;
- long visual sequences directly increase LLM attention cost;
- fine-tuning can risk forgetting if training is poorly managed.

### Architecture is not the only variable

The source makes a particularly important point:

```text
data
learning rate
batch size
token budget
training duration
backbone trainability
```

may matter as much as or more than the exact fusion architecture.

---

## 16. Frozen versus trainable backbones

The source reports a comparison using the same major backbone choices.

### Frozen backbones

Reported benchmark average:

```text
cross-attention: 66.7
self-attention:  60.3
```

Interpretation:

When the LLM and vision encoder cannot adapt, dedicated fusion layers have to
carry more responsibility.

The extra cross-attention machinery is useful.

### Fine-tuned/adapted backbones

Reported:

```text
self-attention:  69.5
cross-attention: 67.3
```

The chapter describes the backbone adaptation as using LoRA in that referenced
study.

Interpretation:

Once the pretrained models can adapt to the multimodal task, the simpler unified
sequence can become highly competitive.

### Do not turn this into a universal law

These numbers belong to the experimental setting described in the source.

They demonstrate:

```text
architecture × training strategy
```

interaction.

They do not prove one architecture always wins.

{{exercise:M01.L06.EX03}}

---

## 17. Side-by-side small-model comparison

The chapter also compares both approaches using small backbones.

The source gives parameter counts:

```text
Unified sequence:
227,888,256 trainable parameters

Cross-attention:
262,192,336 trainable parameters
```

Difference:

```text
≈ 34 million additional parameters
≈ 15% more
```

Those extra parameters come from:

- perceiver resampler;
- gated cross-attention layers.

### Initial loss comparison

Both architectures were trained on the same data slice.

The source reports:

```text
very similar loss curves
```

with cross-attention slightly lower initially.

But this comparison had an important confound.

---

## 18. Fair experiments require matching token budgets

The first comparison used different effective input composition.

The source explains that the cross-attention model used far fewer placeholder
image tokens:

```text
1 instead of 256
```

So its packed sequences contained more text tokens.

That means:

```text
more text training signal per step
```

The comparison was therefore not perfectly controlled.

After matching the token/data budget, the source reports that the loss
difference nearly disappeared.

### The general lesson

When comparing VLM architectures, control:

- training samples;
- total tokens;
- image-token budget;
- text-token budget;
- optimization settings;
- trainable parameters/backbones;
- number of steps.

Otherwise, you may attribute a data-budget advantage to the architecture.

[[IMAGE_NEEDED: Fair VLM architecture comparison |
Show two architectures receiving equal total token budgets, equal image/text
content, same optimizer and training steps, contrasting with an unfair setup
where one model receives more text tokens |
Learner should understand why matched training input is necessary for causal
comparison]]

---

## 19. Why language-model loss may hide visual differences

The source makes a subtle observation.

In multimodal sequences, many language tokens can be predicted largely from:

- language structure;
- question wording;
- previous generated words.

Example answer:

```text
"In this image, we can see a monkey eating a banana."
```

The source argues that only some tokens strongly depend on the image, such as:

```text
monkey
eating
```

while much of the sentence is linguistically predictable.

Therefore, total language-model loss can be dominated by text behavior.

### Consequence

Two VLM architectures can have nearly identical total loss while differing in:

- grounding;
- fine visual recognition;
- OCR;
- spatial reasoning.

So architecture evaluation should include downstream multimodal tasks, not only
training loss.

---

## 20. Why cross-attention integration is harder to engineer

The source gives pseudocode that manually iterates through LLM layers.

A cleaned conceptual version is:

```python
class CrossAttentionVLM(nn.Module):
    def __init__(
        self,
        vision_encoder_ckpt,
        language_model_ckpt,
        cross_attn_layers,
    ):
        super().__init__()

        self.vision_encoder = (
            AutoModel
            .from_pretrained(
                vision_encoder_ckpt
            )
            .vision_model
        )

        self.llm = (
            AutoModelForCausalLM
            .from_pretrained(
                language_model_ckpt
            )
        )

        self.resampler = PerceiverResampler()

        hidden_dim = self.llm.config.hidden_size

        self.cross_attn_blocks = nn.ModuleDict(
            {
                str(layer_idx):
                GatedCrossAttentionLayer(
                    hidden_dim=hidden_dim
                )
                for layer_idx
                in cross_attn_layers
            }
        )

    def forward(
        self,
        input_ids,
        images,
        labels=None,
    ):
        visual_tokens = self.encode_images(
            images
        )

        hidden = self.llm.model.embed_tokens(
            input_ids
        )

        for layer_idx, decoder_layer in enumerate(
            self.llm.model.layers
        ):
            if str(layer_idx) in self.cross_attn_blocks:
                hidden = self.cross_attn_blocks[
                    str(layer_idx)
                ](
                    text_hidden=hidden,
                    image_features=visual_tokens,
                )

            hidden = decoder_layer(
                hidden
            )[0]

        logits = self.llm.lm_head(
            hidden
        )

        return logits
```

### Important source note

The original chapter labels this section as pseudocode.

It explicitly states that a full implementation must also manage:

- causal masks;
- positional embeddings / rotary position logic;
- KV-cache updates.

The supplied snippet also refers to:

```text
llm.config.hidden_size
```

inside a class that stores:

```text
self.llm
```

The instructional version above normalizes that mechanical reference to:

```text
self.llm.config.hidden_size
```

The conceptual architecture remains unchanged.

### Engineering contrast

Cross-attention adapter:

```text
manually walk layers
inject vision at chosen depths
manage decoder state details
```

Unified sequence:

```text
prepare combined embeddings
call LLM once
```

That simplicity is a major practical design advantage.

---

## 21. Fusion is a spectrum

The chapter broadens the architecture discussion into three categories:

```text
early fusion
intermediate fusion
late fusion
```

The question is:

> At what stage should modalities begin interacting?

---

## 22. Early fusion

Early fusion combines modalities before or near the beginning of joint
reasoning.

Conceptually:

```text
vision features ─┐
                 ├→ combined representation → joint model
text features ───┘
```

Advantages:

- deep cross-modal interactions;
- one shared representation;
- subtle relationships can be learned early.

Costs:

- larger combined representation;
- more coupled components;
- reduced modularity.

The source maps the unified sequence / SmolVLM-style approach to early fusion.

```text
visual tokens + text tokens
        ↓
joint self-attention
```

---

## 23. Intermediate fusion

The source positions Flamingo-style cross-attention as **intermediate fusion**.

Why?

The modalities begin separately:

```text
image → vision encoder
text  → language model
```

but exchange information repeatedly inside the network:

```text
LLM layer
↓
cross-attention
↓
LLM layer
↓
cross-attention
...
```

This gives richer interaction than classical late fusion without combining
everything into one sequence at the very beginning.

---

## 24. Late fusion

Late fusion keeps modalities separate until high-level decisions are available.

Example:

```text
vision model
→ "angry gesture: 0.86"

text model
→ "abusive language: 0.91"

then:
combine both scores
→ toxicity decision
```

Advantages:

- modular;
- easy to replace one specialist;
- easy to add additional signals.

Weakness:

- detailed cross-modal information may be lost before the final combination.

For example, if a vision model compresses a frame into one label:

```text
"person"
```

the later text system cannot recover visual details that were discarded.

{{image:early-fusion-classifier}}

{{exercise:M01.L06.EX04}}

---

## 25. The encoder-decoder skeleton

Fusion asks:

```text
when do modalities interact?
```

A different architectural question is:

```text
what is the overall model shape?
```

One influential VLM pattern is:

```text
image encoder
    ↓
visual representation
    ↓
text decoder
    ↓
generated caption/answer
```

The encoder is the:

```text
reader
```

The decoder is the:

```text
writer
```

This pattern existed before modern transformer VLMs.

---

## 26. Show and Tell: the single-vector bottleneck

The source uses a classic image-captioning design.

Conceptually:

```text
image
  ↓
ResNet CNN
  ↓
one vector
  ↓
LSTM initial hidden state
  ↓
caption generation
```

A source-aligned skeleton:

```python
class ShowAndTell(nn.Module):
    def __init__(
        self,
        embed_dim=256,
        hidden_dim=512,
        vocab_size=10000,
    ):
        super().__init__()

        cnn = torchvision.models.resnet50(
            weights=(
                torchvision.models
                .ResNet50_Weights
                .DEFAULT
            )
        )

        self.cnn = nn.Sequential(
            *list(cnn.children())[:-1]
        )

        self.img_proj = nn.Linear(
            2048,
            hidden_dim,
        )

        self.embedding = nn.Embedding(
            vocab_size,
            embed_dim,
        )

        self.lstm = nn.LSTM(
            embed_dim,
            hidden_dim,
            batch_first=True,
        )

        self.output_proj = nn.Linear(
            hidden_dim,
            vocab_size,
        )

    def forward(
        self,
        image,
        captions,
    ):
        feats = self.cnn(
            image
        ).flatten(1)

        h0 = self.img_proj(
            feats
        ).unsqueeze(0)

        c0 = torch.zeros_like(
            h0
        )

        caption_embd = self.embedding(
            captions
        )

        hidden, _ = self.lstm(
            caption_embd,
            (h0, c0),
        )

        return self.output_proj(
            hidden
        )
```

### The bottleneck

The entire image becomes:

```text
one vector
```

The decoder cannot dynamically look back at specific image regions.

Modern attention-based VLMs improve this by keeping many visual tokens.

{{image:vlm-architecture-comparison}}

---

## 27. Comparing three generations of VLM architecture

The source compares the designs roughly as follows.

| Property | Show and Tell | Flamingo-style | SmolVLM-style |
|---|---|---|---|
| Vision encoder | ResNet CNN | SigLIP-like ViT | SigLIP-like ViT |
| Visual representation | 1 vector | fixed compact tokens (e.g. 64) | many projected visual tokens |
| Decoder | LSTM | frozen LLM + gated cross-attention | LLM self-attention |
| Visual injection | initial hidden state | selected cross-attention layers | embedded directly into sequence |
| Fusion | late-ish | intermediate | early |
| Main bottleneck | single visual vector | fusion-layer complexity | sequence length |

The progression is clear:

```text
one image vector
      ↓
multiple compact visual tokens
      ↓
rich visual token sequence
```

The broad encoder-decoder skeleton survives.

What changes is the **connection**.

---

## 28. How to choose an architecture

There is no architecture that is best for every setting.

Start from your constraints.

### If the LLM must remain frozen

A dedicated cross-attention adapter can be attractive.

It lets the model gain visual access while protecting the language backbone.

### If the backbones can adapt

A unified sequence may offer:

- fewer new parameters;
- simpler implementation;
- competitive behavior in the source's comparison.

### If modularity is the top priority

Late fusion may be appropriate.

Separate models can be replaced independently.

### If deep cross-modal interaction is essential

Early or intermediate fusion is usually more appropriate.

### If visual tokens are very numerous

Plan for compression:

```text
perceiver resampler
pixel shuffle
pooling
or another token-reduction strategy
```

### If engineering simplicity matters

Do not underestimate implementation complexity.

A theoretically elegant architecture that is hard to:

- train;
- cache;
- batch;
- deploy;
- debug;

can be a worse practical choice than a simpler design with similar quality.

---

## 29. A checklist for reading any VLM architecture paper

When you encounter a new model, ask:

### Vision side

- Which vision encoder?
- Frozen or trainable?
- How many visual tokens?
- Is there spatial compression?

### Language side

- Which LLM?
- Frozen or trainable?
- Full fine-tune, LoRA, or another adaptation method?

### Bridge

- Linear projector?
- Cross-attention?
- Resampler?
- Query tokens?
- Gating?

### Fusion

- Early?
- Intermediate?
- Late?

### Sequence budget

- How many image tokens enter the LLM?
- How is high resolution handled?
- Is the token budget controlled across comparisons?

### Training

- What data?
- How many steps?
- Which components receive gradients?
- Is loss mainly language-model loss?
- Are downstream visual benchmarks also evaluated?

### Inference

- How are causal masks handled?
- How are positions represented?
- Is KV caching supported?
- What is the generation-time memory cost?

This checklist turns an architecture diagram into an engineering analysis.

{{exercise:M01.L06.EX05}}

---

## 30. The complete architectural mental model

The whole chapter can be summarized as:

```text
RAW IMAGE
    ↓
VISION ENCODER
    ↓
VISUAL TOKENS
    ↓
(optional compression)
    ↓
HOW SHOULD VISION ENTER LANGUAGE?

OPTION A — CROSS-ATTENTION
visual tokens
    ↓
perceiver
    ↓
fixed compact set
    ↓
gated cross-attention
    ↕
LLM hidden states

OPTION B — UNIFIED SEQUENCE
visual tokens
    ↓
linear projection
    ↓
replace image placeholders
    ↓
[visual + text embeddings]
    ↓
LLM self-attention

THEN:
autoregressive text generation
```

The deeper insight is:

> A modern VLM is often not defined by a brand-new vision model or a brand-new
> language model. Its identity comes from how existing powerful components are
> connected, compressed, trained, and allowed to interact.

{{exercise:M01.L06.EX06}}

---

## Important misconceptions

### Misconception 1: "Attention simply chooses one token."

No.

Attention creates a weighted mixture over values.

### Misconception 2: "Q, K, and V are fixed hand-designed features."

They are produced through learned projections.

### Misconception 3: "Self-attention can only operate within one modality."

If image and text embeddings are placed in one compatible sequence,
self-attention can model cross-modal interactions.

### Misconception 4: "Cross-attention requires equal text and image sequence lengths."

No.

Query length and key/value length can differ.

This is exactly why learned queries can compress visual features.

### Misconception 5: "A perceiver resampler is only a modality bridge."

It also acts as a sequence compressor.

### Misconception 6: "Zero-initialized cross-attention gates mean vision is permanently ignored."

No.

They initially protect the pretrained LLM, then become learnable.

### Misconception 7: "Unified sequence means no visual encoder is needed."

The image still needs to be encoded.

The unified part refers to how projected visual and text tokens enter the LLM.

### Misconception 8: "Architecture comparison is fair if the model names differ but the dataset is the same."

Not necessarily.

Token budgets, number of trainable parameters, backbone freezing, and optimizer
settings must also be controlled.

### Misconception 9: "Lower multimodal language-model loss proves better visual understanding."

Not always.

Much of the loss may be predictable from language context without requiring
visual evidence.

### Misconception 10: "Early fusion is always superior to late fusion."

No.

Early fusion improves cross-modal interaction but reduces modularity.

Late fusion preserves modularity but can discard useful fine-grained relations.

### Misconception 11: "Modern VLMs abandoned encoder-decoder architecture."

No.

The reader/writer skeleton remains influential.

The visual-to-language connection has become much richer.

### Misconception 12: "Cross-attention pseudocode can be copied directly into a production decoder."

Not from the supplied example.

The source explicitly omits important implementation details such as causal
masks, position handling, and KV-cache management.

---

## Key terminology

| Term | Meaning |
|---|---|
| Attention | Weighted information aggregation between sequence elements |
| Query (Q) | Vector representing what an element is looking for |
| Key (K) | Vector used to determine relevance to a query |
| Value (V) | Information vector mixed according to attention weights |
| Scaled dot-product attention | softmax(QKᵀ/√d_k)V |
| Attention matrix | Matrix of query-to-key relevance weights |
| Self-attention | Q, K, V originate from the same sequence |
| Cross-attention | Queries and key/value features originate from different streams |
| Visual token | Encoded representation of a visual region/patch |
| Modality projector | Layer mapping visual feature dimension to LLM embedding dimension |
| Perceiver resampler | Learned-query cross-attention module compressing visual features |
| Gated cross-attention | Visual fusion layer whose influence is controlled by learned gates |
| Unified sequence | Architecture placing projected image and text embeddings into one LLM sequence |
| Image placeholder | Token position reserved for a projected visual embedding |
| Frozen backbone | Pretrained component whose parameters are not updated |
| Trainable backbone | Pretrained component allowed to adapt during multimodal training |
| Early fusion | Modalities interact near the beginning of joint processing |
| Intermediate fusion | Modalities interact at selected internal layers |
| Late fusion | Separate modality outputs are combined near the end |
| Encoder-decoder | Pattern where one network encodes input and another generates output |
| Single-vector bottleneck | Compressing an entire image into one vector before decoding |
| Token budget | Amount of model context occupied by image and text representations |
| KV cache | Cached attention keys/values used during autoregressive inference |

---

## Self-check

Before moving on, make sure you can answer:

1. What problem does attention solve?
2. What does a query represent?
3. What does a key represent?
4. What does a value represent?
5. What shape is the attention score matrix for a sequence of six elements?
6. Why are scores divided by √d_k?
7. What does softmax do to one row of the score matrix?
8. How is the new representation computed from attention weights and values?
9. What makes self-attention "self"?
10. What makes cross-attention "cross"?
11. Why can cross-attention use different query and key sequence lengths?
12. How can cross-attention perform compression?
13. Why reuse pretrained vision encoders and LLMs?
14. What does a perceiver resampler do?
15. Why does Flamingo-style architecture use learned visual queries?
16. Why initialize fusion gates at zero?
17. What is the modality projector's job?
18. How does a unified sequence let visual and text information interact?
19. Why must image-placeholder count match visual-token count?
20. Why do high-resolution images create an LLM sequence problem?
21. How does pixel shuffle address that problem?
22. Why did cross-attention perform better in the source's frozen-backbone setting?
23. Why can unified self-attention become competitive when backbones adapt?
24. Why was the source's first small-model architecture comparison not perfectly controlled?
25. Why can total language-model loss hide grounding differences?
26. What additional implementation work does interleaved cross-attention require?
27. What is early fusion?
28. What is intermediate fusion?
29. What is late fusion?
30. Which fusion style is most modular?
31. What is the main limitation of the Show-and-Tell single-vector approach?
32. How did modern VLMs make the encoder-decoder bridge richer?
33. Which architecture questions should you ask when reading a new VLM paper?
34. Why is architectural simplicity itself an engineering advantage?

---

## Retain this idea

**Modern VLM design is fundamentally about the bridge between strong pretrained
vision and language components. Cross-attention creates explicit visual access
through dedicated fusion layers; unified-sequence models project visual features
into the LLM's token space and reuse self-attention. The best design depends not
only on architecture, but also on which backbones can adapt, how visual tokens
are compressed, how training is controlled, and how much implementation
complexity you can justify.**
""",

        "estimated_minutes": 270,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "attention-intuition", "title": "Attention intuition", "order": 1},
            {"id": "qkv", "title": "Query, Key, and Value", "order": 2},
            {"id": "attention-math", "title": "Scaled dot-product attention", "order": 3},
            {"id": "attention-matrix", "title": "Reading an attention matrix", "order": 4},
            {"id": "self-attention", "title": "Self-attention", "order": 5},
            {"id": "cross-attention", "title": "Cross-attention", "order": 6},
            {"id": "cross-attn-compression", "title": "Cross-attention as compression", "order": 7},
            {"id": "modern-blueprint", "title": "The modern VLM blueprint", "order": 8},
            {"id": "flamingo", "title": "Flamingo-style adapter architecture", "order": 9},
            {"id": "perceiver", "title": "Perceiver resampler", "order": 10},
            {"id": "gated-cross-attention", "title": "Gated cross-attention", "order": 11},
            {"id": "unified-sequence", "title": "Unified sequence architecture", "order": 12},
            {"id": "unified-code", "title": "Unified-sequence implementation", "order": 13},
            {"id": "visual-compression", "title": "Visual-token compression", "order": 14},
            {"id": "architecture-comparison", "title": "Architecture comparison", "order": 15},
            {"id": "frozen-vs-trainable", "title": "Frozen versus trainable backbones", "order": 16},
            {"id": "baby-comparison", "title": "Small-model side-by-side comparison", "order": 17},
            {"id": "fair-comparison", "title": "Fair token-budget comparison", "order": 18},
            {"id": "loss-caveat", "title": "Why loss can hide visual differences", "order": 19},
            {"id": "cross-attn-pseudocode", "title": "Cross-attention engineering complexity", "order": 20},
            {"id": "fusion-framework", "title": "Fusion as a spectrum", "order": 21},
            {"id": "early-fusion", "title": "Early fusion", "order": 22},
            {"id": "intermediate-fusion", "title": "Intermediate fusion", "order": 23},
            {"id": "late-fusion", "title": "Late fusion", "order": 24},
            {"id": "encoder-decoder", "title": "Encoder-decoder pattern", "order": 25},
            {"id": "show-and-tell", "title": "Show and Tell", "order": 26},
            {"id": "three-architecture-table", "title": "Three generations of VLM architecture", "order": 27},
            {"id": "architecture-choice", "title": "Choosing an architecture", "order": 28},
            {"id": "architecture-checklist", "title": "Architecture reading checklist", "order": 29},
            {"id": "complete-mental-model", "title": "Complete architectural mental model", "order": 30},
        ],
    },

    "exercises": [
        {
            "id": "M01.L06.EX01",
            "title": "Compute one attention row",
            "lesson_code": "M01.L06",
            "section_id": "attention-math",
            "placement": "after_section",
            "description": (
                "Practice query-key scoring, scaling, softmax intuition, and weighted value mixing."
            ),
            "instructions": (
                "Assume one query has raw dot products [2.0, 1.0, 0.0] against three keys "
                "and d_k=4.\n"
                "1. Divide scores by sqrt(4).\n"
                "2. Compute approximate softmax weights.\n"
                "3. Verify that they sum to 1.\n"
                "4. If scalar values are [10, 20, 30], compute the weighted output.\n"
                "5. Explain which value influenced the output most and why."
            ),
            "expected_output": (
                "A step-by-step scaled score, softmax, and weighted-sum calculation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "attention",
                "softmax",
                "qkv",
                "weighted-sum",
            ],
        },
        {
            "id": "M01.L06.EX02",
            "title": "Design a visual resampler",
            "lesson_code": "M01.L06",
            "section_id": "perceiver",
            "placement": "after_section",
            "description": (
                "Reason about learned queries as both cross-modal access and compression."
            ),
            "instructions": (
                "A vision encoder produces 576 visual tokens, each 768 dimensions.\n"
                "You want to expose only 64 visual tokens to a 1024-dimensional LLM.\n"
                "1. State the number of learned resampler queries.\n"
                "2. Identify Q, K, and V sources.\n"
                "3. State the resampler output sequence length before projection.\n"
                "4. State what the final linear projection must map: 768 → ?\n"
                "5. Explain the compute-versus-information trade-off."
            ),
            "expected_output": (
                "A small architecture diagram plus dimensions and a short compression trade-off."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "cross-attention",
                "perceiver-resampler",
                "visual-compression",
            ],
        },
        {
            "id": "M01.L06.EX03",
            "title": "Choose architecture for frozen and trainable backbones",
            "lesson_code": "M01.L06",
            "section_id": "frozen-vs-trainable",
            "placement": "after_section",
            "description": (
                "Apply the source's architecture comparison to two engineering scenarios."
            ),
            "instructions": (
                ('1. Scenario A: You must keep a strong proprietary LLM frozen and only add new multimodal components.\n'
                 '2. Scenario B: You can LoRA-adapt both the vision encoder and LLM and want the simplest possible architecture.\n'
                 "3. For each scenario, choose cross-attention adapter or unified sequence and justify the decision using the source's findings and engineering trade-offs.")
            ),
            "expected_output": (
                "A two-row decision table covering backbone trainability, likely architecture, "
                "parameter/engineering complexity, and caveats."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "architecture-selection",
                "frozen-backbones",
                "self-attention",
                "cross-attention",
            ],
        },
        {
            "id": "M01.L06.EX04",
            "title": "Classify fusion strategies",
            "lesson_code": "M01.L06",
            "section_id": "late-fusion",
            "placement": "after_section",
            "description": (
                "Distinguish early, intermediate, and late fusion from architecture descriptions."
            ),
            "instructions": (
                ('1. Classify each system:\n'
                 '   - A. Image and text embeddings are concatenated before one transformer.\n'
                 '   - B. A vision encoder runs separately, but visual features enter selected LLM layers through cross-attention.\n'
                 '   - C. Independent vision and text classifiers produce scores that are averaged.\n'
                 '2. For each, state one advantage and one disadvantage.')
            ),
            "expected_output": (
                "A three-row table identifying fusion type, interaction depth, advantage, and cost."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "early-fusion",
                "intermediate-fusion",
                "late-fusion",
            ],
        },
        {
            "id": "M01.L06.EX05",
            "title": "Audit a VLM architecture paper",
            "lesson_code": "M01.L06",
            "section_id": "architecture-checklist",
            "placement": "after_section",
            "description": (
                "Use the lesson's checklist to turn a model diagram into an engineering analysis."
            ),
            "instructions": (
                "Imagine a paper says: 'We use a frozen ViT, compress its 1024 visual tokens "
                "to 32 learned query tokens, inject them every fourth decoder layer, and fine-tune "
                "only the new fusion modules.'\n"
                "Identify:\n"
                "1. vision backbone status,\n"
                "2. compression mechanism,\n"
                "3. fusion type,\n"
                "4. likely attention mechanism,\n"
                "5. which parameters train,\n"
                "6. one deployment complexity you would inspect."
            ),
            "expected_output": (
                "A structured architecture audit with six answers and one short risk note."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "architecture-analysis",
                "cross-attention",
                "fusion",
                "deployment-thinking",
            ],
        },
        {
            "id": "M01.L06.EX06",
            "title": "Design your own VLM bridge",
            "lesson_code": "M01.L06",
            "section_id": "complete-mental-model",
            "placement": "after_section",
            "description": (
                "Synthesize the chapter into a small architecture proposal."
            ),
            "instructions": (
                ('1. Design a VLM for high-resolution document QA.\n'
                 '2. Choose:\n'
                 '   - vision encoder behavior,\n'
                 '   - visual token compression,\n'
                 '   - cross-attention adapter or unified sequence,\n'
                 '   - frozen or trainable backbones,\n'
                 '   - fusion type,\n'
                 '   - one strategy for keeping visual-token cost manageable,\n'
                 '   - two evaluation metrics/tasks beyond training loss.\n'
                 '3. Justify every choice.')
            ),
            "expected_output": (
                "A compact architecture specification and rationale grounded in the chapter."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "vlm-design",
                "token-budget",
                "architecture-selection",
                "evaluation",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L06.QZ01",
        "title": "Core Architectures of Vision-Language Models — Knowledge Check",
        "lesson_code": "M01.L06",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L06.Q01",
                "section_id": "qkv",
                "question": "What is the role of a query vector in attention?",
                "options": [
                    "It represents what information the current element is looking for.",
                    "It stores the optimizer state.",
                    "It determines image file format.",
                    "It is always the final generated token.",
                ],
                "correct": 0,
                "explanation": (
                    "The query is compared with keys to determine which values should contribute."
                ),
            },
            {
                "id": "M01.L06.Q02",
                "section_id": "attention-math",
                "question": "What does QK^T produce before scaling and softmax?",
                "options": [
                    "Query-to-key relevance scores",
                    "The final text output",
                    "Model gradients",
                    "Image pixels",
                ],
                "correct": 0,
                "explanation": (
                    "Each query is compared with every key through dot products."
                ),
            },
            {
                "id": "M01.L06.Q03",
                "section_id": "attention-math",
                "question": "Why divide attention logits by sqrt(d_k)?",
                "options": [
                    "To keep dot-product magnitudes controlled as feature dimension grows",
                    "To remove all negative values",
                    "To convert image features to RGB",
                    "To make every attention weight equal",
                ],
                "correct": 0,
                "explanation": (
                    "Scaling prevents large dimensional dot products from making softmax excessively sharp."
                ),
            },
            {
                "id": "M01.L06.Q04",
                "section_id": "self-attention",
                "question": "What defines self-attention?",
                "options": [
                    "Q, K, and V are derived from the same sequence.",
                    "Q comes from text and K/V must come from images.",
                    "It has no softmax.",
                    "It cannot process visual tokens.",
                ],
                "correct": 0,
                "explanation": (
                    "Self-attention relates elements within one sequence, including a mixed multimodal sequence."
                ),
            },
            {
                "id": "M01.L06.Q05",
                "section_id": "cross-attention",
                "question": "What defines cross-attention?",
                "options": [
                    "Queries and key/value features can originate from different streams.",
                    "All vectors must come from the same token.",
                    "Only values are learned.",
                    "It requires equal sequence lengths.",
                ],
                "correct": 0,
                "explanation": (
                    "Cross-attention bridges one sequence's queries to another sequence's keys and values."
                ),
            },
            {
                "id": "M01.L06.Q06",
                "section_id": "cross-attn-compression",
                "question": "Why can cross-attention act as a compressor?",
                "options": [
                    "A small fixed set of queries can summarize a much larger key/value sequence.",
                    "It deletes every value vector.",
                    "It only accepts one image patch.",
                    "It forces query and key length to match.",
                ],
                "correct": 0,
                "explanation": (
                    "Output sequence length follows the query count, allowing learned queries to summarize many visual features."
                ),
            },
            {
                "id": "M01.L06.Q07",
                "section_id": "perceiver",
                "question": "What does the perceiver resampler do in the source's Flamingo-style architecture?",
                "options": [
                    "Compresses many vision features into a fixed smaller set of visual tokens",
                    "Replaces the LLM tokenizer",
                    "Generates captions directly",
                    "Quantizes the model to 4-bit",
                ],
                "correct": 0,
                "explanation": (
                    "Learned queries attend over vision features and produce a fixed-size summary."
                ),
            },
            {
                "id": "M01.L06.Q08",
                "section_id": "gated-cross-attention",
                "question": "Why initialize cross-attention gates at zero?",
                "options": [
                    "So newly initialized visual adapters initially do not disturb the pretrained LLM",
                    "So the visual pathway can never be used",
                    "To remove gradients permanently",
                    "To make the model late-fusion only",
                ],
                "correct": 0,
                "explanation": (
                    "Zero initialization starts the architecture close to the original LLM and allows visual influence to grow during training."
                ),
            },
            {
                "id": "M01.L06.Q09",
                "section_id": "unified-sequence",
                "question": "What is the core idea of a unified-sequence VLM?",
                "options": [
                    "Project visual features into the LLM embedding space and process visual and text tokens together.",
                    "Use separate final classifiers only.",
                    "Replace visual features with captions before the LLM.",
                    "Use no vision encoder.",
                ],
                "correct": 0,
                "explanation": (
                    "The architecture turns visual features into LLM-compatible token embeddings and relies on self-attention for fusion."
                ),
            },
            {
                "id": "M01.L06.Q10",
                "section_id": "unified-code",
                "question": "Why must image-placeholder count match projected visual-token count in direct replacement?",
                "options": [
                    "Each placeholder position must receive one visual embedding.",
                    "It changes the tokenizer language.",
                    "It controls LoRA rank.",
                    "It determines the number of classes.",
                ],
                "correct": 0,
                "explanation": (
                    "Mask-based replacement requires compatible numbers of target positions and source embeddings."
                ),
            },
            {
                "id": "M01.L06.Q11",
                "section_id": "frozen-vs-trainable",
                "question": "In the source's referenced comparison, which design performed better when backbones were frozen?",
                "options": [
                    "Cross-attention adapter",
                    "Unified sequence",
                    "Show and Tell",
                    "Late-fusion score averaging",
                ],
                "correct": 0,
                "explanation": (
                    "The source reports a clear cross-attention advantage when the pretrained backbones could not adapt."
                ),
            },
            {
                "id": "M01.L06.Q12",
                "section_id": "frozen-vs-trainable",
                "question": "What happened when the backbones were allowed to adapt in the source's comparison?",
                "options": [
                    "The unified-sequence approach became highly competitive and pulled ahead in the cited results.",
                    "Both models stopped training.",
                    "Cross-attention became the only valid architecture.",
                    "The vision encoder was removed.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter uses this result to show that backbone trainability interacts strongly with fusion architecture."
                ),
            },
            {
                "id": "M01.L06.Q13",
                "section_id": "fair-comparison",
                "question": "Why was the first small-model loss comparison not perfectly controlled?",
                "options": [
                    "The models received different effective text/image token budgets.",
                    "One model used no images.",
                    "Different languages were used.",
                    "Only one model had an optimizer.",
                ],
                "correct": 0,
                "explanation": (
                    "Fewer placeholder image tokens let one architecture pack more text, creating extra training signal."
                ),
            },
            {
                "id": "M01.L06.Q14",
                "section_id": "loss-caveat",
                "question": "Why can total language-model loss hide differences in visual grounding?",
                "options": [
                    "Many target tokens can be predicted largely from linguistic context rather than the image.",
                    "Loss never depends on labels.",
                    "Visual tokens cannot influence text generation.",
                    "Every answer token requires equal visual evidence.",
                ],
                "correct": 0,
                "explanation": (
                    "Only a subset of answer tokens may strongly depend on visual evidence, so aggregate loss can be text-dominated."
                ),
            },
            {
                "id": "M01.L06.Q15",
                "section_id": "early-fusion",
                "question": "Which source architecture is mapped to early fusion?",
                "options": [
                    "SmolVLM-style unified sequence",
                    "Independent score averaging",
                    "Show and Tell only",
                    "Pure text generation",
                ],
                "correct": 0,
                "explanation": (
                    "Projected visual and text tokens are combined before joint LLM self-attention."
                ),
            },
            {
                "id": "M01.L06.Q16",
                "section_id": "intermediate-fusion",
                "question": "Why is Flamingo-style architecture described as intermediate fusion?",
                "options": [
                    "Modalities start separately but interact repeatedly through internal cross-attention layers.",
                    "They never interact.",
                    "They are concatenated before either encoder.",
                    "Only final classifier scores are combined.",
                ],
                "correct": 0,
                "explanation": (
                    "The vision stream remains separate initially but is injected during language processing."
                ),
            },
            {
                "id": "M01.L06.Q17",
                "section_id": "late-fusion",
                "question": "What is a major advantage of late fusion?",
                "options": [
                    "Modularity: modality-specific components can often be replaced independently.",
                    "Maximum fine-grained interaction from the first layer",
                    "No need for modality-specific models",
                    "It always uses fewer parameters than every other architecture",
                ],
                "correct": 0,
                "explanation": (
                    "Late fusion keeps modality-specific pipelines more independent, making the system modular."
                ),
            },
            {
                "id": "M01.L06.Q18",
                "section_id": "show-and-tell",
                "question": "What is the key limitation of the classic Show-and-Tell pattern described in the source?",
                "options": [
                    "The whole image is compressed into one vector before the LSTM decodes.",
                    "It uses too many visual tokens.",
                    "It has too many cross-attention layers.",
                    "It requires a frozen LLM.",
                ],
                "correct": 0,
                "explanation": (
                    "The single-vector bottleneck prevents the decoder from dynamically attending back to different image regions."
                ),
            },
            {
                "id": "M01.L06.Q19",
                "section_id": "architecture-choice",
                "question": "Which statement best reflects the chapter's practical architecture lesson?",
                "options": [
                    "Fusion design must be considered together with backbone trainability, token budget, data, and engineering complexity.",
                    "Cross-attention always wins.",
                    "Unified sequence always wins.",
                    "Architecture alone determines model quality.",
                ],
                "correct": 0,
                "explanation": (
                    "The source repeatedly shows that architecture interacts with training conditions and system constraints."
                ),
            },
            {
                "id": "M01.L06.Q20",
                "section_id": "complete-mental-model",
                "type": "open",
                "question": (
                    "Design two versions of the same VLM: one using a Flamingo-style "
                    "cross-attention adapter with frozen backbones, and one using a "
                    "SmolVLM-style unified sequence with adaptable backbones. Describe the "
                    "vision-token path, compression strategy, fusion mechanism, trainable "
                    "components, implementation complexity, and how you would compare them fairly."
                ),
            },
        ],
        "passing_score": 70,
    },
}
