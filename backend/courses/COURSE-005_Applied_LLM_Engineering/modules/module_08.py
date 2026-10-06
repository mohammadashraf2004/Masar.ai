"""M08.L01 — Semantic Search and Retrieval-Augmented Generation.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 8; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M08.L01"

MODULE_ORDER = 8

MODULE_TITLE = "Semantic Search and Retrieval-Augmented Generation"

MODULE_DESCRIPTION = (
    "Learn how modern language models improve search through dense retrieval and "
    "reranking, then extend search into retrieval-augmented generation (RAG). "
    "Explore chunking, vector indexes, hybrid search, retrieval evaluation, "
    "grounded generation, advanced RAG patterns, and RAG evaluation."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Semantic Search and Retrieval-Augmented Generation",

    "slug": "llm-foundations-m08-l01",

    "description": (
        "A practical, beginner-friendly guide to semantic search and RAG: dense "
        "retrieval with embeddings, chunking and vector indexing, lexical versus "
        "semantic search, reranking, search evaluation, grounded generation, "
        "local RAG pipelines, and advanced RAG patterns such as query rewriting, "
        "multi-query, multi-hop, routing, and agentic retrieval."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.25,

    "skill_tags": [
        "semantic-search",
        "dense-retrieval",
        "embeddings",
        "vector-search",
        "faiss",
        "bm25",
        "hybrid-search",
        "reranking",
        "cross-encoder",
        "map",
        "ndcg",
        "rag",
        "grounded-generation",
        "chunking",
        "query-rewriting",
        "multi-query-rag",
        "multi-hop-rag",
        "query-routing",
        "agentic-rag",
        "rag-evaluation",
        "module-08",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M02.L01",
        "M03.L01",
        "M04.L01",
        "M05.L01",
        "M06.L01",
        "M07.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Semantic Search and Retrieval-Augmented Generation",

        "content": (
            r"""
# Semantic Search and Retrieval-Augmented Generation

> **Course:** Large Language Models Foundations  
> **Lesson:** M08.L01  
> **Module:** Semantic Search and Retrieval-Augmented Generation  
> **Source alignment:** Chapter 8, “Semantic Search and Retrieval-Augmented Generation.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the difference between **keyword search** and **semantic search**.
- Describe the chapter’s three major search-system components:
  **dense retrieval, reranking, and RAG**.
- Explain how embeddings turn retrieval into a nearest-neighbor search problem.
- Build the mental model of:
  **documents → chunks → embeddings → index → query embedding → nearest neighbors**.
- Explain why search systems often apply a relevance threshold.
- Explain why query/document embedding models may need retrieval-specific training.
- Compare lexical BM25 search with dense retrieval.
- Explain why **hybrid search** combines complementary strengths.
- Explain why long documents are usually split into chunks.
- Compare one-vector-per-document and multiple-vectors-per-document indexing.
- Explain the role of overlap, titles, paragraphs, and surrounding context in chunk design.
- Distinguish exact nearest-neighbor search, approximate nearest-neighbor libraries, and vector databases.
- Explain the purpose of retrieval-model fine-tuning with positive and negative query-document pairs.
- Explain why reranking is normally a **second-stage** operation.
- Describe a cross-encoder reranker conceptually.
- Explain precision at rank, average precision, and mean average precision.
- Explain why nDCG is useful when relevance is graded rather than binary.
- Define RAG as **retrieval followed by grounded generation**.
- Explain how retrieved context reduces reliance on model-only memory.
- Build a basic local RAG mental model with an embedding model, vector store, retriever, prompt, and generator.
- Explain advanced RAG patterns:
  query rewriting, multi-query, multi-hop, query routing, and agentic RAG.
- Explain the chapter’s RAG evaluation dimensions:
  fluency, perceived utility, citation recall, citation precision, faithfulness, and answer relevance.
- Distinguish retrieval quality from generation quality.

---

## 1. Why language models changed search

Traditional search often relies heavily on the words that appear in the query and documents.

But humans do not always express the same meaning with the same words.

For example:

```text
Query:
how precise was the science
```

A highly relevant passage might say:

```text
praised for its scientific accuracy
```

The words are different, but the meaning is closely related.

This is the core idea of **semantic search**:

> Search by meaning, not only by exact word overlap.

The chapter explains that language models improved mature search systems because they can create contextual representations that capture more than raw keywords.

[[IMAGE_NEEDED: Keyword search versus semantic search | Show the same query entering two pipelines: keyword search matching shared words and semantic search matching a differently worded but meaning-equivalent passage | Learner should notice that semantic relevance does not require exact query terms]]

---

## 2. Why search became important for text generation too

Generative models can answer questions fluently.

But fluency is not the same as factual accuracy.

The chapter highlights a common problem:

```text
model answers confidently
but
the answer may be wrong or outdated
```

One response to this problem is to retrieve relevant information first and provide it to the generator.

That leads to **Retrieval-Augmented Generation**, or:

```text
RAG
```

The idea is simple:

```text
Question
   ↓
Search / retrieval
   ↓
Relevant evidence
   ↓
LLM
   ↓
Grounded answer
```

RAG is especially useful when you want the model to answer from:

- a specific knowledge base,
- internal company data,
- a book,
- product documentation,
- a changing external dataset.

[[IMAGE_NEEDED: Basic RAG motivation | Show a question going first to search, retrieved evidence entering the LLM together with the question, and the LLM producing an answer with source references | Learner should understand that retrieval supplies evidence before generation]]

---

## 3. Three major components: retrieval, reranking, and RAG

The chapter organizes modern semantic-search systems into three major categories.

### Dense retrieval

```text
query
→ embedding
→ nearest documents in embedding space
```

### Reranking

```text
query
+
candidate search results
→ relevance model
→ reorder candidates
```

### RAG

```text
query
→ retrieve evidence
→ generate answer using evidence
```

These components can be combined in one pipeline:

```text
Query
  ↓
First-stage retrieval
  ↓
Candidate results
  ↓
Reranker
  ↓
Best evidence
  ↓
Generative model
  ↓
Grounded answer
```

[[IMAGE_NEEDED: Retrieval reranking RAG stack | Show a three-stage pipeline with dense/lexical retrieval producing candidates, reranker reordering them, and a generative model answering from the top evidence | Learner should see retrieval, reranking, and generation as distinct jobs]]

---

## 4. Dense retrieval: search in embedding space

Recall from earlier lessons:

```text
text
→ embedding model
→ vector
```

Semantically related texts tend to receive nearby representations.

Dense retrieval uses that property.

Suppose we embed three documents:

```text
Document A → vector A
Document B → vector B
Document C → vector C
```

Then embed the query:

```text
Query → query vector
```

Now compare the query vector to every document vector.

