"""M09.L01 — Multimodal Large Language Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 9; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M09.L01"

MODULE_ORDER = 9

MODULE_TITLE = "Multimodal Large Language Models"

MODULE_DESCRIPTION = (
    "Learn how language-model systems extend beyond text by representing images "
    "with Vision Transformers, aligning image and text embeddings with CLIP, and "
    "bridging pretrained vision encoders with language models using architectures "
    "such as BLIP-2 for image captioning and visual question answering."
)

SOURCE_CHAPTER = 9

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Multimodal Large Language Models",

    "slug": "llm-foundations-m09-l01",

    "description": (
        "A practical introduction to multimodal language models: how images become "
        "patch embeddings with Vision Transformers, how CLIP aligns images and text "
        "inside a shared vector space, and how BLIP-2 connects frozen visual encoders "
        "to pretrained language models through a Q-Former."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "multimodal-llms",
        "vision-transformer",
        "vit",
        "image-patches",
        "visual-embeddings",
        "clip",
        "contrastive-learning",
        "multimodal-embeddings",
        "zero-shot-image-classification",
        "cross-modal-search",
        "blip-2",
        "q-former",
        "visual-language-models",
        "image-captioning",
        "visual-question-answering",
        "multimodal-chat",
        "module-09",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M02.L01",
        "M03.L01",
        "M04.L01",
        "M05.L01",
        "M06.L01",
        "M07.L01",
        "M08.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Multimodal Large Language Models",

        "content": (
            r"""
# Multimodal Large Language Models

> **Course:** Large Language Models Foundations  
> **Lesson:** M09.L01  
> **Module:** Multimodal Large Language Models  
> **Source alignment:** Chapter 9, “Multimodal Large Language Models.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what a **modality** is.
- Define a **multimodal model**.
- Explain why multimodality is useful for language-model applications.
- Explain how a **Vision Transformer (ViT)** converts an image into patch embeddings.
- Compare text tokenization with image patching.
- Explain why image patches cannot usually be assigned reusable vocabulary IDs like text tokens.
- Explain how image patches become numerical vectors through linear projection.
- Explain the idea of a **shared multimodal embedding space**.
- Describe the purpose of **CLIP**.
- Explain how CLIP uses separate text and image encoders.
- Explain the intuition behind **contrastive learning** for image-caption pairs.
- Use cosine similarity to compare image and text embeddings conceptually.
- Explain why negative image-text pairs are important during training.
- Describe how CLIP enables zero-shot classification, clustering, search, and generation-related workflows.
- Explain the preprocessing steps required for text and images in CLIP.
- Interpret tensor shapes such as `[1, 512]` and `[1, 3, 224, 224]`.
- Explain why matching text/image embedding dimensions matters.
- Explain the challenge of connecting a visual encoder to a pretrained language model.
- Describe the purpose of BLIP-2’s **Q-Former**.
- Explain the two broad BLIP-2 training stages.
- Explain the three tasks used in BLIP-2’s first training stage.
- Explain how visual representations can act as **soft visual prompts** to an LLM.
- Explain image captioning with a multimodal generative model.
- Explain visual question answering.
- Explain how conversation history can be manually included for multimodal chat.
- Recognize limitations caused by preprocessing, training-domain mismatch, and unsupported visual detail.

---

## 1. What does multimodal mean?

A **modality** is a type of input or information.

Examples include:

```text
text
images
audio
video
sensor data
```

A system is **multimodal** when it can work with more than one modality.

For example:

```text
text + image
```

is a multimodal input.

A model might accept:

```text
image + question
```

and generate:

```text
text answer
```

Notice something important:

> A model can accept one modality without being able to generate that same modality.

For example, a vision-language model may accept:

```text
image + text
```

but produce only:

```text
text
```

[[IMAGE_NEEDED: Multimodal model overview | Show several modalities—text, image, audio, video, sensors—feeding a multimodal model, with text as one possible output | Learner should notice that input modality support and output modality support are separate capabilities]]

### Why multimodality matters

Human communication is not purely textual.

We use:

- facial expressions,
- gestures,
- images,
- tone,
- spatial context,
- sounds.

Adding new modalities can give AI systems access to information that text alone cannot provide.

That can enable tasks such as:

```text
image captioning
visual question answering
image search
image classification
document understanding
multimodal chat
```

---

## 2. The Vision Transformer: applying Transformer ideas to images

Transformers were originally popularized for language.

But the same architecture can work on other structured sequences.

The **Vision Transformer (ViT)** applies Transformer-style processing to images.

The key problem is:

> Text can be split into tokens. How can we create an analogous sequence from an image?

The answer is:

```text
split the image into patches
```

Each patch becomes similar to an image “token.”

[[IMAGE_NEEDED: Text Transformer versus Vision Transformer | Left side shows text → tokens → embeddings → Transformer encoder; right side shows image → patches → patch embeddings → Transformer encoder | Learner should see that tokenization and patching play analogous preprocessing roles]]

---

## 3. Images become patches instead of word tokens

Imagine an image with size:

```text
512 × 512 pixels
```

A single pixel tells us very little.

But a patch containing many neighboring pixels can capture meaningful local visual structure.

ViT divides the image into fixed-size patches.

Conceptually:

```text
Image
┌────┬────┬────┐
│ P1 │ P2 │ P3 │
├────┼────┼────┤
│ P4 │ P5 │ P6 │
├────┼────┼────┤
│ P7 │ P8 │ P9 │
└────┴────┴────┘
```

Now the image has become a sequence:

```text
P1, P2, P3, ..., P9
```

The chapter uses simplified diagrams with larger visible patches for explanation and notes that the original ViT paper famously used `16 × 16` image patches.

[[IMAGE_NEEDED: Image patching | Show a single image divided into a regular grid of patches, then the patches flattened into a sequence P1, P2, P3, ... | Learner should understand image patching as the visual analogue of converting a sentence into a token sequence]]

---

## 4. Why image patches are not ordinary vocabulary tokens

