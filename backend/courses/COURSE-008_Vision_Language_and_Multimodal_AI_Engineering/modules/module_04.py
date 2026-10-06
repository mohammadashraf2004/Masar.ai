"""M01.L04 — Multimodality and Data Engineering for Vision-Language Systems.

Two source chapters -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Sources:
- "Understanding Multimodality: Beyond Text"
- "Training Data and Preprocessing for VLMs"

Page numbers were not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L04"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Vision and Language"

MODULE_DESCRIPTION = (
    "Understand how multimodal systems represent and fuse text, audio, images, "
    "video, and structured outputs, then learn how to build the large-scale "
    "datasets and preprocessing pipelines that train those capabilities."
)

SOURCE_CHAPTER = "Merged: Understanding Multimodality + VLM Training Data"

SOURCE_PAGES = "Source chapters supplied without page numbers"


TOPIC = {
    "title": "Multimodality and Data Engineering for Vision-Language Systems",

    "slug": "vision-language-m01-l04",

    "description": (
        "Connect the conceptual side of multimodality—representations, audio, vision, "
        "video, fusion, live interfaces, and structured outputs—with the practical "
        "data-engineering side of modern VLM training: image-text, video-text and VLA "
        "datasets, sourcing, filtering, diversity, annotation, validation, WebDataset "
        "packaging, preprocessing choices, and dataset-mixture design."
    ),

    "order": 4,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 5.0,

    "skill_tags": [
        "multimodality",
        "multimodal-agents",
        "audio",
        "computer-vision",
        "video-understanding",
        "multimodal-fusion",
        "vlm-data",
        "video-data",
        "vla-data",
        "data-filtering",
        "dataset-diversity",
        "taxonomy",
        "synthetic-annotation",
        "quality-validation",
        "webdataset",
        "dataset-mixtures",
        "ablation-studies",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
    ],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Multimodality and Data Engineering for Vision-Language Systems",

        "content": r"""
# Multimodality and Data Engineering for Vision-Language Systems

> **Lesson:** M01.L04  
> **Module:** Foundations of Vision and Language  
> **Sources:** *Understanding Multimodality: Beyond Text* +  
> *Training Data and Preprocessing for VLMs*.  
> Page numbers were not included in the supplied material.  
> This lesson is an instructor-authored curriculum adaptation rather than a
> reproduction of either source.

---

## Why these two chapters belong together

Multimodality is often taught as a model-architecture topic:

```text
text + image + audio + video
            ↓
       one AI system
```

But a multimodal model can only learn what its training data exposes it to.

If you want a model that can:

- understand images;
- hear speech;
- follow video through time;
- connect a spoken reference such as "this" to a visible object;
- reason over documents;
- issue structured tool calls;
- control a robot;

then the training pipeline must contain data that teaches those behaviors.

So this lesson connects two sides of the same problem:

```text
PART A — MULTIMODALITY
What information does each modality contribute?
How can a model represent and fuse it?

PART B — DATA ENGINEERING
What data teaches those capabilities?
How do we build, filter, annotate, package, and mix it?
```

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Define a modality and explain why text can become an information bottleneck.
- Compare a cascaded speech pipeline with a native/live multimodal interface.
- Explain the roles of tokens, embeddings, visual representations, and acoustic representations.
- Explain why CLIP-style shared representation spaces are useful but are not equivalent to a full multimodal agent.
- Describe what audio contributes beyond a transcript.
- Explain how images are converted into patch-based visual representations.
- Explain why video requires temporal information in addition to visual content.
- Explain multimodal fusion using a point-and-ask example.
- Distinguish human-facing multimodal output from machine-facing structured output.
- Explain why VLM, video-model, and VLA data requirements stack on top of one another.
- Compare pretraining and post-training image-text data.
- Describe the special infrastructure challenges of video-text data.
- Explain what makes VLA datasets unusually expensive and synchronization-sensitive.
- Design a dataset-building funnel from sourcing through training-ready packaging.
- Explain why legal, licensing, privacy, safety, and quality filtering must happen early.
- Use cheap-to-expensive progressive filtering to reduce large raw datasets efficiently.
- Explain how metadata and proxy metrics can help filter millions of samples.
- Describe taxonomy-driven diversity validation.
- Compare human, model-based, and hybrid annotation.
- Explain how model-generated annotations must be validated for hallucination and corruption.
- Explain how WebDataset sharding supports large-scale distributed training.
- Compare raw media, preprocessed media, and stored embeddings as delivery formats.
- Explain why dataset mixture proportions behave like a major training hyperparameter.
- Explain catastrophic forgetting in specialized multimodal training.
- Describe how ablation studies and smaller proxy models can reduce mixture-search cost.
- Build a complete mental model from real-world sensory input to training data to model capability.

---

# PART A — HOW MULTIMODAL SYSTEMS PERCEIVE THE WORLD

## 1. The text bottleneck

For many software agents, perception historically meant text.

Examples:

```text
chat message
document
API response
transcript
structured JSON
```

Text is efficient, but it is a compressed description of reality.

Suppose a user says:

```text
"Oh, fantastic. It's raining again."
```

A transcript preserves the words.

But the original audio may also contain:

- a sigh;
- sarcastic stress;
- slow delivery;
- background rain;
- frustration in the voice.

Likewise, describing an interface in text may lose:

- exact layout;
- color;
- spacing;
- icon shape;
- where the cursor is;
- what the user is pointing at.

This creates a **text bottleneck**.

The user or application must translate high-bandwidth sensory input into words
before the model can reason about it.

Multimodal systems reduce that burden by allowing the original signals to remain
part of the interaction.

### Core idea

```text
text-only system:
world → human translation → text → model

multimodal system:
world → audio/image/video/text → model
```

The second path can preserve information that would otherwise be discarded.

---

## 2. What is a modality?

A **modality** is a type of data or communication channel.

Examples include:

| Modality | Examples |
|---|---|
| Text | prompts, documents, chat |
| Audio | speech, music, environmental sound |
| Image | photographs, screenshots, diagrams |
| Video | temporally ordered visual frames |
| Structured data | JSON, tool arguments, sensor readings |
| Action/control | motor commands, robot joint values |

A multimodal system accepts more than one type and reasons over their
relationships.

The crucial phrase is:

> **reasons over their relationships**

Simply attaching an image to a text model does not automatically create strong
multimodal understanding.

The system must learn how information in one modality relates to information in
another.

---

## 3. Cascaded pipelines versus live multimodal interfaces

### 3.1 The cascaded voice pipeline

Traditional voice systems often use several separate components.

A simplified modern cascade is:

```text
microphone
   ↓
ASR
speech → transcript
   ↓
text model / reasoning
   ↓
text response
   ↓
TTS
text → speech
   ↓
speaker
```

This architecture can work very well.

However, it introduces two important costs.

### Cost 1 — Latency

The system may need to wait for:

1. audio capture;
2. speech recognition;
3. model reasoning;
4. text generation;
5. speech synthesis.

Streaming can reduce delays, but multiple boundaries remain.

### Cost 2 — Information loss

When audio becomes plain text, the system may lose:

- pitch;
- stress;
- rhythm;
- pauses;
- environmental audio;
- overlapping speakers;
- expressive delivery.

### 3.2 Live multimodal interfaces

The second source describes a developer-facing model where one live session can
accept streams such as:

```text
audio
sampled visual frames
text
```

and return outputs such as:

```text
audio
transcription
text
tool events
```

The important engineering shift is not an unverifiable claim about every
internal component of a proprietary system.

The useful claim is at the **application boundary**:

> The developer no longer has to reduce every signal to text before the model
> can use it.

[[IMAGE_NEEDED: Cascaded versus live multimodal interface |
Left: microphone → ASR → transcript → text model → TTS → audio.
Right: one stateful live session receiving audio + visual frames + text and
returning streamed audio/text/tool events |
Learner should notice the number of explicit processing boundaries and where
information can be lost in the cascade]]

### 3.3 Stateful interaction matters

Live multimodal interaction is not only a file-upload problem.

A useful agent may need to connect:

```text
what the user said 5 seconds ago
+
what the camera shows now
+
what a tool just returned
```

inside one ongoing interaction.

That makes **state** and **timing** first-class engineering concerns.

{{exercise:M01.L04.EX01}}

---

## 4. Tokens, embeddings, and model-readable representations

Raw modalities look very different:

```text
text → characters
image → pixels
audio → waveform samples
video → image sequence + time
```

A model does not reason directly over those raw forms forever.

They are transformed into learned numerical representations.

### 4.1 Text representations

A tokenizer maps text to token IDs.

Then an embedding table maps token IDs to vectors.

```text
"multimodal"
    ↓
tokens
    ↓
token IDs
    ↓
embeddings
```

### 4.2 Visual representations

A Vision Transformer-style mental model is:

```text
image
  ↓
split into patches
  ↓
project patches into vectors
  ↓
visual token sequence
```

These "visual tokens" are a useful teaching abstraction.

They do not imply that every vision system treats image patches identically to
word tokens.

### 4.3 Audio representations

Audio begins as a waveform.

A conceptual pipeline is:

```text
waveform
  ↓
short temporal windows / feature extraction
  ↓
learned acoustic representations
```

Useful audio features can carry information related to:

- timing;
- frequency;
- energy;
- pitch;
- intonation;
- non-speech sounds.

The exact representation depends on the system.

### 4.4 Compatible spaces make fusion possible

The stable idea is:

> Each modality must be transformed into a representation the model can use
> during joint computation.

[[IMAGE_NEEDED: Modality-to-representation diagram |
Show text, image, and audio inputs each passing through their own preprocessing/
encoder path into vector representations that enter a shared multimodal context |
Learner should understand that raw media is converted into learned numerical
representations before cross-modal reasoning]]

---

## 5. CLIP as a bridge, not a complete agent

CLIP provides a useful mental model for multimodal representation learning.

It uses:

```text
image encoder
+
text encoder
```

and trains matching image-text pairs to become close in representation space.

Mismatched pairs are pushed farther apart.

This teaches a bridge such as:

```text
photo of bicycle
      ≈
"a bicycle"
```

### But CLIP is not a live multimodal assistant

CLIP-style alignment can answer questions such as:

```text
Which caption best matches this image?
Which image best matches this sentence?
```

A live multimodal agent must do more.

It may need to combine:

- speech;
- image/video;
- dialog history;
- tool results;
- structured actions.

So CLIP is best understood as one foundational idea in cross-modal alignment,
not as the whole multimodal-agent architecture.

---

## 6. What audio contributes beyond text

Speech contains linguistic content, but also information outside the literal
words.

### 6.1 Prosody and paralinguistic cues

Meaning can be affected by:

- intonation;
- emphasis;
- speaking rate;
- hesitation;
- rhythm.

A transcript may preserve none of those directly.

### 6.2 Environmental context

Audio may contain:

- sirens;
- machinery;
- music;
- keyboard sounds;
- background voices.

These signals may matter to the task.

### 6.3 Multilingual interaction

Native audio systems can sometimes support more fluid multilingual interaction
than pipelines that depend on a fixed speech-recognition language setting.

However, performance still depends on:

- model support;
- accent;
- noise;
- microphone quality;
- deployment configuration.

### 6.4 Transcripts still matter

Multimodal does not mean "text is obsolete."

Transcripts remain useful for:

- captions;
- logs;
- search;
- debugging;
- accessibility.

The difference is:

> Text becomes one representation among several, not the mandatory gateway
> through which all perception must pass.

---

## 7. What vision contributes

Images add spatial information.

A system can use visual input for more than whole-image classification.

Examples include:

- reading visible text;
- identifying objects;
- comparing regions;
- interpreting charts;
- locating a UI control;
- understanding scene relationships;
- grounding spoken references.

### 7.1 Vision Transformers as a useful model

A ViT-style image representation looks like:

```text
image
  ↓
patches
  ↓
patch embeddings
  ↓
transformer
  ↓
visual representation
```

### 7.2 Resolution matters

Visual reasoning quality can degrade with:

- tiny text;
- poor lighting;
- compression;
- low resolution;
- motion blur.

This connects directly to data engineering.

If training images never contain:

- small text;
- low-light scenes;
- unusual layouts;

then the model has less opportunity to learn robustness to them.

---

## 8. Video adds time

Video is not just "many images."

It adds **temporal structure**.

A video can encode:

```text
object appears
→ object moves
→ another object reacts
→ consequence occurs
```

The order matters.

### 8.1 Frame sampling

Sending every frame may be unnecessarily expensive.

Many live-agent workflows instead send sampled frames.

This reduces:

- bandwidth;
- token usage;
- compute.

But sampling loses temporal detail.

So it is poorly suited to tasks requiring:

- precise fast-motion analysis;
- frame-by-frame inspection;
- very short transient events.

### 8.2 Video understanding requires data that contains time

This will become important in Part B.

An image-text dataset cannot teach:

```text
what happened first?
what happened after?
what changed over 15 seconds?
```

Those require video-text supervision.

---

## 9. Multimodal fusion: connect the signals

Consider:

```text
user points at a circuit board
and asks:
"What is this part likely to be?"
```

Speech alone is incomplete.

The word:

```text
"this"
```

has no referent.

The image alone is incomplete.

The system does not know:

- which component matters;
- what the user wants to know.

The agent needs to bind:

```text
spoken phrase "this"
+
pointing gesture
+
visual region
+
conversation intent
```

This is **multimodal fusion**.

### Attention as a teaching model

Attention provides useful intuition:

```text
speech representation
       ↕
visual representation
       ↕
dialog context
```

The model learns which pieces should influence one another.

The source correctly treats this as a conceptual explanation rather than a claim
about proprietary internal attention maps.

[[IMAGE_NEEDED: Point-and-ask multimodal fusion |
Show a user pointing at one component on a circuit board while asking "What is
this part?" Then show spoken-text representation, pointing/visual-region
representation, and dialog context converging into one answer |
Learner should understand why neither speech nor image is sufficient by itself]]

{{exercise:M01.L04.EX02}}

---

## 10. Multimodal output: human-facing versus machine-facing

Multimodal systems do not only consume different modalities.

They may also produce different output types.

### 10.1 Human-facing output

Examples:

- spoken response;
- text;
- visual overlay;
- highlighted chart;
- image.

The best output depends on the task.

For example:

```text
Question:
"Which metric changed the most?"

Useful response:
spoken answer
+
visual highlight on the chart
+
short text summary
```

### 10.2 Machine-facing output

An agent may need to produce structured data such as:

```json
{
  "reading": 73,
  "unit": "psi",
  "confidence_note": "needle partially occluded"
}
```

or tool arguments:

```json
{
  "event_title": "Team review",
  "start_time": "14:00"
}
```

### Tool-use boundary

The model can request an action.

The host application should remain responsible for:

- validation;
- authorization;
- execution;
- error handling.

This becomes especially important when visual or audio interpretation can be
uncertain.

---

# PART B — THE DATA THAT TEACHES MULTIMODAL CAPABILITY