The closest vectors become the search results.

Conceptually:

```text
semantic similarity
≈
closeness in embedding space
```

[[IMAGE_NEEDED: Dense retrieval embedding space | Show query and several document points in a vector space, with the nearest two documents highlighted as retrieved results | Learner should connect semantic similarity with nearest-neighbor retrieval]]

### Important design question

Should the system always return something?

Not necessarily.

If every candidate is weakly related, a useful search system may prefer:

```text
"No sufficiently relevant result found."
```

rather than returning the least-bad result as if it were good.

That is why the chapter mentions using a distance or similarity threshold.

---

## 5. Queries and documents are not always semantically symmetric

A subtle point in the chapter is that:

> A query and its best result do not always look semantically similar in the same way two ordinary documents do.

Example:

```text
Query:
When did Interstellar premiere?

Relevant passage:
Interstellar premiered on October 26, 2014, in Los Angeles.
```

The query is a question.

The passage is an answer.

They play different roles.

This is why retrieval embedding models are often trained using:

```text
query
+
relevant result
+
irrelevant result
```

rather than only ordinary sentence similarity.

The training objective teaches:

```text
relevant query-document pair
→ move closer

irrelevant query-document pair
→ move farther apart
```

---

## 6. Build a searchable vector index

A common dense-retrieval pipeline is:

```text
Knowledge base
    ↓
Chunk documents
    ↓
Embed every chunk
    ↓
Store vectors in an index
```

Then at query time:

```text
User query
    ↓
Embed query
    ↓
Search nearest vectors
    ↓
Return matching chunks
```

[[IMAGE_NEEDED: Vector indexing and retrieval | Two phases: indexing phase with documents → chunks → embeddings → vector index, and query phase with query → embedding → nearest-neighbor lookup → retrieved chunks | Learner should distinguish offline indexing from online query retrieval]]

This separation is important.

You generally do **not** want to re-embed the entire corpus every time someone searches.

---

## 7. Dense retrieval example from the chapter

The source uses text from the Wikipedia article about *Interstellar*.

It breaks the article into short sentence-level chunks.

Then it sends them to an embedding API.

Conceptually:

```python
response = co.embed(
    texts=texts,
    input_type="search_document",
).embeddings
```

The source reports:

```text
15 document vectors
4096 dimensions each
```

So:

```text
embeds.shape
→ (15, 4096)
```

Interpretation:

```text
15 chunks
×
4096 embedding features per chunk
```

The lesson is not to memorize `4096`.

The important idea is:

```text
one chunk
→ one dense vector
```

---

## 8. Build a nearest-neighbor index with FAISS

The chapter uses FAISS:

```python
import faiss

dim = embeds.shape[1]

index = faiss.IndexFlatL2(dim)

index.add(
    np.float32(embeds)
)
```

FAISS stores the vectors in a structure optimized for similarity search.

Then a query embedding can be searched against the index.

At small scale, comparing a query against all vectors may be fine.

At larger scale, specialized indexes become important.

### Source-era caution

Exact library APIs may evolve.

Treat the chapter’s code as a concrete demonstration of the architecture:

```text
vectors
→ index
→ nearest-neighbor search
```

not as a permanent API reference.

---

## 9. Query the index

The chapter’s search flow is:

```text
1. Embed the query
2. Search nearest neighbors
3. Retrieve matching text chunks
4. Return distances/scores
```

Conceptually:

```python
query_embed = embed_query(query)

distances, ids = index.search(
    [query_embed],
    number_of_results,
)
```

Then the IDs map back to the original chunks.

For the query:

```text
how precise was the science
```

the best dense-retrieval result discusses:

```text
scientific accuracy
theoretical astrophysics
```

even though the wording does not directly repeat the query.

That is exactly the behavior semantic search aims to provide.

---

## 10. Compare dense retrieval with BM25 keyword search

The chapter compares semantic retrieval to BM25.

BM25 is a lexical retrieval method.

It rewards word overlap and term importance.

For the same query:

```text
how precise was the science
```

the lexical system can rank text containing:

```text
science fiction
```

because of the shared word:

```text
science
```

even if that passage does not answer the intent.

Dense retrieval can instead find:

```text
scientific accuracy
```

despite the lack of exact wording.

[[IMAGE_NEEDED: BM25 versus dense retrieval example | Show the same query with BM25 selecting a passage that shares the word “science,” while dense retrieval selects a passage about “scientific accuracy” | Learner should understand lexical overlap versus semantic relevance]]

### Does this mean dense retrieval replaces keyword search?

No.

The chapter explicitly gives cases where keyword matching remains valuable, especially:

```text
exact phrase lookup
exact identifiers
specific names
literal text matching
```

This leads naturally to hybrid search.

---

## 11. Hybrid search: use lexical and semantic signals together

Dense search is good at:

```text
meaning
paraphrases
conceptual similarity
```

Keyword/BM25 search is good at:

```text
exact terms
rare identifiers
precise phrase matches
```

So a robust system often combines them.

Conceptually:

```text
Query
 ├─ BM25
 │    ↓
 │ lexical candidates
 │
 └─ Dense retrieval
      ↓
   semantic candidates
        ↓
      merge
        ↓
     rerank
```

[[IMAGE_NEEDED: Hybrid search architecture | Show one query branching to BM25 and dense retrieval, candidate lists being merged, then sent to reranking | Learner should see hybrid search as combining complementary retrieval signals]]

The chapter advises hybrid search instead of relying solely on dense retrieval.

---

## 12. Caveat 1: dense retrieval still returns something when nothing is relevant

Suppose the corpus is only about *Interstellar*.

Now ask:

```text
What is the mass of the moon?
```

The embedding search still returns nearest neighbors.

But:

```text
nearest
≠
relevant
```

The nearest vectors may simply be the least unrelated options.

That is why production retrieval often needs:

- similarity thresholds,
- “no result” behavior,
- confidence heuristics,
- downstream validation.

A retriever should not be forced to pretend the corpus contains an answer.

---

## 13. Caveat 2: retrieval quality can drop in a new domain

An embedding model trained primarily on general internet or Wikipedia-like text may work less well on:

```text
legal documents
medical records
technical manuals
specialized internal company terminology
```

if those patterns differ substantially from its training data.

This is a form of domain mismatch.

The chapter later connects this to retrieval fine-tuning.

The practical lesson is:

> Evaluate retrieval on the domain you actually plan to search.

Do not assume strong general semantic embeddings automatically solve every specialized corpus.

---

## 14. Why long documents need chunking

Transformer models have finite context limits.

Embedding an entire long document can also compress many unrelated ideas into one vector.

Suppose a long report contains sections about:

```text
revenue
hiring
security
product roadmap
legal risks
```

One vector for the full report mixes all of those concepts.

