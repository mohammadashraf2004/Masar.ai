"""M01.L09 — Video-Language Models.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 9, "Video-Language Models".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L09"
MODULE_ORDER = 1
MODULE_TITLE = "Foundations of Vision and Language"
MODULE_DESCRIPTION = (
    "Understand how video-language models extend image-based VLMs with temporal "
    "reasoning, efficient attention, embedding and generative pipelines, scalable "
    "retrieval and reranking, Video-RAG, QLoRA domain adaptation, and visual-token "
    "efficiency."
)
SOURCE_CHAPTER = 9
SOURCE_PAGES = "Chapter 9 — page numbers not provided"


TOPIC = {
    "title": "Video-Language Models",
    "slug": "vision-language-m01-l09",
    "description": (
        "Learn how models reason over video through spatial-temporal factorization, "
        "temporal attention and position encoding; compare embedding and generative "
        "video models; build scalable segment retrieval, reranking, and Video-RAG; "
        "fine-tune a video VLM with QLoRA; and optimize token and training efficiency."
    ),
    "order": 9,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 6.0,
    "skill_tags": [
        "video-language-models",
        "video-classification",
        "video-retrieval",
        "video-qa",
        "temporal-modeling",
        "3d-cnn",
        "2plus1d-convolution",
        "optical-flow",
        "factorized-attention",
        "hierarchical-attention",
        "cross-modal-attention",
        "temporal-position-encoding",
        "video-embeddings",
        "faiss",
        "reranking",
        "video-rag",
        "qlora",
        "frame-sampling",
        "label-masking",
        "token-pooling",
        "frame-selection",
        "training-efficiency",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
        "M01.L07",
        "M01.L08",
    ],

    "lesson": {
        "title": "Video-Language Models",
        "content": r"""
# Video-Language Models

> **Lesson:** M01.L09  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 9, *Video-Language Models*.  
> Page numbers were not included in the supplied source.  
> This lesson is an instructor-authored educational adaptation.

---

## Why video is more than a sequence of images

An image answers:

```text
What is present?
```

A video must also answer:

```text
What happened?
In what order?
How did something move?
What changed?
What caused what?
When did the important event occur?
```

That extra dimension is **time**.

The source begins with a simple example:

```text
one frame:
a deer is visible

multiple frames:
the deer is walking through a park
people are calmly watching and interacting with it
```

The story only becomes clear when frames are considered together.

A video therefore contains:

```text
appearance
+
motion
+
order
+
duration
+
event structure
```

This makes video much more expensive to model.

At 30 frames per second:

```text
10 seconds
→ 300 frames
```

If every frame becomes many image-patch tokens, sequence length grows extremely
quickly.

The central engineering problem of this chapter is:

> **How do we preserve enough temporal information to understand the video
> without letting token count and attention cost explode?**

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why temporal information changes the nature of visual understanding.
- Distinguish video classification, retrieval, captioning, summarization, and QA.
- Explain why embedding models and generative models have fundamentally different cost profiles.
- Explain how 3D CNNs extend 2D convolution through time.
- Explain (2+1)D factorization and why it reduces cost.
- Explain the transfer-learning idea behind inflated 3D CNNs.
- Explain two-stream video models and optical flow.
- Explain why modern video systems often learn motion implicitly rather than computing optical flow explicitly.
- Calculate why naive joint attention becomes expensive for video.
- Explain spatial-temporal factorization in transformer attention.
- Explain hierarchical attention for long videos.
- Describe five core temporal-modeling challenges.
- Explain fully joint, factorized, and hierarchical space-time attention.
- Explain language-guided cross-modal temporal attention.
- Explain why temporal position encoding is necessary.
- Distinguish learned, sinusoidal, and text-formatted temporal positions.
- Explain how modern video-language systems combine spatial, temporal, and language mechanisms.
- Choose between embedding, generative, and hybrid video pipelines.
- Explain why embeddings can be precomputed while generated answers cannot.
- Segment long videos into retrieval units.
- Build a video embedding index with FAISS.
- Explain why normalized dot product equals cosine similarity.
- Explain when approximate indexes become useful.
- Explain retrieve-then-rerank.
- Explain why cross-encoder reranking is more expensive but more precise.
- Build the conceptual stages of Video-RAG.
- Choose the number and duration of retrieved segments based on the query.
- Explain video-specific QLoRA concerns.
- Explain frame-sampling trade-offs.
- Explain why video batches create severe GPU memory pressure.
- Explain answer-only label masking for video fine-tuning.
- Design a correct video SFT collator.
- Explain spatial pooling, temporal pooling, and keyframe selection.
- Explain text-conditioned visual-token resampling.
- Explain why query-conditioned frame selection can reduce wasted compute.
- Explain scaling-consistency experiments for video-model design.
- Explain how lower precision and better data selection improve training efficiency.
- Audit source code examples for common implementation mistakes.

---

## 1. What can a video-language system do?

The source demonstrates three broad capability groups.

### Classification

```text
video
→
label
```

Example:

```text
"eating spaghetti"
```

### Retrieval

```text
text query
+
video library
→
ranked videos / clips
```

Example:

```text
"a person eating spaghetti"
→
most relevant clip
```

### Generation

```text
video
+
prompt
→
text
```

This includes:

- captioning;
- summarization;
- video QA.

[[IMAGE_NEEDED: Video-language task map |
Show one video branching into classification, embedding-based retrieval,
captioning, summarization, and question answering |
Learner should distinguish label output, vector output, and free-form text output]]

---

## 2. Video classification

The simplest task assigns a fixed label.

The source uses a VideoMAE-style classifier:

```python
clf = pipeline(
    "video-classification",
    model="MCG-NJU/videomae-small-finetuned-kinetics",
    device=0,
    dtype=torch.bfloat16,
)

predictions = clf(
    video_path,
    top_k=5,
)
```

The model samples/encodes the video and produces scores over known action
classes.

The important difference from image classification is temporal context.

An image model might recognize:

```text
person
door
```

but video classification should distinguish:

```text
opening a door
closing a door
```

The same objects appear in both.

The action depends on **change over time**.

---

## 3. Text-to-video retrieval

Retrieval uses a shared embedding space.

Conceptually:

```text
text query
→ query vector

video
→ video vector

similarity(query, video)
→ relevance score
```

If vectors are L2-normalized:

```text
dot product
=
cosine similarity
```

The source demonstrates a video-capable embedder with:

```text
text input
video input
fps
maximum frame count
```

A simplified workflow:

```python
inputs = [
    {
        "text": (
            "a person eating spaghetti"
        )
    },
    {
        "video": video_a,
        "fps": 1.0,
        "max_frames": 32,
    },
    {
        "video": video_b,
        "fps": 1.0,
        "max_frames": 32,
    },
]

embeddings = embedder.process(
    inputs
)

query = embeddings[0:1]
videos = embeddings[1:]

scores = (
    videos @ query.T
).squeeze(1)
```

The result is cheap to search once video embeddings are precomputed.

---

## 4. Captioning, summarization, and video QA

Generative video models use the same interaction pattern for several tasks.

### Captioning

```text
"Describe what happens in this video."
```

### Summarization

```text
"Give the key moments in three bullet points."
```

### QA

```text
"What is the person doing?"
```

The main difference is the instruction.

The source uses a chat message containing:

```text
video
+
text prompt
```

then calls:

```text
processor.apply_chat_template(...)
model.generate(...)
```

This is the same high-level interface used for image VLMs, extended with video
input.

---

## 5. Frame sampling during inference

The source's processor call includes:

```python
do_sample_frames=True,
num_frames=num_frames,
```

This means the application does not necessarily send every frame.

Instead it samples a limited set.

Why?

A 30 fps video can contain:

```text
1 minute
→ 1,800 frames
```

Processing all frames can be prohibitively expensive.

Frame sampling is therefore part of the model input design.

### The trade-off

Too few frames:

```text
cheap
but can miss brief events
```

Too many frames:

```text
better coverage
but more memory + compute
```

This trade-off appears repeatedly throughout the chapter.

### Source code issue

The supplied `ask_video()` snippet casts:

```python
inputs["pixel_values_videos"].to(
    dtype
)
```

but `dtype` is not defined inside the shown snippet.

A safer instructional pattern is to use an explicitly defined model dtype, for
example:

```python
VIDEO_DTYPE = torch.bfloat16
```

and cast to that.

The lesson preserves the source workflow while making the missing variable
explicit.

---

## 6. The most important systems distinction: embeddings versus generation

A generative model can technically imitate many tasks.

For example, you could ask:

```text
"Which label best describes this video?"
```

or:

```text
"Describe this video so I can search it."
```

So why use specialized embedding models?

Because the computational cost is fundamentally different.

### Embedding model

For 10,000 videos:

```text
embed each video once
→ store vectors

new query
→ embed query once
→ compare with stored vectors
```

### Generative model

For a query over 10,000 videos:

```text
query + video 1 → generation
query + video 2 → generation
...
query + video 10,000 → generation
```

That means thousands of expensive forward/decode passes.

The source describes this choice as one of the most important architecture
decisions in practical video pipelines.

{{exercise:M01.L09.EX01}}

---

## 7. From 2D CNNs to 3D CNNs

A 2D convolution moves across:

```text
height
×
width
```

of one image.

A 3D convolution moves across:

```text
time
×
height
×
width
```

of consecutive frames.

Instead of detecting:

```text
"edge here"
```

it can learn a pattern such as:

```text
"hand moves left across these frames"
```

This made motion directly learnable from pixels.

But the source emphasizes two costs:

- many more parameters;
- much higher compute.

This motivates factorization.

---

## 8. (2+1)D convolution: factor space and time

Rather than one 3D convolution:

```text
space + time jointly
```

split the operation into:

```text
2D spatial convolution
then
1D temporal convolution
```

So:

```text
frames
   ↓
spatial feature extraction
   ↓
temporal feature extraction
```

This is called **(2+1)D convolution**.

The core insight:

> You do not always need to model every spatial and temporal interaction in one
> monolithic operation.

This factorization principle survives into modern transformers.

{{image:factorized-3d-convolution}}

---

## 9. Inflated 3D: transfer image knowledge into video

A second historical strategy starts with a pretrained 2D CNN.

Instead of learning 3D filters from scratch:

```text
pretrained 2D filter
→ copy/inflate through time
→ 3D filter
→ fine-tune on video
```

This reuses image knowledge.

The underlying lesson is familiar:

```text
pretraining
+
adaptation
```

is often more efficient than relearning visual structure from scratch.

---

## 10. Two-stream video models

Another design treats appearance and motion as different signals.

### Spatial stream

Input:

```text
RGB frames
```

Question:

```text
"What objects/scenes are present?"
```

### Temporal stream

Input:

```text
optical flow
```

Question:

```text
"How are pixels moving?"
```

The two streams are later fused.

This architecture made motion explicit.

{{image:two-stream-video-cnn}}

---

## 11. Optical flow intuition

Optical flow represents pixel displacement between frames.

Example:

```text
position at frame t:
(50, 100)

position at frame t+1:
(55, 103)

flow:
(+5, +3)
```

A static area has flow near:

```text
(0, 0)
```

A moving object produces nonzero displacement.

The source notes that optical flow helped distinguish actions with similar
static appearances.

But computing it was expensive and operationally inconvenient.

Modern models often learn motion representations implicitly from frames rather
than requiring an explicit optical-flow preprocessing pipeline.

---

## 12. The transformer problem: space × time explodes

Transformers make long-range interaction easy.

But self-attention has quadratic cost in sequence length.

Suppose:

```text
300 frames
×
196 patches per frame
=
58,800 tokens
```

Joint attention considers roughly:

```text
58,800²
≈ 3.46 billion
```

pairwise token interactions per attention layer.

That is the core scaling problem.

The video does not merely add:

```text
300 frame-level tokens
```

It may add:

```text
300 × hundreds of spatial tokens
```

---

## 13. Factorized attention

The transformer-era answer mirrors (2+1)D convolution.

Instead of attending across all space-time positions at once:

### Step 1 — Spatial attention

Within each frame:

```text
patches attend to patches
```

### Step 2 — Temporal attention

Across frames:

```text
same/similar spatial positions
attend through time
```

A source-stated complexity form is:

```text
O(
    H × W × T
    ×
    (H × W + T)
)
```

where:

```text
H × W = patches per frame
T     = number of frames
```

For:

```text
H × W = 196
T = 300
```

the stated formula gives approximately:

```text
196 × 300 × (196 + 300)
=
29,164,800
≈ 29.2 million
```

The source text quotes **17 million** for this example.

That number does not match its own displayed complexity formula for the stated
196 patches and 300 frames.

The important supported conclusion remains:

```text
~29 million
is dramatically smaller than
~3.46 billion
```

and factorization reduces computation by orders of magnitude.

{{exercise:M01.L09.EX02}}

---

## 14. Hierarchical attention for long videos

Factorized attention helps with hundreds of frames.

What about an hour?

At 30 fps:

```text
1 hour
→ 108,000 frames
```

The source proposes another level of factorization:

```text
long video
→ short segments
→ process each segment
→ create one segment summary
→ attend across segment summaries
```

Example:

```text
1 hour
→ 120 segments of 30 seconds
→ 120 segment representations
```

Instead of one enormous frame-level sequence, higher-level attention operates on
a small summary sequence.

This is **hierarchical aggregation**.

---

## 15. Five core temporal-modeling challenges

The source presents five recurring challenges.

### 15.1 Long-range dependencies

Example:

```text
frame 1:
person lights fuse

frame 200:
explosion
```

The model must connect distant events.

### 15.2 Variable tempo

Some actions happen quickly.

Others unfold slowly.

Uniform sampling can:

- miss fast events;
- oversample slow scenes.

### 15.3 Relevance

A ten-minute video may contain only two seconds relevant to the question.

### 15.4 Order and causality sensitivity

A model should distinguish:

```text
person enters room
```

from:

```text
person exits room
```

even if similar frames exist in both.

### 15.5 Spatial-temporal trade-off

Some tasks need:

```text
fine object detail
```

while others need:

```text
motion and sequence
```

A fixed allocation of compute may not fit every video.

---

## 16. Why attention is useful for temporal reasoning

Compared with a local convolution or step-by-step recurrent update, attention
can directly connect distant frames.

Conceptually:

```text
frame 1
↔
frame 200
```

in one attention layer.

Multiple heads can learn different relationships.

For example:

```text
head A → short-term motion
head B → global scene context
head C → event transition
```

But full attention still becomes too expensive.

Hence the chapter repeatedly returns to:

```text
factorization
selection
hierarchy
```

---

## 17. Three space-time attention strategies

The source presents three broad strategies.

### Fully joint space-time attention

Every patch in every frame attends to every other patch.

Strength:

```text
maximum interaction flexibility
```

Cost:

```text
extremely expensive
```

### Factorized attention

Separate spatial and temporal attention.

Strength:

```text
strong cost/performance balance
```

### Hierarchical attention

Process local segments, then reason over segment summaries.

Strength:

```text
long-video scalability
```

[[IMAGE_NEEDED: Joint, factorized, and hierarchical video attention |
Show full all-to-all patch/frame attention, separate spatial-then-temporal
attention, and local segment processing followed by segment-level attention |
Learner should see progressively stronger scaling strategies]]

