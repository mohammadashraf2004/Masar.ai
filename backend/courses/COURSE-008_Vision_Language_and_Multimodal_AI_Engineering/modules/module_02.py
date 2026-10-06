"""M01.L02 — Vision Language Model Applications.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 2, "Vision Language Model Applications".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L02"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of Vision and Language"

MODULE_DESCRIPTION = (
    "Understand the major tasks modern vision-language models can perform, how "
    "those tasks differ, what model families are commonly used, how systems are "
    "evaluated, and how to implement representative workflows such as zero-shot "
    "object detection and multimodal retrieval."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Chapter 2 — page numbers not provided"


TOPIC = {
    "title": "Vision Language Model Applications",

    "slug": "vision-language-m01-l02",

    "description": (
        "Explore the applied landscape of modern VLMs: image captioning, visual "
        "question answering, reasoning, multimodal retrieval, document AI, video "
        "understanding, open-vocabulary localization, counting, segmentation, "
        "evaluation metrics, and practical model selection."
    ),

    "order": 2,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "vision-language-models",
        "image-captioning",
        "visual-question-answering",
        "visual-reasoning",
        "multimodal-retrieval",
        "ndcg",
        "document-ai",
        "multimodal-rag",
        "video-understanding",
        "zero-shot-object-detection",
        "object-counting",
        "segmentation",
        "hugging-face",
    ],

    "prerequisite_ids": [
        "M01.L01",
    ],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Vision Language Model Applications",

        "content": r"""
# Vision Language Model Applications

> **Lesson:** M01.L02  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 2, *Vision Language Model Applications*.  
> Page numbers were not included in the supplied source.  
> This lesson is an instructor-authored learning adaptation rather than a
> reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the main applied tasks supported by modern vision-language models.
- Distinguish image captioning, visual question answering, and visual reasoning.
- Explain why VQA can fail even when a model recognizes the objects in an image.
- Describe how multimodal retrieval maps images and text into a joint vector space.
- Distinguish text-to-image, image-to-text, and image-to-image retrieval.
- Calculate the intuition behind DCG and NDCG@k and explain why ranking position matters.
- Explain how modern document-understanding systems go beyond OCR.
- Describe multimodal RAG as retrieval of a relevant page followed by VLM generation.
- Explain the special challenges introduced by video and temporal relationships.
- Distinguish text-to-video retrieval from temporal grounding.
- Explain zero-shot object detection and the role of confidence thresholds.
- Use the core Hugging Face workflow for OWLv2-style open-vocabulary detection.
- Explain why VLMs can be useful for dataset annotation even when smaller vision models are better for production.
- Explain object counting as a localization-plus-aggregation problem.
- Compare open-ended segmentation output strategies such as polygons and learned mask tokens.
- Choose an appropriate evaluation benchmark or metric for several VLM application categories.

---

## 1. A map of modern VLM applications

A modern vision-language model is not limited to answering:

> "What is in this image?"

The same multimodal foundation can support several very different tasks.

A useful task map is:

```text
                        VISION + LANGUAGE
                               |
        ------------------------------------------------
        |              |             |                |
   describe        answer        retrieve         localize
   an image       a question     information       objects
        |              |             |                |
   captioning         VQA       image/document   detection
                       |           retrieval      counting
                  reasoning          |           segmentation
                                    |
                               multimodal RAG

                               +
                            VIDEO
                               |
                  temporal understanding
                  retrieval / grounding
```

Each task requires a different form of output.

| Task | Typical input | Typical output |
|---|---|---|
| Image captioning | Image | Natural-language description |
| VQA | Image + question | Focused answer |
| Visual reasoning | Image + complex question | Reasoned answer |
| Retrieval | Image/text query + database | Ranked existing items |
| Document understanding | Document image/page | Structured interpretation or answer |
| Video understanding | Video + prompt | Description/answer/timestamps |
| Object detection | Image + object text prompt | Bounding boxes + labels |
| Counting | Image/video + object prompt | Count and often points/boxes |
| Segmentation | Image + prompt | Pixel-level region/mask |

A major theme in this chapter is:

> The output format tells you what problem you are actually solving.

A model that generates text is solving a different problem from a model that
returns a ranked list, bounding boxes, timestamps, or masks.

---

## 2. Image captioning: turning visual content into language

**Image captioning** generates a natural-language description of an image.

The model must recognize more than isolated objects.

A good caption may need to represent:

- objects;
- attributes;
- actions;
- relationships;
- scene context.

For example:

```text
Input:
An image showing a child holding an umbrella beside a yellow bus.

Weak caption:
"Child. Bus."

Better caption:
"A child holding an umbrella is standing beside a yellow school bus."
```

The better caption expresses relationships and context.

### 2.1 Early encoder-decoder captioning

Early neural captioning systems commonly used:

```text
image
  ↓
CNN visual encoder
  ↓
visual representation
  ↓
RNN / LSTM text decoder
  ↓
caption tokens
```

The visual encoder summarized the image.

The text decoder then generated a caption token by token.

During training, the decoder learned to predict human-written caption text
conditioned on visual features and previous text.

[[IMAGE_NEEDED: Early image-captioning architecture |
Show an image entering a CNN encoder, the visual feature vector flowing into an
RNN/LSTM decoder, and a caption being generated word by word |
Learner should understand image captioning as an encoder-decoder mapping from
visual representation to language]]

### 2.2 Modern captioning

Modern systems typically replace those older components with:

- stronger pretrained visual encoders;
- large pretrained language models;
- multimodal connectors;
- broad image-text pretraining.

This allows generalist VLMs to generate:

- short captions;
- detailed scene descriptions;
- attribute-rich descriptions;
- contextual explanations.

### Captioning is not VQA

Captioning asks:

> "Describe this image."

VQA asks:

> "Answer this specific question about the image."

That distinction matters because the second task tells the model exactly what
visual evidence is relevant.

---

## 3. Visual Question Answering (VQA)

**Visual Question Answering** combines:

```text
image + natural-language question → answer
```

