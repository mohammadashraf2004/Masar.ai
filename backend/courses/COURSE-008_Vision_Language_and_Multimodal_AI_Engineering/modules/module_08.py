"""M01.L08 — Document AI with Vision-Language Models.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 8, "Document AI".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L08"
MODULE_ORDER = 1
MODULE_TITLE = "Foundations of Vision and Language"
MODULE_DESCRIPTION = (
    "Apply VLMs to real document workflows: information extraction, OCR and "
    "document parsing, model selection, multimodal retrieval, early document "
    "architectures, grounded OCR fine-tuning, DocVQA fine-tuning, and "
    "multimodal document RAG."
)
SOURCE_CHAPTER = 8
SOURCE_PAGES = "Chapter 8 — page numbers not provided"


TOPIC = {
    "title": "Document AI with Vision-Language Models",
    "slug": "vision-language-m01-l08",
    "description": (
        "Learn how to solve document AI problems with modern VLMs and specialized "
        "document models. Compare generative and extractive processing, parse "
        "documents to Markdown or structured formats, choose between single-vector "
        "and multivector retrieval, understand LayoutLMv3 and Donut, fine-tune "
        "KOSMOS2.5 for grounded OCR and SmolVLM2 for DocVQA, and build an end-to-end "
        "multimodal document RAG pipeline."
    ),
    "order": 8,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 5.5,
    "skill_tags": [
        "document-ai",
        "document-vqa",
        "ocr",
        "document-parsing",
        "markdown-conversion",
        "information-extraction",
        "layout-analysis",
        "multimodal-rag",
        "document-retrieval",
        "single-vector-retrieval",
        "multivector-retrieval",
        "maxsim",
        "colpali",
        "layoutlmv3",
        "donut",
        "kosmos2.5",
        "smolvlm2",
        "trl",
        "grounded-ocr",
        "bounding-boxes",
        "document-finetuning",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
        "M01.L07",
    ],

    "lesson": {
        "title": "Document AI with Vision-Language Models",
        "content": r"""
# Document AI with Vision-Language Models

> **Lesson:** M01.L08  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 8, *Document AI*.  
> Page numbers were not included in the supplied source.  
> This lesson is an instructor-authored educational adaptation.

---

## Why documents are an ideal multimodal problem

A document is not just text.

A single page may contain:

```text
paragraphs
tables
figures
charts
form fields
equations
logos
captions
headings
spatial layout
```

The meaning can depend on **where** content appears, not only on the words.

For example:

```text
"Total: 1,240"
```

means something different if it appears:

- under a subtotal section;
- in a tax table;
- beside an invoice total label.

This makes documents naturally multimodal.

The source presents several ways to process them:

```text
1. Ask a model directly about the page
2. Parse the document into machine-readable text/structure
3. Run focused tasks such as classification, field extraction, or layout analysis
4. Retrieve the most relevant page/document, then answer from it
```

These are not competing solutions.

They are different tools for different requirements.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why document understanding is fundamentally multimodal.
- Distinguish direct document QA from document parsing.
- Distinguish generative and extractive information extraction.
- Explain the source’s trade-off between flexible generative VLMs and smaller specialized document models.
- Explain why generative document QA can hallucinate.
- Explain why extractive workflows are useful when answers must come directly from the document.
- Describe ChartQA, DocVQA, InfoVQA, and scientific-diagram QA as document-oriented multimodal tasks.
- Explain OCR-only versus end-to-end document conversion.
- Explain how Markdown, HTML, LaTeX, captions, and document tags preserve different document structures.
- Describe the role of OlmOCR-style document transcription.
- Explain the idea behind SmolDocling and DocTags.
- Build a model-selection framework around task type, accuracy, cost per page, and deployment constraints.
- Distinguish single-vector from multivector document retrieval.
- Explain Document Screenshot Embedding-style retrieval.
- Explain late interaction and MaxSim in ColPali-style retrieval.
- Calculate embedding storage for single-vector and multivector systems.
- Explain why multivector retrieval can improve document understanding at the cost of memory and latency.
- Explain the difference between OCR-dependent and OCR-free document models.
- Describe LayoutLMv3’s multimodal inputs.
- Explain token classification for form understanding.
- Describe Donut as an OCR-free encoder-decoder document model.
- Prepare grounded OCR training targets with bounding boxes.
- Explain why bounding boxes must be clipped and rescaled before KOSMOS2.5-style training.
- Explain prompt masking in grounded OCR fine-tuning.
- Fine-tune a modern VLM for DocVQA using chat-formatted SFT.
- Build a multimodal document retrieval pipeline.
- Combine retrieval and generation into document RAG.
- Choose when to use parsing-first RAG versus direct page-image RAG.

---

## 1. The Document AI problem map

The source organizes document AI around several major workloads.

### Direct information extraction

```text
document image
+
question
→
answer
```

### Parsing

```text
document image
→
Markdown / HTML / structured representation
```

### Classification

```text
document
→
invoice / form / receipt / report / ...
```

### Layout analysis

```text
document
→
title / paragraph / table / figure / field regions
```

### Token or field extraction

```text
document
→
name
address
date
invoice number
total
...
```

### Retrieval

```text
query
+
large document collection
→
most relevant page/document
```

### Multimodal RAG

```text
query
→ retrieve page
→ pass page image + query to VLM
→ grounded answer
```

[[IMAGE_NEEDED: Document AI task map |
Show one document page branching into direct QA, OCR/parsing, layout analysis,
classification, field extraction, retrieval, and multimodal RAG |
Learner should understand that Document AI is a family of tasks rather than one
single model problem]]

---

## 2. Direct page understanding versus parse-first workflows

There are two broad ways to use document content.

### Strategy A — Stay in the image modality

```text
page image
+
question
→
VLM
→
answer
```

Advantages:

- preserves layout;
- preserves charts and figures;
- avoids an OCR preprocessing dependency;
- convenient for one-off questions.

### Strategy B — Parse first

```text
PDF/page
→ OCR + table/figure/formula conversion
→ Markdown / HTML / structured text
→ text processing / search / RAG
```

Advantages:

- reusable representation;
- easier text indexing;
- easy integration with text-only LLM pipelines;
- easier downstream search and storage.

The right choice depends on what you need after extraction.

If you want to ask one visual question, direct VLM inference can be enough.

If you want to:

- index thousands of pages;
- search them repeatedly;
- create a knowledge base;
- feed content to other text systems;

parsing becomes valuable.

---

## 3. Generative versus extractive information extraction

The source distinguishes two answer styles.

### Generative processing

A general VLM sees the document and **generates** a response.

Example:

```text
Question:
"What is the capital of France?"

Generated answer:
"The capital of France is Paris."
```

The model is free to construct language.

### Extractive processing

A specialized model identifies the answer directly from document content.

Example:

```text
Extracted answer:
"Paris"
```

The source frames this as localization/extraction rather than open-ended
generation.

### Core trade-off

Generative model:

```text
more flexible
can reason
can explain
can answer open-ended questions
but can hallucinate
```

Extractive model:

```text
narrower
returns concise spans/labels
more directly tied to visible document content
often cheaper/smaller
```

### Instructional caution about the source wording

The chapter describes extractive tasks as "hallucination proof."

Treat that as a simplified contrast with free-form generation, **not** as a
literal guarantee of perfect correctness.

An extractive pipeline can still return a wrong span if:

- OCR is wrong;
- localization is wrong;
- the model selects the wrong region.

The important source-derived idea remains:

> Extractive systems constrain the output much more tightly to document content.

{{image:extractive-document-understanding}}

{{exercise:M01.L08.EX01}}

---

## 4. Generative document-understanding tasks

The source names several benchmark-defined tasks.

### ChartQA

Questions about charts.

The model may need to combine:

- OCR;
- labels;
- axes;
- legend;
- visual comparison;
- arithmetic.

### DocVQA

Question answering over document pages.

Examples:

```text
"What is the invoice number?"
"What date was this letter sent?"
"Who signed the form?"
```

### InfoVQA

Questions about infographics.

Infographics combine:

- icons;
- labels;
- visual hierarchy;
- charts;
- text.

### Scientific diagram QA

Questions about diagrams where text and visual structure jointly carry meaning.

These tasks show why plain text extraction is sometimes insufficient.

---

## 5. Direct document QA with a modern VLM

The source demonstrates a simple image-text pipeline.

Conceptually:

```python
from transformers import pipeline

pipe = pipeline(
    "image-text-to-text",
    model="DOCUMENT_CAPABLE_VLM",
)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "url": "DOCUMENT_PAGE",
            },
            {
                "type": "text",
                "text": (
                    "What is the name of "
                    "the model in the paper?"
                ),
            },
        ],
    }
]

result = pipe(
    text=messages
)
```

This is powerful because no explicit OCR pipeline is required in the application.

But the answer is still generated.

For high-stakes extraction, you should evaluate:

- exactness;
- hallucination;
- omitted fields;
- formatting consistency.

---

## 6. Extractive document QA

The source uses the Transformers task:

```text
document-question-answering
```

for specialized document models.

An example pattern:

```python
from transformers import pipeline

pipe = pipeline(
    "document-question-answering",
    model="impira/layoutlm-document-qa",
)

result = pipe(
    "DOCUMENT_IMAGE",
    "What is the name of the paper?",
)
```

These models may rely on:

- OCR;
- token positions;
- page layout.

They are valuable when:

- answers are short;
- location matters;
- the task does not need broad open-ended reasoning.

---

## 7. Document parsing: convert the whole page

Question answering extracts one answer.

Parsing tries to preserve the entire document.

A target representation might contain:

```markdown
# Heading

Paragraph text.

| Column A | Column B |
|---|---|
| ... | ... |

Equation:

E = mc^2

![figure description](...)
```

A good parser may need to convert:

- text → Markdown;
- tables → HTML/Markdown;
- equations → LaTeX;
- charts → descriptions;
- figures → captions;
- layout → structural ordering.

This representation can then feed:

- text RAG;
- summarization;
- search;
- accessibility tools;
- text-to-speech.

---

## 8. OCR-only versus end-to-end document conversion

The source distinguishes two kinds of parsing systems.

### OCR-focused model

Goal:

```text
image
→
transcribed text
```

It may preserve tables/equations depending on training.

### End-to-end document converter

Goal:

```text
image
→
rich structured document representation
```

This can include:

- tables;
- figures;
- captions;
- reading order;
- structural tags.

The difference is important.

A parser can be technically excellent at OCR but still fail to preserve the
document structure needed by downstream applications.

---

## 9. OlmOCR-style document transcription

The source presents an OCR-specialized VLM that can be loaded through standard
Transformers interfaces.

Its conditioning prompt asks the model to:

- return a plain-text representation;
- convert equations to LaTeX;
- convert tables to HTML;
- describe figures/charts;
- produce Markdown;
- include document metadata.

The lesson here is bigger than one model:

> A document parser is partly defined by its **output contract**.

A good parsing prompt specifies exactly how different structures should be
serialized.

### Source-aligned inference pattern

```python
processor = AutoProcessor.from_pretrained(
    model_id
)

model = AutoModelForImageTextToText.from_pretrained(
    model_id
).to("cuda")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "DOCUMENT_PAGE",
            },
            {
                "type": "text",
                "text": PARSING_PROMPT,
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
).to(model.device)

output_ids = model.generate(
    **inputs,
    max_new_tokens=1000,
)
```

### Long-page implication

Parsing an entire page may require long outputs.

So:

```text
max_new_tokens
```

must be large enough for the document.

That connects Document AI back to the inference/deployment lesson:

long structured output increases decode cost.

---

## 10. SmolDocling and DocTags

The source presents an end-to-end document conversion system that emits
**DocTags**.

Think of DocTags as structural markup.

Examples include concepts such as:

```text
<picture>
<unordered_list>
<otsl>
```

where the tags describe document structure.

This allows the generated representation to be converted back into a richer
digital document.

### Why structured tags are useful

Plain text says:

```text
Revenue 100 200
```

Structured output can preserve:

```text
this is a table
this token belongs to row 2
this block is a picture
this content is a caption
```

That makes downstream rendering much more faithful.

{{image:document-to-markdown-anchoring}}
{{image:smoldocling-otsl-structure}}

---

## 11. DocTags-to-document workflow

The source demonstrates a pipeline:

```text
page image
  ↓
SmolDocling-style VLM
  ↓
DocTags
  ↓
Docling library
  ↓
DoclingDocument
  ↓
Markdown / rendered document
```

A source-aligned skeleton:

```python
doctags = processor.batch_decode(
    trimmed_generated_ids,
    skip_special_tokens=False,
)[0].lstrip()

doctags_doc = (
    DocTagsDocument
    .from_doctags_and_image_pairs(
        [doctags],
        [image],
    )
)

doc = DoclingDocument.load_from_doctags(
    doctags_doc,
    document_name="Document",
)

markdown = doc.export_to_markdown()
```

The generated language is serving as a structured serialization format.

---

## 12. Choosing the right document model

The source strongly rejects the idea of one universal best model.

Start from the task.

### Simple extractive/classification tasks

Candidates include smaller specialized document models.

Benefits:

- cheaper serving;
- fast;
- easier to self-host;
- practical for narrow tasks.

### Complex visual reasoning

Use a modern generalist VLM when you need:

- chart reasoning;
- open-ended QA;
- mixed text/image understanding;
- broad generalization.

### Full document parsing

Use OCR/document-conversion specialists.

### Retrieval

Use dedicated document retrievers.

### Evaluate more than benchmark accuracy

The source proposes considering:

```text
accuracy
cost per page
trade-off between both
```

Also consider:

- latency;
- memory;
- self-hosting complexity;
- language support;
- target document type;
- hallucination tolerance.

---

## 13. Document-model evaluation

The chapter names OCR-oriented benchmarks such as:

- OmniDocBench;
- OlmOCRBench.

It also warns that some benchmarks can become:

- saturated;
- noisy;
- less useful for distinguishing models.

This gives a general evaluation lesson:

> Do not pick a model from one leaderboard number.

A useful document evaluation should include:

- benchmark score;
- your own documents;
- cost per page;
- latency;
- failure modes.

---

## 14. Multimodal document retrieval

Suppose you have:

```text
10,000 pages
```

and the question:

```text
"How much has world temperature changed?"
```

You do not want to pass every page into the answer model.

Instead:

```text
query
   ↓
document retriever
   ↓
top relevant page(s)
   ↓
answering model
```

This is the retrieval stage of document RAG.

The source divides document retrievers into:

```text
single-vector
multivector
```

---

## 15. Single-vector document retrieval

A single-vector retriever compresses an entire document/page into one embedding.