---

## 18. Dynamic token pruning

The source uses a modern model example to illustrate an additional idea:

```text
consecutive frames are often redundant
```

If frame `t` and frame `t+1` are nearly identical, many visual tokens do not
need to be repeated.

A system can:

```text
compare neighboring frames
→ identify redundant visual tokens
→ prune them
```

This adds **relevance filtering** on top of factorized processing.

The video sequence becomes smaller before expensive downstream reasoning.

---

## 19. Cross-modal attention: let the question guide the video

Video QA introduces a powerful signal:

```text
the user's question
```

Suppose the question is:

```text
"When does the person open the gift?"
```

The model does not need equal attention on every frame.

Cross-modal attention can use:

```text
text features as queries
video features as keys/values
```

so the question helps locate relevant moments.

This is especially useful for:

- temporal grounding;
- sentence-to-video segment retrieval;
- question-focused video QA.

---

## 20. Temporal position encoding

Self-attention alone has no inherent notion of token order.

Without positional information, the model cannot reliably know whether:

```text
A happened before B
```

or:

```text
B happened before A
```

So temporal position information is added.

The source lists several forms.

### Learned position embeddings

```text
frame 0 → e0
frame 1 → e1
...
```

### Sinusoidal positions

Fixed sin/cos functions.

### Text-formatted timestamps

Represent time using tokens such as:

```text
"frame 15"
"00:00:15"
```

The purpose is the same:

```text
give the model a sense of when
```

[[IMAGE_NEEDED: Temporal position encoding |
Show visually identical/similar frame tokens receiving different time-position
signals before attention |
Learner should understand why attention needs explicit order information]]

---

## 21. A modern video-language blueprint

The source combines the temporal mechanisms into a high-level pipeline:

```text
video frames
   ↓
vision encoder
   ↓
patch features
   ↓
temporal position information
   ↓
spatial/temporal processing
   ↓
video representation
   ↓
language interaction
   ↓
caption / QA / summary
```

The important pattern is composition.

Modern systems combine familiar building blocks:

- pretrained vision encoders;
- attention;
- temporal positions;
- token compression;
- language decoders.

The innovation is often in how these parts are connected efficiently.

---

## 22. From image-language models to video-language models

The source sketches an evolution.

### CLIP-style image-language embedding

```text
image ↔ text
```

### Video-text contrastive models

```text
video clip ↔ description
```

Temporal information is now part of pretraining.

### Multimodal foundation models

Combine objectives such as:

- masked modeling;
- contrastive learning;
- next-token prediction.

### Modern generative video LLMs

```text
video encoder
→ language model
→ conversational output
```

This enables:

- QA;
- detailed captions;
- summarization;
- instruction following;
- multiturn video discussion.

{{image:video-language-evolution}}

---

## 23. Three practical video model families

The source groups systems by what they output.

### Embedding models

Output:

```text
vector
```

Best for:

- search;
- ranking;
- clustering.

### Generative models

Output:

```text
text
```

Best for:

- QA;
- reasoning;
- summarization;
- conversation.

### Hybrid pipelines

Output:

```text
retrieval
+
generated answer
```

Best for:

- long videos;
- large libraries;
- grounded QA.

---

## 24. Contrastive versus autoregressive objectives

Embedding models use a contrastive idea:

```text
matching video-text pair
→ close in embedding space

nonmatching pair
→ farther apart
```

The output is a fixed-size vector.

Generative models use an autoregressive objective:

```text
predict next token
given previous context
```

The output is variable-length text.

These objectives create different serving behavior.

### Embeddings are reusable

```text
video → vector
```

can be computed offline once.

### Generated answers are query-specific

You cannot precompute:

```text
the answer to a question
that has not been asked yet
```

That explains the cost difference in large-scale search.

---

## 25. Retrieve for breadth, generate for depth

The source gives a 10,000-segment example.

Embedding-only retrieval:

```text
1 query embedding
+
10,000 vector similarities
```

Generative-only search:

```text
10,000 video-question generations
```

Hybrid:

```text
retrieve top 5
→ generate over top 5
```

This is the core Video-RAG pattern:

> **Retrieval handles breadth. Generation handles depth.**

---

## 26. Segment long videos before indexing

A whole-video embedding can be too coarse.

Imagine a ten-minute cooking video containing:

```text
30 sec chopping
2 min frying
7 min plating/talking
```

A query:

```text
"chopping vegetables"
```

may be diluted inside one global video embedding.

The source recommends splitting videos into short retrieval units.

Typical source guidance:

```text
5–10 seconds
```

as a practical default.

Action-dense content may need shorter segments.

Slow content may use longer segments.

The goal:

```text
approximately one meaningful event per segment
```

---

## 27. Segmenting with ffmpeg

The source provides a practical fixed-length segmenter.

Conceptual skeleton:

```python
def segment_video(
    video_path,
    out_dir,
    segment_seconds=5,
):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-c",
            "copy",
            "-map",
            "0",
            "-f",
            "segment",
            "-segment_time",
            str(segment_seconds),
            "-reset_timestamps",
            "1",
            output_pattern,
        ],
        check=True,
    )
```

The important idea is not the shell syntax.

It is:

```text
retrieval unit != whole source video
```

You create smaller searchable temporal chunks.

---

## 28. Embed every segment offline

After segmentation:

```text
segment 1 → embedding
segment 2 → embedding
segment 3 → embedding
...
```

This is an offline cost.

At query time, those video vectors already exist.

A helper may use:

```text
fps = 1.0
max_frames = 32
```

to control how much of each clip is sampled.

Again, this is a coverage/compute trade-off.

---

## 29. Build a FAISS index

If embeddings are L2-normalized, inner-product search can represent cosine
similarity.

Conceptually:

```python
index = faiss.IndexFlatIP(
    vectors.shape[1]
)

index.add(
    vectors.astype(
        np.float32
    )
)
```

Then query:

```python
scores, ids = index.search(
    query_vector,
    k,
)
```

### Source code issue

The supplied text shows:

```python
import faiss-cpu
```

That is a package/install name style, not valid Python import syntax.

The intended module import in Python is:

```python
import faiss
```

The lesson explicitly separates package naming from import naming instead of
copying the malformed line.

---

## 30. Scaling beyond exact search

For a tiny demo:

```text
IndexFlatIP
```

is fine.

At much larger segment counts, the source recommends approximate structures such
as:

```text
IVF
HNSW
```

The embedding workflow does not change.

Only the index/search strategy changes.

Trade-off:

```text
exact search
→ simple + precise
→ slower at very large scale

approximate search
→ faster/scalable
→ may trade a little recall for speed
```

{{exercise:M01.L09.EX03}}

---

## 31. Retrieve, then rerank

Embedding similarity is fast but coarse.

A second model can rescore only the top candidates.

Pipeline:

```text
query
→ embedding retrieval
→ top 20–50
→ expensive query-video reranker
→ best 5
```

The reranker sees the query and candidate video **together**.

That gives it richer pairwise context than independent embeddings.

---

## 32. When is reranking worth it?

Use reranking when:

- top retrieval candidates are close;
- query is ambiguous;
- precision is important;
- false positives are costly.

The source gives examples such as:

- medical video search;
- legal discovery.

Skip reranking when top results are already clearly correct and latency/cost
matters more.

The key principle:

> Spend expensive reasoning only on a small candidate set.

---

## 33. Video-RAG

Video-RAG combines:

```text
embedding retrieval
+
generative video reasoning
```

Pipeline:

```text
long video/library
   ↓
segments
   ↓
embeddings + index
   ↓
query
   ↓
retrieve top-k segments
   ↓
(optional rerank)
   ↓
send survivors + question to video VLM
   ↓
grounded answer
```