Example:

```text
Image: two cars parked beside a building

Question:
"Which car is closer to the entrance?"

Answer:
"The blue car."
```

The model must align language with the correct visual evidence.

### 3.1 Why VQA is harder than object recognition

Recognizing the objects may not be enough.

A VQA model may need to:

- count objects;
- compare objects;
- identify attributes;
- localize regions;
- interpret relative positions;
- understand interactions;
- use ordinary world knowledge.

Consider:

```text
Question:
"Which cup is likely to spill first if the table tilts left?"
```

Simply detecting "cups" is not enough.

The model must combine visual geometry and reasoning.

### 3.2 Evolution of VQA systems

Early VQA systems often looked like:

```text
image → CNN features ─┐
                      ├→ fusion → classifier → answer
question → RNN text ──┘
```

This worked for simpler questions.

Later systems added **attention**, allowing the question to guide which image
regions matter.

A question such as:

```text
"What color is the traffic light?"
```

should make the system focus on the traffic light, not the entire scene equally.

Modern VQA models use transformer-based multimodal architectures trained on
large-scale image-text data.

[[IMAGE_NEEDED: VQA evolution |
Show three stages: CNN+RNN fusion, attention-guided VQA, and transformer-based
multimodal VQA |
Learner should notice how question-conditioned visual focus becomes more
explicit and representations become more general]]

### 3.3 VQA is still imperfect

The source emphasizes several remaining weaknesses:

- multistep reasoning;
- abstract concepts;
- counterfactual "what if" questions;
- dataset bias;
- lack of transparent rationale;
- multi-turn visual conversations.

A model can also answer correctly for the wrong reason.

This is why evaluation must test whether the image is genuinely necessary.

### 3.4 MMMU and MMMU-Pro

The chapter presents **MMMU** as a multimodal benchmark spanning multiple broad
disciplines and using complex visual material such as:

- charts;
- tables;
- diagrams;
- textbook figures;
- infographics.

**MMMU-Pro** increases difficulty by:

- filtering questions that a text-only model could answer;
- making answer choices harder to guess;
- including settings where the question itself is embedded visually.

The lesson to retain is not a leaderboard number.

It is:

> A serious visual benchmark should make visual perception necessary.

{{exercise:M01.L02.EX01}}

---

## 4. Visual reasoning: when seeing is not enough

VQA can sometimes be answered from one localized observation.

**Visual reasoning** becomes important when the answer requires multiple
intermediate relationships or calculations.

Examples include:

- interpreting a supplement label and reasoning about ingredient interactions;
- calculating totals from an invoice;
- comparing values across a chart;
- solving geometry from a diagram;
- combining several visual clues.

A conceptual workflow is:

```text
visual evidence
      ↓
identify relevant elements
      ↓
relate or compare them
      ↓
perform logic/calculation
      ↓
generate answer
```

### 4.1 Why visual reasoning is difficult

A model may perceive the image only through a limited visual representation.

Then it may continue its reasoning mainly in text.

If an important detail was missed at the visual stage, later reasoning cannot
recover it reliably.

Long and complex reasoning also requires:

- sufficient context length;
- stable grounding;
- memory of intermediate evidence;
- careful interaction between visual and language representations.

### 4.2 Evaluation depends on the reasoning type

Different visual reasoning tasks require different benchmarks.

The supplied chapter names examples such as:

- **MathVista** for visual mathematics/diagram reasoning;
- **MMMU / MMMU-Pro** for broad multimodal reasoning;
- **OSWorld** for GUI/computer-use interactions.

The key principle is:

> "Visual reasoning" is not one single problem. Choose evaluation that matches
> the actual kind of reasoning required.

---

## 5. Visual-language retrieval

Generative tasks create new output.

Retrieval tasks do something different:

> Find the most relevant existing item from a collection.

A multimodal retrieval model maps inputs into a shared representation space.

Conceptually:

```text
image → encoder → vector
text  → encoder → vector
```

Semantically related items should be close.

Distance or similarity may be measured with:

- cosine similarity;
- Euclidean distance.

### 5.1 Text-to-image retrieval

Input:

```text
"a red sneaker with white laces"
```

Output:

```text
ranked images most relevant to the text
```

### 5.2 Image-to-text retrieval

Input:

```text
an image
```

Output:

```text
ranked captions/descriptions
```

### 5.3 Image-to-image retrieval

Input:

```text
query image
```

Output:

```text
visually or semantically similar images
```

### Retrieval is a ranking problem

The system does not just ask:

> "Is this result relevant?"

It asks:

> "Which relevant results should appear first?"

That is why ranking metrics matter.

---

## 6. Retrieval gets harder with documents

A natural image contains visual concepts.

A document can contain:

- paragraphs;
- small text;
- charts;
- tables;
- diagrams;
- formulas;
- layout;
- headers;
- footnotes;
- multi-column structures.

This makes document retrieval a richer multimodal task.

The source describes a major direction in modern document retrieval:
**treat the whole page visually rather than depending entirely on OCR first**.

### 6.1 Multi-vector page retrieval

The chapter describes models such as ColPali and ColQwen2 as using page-level
visual representations with finer-grained matching.

Instead of compressing an entire page into only one vector, a model can keep
multiple visual token representations.

This enables more detailed query-to-page matching.

A simplified mental model is:

```text
document page
     ↓
vision-language encoder
     ↓
[v1, v2, v3, ... vn]
     ↑
fine-grained matching
     ↑
query vectors
```

### 6.2 Single-vector retrieval

Another design compresses the whole input into one embedding.

This is simpler and often cheaper to index, but it may lose some fine-grained
information.

So retrieval systems can trade off:

- efficiency;
- storage;
- matching granularity;
- accuracy.

### 6.3 ViDoRe

The supplied chapter identifies **ViDoRe** as a major benchmark for visual
document retrieval.

The educational point is:

> Use a document-specific retrieval benchmark when your real input is
> document pages, not ordinary photographs.

---

## 7. NDCG@k: evaluating ranked retrieval results

