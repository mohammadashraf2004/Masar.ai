"""M10.L01 — Creating Text Embedding Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 10; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M10.L01"

MODULE_ORDER = 10

MODULE_TITLE = "Creating Text Embedding Models"

MODULE_DESCRIPTION = (
    "Learn how text embedding models are created and adapted using contrastive "
    "learning, sentence-transformers, bi-encoders, different loss functions, "
    "hard negatives, supervised fine-tuning, Augmented SBERT, TSDAE, and domain adaptation."
)

SOURCE_CHAPTER = 10

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Creating Text Embedding Models",

    "slug": "llm-foundations-m10-l01",

    "description": (
        "A practical guide to creating and fine-tuning text embedding models. "
        "The lesson explains what embeddings should represent, how contrastive "
        "learning works, why sentence-transformers use bi-encoders, how data and "
        "loss functions shape embedding quality, how to evaluate embeddings, "
        "and how supervised and unsupervised adaptation methods can specialize "
        "an existing model."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.75,

    "skill_tags": [
        "text-embeddings",
        "contrastive-learning",
        "sentence-transformers",
        "sbert",
        "bi-encoder",
        "cross-encoder",
        "siamese-network",
        "nli",
        "mnli",
        "stsb",
        "mteb",
        "cosine-similarity-loss",
        "multiple-negatives-ranking-loss",
        "hard-negatives",
        "embedding-finetuning",
        "augmented-sbert",
        "tsdae",
        "domain-adaptation",
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
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Creating Text Embedding Models",

        "content": (
            r"""
# Creating Text Embedding Models

> **Course:** Large Language Models Foundations  
> **Lesson:** M10.L01  
> **Module:** Creating Text Embedding Models  
> **Source alignment:** Chapter 10, “Creating Text Embedding Models.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what a text embedding model is trying to represent.
- Explain why “good” embeddings depend on the task.
- Define **contrastive learning** and explain why positive and negative examples matter.
- Explain how contrastive learning relates to word2vec.
- Distinguish a **cross-encoder** from a **bi-encoder / SBERT** architecture.
- Explain why cross-encoders can be accurate but expensive for large-scale pair comparison.
- Explain how sentence-transformers uses pooling to create fixed-size sentence embeddings.
- Explain why shared weights make the architecture Siamese.
- Identify the two main ingredients required for contrastive learning:
  **training pairs/triplets** and a **loss function**.
- Explain how NLI data can provide entailment, neutral, and contradiction examples.
- Build the mental model of training an embedding model from a pretrained Transformer backbone.
- Explain what STSB evaluates.
- Explain what MTEB is used for.
- Compare **softmax loss**, **cosine similarity loss**, and **Multiple Negatives Ranking loss**.
- Explain why loss-function choice can strongly affect embedding quality.
- Explain in-batch negatives.
- Distinguish easy, semi-hard, and hard negatives.
- Explain why hard negatives can improve retrieval-style representations.
- Fine-tune a pretrained sentence-transformer rather than starting from a generic BERT base model.
- Explain why training-data quality is often the hardest part of embedding fine-tuning.
- Explain **Augmented SBERT** and the difference between gold and silver data.
- Explain how a cross-encoder can label additional pairs for training a faster bi-encoder.
- Explain the intuition behind **TSDAE**.
- Explain how TSDAE reconstructs an original sentence from a damaged version.
- Explain why TSDAE is useful when labels are unavailable.
- Explain how unsupervised pretraining can be used for **domain adaptation**.
- Design an end-to-end embedding-model training and evaluation workflow.

---

## 1. What is an embedding model trying to do?

Text is difficult for machine-learning systems to use directly.

A sentence such as:

```text
The dog is sleeping on the sofa.
```

is made of symbols and words.

Many downstream algorithms instead need numerical inputs.

An embedding model converts text into a vector:

```text
text
 ↓
embedding model
 ↓
[0.17, -0.42, 0.08, ..., 0.31]
```

This vector is the **embedding**.

The goal is not merely to convert text into numbers.

The important goal is:

> The numbers should preserve information that matters for the task.

{{image:text-to-embedding}}

### Why embeddings matter

Earlier chapters used embeddings for:

```text
classification
clustering
semantic search
topic modeling
retrieval
memory-like systems
multimodal alignment
```

That is why this chapter treats embedding models as foundational infrastructure rather than a niche technique.

---

## 2. A “good embedding” depends on what similarity means

Suppose we want semantic similarity.

Then we want:

```text
"The dog is sleeping."

and

"A canine is taking a nap."

→ close together
```

while:

```text
"Quarterly revenue increased by 18%."

→ farther away
```

But semantic meaning is not the only possible objective.

For sentiment classification, we may instead want:

```text
"I loved this film."
"This movie was fantastic."

→ close together
```

and:

```text
"This was terrible."

→ farther away
```

even though all three sentences discuss movies.

[[IMAGE_NEEDED: Semantic space versus sentiment space | Show the same documents organized in two embedding spaces: one grouping by semantic topic and another grouping by positive/negative sentiment | Learner should see that fine-tuning changes what “similarity” means]]

### The central design question

Before training an embedding model, ask:

> Which relationships should the geometry of this vector space preserve?

That answer determines:

- training data,
- positive pairs,
- negative pairs,
- loss function,
- evaluation task.

---

## 3. Contrastive learning: learn by comparison

One of the chapter’s central techniques is **contrastive learning**.

The objective is:

```text
similar examples
→ embeddings become closer

dissimilar examples
→ embeddings become farther apart
```

The model learns relationships through contrasts.

Instead of saying only:

```text
"This sentence is about dogs."
```

we teach the model with comparisons such as:

```text
Sentence A and Sentence B are similar.

Sentence A and Sentence C are dissimilar.
```

[[IMAGE_NEEDED: Contrastive learning geometry | Show an anchor sentence, a positive sentence being pulled closer in vector space, and a negative sentence being pushed farther away | Learner should understand contrastive learning as reshaping embedding geometry through comparisons]]

### Why alternatives are informative

The chapter uses the idea of **contrastive explanation**:

```text
Why P rather than Q?
```

Comparing alternatives reveals distinguishing information.

For embeddings:

```text
Why is this sentence similar to A
but not to B?
```

forces the model to learn features that separate the concepts.

---

## 4. The dog-versus-cat intuition

Imagine teaching a model the concept:

```text
dog
```

Possible features include:

```text
four legs
tail
nose
fur
```

But those features also describe a cat.

A contrast:

```text
Why dog rather than cat?
```

forces attention toward more discriminative properties.

The same principle applies to text embeddings.

Positive examples teach:

```text
what belongs together
```

Negative examples teach:

```text
what should remain distinct
```

Both are needed for useful representation geometry.

---

## 5. Contrastive learning already appeared in word2vec

The chapter connects this idea back to word2vec.

In word2vec-style training:

```text
nearby word
→ positive example

random unrelated word
→ negative example
```

The model learns word representations by contrasting:

```text
likely contextual neighbors
against
unlikely contextual neighbors
```

So modern sentence-embedding training is part of a longer contrastive-learning tradition.

---