## 11. From multimodal capability to multimodal data

Now connect the previous sections to training.

A model cannot learn robust multimodal behavior from architecture alone.

It needs examples connecting modalities.

The VLM-data source emphasizes the enormous scale difference between a
traditional labeled vision task and modern multimodal training.

For one cited VLM example, the source describes millions of samples and tens of
billions of tokens across training stages.

The important lesson is not the exact number.

It is the change in engineering scale:

```text
small vision project:
thousands of labeled examples

modern multimodal training:
millions to billions of heterogeneous examples
```

### Different stages need different data

The source distinguishes:

```text
PRETRAINING
broad image-language correspondence
natural scenes
documents
infographics
diagrams

POST-TRAINING
task-oriented Q&A
reasoning
OCR
math
multi-page documents
specialized instruction following
```

So data quality and structure evolve with the learning objective.

[[IMAGE_NEEDED: Training-stage data evolution |
Show pretraining with large noisy/broad caption-style data flowing into a
general VLM, followed by post-training with smaller high-quality Q&A, OCR,
reasoning, document and task data |
Learner should see that later stages use more task-specific supervision]]

---

## 12. Data requirements stack across model types

The source presents a useful hierarchy.

| Data type | VLM | Video model | VLA |
|---|---:|---:|---:|
| Image-text pairs | ✓ | ✓ | ✓ |
| Video-text pairs | ✗ | ✓ | ✓ |
| Action/control data | ✗ | ✗ | ✓ |

This mirrors the capability stack:

```text
VLM:
see + understand language

Video model:
VLM capabilities
+
understand change through time

VLA:
visual-language understanding
+
temporal context
+
physical actions
```

A VLA system does not need robot demonstrations to relearn every visual concept.

It can inherit perception from a strong VLM and use scarce robotics data mainly
to learn:

```text
how to act given what is seen
```

This is one reason pretrained multimodal foundations are so valuable.

---

## 13. Image-text datasets: the foundation

The source identifies two common forms.

### 13.1 Image-caption pairs

Example:

```text
image
+
"A dog running through a park."
```

These teach basic visual-language correspondence.

### 13.2 Conversational multimodal data

Example:

```text
image

user:
"What animal is this?"

assistant:
"A giraffe."

user:
"What is it standing beside?"

assistant:
"A tree."
```

This teaches richer behavior such as:

- instruction following;
- dialogue;
- reasoning;
- question answering.

### 13.3 Pretraining data can be noisy

Web-scale pairs may use:

- alt text;
- filenames;
- SEO descriptions;
- nearby HTML text.

These are cheap and abundant, but often messy.

The source's examples show captions that look more like product titles or web
metadata than carefully written descriptions.

This is normal pretraining data reality:

```text
lower average annotation quality
×
huge scale
```

### 13.4 Post-training data is more curated

Later-stage datasets tend to use:

- validated conversations;
- synthetic Q&A;
- reasoning data;
- document questions;
- OCR tasks.

The key trade-off is:

```text
pretraining:
massive + noisy

post-training:
smaller + expensive + targeted
```

---

## 14. Video-text datasets teach time

Video-text data can contain several annotation styles.

### Simple caption

```text
"A person prepares a meal."
```

### Temporally grounded annotation

```text
00:15–00:23
"The person folds the top corners inward."
```

### Narrative relationship

```text
00:45 add salt
→ mixture thickens
→ 01:30 shape into balls
```

The third form teaches more than recognition.

It teaches:

- order;
- cause/effect;
- progression;
- long-range temporal structure.

### 14.1 Why video data is expensive

The source highlights four major costs.

#### Storage

A video contains many frames and can be much larger than an image.

#### Availability

Large video collections are harder to collect than web images.

#### Annotation

Fine-grained temporal annotation can take far longer than labeling one image.

#### I/O bottlenecks

Training can stall if GPUs wait for:

- video decoding;
- frame extraction;
- preprocessing.

A fast model is useless if the data pipeline cannot keep it fed.

[[IMAGE_NEEDED: Video-data cost stack |
Show one video branching into storage, frame decoding, temporal annotation, and
training I/O challenges |
Learner should understand that video data engineering is an infrastructure
problem as well as an annotation problem]]

---

## 15. Vision-language-action datasets

VLA data adds physical action.

An episode may include:

```text
language instruction
+
camera observations
+
robot state
+
joint angles
+
gripper state
+
action trajectory
```

Example instruction:

```text
"Pick up the red ball and place it in the bucket."
```

### 15.1 Synchronization is critical

Unlike an image-caption pair, a robot episode is a synchronized timeline.

The system must know that:

```text
frame at time t
↔ robot joint state at time t
↔ action command at time t
```

If streams drift apart, the example becomes misleading.

### 15.2 VLA data is scarce

You can collect images from the web.

Robot demonstrations require:

- physical hardware;
- simulation;
- teleoperation;
- experts;
- time.

So VLA datasets may be valuable even at sizes that look tiny compared with
image datasets.

### 15.3 Action representation is not standardized

The source notes two broad styles:

```text
discrete action tokens
```

versus:

```text
continuous floating-point trajectories
```

That choice affects:

- training;
- generalization;
- dataset interoperability.

---

## 16. Build datasets as a funnel

The source proposes a six-stage pipeline:

```text
1. Data sourcing
      ↓
2. Data filtering
      ↓
3. Diversity validation
      ↓
4. Data annotation
      ↓
5. Quality validation
      ↓
6. Preparing for consumption
```

This funnel is one of the most important ideas in the combined lesson.

### Why funnel design matters

Expensive work should happen **after** cheap filters have removed obvious
failures.

Do not spend a costly multimodal model call on a sample that could have been
removed using:

- missing metadata;
- invalid license;
- corrupt file check;
- trivial duration rule.

{{image:finevideo-data-pipeline}}

{{exercise:M01.L04.EX03}}

---

## 17. Data sourcing at scale

The source presents three common strategies.

### 17.1 Build proprietary/domain data

Advantages:

- directly relevant;
- often high quality;
- can cover unique edge cases.

Disadvantages:

- usually small;
- expensive to create.

### 17.2 Expand existing datasets

You can:

- add new samples;
- enrich metadata;
- add structure;
- improve annotations.

### 17.3 Crawl public web content

This can provide enormous scale.

But it creates problems around:

- licensing;
- quality;
- privacy;
- safety;
- duplication;
- broken links;
- missing metadata.

### Metadata is valuable

Keep useful associated information when available:

```text
title
caption
timestamp
source
license
duration
language
document structure
```

Metadata makes later filtering and categorization cheaper.

---

## 18. Licensing, privacy, ethics, and safety

Data collection is not only an optimization problem.

The source emphasizes that collection must respect:

- licensing;
- ethical constraints;
- privacy;
- sensitive information;
- harmful content.

Potential filters may need to remove:

- unlicensed content;
- personally identifiable information;
- extreme violence;
- hate-related material;
- other content incompatible with the dataset's intended use.

### Why this belongs early in the pipeline

If problematic samples survive until expensive annotation:

```text
you pay to process data
that you later discard
```

Worse, they may accidentally enter training.

So legal/ethical constraints should influence **sourcing and early filtering**,
not only final review.

---

## 19. Filtering millions of samples: cheap first, expensive later

Suppose you have:

```text
1.8 million candidate videos
```

If expensive analysis took one minute per video, processing serially would take
years.

The source recommends combining:

- parallelism;
- progressive filtering.

A conceptual funnel is:

```text
1.8M raw videos
     ↓
cheap metadata filter
     ↓
800K
     ↓
medium-cost semantic/filtering stage
     ↓
400K
     ↓
expensive visual analysis
     ↓
100K or fewer
```

