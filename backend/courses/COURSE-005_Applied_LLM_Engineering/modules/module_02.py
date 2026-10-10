"""M02.L01 — Tokens and Embeddings.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 2; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"

MODULE_ORDER = 2

MODULE_TITLE = "Tokens and Embeddings"

MODULE_DESCRIPTION = (
    "Understand how language models convert text into tokens and token IDs, "
    "map those IDs into embeddings, create contextualized representations, "
    "produce sentence-level embeddings, and reuse embedding ideas in systems "
    "such as semantic search and recommendation."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Tokens and Embeddings",

    "slug": "llm-foundations-m02-l01",

    "description": (
        "A practical, beginner-friendly deep dive into tokenization and embeddings: "
        "how tokenizers prepare LLM inputs and outputs, why tokenizer design matters, "
        "how token IDs become vectors, how language models contextualize those vectors, "
        "how whole texts become embeddings, and how word2vec-style learning can power "
        "recommendation systems."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.25,

    "skill_tags": [
        "llm-tokenization",
        "tokens",
        "token-ids",
        "bpe",
        "wordpiece",
        "sentencepiece",
        "special-tokens",
        "token-embeddings",
        "contextual-embeddings",
        "text-embeddings",
        "word2vec",
        "negative-sampling",
        "recommendation-systems",
        "hugging-face",
    ],

    "prerequisite_ids": [
        "M01.L01",
    ],


    # =======================================================================
    # INLINE IMAGE RULES
    # =======================================================================
    #
    # Images are requested inline using [[IMAGE_NEEDED: ...]] placeholders.
    # The course author adds the actual image files manually later.
    # Each request appears immediately after the explanation it supports.
    #
    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Tokens and Embeddings",

        "content": (
            r"""
# Tokens and Embeddings

> **Course:** Large Language Models Foundations  
> **Lesson:** M02.L01  
> **Module:** Tokens and Embeddings  
> **Source alignment:** Chapter 2, “Tokens and Embeddings.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why an LLM does **not** directly read raw text.
- Trace the complete path from **text → tokens → token IDs → embeddings → model representations → output token IDs → text**.
- Distinguish among **word, subword, character, and byte tokenization**.
- Explain how tokenizer behavior depends on the **tokenization algorithm, tokenizer configuration, and training dataset**.
- Recognize the purpose of common **special tokens** such as `[CLS]`, `[SEP]`, `[MASK]`, `<s>`, and chat-role tokens.
- Explain why a tokenizer and its pretrained language model are tightly coupled.
- Distinguish **token IDs**, **raw/static token embeddings**, **contextualized token embeddings**, and **text embeddings**.
- Inspect tokenizer output and model embedding shapes using Hugging Face.
- Explain the core intuition behind **word2vec**, including skip-gram and negative sampling.
- Explain how the same embedding idea can be used for non-language objects such as songs in a recommendation system.
- Reason about how tokenizer and embedding design choices affect context usage and downstream applications.

---

## 1. The central mental model: text must become numbers

A language model performs numerical computation. Human language, however, arrives as text.

That means the system needs a bridge between:

```text
Human-readable language
        ↓
Machine-readable numbers
```

Chapter 2 focuses on two parts of that bridge:

1. **Tokens** divide text into manageable pieces.
2. **Embeddings** represent those pieces—or larger pieces of text—as numerical vectors.

The easiest high-level pipeline to remember is:

```text
Raw text
   ↓
Tokenizer
   ↓
Tokens
   ↓
Token IDs
   ↓
Embedding lookup
   ↓
Token vectors
   ↓
Language model
   ↓
Contextualized representations / generated token IDs
   ↓
Tokenizer decodes generated IDs
   ↓
Readable output text
```

This pipeline already fixes one of the most common beginner misunderstandings:

> **A token ID is not an embedding.**

A token ID is an integer that points to an entry in a tokenizer vocabulary. An embedding is a vector of numerical values associated with that token and used by the model for computation.

For example, imagine a tiny vocabulary:

```text
ID 10 → "cat"
ID 11 → "dog"
ID 12 → "runs"
```

The integer `10` does not contain the meaning of “cat.” It is only an identifier.

Inside the model, ID `10` might be mapped to a vector such as:

```text
[0.17, -0.52, 0.04, 0.91, ...]
```

That vector—not the integer ID—is the numerical representation used by the neural network.

[[IMAGE_NEEDED: Tokens-to-embeddings overview | A left-to-right diagram showing raw text being split into tokens, tokens mapped to integer IDs, IDs mapped to embedding vectors, and vectors passed into a language model | Learner should notice that tokenization and embedding are separate stages and that token IDs are identifiers rather than semantic vectors]]

### Why tokens matter on both input and output

Tokens are not only how the model receives your prompt.

A generative language model also produces its answer **one token at a time**. The generated result is initially a sequence of token IDs. A tokenizer then converts those IDs back into human-readable text.

So the tokenizer is used in two directions:

```text
INPUT:
text → token IDs → model

OUTPUT:
model-generated token IDs → text
```

That is why tokenization is not a cosmetic preprocessing detail. It is part of the interface between language and the model.

---

## 2. What exactly is a token?

A **token** is a unit used by a tokenizer to represent part of a text sequence.

A token might be:

- a complete word,
- part of a word,
- a character,
- a byte,
- punctuation,
- or a special control symbol.

Consider a prompt similar to the chapter example:

```text
Write an email apologizing to Sarah for the gardening mishap.
```

A subword tokenizer might split pieces approximately like this:

```text
Write
an
email
apolog
izing
to
Sarah
for
the
garden
ing
m
ish
ap
.
```

The exact split depends on the tokenizer.

The important point is that **token boundaries do not have to match word boundaries**.

The word:

```text
apologizing
```

may become something like:

```text
apolog + izing
```

A less familiar word might be divided into even smaller pieces.

### Why subwords are useful

Suppose the vocabulary contains:

```text
apolog
ize
izing
etic
ist
```

Then the tokenizer can reuse pieces across multiple related words instead of storing a completely separate token for every possible word form.

That gives the vocabulary more expressive power.

It also helps the tokenizer represent words it did not see as complete units during tokenizer training.

### Tokens can contain surprising boundaries

A beginner might expect:

```text
Subject
```

to always be one token.

But a tokenizer may encode it as:

```text
Sub + ject
```

