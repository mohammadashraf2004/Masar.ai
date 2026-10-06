"""M11.L01 — Fine-Tuning Representation Models for Classification.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 11; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M11.L01"

MODULE_ORDER = 11

MODULE_TITLE = "Fine-Tuning Representation Models for Classification"

MODULE_DESCRIPTION = (
    "Learn how to adapt pretrained representation models for classification by "
    "fine-tuning BERT end to end, freezing selected layers, using SetFit for "
    "few-shot classification, continuing masked-language-model pretraining for "
    "domain adaptation, and fine-tuning token-level classifiers for named-entity recognition."
)

SOURCE_CHAPTER = 11

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Fine-Tuning Representation Models for Classification",

    "slug": "llm-foundations-m11-l01",

    "description": (
        "A practical guide to adapting pretrained representation models for "
        "classification. The lesson covers full BERT fine-tuning, partial freezing, "
        "few-shot SetFit training, continued masked-language-model pretraining, and "
        "named-entity recognition with token-label alignment."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.75,

    "skill_tags": [
        "bert",
        "representation-models",
        "supervised-classification",
        "fine-tuning",
        "layer-freezing",
        "sequence-classification",
        "setfit",
        "few-shot-classification",
        "contrastive-learning",
        "masked-language-modeling",
        "continued-pretraining",
        "domain-adaptation",
        "named-entity-recognition",
        "token-classification",
        "bio-labels",
        "label-alignment",
        "seqeval",
        "module-11",
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
        "M09.L01",
        "M10.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Fine-Tuning Representation Models for Classification",

        "content": (
            r"""
# Fine-Tuning Representation Models for Classification

> **Course:** Large Language Models Foundations  
> **Lesson:** M11.L01  
> **Module:** Fine-Tuning Representation Models for Classification  
> **Source alignment:** Chapter 11, “Fine-Tuning Representation Models for Classification.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the difference between using a **frozen pretrained representation model** and **fine-tuning** it.
- Explain how a classification head is attached to BERT.
- Explain how gradients update both the task head and pretrained encoder during full fine-tuning.
- Prepare text classification data using tokenization and dynamic padding.
- Explain why metrics such as F1 should be monitored during training.
- Interpret key training hyperparameters such as learning rate, batch size, epochs, and weight decay.
- Explain why full fine-tuning can outperform using a frozen feature extractor.
- Explain what **layer freezing** does and why it trades compute for adaptability.
- Compare training only the classification head with unfreezing later BERT blocks.
- Explain the central idea of **few-shot classification**.
- Describe SetFit’s three-stage algorithm.
- Explain how SetFit creates positive and negative sentence pairs from class labels.
- Explain why SetFit can learn from very few labeled examples.
- Explain the role of a pretrained SentenceTransformer inside SetFit.
- Explain the difference between ordinary task fine-tuning and **continued pretraining**.
- Explain why continued masked-language-model pretraining can adapt BERT to a domain.
- Compare token masking and whole-word masking.
- Explain how MLM predictions can reveal a shift toward domain vocabulary.
- Define **Named-Entity Recognition (NER)** as token-level classification.
- Explain BIO-style labels such as `B-PER`, `I-PER`, and `O`.
- Explain why word-level NER labels must be aligned with subword tokens.
- Explain the purpose of the `-100` ignore label.
- Explain why NER needs token-level evaluation rather than document-level evaluation.
- Build the mental model of end-to-end fine-tuning for sequence classification and token classification.
- Decide when to use full fine-tuning, partial freezing, SetFit, continued pretraining, or NER fine-tuning.

---

## 1. What changes when we stop freezing the model?

Earlier classification examples used pretrained representation models mostly as fixed components.

A frozen encoder behaves like:

```text
text
 ↓
pretrained encoder
(weights unchanged)
 ↓
representation
 ↓
classifier
 ↓
label
```

Chapter 11 asks:

> What if the pretrained model itself is allowed to learn from the target classification task?

Now the pipeline becomes:

```text
text
 ↓
pretrained BERT
(weights updated)
 ↓
classification head
(weights updated)
 ↓
label
```

The error signal flows backward through both parts.

[[IMAGE_NEEDED: Frozen versus fine-tuned classifier | Left side shows frozen BERT feeding a trainable classifier; right side shows both BERT and classification head trainable with backward arrows through the whole network | Learner should see the difference between fixed feature extraction and end-to-end task adaptation]]

The chapter then expands this idea in four directions:

```text
1. Supervised sequence classification
2. Few-shot SetFit classification
3. Continued pretraining with MLM
4. Named-entity recognition
```

---

## 2. Fine-tuning creates a task-specific representation model

A general pretrained BERT model has learned broad language patterns.

But sentiment classification requires representations useful for:

```text
positive
versus
negative
```

Fine-tuning updates BERT so that its internal features become more useful for the target labels.

A classification head is added on top.

Conceptually:

```text
tokens
  ↓
BERT encoder
  ↓
pooled representation
  ↓
classification head
  ↓
logits for each class
```

During training:

```text
prediction error
  ↓
classification head
  ↓
BERT layers
```

Both can learn together.

[[IMAGE_NEEDED: Task-specific BERT classifier | Show tokenized text entering pretrained BERT, pooled representation entering a small feedforward classification head, and gradients flowing backward through both components | Learner should understand joint optimization]]

---

## 3. The supervised sentiment dataset

The chapter reuses the Rotten Tomatoes dataset.

It reports:

```text
5,331 positive reviews
5,331 negative reviews
```

The classification problem is:

```text
review
→ 0 or 1
```

This is useful because earlier chapters used the same task without fully updating the pretrained representation model.

That creates a clean conceptual comparison:

```text
same kind of task
different training strategy
```

---

## 4. Load BERT with a sequence-classification head

The chapter uses:

```python
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

model_id = "bert-base-cased"

model = AutoModelForSequenceClassification.from_pretrained(
    model_id,
    num_labels=2,
)

tokenizer = AutoTokenizer.from_pretrained(
    model_id
)
```

The important argument is:

```python
num_labels=2
```

because the task contains:

```text
negative
positive
```

The library creates a model with an appropriate classification head on top of BERT.

---

## 5. Tokenize the text before fine-tuning

The classifier does not consume raw strings directly.

The chapter defines:

```python
def preprocess_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
    )
```

Then maps that function over the dataset.

This produces model inputs such as:

```text
input_ids
attention_mask
```

### Why truncation?

BERT has a finite maximum sequence length.

If an example is too long:

```text
truncation=True
```

prevents it from exceeding the model’s supported input size.