The exact numbers are examples.

The strategy is the key:

> Never run your most expensive filter on data that a cheap rule could have
> eliminated.

### 19.1 Parallelism

Independent samples can often be split across workers:

```python
videos_per_worker = total_videos // num_workers
```

Each worker processes a different chunk.

This reduces wall-clock time.

### 19.2 Progressive filtering reduces total cost

Parallelism makes the same work faster.

A funnel removes unnecessary work entirely.

You usually want both.

---

## 20. Filtering proxies and corruption checks

Humans cannot inspect millions of items one by one.

So dataset builders use **proxies**: measurable features correlated with useful
content.

### 20.1 Audio dynamism

The source gives a simple proxy:

```text
word density =
number of caption words
/
video duration in seconds
```

A very low value may indicate a video with little spoken information.

### 20.2 Visual dynamism

The source describes using FFmpeg freeze detection to estimate whether large
parts of a video are visually static.

The implementation idea is:

```text
split video into temporal segments
      ↓
measure low-motion/frozen segments
      ↓
compute fraction
      ↓
discard if too static for the target dataset
```

The threshold is not universal.

It should be chosen by evaluating samples at different settings.

### 20.3 Corrupt-file validation

This is essential before annotation and training.

For video:

- can it open?
- can it seek?
- can frames be decoded?

For VLA:

- are camera and action streams synchronized?
- are robot states aligned with timestamps?

Why?

A corrupt sample can cause two kinds of damage.

#### During annotation

An annotation model may invent an answer when media fails to load correctly.

#### During training

The run may:

- crash;
- or learn from incorrect annotation.

---

## 21. Diversity at scale: build a taxonomy

A dataset can be large and still be narrow.

Example:

```text
1,000,000 videos
but 70% come from one content type
```

The model may become disproportionately good at that niche.

A **taxonomy** creates controlled categories for measuring and controlling
coverage.

### 21.1 You do not need a category for everything

The source recommends focusing on:

- categories you care about;
- categories you want to exclude;
- an "other" bucket.

### 21.2 Hierarchical taxonomy

A two-level taxonomy might look like:

```text
Education
├── Tutorials
├── Lectures
└── Livestreams

Entertainment
├── Gaming
├── Music
└── Movies & trailers
```

This supports:

- coarse balancing;
- fine-grained analysis;
- later slicing by users.

### 21.3 Taxonomy development is iterative

The source describes a process with:

1. synthetic initial taxonomy;
2. granularity adjustment;
3. expert refinement.

This is important.

A taxonomy should evolve after seeing real classification results.

[[IMAGE_NEEDED: Hierarchical dataset taxonomy |
Show broad categories branching into several subcategories and a separate
"other" branch, with sample counts beside each category |
Learner should see how taxonomy supports both diversity analysis and dataset
rebalancing]]

---

## 22. Categorize cheaply enough to scale

The source describes using a large language model to assign category labels
from metadata such as:

```text
title
description
channel
closed captions
```

A tightly constrained prompt asks for only one taxonomy label.

### Metadata can bias classification

An important finding in the source is that some platform-provided category tags
could bias the classifier.

Removing them improved classification quality in that workflow.

This gives a broader lesson:

> Metadata is useful evidence, but noisy metadata can also become a shortcut.

### Teacher → small classifier pattern

Running a very large model over every sample can be expensive.

A scalable alternative is:

```text
large model labels subset
        ↓
train smaller specialized classifier
        ↓
small classifier labels remaining dataset
```

This pattern mirrors a broader principle seen throughout multimodal engineering:

> Use an expensive general model to bootstrap a cheaper specialist.

---

## 23. Data annotation at scale

After filtering and diversity control, the remaining samples can be annotated.

The source presents three strategies.

### 23.1 Human annotation

Strengths:

- high quality;
- useful for subtle tasks;
- ideal for gold-standard evaluation data.

Weaknesses:

- expensive;
- slow.

### 23.2 Model-based annotation

Use a strong existing VLM to create:

- captions;
- Q&A;
- structured labels;
- reasoning-style annotations.

Advantages:

- scalable;
- much cheaper per sample.

Risk:

- hallucinations;
- inconsistent formatting;
- systematic model bias.

### 23.3 Hybrid annotation

A practical compromise:

```text
model annotates most samples
       ↓
automatic validation
       ↓
humans inspect selected examples
       ↓
refine filters/prompts
```

This is often the most realistic production strategy.

---

## 24. Build a synthetic Q&A pipeline

The source demonstrates enriching noisy web image data using a VLM.

The high-level pipeline is:

```text
stream image-text examples
      ↓
download image
      ↓
send image + instruction to VLM
      ↓
request 3 Q&A pairs in JSON
      ↓
parse result
      ↓
validate
      ↓
save enriched example
```

A simplified source-aligned prompt is:

```text
Generate 3 question-answer pairs about this image.
Return JSON:
[
  {"question": "...", "answer": "..."}
]
```

### 24.1 Why structured output helps

JSON is easier to:

- parse;
- validate;
- reject if malformed;
- transform into training format.

### 24.2 Error handling is mandatory

At internet scale, failures are normal:

- broken URL;
- timeout;
- invalid image;
- unexpected response;
- malformed JSON.

The pipeline should not crash because one sample fails.

### 24.3 Production validation should check

At minimum:

- valid structure;
- answer supported by image;
- question is answerable;
- no obvious hallucination;
- correct number of Q&A items.

{{image:docmatix-synthesis-pipeline}}

{{exercise:M01.L04.EX04}}

---

## 25. Quality validation: do not trust synthetic labels blindly

The source gives several patterns.

### 25.1 Domain-specific automatic checks

For video, reject impossible timestamps such as:

```text
annotation says 15:00
video duration = 05:00
```

### 25.2 Consistency checks

For documents:

```text
parse same page multiple times
        ↓
compare outputs
        ↓
flag contradictions
```

### 25.3 Rule-based hallucination detection

Examples:

- generated text not visible in source;
- invalid coordinate ranges;
- impossible temporal references.

### 25.4 Human spot checks

The source describes manually reviewing a small percentage of generated
annotations to discover new error modes.

This is valuable because automated filters can only catch failures that you
already know how to describe.

### Quality control is a loop

```text
annotate
  ↓
inspect
  ↓
discover failure mode
  ↓
add validator/filter
  ↓
annotate again
```

---

## 26. Preparing the dataset for consumption

A dataset is not useful at scale if training nodes cannot load it efficiently.

The source highlights **WebDataset**.

### 26.1 Shards instead of millions of tiny files

A shard is a tar archive such as:

```text
dataset-000000.tar
```

Inside:

```text
sample001.jpg
sample001.txt
sample001.json

sample002.jpg
sample002.txt
sample002.json
```

Matching basenames associate files with the same sample.

### 26.2 Why sharding helps distributed training

Instead of thousands of tiny requests, a worker downloads a manageable archive.

Different nodes can read different shards.

Example:

```text
Node 1 → shards 000000–000010
Node 2 → shards 000011–000020
Node 3 → shards 000021–000030
```

This reduces coordination and I/O overhead.

[[IMAGE_NEEDED: WebDataset sharding |
Show a large dataset split into tar shards, each shard containing image/text/
metadata files with matching basenames, then multiple training nodes reading
different shard ranges |
Learner should understand why sharding improves distributed input throughput]]

---

## 27. Raw, preprocessed, or embeddings?

The source gives three delivery choices.

