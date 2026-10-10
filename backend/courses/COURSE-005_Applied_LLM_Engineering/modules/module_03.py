"""M03.L01 — Looking Inside Large Language Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 3; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"

MODULE_ORDER = 3

MODULE_TITLE = "Looking Inside Large Language Models"

MODULE_DESCRIPTION = (
    "Build an intuitive and practical mental model of how generative Transformer "
    "language models produce text: autoregressive generation, the forward pass, "
    "the language modeling head, decoding, context processing, KV caching, "
    "Transformer blocks, attention, query/key/value calculations, and modern "
    "efficiency improvements such as grouped-query attention, Flash Attention, "
    "normalization changes, and rotary positional embeddings."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Looking Inside Large Language Models",

    "slug": "llm-foundations-m03-l01",

    "description": (
        "A beginner-friendly deep dive into the internal flow of generative "
        "Transformer LLMs, from token-by-token generation and next-token scoring "
        "through Transformer blocks, self-attention, query/key/value vectors, "
        "KV caching, and modern architectural improvements."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.5,

    "skill_tags": [
        "transformers",
        "autoregressive-generation",
        "forward-pass",
        "lm-head",
        "decoding",
        "context-window",
        "kv-cache",
        "self-attention",
        "multi-head-attention",
        "query-key-value",
        "feedforward-network",
        "grouped-query-attention",
        "flash-attention",
        "rope",
        "llm-architecture",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M02.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Looking Inside Large Language Models",

        "content": (
            r"""
# Looking Inside Large Language Models

> **Course:** Large Language Models Foundations  
> **Lesson:** M03.L01  
> **Module:** Looking Inside Large Language Models  
> **Source alignment:** Chapter 3, “Looking Inside Large Language Models.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why a generative LLM produces text **one token at a time**.
- Define **autoregressive generation** and trace the generation loop.
- Explain the role of the **tokenizer**, **Transformer stack**, and **language modeling head**.
- Interpret the shapes of hidden-state tensors and LM-head outputs.
- Explain the difference between **model scores** and the final **decoding decision**.
- Distinguish deterministic greedy decoding from probability-based sampling at a conceptual level.
- Explain what the **context length** limits.
- Explain why generation becomes expensive without caching.
- Describe the purpose of the **KV cache**.
- Identify the two major computational components of a Transformer block: **attention** and the **feedforward network**.
- Explain the intuition behind self-attention.
- Describe the two central operations of attention: **relevance scoring** and **information combination**.
- Explain the roles of **queries, keys, and values** without treating them as mysterious terminology.
- Explain why multi-head attention performs several attention operations in parallel.
- Distinguish full attention, local/sparse attention, multi-query attention, and grouped-query attention at a conceptual level.
- Explain what Flash Attention optimizes.
- Explain why positional information is necessary and where **RoPE** enters attention.
- Build a coherent end-to-end mental model of one next-token generation step.

---

## 1. The first big idea: an LLM writes one token at a time

From the outside, a text-generation system appears simple:

```text
Prompt
   ↓
Language model
   ↓
Generated response
```

That picture is useful, but it hides the most important fact about generation:

> **A generative Transformer does not normally produce an entire response in one step. It repeatedly predicts one next token.**

Suppose the prompt is:

```text
The capital of France is
```

The model processes the prompt and predicts a distribution over possible next tokens.

A likely next token might decode to:

```text
Paris
```

Now the effective sequence becomes:

```text
The capital of France is Paris
```

The model runs again to predict what comes next.

Then again.

And again.

This creates the generation loop:

```text
1. Read the current token sequence.
2. Predict scores for the next token.
3. Select one token.
4. Append that token to the sequence.
5. Repeat.
```

[[IMAGE_NEEDED: Autoregressive token generation loop | Show an initial prompt entering the model, one output token being selected, that token appended to the prompt, and the enlarged sequence entering the model again for the next step | Learner should notice that generation is an iterative loop rather than one operation that writes the whole answer at once]]

### A simple conceptual example

Imagine the current text is:

```text
I like machine
```

A hypothetical model might assign:

```text
"learning"     0.63
"tools"        0.12
"systems"      0.08
"models"       0.06
other tokens   0.11
```

After a decoding strategy chooses:

```text
learning
```

the next model input conceptually becomes:

```text
I like machine learning
```

The model now predicts another next token.

### What does “autoregressive” mean?

A model is **autoregressive** when earlier generated outputs become part of the input used to generate later outputs.

In text generation:

```text
generated token 1
        ↓
helps generate token 2
        ↓
tokens 1 and 2
        ↓
help generate token 3
        ↓
...
```

This is why decoder-style generative LLMs are commonly described as autoregressive.

The output is not planned as a finished paragraph and emitted all at once. It emerges sequentially.

---

## 2. Loading a generative model

The chapter begins with the same Phi-3 family used previously.

```python
import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)
```

Load the tokenizer:

```python
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct"
)
```

Load the causal language model:

```python
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="cuda",
    torch_dtype="auto",
    trust_remote_code=True,
)
```

Then create a generation pipeline:

```python
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=False,
    max_new_tokens=50,
    do_sample=False,
)
```

Let's unpack the important pieces.

### `text-generation`

This tells the pipeline that the task is autoregressive text generation.

### `return_full_text=False`

The returned value focuses on newly generated text rather than returning the original prompt together with it.

### `max_new_tokens=50`

Generation may add at most 50 new tokens.

Again:

```text
50 tokens ≠ necessarily 50 words
```

The tokenizer determines the units.

### `do_sample=False`

This asks generation not to sample randomly from the probability distribution.

The chapter later connects deterministic behavior like this to greedy next-token selection.

Now generation becomes simple:

```python
prompt = (
    "Write an email apologizing to Sarah for the tragic gardening mishap. "
    "Explain how it happened."
)

output = generator(prompt)

print(output[0]["generated_text"])
```

The important learning point is not the email itself.

The important point is what happens repeatedly underneath:

```text
tokenize
→ model forward pass
→ next-token scores
→ choose token
→ append token
→ repeat
```

---

## 3. What happens in one forward pass?

A **forward pass** means input values flow through the neural network's computations until output values are produced.

For one next-token step, the chapter gives us three major system components:

```text
Tokenizer
    ↓
Stack of Transformer blocks
    ↓
Language Modeling Head (LM head)
```

This is one of the most useful diagrams to remember.

### Component 1 — Tokenizer

The tokenizer converts visible text into token IDs.

For example:

```text
"The capital of France is"

→ [token_id_1, token_id_2, ..., token_id_6]
```

Those IDs identify rows in the model's token-embedding table.

### Component 2 — Transformer stack

The token representations flow through a stack of Transformer blocks.

The chapter's Phi-3 example contains:

```text
32 Transformer decoder layers
```

Each block contains major components including:

```text
self-attention
feedforward/MLP processing
normalization
residual paths
```

At a high level, the stack progressively transforms the representation of every token position.

### Component 3 — LM head

After the Transformer stack, the model still has vectors.

The **language modeling head** maps those vectors into one score for every vocabulary token.

For the chapter's Phi-3 example, the model vocabulary has:

```text
32,064 tokens
```

so the LM head produces:

```text
32,064 output scores
```

for each sequence position.

[[IMAGE_NEEDED: One Transformer forward pass | Show tokenizer → token embeddings → stacked Transformer decoder blocks → final hidden vectors → LM head → score for every vocabulary token | Learner should notice that the Transformer does not directly output a word; the LM head converts a hidden representation into vocabulary-wide next-token scores]]

### The model structure tells the same story

The chapter prints the model and highlights a structure conceptually like:

```text
Phi3ForCausalLM
├── model
│   ├── embed_tokens
│   ├── decoder layers × 32
│   └── final normalization
└── lm_head
```

The embedding layer is shown as roughly:

```text
Embedding(32064, 3072)
```

Interpretation:

```text
32,064 vocabulary tokens
×
3,072 values per token vector
```

The LM head is shown as roughly:

```text
Linear(
    in_features=3072,
    out_features=32064
)
```

This reveals a beautiful symmetry:

```text
internal model vector
      3072 values
          ↓
       LM head
          ↓
one score for every token
      32064 scores
```

The internal representation width is often called the model dimension.

---

## 4. The LM head: from hidden vector to next-token scores

The Transformer stack produces learned representations.

But a generative model needs to answer:

> Which vocabulary token should come next?

The LM head bridges those two spaces.

Suppose the final hidden representation of the current position is:

```text
h = [3072 values]
```

The LM head maps that to something like:

```text
[token_0_score,
 token_1_score,
 token_2_score,
 ...
 token_32063_score]
```

The output has one value associated with each known vocabulary token.

### The chapter's code path

Tokenize:

```python
prompt = "The capital of France is"

input_ids = tokenizer(
    prompt,
    return_tensors="pt"
).input_ids

input_ids = input_ids.to("cuda")
```

Run only the underlying Transformer model:

```python
model_output = model.model(input_ids)
```

Then apply the LM head:

```python
lm_head_output = model.lm_head(model_output[0])
```

The chapter reports an output shape:

```text
[1, 6, 32064]
```

Let's decode that shape.

```text
1      = one sequence in the batch
6      = six token positions
32064  = one vocabulary score per token position
```

To predict the **next** token, we care about the final sequence position:

```python
lm_head_output[0, -1]
```

Interpretation:

```text
batch item 0
last token position
all 32,064 vocabulary scores
```

Then:

```python
token_id = lm_head_output[0, -1].argmax(-1)
```

returns the ID with the highest score.

Decoding:

```python
tokenizer.decode(token_id)
```

produces:

```text
Paris
```

for the chapter's example.

### A subtle but important detail

The chapter loosely describes these outputs as probability scores.

In practice for this code path, the LM head produces model scores before the final selection machinery. For the learning goal here, the important idea is:

```text
hidden state
→ vocabulary-wide scores
→ decoding strategy
→ chosen token
```

The lesson does not require you to derive the mathematical transformation yet.

[[IMAGE_NEEDED: LM head vocabulary scoring | Show one final hidden vector entering the LM head and expanding into a ranked list of candidate vocabulary tokens with scores, with “Paris” highlighted as the chosen candidate | Learner should notice the dimensional jump from one hidden vector to one score per vocabulary entry]]

---

## 5. Model scoring is not the same as token selection

The neural network produces scores for possible next tokens.

Another step chooses which token actually becomes output.

That decision process is the **decoding strategy**.

### Greedy decoding

The simplest strategy is:

```text
always choose the highest-scoring token
```

Example:

```text
Dear       40%
Hello      24%
Hi         16%
Greetings   9%
...
```

Greedy decoding chooses:

```text
Dear
```

because it has the highest score.

### Sampling

Another possibility is to sample based on the distribution.

Then `Dear` may have the greatest chance of selection, but it is not absolutely guaranteed to be selected.

This allows variation among plausible candidates.

The chapter introduces this distinction now and leaves a deeper exploration of generation controls such as temperature to a later chapter.

### Why this distinction matters

The model and decoding algorithm are not exactly the same thing.

Conceptually:

```text
MODEL
"What tokens look plausible?"
        ↓
DECODER
"Which plausible token should we actually emit?"
```

This helps explain why the same model can behave differently under different generation settings.

---

## 6. Token streams, parallel processing, and context length

One reason Transformers became so important is that their architecture supports substantial parallel processing of sequence positions compared with earlier recurrent approaches.

A useful first mental model is to imagine one processing stream per token position:

```text
token 1 → processing stream 1
token 2 → processing stream 2
token 3 → processing stream 3
...
token N → processing stream N
```

These streams are **not independent** because attention lets positions exchange information.

But the parallel-stream picture is useful for understanding tensor shapes and context limits.

[[IMAGE_NEEDED: Parallel token processing streams | Show several input token embeddings entering parallel vertical streams through the same stack of Transformer blocks, with attention links connecting token positions | Learner should notice both parallel per-position processing and the cross-position interaction introduced by attention]]

### Context length

A model can only process up to a certain number of token positions at once.

That maximum is its **context length**.

If a model has a 4K context limit, then the model cannot simultaneously process an arbitrarily long token sequence beyond that limit.

Context length therefore constrains how much tokenized information can be present in one model context.

Remember from Chapter 2:

```text
characters ≠ words ≠ tokens
```

So the amount of human-readable text that fits depends partly on tokenization.

### Hidden-state shape

