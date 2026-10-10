"""M04.L01 — Text Classification.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 4; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"

MODULE_ORDER = 4

MODULE_TITLE = "Text Classification"

MODULE_DESCRIPTION = (
    "Learn how pretrained representation and generative language models can be "
    "used for text classification through task-specific models, frozen embedding "
    "models plus lightweight classifiers, zero-shot embedding similarity, and "
    "prompted generative models, with practical evaluation using precision, recall, "
    "accuracy, and F1."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Text Classification",

    "slug": "llm-foundations-m04-l01",

    "description": (
        "A practical introduction to classifying text with pretrained language "
        "models, comparing task-specific encoder models, frozen text embeddings "
        "with classical classifiers, zero-shot embedding classification, and "
        "generative sequence-to-sequence or chat models."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.5,

    "skill_tags": [
        "text-classification",
        "sentiment-analysis",
        "representation-models",
        "task-specific-models",
        "embeddings",
        "logistic-regression",
        "zero-shot-classification",
        "cosine-similarity",
        "generative-classification",
        "flan-t5",
        "prompt-engineering",
        "precision",
        "recall",
        "f1-score",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M02.L01",
        "M03.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Text Classification",

        "content": (
            r"""
# Text Classification

> **Course:** Large Language Models Foundations  
> **Lesson:** M04.L01  
> **Module:** Text Classification  
> **Source alignment:** Chapter 4, “Text Classification.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what a text-classification task is.
- Distinguish **binary**, multiclass, and task-specific classification at a conceptual level.
- Load and inspect a labeled text dataset.
- Explain the difference between **representation models** and **generative models** for classification.
- Use a pretrained **task-specific classifier**.
- Explain why domain mismatch can affect classification quality.
- Read a confusion-matrix interpretation.
- Explain **precision, recall, accuracy, and F1** in learner-friendly language.
- Use a frozen embedding model as a feature extractor.
- Train a lightweight classifier such as logistic regression on embeddings.
- Explain why this approach is cheaper than fine-tuning the full language model.
- Perform **zero-shot classification** using label descriptions and cosine similarity.
- Explain how label wording can affect zero-shot performance.
- Use a generative model such as Flan-T5 for classification by prompting it.
- Explain why generated text must often be mapped back to numerical labels for evaluation.
- Compare task-specific models, embedding-based approaches, and generative approaches.
- Recognize important evaluation caveats, including possible benchmark contamination for opaque closed models.

---

## 1. What is text classification?

Text classification asks a model to assign one or more labels to text.

The simplest mental model is:

```text
Text
  ↓
Classifier
  ↓
Label
```

For example:

```text
"I loved this movie."

→ Positive
```

or:

```text
"This was boring and disappointing."

→ Negative
```

The chapter focuses on **sentiment classification**, but the same basic idea appears in many tasks:

```text
customer message → intent
email → spam / not spam
article → topic
review → positive / negative
text → language
document → category
```

The model is not being asked to write a long answer.

It is being asked to decide:

> Which class best describes this input?

{{image:text-classification-overview}}

### Classification can be binary or multiclass

The chapter uses two sentiment labels:

```text
0 → negative
1 → positive
```

This is a **binary classification** problem because there are two possible classes.

A multiclass task might instead use:

```text
billing
technical_support
sales
account_access
other
```

The same general ideas still apply.

---

## 2. Four practical routes to classification

This chapter is especially useful because it does not present classification as one single technique.

Instead, it demonstrates several approaches.

### Route 1 — Task-specific representation model

```text
text
 ↓
pretrained classifier
 ↓
class scores
 ↓
label
```

The whole model has already been fine-tuned for a classification task.

### Route 2 — Embeddings + lightweight supervised classifier

```text
text
 ↓
frozen embedding model
 ↓
text vector
 ↓
logistic regression
 ↓
label
```

Here the embedding model creates features, while a small classifier is trained on your labeled data.

### Route 3 — Zero-shot embeddings

```text
document embedding
        ↘
      similarity → closest label
        ↗
label-description embedding
```

No labeled training examples are required.

### Route 4 — Generative model

```text
instruction + document
        ↓
generative model
        ↓
"positive"
        ↓
map to label 1
```

The chapter explores both an encoder-decoder model and a closed generative model.

[[IMAGE_NEEDED: Four classification routes | Four side-by-side pipelines showing task-specific model, frozen embeddings plus classifier, zero-shot label similarity, and generative prompting | Learner should see that the same classification goal can be solved with very different model architectures and training requirements]]

### Why learn more than one route?

Because real projects differ in:

- amount of labeled data,
- available compute,
- latency needs,
- cost constraints,
- privacy requirements,
- model availability,
- required accuracy,
- and how easily the classes can be described in natural language.

There is rarely one universal best architecture.

---

## 3. The movie-review dataset

The chapter uses the `rotten_tomatoes` dataset from the Hugging Face ecosystem.

Load it with:

```python
from datasets import load_dataset

data = load_dataset("rotten_tomatoes")
```

The chapter reports three splits:

```text
train       8,530 examples
validation  1,066 examples
test        1,066 examples
```

Each item contains:

```text
text
label
```

The labels are:

```text
0 → negative review
1 → positive review
```

The full dataset contains balanced positive and negative examples, and the test set shown in the chapter contains:

```text
533 negative
533 positive
```

### Why split data?

A model should not be judged only on examples used to train it.

A typical workflow separates data into:

```text
training set
    used to fit trainable components

validation set
    useful for model or hyperparameter decisions

test set
    used for final evaluation on unseen examples
```

This helps us estimate whether the learned pattern generalizes.

### Important baseline reminder

The chapter explicitly advises comparing language-model approaches against strong classical baselines such as:

```text
TF-IDF
+
logistic regression
```

This is good engineering practice.

A larger or newer model is not automatically the right choice.

---

## 4. Representation models for classification

Representation models focus on turning text into useful numerical representations.

Encoder-style architectures such as BERT are common examples.

The chapter presents two ways to use representation models:

```text
A. task-specific representation model

B. general-purpose embedding model
```

### Task-specific model

A foundation model such as BERT can be fine-tuned for a particular classification task.

After fine-tuning, you can give it text and directly receive class scores.

### Embedding model

A general-purpose embedding model instead produces a vector representation.

That vector can then be passed into another classifier.

The difference is important:

```text
TASK-SPECIFIC MODEL
text → label scores directly
```

versus:

```text
EMBEDDING MODEL
text → vector → another classifier → label
```

[[IMAGE_NEEDED: Task-specific versus embedding classification | Show a pretrained task-specific encoder going directly from text to sentiment label beside a frozen embedding encoder producing a vector that then feeds logistic regression | Learner should notice that the first model performs the task directly while the second separates feature extraction from classification]]

---

## 5. Choosing a representation model

The chapter stresses that model selection is not trivial.

Important factors include:

- language support,
- underlying architecture,
- model size,
- task compatibility,
- inference speed,
- measured performance.

The chapter names several BERT-family starting points:

```text
BERT base
RoBERTa base
DistilBERT base
DeBERTa base
bert-tiny
ALBERT base v2
```

These are not presented as a permanent ranking.

They are examples of useful baseline model families.

### Why encoder models remain valuable

Generative LLMs receive much attention, but encoder-only models can be highly effective for focused tasks.

They are often:

- smaller,
- cheaper to run,
- easier to deploy,
- and naturally suited to representation/classification workloads.

This is an important engineering lesson:

> Do not automatically use a generative LLM just because the input is text.

### Domain fit matters

The chapter deliberately uses a sentiment model fine-tuned on tweets:

```text
cardiffnlp/twitter-roberta-base-sentiment-latest
```

for movie reviews.

That lets us examine **generalization across domains**.

Tweets and movie reviews both contain sentiment, but their language style differs.

A model trained directly on movie-review sentiment may perform better.

So model selection should ask:

```text
Was this model trained for my task?
Was it trained on language similar to my domain?
```

---

## 6. Using a pretrained task-specific classifier

Load the chapter's sentiment model:

```python
from transformers import pipeline

model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"

pipe = pipeline(
    model=model_path,
    tokenizer=model_path,
    return_all_scores=True,
    device="cuda:0",
)
```

The tokenizer converts text into token IDs before the model processes it.

The classification pipeline then returns class scores.

### Running inference over the test split

The chapter uses:

```python
import numpy as np

from tqdm import tqdm
from transformers.pipelines.pt_utils import KeyDataset

y_pred = []

for output in tqdm(
    pipe(KeyDataset(data["test"], "text")),
    total=len(data["test"]),
):
    negative_score = output[0]["score"]
    positive_score = output[2]["score"]

    assignment = np.argmax(
        [negative_score, positive_score]
    )

    y_pred.append(assignment)
```

The important flow is:

```text
review
 ↓
tokenizer
 ↓
pretrained sentiment model
 ↓
class scores
 ↓
select larger relevant score
 ↓
0 or 1
```