## 6. Why not use a cross-encoder for everything?

Before sentence-transformers, sentence similarity commonly used a **cross-encoder**.

A cross-encoder receives both sentences together:

```text
Sentence A
[SEP]
Sentence B
 ↓
Transformer
 ↓
similarity score
```

The model can directly compare the two sequences token by token.

That can provide strong accuracy.

But it creates a scaling problem.

[[IMAGE_NEEDED: Cross-encoder architecture | Show sentence A and sentence B concatenated with a separator and passed through one Transformer that produces a similarity score | Learner should notice that the pair must be processed together for every comparison]]

### The pairwise explosion

Suppose we have:

```text
10,000 sentences
```

and want every possible pair.

The number of pair comparisons is:

```text
n(n - 1) / 2
```

For:

```text
n = 10,000
```

that becomes:

```text
49,995,000 pair evaluations
```

That is extremely expensive.

A cross-encoder also usually gives:

```text
one similarity score
```

rather than reusable independent embeddings.

---

## 7. Why simple BERT sentence pooling was not enough

One idea is:

```text
BERT output
→ use [CLS]
```

or:

```text
BERT token outputs
→ average them
```

to produce a sentence vector.

But the chapter notes that naive approaches like this historically produced weak sentence-similarity representations compared with methods specifically trained for sentence embeddings.

This motivates SBERT.

---

## 8. SBERT: create reusable sentence embeddings

Sentence-transformers introduced a more efficient approach.

Instead of:

```text
sentence pair
→ model
→ one score
```

we do:

```text
sentence A
→ encoder
→ embedding A

sentence B
→ same encoder
→ embedding B
```

Then compare:

```text
embedding A
vs
embedding B
```

This architecture is called:

```text
bi-encoder
```

and, in the original BERT-based formulation:

```text
SBERT
```

or:

```text
Sentence-BERT
```

[[IMAGE_NEEDED: Bi-encoder versus cross-encoder | Left side shows cross-encoder processing a pair together for one score; right side shows the same shared encoder independently generating reusable embeddings that can later be compared | Learner should understand why bi-encoders scale better for retrieval]]

---

## 9. Why the architecture is called Siamese

The chapter describes the training architecture as two BERT models:

```text
BERT A
BERT B
```

but they share:

```text
the same architecture
the same weights
```

So conceptually:

```text
Sentence A → shared encoder → embedding A
Sentence B → shared encoder → embedding B
```

This is called a **Siamese network**.

Because weights are shared, deployment only needs one encoder.

You simply call it repeatedly on different sentences.

---

## 10. Pool token representations into one sentence vector

A Transformer produces contextual representations for multiple tokens.

But sentence search needs one fixed-size vector per sentence.

Sentence-transformers adds a pooling step.

The chapter highlights **mean pooling**:

```text
token embedding 1
token embedding 2
token embedding 3
...
        ↓
      average
        ↓
sentence embedding
```

The output has fixed dimensionality no matter whether the input has:

```text
5 tokens
15 tokens
40 tokens
```

This makes embeddings easy to:

- store,
- index,
- compare,
- cluster.

---

## 11. Two things contrastive training requires

The chapter reduces the training problem to two essentials.

### 1. Contrastive data

We need examples describing:

```text
similar
dissimilar
or degrees of similarity
```

### 2. A loss function

We need a mathematical objective that tells the model how to change when the embedding relationships are wrong.

Conceptually:

```text
training examples
+
loss function
+
encoder
→ learned embedding geometry
```

Much of the rest of the chapter explores how changing the first two components changes model quality.

---

## 12. Natural Language Inference as contrastive data

The chapter uses Natural Language Inference, or:

```text
NLI
```

NLI asks about the relationship between:

```text
premise
and
hypothesis
```

Common labels are:

```text
entailment
neutral
contradiction
```

Example:

```text
Premise:
He is in a cinema watching Coco.

Hypothesis:
He is in a movie theater watching Coco.

→ entailment
```

Another hypothesis:

```text
He is at home watching Frozen.

→ contradiction
```

[[IMAGE_NEEDED: NLI as contrastive data | Show one premise with an entailment hypothesis, neutral hypothesis, and contradiction hypothesis branching from it | Learner should understand how NLI labels naturally create different similarity relationships]]

### Why NLI is useful for embeddings

The labels can be interpreted as relationship strength.

For example:

```text
entailment
→ strongly related

contradiction
→ dissimilar for the intended contrastive objective
```

This makes NLI data convenient for training embedding models.

---

## 13. The chapter’s MNLI training data

The chapter uses the:

```text
Multi-Genre Natural Language Inference
```

dataset.

The full corpus contains hundreds of thousands of annotated sentence pairs.

For efficient demonstration, the chapter uses:

```text
50,000 sentence pairs
```

from the training split.

The source’s label mapping is:

```text
0 = entailment
1 = neutral
2 = contradiction
```

Example:

```text
Premise:
One of our number will carry out your instructions minutely.

Hypothesis:
A member of my team will execute your orders with immense precision.

Label:
entailment
```

The two sentences communicate nearly the same meaning.

---

## 14. Build an embedding model from a pretrained Transformer backbone

The chapter begins with:

```python
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "bert-base-uncased"
)
```

The intention is to start from a pretrained language-model backbone and train it into a stronger sentence embedding model.

This is different from training BERT itself from random initialization.

The backbone already contains language knowledge.

We are teaching it:

```text
how sentence-level similarity should be represented
```

### Trainable layers

The chapter notes that sentence-transformers typically leaves all layers trainable during this process.

That allows the full representation stack to adapt to the sentence-embedding objective.

---

## 15. Baseline training with softmax loss

For historical/illustrative purposes, the chapter first uses a softmax-style loss.

Conceptually:

```text
sentence embeddings
+
their relationship features
→ classifier
→ NLI label
```

The model learns through a classification objective.

The chapter emphasizes that this is mainly an introductory baseline and that more suitable losses are explored later.

---

## 16. Evaluate semantic similarity with STSB

Training loss alone does not tell us whether the embeddings are useful.

The chapter evaluates using:

```text
Semantic Textual Similarity Benchmark
```

or:

```text
STSB
```

STSB contains sentence pairs with human similarity scores.

The original scores are:

```text
1 to 5
```

and the chapter normalizes them to:

```text
0 to 1
```

The evaluator compares:

```text
human similarity scores
against
embedding-based similarity scores
```

[[IMAGE_NEEDED: STSB evaluation | Show human-labeled sentence similarity scores compared with cosine similarity produced from model embeddings, then compute a correlation metric | Learner should understand that evaluation checks whether embedding geometry agrees with human similarity judgments]]

---

## 17. Interpret the evaluation score

The chapter focuses primarily on:

```text
pearson_cosine
```

Conceptually, it asks:

> Do pairs humans consider more similar also receive higher embedding cosine similarity?

The first softmax-loss example reports approximately:

```text
Pearson cosine ≈ 0.598
```

which the chapter uses as a baseline for later experiments.

Do not interpret the number as universal model quality.

It is tied to:

- this dataset,
- this evaluator,
- this training configuration,
- this model.