This is the video version of text/document RAG.

[[IMAGE_NEEDED: End-to-end Video-RAG |
Show long videos split into segments, embedded and indexed; a query retrieves
top clips, optional reranker reorders them, and a generative video VLM answers
using only selected clips |
Learner should see retrieval and generation as complementary cost tiers]]

---

## 34. Feed multiple retrieved clips to a video VLM

The source builds one chat message containing several video entries.

Conceptually:

```python
content = [
    {
        "type": "video",
        "path": segment_a,
    },
    {
        "type": "video",
        "path": segment_b,
    },
    {
        "type": "text",
        "text": question,
    },
]

messages = [
    {
        "role": "user",
        "content": content,
    }
]
```

The generator receives only selected evidence.

That turns a large-library problem into a small-context reasoning problem.

---

## 35. Ground the generator to retrieved evidence

The source uses an instruction conceptually like:

```text
Answer using ONLY the provided video clips.

If the clips do not contain enough information,
say so.
```

This is an important RAG principle.

Retrieval reduces the search space.

The prompt should also discourage unsupported answers.

This does not guarantee perfect grounding, but it makes the intended behavior
explicit.

---

## 36. How many segments should you retrieve?

The source recommends adjusting `k` by question type.

Short factual question:

```text
2–3 relevant segments may be enough
```

Broad question spanning the video:

```text
more segments may be needed
```

The source suggests:

```text
start around k=5
```

and tune based on answer quality and context-window limits.

This is a classic recall-versus-context trade-off.

More clips:

```text
higher evidence coverage
but
more tokens + more distractors + more cost
```

---

## 37. Why fine-tune a video VLM?

General models may not understand specialized domains well.

Examples from the source:

- surgical procedures;
- factory inspections;
- drone surveys.

Fine-tuning can teach:

- domain vocabulary;
- domain-specific actions;
- expected answer style;
- subtle temporal patterns.

The source uses QLoRA to keep adaptation affordable.

---

## 38. QLoRA for video adaptation

The broad setup carries over from image VLM fine-tuning.

```text
4-bit quantized base model
+
trainable LoRA adapters
```

The source uses:

```text
NF4
double quantization
BF16 compute
```

then injects LoRA into projection layers such as:

```text
q_proj
k_proj
v_proj
gate_proj
```

The key difference is not QLoRA itself.

The difference is the **video input**.

---

## 39. Three video-specific fine-tuning concerns

The source highlights three.

### 39.1 Frame sampling policy

Choose:

```text
num_frames
```

for training.

Ideally it should resemble inference.

Too few:

```text
miss actions
```

Too many:

```text
excess context + memory
```

The source suggests eight frames as a starting point for short clips.

Treat it as a starting heuristic.

### 39.2 Memory pressure

A batch of:

```text
4 videos
× 8 frames
=
32 images worth of pixel tensors
```

before considering model activations.

This can be expensive.

The source recommends small per-device batches plus gradient accumulation.

### 39.3 Label masking

Train on:

```text
assistant answer tokens
```

not:

- user prompt;
- video placeholder/input tokens.

This is the same principle from earlier post-training lessons.

---

## 40. Video SFT dataset shape

A minimal domain example can be:

```json
{
  "video": "clip1.mp4",
  "question": "What does the person pick up?",
  "answer": "A spoon."
}
```

That becomes a chat conversation:

```text
USER
[video]
What does the person pick up?

ASSISTANT
A spoon.
```

The format is simple.

The complexity lies in:

- loading/sampling video frames;
- GPU memory;
- masking labels correctly.

---

## 41. Building a correct video collator

The source constructs user/assistant conversations correctly.

However, the pasted collator ends with:

```python
"labels": toks["input_ids"]
```

which trains on the entire tokenized conversation.

That conflicts with the chapter's own preceding statement that:

> only assistant answer tokens should receive training loss.

So the lesson follows the chapter's stated training objective and makes the
masking explicit.

Conceptually:

```text
USER TOKENS    → -100
VIDEO TOKENS   → -100
ASSISTANT TEXT → target token IDs
PADDING        → -100
```

A high-level implementation strategy is:

1. build the full conversation;
2. tokenize it;
3. identify where the assistant answer begins;
4. clone `input_ids` to `labels`;
5. set earlier positions to `-100`;
6. mask padding positions too.

Pseudocode:

```python
labels = input_ids.clone()

labels[:, :assistant_start] = -100
labels[attention_mask == 0] = -100
```

For batched variable-length conversations, each sample needs its own answer-start
position.

### Why this correction matters

Without masking:

```text
loss includes user prompt
+
special/video input tokens
+
assistant answer
```

That is not the objective the chapter says it wants.

The lesson therefore flags the inconsistency rather than silently copying the
pasted collator.

{{exercise:M01.L09.EX04}}

---

## 42. Use gradient accumulation to control video memory

Suppose GPU memory only fits:

```text
batch size = 1
```

but you want an effective batch of 8.

Use:

```text
per-device batch = 1
gradient accumulation = 8
```

Conceptually:

```text
forward/backward sample 1
accumulate gradient

sample 2
accumulate gradient
...
sample 8
optimizer step
```

This does not eliminate all memory cost, but it avoids keeping multiple full
video samples active in one microbatch.

---

## 43. Fine-tuned adapters can drop into Video-RAG

After training:

```text
base video VLM
+
domain LoRA adapter
```

can replace the generic generator inside Video-RAG.

The source also notes that a specialized embedding model could improve the
retrieval side.

This creates two independent levers:

```text
better retrieval
→ better evidence

better generator
→ better interpretation
```

Improving both can compound system quality.

---

## 44. Why video creates too many visual tokens

Adjacent video frames are often highly redundant.

Example:

```text
frame 100
frame 101
frame 102
```

may differ only slightly.

Yet a naive encoder can produce hundreds of visual tokens for every frame.

Then those visual tokens are projected into the LLM hidden dimension.

The source notes that vision features may be lower-dimensional than LLM
embeddings, so large numbers of projected video tokens can flood the language
model context.

This is both a:

- sequence-length problem;
- representation-efficiency problem.

---

## 45. Spatial and temporal token pooling

### Spatial pooling

Reduce tokens **within each frame**.

Example:

```text
196 patch tokens
→ pooled subset / averages
→ fewer spatial tokens
```

### Temporal pooling

Reduce tokens **across nearby frames**.

Example:

```text
features from frames 1–4
→ averaged/combined representation
```

Both reduce total visual-token count.

{{image:video-token-reduction-strategies}}
{{image:videollama3-dynamic-vision-tokens}}

---

## 46. Intelligent frame selection

Uniform sampling ignores the question.

But in a long video, only a tiny fraction may matter.

The source describes an agent-like pattern where a language model/controller
iteratively decides which frames to inspect.

Conceptually:

```text
question
→ choose candidate time/frame
→ inspect
→ update belief
→ choose next frame
→ stop when enough evidence
```

This converts frame selection into a reasoning/search problem.

{{image:videoagent-adaptive-frame-retrieval}}

Potential benefit:

```text
much less visual processing
```

for sparse-relevance questions.

---

## 47. Text-conditioned visual-token resampling

Frame selection works at frame level.

Text-conditioned resampling can work at finer granularity.

Question:

```text
"What color is the ball?"
```

The system can prioritize visual tokens related to:

```text
ball regions
```

instead of preserving all frame patches.

The source describes a Q-Former-style approach where the text question guides
downsampling.

Trade-off:

For a new conversational question, visual tokens may need to be selected again.

So per-turn efficiency gains can shrink in long multiturn conversations.

---

## 48. Experiment cheaply before scaling

Large video-model experiments are expensive.

The source revisits a scaling-consistency idea:

```text
test design choices on smaller proxy models
→ identify winner
→ run expensive large-scale training once
```

Possible choices to test:

- frame rate;
- number of frames;
- temporal attention design;
- fusion method;
- data mixture.

The source reports that some referenced experiments found choices transferring
across model scales after sufficient data.

Treat the exact scale/sample thresholds as source-specific findings.

The general workflow is:

> Use cheaper proxy experiments to narrow architecture decisions before paying
> for full-scale training.

---

## 49. Low-precision video training

The source connects video training to the same precision/memory trade-offs seen
earlier.

Examples include:

- QLoRA/NF4 for adaptation;
- FP8-style mixed precision for large-scale training.

Goal:

```text
smaller memory footprint
→ larger batches / higher throughput
```

provided hardware and training stability support the chosen precision.

---

## 50. Better data can beat more data

The source closes training efficiency with a data-quality lesson.

Instead of:

```text
collect everything
```

a strong strategy is:

```text
diversity first
then
quality filtering
```

Why?

A redundant video dataset may add huge storage and compute without adding much
new information.

For video, where every sample is expensive, sample quality matters even more.

---

## 51. Video pipeline decision framework

### Need a fixed action label?

Use:

```text
video classifier
```

### Need search over a large video library?

Use:

```text
embedding model
+
vector index
```

### Need high-precision search?

Use:

```text
embedding retrieval
+
reranker
```

### Need open-ended reasoning over one short video?

Use:

```text
generative video VLM
```

### Need QA over long videos or a large library?

Use:

```text
Video-RAG
```

### Need a specialized domain?

Use:

```text
QLoRA / PEFT adaptation
```

### Need lower inference/training cost?

Tune:

- segment duration;
- frame count;
- token pooling;
- frame selection;
- quantization/precision;
- model size.

---

## 52. Evaluate the stages separately

Video systems have several failure points.

### Classification

Measure task accuracy/top-k performance.

### Retrieval

Measure:

- Recall@k;
- ranking quality.

### Reranking

Measure whether relevant clips move upward.

### Video-RAG

Separate:

```text
retrieval quality
from
answer quality
```

A wrong answer can come from:

- wrong segment retrieval;
- insufficient frame sampling;
- poor generation.

### Fine-tuning

Compare:

- base model;
- adapted model;
- domain test set;
- general behavior if retention matters.

### Efficiency

Track:

- frames per example;
- visual token count;
- GPU memory;
- retrieval latency;
- rerank latency;
- generation latency.

{{exercise:M01.L09.EX05}}

---

## 53. Source-specific implementation notes

The source is rich in practical code but contains a few pasted-code and arithmetic
issues.

### Undefined `dtype`

The `ask_video()` examples cast video tensors with:

```text
dtype
```

without defining it in the shown function scope.

The instructional version uses an explicitly defined dtype.

### FAISS import

The source shows:

```python
import faiss-cpu
```

which is not valid Python import syntax.

`faiss-cpu` is a package distribution name; Python code imports the `faiss`
module.

### Fine-tuning label masking mismatch

The prose explicitly says:

```text
train only on assistant answer tokens
```

but the pasted collator sets:

```python
labels = input_ids
```

with no mask.

The lesson follows the stated training goal and explains the necessary masking.

### Factorized-attention arithmetic

The source states:

```text
O(HWT(HW + T))
```

and gives:

```text
196 patches
300 frames
```

which evaluate to approximately:

```text
29.2 million
```

under that formula, not the quoted 17 million.

The source's main point—factorization is vastly cheaper than ~3.46 billion full
joint comparisons—still holds.

### Dynamic helper imports

The source uses `importlib` to load helper scripts from model repositories.

It explicitly warns that this usage can evolve as libraries mature.

So preserve the conceptual workflow, and check the relevant model documentation
when actually implementing it.

---

## 54. The complete video-language mental model

The chapter can be summarized as:

```text
VIDEO
  ↓
frames
  ↓
spatial visual features
  ↓
HOW DO WE HANDLE TIME?

historical:
3D CNN
(2+1)D
optical flow / two-stream

modern:
temporal positions
factorized attention
hierarchical attention
token pruning
question-guided attention

  ↓
WHAT OUTPUT DO WE NEED?

CLASSIFICATION
→ label

SEARCH
→ embedding

REASONING
→ generated text

LARGE-SCALE QA
→ segment
→ embed
→ index
→ retrieve
→ rerank
→ generate

DOMAIN ADAPTATION
→ QLoRA
→ video-aware frame sampling
→ memory control
→ answer-only label masking

EFFICIENCY
→ spatial pooling
→ temporal pooling
→ keyframe selection
→ text-conditioned resampling
→ lower precision
→ better data
```

The central idea is:

> **Video understanding is image understanding plus a carefully managed time
> dimension. Almost every successful architecture reduces the cost of time
> through factorization, selection, compression, or hierarchy.**

{{exercise:M01.L09.EX06}}

---

## Important misconceptions

### Misconception 1: "A video model is just an image model run on every frame."

That loses the relationships between frames.

Video understanding requires temporal structure.

### Misconception 2: "If every frame is classified correctly, the action is understood."

Not necessarily.

Actions can depend on ordering and transitions.

### Misconception 3: "More frames always improve video understanding."

More frames increase coverage but also increase redundancy, memory, and compute.

### Misconception 4: "Full joint attention is always the most practical approach."

Its quadratic cost becomes extreme for video.

### Misconception 5: "Factorization is only an old CNN trick."

The same space/time factorization principle appears in modern attention systems.

### Misconception 6: "Self-attention automatically knows frame order."

It needs temporal/positional information.

### Misconception 7: "Embedding and generative models are interchangeable in production."

They can solve overlapping tasks, but their cost profiles are radically
different.

### Misconception 8: "One embedding for a ten-minute video is always enough."

Fine-grained events can be diluted.

Segment-level retrieval is often more useful.

### Misconception 9: "Reranking should be applied to the entire video corpus."

That defeats the purpose.

Use cheap retrieval first, then rerank a small candidate set.

### Misconception 10: "Video-RAG generates over every video."

It retrieves a small relevant subset first.

### Misconception 11: "Image VLM fine-tuning code transfers to video unchanged."

Video adds frame sampling, much larger pixel tensors, and temporal input
considerations.

### Misconception 12: "The source's pasted collator masks non-answer tokens."

Its prose says it should, but the shown return block does not.

### Misconception 13: "Frame selection and token pooling are the same."

Frame selection removes entire temporal observations.

Token pooling can compress spatial or temporal features after encoding.

### Misconception 14: "More training video is always better."

Redundant low-quality data can consume enormous compute without adding useful
coverage.

---

## Key terminology

| Term | Meaning |
|---|---|
| Video-language model | Model combining video understanding with language representations or generation |
| Temporal modeling | Representing motion, order, duration, and event relationships |
| Video classification | Assigning a fixed action/event label |
| Video embedding | Fixed-size vector representing a video or segment |
| Video retrieval | Ranking video segments by relevance to a query |
| Video QA | Answering questions about video content |
| 3D convolution | Convolution across time and space |
| (2+1)D convolution | Spatial 2D convolution followed by temporal 1D convolution |
| I3D | Inflating pretrained 2D filters through time for video |
| Optical flow | Pixel-motion field between frames |
| Two-stream model | Separate appearance and motion processing branches |
| Joint space-time attention | Attention over all patches across all frames |
| Factorized attention | Separate spatial and temporal attention |
| Hierarchical attention | Local segment processing followed by segment-level attention |
| Temporal position encoding | Signal representing time/order of frames |
| Cross-modal attention | Attention connecting text and video representations |
| Contrastive objective | Pull matching pairs together and push nonmatches apart |
| Autoregressive objective | Predict the next text token from prior context |
| Segment | Short temporal clip used as a retrieval unit |
| FAISS | Vector-similarity indexing/search library |
| Approximate nearest neighbor | Faster vector search that may trade exactness for scalability |
| Reranker | Expensive model that rescores a small candidate set |
| Video-RAG | Video retrieval followed by grounded generative answering |
| QLoRA | Quantized base model plus trainable LoRA adapters |
| Frame sampling | Selecting a limited number of frames for model input |
| Label masking | Excluding prompt/video/input positions from answer-generation loss |
| Spatial pooling | Reducing visual tokens within frames |
| Temporal pooling | Reducing representations across nearby frames |
| Keyframe selection | Selecting the most informative frames |
| Text-conditioned resampling | Using the query to choose visual tokens |
| Scaling consistency | Testing choices on smaller proxies before expensive large-scale training |