A retrieval system should put highly relevant results near the top.

**Normalized Discounted Cumulative Gain (NDCG)** measures this.

Let's build the idea piece by piece.

### 7.1 Gain

Suppose a human evaluator assigns relevance scores:

```text
3 = highly relevant
2 = relevant
1 = weakly relevant
0 = irrelevant
```

That score is the **gain**.

### 7.2 Cumulative gain

If the top results have gains:

```text
[3, 2, 0, 1]
```

plain cumulative gain would simply add:

```text
3 + 2 + 0 + 1 = 6
```

But this treats position 1 and position 4 equally.

Search users usually care more about the top results.

### 7.3 Discount the lower positions

The chapter introduces a logarithmic discount.

A simple form is:

```text
gain_i / log2(i + 1)
```

At position 1:

```text
log2(2) = 1
```

so the first result receives no positional penalty.

At later positions, the denominator increases.

### 7.4 DCG

Using the simplified formulation from the chapter:

```text
DCG@k = Σ gain_i / log2(i + 1)
```

for positions `i = 1 ... k`.

### 7.5 Normalize

Different queries may have different numbers and grades of relevant items.

So we compare the actual DCG to the **ideal DCG (IDCG)**.

The ideal list sorts results by relevance perfectly.

Then:

```text
NDCG@k = DCG@k / IDCG@k
```

The score is between 0 and 1.

- `1.0` means perfect ordering.
- lower values mean the ranking is less ideal.

### Worked example

Suppose the system returns gains:

```text
[3, 1, 2]
```

Then:

```text
DCG@3 =
3/log2(2)
+ 1/log2(3)
+ 2/log2(4)
```

Approximately:

```text
3/1
+ 1/1.585
+ 2/2

= 3 + 0.631 + 1
= 4.631
```

The ideal ordering is:

```text
[3, 2, 1]
```

So:

```text
IDCG@3 =
3/log2(2)
+ 2/log2(3)
+ 1/log2(4)

≈ 3 + 1.262 + 0.5
≈ 4.762
```

Therefore:

```text
NDCG@3 ≈ 4.631 / 4.762 ≈ 0.972
```

A high score tells us the ranking is close to ideal.

{{exercise:M01.L02.EX02}}

---

## 8. Document understanding: beyond reading text

Retrieval finds a page.

**Document understanding** interprets the page.

Documents combine multiple information types:

```text
text
+
layout
+
tables
+
charts
+
figures
+
spatial relationships
```

Traditional systems often looked like:

```text
document
  ↓
OCR
  ↓
recognized text + bounding boxes
  ↓
handcrafted parsing rules
  ↓
structured output
```

This can work well for predictable templates.

But difficult cases include:

- poor scans;
- unusual layouts;
- handwriting;
- infographics;
- nested tables;
- diagrams;
- mixed text and visual semantics.

Modern deep-learning systems can integrate visual and linguistic information
more directly.

### 8.1 A hierarchical document-understanding pipeline

The chapter describes document understanding as several layers.

#### Layer 1 — Recognition

Detect:

- text;
- visual elements;
- layout regions.

#### Layer 2 — Structure

Identify:

- paragraphs;
- tables;
- figures;
- relationships among components.

#### Layer 3 — Meaning

Perform tasks such as:

- question answering;
- summarization;
- knowledge extraction.

A good mental model is:

```text
pixels
  ↓
recognize elements
  ↓
understand layout/structure
  ↓
combine visual + textual evidence
  ↓
extract meaning
```

[[IMAGE_NEEDED: Hierarchical document understanding |
Show a document page being decomposed into text blocks, table regions, figures,
and spatial layout, followed by a semantic reasoning layer and a final answer |
Learner should understand that document AI must reason over both content and
layout]]

### 8.2 OCR is still useful

The chapter does not claim OCR is obsolete.

OCR remains important, especially for:

- transcription;
- structured extraction;
- converting document images into text/Markdown/HTML.

It also remains challenging for:

- handwriting;
- noisy scans;
- complex media.

The chapter points to OCR-focused benchmarks such as:

- OmniDocBench;
- OlmOCRBench.

The general lesson:

> Choose evaluation based on whether you need transcription quality or semantic
> document understanding.

---

## 9. Document VQA and multimodal RAG

A document VQA task looks like:

```text
document page + question → answer
```

Older approaches often required:

- OCR text;
- bounding boxes;
- engineered layout features.

The chapter mentions LayoutLM as a representative earlier design.

Generalist VLMs can now answer many document questions more directly from
visual input.

But a harder case is:

> What if the answer is somewhere inside a large collection of documents?

Then the system needs retrieval first.

### 9.1 Multimodal RAG

A simplified pipeline is:

```text
question
  ↓
multimodal retriever
  ↓
retrieve relevant page(s)
  ↓
question + relevant page(s)
  ↓
VLM
  ↓
generated answer
```

This is **multimodal retrieval-augmented generation**.

The idea is identical in spirit to text RAG:

- retrieval narrows the evidence;
- generation interprets the retrieved evidence.

But here the retrieved evidence may be a visually rich page rather than plain
text chunks.

### Why retrieval matters

Without retrieval, a VLM might need to process every page.

That can be:

- slow;
- expensive;
- context-heavy;
- difficult to scale.

Retrieval focuses the expensive multimodal reasoning step on likely evidence.

[[IMAGE_NEEDED: Multimodal document RAG |
Show a user question entering a visual document retriever, several pages being
ranked, the top page being passed with the question into a VLM, and a grounded
answer coming out |
Learner should distinguish retrieval from generation and see why both are
needed]]

{{exercise:M01.L02.EX03}}

---

## 10. Video understanding: adding time

A video is a sequence of frames, but treating it as "just many images" misses
the central challenge:

> Time changes meaning.

A video model must represent:

- motion;
- event order;
- actions;
- interactions;
- temporal dependencies.

Example:

```text
Frame 1: person places cup on table
Frame 2: person leaves
Frame 3: cat knocks over cup
```

A single frame does not fully explain:

> "Who caused the cup to fall?"

The answer depends on temporal sequence.

### 10.1 Frame sampling

Video contains too many frames to process naively.

So systems often sample.

If you sample **too sparsely**:

- important events can disappear.

If you sample **too densely**:

- compute cost increases;
- many neighboring frames are redundant.

This creates an engineering trade-off:

```text
temporal coverage ↔ computational efficiency
```

### 10.2 Text-to-video retrieval

Input:

```text
"a deer crossing the road"
```

Output:

```text
ranked videos or clips
```

This is similar to image-text retrieval, but the visual representation must
capture temporal content.

### 10.3 Temporal grounding

Temporal grounding asks:

> "Where in the video does this event happen?"

Output might be:

```text
start: 02:14
end:   02:23
```

This is different from general video QA.

### 10.4 Evaluation categories

The chapter groups video evaluation into:

- general video understanding;
- long-video understanding;
- temporal grounding/reasoning.

It mentions benchmarks such as:

- VideoMME;
- LVBench;
- TemporalBench.

The lesson is:

> Video systems should be evaluated on the temporal behavior they are actually
> expected to perform.

---

## 11. Instance localization with language

Traditional object detectors are often trained for a fixed class set.

For example:

```text
classes = ["person", "car", "dog", "cat"]
```

A traditional detector may not understand a new free-form prompt such as:

```text
"plastic bottle caps"
```

unless the task was explicitly designed and trained for it.

Modern open-vocabulary systems can use natural language as the specification.

This opens tasks such as:

- zero-shot object detection;
- image-guided detection;
- open-ended counting;
- prompt-based segmentation.

---

## 12. Zero-shot object detection

**Zero-shot object detection** means locating objects described with open-ended
text prompts without training a new detector specifically for those labels.

Example:

```text
image + ["bee", "pink flower"]
           ↓
       detector
           ↓
bee          → bounding box
pink flower  → bounding box
```

The output includes spatial information.

### 12.1 Specialized open-vocabulary detectors

The chapter highlights models such as:

- OWLv2;
- GroundingDINO.

A high-level OWLv2-style design is:

```text
image → vision encoder ─┐
                        ├→ cross-modal matching → boxes + labels
text  → text encoder  ──┘
```

GroundingDINO uses a related multimodal detection approach with richer feature
interaction.

### 12.2 Generalist VLM detection

A generalist VLM can sometimes respond to prompts such as:

```text
"detect the bee"
```

and produce coordinate tokens or structured coordinates.

The key difference is:

- specialized detectors are built mainly for localization;
- generalist VLMs can perform many additional tasks.

### 12.3 Production trade-off

The supplied chapter makes an important practical point:

> A generalist VLM may be less cost-efficient in production than a specialized
> computer-vision detector.

However, the VLM can be extremely useful for **annotation**.

Example workflow:

```text
unlabeled factory images
       ↓
generalist VLM
"label only plastic caps"
       ↓
automatic bounding boxes
       ↓
human review
       ↓
train small specialized detector
       ↓
cheap production inference
```

This is an important engineering pattern:

> Use a powerful general model to create training data for a cheaper specialist.

[[IMAGE_NEEDED: VLM-assisted annotation pipeline |
Show raw factory images entering a generalist VLM, automatically generated
bounding boxes being reviewed, then a smaller detector being trained and
deployed |
Learner should understand how expensive general models can bootstrap efficient
task-specific models]]

---

## 13. Practical OWLv2 inference

The supplied chapter gives a Hugging Face example using
`AutoModelForZeroShotObjectDetection`.

### 13.1 Load the model

```python
import torch

from transformers import (
    AutoProcessor,
    AutoModelForZeroShotObjectDetection,
)

model_id = "google/owlv2-base-patch16-ensemble"

device = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

processor = AutoProcessor.from_pretrained(model_id)

model = (
    AutoModelForZeroShotObjectDetection
    .from_pretrained(model_id)
    .to(device)
)
```

### 13.2 Load the image and prompts

```python
import requests
from PIL import Image

image_url = (
    "https://huggingface.co/datasets/"
    "vlmbook/images/resolve/main/bee.jpg"
)

image = Image.open(
    requests.get(
        image_url,
        stream=True,
    ).raw
)

queries = [[
    "bee on the flower",
    "bee in the hive",
]]

inputs = processor(
    images=image,
    text=queries,
    return_tensors="pt",
).to(device)
```

### Important source-code note

The supplied source snippet defines:

```text
queries = ...
```

but later calls the processor using a different variable name:

```text
text_queries
```

That is inconsistent.

The instructional version above deliberately uses the same variable name
`queries` in both places.

This is a correction for executable consistency, not a conceptual change to
the chapter.

### 13.3 Run inference and post-process

```python
with torch.no_grad():
    outputs = model(**inputs)

target_sizes = [image.size[::-1]]

results = processor.post_process_grounded_object_detection(
    outputs=outputs,
    threshold=0.3,
    target_sizes=target_sizes,
    text_labels=queries,
)
```

The result structure can include:

- `boxes`;
- `scores`;
- labels/text labels.

### 13.4 Inspect detections

```python
for box, score, label in zip(
    results[0]["boxes"],
    results[0]["scores"],
    results[0]["text_labels"],
):
    coords = [
        round(value, 2)
        for value in box.tolist()
    ]

    print(
        f"Detected '{label}' "
        f"with confidence {score:.2f} "
        f"at {coords}"
    )
```

### 13.5 Bounding boxes

The returned box is typically expressed as:

```text
[x_min, y_min, x_max, y_max]
```

This is different from another common representation:

```text
[x, y, width, height]
```

Never assume the format.

Check the model documentation or processor output contract.

### 13.6 Confidence threshold

A confidence threshold filters weak detections.

For example:

```python
threshold=0.3
```

means lower-confidence predictions are removed.

If we lower the threshold:

```text
0.30 → fewer predictions
0.05 → more predictions
0.01 → many more predictions
```

This creates a precision/recall trade-off.