For the chapter's six-token example, the Transformer stack output has shape:

```text
[1, 6, 3072]
```

Interpretation:

```text
1      batch item
6      token positions
3072   hidden values per token position
```

After the LM head:

```text
[1, 6, 32064]
```

Interpretation:

```text
1      batch item
6      token positions
32064  vocabulary scores per position
```

This transformation is worth memorizing conceptually:

```text
[batch, sequence, hidden_size]
              ↓ LM head
[batch, sequence, vocabulary_size]
```

### Why only the last position selects the next generated token

For next-token generation, the model needs the prediction corresponding to the end of the current sequence.

So the final position's hidden vector becomes the relevant LM-head input for choosing the next token.

However, the earlier token positions were not wasted.

Their representations contribute contextual information through attention.

That is why the final token's representation can encode information from earlier tokens.

---

{{exercise:M03.L01.EX01}}

---

## 7. Why generation would waste work without caching

Return to autoregressive generation.

Suppose the prompt token sequence is:

```text
A B C D
```

The model computes representations and predicts:

```text
E
```

The next sequence is:

```text
A B C D E
```

A naive implementation could recompute everything for:

```text
A B C D
```

again, even though those tokens were already processed.

Then after generating `F`, it could recompute:

```text
A B C D E
```

again.

This repeats a lot of work.

### The key/value cache

Attention calculations use objects called:

```text
queries
keys
values
```

which we will explain later.

During generation, the model can cache previously computed **keys and values** so that earlier attention computations do not need to be recreated from scratch at every step.

This optimization is called the:

```text
KV cache
```

The high-level intuition is:

```text
WITHOUT CACHE

step 1:
A B C D → compute

step 2:
A B C D E → recompute much of A B C D

step 3:
A B C D E F → recompute much of A B C D E
```

versus:

```text
WITH KV CACHE

step 1:
compute A B C D
store useful K/V results

step 2:
reuse cached A B C D
compute new position E

step 3:
reuse cached history
compute new position F
```

[[IMAGE_NEEDED: KV cache generation comparison | Side-by-side diagram of generation without cache repeatedly recalculating all previous token streams versus generation with cached keys/values where only the new token stream requires fresh computation | Learner should notice that caching avoids duplicated attention work for previous positions]]

### Chapter timing example

The chapter times generation of 100 tokens on a Colab T4 GPU.

With:

```python
use_cache=True
```

the reported example takes about:

```text
4.5 seconds
```

Without cache:

```python
use_cache=False
```

the reported example takes about:

```text
21.8 seconds
```

These values are specific to the chapter's environment and example, not universal performance guarantees.

The lesson is the size of the difference:

> Reusing previous attention results can dramatically reduce repeated work during autoregressive generation.

### Why APIs often stream tokens

Even optimized generation is sequential.

Users may not want to wait until the entire response is finished.

So systems often display tokens as they are generated.

That improves perceived responsiveness even though the model is still producing the response token by token.

---

## 8. Inside a Transformer block

Most of the model's repeated computation happens in a stack of Transformer blocks.

A simplified block contains two central computational components:

```text
1. Self-attention
2. Feedforward neural network / MLP
```

A useful mental model is:

```text
ATTENTION
"What information from the sequence matters here?"
        ↓
FEEDFORWARD NETWORK
"How should this representation be transformed?"
```

Each block passes its output to the next block.

So if the model has 32 blocks:

```text
block 1
  ↓
block 2
  ↓
block 3
  ↓
...
block 32
```

[[IMAGE_NEEDED: Simplified Transformer block | Show input vectors entering self-attention, then a feedforward/MLP stage, then output vectors continuing to the next Transformer block | Learner should remember attention as contextual information mixing and the feedforward network as per-position transformation/processing]]

### Feedforward network intuition

The chapter gives a simple example:

```text
"The Shawshank"
```

A well-trained language model may strongly associate that sequence with:

```text
"Redemption"
```

The feedforward components across model layers contribute to the learned information and behaviors that make such predictions possible.

However, the chapter also warns against thinking of an LLM as merely a giant database.

A useful model must do more than memorize exact training fragments.

It also has to generalize to inputs and combinations that were not seen in precisely the same form.

So a better intuition is:

```text
learned information
+
learned patterns
+
transformations that support generalization
```

rather than:

```text
lookup database of stored sentences
```

---

## 9. Attention: bringing relevant context into a token representation

Language depends heavily on context.

Consider:

```text
The dog chased the squirrel because it ...
```

What does:

```text
it
```

refer to?

The correct interpretation depends on context.

A model cannot understand such relationships by treating each token as isolated.

Self-attention gives a token position a mechanism for incorporating information from other relevant positions in the sequence.

### The simplest attention intuition

When processing a current token position:

```text
1. Score how relevant other allowed positions are.
2. Combine information from those positions according to those scores.
```

That is the heart of attention.

[[IMAGE_NEEDED: Attention intuition with pronoun reference | Show “The dog chased the squirrel because it” with the current token “it” highlighted and attention links of different strengths to earlier words, especially dog and squirrel | Learner should notice that attention lets the current representation incorporate information from relevant earlier positions]]

The chapter summarizes attention in exactly two conceptual steps:

```text
Step 1:
relevance scoring

Step 2:
information combination
```

Everything involving queries, keys, and values is machinery that enables these two operations.

---

## 10. Query, key, and value: the least mysterious explanation

The terms **query**, **key**, and **value** can sound more complicated than the underlying idea.

Let's use a retrieval analogy.

Imagine the current token position is asking:

```text
"What previous information is relevant to me?"
```

The **query** represents what the current position is looking for.

Each previous position has a **key** that participates in deciding whether that position is relevant.

Each previous position also has a **value**, representing the information that can be brought into the new representation.

Conceptually:

```text
QUERY
What am I looking for?

KEY
How relevant is this position to that query?

VALUE
What information should I take from this position?
```

This analogy is imperfect, but it gives you a usable mental model.

### Where Q, K, and V come from

The attention layer receives input vectors.

During training, the model learns three projection matrices:

```text
W_Q  query projection
W_K  key projection
W_V  value projection
```

The input vectors are transformed:

```text
input × W_Q → queries
input × W_K → keys
input × W_V → values
```

The important point is that Q, K, and V are not separate pieces of text.