The model can still generate the correct visible word because decoding joins the token pieces.

This teaches an important rule:

> **Visible words and model tokens are different abstractions.**

A human thinks in words and sentences. The model receives a tokenizer-defined sequence.

[[IMAGE_NEEDED: Visible text versus token pieces | Show one sentence with colored token boundaries, including at least one full-word token, one split word such as apolog + izing, punctuation as its own token, and a special token | Learner should notice that tokens can be words, subwords, punctuation, or control symbols]]

### Token IDs

Once a tokenizer divides text into tokens, it replaces each token with the token's vocabulary ID.

Conceptually:

```text
Token         Token ID
----------------------
<s>              1
Write        14350
an             385
email         4876
...
```

The model does not receive the original string.

It receives a tensor containing IDs, for example:

```text
tensor([[1, 14350, 385, 4876, ...]])
```

Those IDs refer to the tokenizer's vocabulary table.

---

## 3. Inspecting LLM tokens in code

The chapter uses a Phi-3 tokenizer and language model to make this process visible.

### 3.1 Load the model and tokenizer

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="cuda",
    torch_dtype="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct"
)
```

Two objects are loaded:

```text
tokenizer
    turns text into model-compatible token IDs
    and token IDs back into text

model
    processes those numerical inputs
    and predicts/generates output token IDs
```

### 3.2 Tokenize a prompt

```python
prompt = (
    "Write an email apologizing to Sarah for the tragic gardening mishap. "
    "Explain how it happened.<|assistant|>"
)

input_ids = tokenizer(
    prompt,
    return_tensors="pt"
).input_ids.to("cuda")
```

The useful part to focus on is:

```python
tokenizer(prompt, return_tensors="pt")
```

The tokenizer processes text.

Then:

```python
.input_ids
```

retrieves the integer IDs.

And:

```python
.to("cuda")
```

moves the tensor to the GPU because the model in this example is also loaded there.

### 3.3 Generate new tokens

```python
generation_output = model.generate(
    input_ids=input_ids,
    max_new_tokens=20
)
```

`max_new_tokens=20` means:

> Generate no more than 20 additional tokens after the supplied prompt.

It does **not** mean 20 words.

Some generated tokens may be complete words. Others may be word fragments, punctuation, or other token units.

### 3.4 Decode the result

```python
print(tokenizer.decode(generation_output[0]))
```

This reverses the mapping from token IDs back to text.

### 3.5 Inspect the tokens yourself

A highly useful debugging habit is to decode IDs individually:

```python
for token_id in input_ids[0]:
    print(tokenizer.decode(token_id))
```

This lets you see how the tokenizer actually understands the text.

When working with unfamiliar languages, code, unusual symbols, or domain-specific vocabulary, inspecting tokenization can reveal why a model uses more context than expected or struggles with certain input patterns.

[[IMAGE_NEEDED: Tokenizer input-output pipeline | A diagram showing prompt text → tokenizer → token IDs → generative model → old plus newly generated token IDs → tokenizer decode → readable text | Learner should notice that the model communicates through numerical token IDs on both the input and output sides]]

### Worked reasoning example

Suppose a tokenizer generates:

```text
"unbelievable" → ["un", "believ", "able"]
```

and assigns:

```text
"un"     → 410
"believ" → 9721
"able"   → 330
```

The model receives:

```text
[410, 9721, 330]
```

It does **not** directly receive:

```text
"unbelievable"
```

If the model later generates those same three IDs, the tokenizer can decode them back into a visible word.

That separation is fundamental.

---

## 4. Why different tokenizers split the same text differently

There is no universal tokenization of a sentence.

Two models can receive the exact same text and convert it into different token sequences.

The chapter identifies three major causes.

### 4.1 The tokenization method

Different tokenization algorithms learn or apply token vocabularies differently.

Methods discussed in the chapter include:

- **Byte Pair Encoding (BPE)** — widely associated with GPT-style tokenizers.
- **WordPiece** — used by BERT.
- **SentencePiece** — an implementation that can support approaches including BPE and the unigram language model.

These methods all aim to represent text efficiently, but they do not construct vocabularies in exactly the same way.

### 4.2 Tokenizer configuration and vocabulary choices

Even after an algorithm is selected, the designer still makes decisions such as:

- vocabulary size,
- special tokens,
- treatment of capitalization,
- domain-specific control tokens.

A vocabulary might contain roughly tens of thousands of tokens, while some newer tokenizers use larger vocabularies.

A larger vocabulary can allow common strings to fit into fewer tokens, although vocabulary design involves tradeoffs.

### 4.3 The tokenizer's training data

The vocabulary is influenced by the dataset used to train the tokenizer.

A tokenizer trained mostly on:

```text
English prose
```

will learn different useful pieces from one trained heavily on:

```text
source code
```

or:

```text
multilingual text
```

This gives us a compact rule:

```text
Tokenizer behavior
    =
tokenization method
    +
configuration choices
    +
training-data domain
```

This is one of the most important ideas in the chapter.

---

## 5. Four useful ways to think about tokenization

The chapter highlights four broad tokenization levels.

### 5.1 Word tokens

A word tokenizer attempts to represent text using entire words.

Example:

```text
machine learning works

→ ["machine", "learning", "works"]
```

This feels natural to humans.

But it creates problems.

A vocabulary would need to contain many forms:

```text
apology
apologize
apologetic
apologist
apologizing
...
```

And when a new word appears that is not in the vocabulary, the tokenizer may not have a good representation for it.

Word-level tokenization was historically important, including in methods such as word2vec, and the same idea can be useful outside language for treating objects such as songs as tokens.

### 5.2 Subword tokens

Subword tokenization mixes full words and word pieces.

Example:

```text
apologizing

→ apolog + izing
```

This gives the tokenizer two advantages:

1. Common words can remain compact.
2. New or rare words can often be constructed from smaller known pieces.

That balance is why subword tokenization is common in modern language models.

### 5.3 Character tokens

A character-level system might encode:

```text
play