Text tokenization works because tokenizers have a reusable vocabulary.

For example:

```text
token "cat"
→ token ID 9246
```

That token can appear across many documents.

Image patches are different.

A small pixel patch from one image is unlikely to appear in exactly the same form in another image.

So we generally do not build a vocabulary like:

```text
patch #17392
```

Instead:

```text
patch pixels
→ numerical projection
→ patch embedding
```

The patch becomes a vector directly.

This vector can then be processed by a Transformer encoder.

---

## 5. From raw patch pixels to patch embeddings

The patch pipeline is:

```text
image patch
    ↓
flatten pixel values
    ↓
linear projection
    ↓
dense embedding vector
```

Each patch receives a vector representation.

Then the image becomes:

```text
embedding(P1)
embedding(P2)
embedding(P3)
...
```

These patch embeddings can be fed to a Transformer encoder similarly to token embeddings.

[[IMAGE_NEEDED: Patch embedding pipeline | Show image patch → flattened pixel vector → linear projection → dense patch embedding, repeated for several patches before entering a Transformer encoder | Learner should understand how raw visual data is turned into Transformer-compatible numerical representations]]

### The big abstraction

Once both text tokens and image patches have become vectors:

```text
text token → vector
image patch → vector
```

the Transformer operates on numerical representations.

The original raw modality has already been encoded.

---

## 6. Vision Transformers create reusable image representations

Just as language encoders produce useful representations for tasks such as:

```text
classification
search
clustering
```

Vision Transformers can produce representations useful for:

```text
image classification
visual retrieval
multimodal alignment
vision-language systems
```

This representation-learning role makes ViT a natural building block for multimodal systems.

---

## 7. Multimodal embeddings: put different modalities in one vector space

In previous lessons, text embedding models mapped:

```text
text
→ vector
```

A multimodal embedding model can map:

```text
text
→ vector

image
→ vector
```

with both vectors living in the **same embedding space**.

That means we can directly compare them.

For example:

```text
text:
"a picture of a puppy"

image:
photo of a puppy
```

should ideally have similar embeddings.

[[IMAGE_NEEDED: Shared image-text embedding space | Show image embeddings and text embeddings as points in the same vector space, with matching image-caption pairs close together and unrelated pairs farther apart | Learner should understand why shared embedding geometry enables cross-modal comparison]]

---

## 8. CLIP: connect language and images through embeddings

The chapter introduces **CLIP**:

```text
Contrastive Language-Image Pre-training
```

CLIP contains two major encoder paths:

```text
Text
  ↓
Text encoder
  ↓
Text embedding
```

and:

```text
Image
  ↓
Image encoder
  ↓
Image embedding
```

The two embedding types are trained to be comparable.

This makes CLIP useful for:

- zero-shot image classification,
- clustering,
- image/text retrieval,
- multimodal search,
- representation inputs to generation systems.

[[IMAGE_NEEDED: CLIP dual encoder | Show a text encoder and an image encoder processing a caption and its matching image separately, producing two embeddings in the same vector space | Learner should see CLIP as a dual-encoder alignment model]]

---

## 9. CLIP learns from image-caption pairs

Imagine a dataset:

```text
Image A ↔ "a dog running through snow"
Image B ↔ "a red sports car"
Image C ↔ "a bowl of fruit"
```

Each training item contains:

```text
image
+
text describing that image
```

CLIP creates embeddings for both.

Then training tries to make matched pairs similar.

Conceptually:

```text
image A ↔ caption A
should be close

image A ↔ caption B
should be farther apart
```

This is a form of **contrastive learning**.

---

## 10. Contrastive learning: learn similarity by comparing positives and negatives

A positive pair is:

```text
matching image + caption
```

A negative pair is:

```text
nonmatching image + caption
```

Training encourages:

```text
positive pair
→ higher similarity

negative pair
→ lower similarity
```

This teaches the model both:

```text
what belongs together
and
what does not belong together
```

[[IMAGE_NEEDED: CLIP contrastive training matrix | Show a batch of images on one axis and captions on the other, forming a similarity matrix where diagonal matching pairs are highlighted as positives and off-diagonal pairs are negatives | Learner should understand why batch-wise contrastive learning provides both positive and negative examples]]

### Why negative examples matter

If training only says:

```text
"make matched pairs similar"
```

without distinguishing mismatched pairs, embeddings may not become discriminative enough.

Good representation learning needs structure:

```text
similar things close
different things separated
```

This connects directly to retrieval fine-tuning from Chapter 8.

---

## 11. Cosine similarity compares image and text vectors

Once the embeddings share one vector space, we can compute:

```text
similarity(
    image_embedding,
    text_embedding
)
```

The chapter uses cosine similarity.

If embeddings are normalized, the dot product gives the cosine-similarity relationship.

Conceptually:

```text
same meaning
→ smaller angle
→ higher similarity

different meaning
→ larger angle
→ lower similarity
```

A single raw score may be difficult to interpret without comparing it to other candidate pairs.

That is why the chapter expands the example into a similarity matrix containing multiple images and captions.

---

## 12. What can CLIP-style embeddings do?

### Zero-shot classification

Suppose we have one image and candidate text labels:

```text
"a photo of a dog"
"a photo of a car"
"a photo of a mountain"
```

Embed all labels and the image.

Pick the label whose vector is closest.

No task-specific classifier head is required.

### Cross-modal search

Query with text:

```text
"puppy playing in snow"
```

Retrieve matching images.

Or reverse the direction:

```text
image
→ retrieve related text
```

### Clustering

Cluster image embeddings and compare them with text concepts.

### Generation-related systems

Multimodal embeddings can also provide conditioning signals for generation architectures.

[[IMAGE_NEEDED: CLIP applications | Show a shared embedding space branching into zero-shot classification, image search from text, text search from image, clustering, and generation conditioning | Learner should understand that one aligned representation space enables many applications]]

---

## 13. Practical CLIP pipeline: tokenizer, image processor, model