They are different learned projections of the token representations.

[[IMAGE_NEEDED: Query-key-value projection | Show the same set of token input vectors branching through three learned projection matrices W_Q, W_K, and W_V to create query, key, and value representations | Learner should notice that Q, K, and V are different learned views of the same underlying token representations]]

---

## 11. Attention step 1: relevance scoring

Assume we are processing the current final token position.

Its query vector is compared with key vectors for the positions it is allowed to attend to.

Conceptually:

```text
current query
      ×
candidate keys
      ↓
relevance scores
```

If we simplify the idea:

```text
current token: "it"

previous positions:
"The"       → low relevance
"dog"       → some relevance
"chased"    → some relevance
"the"       → low relevance
"squirrel"  → high relevance
"because"   → low relevance
```

The raw scores are normalized with a softmax step so the attention weights form a usable distribution.

Conceptually:

```text
raw relevance scores
        ↓
      softmax
        ↓
normalized attention weights
```

The weights indicate how strongly the current position should draw from the allowed context positions.

### Why “allowed” matters

A decoder-style generative Transformer is autoregressive.

When predicting later text, it must not leak information from future positions.

So decoder attention is masked so the current position can attend only to allowed earlier positions and itself, not future positions that have not been generated yet.

This is one reason the attention pattern for generative decoders looks directional.

---

## 12. Attention step 2: combine information

After relevance weights are computed, the model uses them to combine value vectors.

Simplified:

```text
attention weight for token 1 × value 1
attention weight for token 2 × value 2
attention weight for token 3 × value 3
...
                     ↓
                    sum
                     ↓
new context-aware output vector
```

If the token `squirrel` receives a larger relevance weight for the current token `it`, then the `squirrel` value contributes more strongly to the result.

This produces a new representation that includes contextual information selected from the sequence.

So the complete simplified attention story is:

```text
QUERY + KEYS
    ↓
relevance scores
    ↓
normalized weights
    ↓
weights × VALUES
    ↓
weighted combination
    ↓
context-aware representation
```

[[IMAGE_NEEDED: Two-step attention calculation | First panel shows current query compared with keys to create relevance weights; second panel multiplies those weights by value vectors and sums them into one output vector | Learner should connect query/key interaction with scoring and values with information transfer]]

This is the core mechanism you should understand before worrying about the exact matrix equations.

---

## 13. Why attention uses multiple heads

One attention operation may learn one useful pattern.

But language can contain many relationships simultaneously.

For example, a model might need to track:

```text
pronoun reference
syntactic structure
nearby phrase relationships
longer-range dependencies
other learned patterns
```

The Transformer therefore performs several attention operations in parallel.

Each parallel attention operation is called an **attention head**.

Conceptually:

```text
input representations
       ↓
 ┌─────┼─────┐
 ↓     ↓     ↓
head 1 head 2 head 3 ...
 ↓     ↓     ↓
 └─────┼─────┘
       ↓
combine head outputs
       ↓
attention-layer output
```

Each head has learned projections that allow it to develop different attention behavior.

The chapter's key intuition is not that each head has one human-readable role.

The important point is:

> Multiple heads increase the model's capacity to capture different relationships in parallel.

[[IMAGE_NEEDED: Multi-head attention | Show one input sequence branching into several parallel attention heads, each with different attention patterns, then recombining into a single output | Learner should notice that multi-head attention repeats the same core mechanism in parallel with different learned projections]]

---

## 14. Making attention more efficient

Attention is powerful, but it is computationally expensive.

As models and context lengths grow, researchers look for ways to reduce attention cost without sacrificing too much quality.

The chapter presents several approaches.

### 14.1 Full attention

In a decoder-style full-attention pattern, a token can attend to all allowed previous positions.

Conceptually:

```text
current token
    ↓
all earlier tokens are candidates
```

This provides broad context but can be costly.

### 14.2 Local or sparse attention

Sparse/local attention restricts how many previous positions are visible to a given attention operation.

Conceptually:

```text
current token
    ↓
only a smaller neighborhood of earlier tokens
```

This can improve efficiency.

But if every layer were restricted too aggressively, the model could lose important long-range information.

The chapter describes architectures that mix broader and restricted attention patterns.

[[IMAGE_NEEDED: Full versus local attention | Show two triangular decoder-attention grids: one where each position can see all previous positions, and one where each position sees only a recent local window | Learner should notice the efficiency-versus-context tradeoff]]

### 14.3 Multi-head attention

In standard multi-head attention, each head has its own query, key, and value projections.

Conceptually:

```text
head 1 → Q1 K1 V1
head 2 → Q2 K2 V2
head 3 → Q3 K3 V3
...
```

### 14.4 Multi-query attention

Multi-query attention keeps separate query projections per head while sharing keys and values.

Conceptually:

```text
head 1 → Q1
head 2 → Q2
head 3 → Q3
             \
shared K and V
```

The chapter presents this as a way to improve inference scalability by reducing key/value matrix requirements.

### 14.5 Grouped-query attention

Grouped-query attention finds a middle ground.

Instead of:

```text
one K/V pair per head
```

or:

```text
one shared K/V pair for every head
```

it uses:

```text
several groups of heads
each group shares K/V
```

Conceptually:

```text
Heads 1–4   → shared K/V group A
Heads 5–8   → shared K/V group B
Heads 9–12  → shared K/V group C
```

The chapter describes this as trading a little of multi-query attention's efficiency for improved quality.

[[IMAGE_NEEDED: MHA vs MQA vs GQA | Three side-by-side diagrams showing multi-head attention with unique Q/K/V per head, multi-query attention with unique Q but one shared K/V set, and grouped-query attention with unique queries and several shared K/V groups | Learner should understand exactly what is being shared in each design]]

---

## 15. Flash Attention: optimize data movement, not the meaning of attention

Flash Attention is an implementation approach for making attention faster and more memory-efficient on GPUs.

The chapter's important intuition is:

> The mathematical goal of attention is preserved, but the computation is organized to use GPU memory systems more efficiently.

Modern GPUs have different memory levels.

The chapter specifically highlights movement between:

```text
SRAM
and
HBM
```

Moving data can become a major performance cost.

Flash Attention improves execution by optimizing how attention-related data is loaded, moved, and processed.

This distinction matters:

```text
Flash Attention
≠ a new semantic meaning of attention

Flash Attention
= a more efficient way to carry out attention calculations
```

[[IMAGE_NEEDED: Flash Attention memory intuition | Show a GPU diagram with slower/larger HBM and faster/smaller SRAM, comparing inefficient repeated data movement with a tiled/reuse-oriented attention computation | Learner should notice that Flash Attention targets memory movement and execution efficiency rather than changing what attention conceptually means]]

---

## 16. Modern Transformer blocks add engineering refinements

The original Transformer block established the core architecture.

Newer models retain the same major ideas but refine details.

The chapter highlights several examples.

### Normalization placement

Some newer Transformer designs normalize inputs **before** attention and feedforward processing.

This is commonly described as pre-normalization.

The chapter notes that this has been associated with reduced required training time.

### RMSNorm

The chapter highlights RMSNorm as a simpler, more efficient alternative to the LayerNorm used in the original Transformer.

You do not need its equation yet.

At this stage, the key point is that normalization remains part of the block, but implementation choices have evolved.

### Activation functions

The chapter contrasts the original Transformer's ReLU with newer variants such as SwiGLU.

Again, the lesson's goal here is architectural awareness:

```text
core Transformer idea remains
+
details continue to improve
```

### Residual connections

A more complete Transformer-block picture also includes residual paths.

These allow information to move around major sublayers rather than forcing every transformation to completely replace the incoming representation.

[[IMAGE_NEEDED: Original versus modern Transformer block | Side-by-side simplified diagrams showing the original attention + feedforward block with normalization/residual structure and a newer block with pre-normalization, RMSNorm-style labels, grouped-query attention, and modern feedforward activation | Learner should notice that the skeleton remains recognizable while important implementation details evolve]]

---

## 17. Why a Transformer needs positional information

Attention compares token representations across a sequence.

But language depends on order.

Consider:

```text
dog bites man
```

versus:

```text
man bites dog
```

The same words appear, but the meaning changes because their positions change.

The model therefore needs information about token order.

### Earlier positional approaches

The chapter describes original Transformer approaches using absolute positional information.

Conceptually:

```text
first token  → position 1
second token → position 2
third token  → position 3
...
```

This positional signal may be fixed or learned depending on the design.

### Why training efficiency complicates position

Training examples can have very different lengths.

It would be inefficient to waste most of a long context window on padding for every short document.

A common idea is therefore to pack multiple shorter documents into one training context.

Conceptually:

```text
| doc A | doc B | doc C | padding |
```

This creates practical challenges for positional schemes because each document is semantically separate even if it shares the same packed training context.

[[IMAGE_NEEDED: Sequence packing | Show several short documents packed into one fixed-length training context with boundaries between documents and little padding at the end | Learner should notice why packing improves space utilization and why position handling must respect document boundaries]]

---

## 18. Rotary positional embeddings (RoPE)

The chapter highlights **Rotary Positional Embeddings**, or **RoPE**, as an important modern positional method.

The core lesson-level intuition is:

> RoPE mixes positional information into the attention process by transforming query and key representations according to token position.

Instead of thinking of position as merely another vector added once at the beginning, the chapter emphasizes that rotary positional information enters during attention.

Conceptually:

```text
token representations
        ↓
Q and K projections
        ↓
apply positional rotation
        ↓
position-aware Q and K
        ↓
relevance scoring
```

[[IMAGE_NEEDED: RoPE placement in attention | Show query and key projections followed by a rotary positional transformation before Q×K relevance scoring; values remain on the information-combination path | Learner should notice that RoPE injects position into Q and K immediately before attention relevance scoring]]

### Why "rotary"?

The method is based on rotating vector components in embedding space according to position.

You do not need to perform the mathematical rotation in this lesson.

The key architectural understanding is enough:

```text
RoPE helps attention know where tokens are
and how positions relate
```

Position is indispensable because the sequence order itself contains information.

---

## 19. Put the entire next-token step together

Now we can build the complete mental model.

Suppose the prompt is:

```text
The capital of France is
```

### Step 1 — Tokenize

```text
visible text
    ↓
tokenizer
    ↓
token IDs
```

### Step 2 — Retrieve token embeddings

Each token ID selects its learned input vector.

```text
token ID
    ↓
embedding lookup
    ↓
token vector
```

### Step 3 — Add/use positional information

The model needs to know where each token occurs in the sequence.

In a modern RoPE-style architecture, positional information participates in the attention computation through queries and keys.

### Step 4 — Enter Transformer block 1

Attention asks:

```text
Which previous token information matters for this position?
```

Then the feedforward network transforms the representation.

Normalization and residual structures help organize the block.

### Step 5 — Repeat through the entire Transformer stack

```text
block 1
→ block 2
→ block 3
→ ...
→ final block
```

Representations become progressively transformed.

### Step 6 — Take the last position's final hidden representation

Conceptually:

```text
[3072 values]
```

for the chapter's model.

### Step 7 — LM head maps that vector to vocabulary scores

Conceptually:

```text
[3072]
   ↓
LM head
   ↓
[32064 scores]
```

### Step 8 — Decode/select one token

A decoding strategy chooses the actual output token.

For the example:

```text
Paris
```

### Step 9 — Append it

The sequence becomes:

```text
The capital of France is Paris
```

### Step 10 — Repeat for the following token

KV caching can reuse prior attention keys and values instead of recomputing all earlier work.

This continues until a stopping condition is reached.

[[IMAGE_NEEDED: Complete next-token generation pipeline | A detailed left-to-right or top-to-bottom diagram showing text → tokenizer → IDs → embeddings → positional handling → repeated Transformer blocks containing attention and MLP → last hidden vector → LM head → vocabulary scores → decoding → selected token → append to context → repeat, with KV cache shown beside attention | Learner should be able to use this figure as the final mental model for the entire chapter]]

---