→ p + l + a + y
```

This can represent new words because the letters themselves are available.

But sequences become longer.

A subword model might represent `play` using one token, while a character model needs four.

With a fixed context capacity, longer token sequences mean less text fits into the model at once.

### 5.4 Byte tokens

Another approach represents text at the byte level.

This can be particularly useful for broad character coverage and multilingual settings.

The chapter also points out an important nuance:

> A subword tokenizer may include byte tokens as a fallback without being a fully byte-level or “tokenization-free” model.

So do not classify a tokenizer as byte-level merely because bytes exist somewhere in its vocabulary.

[[IMAGE_NEEDED: Word vs subword vs character vs byte tokenization | Use the same short input and show four parallel rows demonstrating how it would be segmented as whole words, subwords, individual characters, and bytes | Learner should compare sequence length, vocabulary flexibility, and the ability to handle unseen text]]

### Practical comparison

| Scheme | Main intuition | Strength | Cost / limitation |
|---|---|---|---|
| Word | One token per known word | Human-readable units | Huge/open vocabulary and unseen-word issues |
| Subword | Reuse meaningful pieces | Good balance of compactness and coverage | Boundaries can look unintuitive |
| Character | One character per token | Can represent unseen words | Long sequences |
| Byte | Work from byte representations | Broad symbol/language coverage | Can create even lower-level sequences |

The chapter's goal is not to tell you one method is always best.

The goal is to help you see tokenization as an **engineering choice that changes what the model sees**.

---

## 6. Special tokens: vocabulary entries that control structure

Not every token represents ordinary visible text.

Tokenizers often contain **special tokens** that have structural or task-specific meanings.

Examples from the chapter include:

### Beginning-of-text tokens

```text
<s>
```

These can indicate the start of an input sequence.

### End-of-text tokens

An end token can signal that generation should stop.

### Padding tokens

```text
[PAD]
```

Padding is used when inputs need to be aligned to a common length.

### Unknown tokens

```text
[UNK]
```

These stand for text the tokenizer cannot represent through its ordinary vocabulary.

### Classification token

BERT commonly uses:

```text
[CLS]
```

The model can use this special position as a representation for classification-oriented tasks.

### Separator token

BERT also uses:

```text
[SEP]
```

This can separate pieces of text, such as a query and a candidate document in a paired-input task.

### Mask token

```text
[MASK]
```

This is used in BERT-style masked language modeling.

### Chat-role tokens

The chapter's Phi-3 discussion includes role-oriented tokens such as:

```text
<|user|>
<|assistant|>
<|system|>
```

These reflect the importance of conversational interaction for chat models.

### Domain-specific special tokens

Specialized models can go even further.

A code model might use tokens related to:

```text
filename
repository name
fill-in-the-middle generation
```

A scientific model might include dedicated structures for:

```text
citations
mathematics
reasoning markers
biological sequences
```

This gives us a useful insight:

> **The vocabulary can encode assumptions about the tasks a model is expected to perform.**

Tokenization is therefore connected to model specialization.

---

## 7. What real tokenizer comparisons teach us

The chapter compares multiple trained tokenizers using text containing:

- capitalization,
- non-English text,
- emoji,
- code-like syntax,
- indentation and whitespace,
- numbers,
- special symbols.

The purpose of the comparison is not memorizing every tokenizer's exact output.

The real goal is learning **what to inspect**.

### 7.1 BERT uncased: information can intentionally disappear

An uncased BERT tokenizer converts capitalization away.

So:

```text
English
CAPITALIZATION
```

is normalized toward lowercase behavior.

The chapter also shows that some unsupported symbols may become:

```text
[UNK]
```

This means information can be lost before the model even begins computation.

That is a major lesson:

> If the tokenizer cannot preserve information, the model cannot later recover that information from the token sequence.

### 7.2 BERT cased: preserving case can increase token fragmentation

The cased BERT tokenizer preserves uppercase text, but an all-caps word may be split into more pieces.

For example, the chapter shows a capitalized word requiring substantially more tokens than in some later tokenizers.

This demonstrates a tradeoff:

```text
preserve information
        versus
represent it compactly
```

### 7.3 GPT-2: newlines and byte fallback

The chapter's GPT-2 comparison demonstrates better preservation of line breaks and broad character reconstruction through byte-oriented fallback behavior.

This is useful because formatting itself can carry meaning.

### 7.4 Code-oriented tokenizers care about whitespace

Whitespace is especially meaningful in languages such as Python.

Consider:

```python
if ready:
    run_model()
```

The indentation tells Python which statement belongs inside the `if` block.

A tokenizer that efficiently represents common indentation patterns makes the sequence easier for a code model to work with.

The chapter notes that newer or code-oriented tokenizers may include compact representations for runs of spaces.

### 7.5 Specialized tokenizers encode domain structure

StarCoder2 includes tokens associated with code repositories and files.

Galactica includes special structures related to scientific content.

This illustrates the broader principle:

```text
Domain-specific data
        ↓
Domain-aware tokenizer choices
        ↓
Potentially easier modeling of that domain
```

### 7.6 Number tokenization can vary

The chapter also demonstrates that some tokenizers split numbers by digits while others may treat larger digit groups as single tokens.

So:

```text
600
```

might be:

```text
["600"]
```

or:

```text
["6", "0", "0"]
```

depending on the tokenizer.

You do not need to assume either strategy is universally superior.

What matters here is recognizing that **tokenization changes the basic units the model must learn to reason over**.

[[IMAGE_NEEDED: Comparison of real tokenizer behavior | A compact comparison graphic using one mixed input with English capitalization, emoji/non-English text, code indentation, and numbers, showing that BERT-like, GPT-like, and code-focused tokenizers preserve and split information differently | Learner should notice that tokenizer choices affect case, unknown symbols, whitespace, number segmentation, and sequence length]]

### Practical diagnostic questions

When evaluating a tokenizer for a task, ask:

1. Does it preserve the languages I care about?
2. Does it preserve capitalization when that matters?
3. How does it handle whitespace and newlines?
4. How many tokens does domain vocabulary require?
5. Does it represent code efficiently?
6. What special tokens does it provide?
7. How does it handle rare or unseen symbols?
8. How much of the context window will typical inputs consume?

These questions are more useful than simply asking, “Which tokenizer is best?”

---

{{exercise:M02.L01.EX01}}

---

## 8. From token IDs to token embeddings

Tokenization solves only the first part of the representation problem.

After tokenization, the model has something like:

```text
[1, 14350, 385, 4876, ...]
```

These are integer identifiers.

Neural networks need richer numerical representations.

That is where the **embedding matrix** comes in.

### 8.1 One vector per vocabulary token

A pretrained language model stores an embedding vector associated with each vocabulary token.

Conceptually:

```text
Tokenizer vocabulary
-------------------------------
ID 0   token A
ID 1   token B
ID 2   token C
...
ID N   token N