Conceptually:

```text
document page
→ VLM document encoder
→ one vector

text query
→ text encoder
→ one vector

cosine similarity
→ relevance
```

The source names Document Screenshot Embedding-style systems as an example.

### Advantage

Extremely compact index.

If:

```text
1,000,000 documents
× 1,024 dimensions
× 4 bytes
```

then approximate embedding storage is:

```text
4,096,000,000 bytes
≈ 4.1 GB decimal
```

before database/index overhead.

That is manageable at large scale.

### Limitation

One vector must summarize:

- all text;
- all regions;
- all figures;
- all layout.

Fine-grained information may be lost.

---

## 16. Multivector document retrieval

A multivector retriever preserves many token-level embeddings.

Conceptually:

```text
document
→ visual/document tokens
→ one vector per token

query
→ query token embeddings
```

Instead of comparing one vector to one vector, the retriever performs **late
interaction**.

This keeps local document detail available at retrieval time.

The source names ColPali as the major example.

{{image:single-vs-multivector-retrieval}}
{{image:document-screenshot-embedding}}
{{image:standard-retrieval-vs-colpali}}

---

## 17. Late interaction and MaxSim

The source describes a MaxSim-style scoring process.

For each query token:

```text
find the most similar document token
```

Then combine those best matches.

Conceptually:

```text
query token q1
→ best document token similarity

query token q2
→ best document token similarity

query token q3
→ best document token similarity

sum
→ document relevance score
```

This lets different parts of the question match different regions of a page.

Example query:

```text
"temperature change since the 19th century"
```

Different query tokens may match:

- temperature label;
- historical-period text;
- numeric value.

This is difficult to preserve in one global embedding.

---

## 18. The memory cost of multivector retrieval

Single-vector storage:

```text
documents
× dimensions
× bytes
```

Multivector storage:

```text
documents
× tokens per document
× dimensions
× bytes
```

The source gives an illustrative example:

```text
1M documents
× 200 tokens
× 128 dimensions
× 4 bytes
≈ 102.4 GB decimal
```

before index overhead.

Compare that with the single-vector example of roughly 4 GB.

### Trade-off

Single vector:

```text
lower memory
faster similarity
less fine-grained
```

Multivector:

```text
higher memory
slower retrieval
better detailed document matching
```

Vector databases may add compression and indexing optimizations, so actual
production numbers depend on the implementation.

{{exercise:M01.L08.EX02}}

---

## 19. Before and after the VLM boom

The source contrasts two eras.

### Earlier Document AI

Focused on tasks such as:

- classification;
- layout analysis;
- token classification;
- extractive QA.

Models were often specialized.

### Modern VLM Document AI

Supports more open-ended tasks:

- visual question answering;
- chart understanding;
- document reasoning;
- flexible parsing;
- multimodal RAG.

The earlier models are still useful.

A small specialized model may be better than a giant VLM when the task is only:

```text
classify invoice type
```

or:

```text
extract one known field
```

---

## 20. OCR-dependent versus OCR-free models

### OCR-dependent

Pipeline:

```text
document
→ OCR
→ text + positions
→ document model
```

The output quality depends partly on OCR quality.

The source uses LayoutLM-style models as examples.

### OCR-free

Pipeline:

```text
document image
→ model directly
→ structured/text output
```

The source names examples including:

- Donut;
- Pix2Struct;
- Nougat.

OCR-free does not mean the model ignores text.

It means there is no external OCR stage required by the application pipeline.

---

## 21. LayoutLMv3: text + image + layout

The source describes LayoutLMv3 as an encoder-only model.

It combines:

```text
OCR text tokens
+
document image patches
+
bounding-box/layout coordinates
```

This is useful because two identical words can mean different things depending
on where they appear.

Example:

```text
DATE
```

may be:

- a question/label;
- an answer;
- a table header.

The 2D layout helps distinguish roles.

---

## 22. Token classification for forms

A form-understanding dataset may label tokens as:

```text
B-QUESTION
I-QUESTION
B-ANSWER
I-ANSWER
O
```

{{image:funsd-form-fields}}

The prefix:

```text
B
```

means beginning of a labeled span.

```text
I
```

means inside the span.

```text
O
```

means outside any target entity.

A model head can be initialized for the number of target classes:

```python
model = AutoModelForTokenClassification.from_pretrained(
    model_id,
    num_labels=7,
)
```

Then the processor receives:

```text
text
bounding boxes
image
```

and predicts a label per token.

This is a classic example of a narrow task where a specialized document model
remains attractive.

---

## 23. Donut: OCR-free encoder-decoder document understanding

The source presents Donut as a generative OCR-free model.

Conceptually:

```text
document image
→ visual encoder
→ text decoder
→ structured output
```

The task can be conditioned using task tokens such as:

```text
<classification>
<parsing>
```

This resembles modern VLM design:

```text
visual encoder
+
autoregressive decoder
```

but specialized around document tasks.

{{image:layoutlmv3-architecture}}
{{image:donut-document-model}}

---

## 24. When to fine-tune a modern VLM

The source notes that modern generalist VLMs may already solve many document
tasks out of the box.

Fine-tuning becomes more attractive when:

- domain is specialized;
- output format is strict;
- task is unusual;
- grounding/localization is required;
- base model accuracy is insufficient.

The chapter then demonstrates two levels:

```text
LOWER-LEVEL / SPATIAL
KOSMOS2.5
grounded OCR with location tokens

HIGHER-LEVEL / CONVERSATIONAL
SmolVLM2
DocVQA using chat-formatted SFT
```

---

## 25. KOSMOS2.5 grounded OCR

The source describes KOSMOS2.5 as layout-aware.

It can generate text together with location tokens.

Conceptual output:

```text
<bbox>
<x_88><y_930><x_842><y_951>
</bbox>
EU countries are required...
```

The target is not just:

```text
recognized text
```

It is:

```text
recognized text + spatial grounding
```

This requires special preprocessing.

---

## 26. The DocLayNet training data

The source uses a small DocLayNet dataset variant.

Relevant fields include:

- image;
- bounding boxes;
- category IDs;
- segmentation;
- area;
- `pdf_cells`;
- metadata.

For grounded OCR, the chapter focuses especially on:

```text
image
pdf_cells
```

A `pdf_cell` contains text plus a bounding box.

This can be converted into the model's target serialization.

---

## 27. Why bounding boxes need cleaning

Real document datasets contain messy coordinates.

The source handles:

### Nested lists

`pdf_cells` may contain lists of lists.

Flatten them.

### Negative/out-of-page coordinates

A region may extend beyond the visible page.

Clip it to:

```text
0 ≤ x ≤ page width
0 ≤ y ≤ page height
```

### Tiny boxes

Very small boxes may be unusable.

Reject regions whose width/height falls below a threshold.

### Why this matters

Invalid geometry can create:

- impossible targets;
- unstable training;
- meaningless localization tokens.

---

## 28. Coordinate systems must match the model input

A dataset bounding box may be defined in original-image coordinates.

But the processor may resize the image.

Suppose:

```text
original:
W_original × H_original

processed:
W_target × H_target
```

Scale factors:

```text
scale_x = W_target / W_original
scale_y = H_target / H_original
```

Then:

```text
x_target = x_original × scale_x
y_target = y_original × scale_y
```

The source uses this to create model-specific location tokens.

This is a crucial principle in spatial VLM training:

> Grounding labels must live in the same coordinate system the model is trained
> to predict.

[[IMAGE_NEEDED: Bounding-box coordinate rescaling |
Show one original document page with a text box, then the resized model input
with the corresponding scaled box and coordinate tokens |
Learner should understand why original pixel coordinates cannot be copied
unchanged after image resizing]]

{{exercise:M01.L08.EX03}}

---

## 29. Serialize grounded OCR targets

The source's preprocessing creates target lines conceptually like:

```text
<bbox>
<x_120><y_45><x_420><y_80>
</bbox>
Notes to Consolidated Financial Statements
```

A simplified target builder:

```python
target_line = (
    f"<bbox>"
    f"<x_{px0}>"
    f"<y_{py0}>"
    f"<x_{px1}>"
    f"<y_{py1}>"
    f"</bbox>"
    f"{text}"
)
```

All lines are joined into the target sequence.

So the decoder learns one autoregressive language containing:

```text
geometry tokens
+
OCR text
```

---

## 30. Grounded OCR data collation

The source's collator:

1. converts images to RGB;
2. extracts `pdf_cells`;
3. records original image sizes;
4. runs the image processor to discover model target sizes;
5. rescales boxes;
6. serializes OCR targets;
7. prefixes the task prompt;
8. tokenizes/pads a batch;
9. creates labels;
10. masks prompt tokens with `-100`.

Conceptually:

```python
labels = inputs["input_ids"].clone()

for idx, prompt_ids in enumerate(
    prompt_ids_batch
):
    labels[
        idx,
        :len(prompt_ids)
    ] = -100
```

This connects directly to the prompt-masking lesson from post-training.

The model should learn to generate:

```text
bounding boxes + OCR text
```

not to waste loss reproducing the task instruction.

---

## 31. Training grounded OCR

The source configures a standard Transformers `Trainer`.

Important hyperparameters shown include:

- epochs;
- per-device batch size;
- gradient accumulation;
- learning rate;
- weight decay;
- BF16;
- periodic saving;
- experiment logging.

The exact values are source example settings, not universal defaults.

The educational point is the architecture of the training pipeline:

```text
dataset
→ geometry cleanup
→ coordinate scaling
→ target serialization
→ masking
→ Trainer
```

### Source-code note

The pasted source contains typographic quote characters in one training argument
line.

Treat these as transcription artifacts, not valid Python syntax.

---

## 32. Convert predicted location tokens back to page coordinates

At inference, the model produces processed-image coordinates.

To draw them on the original image:

```text
predicted processed coordinates
× inverse resize scale
→ original-image coordinates
```

The source parses:

```text
<bbox><x_...><y_...><x_...><y_...></bbox>
```

with regular expressions.

Then it rescales and draws polygons.

This closes the grounding loop:

```text
original page
→ resized model input
→ generated coordinate tokens
→ inverse scaling
→ original page overlay
```

---

## 33. Fine-tuning SmolVLM2 for DocVQA

Document VQA is structurally simpler than grounded OCR.

Training example:

```text
image
+
question
→
text answer
```

So it fits naturally into a chat template.

The source formats each sample as:

```text
USER:
[document image]
Answer this question based on the document: <question>

ASSISTANT:
<answer>
```

### Source syntax correction

The supplied chapter contains the conceptual line:

```text
prompt = Answer this question based on the document: {sample['question']}
```

which is missing Python string/f-string syntax.

The intended executable form is:

```python
prompt = (
    "Answer this question based on "
    f"the document: {sample['question']}"
)
```

This is a mechanical code correction; the instructional content is unchanged.

---

## 34. Format DocVQA as multimodal conversation

A source-aligned formatting function:

```python
def format_ds(sample):
    image = sample["image"]

    if image.mode != "RGB":
        image = image.convert("RGB")

    prompt = (
        "Answer this question based on "
        f"the document: {sample['question']}"
    )

    return {
        "images": [
            image
        ],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image,
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            sample["answers"][0]
                        ),
                    }
                ],
            },
        ],
    }
```

Why RGB normalization?

A mixed dataset can contain image modes that the processor/model does not expect.

Normalizing them prevents inconsistent input handling.

---

## 35. SFTTrainer for document QA

The source uses TRL's:

```text
SFTConfig
SFTTrainer
```

This keeps the high-level training code small.

Conceptually:

```python
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    processing_class=processor,
)

trainer.train()
```

The hard part is not the trainer call.

The hard parts are:

- good examples;
- correct document images;
- correct question-answer pairs;
- correct chat formatting;
- evaluation.

This is exactly why the earlier lessons separated **training abstraction** from
**training correctness**.

{{exercise:M01.L08.EX04}}

---

## 36. Document RAG: retrieve, then answer

Document RAG separates:

```text
WHERE is the answer?
```

from:

```text
WHAT is the answer?
```

Pipeline:

```text
PDF
 ↓
pages as images
 ↓
document retriever
 ↓
top page
 ↓
VLM + query
 ↓
generated answer
```

This is especially useful when the complete document is too large to place in
one model context.

[[IMAGE_NEEDED: Multimodal document RAG |
Show PDF → page images → multimodal retriever → top relevant page → VLM with
user query → answer |
Learner should see retrieval and answer generation as separate model stages]]

---

## 37. ColPali-style page retrieval

The source demonstrates a multivector retriever over page images.

### Step 1 — Convert PDF pages to images

```text
PDF
→
page 1 image
page 2 image
...
```

### Step 2 — Encode pages

```python
with torch.no_grad():
    image_inputs = processor(
        images=images
    )

    image_outputs = model(
        **image_inputs
    )

    image_embeddings = (
        image_outputs.embeddings
    )
```

### Step 3 — Encode query

```python
text_query = (
    "How much has the world "
    "temperature changed so far?"
)

with torch.no_grad():
    text_inputs = processor(
        text=text_query
    )

    text_outputs = model(
        **text_inputs
    )

    query_embeddings = (
        text_outputs.embeddings
    )
```

### Step 4 — Score pages

```python
scores = processor.score_retrieval(
    query_embeddings,
    image_embeddings,
)
```

### Step 5 — Select best page

```python
best_page = torch.argmax(
    scores
).item()
```

That page becomes context for the answer model.

---

## 38. Bare-model retrieval versus a vector database

The source notes that direct tensor scoring is fine for a small example.

Production retrieval usually needs a vector database or specialized index.

Why?

At scale you need:

- persistent embeddings;
- indexing;
- compression;
- search;
- memory management;
- filtering;
- batch ingestion.

This becomes particularly important for multivector retrievers because their
embedding footprint can become large.

---

## 39. Generate the answer from the retrieved page

After retrieval:

```text
best page image
+
original query
→
document-capable VLM
```

Source-aligned message structure:

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": images[best_page],
            },
            {
                "type": "text",
                "text": text_query,
            },
        ],
    }
]
```

Then run generation.

This makes the answer model reason over the **original page**, not just a text
snippet extracted from it.

That preserves:

- chart layout;
- typography;
- visual relationships.

---

## 40. End-to-end multimodal document RAG

The source combines everything into one function.

High-level version:

```text
load PDF
  ↓
render pages
  ↓
encode every page
  ↓
encode query
  ↓
score relevance
  ↓
select best page
  ↓
send page + query to VLM
  ↓
return score + page index + answer
```

This is a clean separation of responsibilities:

```text
retriever
→ chooses evidence