---

## 18. Understand the main training arguments

The source configures:

```text
num_train_epochs
per_device_train_batch_size
per_device_eval_batch_size
warmup_steps
fp16
eval_steps
logging_steps
```

### Epochs

```text
num_train_epochs
```

controls how many passes the model makes over the training data.

### Batch size

```text
per_device_train_batch_size
```

controls how many examples are processed together.

### Warmup

```text
warmup_steps
```

gradually increases the learning rate at the beginning.

### FP16

```text
fp16=True
```

uses mixed/lower-precision computation to reduce memory usage and potentially increase speed.

### Evaluation/logging intervals

These define how often the training process:

```text
evaluates
and
reports progress
```

---

## 19. One benchmark is not enough: MTEB

A strong embedding model should work across more than one similarity dataset.

The chapter introduces:

```text
Massive Text Embedding Benchmark
```

or:

```text
MTEB
```

MTEB combines many tasks and languages.

The source describes categories across:

```text
classification
clustering
retrieval
similarity
and other embedding tasks
```

The main lesson is:

> Evaluate embeddings on the kinds of tasks you actually care about.

A model excellent on sentence similarity may not automatically be excellent for:

```text
banking-intent classification
retrieval
clustering
```

[[IMAGE_NEEDED: Multi-task embedding evaluation | Show one embedding model evaluated across several task families such as similarity, classification, clustering, and retrieval | Learner should understand why broad evaluation is more informative than one benchmark score]]

### Performance is not only accuracy

The chapter also notes:

```text
latency matters
```

Embedding models are often called frequently during:

- search,
- indexing,
- recommendation,
- clustering.

So useful evaluation includes both:

```text
quality
and
speed
```

---

## 20. Loss functions shape the embedding space

A loss function defines what errors matter during training.

Different losses produce different learning behavior.

The chapter focuses on:

```text
softmax loss
cosine similarity loss
Multiple Negatives Ranking loss
```

The experiments illustrate a powerful principle:

> The same basic model and data can behave very differently depending on the training objective.

---

## 21. Cosine similarity loss

Cosine similarity loss is intuitive for graded similarity.

Suppose a sentence pair has a target score:

```text
1.0 → very similar
0.7 → somewhat similar
0.2 → weakly related
0.0 → dissimilar
```

The training objective compares:

```text
predicted cosine similarity
against
target similarity
```

and adjusts the encoder.

[[IMAGE_NEEDED: Cosine similarity loss | Show two sentence embeddings with a target similarity score; training adjusts their angle so predicted cosine similarity approaches the labeled value | Learner should understand cosine loss as matching vector similarity to human/data-provided similarity]]

### Converting MNLI labels

The chapter maps:

```text
entailment → 1
neutral → 0
contradiction → 0
```

for this demonstration.

This simplifies NLI into:

```text
similar
versus
not similar
```

### Chapter result

The cosine-loss example reports approximately:

```text
Pearson cosine ≈ 0.722
```

which is substantially above the earlier softmax baseline of about `0.598`.

This illustrates how strongly the loss function can affect representation quality.

---

## 22. Multiple Negatives Ranking loss

The next loss is:

```text
Multiple Negatives Ranking loss
```

often abbreviated:

```text
MNR loss
```

The chapter also notes related names such as:

```text
InfoNCE
NT-Xent-style objectives
```

The basic data unit can be:

```text
anchor
+
positive
```

and the other examples in the batch become negatives.

Suppose:

```text
Anchor:
When was the Eiffel Tower built?

Positive:
Construction was completed in 1889.
```

Other answers in the same batch can be treated as negative candidates.

The model must rank the true matching sentence above the other candidates.

[[IMAGE_NEEDED: Multiple Negatives Ranking loss | Show one anchor compared against one positive and several in-batch negative candidates, with the positive required to receive the highest similarity | Learner should see MNR as a ranking problem within a batch]]

---

## 23. In-batch negatives make one batch much more informative

Imagine a batch with:

```text
32 positive anchor-positive pairs
```

For one anchor:

```text
its matched positive
→ correct target

the other positives in the batch
→ candidate negatives
```

This creates many contrastive comparisons without manually labeling every negative pair.

That is why larger batches can be useful for MNR loss.

More examples in the batch mean:

```text
more competing candidates
→ harder ranking task
```

The chapter explicitly notes this relationship.

---

## 24. MNR can produce much stronger embeddings

The chapter filters MNLI to entailment pairs and adds unrelated hypotheses as negatives.

The training dataset becomes:

```text
anchor
positive
negative
```

The source reports approximately:

```text
Pearson cosine ≈ 0.809
```

for the MNR-loss experiment.

Looking at the reported experiment outputs:

```text
Softmax baseline        ≈ 0.598
Cosine similarity loss  ≈ 0.722
MNR loss                ≈ 0.809
```

The lesson is not that these exact numbers will always occur.

The lesson is:

> Data construction and loss function can materially change the resulting embedding geometry.

---

## 25. Easy negatives may make training too easy

Consider:

```text
Question:
How many people live in Amsterdam?

Correct answer:
Almost a million people live in Amsterdam.
```

An easy negative might be:

```text
The Pacific Ocean is the largest ocean.
```

This is obviously unrelated.

The model can separate it without learning much nuance.

If all negatives are that easy, training may not teach fine distinctions.

---

## 26. Hard negatives force more precise representations

A hard negative for the Amsterdam question might say:

```text
More than a million people live in Utrecht, which is more than Amsterdam.
```

It contains:

```text
population
Dutch city
Amsterdam
numbers
```

but it is still not the correct answer.

That is much harder.

[[IMAGE_NEEDED: Easy versus semi-hard versus hard negatives | Show an anchor query with three negative answers: unrelated, topically related, and highly similar but incorrect | Learner should understand that difficult negatives force the model to learn finer semantic distinctions]]

### Three negative categories in the chapter

#### Easy negatives

Random unrelated examples.

#### Semi-hard negatives

Examples retrieved as semantically related by a pretrained embedding model.

#### Hard negatives

Examples very close to the target but still wrong.

These often require:

- human labeling,
- retrieval + manual review,
- generative-model assistance,
- stronger teacher models.

---

## 27. Hard-negative mining is often a data problem

Training code is often easier than finding excellent contrastive examples.

A good embedding dataset needs:

```text
clear positives
+
informative negatives
```

Poor negatives can make the task trivial.

Incorrect negatives can actively damage the model.

The chapter therefore emphasizes that:

> High-quality data is one of the hardest parts of embedding-model training.

This matters especially for domain-specific retrieval.

---

{{exercise:M10.L01.EX01}}

---

## 28. Fine-tune an existing embedding model instead of starting from a generic backbone

Starting from:

```text
bert-base-uncased
```

requires teaching the model sentence-level embedding behavior.

A more efficient alternative is:

```text
start from an already trained sentence embedding model
```

and specialize it.

The chapter uses:

```python
SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
```

Then it fine-tunes with MNR loss.

This usually requires less work than building the sentence-embedding behavior from the generic language-model backbone.

---

## 29. Supervised embedding fine-tuning

The workflow is:

```text
pretrained embedding model
+
labeled contrastive data
+
loss function
+
evaluator
→ domain/task-adapted embedding model
```

The chapter reports approximately:

```text
Pearson cosine ≈ 0.851
```

for the all-MiniLM-L6-v2 fine-tuning demonstration.

But the source also gives an important caveat:

> That pretrained model had already been trained on the full MNLI dataset, while the demonstration fine-tuned it on only a subset.

So the number should not be interpreted as a clean independent improvement caused only by the new fine-tuning run.

This is a good lesson in experimental interpretation.

---

## 30. Adapt the language model to the domain before contrastive training

The chapter suggests another option.

If a generic BERT model does not understand your domain vocabulary well, you can first adapt it using an unsupervised language-modeling objective.

Conceptually:

```text
generic pretrained Transformer
      ↓
domain-adaptive pretraining
      ↓
domain-aware Transformer
      ↓
contrastive sentence-embedding training
```

This separates two problems:

```text
learn domain language
and
learn task-specific embedding geometry
```

The next sections return to this idea through TSDAE.

---

## 31. The main bottleneck is often the training data

Positive pairs are frequently easier to create.

Examples include:

```text
question ↔ answer
title ↔ abstract
duplicate question ↔ duplicate question
query ↔ clicked/relevant result
sentence ↔ paraphrase
```

Hard negatives are more difficult.

You need examples that are:

```text
plausibly related
but
actually wrong
```

That is much more informative than random noise.

The quality of these pairs can matter as much as the model architecture.

---

## 32. What if labeled data is scarce? Augmented SBERT

Large embedding models are often trained on huge pair datasets.

But a real company may have:

```text
2,000 labeled examples
5,000 labeled examples
10,000 labeled examples
```

rather than millions.

The chapter introduces:

```text
Augmented SBERT
```

to expand a small labeled dataset.

The central idea:

```text
train accurate but slow teacher
→ label more data
→ train fast embedding model on expanded data
```

[[IMAGE_NEEDED: Augmented SBERT overview | Show small gold dataset → train cross-encoder teacher → label many unlabeled sentence pairs → silver dataset → combine gold + silver → train bi-encoder/SBERT | Learner should memorize the teacher-labeler-student workflow]]

---

## 33. Gold data versus silver data

The chapter uses two names.

### Gold dataset

Human-annotated ground truth.

```text
high confidence
smaller
more expensive
```

### Silver dataset

Automatically labeled examples produced by a trained model.

```text
larger
cheaper
not guaranteed ground truth
```

The goal is:

```text
gold quality
+
silver scale
```

to create a larger training set.

---

## 34. The four Augmented SBERT steps

### Step 1 — Train a cross-encoder on gold data

The teacher learns pairwise similarity/classification from the labeled examples.

### Step 2 — Create additional sentence pairs

These pairs may come from:

- existing unlabeled data,
- random recombinations,
- retrieval-based candidate generation.

### Step 3 — Label them with the cross-encoder

The teacher predicts labels.

These become:

```text
silver data
```

### Step 4 — Train the bi-encoder

Train the faster sentence embedding model on:

```text
gold + silver
```

The cross-encoder is accurate but slow.

The bi-encoder is efficient at producing reusable embeddings.

Augmented SBERT uses the first to improve training data for the second.

---

## 35. Candidate generation affects silver-data quality

If you generate new sentence pairs randomly, most may be obviously unrelated.

That creates many easy negatives.

The chapter suggests a better strategy:

```text
use an existing embedding model
→ retrieve top-k semantically similar candidates
→ let the cross-encoder label them
```

This focuses labeling effort on harder, more informative examples.

The initial embedding model may be imperfect, but it can still be useful for candidate generation.

---

## 36. Augmented SBERT can recover much of the performance with less gold data

The chapter simulates limited labeled data.

It uses:

```text
10,000 gold examples
```

and labels additional examples with the trained cross-encoder.

The reported result is approximately:

```text
Pearson cosine ≈ 0.710
```

The earlier cosine-loss experiment using the larger original training set reported about:

```text
0.722
```

The chapter’s lesson is that augmentation can approach the larger-data result while requiring fewer manually labeled examples.

Again, the exact scores are experiment-specific.

---

## 37. What if you have no labels at all?

Many real datasets have:

```text
documents
but no similarity labels
```

The chapter mentions several unsupervised approaches, including:

```text
SimCSE
Contrastive Tension
TSDAE
GPL
```

It then focuses on:

```text
TSDAE
```

because of its usefulness for unsupervised embedding learning and domain adaptation.

---

## 38. TSDAE: learn embeddings by reconstructing damaged sentences

TSDAE stands for:

```text
Transformer-based Sequential Denoising Auto-Encoder
```

Its core idea:

```text
original sentence
      ↓
remove some words
      ↓
damaged sentence
      ↓
encoder
      ↓
sentence embedding
      ↓
decoder
      ↓
reconstruct original sentence
```

[[IMAGE_NEEDED: TSDAE denoising autoencoder | Show original sentence → word deletion/noise → damaged sentence → encoder → single sentence embedding → decoder → reconstructed original sentence | Learner should understand that reconstruction pressure teaches the embedding to preserve sentence information]]

Example from the chapter:

```text
Original:
Grim faces and hardened jaws are not people-friendly.

Damaged:
Grim jaws are.
```

The system must use the compressed embedding representation to reconstruct the original.

---

## 39. Why reconstruction can teach useful sentence embeddings

Imagine an embedding that forgets almost everything about the sentence.

The decoder would be unable to reconstruct the original.

Therefore training rewards embeddings that preserve important information.

The logic is:

```text
better sentence representation
→ better reconstruction
```

After training, we keep the encoder for embedding generation.

The decoder is mainly needed for the denoising training objective.

---

## 40. TSDAE versus masked language modeling

Masked language modeling asks the model to reconstruct missing token-level information.

TSDAE instead damages the sentence and asks the decoder to reconstruct the entire original sequence from the sentence embedding.

Conceptually:

```text
MLM:
recover missing tokens from context

TSDAE:
compress damaged sentence
→ sentence embedding
→ reconstruct original sentence
```

This directly pressures the sentence-level vector to carry meaningful information.

---

## 41. TSDAE needs sentences, not human labels

The chapter creates a flat text collection from MNLI sentences.

Then labels are ignored.

Noise is introduced automatically.

So the training data becomes:

```text
damaged sentence
original sentence
```

rather than:

```text
sentence A
sentence B
human similarity label
```

This is why TSDAE is an unsupervised approach.

---

## 42. The chapter uses CLS pooling for TSDAE

For this example, the chapter creates:

```text
Transformer backbone
+
CLS pooling
```

rather than mean pooling.

The source explains that the TSDAE paper found CLS pooling useful for this reconstruction setting because mean pooling can discard positional information needed for reconstruction.

The important lesson is:

> Pooling strategy can depend on the training objective.

There is no universal pooling rule for every embedding-learning setup.

---

## 43. DenoisingAutoEncoderLoss

The chapter uses:

```text
DenoisingAutoEncoderLoss
```