Embedding matrix
------------------------------------------
ID 0 → [ ... embedding values ... ]
ID 1 → [ ... embedding values ... ]
ID 2 → [ ... embedding values ... ]
...
ID N → [ ... embedding values ... ]
```

If the vocabulary contains `V` tokens and every embedding has `D` dimensions, the embedding table can be thought of as a matrix:

```text
V × D
```

When the model receives token ID `i`, it retrieves the embedding vector in row `i`.

[[IMAGE_NEEDED: Vocabulary embedding matrix | Show a tokenizer vocabulary column with token IDs pointing to rows in a matrix where each row contains a dense vector | Learner should notice that every vocabulary token has a learned vector and that the token ID acts as the lookup key]]

### 8.2 The tokenizer and model must agree

The chapter emphasizes that a pretrained language model is tied to its tokenizer.

Why?

Imagine tokenizer A says:

```text
ID 420 = "cat"
```

but tokenizer B says:

```text
ID 420 = "database"
```

If a model was trained assuming tokenizer A, feeding it IDs created by tokenizer B would make those numbers refer to the wrong learned vectors.

So a tokenizer is not a freely interchangeable text splitter after model training.

The mapping has meaning because the model learned parameters using that mapping.

### 8.3 Embeddings begin randomly, then training shapes them

Before training, embedding vectors can start as random numerical values.

During training, the model updates its parameters—including embeddings—so they become useful for the task being learned.

The important transition is:

```text
random vectors
     ↓
training on many examples
     ↓
vectors useful for modeling language patterns
```

The final values are learned, not manually assigned semantic labels.

---

## 9. Static embeddings versus contextualized embeddings

A raw vocabulary embedding associates a token with an initial learned vector.

But language is contextual.

Consider the word:

```text
bank
```

Compare:

```text
I deposited money at the bank.
```

with:

```text
We sat on the bank of the river.
```

The visible word is the same.

Its role and meaning are different.

A language model processes the token together with the surrounding sequence and produces **contextualized token representations**.

So the useful mental model is:

```text
raw token embedding
        +
surrounding context processed by the model
        ↓
contextualized token embedding
```

The resulting representation for the same token can differ depending on its sentence.

That is a major improvement over purely static word representations.

[[IMAGE_NEEDED: Static versus contextual token embedding | Show the word “bank” appearing in a financial sentence and a river sentence; start from the same token-level lookup concept and end with two different contextual vectors | Learner should notice that the language model changes a token's representation according to surrounding context]]

### Why contextual token embeddings matter

The chapter connects these representations to tasks such as:

- named-entity recognition,
- extractive text summarization,
- text classification,
- and other systems that need token-level understanding.

Contextual representations are also an important bridge toward understanding how modern Transformer models operate internally.

---

## 10. Inspecting contextual token embeddings with a language model

The chapter demonstrates this using DeBERTa.

### 10.1 Load a tokenizer and model

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/deberta-base"
)

model = AutoModel.from_pretrained(
    "microsoft/deberta-v3-xsmall"
)
```

### 10.2 Tokenize text

```python
tokens = tokenizer(
    "Hello world",
    return_tensors="pt"
)
```

### 10.3 Process those tokens through the model

```python
output = model(**tokens)[0]
```

Now inspect the shape:

```python
print(output.shape)
```

The chapter reports:

```text
torch.Size([1, 4, 384])
```

Let's interpret each dimension.

### Dimension 1: batch size

```text
1
```

One input sequence is being processed.

Batching allows multiple sequences to be processed together.

### Dimension 2: number of tokens

```text
4
```

But the visible input contained only two words:

```text
Hello world
```

Why four positions?

Inspecting the tokenization shows:

```text
[CLS]
Hello
world
[SEP]
```

The two extra positions are special tokens.

### Dimension 3: embedding width

```text
384
```

Each of the four token positions is represented by a vector containing 384 values.

So the output can be understood as:

```text
1 sequence
× 4 token positions
× 384 values per contextual token representation
```

This way of reading tensor shapes is extremely valuable in practical NLP.

### Follow the data, not just the API

When you see:

```python
output.shape
```

do not merely memorize a result.

Ask:

```text
What does each axis represent?
```

That habit makes model outputs far easier to debug.

[[IMAGE_NEEDED: From token IDs to contextual embeddings | Show “Hello world” becoming [CLS], Hello, world, [SEP], then token IDs, then raw embedding vectors entering the language model, then four contextual output vectors of width 384 | Learner should connect sequence length with token positions and understand what the [1, 4, 384] output shape represents]]

---

## 11. Text embeddings: one vector for a sentence or document

Token embeddings represent individual token positions.

Many applications need to represent an **entire piece of text** with a single vector.

Examples include:

- a sentence,
- a paragraph,
- a support ticket,
- a document,
- a search query.

A text embedding model can be viewed as:

```text
Text
  ↓
Embedding model
  ↓
One dense vector representing the text
```

For example:

```text
"Best movie ever!"
```

might become a vector with hundreds of numerical dimensions.

The values themselves are not meant to be read manually.

Their usefulness comes from how vectors relate to one another.

### Why one vector is useful

If semantically similar pieces of text receive nearby vectors, we can build systems that compare meaning rather than exact words.

For example:

```text
Query:
"How do I reset my password?"

Document A:
"Steps for changing a forgotten password"

Document B:
"How to choose a payment method"
```

A good embedding model should place the query closer to document A in embedding space because their meanings are related.

That is the foundation of semantic retrieval.

The chapter later connects text embeddings to:

- categorization,
- semantic search,
- topic-oriented applications,
- retrieval-augmented generation.

[[IMAGE_NEEDED: Sentence-to-vector embedding | Show a complete sentence entering a text embedding model and emerging as one vector, followed by three example application branches: semantic search, categorization, and RAG retrieval | Learner should notice the difference between many per-token vectors and one vector representing a whole text]]

### A sentence-transformers example

The chapter uses `sentence-transformers`:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-mpnet-base-v2"
)