The chapter loads three conceptual components.

### Text tokenizer

```python
clip_tokenizer = CLIPTokenizerFast.from_pretrained(
    model_id
)
```

### Image processor

```python
clip_processor = CLIPProcessor.from_pretrained(
    model_id
)
```

### CLIP model

```python
model = CLIPModel.from_pretrained(
    model_id
)
```

The responsibilities are:

```text
text tokenizer
→ convert text to model-compatible token IDs

image processor
→ resize/normalize image into expected tensor

CLIP model
→ produce text and image embeddings
```

This mirrors the broader lesson from earlier chapters:

> Preprocessing is part of the model interface.

---

## 14. Tokenize a CLIP caption

The source uses a caption like:

```text
a puppy playing in the snow
```

Tokenization returns:

```text
input_ids
attention_mask
```

The token sequence includes special boundary tokens such as:

```text
<|startoftext|>
...
<|endoftext|>
```

This is another reminder that multimodal systems still rely on standard text-tokenization principles on their language side.

---

## 15. Create a CLIP text embedding

The chapter uses:

```python
text_embedding = model.get_text_features(
    **inputs
)
```

The resulting shape is:

```text
[1, 512]
```

Interpretation:

```text
1 text input
×
512 embedding values
```

So one caption becomes one 512-dimensional vector.

---

## 16. Preprocess an image for CLIP

The source starts with a larger image and applies the CLIP processor.

Conceptually:

```python
processed_image = clip_processor(
    text=None,
    images=image,
    return_tensors="pt",
)["pixel_values"]
```

The chapter reports a tensor shape like:

```text
[1, 3, 224, 224]
```

Interpretation:

```text
1 image
3 channels (RGB)
224 height
224 width
```

[[IMAGE_NEEDED: Image preprocessing tensor shape | Show a normal RGB image being resized/normalized into a tensor labeled [batch=1, channels=3, height=224, width=224] | Learner should be able to interpret the four tensor dimensions]]

Preprocessing matters because the model expects a specific input size and normalization.

---

## 17. Create the image embedding

The chapter then computes:

```python
image_embedding = model.get_image_features(
    processed_image
)
```

The result also has shape:

```text
[1, 512]
```

Now we have:

```text
text embedding  → [1, 512]
image embedding → [1, 512]
```

The equal dimensions matter because we want to compare them in the same vector space.

This is one of the most important details in the CLIP architecture.

---

## 18. Compare image and caption

The chapter normalizes both embeddings and computes a dot product.

Conceptually:

```python
text_embedding = normalize(text_embedding)
image_embedding = normalize(image_embedding)

score = text_embedding @ image_embedding.T
```

The output is a similarity score.

Do not treat one score as inherently “good” or “bad” without context.

A much more useful comparison is:

```text
this image versus several captions
```

or:

```text
several images versus several captions
```

Then relative similarity becomes interpretable.

---

## 19. Higher-level CLIP usage

The chapter also shows a sentence-transformers wrapper that simplifies multimodal embedding creation.

Conceptually:

```python
model = SentenceTransformer(
    "clip-ViT-B-32"
)

image_embeddings = model.encode(images)
text_embeddings = model.encode(captions)

similarities = util.cos_sim(
    image_embeddings,
    text_embeddings,
)
```

This illustrates an important engineering principle:

```text
same underlying capability
can be exposed through different abstraction levels
```

Use lower-level APIs when you need control.

Use higher-level wrappers when convenience is more important.

---

{{exercise:M09.L01.EX01}}

---

## 20. From multimodal embeddings to multimodal generation

CLIP allows:

```text
image ↔ text comparison
```

But it does not by itself turn a text-only LLM into a conversational visual assistant.

For that we need to connect:

```text
visual representation
```

to:

```text
language-model input representation
```

This creates a **modality gap**.

A pretrained vision model speaks in one embedding representation.

A pretrained LLM expects another internal representation format.

The chapter introduces BLIP-2 as a bridge.

---

## 21. BLIP-2: connect a frozen vision encoder to a frozen LLM

Training a huge multimodal LLM from scratch would require enormous resources.

BLIP-2 uses a modular strategy:

```text
pretrained vision encoder
+
small trainable bridge
+
pretrained language model
```

The bridge is called:

```text
Q-Former
```

or:

```text
Querying Transformer
```

[[IMAGE_NEEDED: BLIP-2 high-level architecture | Show frozen Vision Transformer → trainable Q-Former → projection → frozen LLM, clearly marking which components are frozen and which bridge is trainable | Learner should understand BLIP-2 as connecting pretrained models instead of retraining everything]]

This is an efficient transfer-learning idea:

> Reuse expensive pretrained components and train the adapter between them.

---

## 22. Q-Former: bridge visual and language representations

The chapter explains that the Q-Former contains two interacting modules:

```text
Image Transformer
Text Transformer
```

with shared attention-related structure.

The image side interacts with features extracted from the frozen ViT.

The text side interacts with language.

The goal is to learn representations that make visual information usable by the language model.

---

## 23. BLIP-2 training stage 1: learn vision-language representations

The first training stage uses:

```text
image + caption pairs
```

Images go through the frozen vision encoder.

Captions go through the language-related Q-Former path.

The Q-Former then learns from three tasks.

### Image-text contrastive learning

Encourage matched image/text representations to align.

### Image-text matching

Predict whether:

```text
image
+
text
```

are a matched pair.

This is a classification problem.

### Image-grounded text generation

Generate language conditioned on visual information.

[[IMAGE_NEEDED: BLIP-2 stage 1 objectives | Show image and caption inputs entering Q-Former training with three output branches labeled contrastive alignment, image-text matching, and image-grounded text generation | Learner should remember the three complementary objectives]]

Together, these objectives teach the Q-Former to extract language-relevant visual information.

---

## 24. BLIP-2 training stage 2: convert visual representations into an LLM-compatible prompt

After stage 1, the learned Q-Former outputs contain visual information.