| Format | Storage | Loading | Preprocessing | Flexibility |
|---|---|---|---|---|
| Raw files | largest | slowest | during training | highest |
| Preprocessed | medium | faster | paid upfront | medium |
| Embeddings | smallest | fastest | paid upfront | lowest |

### 27.1 Raw files

Store original images/videos.

Best when:

- research is changing quickly;
- different teams need different preprocessing.

Cost:

- preprocessing is repeated every training run.

### 27.2 Preprocessed files

Examples:

- resized images;
- sampled video frames;
- normalized pixels.

Best when:

- training preprocessing is stable;
- throughput matters.

Trade-off:

- future preprocessing changes may require rebuilding the dataset.

### 27.3 Precomputed embeddings

Store features from a fixed encoder.

Advantages:

- compact;
- fast loading.

Trade-off:

- locked to that encoder/representation.

This is particularly useful in:

- retrieval;
- transfer learning;
- systems where the encoder is frozen.

---

## 28. Dataset mixtures are a hidden hyperparameter

After building individual datasets, one major question remains:

> How much of each dataset should the model see?

This can have an effect comparable to architecture changes.

A general model may train on:

```text
OCR
documents
captioning
visual QA
charts
tables
reasoning
pure text
screenshots
```

The proportions matter.

### 28.1 The specialization tension

Train on too much specialized data:

```text
excellent niche performance
+
risk of losing general capabilities
```

Train on too much general data:

```text
general skills preserved
+
weak specialization
```

This creates a balance problem.

### 28.2 Catastrophic forgetting

When continued training on a narrow distribution harms previously learned
skills, we call that **catastrophic forgetting**.

For example, a document-specialized VLM might improve OCR while becoming worse
at general visual conversation if the mixture becomes too narrow.

### 28.3 Preserve some general-purpose data

The source emphasizes retaining general-purpose image-text and conversational
data during specialization when preserving broad ability matters.

The exact proportion depends on:

- amount of specialized data;
- model size;
- sensitivity to forgetting;
- whether general ability matters to the product.

---

## 29. Task-driven mixture design

The source gives examples where different model sizes benefit from different
mixture proportions.

A key finding described is:

> Smaller models may benefit from a greater share of foundational lower-level
> capabilities such as OCR/document tasks before attempting more complex
> reasoning.

This leads to an important principle:

```text
mixture design depends on model capacity
```

A mixture tuned for a larger model should not automatically be copied to a much
smaller model.

### Bridge data

The source also describes the idea of a **bridge category**.

For document specialization, examples of natural images containing text can
connect:

```text
formal document OCR
↔
real-world text recognition
```

Examples include:

- street signs;
- product labels;
- screenshots.

Bridge data can help the model generalize a specialized skill beyond the narrow
source domain.

{{image:smolvlm-data-mixture-comparison}}

{{exercise:M01.L04.EX05}}

---

## 30. Find the mixture with ablation studies

Full-scale VLM experiments are expensive.

So the source describes using smaller experiments to compare candidate mixtures.

A useful workflow is:

```text
1. define several candidate mixtures
2. train proxy models for limited steps
3. evaluate on diverse benchmarks
4. keep the strongest mixtures
5. train them longer
6. validate on a larger model
```

### 30.1 Do not judge mixtures only by training loss

Changing data distribution changes the loss landscape.

The better question is:

> Does this mixture improve the capabilities we care about?

Track validation across tasks such as:

- VQA;
- document understanding;
- multi-image reasoning;
- OCR;
- target specialization.

### 30.2 Keep ablations representative

A critical lesson from the source:

If the final run uses:

```text
70% medium-quality
20% high-quality
10% general data
```

then an ablation using:

```text
100% high-quality data
```

may not predict the final result.

The experimental distribution should resemble the intended training
distribution.

### 30.3 Scaling consistency

The source discusses research suggesting that, above an appropriate proxy model
scale and dataset size, some design choices can correlate with larger-model
results.

{{image:scaling-consistency}}

The practical takeaway is:

> Explore many ideas on cheaper proxy setups, then promote promising choices to
> expensive training runs.

Do not interpret this as a guarantee that every small-model result transfers.

---

## 31. Dataset engineering is iterative

Strong teams do not build one dataset and stop.

The loop is:

```text
build mixture
   ↓
train model
   ↓
evaluate failures
   ↓
identify missing/overrepresented data
   ↓
change filters / taxonomy / annotations / mixture
   ↓
train again
```

Examples of failure-driven changes:

```text
poor OCR
→ add more OCR/document data

hallucinated charts
→ improve chart annotation quality

weak long-video reasoning
→ increase temporally grounded examples

forgetting general conversation
→ restore general multimodal data
```

The dataset becomes part of the model-development cycle.

---

## 32. The complete multimodal mental model

Now connect both source chapters.

### Step 1 — The world produces high-bandwidth signals

```text
speech
images
video
text
environment
robot state
```

### Step 2 — Each modality becomes a model-readable representation

```text
text → token embeddings
image → visual embeddings
audio → acoustic representations
video → visual + temporal representations
actions → tokens or continuous control values
```

### Step 3 — The model learns relationships across modalities

```text
matching image ↔ caption
spoken "this" ↔ pointed object
video event ↔ timestamped description
instruction ↔ robot action
```

### Step 4 — Training data must contain those relationships

```text
image-text pairs
video-text pairs
multimodal conversations
document Q&A
temporal annotations
robot demonstrations
```

### Step 5 — Raw data must be engineered

```text
source
→ filter
→ diversify
→ annotate
→ validate
→ package
```

### Step 6 — Dataset mixtures determine capability balance

```text
general multimodal data
+
target-domain data
+
bridge data
+
text
```

### Step 7 — Evaluation feeds back into data design

```text
model failure
→ data diagnosis
→ pipeline change
→ new training run
```

That is the real multimodal development cycle.

[[IMAGE_NEEDED: End-to-end multimodal learning lifecycle |
Show real-world modalities → representations → multimodal model → output/tool
use, and underneath show the training-data path from raw media → filtering →
annotation → shards → mixture → training → evaluation → feedback to data |
Learner should connect application-time multimodality with training-time data
engineering]]

{{exercise:M01.L04.EX06}}

---

## Important misconceptions

### Misconception 1: "Multimodal just means adding an image attachment to a chat."

True multimodality requires useful relationships across modalities.

The system must connect visual, audio, text, temporal, or structured signals
rather than merely receive them independently.

### Misconception 2: "A transcript contains everything important in speech."

A transcript can discard prosody, timing, non-speech sounds, and other acoustic
context.

### Misconception 3: "Native multimodal means we know every internal architectural detail."

No.

The source explicitly distinguishes the public interface and conceptual teaching
model from unverifiable proprietary internals.

### Misconception 4: "CLIP and a multimodal conversational agent are the same thing."

CLIP aligns image and text representations.

A multimodal agent may also need dialogue state, audio, tools, video, and
generative outputs.

### Misconception 5: "Video training is just image training with more files."

Video requires temporal alignment, larger storage, expensive decoding, and
different annotation.

### Misconception 6: "A huge dataset is automatically diverse."

Large datasets can still overrepresent a narrow category.

Diversity must be measured and controlled.

### Misconception 7: "Run the best VLM on every raw sample and filter later."

That is usually too expensive.

Cheap filters should eliminate obvious failures before costly annotation or
visual analysis.

### Misconception 8: "Model-generated annotations are ground truth."

Synthetic labels can hallucinate, contradict the media, or fail structurally.

They need validation.

### Misconception 9: "Ignoring broken files is harmless."

Corrupt files can produce bad annotations, training crashes, or misleading
examples.