vector = model.encode("Best movie ever!")
```

Inspect the shape:

```python
print(vector.shape)
```

The chapter's example produces:

```text
(768,)
```

That means:

```text
one sentence
→ one vector
→ 768 numerical values
```

Do not confuse this with the earlier DeBERTa output:

```text
[1, 4, 384]
```

That earlier output contained one vector **for every token position**.

Here:

```text
(768,)
```

is one vector for the complete text.

### Token embedding versus text embedding

| Representation | Represents | Typical shape intuition |
|---|---|---|
| Token ID | Vocabulary entry | scalar integer per token |
| Raw token embedding | One vocabulary token | one vector |
| Contextual token embedding | One token in a particular context | one vector per token position |
| Text embedding | Entire sentence/document | one vector per text |

This table is worth remembering.

---

## 12. Word embeddings before modern LLMs

Before contextual language-model embeddings became dominant, methods such as:

- word2vec,
- GloVe,
- fastText,

were widely used to create useful word representations.

The chapter demonstrates pretrained GloVe embeddings through Gensim:

```python
import gensim.downloader as api

model = api.load("glove-wiki-gigaword-50")
```

This downloads vectors learned from large amounts of text.

Then:

```python
model.most_similar(
    [model["king"]],
    topn=11
)
```

returns nearby vectors.

The chapter's example includes words such as:

```text
prince
queen
emperor
kingdom
throne
ruler
```

That result demonstrates the purpose of an embedding space:

> Nearby vectors often correspond to related usage patterns or meanings.

### Important interpretation

The model was not given a manually written rule:

```text
king is related to queen
king is related to prince
```

Instead, the relationships emerge from patterns in the training data.

This is one of the central ideas behind representation learning.

---

## 13. How word2vec learns useful vectors

The chapter uses word2vec to introduce an important learning pattern that will appear again later.

The key question is:

> How can we train vectors so that words occurring in similar contexts become meaningfully related?

### 13.1 Build examples from a sliding window

Suppose we have a sequence of words:

```text
Thou shalt not make a machine in the likeness of a human mind
```

Choose a center word and look at nearby words within a window.

If the window includes two neighbors on each side, the center word can be paired with several nearby words.

These become **positive examples**.

Conceptually:

```text
(center word, nearby word) → related / positive
```

[[IMAGE_NEEDED: Word2vec sliding window | Show a short sentence with one center word highlighted and two neighboring words on each side inside a sliding window; draw positive training pairs from the center to each neighbor | Learner should notice how ordinary running text is converted into many word-pair training examples]]

### 13.2 Why positive examples alone are not enough

Imagine every training target were:

```text
1 = these two words are neighbors
```

A useless model could always predict:

```text
1
```

and appear correct.

So training also needs examples where the pair is not expected to represent a normal neighboring relationship.

These are **negative examples**.

Conceptually:

```text
(real neighbor pair)   → 1
(random/non-neighbor)  → 0
```

This gives the model something meaningful to discriminate.

### 13.3 Skip-gram and negative sampling

The chapter emphasizes two ideas:

**Skip-gram**

Use a center word to predict or learn relationships with surrounding words.

**Negative sampling**

Add sampled non-neighbor examples so the model learns to distinguish real contextual relationships from unrelated pairs.

A simplified training set might look like:

```text
(machine, make)     → 1
(machine, in)       → 1
(machine, likeness) → 1

(machine, banana)   → 0
(machine, ocean)    → 0
(machine, violin)   → 0
```

The exact examples depend on the dataset and sampling.

[[IMAGE_NEEDED: Positive and negative word2vec pairs | Two groups of word pairs: genuine context neighbors labeled 1 and sampled unrelated pairs labeled 0, feeding a small neural network | Learner should notice that embeddings improve because the model learns to separate observed contextual relationships from negative samples]]

### 13.4 Initialize an embedding matrix

Just as with a language model vocabulary, each word receives a vector.

Initially:

```text
word → random vector
```

Then training repeatedly adjusts those vectors.

If two words participate in similar contextual patterns, the learning process can move their representations into useful relative positions.

### 13.5 The real product is the learned embedding space

The classification task is a training mechanism.

What we ultimately care about is the vector representation learned during that process.

After training:

```text
word → useful learned vector
```

Those vectors can be used for similarity calculations and downstream applications.

### The broader idea

The chapter uses word2vec to prepare you for a much more general concept:

> Learn representations by training a model to distinguish related pairs from unrelated pairs.

That pattern appears again in contrastive learning and cross-modal systems.

---

## 14. Embeddings beyond words: a song recommendation system

One of the most valuable lessons in the chapter is that embeddings are **not limited to language**.

If you can express data as meaningful sequences or relationships, you can often learn embeddings for other objects.

The chapter's example treats:

```text
song ≈ word/token
playlist ≈ sentence
```

This is a powerful abstraction.

### Step 1: Treat each playlist as a sequence

Imagine playlists:

```text
Playlist A:
song_10, song_41, song_8, song_99

Playlist B:
song_2, song_41, song_8, song_13
```

Songs that repeatedly occur in similar playlist neighborhoods may have related listening patterns.

### Step 2: Train Word2Vec over song IDs

The chapter uses:

```python
from gensim.models import Word2Vec

model = Word2Vec(
    playlists,
    vector_size=32,
    window=20,
    negative=50,
    min_count=1,
    workers=4,
)
```

Interpret the important parameters:

```text
vector_size=32
    each song receives a 32-dimensional embedding

window=20
    contextual relationships can consider a relatively wide playlist neighborhood

negative=50
    training uses many sampled negative examples

min_count=1
    keep songs that appear at least once

workers=4
    use multiple worker threads during training
```

### Step 3: Ask for nearest neighbors

Once every song has an embedding:

```python
model.wv.most_similar(
    positive=str(song_id)
)
```

can retrieve songs whose vectors are nearby.

The chapter shows examples where familiar songs receive recommendations by related artists or genres.

This demonstrates the general mechanism:

```text
human-created co-occurrence behavior
        ↓
training examples
        ↓
learned item embeddings
        ↓
nearest-neighbor similarity
        ↓