#### High threshold

- fewer boxes;
- usually fewer false positives;
- may miss real objects.

#### Low threshold

- more boxes;
- may recover difficult objects;
- may include more false positives.

There is no universal threshold.

Tune it for your use case.

### Another source-code note

The supplied chapter's lower-threshold demonstration contains incomplete or
inconsistent lines around the target-size setup and result count.

The conceptual point is still clear:

> Lowering the confidence threshold returns more candidate detections.

The corrected lesson avoids presenting the malformed fragment as executable
code.

{{exercise:M01.L02.EX04}}

---

## 14. Object counting

Counting sounds simple:

```text
detect all objects
  ↓
count detections
```

But the quality of the count depends on the quality of localization.

Errors happen when the system:

- misses instances;
- detects the same object multiple times;
- confuses similar objects;
- fails under occlusion;
- loses objects across video frames.

Modern VLMs may count by:

- pointing to instances;
- detecting boxes;
- tracking objects in video;
- aggregating the localized instances.

### Example

Suppose the task is:

```text
"How many boats are in the marina?"
```

A trustworthy system should ideally expose its localized instances.

This is stronger than returning only:

```text
"45"
```

because localization makes the count easier to verify.

### Counting in video

Video adds tracking.

The same boat appearing in 30 frames should not be counted 30 times.

So video counting often becomes:

```text
detect
  ↓
associate across time
  ↓
track identity
  ↓
count unique instances
```

---

## 15. Image segmentation with language prompts

Object detection answers:

> "Where is the object approximately?"

Segmentation answers:

> "Which exact pixels belong to the object?"

A prompt may look like:

```text
"segment the bird"
```

The model must return a mask or an encoding that can be converted into a mask.

### 15.1 Polygon-style output

The chapter describes Moondream2-style output using SVG-like polygon/path data.

Conceptually:

```json
{
  "path": "polygon/path representation",
  "bbox": {
    "x_min": 0.0,
    "y_min": 0.0,
    "x_max": 0.78,
    "y_max": 0.99
  }
}
```

This represents the region geometrically.

### 15.2 Tokenized mask representation

The chapter also describes a PaliGemma2-style approach.

A prompt may be:

```text
"segment bird; plant"
```

The model generates:

- localization tokens;
- segmentation codebook tokens.

A separate decoder such as a variational autoencoder then converts those tokens
into a pixel mask.

A simplified flow is:

```text
image + prompt
    ↓
multimodal model
    ↓
location tokens + segmentation tokens
    ↓
mask decoder
    ↓
pixel segmentation mask
```

### Detection vs segmentation

| Task | Spatial output |
|---|---|
| Detection | Bounding box |
| Counting | Number, often supported by points/boxes |
| Segmentation | Pixel-precise mask |

---

## 16. How to choose a model for the application

Do not begin with:

> "Which model is best?"

Begin with:

> "What output does my application need?"

### Step 1 — Define the task

Ask whether the application needs:

- a caption;
- a focused answer;
- multistep reasoning;
- ranked retrieval;
- document extraction;
- video timestamps;
- bounding boxes;
- a count;
- segmentation masks.

### Step 2 — Decide whether generation is necessary

If the goal is to retrieve existing items, a generative VLM may be unnecessary.

For retrieval, use an embedding model and vector index.

If the goal is open-ended language output, generation becomes more relevant.

### Step 3 — Consider specialization

A generalist VLM offers flexibility.

A specialized model may offer:

- lower latency;
- lower cost;
- simpler deployment;
- better task-specific behavior.

### Step 4 — Match the benchmark to the task

Examples from the supplied chapter:

| Application | Evaluation examples |
|---|---|
| Broad multimodal understanding | MMMU |
| Harder multimodal reasoning | MMMU-Pro |
| Visual mathematics | MathVista |
| GUI/computer use | OSWorld |
| Visual document retrieval | ViDoRe |
| OCR | OmniDocBench, OlmOCRBench |
| General video understanding | VideoMME |
| Long-video understanding | LVBench |
| Temporal video reasoning | TemporalBench |
| Ranked retrieval | NDCG@k |

### Step 5 — Validate on your own data

Benchmarks are useful, but application performance depends on:

- domain;
- image quality;
- prompt style;
- language;
- latency constraints;
- cost constraints;
- hardware;
- acceptable error modes.

Your own evaluation set is essential.

---

## 17. The complete mental model

The chapter can be compressed into one application-oriented framework.

### If you need a description

Use:

```text
image → VLM → caption
```

### If you need a focused answer

Use:

```text
image + question → VLM → answer
```

### If you need multiple inference steps

Use:

```text
visual evidence → reasoning → answer
```

### If you need to find relevant content

Use:

```text
query → multimodal embedding → vector search → ranked results
```

### If you need an answer from many documents

Use:

```text
question
  ↓
multimodal retriever
  ↓
relevant page
  ↓
VLM
  ↓
answer
```

### If you need video moments

Use:

```text
video + text query
  ↓
temporal model
  ↓
relevant clip/timestamps
```

### If you need locations

Use:

```text
image + text prompt
  ↓
open-vocabulary detector
  ↓
boxes
```

### If you need exact regions

Use:

```text
image + prompt
  ↓
segmentation-capable model
  ↓
mask
```

The core engineering habit is:

> Match the model architecture, output format, evaluation metric, and deployment
> strategy to the actual task instead of treating every visual problem as
> "send an image to a VLM."

---

## Important misconceptions

### Misconception 1: "Image captioning and VQA are basically the same."

They share multimodal understanding, but the task is different.

Captioning produces a general description.

VQA conditions the answer on a specific question.

### Misconception 2: "If a VLM gets a reasoning benchmark question correct, it must have reasoned correctly."

A correct answer does not prove a faithful reasoning process.

Models can exploit biases or shortcuts.

### Misconception 3: "Retrieval is just classification."

Retrieval ranks existing items by relevance.

Classification maps an input to one or more class labels.

### Misconception 4: "OCR and document understanding are identical."