---

## Self-check

Before moving on, make sure you can answer:

1. Why does time make video understanding different from image understanding?
2. What is the difference between video classification and video QA?
3. How does text-to-video retrieval work?
4. Why does L2 normalization make dot product equivalent to cosine similarity?
5. Why are embeddings reusable across queries?
6. Why are generated answers not reusable in the same way?
7. What does 3D convolution add to 2D convolution?
8. What is (2+1)D factorization?
9. What is I3D trying to reuse?
10. What are the two branches in a two-stream model?
11. What does optical flow encode?
12. Why did explicit optical-flow pipelines become operationally unattractive?
13. How many tokens result from 300 frames × 196 patches?
14. Why does full attention over that sequence become expensive?
15. How does factorized attention reduce cost?
16. What is hierarchical attention?
17. What are the five temporal-modeling challenges in the source?
18. Why can uniform frame sampling fail on mixed-tempo video?
19. Why should a model care about frame order?
20. What is fully joint space-time attention?
21. What is dynamic token pruning?
22. How can a question guide temporal attention?
23. Why is temporal position encoding necessary?
24. What forms of temporal position encoding does the source mention?
25. What does an embedding video model output?
26. What does a generative video model output?
27. Why is a hybrid pipeline useful?
28. Why segment long videos before retrieval?
29. What segment lengths does the source suggest as practical starting points?
30. Why embed segments offline?
31. Why can IndexFlatIP implement cosine search for normalized embeddings?
32. When might IVF/HNSW-style approximate indexes be useful?
33. What is retrieve-then-rerank?
34. Why is reranking more precise but more expensive?
35. What are the main stages of Video-RAG?
36. Why should the generator see only retrieved clips?
37. Why can a larger `k` both help and hurt?
38. What does QLoRA contribute to video fine-tuning?
39. Why should training and inference frame policies be similar?
40. Why is video batch memory much larger than image batch memory?
41. What tokens should be masked during video SFT?
42. What is wrong with using `labels = input_ids` if the goal is answer-only loss?
43. How does gradient accumulation help video training?
44. How can an adapted generator improve Video-RAG?
45. What is spatial pooling?
46. What is temporal pooling?
47. What is intelligent frame selection?
48. What is text-conditioned token resampling?
49. Why can query-conditioned resampling become less efficient in multiturn chat?
50. What is scaling consistency?
51. Why can low precision improve training throughput?
52. Why is data selection especially valuable for video?
53. What source arithmetic/code inconsistencies should you recognize before copying the examples?
54. What is the chapter's recurring efficiency principle?

---

## Retain this idea