recommendations
```

[[IMAGE_NEEDED: Playlist-to-song-embeddings recommender | Show playlists as sequences of song IDs feeding a Word2Vec-style model, producing one vector per song, followed by nearest-neighbor lookup that returns similar songs | Learner should notice that the same algorithmic idea used for word context can model item similarity from playlist co-occurrence]]

### Why this example matters

It changes how you should think about embeddings.

Do not ask only:

```text
How do I embed text?
```

Also ask:

```text
What are my objects?
What relationships or sequences connect them?
Can those relationships be used to learn a useful vector space?
```

That is the more general engineering insight.

---

{{exercise:M02.L01.EX02}}

---

## 15. Putting tokens and embeddings together

You now have enough pieces to trace a modern language-model input from beginning to end.

Consider:

```text
"Hello world"
```

### Stage 1 — Tokenization

The tokenizer might produce:

```text
[CLS]
Hello
world
[SEP]
```

### Stage 2 — Convert tokens to IDs

Conceptually:

```text
[101, 7592, 2088, 102]
```

The exact IDs depend on the tokenizer.

### Stage 3 — Embedding lookup

Each ID selects a learned row from an embedding matrix:

```text
101  → vector A
7592 → vector B
2088 → vector C
102  → vector D
```

### Stage 4 — Contextual processing

The Transformer layers process those vectors together.

The output contains contextualized representations:

```text
contextual([CLS])
contextual(Hello)
contextual(world)
contextual([SEP])
```

### Stage 5 — Use the output for a task

Depending on the model and application, those representations could support:

- classification,
- named-entity recognition,
- extraction,
- retrieval,
- semantic comparison,
- or other downstream tasks.

A generative model uses its representations to predict the next token and repeatedly continue the sequence.

### A compact final diagram

```text
TEXT
"Hello world"
    ↓
TOKENIZER
["[CLS]", "Hello", "world", "[SEP]"]
    ↓
TOKEN IDS
[101, 7592, 2088, 102]
    ↓
EMBEDDING LOOKUP
4 raw vectors
    ↓
TRANSFORMER / LANGUAGE MODEL
4 contextualized vectors
    ↓
TASK-SPECIFIC USE
classification / extraction / generation / etc.
```

For sentence embedding systems, an additional process ultimately gives:

```text
whole text
    ↓