If the user asks:

```text
What were the security risks?
```

a more focused security chunk may be much easier to retrieve.

This leads to the chunking principle:

> Search works better when the indexed unit aligns with the unit of information users are likely to ask about.

[[IMAGE_NEEDED: Whole document vector versus chunk vectors | Show one long document mapped to a single compressed vector on the left, and the same document split into multiple topic-specific chunks with separate vectors on the right | Learner should see why multiple chunk vectors preserve more retrievable detail]]

---

## 15. One vector per document

The chapter describes two broad ways to create one vector for a long document.

### Option A — Embed only a representative portion

For example:

```text
title
first paragraph
abstract
```

Advantage:

```text
simple and fast
```

Disadvantage:

```text
unembedded content becomes unsearchable
```

### Option B — Embed multiple chunks, then average them

Conceptually:

```text
chunk 1 vector
chunk 2 vector
chunk 3 vector
        ↓
      average
        ↓
one document vector
```

Advantage:

```text
the whole document contributes
```

Disadvantage:

```text
many concepts are compressed into one vector
```

Specific details may become harder to retrieve.

---

## 16. Multiple vectors per document

A stronger approach for many search systems is:

```text
document
→ chunk 1 → vector 1
→ chunk 2 → vector 2
→ chunk 3 → vector 3
```

Now the index stores chunk vectors rather than only document-level vectors.

Benefits:

- full-text coverage,
- more localized concepts,
- better retrieval of specific information,
- richer search index.

But chunking itself becomes a design problem.

---

## 17. Chunking strategies

The chapter gives several options.

### Sentence chunks

```text
one sentence
→ one embedding
```

Pros:

```text
very focused
```

Cons:

```text
may lose surrounding context
```

### Paragraph chunks

Often a natural choice when paragraphs are short and coherent.

### Multi-sentence chunks

The chapter suggests grouping several sentences when needed.

### Add document title

A chunk may gain useful context if prefixed with:

```text
document title
```

### Overlap adjacent chunks

Example:

```text
Chunk A:
sentences 1–5

Chunk B:
sentences 4–8
```

The overlap preserves context near boundaries.

[[IMAGE_NEEDED: Chunking strategies | Show one document split four ways: sentence chunks, paragraph chunks, fixed multi-sentence chunks, and overlapping chunks with shared boundary text | Learner should understand that chunk size and overlap change retrieval behavior]]

### No universally best chunk size

The chapter’s principle is:

> Chunking should match the kinds of documents and questions your application expects.

This is one of the most important RAG design decisions.

---

## 18. Exact search, approximate nearest neighbors, and vector databases

At small scale:

```text
thousands or tens of thousands of vectors
```

direct comparison may be practical.

At larger scale:

```text
millions of vectors
```

specialized retrieval systems become important.

The chapter mentions approximate-nearest-neighbor tools such as:

```text
Annoy
FAISS
```

These are designed to retrieve nearby vectors efficiently.

It also mentions vector databases such as:

```text
Weaviate
Pinecone
```

which add database-like capabilities.

### Vector database advantages

The chapter highlights:

- adding/deleting vectors without rebuilding everything,
- filtering,
- retrieval customization beyond raw vector distance.

Conceptually:

```text
vector index
→ optimized similarity lookup

vector database
→ similarity lookup + persistent data-management features
```

---

## 19. Fine-tuning embeddings for retrieval

Suppose a document says:

```text
Interstellar premiered on October 26, 2014, in Los Angeles.
```

Relevant queries might include:

```text
Interstellar release date
When did Interstellar premiere?
```

An irrelevant query might be:

```text
Interstellar cast
```

All three queries mention the same film.

A generic embedding model may place them all relatively close to the passage.

Retrieval training teaches the model the specific concept of **relevance**.

[[IMAGE_NEEDED: Retrieval fine-tuning positive and negative pairs | Show one relevant document with two positive query arrows being pulled closer and one irrelevant query arrow being pushed farther away after training | Learner should understand retrieval fine-tuning as shaping the geometry around task-specific relevance]]

The training goal is:

```text
positive query-document pair
→ closer

negative query-document pair
→ farther apart
```

This is similar in spirit to contrastive representation learning introduced earlier.

---

## 20. Reranking: improve the order after retrieval

A retriever must be fast enough to search a large corpus.

A reranker can afford to be slower because it only sees a shortlist.

Typical two-stage search:

```text
millions of documents
      ↓
fast first-stage retrieval
      ↓
top 100 candidates
      ↓
slower reranker
      ↓
top 10 best-ranked results
```

[[IMAGE_NEEDED: Two-stage retrieval and reranking | Show a huge corpus narrowed by a fast first-stage retriever to a small candidate set, followed by a slower relevance reranker producing the final ordered results | Learner should understand why reranking is normally applied to a shortlist rather than the whole corpus]]

The first stage can be:

- BM25,
- dense retrieval,
- hybrid search.

Then the reranker changes result order.

---

## 21. Reranker example

The chapter sends:

```text
query
+
candidate documents
```

to a reranking model.

The reranker returns:

```text
document
+
relevance score
```

Then the candidates are sorted by relevance.

This can rescue a weak first-stage ranking.

For example:

```text
BM25 candidate set
        ↓
reranker
        ↓
most semantically relevant passage moves upward
```

The important lesson is:

> First-stage retrieval mainly optimizes recall and speed; reranking can improve precision near the top.

---

## 22. How cross-encoder rerankers work

Dense retrieval usually embeds:

```text
query separately
document separately
```

Then compares the vectors.

A cross-encoder reranker instead evaluates:

```text
query + candidate document
```

together in the same model pass.

That allows richer token-level interaction between the query and document.

Conceptually:

```text
Dense retriever:
embed(query)
embed(doc)
compare vectors

Cross-encoder:
model(query, doc together)
→ relevance score
```

[[IMAGE_NEEDED: Bi-encoder versus cross-encoder | Left side shows query and document encoded independently then compared; right side shows query and document entering the same model together to produce one relevance score | Learner should understand why cross-encoders can judge relevance more deeply but are more expensive]]

This is why cross-encoders are often used after candidate retrieval rather than across the entire corpus.

---

## 23. Search evaluation requires relevance judgments

To evaluate a retrieval system, the chapter says we need:

```text
1. document archive
2. test queries
3. relevance judgments
```

For each query, we need to know which documents are considered relevant.

Without that, we cannot objectively measure search quality.

Example:

```text
Query Q1

Relevant documents:
D2
D5
D9
```

Then compare what the search system retrieves.

[[IMAGE_NEEDED: Retrieval evaluation test set | Show a query linked to a corpus with certain documents marked relevant, then a search system returning a ranked list that can be scored against those relevance judgments | Learner should see that search evaluation requires labeled relevance data]]