Now those representations need to be accepted by the LLM.

The chapter describes a projection layer that transforms them into the expected dimensionality.

Conceptually:

```text
image
  ↓
frozen ViT
  ↓
Q-Former
  ↓
projection
  ↓
LLM-compatible vectors
  ↓
language model
```

The projected vectors behave like:

```text
soft visual prompts
```

They condition the LLM on the image.

[[IMAGE_NEEDED: Soft visual prompt bridge | Show Q-Former visual outputs passing through a linear projection into a sequence of LLM-compatible embedding vectors inserted before textual prompt embeddings | Learner should understand how image information becomes conditioning context for the LLM]]

---

## 25. What is a soft visual prompt?

A normal text prompt is visible:

```text
Describe this image.
```

A soft visual prompt is different.

It consists of learned continuous vectors.

Conceptually:

```text
image
→ visual vectors
→ projected vectors
→ LLM input embedding space
```

The LLM receives these vectors as context before or alongside text.

The visual information has therefore been translated into the language model’s internal representation format.

This is the main bridge between:

```text
vision
and
language generation
```

---

## 26. BLIP-2 is one design pattern among many

The source mentions later visual language models such as:

```text
LLaVA
Idefics 2
```

Their architectures differ.

But the recurring principle is:

```text
visual encoder
→ visual features
→ projection/adapter/bridge
→ language model
```

That is the transferable architectural idea.

Specific model families will evolve, but the modality-bridging problem remains.

---

## 27. Multimodal models need multimodal preprocessing

The chapter loads:

```python
from transformers import (
    AutoProcessor,
    Blip2ForConditionalGeneration,
)
```

The processor handles:

```text
image preprocessing
+
text tokenization
```

This is analogous to combining:

```text
image processor
+
tokenizer
```

into one model-facing interface.

### Why this matters

The model expects:

- image shape,
- pixel normalization,
- text token IDs,
- attention masks,
- model-specific formatting.

A processor helps produce the correct combination.

---

## 28. BLIP-2 image preprocessing

The source starts with a non-square image.

The processor transforms it to:

```text
[1, 3, 224, 224]
```

That means the visual model receives a standardized square input.

The chapter warns that unusual aspect ratios can be distorted during preprocessing.

[[IMAGE_NEEDED: Aspect-ratio preprocessing caution | Show a wide original image being transformed into a square 224×224 model input, with visual distortion highlighted | Learner should recognize that preprocessing itself can alter visual information]]

This is a general machine-learning lesson:

> The model reasons about the processed input—not the untouched original file.

If preprocessing removes or distorts information, the model cannot recover it.

---

## 29. BLIP-2 text preprocessing

The processor also exposes the tokenizer used by the language side.

The source tokenizes a sentence and shows subword pieces.

For example, a word such as:

```text
vocalization
```

may split conceptually into pieces.

This reconnects multimodal systems to Chapter 2:

```text
image side
→ pixel preprocessing

text side
→ tokenizer
```

Both modalities require transformation before the main model can use them.

---

## 30. Use case 1 — Image captioning

Image captioning asks:

> What does this image contain?

The pipeline is:

```text
image
  ↓
processor
  ↓
visual encoder / multimodal bridge
  ↓
language model
  ↓
caption tokens
  ↓
decoded caption
```

The chapter’s example produces a caption similar to:

```text
an orange supercar driving on the road at sunset
```

[[IMAGE_NEEDED: Image captioning pipeline | Show an image entering processor → vision encoder/Q-Former → LLM → generated caption | Learner should understand captioning as visual input conditioned text generation]]

The exact wording can vary.

The important idea is that the model converts visual evidence into generated language.

---

## 31. Captioning quality depends on training coverage

A model trained mainly on common public image-caption data may perform well on:

```text
cars
animals
common scenes
objects
```

but struggle with:

```text
rare scientific images
company-specific diagrams
specialized machinery
fictional characters
medical imagery
domain-specific visual conventions
```

This is the multimodal version of domain shift.

Do not assume a general-purpose visual-language model fully understands every visual domain.

---

## 32. Ambiguous images reveal interpretation, not objective truth

The source shows a Rorschach inkblot example.

The model captions it as something like a bat.

This is useful for understanding ambiguity.

Some images do not have one objectively correct semantic interpretation.

A model output may reflect:

- training patterns,
- learned visual associations,
- prompt wording.

In ambiguous cases, the answer should be interpreted as:

```text
a plausible model interpretation
```

rather than guaranteed truth.

---

## 33. Use case 2 — Visual question answering

Image captioning uses:

```text
image only
→ text
```

Visual Question Answering (VQA) uses:

```text
image
+
question
→ answer
```

Example:

```text
Image:
sports car at sunset

Question:
What do you see in this picture?

Answer:
A sports car driving on a road at sunset.
```

The model must process both modalities together.

[[IMAGE_NEEDED: Visual question answering | Show an image and textual question entering the multimodal model together, producing a text answer tied to visual evidence | Learner should distinguish VQA from unconditional image captioning]]

---

## 34. A prompt changes image generation behavior

Without a question, the model may produce a generic caption.

With a question:

```text
Question: What color is the car?
Answer:
```

the same visual representation is used differently.

This shows that multimodal generation combines:

```text
visual context
+
textual instruction
```

The prompt tells the language model which part of the visual information matters for the task.

---

## 35. From VQA to multimodal chat

The chapter extends visual question answering into multiple turns.

Conceptually:

```text
Image
+
Question 1
+
Answer 1
+
Question 2
→ Answer 2
```

Earlier conversation is manually included in the prompt.

This is the same memory principle from Chapter 7:

> A model “remembers” earlier turns when the application includes them in later context.

[[IMAGE_NEEDED: Multimodal chat memory | Show one persistent image plus conversation history—Q1/A1, Q2/A2—being assembled into the next multimodal prompt | Learner should connect multimodal chat with application-managed conversation memory]]

---

## 36. Multimodal chat still needs application-level memory

The source builds a list:

```python
memory = []
```

and appends:

```text
(question, generated_answer)
```

after each turn.

When a new question arrives, the application reconstructs prior conversation text and sends it again.

That means:

```text
model
does not automatically remember

application
stores history

prompt
reintroduces history
```

This is the same principle whether the conversation is:

```text
text-only
or
image + text
```

---

## 37. Common multimodal failure sources

A multimodal system can fail at several stages.

### Visual preprocessing failure

The input image may be:

- resized badly,
- cropped,
- distorted,
- too low resolution.

### Visual encoder failure

The visual features may not represent important domain-specific details.

### Modality-bridge failure

The projection between image and LLM representations may lose information.

### Language-model failure

The LLM may:

- hallucinate details,
- overinterpret the image,
- rely on priors rather than actual visual evidence.

### Prompt failure

The question may be ambiguous.

A strong multimodal system therefore needs debugging by stage.

---

## 38. CLIP and BLIP-2 solve different problems

This distinction is worth remembering.

### CLIP-style model

Best mental model:

```text
image
↔
text
similarity
```

Primary capability:

```text
shared representation space
```

Useful for:

```text
search
classification
clustering
cross-modal retrieval
```

### BLIP-2-style model

Best mental model:

```text
image
+
text prompt
→
generated language
```

Primary capability:

```text
condition a generative LLM on visual information
```

Useful for:

```text
captioning
VQA
multimodal chat
```

[[IMAGE_NEEDED: CLIP versus BLIP-2 | Side-by-side diagram: CLIP maps image/text to shared embeddings for similarity, while BLIP-2 maps image features through Q-Former/projection into an LLM for text generation | Learner should clearly distinguish multimodal retrieval embeddings from multimodal generation]]

---

## 39. Put the complete chapter together

The chapter can be understood as three architectural layers.

### Layer 1 — Represent images with Transformers

```text
image
→ patches
→ patch embeddings
→ Vision Transformer
→ visual representation
```

### Layer 2 — Align image and text representations

```text
image encoder
→ image embedding
                 ↘
                shared vector space
                 ↗
text encoder
→ text embedding
```

This gives us CLIP-style multimodal embeddings.

### Layer 3 — Feed visual information into a language generator

```text
image
→ visual encoder
→ Q-Former
→ projection
→ soft visual prompt
→ LLM
→ text response
```

This gives us BLIP-2-style multimodal generation.

[[IMAGE_NEEDED: Complete multimodal architecture map | Show three stacked stages: ViT patch representation, CLIP shared image-text embedding alignment, and BLIP-2 visual-to-language generation bridge | Learner should use this figure as the chapter’s final mental map]]

---