one semantic vector
```

That vector can be indexed and compared for applications such as semantic search.

---

## Important misconceptions

### Misconception 1

> A token is the same thing as a word.

### Why this is wrong

A token can be a word, subword, character, byte, punctuation symbol, or special token.

Always inspect the tokenizer rather than assuming word boundaries.

---

### Misconception 2

> A token ID contains semantic meaning.

### Why this is wrong

The token ID is an index into a vocabulary.

The learned embedding vector is the richer numerical representation used by the model.

Changing a token's arbitrary integer label would not by itself create a new semantic relationship. What matters is how the model associates that index with learned parameters.

---

### Misconception 3

> Any tokenizer can be used with any pretrained model.

### Why this is wrong

The model was trained using a particular mapping between token IDs and vocabulary entries.

Replacing the tokenizer can change what each input ID means to the model.

---

### Misconception 4

> Embeddings always represent a word the same way.

### Why this is wrong

Static word embeddings associate one vector with a word/token, but language models can create contextualized token embeddings whose values depend on the surrounding sequence.

---

### Misconception 5

> A text embedding is just a token ID for a sentence.

### Why this is wrong

A text embedding is a dense learned vector representing a larger piece of text.

It is not an identifier.

---

### Misconception 6

> Tokenization is only an implementation detail and does not affect model behavior.

### Why this is wrong

Tokenization affects sequence length, preservation of capitalization and whitespace, multilingual coverage, representation of code and numbers, special control structures, and how much information fits into a finite context.

---

## Key terminology

| Term | Meaning |
|---|---|
| Token | A tokenizer-defined unit such as a word, subword, character, byte, punctuation mark, or special symbol |
| Tokenizer | Component that maps text to token IDs and decodes token IDs back to text |
| Vocabulary | The tokenizer's collection of known tokens and their IDs |
| Token ID | Integer identifier for a token in the vocabulary |
| BPE | Byte Pair Encoding, a common subword tokenization method |
| WordPiece | Tokenization approach associated with BERT |
| SentencePiece | Tokenizer implementation supporting approaches including BPE and unigram language modeling |
| Special token | Token with a structural/task role rather than ordinary text meaning |
| `[UNK]` | Unknown token used when text cannot be represented through the ordinary vocabulary |
| `[CLS]` | Classification-oriented special token in BERT-style models |
| `[SEP]` | Separator special token used to delimit pieces of input |
| `[MASK]` | Token used in masked language modeling |
| Embedding | Dense numerical vector used to represent an item |
| Embedding matrix | Table containing learned vectors for vocabulary entries |
| Static embedding | One learned representation associated with a token/word independent of its current sentence |
| Contextualized embedding | Representation of a token after the language model has processed its surrounding context |
| Text embedding | Single vector representing a sentence, paragraph, or document |
| Embedding dimension | Number of numerical values in an embedding vector |
| Skip-gram | Word2vec approach built around learning relationships between a center word and nearby words |
| Negative sampling | Training technique that adds sampled non-neighbor examples |
| Semantic similarity | Similarity based on meaning or usage patterns rather than exact string equality |
| Recommendation embedding | Vector representation of an item learned from behavioral/contextual relationships |

---

## Self-check

Before continuing, make sure you can answer these without looking back:

1. Why does an LLM need a tokenizer?
2. What is the difference between a token and a token ID?
3. Why is a token ID not an embedding?
4. What advantage does subword tokenization have over pure word tokenization?
5. Why can character tokenization consume a context window faster?
6. What three broad factors determine tokenizer behavior?
7. Why can whitespace tokenization matter for code?
8. What is a special token? Give three examples.
9. Why should a pretrained model normally use its associated tokenizer?
10. What shape would you expect from a model that outputs one vector per token?
11. How is a text embedding different from a contextual token embedding?
12. What do skip-gram and negative sampling contribute to word2vec?
13. How can playlists be treated like sentences to learn song embeddings?
14. Why can nearest-neighbor search over embeddings support recommendations?
15. Trace the full path from raw text to contextualized token vectors.

---

## Retain this idea

**An LLM never works directly with the sentence you see on screen. A tokenizer first defines the model's units and maps them to IDs; the model then maps those IDs into learned vectors and transforms them according to context. Understanding this separation—text, tokens, IDs, embeddings, and contextual representations—is foundational to understanding everything that follows in modern language models.**
"""
        ),

        "estimated_minutes": 135,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "mental-model",
                "title": "The central mental model: text must become numbers",
                "order": 1,
            },
            {
                "id": "tokenization",
                "title": "What exactly is a token?",
                "order": 2,
            },
            {
                "id": "tokenizer-code",
                "title": "Inspecting LLM tokens in code",
                "order": 3,
            },
            {
                "id": "tokenizer-design",
                "title": "Why different tokenizers split the same text differently",
                "order": 4,
            },
            {
                "id": "token-types",
                "title": "Four useful ways to think about tokenization",
                "order": 5,
            },
            {
                "id": "special-tokens",
                "title": "Special tokens: vocabulary entries that control structure",
                "order": 6,
            },
            {
                "id": "comparing-tokenizers",
                "title": "What real tokenizer comparisons teach us",
                "order": 7,
            },
            {
                "id": "token-embeddings",
                "title": "From token IDs to token embeddings",
                "order": 8,
            },
            {
                "id": "contextual-embeddings",
                "title": "Static embeddings versus contextualized embeddings",
                "order": 9,
            },
            {
                "id": "deberta-example",
                "title": "Inspecting contextual token embeddings with a language model",
                "order": 10,
            },
            {
                "id": "text-embeddings",
                "title": "Text embeddings: one vector for a sentence or document",
                "order": 11,
            },
            {
                "id": "word-embeddings",
                "title": "Word embeddings before modern LLMs",
                "order": 12,
            },
            {
                "id": "word2vec-training",
                "title": "How word2vec learns useful vectors",
                "order": 13,
            },
            {
                "id": "recommendations",
                "title": "Embeddings beyond words: a song recommendation system",
                "order": 14,
            },
            {
                "id": "putting-it-together",
                "title": "Putting tokens and embeddings together",
                "order": 15,
            },
            {
                "id": "misconceptions",
                "title": "Important misconceptions",
                "order": 16,
            },
            {
                "id": "terminology",
                "title": "Key terminology",
                "order": 17,
            },
            {
                "id": "self-check",
                "title": "Self-check",
                "order": 18,
            },
            {
                "id": "retention",
                "title": "Retain this idea",
                "order": 19,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M02.L01.EX01",

            "title": "Inspect and Compare Tokenization",

            "lesson_code": "M02.L01",

            "section_id": "comparing-tokenizers",

            "placement": "after_section",

            "description": (
                "Practice reading tokenizer output and reasoning about how "
                "tokenization choices affect model inputs."
            ),

            "instructions": (
                "Use at least two tokenizers available through Hugging Face. "
                "Tokenize the same short mixed input containing: (1) normal English, "
                "(2) an ALL-CAPS word, (3) a number, (4) punctuation, and (5) a "
                "short code fragment with indentation. Then:\n"
                "1. Print the token IDs for each tokenizer.\n"
                "2. Decode or convert the IDs back to individual token strings.\n"
                "3. Count how many tokens each tokenizer creates.\n"
                "4. Identify at least three differences in segmentation.\n"
                "5. Explain whether capitalization, whitespace, numbers, or code "
                "structure are preserved differently.\n"
                "6. State one practical consequence of each difference.\n"
                "7. Finish with a short paragraph explaining why tokenizer choice "
                "is part of model design rather than a neutral preprocessing step."
            ),

            "expected_output": (
                "A short notebook or script plus a comparison table containing "
                "the input, tokenizer names, token counts, token strings, notable "
                "differences, and an interpretation of how those differences could "
                "affect context use or model specialization."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tokenization-inspection",
                "token-id-decoding",
                "tokenizer-comparison",
                "engineering-reasoning",
            ],
        },

        {
            "id": "M02.L01.EX02",

            "title": "Build the Embedding Mental Model",

            "lesson_code": "M02.L01",

            "section_id": "recommendations",

            "placement": "after_section",

            "description": (
                "Connect token-level embeddings, contextual embeddings, whole-text "
                "embeddings, and recommendation embeddings through one applied analysis."
            ),

            "instructions": (
                "Complete the following four-part exercise:\n"
                "1. TOKEN LEVEL: Choose a two- or three-word sentence, tokenize it, "
                "and list its visible tokens and token IDs.\n"
                "2. CONTEXT LEVEL: Use a Transformer encoder to process the sentence. "
                "Record the output tensor shape and explain what every dimension means.\n"
                "3. TEXT LEVEL: Use a sentence embedding model to produce one vector "
                "for the full sentence. Record the vector shape and explain how it "
                "differs from the contextual token output.\n"
                "4. GENERALIZATION: Imagine the items were songs instead of words. "
                "Explain how playlists could provide positive contextual relationships "
                "and how nearest-neighbor search over learned song vectors could produce "
                "recommendations.\n"
                "Finally, write the pipeline from raw text to token IDs to embeddings "
                "in your own words."
            ),

            "expected_output": (
                "A notebook or written analysis containing tokenization output, "
                "at least two tensor/vector shapes with explanations, a comparison "
                "of contextual token embeddings versus text embeddings, and a concise "
                "description of the playlist-based recommendation analogy."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "token-ids",
                "contextual-embeddings",
                "tensor-shape-interpretation",
                "text-embeddings",
                "embedding-generalization",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M02.L01.QZ01",

        "title": "Tokens and Embeddings — Knowledge Check",

        "lesson_code": "M02.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M02.L01.Q01",

                "section_id": "mental-model",

                "question": (
                    "Which sequence best describes how raw text becomes numerical "
                    "input that a language model can process?"
                ),

                "options": [
                    "Text → embedding dimensions → vocabulary → token IDs",
                    "Text → tokenizer → token IDs → embedding lookup → model",
                    "Text → model → tokenizer → embedding lookup",
                    "Text → token IDs → tokenizer → words → model",
                ],

                "correct": 1,

                "explanation": (
                    "The tokenizer first segments text and maps those pieces to "
                    "integer token IDs. The model then uses those IDs to retrieve "
                    "learned vectors before deeper processing."
                ),
            },

            {
                "id": "M02.L01.Q02",

                "section_id": "tokenization",

                "question": "Which statement about tokens is correct?",

                "options": [
                    "Every token must be a complete visible word.",
                    "A token is always a single character.",
                    "A token can be a full word, subword, punctuation mark, byte, or special symbol.",
                    "Tokens only exist on the input side of a generative model.",
                ],

                "correct": 2,

                "explanation": (
                    "Tokenizer vocabularies may contain multiple kinds of units, "
                    "and generated outputs are also produced as token IDs before "
                    "being decoded to text."
                ),
            },

            {
                "id": "M02.L01.Q03",

                "section_id": "token-types",

                "question": (
                    "Why is subword tokenization often a useful compromise between "
                    "word-level and character-level tokenization?"
                ),

                "options": [
                    "It guarantees that every sentence uses exactly one token.",
                    "It can keep common units compact while constructing rarer words from smaller known pieces.",
                    "It removes the need for a tokenizer vocabulary.",
                    "It preserves only whitespace and punctuation.",
                ],

                "correct": 1,

                "explanation": (
                    "Subword systems can encode common words or fragments compactly "
                    "while retaining the ability to represent unfamiliar words from "
                    "smaller units."
                ),
            },

            {
                "id": "M02.L01.Q04",

                "section_id": "tokenizer-design",

                "question": (
                    "According to the lesson, which combination most directly "
                    "determines a tokenizer's behavior?"
                ),

                "options": [
                    "Only the number of model parameters",
                    "Only the GPU and batch size",
                    "Tokenization method, tokenizer configuration, and tokenizer training data",
                    "Prompt length, optimizer, and inference temperature",
                ],

                "correct": 2,

                "explanation": (
                    "The chapter organizes tokenizer behavior around the chosen "
                    "method, design choices such as vocabulary/special tokens, and "
                    "the domain of the data used to train the tokenizer."
                ),
            },

            {
                "id": "M02.L01.Q05",

                "section_id": "special-tokens",

                "question": "What is the main role of a special token such as [SEP]?",

                "options": [
                    "It necessarily represents an ordinary English word.",
                    "It carries a structural or task-specific function in the model input.",
                    "It replaces the embedding matrix.",
                    "It increases the GPU's VRAM.",
                ],

                "correct": 1,

                "explanation": (
                    "Special tokens are vocabulary entries with structural or "
                    "task-oriented roles; [SEP], for example, can delimit pieces "
                    "of a paired input."
                ),
            },

            {
                "id": "M02.L01.Q06",

                "section_id": "token-embeddings",

                "question": (
                    "Why should you normally use a pretrained model with the "
                    "tokenizer associated with that model?"
                ),

                "options": [
                    "Because all tokenizers produce the same IDs but at different speeds.",
                    "Because the model learned parameters assuming a particular mapping between token IDs and vocabulary entries.",
                    "Because the tokenizer performs all neural-network computation.",
                    "Because embeddings are stored only in the tokenizer.",
                ],

                "correct": 1,

                "explanation": (
                    "The token IDs are meaningful only in relation to the vocabulary "
                    "mapping used during training. A different tokenizer can map the "
                    "same integer to a different token."
                ),
            },

            {
                "id": "M02.L01.Q07",

                "section_id": "deberta-example",

                "question": (
                    "A model output has shape [1, 4, 384]. In the chapter's "
                    "contextual-embedding example, what does the 4 represent?"
                ),

                "options": [
                    "Four different models",
                    "Four training epochs",
                    "Four token positions in the processed input sequence",
                    "Four possible labels",
                ],

                "correct": 2,

                "explanation": (
                    "The sentence is represented by four token positions after "
                    "special tokens are included: [CLS], Hello, world, and [SEP]."
                ),
            },

            {
                "id": "M02.L01.Q08",

                "section_id": "text-embeddings",

                "question": (
                    "Which statement best distinguishes a text embedding from "
                    "contextualized token embeddings?"
                ),

                "options": [
                    "A text embedding is always an integer ID.",
                    "A text embedding represents a whole text with one vector, while contextualized token outputs provide vectors for token positions.",
                    "Contextualized token embeddings cannot contain numerical values.",
                    "There is no practical difference between them.",
                ],

                "correct": 1,

                "explanation": (
                    "Text embedding models produce a single vector for a larger "
                    "piece of text, while token-level model outputs provide one "
                    "context-sensitive vector per token position."
                ),
            },

            {
                "id": "M02.L01.Q09",

                "section_id": "word2vec-training",

                "question": (
                    "Why does word2vec-style training use negative examples in "
                    "addition to true neighboring word pairs?"
                ),

                "options": [
                    "To make all embeddings equal",
                    "To prevent the model from succeeding by always predicting that every pair is related",
                    "To remove the embedding matrix",
                    "To convert characters into bytes",
                ],

                "correct": 1,

                "explanation": (
                    "If every target were positive, a model could always predict "
                    "the positive class. Negative samples create a meaningful "
                    "discrimination task."
                ),
            },

            {
                "id": "M02.L01.Q10",

                "section_id": "recommendations",

                "question": (
                    "In the chapter's recommendation-system analogy, what plays "
                    "the role of a sentence and what plays the role of a word?"
                ),

                "options": [
                    "A song is the sentence and a playlist is the word.",
                    "The artist is the sentence and the listener is the word.",
                    "A playlist is treated like a sentence and each song like a token/word.",
                    "The embedding vector is the sentence and the model is the word.",
                ],

                "correct": 2,

                "explanation": (
                    "The system treats songs as sequence items analogous to words "
                    "and playlists as sequences analogous to sentences, allowing "
                    "co-occurrence patterns to shape song embeddings."
                ),
            },

            {
                "id": "M02.L01.Q11",

                "section_id": "comparing-tokenizers",

                "question": (
                    "Why can efficient representations of repeated spaces or "
                    "indentation be useful for code-oriented models?"
                ),

                "options": [
                    "Whitespace has no meaning in code, so it should always be removed.",
                    "It can reduce sequence burden while preserving structural information important in code such as indentation.",
                    "It prevents the model from using special tokens.",
                    "It makes every number a single token.",
                ],

                "correct": 1,

                "explanation": (
                    "In languages such as Python, indentation carries structure. "
                    "Representing common whitespace patterns efficiently can make "
                    "the sequence easier for a code-focused model to learn."
                ),
            },

            {
                "id": "M02.L01.Q12",

                "section_id": "putting-it-together",

                "type": "open",

                "question": (
                    "Take the sentence “Machine learning is useful.” Explain, in "
                    "your own words, the path from visible text to token IDs to "
                    "learned token vectors to contextualized representations. Then "
                    "explain how a separate text-embedding model could represent "
                    "the whole sentence with one vector."
                ),
            },
        ],

        "passing_score": 70,
    },
}