The decoder tries to reconstruct the original sentence from the embedding of the damaged sentence.

It also ties some encoder/decoder parameters.

Conceptually:

```text
damaged input
→ encoder parameters
→ sentence vector
→ decoder
→ reconstruction loss
→ update representation model
```

The objective directly measures how much useful information survived the compression.

---

## 44. TSDAE produces useful embeddings without labels

The chapter reports approximately:

```text
Pearson cosine ≈ 0.699
```

after TSDAE training.

The important point is not that `0.699` beats every supervised method.

It does not in these experiments.

The important point is:

> The model learned a useful sentence representation without human-provided similarity labels.

That makes TSDAE valuable when labeled pair data is scarce.

---

## 45. Domain adaptation: teach an embedding model your language

General embedding models may underrepresent specialized concepts.

Examples:

```text
legal clauses
medical terminology
semiconductor manufacturing
internal product names
academic subfields
```

The target domain may contain words, topics, and relationships underrepresented in general pretraining data.

Domain adaptation aims to move the model toward that target domain.

[[IMAGE_NEEDED: Domain adaptation | Show a generic source-domain embedding model being adapted using unlabeled target-domain documents, producing a new model whose representation space better reflects target terminology and concepts | Learner should understand domain adaptation as specialization rather than training from nothing]]

---

## 46. Adaptive pretraining before supervised fine-tuning

The chapter proposes a two-stage pattern.

### Stage 1 — Unsupervised domain adaptation

Train on target-domain text using:

```text
TSDAE
or
masked language modeling
```

This helps the model learn the language of the domain.

### Stage 2 — Supervised embedding fine-tuning

Use:

```text
general-domain labeled pairs
or
target-domain labeled pairs
```

to shape the embedding space.

Conceptually:

```text
general model
   ↓
unsupervised target-domain adaptation
   ↓
domain-aware model
   ↓
contrastive supervised fine-tuning
   ↓
task-ready embedding model
```

This allows unlabeled in-domain text to contribute even when labeled in-domain data is limited.

---

## 47. What the chapter’s experiments teach

The reported examples are roughly:

| Training approach | Approx. Pearson cosine reported |
|---|---:|
| Softmax-loss baseline | 0.598 |
| Cosine similarity loss | 0.722 |
| Multiple Negatives Ranking loss | 0.809 |
| Fine-tuned pretrained MiniLM embedding model | 0.851 |
| Augmented SBERT | 0.710 |
| TSDAE | 0.699 |

Do not read this as a universal leaderboard.

The experiments differ in:

- starting model,
- amount of data,
- labeling assumptions,
- training objective,
- whether the starting model had already seen related data.

The useful conclusions are qualitative:

```text
loss function matters
negative quality matters
starting checkpoint matters
data scale matters
domain fit matters
evaluation design matters
```

---

## 48. A practical embedding-model development workflow

A strong workflow can be:

### Step 1 — Define the intended similarity

Ask:

```text
semantic?
retrieval relevance?
sentiment?
domain-specific equivalence?
```

### Step 2 — Choose the starting model

Decide whether to use:

```text
generic Transformer backbone
or
pretrained embedding model
```

### Step 3 — Build training relationships

Collect:

```text
positive pairs
negative pairs
hard negatives
similarity scores
```

depending on the objective.

### Step 4 — Choose the loss

Examples:

```text
cosine similarity loss
MNR loss
denoising loss
```

### Step 5 — Train

Configure:

```text
batch size
epochs
warmup
precision
evaluation schedule
```

### Step 6 — Evaluate

Use:

```text
STSB
domain-specific retrieval set
MTEB tasks
latency measurements
```

### Step 7 — Analyze failures

Inspect:

- false neighbors,
- hard negatives,
- domain terms,
- query/document mismatches.

### Step 8 — Improve the data

Often the highest-value improvement is:

```text
better examples
rather than
more architecture complexity
```

### Step 9 — Adapt to the target domain

Use:

```text
unsupervised target-domain adaptation
+
supervised fine-tuning
```

if needed.

[[IMAGE_NEEDED: Embedding model development lifecycle | Show objective definition → data pairs/negatives → model/loss → training → evaluation → error analysis → better data/domain adaptation → retraining | Learner should see embedding development as an iterative data-and-objective loop]]

---