generator
→ interprets evidence
```

{{exercise:M01.L08.EX05}}

---

## 41. Parse-first RAG versus image-page RAG

The source introduces both patterns across the chapter.

### Parse-first RAG

```text
PDF
→ Markdown
→ chunk text
→ text embeddings
→ retrieve
→ LLM answer
```

Best when:

- text dominates;
- you need reusable structured content;
- indexing must be compact;
- downstream tools are text-oriented.

### Image-page RAG

```text
PDF
→ page images
→ multimodal embeddings
→ retrieve page
→ VLM answer
```

Best when:

- layout matters;
- charts matter;
- OCR alone may lose information;
- the page is naturally visual.

### Hybrid

A real system can keep both:

```text
parsed text
+
page image
```

and choose the representation appropriate to each query.

---

## 42. Document AI decision framework

Start with the output you need.

### Need one exact field?

Try:

```text
extractive document QA
or
token classification
```

### Need an open-ended explanation?

Use:

```text
generative VLM
```

### Need the entire document converted?

Use:

```text
OCR/document parser
```

### Need field locations?

Use:

```text
layout-aware model
or
grounded OCR
```

### Need to search many documents?

Use:

```text
document retriever
```

### Need search + final answer?

Use:

```text
multimodal document RAG
```

### Need low serving cost for a narrow task?

Consider:

```text
small specialized model
```

before defaulting to a large VLM.

---

## 43. Single-vector or multivector retrieval?

Choose single-vector when:

- millions of documents;
- storage is constrained;
- latency is critical;
- queries are relatively broad.

Choose multivector when:

- fine-grained page understanding matters;
- documents are visually complex;
- retrieval accuracy matters more than index size;
- you can afford more storage and compute.

The key trade-off:

```text
compression
vs
fine-grained matching
```

---

## 44. Evaluate each stage separately

A document RAG system can fail in several ways.

### Retrieval failure

Correct page never reaches the VLM.

### Parsing failure

OCR or table conversion is wrong.

### Generation failure

Correct page is retrieved, but the answer model hallucinates.

### Grounding failure

Text is recognized, but its location is wrong.

### Task-format failure

Output does not match required JSON/Markdown/tag schema.

So evaluate each stage separately.

Example metrics:

```text
retrieval:
Recall@k / NDCG

extractive QA:
exact match / F1

OCR:
character/word error

grounding:
box overlap / localization quality

generation:
task-specific QA accuracy + manual inspection

cost:
latency / memory / cost per page
```

The source especially emphasizes model benchmarks and cost per page when choosing
production document systems.

---

## 45. Source-specific implementation notes

Several pasted code fragments need careful reading.

### 1. Chapter title typo

The uploaded text begins with:

```text
"hapter 8"
```

The intended title is clearly:

```text
Chapter 8. Document AI
```

### 2. "Hallucination proof"

The chapter uses this phrase for extractive QA.

Treat it as a simplified contrast, not an absolute correctness guarantee.

### 3. SmolVLM2 prompt construction

The source omits string/f-string syntax around:

```text
Answer this question based on the document: ...
```

The lesson provides an executable version.

### 4. Code formatting artifacts

The pasted chapter includes several notebook/paste artifacts such as:

- indentation loss;
- line wrapping;
- typographic quotation marks;
- commands merged onto the same line.

These are mechanical issues.

The instructional sequence and model/data ideas are preserved.

### 5. Model names and APIs are source examples

The chapter uses specific checkpoints and library calls to teach the workflow.

The durable knowledge is:

```text
task → representation → model family → preprocessing → training/inference
```

rather than memorizing one checkpoint name.

---

## 46. The complete Document AI mental model

The whole chapter can be summarized as:

```text
DOCUMENT
   ↓
WHAT DO YOU NEED?

A. ONE ANSWER
   ├─ extractive model
   └─ generative VLM

B. FULL CONTENT
   ├─ OCR
   └─ structured document parser

C. STRUCTURED FIELDS / LAYOUT
   ├─ LayoutLM-style model
   └─ grounded OCR model

D. SEARCH
   ├─ single-vector retriever
   └─ multivector retriever

E. SEARCH + ANSWER
   └─ multimodal RAG

CUSTOMIZATION
   ↓
grounded OCR fine-tuning
or
DocVQA SFT

PRODUCTION DECISION
   ↓