---

## 24. Precision at position k

Imagine the ranked results are:

```text
Rank 1: relevant
Rank 2: irrelevant
Rank 3: relevant
```

At rank 1:

```text
precision@1 = 1 / 1 = 1.0
```

At rank 3:

```text
relevant results so far = 2
results examined = 3

precision@3 = 2 / 3
```

Ranking matters.

A relevant result at position 1 is more useful than the same relevant result buried at position 10.

This motivates average precision.

---

## 25. Average Precision (AP)

Average Precision rewards systems that place relevant results early.

A simplified procedure:

```text
1. Walk down the ranked list.
2. Whenever a result is relevant, calculate precision at that position.
3. Average those precision values over the relevant documents.
```

Example:

```text
Rank 1: relevant
Rank 2: irrelevant
Rank 3: relevant
```

Then:

```text
precision@1 = 1/1 = 1.0
precision@3 = 2/3 ≈ 0.67
```

The AP summarizes ranking quality for one query.

[[IMAGE_NEEDED: Average Precision calculation | Show a ranked list with relevant items highlighted at positions 1 and 3, annotate precision@1 and precision@3, then average them | Learner should understand that AP rewards earlier relevant documents]]

---

## 26. Mean Average Precision (MAP)

Average Precision scores one query.

Mean Average Precision scores the system across many test queries.

Conceptually:

```text
Query 1 → AP1
Query 2 → AP2
Query 3 → AP3
...
        ↓
average
        ↓
MAP
```

MAP gives one number that can be used to compare retrieval systems on the same evaluation set.

### nDCG

The chapter also mentions:

```text
normalized discounted cumulative gain
```

or:

```text
nDCG
```

A key difference is that relevance can be graded.

Instead of:

```text
relevant / not relevant
```

you can have:

```text
highly relevant
somewhat relevant
weakly relevant
not relevant
```

This is useful when relevance is not binary.

---

{{exercise:M08.L01.EX01}}

---

## 27. Retrieval-Augmented Generation

Now we combine retrieval with generation.

A basic RAG system has two stages:

```text
1. Retrieval
2. Grounded generation
```

The generator receives:

```text
user question
+
retrieved evidence
```

and is asked to answer using that evidence.

[[IMAGE_NEEDED: Basic RAG pipeline | Show question → retriever → top evidence chunks → prompt containing question + context → LLM → grounded answer with citations | Learner should memorize retrieval first, generation second]]

### Why RAG helps

The generator no longer has to rely only on what is stored in model parameters.

It can use external information supplied at runtime.

This helps with:

- private/internal data,
- more current knowledge,
- domain-specific information,
- source-grounded answers.

The chapter frames RAG as a way to reduce hallucinations and improve factuality.

Important nuance:

> Retrieval does not guarantee correctness. Bad retrieval can ground the model on bad or irrelevant evidence.

---

## 28. Grounded generation

The generation stage receives:

```text
Question:
...

Relevant information:
chunk A
chunk B
chunk C
```

Then the prompt instructs the model to answer from that context.

This is **grounded generation**.

A useful prompt pattern is:

```text
Relevant information:
{context}

Answer the following question using the relevant information above:
{question}
```

The exact prompt can vary.

What matters is clearly separating:

```text
retrieved evidence
from
user question
```

and specifying how the evidence should be used.

---

## 29. Managed RAG example from the chapter

The source first retrieves relevant passages.

Then it sends:

```text
query
+
retrieved documents
```

to a managed chat model.

The example question is about:

```text
income generated
```

and the retrieved passage contains the film’s worldwide gross.

The model generates an answer grounded in that passage.

The chapter also demonstrates citation metadata pointing back to the supporting document.

This shows one of RAG’s strongest user-facing features:

> The system can potentially tell the user where the answer came from.

---

## 30. Local RAG architecture

The chapter then recreates the same idea with local components.

The system contains:

```text
Generation model
Embedding model
Vector store
Retriever
Prompt template
RAG chain
```

High-level flow:

```text
documents
→ embedding model
→ vector database

question
→ retriever
→ relevant chunks
→ prompt
→ local LLM
→ answer
```

[[IMAGE_NEEDED: Local RAG components | Show documents indexed by an embedding model into a local FAISS vector store, with question → retriever → context → prompt → local LLM → answer | Learner should see that RAG can be implemented entirely from modular local components]]

---

## 31. Separate retrieval model from generation model

A RAG system normally uses at least two model roles.

### Embedding model

Used for:

```text
indexing
query encoding
retrieval
```

### Generative model

Used for:

```text
reading retrieved context
writing the final answer
```

They do not have to be the same model.

This is a fundamental design pattern:

```text
representation model
+
generative model
```

working together.

The chapter uses a sentence embedding model for retrieval and Phi-3 for generation.

---

## 32. The RAG prompt is a critical control point

The source builds a prompt with two variables:

```text
context
question
```

Conceptually:

```python
template = (
    "Relevant information:\n"
    "{context}\n\n"
    "Provide a concise answer to the following question "
    "using the relevant information above:\n"
    "{question}"
)
```

This prompt decides:

- whether the model should rely on context,
- how concise the answer should be,
- whether unsupported claims are allowed,
- whether citations should be returned,
- what to do when the context lacks an answer.

A RAG pipeline is therefore not only about retrieval.

The generation prompt strongly influences grounded behavior.

---

## 33. RAG can fail in multiple places

A useful way to debug RAG is to separate failure stages.

### Retrieval failure

The correct evidence was never retrieved.

Possible causes:

- poor chunks,
- wrong embedding model,
- domain mismatch,
- bad query,
- insufficient candidate count.

### Reranking failure

The correct document was retrieved but ranked too low.

### Context-construction failure

Good evidence exists, but:

- too much irrelevant context is included,
- chunks are duplicated,
- context is truncated.

### Generation failure

The model sees the right evidence but:

- ignores it,
- misreads it,
- adds unsupported claims,
- answers beyond the context.

This leads to a key engineering habit:

> Evaluate retrieval and generation separately before judging the whole RAG system.

---

## 34. Advanced RAG: query rewriting

Conversation questions are often not written like good search queries.

Example from the chapter:

```text
We have an essay due tomorrow...
I love penguins...
Maybe dolphins...
Where do they live for example?
```

The search need is simply:

```text
Where do dolphins live
```

Query rewriting transforms:

```text
verbose conversational request
→ concise retrieval query
```

[[IMAGE_NEEDED: Query rewriting | Show a long conversational user message being condensed by an LLM into a short search-optimized query before retrieval | Learner should understand that user language and retrieval language can differ]]

This can improve retrieval especially in chat applications.

---

## 35. Advanced RAG: multi-query retrieval