---

## 6. Dynamic padding creates batch-compatible shapes

Sentences have different lengths.

One batch may contain sequences of:

```text
18 tokens
34 tokens
51 tokens
```

The model expects a rectangular tensor.

So shorter sequences are padded.

The chapter uses:

```python
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(
    tokenizer=tokenizer
)
```

This pads examples to the longest sequence in the current batch.

[[IMAGE_NEEDED: Dynamic batch padding | Show three token sequences of different lengths being padded to the length of the longest sequence in that batch | Learner should understand why padding is required for tensor batches without padding every sample to a global maximum]]

---

## 7. Track an evaluation metric during training

The chapter defines an F1 metric function.

Conceptually:

```text
model logits
 ↓
argmax
 ↓
predicted labels
 ↓
compare with true labels
 ↓
F1
```

The reason to evaluate during training is not merely to obtain a final number.

Metrics can help detect:

```text
improvement
plateau
overfitting
regression
```

The general lesson is:

> Training loss tells you how optimization is progressing; task metrics tell you whether the model is becoming useful for the task you care about.

---

## 8. Understand the main classification training settings

The source uses settings including:

```text
learning_rate = 2e-5
train batch size = 16
eval batch size = 16
epochs = 1
weight_decay = 0.01
```

### Learning rate

Controls the size of parameter updates.

Too large:

```text
training may become unstable
```

Too small:

```text
adaptation may be very slow
```

### Batch size

Controls how many examples are processed before an optimizer update.

### Epochs

Controls how many full passes are made over the training dataset.

### Weight decay

Regularization that can discourage parameters from growing excessively.

The exact best values are task-dependent.

---

## 9. The Trainer coordinates optimization

The chapter uses Hugging Face’s `Trainer`.

Conceptually, the trainer combines:

```text
model
training arguments
training dataset
evaluation dataset
tokenizer
data collator
metric function
```

Then:

```python
trainer.train()
```

runs optimization.

Afterward:

```python
trainer.evaluate()
```

reports performance.

This abstraction lets the learner focus on:

```text
model
data
objective
evaluation
```

rather than manually writing every training-loop detail.

---

## 10. Full fine-tuning result

The chapter reports approximately:

```text
F1 ≈ 0.85
```

for the fully fine-tuned BERT sentiment classifier.

It compares this with an earlier pretrained task-specific model result around:

```text
F1 ≈ 0.80
```

The useful lesson is:

> When sufficient labeled data is available, adapting the full representation model to your exact task can improve task-specific performance.

Do not turn the exact numbers into a universal guarantee.

The result belongs to this particular dataset, model, and training configuration.

---

## 11. Layer freezing: reduce how much of BERT is updated

Full fine-tuning updates a large number of parameters.

That costs:

- training memory,
- compute,
- time.

A cheaper alternative is to freeze some parameters.

For a frozen parameter:

```python
param.requires_grad = False
```

the optimizer does not update it.

The chapter explores how much performance is lost as more of BERT is frozen.

[[IMAGE_NEEDED: Layer-freezing spectrum | Show BERT embeddings + 12 encoder blocks + classifier, with three configurations: all trainable, only classifier trainable, and only later encoder blocks plus classifier trainable | Learner should understand freezing as a continuum rather than an all-or-nothing choice]]

---

## 12. Inspect BERT before deciding what to freeze

The source prints parameter names such as:

```text
bert.embeddings...
bert.encoder.layer.0...
...
bert.encoder.layer.11...
bert.pooler...
classifier...
```

This reveals a broad structure:

```text
embedding layers
12 encoder blocks
pooler
classification head
```

Understanding parameter names matters because selective freezing requires knowing which modules you are turning off.

---

## 13. Freeze BERT and train only the classification head

The chapter first freezes everything except parameters beginning with:

```text
classifier
```

Conceptually:

```text
BERT
frozen

classification head
trainable
```

Training becomes faster because backpropagation does not update the large encoder.

But the representation model itself cannot adapt to movie-review sentiment.

### Reported result

The source reports approximately:

```text
F1 ≈ 0.63
```

which is substantially below full fine-tuning in that experiment.

This demonstrates the cost of freezing too much.

---

## 14. Partial unfreezing finds a middle ground

The chapter next freezes most of BERT but leaves later parts trainable.

Conceptually:

```text
early BERT blocks
frozen

later BERT block(s)
trainable

classifier
trainable
```

The source’s shown configuration reports about:

```text
F1 ≈ 0.80
```

This is better than the classifier-only result while still reducing the amount of trainable computation.

[[IMAGE_NEEDED: Partial BERT freezing | Show early encoder blocks locked and later encoder blocks plus classifier unlocked, with gradient flow only through the trainable tail | Learner should see why partial fine-tuning can preserve adaptability while reducing compute]]

---

## 15. The real freezing tradeoff

The lesson from the chapter is not:

```text
always freeze
```

or:

```text
never freeze
```

It is:

```text
more trainable layers
→ greater adaptation capacity
→ more compute

more frozen layers
→ less adaptation capacity
→ faster/cheaper training
```

The source’s experiments show performance improving as more useful parts of the encoder are allowed to learn, then stabilizing.

For resource-constrained projects, selective freezing can be a practical compromise.

---

{{exercise:M11.L01.EX01}}

---

## 16. Few-shot classification: what if labeled data is scarce?

Full fine-tuning used thousands of labeled reviews.

But many real projects have only a handful of carefully labeled examples.

**Few-shot classification** asks:

> Can we learn a useful classifier from only a small number of labeled examples per class?

The chapter introduces:

```text
SetFit
```

for this setting.

[[IMAGE_NEEDED: Few-shot classification | Show two classes with only a small handful of labeled examples feeding a model that must classify unseen text | Learner should understand the low-label-data setting]]

---

## 17. SetFit: combine contrastive embeddings with a classifier

SetFit builds on sentence-transformers.

Its three stages are:

```text
1. Generate positive and negative sentence pairs
2. Fine-tune an embedding model with those pairs
3. Train a classifier over the resulting embeddings
```

This is elegant because ordinary classification labels are converted into contrastive training data.

[[IMAGE_NEEDED: Three-stage SetFit pipeline | Show class-labeled examples → positive/negative pair generation → contrastive SentenceTransformer fine-tuning → embeddings → classifier | Learner should memorize the three SetFit stages]]

---

## 18. Stage 1 — Generate positive and negative pairs

Suppose we have:

```text
Class A: programming languages
Class B: pets
```

SetFit assumes:

```text
same-class pair
→ positive

different-class pair
→ negative
```

Example:

```text
"Python supports decorators."
"Java has static typing."

→ positive if both belong to programming class
```

and:

```text
"Python supports decorators."
"My dog loves long walks."

→ negative
```

This converts a small classification dataset into many training pairs.

---

## 19. Pair generation amplifies a small labeled dataset

If one class contains:

```text
16 examples
```

the number of unique within-class pairs is:

```text
16 × 15 / 2 = 120
```

With multiple classes, additional cross-class negative pairs can be generated too.

That means:

```text
few labeled examples
→ many contrastive relationships
```

This is one reason SetFit can be data-efficient.

---

## 20. Stage 2 — Fine-tune the embedding model

The generated pairs are used for contrastive learning.

The goal is to reshape the embedding space so that:

```text
same-class examples
→ closer

different-class examples
→ farther apart
```

This means the representation model becomes tuned specifically to the classification task.

The chapter deliberately connects this step to Chapter 10’s contrastive-learning material.

---

## 21. Stage 3 — Train the classifier

After the embedding model is adapted:

```text
sentence
→ tuned embedding
```

the classifier learns:

```text
embedding
→ class
```

The chapter notes that this can be:

- logistic regression,
- or another classification head.

The key idea is that the features themselves were already reshaped by SetFit’s contrastive stage.

---

## 22. Simulate a tiny training set

The chapter samples:

```text
16 reviews per class
```

For two classes:

```text
32 labeled reviews total
```

Compare that with roughly:

```text
8,500 training reviews
```

used in the larger supervised experiment.

That is an enormous reduction in manual labeling requirements.

---

## 23. Start SetFit from a strong pretrained embedding model

The source uses:

```text
sentence-transformers/all-mpnet-base-v2
```

The logic is:

```text
strong general sentence embeddings
+
small amount of task-specific contrastive data
→ task-adapted embedding space
```

This is usually more data-efficient than starting from a generic language-model backbone with only a handful of labels.

---

## 24. SetFit training creates many sentence pairs

The chapter configures parameters such as:

```text
num_epochs = 3
num_iterations = 20
```

The displayed training output reports:

```text
1,280 unique pairs
```

from only:

```text
32 labeled documents
```

### Source consistency note

The surrounding prose contains an arithmetic slip when it writes:

```text
20 × 32 = 680
```

Mathematically:

```text
20 × 32 = 640
```

and doubling 640 for positive and negative pair generation gives:

```text
1,280
```

which matches the displayed training output.

The important learning point is unchanged:

> Pair construction can greatly amplify a small labeled dataset.

---

## 25. Few-shot SetFit result

The chapter reports an F1 around:

```text
0.836
```

and discusses it approximately as:

```text
0.85
```

using only 32 labeled documents.

The important insight is:

> With a strong pretrained embedding model and contrastive pair generation, useful classification can be learned from very little labeled data.

Again, this is a source experiment—not a guarantee for every dataset.

---

## 26. SetFit can also synthesize examples from labels

The source notes that SetFit supports a zero-shot-style approach.

If labels are:

```text
happy
sad
```

synthetic training examples can be created from those label concepts.

This means SetFit can create a classification training signal even when no human-labeled examples are initially available.

The lesson here is broader:

> Label semantics themselves can become weak supervision.

---

## 27. Fine-tuning is not the only adaptation step

The usual pipeline is:

```text
pretraining
→ task fine-tuning
```

But domain-specific data can create a problem.

A general BERT model may know ordinary language well but may not know:

- medical terminology,
- legal language,
- company jargon,
- specialized movie-review expressions.

The chapter inserts another stage:

```text
general pretraining
→ continued domain pretraining
→ task fine-tuning
```

[[IMAGE_NEEDED: Two-stage versus three-stage adaptation | Show standard pretrained model → task fine-tuning beside pretrained model → continued domain MLM → task fine-tuning | Learner should see where domain adaptation fits]]

---

## 28. Continued pretraining with Masked Language Modeling

The chapter continues BERT pretraining using the same broad objective BERT originally learned:

```text
Masked Language Modeling
```

Take:

```text
What a horrible movie!
```

Mask one token:

```text
What a horrible [MASK]!
```

Then train the model to predict the missing token.

But now the training data comes from the target domain.

This shifts BERT’s representations toward domain-specific vocabulary and usage.

---

## 29. Load BERT for masked language modeling

The source uses:

```python
from transformers import (
    AutoModelForMaskedLM,
    AutoTokenizer,
)

model = AutoModelForMaskedLM.from_pretrained(
    "bert-base-cased"
)

tokenizer = AutoTokenizer.from_pretrained(
    "bert-base-cased"
)
```

Notice that this is not yet the sequence-classification model.

We are temporarily returning to the pretraining-style task.

---

## 30. Continued pretraining does not need sentiment labels

The movie-review text is reused.

But the sentiment labels are removed.

Why?

Because the objective is:

```text
predict masked text
```

not:

```text
predict positive/negative
```

The training signal comes directly from the text itself.

This is a form of self-supervised learning.

---

## 31. Token masking versus whole-word masking

The chapter describes two masking styles.

### Token masking

Randomly mask token pieces.

For example, a subword sequence may contain only one masked fragment.

### Whole-word masking

If a word is split into multiple subword tokens, mask the whole word together.

[[IMAGE_NEEDED: Token masking versus whole-word masking | Show one tokenized sentence where a single subword is masked versus another where all subwords belonging to one word are masked | Learner should understand why whole-word masking is a harder prediction task]]

The source uses token masking for faster convergence in the demonstration.

---

## 32. Let the data collator create masks dynamically

The chapter uses:

```python
from transformers import (
    DataCollatorForLanguageModeling,
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,
    mlm_probability=0.15,
)
```

This means roughly:

```text
15% of token positions
```

are candidates for masking under the collator’s MLM behavior.

Dynamic masking means the model can see different corrupted versions across training batches/epochs.

---

## 33. Continue pretraining on the target-domain text

The source creates another `Trainer` for the masked-language-modeling objective.

The important architecture is:

```text
general pretrained BERT
+
unlabeled target-domain text
+
MLM objective
→ domain-adapted BERT
```

### Source consistency note

The displayed `TrainingArguments` code sets:

```text
num_train_epochs=10
```

while nearby prose says:

```text
20 epochs
```

The source is inconsistent on that detail.

When reproducing the experiment, use the code/configuration you intentionally choose rather than assuming both statements can be true simultaneously.

---

## 34. Inspect how continued pretraining changes predictions