[[IMAGE_NEEDED: Task-specific sentiment inference | Show a movie-review sentence flowing through tokenizer → pretrained sentiment encoder → negative/neutral/positive score outputs, with negative and positive mapped into the chapter's binary labels | Learner should notice that the model has already learned the classification task and no new training is being performed here]]

### Frozen does not mean useless

In this chapter, pretrained language models are kept frozen.

That means:

```text
their weights are not updated
```

during these examples.

We are leveraging knowledge already learned during pretraining and fine-tuning.

---

## 7. Evaluating a classifier

Prediction is only half the job.

We also need to know how well the classifier performs.

The chapter uses:

```python
from sklearn.metrics import classification_report

def evaluate_performance(y_true, y_pred):
    performance = classification_report(
        y_true,
        y_pred,
        target_names=[
            "Negative Review",
            "Positive Review",
        ],
    )
    print(performance)
```

This reports:

- precision,
- recall,
- F1,
- support,
- accuracy,
- aggregate averages.

Before understanding these metrics, start with the confusion matrix.

---

## 8. The confusion matrix

For binary classification, every prediction falls into one of four categories.

Assume **positive review** is the positive class.

### True Positive — TP

The review is positive.

The model predicts positive.

```text
actual: positive
predicted: positive
```

Correct.

### True Negative — TN

The review is negative.

The model predicts negative.

```text
actual: negative
predicted: negative
```

Correct.

### False Positive — FP

The review is actually negative.

The model predicts positive.

```text
actual: negative
predicted: positive
```

Incorrect.

### False Negative — FN

The review is actually positive.

The model predicts negative.

```text
actual: positive
predicted: negative
```

Incorrect.

A compact matrix:

```text
                     Predicted
                  Negative   Positive

Actual Negative      TN         FP

Actual Positive      FN         TP
```

[[IMAGE_NEEDED: Binary confusion matrix | A 2×2 matrix labeled TN, FP, FN, TP using negative and positive movie reviews on the axes, with correct cells visually distinguished from error cells | Learner should be able to identify all four outcomes before learning precision and recall]]

---

## 9. Precision, recall, accuracy, and F1

These metrics answer different questions.

### Accuracy

Accuracy asks:

> Out of all predictions, how many were correct?

Conceptually:

```text
accuracy =
correct predictions
-------------------
all predictions
```

or:

```text
(TP + TN) / (TP + TN + FP + FN)
```

Accuracy is easy to understand, but it can be misleading when classes are strongly imbalanced.

### Precision

Precision asks:

> When the model predicts this class, how often is it right?

For the positive class:

```text
precision =
TP
-------
TP + FP
```

High precision means few false positive predictions.

### Recall

Recall asks:

> Of the examples that truly belong to this class, how many did the model find?

```text
recall =
TP
-------
TP + FN
```

High recall means few true positive examples were missed.

### F1 score

F1 balances precision and recall.

Conceptually:

```text
F1 = harmonic balance of precision and recall
```

The exact formula is:

```text
2 × precision × recall
----------------------
 precision + recall
```

### Easy intuition

Imagine detecting urgent support tickets.

If your model marks many normal tickets as urgent:

```text
precision suffers
```

If your model misses many truly urgent tickets:

```text
recall suffers
```

F1 becomes useful when both error types matter.

[[IMAGE_NEEDED: Precision vs recall intuition | Show a collection of actual positive items and predicted-positive items as overlapping sets, with TP in the overlap, FP in predicted-only, and FN in actual-only; annotate precision as purity of predictions and recall as coverage of true positives | Learner should understand the different questions precision and recall answer]]

### Chapter result for the task-specific model

The chapter reports a weighted F1 around:

```text
0.80
```

for the selected Twitter sentiment model on the movie-review test set.

That is useful precisely because the model was not fine-tuned specifically on this movie-review dataset.

---

## 10. Classification using frozen embeddings

Now we take a different approach.

Instead of asking one pretrained model to directly output sentiment, use a general-purpose embedding model to turn each review into a numerical feature vector.

The pipeline becomes:

```text
review text
    ↓
frozen embedding model
    ↓
embedding vector
    ↓
trainable lightweight classifier
    ↓
label
```

This cleanly separates:

```text
feature extraction
```

from:

```text
classification
```

### Why this is useful

Fine-tuning a large language model can require substantial compute.

But training logistic regression over already-computed embeddings is comparatively lightweight and can often run comfortably on CPU.

So we can reuse a strong pretrained model without updating its weights.

[[IMAGE_NEEDED: Frozen embeddings plus logistic regression | Show movie reviews entering a frozen embedding model, producing fixed-size vectors, then those vectors and labels feeding a small trainable logistic-regression classifier | Learner should notice that only the small classifier is trained while the embedding model remains unchanged]]

---

## 11. Create text embeddings

The chapter uses:

```text
sentence-transformers/all-mpnet-base-v2
```

Load it:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-mpnet-base-v2"
)
```

Generate training embeddings:

```python
train_embeddings = model.encode(
    data["train"]["text"],
    show_progress_bar=True,
)
```

Generate test embeddings:

```python
test_embeddings = model.encode(
    data["test"]["text"],
    show_progress_bar=True,
)
```

The chapter reports:

```text
train_embeddings.shape
→ (8530, 768)
```

Interpretation:

```text
8,530 training reviews
×
768 numerical features per review
```

Each review becomes one point in a 768-dimensional embedding space.

The classifier no longer sees raw text.

It sees vectors.

---

## 12. Train a lightweight classifier on the embeddings

The chapter uses logistic regression:

```python
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(
    random_state=42
)

clf.fit(
    train_embeddings,
    data["train"]["label"],
)
```

Notice what is being trained:

```text
logistic regression
```

not:

```text
the embedding model
```

The embedding model remains frozen.

### Prediction

```python
y_pred = clf.predict(
    test_embeddings
)
```

Then evaluate:

```python
evaluate_performance(
    data["test"]["label"],
    y_pred,
)
```

The chapter reports weighted F1 around:

```text
0.85
```

That exceeds the approximately `0.80` from the earlier task-specific sentiment model in this specific experiment.

Do not turn that into a universal rule.

The lesson is:

> Strong general-purpose embeddings can provide excellent reusable features for small supervised classifiers.

### Why this architecture is attractive

You get a modular system:

```text
Embedding model
     ↓
fixed feature representation

Classifier
     ↓
cheap task-specific training
```

If you later change the classifier, you may reuse embeddings.

If you add a new task with labeled data, you may reuse the embedding model.

This makes embeddings powerful infrastructure.

---

{{exercise:M04.L01.EX01}}

---

## 13. What if you have no labeled examples?

Labels can be expensive.

Humans may need to read thousands of examples and assign:

```text
positive
negative
billing
technical
urgent
not urgent
...
```

The chapter asks whether we can first test a classification idea **without collecting labeled training examples**.

This leads to zero-shot classification.

### Zero-shot classification

You know the candidate classes, but you do not have labeled examples for training.

For movie sentiment, you know the labels:

```text
negative
positive
```

but imagine you have no annotated movie-review dataset.

The chapter uses a creative embedding approach.

---

## 14. Turn labels into natural-language descriptions

A bare class name such as:

```text
positive
```

is meaningful, but a richer description gives the embedding model more semantic context.

The chapter uses descriptions such as:

```text
"A negative review"
"A positive review"
```

Embed them:

```python
label_embeddings = model.encode(
    [
        "A negative review",
        "A positive review",
    ]
)
```

Now both sides live in vector space:

```text
document → embedding

label description → embedding
```

We can compare them.

[[IMAGE_NEEDED: Zero-shot label embeddings | Show a review sentence and two label descriptions (“A negative review”, “A positive review”) each passing through the same embedding model into vectors | Learner should notice that natural-language labels become comparable vectors without supervised fitting]]

---

## 15. Cosine similarity for zero-shot classification

We need a way to compare vectors.

The chapter uses **cosine similarity**.

Intuitively, cosine similarity compares the direction of two vectors.

If two embeddings point in similar directions in semantic space, their cosine similarity is higher.

Conceptually:

```text
review embedding
        ↘
      cosine similarity
        ↗
label embedding
```

For one review:

```text
similarity(review, negative_label) = 0.41
similarity(review, positive_label) = 0.77
```

we predict:

```text
positive
```

because it has the higher similarity.

### Code

```python
from sklearn.metrics.pairwise import cosine_similarity

sim_matrix = cosine_similarity(
    test_embeddings,
    label_embeddings,
)

y_pred = np.argmax(
    sim_matrix,
    axis=1,
)
```

The matrix contains:

```text
one row per document
one column per candidate label
```

and `argmax` selects the most similar label.

[[IMAGE_NEEDED: Cosine zero-shot classification | Show one document embedding as an arrow and two candidate-label vectors; one label vector has a smaller angle/higher similarity and is selected | Learner should understand that classification is performed by semantic proximity rather than a separately trained classifier]]

### Chapter result

The chapter reports weighted F1 around:

```text
0.78
```

despite using no labeled training examples in this approach.

That is the important result—not because `0.78` is universally expected, but because useful classification can emerge purely from semantic embedding relationships.

---

## 16. Label wording is part of the model input

A subtle but valuable lesson appears in the chapter's tip.

Instead of:

```text
"A negative review"
"A positive review"
```

try more specific descriptions:

```text
"A very negative movie review"
"A very positive movie review"
```

Why could this matter?

Because the embedding model represents the meaning of the description.

The phrase:

```text
movie review
```

adds domain context.

The modifier:

```text
very
```

changes the semantic region.

This means zero-shot embedding classification is partly an exercise in **label-description design**.

That is analogous to prompt engineering:

```text
better task description
→ potentially better model behavior
```

### Practical lesson

Do not assume label names are neutral.

Compare candidate descriptions.

For example, instead of:

```text
"billing"
```

you might test:

```text
"A customer request about invoices, charges, or payments"
```

The more descriptive version may represent the intended class more clearly.

---

## 17. Classification with generative models

A task-specific classifier naturally produces class scores.

A generative model naturally produces text.

So classification with a generative model requires a different pattern:

```text
document
+
instruction
    ↓
generative model
    ↓
generated text label
```

For example:

```text
Instruction:
Is the following sentence positive or negative?

Document:
"Surprisingly moving and beautifully acted."

Output:
positive
```

The classification task has been reframed as text generation.

### Prompt engineering becomes important

If you give a generic generative model only:

```text
"Surprisingly moving and beautifully acted."
```

the model does not inherently know that you want sentiment classification.

You need to specify the task.

That is why the prompt becomes part of the classifier's behavior.

[[IMAGE_NEEDED: Generative classification versus task-specific classification | Show task-specific model: text → numeric class scores, beside generative model: instruction + text → generated class word | Learner should notice that generative classification requires explicitly expressing the task in the prompt]]

---

## 18. T5 and the text-to-text idea

The chapter introduces the **Text-to-Text Transfer Transformer (T5)** family.

Unlike encoder-only BERT or decoder-only GPT-style models, T5 uses an encoder-decoder Transformer architecture.

Its key framing is powerful:

> Express many NLP tasks as text input → text output.

For example:

```text
classification:
"sentiment: This movie was excellent"
→ "positive"
```

or another task might also be expressed in text.

This gives one architecture a unified interface across multiple tasks.

### Pretraining and fine-tuning idea

The chapter explains that T5 pretraining masks spans of tokens and asks the model to reconstruct them.

Then downstream tasks are converted into text-to-text formats.

Later instruction-tuned families such as Flan-T5 extend this idea with a wide variety of tasks expressed as instructions.

[[IMAGE_NEEDED: T5 text-to-text unification | Show several tasks such as sentiment classification, summarization, and question answering all converted into textual prompts entering the same encoder-decoder model and producing textual outputs | Learner should see how text-to-text framing unifies tasks]]

---

## 19. Use Flan-T5 for sentiment classification

Load the model:

```python
from transformers import pipeline

pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    device="cuda:0",
)
```

Now create a task instruction:

```python
prompt = (
    "Is the following sentence positive or negative? "
)
```

Add that instruction to every review:

```python
data = data.map(
    lambda example: {
        "t5": prompt + example["text"]
    }
)
```

The model now sees input like:

```text
Is the following sentence positive or negative?
<movie review>
```

### Generate predictions

```python
y_pred = []

