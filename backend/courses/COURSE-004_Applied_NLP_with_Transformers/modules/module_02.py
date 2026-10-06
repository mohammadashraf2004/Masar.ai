'''M02.L01 — Text Classification with DistilBERT.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 2. Page range was not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
'''

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"
MODULE_ORDER = 2
MODULE_TITLE = "Text Classification"
MODULE_DESCRIPTION = (
    "Build an end-to-end mental model for transformer text classification: "
    "inspect an emotion dataset, tokenize text for DistilBERT, compare feature "
    "extraction with fine-tuning, evaluate errors, and run inference."
)
SOURCE_CHAPTER = 2
SOURCE_PAGES = "Chapter 2 (page range not provided)"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Text Classification with DistilBERT",
    "slug": "applied-nlp-transformers-m02-l01",
    "description": (
        "Learn text classification through an emotion-classification project "
        "using Hugging Face Datasets, tokenization, DistilBERT, feature "
        "extraction, fine-tuning, evaluation, and inference."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 3.0,
    "skill_tags": [
        "nlp",
        "text-classification",
        "transformers",
        "distilbert",
        "hugging-face-datasets",
        "tokenization",
        "fine-tuning",
        "error-analysis",
        "module-02",
    ],
    "prerequisite_ids": [],

    "lesson": {
        "title": "Text Classification with DistilBERT",
        "content": r'''# Text Classification with DistilBERT

> **Course:** Applied NLP with Transformers  
> **Lesson:** M02.L01  
> **Module:** Text Classification  
> **Source alignment:** BOOK-004, Chapter 2. The supplied chapter text did not include a page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what text classification is and where it is used.
- Load and inspect a Hugging Face `DatasetDict`.
- Check class balance and text length before training.
- Explain character, word, and subword tokenization.
- Use the tokenizer associated with a pretrained DistilBERT checkpoint.
- Explain `input_ids`, padding, truncation, and `attention_mask`.
- Describe the difference between feature extraction and fine-tuning.
- Extract DistilBERT hidden states for a traditional classifier.
- Fine-tune a transformer for sequence classification.
- Evaluate a classifier with accuracy, F1-score, and a confusion matrix.
- Use per-example loss to perform basic error analysis.
- Save a trained model and use it for inference on new text.

---

## 1. What text classification is

Text classification means assigning a piece of text to one of a set of predefined categories.

Examples include:

- deciding whether an email is spam,
- routing a support ticket by language,
- categorizing customer feedback,
- predicting sentiment,
- detecting an emotion expressed in a message.

In this chapter's project, the input is a tweet and the output is one emotion class.

A simplified view is:

```text
raw text
   ↓
tokenizer
   ↓
numerical model inputs
   ↓
DistilBERT
   ↓
classification layer
   ↓
predicted class
```

The chapter uses **DistilBERT**, a smaller and more efficient variant of BERT. The important idea is not merely the model name. The important idea is that we begin with a model that has already learned useful language representations and adapt it to our classification problem.

A **checkpoint** is the stored set of pretrained weights loaded into a transformer architecture.

The chapter also introduces three important parts of the Hugging Face ecosystem:

1. **Datasets** — load, inspect, transform, and batch data.
2. **Tokenizers** — convert raw text into the numerical representation expected by the model.
3. **Transformers** — load pretrained models and fine-tune or use them for inference.

[[IMAGE_NEEDED: Transformer text-classification pipeline | A simple flow from raw tweet to Dataset processing, tokenizer, DistilBERT, classification output, and prediction on new text | Learner should notice that text must pass through data preparation and tokenization before the transformer can classify it]]

### The project

The project is emotion classification from English tweets.

The chapter's loaded dataset metadata later shows these six classes:

```text
sadness
joy
love
anger
fear
surprise
```

> **Source consistency note:** Earlier prose in the supplied chapter mentions `disgust`, while the actual `ClassLabel` metadata shown later contains `love`. For the executable workflow, follow the labels reported by the loaded dataset object.

This is a useful real-world lesson: **inspect the dataset itself instead of assuming its labels from a description.**

---

## 2. Load and understand the dataset

The chapter loads the emotion dataset with Hugging Face Datasets:

```python
from datasets import load_dataset

emotions = load_dataset("emotion")
```

The returned object is a `DatasetDict`.

Think of it as a dictionary whose values are datasets:

```text
emotions
├── train
├── validation
└── test
```

The chapter shows:

```text
train:      16,000 rows
validation:  2,000 rows
test:        2,000 rows
```

Each row contains:

```text
text  -> the tweet
label -> the target emotion stored as an integer
```

You can access the training split like an ordinary dictionary:

```python
train_ds = emotions["train"]
```

You can inspect its size:

```python
len(train_ds)
```

You can inspect one row:

```python
train_ds[0]
```

A row behaves like a Python dictionary:

```python
{
    "text": "i didnt feel humiliated",
    "label": 0,
}
```

You can inspect the available columns:

```python
train_ds.column_names
```

And inspect the schema:

```python
train_ds.features
```

The `text` field is a string. The `label` field is represented by a `ClassLabel` object, which stores the integer-to-class mapping.

### Why integer labels are useful

Models work with numbers, so storing class labels as integers is convenient.

But humans usually want readable names such as `sadness` or `anger`.

A learner-friendly version is:

```python
label_feature = emotions["train"].features["label"]
print(label_feature.int2str(0))
```

The main idea is:

```text
model-friendly label: 0
human-friendly label: sadness
```

### What if the data is not on the Hub?

The chapter shows that `load_dataset()` can also load common local or remote formats.

```python
load_dataset("csv", data_files="my_file.csv")
load_dataset("text", data_files="my_file.txt")
load_dataset("json", data_files="my_file.jsonl")
```

For a semicolon-separated text file with no headers, the chapter uses:

```python
emotions_local = load_dataset(
    "csv",
    data_files="train.txt",
    sep=";",
    names=["text", "label"],
)
```

The important lesson is that the same dataset interface can be used whether the original data comes from the Hub, a local file, or a remote file.

### Dataset mental model

Do not think only:

> "I downloaded some text."

Think:

> "I now have structured splits, columns, feature types, and label metadata that I can inspect and transform reproducibly."

---

## 3. Inspect the data before modeling

A common beginner mistake is to load data and immediately train a model.

The chapter does something better: it first tries to understand the data.

### Convert temporarily to Pandas

```python
import pandas as pd

emotions.set_format(type="pandas")
df = emotions["train"][:]
```

To create readable label names:

```python
def label_int2str(row):
    return emotions["train"].features["label"].int2str(row)

df["label_name"] = df["label"].apply(label_int2str)
```

Now each row has both:

```text
label      -> integer
label_name -> readable emotion
```

### Check 1: class distribution

Before training a classifier, ask:

> Do all classes appear equally often?

The chapter visualizes class counts:

```python
df["label_name"].value_counts(ascending=True).plot.barh()
```

The result is imbalanced: some classes appear much more often than others.

Why does that matter?

Imagine this dataset:

```text
90% joy
10% fear
```

A useless classifier that always predicts `joy` would already reach 90% accuracy.

That is why accuracy must be interpreted in the context of class distribution.

Possible ways to address imbalance include:

- oversampling minority classes,
- undersampling majority classes,
- collecting more labeled examples for rare classes.

The chapter deliberately keeps the raw distribution for this project.

It also warns not to perform sampling before creating train/test splits, because that can cause **data leakage**.

[[IMAGE_NEEDED: Emotion class distribution | A horizontal bar chart showing that some emotion classes are much more frequent than others | Learner should notice why class imbalance changes how raw accuracy should be interpreted]]

### Check 2: text length

Transformers have a maximum input length.

For DistilBERT, the chapter reports a maximum context size of **512 tokens**.

Before worrying about truncation, inspect the lengths of the actual texts:

```python
df["Words Per Tweet"] = df["text"].str.split().apply(len)
```

The chapter finds that most tweets are short, around 15 words, and well below the model limit.

Why does this check matter?

If many texts are longer than the model limit, truncation can remove information that may be important for classification.

```text
model limit + long examples
            ↓
possible truncation
            ↓
possible information loss
```

[[IMAGE_NEEDED: Tweet length distribution by emotion | Boxplots of words per tweet grouped by emotion, all well below the DistilBERT input limit | Learner should notice that these tweets are short enough that truncation is unlikely to remove important content]]

After inspection, the chapter resets the dataset output format:

```python
emotions.reset_format()
```

### Practical habit

Before modeling text, inspect at least:

```text
1. columns
2. labels
3. class frequencies
4. example texts
5. text lengths
```

That habit often prevents mistakes that no model architecture can fix later.

---

## 4. From raw text to tokens

A transformer cannot directly consume a Python string such as:

```text
"Tokenizing text is a core task of NLP."
```

It needs numerical inputs.

The bridge from text to model input is **tokenization**.

The chapter builds intuition by comparing three approaches:

1. character tokenization,
2. word tokenization,
3. subword tokenization.

### 4.1 Character tokenization

Character tokenization splits text into individual characters.

```python
text = "Tokenizing text is a core task of NLP."
tokenized_text = list(text)
```

Conceptually:

```text
"cat"
 ↓
["c", "a", "t"]
```

Each unique character can be mapped to an integer ID:

```python
token2idx = {
    ch: idx
    for idx, ch in enumerate(sorted(set(tokenized_text)))
}
```

Then the characters can be transformed into IDs:

```python
input_ids = [token2idx[token] for token in tokenized_text]
```

A token ID is an identifier, not a meaningful numerical magnitude.

If token `"a"` has ID `4` and token `"b"` has ID `18`, that does **not** mean `"b"` is somehow 14 units larger than `"a"`.

The chapter uses one-hot encoding to illustrate why categorical IDs should not be interpreted as ordinal values.

Character tokenization can represent misspellings and unusual words, but it creates long sequences and forces the model to learn word structure from characters.

### 4.2 Word tokenization

Word tokenization keeps more linguistic structure.

```python
tokenized_text = text.split()
```

Conceptually:

```text
"transformers are useful"
 ↓
["transformers", "are", "useful"]
```

This is shorter and more meaningful than character-level input.

But a pure word vocabulary can become enormous because word forms, misspellings, and rare words all create vocabulary pressure.

A fixed word vocabulary often maps unseen words to a shared token such as `[UNK]`, which can lose information.

### 4.3 Subword tokenization

Subword tokenization is the compromise.

The goal is:

- keep frequent words whole,
- split rare or complex words into smaller reusable units.

For BERT and DistilBERT, the chapter discusses **WordPiece**.

Load the tokenizer associated with the DistilBERT checkpoint:

```python
from transformers import AutoTokenizer

model_ckpt = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
```

Encode a sentence:

```python
text = "Tokenizing text is a core task of NLP."
encoded_text = tokenizer(text)
```

The tokenizer returns fields including:

```text
input_ids
attention_mask
```

Convert IDs back into visible tokens:

```python
tokens = tokenizer.convert_ids_to_tokens(encoded_text.input_ids)
print(tokens)
```

The chapter's example contains special and subword tokens such as:

```text
[CLS]
token
##izing
...
[SEP]
```

Important observations:

- `[CLS]` is a special token at the beginning.
- `[SEP]` marks sequence separation/end.
- this checkpoint lowercases the input,
- a word may be split into subwords,
- a `##` prefix means the piece continues the previous token.

For example:

```text
token + ##izing -> tokenizing
```

Useful tokenizer properties include:

```python
tokenizer.vocab_size
tokenizer.model_max_length
tokenizer.model_input_names
```

The chapter reports:

```text
vocabulary size: 30,522
maximum length: 512
model inputs: ["input_ids", "attention_mask"]
```

### One rule you should remember

Use the tokenizer that belongs to the pretrained model.

A model learned meanings in relation to its tokenizer's vocabulary and ID mapping. Changing the tokenizer arbitrarily is like changing the meaning of the model's dictionary.

{{exercise:M02.L01.EX01}}

---

## 5. Tokenize the whole dataset

Tokenizing one sentence is useful for understanding the idea. Training requires tokenizing all examples.

The chapter defines a processing function:

```python
def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding=True,
        truncation=True,
    )
```

### Padding

Different texts have different lengths, while neural-network batches usually need rectangular tensors.

```text
Sentence A -> 6 tokens
Sentence B -> 10 tokens
```

Padding extends the shorter sequence:

```text
Sentence A -> 6 real tokens + 4 PAD tokens
Sentence B -> 10 real tokens
```

### Attention mask

Padding creates fake positions that should not contribute like real text.

Simplified example:

```text
input_ids:
[101, 2009, 2003, 2204, 102,   0,   0]

attention_mask:
[  1,    1,    1,    1,   1,   0,   0]
```

Interpretation:

```text
1 -> real input token
0 -> padding position
```

The model can use the mask to ignore padded positions.

[[IMAGE_NEEDED: Padding and attention mask | Two tokenized sequences of different lengths padded to the same width, with an attention mask showing 1 for real tokens and 0 for padding | Learner should understand that padding fixes tensor shape while the mask prevents PAD positions from being treated as meaningful text]]

### Truncation

If input exceeds the model's maximum context size, `truncation=True` cuts it to an acceptable length.

This is why the earlier text-length inspection mattered.

### Apply the function across the dataset

```python
emotions_encoded = emotions.map(
    tokenize,
    batched=True,
    batch_size=None,
)
```

After tokenization, the dataset contains additional columns:

```text
text
label
input_ids
attention_mask
```

### Mental model for `map()`

Think of:

```python
dataset.map(function)
```

as:

> "Apply the same transformation consistently to the dataset and store the returned fields."

This pattern appears repeatedly in the chapter.

---

## 6. Approach A — use DistilBERT as a feature extractor

A pretrained transformer already converts text into useful internal vectors called **hidden states**.

One way to build a classifier is:

```text
text
 ↓
DistilBERT (frozen)
 ↓
hidden-state vector
 ↓
small classifier
 ↓
emotion
```

The pretrained transformer is not updated. It acts as a feature generator.

[[IMAGE_NEEDED: Feature-extraction architecture | DistilBERT encoder shown as frozen, producing a hidden-state vector that is passed to a separate classifier such as logistic regression | Learner should notice that only the final classifier is trained while the transformer body stays unchanged]]

### Load the pretrained encoder

```python
import torch
from transformers import AutoModel

model_ckpt = "distilbert-base-uncased"
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = AutoModel.from_pretrained(model_ckpt).to(device)
```

### Inspect the hidden state for one sentence

```python
text = "this is a test"
inputs = tokenizer(text, return_tensors="pt")
inputs = {key: value.to(device) for key, value in inputs.items()}

with torch.no_grad():
    outputs = model(**inputs)
```

`torch.no_grad()` is appropriate because we are not training the transformer during feature extraction.

The chapter shows a last hidden-state shape like:

```text
[batch_size, number_of_tokens, hidden_dimension]
[1, 6, 768]
```

That means:

- 1 sequence,
- 6 token positions,
- one 768-dimensional representation for each position.

For classification, the chapter uses the representation associated with the first `[CLS]` position:

```python
cls_vector = outputs.last_hidden_state[:, 0]
```

Shape:

```text
[1, 768]
```

So one piece of text becomes one fixed-size vector.

### Extract vectors for the whole dataset

```python
def extract_hidden_states(batch):
    inputs = {
        key: value.to(device)
        for key, value in batch.items()
        if key in tokenizer.model_input_names
    }

    with torch.no_grad():
        last_hidden_state = model(**inputs).last_hidden_state

    return {
        "hidden_state": last_hidden_state[:, 0].cpu().numpy()
    }
```

The tokenized columns are formatted as tensors:

```python
emotions_encoded.set_format(
    "torch",
    columns=["input_ids", "attention_mask", "label"],
)
```

Then:

```python
emotions_hidden = emotions_encoded.map(
    extract_hidden_states,
    batched=True,
)
```

### Build a traditional feature matrix

```python
import numpy as np

X_train = np.array(emotions_hidden["train"]["hidden_state"])
X_valid = np.array(emotions_hidden["validation"]["hidden_state"])
y_train = np.array(emotions_hidden["train"]["label"])
y_valid = np.array(emotions_hidden["validation"]["label"])
```

The chapter reports:

```text
X_train -> (16000, 768)
X_valid -> (2000, 768)
```

So the NLP problem has become a familiar machine-learning problem: one fixed-size numerical feature vector and one target label per example.

### Visualize the representation

The chapter uses UMAP to project the 768-dimensional hidden states into two dimensions.

This is a diagnostic visualization, not the classifier.

A 2D projection can help reveal structure, but it must be interpreted carefully: overlap in 2D does not prove that classes overlap in the original 768-dimensional space.

[[IMAGE_NEEDED: UMAP projection of emotion hidden states | A 2D projection with separate panels or colors for sadness, joy, love, anger, fear, and surprise | Learner should notice that some emotions form similar regions while a 2D projection is only a simplified view of the original 768-dimensional space]]

### Train a simple classifier

```python
from sklearn.linear_model import LogisticRegression

lr_clf = LogisticRegression(max_iter=3000)
lr_clf.fit(X_train, y_train)
```

The chapter reports validation accuracy of approximately:

```text
0.633
```

That number alone is hard to interpret, so the chapter compares it with a majority-class baseline:

```python
from sklearn.dummy import DummyClassifier

dummy_clf = DummyClassifier(strategy="most_frequent")
dummy_clf.fit(X_train, y_train)
```

The baseline accuracy is about:

```text
0.352
```

Comparison:

```text
majority baseline   ≈ 35%
feature classifier  ≈ 63%
```

The DistilBERT representations clearly contain useful information about emotion.

### Confusion matrix

Accuracy tells you how often the prediction is correct overall.

A **confusion matrix** tells you *which classes are confused with which other classes*.

The chapter observes patterns such as:

- anger and fear are often confused with sadness,
- love and surprise are often confused with joy.

[[IMAGE_NEEDED: Feature-based confusion matrix | A normalized confusion matrix for the logistic-regression classifier using DistilBERT hidden states | Learner should notice that the diagonal represents correct predictions while off-diagonal cells reveal specific class confusions]]

### When feature extraction is attractive

Feature extraction can be useful when:

- training resources are limited,
- no GPU is available,
- you want a fast baseline,
- you want to use a traditional classifier.

But the transformer's representations are not being optimized specifically for your classification task.

That motivates fine-tuning.

---

## 7. Approach B — fine-tune DistilBERT end to end

In fine-tuning, the transformer itself is updated.

```text
text
 ↓
DistilBERT
 ↓
classification head
 ↓
loss
 ↓
backpropagation updates BOTH the head and transformer
```

This allows the hidden representations to adapt to the classification task.

[[IMAGE_NEEDED: Fine-tuning architecture | DistilBERT encoder connected to a classification head with both parts marked trainable and an arrow from loss/backpropagation updating the full model | Learner should contrast this with feature extraction, where the encoder is frozen]]

### Load a model with a classification head

```python
from transformers import AutoModelForSequenceClassification

num_labels = 6

model = (
    AutoModelForSequenceClassification
    .from_pretrained(model_ckpt, num_labels=num_labels)
    .to(device)
)
```

`AutoModel` gives the pretrained encoder.

`AutoModelForSequenceClassification` gives:

```text
pretrained encoder
+
classification head
```

The newly added classification head starts untrained, so an initialization warning is expected.

### Define evaluation metrics

```python
from sklearn.metrics import accuracy_score, f1_score

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)

    f1 = f1_score(labels, preds, average="weighted")
    acc = accuracy_score(labels, preds)

    return {
        "accuracy": acc,
        "f1": f1,
    }
```

Why use both?

- **Accuracy** asks: "What fraction did we classify correctly?"
- **F1-score** combines precision and recall and can be more informative when class frequencies differ.

### Configure training

Representative settings from the chapter include:

```python
from transformers import TrainingArguments

batch_size = 64
model_name = f"{model_ckpt}-finetuned-emotion"

training_args = TrainingArguments(
    output_dir=model_name,
    num_train_epochs=2,
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    push_to_hub=True,
)
```

Then:

```python
from transformers import Trainer

trainer = Trainer(
    model=model,
    args=training_args,
    compute_metrics=compute_metrics,
    train_dataset=emotions_encoded["train"],
    eval_dataset=emotions_encoded["validation"],
    tokenizer=tokenizer,
)

trainer.train()
```

The chapter reports validation performance after two epochs of roughly:

```text
accuracy ≈ 0.9225
F1       ≈ 0.9226
```

Compare the chapter's two approaches:

| Approach | What is trained? | Approx. result shown |
|---|---|---:|
| Feature extraction | Separate classifier | 63% accuracy |
| Fine-tuning | Transformer + classification head | 92% accuracy / F1 |

The point is not that fine-tuning always gives exactly these numbers.

The point is that updating the transformer for the task can produce much stronger task-specific representations.

### PyTorch and TensorFlow interoperability

The chapter also demonstrates corresponding TensorFlow classes, such as:

```python
from transformers import TFAutoModelForSequenceClassification
```

The main concept is that the same transformer family can be used through different supported deep-learning frameworks.

For this lesson, the main workflow remains the PyTorch/Trainer path because that is the chapter's central training example.

{{exercise:M02.L01.EX02}}

---

## 8. Evaluate, inspect errors, save, and use the model

A model is not finished when `trainer.train()` stops.

You still need to understand its behavior.

### Get validation predictions

```python
preds_output = trainer.predict(
    emotions_encoded["validation"]
)
```

This returns predictions, label IDs, and evaluation metrics.

Convert the raw class scores to predicted class IDs:

```python
import numpy as np

y_preds = np.argmax(
    preds_output.predictions,
    axis=1,
)
```

Then inspect the confusion matrix again.

After fine-tuning, the matrix is much closer to the ideal diagonal pattern, although some emotion pairs remain difficult.

### Error analysis with per-example loss

One of the most valuable ideas in the chapter is to inspect individual examples by their model loss.

A high loss means the model found this labeled example difficult or was confidently wrong.

A low loss means the model found the example easy and confident.

The chapter computes per-example loss:

```python
from torch.nn.functional import cross_entropy

def forward_pass_with_label(batch):
    inputs = {
        key: value.to(device)
        for key, value in batch.items()
        if key in tokenizer.model_input_names
    }

    with torch.no_grad():
        output = model(**inputs)
        pred_label = torch.argmax(output.logits, axis=-1)
        loss = cross_entropy(
            output.logits,
            batch["label"].to(device),
            reduction="none",
        )

    return {
        "loss": loss.cpu().numpy(),
        "predicted_label": pred_label.cpu().numpy(),
    }
```

### What high-loss examples can reveal

#### 1. Wrong or ambiguous labels

Human labeling is imperfect.

Some texts may:

- be mislabeled,
- express more than one emotion,
- not clearly belong to any existing class.

A difficult example is not automatically evidence of a bad model. Sometimes it is evidence of a difficult dataset.

#### 2. Dataset quirks

Models can exploit shortcuts.

A strange URL fragment, repeated phrase, formatting pattern, or unusual token may influence a prediction.

Error analysis helps you ask:

> Is the model learning the concept I intended, or is it learning an accidental shortcut?

### Also inspect very low-loss examples

Do not only inspect failures.

Very confident predictions can reveal shortcuts too.

A useful workflow is:

```text
sort by highest loss
    ↓
inspect hard/wrong examples

sort by lowest loss
    ↓
inspect suspiciously easy examples

identify label/data patterns
    ↓
improve data or modeling choices
```

This is often more valuable than immediately trying a larger model.

### Save and share

The chapter uses the Trainer API to push the model to the Hugging Face Hub:

```python
trainer.push_to_hub(
    commit_message="Training completed!"
)
```

### Run inference

A saved fine-tuned model can be loaded into a pipeline:

```python
from transformers import pipeline

model_id = (
    "transformersbook/"
    "distilbert-base-uncased-finetuned-emotion"
)

classifier = pipeline(
    "text-classification",
    model=model_id,
)
```

Test a new message:

```python
custom_tweet = "I saw a movie today and it was really good."

preds = classifier(
    custom_tweet,
    return_all_scores=True,
)
```

The output contains a score for each class. The chapter's example assigns the strongest probability to `joy`.

[[IMAGE_NEEDED: Emotion prediction probabilities | A bar chart showing the model's class probabilities for a new positive tweet, with joy clearly highest | Learner should notice that inference produces scores across classes and the final predicted class comes from the strongest score]]

---

## The full workflow

```text
1. Define the classification problem
        ↓
2. Load train / validation / test splits
        ↓
3. Inspect labels, imbalance, and text length
        ↓
4. Load the tokenizer matching the checkpoint
        ↓
5. Convert text to input_ids + attention_mask
        ↓
6. Choose a training strategy
        ↓
   Feature extraction OR fine-tuning
        ↓
7. Evaluate with metrics + confusion matrix
        ↓
8. Inspect high- and low-loss examples
        ↓
9. Save the model
        ↓
10. Run inference on new text
```

This pattern extends beyond emotion detection. The labels may change, but the core workflow remains useful for many text-classification tasks.

---

## Important misconceptions

### Misconception 1

> Token IDs are meaningful numerical quantities.

### Why this is wrong

An ID is an index into a vocabulary. Arithmetic differences between token IDs do not represent linguistic similarity.

### Misconception 2

> High validation accuracy means the model is automatically good.

### Why this is wrong

Accuracy must be interpreted alongside class balance, baselines, confusion patterns, and per-example errors.

### Misconception 3

> Padding tokens are ordinary words that the model should learn from.

### Why this is wrong

Padding exists to make batch tensors the same length. The attention mask marks those positions so they can be ignored.

### Misconception 4

> Feature extraction and fine-tuning are the same training strategy.

### Why this is wrong

Feature extraction keeps the transformer frozen. Fine-tuning updates the transformer itself together with the classification head.

### Misconception 5

> If a model is wrong, the model must be the only problem.

### Why this is wrong

High-loss examples can expose ambiguous labels, annotation errors, or unexpected data artifacts.

---

## Key terminology

| Term | Meaning |
|---|---|
| Text classification | Assigning text to one of a predefined set of labels |
| DistilBERT | A smaller, more efficient BERT-family transformer used in the chapter |
| Checkpoint | Stored pretrained weights loaded into a model architecture |
| Dataset split | A partition such as train, validation, or test |
| Class imbalance | Unequal numbers of examples across target classes |
| Tokenization | Splitting/encoding text into model-consumable units |
| Token ID | Integer identifier for a vocabulary token |
| Subword | Token unit smaller than a full word but often larger than a character |
| WordPiece | Subword tokenization approach used by BERT/DistilBERT tokenizers |
| `[CLS]` | Special token placed at the start of the sequence in this tokenizer |
| `[SEP]` | Special token used to mark sequence separation/end |
| `[PAD]` | Special padding token used to equalize sequence lengths |
| `input_ids` | Integer token IDs passed to the model |
| `attention_mask` | Mask indicating real tokens versus padded positions |
| Hidden state | Internal vector representation produced by the transformer |
| Feature extraction | Using frozen transformer representations as features for another classifier |
| Fine-tuning | Updating pretrained model parameters for the target task |
| Classification head | Final task-specific layer that produces class scores |
| Baseline | Simple reference model used to judge whether a trained model adds value |
| Confusion matrix | Matrix showing true classes against predicted classes |
| F1-score | Metric combining precision and recall |
| Error analysis | Inspecting predictions/examples to understand failure patterns |

---

## Self-check

Before continuing, make sure you can answer:

1. Why should you inspect class distribution before trusting accuracy?
2. What is the difference between a token and a token ID?
3. Why must the tokenizer match the pretrained checkpoint?
4. What problem do padding and `attention_mask` solve together?
5. What does a hidden-state shape of `[batch, tokens, 768]` mean?
6. How does feature extraction differ from fine-tuning?
7. Why is a majority-class baseline useful?
8. What can a confusion matrix reveal that accuracy cannot?
9. Why should you inspect both high-loss and low-loss examples?
10. What additional component does `AutoModelForSequenceClassification` provide compared with `AutoModel`?

---

## Retain this idea

**A transformer text classifier is not just a model call: good classification comes from understanding the dataset, using the correct tokenizer, choosing an appropriate training strategy, evaluating against meaningful baselines, and inspecting the model's mistakes before deployment.**
''',
        "estimated_minutes": 180,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "classification-overview", "title": "What text classification is", "order": 1},
            {"id": "load-dataset", "title": "Load and understand the dataset", "order": 2},
            {"id": "inspect-data", "title": "Inspect the data before modeling", "order": 3},
            {"id": "tokenization", "title": "From raw text to tokens", "order": 4},
            {"id": "tokenize-dataset", "title": "Tokenize the whole dataset", "order": 5},
            {"id": "feature-extraction", "title": "Use DistilBERT as a feature extractor", "order": 6},
            {"id": "fine-tuning", "title": "Fine-tune DistilBERT end to end", "order": 7},
            {"id": "evaluation-error-analysis", "title": "Evaluate, inspect errors, save, and use the model", "order": 8},
        ],
    },

    "exercises": [
        {
            "id": "M02.L01.EX01",
            "title": "Inspect DistilBERT Tokenization",
            "lesson_code": "M02.L01",
            "section_id": "tokenization",
            "placement": "after_section",
            "description": (
                "Practice reading subword tokens, special tokens, input IDs, "
                "and attention masks produced by the DistilBERT tokenizer."
            ),
            "instructions": (
                "1. Load AutoTokenizer with the `distilbert-base-uncased` checkpoint.\n"
                "2. Tokenize two sentences of clearly different lengths together with padding enabled.\n"
                "3. Print the tokens for the first sentence with `convert_ids_to_tokens()`.\n"
                "4. Identify `[CLS]`, `[SEP]`, any subword tokens beginning with `##`, and padded positions.\n"
                "5. Print the attention masks and explain why the padded positions contain 0.\n"
                "6. In 3-5 sentences, explain why changing to an unrelated tokenizer would be dangerous."
            ),
            "expected_output": (
                "A short Python example plus printed tokens, input IDs, attention masks, "
                "and a brief interpretation of special tokens, subwords, padding, and tokenizer/model compatibility."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "tokenization",
                "subword-tokenization",
                "attention-mask",
                "transformer-inputs",
            ],
        },
        {
            "id": "M02.L01.EX02",
            "title": "Choose and Evaluate a Classification Strategy",
            "lesson_code": "M02.L01",
            "section_id": "fine-tuning",
            "placement": "after_section",
            "description": (
                "Connect the chapter's two training strategies to evaluation and error-analysis decisions."
            ),
            "instructions": (
                "1. Create a two-column comparison of feature extraction and fine-tuning.\n"
                "2. For each approach, state which model parameters are updated and its main resource trade-off.\n"
                "3. Record the approximate validation result reported in the chapter for each approach.\n"
                "4. Explain why the approximately 63% feature-based accuracy should be compared with the approximately 35% majority baseline.\n"
                "5. Describe one confusion-matrix pattern reported in the chapter.\n"
                "6. Explain what you would inspect among the highest-loss validation examples before deciding to use a larger model."
            ),
            "expected_output": (
                "A concise comparison table and written analysis demonstrating understanding of frozen features, "
                "end-to-end fine-tuning, baselines, confusion matrices, and per-example error analysis."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "feature-extraction",
                "fine-tuning",
                "evaluation",
                "error-analysis",
            ],
        },
    ],

    "quiz": {
        "id": "M02.L01.QZ01",
        "title": "Text Classification with DistilBERT — Knowledge Check",
        "lesson_code": "M02.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M02.L01.Q01",
                "section_id": "inspect-data",
                "question": "Why does the chapter compare the trained classifier with a majority-class baseline?",
                "options": [
                    "To prove that the validation set contains no label errors",
                    "To give raw accuracy a meaningful reference point when classes are imbalanced",
                    "To replace the need for a confusion matrix",
                    "To determine the tokenizer vocabulary size",
                ],
                "correct": 1,
                "explanation": (
                    "In an imbalanced dataset, a trivial classifier can achieve non-trivial accuracy by always "
                    "predicting the most frequent class. A baseline shows how much value the trained model adds."
                ),
            },
            {
                "id": "M02.L01.Q02",
                "section_id": "tokenization",
                "question": "What does the `##` prefix on a WordPiece token such as `##izing` indicate?",
                "options": [
                    "The token is padding",
                    "The token starts a completely new word",
                    "The token continues the previous token without whitespace",
                    "The token must be ignored by the model",
                ],
                "correct": 2,
                "explanation": (
                    "The prefix marks a continuation subword. Pieces such as `token` and `##izing` combine back into the original word."
                ),
            },
            {
                "id": "M02.L01.Q03",
                "section_id": "tokenize-dataset",
                "question": "Why is an attention mask returned when shorter sequences are padded?",
                "options": [
                    "To tell the model which positions are real tokens and which are padding",
                    "To convert labels from integers to strings",
                    "To choose the emotion with the largest class frequency",
                    "To reduce the tokenizer vocabulary to 512 words",
                ],
                "correct": 0,
                "explanation": (
                    "Padding makes sequence tensors the same length, while the attention mask identifies padded positions so they are not treated like meaningful input tokens."
                ),
            },
            {
                "id": "M02.L01.Q04",
                "section_id": "fine-tuning",
                "question": "What is the central difference between feature extraction and fine-tuning in this chapter?",
                "options": [
                    "Feature extraction uses no tokenizer",
                    "Fine-tuning cannot use pretrained weights",
                    "Feature extraction requires TensorFlow while fine-tuning requires PyTorch",
                    "Feature extraction freezes the transformer, while fine-tuning updates it for the task",
                ],
                "correct": 3,
                "explanation": (
                    "The feature-based approach uses fixed hidden states from a frozen transformer. Fine-tuning updates the transformer parameters together with the classification head."
                ),
            },
            {
                "id": "M02.L01.Q05",
                "section_id": "evaluation-error-analysis",
                "type": "open",
                "question": (
                    "Suppose several validation examples have very high loss. Using the chapter's error-analysis approach, "
                    "explain at least three things you would investigate before deciding that the solution is simply to use a larger model."
                ),
            },
        ],
        "passing_score": 70,
    },
}