**Video is expensive because time multiplies visual tokens and introduces order,
motion, relevance, and long-range dependencies. The recurring solution is to
avoid modeling everything equally: factor space and time, summarize long
sequences hierarchically, retrieve only relevant clips, rerank only a small
candidate set, and generate only over the evidence that matters.**
""",

        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "video-task-map", "title": "Video-language task map", "order": 1},
            {"id": "classification", "title": "Video classification", "order": 2},
            {"id": "embedding-retrieval", "title": "Text-to-video retrieval", "order": 3},
            {"id": "generative-video", "title": "Generative video tasks", "order": 4},
            {"id": "frame-sampling-inference", "title": "Frame sampling at inference", "order": 5},
            {"id": "embedding-vs-generation", "title": "Embeddings versus generation", "order": 6},
            {"id": "3d-cnn", "title": "3D CNNs", "order": 7},
            {"id": "2plus1d", "title": "(2+1)D convolution", "order": 8},
            {"id": "i3d", "title": "Inflated 3D", "order": 9},
            {"id": "two-stream", "title": "Two-stream video models", "order": 10},
            {"id": "optical-flow", "title": "Optical flow", "order": 11},
            {"id": "attention-explosion", "title": "The space-time attention explosion", "order": 12},
            {"id": "factorized-attention", "title": "Factorized attention", "order": 13},
            {"id": "hierarchical-attention", "title": "Hierarchical attention", "order": 14},
            {"id": "temporal-challenges", "title": "Five temporal-modeling challenges", "order": 15},
            {"id": "attention-helps-time", "title": "Attention for temporal reasoning", "order": 16},
            {"id": "three-attention-strategies", "title": "Three space-time attention strategies", "order": 17},
            {"id": "dynamic-tokens", "title": "Dynamic token pruning", "order": 18},
            {"id": "cross-modal-temporal", "title": "Language-guided temporal attention", "order": 19},
            {"id": "temporal-position", "title": "Temporal position encoding", "order": 20},
            {"id": "modern-video-blueprint", "title": "Modern video-language blueprint", "order": 21},
            {"id": "model-evolution", "title": "Evolution to video-language models", "order": 22},
            {"id": "output-families", "title": "Video model output families", "order": 23},
            {"id": "contrastive-vs-autoregressive", "title": "Contrastive versus autoregressive", "order": 24},
            {"id": "retrieve-reason", "title": "Retrieve for breadth, generate for depth", "order": 25},
            {"id": "segment-videos", "title": "Segment videos before indexing", "order": 26},
            {"id": "ffmpeg-segmentation", "title": "Video segmentation with ffmpeg", "order": 27},
            {"id": "segment-embeddings", "title": "Offline segment embeddings", "order": 28},
            {"id": "faiss-index", "title": "FAISS indexing", "order": 29},
            {"id": "approximate-index", "title": "Approximate vector indexes", "order": 30},
            {"id": "reranking", "title": "Retrieve then rerank", "order": 31},
            {"id": "reranker-cost", "title": "When reranking is worth it", "order": 32},
            {"id": "video-rag", "title": "Video-RAG", "order": 33},
            {"id": "rag-generation", "title": "Generation from retrieved clips", "order": 34},
            {"id": "rag-grounding-prompt", "title": "Ground generation to evidence", "order": 35},
            {"id": "rag-k", "title": "Choosing retrieval k", "order": 36},
            {"id": "domain-finetuning", "title": "Why fine-tune a video VLM", "order": 37},
            {"id": "video-qlora", "title": "QLoRA for video", "order": 38},
            {"id": "video-finetune-concerns", "title": "Video-specific fine-tuning concerns", "order": 39},
            {"id": "video-dataset", "title": "Video SFT dataset format", "order": 40},
            {"id": "video-collator", "title": "Correct answer-only label masking", "order": 41},
            {"id": "training-memory", "title": "Gradient accumulation for video", "order": 42},
            {"id": "adapter-deployment", "title": "Adapters inside Video-RAG", "order": 43},
            {"id": "token-efficiency", "title": "Video visual-token pressure", "order": 44},
            {"id": "pooling", "title": "Spatial and temporal pooling", "order": 45},
            {"id": "frame-selection", "title": "Intelligent frame selection", "order": 46},
            {"id": "text-conditioned-resampling", "title": "Text-conditioned token resampling", "order": 47},
            {"id": "scaling-consistency", "title": "Scaling-consistency experiments", "order": 48},
            {"id": "low-precision-training", "title": "Low-precision training", "order": 49},
            {"id": "better-data", "title": "Smarter video data", "order": 50},
            {"id": "pipeline-choice", "title": "Video pipeline decision framework", "order": 51},
            {"id": "evaluation", "title": "Stage-by-stage evaluation", "order": 52},
            {"id": "source-caveats", "title": "Source-specific implementation notes", "order": 53},
            {"id": "complete-mental-model", "title": "Complete video-language mental model", "order": 54},
        ],
    },

    "exercises": [
        {
            "id": "M01.L09.EX01",
            "title": "Choose embedding, generative, or hybrid",
            "lesson_code": "M01.L09",
            "section_id": "embedding-vs-generation",
            "placement": "after_section",
            "description": (
                "Match video product requirements to the correct model-output family."
            ),
            "instructions": (
                ('1. Choose embedding model, generative video model, or hybrid pipeline for:\n'
                 "   - A. Search 2 million clips for 'person falling from a bicycle'.\n"
                 '   - B. Summarize one 20-second clip.\n'
                 '   - C. Answer questions over a 5,000-hour archive.\n'
                 '   - D. Cluster similar sports highlights.\n'
                 '2. For each, explain why the output type and serving cost fit the task.')
            ),
            "expected_output": (
                "A four-row table with model family, output, cost rationale, and main limitation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "video-embeddings",
                "generation",
                "hybrid-pipelines",
            ],
        },
        {
            "id": "M01.L09.EX02",
            "title": "Compare joint and factorized attention cost",
            "lesson_code": "M01.L09",
            "section_id": "factorized-attention",
            "placement": "after_section",
            "description": (
                "Quantify why factorization is essential for video transformers."
            ),
            "instructions": (
                "A video has T=120 frames and 196 patch tokens per frame.\n"
                "1. Compute N = 196×120.\n"
                "2. Compute N² for full joint attention interaction count.\n"
                "3. Compute 196×120×(196+120) using the chapter's factorized formula.\n"
                "4. Compute the approximate reduction ratio.\n"
                "5. Explain what information factorization chooses not to model directly in one operation."
            ),
            "expected_output": (
                "Step-by-step arithmetic and a short efficiency interpretation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "factorized-attention",
                "complexity",
                "temporal-modeling",
            ],
        },
        {
            "id": "M01.L09.EX03",
            "title": "Design a scalable video retrieval index",
            "lesson_code": "M01.L09",
            "section_id": "approximate-index",
            "placement": "after_section",
            "description": (
                "Design the segmentation, embedding, and indexing stages of large-scale video search."
            ),
            "instructions": (
                "You have 20,000 one-hour lecture videos.\n"
                "Design a retrieval plan including:\n"
                "1. segment duration,\n"
                "2. frame sampling for embeddings,\n"
                "3. offline embedding workflow,\n"
                "4. exact or approximate FAISS index,\n"
                "5. metadata stored per vector,\n"
                "6. one retrieval-quality metric.\n"
                "Explain why whole-video embeddings would be too coarse."
            ),
            "expected_output": (
                "A six-part retrieval architecture with rationale."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "video-segmentation",
                "faiss",
                "retrieval",
                "indexing",
            ],
        },
        {
            "id": "M01.L09.EX04",
            "title": "Repair a video SFT collator",
            "lesson_code": "M01.L09",
            "section_id": "video-collator",
            "placement": "after_section",
            "description": (
                "Apply answer-only label masking to multimodal video fine-tuning."
            ),
            "instructions": (
                "Suppose tokenized input contains:\n"
                "[USER_PROMPT][VIDEO_PLACEHOLDERS][ASSISTANT_ANSWER][PAD]\n"
                "Create the conceptual labels for training.\n"
                "Mark which regions become -100 and which retain token IDs.\n"
                "Then explain why labels=input_ids for the entire sequence conflicts with "
                "the source's stated answer-only training objective."
            ),
            "expected_output": (
                "A token-region mask diagram and a short explanation of the loss correction."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "label-masking",
                "video-sft",
                "qlora",
            ],
        },
        {
            "id": "M01.L09.EX05",
            "title": "Diagnose a weak Video-RAG answer",
            "lesson_code": "M01.L09",
            "section_id": "evaluation",
            "placement": "after_section",
            "description": (
                "Separate retrieval, sampling, reranking, and generation failures."
            ),
            "instructions": (
                "A Video-RAG system answers a question incorrectly.\n"
                "Create a debugging sequence that checks:\n"
                "1. whether the correct segment exists in top-20 retrieval,\n"
                "2. whether reranking promotes it,\n"
                "3. whether sampled frames actually contain the event,\n"
                "4. whether the generator answers correctly when given the known-good segment,\n"
                "5. whether increasing k adds useful evidence or only distraction."
            ),
            "expected_output": (
                "A diagnostic decision tree that identifies which stage is responsible."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "video-rag",
                "retrieval-evaluation",
                "reranking",
                "generation-evaluation",
            ],
        },
        {
            "id": "M01.L09.EX06",
            "title": "Design an efficient long-video assistant",
            "lesson_code": "M01.L09",
            "section_id": "complete-mental-model",
            "placement": "after_section",
            "description": (
                "Synthesize temporal modeling, retrieval, generation, and efficiency choices."
            ),
            "instructions": (
                ('1. Design a system that answers questions about 2-hour factory-inspection videos.\n'
                 '2. Specify:\n'
                 '   - segmentation strategy,\n'
                 '   - embedding model role,\n'
                 '   - vector index,\n'
                 '   - reranking policy,\n'
                 '   - generation stage,\n'
                 '   - frame count policy,\n'
                 '   - whether domain QLoRA is needed,\n'
                 '   - one token-reduction strategy,\n'
                 '   - evaluation metrics for retrieval and answers.\n'
                 '3. Justify every choice.')
            ),
            "expected_output": (
                "An end-to-end architecture proposal grounded in the chapter's patterns."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "video-system-design",
                "video-rag",
                "temporal-efficiency",
                "qlora",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L09.QZ01",
        "title": "Video-Language Models — Knowledge Check",
        "lesson_code": "M01.L09",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L09.Q01",
                "section_id": "video-task-map",
                "question": "What does video add beyond a static image?",
                "options": [
                    "Temporal order, motion, duration, and event relationships",
                    "Only more RGB channels",
                    "Only higher image resolution",
                    "No additional modeling problem",
                ],
                "correct": 0,
                "explanation": (
                    "Video understanding must model how visual content changes over time."
                ),
            },
            {
                "id": "M01.L09.Q02",
                "section_id": "embedding-retrieval",
                "question": "Why can dot product be used as cosine similarity in the source's retrieval example?",
                "options": [
                    "The embeddings are L2-normalized.",
                    "The videos contain one frame.",
                    "Dot product always equals cosine similarity.",
                    "The model outputs probabilities.",
                ],
                "correct": 0,
                "explanation": (
                    "For unit-length vectors, dot product equals cosine similarity."
                ),
            },
            {
                "id": "M01.L09.Q03",
                "section_id": "embedding-vs-generation",
                "question": "Why are embedding models much cheaper for large-library search?",
                "options": [
                    "Video embeddings can be precomputed once and reused for every query.",
                    "They generate longer answers.",
                    "They require one LLM generation per query-video pair.",
                    "They never process video.",
                ],
                "correct": 0,
                "explanation": (
                    "At query time, retrieval compares one query vector against stored video vectors."
                ),
            },
            {
                "id": "M01.L09.Q04",
                "section_id": "2plus1d",
                "question": "What is the main idea of (2+1)D convolution?",
                "options": [
                    "Factor spatial processing and temporal processing into separate operations.",
                    "Use only one video frame.",
                    "Replace convolutions with text generation.",
                    "Compute optical flow only.",
                ],
                "correct": 0,
                "explanation": (
                    "Spatial 2D convolution is followed by temporal 1D convolution."
                ),
            },
            {
                "id": "M01.L09.Q05",
                "section_id": "two-stream",
                "question": "What does the temporal stream in a classic two-stream model consume?",
                "options": [
                    "Optical flow",
                    "Only text",
                    "Audio transcripts",
                    "A FAISS index",
                ],
                "correct": 0,
                "explanation": (
                    "The temporal stream explicitly models pixel motion through optical flow."
                ),
            },
            {
                "id": "M01.L09.Q06",
                "section_id": "attention-explosion",
                "question": "Why is naive joint attention so expensive for video?",
                "options": [
                    "The number of tokens grows with frames × patches, and attention is quadratic in token count.",
                    "Video has no tokens.",
                    "Attention is linear in all cases.",
                    "Only the tokenizer consumes compute.",
                ],
                "correct": 0,
                "explanation": (
                    "Space and time multiply sequence length before the quadratic attention cost is applied."
                ),
            },
            {
                "id": "M01.L09.Q07",
                "section_id": "factorized-attention",
                "question": "How does factorized attention reduce video compute?",
                "options": [
                    "It performs spatial and temporal attention separately rather than one full space-time operation.",
                    "It removes all temporal information.",
                    "It converts video to audio.",
                    "It uses no attention.",
                ],
                "correct": 0,
                "explanation": (
                    "Factorization avoids all-to-all interactions over the full space-time token grid at once."
                ),
            },
            {
                "id": "M01.L09.Q08",
                "section_id": "hierarchical-attention",
                "question": "What is hierarchical attention designed to handle?",
                "options": [
                    "Very long videos by summarizing local segments before global reasoning",
                    "Only single images",
                    "Tokenizer compression",
                    "Model quantization",
                ],
                "correct": 0,
                "explanation": (
                    "Local segments are processed first, then higher-level attention operates over their summaries."
                ),
            },
            {
                "id": "M01.L09.Q09",
                "section_id": "temporal-position",
                "question": "Why is temporal position encoding necessary?",
                "options": [
                    "Self-attention alone does not inherently encode frame order.",
                    "Video frames have no pixels.",
                    "It increases LoRA rank.",
                    "It creates the FAISS index.",
                ],
                "correct": 0,
                "explanation": (
                    "Temporal positions tell the model when each frame/token occurs."
                ),
            },
            {
                "id": "M01.L09.Q10",
                "section_id": "cross-modal-temporal",
                "question": "What is the benefit of language-guided cross-modal attention in video QA?",
                "options": [
                    "The question can focus visual attention on temporally relevant moments.",
                    "It forces every frame to receive equal weight.",
                    "It removes text from the model.",
                    "It converts embeddings to labels.",
                ],
                "correct": 0,
                "explanation": (
                    "Text features can guide the model toward the frames that answer the query."
                ),
            },
            {
                "id": "M01.L09.Q11",
                "section_id": "segment-videos",
                "question": "Why segment long videos before retrieval?",
                "options": [
                    "A whole-video embedding can dilute short relevant events.",
                    "FAISS can only store MP4 files.",
                    "Segments eliminate all compute.",
                    "Generative models require exactly five seconds.",
                ],
                "correct": 0,
                "explanation": (
                    "Short clips provide finer-grained retrieval units tied to individual events."
                ),
            },
            {
                "id": "M01.L09.Q12",
                "section_id": "faiss-index",
                "question": "Which index does the source use for exact inner-product search in the demo?",
                "options": [
                    "IndexFlatIP",
                    "IndexFlatL2 only",
                    "B-tree",
                    "BM25",
                ],
                "correct": 0,
                "explanation": (
                    "Normalized embeddings let IndexFlatIP implement cosine-equivalent ranking."
                ),
            },
            {
                "id": "M01.L09.Q13",
                "section_id": "reranking",
                "question": "Why add a reranker after embedding retrieval?",
                "options": [
                    "It can jointly inspect the query and candidate video for more precise scoring.",
                    "It makes retrieval cheaper than vector search.",
                    "It removes the need for candidate retrieval.",
                    "It stores one vector forever.",
                ],
                "correct": 0,
                "explanation": (
                    "Reranking spends more compute on only a small shortlist."
                ),
            },
            {
                "id": "M01.L09.Q14",
                "section_id": "video-rag",
                "question": "What is the core Video-RAG pattern?",
                "options": [
                    "Retrieve relevant clips, optionally rerank them, then generate an answer from the selected evidence.",
                    "Generate over every video in the library.",
                    "Classify every video and stop.",
                    "Convert all videos to text before any search.",
                ],
                "correct": 0,
                "explanation": (
                    "Retrieval narrows the search space before expensive generative reasoning."
                ),
            },
            {
                "id": "M01.L09.Q15",
                "section_id": "video-finetune-concerns",
                "question": "Which concern is specific to video VLM fine-tuning compared with a single-image example?",
                "options": [
                    "Choosing how many frames to sample from each clip",
                    "Having a learning rate",
                    "Using an optimizer",
                    "Having labels",
                ],
                "correct": 0,
                "explanation": (
                    "Video introduces a temporal sampling policy that strongly affects coverage and memory."
                ),
            },
            {
                "id": "M01.L09.Q16",
                "section_id": "video-collator",
                "question": "If the objective is answer-only SFT, what should happen to user/video prompt positions in labels?",
                "options": [
                    "They should be masked with an ignore index such as -100.",
                    "They should always equal input_ids.",
                    "They should be duplicated twice.",
                    "They should become video embeddings.",
                ],
                "correct": 0,
                "explanation": (
                    "Masking prevents loss from being computed on the input context."
                ),
            },
            {
                "id": "M01.L09.Q17",
                "section_id": "pooling",
                "question": "What is temporal pooling?",
                "options": [
                    "Reducing representations across nearby frames/time steps",
                    "Reducing token dimension only within one text prompt",
                    "Adding more video frames",
                    "Training a reranker",
                ],
                "correct": 0,
                "explanation": (
                    "Temporal pooling compresses redundant information across time."
                ),
            },
            {
                "id": "M01.L09.Q18",
                "section_id": "frame-selection",
                "question": "Why can intelligent frame selection improve long-video efficiency?",
                "options": [
                    "It spends visual compute on frames most likely to contain relevant evidence.",
                    "It guarantees every frame is processed.",
                    "It increases sequence length.",
                    "It removes the question.",
                ],
                "correct": 0,
                "explanation": (
                    "Sparse relevance means many frames can be skipped without helping the answer."
                ),
            },
            {
                "id": "M01.L09.Q19",
                "section_id": "better-data",
                "question": "What data strategy does the source emphasize for efficient video training?",
                "options": [
                    "Prioritize diversity, then refine for quality instead of blindly maximizing volume.",
                    "Keep every available clip regardless of redundancy.",
                    "Use only one source.",
                    "Remove all filtering.",
                ],
                "correct": 0,
                "explanation": (
                    "Video samples are expensive, so each retained sample should add useful coverage."
                ),
            },
            {
                "id": "M01.L09.Q20",
                "section_id": "complete-mental-model",
                "type": "open",
                "question": (
                    "Design a Video-RAG system for a large archive of long industrial videos. "
                    "Explain how you would segment videos, sample frames, embed and index clips, "
                    "choose exact or approximate search, rerank candidates, generate grounded "
                    "answers, fine-tune with QLoRA if needed, mask training labels correctly, "
                    "and control visual-token cost."
                ),
            },
        ],
        "passing_score": 70,
    },
}