Before domain adaptation, the source asks BERT to fill:

```text
What a horrible [MASK]!
```

The original model predicts words such as:

```text
idea
dream
thing
day
thought
```

After continued training on movie reviews, predictions shift toward:

```text
movie
film
mess
comedy
story
```

[[IMAGE_NEEDED: MLM before versus after domain adaptation | Show the same masked sentence with general BERT predicting generic nouns and movie-domain-adapted BERT predicting film-related nouns | Learner should see evidence that continued pretraining shifts the model toward domain language]]

This is not yet a sentiment classifier.

It is evidence that the representation model has become more specialized toward movie-review language.

---

## 35. Fine-tune the adapted model for classification

After continued pretraining:

```text
domain-adapted BERT
```

becomes the starting checkpoint for:

```text
sequence classification
```

Conceptually:

```text
bert-base
  ↓
domain MLM
  ↓
domain-adapted BERT
  ↓
classification fine-tuning
  ↓
task-specific model
```

The chapter’s main message is:

> Continued pretraining can be inserted before supervised fine-tuning when the target domain differs from general pretraining data.

---

## 36. Named-Entity Recognition changes the unit of classification

So far, the model predicted:

```text
one label per document
```

NER instead predicts:

```text
one label per token
```

Example sentence:

```text
Dean Palmer plays for the Rangers.
```

Possible entities:

```text
Dean Palmer → person
Rangers     → organization
```

[[IMAGE_NEEDED: Document classification versus NER | Left side shows one review receiving one sentiment label; right side shows one sentence with entity labels attached to individual token spans | Learner should see the shift from sequence-level to token-level prediction]]

NER is useful for tasks such as:

- extracting people,
- locations,
- organizations,
- domain-specific entities,
- de-identification/anonymization.

---

## 37. The CoNLL-2003 NER dataset

The chapter uses the English CoNLL-2003 dataset.

It contains token-level entity annotations.

An example includes:

```text
Dean
Palmer
...
Rangers
```

with one NER tag for each original word.

The entity categories include:

```text
PER  person
ORG  organization
LOC  location
MISC miscellaneous
O    outside any entity
```

---

## 38. BIO labels preserve multi-word entity boundaries

The chapter uses labels such as:

```text
B-PER
I-PER
B-ORG
I-ORG
O
```

Interpretation:

```text
B = beginning of an entity
I = inside the same entity
O = outside any entity
```

For:

```text
Dean Palmer
```

we want:

```text
Dean   → B-PER
Palmer → I-PER
```

This tells us:

```text
one person named "Dean Palmer"
```

rather than:

```text
two separate people
```

[[IMAGE_NEEDED: BIO entity span | Show “Dean Palmer” with Dean labeled B-PER and Palmer labeled I-PER, plus “Rangers” labeled B-ORG and non-entities labeled O | Learner should understand how BIO tags preserve phrase boundaries]]

---

## 39. Load BERT for token classification

The source uses:

```python
from transformers import (
    AutoModelForTokenClassification,
)

model = AutoModelForTokenClassification.from_pretrained(
    "bert-base-cased",
    num_labels=len(id2label),
    id2label=id2label,
    label2id=label2id,
)
```

This differs from:

```text
AutoModelForSequenceClassification
```

because the model now produces:

```text
a prediction for each token position
```

rather than one pooled sequence label.

---

## 40. Word labels do not automatically align with subword tokens

The dataset is labeled at the word level.

But BERT tokenization can split words.

The chapter’s example includes:

```text
homer
→
home
##r
```

Another example is:

```text
Maarten
→
Ma
##arte
##n
```

Now we have a problem.

The original dataset has:

```text
one word label
```

but the tokenizer produced:

```text
multiple subword positions
```

We must align them.