OCR transcribes text.

Document understanding combines text with layout, tables, figures, and semantic
relationships.

### Misconception 5: "Video is just a batch of independent images."

Temporal order, motion, tracking, and event relationships are central.

### Misconception 6: "A lower detection threshold is always better because it finds more objects."

A lower threshold increases candidate detections but may also increase false
positives.

### Misconception 7: "A generalist VLM should replace all specialized vision models."

Generalist VLMs are flexible, but specialized models can be much cheaper and
more efficient for production.

### Misconception 8: "Object counting is independent of object localization."

Counting quality usually depends heavily on detecting, pointing to, or tracking
the instances correctly.

### Misconception 9: "A segmentation model must output every pixel directly as text."

Some systems generate compact geometric representations or learned mask tokens
that are decoded afterward.

---

## Key terminology

| Term | Meaning |
|---|---|
| Image captioning | Generating a natural-language description of an image |
| VQA | Answering a natural-language question using visual evidence |
| Visual reasoning | Combining multiple visual observations and logic to derive an answer |
| Retrieval | Ranking existing items by relevance to a query |
| Joint embedding space | Vector space where related images and text are represented near each other |
| Text-to-image retrieval | Ranking images for a text query |
| Image-to-text retrieval | Ranking text descriptions for an image query |
| Image-to-image retrieval | Ranking images for an image query |
| Cosine similarity | Similarity based on the angle between vectors |
| NDCG@k | Ranking metric rewarding highly relevant results near the top of the first k positions |
| OCR | Optical character recognition; converting visible text into machine-readable text |
| Document understanding | Interpreting text, layout, tables, figures, and document semantics |
| Document VQA | Answering questions using document content and layout |
| Multimodal RAG | Retrieving visual/document evidence before generating an answer with a VLM |
| Temporal dimension | Time relationships among video frames/events |
| Text-to-video retrieval | Ranking video clips using a text query |
| Temporal grounding | Locating the start/end time of an event described by text |
| Zero-shot detection | Detecting objects described by open-ended prompts without retraining for those classes |
| Bounding box | Rectangle identifying an object's approximate location |
| Confidence threshold | Minimum score required to retain a detection |
| Open-vocabulary detection | Detection where categories can be specified with natural language |
| Object counting | Estimating the number of object instances |
| Tracking | Maintaining object identity across video frames |
| Segmentation | Assigning object/region membership at pixel level |
| Mask | Pixel-level representation of a segmented region |
| Model card | Documentation describing model usage, limitations, and recommended settings |

---

## Self-check

Before moving on, make sure you can answer:

1. What is the difference between image captioning and VQA?
2. Why can VQA require more than object recognition?
3. What makes visual reasoning different from simple VQA?
4. Why should a good multimodal benchmark force the model to use the image?
5. What are the three retrieval directions discussed in this lesson?
6. Why is multimodal document retrieval harder than ordinary image retrieval?
7. What does NDCG reward?
8. Why do we divide DCG by ideal DCG?
9. What is the difference between OCR and document understanding?
10. What are the two main stages of multimodal RAG?
11. Why is frame sampling necessary for video models?
12. What is temporal grounding?
13. What does zero-shot object detection return?
14. Why can a generalist VLM be useful for annotation even if you do not deploy it?
15. What happens when you lower a detection confidence threshold?
16. Why does object counting benefit from localization?
17. How is segmentation spatially more precise than detection?
18. Why should model selection begin with the required output format?

---

## Retain this idea