{{exercise:M10.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> A good embedding model always places semantically similar text close together.

### Why this is incomplete

The embedding objective may intentionally focus on sentiment, retrieval relevance, or another task-specific relationship instead of broad semantic similarity.

---

### Misconception 2

> Cross-encoders are always better because they can compare both sentences jointly.

### Why this is incomplete

Cross-encoders can be accurate, but they are much more expensive when comparing large numbers of texts and generally do not create reusable independent embeddings.

---

### Misconception 3

> SBERT uses two completely different BERT models.

### Why this is wrong

The Siamese/bi-encoder setup uses shared weights. Conceptually there are two branches during pair processing, but they are the same encoder parameters.

---

### Misconception 4

> Any negative example is equally useful.

### Why this is wrong

Easy random negatives may teach very little. Hard negatives force the model to distinguish highly similar but incorrect alternatives.

---

### Misconception 5

> A larger batch only affects training speed.

### Why this is wrong

With MNR loss, larger batches also provide more in-batch negative candidates and can make the ranking task more difficult.

---

### Misconception 6

> Fine-tuning an embedding model is mainly a coding challenge.

### Why this is wrong

The chapter repeatedly emphasizes that collecting high-quality positive and especially hard-negative pairs is a major difficulty.

---

### Misconception 7

> Silver data is equivalent to gold ground truth.

### Why this is wrong

Silver labels are predictions produced by another model and can contain errors.

---

### Misconception 8

> Unsupervised embedding training means the model receives no training signal.

### Why this is wrong

TSDAE generates its own signal by damaging sentences and training the model to reconstruct the original sentence.

---

### Misconception 9

> TSDAE is always better than supervised contrastive learning.

### Why this is wrong

The chapter notes that supervised methods generally outperform unsupervised ones when good labeled data exists. TSDAE is valuable when labels are missing and for adaptation.

---

### Misconception 10

> One benchmark score is enough to select an embedding model.

### Why this is wrong

Embedding use cases differ. Broader benchmarks such as MTEB and domain-specific evaluation are needed, and latency may matter too.

---

## Key terminology

| Term | Meaning |
|---|---|
| Embedding model | Model that converts text into dense numerical representations |
| Embedding space | Vector space in which relationships between embeddings are represented geometrically |
| Semantic similarity | Degree to which two texts express related meaning |
| Contrastive learning | Training strategy that learns by comparing similar and dissimilar examples |
| Positive pair | Two examples that should be represented as related |
| Negative pair | Two examples that should be represented as unrelated |
| Cross-encoder | Model that processes two texts jointly and outputs a relationship/relevance score |
| Bi-encoder | Model that encodes two texts independently into reusable embeddings |
| SBERT | Sentence-BERT / sentence-transformer bi-encoder architecture |
| Siamese network | Two processing branches sharing identical weights |
| Pooling | Operation reducing token-level representations to one fixed-size sentence vector |
| Mean pooling | Averaging token representations |
| CLS pooling | Using a special classification-token representation as the sentence vector |
| NLI | Natural Language Inference |
| MNLI | Multi-Genre Natural Language Inference dataset |
| Entailment | Relationship where the hypothesis follows from the premise |
| Contradiction | Relationship where the hypothesis conflicts with the premise |
| Neutral | Relationship where neither entailment nor contradiction holds |
| STSB | Semantic Textual Similarity Benchmark |
| MTEB | Massive Text Embedding Benchmark |
| Softmax loss | Classification-oriented loss used as the chapter’s baseline example |
| Cosine similarity loss | Loss aligning embedding cosine similarity with target similarity scores |
| MNR loss | Multiple Negatives Ranking loss |
| In-batch negative | Example from the current batch reused as a negative candidate |
| Easy negative | Clearly unrelated negative example |
| Semi-hard negative | Related example that is not extremely difficult |
| Hard negative | Highly similar but incorrect/dissimilar example |
| Gold dataset | Human-labeled ground-truth dataset |
| Silver dataset | Automatically labeled dataset created by a teacher model |
| Augmented SBERT | Data-augmentation approach using a cross-encoder teacher to label extra pairs for bi-encoder training |
| TSDAE | Transformer-based Sequential Denoising Auto-Encoder |
| Denoising | Corrupting input so the model must reconstruct the original |
| Domain adaptation | Adapting a model from a source domain to a target domain |
| Adaptive pretraining | Additional pretraining on target-domain text before downstream fine-tuning |

---

## Self-check

Before moving on, make sure you can answer:

1. What does an embedding model produce?
2. Why does the definition of “good similarity” depend on the downstream task?
3. What is contrastive learning?
4. Why are negative examples necessary?
5. How does word2vec relate conceptually to contrastive learning?
6. How does a cross-encoder differ from a bi-encoder?
7. Why does the cross-encoder become expensive at large scale?
8. Why are reusable embeddings useful for retrieval?
9. What does mean pooling do?
10. Why is SBERT described as Siamese?
11. What two ingredients are required for contrastive training?
12. How can NLI labels be converted into contrastive relationships?
13. What is MNLI?
14. What does STSB evaluate?
15. Why is correlation useful for evaluating embedding similarity?
16. What does MTEB add beyond one benchmark?
17. What is cosine similarity loss optimizing?
18. What does MNR loss ask an embedding model to do?
19. What is an in-batch negative?
20. Why can a larger MNR batch be more useful?
21. What is the difference between easy and hard negatives?
22. Why are hard negatives difficult to collect?
23. Why might fine-tuning an existing sentence-transformer be more efficient than starting with generic BERT?
24. What is the difference between gold and silver data?
25. What are the four major steps in Augmented SBERT?
26. Why use a cross-encoder as a teacher?
27. What does TSDAE do to the input sentence?
28. Why can sentence reconstruction produce useful embeddings?
29. Why is TSDAE considered unsupervised?
30. What role can TSDAE play in domain adaptation?
31. Why should embedding evaluation include target-domain tasks?
32. Design a complete training workflow for a domain-specific retrieval embedding model.

---

## Retain this idea

**An embedding model is not useful merely because it turns text into vectors; it is useful when the geometry of those vectors reflects the relationships your application cares about. Contrastive learning creates that geometry by teaching which examples belong together and which must remain apart. Sentence-transformers makes this practical through reusable bi-encoder embeddings, while the training data, loss function, negative difficulty, evaluation task, and starting checkpoint determine what the model ultimately learns. When labels are limited, Augmented SBERT can expand training data; when labels are absent, TSDAE can learn from reconstruction; and when the domain changes, unsupervised adaptation followed by fine-tuning can specialize the representation space.**
"""
        ),

        "estimated_minutes": 225,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "embedding-models", "title": "What is an embedding model trying to do?", "order": 1},
            {"id": "what-should-embedding-capture", "title": "A good embedding depends on what similarity means", "order": 2},
            {"id": "contrastive-learning", "title": "Contrastive learning: learn by comparison", "order": 3},
            {"id": "dog-cat-intuition", "title": "The dog-versus-cat intuition", "order": 4},
            {"id": "word2vec-connection", "title": "Contrastive learning already appeared in word2vec", "order": 5},
            {"id": "cross-encoder-problem", "title": "Why not use a cross-encoder for everything?", "order": 6},
            {"id": "naive-bert-embeddings", "title": "Why simple BERT sentence pooling was not enough", "order": 7},
            {"id": "sbert", "title": "SBERT: create reusable sentence embeddings", "order": 8},
            {"id": "siamese", "title": "Why the architecture is called Siamese", "order": 9},
            {"id": "pooling", "title": "Pool token representations into one sentence vector", "order": 10},
            {"id": "two-needs", "title": "Two things contrastive training requires", "order": 11},
            {"id": "nli", "title": "Natural Language Inference as contrastive data", "order": 12},
            {"id": "mnli", "title": "The chapter’s MNLI training data", "order": 13},
            {"id": "train-from-backbone", "title": "Build an embedding model from a pretrained Transformer backbone", "order": 14},
            {"id": "softmax-loss", "title": "Baseline training with softmax loss", "order": 15},
            {"id": "stsb", "title": "Evaluate semantic similarity with STSB", "order": 16},
            {"id": "correlation", "title": "Interpret the evaluation score", "order": 17},
            {"id": "training-arguments", "title": "Understand the main training arguments", "order": 18},
            {"id": "mteb", "title": "One benchmark is not enough: MTEB", "order": 19},
            {"id": "loss-functions", "title": "Loss functions shape the embedding space", "order": 20},
            {"id": "cosine-loss", "title": "Cosine similarity loss", "order": 21},
            {"id": "mnr", "title": "Multiple Negatives Ranking loss", "order": 22},
            {"id": "in-batch-negatives", "title": "In-batch negatives make one batch much more informative", "order": 23},
            {"id": "mnr-result", "title": "MNR can produce much stronger embeddings", "order": 24},
            {"id": "easy-negatives", "title": "Easy negatives may make training too easy", "order": 25},
            {"id": "hard-negatives", "title": "Hard negatives force more precise representations", "order": 26},
            {"id": "negative-mining", "title": "Hard-negative mining is often a data problem", "order": 27},
            {"id": "fine-tune-pretrained", "title": "Fine-tune an existing embedding model instead of starting from a generic backbone", "order": 28},
            {"id": "supervised-finetuning", "title": "Supervised embedding fine-tuning", "order": 29},
            {"id": "domain-adaptation-note", "title": "Adapt the language model to the domain before contrastive training", "order": 30},
            {"id": "data-bottleneck", "title": "The main bottleneck is often the training data", "order": 31},
            {"id": "augmented-sbert", "title": "What if labeled data is scarce? Augmented SBERT", "order": 32},
            {"id": "gold-silver", "title": "Gold data versus silver data", "order": 33},
            {"id": "aug-sbert-steps", "title": "The four Augmented SBERT steps", "order": 34},
            {"id": "silver-pair-quality", "title": "Candidate generation affects silver-data quality", "order": 35},
            {"id": "aug-sbert-result", "title": "Augmented SBERT can recover much of the performance with less gold data", "order": 36},
            {"id": "unsupervised", "title": "What if you have no labels at all?", "order": 37},
            {"id": "tsdae", "title": "TSDAE: learn embeddings by reconstructing damaged sentences", "order": 38},
            {"id": "tsdae-intuition", "title": "Why reconstruction can teach useful sentence embeddings", "order": 39},
            {"id": "tsdae-vs-mlm", "title": "TSDAE versus masked language modeling", "order": 40},
            {"id": "tsdae-data", "title": "TSDAE needs sentences, not human labels", "order": 41},
            {"id": "tsdae-pooling", "title": "The chapter uses CLS pooling for TSDAE", "order": 42},
            {"id": "tsdae-loss", "title": "DenoisingAutoEncoderLoss", "order": 43},
            {"id": "tsdae-result", "title": "TSDAE produces useful embeddings without labels", "order": 44},
            {"id": "domain-adaptation", "title": "Domain adaptation: teach an embedding model your language", "order": 45},
            {"id": "adaptive-pretraining", "title": "Adaptive pretraining before supervised fine-tuning", "order": 46},
            {"id": "experiment-results", "title": "What the chapter’s experiments teach", "order": 47},
            {"id": "workflow", "title": "A practical embedding-model development workflow", "order": 48},
            {"id": "misconceptions", "title": "Important misconceptions", "order": 49},
            {"id": "terminology", "title": "Key terminology", "order": 50},
            {"id": "self-check", "title": "Self-check", "order": 51},
            {"id": "retain", "title": "Retain this idea", "order": 52},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M10.L01.EX01",

            "title": "Compare Embedding Losses and Negative Quality",

            "lesson_code": "M10.L01",

            "section_id": "negative-mining",

            "placement": "after_section",

            "description": (
                "Build intuition for how the loss function and negative examples change "
                "the learned embedding space."
            ),

            "instructions": (
                "Use a manageable semantic-similarity or NLI dataset.\n"
                "1. Start from the same base Transformer or sentence-transformer for "
                "all experiments.\n"
                "2. Train or conceptually configure one model with cosine similarity loss.\n"
                "3. Train or conceptually configure another with Multiple Negatives Ranking loss.\n"
                "4. Evaluate both on the same STSB-style evaluator or held-out similarity set.\n"
                "5. Create five anchor-positive examples.\n"
                "6. For each anchor, write one easy negative and one hard negative.\n"
                "7. Explain why each hard negative is difficult but still incorrect.\n"
                "8. If compute allows, fine-tune once using easy/random negatives and "
                "once using harder mined negatives.\n"
                "9. Compare the resulting nearest neighbors for at least five test queries.\n"
                "10. Write a conclusion explaining whether the model architecture, "
                "loss, or training data appeared to have the strongest effect."
            ),

            "expected_output": (
                "A notebook or report containing loss configurations, evaluation results, "
                "easy/hard negative examples, nearest-neighbor comparisons, and a written "
                "analysis of how objective and data difficulty affected the embedding space."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "contrastive-learning",
                "cosine-similarity-loss",
                "mnr-loss",
                "hard-negatives",
                "embedding-evaluation",
                "error-analysis",
            ],
        },

        {
            "id": "M10.L01.EX02",

            "title": "Design a Domain-Specific Embedding Training Pipeline",

            "lesson_code": "M10.L01",

            "section_id": "workflow",

            "placement": "after_section",

            "description": (
                "Design a realistic end-to-end embedding adaptation strategy using "
                "the supervised, augmented, and unsupervised techniques from the chapter."
            ),

            "instructions": (
                "Assume you need an embedding model for semantic search over a specialized "
                "technical knowledge base and have 100,000 unlabeled documents but only "
                "3,000 labeled query-document pairs.\n"
                "1. Define what similarity/relevance means for the application.\n"
                "2. Choose a pretrained starting embedding model and explain why starting "
                "from it is preferable to a generic BERT backbone.\n"
                "3. Define how the 3,000 labeled pairs will be split into train/evaluation data.\n"
                "4. Define how positive pairs and hard negatives will be created.\n"
                "5. Decide whether you would apply TSDAE to the 100,000 unlabeled documents "
                "before supervised fine-tuning. Explain your reasoning.\n"
                "6. Design an Augmented SBERT step that trains a cross-encoder teacher "
                "and labels additional candidate pairs.\n"
                "7. Explain how you would generate candidate pairs for the silver dataset "
                "without relying only on random sampling.\n"
                "8. Choose a contrastive loss for the final bi-encoder training.\n"
                "9. Define both general evaluation and domain-specific retrieval evaluation.\n"
                "10. Include latency, indexing speed, and model size in the final model-selection criteria."
            ),

            "expected_output": (
                "A complete embedding-training architecture covering target similarity, "
                "starting checkpoint, TSDAE/domain adaptation, gold/silver data, hard-negative "
                "mining, cross-encoder teacher, bi-encoder fine-tuning, evaluation, and "
                "deployment tradeoffs."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "embedding-system-design",
                "domain-adaptation",
                "augmented-sbert",
                "tsdae",
                "hard-negative-mining",
                "retrieval-evaluation",
                "model-selection",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M10.L01.QZ01",

        "title": "Creating Text Embedding Models — Knowledge Check",

        "lesson_code": "M10.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M10.L01.Q01",
                "section_id": "what-should-embedding-capture",
                "question": (
                    "Why can two embedding models organize the same texts differently?"
                ),
                "options": [
                    "Because an embedding objective can be trained to emphasize different relationships such as semantic meaning or sentiment.",
                    "Because embeddings cannot represent meaning.",
                    "Because every model must use random coordinates.",
                    "Because vector spaces cannot be fine-tuned.",
                ],
                "correct": 0,
                "explanation": (
                    "Training data and objectives define which relationships the vector "
                    "geometry should preserve."
                ),
            },
            {
                "id": "M10.L01.Q02",
                "section_id": "contrastive-learning",
                "question": "What is the core goal of contrastive learning?",
                "options": [
                    "Make every embedding identical.",
                    "Pull related examples closer and push unrelated examples farther apart.",
                    "Convert all sentences into labels.",
                    "Remove negative examples.",
                ],
                "correct": 1,
                "explanation": (
                    "Contrastive learning shapes the embedding geometry from examples "
                    "of similarity and dissimilarity."
                ),
            },
            {
                "id": "M10.L01.Q03",
                "section_id": "cross-encoder-problem",
                "question": "Why is a cross-encoder expensive for large-scale similarity search?",
                "options": [
                    "It must jointly process each query-document or sentence pair.",
                    "It cannot use GPUs.",
                    "It produces vectors that are too small.",
                    "It requires no model inference.",
                ],
                "correct": 0,
                "explanation": (
                    "Each candidate pair requires a new joint forward pass, so the "
                    "number of computations grows rapidly."
                ),
            },
            {
                "id": "M10.L01.Q04",
                "section_id": "sbert",
                "question": "What is the main scaling advantage of a bi-encoder?",
                "options": [
                    "Each text can be embedded independently and reused for many comparisons.",
                    "It always produces perfect similarity scores.",
                    "It does not need training data.",
                    "It concatenates all documents into one sequence.",
                ],
                "correct": 0,
                "explanation": (
                    "Independent reusable vectors make retrieval and large-scale comparison much cheaper."
                ),
            },
            {
                "id": "M10.L01.Q05",
                "section_id": "siamese",
                "question": "Why is the SBERT training architecture described as Siamese?",
                "options": [
                    "Two branches process sentences using shared encoder weights.",
                    "Two unrelated models are trained with different vocabularies.",
                    "The model always processes exactly two languages.",
                    "The pooling layer is duplicated permanently.",
                ],
                "correct": 0,
                "explanation": (
                    "The branches are conceptually separate during pair processing but "
                    "use the same model parameters."
                ),
            },
            {
                "id": "M10.L01.Q06",
                "section_id": "nli",
                "question": "Why is NLI useful for embedding training?",
                "options": [
                    "Entailment, neutral, and contradiction relationships can be turned into similarity/contrast examples.",
                    "NLI contains only images.",
                    "NLI removes the need for a loss function.",
                    "NLI always provides hard negatives.",
                ],
                "correct": 0,
                "explanation": (
                    "NLI naturally supplies sentence-pair relationships that can guide "
                    "contrastive learning."
                ),
            },
            {
                "id": "M10.L01.Q07",
                "section_id": "stsb",
                "question": "What does STSB primarily provide?",
                "options": [
                    "Human-labeled sentence-pair similarity scores",
                    "Image-caption pairs",
                    "Only contradiction examples",
                    "A vector database",
                ],
                "correct": 0,
                "explanation": (
                    "STSB is used to compare embedding similarity against human judgments."
                ),
            },
            {
                "id": "M10.L01.Q08",
                "section_id": "mteb",
                "question": "Why use MTEB instead of relying on one similarity benchmark?",
                "options": [
                    "It evaluates embedding models across multiple task families and datasets.",
                    "It only measures GPU memory.",
                    "It trains the model automatically.",
                    "It removes the need for domain evaluation.",
                ],
                "correct": 0,
                "explanation": (
                    "Embedding quality is task-dependent, so broader benchmark coverage "
                    "reveals strengths and weaknesses."
                ),
            },
            {
                "id": "M10.L01.Q09",
                "section_id": "cosine-loss",
                "question": "What does cosine similarity loss try to align?",
                "options": [
                    "Predicted embedding cosine similarity with a target similarity score.",
                    "The number of tokens with the batch size.",
                    "The vocabulary size with the GPU memory.",
                    "The classifier label with a document ID.",
                ],
                "correct": 0,
                "explanation": (
                    "The loss adjusts embeddings so their cosine similarity approaches "
                    "the labeled similarity value."
                ),
            },
            {
                "id": "M10.L01.Q10",
                "section_id": "mnr",
                "question": "What does Multiple Negatives Ranking loss encourage?",
                "options": [
                    "The anchor to rank its true positive above competing negative candidates.",
                    "All examples to have equal similarity.",
                    "Only the negative examples to be embedded.",
                    "The model to generate text instead of vectors.",
                ],
                "correct": 0,
                "explanation": (
                    "MNR treats the learning problem as selecting the correct positive "
                    "from a set of competing candidates."
                ),
            },
            {
                "id": "M10.L01.Q11",
                "section_id": "in-batch-negatives",
                "question": "Why can larger batches help MNR loss?",
                "options": [
                    "They provide more in-batch negative candidates, making the ranking task harder.",
                    "They remove all negatives.",
                    "They make every sentence shorter.",
                    "They disable cosine similarity.",
                ],
                "correct": 0,
                "explanation": (
                    "More candidates create a more demanding contrastive ranking problem."
                ),
            },
            {
                "id": "M10.L01.Q12",
                "section_id": "hard-negatives",
                "question": "What is a hard negative?",
                "options": [
                    "An unrelated random sentence.",
                    "A highly similar/plausible example that is still incorrect or not the true match.",
                    "The positive example itself.",
                    "A sentence that cannot be tokenized.",
                ],
                "correct": 1,
                "explanation": (
                    "Hard negatives force the model to learn subtle distinctions rather "
                    "than relying on obvious topic differences."
                ),
            },
            {
                "id": "M10.L01.Q13",
                "section_id": "gold-silver",
                "question": "What is silver data in Augmented SBERT?",
                "options": [
                    "Automatically labeled examples produced by a teacher model.",
                    "Only manually verified human labels.",
                    "Unlabeled text that is never used.",
                    "A model checkpoint format.",
                ],
                "correct": 0,
                "explanation": (
                    "Silver data expands the training set using predictions from the "
                    "fine-tuned cross-encoder."
                ),
            },
            {
                "id": "M10.L01.Q14",
                "section_id": "aug-sbert-steps",
                "question": "Why does Augmented SBERT use a cross-encoder before training the bi-encoder?",
                "options": [
                    "The cross-encoder serves as a more accurate teacher for labeling additional sentence pairs.",
                    "The cross-encoder creates image embeddings.",
                    "The bi-encoder cannot process text.",
                    "The cross-encoder replaces the evaluation benchmark.",
                ],
                "correct": 0,
                "explanation": (
                    "The teacher generates silver labels that increase the amount of "
                    "training data available to the efficient bi-encoder."
                ),
            },
            {
                "id": "M10.L01.Q15",
                "section_id": "tsdae",
                "question": "What is the main training idea behind TSDAE?",
                "options": [
                    "Damage a sentence, encode it into one vector, and reconstruct the original sentence.",
                    "Use only human similarity labels.",
                    "Train a cross-encoder on images.",
                    "Randomly assign embeddings.",
                ],
                "correct": 0,
                "explanation": (
                    "Denoising reconstruction pressures the sentence embedding to "
                    "retain enough information about the original input."
                ),
            },
            {
                "id": "M10.L01.Q16",
                "section_id": "domain-adaptation",
                "question": "Why use unsupervised domain adaptation before supervised embedding fine-tuning?",
                "options": [
                    "To expose the model to target-domain language and concepts before shaping the final embedding objective.",
                    "To remove all domain-specific words.",
                    "To guarantee zero training cost.",
                    "To replace the tokenizer with labels.",
                ],
                "correct": 0,
                "explanation": (
                    "Unsupervised target-domain training can improve the model's familiarity "
                    "with specialized language before contrastive fine-tuning."
                ),
            },
            {
                "id": "M10.L01.Q17",
                "section_id": "workflow",
                "type": "open",
                "question": (
                    "You need to build a semantic-search embedding model for a specialized "
                    "domain with abundant unlabeled documents but limited labeled query-document "
                    "pairs. Design a training strategy using concepts from this chapter. Include "
                    "the starting checkpoint, TSDAE/domain adaptation, positive pairs, hard "
                    "negatives, loss function, possible Augmented SBERT teacher labeling, and "
                    "both general and domain-specific evaluation."
                ),
            },
        ],

        "passing_score": 70,
    },
}