{{exercise:M09.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> A multimodal model must generate every modality it accepts.

### Why this is wrong

A model may accept images and text while generating only text.

---

### Misconception 2

> Vision Transformers assign image patches vocabulary IDs just like word tokens.

### Why this is wrong

Image patches are usually linearly projected into continuous embeddings rather than looked up from a reusable discrete text vocabulary.

---

### Misconception 3

> CLIP uses one encoder for both raw text and raw pixels.

### Why this is wrong

CLIP uses modality-specific encoders whose outputs are trained to occupy a comparable shared embedding space.

---

### Misconception 4

> If image and text embeddings both have 512 dimensions, they are automatically semantically aligned.

### Why this is wrong

Matching shape is necessary for direct comparison, but training is what makes corresponding concepts occupy related regions.

---

### Misconception 5

> CLIP is primarily a text-generation model.

### Why this is wrong

CLIP is primarily a multimodal representation/alignment model. It creates comparable image and text embeddings.

---

### Misconception 6

> BLIP-2 trains both the vision encoder and LLM from scratch.

### Why this is wrong

The chapter’s central BLIP-2 idea is to reuse frozen pretrained components and train a bridge between them.

---

### Misconception 7

> Soft visual prompts are normal text captions.

### Why this is wrong

They are continuous learned vectors that condition the LLM internally.

---

### Misconception 8

> A visual-language model sees the exact original image.

### Why this is wrong

The image is resized, normalized, and otherwise preprocessed before inference.

---

### Misconception 9

> Multimodal chat automatically remembers prior turns.

### Why this is wrong

The chapter manually stores previous Q/A pairs and rebuilds the later prompt from them.

---

### Misconception 10

> A confident visual answer proves the image contains that information.

### Why this is wrong

The language model can still hallucinate or rely on learned priors. Visual grounding must be evaluated.

---

## Key terminology

| Term | Meaning |
|---|---|
| Modality | Type of information such as text, image, audio, or video |
| Multimodal model | Model able to process more than one modality |
| Vision Transformer (ViT) | Transformer architecture that processes image patches |
| Image patch | Local rectangular region of an image used as a visual sequence element |
| Patch embedding | Dense vector created from an image patch |
| Linear projection | Learned transformation that maps raw patch features into embedding space |
| Visual encoder | Model that converts images into learned feature representations |
| Multimodal embedding | Vector representation aligned across more than one modality |
| CLIP | Contrastive Language-Image Pre-training model family |
| Shared embedding space | Vector space where comparable image and text concepts can be directly compared |
| Contrastive learning | Training approach that pulls matched examples together and pushes mismatched examples apart |
| Positive pair | Matching image-text pair |
| Negative pair | Nonmatching image-text pair |
| Cosine similarity | Similarity measure based on vector direction |
| Zero-shot image classification | Classifying an image by comparing its embedding to textual class descriptions |
| Cross-modal retrieval | Retrieving one modality using a query from another modality |
| BLIP-2 | Architecture connecting pretrained visual and language models through a trainable bridge |
| Q-Former | Querying Transformer used by BLIP-2 to bridge vision and language |
| Image-text matching | Task that predicts whether image and text belong together |
| Image-grounded generation | Generating text conditioned on image information |
| Soft visual prompt | Continuous visual-derived embedding sequence used to condition an LLM |
| Processor | Model-specific preprocessing interface for image and/or text |
| Image captioning | Generating descriptive text from an image |
| Visual Question Answering (VQA) | Answering a text question using visual input |
| Multimodal chat | Multi-turn interaction involving visual and textual context |
| Domain shift | Performance degradation when deployment data differs from training data |

---

## Self-check

Before moving on, make sure you can answer:

1. What is a modality?
2. What makes a model multimodal?
3. Why might multimodality increase the usefulness of LLM systems?
4. Why can’t ordinary word tokenization be applied directly to images?
5. How does ViT create an image sequence?
6. What happens to each image patch before entering the Transformer?
7. Why are patch embeddings analogous to token embeddings?
8. What does a shared multimodal embedding space enable?
9. What are the two encoder paths in CLIP?
10. What is a positive CLIP training pair?
11. Why are negative pairs necessary?
12. How does cosine similarity help compare image and text?
13. What is zero-shot image classification with CLIP?
14. What does `[1, 512]` represent for a CLIP embedding?
15. What does `[1, 3, 224, 224]` represent for an image tensor?
16. Why must text and image embeddings occupy a compatible vector space?
17. What problem does BLIP-2 solve?
18. What is the role of the Q-Former?
19. What are the three first-stage BLIP-2 training objectives?
20. What happens during BLIP-2’s second stage?
21. What is a soft visual prompt?
22. How is CLIP different from BLIP-2?
23. What is image captioning?
24. How does visual question answering differ from captioning?
25. How does the chapter create multimodal conversation memory?
26. Why can image preprocessing cause errors?
27. Why can domain-specific imagery be difficult?
28. Explain the full progression: image → patches → visual embedding → multimodal alignment → language generation.

---

## Retain this idea

**Multimodal language systems become possible by translating different forms of raw data into compatible numerical representations. Vision Transformers turn images into sequences of patch embeddings. CLIP aligns visual and textual representations inside one shared vector space, enabling cross-modal similarity, search, clustering, and zero-shot classification. BLIP-2 goes further by bridging a visual encoder to a pretrained LLM through the Q-Former and projection layers, turning visual features into soft prompts that condition text generation. The core pattern is always the same: represent each modality, align or project those representations, and then use them for the downstream task.**
"""
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "what-is-multimodality", "title": "What does multimodal mean?", "order": 1},
            {"id": "vision-transformer", "title": "The Vision Transformer: applying Transformer ideas to images", "order": 2},
            {"id": "image-patches", "title": "Images become patches instead of word tokens", "order": 3},
            {"id": "patch-vs-token", "title": "Why image patches are not ordinary vocabulary tokens", "order": 4},
            {"id": "patch-embedding", "title": "From raw patch pixels to patch embeddings", "order": 5},
            {"id": "vision-representation", "title": "Vision Transformers create reusable image representations", "order": 6},
            {"id": "multimodal-embeddings", "title": "Multimodal embeddings: put different modalities in one vector space", "order": 7},
            {"id": "clip", "title": "CLIP: connect language and images through embeddings", "order": 8},
            {"id": "clip-training-data", "title": "CLIP learns from image-caption pairs", "order": 9},
            {"id": "contrastive-learning", "title": "Contrastive learning: learn similarity by comparing positives and negatives", "order": 10},
            {"id": "cosine-similarity", "title": "Cosine similarity compares image and text vectors", "order": 11},
            {"id": "clip-use-cases", "title": "What can CLIP-style embeddings do?", "order": 12},
            {"id": "clip-components", "title": "Practical CLIP pipeline: tokenizer, image processor, model", "order": 13},
            {"id": "clip-text", "title": "Tokenize a CLIP caption", "order": 14},
            {"id": "clip-text-embedding", "title": "Create a CLIP text embedding", "order": 15},
            {"id": "clip-image-processing", "title": "Preprocess an image for CLIP", "order": 16},
            {"id": "clip-image-embedding", "title": "Create the image embedding", "order": 17},
            {"id": "similarity-example", "title": "Compare image and caption", "order": 18},
            {"id": "sentence-transformers-clip", "title": "Higher-level CLIP usage", "order": 19},
            {"id": "from-embeddings-to-generation", "title": "From multimodal embeddings to multimodal generation", "order": 20},
            {"id": "blip2", "title": "BLIP-2: connect a frozen vision encoder to a frozen LLM", "order": 21},
            {"id": "qformer", "title": "Q-Former: bridge visual and language representations", "order": 22},
            {"id": "blip-stage1", "title": "BLIP-2 training stage 1: learn vision-language representations", "order": 23},
            {"id": "blip-stage2", "title": "BLIP-2 training stage 2: convert visual representations into an LLM-compatible prompt", "order": 24},
            {"id": "soft-prompt", "title": "What is a soft visual prompt?", "order": 25},
            {"id": "modern-vlms", "title": "BLIP-2 is one design pattern among many", "order": 26},
            {"id": "blip-preprocessing", "title": "Multimodal models need multimodal preprocessing", "order": 27},
            {"id": "image-preprocessing", "title": "BLIP-2 image preprocessing", "order": 28},
            {"id": "text-preprocessing", "title": "BLIP-2 text preprocessing", "order": 29},
            {"id": "captioning", "title": "Use case 1 — Image captioning", "order": 30},
            {"id": "captioning-limitations", "title": "Captioning quality depends on training coverage", "order": 31},
            {"id": "subjective-images", "title": "Ambiguous images reveal interpretation, not objective truth", "order": 32},
            {"id": "vqa", "title": "Use case 2 — Visual question answering", "order": 33},
            {"id": "vqa-prompt", "title": "A prompt changes image generation behavior", "order": 34},
            {"id": "multimodal-chat", "title": "From VQA to multimodal chat", "order": 35},
            {"id": "multimodal-memory", "title": "Multimodal chat still needs application-level memory", "order": 36},
            {"id": "multimodal-limitations", "title": "Common multimodal failure sources", "order": 37},
            {"id": "clip-vs-blip", "title": "CLIP and BLIP-2 solve different problems", "order": 38},
            {"id": "full-pipeline", "title": "Put the complete chapter together", "order": 39},
            {"id": "misconceptions", "title": "Important misconceptions", "order": 40},
            {"id": "terminology", "title": "Key terminology", "order": 41},
            {"id": "self-check", "title": "Self-check", "order": 42},
            {"id": "retain", "title": "Retain this idea", "order": 43},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M09.L01.EX01",

            "title": "Explore a Shared Image-Text Embedding Space",

            "lesson_code": "M09.L01",

            "section_id": "sentence-transformers-clip",

            "placement": "after_section",

            "description": (
                "Practice CLIP-style multimodal embeddings and learn to interpret "
                "relative similarities rather than isolated scores."
            ),

            "instructions": (
                "Prepare 4–6 images with clear semantic differences and write 4–6 "
                "candidate captions or class descriptions.\n"
                "1. Load a CLIP-compatible model.\n"
                "2. Encode every image into an embedding.\n"
                "3. Encode every text description into an embedding.\n"
                "4. Print both embedding matrix shapes and explain the dimensions.\n"
                "5. Normalize the embeddings if required by your chosen API.\n"
                "6. Calculate the full image-text cosine-similarity matrix.\n"
                "7. For each image, rank all candidate texts from most similar to least similar.\n"
                "8. Identify at least one correct strong match and one surprising mismatch.\n"
                "9. Explain why a single similarity score is harder to interpret than "
                "relative scores across multiple candidates.\n"
                "10. Describe how this same workflow could support zero-shot image "
                "classification or text-to-image retrieval."
            ),

            "expected_output": (
                "A notebook or report containing image/text embedding shapes, the "
                "similarity matrix, ranked text candidates for each image, one error "
                "analysis, and an explanation of zero-shot classification or cross-modal search."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "clip",
                "multimodal-embeddings",
                "cosine-similarity",
                "zero-shot-classification",
                "cross-modal-retrieval",
            ],
        },

        {
            "id": "M09.L01.EX02",

            "title": "Design a Multimodal Visual Assistant",

            "lesson_code": "M09.L01",

            "section_id": "full-pipeline",

            "placement": "after_section",

            "description": (
                "Connect image preprocessing, visual encoding, multimodal bridging, "
                "language generation, conversation memory, and output validation."
            ),

            "instructions": (
                "Design a visual assistant for product-support images.\n"
                "1. Define what image formats and sizes the application accepts.\n"
                "2. Describe the preprocessing pipeline and explain one possible "
                "distortion or information-loss risk.\n"
                "3. Explain how a Vision Transformer converts the processed image "
                "into visual representations.\n"
                "4. Explain how a BLIP-2-style bridge could turn those representations "
                "into LLM-compatible soft visual prompts.\n"
                "5. Define one image-captioning task and one visual-question-answering task.\n"
                "6. Add multi-turn conversation memory and explain what information is "
                "stored outside the model.\n"
                "7. Define at least four multimodal failure cases, including one caused "
                "by preprocessing and one caused by model hallucination.\n"
                "8. Define how the application should respond when visual evidence is insufficient.\n"
                "9. Compare where a CLIP-style model would be useful in this application "
                "versus where a BLIP-2-style generative model would be useful.\n"
                "10. Draw or write the complete architecture from uploaded image to final answer."
            ),

            "expected_output": (
                "An architecture diagram or structured design covering preprocessing, "
                "vision encoding, modality bridging, generation, memory, CLIP-style "
                "retrieval/classification options, failure handling, and validation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "vision-transformer",
                "blip-2",
                "q-former",
                "image-captioning",
                "visual-question-answering",
                "multimodal-memory",
                "multimodal-system-design",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M09.L01.QZ01",

        "title": "Multimodal Large Language Models — Knowledge Check",

        "lesson_code": "M09.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M09.L01.Q01",
                "section_id": "what-is-multimodality",
                "question": "What is a modality?",
                "options": [
                    "A type of information such as text, image, audio, or video",
                    "A specific tokenizer vocabulary",
                    "A Transformer layer",
                    "A loss function",
                ],
                "correct": 0,
                "explanation": (
                    "A modality refers to a type or channel of information the system "
                    "can process."
                ),
            },
            {
                "id": "M09.L01.Q02",
                "section_id": "image-patches",
                "question": "How does a Vision Transformer create a sequence from an image?",
                "options": [
                    "It converts every image into a sentence first.",
                    "It divides the image into patches and represents those patches as vectors.",
                    "It assigns every possible image a single token ID.",
                    "It uses only the image filename.",
                ],
                "correct": 1,
                "explanation": (
                    "ViT turns spatial image regions into patch embeddings that can "
                    "be processed as a sequence."
                ),
            },
            {
                "id": "M09.L01.Q03",
                "section_id": "patch-vs-token",
                "question": "Why are image patches not normally mapped to a fixed vocabulary like text tokens?",
                "options": [
                    "Exact image patches vary enormously and are not reusable discrete symbols in the same way words/subwords are.",
                    "Images contain no numbers.",
                    "Transformers cannot process continuous vectors.",
                    "Image patches are always identical.",
                ],
                "correct": 0,
                "explanation": (
                    "Visual patches are generally projected directly into continuous "
                    "embeddings instead of looked up from a finite reusable token vocabulary."
                ),
            },
            {
                "id": "M09.L01.Q04",
                "section_id": "clip",
                "question": "What is CLIP mainly designed to do?",
                "options": [
                    "Generate videos from text",
                    "Create comparable embeddings for text and images",
                    "Replace every image with a caption during training",
                    "Train only on audio",
                ],
                "correct": 1,
                "explanation": (
                    "CLIP aligns text and image representations in a shared embedding space."
                ),
            },
            {
                "id": "M09.L01.Q05",
                "section_id": "contrastive-learning",
                "question": "What is the purpose of contrastive learning in CLIP?",
                "options": [
                    "Move matched image-text pairs closer and mismatched pairs farther apart in embedding space.",
                    "Generate longer captions.",
                    "Delete negative examples.",
                    "Make every embedding identical.",
                ],
                "correct": 0,
                "explanation": (
                    "Contrastive training shapes the representation space so matching "
                    "concepts align and nonmatching examples become more separated."
                ),
            },
            {
                "id": "M09.L01.Q06",
                "section_id": "clip-use-cases",
                "question": "How can CLIP perform zero-shot image classification?",
                "options": [
                    "By comparing the image embedding with embeddings of candidate textual class descriptions.",
                    "By retraining a classifier head for every image.",
                    "By counting image pixels.",
                    "By asking a BM25 index.",
                ],
                "correct": 0,
                "explanation": (
                    "Candidate labels can be expressed as text and compared directly "
                    "with the image representation in the shared vector space."
                ),
            },
            {
                "id": "M09.L01.Q07",
                "section_id": "clip-text-embedding",
                "question": "What does a CLIP text embedding shape of [1, 512] mean?",
                "options": [
                    "One text input represented by a 512-dimensional vector",
                    "512 different models",
                    "One image with 512 channels",
                    "512 text inputs with one dimension",
                ],
                "correct": 0,
                "explanation": (
                    "The batch contains one text item and the embedding has 512 values."
                ),
            },
            {
                "id": "M09.L01.Q08",
                "section_id": "clip-image-processing",
                "question": "What does an image tensor shape [1, 3, 224, 224] represent?",
                "options": [
                    "One image, three RGB channels, 224-pixel height, 224-pixel width",
                    "One model, three layers, 224 tokens, 224 labels",
                    "Three images with 224 captions",
                    "224 models with three channels",
                ],
                "correct": 0,
                "explanation": (
                    "This is the standard batch-channel-height-width interpretation."
                ),
            },
            {
                "id": "M09.L01.Q09",
                "section_id": "blip2",
                "question": "What is the central architectural idea of BLIP-2?",
                "options": [
                    "Train a vision model and language model from scratch every time.",
                    "Connect frozen pretrained vision and language models using a trainable bridge.",
                    "Convert all images into filenames.",
                    "Use only a text tokenizer.",
                ],
                "correct": 1,
                "explanation": (
                    "BLIP-2 reuses pretrained components and trains the Q-Former bridge "
                    "to connect them."
                ),
            },
            {
                "id": "M09.L01.Q10",
                "section_id": "blip-stage1",
                "question": "Which is one of the first-stage BLIP-2 training objectives?",
                "options": [
                    "Image-text matching",
                    "BM25 ranking",
                    "Audio transcription",
                    "Vector database indexing",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter lists image-text contrastive learning, image-text "
                    "matching, and image-grounded text generation."
                ),
            },
            {
                "id": "M09.L01.Q11",
                "section_id": "soft-prompt",
                "question": "What is a soft visual prompt in this lesson?",
                "options": [
                    "A human-written caption pasted above the image",
                    "Projected continuous visual embeddings used to condition the language model",
                    "A low-resolution image filename",
                    "A system message that contains no image information",
                ],
                "correct": 1,
                "explanation": (
                    "BLIP-2 projects visual representations into the LLM’s embedding "
                    "space so they can act as non-textual conditioning vectors."
                ),
            },
            {
                "id": "M09.L01.Q12",
                "section_id": "image-preprocessing",
                "question": "Why can image preprocessing affect multimodal model quality?",
                "options": [
                    "Resizing or reshaping may distort or remove visual information before the model sees it.",
                    "Preprocessing always improves every image.",
                    "The model ignores processed pixels.",
                    "Image preprocessing modifies the LLM vocabulary.",
                ],
                "correct": 0,
                "explanation": (
                    "The visual encoder only sees the transformed input, so preprocessing "
                    "can become an information bottleneck."
                ),
            },
            {
                "id": "M09.L01.Q13",
                "section_id": "vqa",
                "question": "What distinguishes visual question answering from simple image captioning?",
                "options": [
                    "VQA combines an image with a textual question and generates an answer targeted to that question.",
                    "VQA uses no images.",
                    "Captioning always requires a conversation history.",
                    "VQA cannot generate text.",
                ],
                "correct": 0,
                "explanation": (
                    "VQA conditions generation on both visual information and a specific textual query."
                ),
            },
            {
                "id": "M09.L01.Q14",
                "section_id": "multimodal-memory",
                "question": "How does the chapter create memory for multimodal chat?",
                "options": [
                    "It permanently updates the BLIP-2 weights after each answer.",
                    "It stores prior questions/answers externally and includes them in later prompts.",
                    "It adds more image patches after every turn.",
                    "It converts memory into a tokenizer vocabulary.",
                ],
                "correct": 1,
                "explanation": (
                    "Conversation history is managed at the application level and "
                    "reintroduced in later prompt text."
                ),
            },
            {
                "id": "M09.L01.Q15",
                "section_id": "clip-vs-blip",
                "question": "Which comparison is correct?",
                "options": [
                    "CLIP is mainly for aligned image/text representations; BLIP-2 is designed to condition language generation on images.",
                    "CLIP and BLIP-2 are identical architectures.",
                    "BLIP-2 performs only vector similarity and cannot generate text.",
                    "CLIP requires Q-Former.",
                ],
                "correct": 0,
                "explanation": (
                    "CLIP focuses on multimodal representation alignment, while BLIP-2 "
                    "bridges vision into an LLM for generation."
                ),
            },
            {
                "id": "M09.L01.Q16",
                "section_id": "full-pipeline",
                "type": "open",
                "question": (
                    "Explain how a multimodal system can progress from raw image pixels "
                    "to a generated textual answer. Include image patches, visual "
                    "embeddings, CLIP-style alignment, BLIP-2/Q-Former, soft visual "
                    "prompts, textual prompting, and one limitation introduced by preprocessing."
                ),
            },
        ],

        "passing_score": 70,
    },
}