[[IMAGE_NEEDED: Word-to-subword label mismatch | Show one labeled word such as “Maarten/B-PER” split into Ma, ##arte, ##n, creating multiple token positions that need aligned labels | Learner should see why token classification requires special preprocessing]]

---

## 41. Convert beginning labels into inside labels for later subtokens

Suppose:

```text
Maarten → B-PER
```

and tokenization produces:

```text
Ma
##arte
##n
```

The aligned labels should conceptually be:

```text
Ma      → B-PER
##arte  → I-PER
##n     → I-PER
```

Why not:

```text
B-PER
B-PER
B-PER
```

Because that would incorrectly indicate three separate entity beginnings.

This is one of the most important implementation details in NER fine-tuning.

---

## 42. Special tokens receive an ignore label

BERT inserts special tokens such as:

```text
[CLS]
[SEP]
```

These do not correspond to original labeled words.

The chapter assigns them:

```text
-100
```

During loss/evaluation handling, `-100` is used as an ignored label.

Conceptually:

```text
special token
→ no entity target
→ ignore during classification loss/metrics
```

---

## 43. The alignment function maps token positions back to words

The chapter uses tokenizer metadata:

```python
word_ids = token_ids.word_ids(
    batch_index=index
)
```

Each subtoken can therefore be associated with:

```text
which original word produced it
```

The alignment loop then handles three cases.

### Case 1 — Start of a new word

Use the word’s original label.

### Case 2 — Special token

Use:

```text
-100
```

### Case 3 — Additional subtoken of same word

If the original entity tag is a `B-...` label, convert the later pieces to the matching `I-...` label.

This is a preprocessing transformation—not a model prediction.

---

## 44. NER requires token-level evaluation

Sequence classification gives:

```text
one prediction per document
```

NER gives:

```text
many predictions per document
```

The chapter therefore iterates through:

```text
document
then
token
```

and ignores token labels equal to:

```text
-100
```

It uses the `seqeval` evaluation library and returns:

```text
overall F1
```

This is designed for sequence-labeling tasks rather than ordinary document classification.

---

## 45. Use a token-classification data collator

The chapter switches from:

```text
DataCollatorWithPadding
```

to:

```text
DataCollatorForTokenClassification
```

because labels now exist at token positions and need to remain aligned when batches are padded.

This is a good example of a larger rule:

> Preprocessing and batching must match the prediction granularity of the task.

---

## 46. Fine-tuning NER still follows the familiar training pattern

Once tokenization and label alignment are correct, the rest looks familiar:

```text
model
training arguments
tokenized train set
tokenized evaluation set
token-classification collator
metric function
```

Then:

```python
trainer.train()
trainer.evaluate()
```

The architecture changed from sequence-level to token-level classification, but the overall fine-tuning process remains recognizable.

---

## 47. Inspect NER predictions manually

The chapter saves the trained model and uses a token-classification pipeline.

For:

```text
My name is Maarten.
```

the source reports:

```text
Ma      → B-PER
##arte  → I-PER
##n     → I-PER
```

This confirms that the tokenizer split the name, but the model still recognizes the full span as one person entity.

[[IMAGE_NEEDED: NER subtoken inference | Show “Maarten” tokenized into Ma / ##arte / ##n with B-PER / I-PER / I-PER, then reconstructed visually as one person entity span | Learner should connect subtoken predictions back to a human-readable entity]]

---

## 48. Compare the chapter’s adaptation strategies

| Situation | Main method | What changes? | Data need |
|---|---|---|---|
| Plenty of labeled sequence data | Full BERT fine-tuning | Encoder + classifier | High |
| Limited compute | Partial freezing | Only selected layers + classifier | Moderate/high |
| Very few labels | SetFit | Embedding space + classifier | Low |
| Strong domain shift, lots of unlabeled text | Continued MLM pretraining | Language representation before task fine-tuning | No labels for MLM |
| Token/span extraction | NER fine-tuning | Token-level classifier + encoder | Token-labeled data |

These methods are not interchangeable.

They solve different constraints.

---

## 49. A practical decision guide

### You have thousands of labeled examples and enough compute

Start with:

```text
full fine-tuning
```

and compare against a frozen baseline.

### Compute is limited

Try:

```text
partial freezing
```

and measure performance versus training cost.

### You only have a handful of labels per class

Consider:

```text
SetFit
```

because it amplifies class labels into contrastive sentence pairs.

### Your data uses specialized language

Consider:

```text
continued masked-language-model pretraining
```

before task fine-tuning.

### You need entities/spans rather than one label per document

Use:

```text
token classification / NER
```

with careful subword label alignment.

---

## 50. Put the complete chapter together

The chapter is really about **where adaptation happens**.

### Sequence classification

```text
pretrained BERT
+
classification head
+
labeled reviews
→
task-specific sequence classifier
```

### Partial freezing

```text
pretrained BERT
+
some frozen layers
+
some trainable layers
+
classifier
→
lower-cost task adaptation
```

### SetFit

```text
few labeled examples
→ positive/negative pairs
→ contrastive embedding fine-tuning
→ classifier
```

### Continued pretraining

```text
general BERT
+
unlabeled domain text
+
masked language modeling
→ domain-adapted BERT
→ supervised task fine-tuning
```

### NER

```text
word-labeled sentences
→ subword tokenization
→ label alignment
→ token-level BERT classifier
→ entity spans
```

[[IMAGE_NEEDED: Chapter 11 adaptation map | Show five branches from a pretrained representation model: full sequence fine-tuning, partial freezing, SetFit, continued MLM then classification, and token-level NER | Learner should use this as the final decision map for the chapter]]

---

{{exercise:M11.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Fine-tuning only means training a new classifier on frozen embeddings.

### Why this is wrong

In full fine-tuning, gradients update the pretrained representation model as well as the classification head.

---

### Misconception 2

> Freezing more layers can only improve training.

### Why this is wrong

Freezing reduces computation but also limits how much the representation model can adapt to the target task.

---

### Misconception 3

> If a frozen model trains faster, it is automatically the better production choice.

### Why this is wrong

Training cost is only one metric. The chapter’s classifier-only experiment shows a large performance drop compared with full fine-tuning.

---

### Misconception 4

> Few-shot learning means no supervised labels.

### Why this is wrong

Few-shot classification still uses labeled examples; it simply uses very few per class.

---

### Misconception 5

> SetFit trains only logistic regression.

### Why this is wrong

SetFit first contrastively adapts a sentence embedding model, then trains a classifier over the adapted embeddings.

---

### Misconception 6

> Continued pretraining and classification fine-tuning are the same task.

### Why this is wrong

Continued pretraining uses an unsupervised/self-supervised language-modeling objective such as MLM. Classification fine-tuning uses labeled task targets.

---

### Misconception 7

> Continued MLM pretraining requires sentiment labels.

### Why this is wrong

The source explicitly removes the labels because the training target comes from predicting masked text.

---

### Misconception 8

> NER assigns one label to the whole sentence.

### Why this is wrong

NER predicts labels at the token level so different spans can correspond to people, organizations, locations, and other entities.

---

### Misconception 9

> A word-level NER label can simply be copied unchanged to every subtoken.

### Why this is wrong

For BIO tagging, later subtokens of an entity need `I-...` labels rather than repeated `B-...` labels.

---

### Misconception 10

> Special tokens such as `[CLS]` and `[SEP]` should receive normal entity labels.

### Why this is wrong

They do not correspond to labeled words and are ignored using a value such as `-100`.

---

## Key terminology

| Term | Meaning |
|---|---|
| Fine-tuning | Updating pretrained model parameters for a downstream task |
| Representation model | Model such as BERT that creates contextual representations of text |
| Classification head | Task-specific neural layer mapping representations to class logits |
| Sequence classification | Predicting one label for an entire input sequence/document |
| Frozen parameter | Parameter excluded from training updates |
| Partial freezing | Training only selected layers while keeping others fixed |
| Gradient | Signal used by backpropagation to update trainable parameters |
| Data collator | Component that prepares/pads examples into model-ready batches |
| F1 score | Harmonic balance of precision and recall |
| Few-shot classification | Supervised classification using only a small number of labeled examples |
| SetFit | Few-shot framework combining contrastive sentence-transformer tuning with a classifier |
| Positive pair | Pair expected to be similar, often sampled from the same class |
| Negative pair | Pair expected to be dissimilar, often sampled from different classes |
| Contrastive learning | Training by pulling similar examples together and separating dissimilar examples |
| Continued pretraining | Further pretraining an already pretrained model on new/domain data |
| MLM | Masked Language Modeling |
| Token masking | Masking individual subword tokens |
| Whole-word masking | Masking all subword pieces belonging to a word |
| Domain adaptation | Adapting a general pretrained model to specialized target-domain language |
| NER | Named-Entity Recognition |
| Token classification | Predicting a label for each token position |
| BIO tagging | Entity labeling scheme using Beginning, Inside, and Outside tags |
| B-PER | Beginning of a person entity |
| I-PER | Inside/continuation of a person entity |
| O | Token outside any tracked entity |
| Label alignment | Mapping word-level labels onto subword-token positions |
| `-100` ignore label | Value conventionally excluded from token-classification loss/metrics |
| seqeval | Evaluation tooling for sequence-labeling tasks |

---

## Self-check

Before moving on, make sure you can answer:

1. What is the difference between a frozen encoder and full fine-tuning?
2. What does the classification head do?
3. Why can full fine-tuning improve task-specific representations?
4. Why is dynamic padding needed?
5. Why track F1 in addition to training loss?
6. What does layer freezing change during backpropagation?
7. What happened in the chapter when only the classification head was trainable?
8. Why can partial unfreezing be a useful compromise?
9. What is few-shot classification?
10. What are SetFit’s three stages?
11. How does SetFit create positive pairs?
12. How does SetFit create negative pairs?
13. Why can a small labeled dataset generate many pairwise training examples?
14. What role does the SentenceTransformer play in SetFit?
15. What is continued pretraining?
16. Why can domain-specific MLM improve later classification?
17. Why are labels removed during MLM?
18. What is the difference between token masking and whole-word masking?
19. How did the chapter demonstrate a domain shift after continued pretraining?
20. What is Named-Entity Recognition?
21. How is NER different from document classification?
22. What do B, I, and O mean in BIO labeling?
23. Why does subword tokenization create a label-alignment problem?
24. How should `B-PER` for a split word be propagated to later subtokens?
25. Why are `[CLS]` and `[SEP]` assigned `-100`?
26. Why does NER require token-level metrics?
27. When would you choose SetFit over full BERT fine-tuning?
28. When would you use continued pretraining before fine-tuning?
29. When would partial freezing be attractive?
30. Design a complete NER fine-tuning pipeline from labeled words to predicted entity spans.

---

## Retain this idea

**Fine-tuning representation models is about deciding how much of a pretrained model should adapt, what supervision is available, and at what granularity predictions are made. With abundant labeled data, full BERT fine-tuning lets the representation model and task head specialize together. When compute is limited, selective freezing trades adaptability for efficiency. When labels are scarce, SetFit transforms class labels into contrastive pairs and learns a task-specific embedding space. When the language itself differs from pretraining data, continued MLM can adapt the model before supervised fine-tuning. And when the task is entity extraction, the problem shifts from one label per document to one aligned label per subword token.**
"""
        ),

        "estimated_minutes": 225,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "chapter-roadmap", "title": "What changes when we stop freezing the model?", "order": 1},
            {"id": "task-specific-model", "title": "Fine-tuning creates a task-specific representation model", "order": 2},
            {"id": "dataset", "title": "The supervised sentiment dataset", "order": 3},
            {"id": "load-sequence-model", "title": "Load BERT with a sequence-classification head", "order": 4},
            {"id": "tokenize-classification", "title": "Tokenize the text before fine-tuning", "order": 5},
            {"id": "dynamic-padding", "title": "Dynamic padding creates batch-compatible shapes", "order": 6},
            {"id": "metrics", "title": "Track an evaluation metric during training", "order": 7},
            {"id": "training-arguments", "title": "Understand the main classification training settings", "order": 8},
            {"id": "trainer", "title": "The Trainer coordinates optimization", "order": 9},
            {"id": "full-ft-result", "title": "Full fine-tuning result", "order": 10},
            {"id": "freeze-intuition", "title": "Layer freezing: reduce how much of BERT is updated", "order": 11},
            {"id": "bert-layers", "title": "Inspect BERT before deciding what to freeze", "order": 12},
            {"id": "classifier-only", "title": "Freeze BERT and train only the classification head", "order": 13},
            {"id": "partial-unfreezing", "title": "Partial unfreezing finds a middle ground", "order": 14},
            {"id": "freezing-tradeoff", "title": "The real freezing tradeoff", "order": 15},
            {"id": "few-shot", "title": "Few-shot classification: what if labeled data is scarce?", "order": 16},
            {"id": "setfit", "title": "SetFit: combine contrastive embeddings with a classifier", "order": 17},
            {"id": "setfit-pairs", "title": "Stage 1 — Generate positive and negative pairs", "order": 18},
            {"id": "pair-growth", "title": "Pair generation amplifies a small labeled dataset", "order": 19},
            {"id": "setfit-stage2", "title": "Stage 2 — Fine-tune the embedding model", "order": 20},
            {"id": "setfit-stage3", "title": "Stage 3 — Train the classifier", "order": 21},
            {"id": "setfit-example", "title": "Simulate a tiny training set", "order": 22},
            {"id": "setfit-model", "title": "Start SetFit from a strong pretrained embedding model", "order": 23},
            {"id": "setfit-training", "title": "SetFit training creates many sentence pairs", "order": 24},
            {"id": "setfit-result", "title": "Few-shot SetFit result", "order": 25},
            {"id": "setfit-zero-shot-note", "title": "SetFit can also synthesize examples from labels", "order": 26},
            {"id": "continued-pretraining", "title": "Fine-tuning is not the only adaptation step", "order": 27},
            {"id": "mlm-domain", "title": "Continued pretraining with Masked Language Modeling", "order": 28},
            {"id": "mlm-model", "title": "Load BERT for masked language modeling", "order": 29},
            {"id": "mlm-no-labels", "title": "Continued pretraining does not need sentiment labels", "order": 30},
            {"id": "masking", "title": "Token masking versus whole-word masking", "order": 31},
            {"id": "mlm-collator", "title": "Let the data collator create masks dynamically", "order": 32},
            {"id": "mlm-training", "title": "Continue pretraining on the target-domain text", "order": 33},
            {"id": "mlm-before-after", "title": "Inspect how continued pretraining changes predictions", "order": 34},
            {"id": "mlm-to-classifier", "title": "Fine-tune the adapted model for classification", "order": 35},
            {"id": "ner", "title": "Named-Entity Recognition changes the unit of classification", "order": 36},
            {"id": "conll", "title": "The CoNLL-2003 NER dataset", "order": 37},
            {"id": "bio-labels", "title": "BIO labels preserve multi-word entity boundaries", "order": 38},
            {"id": "token-classifier", "title": "Load BERT for token classification", "order": 39},
            {"id": "wordpiece-problem", "title": "Word labels do not automatically align with subword tokens", "order": 40},
            {"id": "label-alignment", "title": "Convert beginning labels into inside labels for later subtokens", "order": 41},
            {"id": "special-ignore", "title": "Special tokens receive an ignore label", "order": 42},
            {"id": "align-function", "title": "The alignment function maps token positions back to words", "order": 43},
            {"id": "ner-evaluation", "title": "NER requires token-level evaluation", "order": 44},
            {"id": "ner-collator", "title": "Use a token-classification data collator", "order": 45},
            {"id": "ner-training", "title": "Fine-tuning NER still follows the familiar training pattern", "order": 46},
            {"id": "ner-inference", "title": "Inspect NER predictions manually", "order": 47},
            {"id": "method-comparison", "title": "Compare the chapter’s adaptation strategies", "order": 48},
            {"id": "decision-guide", "title": "A practical decision guide", "order": 49},
            {"id": "full-workflow", "title": "Put the complete chapter together", "order": 50},
            {"id": "misconceptions", "title": "Important misconceptions", "order": 51},
            {"id": "terminology", "title": "Key terminology", "order": 52},
            {"id": "self-check", "title": "Self-check", "order": 53},
            {"id": "retain", "title": "Retain this idea", "order": 54},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M11.L01.EX01",

            "title": "Measure the Cost of Freezing BERT Layers",

            "lesson_code": "M11.L01",

            "section_id": "freezing-tradeoff",

            "placement": "after_section",

            "description": (
                "Compare full fine-tuning, classifier-only training, and partial "
                "unfreezing so the compute/performance tradeoff becomes concrete."
            ),

            "instructions": (
                "Use a small binary text-classification dataset and one pretrained BERT "
                "sequence-classification model.\n"
                "1. Create one run where all parameters are trainable.\n"
                "2. Create a second run where only the classification head is trainable.\n"
                "3. Create a third run where the classification head and one or more "
                "later encoder blocks are trainable.\n"
                "4. Keep the data split, seed, epoch count, metric, and major training "
                "settings as consistent as possible.\n"
                "5. Count trainable parameters for each configuration.\n"
                "6. Record training time or approximate compute cost.\n"
                "7. Record F1 or another suitable held-out metric.\n"
                "8. Compare the three configurations in a table.\n"
                "9. Inspect at least five examples where the classifier-only model fails "
                "but a more extensively fine-tuned model succeeds.\n"
                "10. Recommend a configuration for a resource-constrained deployment "
                "and explain the performance sacrifice you would accept."
            ),

            "expected_output": (
                "A comparison table with trainable parameter counts, training cost/time, "
                "evaluation performance, five error examples, and a short recommendation "
                "describing the compute-versus-adaptation tradeoff."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "bert-finetuning",
                "layer-freezing",
                "sequence-classification",
                "f1-evaluation",
                "model-efficiency",
                "error-analysis",
            ],
        },

        {
            "id": "M11.L01.EX02",

            "title": "Design the Right Adaptation Strategy for Three Classification Problems",

            "lesson_code": "M11.L01",

            "section_id": "full-workflow",

            "placement": "after_section",

            "description": (
                "Choose among full fine-tuning, SetFit, continued pretraining, and NER "
                "based on data volume, domain shift, compute, and prediction granularity."
            ),

            "instructions": (
                "Design solutions for these three scenarios:\n"
                "A. 50,000 labeled customer messages with five intent classes.\n"
                "B. 12 labeled examples per class for a specialized industrial fault taxonomy, "
                "plus 200,000 unlabeled internal documents.\n"
                "C. 15,000 sentences labeled with people, organization, location, and "
                "product spans.\n"
                "For each scenario:\n"
                "1. Choose the pretrained starting model.\n"
                "2. Decide whether to use full fine-tuning, partial freezing, SetFit, "
                "continued MLM pretraining, token classification, or a combination.\n"
                "3. Explain exactly what data is used by each training stage.\n"
                "4. Define the prediction granularity: document or token.\n"
                "5. Define the most important preprocessing step.\n"
                "6. Define at least two evaluation metrics/checks.\n"
                "7. Identify the largest likely failure mode.\n"
                "8. Explain how compute limitations would change the plan.\n"
                "9. For scenario B, explain whether you would run continued MLM before SetFit.\n"
                "10. For scenario C, explain how word labels are aligned to subword tokens."
            ),

            "expected_output": (
                "A three-scenario design table specifying model, adaptation strategy, "
                "training data, preprocessing, prediction granularity, evaluation, "
                "failure modes, and compute-sensitive alternatives."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "fine-tuning-strategy",
                "few-shot-classification",
                "continued-pretraining",
                "domain-adaptation",
                "ner",
                "token-label-alignment",
                "model-selection",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M11.L01.QZ01",

        "title": "Fine-Tuning Representation Models for Classification — Knowledge Check",

        "lesson_code": "M11.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M11.L01.Q01",
                "section_id": "chapter-roadmap",
                "question": "What changes during full BERT fine-tuning compared with a frozen encoder setup?",
                "options": [
                    "Only the tokenizer is updated.",
                    "Both the pretrained representation model and classification head can receive parameter updates.",
                    "The classification head is removed.",
                    "No labeled data is used.",
                ],
                "correct": 1,
                "explanation": (
                    "Full fine-tuning backpropagates the task loss through the classifier "
                    "and into the pretrained encoder."
                ),
            },
            {
                "id": "M11.L01.Q02",
                "section_id": "dynamic-padding",
                "question": "Why use a padding data collator for sequence classification?",
                "options": [
                    "To make variable-length examples compatible inside a tensor batch.",
                    "To create new class labels.",
                    "To freeze BERT.",
                    "To convert F1 into accuracy.",
                ],
                "correct": 0,
                "explanation": (
                    "Examples in a batch must share compatible dimensions, so shorter "
                    "sequences are padded."
                ),
            },
            {
                "id": "M11.L01.Q03",
                "section_id": "full-ft-result",
                "question": "What is the main lesson from the chapter’s full fine-tuning experiment?",
                "options": [
                    "Updating the representation model can improve task-specific classification when enough labeled data is available.",
                    "Frozen models always outperform fine-tuned models.",
                    "Classification heads are unnecessary.",
                    "Training metrics are not useful.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter’s experiment shows that end-to-end adaptation can "
                    "outperform a less tailored pretrained setup."
                ),
            },
            {
                "id": "M11.L01.Q04",
                "section_id": "classifier-only",
                "question": "What happens when only the classification head is trainable?",
                "options": [
                    "The BERT representations remain fixed while the small task head adapts.",
                    "All BERT layers update normally.",
                    "The tokenizer learns new subwords.",
                    "The task becomes unsupervised.",
                ],
                "correct": 0,
                "explanation": (
                    "Freezing BERT prevents its representation layers from adapting to "
                    "the target classification task."
                ),
            },
            {
                "id": "M11.L01.Q05",
                "section_id": "freezing-tradeoff",
                "question": "What is the central tradeoff of freezing layers?",
                "options": [
                    "Less compute but less task-specific representation adaptation.",
                    "More compute and always worse accuracy.",
                    "No change in training cost.",
                    "It changes document labels into token labels.",
                ],
                "correct": 0,
                "explanation": (
                    "Freezing reduces trainable computation while limiting how much of "
                    "the pretrained network can learn from the new task."
                ),
            },
            {
                "id": "M11.L01.Q06",
                "section_id": "setfit",
                "question": "What are SetFit’s three conceptual stages?",
                "options": [
                    "Pair generation → embedding fine-tuning → classifier training",
                    "Tokenization → masked language modeling → text generation",
                    "Clustering → reranking → RAG",
                    "Image encoding → Q-Former → captioning",
                ],
                "correct": 0,
                "explanation": (
                    "SetFit first constructs contrastive pairs, then adapts the embedding "
                    "model, then fits a classifier."
                ),
            },
            {
                "id": "M11.L01.Q07",
                "section_id": "setfit-pairs",
                "question": "How does SetFit obtain positive and negative pairs from ordinary class labels?",
                "options": [
                    "Same-class samples become positive pairs and different-class samples become negative pairs.",
                    "Every pair is labeled positive.",
                    "Only random unlabeled sentences are used.",
                    "The tokenizer invents the pair labels.",
                ],
                "correct": 0,
                "explanation": (
                    "SetFit converts categorical supervision into contrastive relationships."
                ),
            },
            {
                "id": "M11.L01.Q08",
                "section_id": "setfit-result",
                "question": "Why is SetFit attractive in a few-shot setting?",
                "options": [
                    "It can turn a small number of labeled examples into many contrastive training pairs and adapt a strong embedding model.",
                    "It requires millions of labels per class.",
                    "It does not use representations.",
                    "It only works for NER.",
                ],
                "correct": 0,
                "explanation": (
                    "Pair generation plus pretrained embeddings make SetFit highly "
                    "data-efficient in the chapter’s example."
                ),
            },
            {
                "id": "M11.L01.Q09",
                "section_id": "continued-pretraining",
                "question": "What is continued pretraining used for in this chapter?",
                "options": [
                    "Adapting a general pretrained BERT model to target-domain language before task fine-tuning.",
                    "Replacing BERT with logistic regression.",
                    "Generating class labels from images.",
                    "Evaluating token-level F1 only.",
                ],
                "correct": 0,
                "explanation": (
                    "The added pretraining stage helps the representation model absorb "
                    "domain-specific vocabulary and patterns."
                ),
            },
            {
                "id": "M11.L01.Q10",
                "section_id": "mlm-no-labels",
                "question": "Why are sentiment labels removed during the MLM stage?",
                "options": [
                    "Because MLM learns from predicting masked text rather than supervised sentiment targets.",
                    "Because BERT cannot process labels.",
                    "Because labels are only used by tokenizers.",
                    "Because MLM is an image task.",
                ],
                "correct": 0,
                "explanation": (
                    "The text itself provides the self-supervised target for masked "
                    "language modeling."
                ),
            },
            {
                "id": "M11.L01.Q11",
                "section_id": "masking",
                "question": "What distinguishes whole-word masking from token masking?",
                "options": [
                    "Whole-word masking hides all subword pieces belonging to a selected word.",
                    "Whole-word masking does not use a tokenizer.",
                    "Token masking always removes the whole sentence.",
                    "There is no difference.",
                ],
                "correct": 0,
                "explanation": (
                    "When a word is split into several subwords, whole-word masking "
                    "masks the complete word rather than only one piece."
                ),
            },
            {
                "id": "M11.L01.Q12",
                "section_id": "mlm-before-after",
                "question": "What did the chapter’s masked-word example demonstrate after continued pretraining on movie reviews?",
                "options": [
                    "Predictions shifted toward movie-related vocabulary.",
                    "The model forgot how to generate tokens.",
                    "The tokenizer was completely replaced.",
                    "The model became an NER system automatically.",
                ],
                "correct": 0,
                "explanation": (
                    "The source contrasts generic completions with film/movie-oriented "
                    "completions after domain adaptation."
                ),
            },
            {
                "id": "M11.L01.Q13",
                "section_id": "ner",
                "question": "What is the main prediction-level difference between sentiment classification and NER?",
                "options": [
                    "Sentiment usually predicts one label per sequence; NER predicts labels across token positions.",
                    "NER predicts only one label per dataset.",
                    "Sentiment requires BIO tagging.",
                    "NER uses no tokenizer.",
                ],
                "correct": 0,
                "explanation": (
                    "NER is a token-level classification task rather than a document-level task."
                ),
            },
            {
                "id": "M11.L01.Q14",
                "section_id": "bio-labels",
                "question": "What does `B-PER` mean?",
                "options": [
                    "Beginning of a person entity",
                    "Background person score",
                    "Beginning of a paragraph",
                    "BERT person embedding",
                ],
                "correct": 0,
                "explanation": (
                    "`B-` marks the beginning of an entity span and `PER` identifies "
                    "the entity type as person."
                ),
            },
            {
                "id": "M11.L01.Q15",
                "section_id": "label-alignment",
                "question": (
                    "If a word labeled `B-PER` is split into three subword tokens, "
                    "how should the later pieces generally be labeled in the chapter’s alignment strategy?"
                ),
                "options": [
                    "B-PER, B-PER",
                    "I-PER, I-PER",
                    "O, O",
                    "-100, -100",
                ],
                "correct": 1,
                "explanation": (
                    "Only the first token begins the entity; later pieces remain inside "
                    "the same entity span."
                ),
            },
            {
                "id": "M11.L01.Q16",
                "section_id": "special-ignore",
                "question": "Why are special tokens assigned `-100` in the NER labels?",
                "options": [
                    "So they can be ignored by the token-classification loss/evaluation logic.",
                    "Because -100 means person.",
                    "To make them trainable.",
                    "To convert them into padding text.",
                ],
                "correct": 0,
                "explanation": (
                    "Special tokens do not correspond to original labeled words and "
                    "should not contribute normal entity targets."
                ),
            },
            {
                "id": "M11.L01.Q17",
                "section_id": "full-workflow",
                "type": "open",
                "question": (
                    "You have a specialized classification project with limited compute, "
                    "only 20 labeled examples per class, and a large collection of unlabeled "
                    "in-domain text. Design an adaptation strategy using the chapter’s methods. "
                    "Explain whether you would use continued MLM, SetFit, layer freezing, "
                    "or full fine-tuning, and describe the evaluation needed to decide."
                ),
            },
        ],

        "passing_score": 70,
    },
}