Some questions contain multiple information needs.

Example:

```text
Compare Nvidia financial results in 2020 vs 2023.
```

A single search query may not retrieve the best evidence for both years.

Instead:

```text
Query 1:
Nvidia 2020 financial results

Query 2:
Nvidia 2023 financial results
```

Then combine the results before generation.

Conceptually:

```text
user question
     ↓
query decomposition
   ↙      ↘
Q1        Q2
↓          ↓
retrieve  retrieve
   ↘      ↙
combine evidence
     ↓
generate comparison
```

This improves coverage for multi-part questions.

---

## 36. Advanced RAG: multi-hop retrieval

Some questions require later searches to depend on earlier results.

Example from the chapter:

```text
Who are the largest car manufacturers in 2023?
Do they each make EVs?
```

First retrieve:

```text
largest car manufacturers 2023
```

Suppose the results identify:

```text
Toyota
Volkswagen
Hyundai
```

Now the next queries can be formed:

```text
Toyota electric vehicles
Volkswagen electric vehicles
Hyundai electric vehicles
```

This is **multi-hop retrieval**.

[[IMAGE_NEEDED: Multi-hop RAG | Show first retrieval producing entities, then each entity generating follow-up queries whose evidence is combined into a final answer | Learner should see that later retrieval depends on earlier retrieval results]]

Unlike ordinary multi-query retrieval, the second-stage queries cannot necessarily be known before the first search completes.

---

## 37. Advanced RAG: query routing

Some applications have multiple knowledge sources.

For example:

```text
HR question
→ HR knowledge system

customer question
→ CRM

engineering question
→ technical documentation
```

Query routing asks:

> Which source should answer this information need?

Conceptually:

```text
user question
     ↓
router
 ┌───┼────┐
 ↓   ↓    ↓
HR  CRM  Docs
```

This is especially useful when each source has different permissions, structure, or retrieval methods.

---

## 38. Advanced RAG: agentic retrieval

As query rewriting evolves into:

- deciding whether search is required,
- generating multiple queries,
- issuing sequential searches,
- choosing between data sources,
- using different tools,

the RAG system begins to resemble an agent.

The chapter calls this direction:

```text
agentic RAG
```

The retrievers/data sources can be abstracted as tools.

Then the model helps decide:

```text
whether to search
where to search
what query to issue
whether another search is needed
```

[[IMAGE_NEEDED: Agentic RAG architecture | Show an LLM/controller choosing among several retrieval tools/data sources, inspecting observations, issuing follow-up queries, then generating a final grounded answer | Learner should connect advanced RAG with the agent/tool ideas from Chapter 7]]

With greater autonomy comes the same reliability concern from the previous lesson:

```text
more dynamic decisions
→ more possible failure modes
→ stronger need for observability and validation
```

---

## 39. Evaluating RAG requires more than one score

A RAG system includes:

```text
retrieval
+
generation
+
citation/grounding behavior
```

So one metric is rarely enough.

The chapter discusses several evaluation dimensions.

### Fluency

Is the generated answer readable and cohesive?

### Perceived utility

Is it useful and informative?

### Citation recall

Of the claims about the external world, how many are supported by citations?

### Citation precision

Do the citations actually support the claims they are attached to?

### Faithfulness

Is the answer consistent with the provided context?

### Answer relevance

Does the answer actually address the user’s question?

[[IMAGE_NEEDED: RAG evaluation dimensions | Show a RAG answer surrounded by evaluation checks for retrieval quality, faithfulness, answer relevance, citation precision/recall, fluency, and utility | Learner should see that RAG quality is multidimensional]]

The source also notes that human evaluation is valuable and that some tooling uses an LLM as a judge for automated scoring.

---

## 40. Evaluate retrieval and generation separately

Suppose the final answer is wrong.

There are at least two very different possibilities.

### Case A — Retrieval failed

The evidence never contained the answer.

Fixing the generator will not solve this.

### Case B — Retrieval succeeded

The correct evidence was present, but the model ignored or misinterpreted it.

Fixing the retriever may not solve this.

A strong RAG evaluation therefore asks separately:

```text
Did we retrieve useful evidence?

Did the generator use that evidence correctly?
```

This separation makes system improvement much more targeted.

---

## 41. Put the whole semantic-search and RAG pipeline together

A robust modern pipeline can look like:

### Offline indexing

```text
Documents
  ↓
Chunking
  ↓
Embedding model
  ↓
Vector index/database
```

### Online query path

```text
User question
  ↓
Optional query rewrite
  ↓
Hybrid first-stage retrieval
  ↓
Candidate documents
  ↓
Reranker
  ↓
Best evidence chunks
  ↓
RAG prompt
  ↓
Generative model
  ↓
Grounded answer + sources
```

### Advanced extensions

```text
multi-query
multi-hop
routing
agentic tool selection
```

### Evaluation

```text
retrieval metrics
+
generation/grounding metrics
```

[[IMAGE_NEEDED: Complete semantic search and RAG architecture | Show offline indexing with chunking/embeddings/vector database and online flow with query rewrite → hybrid retrieval → reranker → context assembly → generator → cited answer, with evaluation attached to both retrieval and generation | Learner should use this as the final architecture map for the chapter]]

---