for output in tqdm(
    pipe(KeyDataset(data["test"], "t5")),
    total=len(data["test"]),
):
    text = output[0]["generated_text"]

    y_pred.append(
        0 if text == "negative" else 1
    )
```

This reveals an important practical issue:

> Generative output must be constrained or normalized before standard classification evaluation.

The model outputs:

```text
"negative"
```

while your evaluation labels are:

```text
0
```

So you must map between representations.

### Chapter result

The chapter reports weighted F1 around:

```text
0.84
```

for this Flan-T5-small example.

The noteworthy part is that we did not train a new sentiment head on the Rotten Tomatoes training split for this example.

We relied on the model's instruction-following abilities.

---

## 20. Closed generative models as classifiers

The chapter also discusses using a closed model through an API.

The workflow is different from loading an open model locally.

Conceptually:

```text
your application
     ↓ API request
provider-hosted model
     ↓ API response
generated label
```

Advantages can include:

- no need to host the model,
- no requirement for local GPU memory,
- easy access to capable models.

Tradeoffs can include:

- API cost,
- rate limits,
- less control over the underlying model,
- data leaving your local environment,
- limited transparency about training data.

The chapter uses an OpenAI API example from the time it was written.

Because APIs, model names, SDK syntax, and prices can change, treat that specific code as a **historical example from the source chapter**, not as a timeless current API reference.

### Prompt structure

The chapter's classification prompt follows a strict pattern:

```text
Predict whether this document is positive or negative.