### Misconception 10: "Once data is cleaned, mixture proportions do not matter."

Mixture composition strongly affects what the model retains and specializes in.

### Misconception 11: "Specialization means using only specialized data."

That can cause forgetting.

General-purpose data may still be needed to preserve broader capability.

### Misconception 12: "Training loss is enough to choose a dataset mixture."

Downstream validation is more meaningful because mixture changes also change the
training-loss distribution.

---

## Key terminology

| Term | Meaning |
|---|---|
| Modality | A type of input or communication channel |
| Text bottleneck | Loss of information caused by converting richer signals into text first |
| ASR | Automatic speech recognition |
| TTS | Text-to-speech |
| Native/live multimodal interface | Developer-facing session accepting multiple modalities directly |
| Embedding | Learned numerical vector representation |
| Visual token | Teaching abstraction for vectorized visual regions/patches |
| Acoustic representation | Learned numerical representation of audio |
| Shared representation space | Space where related modalities can be compared or fused |
| Fusion | Combining information from multiple modalities for one task |
| Prosody | Rhythm, stress, intonation, and related speech characteristics |
| Temporal grounding | Connecting a description to a specific time interval |
| Structured output | Machine-readable response such as JSON or tool arguments |
| VLM | Vision-language model |
| VLA | Vision-language-action model |
| Image-caption pair | Image plus natural-language description |
| Conversational data | Multiturn image/text instruction-response examples |
| Data funnel | Progressive pipeline from raw candidates to training-ready data |
| Filtering proxy | Cheap measurable feature correlated with desired quality |
| Taxonomy | Controlled category system used for dataset analysis and balancing |
| Synthetic annotation | Labels generated by an existing model |
| Hybrid annotation | Model annotation plus strategic human validation |
| Quality validation | Checks ensuring samples and labels are trustworthy |
| WebDataset | Sharded tar-based dataset format commonly used for scalable training |
| Shard | Archive containing a subset of dataset samples |
| Preprocessed media | Media already resized/sample-normalized before training |
| Precomputed embedding | Stored feature vector from a fixed encoder |
| Dataset mixture | Combination and sampling proportions of several datasets/tasks |
| Catastrophic forgetting | Loss of previously learned abilities during narrow continued training |
| Bridge data | Data connecting a specialized domain to broader real-world capability |
| Ablation study | Controlled experiment varying one design/data choice |
| Proxy model | Smaller/cheaper model used to test decisions before full-scale runs |

---

## Self-check

Before moving on, make sure you can answer:

1. Why can text become a bottleneck for an AI agent?
2. What information can disappear when speech is converted to a transcript?
3. What is the main developer-visible difference between a cascaded voice
   pipeline and a live multimodal interface?
4. Why do text, image, and audio all need learned representations?
5. What does CLIP-style alignment teach?
6. Why is CLIP not equivalent to a multimodal conversational agent?
7. What does audio contribute beyond linguistic content?
8. Why can image resolution change VLM performance?
9. Why is video fundamentally different from a set of independent images?
10. What is multimodal fusion?
11. Why does the word "this" in a spoken question often require visual context?
12. What is the difference between human-facing and machine-facing output?
13. Why do video models require image-text data as well as video-text data?
14. What additional data does a VLA model need?
15. Why is synchronization critical in a robot demonstration?
16. What are the six stages of the dataset-building funnel?
17. Why should licensing/privacy filtering happen early?
18. What is the difference between parallel filtering and funnel filtering?
19. What is a filtering proxy?
20. Why must corrupt media be detected before annotation?
21. How does a taxonomy support diversity?
22. Why can metadata sometimes hurt classification?
23. What is the teacher-to-small-classifier strategy?
24. What are the strengths and weaknesses of human versus model annotation?
25. Why should synthetic Q&A be returned in structured format?
26. Name two ways to validate model-generated annotations.
27. Why does WebDataset help multinode training?
28. When would you store raw media instead of embeddings?
29. Why are dataset mixture proportions important?
30. What is catastrophic forgetting?
31. What is bridge data?
32. Why should mixture ablations resemble the final training distribution?
33. Why should mixture decisions be judged on validation tasks rather than only
   training loss?
34. How can model failures guide the next version of the dataset?

---

## Retain this idea