{{exercise:M03.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> The LLM writes the entire response in one neural-network pass.

### Why this is wrong

Generative LLMs normally generate one token at a time. Each newly generated token becomes part of the sequence used for later generation.

---

### Misconception 2

> The Transformer stack directly outputs the final word.

### Why this is wrong

The Transformer stack produces hidden representations. The LM head maps those representations into vocabulary-wide scores, and a decoding strategy chooses an output token.

---

### Misconception 3

> Only the final input token matters because only its output is used to choose the next token.

### Why this is wrong

Earlier positions contribute contextual information through attention. Their final outputs may not directly choose the next generated token, but intermediate representations from previous positions are essential to the current position's computation.

---

### Misconception 4

> The KV cache stores the generated English text.

### Why this is wrong

The visible text/tokens are still part of the sequence, but the KV cache specifically reuses previously calculated key/value representations inside attention so the model can avoid repeating expensive work.

---

### Misconception 5

> Attention is just a database lookup.

### Why this is wrong

Attention computes learned relevance scores between projected representations and forms a weighted combination of value vectors. The relationships emerge from trained model parameters.

---

### Misconception 6

> Query, key, and value correspond to three different sentences.

### Why this is wrong

They are learned projections of input representations used for different roles inside attention.

---

### Misconception 7

> Multi-head attention means the model generates several answers and votes.

### Why this is wrong

Multiple attention heads perform attention calculations in parallel inside a layer. Their results are combined to form the layer's representation.

---

### Misconception 8

> Flash Attention is a different semantic attention mechanism that changes what the model pays attention to.

### Why this is wrong

In the chapter, Flash Attention is introduced as an implementation optimization that makes attention computation more efficient on GPU memory systems.

---

### Misconception 9

> Positional information is optional because the tokens already contain their order.

### Why this is wrong

Token embeddings themselves do not automatically encode the token's sequence position. Transformer architectures need positional information so order can affect processing.

---

## Key terminology

| Term | Meaning |
|---|---|
| Autoregressive model | Model whose earlier generated outputs become part of the input used for later predictions |
| Forward pass | One flow of input through the neural network's computation to produce outputs |
| Transformer block | Repeated neural-network unit containing attention and feedforward processing plus supporting operations |
| LM head | Output layer that maps a hidden representation into vocabulary-wide next-token scores |
| Hidden state | Internal vector representation produced by the model for a token position |
| Decoding strategy | Rule/process used to choose an actual output token from model scores |
| Greedy decoding | Always selecting the highest-scoring next token |
| Sampling | Selecting among candidate tokens according to a probability distribution rather than always taking the top one |
| Context length | Maximum number of token positions the model can process in one context |
| KV cache | Cached attention key/value representations from earlier tokens used to avoid redundant generation computation |
| Self-attention | Mechanism that lets a token position incorporate information from other allowed positions in the same sequence |
| Query | Learned projection representing what a token position uses for relevance matching |
| Key | Learned projection used to determine a position's relevance to a query |
| Value | Learned projection carrying information that can be combined into the attention output |
| Attention weight | Normalized relevance value determining how strongly a position contributes |
| Attention head | One parallel instance of the attention calculation with its own learned projections |
| Multi-head attention | Several attention heads computed in parallel and then combined |
| Sparse/local attention | Attention pattern that restricts each position to a subset of context positions |
| Multi-query attention | Attention variant where heads keep distinct queries while sharing keys and values |
| Grouped-query attention | Attention variant where groups of heads share key/value representations |
| Flash Attention | GPU-efficient implementation approach that reduces costly memory movement during attention |
| Feedforward network / MLP | Per-position neural-network transformation inside a Transformer block |
| Residual connection | Path that carries information around a sublayer and combines it with the transformed result |
| RMSNorm | Normalization variant highlighted in the chapter as a modern Transformer refinement |
| RoPE | Rotary positional embeddings, a positional method applied to query/key representations before relevance scoring |
| Sequence packing | Efficiently placing multiple short training documents into a larger fixed-size context |

---

## Self-check

Before moving on, make sure you can answer these:

1. Why is a text-generation LLM called autoregressive?
2. What are the three major components of the chapter's high-level LLM pipeline?
3. What does the Transformer stack output before the LM head?
4. What does the LM head output?
5. Why do we select from the final sequence position when generating the next token?
6. What is the difference between model scoring and decoding?
7. What does `[1, 6, 3072]` represent in the chapter's example?
8. Why are previous token positions still important even when only the last position predicts the next token?
9. What repeated work does a KV cache reduce?
10. What are the two major components of a simplified Transformer block?
11. What are the two conceptual steps of attention?
12. What is the intuitive role of a query?
13. What is the intuitive role of a key?
14. What is the intuitive role of a value?
15. Why do Transformers use multiple attention heads?
16. How does local attention differ from full attention?
17. What does multi-query attention share?
18. How does grouped-query attention differ from multi-query attention?
19. What does Flash Attention optimize?
20. Why does a model need positional information?
21. Where does the chapter place RoPE within the attention process?
22. Trace the complete process from prompt text to one newly generated token.

---

## Retain this idea

**A generative Transformer LLM is best understood as a repeated next-token prediction machine. The tokenizer creates token IDs, embeddings turn them into vectors, stacked Transformer blocks repeatedly mix contextual information through attention and transform representations through feedforward networks, the LM head converts the final position into vocabulary-wide scores, and a decoding strategy selects one token. That token is appended to the context, cached attention state is reused where possible, and the entire generation cycle continues.**
"""
        ),

        "estimated_minutes": 150,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "generation-loop",
                "title": "The first big idea: an LLM writes one token at a time",
                "order": 1,
            },
            {
                "id": "first-generation",
                "title": "Loading a generative model",
                "order": 2,
            },
            {
                "id": "forward-pass",
                "title": "What happens in one forward pass?",
                "order": 3,
            },
            {
                "id": "lm-head",
                "title": "The LM head: from hidden vector to next-token scores",
                "order": 4,
            },
            {
                "id": "decoding",
                "title": "Model scoring is not the same as token selection",
                "order": 5,
            },
            {
                "id": "parallel-context",
                "title": "Token streams, parallel processing, and context length",
                "order": 6,
            },
            {
                "id": "kv-cache",
                "title": "Why generation would waste work without caching",
                "order": 7,
            },
            {
                "id": "transformer-block",
                "title": "Inside a Transformer block",
                "order": 8,
            },
            {
                "id": "attention-intuition",
                "title": "Attention: bringing relevant context into a token representation",
                "order": 9,
            },
            {
                "id": "qkv",
                "title": "Query, key, and value: the least mysterious explanation",
                "order": 10,
            },
            {
                "id": "attention-score",
                "title": "Attention step 1: relevance scoring",
                "order": 11,
            },
            {
                "id": "attention-combine",
                "title": "Attention step 2: combine information",
                "order": 12,
            },
            {
                "id": "multi-head",
                "title": "Why attention uses multiple heads",
                "order": 13,
            },
            {
                "id": "efficient-attention",
                "title": "Making attention more efficient",
                "order": 14,
            },
            {
                "id": "flash-attention",
                "title": "Flash Attention: optimize data movement, not the meaning of attention",
                "order": 15,
            },
            {
                "id": "modern-block",
                "title": "Modern Transformer blocks add engineering refinements",
                "order": 16,
            },
            {
                "id": "position",
                "title": "Why a Transformer needs positional information",
                "order": 17,
            },
            {
                "id": "rope",
                "title": "Rotary positional embeddings (RoPE)",
                "order": 18,
            },
            {
                "id": "full-pass",
                "title": "Put the entire next-token step together",
                "order": 19,
            },
            {
                "id": "misconceptions",
                "title": "Important misconceptions",
                "order": 20,
            },
            {
                "id": "terminology",
                "title": "Key terminology",
                "order": 21,
            },
            {
                "id": "self-check",
                "title": "Self-check",
                "order": 22,
            },
            {
                "id": "retain",
                "title": "Retain this idea",
                "order": 23,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M03.L01.EX01",

            "title": "Trace One Next-Token Forward Pass",

            "lesson_code": "M03.L01",

            "section_id": "parallel-context",

            "placement": "after_section",

            "description": (
                "Inspect the hidden-state and LM-head shapes of a short prompt, "
                "then connect each tensor dimension to the architecture."
            ),

            "instructions": (
                "Using the Phi-3 example from the lesson or the same conceptual "
                "workflow with an available causal language model:\n"
                "1. Tokenize the prompt `The capital of France is`.\n"
                "2. Print the number of token IDs produced.\n"
                "3. Run the underlying Transformer model without asking generate() "
                "to produce a full response.\n"
                "4. Print the hidden-state tensor shape.\n"
                "5. Pass the hidden states through the LM head and print its shape.\n"
                "6. Select the final sequence position.\n"
                "7. Find the highest-scoring token ID for that position.\n"
                "8. Decode that token ID.\n"
                "9. Explain what the batch, sequence, hidden-size, and vocabulary-size "
                "dimensions mean.\n"
                "10. Write one paragraph explaining why this is only one step in "
                "autoregressive generation rather than a complete answer."
            ),

            "expected_output": (
                "A notebook or script showing token IDs, tensor shapes, the selected "
                "next-token ID and decoded token, plus a written explanation of each "
                "dimension and the forward-pass flow."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "forward-pass",
                "tensor-shape-interpretation",
                "lm-head",
                "next-token-selection",
                "autoregressive-reasoning",
            ],
        },

        {
            "id": "M03.L01.EX02",

            "title": "Explain Attention and Generation as an Engineer",

            "lesson_code": "M03.L01",

            "section_id": "full-pass",

            "placement": "after_section",

            "description": (
                "Consolidate the chapter by reasoning through attention, caching, "
                "and the complete generation loop."
            ),

            "instructions": (
                "Consider the prompt: `Sarah fed the cat because it`.\n"
                "1. Identify the current token position being processed for next-token "
                "prediction.\n"
                "2. Explain in plain language what the query for that position is trying "
                "to accomplish.\n"
                "3. Explain how keys participate in relevance scoring.\n"
                "4. Explain how values contribute information after relevance weights "
                "are known.\n"
                "5. Draw or write a tiny hypothetical attention-weight table over the "
                "previous words. The numbers do not need to come from a real model, but "
                "they must sum to 1 and should illustrate the mechanism rather than claim "
                "to be actual model weights.\n"
                "6. Explain why future positions must not be visible to a decoder model "
                "during autoregressive generation.\n"
                "7. Explain what would be recomputed at the next generation step without "
                "a KV cache and what the cache allows the model to reuse.\n"
                "8. Compare standard multi-head attention, multi-query attention, and "
                "grouped-query attention in terms of what happens to key/value sharing.\n"
                "9. Explain where RoPE enters the attention path.\n"
                "10. Finish by writing the complete pipeline from visible prompt to "
                "selected next token in 8–12 ordered steps."
            ),

            "expected_output": (
                "A structured written analysis containing an illustrative attention "
                "table, explanations of Q/K/V and causal masking, a KV-cache explanation, "
                "a comparison of MHA/MQA/GQA, RoPE placement, and a complete generation "
                "pipeline."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "attention-intuition",
                "query-key-value",
                "causal-attention",
                "kv-cache",
                "grouped-query-attention",
                "rope",
                "systems-thinking",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M03.L01.QZ01",

        "title": "Looking Inside Large Language Models — Knowledge Check",

        "lesson_code": "M03.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M03.L01.Q01",

                "section_id": "generation-loop",

                "question": (
                    "Why are generative Transformer LLMs described as autoregressive?"
                ),

                "options": [
                    "They generate all output tokens simultaneously and then reorder them.",
                    "They use their earlier generated tokens as part of the context for generating later tokens.",
                    "They can only process numerical datasets.",
                    "They always choose the highest-scoring token.",
                ],

                "correct": 1,

                "explanation": (
                    "Autoregressive generation means each generated token becomes "
                    "part of the sequence used to predict subsequent tokens."
                ),
            },

            {
                "id": "M03.L01.Q02",

                "section_id": "forward-pass",

                "question": (
                    "Which ordering best matches the chapter's high-level forward-pass architecture?"
                ),

                "options": [
                    "LM head → tokenizer → Transformer blocks",
                    "Tokenizer → Transformer blocks → LM head",
                    "Transformer blocks → tokenizer → embedding matrix",
                    "Tokenizer → LM head → Transformer blocks",
                ],

                "correct": 1,

                "explanation": (
                    "The tokenizer prepares token IDs, Transformer blocks process "
                    "their representations, and the LM head maps the final hidden "
                    "representations into vocabulary-wide output scores."
                ),
            },

            {
                "id": "M03.L01.Q03",

                "section_id": "lm-head",

                "question": (
                    "In the chapter's Phi-3 example, what is the purpose of the LM head?"
                ),

                "options": [
                    "To split raw text into tokens",
                    "To store the model's KV cache",
                    "To map a hidden representation into one score for each vocabulary token",
                    "To reduce the context length to one token",
                ],

                "correct": 2,

                "explanation": (
                    "The LM head projects the hidden model representation into the "
                    "vocabulary dimension so next-token candidates can be scored."
                ),
            },

            {
                "id": "M03.L01.Q04",

                "section_id": "decoding",

                "question": "What does greedy decoding do?",

                "options": [
                    "Always chooses the highest-scoring next token.",
                    "Always selects a random token.",
                    "Uses only the first token in the prompt.",
                    "Removes the LM head from generation.",
                ],

                "correct": 0,

                "explanation": (
                    "Greedy decoding selects the top-scoring candidate at each step "
                    "rather than sampling among multiple candidates."
                ),
            },

            {
                "id": "M03.L01.Q05",

                "section_id": "parallel-context",

                "question": (
                    "What does the tensor shape [1, 6, 3072] represent in the chapter's example?"
                ),

                "options": [
                    "One model, six layers, and 3,072 GPUs",
                    "One batch item, six token positions, and a 3,072-value hidden representation per position",
                    "One tokenizer, six vocabularies, and 3,072 special tokens",
                    "One token, six probability scores, and 3,072 context windows",
                ],

                "correct": 1,

                "explanation": (
                    "The axes correspond to batch size, sequence length, and hidden/model dimension."
                ),
            },

            {
                "id": "M03.L01.Q06",

                "section_id": "kv-cache",

                "question": (
                    "What is the main reason to use a KV cache during autoregressive generation?"
                ),

                "options": [
                    "To change the tokenizer vocabulary during every generation step",
                    "To avoid repeatedly recalculating attention key/value results for earlier tokens",
                    "To guarantee factual correctness",
                    "To force the model to use greedy decoding",
                ],

                "correct": 1,

                "explanation": (
                    "Caching previous attention keys and values lets later generation "
                    "steps reuse earlier computation instead of repeating it."
                ),
            },

            {
                "id": "M03.L01.Q07",

                "section_id": "transformer-block",

                "question": (
                    "Which two components form the simplified core of a Transformer block in this chapter?"
                ),

                "options": [
                    "Tokenizer and decoder",
                    "Embedding table and vocabulary",
                    "Attention layer and feedforward neural network",
                    "Sampler and API",
                ],

                "correct": 2,

                "explanation": (
                    "The chapter presents self-attention and the feedforward/MLP "
                    "stage as the two major computational components of the block."
                ),
            },

            {
                "id": "M03.L01.Q08",

                "section_id": "attention-intuition",

                "question": (
                    "What are the two major conceptual steps of attention?"
                ),

                "options": [
                    "Tokenization and detokenization",
                    "Relevance scoring and combining information",
                    "Training and deployment",
                    "Sampling and stopping",
                ],

                "correct": 1,

                "explanation": (
                    "Attention first determines how relevant allowed positions are "
                    "and then combines their information according to those weights."
                ),
            },

            {
                "id": "M03.L01.Q09",

                "section_id": "qkv",

                "question": (
                    "Which description best matches the relationship among queries, keys, and values?"
                ),

                "options": [
                    "They are three unrelated input documents.",
                    "They are learned projections of token representations used for relevance scoring and information transfer.",
                    "They are three different tokenizers.",
                    "They are only used after the model has finished generating.",
                ],

                "correct": 1,

                "explanation": (
                    "Q, K, and V come from learned projections of the model's input "
                    "representations and serve different roles inside self-attention."
                ),
            },

            {
                "id": "M03.L01.Q10",

                "section_id": "multi-head",

                "question": "Why does a Transformer use multiple attention heads?",

                "options": [
                    "To create several complete answers and vote on one",
                    "To increase its capacity to model different attention relationships in parallel",
                    "To eliminate the need for embeddings",
                    "To make future tokens visible",
                ],

                "correct": 1,

                "explanation": (
                    "Multiple heads perform parallel attention operations with "
                    "different learned projections, increasing representational capacity."
                ),
            },

            {
                "id": "M03.L01.Q11",

                "section_id": "efficient-attention",

                "question": (
                    "How does grouped-query attention differ from multi-query attention?"
                ),

                "options": [
                    "Grouped-query attention removes queries completely.",
                    "Grouped-query attention allows several groups of heads to share key/value representations rather than making every head share one global K/V set.",
                    "Grouped-query attention always performs full bidirectional attention.",
                    "Grouped-query attention replaces attention with an MLP.",
                ],

                "correct": 1,

                "explanation": (
                    "Multi-query attention shares one K/V set broadly, while grouped-query "
                    "attention uses multiple shared K/V groups as a quality-efficiency compromise."
                ),
            },

            {
                "id": "M03.L01.Q12",

                "section_id": "flash-attention",

                "question": (
                    "What does Flash Attention primarily optimize in the chapter's explanation?"
                ),

                "options": [
                    "The English vocabulary",
                    "The tokenizer's capitalization rules",
                    "How attention computation uses and moves data through GPU memory",
                    "The number of documents in the training dataset",
                ],

                "correct": 2,

                "explanation": (
                    "Flash Attention is introduced as an execution optimization that "
                    "reduces inefficient movement between GPU memory systems."
                ),
            },

            {
                "id": "M03.L01.Q13",

                "section_id": "rope",

                "question": (
                    "Where does the chapter place rotary positional information in a RoPE-style attention path?"
                ),

                "options": [
                    "Only after the LM head",
                    "Into query and key representations before relevance scoring",
                    "Only inside the tokenizer",
                    "After generation is complete",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter explains RoPE as incorporating positional information "
                    "into queries and keys just before attention relevance scoring."
                ),
            },

            {
                "id": "M03.L01.Q14",

                "section_id": "full-pass",

                "type": "open",

                "question": (
                    "Explain one complete next-token generation step, starting with "
                    "visible prompt text and ending with a selected output token. "
                    "Your explanation must include tokenization, embeddings, Transformer "
                    "blocks, attention, the final hidden representation, the LM head, "
                    "decoding, and how KV caching helps on the following step."
                ),
            },
        ],

        "passing_score": 70,
    },
}