[DOCUMENT]

Return 1 for positive and 0 for negative.
Do not return anything else.
```

This is good classification prompting because the output contract is explicit.

### Why strict output instructions matter

Suppose your evaluation code expects:

```text
0
```

or:

```text
1
```

but the model returns:

```text
"This is clearly a positive review because..."
```

Your parser may fail.

So a production classifier should define:

```text
allowed labels
output format
fallback handling
validation
```

Do not assume a generative model will always obey formatting perfectly.

---

## 21. Cost, rate limits, and benchmark uncertainty

The chapter adds several engineering cautions.

### API cost

A model invocation may have a small per-request cost.

Across thousands or millions of documents, that matters.

Always think in terms of:

```text
cost per item
×
number of items
×
number of retries / repeated experiments
```

### Rate limits

External APIs may limit requests over time.

The chapter mentions **exponential backoff** as one strategy.

Conceptually:

```text
request fails due to rate limit
        ↓
wait briefly
        ↓
retry
        ↓
if it fails again, wait longer
        ↓
retry until success or maximum retries
```

### Benchmark contamination

The chapter reports a strong result for a closed generative model, but warns that the model's training data is not fully known.

If the benchmark dataset appeared in training, measured performance may not cleanly reflect unseen generalization.

This is a very important evaluation principle:

> A high benchmark score is easiest to interpret when you know the test data was genuinely unseen during model training.

[[IMAGE_NEEDED: Closed-model evaluation caveats | Show an API-based classifier with three warning branches: usage cost, rate limits/retries, and unknown training-data overlap with benchmark datasets | Learner should notice that model quality is only one part of production evaluation]]

---

## 22. Comparing the chapter's classification approaches

The chapter provides a useful spectrum.

| Approach | Requires labeled training data from you? | What is trained by you? | Main output | Chapter example |
|---|---:|---|---|---|
| Task-specific pretrained model | No | Nothing | Class scores | Twitter-RoBERTa sentiment |
| Embeddings + classifier | Yes | Small classifier | Class label | MPNet embeddings + logistic regression |
| Zero-shot embeddings | No | Nothing | Most similar label | Label descriptions + cosine similarity |
| Generative model | No additional domain labels required in example | Nothing | Generated text label | Flan-T5 / API model |

### Chapter-reported weighted F1 results

For the specific experiments in the source:

```text
Task-specific sentiment model:
~0.80

Frozen embeddings + logistic regression:
~0.85

Zero-shot embedding similarity:
~0.78

Flan-T5:
~0.84