**Vision-language applications differ mainly in what evidence must be understood
and what output must be produced. A strong engineer first defines the task
(caption, answer, ranking, timestamp, box, count, or mask), then chooses the
model, evaluation method, and deployment strategy that fit that task.**
""",

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "task-map",
                "title": "A map of modern VLM applications",
                "order": 1,
            },
            {
                "id": "image-captioning",
                "title": "Image captioning",
                "order": 2,
            },
            {
                "id": "vqa",
                "title": "Visual Question Answering",
                "order": 3,
            },
            {
                "id": "visual-reasoning",
                "title": "Visual reasoning",
                "order": 4,
            },
            {
                "id": "retrieval",
                "title": "Visual-language retrieval",
                "order": 5,
            },
            {
                "id": "document-retrieval",
                "title": "Document retrieval",
                "order": 6,
            },
            {
                "id": "ndcg",
                "title": "NDCG@k",
                "order": 7,
            },
            {
                "id": "document-understanding",
                "title": "Document understanding",
                "order": 8,
            },
            {
                "id": "doc-vqa-rag",
                "title": "Document VQA and multimodal RAG",
                "order": 9,
            },
            {
                "id": "video",
                "title": "Video understanding",
                "order": 10,
            },
            {
                "id": "localization",
                "title": "Instance localization with language",
                "order": 11,
            },
            {
                "id": "zero-shot-detection",
                "title": "Zero-shot object detection",
                "order": 12,
            },
            {
                "id": "owlv2-code",
                "title": "Practical OWLv2 inference",
                "order": 13,
            },
            {
                "id": "counting",
                "title": "Object counting",
                "order": 14,
            },
            {
                "id": "segmentation",
                "title": "Image segmentation with language prompts",
                "order": 15,
            },
            {
                "id": "model-selection",
                "title": "How to choose a model for the application",
                "order": 16,
            },
            {
                "id": "chapter-mental-model",
                "title": "The complete mental model",
                "order": 17,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L02.EX01",

            "title": "Separate captioning, VQA, and reasoning",

            "lesson_code": "M01.L02",

            "section_id": "vqa",

            "placement": "after_section",

            "description": (
                "Practice recognizing when three visually grounded tasks require "
                "different outputs and different reasoning depth."
            ),

            "instructions": (
                "Imagine an image showing three people standing beside two bicycles, "
                "with one person holding a helmet.\n"
                "1. Write one image-captioning prompt.\n"
                "2. Write one direct VQA question.\n"
                "3. Write one visual-reasoning question that requires combining at "
                "least two observations.\n"
                "4. For each, describe the expected output format."
            ),

            "expected_output": (
                "Three prompts/questions with a short explanation identifying which "
                "task each belongs to and what evidence/output it requires."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "image-captioning",
                "visual-question-answering",
                "visual-reasoning",
                "task-framing",
            ],
        },

        {
            "id": "M01.L02.EX02",

            "title": "Calculate and interpret NDCG@3",

            "lesson_code": "M01.L02",

            "section_id": "ndcg",

            "placement": "after_section",

            "description": (
                "Calculate a ranking-quality score and interpret why result order "
                "matters."
            ),

            "instructions": (
                "A retriever returns three items with relevance gains [2, 3, 1].\n"
                "1. Compute DCG@3 using gain/log2(i+1).\n"
                "2. Compute the ideal ordering.\n"
                "3. Compute IDCG@3.\n"
                "4. Compute NDCG@3.\n"
                "5. Explain why the score is below 1 even though all three relevant "
                "items were retrieved."
            ),

            "expected_output": (
                "A step-by-step calculation of DCG, IDCG, NDCG, and a short explanation "
                "of how ranking order affects the score."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "retrieval-evaluation",
                "dcg",
                "ndcg",
                "ranking",
            ],
        },

        {
            "id": "M01.L02.EX03",

            "title": "Design a multimodal document RAG pipeline",

            "lesson_code": "M01.L02",

            "section_id": "doc-vqa-rag",

            "placement": "after_section",

            "description": (
                "Design the retrieval and generation stages for question answering "
                "over visually rich documents."
            ),

            "instructions": (
                "You have 20,000 insurance-policy pages containing paragraphs, tables, "
                "charts, and scanned images. Design a multimodal RAG pipeline.\n"
                "1. State what should be indexed.\n"
                "2. Describe how a user question is embedded/searched.\n"
                "3. State what evidence is passed to the VLM.\n"
                "4. Describe the generated output.\n"
                "5. Name one retrieval metric and one answer-quality check you would use."
            ),

            "expected_output": (
                "A pipeline diagram or ordered workflow from indexing to retrieval to "
                "VLM answer generation, plus a short evaluation plan."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "document-retrieval",
                "multimodal-rag",
                "vlm",
                "evaluation",
            ],
        },

        {
            "id": "M01.L02.EX04",

            "title": "Tune an object-detection threshold",

            "lesson_code": "M01.L02",

            "section_id": "owlv2-code",

            "placement": "after_section",

            "description": (
                "Reason about confidence thresholds and production trade-offs in "
                "zero-shot object detection."
            ),

            "instructions": (
                "A detector produces candidate scores [0.91, 0.74, 0.42, 0.29, 0.08].\n"
                "1. List retained detections at thresholds 0.5, 0.3, and 0.1.\n"
                "2. Which threshold would you start with if missing a real object is "
                "very costly?\n"
                "3. Which direction would you adjust if false positives are too high?\n"
                "4. Explain why a benchmark threshold should not automatically become "
                "your production threshold."
            ),

            "expected_output": (
                "Three retained-detection sets and a short precision/recall-oriented "
                "justification for threshold selection."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "zero-shot-detection",
                "confidence-threshold",
                "precision-recall-tradeoff",
                "production-evaluation",
            ],
        },

        {
            "id": "M01.L02.EX05",

            "title": "Choose the correct VLM application pattern",

            "lesson_code": "M01.L02",

            "section_id": "model-selection",

            "placement": "after_section",

            "description": (
                "Match real-world product requirements to the correct multimodal task."
            ),

            "instructions": (
                "For each scenario, choose the most appropriate task: captioning, VQA, "
                "visual reasoning, retrieval, multimodal RAG, temporal grounding, "
                "zero-shot detection, counting, or segmentation.\n"
                "A. Find the page containing a specific clause in 5,000 scanned PDFs.\n"
                "B. Find the exact 30-second segment where a player scores.\n"
                "C. Draw a precise mask around every damaged panel in a photo.\n"
                "D. Answer 'How much tax is shown on this invoice?'.\n"
                "E. Find all 'red safety helmets' in a warehouse image."
            ),

            "expected_output": (
                "A five-row table containing scenario, chosen task, expected output, "
                "and one-sentence justification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "task-selection",
                "multimodal-system-design",
                "output-format-reasoning",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L02.QZ01",

        "title": "Vision Language Model Applications — Knowledge Check",

        "lesson_code": "M01.L02",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L02.Q01",
                "section_id": "image-captioning",
                "question": (
                    "What best distinguishes image captioning from visual question answering?"
                ),
                "options": [
                    "Captioning produces a general description, while VQA answers a specific question.",
                    "Captioning requires no visual input.",
                    "VQA can only classify images into fixed labels.",
                    "Captioning always returns bounding boxes.",
                ],
                "correct": 0,
                "explanation": (
                    "Captioning summarizes visual content broadly, while VQA conditions "
                    "the output on a user-specified question."
                ),
            },
            {
                "id": "M01.L02.Q02",
                "section_id": "vqa",
                "question": (
                    "Why can VQA be harder than simple object recognition?"
                ),
                "options": [
                    "It never uses image features.",
                    "It may require counting, comparison, localization, and relationships.",
                    "It only works on black-and-white images.",
                    "It requires a vector database for every question.",
                ],
                "correct": 1,
                "explanation": (
                    "Many visual questions require relational or structured interpretation "
                    "rather than merely naming visible objects."
                ),
            },
            {
                "id": "M01.L02.Q03",
                "section_id": "visual-reasoning",
                "question": (
                    "What most directly characterizes visual reasoning?"
                ),
                "options": [
                    "Copying OCR text exactly",
                    "Combining multiple visual observations with logic or calculation",
                    "Sorting files alphabetically",
                    "Compressing an image using DCT",
                ],
                "correct": 1,
                "explanation": (
                    "Visual reasoning requires several pieces of visual evidence to be "
                    "combined before the final answer is produced."
                ),
            },
            {
                "id": "M01.L02.Q04",
                "section_id": "retrieval",
                "question": (
                    "What is the output of a multimodal retrieval system?"
                ),
                "options": [
                    "Only newly generated prose",
                    "A ranked list of existing items",
                    "A neural-network training loss only",
                    "A segmentation mask in every case",
                ],
                "correct": 1,
                "explanation": (
                    "Retrieval identifies and ranks existing database items according "
                    "to their relevance to the query."
                ),
            },
            {
                "id": "M01.L02.Q05",
                "section_id": "ndcg",
                "question": (
                    "Why does NDCG discount results appearing lower in the ranking?"
                ),
                "options": [
                    "Lower-ranked results are always incorrect.",
                    "Search quality usually values highly relevant results more when they appear early.",
                    "The metric ignores relevance labels.",
                    "It converts images into text.",
                ],
                "correct": 1,
                "explanation": (
                    "The positional discount encodes the idea that relevant results are "
                    "more useful when users see them near the top."
                ),
            },
            {
                "id": "M01.L02.Q06",
                "section_id": "document-understanding",
                "question": (
                    "What does document understanding add beyond OCR?"
                ),
                "options": [
                    "Only a larger font size",
                    "Interpretation of layout, tables, figures, structure, and semantic relationships",
                    "A requirement to discard all text",
                    "Only video timestamps",
                ],
                "correct": 1,
                "explanation": (
                    "Document understanding integrates recognized content with spatial "
                    "and structural information."
                ),
            },
            {
                "id": "M01.L02.Q07",
                "section_id": "doc-vqa-rag",
                "question": (
                    "What is the correct high-level order in multimodal document RAG?"
                ),
                "options": [
                    "Generate first, retrieve later",
                    "Retrieve relevant visual/document evidence, then generate using that evidence",
                    "Segment every page, then ignore the question",
                    "Train a new model for every query",
                ],
                "correct": 1,
                "explanation": (
                    "RAG retrieves likely evidence first and then uses a generative model "
                    "to answer from that evidence."
                ),
            },
            {
                "id": "M01.L02.Q08",
                "section_id": "video",
                "question": (
                    "What new challenge makes video more than a collection of independent images?"
                ),
                "options": [
                    "Video has no visual information.",
                    "Temporal relationships and motion matter.",
                    "Video cannot contain text.",
                    "Video never needs sampling.",
                ],
                "correct": 1,
                "explanation": (
                    "Event order, motion, and cross-frame relationships are central to "
                    "understanding video."
                ),
            },
            {
                "id": "M01.L02.Q09",
                "section_id": "video",
                "question": (
                    "What does temporal grounding return?"
                ),
                "options": [
                    "Only a model parameter count",
                    "The time interval in which a described event occurs",
                    "A JPEG compression ratio",
                    "A list of OCR tokens only",
                ],
                "correct": 1,
                "explanation": (
                    "Temporal grounding maps a text-described event to the relevant "
                    "timestamp or time segment in a video."
                ),
            },
            {
                "id": "M01.L02.Q10",
                "section_id": "zero-shot-detection",
                "question": (
                    "What makes zero-shot object detection different from a detector "
                    "trained only on a fixed class list?"
                ),
                "options": [
                    "It can use open-ended text prompts to specify target objects.",
                    "It cannot output locations.",
                    "It requires no visual encoder.",
                    "It performs only image captioning.",
                ],
                "correct": 0,
                "explanation": (
                    "Open-vocabulary detection lets language define the target categories "
                    "without training a new detector for each requested label."
                ),
            },
            {
                "id": "M01.L02.Q11",
                "section_id": "owlv2-code",
                "question": (
                    "What usually happens when the detection confidence threshold is lowered?"
                ),
                "options": [
                    "Fewer candidate boxes are returned.",
                    "More candidate boxes are retained.",
                    "The image becomes smaller.",
                    "The text prompt is deleted.",
                ],
                "correct": 1,
                "explanation": (
                    "A lower threshold allows weaker detections to survive filtering, "
                    "which generally increases the number of returned boxes."
                ),
            },
            {
                "id": "M01.L02.Q12",
                "section_id": "counting",
                "question": (
                    "Why is localization useful for object counting?"
                ),
                "options": [
                    "It makes every object the same color.",
                    "It exposes which instances the model believes it counted.",
                    "It removes the need for visual input.",
                    "It guarantees perfect tracking.",
                ],
                "correct": 1,
                "explanation": (
                    "Boxes, points, or tracks make the counted instances explicit and "
                    "help reveal misses or duplicates."
                ),
            },
            {
                "id": "M01.L02.Q13",
                "section_id": "segmentation",
                "question": (
                    "How is segmentation more spatially precise than object detection?"
                ),
                "options": [
                    "It predicts pixel-level regions instead of only rectangular boxes.",
                    "It always produces longer text.",
                    "It cannot identify object classes.",
                    "It uses no model output.",
                ],
                "correct": 0,
                "explanation": (
                    "Segmentation identifies the object region at pixel level, whereas "
                    "detection usually localizes with a bounding box."
                ),
            },
            {
                "id": "M01.L02.Q14",
                "section_id": "model-selection",
                "question": (
                    "What should be the first question when choosing a VLM application design?"
                ),
                "options": [
                    "Which model has the longest name?",
                    "What exact task and output format does the application require?",
                    "Which benchmark has the most questions?",
                    "Can every component be replaced with a language model?",
                ],
                "correct": 1,
                "explanation": (
                    "Task definition determines whether you need generation, ranking, "
                    "timestamps, boxes, counts, or masks, which then guides model choice."
                ),
            },
            {
                "id": "M01.L02.Q15",
                "section_id": "chapter-mental-model",
                "type": "open",
                "question": (
                    "Design a VLM-based system for a company with 50,000 scanned manuals. "
                    "Users must ask questions, retrieve the most relevant page, and receive "
                    "a grounded answer. Describe the retrieval stage, generation stage, "
                    "and at least one evaluation method for each."
                ),
            },
        ],

        "passing_score": 70,
    },
}