accuracy
cost per page
latency
memory
hallucination tolerance
document complexity
```

The most important idea is:

> **Document AI is not one model choice. It is a task decomposition problem.**
> First decide whether you need extraction, parsing, layout, retrieval, or
> generation. Then choose the smallest and most reliable architecture that
> solves that requirement.

{{exercise:M01.L08.EX06}}

---

## Important misconceptions

### Misconception 1: "A PDF is basically plain text."

No.

Documents can encode important meaning in layout, charts, tables, figures, and
spatial relationships.

### Misconception 2: "OCR and document understanding are the same thing."

OCR answers:

```text
what characters are visible?
```

Document understanding may also require:

```text
what does this field mean?
which table cell answers the question?
how are these visual regions related?
```

### Misconception 3: "A generative VLM is always the best document model."

No.

A small specialized model may be cheaper and more reliable for narrow tasks.

### Misconception 4: "Extractive QA can never be wrong."

The source contrasts it with hallucinating generation, but extraction can still
fail through OCR/localization/model errors.

### Misconception 5: "Parsing only means extracting words."

Modern parsing may preserve:

- tables;
- equations;
- figures;
- captions;
- hierarchy;
- reading order.

### Misconception 6: "Single-vector and multivector retrieval differ only in model size."

Their fundamental difference is how much document representation is preserved
in the index.

### Misconception 7: "Multivector retrieval is free accuracy."

It can require much more:

- storage;
- retrieval compute;
- specialized indexing.

### Misconception 8: "OCR-free means the model does not recognize text."

It means there is no required external OCR stage.

### Misconception 9: "Bounding boxes can be used unchanged after resizing an image."

No.

Coordinate systems must be transformed consistently.

### Misconception 10: "The Trainer call is the hard part of grounded OCR."

The difficult work is preparing correct spatial targets.

### Misconception 11: "Document RAG requires converting everything to text."

The source demonstrates page-image retrieval followed by VLM generation.

### Misconception 12: "If the generator gives a wrong answer, the generator is always the problem."

The retriever may have provided the wrong page.

Evaluate components separately.

---

## Key terminology

| Term | Meaning |
|---|---|
| Document AI | ML systems for understanding, extracting, parsing, classifying, or retrieving documents |
| Generative extraction | Model generates an answer from document context |
| Extractive extraction | Model selects/returns content tied directly to document text/regions |
| DocVQA | Visual question answering over documents |
| ChartQA | Question answering over charts |
| InfoVQA | Question answering over infographics |
| OCR | Optical character recognition |
| Document parsing | Converting a document into text/structured representation |
| Markdown conversion | Serializing page content into Markdown |
| DocTags | Structured tags used to represent document content/layout |
| Layout analysis | Identifying structural regions such as titles, tables, figures, and fields |
| OCR-dependent model | Model that consumes OCR text/positions alongside the document |
| OCR-free model | Model that processes the document image without an external OCR stage |
| LayoutLMv3 | Layout-aware encoder model combining text, image, and bounding boxes |
| Donut | OCR-free document encoder-decoder model |
| Grounded OCR | OCR that also outputs spatial locations |
| Bounding box | Rectangle localizing content on a page |
| Coordinate scaling | Mapping boxes between original and processed image sizes |
| Prompt masking | Excluding instruction/input tokens from target loss |
| Single-vector retrieval | One embedding represents one page/document |
| Multivector retrieval | Many embeddings represent one page/document |
| Late interaction | Comparing query/document token embeddings at retrieval time |
| MaxSim | Per-query-token maximum-similarity matching aggregated into a relevance score |
| ColPali | Multivector multimodal document retrieval approach/model family |
| DSE | Document Screenshot Embedding-style single-vector retrieval |
| Multimodal RAG | Retrieval plus answer generation using multimodal evidence |
| Cost per page | Production cost metric for document processing |
| Recall@k | Whether relevant evidence appears in top-k retrieval results |
| NDCG | Ranking metric rewarding relevant results near the top |

---

## Self-check

Before moving on, make sure you can answer:

1. Why are documents naturally multimodal?
2. What is the difference between direct page QA and parse-first processing?
3. What is generative information extraction?
4. What is extractive information extraction?
5. Why can generative document QA hallucinate?
6. Why is the phrase "hallucination proof" too absolute for extractive systems?
7. What is DocVQA?
8. What is ChartQA?
9. What does a full document parser preserve beyond OCR text?
10. Why might tables be serialized to Markdown or HTML?
11. Why might formulas be rendered as LaTeX?
12. What is the difference between OCR-only and end-to-end document conversion?
13. What are DocTags?
14. Why are structural tags useful?
15. What factors should determine document-model selection?
16. Why is cost per page important?
17. What is multimodal document retrieval?
18. What is a single-vector retriever?
19. What is a multivector retriever?
20. How does MaxSim work conceptually?
21. Why is single-vector indexing memory efficient?
22. Why is multivector indexing expensive?
23. Why can multivector retrieval be more accurate?
24. What is an OCR-dependent model?
25. What is an OCR-free model?
26. What inputs does LayoutLMv3 combine?
27. What does B-QUESTION mean in token classification?
28. Why is Donut considered OCR-free?
29. When should you consider a small specialized model instead of a general VLM?
30. What does grounded OCR output in addition to text?
31. Why must nested `pdf_cells` be flattened?
32. Why must invalid boxes be clipped?
33. Why must boxes be rescaled after image preprocessing?
34. Why mask the `<ocr>` prompt during training?
35. What is the basic input/output structure of DocVQA SFT?
36. Why convert images to RGB before training?
37. What does the document retriever do in RAG?
38. What does the generator do?
39. Why can page-image RAG preserve information that text-only RAG loses?
40. When is parse-first RAG preferable?
41. When is multimodal page RAG preferable?
42. How would you measure retrieval quality?
43. How would you evaluate grounded OCR separately from OCR text quality?
44. Why should retrieval and generation errors be diagnosed separately?
45. What is the central task-decomposition lesson of Document AI?

---

## Retain this idea

**Document AI is best solved by first deciding what information product you
actually need. Exact field extraction, whole-page parsing, layout grounding,
document retrieval, and open-ended visual reasoning are different problems.
Modern VLMs make many of them possible with one general model, but specialized
document models remain valuable when the task is narrow, cost-sensitive, or
requires strict extraction.**
""",

        "estimated_minutes": 330,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "document-ai-map", "title": "The Document AI problem map", "order": 1},
            {"id": "direct-vs-parsed", "title": "Direct versus parse-first workflows", "order": 2},
            {"id": "generative-vs-extractive", "title": "Generative versus extractive extraction", "order": 3},
            {"id": "generative-document-tasks", "title": "Generative document tasks", "order": 4},
            {"id": "generative-inference", "title": "Direct document QA", "order": 5},
            {"id": "extractive-models", "title": "Extractive document QA", "order": 6},
            {"id": "document-parsing", "title": "Document parsing", "order": 7},
            {"id": "ocr-only-vs-end-to-end", "title": "OCR-only versus end-to-end conversion", "order": 8},
            {"id": "olmocr", "title": "OlmOCR-style transcription", "order": 9},
            {"id": "smoldocling", "title": "SmolDocling and DocTags", "order": 10},
            {"id": "docling-workflow", "title": "DocTags-to-document workflow", "order": 11},
            {"id": "model-selection", "title": "Choosing the right document model", "order": 12},
            {"id": "ocr-benchmarks", "title": "Document-model evaluation", "order": 13},
            {"id": "retrieval", "title": "Multimodal document retrieval", "order": 14},
            {"id": "single-vector", "title": "Single-vector retrieval", "order": 15},
            {"id": "multivector", "title": "Multivector retrieval", "order": 16},
            {"id": "maxsim", "title": "Late interaction and MaxSim", "order": 17},
            {"id": "retrieval-memory", "title": "Retrieval memory trade-offs", "order": 18},
            {"id": "old-vs-modern", "title": "Early versus modern Document AI", "order": 19},
            {"id": "ocr-dependent-free", "title": "OCR-dependent and OCR-free models", "order": 20},
            {"id": "layoutlmv3", "title": "LayoutLMv3", "order": 21},
            {"id": "token-classification", "title": "Token classification", "order": 22},
            {"id": "donut", "title": "Donut", "order": 23},
            {"id": "modern-vlm-finetuning", "title": "When to fine-tune modern VLMs", "order": 24},
            {"id": "kosmos-task", "title": "KOSMOS2.5 grounded OCR", "order": 25},
            {"id": "doclaynet", "title": "DocLayNet training data", "order": 26},
            {"id": "bbox-cleaning", "title": "Bounding-box cleanup", "order": 27},
            {"id": "bbox-scaling", "title": "Bounding-box coordinate scaling", "order": 28},
            {"id": "kosmos-targets", "title": "Serialize grounded OCR targets", "order": 29},
            {"id": "kosmos-collator", "title": "Grounded OCR data collation", "order": 30},
            {"id": "kosmos-training", "title": "Training grounded OCR", "order": 31},
            {"id": "kosmos-postprocess", "title": "Grounded OCR postprocessing", "order": 32},
            {"id": "docvqa-sft", "title": "SmolVLM2 DocVQA fine-tuning", "order": 33},
            {"id": "docvqa-format", "title": "DocVQA chat formatting", "order": 34},
            {"id": "trl-docvqa", "title": "SFTTrainer for document QA", "order": 35},
            {"id": "rag-map", "title": "Document RAG", "order": 36},
            {"id": "colpali", "title": "ColPali-style retrieval", "order": 37},
            {"id": "retrieval-production", "title": "Production retrieval indexes", "order": 38},
            {"id": "rag-generation", "title": "Generate from the retrieved page", "order": 39},
            {"id": "e2e-rag", "title": "End-to-end multimodal document RAG", "order": 40},
            {"id": "parse-rag-vs-image-rag", "title": "Parse-first versus image-page RAG", "order": 41},
            {"id": "task-decision", "title": "Document AI decision framework", "order": 42},
            {"id": "retriever-decision", "title": "Single-vector or multivector", "order": 43},
            {"id": "evaluation", "title": "Stage-by-stage evaluation", "order": 44},
            {"id": "source-caveats", "title": "Source-specific implementation notes", "order": 45},
            {"id": "complete-mental-model", "title": "Complete Document AI mental model", "order": 46},
        ],
    },

    "exercises": [
        {
            "id": "M01.L08.EX01",
            "title": "Choose generative or extractive processing",
            "lesson_code": "M01.L08",
            "section_id": "generative-vs-extractive",
            "placement": "after_section",
            "description": (
                "Match document requirements to the correct answer-generation style."
            ),
            "instructions": (
                "Choose generative VLM, extractive model, or both for each case:\n"
                "A. Return the exact invoice number.\n"
                "B. Explain what a scientific chart implies.\n"
                "C. Extract a short customer name with minimal free-form generation.\n"
                "D. Summarize the financial risks described across a page.\n"
                "For each, explain hallucination tolerance, reasoning need, and expected output format."
            ),
            "expected_output": (
                "A four-row table with task, approach, reason, and main risk."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "information-extraction",
                "generative-vs-extractive",
                "document-model-selection",
            ],
        },
        {
            "id": "M01.L08.EX02",
            "title": "Calculate retrieval index size",
            "lesson_code": "M01.L08",
            "section_id": "retrieval-memory",
            "placement": "after_section",
            "description": (
                "Compare storage requirements of single-vector and multivector retrieval."
            ),
            "instructions": (
                "You have 2,000,000 pages.\n"
                "Single-vector system: 768 dimensions/page, FP32.\n"
                "Multivector system: 160 token vectors/page, 128 dimensions/vector, FP32.\n"
                "1. Compute raw bytes for both indexes.\n"
                "2. Convert to approximate GB.\n"
                "3. Compute the storage ratio.\n"
                "4. Explain what accuracy/latency benefit could justify the larger index."
            ),
            "expected_output": (
                "Step-by-step storage calculations plus a retrieval trade-off explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "document-retrieval",
                "multivector",
                "storage-planning",
            ],
        },
        {
            "id": "M01.L08.EX03",
            "title": "Rescale a document bounding box",
            "lesson_code": "M01.L08",
            "section_id": "bbox-scaling",
            "placement": "after_section",
            "description": (
                "Practice converting dataset coordinates to model-input coordinates."
            ),
            "instructions": (
                "Original page size: 1600×2400.\n"
                "Processed model size: 800×1200.\n"
                "Original box: x=200, y=300, width=600, height=400.\n"
                "1. Compute scale_x and scale_y.\n"
                "2. Convert the box to x0,y0,x1,y1.\n"
                "3. Rescale all four coordinates.\n"
                "4. Explain what would go wrong if original coordinates were used as targets."
            ),
            "expected_output": (
                "Numeric coordinate conversion and one grounding-error explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "bounding-boxes",
                "coordinate-scaling",
                "grounded-ocr",
            ],
        },
        {
            "id": "M01.L08.EX04",
            "title": "Design a DocVQA SFT example",
            "lesson_code": "M01.L08",
            "section_id": "trl-docvqa",
            "placement": "after_section",
            "description": (
                "Prepare one complete multimodal training example for document question answering."
            ),
            "instructions": (
                "Create a training example containing:\n"
                "- one RGB document image,\n"
                "- question: 'What is the invoice date?',\n"
                "- answer: 'March 18, 2026'.\n"
                "Write the chat-style user/assistant structure, state what the processor must do, "
                "and identify what should contribute to language-model loss."
            ),
            "expected_output": (
                "One formatted multimodal SFT example plus a short loss-region explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "docvqa",
                "sft",
                "chat-template",
            ],
        },
        {
            "id": "M01.L08.EX05",
            "title": "Build a document RAG pipeline",
            "lesson_code": "M01.L08",
            "section_id": "e2e-rag",
            "placement": "after_section",
            "description": (
                "Design retrieval and generation as separate stages."
            ),
            "instructions": (
                "You have a 120-page PDF with charts and tables.\n"
                "Design a RAG pipeline that:\n"
                "1. renders pages,\n"
                "2. creates page embeddings,\n"
                "3. embeds the query,\n"
                "4. retrieves top-k pages,\n"
                "5. sends evidence pages to a VLM,\n"
                "6. returns answer + page reference.\n"
                "State one metric for retrieval and one metric/check for generation."
            ),
            "expected_output": (
                "An end-to-end pipeline diagram and two-stage evaluation plan."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "multimodal-rag",
                "colpali",
                "retrieval",
                "generation",
            ],
        },
        {
            "id": "M01.L08.EX06",
            "title": "Choose a Document AI architecture",
            "lesson_code": "M01.L08",
            "section_id": "complete-mental-model",
            "placement": "after_section",
            "description": (
                "Select the smallest suitable architecture for several document products."
            ),
            "instructions": (
                "For each product, choose a likely approach and justify it:\n"
                "A. Mobile form-type classifier.\n"
                "B. Cloud system that converts scientific PDFs to Markdown.\n"
                "C. Invoice field extractor that must return exact spans.\n"
                "D. Search engine over one million visually complex PDF pages.\n"
                "E. Analyst assistant that searches documents and answers open-ended questions.\n"
                "For retrieval cases, state whether you prefer single-vector or multivector."
            ),
            "expected_output": (
                "A five-row architecture decision table with cost, accuracy, and deployment rationale."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "document-ai-design",
                "model-selection",
                "retriever-selection",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L08.QZ01",
        "title": "Document AI with Vision-Language Models — Knowledge Check",
        "lesson_code": "M01.L08",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L08.Q01",
                "section_id": "document-ai-map",
                "question": "Why are documents naturally multimodal?",
                "options": [
                    "They combine text with layout, tables, images, charts, and other visual structure.",
                    "They contain only text tokens.",
                    "They cannot be represented as images.",
                    "They never require spatial reasoning.",
                ],
                "correct": 0,
                "explanation": (
                    "Document meaning can depend on both textual content and visual/layout structure."
                ),
            },
            {
                "id": "M01.L08.Q02",
                "section_id": "generative-vs-extractive",
                "question": "What is the main difference between generative and extractive document QA?",
                "options": [
                    "Generative systems compose an answer, while extractive systems return content tied directly to the document.",
                    "Extractive systems never use documents.",
                    "Generative systems cannot process images.",
                    "They are exactly the same objective.",
                ],
                "correct": 0,
                "explanation": (
                    "The source contrasts open-ended generation with constrained answer extraction."
                ),
            },
            {
                "id": "M01.L08.Q03",
                "section_id": "document-parsing",
                "question": "Why parse a document into Markdown or another structured text format?",
                "options": [
                    "To make the whole document reusable by search, RAG, LLM, and other text-based systems.",
                    "To remove all content.",
                    "To increase image resolution.",
                    "To eliminate the need for any model.",
                ],
                "correct": 0,
                "explanation": (
                    "Parsing produces a machine-readable representation suitable for downstream pipelines."
                ),
            },
            {
                "id": "M01.L08.Q04",
                "section_id": "smoldocling",
                "question": "What is the purpose of a structured representation such as DocTags?",
                "options": [
                    "Preserve document elements and structure such as pictures, lists, and tables.",
                    "Only compress JPEG images.",
                    "Replace the tokenizer vocabulary.",
                    "Store optimizer state.",
                ],
                "correct": 0,
                "explanation": (
                    "Structured tags carry layout/document semantics beyond plain OCR text."
                ),
            },
            {
                "id": "M01.L08.Q05",
                "section_id": "model-selection",
                "question": "Which is the chapter's main model-selection principle?",
                "options": [
                    "Choose based on task, accuracy, cost, and deployment constraints rather than assuming one universal best model.",
                    "Always choose the largest VLM.",
                    "Always choose LayoutLM.",
                    "Use only benchmark rank.",
                ],
                "correct": 0,
                "explanation": (
                    "Different document tasks have different cost, precision, and reasoning needs."
                ),
            },
            {
                "id": "M01.L08.Q06",
                "section_id": "single-vector",
                "question": "What does a single-vector document retriever store?",
                "options": [
                    "One embedding for each page or document.",
                    "One embedding for every character only.",
                    "No embeddings.",
                    "Only generated answers.",
                ],
                "correct": 0,
                "explanation": (
                    "The full document/page representation is compressed into one vector."
                ),
            },
            {
                "id": "M01.L08.Q07",
                "section_id": "multivector",
                "question": "What does a multivector retriever preserve?",
                "options": [
                    "Multiple token/patch-level embeddings for each document.",
                    "Only one scalar per page.",
                    "Only OCR confidence.",
                    "Only filenames.",
                ],
                "correct": 0,
                "explanation": (
                    "Fine-grained token-level embeddings enable late interaction during retrieval."
                ),
            },
            {
                "id": "M01.L08.Q08",
                "section_id": "maxsim",
                "question": "What is the core idea of MaxSim-style late interaction?",
                "options": [
                    "Each query token finds its best-matching document token, and the matches are aggregated.",
                    "All document vectors are averaged before the query exists.",
                    "Only the first token is compared.",
                    "The model generates an answer before retrieval.",
                ],
                "correct": 0,
                "explanation": (
                    "Late interaction preserves local matching between individual query and document representations."
                ),
            },
            {
                "id": "M01.L08.Q09",
                "section_id": "retrieval-memory",
                "question": "Why is multivector retrieval more memory-intensive?",
                "options": [
                    "It stores many vectors per document instead of one.",
                    "It stores no vectors.",
                    "It forces FP64 training.",
                    "It duplicates every PDF file exactly.",
                ],
                "correct": 0,
                "explanation": (
                    "The index size scales with documents × token count × embedding dimension."
                ),
            },
            {
                "id": "M01.L08.Q10",
                "section_id": "ocr-dependent-free",
                "question": "What defines an OCR-dependent document model?",
                "options": [
                    "It consumes externally produced OCR text/positions as part of its input.",
                    "It cannot process text.",
                    "It generates no output.",
                    "It must be a language-only model.",
                ],
                "correct": 0,
                "explanation": (
                    "External OCR is a required preprocessing stage for these models."
                ),
            },
            {
                "id": "M01.L08.Q11",
                "section_id": "layoutlmv3",
                "question": "Which inputs does LayoutLMv3 combine according to the source?",
                "options": [
                    "OCR text, image patches, and layout/bounding-box information",
                    "Audio and video only",
                    "Only a document title",
                    "Only a single image vector",
                ],
                "correct": 0,
                "explanation": (
                    "Its strength is representing language, visual appearance, and 2D document layout together."
                ),
            },
            {
                "id": "M01.L08.Q12",
                "section_id": "donut",
                "question": "Why is Donut described as OCR-free?",
                "options": [
                    "It can process document images directly without requiring an external OCR stage.",
                    "It never recognizes text.",
                    "It is not a vision model.",
                    "It only classifies image colors.",
                ],
                "correct": 0,
                "explanation": (
                    "OCR-free means the pipeline does not depend on a separate OCR system."
                ),
            },
            {
                "id": "M01.L08.Q13",
                "section_id": "bbox-scaling",
                "question": "Why must bounding boxes be rescaled during grounded OCR preprocessing?",
                "options": [
                    "The processor can resize the page, so target coordinates must match the processed image coordinate system.",
                    "Bounding boxes are always text strings.",
                    "Rescaling changes the answer language.",
                    "It reduces LoRA rank.",
                ],
                "correct": 0,
                "explanation": (
                    "Spatial labels must refer to the geometry actually seen by the model."
                ),
            },
            {
                "id": "M01.L08.Q14",
                "section_id": "kosmos-collator",
                "question": "Why are prompt tokens set to -100 in the grounded OCR labels?",
                "options": [
                    "To exclude the instruction/prompt from the generation loss.",
                    "To delete image pixels.",
                    "To create a bounding box.",
                    "To select the best retrieval page.",
                ],
                "correct": 0,
                "explanation": (
                    "The target loss should focus on the grounded OCR output rather than reproducing the input instruction."
                ),
            },
            {
                "id": "M01.L08.Q15",
                "section_id": "docvqa-format",
                "question": "What is the basic supervised structure used for SmolVLM2 DocVQA fine-tuning?",
                "options": [
                    "Document image + user question → assistant text answer",
                    "Audio → bounding box",
                    "Document ID → optimizer state",
                    "Question only → image generation",
                ],
                "correct": 0,
                "explanation": (
                    "DocVQA is a natural multimodal chat/SFT task."
                ),
            },
            {
                "id": "M01.L08.Q16",
                "section_id": "rag-map",
                "question": "What is the purpose of the retriever in document RAG?",
                "options": [
                    "Select the most relevant page/document evidence before answer generation.",
                    "Generate the final answer without reading documents.",
                    "Train the vision encoder from scratch.",
                    "Convert every page to audio.",
                ],
                "correct": 0,
                "explanation": (
                    "Retrieval narrows a large collection to the evidence likely to contain the answer."
                ),
            },
            {
                "id": "M01.L08.Q17",
                "section_id": "colpali",
                "question": "After ColPali-style page scoring, what does the source example do?",
                "options": [
                    "Selects the highest-scoring page and passes it to a VLM with the query.",
                    "Deletes the document.",
                    "Retrains the retriever immediately.",
                    "Converts the page to audio.",
                ],
                "correct": 0,
                "explanation": (
                    "Retrieval is followed by answer generation over the selected page image."
                ),
            },
            {
                "id": "M01.L08.Q18",
                "section_id": "parse-rag-vs-image-rag",
                "question": "When can image-page RAG be preferable to text-only parse-first RAG?",
                "options": [
                    "When layout, charts, figures, or visual relationships are important.",
                    "When no documents exist.",
                    "When the query contains no text.",
                    "When vector search is forbidden.",
                ],
                "correct": 0,
                "explanation": (
                    "The original page preserves visual information that text conversion can lose."
                ),
            },
            {
                "id": "M01.L08.Q19",
                "section_id": "evaluation",
                "question": "Why evaluate retrieval and generation separately?",
                "options": [
                    "A wrong final answer may be caused by retrieving the wrong evidence or by misinterpreting correct evidence.",
                    "Retrieval cannot fail.",
                    "Generation cannot fail.",
                    "Both stages use identical metrics.",
                ],
                "correct": 0,
                "explanation": (
                    "Separating stages makes the root cause of errors diagnosable."
                ),
            },
            {
                "id": "M01.L08.Q20",
                "section_id": "complete-mental-model",
                "type": "open",
                "question": (
                    "Design a Document AI system for a company with invoices, financial "
                    "reports, and visually complex PDF manuals. The system must extract exact "
                    "invoice fields, convert reports to searchable structured text, retrieve "
                    "relevant manual pages, and answer open-ended questions. Choose the model "
                    "family or workflow for each task, explain whether OCR is required, choose "
                    "single-vector or multivector retrieval, and describe how you would evaluate "
                    "the complete system."
                ),
            },
        ],
        "passing_score": 70,
    },
}