Closed generative API model:
~0.91
```

These numbers are **results from the chapter's particular setup**, not a ranking that applies to every classification problem.

Different:

- datasets,
- prompts,
- class definitions,
- embedding models,
- domain match,
- model versions,
- and evaluation methods

can change the result.

### The more useful decision framework

Ask:

```text
Do I have labeled data?
Do I need low latency?
Can I host a model?
Do I need privacy?
How expensive is inference?
How stable must the output format be?
Can I tolerate API dependence?
Does a task-specific model already exist?
Can an embedding model separate the classes well?
Can the labels be clearly described?
```

That is much more useful than asking for a universally best model.

---

{{exercise:M04.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Text classification always requires fine-tuning a large model.

### Why this is wrong

The chapter demonstrates classification using already-fine-tuned models, frozen embeddings plus a small classifier, zero-shot embedding similarity, and prompted generative models.

---

### Misconception 2

> If I use embeddings, the embedding model itself must be retrained.

### Why this is wrong

In the supervised embedding example, the embedding model stays frozen. Only logistic regression is trained.

---

### Misconception 3

> Accuracy tells me everything I need to know.

### Why this is wrong

Precision and recall reveal different failure patterns, while F1 summarizes their balance. Accuracy can hide problems, especially with class imbalance.

---

### Misconception 4

> Zero-shot classification means the model has never seen language related to the labels.

### Why this is wrong

Zero-shot here means you do not provide labeled examples for this target task. The pretrained embedding model has already learned broad language representations from prior training.

---

### Misconception 5

> Label names do not matter when using zero-shot embeddings.

### Why this is wrong

The label text is itself embedded. Different descriptions can produce different vector representations and therefore different similarities.

---

### Misconception 6

> A generative model automatically knows which classification task you want.

### Why this is wrong

You need to communicate the task through the prompt or instruction.

---

### Misconception 7

> A higher score from one chapter experiment proves that approach is always superior.

### Why this is wrong

Those results belong to a particular dataset, model, prompt, domain, and evaluation setup.

---

## Key terminology

| Term | Meaning |
|---|---|
| Text classification | Assigning a predefined label/class to input text |
| Binary classification | Classification with two possible classes |
| Sentiment analysis | Classification of emotional/opinion polarity such as positive versus negative |
| Representation model | Model primarily used to create useful representations of text |
| Task-specific model | Pretrained model fine-tuned to perform a particular downstream task |
| Embedding model | Model that maps text into dense numerical vectors |
| Frozen model | Model whose weights are not updated during the current training process |
| Feature extraction | Turning raw input into numerical features used by another model |
| Logistic regression | Lightweight classical model commonly used for classification |
| Confusion matrix | Table summarizing true positives, true negatives, false positives, and false negatives |
| Precision | Among predicted positives, the fraction that are truly positive |
| Recall | Among actual positives, the fraction correctly found |
| Accuracy | Fraction of all predictions that are correct |
| F1 score | Harmonic balance of precision and recall |
| Zero-shot classification | Assigning labels without task-specific labeled training examples |
| Label embedding | Vector representation of a natural-language class description |
| Cosine similarity | Similarity measure based on the angle between vectors |
| Generative classification | Reframing classification as generation of a textual label |
| Prompt engineering | Iteratively designing instructions/input wording to improve model outputs |
| Encoder-decoder model | Architecture with an encoder that processes input and a decoder that generates output |
| T5 | Text-to-Text Transfer Transformer family |
| Flan-T5 | Instruction-tuned T5 family trained across many prompted tasks |
| Rate limit | Restriction on how frequently an external API may be called |
| Exponential backoff | Retry strategy that progressively increases waiting time after repeated failures |
| Benchmark contamination | Possibility that evaluation data was present in a model's training data |

---

## Self-check

Before continuing, make sure you can answer:

1. What is text classification?
2. Why is sentiment classification in this chapter a binary task?
3. What is the difference between a task-specific model and an embedding model?
4. Why can domain mismatch hurt a pretrained classifier?
5. What are TP, TN, FP, and FN?
6. What question does precision answer?
7. What question does recall answer?
8. Why can F1 be more informative than accuracy alone?
9. In the embedding-classifier approach, which model is frozen and which model is trained?
10. What does `(8530, 768)` mean for the training embeddings?
11. How does zero-shot embedding classification work?
12. Why can richer label descriptions change zero-shot results?
13. Why does a generative classifier need a prompt?
14. Why do generated labels often need to be normalized or mapped before evaluation?
15. What is the conceptual difference between T5 classification and a BERT-style task-specific classifier?
16. Why should API cost and rate limits matter when classifying large datasets?
17. Why can unknown training-data overlap make a closed-model benchmark difficult to interpret?
18. Under what circumstances might embeddings + logistic regression be attractive?
19. Why should you still compare against classical baselines such as TF-IDF + logistic regression?
20. Describe all four classification routes covered in this lesson.

---

## Retain this idea

**Text classification is not one model architecture—it is a goal that can be reached in several ways. A task-specific encoder can directly output class scores; a frozen embedding model can provide reusable features for a lightweight supervised classifier; label descriptions can enable zero-shot classification through vector similarity; and a generative model can turn the problem into instruction-following text generation. The best engineering choice depends on your labels, data, domain, compute, cost, latency, privacy, and evaluation needs.**
"""
        ),

        "estimated_minutes": 150,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "what-is-classification", "title": "What is text classification?", "order": 1},
            {"id": "four-routes", "title": "Four practical routes to classification", "order": 2},
            {"id": "dataset", "title": "The movie-review dataset", "order": 3},
            {"id": "representation-models", "title": "Representation models for classification", "order": 4},
            {"id": "model-selection", "title": "Choosing a representation model", "order": 5},
            {"id": "task-specific", "title": "Using a pretrained task-specific classifier", "order": 6},
            {"id": "evaluation", "title": "Evaluating a classifier", "order": 7},
            {"id": "confusion-matrix", "title": "The confusion matrix", "order": 8},
            {"id": "metrics", "title": "Precision, recall, accuracy, and F1", "order": 9},
            {"id": "embedding-supervised", "title": "Classification using frozen embeddings", "order": 10},
            {"id": "embedding-code", "title": "Create text embeddings", "order": 11},
            {"id": "logistic-regression", "title": "Train a lightweight classifier on the embeddings", "order": 12},
            {"id": "zero-shot", "title": "What if you have no labeled examples?", "order": 13},
            {"id": "label-embeddings", "title": "Turn labels into natural-language descriptions", "order": 14},
            {"id": "cosine", "title": "Cosine similarity for zero-shot classification", "order": 15},
            {"id": "label-wording", "title": "Label wording is part of the model input", "order": 16},
            {"id": "generative-models", "title": "Classification with generative models", "order": 17},
            {"id": "t5", "title": "T5 and the text-to-text idea", "order": 18},
            {"id": "flan-t5", "title": "Use Flan-T5 for sentiment classification", "order": 19},
            {"id": "closed-model", "title": "Closed generative models as classifiers", "order": 20},
            {"id": "api-caveats", "title": "Cost, rate limits, and benchmark uncertainty", "order": 21},
            {"id": "comparison", "title": "Comparing the chapter's classification approaches", "order": 22},
            {"id": "misconceptions", "title": "Important misconceptions", "order": 23},
            {"id": "terminology", "title": "Key terminology", "order": 24},
            {"id": "self-check", "title": "Self-check", "order": 25},
            {"id": "retain", "title": "Retain this idea", "order": 26},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M04.L01.EX01",

            "title": "Build and Evaluate an Embedding Classifier",

            "lesson_code": "M04.L01",

            "section_id": "logistic-regression",

            "placement": "after_section",

            "description": (
                "Practice the chapter's supervised embedding workflow and interpret "
                "classification metrics instead of only reporting one score."
            ),

            "instructions": (
                "Using the Rotten Tomatoes dataset or an equivalent binary text dataset:\n"
                "1. Load the train and test splits.\n"
                "2. Generate embeddings for both splits using a frozen sentence-transformer.\n"
                "3. Print the embedding shapes and explain both dimensions.\n"
                "4. Train logistic regression using the training embeddings and labels.\n"
                "5. Predict the test labels.\n"
                "6. Produce a classification report.\n"
                "7. Build or inspect a confusion matrix.\n"
                "8. Explain precision and recall separately for one class.\n"
                "9. Identify whether false positives or false negatives are more common.\n"
                "10. Write a short explanation of why this is not full language-model fine-tuning."
            ),

            "expected_output": (
                "A notebook or script containing embedding shapes, fitted logistic "
                "regression, test predictions, classification metrics, a confusion "
                "matrix, and a written interpretation of at least two error types."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "embedding-feature-extraction",
                "logistic-regression",
                "classification-evaluation",
                "confusion-matrix",
                "precision-recall",
            ],
        },

        {
            "id": "M04.L01.EX02",

            "title": "Compare Three No-Fine-Tuning Classification Strategies",

            "lesson_code": "M04.L01",

            "section_id": "comparison",

            "placement": "after_section",

            "description": (
                "Compare task-specific inference, zero-shot embedding similarity, "
                "and prompted generative classification under the same conceptual task."
            ),

            "instructions": (
                "Choose 10–20 short text examples from a classification task with "
                "known labels. Compare three approaches:\n"
                "1. A pretrained task-specific classifier, if one appropriate to the "
                "task is available.\n"
                "2. A frozen embedding model with natural-language label descriptions "
                "and cosine similarity.\n"
                "3. A generative model prompted to return exactly one allowed label.\n"
                "For each approach, record the predicted labels. Then:\n"
                "4. Note where the systems disagree.\n"
                "5. For the zero-shot approach, test at least two different label "
                "descriptions and record whether predictions change.\n"
                "6. For the generative approach, define an explicit output contract.\n"
                "7. Compare the approaches on compute/hosting requirements, latency, "
                "need for labeled data, output stability, and domain fit.\n"
                "8. Do not choose a universal winner; explain which constraints would "
                "make each approach attractive."
            ),

            "expected_output": (
                "A comparison table with predictions from three approaches, notes on "
                "disagreements, two versions of zero-shot label descriptions, and a "
                "short engineering analysis of the tradeoffs."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "classification-strategy-comparison",
                "zero-shot-classification",
                "label-description-design",
                "prompt-design",
                "model-selection",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M04.L01.QZ01",

        "title": "Text Classification — Knowledge Check",

        "lesson_code": "M04.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M04.L01.Q01",
                "section_id": "what-is-classification",
                "question": "What is the primary goal of text classification?",
                "options": [
                    "Generate the longest possible response.",
                    "Assign a predefined label or class to input text.",
                    "Convert every word into a different language.",
                    "Train a tokenizer from scratch.",
                ],
                "correct": 1,
                "explanation": (
                    "Classification maps input text into one or more predefined "
                    "categories rather than generating unrestricted text."
                ),
            },
            {
                "id": "M04.L01.Q02",
                "section_id": "representation-models",
                "question": (
                    "What is the key difference between a task-specific representation "
                    "model and a general-purpose embedding model in this chapter?"
                ),
                "options": [
                    "The task-specific model directly produces task-oriented class scores, while the embedding model produces reusable vectors.",
                    "The embedding model cannot process text.",
                    "The task-specific model must always be larger.",
                    "Only the embedding model uses a tokenizer.",
                ],
                "correct": 0,
                "explanation": (
                    "Task-specific models are already adapted to a downstream task, "
                    "while embedding models produce vectors that can be reused for "
                    "many tasks."
                ),
            },
            {
                "id": "M04.L01.Q03",
                "section_id": "model-selection",
                "question": "Why can domain fit matter when selecting a pretrained classifier?",
                "options": [
                    "Because a model trained on similar language and examples may generalize better to the target task.",
                    "Because all domains use completely different token IDs.",
                    "Because models can only classify the exact sentences they saw during training.",
                    "Because domain fit determines the GPU brand required.",
                ],
                "correct": 0,
                "explanation": (
                    "Task and language similarity between training data and deployment "
                    "data can strongly affect generalization."
                ),
            },
            {
                "id": "M04.L01.Q04",
                "section_id": "confusion-matrix",
                "question": (
                    "If a review is actually positive but the model predicts negative, "
                    "what is that outcome for the positive class?"
                ),
                "options": [
                    "True positive",
                    "True negative",
                    "False positive",
                    "False negative",
                ],
                "correct": 3,
                "explanation": (
                    "The example truly belongs to the positive class but the model "
                    "failed to identify it, making it a false negative."
                ),
            },
            {
                "id": "M04.L01.Q05",
                "section_id": "metrics",
                "question": "What question does precision answer?",
                "options": [
                    "Among all true positive examples, how many did we find?",
                    "Among the examples predicted as this class, how many were actually correct?",
                    "How many GPU operations were needed?",
                    "How many labels exist?",
                ],
                "correct": 1,
                "explanation": (
                    "Precision measures the correctness or purity of positive predictions."
                ),
            },
            {
                "id": "M04.L01.Q06",
                "section_id": "metrics",
                "question": "What question does recall answer?",
                "options": [
                    "Among the truly relevant examples, how many did the model successfully find?",
                    "How many total tokens were generated?",
                    "How close are two embedding vectors?",
                    "How much memory does the model need?",
                ],
                "correct": 0,
                "explanation": (
                    "Recall measures coverage of the true members of a class."
                ),
            },
            {
                "id": "M04.L01.Q07",
                "section_id": "embedding-supervised",
                "question": (
                    "What is trained in the chapter's supervised embedding approach?"
                ),
                "options": [
                    "The full sentence-transformer model and tokenizer",
                    "Only a lightweight classifier such as logistic regression, while the embedding model stays frozen",
                    "Nothing at all",
                    "Only the tokenizer vocabulary",
                ],
                "correct": 1,
                "explanation": (
                    "The embedding model is used as a fixed feature extractor and "
                    "the small downstream classifier is fitted on labeled embeddings."
                ),
            },
            {
                "id": "M04.L01.Q08",
                "section_id": "embedding-code",
                "question": "What does an embedding matrix shape of (8530, 768) mean?",
                "options": [
                    "8,530 models each with 768 tokenizers",
                    "8,530 input examples, each represented by a 768-dimensional vector",
                    "768 labels for each of 8,530 tokens",
                    "8,530 epochs and 768 GPUs",
                ],
                "correct": 1,
                "explanation": (
                    "Each of the 8,530 documents has one 768-value embedding vector."
                ),
            },
            {
                "id": "M04.L01.Q09",
                "section_id": "cosine",
                "question": (
                    "How does the chapter's zero-shot embedding classifier choose a label?"
                ),
                "options": [
                    "It randomly chooses among candidate labels.",
                    "It trains a full language model on the test set.",
                    "It chooses the label description whose embedding has the highest cosine similarity to the document embedding.",
                    "It uses only the number of words in the document.",
                ],
                "correct": 2,
                "explanation": (
                    "Document and label descriptions are embedded into the same vector "
                    "space and classification is based on semantic similarity."
                ),
            },
            {
                "id": "M04.L01.Q10",
                "section_id": "label-wording",
                "question": "Why might changing a zero-shot label description change predictions?",
                "options": [
                    "Because the label description itself is embedded and its wording changes the vector representation.",
                    "Because cosine similarity only works with one-word labels.",
                    "Because the tokenizer stops functioning after the first label.",
                    "Because label text changes the test labels in the dataset.",
                ],
                "correct": 0,
                "explanation": (
                    "Natural-language class descriptions are part of the semantic "
                    "input to the embedding model, so wording can matter."
                ),
            },
            {
                "id": "M04.L01.Q11",
                "section_id": "generative-models",
                "question": (
                    "Why does a generic generative model need an instruction for classification?"
                ),
                "options": [
                    "Because raw input text alone does not specify which task or output format you want.",
                    "Because generative models cannot read movie reviews.",
                    "Because instructions replace the tokenizer.",
                    "Because classification labels must be hidden.",
                ],
                "correct": 0,
                "explanation": (
                    "The prompt communicates both the requested task and, ideally, "
                    "the desired output format."
                ),
            },
            {
                "id": "M04.L01.Q12",
                "section_id": "flan-t5",
                "question": (
                    "Why does the Flan-T5 example map generated words such as "
                    "`negative` and `positive` back to numerical labels?"
                ),
                "options": [
                    "Because standard classification evaluation compares predictions to numerical target labels in this dataset.",
                    "Because T5 cannot generate text.",
                    "Because embeddings only accept integers.",
                    "Because labels must always be 0 and 1 in every classification problem.",
                ],
                "correct": 0,
                "explanation": (
                    "The dataset uses numerical sentiment targets, while the generative "
                    "model outputs text, so the representations must be aligned for evaluation."
                ),
            },
            {
                "id": "M04.L01.Q13",
                "section_id": "api-caveats",
                "question": (
                    "Why can evaluation of an opaque closed model on a public benchmark "
                    "be difficult to interpret?"
                ),
                "options": [
                    "Because closed models never produce labels.",
                    "Because the benchmark may have appeared in unknown training data, making unseen-data generalization uncertain.",
                    "Because precision and recall do not work for APIs.",
                    "Because API models cannot process test sets.",
                ],
                "correct": 1,
                "explanation": (
                    "Without knowing the training corpus, it can be difficult to rule "
                    "out overlap between benchmark examples and training data."
                ),
            },
            {
                "id": "M04.L01.Q14",
                "section_id": "comparison",
                "type": "open",
                "question": (
                    "You need to classify customer messages into five intents. Compare "
                    "a task-specific classifier, embeddings plus a lightweight supervised "
                    "classifier, zero-shot label similarity, and a prompted generative "
                    "model. Explain what data each requires, what is trained, and one "
                    "practical advantage or limitation of each."
                ),
            },
        ],

        "passing_score": 70,
    },
}