**Multimodal intelligence is learned from structured relationships between
modalities. The model architecture determines how signals can be represented and
combined; the dataset pipeline determines which relationships the model actually
gets the chance to learn. Strong multimodal systems therefore require both good
representation design and disciplined data engineering.**
""",

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "text-bottleneck", "title": "The text bottleneck", "order": 1},
            {"id": "modalities", "title": "What is a modality?", "order": 2},
            {"id": "cascade-vs-native", "title": "Cascaded vs live multimodal interfaces", "order": 3},
            {"id": "representations", "title": "Tokens, embeddings, and representations", "order": 4},
            {"id": "clip-bridge", "title": "CLIP as a bridge", "order": 5},
            {"id": "audio", "title": "What audio contributes", "order": 6},
            {"id": "vision", "title": "What vision contributes", "order": 7},
            {"id": "video-multimodal", "title": "Video adds time", "order": 8},
            {"id": "fusion", "title": "Multimodal fusion", "order": 9},
            {"id": "outputs", "title": "Human-facing and machine-facing output", "order": 10},
            {"id": "data-scale", "title": "From capability to training data", "order": 11},
            {"id": "data-stack", "title": "Stacked data requirements", "order": 12},
            {"id": "image-text-data", "title": "Image-text datasets", "order": 13},
            {"id": "video-data", "title": "Video-text datasets", "order": 14},
            {"id": "vla-data", "title": "Vision-language-action datasets", "order": 15},
            {"id": "dataset-funnel", "title": "The dataset-building funnel", "order": 16},
            {"id": "sourcing", "title": "Data sourcing at scale", "order": 17},
            {"id": "responsible-data", "title": "Licensing, privacy, ethics, and safety", "order": 18},
            {"id": "filtering", "title": "Progressive filtering", "order": 19},
            {"id": "filtering-proxies", "title": "Filtering proxies and corruption checks", "order": 20},
            {"id": "diversity", "title": "Dataset diversity and taxonomy", "order": 21},
            {"id": "categorization", "title": "Scalable categorization", "order": 22},
            {"id": "annotation", "title": "Annotation at scale", "order": 23},
            {"id": "synthetic-pipeline", "title": "Synthetic Q&A generation", "order": 24},
            {"id": "quality-validation", "title": "Quality validation", "order": 25},
            {"id": "packaging", "title": "WebDataset packaging", "order": 26},
            {"id": "delivery-formats", "title": "Raw, preprocessed, or embeddings", "order": 27},
            {"id": "mixtures", "title": "Dataset mixtures", "order": 28},
            {"id": "task-mixtures", "title": "Task-driven mixture design", "order": 29},
            {"id": "ablations", "title": "Ablation studies and proxy experiments", "order": 30},
            {"id": "iterative-data", "title": "Iterative data engineering", "order": 31},
            {"id": "combined-mental-model", "title": "The complete multimodal mental model", "order": 32},
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L04.EX01",
            "title": "Redesign a cascaded voice agent",
            "lesson_code": "M01.L04",
            "section_id": "cascade-vs-native",
            "placement": "after_section",
            "description": (
                "Compare a transcript-first architecture with a live multimodal interaction."
            ),
            "instructions": (
                "A maintenance assistant currently uses microphone → ASR → text LLM → TTS. "
                "Users often describe machine sounds and point a phone camera at the machine.\n"
                "1. Draw the current pipeline.\n"
                "2. List three types of information that can be lost before the LLM sees it.\n"
                "3. Redesign it as a live multimodal interaction using audio + sampled images + text/tool state.\n"
                "4. State one reason you might still keep transcripts."
            ),
            "expected_output": (
                "Two small architecture diagrams plus a short comparison of latency, "
                "information preservation, and logging/accessibility."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "multimodal-architecture",
                "audio",
                "vision",
                "system-design",
            ],
        },
        {
            "id": "M01.L04.EX02",
            "title": "Resolve a multimodal reference",
            "lesson_code": "M01.L04",
            "section_id": "fusion",
            "placement": "after_section",
            "description": (
                "Identify which modalities are needed to answer a point-and-ask request."
            ),
            "instructions": (
                "A user points to one connector among six on a circuit board and asks, "
                "'Can I unplug this one?'\n"
                "1. Identify what information exists in speech, image, gesture/spatial context, "
                "and conversation history.\n"
                "2. Explain why text transcription alone is insufficient.\n"
                "3. Describe the representation relationships the system must bind.\n"
                "4. State what uncertainty should be surfaced before any high-risk action."
            ),
            "expected_output": (
                "A modality-by-modality evidence table and a short fusion explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "multimodal-fusion",
                "grounding",
                "context",
                "uncertainty",
            ],
        },
        {
            "id": "M01.L04.EX03",
            "title": "Design a cheap-to-expensive dataset funnel",
            "lesson_code": "M01.L04",
            "section_id": "dataset-funnel",
            "placement": "after_section",
            "description": (
                "Build a scalable filtering pipeline for a large raw multimodal collection."
            ),
            "instructions": (
                "You have 2,000,000 candidate videos for a training dataset.\n"
                "Design at least four filtering stages from cheapest to most expensive.\n"
                "Include: licensing/metadata, corruption checks, a cheap relevance proxy, "
                "and a model-based visual analysis stage.\n"
                "For each stage, state what it removes and why it belongs at that point."
            ),
            "expected_output": (
                "A funnel diagram or table with stage, approximate relative cost, "
                "input count, output count estimate, and filtering purpose."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "data-filtering",
                "cost-optimization",
                "dataset-pipeline",
            ],
        },
        {
            "id": "M01.L04.EX04",
            "title": "Validate synthetic multimodal Q&A",
            "lesson_code": "M01.L04",
            "section_id": "synthetic-pipeline",
            "placement": "after_section",
            "description": (
                "Turn model-generated Q&A into trustworthy training data."
            ),
            "instructions": (
                "A VLM generates three Q&A pairs per image in JSON.\n"
                "Design validation checks for:\n"
                "1. JSON structure,\n"
                "2. answerability from the image,\n"
                "3. hallucinated objects/text,\n"
                "4. duplicate or trivial questions,\n"
                "5. corrupt source media.\n"
                "Then state when a sample should be escalated to a human reviewer."
            ),
            "expected_output": (
                "A validation checklist or pseudocode pipeline with pass/reject/escalate rules."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "synthetic-data",
                "quality-validation",
                "hallucination-filtering",
            ],
        },
        {
            "id": "M01.L04.EX05",
            "title": "Design a specialization mixture",
            "lesson_code": "M01.L04",
            "section_id": "task-mixtures",
            "placement": "after_section",
            "description": (
                "Balance domain expertise with preservation of general multimodal capability."
            ),
            "instructions": (
                "You are specializing a general VLM for industrial document inspection.\n"
                "Propose a mixture across:\n"
                "- industrial documents,\n"
                "- general documents/OCR,\n"
                "- natural images containing text,\n"
                "- general visual conversation,\n"
                "- pure text.\n"
                "Your percentages must sum to 100%.\n"
                "Explain which category acts as bridge data and how you would detect "
                "catastrophic forgetting."
            ),
            "expected_output": (
                "A 100% mixture table plus justification and a validation plan covering "
                "both specialized and general capabilities."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "dataset-mixture",
                "catastrophic-forgetting",
                "bridge-data",
                "evaluation",
            ],
        },
        {
            "id": "M01.L04.EX06",
            "title": "Trace capability back to training data",
            "lesson_code": "M01.L04",
            "section_id": "combined-mental-model",
            "placement": "after_section",
            "description": (
                "Connect a multimodal product requirement to the representations and data "
                "needed to learn it."
            ),
            "instructions": (
                "Design a multimodal warehouse assistant that can:\n"
                "- hear a spoken question,\n"
                "- inspect a camera frame,\n"
                "- answer about labels and damaged boxes,\n"
                "- find the relevant moment in a short video,\n"
                "- produce structured JSON for an inventory tool.\n"
                "For each capability, state the needed modality, representation concept, "
                "training-data type, and one quality check."
            ),
            "expected_output": (
                "A capability matrix connecting product behavior → modality → representation "
                "→ dataset → validation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "multimodal-system-design",
                "training-data-design",
                "fusion",
                "evaluation",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L04.QZ01",

        "title": "Multimodality and VLM Data Engineering — Knowledge Check",

        "lesson_code": "M01.L04",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L04.Q01",
                "section_id": "text-bottleneck",
                "question": "What is the text bottleneck in a multimodal system?",
                "options": [
                    "Text models always use too many parameters.",
                    "Rich sensory information may be lost when audio, images, or other signals must first be converted into text.",
                    "Text cannot be tokenized.",
                    "Images cannot contain text.",
                ],
                "correct": 1,
                "explanation": (
                    "The bottleneck is the loss of information that can occur when richer "
                    "signals are compressed into a text description or transcript."
                ),
            },
            {
                "id": "M01.L04.Q02",
                "section_id": "cascade-vs-native",
                "question": "Which sequence best describes a common cascaded voice pipeline?",
                "options": [
                    "Audio → ASR → text model → TTS",
                    "Image → FAISS → robot action",
                    "Text → image encoder → ASR",
                    "Video → tokenizer → JPEG",
                ],
                "correct": 0,
                "explanation": (
                    "The traditional cascade converts speech to text, reasons in text, then "
                    "converts the text response back to speech."
                ),
            },
            {
                "id": "M01.L04.Q03",
                "section_id": "representations",
                "question": "What common principle applies to text, image, and audio inputs?",
                "options": [
                    "They must remain in raw human-readable form throughout the model.",
                    "They are transformed into numerical representations that the model can process.",
                    "They all use exactly the same tokenizer.",
                    "They must all be converted to JPEG.",
                ],
                "correct": 1,
                "explanation": (
                    "Different modality encoders/preprocessors convert raw input into learned "
                    "representations suitable for model computation."
                ),
            },
            {
                "id": "M01.L04.Q04",
                "section_id": "clip-bridge",
                "question": "What does CLIP-style contrastive training primarily teach?",
                "options": [
                    "How to execute robot motor commands",
                    "How to align matching image and text representations",
                    "How to synthesize speech",
                    "How to shard WebDataset archives",
                ],
                "correct": 1,
                "explanation": (
                    "CLIP learns a shared semantic relationship between corresponding image "
                    "and text representations."
                ),
            },
            {
                "id": "M01.L04.Q05",
                "section_id": "audio",
                "question": "Which information can be lost in a plain speech transcript?",
                "options": [
                    "Only punctuation",
                    "Prosody, emphasis, timing, and environmental sounds",
                    "All word meaning",
                    "Image resolution",
                ],
                "correct": 1,
                "explanation": (
                    "Transcription focuses on linguistic content and may omit acoustic context "
                    "such as intonation, pauses, and non-speech sound."
                ),
            },
            {
                "id": "M01.L04.Q06",
                "section_id": "fusion",
                "question": "Why does the request 'What is this?' often require multimodal fusion?",
                "options": [
                    "The word 'this' may need visual or spatial context to identify its referent.",
                    "The word cannot be tokenized.",
                    "The image always contains the answer as text.",
                    "Speech cannot be represented numerically.",
                ],
                "correct": 0,
                "explanation": (
                    "A deictic word such as 'this' is incomplete without the scene or gesture "
                    "that indicates what the user means."
                ),
            },
            {
                "id": "M01.L04.Q07",
                "section_id": "data-stack",
                "question": "What data does a VLA model require beyond a basic image-text VLM foundation?",
                "options": [
                    "Only more captions",
                    "Video/temporal data and action/control data",
                    "Only static HTML",
                    "No additional data",
                ],
                "correct": 1,
                "explanation": (
                    "VLA capability extends visual-language understanding with temporal and "
                    "physical-action supervision."
                ),
            },
            {
                "id": "M01.L04.Q08",
                "section_id": "image-text-data",
                "question": "What broad difference does the source emphasize between pretraining and post-training image-text data?",
                "options": [
                    "Pretraining tends to be massive and noisy; post-training is smaller and more curated/task-specific.",
                    "Post-training never uses images.",
                    "Pretraining uses only human annotation.",
                    "They always use identical data distributions.",
                ],
                "correct": 0,
                "explanation": (
                    "Web-scale pretraining prioritizes breadth and scale, while later stages "
                    "use more expensive, targeted supervision."
                ),
            },
            {
                "id": "M01.L04.Q09",
                "section_id": "video-data",
                "question": "Which is NOT one of the major video-data challenges described in the lesson?",
                "options": [
                    "Storage",
                    "Annotation cost",
                    "Training I/O",
                    "Images cannot be represented as vectors",
                ],
                "correct": 3,
                "explanation": (
                    "The difficulty comes from scale, availability, annotation and I/O—not "
                    "from an inability to represent images numerically."
                ),
            },
            {
                "id": "M01.L04.Q10",
                "section_id": "vla-data",
                "question": "Why is synchronization especially important in a VLA dataset?",
                "options": [
                    "The correct visual observation, robot state, and action must correspond to the same time.",
                    "It makes image files smaller.",
                    "It eliminates the need for language instructions.",
                    "It converts continuous actions into captions automatically.",
                ],
                "correct": 0,
                "explanation": (
                    "Misaligned time streams teach the model incorrect observation-action "
                    "relationships."
                ),
            },
            {
                "id": "M01.L04.Q11",
                "section_id": "dataset-funnel",
                "question": "Why should cheap filters generally come before expensive model-based filters?",
                "options": [
                    "To reduce the number of samples that require costly analysis",
                    "Because expensive models cannot process media",
                    "Because metadata is always more accurate than vision",
                    "To increase dataset corruption",
                ],
                "correct": 0,
                "explanation": (
                    "Progressive filtering avoids spending expensive compute on samples that "
                    "could have been rejected cheaply."
                ),
            },
            {
                "id": "M01.L04.Q12",
                "section_id": "filtering-proxies",
                "question": "What is a filtering proxy?",
                "options": [
                    "A measurable feature used as an approximate signal for quality or relevance",
                    "A replacement for all human evaluation",
                    "A model checkpoint",
                    "A dataset license",
                ],
                "correct": 0,
                "explanation": (
                    "A proxy is a cheap measurable characteristic that correlates with a "
                    "desired property, even if it is not a perfect measurement."
                ),
            },
            {
                "id": "M01.L04.Q13",
                "section_id": "diversity",
                "question": "What is the main purpose of a dataset taxonomy?",
                "options": [
                    "To compress every image",
                    "To measure and control category coverage and dataset balance",
                    "To replace training labels",
                    "To increase video frame rate",
                ],
                "correct": 1,
                "explanation": (
                    "A taxonomy provides controlled categories that make diversity measurable "
                    "and supports rebalancing or filtering."
                ),
            },
            {
                "id": "M01.L04.Q14",
                "section_id": "annotation",
                "question": "What best describes a hybrid annotation strategy?",
                "options": [
                    "Humans label every sample with no automation.",
                    "Models generate most annotations while humans handle quality control and difficult cases.",
                    "No annotations are created.",
                    "Only metadata is retained.",
                ],
                "correct": 1,
                "explanation": (
                    "Hybrid pipelines combine scalable model-based generation with strategic "
                    "human review."
                ),
            },
            {
                "id": "M01.L04.Q15",
                "section_id": "quality-validation",
                "question": "Why might the same document be parsed multiple times during quality validation?",
                "options": [
                    "To increase file size",
                    "To detect contradictory or unstable generated annotations",
                    "To create more padding tokens",
                    "To avoid using a VLM",
                ],
                "correct": 1,
                "explanation": (
                    "Repeated parsing can expose inconsistency and hallucination in synthetic "
                    "document annotations."
                ),
            },
            {
                "id": "M01.L04.Q16",
                "section_id": "packaging",
                "question": "Why are WebDataset tar shards useful in distributed training?",
                "options": [
                    "They group many sample files into larger archives that different nodes can read efficiently.",
                    "They eliminate the need for storage.",
                    "They force all nodes to read the same files simultaneously.",
                    "They convert images into language automatically.",
                ],
                "correct": 0,
                "explanation": (
                    "Sharding reduces tiny-file overhead and lets workers consume independent "
                    "parts of a large dataset."
                ),
            },
            {
                "id": "M01.L04.Q17",
                "section_id": "delivery-formats",
                "question": "What is the main trade-off of storing precomputed embeddings?",
                "options": [
                    "Fast compact loading, but dependence on the encoder used to create them",
                    "Largest storage and slowest loading",
                    "No preprocessing has ever been done",
                    "They preserve unlimited flexibility",
                ],
                "correct": 0,
                "explanation": (
                    "Embeddings are efficient but lock the dataset to a specific feature "
                    "representation."
                ),
            },
            {
                "id": "M01.L04.Q18",
                "section_id": "mixtures",
                "question": "What is catastrophic forgetting in dataset-mixture design?",
                "options": [
                    "The dataset files are deleted.",
                    "Specialized continued training degrades previously learned general abilities.",
                    "A tokenizer forgets its vocabulary during inference.",
                    "A WebDataset shard is missing.",
                ],
                "correct": 1,
                "explanation": (
                    "Overly narrow specialization can harm earlier broad capabilities."
                ),
            },
            {
                "id": "M01.L04.Q19",
                "section_id": "ablations",
                "question": "Why should mixture experiments be evaluated on downstream validation tasks rather than only training loss?",
                "options": [
                    "Changing the data mixture changes the loss distribution, so lower training loss does not directly guarantee better target capabilities.",
                    "Training loss cannot be computed for VLMs.",
                    "Validation tasks are always free.",
                    "Mixture proportions do not affect loss.",
                ],
                "correct": 0,
                "explanation": (
                    "The purpose of mixture design is better capability, and training loss is "
                    "not directly comparable when the underlying data distribution changes."
                ),
            },
            {
                "id": "M01.L04.Q20",
                "section_id": "combined-mental-model",
                "type": "open",
                "question": (
                    "Explain how you would build a multimodal agent that understands speech, "
                    "camera images, and short videos. Trace the path from raw modalities to "
                    "learned representations and fusion, then describe the image-text, "
                    "video-text, annotation, filtering, packaging, and dataset-mixture "
                    "decisions needed to train the system."
                ),
            },
        ],

        "passing_score": 70,
    },
}