{{exercise:M08.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Semantic search means keyword search is obsolete.

### Why this is wrong

Exact phrases, identifiers, names, and literal terms are often handled very well by lexical retrieval. The chapter recommends hybrid approaches.

---

### Misconception 2

> The nearest vector is always a relevant answer.

### Why this is wrong

Nearest-neighbor search always returns the closest available items, even when the corpus contains no real answer.

---

### Misconception 3

> One document should always have one embedding.

### Why this is wrong

Long documents often benefit from multiple chunk embeddings so specific concepts remain retrievable.

---

### Misconception 4

> Smaller chunks are always better.

### Why this is wrong

Very small chunks can lose necessary context. Chunking must balance focus and context.

---

### Misconception 5

> Dense retrieval and reranking do the same job.

### Why this is wrong

Dense retrieval efficiently finds candidate documents. Reranking more carefully scores a smaller candidate set and changes their order.

---

### Misconception 6

> Rerankers should score every document in a million-document corpus.

### Why this is wrong

Cross-encoder-style reranking is usually too expensive for the full corpus and is therefore applied after first-stage retrieval.

---

### Misconception 7

> RAG guarantees factual answers.

### Why this is wrong

Poor retrieval, bad context assembly, or incorrect generation can still produce wrong answers.

---

### Misconception 8

> If a RAG answer is fluent, the RAG system is working well.

### Why this is wrong

Fluency is only one dimension. Evidence support, relevance, citations, and retrieval quality also matter.

---

### Misconception 9

> Query rewriting changes the user’s intent.

### Why this is wrong

Its purpose is to express the same information need in a form that is easier for the retriever to handle.

---

### Misconception 10

> Multi-query and multi-hop RAG are identical.

### Why this is wrong

Multi-query can issue several related searches in parallel, while multi-hop retrieval forms later queries using information discovered in earlier retrieval steps.

---

## Key terminology

| Term | Meaning |
|---|---|
| Semantic search | Retrieval based on meaning rather than only word overlap |
| Dense retrieval | Retrieval using dense query/document embeddings |
| Lexical search | Retrieval based on words/tokens and their occurrence |
| BM25 | Widely used lexical ranking method |
| Hybrid search | Search that combines lexical and semantic retrieval signals |
| Embedding | Dense vector representation of text |
| Nearest-neighbor search | Finding vectors closest to a query vector |
| FAISS | Library used for efficient vector similarity search |
| Vector database | Database designed to store/query vector representations with persistence and filtering features |
| Chunk | Smaller unit of a document indexed independently |
| Chunk overlap | Repeated boundary context shared by adjacent chunks |
| Retriever | Component that selects potentially relevant documents/chunks |
| Reranker | Model that rescoring candidates based on query relevance |
| Cross-encoder | Model that processes query and candidate together to assign relevance |
| Precision@k | Fraction of top-k results that are relevant |
| Average Precision | Ranking metric averaging precision values at positions containing relevant results |
| MAP | Mean Average Precision across multiple queries |
| nDCG | Ranking metric supporting graded relevance and position discounting |
| RAG | Retrieval-Augmented Generation |
| Grounded generation | Generation conditioned on retrieved external evidence |
| Query rewriting | Rephrasing a user request into a search-optimized query |
| Multi-query RAG | Retrieving evidence with multiple queries for one user question |
| Multi-hop RAG | Sequential retrieval where later queries depend on earlier retrieved information |
| Query routing | Choosing which data source/retriever should handle a query |
| Agentic RAG | Retrieval system where an LLM dynamically decides retrieval/tool actions |
| Citation recall | How many externally grounded claims are supported with citations |
| Citation precision | How often citations actually support the claims they are attached to |
| Faithfulness | Consistency of generated answer with provided context |
| Answer relevance | Degree to which generated answer addresses the user question |

---

## Self-check

Before moving on, make sure you can answer:

1. What is the difference between keyword search and semantic search?
2. What are the three major search components introduced in the chapter?
3. How does dense retrieval work?
4. Why might a similarity threshold be useful?
5. Why may retrieval-specific embedding training be necessary?
6. What does an embedding matrix shape such as `(15, 4096)` represent?
7. What does a vector index do?
8. Why did dense retrieval outperform BM25 for the “how precise was the science” example?
9. In what situations can BM25 still be better?
10. What is hybrid search?
11. Why is chunking necessary for long documents?
12. What are the tradeoffs between one-vector-per-document and multiple-vectors-per-document?
13. Why can overlapping chunks help?
14. What is the role of an approximate nearest-neighbor index?
15. How is a vector database different from a simple vector index?
16. What do positive and negative pairs do during retrieval fine-tuning?
17. Why is reranking normally a second-stage process?
18. How does a cross-encoder reranker differ from independent query/document embeddings?
19. What three components are required for retrieval evaluation?
20. What does Average Precision reward?
21. How is MAP calculated conceptually?
22. Why is nDCG useful?
23. What are the two stages of basic RAG?
24. What does grounded generation mean?
25. Why should retrieval and generation be evaluated separately?
26. What does query rewriting improve?
27. How does multi-query RAG work?
28. How does multi-hop RAG differ?
29. What is query routing?
30. Why does advanced RAG begin to resemble an agent?
31. Name at least four RAG evaluation dimensions.
32. Draw or explain the complete pipeline from raw documents to a cited RAG answer.

---

## Retain this idea

**Modern search systems increasingly combine several complementary stages. Dense retrieval finds semantically related candidates, lexical search preserves exact-match strengths, reranking improves the ordering of shortlisted results, and RAG adds a generator that answers from retrieved evidence. The quality of the final system depends not only on the LLM, but also on chunking, embedding quality, candidate retrieval, reranking, context construction, grounding instructions, and evaluation. Strong RAG engineering therefore means designing and measuring the entire retrieval-and-generation pipeline rather than treating retrieval as a single vector-search call.**
"""
        ),

        "estimated_minutes": 195,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-search", "title": "Why language models changed search", "order": 1},
            {"id": "rag-motivation", "title": "Why search became important for text generation too", "order": 2},
            {"id": "three-components", "title": "Three major components: retrieval, reranking, and RAG", "order": 3},
            {"id": "dense-retrieval", "title": "Dense retrieval: search in embedding space", "order": 4},
            {"id": "query-document-asymmetry", "title": "Queries and documents are not always semantically symmetric", "order": 5},
            {"id": "indexing-pipeline", "title": "Build a searchable vector index", "order": 6},
            {"id": "dense-example", "title": "Dense retrieval example from the chapter", "order": 7},
            {"id": "faiss", "title": "Build a nearest-neighbor index with FAISS", "order": 8},
            {"id": "search-function", "title": "Query the index", "order": 9},
            {"id": "bm25", "title": "Compare dense retrieval with BM25 keyword search", "order": 10},
            {"id": "hybrid-search", "title": "Hybrid search: use lexical and semantic signals together", "order": 11},
            {"id": "dense-caveats", "title": "Caveat 1: dense retrieval still returns something when nothing is relevant", "order": 12},
            {"id": "domain-shift", "title": "Caveat 2: retrieval quality can drop in a new domain", "order": 13},
            {"id": "chunking-why", "title": "Why long documents need chunking", "order": 14},
            {"id": "one-vector", "title": "One vector per document", "order": 15},
            {"id": "multi-vector", "title": "Multiple vectors per document", "order": 16},
            {"id": "chunking-strategies", "title": "Chunking strategies", "order": 17},
            {"id": "index-scale", "title": "Exact search, approximate nearest neighbors, and vector databases", "order": 18},
            {"id": "retrieval-finetuning", "title": "Fine-tuning embeddings for retrieval", "order": 19},
            {"id": "reranking", "title": "Reranking: improve the order after retrieval", "order": 20},
            {"id": "reranker-example", "title": "Reranker example", "order": 21},
            {"id": "cross-encoder", "title": "How cross-encoder rerankers work", "order": 22},
            {"id": "retrieval-evaluation", "title": "Search evaluation requires relevance judgments", "order": 23},
            {"id": "precision-at-k", "title": "Precision at position k", "order": 24},
            {"id": "average-precision", "title": "Average Precision (AP)", "order": 25},
            {"id": "map", "title": "Mean Average Precision (MAP)", "order": 26},
            {"id": "rag", "title": "Retrieval-Augmented Generation", "order": 27},
            {"id": "grounded-generation", "title": "Grounded generation", "order": 28},
            {"id": "rag-api-example", "title": "Managed RAG example from the chapter", "order": 29},
            {"id": "local-rag", "title": "Local RAG architecture", "order": 30},
            {"id": "local-embedding-model", "title": "Separate retrieval model from generation model", "order": 31},
            {"id": "rag-prompt", "title": "The RAG prompt is a critical control point", "order": 32},
            {"id": "rag-failure-modes", "title": "RAG can fail in multiple places", "order": 33},
            {"id": "query-rewriting", "title": "Advanced RAG: query rewriting", "order": 34},
            {"id": "multi-query", "title": "Advanced RAG: multi-query retrieval", "order": 35},
            {"id": "multi-hop", "title": "Advanced RAG: multi-hop retrieval", "order": 36},
            {"id": "query-routing", "title": "Advanced RAG: query routing", "order": 37},
            {"id": "agentic-rag", "title": "Advanced RAG: agentic retrieval", "order": 38},
            {"id": "rag-evaluation", "title": "Evaluating RAG requires more than one score", "order": 39},
            {"id": "retrieval-vs-generation-eval", "title": "Evaluate retrieval and generation separately", "order": 40},
            {"id": "full-pipeline", "title": "Put the whole semantic-search and RAG pipeline together", "order": 41},
            {"id": "misconceptions", "title": "Important misconceptions", "order": 42},
            {"id": "terminology", "title": "Key terminology", "order": 43},
            {"id": "self-check", "title": "Self-check", "order": 44},
            {"id": "retain", "title": "Retain this idea", "order": 45},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M08.L01.EX01",

            "title": "Build and Evaluate a Two-Stage Search System",

            "lesson_code": "M08.L01",

            "section_id": "map",

            "placement": "after_section",

            "description": (
                "Build a small semantic/lexical retrieval experiment and learn to "
                "evaluate ranking quality rather than judging search by intuition alone."
            ),

            "instructions": (
                "Use a small corpus of 20–50 short passages and create at least 8 "
                "queries with manually identified relevant passages.\n"
                "1. Build a lexical BM25 retriever.\n"
                "2. Build a dense retriever using a sentence embedding model.\n"
                "3. Compare the top-5 results for every query.\n"
                "4. Identify at least two queries where lexical search works better and "
                "two where dense retrieval works better.\n"
                "5. Create a hybrid candidate set from both retrievers.\n"
                "6. Apply a reranker if available; otherwise define how a cross-encoder "
                "reranker would score the candidate set.\n"
                "7. Compute or manually calculate precision at relevant ranks for at "
                "least three queries.\n"
                "8. Calculate Average Precision for those queries.\n"
                "9. Compute their mean to obtain MAP for the mini test set.\n"
                "10. Explain what retrieval errors remain after reranking."
            ),

            "expected_output": (
                "A notebook or report containing lexical and dense retrieval results, "
                "hybrid candidates, optional reranked results, manually defined relevance "
                "judgments, AP calculations, MAP, and a short error analysis."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "bm25",
                "dense-retrieval",
                "hybrid-search",
                "reranking",
                "precision-at-k",
                "average-precision",
                "map",
            ],
        },

        {
            "id": "M08.L01.EX02",

            "title": "Design and Diagnose a RAG Pipeline",

            "lesson_code": "M08.L01",

            "section_id": "full-pipeline",

            "placement": "after_section",

            "description": (
                "Design a complete RAG application from indexing through generation "
                "and diagnose failures by stage."
            ),

            "instructions": (
                "Design a RAG assistant for a collection of long technical documents.\n"
                "1. Define the document unit and your chunking strategy, including "
                "approximate chunk size, overlap, and whether titles/metadata are added.\n"
                "2. Choose a retrieval architecture: dense only or hybrid lexical+dense. "
                "Explain why.\n"
                "3. Define the vector index/database role.\n"
                "4. Define the first-stage candidate count and the number of documents "
                "passed to the reranker.\n"
                "5. Define the final number of evidence chunks supplied to the generator.\n"
                "6. Write a RAG prompt that requires answers to use the supplied context "
                "and to say when the context does not support an answer.\n"
                "7. Add a query-rewriting step for conversational questions.\n"
                "8. Give one example requiring multi-query retrieval and one requiring "
                "multi-hop retrieval.\n"
                "9. Define at least four retrieval metrics or checks and four generation/"
                "grounding checks.\n"
                "10. Describe how you would debug these failures separately: correct "
                "document not retrieved, correct document retrieved but reranked too low, "
                "correct evidence in context but model gives unsupported answer, and "
                "citation attached to the wrong claim."
            ),

            "expected_output": (
                "An end-to-end RAG architecture containing indexing, chunking, hybrid "
                "retrieval, reranking, context assembly, prompt, generation, advanced "
                "query handling, evaluation criteria, and a stage-by-stage failure "
                "diagnosis table."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "rag-design",
                "chunking",
                "retrieval",
                "reranking",
                "query-rewriting",
                "multi-query-rag",
                "multi-hop-rag",
                "rag-evaluation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M08.L01.QZ01",

        "title": "Semantic Search and Retrieval-Augmented Generation — Knowledge Check",

        "lesson_code": "M08.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M08.L01.Q01",
                "section_id": "why-search",
                "question": "What is the defining goal of semantic search?",
                "options": [
                    "Retrieve only documents containing the exact query words.",
                    "Retrieve information based on meaning, even when wording differs.",
                    "Generate an answer without looking at any documents.",
                    "Convert every document into a keyword list only.",
                ],
                "correct": 1,
                "explanation": (
                    "Semantic search aims to retrieve conceptually relevant information "
                    "rather than depending only on lexical overlap."
                ),
            },
            {
                "id": "M08.L01.Q02",
                "section_id": "three-components",
                "question": "Which ordering best represents a common modern search pipeline?",
                "options": [
                    "Generation → retrieval → tokenization",
                    "Retrieval → reranking → grounded generation",
                    "Reranking → indexing → model training",
                    "Prompting → clustering → translation",
                ],
                "correct": 1,
                "explanation": (
                    "A fast retriever finds candidates, a reranker improves ordering, "
                    "and a generator may then answer from top evidence."
                ),
            },
            {
                "id": "M08.L01.Q03",
                "section_id": "dense-retrieval",
                "question": "How does dense retrieval identify candidate documents?",
                "options": [
                    "By counting only exact word overlap",
                    "By embedding queries/documents and retrieving nearby vectors",
                    "By generating a summary for every document on every query",
                    "By sorting documents alphabetically",
                ],
                "correct": 1,
                "explanation": (
                    "Dense retrieval converts text into vectors and uses nearest-neighbor "
                    "search to find semantically related documents."
                ),
            },
            {
                "id": "M08.L01.Q04",
                "section_id": "dense-caveats",
                "question": (
                    "Why can dense retrieval return misleading results when the corpus "
                    "contains no answer?"
                ),
                "options": [
                    "Nearest-neighbor search still returns the closest available vectors even if none are truly relevant.",
                    "Dense retrieval refuses to return any vectors.",
                    "Embedding models only work on questions.",
                    "The index deletes low-score documents.",
                ],
                "correct": 0,
                "explanation": (
                    "Closeness is relative to what exists in the index, so systems may "
                    "need thresholds or abstention behavior."
                ),
            },
            {
                "id": "M08.L01.Q05",
                "section_id": "hybrid-search",
                "question": "Why combine lexical and dense retrieval?",
                "options": [
                    "Because both methods make identical errors.",
                    "Because lexical search is strong for exact terms while dense retrieval captures semantic similarity.",
                    "Because dense retrieval cannot process text.",
                    "Because BM25 requires embeddings.",
                ],
                "correct": 1,
                "explanation": (
                    "Hybrid search combines complementary exact-match and semantic signals."
                ),
            },
            {
                "id": "M08.L01.Q06",
                "section_id": "chunking-strategies",
                "question": "Why can chunk overlap improve retrieval?",
                "options": [
                    "It guarantees every result is relevant.",
                    "It preserves some surrounding context near chunk boundaries.",
                    "It removes the need for an embedding model.",
                    "It makes documents shorter than one token.",
                ],
                "correct": 1,
                "explanation": (
                    "Overlapping context reduces the chance that useful meaning is split "
                    "awkwardly across chunk boundaries."
                ),
            },
            {
                "id": "M08.L01.Q07",
                "section_id": "reranking",
                "question": "Why is reranking normally applied after first-stage retrieval?",
                "options": [
                    "Rerankers are often more expensive, so they are used on a smaller candidate set.",
                    "Rerankers cannot process queries.",
                    "Retrievers require reranker outputs before indexing.",
                    "Reranking is only for image search.",
                ],
                "correct": 0,
                "explanation": (
                    "First-stage retrieval narrows the corpus, making slower and richer "
                    "relevance scoring affordable on the shortlist."
                ),
            },
            {
                "id": "M08.L01.Q08",
                "section_id": "cross-encoder",
                "question": "What distinguishes a cross-encoder reranker from dense bi-encoder retrieval?",
                "options": [
                    "It processes query and candidate together before assigning a relevance score.",
                    "It cannot see the query.",
                    "It only performs keyword matching.",
                    "It produces no score.",
                ],
                "correct": 0,
                "explanation": (
                    "Joint processing allows deeper query-document interaction but costs "
                    "more computation per candidate."
                ),
            },
            {
                "id": "M08.L01.Q09",
                "section_id": "average-precision",
                "question": "What does Average Precision reward?",
                "options": [
                    "Only the number of indexed documents",
                    "Relevant results appearing early in the ranking",
                    "Longer generated answers",
                    "Larger embedding dimensions",
                ],
                "correct": 1,
                "explanation": (
                    "AP averages precision at the positions where relevant documents "
                    "appear, so earlier relevant items improve the score."
                ),
            },
            {
                "id": "M08.L01.Q10",
                "section_id": "map",
                "question": "How is MAP obtained conceptually?",
                "options": [
                    "Average the Average Precision scores across test queries.",
                    "Add all embedding dimensions.",
                    "Count only the first retrieved document.",
                    "Measure generation temperature.",
                ],
                "correct": 0,
                "explanation": (
                    "MAP is the mean of per-query AP values on a shared evaluation set."
                ),
            },
            {
                "id": "M08.L01.Q11",
                "section_id": "rag",
                "question": "What are the two core stages of a basic RAG system?",
                "options": [
                    "Fine-tuning and quantization",
                    "Retrieval and grounded generation",
                    "Clustering and classification",
                    "Tokenization and translation",
                ],
                "correct": 1,
                "explanation": (
                    "RAG retrieves evidence first, then asks a generator to answer using "
                    "that evidence."
                ),
            },
            {
                "id": "M08.L01.Q12",
                "section_id": "rag-failure-modes",
                "question": (
                    "If the correct evidence is present in the context but the model "
                    "adds unsupported claims, which stage most directly failed?"
                ),
                "options": [
                    "Index creation",
                    "Generation/grounding",
                    "Chunk storage",
                    "Query embedding",
                ],
                "correct": 1,
                "explanation": (
                    "Retrieval succeeded in this case; the generator failed to remain "
                    "faithful to the supplied evidence."
                ),
            },
            {
                "id": "M08.L01.Q13",
                "section_id": "query-rewriting",
                "question": "What is the purpose of query rewriting?",
                "options": [
                    "Change the user’s intended question into a different task.",
                    "Express the same information need in a form that is easier to retrieve.",
                    "Delete the retrieval stage.",
                    "Increase the model vocabulary.",
                ],
                "correct": 1,
                "explanation": (
                    "Query rewriting removes conversational noise and creates a search-"
                    "optimized expression of the same intent."
                ),
            },
            {
                "id": "M08.L01.Q14",
                "section_id": "multi-hop",
                "question": "What makes multi-hop retrieval different from ordinary multi-query retrieval?",
                "options": [
                    "Later queries can depend on information discovered in earlier retrieval steps.",
                    "It always uses exactly one query.",
                    "It cannot use a vector database.",
                    "It performs no generation.",
                ],
                "correct": 0,
                "explanation": (
                    "Multi-hop systems retrieve iteratively, using earlier results to "
                    "form follow-up information needs."
                ),
            },
            {
                "id": "M08.L01.Q15",
                "section_id": "rag-evaluation",
                "question": "What does faithfulness evaluate in RAG?",
                "options": [
                    "Whether the answer is consistent with the provided context.",
                    "Whether the embedding vectors are normalized.",
                    "Whether every query contains keywords.",
                    "Whether the generator is the largest available model.",
                ],
                "correct": 0,
                "explanation": (
                    "Faithfulness asks whether generated claims remain supported by the "
                    "retrieved context."
                ),
            },
            {
                "id": "M08.L01.Q16",
                "section_id": "full-pipeline",
                "type": "open",
                "question": (
                    "Design a production RAG pipeline for a collection of long company "
                    "documents. Explain your chunking strategy, lexical/dense retrieval "
                    "choice, reranking stage, context assembly, generation prompt, "
                    "query rewriting, citation handling, and how you would evaluate "
                    "retrieval quality separately from grounded-answer quality."
                ),
            },
        ],

        "passing_score": 70,
    },
}
