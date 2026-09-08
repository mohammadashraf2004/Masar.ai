"""
backend/seeds/levels/level_06_advanced_rag.py

AI Developer career track -- Level 6: Advanced RAG.

Exported as a standalone LEVEL dict (same convention used in
level_05_embeddings_semantic_search.py) until common.py exists to
standardize the import/export shape across level files.

Shape matches seed_track_ai_developer.py's LEVELS entries:
    LEVEL = {"title", "description", "order", "topics": [ ... ]}
    each topic = {title, slug, description, order, difficulty,
                   estimated_hours, skill_tags, prerequisite_ids,
                   lesson, exercises, quiz, project}
"""
from app.models.learning import DifficultyLevel

LEVEL = {
    "title": "Level 6: Advanced RAG",
    "description": (
        "Go beyond a single dense-vector lookup: understand why pure semantic "
        "search breaks down for exact identifiers, numbers, and rare terms, "
        "and how sparse search, hybrid retrieval, and reranking fix it."
    ),
    "order": 6,
    "topics": [
        {
            # ------------------------------------------------------------
            # Topic 1
            # ------------------------------------------------------------
            "title": "Dense Retrieval",
            "slug": "ai-developer-advanced-rag-dense-retrieval",
            "description": (
                "How dense retrieval actually works under the hood -- embedding "
                "queries and documents into the same vector space and searching "
                "by similarity -- and where it starts to break down."
            ),
            "order": 1,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "embeddings", "retrieval", "vector-search"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Dense Retrieval",
                "content": """# Dense Retrieval

You've already built a basic RAG pipeline: embed a document, embed a query, find the nearest vectors, hand the results to an LLM. That whole approach has a name -- **dense retrieval** -- and understanding it precisely is what lets you see exactly where it breaks.

## What Is Dense Retrieval?

Dense retrieval represents both the **query** and the **documents** as dense vectors, then finds the document vectors most similar to the query vector.

```
User Query
    ↓
Embedding Model
    ↓
Dense Vector
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Top-K Documents
```

Say a user asks *"How can I graduate from the university?"* An embedding model turns that into something like `[0.12, -0.43, 0.87, 0.21, ...]`. Your documents were embedded the same way ahead of time -- Chunk A might be `[0.10, -0.40, 0.82, ...]`, Chunk B `[-0.72, 0.15, 0.03, ...]`. The system compares the query vector against every document vector and returns whichever are closest.

## Why "Dense"?

Because the vector is a continuous numerical representation spread across many dimensions -- 384, 768, 1024, depending on the model -- and *most of those dimensions carry a nonzero value*. Contrast that later with **sparse** vectors (like BM25's), where almost all dimensions are zero and only a few words "light up." Dense vs. sparse is really about how the meaning is distributed across the vector.

## Why It's Powerful: Meaning, Not Just Words

Dense retrieval's whole advantage is retrieving by *meaning* rather than exact word overlap. If your database holds:

> "Students must successfully complete the required number of academic credits before graduation."

...and the user asks *"How many credits do I need to finish my degree?"* -- there's no exact phrase match anywhere in that sentence. But an embedding model places both close together in vector space, because *"credits required for graduation"* and *"academic credits before graduation"* mean roughly the same thing.

## Dense Retrieval vs. Keyword Search

Take a document: *"Students must complete 160 credit hours to graduate."* And a query: *"What is the required number of academic hours for finishing my degree?"*

A keyword search struggles here -- "required," "academic hours," "finishing," and "degree" don't literally appear in the document; it says "complete," "credit hours," and "graduate" instead. Dense retrieval doesn't care about that surface mismatch: it recognizes that *required academic hours ≈ credit hours required* and *finishing degree ≈ graduate*, and scores the document highly anyway.

## Where This Sits in RAG

```
                 RAG
                  │
                  ↓
               Retrieval
                  │
                  ↓
          ┌───────────────┐
          │ Dense Search  │
          └───────┬───────┘
                  ↓
             Top-K chunks
                  ↓
             Context
                  ↓
                 LLM
                  ↓
               Answer
```

Dense retrieval is *one way* of implementing the retrieval stage of RAG -- not the only way, and not automatically the best way for every kind of content.

## Where Qdrant / FAISS Actually Fit

It's worth being precise here, because it's a common source of confusion: **neither Qdrant nor FAISS is the embedding model.** They play a different role.

The embedding model converts text into vectors:

```
Embedding Model
      ↓
[0.12, 0.43, -0.82, ...]
```

Qdrant / FAISS store those vectors and search them:

```
Vectors
   ↓
FAISS / Qdrant
   ↓
Nearest vectors
```

So the full pipeline, for documents, is `Document → Embedding Model → Vector → Qdrant`. Then at query time: `User Query → Same Embedding Model → Query Vector → Qdrant similarity search → Top-K chunks`.

## Same Embedding Space, Non-Negotiable

This is an easy mistake to make in production: if your documents were embedded with **Embedding Model A** and your query gets embedded with **Embedding Model B**, you generally *cannot* assume those vectors are comparable at all. Cosine similarity between vectors from two different embedding spaces is close to meaningless.

```
Documents ──→ Embedding Model
                   │
                   ↓
              Vector Space
                   ↑
                   │
Query ─────→ Same Embedding Model
```

Both sides need to land in the same, compatible vector space -- always the same model (or at least the same model family and version) for indexing and querying.

## Where Dense Retrieval Falls Apart

This is where Advanced RAG actually starts. Dense retrieval is good at meaning, and *bad* at a few specific things:

**Exact identifiers.** A query like *"What is CSE251?"* asks an embedding model to distinguish between `CSE251`, `CSE252`, `CSE351`, and `CSE451` -- codes that are semantically almost identical to a model, even though they refer to completely different things.

**Numbers.** If your documents say Course A has 3 credits, Course B has 4, and Course C has 6, a query like *"Which course has 4 credits?"* needs precise, literal matching -- not "close enough in meaning."

**Rare words.** Something like `REG-2025-17A`, a course code, or a specific legal reference number is exactly the kind of rare, low-frequency token that *keyword* search is often better suited to catch than a dense embedding.

## Why This Leads to Advanced RAG

None of this means dense retrieval is wrong -- it means it isn't *sufficient* on its own. A stronger system combines multiple retrieval strategies and lets them cover each other's blind spots:

```
                    Query
                      ↓
             ┌────────┴────────┐
             ↓                 ↓
       Dense Retrieval     BM25 Search
             ↓                 ↓
             └────────┬────────┘
                      ↓
                 Combine Results
                      ↓
                   Reranker
                      ↓
                Best Context
                      ↓
                     LLM
```

That combination -- sparse retrieval, hybrid search, reciprocal rank fusion, and reranking -- is exactly what the rest of this level covers.

## From What You've Built to What's Next

You've already written something close to this:

```python
query_embedding = model.encode(query)

results = vector_db.similarity_search(
    query_embedding,
    k=5
)
```

The mental model to keep from here on: **dense retrieval = semantic representation + vector similarity + nearest-neighbor search.** It gives you high *semantic recall*, but not perfect precision -- which is exactly why production RAG systems layer other retrieval methods on top rather than stopping here.

*The single idea to keep:* dense retrieval finds meaning ≈ meaning, but it was never designed to nail exact identifiers, numbers, or rare terms -- and that gap is the entire reason Advanced RAG exists.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Pick the Right Retrieval Method",
                    "description": (
                        "Your university database contains:\n\n"
                        "- CSE251 — Machine Learning — 3 credits\n"
                        "- CSE252 — Deep Learning — 3 credits\n"
                        "- CSE351 — Computer Vision — 4 credits\n\n"
                        "A user asks: \"What is the course code for Computer Vision?\"\n\n"
                        "Would you rely only on dense retrieval, or would you want another "
                        "retrieval method to help surface the exact course code? Explain your "
                        "reasoning in terms of what dense retrieval is good and bad at."
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "retrieval", "critical-thinking"],
                },
                {
                    "title": "Same Space, Different Models",
                    "description": (
                        "You inherit a RAG pipeline where documents were embedded months ago "
                        "with `text-embedding-3-small`, but a teammate just changed the query-time "
                        "embedding call to use `text-embedding-3-large` for 'better quality.' "
                        "Explain what will happen to retrieval quality and why, then write the "
                        "one-line fix."
                    ),
                    "starter_code": (
                        "# Bug: documents and queries are embedded with different models.\n"
                        "# Fix the query-time embedding call so it matches the index.\n\n"
                        "DOCUMENT_EMBED_MODEL = \"text-embedding-3-small\"\n\n"
                        "def embed_query(query: str):\n"
                        "    # BUG: mismatched model\n"
                        "    return embed(query, model=\"text-embedding-3-large\")\n"
                    ),
                    "solution_code": (
                        "DOCUMENT_EMBED_MODEL = \"text-embedding-3-small\"\n\n"
                        "def embed_query(query: str):\n"
                        "    return embed(query, model=DOCUMENT_EMBED_MODEL)\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "embeddings", "debugging"],
                },
            ],
            "quiz": {
                "title": "Dense Retrieval — Knowledge Check",
                "questions": [
                    {
                        "question": "What makes a vector 'dense' rather than 'sparse'?",
                        "options": [
                            "It only contains whole numbers",
                            "Most of its dimensions carry a nonzero value, spreading meaning across the whole vector",
                            "It always has more than 1000 dimensions",
                            "It is generated only by transformer models",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Dense vectors distribute meaning across most dimensions with continuous "
                            "nonzero values, unlike sparse vectors (e.g. BM25) where nearly all "
                            "dimensions are zero and only a few terms are active."
                        ),
                    },
                    {
                        "question": (
                            "A document says 'Students must complete 160 credit hours to graduate' "
                            "and a query asks 'What is the required number of academic hours for "
                            "finishing my degree?' Why can dense retrieval match these even though "
                            "almost no words overlap?"
                        ),
                        "options": [
                            "Dense retrieval always does an exact substring match first",
                            "The embedding model places semantically similar phrases close together in vector space, regardless of exact wording",
                            "Dense retrieval ignores the query and returns the most popular document",
                            "It can't -- this is a case dense retrieval would fail",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Dense retrieval works on meaning, not literal word overlap, so phrases "
                            "like 'academic hours' and 'credit hours' land close together in the "
                            "embedding space even with zero shared keywords."
                        ),
                    },
                    {
                        "question": "In a RAG pipeline, what role do Qdrant and FAISS actually play?",
                        "options": [
                            "They generate the embeddings from raw text",
                            "They store vectors and perform nearest-neighbor similarity search over them",
                            "They fine-tune the embedding model",
                            "They replace the LLM in the answer-generation step",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Qdrant and FAISS are vector stores/search engines -- they index and "
                            "search vectors that an embedding model already produced. They don't "
                            "create embeddings themselves."
                        ),
                    },
                    {
                        "question": (
                            "Why is it risky to embed your documents with one model and your "
                            "queries with a different model?"
                        ),
                        "options": [
                            "It isn't risky -- similarity search works across any two embedding spaces",
                            "It only matters if the models have different dimension counts",
                            "The vectors may not live in a comparable space, making similarity scores meaningless",
                            "It only affects speed, not accuracy",
                        ],
                        "correct": 2,
                        "explanation": (
                            "Different embedding models generally produce incompatible vector "
                            "spaces. Similarity scores computed across two different spaces aren't "
                            "reliable, even if the vectors happen to have the same dimensionality."
                        ),
                    },
                    {
                        "question": (
                            "Which of the following is dense retrieval LEAST reliable for, on its own?"
                        ),
                        "options": [
                            "Matching a paraphrased question to a semantically similar passage",
                            "Finding an exact course code like CSE251 among very similar codes",
                            "Retrieving a passage about a topic described with different words",
                            "Ranking documents by overall topical relevance",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Exact identifiers, numbers, and rare tokens are dense retrieval's "
                            "weak spot -- embeddings represent meaning, and near-identical codes "
                            "like CSE251 vs CSE252 can end up with very similar vectors despite "
                            "referring to completely different things."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 2
            # ------------------------------------------------------------
            "title": "BM25",
            "slug": "ai-developer-advanced-rag-bm25",
            "description": (
                "A keyword-based retrieval algorithm that ranks documents by how "
                "well their terms match the query -- exactly where dense retrieval "
                "tends to struggle: exact IDs, codes, and rare terms."
            ),
            "order": 2,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "bm25", "retrieval", "keyword-search"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "BM25",
                "content": """# BM25

Dense retrieval is excellent at finding information by meaning, but it can struggle with exact words, IDs, numbers, and rare terms. **BM25** is the classic answer to that gap -- a powerful, keyword-based retrieval algorithm.

## The Basic Idea

BM25 doesn't understand the *meaning* of text the way an embedding model does. Instead, it asks one question: *"How well do the words in the query match the words in this document?"*

Query: `CSE251 credit hours`

Document A: *"CSE251 — Machine Learning — 3 credit hours"*
Document B: *"CSE351 — Computer Vision — 4 credit hours"*

BM25 strongly favors Document A, because it contains the exact important terms: **CSE251**, **credit**, **hours**.

## Why BM25 Is Useful

Search your university documents for `CSE251`. Dense retrieval might surface CSE251, CSE252, CSE351, and CSE451 alike -- because they're all *semantically related* (they're all courses). BM25 focuses on the literal word `CSE251`, so the exact match wins decisively.

That makes BM25 particularly strong for: **course codes, product IDs, names, error messages, technical terms, legal references, numbers, exact phrases.**

## BM25 vs. Dense Retrieval

| | Dense Retrieval | BM25 |
|---|---|---|
| Main idea | Meaning | Words |
| Representation | Vectors | Terms |
| Semantic similarity | Strong | Weak |
| Exact keyword matching | Weak | Strong |
| Rare identifiers | Weak | Strong |
| Synonyms / paraphrases | Strong | Weak |
| Numbers / codes | Weak | Strong |

Two different questions, essentially: dense retrieval asks *"do these two texts mean similar things?"*; BM25 asks *"do these two texts contain the same important words?"*

## A Worked Example

Three documents:

1. *"Students need 160 credit hours for graduation."*
2. *"Graduation requires completing the required academic credits."*
3. *"CSE251 is a 3-credit Machine Learning course."*

Query: *"How many credit hours are required for graduation?"*

**Dense retrieval** might rank them `Doc 1 → 0.91`, `Doc 2 → 0.87`, `Doc 3 → 0.42` -- Documents 1 and 2 share meaning even with different wording.

**BM25** looks for matching terms like *credit*, *hours*, *required*, *graduation*. Document 1 contains the most of those literally, so it likely still comes out on top, with Document 2 close behind and Document 3 far behind. Both approaches land in a similar place here -- they just get there by looking at the problem differently.

## What BM25 Actually Considers

You don't need the formula yet -- just the three ideas behind it.

**① Term frequency.** How often does a query term appear? If a document mentions *graduation* three times, that's some evidence of relevance -- though BM25 doesn't reward unlimited repetition; the benefit tapers off.

**② Inverse document frequency.** A word appearing in almost every document (*student*, *course*, *university*) isn't very informative. A word appearing in only a few documents (*CSE251*) is much more informative. **Rare term → more valuable. Common term → less valuable.**

**③ Document length.** Finding `CSE251` once in a short, focused document is more meaningful than finding it once inside a 5,000-word regulation document. BM25 compensates for document length so long documents don't win purely by containing more words.

## Why Not Just Count Matching Words?

A naive scorer like `score = number_of_matching_words` is too crude. BM25 improves on it by combining **term frequency + term rarity + document length** into one score -- which is exactly why it became the standard traditional information-retrieval algorithm, long before embeddings existed.

## BM25 in Python

A common implementation is `rank_bm25`:

```python
from rank_bm25 import BM25Okapi

documents = [
    "Students need 160 credit hours for graduation.",
    "CSE251 is a 3-credit Machine Learning course.",
    "Registration opens before the semester."
]

tokenized_docs = [doc.lower().split() for doc in documents]

bm25 = BM25Okapi(tokenized_docs)

query = "credit hours graduation"
tokenized_query = query.lower().split()

scores = bm25.get_scores(tokenized_query)
# conceptually: [2.81, 1.24, 0.00]
```

Rank the documents by score, and you have a working keyword retriever -- no embedding model involved.

## Two Independent Architectures

```
                 BM25
                  │
Query ──→ Tokenize
                  │
                  ↓
            Keyword Search
                  │
                  ↓
             BM25 Scores
                  │
                  ↓
              Top-K Docs
```

```
              Dense Search
                   │
Query ──→ Embedding Model
                   │
                   ↓
              Query Vector
                   │
                   ↓
             Vector Database
                   │
                   ↓
                Top-K Docs
```

BM25 needs **no embedding model at all** -- it's a completely separate retrieval system from dense search.

## Why Advanced RAG Uses Both

For a query like *"What are the requirements for CSE251?"*, dense retrieval understands *requirements*, *course*, *Machine Learning*, *CSE251* as related concepts. BM25 strongly prioritizes documents that literally contain `CSE251` and `requirements`.

Rather than choosing **Dense OR BM25**, Advanced RAG combines them: **Dense AND BM25**. That combination is called **Hybrid Search**, covered in a later lesson -- but first, the next lesson steps back to the broader concept BM25 is one example of: **Sparse Retrieval**.

## Mental Model

Two librarians helping you find a book. One asks *"which books are about the same topic?"* -- that's dense retrieval. The other asks *"which books contain the exact words you're searching for?"* -- that's BM25. A good RAG system benefits from asking both questions.

*The single idea to keep:* BM25 ranks by term frequency, term rarity, and document length -- no meaning required -- which makes it the natural complement to dense retrieval's blind spots on exact IDs, codes, and rare terms.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Why BM25, Why Dense",
                    "description": (
                        "You have three documents:\n\n"
                        "A: \"CSE251 is Machine Learning and has 3 credit hours.\"\n"
                        "B: \"Machine learning courses teach algorithms and statistical models.\"\n"
                        "C: \"CSE351 is Computer Vision and has 4 credit hours.\"\n\n"
                        "Query: \"What is CSE251?\"\n\n"
                        "Answer: (1) Why might BM25 be especially useful here? "
                        "(2) Why might dense retrieval also return Document B? "
                        "(3) What is the main difference between what BM25 and dense "
                        "retrieval are each looking for?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "bm25", "critical-thinking"],
                },
                {
                    "title": "Build a Minimal BM25 Search",
                    "description": (
                        "Using `rank_bm25`, index the given documents, tokenize the query "
                        "the same way as the documents, score all documents against it, "
                        "and return the top result's original text (not just its score)."
                    ),
                    "starter_code": (
                        "from rank_bm25 import BM25Okapi\n\n"
                        "documents = [\n"
                        "    \"Students need 160 credit hours for graduation.\",\n"
                        "    \"CSE251 is a 3-credit Machine Learning course.\",\n"
                        "    \"Registration opens before the semester.\",\n"
                        "]\n\n"
                        "def top_bm25_result(documents, query):\n"
                        "    # TODO: tokenize documents, build BM25Okapi index,\n"
                        "    # tokenize the query the same way, score, and return\n"
                        "    # the highest-scoring document's original text.\n"
                        "    pass\n\n"
                        "print(top_bm25_result(documents, \"credit hours graduation\"))\n"
                    ),
                    "solution_code": (
                        "from rank_bm25 import BM25Okapi\n\n"
                        "def top_bm25_result(documents, query):\n"
                        "    tokenized_docs = [doc.lower().split() for doc in documents]\n"
                        "    bm25 = BM25Okapi(tokenized_docs)\n"
                        "    tokenized_query = query.lower().split()\n"
                        "    scores = bm25.get_scores(tokenized_query)\n"
                        "    best_idx = max(range(len(scores)), key=lambda i: scores[i])\n"
                        "    return documents[best_idx]\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "bm25", "python"],
                },
            ],
            "quiz": {
                "title": "BM25 — Knowledge Check",
                "questions": [
                    {
                        "question": "What question does BM25 fundamentally ask about a query and a document?",
                        "options": [
                            "Do they mean similar things semantically?",
                            "How well do the words in the query match the words in the document?",
                            "Were they written by the same author?",
                            "Are they the same length?",
                        ],
                        "correct": 1,
                        "explanation": (
                            "BM25 is a lexical/keyword algorithm -- it scores documents by term "
                            "overlap with the query, not by semantic meaning."
                        ),
                    },
                    {
                        "question": "Why does inverse document frequency make rare terms more valuable in BM25?",
                        "options": [
                            "Rare terms are always longer words",
                            "A term appearing in almost every document carries little discriminating power, while a rare term strongly narrows down relevant documents",
                            "BM25 assigns random weights to rare terms",
                            "Rare terms are weighted lower to avoid spam",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Common words like 'student' or 'course' appear everywhere and don't "
                            "help distinguish relevant documents. A rare term like 'CSE251' is far "
                            "more informative because so few documents contain it."
                        ),
                    },
                    {
                        "question": (
                            "Why does BM25 account for document length when scoring term matches?"
                        ),
                        "options": [
                            "Longer documents are always considered more authoritative",
                            "Shorter documents are penalized regardless of content",
                            "Finding a term once in a short, focused document can be more meaningful than finding it once in a very long document",
                            "Document length has no effect on BM25 scoring",
                        ],
                        "correct": 2,
                        "explanation": (
                            "BM25 compensates for length so long documents don't automatically "
                            "win just by containing more words overall; a single match in a short "
                            "document can be more significant."
                        ),
                    },
                    {
                        "question": "Which of these is BM25 typically strongest at retrieving?",
                        "options": [
                            "A paraphrased question with no shared vocabulary with the source",
                            "An exact course code, product ID, or error message",
                            "A general topical summary written in different words",
                            "A translated version of the same sentence",
                        ],
                        "correct": 1,
                        "explanation": (
                            "BM25 excels at exact term matches -- codes, IDs, and technical terms "
                            "-- which is precisely where dense retrieval tends to be weaker."
                        ),
                    },
                    {
                        "question": "What does BM25 require to run, compared to dense retrieval?",
                        "options": [
                            "The same embedding model used for dense retrieval",
                            "No embedding model at all -- it works directly on tokenized text",
                            "A GPU for vector computation",
                            "A vector database like Qdrant or FAISS",
                        ],
                        "correct": 1,
                        "explanation": (
                            "BM25 is a purely lexical algorithm operating on tokenized terms -- it "
                            "doesn't need an embedding model or a vector database at all."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 3
            # ------------------------------------------------------------
            "title": "Sparse Retrieval",
            "slug": "ai-developer-advanced-rag-sparse-retrieval",
            "description": (
                "The broader concept BM25 belongs to: representing text through its "
                "terms rather than dense vectors, and why lexical and semantic "
                "retrieval solve different problems."
            ),
            "order": 3,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "sparse-retrieval", "bm25", "retrieval"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Sparse Retrieval",
                "content": """# Sparse Retrieval

So far: **dense retrieval** searches by meaning, and **BM25** searches by matching words. Now we zoom out one level, because BM25 is actually one example of a broader category -- **sparse retrieval** -- and understanding that category is what sets up Hybrid Search.

## What Does "Sparse" Mean?

Imagine representing a document over a vocabulary of 10,000 words. A document might look like:

```
[0, 0, 0, 2, 0, 0, 1, 0, 0, 0, ...]
```

Most values are zero -- only a handful of positions (the words that actually appear) carry a value. That's a **sparse representation**.

Compare that to an embedding:

```
[0.21, -0.43, 0.71, 0.18, -0.62, 0.33, ...]
```

Most dimensions here have non-zero values. That's a **dense representation**.

```
Dense
────────────────
Text → Embedding → [0.21, -0.43, 0.71, 0.18, ...]
                    ↑
              lots of values

Sparse
────────────────
Text → Term representation → [0, 0, 0, 1, 0, 0, 0, 3, ...]
                              ↑
                         mostly zeros
```

So: **dense retrieval represents meaning using dense vectors. Sparse retrieval represents text primarily through its terms.**

## Where BM25 Fits

BM25 *is* a sparse retrieval algorithm:

```
Sparse Retrieval
       │
       ├── BM25
       │
       └── Other lexical retrieval approaches
```

Which gives two parallel chains:

```
Dense Retrieval → Semantic similarity → Embeddings
Sparse Retrieval → Lexical similarity → Words/terms → BM25
```

## Why "Lexical"?

You'll see this word constantly in RAG literature. **Lexical** just means *related to the actual words/terms in the text*. For the query *"Python FastAPI authentication,"* a lexical retrieval system cares specifically about the terms **Python**, **FastAPI**, **authentication** -- if a document contains those, that's strong evidence of relevance.

## Example: Technical Documentation

- Document A: *"FastAPI authentication using OAuth2 and JWT."*
- Document B: *"Building REST APIs with Flask."*
- Document C: *"Authentication in Django applications."*

Query: *"FastAPI OAuth2 authentication"*

Sparse retrieval is very effective here because the exact technical terms -- **FastAPI**, **OAuth2**, **authentication** -- all matter, and Document A contains all three.

## Sparse Retrieval in a Bilingual RAG System

In an Arabic academic RAG system, a student asks: *"ما هي متطلبات CSE251؟"* -- the identifier `CSE251` is critical here, and sparse retrieval can lean hard on that exact term. Meanwhile, if the student instead asks *"ما هي متطلبات مقرر تعلم الآلة؟"* (using different wording than the stored document), dense retrieval is what picks up the semantic relationship despite the different phrasing.

```
Sparse → Exact terms, codes, names, numbers, technical terminology
Dense  → Meaning, paraphrases, semantic relationships, different wording
```

## Two Librarians, Revisited

**Librarian 1 (Dense):** you say *"I need information about finishing my university degree,"* and even without your exact words appearing anywhere, they find something semantically related.

**Librarian 2 (Sparse):** you say *"Find CSE251,"* and they search for the literal term `CSE251` and return documents containing it.

## Sparse Doesn't Mean Outdated

It's tempting to assume dense embeddings are "more advanced" and sparse retrieval is legacy technology. That's not the right framing. Modern RAG systems very often use **Dense + Sparse together**, precisely because they solve *different* retrieval problems, not because one has replaced the other.

**Where sparse wins:** Documents `CSE251 — Machine Learning`, `CSE252 — Deep Learning`, `CSE351 — Computer Vision`. Query: `CSE251`. Sparse retrieval has an obvious, decisive advantage -- exact term match.

**Where dense wins:** Document: *"Students must complete 160 credit hours before receiving their degree."* Query: *"How many academic credits do I need to finish university?"* The wording differs enough (*academic credits* vs. *credit hours*, *finish university* vs. *receiving their degree*) that dense retrieval's grasp of meaning is what closes the gap.

## The Real Power: Combining Them

```
                    Query
                      ↓
             ┌────────┴────────┐
             ↓                 ↓
       Dense Retrieval   Sparse Retrieval
             ↓                 ↓
        semantic match    keyword match
             ↓                 ↓
             └────────┬────────┘
                      ↓
                Combined Results
                      ↓
                   Reranking
                      ↓
                     LLM
```

This is **Hybrid Search** -- the subject of the next lesson.

## Three Terms Not to Confuse

- **Sparse representation** -- a way of representing information where most values are zero.
- **Sparse retrieval** -- retrieval based primarily on sparse/lexical representations.
- **BM25** -- a specific ranking algorithm commonly used for sparse/lexical retrieval.

So `Sparse Retrieval → BM25` is a useful mental shortcut, but remember sparse retrieval is the broader concept; BM25 is just its most common implementation.

## The Advanced RAG Mental Model So Far

```
                 RETRIEVAL
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
       DENSE                SPARSE
          │                   │
    Embeddings              Terms
          │                   │
    Vector Search            BM25
          │                   │
          └─────────┬─────────┘
                    ↓
              Hybrid Search
```

*The single idea to keep:* sparse retrieval represents text as mostly-zero term vectors and matches on literal words; BM25 is its most common algorithm. The question worth asking isn't *"which is better, dense or sparse?"* -- it's *"when does each work best, and how do we combine them?"*
""",
                "estimated_minutes": 25,
                "has_code_examples": False,
            },
            "exercises": [
                {
                    "title": "Debugging an Error Message Query",
                    "description": (
                        "Query: \"What is the error ModuleNotFoundError: fastapi?\"\n\n"
                        "Knowledge base:\n"
                        "A: \"FastAPI installation and dependency troubleshooting.\"\n"
                        "B: \"How to build APIs with Django.\"\n"
                        "C: \"ModuleNotFoundError: fastapi occurs when FastAPI is not installed.\"\n\n"
                        "Answer: (1) Would sparse retrieval be useful here? Why? "
                        "(2) Would dense retrieval be useful here? Why? "
                        "(3) Why could combining both be better than using only one?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "sparse-retrieval", "critical-thinking"],
                },
                {
                    "title": "Sparse vs. Dense Representation",
                    "description": (
                        "Given a toy vocabulary of 8 words and a document's word counts, write "
                        "a function that builds its sparse term-count vector, then explain in a "
                        "sentence why the result is described as 'sparse' when the vocabulary "
                        "grows to 10,000 words instead of 8."
                    ),
                    "starter_code": (
                        "VOCAB = [\"cse251\", \"credit\", \"hours\", \"machine\", \"learning\",\n"
                        "         \"vision\", \"course\", \"graduation\"]\n\n"
                        "def sparse_vector(document_words: list[str]) -> list[int]:\n"
                        "    # TODO: return a list the same length as VOCAB, where each\n"
                        "    # position holds the count of that vocab word in document_words.\n"
                        "    pass\n\n"
                        "doc = \"cse251 machine learning course credit hours\".split()\n"
                        "print(sparse_vector(doc))\n"
                    ),
                    "solution_code": (
                        "VOCAB = [\"cse251\", \"credit\", \"hours\", \"machine\", \"learning\",\n"
                        "         \"vision\", \"course\", \"graduation\"]\n\n"
                        "def sparse_vector(document_words: list[str]) -> list[int]:\n"
                        "    return [document_words.count(term) for term in VOCAB]\n"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "sparse-retrieval", "python"],
                },
            ],
            "quiz": {
                "title": "Sparse Retrieval — Knowledge Check",
                "questions": [
                    {
                        "question": "What makes a representation 'sparse'?",
                        "options": [
                            "It has fewer than 100 dimensions",
                            "Most of its values are zero, with only a few positions holding meaningful values",
                            "It can only represent numbers, not text",
                            "It is generated by a neural network",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A sparse representation is mostly zeros -- only the terms that "
                            "actually appear in the text have nonzero values, unlike dense "
                            "embeddings where most dimensions carry information."
                        ),
                    },
                    {
                        "question": "What is the relationship between sparse retrieval and BM25?",
                        "options": [
                            "They are unrelated retrieval families",
                            "BM25 is one specific algorithm within the broader category of sparse retrieval",
                            "Sparse retrieval is a newer replacement for BM25",
                            "BM25 is a type of dense retrieval",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Sparse retrieval is the broader concept -- retrieval based on "
                            "lexical/term representations -- and BM25 is its most common "
                            "ranking algorithm."
                        ),
                    },
                    {
                        "question": "What does 'lexical' mean in the context of retrieval?",
                        "options": [
                            "Related to the meaning of a sentence as a whole",
                            "Related to the actual words/terms present in the text",
                            "Related to how a document is formatted",
                            "Related to the language a document is translated from",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Lexical retrieval cares about the literal words and terms in the "
                            "text, as opposed to semantic meaning captured by embeddings."
                        ),
                    },
                    {
                        "question": (
                            "Why do modern RAG systems often combine dense and sparse retrieval "
                            "rather than picking one?"
                        ),
                        "options": [
                            "Sparse retrieval has been fully replaced and combining is only for legacy support",
                            "They solve different retrieval problems -- semantic similarity vs. exact term matching",
                            "Combining them is required by vector database vendors",
                            "Dense retrieval alone is always sufficient, but sparse adds speed",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Dense and sparse retrieval address different weaknesses -- dense "
                            "handles paraphrasing and meaning, sparse handles exact identifiers "
                            "and rare terms -- so combining them covers more cases than either alone."
                        ),
                    },
                    {
                        "question": (
                            "For the query 'CSE251' against documents CSE251, CSE252, and CSE351, "
                            "which retrieval approach has the clearer advantage, and why?"
                        ),
                        "options": [
                            "Dense retrieval, because the course codes are semantically similar",
                            "Sparse retrieval, because it can match the exact literal term CSE251",
                            "Neither approach can distinguish between these documents",
                            "Dense retrieval, because it ignores numbers entirely",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Sparse retrieval matches the exact term 'CSE251' directly, while "
                            "dense retrieval may struggle since the course codes are semantically "
                            "very similar to each other."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 4
            # ------------------------------------------------------------
            "title": "Hybrid Search",
            "slug": "ai-developer-advanced-rag-hybrid-search",
            "description": (
                "Combining dense and sparse retrieval so a single query benefits "
                "from both semantic understanding and exact keyword matching."
            ),
            "order": 4,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "hybrid-search", "retrieval", "bm25", "embeddings"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Hybrid Search",
                "content": """# Hybrid Search

We now combine the two retrieval approaches from the last two lessons: **dense retrieval**, which understands meaning, and **sparse retrieval / BM25**, which matches exact words. That combination is **Hybrid Search**.

## The Problem Hybrid Search Solves

A user asks: *"What are the requirements for CSE251?"* Your knowledge base has:

- Document A: *"CSE251 — Machine Learning — 3 credit hours. Prerequisites: CSE201 and MATH201."*
- Document B: *"Machine learning courses teach algorithms, statistical models, and prediction techniques."*
- Document C: *"Students must complete the required courses before graduation."*

**Dense retrieval** sees A and B as semantically related to machine learning, so it might rank A as very relevant, B as relevant, and C as somewhat relevant.

**BM25** sees the exact term `CSE251` only in Document A, so it ranks A as very strong, B as weak, and C as irrelevant.

Each retrieval method is looking at the same query through a different lens.

## Dense + BM25, Not Dense OR BM25

```
                         Query
                           │
                ┌──────────┴──────────┐
                ↓                     ↓
        Dense Retrieval          BM25 Retrieval
                ↓                     ↓
          Semantic Results       Keyword Results
                ↓                     ↓
                └──────────┬──────────┘
                           ↓
                    Combine Results
                           ↓
                     Final Candidates
                           ↓
                       Reranking
                           ↓
                          LLM
```

Running both retrievers and combining their outputs gives you the strengths of each.

## A Worked Example

Query: *"How many credits does CSE251 have?"*

Dense retrieval might rank: (1) general Machine Learning course info, (2) the CSE251 course description, (3) other Machine Learning courses.

BM25 might rank: (1) `CSE251 — Machine Learning — 3 credits`, (2) CSE251 prerequisites, (3) other references to CSE251.

Combine the two, and the CSE251 document -- which shows up strongly in *both* lists -- becomes an unusually strong candidate.

## Why This Is Powerful

**Query A**: *"How do I finish my degree?"* -- dense retrieval is doing most of the work here, since *finish my degree ≈ graduate ≈ graduation requirements*.

**Query B**: *"What is CSE251?"* -- sparse retrieval is doing most of the work, since `CSE251` is an exact identifier.

**Query C**: *"What are the CSE251 graduation requirements?"* -- now *both* matter: dense retrieval understands *graduation requirements*, while BM25 catches `CSE251`. This is the ideal hybrid-search query -- and real user questions look like Query C far more often than you'd expect.

## The Architecture

```
                     User Query
                         │
                ┌────────┴────────┐
                ↓                 ↓
             Embed             Tokenize
                ↓                 ↓
          Dense Search          BM25
                ↓                 ↓
           Top-K Dense        Top-K Sparse
                │                 │
                └────────┬────────┘
                         ↓
                  Result Fusion
                         ↓
                  Final Top-K
                         ↓
                    Reranker
                         ↓
                      Context
                         ↓
                        LLM
```

Notice the retrieval system produces *candidates* first -- it doesn't hand everything straight to the LLM. Those candidates get combined, and can be improved further downstream.

## The Catch: Scores Aren't Comparable

This is one of the most important engineering details in this whole level. Suppose dense retrieval produces:

```
Document A → 0.92
Document B → 0.84
Document C → 0.73
```

...and BM25 produces:

```
Document A → 12.4
Document B → 8.7
Document C → 2.1
```

You **cannot** just do `combined = dense_score + bm25_score`. Dense scores live roughly in `0 → 1`; BM25 scores can range much higher with no fixed ceiling. A raw sum would let BM25 dominate the combination purely because of its larger numbers, not because it's actually more reliable for that query. This mismatch is exactly why **result fusion methods** exist -- and one of the most useful is **RRF**, covered next.

## Two Ways to Combine Results

**Method 1**: normalize each retriever's scores onto a common scale, then take a weighted combination.
**Method 2**: ignore raw scores entirely and combine *rankings* instead -- this is RRF.

## A Quick Mental Model in Python

```python
dense_results = ["doc_A", "doc_C", "doc_B"]
bm25_results = ["doc_B", "doc_A", "doc_D"]
```

Dense ranks: A → 1, C → 2, B → 3. BM25 ranks: B → 1, A → 2, D → 3. Both systems agree that **A** and **B** are important, so a combined system should probably rank them highly -- but doing that *systematically*, across many documents and queries, is exactly the problem the next lesson (RRF) solves.

## Hybrid Search in a Bilingual RAG System

*"ما هي متطلبات مقرر CSE251؟"* -- dense retrieval understands **متطلبات** (requirements) and **مقرر** (course) and retrieves semantically relevant academic content, while BM25 strongly matches the literal `CSE251`. Arabic semantic meaning plus an exact course code together produce noticeably better retrieval than either alone -- one reason hybrid retrieval is a strong default for technical and multilingual RAG systems.

## When Should You Use It?

Hybrid search shines when your documents mix **semantic content** (graduation requirements, registration rules, academic policies) with **exact content** (`CSE251`, `2025/2026`, `160 credit hours`, `REG-123`). Most real-world enterprise document sets contain both -- which is why hybrid retrieval is so common in production RAG.

## The Bigger Picture

```
                    Advanced Retrieval
                           │
             ┌─────────────┴─────────────┐
             ↓                           ↓
          Dense                         Sparse
             │                           │
        Embeddings                      BM25
             │                           │
             └─────────────┬─────────────┘
                           ↓
                     Hybrid Search
                           ↓
                     Result Fusion
                           ↓
                         RRF
                           ↓
                       Reranking
                           ↓
                    Best Documents
```

*The single idea to keep:* Hybrid Search runs dense and sparse retrieval side by side rather than choosing one, but combining their raw scores directly is a trap -- the scales don't match, which is exactly the problem the next lesson's fusion method solves.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Spot the Overlap",
                    "description": (
                        "Dense Retrieval returns: 1. Document A, 2. Document C, 3. Document B.\n"
                        "BM25 returns: 1. Document B, 2. Document A, 3. Document D.\n\n"
                        "Answer: (1) Which documents appear in both retrieval results? "
                        "(2) Why is that useful? "
                        "(3) Why shouldn't we simply add the raw dense score and raw BM25 "
                        "score together?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "hybrid-search", "critical-thinking"],
                },
                {
                    "title": "Classify the Query",
                    "description": (
                        "For each query below, decide whether dense retrieval, sparse (BM25) "
                        "retrieval, or both would be the primary driver of a good result, and "
                        "justify each in one sentence:\n\n"
                        "1. \"How do I finish my degree?\"\n"
                        "2. \"What is CSE251?\"\n"
                        "3. \"What are the CSE251 graduation requirements?\"\n"
                        "4. \"REG-2025-17A status\""
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "hybrid-search", "critical-thinking"],
                },
            ],
            "quiz": {
                "title": "Hybrid Search — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the core idea behind Hybrid Search?",
                        "options": [
                            "Replace dense retrieval entirely with BM25 for speed",
                            "Run dense and sparse retrieval together and combine their results instead of choosing only one",
                            "Use dense retrieval only for short queries and BM25 only for long queries",
                            "Average every document's length before retrieval",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Hybrid Search runs both dense and sparse retrievers and combines "
                            "their results, since each captures relevance that the other can miss."
                        ),
                    },
                    {
                        "question": (
                            "Why is 'What are the CSE251 graduation requirements?' described as "
                            "an ideal hybrid-search query?"
                        ),
                        "options": [
                            "It is short enough for both retrievers to process quickly",
                            "It contains both a semantic concept (graduation requirements) and an exact identifier (CSE251)",
                            "It only contains an exact identifier, so BM25 alone is enough",
                            "It avoids using any technical terms",
                        ],
                        "correct": 1,
                        "explanation": (
                            "The query mixes a semantic phrase that dense retrieval understands "
                            "with an exact code that BM25 matches precisely -- exactly the case "
                            "hybrid search is built for."
                        ),
                    },
                    {
                        "question": (
                            "Dense retrieval scores range roughly 0 to 1, while BM25 scores can "
                            "range much higher with no fixed ceiling. What goes wrong if you "
                            "simply add the two raw scores together?"
                        ),
                        "options": [
                            "Nothing goes wrong, this is the standard approach",
                            "BM25's larger scale would disproportionately dominate the combined score, regardless of actual relevance",
                            "Dense retrieval's scores would always dominate instead",
                            "The scores would automatically normalize themselves during addition",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Because BM25 scores can be much larger in magnitude than dense "
                            "scores, naive addition lets BM25 dominate the combination purely "
                            "due to scale, not relevance -- which is why fusion methods like RRF "
                            "combine rankings instead of raw scores."
                        ),
                    },
                    {
                        "question": (
                            "In a hybrid retrieval architecture, what happens immediately after "
                            "Result Fusion, before the LLM sees anything?"
                        ),
                        "options": [
                            "The raw query is sent directly to the LLM",
                            "The final candidates typically go through a reranking step",
                            "The documents are re-embedded from scratch",
                            "BM25 runs a second time on the fused results",
                        ],
                        "correct": 1,
                        "explanation": (
                            "After dense and sparse results are fused into final candidates, a "
                            "reranker typically refines their order before the best context is "
                            "passed to the LLM."
                        ),
                    },
                    {
                        "question": (
                            "What kind of document collections benefit most from Hybrid Search?"
                        ),
                        "options": [
                            "Collections containing only exact numeric codes",
                            "Collections containing only free-form narrative text",
                            "Collections that mix semantic content (policies, explanations) with exact content (codes, IDs, numbers)",
                            "Collections with fewer than 10 documents",
                        ],
                        "correct": 2,
                        "explanation": (
                            "Hybrid Search is most valuable when documents combine both semantic "
                            "and exact information -- which describes most real-world enterprise "
                            "and academic document sets."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 5
            # ------------------------------------------------------------
            "title": "RRF (Reciprocal Rank Fusion)",
            "slug": "ai-developer-advanced-rag-rrf",
            "description": (
                "How to combine multiple ranked retrieval lists using rank "
                "positions instead of incomparable raw scores."
            ),
            "order": 5,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "rrf", "hybrid-search", "retrieval"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "RRF (Reciprocal Rank Fusion)",
                "content": """# RRF (Reciprocal Rank Fusion)

Hybrid Search left us with one open problem: how do you combine two rankings when their underlying scores aren't directly comparable? The answer is **RRF**.

```
                 Query
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
       Dense              BM25
          ↓                 ↓
      Ranking A          Ranking B
          └────────┬────────┘
                   ↓
              Combine
```

## What Is RRF?

RRF stands for **Reciprocal Rank Fusion** -- don't worry about the name. The core idea: **RRF combines multiple ranked lists by rewarding documents that appear near the top of those lists.** It doesn't look at the actual score each retriever assigned. It only cares about *position*: what rank did this document get?

## Why Rank Instead of Score?

Recall the earlier example. Dense: `Document A → 0.92, Document C → 0.84, Document B → 0.73`. BM25: `Document B → 12.4, Document A → 8.7, Document D → 2.1`. Those scores have completely different meanings and scales -- but the *rankings* are trivial to compare:

```
Dense: A → #1, C → #2, B → #3
BM25:  B → #1, A → #2, D → #3
```

RRF's philosophy, in plain words: *"I don't care whether your score was 0.92 or 12.4. I care that you ranked this document highly."*

## The Formula

$$ RRF(d) = \\sum_i \\frac{1}{k + rank_i(d)} $$

Where `d` is a document, `rank_i(d)` is that document's rank in retriever `i`, and `k` is a constant (commonly 60). You don't need to memorize this -- the mental model matters more: **higher rank → higher RRF contribution.**

## A Worked Example (k = 0, for simplicity)

Dense: `1. A, 2. C, 3. B`. BM25: `1. B, 2. A, 3. D`.

**Document A**: dense rank 1 → `1/1 = 1.0`; BM25 rank 2 → `1/2 = 0.5`. Total: `1.5`.
**Document B**: dense rank 3 → `1/3 = 0.33`; BM25 rank 1 → `1/1 = 1.0`. Total: `1.33`.
**Document C**: only in dense, rank 2 → `1/2 = 0.5`. Total: `0.5`.
**Document D**: only in BM25, rank 3 → `1/3 = 0.33`. Total: `0.33`.

Final ranking: `A (1.50) > B (1.33) > C (0.50) > D (0.33)`.

Notice: A was dense #1 / BM25 #2 -- both systems support it strongly. B was dense #3 / BM25 #1 -- BM25 strongly supports it, dense less so. RRF blends both signals into one ranking.

## Why RRF Works Well for Hybrid Search

```
             Dense       BM25
               ↓           ↓
               A           B
               C           A
               B           F
               D           C
               E           G
                \\          /
                 \\        /
                  RRF
                   ↓
             Combined ranking
```

Documents that sit near the top of *both* lists get strong combined support -- exactly what you want when dense and sparse retrieval have complementary strengths.

## No Score Normalization Required

This is one of RRF's biggest practical advantages. Score-based fusion needs you to normalize dense scores, normalize BM25 scores, then weight-combine them. RRF skips all of that:

```
Dense ranking ──┐
                ├──→ RRF → Combined ranking
BM25 ranking ───┘
```

No need to make `0.82` comparable to `17.4` -- ranks are used directly.

## A Minimal Python Implementation

```python
def rrf(results_lists, k=60):
    scores = {}

    for results in results_lists:
        for rank, doc in enumerate(results, start=1):
            scores[doc] = scores.get(doc, 0) + 1 / (k + rank)

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

dense_results = ["A", "C", "B", "D"]
bm25_results = ["B", "A", "E", "C"]

results = rrf([dense_results, bm25_results])
print(results)
# conceptually: A and B score highest, C medium, D and E lower
```

The exact numbers matter less than the resulting order.

## Why k = 60?

`k = 60` is just a commonly used default. The constant controls how strongly rank differences affect the final score -- `1/(60+1)` vs. `1/(60+10)` differ, but not by a huge margin. This keeps the very top result from completely overwhelming everything else. You generally don't need to touch `k` unless you're actively tuning the retrieval system.

## RRF in a Bilingual RAG System

*"ما هي متطلبات CSE251؟"* -- Dense retrieval returns chunks `42, 17, 91, 12`. BM25 returns chunks `91, 42, 55, 17`. RRF notices that chunks 42, 91, and 17 rank highly in *both* lists, so they get strong combined scores -- you're now trusting evidence from multiple retrieval strategies rather than any single one.

## RRF Is Not a Reranker

This distinction matters a lot going forward. **RRF** combines results *from different retrievers* (`Dense ──┐ ├──→ RRF; BM25 ───┘`). **Reranking** takes the already-combined candidates and asks a more powerful model *"which of these is actually most relevant to this query?"* (`RRF Results → Reranker → Better ordering`). A stronger pipeline chains both:

```
                         Query
                           ↓
                ┌──────────┴──────────┐
                ↓                     ↓
             Dense                  BM25
                ↓                     ↓
                └──────────┬──────────┘
                           ↓
                          RRF
                           ↓
                    Candidate Docs
                           ↓
                       Reranker
                           ↓
                     Best Documents
                           ↓
                          LLM
```

## Why RRF Matters for Recall

If Dense retrieves `A, C, B, D, E` and BM25 retrieves `B, A, F, C, G`, using Dense alone completely misses `F` and `G`; using BM25 alone completely misses `D` and `E`. RRF lets both systems contribute, which improves retrieval *recall* -- you give the pipeline more chances to surface a genuinely useful document that only one retriever happened to find.

## The Bigger Picture

```
                     Query
                       ↓
              ┌────────┴────────┐
              ↓                 ↓
           Dense              Sparse
              ↓                 ↓
       Vector Search          BM25
              ↓                 ↓
              └────────┬────────┘
                       ↓
                      RRF
                       ↓
                Candidate Set
                       ↓
                  Reranking
                       ↓
                Relevant Context
                       ↓
                      LLM
```

*The single idea to keep:* RRF fuses ranked lists using **rank position**, not raw score, which sidesteps the score-comparability problem entirely -- and it's a *fusion* step, not a reranker, so the pipeline still benefits from an actual reranking stage afterward.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Trace an RRF Calculation",
                    "description": (
                        "Dense: 1. A, 2. B, 3. C.\n"
                        "BM25: 1. C, 2. A, 3. D.\n\n"
                        "Answer: (1) Which documents appear in both lists? "
                        "(2) Which document gets the strongest BM25 contribution? "
                        "(3) Why is RRF useful here instead of simply adding the original Dense "
                        "and BM25 scores? "
                        "(4) Is RRF a reranker, or does it combine retrieval results?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "rrf", "critical-thinking"],
                },
                {
                    "title": "Implement RRF",
                    "description": (
                        "Implement Reciprocal Rank Fusion for an arbitrary number of ranked "
                        "result lists and return documents sorted by combined RRF score, "
                        "highest first."
                    ),
                    "starter_code": (
                        "def rrf(results_lists, k=60):\n"
                        "    # TODO: for each list, walk through it with 1-based rank,\n"
                        "    # accumulate 1 / (k + rank) per document across all lists,\n"
                        "    # then return (doc, score) pairs sorted by score descending.\n"
                        "    pass\n\n"
                        "dense_results = [\"A\", \"C\", \"B\", \"D\"]\n"
                        "bm25_results = [\"B\", \"A\", \"E\", \"C\"]\n\n"
                        "print(rrf([dense_results, bm25_results]))\n"
                    ),
                    "solution_code": (
                        "def rrf(results_lists, k=60):\n"
                        "    scores = {}\n"
                        "    for results in results_lists:\n"
                        "        for rank, doc in enumerate(results, start=1):\n"
                        "            scores[doc] = scores.get(doc, 0) + 1 / (k + rank)\n"
                        "    return sorted(scores.items(), key=lambda x: x[1], reverse=True)\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "rrf", "python"],
                },
            ],
            "quiz": {
                "title": "RRF (Reciprocal Rank Fusion) — Knowledge Check",
                "questions": [
                    {
                        "question": "What does RRF actually use to combine multiple ranked lists?",
                        "options": [
                            "Each retriever's raw relevance score, normalized to 0-1",
                            "Each document's rank position within each list, ignoring the raw scores entirely",
                            "The total number of documents each retriever returned",
                            "The average embedding vector of all retrieved documents",
                        ],
                        "correct": 1,
                        "explanation": (
                            "RRF cares only about where a document ranked in each list, not the "
                            "underlying score, which sidesteps the problem of incomparable score scales."
                        ),
                    },
                    {
                        "question": (
                            "Dense ranks Document X at #1 and BM25 ranks it at #2. What does "
                            "RRF conclude from this?"
                        ),
                        "options": [
                            "Document X should be discarded because the two rankings disagree",
                            "Document X receives strong combined support because both retrievers rank it highly",
                            "Document X is ignored because RRF only uses the top-ranked result from each list",
                            "Document X's score is averaged down to a low value",
                        ],
                        "correct": 1,
                        "explanation": (
                            "When a document ranks highly across multiple retrievers, its RRF "
                            "contributions from each list add up, giving it strong combined support."
                        ),
                    },
                    {
                        "question": "What role does the constant k play in the RRF formula?",
                        "options": [
                            "It sets the maximum number of documents RRF can combine",
                            "It controls how strongly rank differences affect the final score, preventing the top result from completely dominating",
                            "It determines how many retrievers can be used at once",
                            "It converts BM25 scores into dense-compatible scores",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A commonly used default like k=60 smooths out the effect of exact "
                            "rank position so the very top result doesn't overwhelmingly dominate "
                            "the combined score."
                        ),
                    },
                    {
                        "question": "Why doesn't RRF require normalizing dense and BM25 scores first?",
                        "options": [
                            "Because RRF secretly normalizes them internally using softmax",
                            "Because RRF operates on rank positions, which are already directly comparable across retrievers",
                            "Because RRF only works when both retrievers use identical score scales already",
                            "Normalization is still required; RRF just automates it",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Ranks (1st, 2nd, 3rd...) mean the same thing regardless of which "
                            "retriever produced them, so RRF avoids the normalization step entirely "
                            "that score-based fusion would need."
                        ),
                    },
                    {
                        "question": "What is the key difference between RRF and a reranker?",
                        "options": [
                            "RRF and a reranker are two names for the same technique",
                            "RRF combines results from different retrievers into one ranking; a reranker re-evaluates the combined candidates for relevance afterward",
                            "A reranker runs before retrieval; RRF runs after generation",
                            "RRF requires an LLM; a reranker does not",
                        ],
                        "correct": 1,
                        "explanation": (
                            "RRF is a fusion step that merges multiple ranked lists into one. "
                            "Reranking is a separate, later step that re-evaluates the fused "
                            "candidates with a more powerful relevance model."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 6
            # ------------------------------------------------------------
            "title": "Reranking",
            "slug": "ai-developer-advanced-rag-reranking",
            "description": (
                "Adding a second, more careful relevance pass on top of fast "
                "hybrid retrieval, and why a two-stage recall-then-precision "
                "architecture is standard in production RAG."
            ),
            "order": 6,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "reranking", "retrieval", "recall", "precision"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Reranking",
                "content": """# Reranking

The pipeline so far:

```
Query
  ↓
Dense Retrieval ──┐
                  ├──→ RRF
BM25 ─────────────┘
                  ↓
            Candidate Documents
```

But there's still an open question: **are the top candidates actually the best documents for this exact question?** That's what reranking answers.

## What Is Reranking?

Reranking takes the documents from the first retrieval stage and re-orders them using a more accurate (and more expensive) relevance calculation. Think of retrieval as a fast first filter, and reranking as a slower, more careful second filter.

```
                    Query
                      ↓
              Fast Retrieval
             ↙             ↘
         Dense             BM25
             ↘             ↙
                   RRF
                    ↓
             20 candidates
                    ↓
                Reranker
                    ↓
              Best 5 documents
                    ↓
                   LLM
```

## Why Two Stages?

Why not just run the (expensive) reranker over the *whole* database? Because at scale that's simply too slow. If your database has 1,000,000 documents, comparing the query against all of them with a powerful reranking model is impractical.

Instead: **Stage 1 (Retrieval)** searches the entire database quickly, `1,000,000 docs → fast retrieval → 50 candidates`. **Stage 2 (Reranking)** carefully evaluates only those 50, `50 candidates → reranker → top 5`. The guiding principle: **recall first, precision second.**

## Retrieval vs. Reranking

**Retrieval** asks *"which documents might be relevant?"* Its goal is to not miss anything useful, so it favors high **recall**.

**Reranking** asks *"which of these candidates are actually the most relevant?"* Its goal is to put the best documents at the top, so it favors high **precision**.

## A Worked Example

Query: *"What are the prerequisites for CSE251?"* Hybrid Search returns 8 candidates, roughly: CSE251 course description, general Machine Learning info, CSE251 curriculum info, CSE252 prerequisites, general registration requirements, graduation requirements, CS course list, CSE251 learning outcomes.

The first stage did fine -- it surfaced the relevant CSE251 documents -- but the *ordering* isn't ideal. A reranker inspects the query against each candidate more carefully and might produce: CSE251 course description → 0.97, CSE251 curriculum info → 0.91, CSE251 learning outcomes → 0.64, CSE252 prerequisites → 0.42, general registration rules → 0.20. Now only the top few need to reach the LLM.

## How Is Reranking Different From Embeddings?

Dense retrieval compares two *independent* representations: `Query → Embedding → Query Vector`, `Document → Embedding → Document Vector`, then `similarity(Query Vector, Document Vector)`.

A reranker instead looks at **query + document together** and directly estimates relevance:

```
Query:
"What are the prerequisites for CSE251?"

          +

Document:
"CSE251 requires CSE201 and MATH201."

          ↓

      Reranker

          ↓

Relevance Score: 0.97
```

This is a much more focused judgment than comparing two embeddings computed in isolation.

## Why Reranking Improves Results

Document A: *"CSE251 is Machine Learning. It requires CSE201 and MATH201."* Document B: *"Machine learning is a field of artificial intelligence involving algorithms, statistics, and prediction."* Query: *"What are the prerequisites for CSE251?"*

Both documents are semantically related to Machine Learning, so dense retrieval might score both fairly high. A reranker, looking at the query and each document *together*, notices the query specifically asks about **prerequisites** -- Document A actually contains them, Document B only discusses the field generally. So the reranker scores A as highly relevant and B as much less relevant, which is exactly the distinction we want.

## Reranking After RRF

```
                         Query
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
       Dense Retrieval             BM25
              ↓                         ↓
              └────────────┬────────────┘
                           ↓
                          RRF
                           ↓
                   Candidate Documents
                           ↓
                       Reranker
                           ↓
                    Top Relevant Docs
                           ↓
                          LLM
```

This is a very common architecture for strong RAG systems.

## The Reranker Behind the API Call

Something like `BAAI/bge-reranker-v2-m3` used through `CrossEncoder` fits exactly here:

```python
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")

pairs = [(query, document) for document in candidates]
scores = reranker.predict(pairs)
```

What matters isn't memorizing this API -- it's understanding what's happening conceptually: `Query + Candidate Document → Reranker → Relevance Score`. You're literally asking the model, *"how relevant is this specific document to this specific question?"*

## Why Not Use the Reranker From the Start?

Computational cost. With a 1,000,000-chunk database, retrieval narrows `1,000,000 → top 50`, and reranking narrows `50 → top 5`. Running the reranker against all a million chunks directly would be far more expensive for no real benefit -- this two-tier approach is called **two-stage retrieval**: a fast, broad first stage (dense, BM25, hybrid, RRF), followed by a slow, accurate second stage (the reranker).

## Recall vs. Precision, Precisely

**Recall**: how many of the relevant documents did we successfully retrieve? If there are 10 relevant documents and your retriever finds 8, recall = 8/10 = 80%.

**Precision**: how many of the retrieved documents are actually relevant? If you retrieved 10 documents and only 7 are relevant, precision = 7/10 = 70%.

A useful (not absolute) mental model: **retrieval optimizes for recall; reranking optimizes for precision/order.**

## Reranking Can't Create New Information

If retrieval gives you `A, B, C, D, E`, the reranker can reorder them into, say, `C, A, E, B, D` -- but it **cannot** magically retrieve Document X if X was never in the candidate set to begin with. Reranking improves *ordering*; it cannot recover documents the first stage completely missed. This is exactly why retrieval quality still matters, even once you have a great reranker.

## An Analogy

Hiring: retrieval is receiving 1,000 applications and quickly filtering to 50 candidates. Reranking is a senior interviewer carefully evaluating those 50 and selecting the 5 strongest. You wouldn't ask the senior interviewer to personally review all 1,000 applications when a fast initial filter can do most of the work.

## Where the LLM Fits

```
Query
  ↓
Dense + BM25
  ↓
RRF
  ↓
Reranker
  ↓
Top documents
  ↓
Context
  ↓
LLM
  ↓
Answer
```

The LLM shouldn't have to wade through dozens of weak documents -- feeding it a small amount of *highly* relevant context improves answer quality, latency, cost, grounding, and resistance to irrelevant context.

*The single idea to keep:* retrieve broadly to protect recall, rerank carefully to protect precision, and only then generate -- reranking sharpens the order of what retrieval found, but it can never rescue what retrieval missed.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Rerank These Candidates",
                    "description": (
                        "After Hybrid Search you have:\n"
                        "A → CSE251 general description\n"
                        "B → Machine Learning theory\n"
                        "C → CSE251 prerequisites\n"
                        "D → CSE252 prerequisites\n"
                        "E → University graduation requirements\n\n"
                        "Query: \"What are the prerequisites for CSE251?\"\n\n"
                        "Answer: (1) Which document should the reranker probably put first? "
                        "(2) Why might dense retrieval have ranked Document B relatively high? "
                        "(3) Why is it useful to rerank only 20-50 candidates instead of the "
                        "entire database? "
                        "(4) Can a reranker find a document that the retrieval stage completely missed?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "reranking", "critical-thinking"],
                },
                {
                    "title": "Recall vs. Precision, Computed",
                    "description": (
                        "There are 12 truly relevant documents for a query in your corpus. "
                        "Your retriever returns 20 documents total, of which 9 are among the "
                        "12 relevant ones. Compute recall and precision for this retrieval, "
                        "then explain in one sentence which of the two a reranking stage is "
                        "primarily meant to improve."
                    ),
                    "starter_code": (
                        "relevant_total = 12\n"
                        "retrieved_total = 20\n"
                        "retrieved_relevant = 9\n\n"
                        "def recall(relevant_total, retrieved_relevant):\n"
                        "    # TODO\n"
                        "    pass\n\n"
                        "def precision(retrieved_total, retrieved_relevant):\n"
                        "    # TODO\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def recall(relevant_total, retrieved_relevant):\n"
                        "    return retrieved_relevant / relevant_total\n\n"
                        "def precision(retrieved_total, retrieved_relevant):\n"
                        "    return retrieved_relevant / retrieved_total\n\n"
                        "# recall = 9/12 = 0.75, precision = 9/20 = 0.45\n"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "reranking", "evaluation"],
                },
            ],
            "quiz": {
                "title": "Reranking — Knowledge Check",
                "questions": [
                    {
                        "question": "What does a reranker do that the first retrieval stage doesn't?",
                        "options": [
                            "It fetches new documents not found by retrieval",
                            "It re-evaluates and re-orders the already-retrieved candidates using a more accurate relevance calculation",
                            "It generates the final answer instead of the LLM",
                            "It converts documents into dense vectors for the first time",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Reranking takes the candidates retrieval already found and re-orders "
                            "them with a more careful, more expensive relevance judgment -- it "
                            "doesn't add new candidates to the pool."
                        ),
                    },
                    {
                        "question": "Why use a fast retrieval stage before an expensive reranking stage, rather than reranking everything?",
                        "options": [
                            "Reranking models cannot process more than 5 documents at once",
                            "Running an expensive relevance model against millions of documents directly would be too slow and costly",
                            "Fast retrieval always produces more accurate results than reranking",
                            "Reranking is only needed for non-English queries",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Two-stage retrieval narrows a huge corpus down with a cheap method "
                            "first, so the expensive, accurate reranker only has to evaluate a "
                            "small candidate set."
                        ),
                    },
                    {
                        "question": "In the recall-vs-precision framing, what does retrieval typically optimize for, and what does reranking typically optimize for?",
                        "options": [
                            "Retrieval optimizes precision; reranking optimizes recall",
                            "Retrieval optimizes recall; reranking optimizes precision/ordering",
                            "Both optimize exclusively for recall",
                            "Both optimize exclusively for precision",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Retrieval aims to not miss relevant documents (recall), while "
                            "reranking aims to put the truly best documents at the top of an "
                            "already-retrieved set (precision)."
                        ),
                    },
                    {
                        "question": "If retrieval returns candidates A, B, C, D, E but the truly best document, X, was never retrieved, what can reranking do about it?",
                        "options": [
                            "Reranking can still surface X because it searches the full database",
                            "Nothing -- reranking can only reorder A-E; it cannot recover a document that was never in the candidate set",
                            "Reranking will automatically request a second retrieval pass to find X",
                            "Reranking replaces missing documents with generated placeholders",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Reranking only reorders the candidates it's given -- it cannot "
                            "recover documents that the first-stage retrieval missed entirely, "
                            "which is why retrieval quality still matters."
                        ),
                    },
                    {
                        "question": "Why does feeding the LLM only the reranked top few documents (instead of dozens of weak candidates) tend to help?",
                        "options": [
                            "It has no effect on answer quality, only on cost",
                            "It can improve answer quality, latency, cost, grounding, and resistance to irrelevant context",
                            "LLMs cannot technically accept more than 5 documents of context",
                            "It removes the need for a retrieval stage entirely",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Giving the LLM a small amount of highly relevant context, rather "
                            "than many weak candidates, tends to improve answer quality, speed, "
                            "cost, and grounding."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 7
            # ------------------------------------------------------------
            "title": "Cross-Encoders",
            "slug": "ai-developer-advanced-rag-cross-encoders",
            "description": (
                "The model architecture behind most rerankers: processing query "
                "and document together for a fine-grained relevance score, and "
                "why that makes it too slow to use for initial retrieval."
            ),
            "order": 7,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "cross-encoder", "reranking", "bi-encoder"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Cross-Encoders",
                "content": """# Cross-Encoders

Reranking needs a model to actually do the reranking. One important answer is a **Cross-Encoder**.

## What Is a Cross-Encoder?

A Cross-Encoder takes the query and document **together** and directly predicts how relevant they are. Instead of `Query → Vector`, `Document → Vector`, then `Similarity`, it does:

```
Query + Document
       ↓
Cross-Encoder
       ↓
Relevance Score
```

For example:

```
Query:
"What are the prerequisites for CSE251?"

        +

Document:
"CSE251 requires CSE201 and MATH201."

        ↓

    Cross-Encoder

        ↓

Score = 0.97
```

The model directly evaluates the relationship between the two texts, rather than comparing two representations computed separately.

## Why "Cross"?

Because the model receives both pieces of text *at the same time* and lets them interact while processing:

```
Query ─────┐
           ├──→ Transformer → Score
Document ──┘
```

That interaction is what a Bi-Encoder (embedding model) doesn't allow.

## Bi-Encoder vs. Cross-Encoder

A **Bi-Encoder** (standard embedding model) encodes the query and document *separately*: `Query → Embedding Model → Query Vector`, `Document → Embedding Model → Document Vector`, then `similarity(Query Vector, Document Vector)`. This is extremely useful for searching a huge database, because you can **precompute** all document embeddings ahead of time -- `1,000,000 documents → 1,000,000 vectors` -- and at search time you only need to embed the query and search the vector database. Very fast.

A **Cross-Encoder** processes `Query + Document → Cross-Encoder → Score` for every single pair. If you have 50 candidates, you need 50 Cross-Encoder evaluations -- far more expensive than a vector similarity lookup, and completely impractical against 1,000,000 documents directly. That's why Cross-Encoders are used **after** retrieval, not instead of it.

## The Two-Stage Architecture

```
                  User Query
                      ↓
          ┌───────────┴───────────┐
          ↓                       ↓
      Dense Search              BM25
          ↓                       ↓
          └───────────┬───────────┘
                      ↓
                     RRF
                      ↓
                50 Candidates
                      ↓
                Cross-Encoder
                      ↓
                  Top 5
                      ↓
                     LLM
```

This is one of the most important architectures to internalize in Advanced RAG.

## Why a Cross-Encoder Is More Accurate

Query: *"What are the prerequisites for CSE251?"* Document A: *"CSE251 is a Machine Learning course worth 3 credit hours."* Document B: *"CSE251 requires CSE201 and MATH201 before registration."*

Both documents mention CSE251 and are about the course, so a dense embedding model might treat both as fairly relevant. A Cross-Encoder, examining the specific relationship, notices the query asks about **prerequisites** -- Document A talks about credit hours, Document B directly names the prerequisites. So it scores Document B → 0.96 and Document A → 0.48, making a much more fine-grained relevance judgment than a Bi-Encoder comparison would.

## Why Not Use a Cross-Encoder for Everything?

Speed and cost. Cross-encoding 1,000,000 query-document pairs would be far too slow and expensive. Instead: `1,000,000 → Dense + BM25 → 50 → Cross-Encoder → 5` -- fast retrieval combined with accurate reranking, each doing the part it's suited for.

## The Reranker You've Already Used

`BAAI/bge-reranker-v2-m3` via `CrossEncoder` is exactly this pattern:

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")

pairs = [(query, document) for document in documents]
scores = reranker.predict(pairs)
```

The key detail is the `(query, document)` pair -- the model sees both texts together, not two independently-computed vectors.

## A Concrete Example

```python
query = "What are the prerequisites for CSE251?"

documents = [
    "CSE251 is Machine Learning and has 3 credits.",
    "CSE251 requires CSE201 and MATH201.",
    "Machine learning uses statistical models."
]

pairs = [(query, documents[0]), (query, documents[1]), (query, documents[2])]
scores = reranker.predict(pairs)
# conceptually: [0.42, 0.96, 0.31]
```

Sorting by score: Document 2 first, then Document 1, then Document 3 -- Document 2 becomes the most important context for the LLM.

## Cross-Encoder vs. Bi-Encoder, Side by Side

| | Bi-Encoder | Cross-Encoder |
|---|---|---|
| Query encoded separately | Yes | No |
| Document encoded separately | Yes | No |
| Query + document processed together | No | Yes |
| Very fast retrieval | Yes | No |
| Good for millions of documents | Yes | No |
| Strength of relevance judgment | Good | Excellent |
| Typical RAG role | Retrieval | Reranking |

Mental shortcut: **Bi-Encoder → "find candidates quickly." Cross-Encoder → "now carefully judge these candidates."**

## An Analogy

A restaurant search over 100,000 options. A Bi-Encoder quickly narrows that to 50 based on general preferences. A Cross-Encoder then evaluates each of those 50 against your *exact* request -- *"a quiet Italian restaurant with outdoor seating"* -- producing something like Restaurant A → 95% match, B → 82%, C → 41%.

## One Important Limitation

A Cross-Encoder **cannot recover a document that retrieval never retrieved**. If the correct document is X but Dense + BM25 retrieve `A, B, C, D, E`, the Cross-Encoder only ever sees `A, B, C, D, E` -- it can't suddenly discover X. So: **bad retrieval → Cross-Encoder → still just a better ordering of bad candidates.** You need good recall *and* good reranking, not one instead of the other.

## The Complete Pipeline

```
                           QUERY
                             ↓
              ┌──────────────┴──────────────┐
              ↓                             ↓
       Dense Retrieval                  Sparse Retrieval
              ↓                             ↓
          Embeddings                      BM25
              ↓                             ↓
              └──────────────┬──────────────┘
                             ↓
                            RRF
                             ↓
                     Candidate Documents
                             ↓
                       Cross-Encoder
                             ↓
                       Top Documents
                             ↓
                          Context
                             ↓
                            LLM
                             ↓
                           Answer
```

## In a Bilingual RAG System

For *"ما هي متطلبات مقرر CSE251؟"*, the pipeline runs Dense Search and BM25 in parallel, fuses with RRF, sends the candidate chunks through a BGE Cross-Encoder, and passes the most relevant chunks to the LLM to produce **الإجابة باللغة العربية**. The Cross-Encoder is what lets the system distinguish a CSE251 *course description* from CSE251 *prerequisites* even though both are clearly about the same course.

*The single idea to keep:* a Cross-Encoder trades speed for accuracy by letting the query and document interact directly -- which is exactly why it belongs after fast retrieval, not instead of it, and why it can sharpen ordering but never rescue a document retrieval never found.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Judge the Cross-Encoder Scores",
                    "description": (
                        "Query: \"What are the prerequisites for CSE251?\"\n\n"
                        "Candidates:\n"
                        "A: \"CSE251 is a 3-credit Machine Learning course.\"\n"
                        "B: \"CSE251 requires CSE201 and MATH201.\"\n"
                        "C: \"Machine Learning is an important AI field.\"\n"
                        "D: \"CSE252 requires CSE201.\"\n\n"
                        "Answer: (1) Which document should the Cross-Encoder rank highest? "
                        "(2) Why might a basic dense retriever consider A relevant? "
                        "(3) Why is B more relevant than A? "
                        "(4) Why do we use the Cross-Encoder after initial retrieval instead "
                        "of searching the entire database with it?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "cross-encoder", "critical-thinking"],
                },
                {
                    "title": "Bi-Encoder or Cross-Encoder?",
                    "description": (
                        "For each scenario, say whether a Bi-Encoder or a Cross-Encoder is the "
                        "right tool, and justify in one sentence:\n\n"
                        "1. Searching 2 million support tickets for the top 100 candidates.\n"
                        "2. Precisely ordering 40 already-retrieved candidates before sending "
                        "5 to the LLM.\n"
                        "3. Precomputing and storing embeddings for every product in a catalog "
                        "overnight.\n"
                        "4. Deciding, between two very similar-looking passages, which one "
                        "actually answers a specific sub-question."
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "cross-encoder", "bi-encoder", "critical-thinking"],
                },
            ],
            "quiz": {
                "title": "Cross-Encoders — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the defining difference between a Cross-Encoder and a Bi-Encoder?",
                        "options": [
                            "A Cross-Encoder uses more dimensions in its output vector",
                            "A Cross-Encoder processes the query and document together, letting them interact; a Bi-Encoder encodes them separately",
                            "A Cross-Encoder is only used for translation tasks",
                            "A Bi-Encoder always produces more accurate relevance scores",
                        ],
                        "correct": 1,
                        "explanation": (
                            "The defining trait of a Cross-Encoder is joint processing of the "
                            "query and document, allowing direct interaction, unlike a Bi-Encoder "
                            "which encodes each independently."
                        ),
                    },
                    {
                        "question": "Why can a Bi-Encoder search millions of documents quickly, while a Cross-Encoder can't?",
                        "options": [
                            "Bi-Encoders use smaller neural networks",
                            "Document embeddings can be precomputed once with a Bi-Encoder, but a Cross-Encoder must process each query-document pair fresh at search time",
                            "Cross-Encoders can only run on CPUs",
                            "Bi-Encoders don't need a vector database",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Bi-Encoder document vectors can be computed once, ahead of time, and "
                            "reused for every query. A Cross-Encoder has to jointly process each "
                            "new query-document pair, which doesn't scale to millions of documents."
                        ),
                    },
                    {
                        "question": (
                            "Two documents both mention 'CSE251' and are about Machine Learning, "
                            "but only one actually lists prerequisites. Why might a Cross-Encoder "
                            "distinguish them better than a Bi-Encoder similarity score?"
                        ),
                        "options": [
                            "The Cross-Encoder ignores the word CSE251 entirely",
                            "The Cross-Encoder examines the specific relationship between the exact query and each document, rather than comparing two independently-computed vectors",
                            "Bi-Encoders cannot process documents about courses",
                            "Cross-Encoders always assign a score of 1.0 to exact keyword matches",
                        ],
                        "correct": 1,
                        "explanation": (
                            "By processing query and document jointly, a Cross-Encoder can pick "
                            "up on fine-grained relevance -- like whether prerequisites are "
                            "actually mentioned -- that two separately-computed embeddings might miss."
                        ),
                    },
                    {
                        "question": "In a typical RAG pipeline, what role does a Cross-Encoder usually play?",
                        "options": [
                            "Initial retrieval across the entire document database",
                            "Reranking a small set of already-retrieved candidates",
                            "Generating the final natural-language answer",
                            "Chunking documents before embedding",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Cross-Encoders are typically used as rerankers on a small candidate "
                            "set produced by faster retrieval methods, not for searching the full "
                            "database directly."
                        ),
                    },
                    {
                        "question": "If Dense + BM25 retrieval never includes the truly best document X in its candidates, what happens when a Cross-Encoder reranks that candidate set?",
                        "options": [
                            "The Cross-Encoder will still surface X by searching beyond the given candidates",
                            "The Cross-Encoder can only reorder the candidates it was given -- it cannot introduce X",
                            "The pipeline automatically restarts retrieval to find X",
                            "The Cross-Encoder replaces the missing document with a generated summary",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A Cross-Encoder reranks only the candidates it receives -- it has no "
                            "way to recover a relevant document that retrieval failed to surface "
                            "in the first place."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 8
            # ------------------------------------------------------------
            "title": "Query Rewriting",
            "slug": "ai-developer-advanced-rag-query-rewriting",
            "description": (
                "Transforming a user's raw question into a clearer retrieval "
                "query -- resolving pronouns and conversational noise -- while "
                "preserving their original intent."
            ),
            "order": 8,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "query-rewriting", "retrieval", "llm"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Query Rewriting",
                "content": """# Query Rewriting

The pipeline so far: `Query → Dense + BM25 → RRF → Cross-Encoder → Best documents`. But there's still a gap upstream of all of it: **what if the user's original question isn't a good search query in the first place?** That's what Query Rewriting solves.

## What Is Query Rewriting?

Query rewriting transforms the user's original question into a better query *for retrieval*. Critically, it does **not** change what the user wants -- it changes the *search representation* of their question.

User: *"What do I need to take before this course?"* -- vague on its own. A query-rewriting system might turn it into: *"Prerequisites for CSE251."* Retrieval then runs on the rewritten query.

## Why It's Needed

Users don't naturally phrase things for retrieval. They use pronouns, vague language, conversational filler, long rambling questions, missing keywords, and references to earlier messages. *"What about its prerequisites?"* is perfectly clear to a human following the conversation -- a retriever has no built-in way to know what "its" refers to.

## The Basic Architecture

Without rewriting: `User Question → Retriever → Documents`. With rewriting: `User Question → Query Rewriter → Better Search Query → Retriever → Documents`. **Query rewriting happens before retrieval.**

## A Conversation Example

```
User: What is CSE251?
Assistant: CSE251 is Machine Learning.
User: What are its prerequisites?
```

Send *"What are its prerequisites?"* straight to a vector database, and "its" is unresolved -- the conversation knows the referent, but the retrieval system doesn't. A query rewriter resolves this into *"What are the prerequisites for CSE251?"* -- now retrieval has a clear, self-contained query.

## Rewriting Does Not Answer the Question

This distinction matters. The rewriter's job is `Question → Better Search Query`, **not** `Question → Answer`. The full flow stays: `Better Search Query → Retrieval → Context → LLM → Answer`. The rewriter is part of the *retrieval* pipeline, not the *answering* stage.

## Removing Conversational Noise

*"Hey, can you please tell me exactly how many credit hours I need if I want to graduate from the AI Engineering program?"* really wants one thing: `credit hours required for AI Engineering graduation`. A rewrite like *"AI Engineering graduation required credit hours"* is far more focused for retrieval.

## Making Implicit Information Explicit

If the prior turn established *"CSE251 is Machine Learning"* and the user then asks *"What do I need before taking it?"*, the rewriter can produce *"CSE251 Machine Learning prerequisites"* -- explicitly naming the entity that "it" referred to. That's a meaningfully better input for BM25, dense retrieval, and hybrid search alike.

## Implementing It With an LLM

```python
rewrite_prompt = \"\"\"
Rewrite the user's question into a concise
search query for a knowledge base.

Conversation:
{conversation}

User question:
{question}

Return only the search query.
\"\"\"

rewritten_query = llm.invoke(rewrite_prompt)
```

Given the conversation *"What is CSE251?" → "CSE251 is Machine Learning."* and the question *"What are its prerequisites?"*, the LLM might produce simply `CSE251 prerequisites` -- which is what gets searched.

## Where It Fits in the Full Pipeline

```
                     User Question
                           ↓
                    Query Rewriter
                           ↓
                   Better Search Query
                           ↓
             ┌─────────────┴─────────────┐
             ↓                           ↓
       Dense Retrieval               BM25
             ↓                           ↓
             └─────────────┬─────────────┘
                           ↓
                          RRF
                           ↓
                     Candidates
                           ↓
                    Cross-Encoder
                           ↓
                    Best Documents
                           ↓
                          LLM
```

## Rewriting Substantially Helps BM25

`"What about it?"` gives BM25 almost nothing to work with -- no meaningful terms at all. After rewriting to `"CSE251 prerequisites"`, BM25 suddenly has `CSE251` and `prerequisites` -- two excellent lexical search terms. Query rewriting can dramatically improve sparse retrieval's effectiveness.

## It Also Helps Dense Retrieval

`"How many do I need?"` is semantically ambiguous on its own. Rewritten to `"How many credit hours are required for AI Engineering graduation?"`, the embedding now represents a much clearer concept: `Bad Query → Poor embedding → Poor retrieval` becomes `Clear Query → Better embedding → Better retrieval`.

## Rewriting Isn't Always Necessary

Don't automatically run every query through an LLM rewriter. *"What are the prerequisites for CSE251?"* is already an excellent search query -- rewriting it into *"CSE251 course prerequisites"* may improve nothing, while still costing extra latency, extra API spend, another model call, and another possible point of failure. A good system rewrites when it's actually needed, not unconditionally.

## The Big Risk: Changing Meaning

Original: *"What are the prerequisites for CSE251?"* Bad rewrite: *"What courses should I take to graduate?"* -- that is **not** the same question; the rewriter has silently changed the user's intent, and retrieval will now find the wrong documents. The governing rule: **improve the query without changing the user's intent.**

## Rewriting vs. Expansion

**Query Rewriting** turns one query into a *clearer version of the same query*: `"What about its prerequisites?" → "CSE251 prerequisites"`. **Query Expansion** *adds* related terms or concepts: `"CSE251 prerequisites" → "CSE251 prerequisites, required courses, prerequisite subjects, course requirements"`. The next lesson covers expansion in depth.

## In a Bilingual RAG System

*"طب والمادة دي محتاجة إيه قبل ما أسجلها؟"* could be rewritten into *"متطلبات التسجيل السابقة لمقرر CSE251"* -- an explicit Arabic search query that then flows through Dense + BM25 → RRF → Cross-Encoder → relevant academic chunks. This matters most when users interact conversationally rather than typing formal search queries.

## The Core Engineering Idea

Query rewriting is a bridge between human language and retrieval language: `Human Query → Query Rewriting → Retrieval-Friendly Query`. Users speak naturally and conversationally; the retrieval system wants something explicit and self-contained -- rewriting is what closes that gap.

*The single idea to keep:* rewriting makes a query clearer for retrieval without changing what the user actually meant -- and skipping it when the original query is already clear saves latency and cost without losing anything.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Resolve the Reference",
                    "description": (
                        "Conversation:\n"
                        "User: What is CSE251?\n"
                        "Assistant: CSE251 is Machine Learning.\n"
                        "User: What about its prerequisites?\n\n"
                        "Answer: (1) Why might the original query be difficult for retrieval? "
                        "(2) What would be a good rewritten query? "
                        "(3) Should the rewritten query change the user's intent? "
                        "(4) Why shouldn't we rewrite every query automatically?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "query-rewriting", "critical-thinking"],
                },
                {
                    "title": "Spot the Bad Rewrite",
                    "description": (
                        "For each pair, decide whether the rewrite preserves the user's intent "
                        "or silently changes it, and explain why:\n\n"
                        "1. Original: \"What are the prerequisites for CSE251?\" → Rewrite: "
                        "\"CSE251 prerequisite courses\"\n"
                        "2. Original: \"What are the prerequisites for CSE251?\" → Rewrite: "
                        "\"What courses should I take to graduate?\"\n"
                        "3. Original: \"What about its credit hours?\" (after discussing CSE251) "
                        "→ Rewrite: \"CSE251 credit hours\"\n"
                        "4. Original: \"How many credits does CSE251 have?\" → Rewrite: "
                        "\"CSE251 registration deadline\""
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "query-rewriting", "critical-thinking"],
                },
            ],
            "quiz": {
                "title": "Query Rewriting — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the goal of query rewriting?",
                        "options": [
                            "To directly answer the user's question without retrieval",
                            "To transform the user's question into a clearer retrieval query while preserving their original intent",
                            "To translate the query into another language",
                            "To shorten every query to a single keyword",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Query rewriting improves how a question is represented for search "
                            "-- resolving vague or conversational phrasing -- without changing "
                            "what the user actually wants to know."
                        ),
                    },
                    {
                        "question": (
                            "In a multi-turn conversation, why does a query like 'What about its "
                            "prerequisites?' cause a problem for retrieval on its own?"
                        ),
                        "options": [
                            "Retrieval systems cannot process questions with pronouns at all",
                            "The retriever has no built-in way to resolve what 'its' refers to from earlier conversation turns",
                            "The query is too long for an embedding model",
                            "BM25 cannot process questions, only statements",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A retriever sees only the current query text, not conversational "
                            "context, so unresolved pronouns like 'its' leave it with an ambiguous "
                            "search target."
                        ),
                    },
                    {
                        "question": "Where does query rewriting sit in the RAG pipeline?",
                        "options": [
                            "After the LLM generates its final answer",
                            "Before retrieval, transforming the question into a better search query",
                            "Inside the reranker, replacing the Cross-Encoder",
                            "It replaces the retrieval stage entirely",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Query rewriting happens before retrieval -- it produces the query "
                            "that then gets sent to dense and sparse retrieval."
                        ),
                    },
                    {
                        "question": (
                            "A rewrite turns 'What are the prerequisites for CSE251?' into 'What "
                            "courses should I take to graduate?' What has gone wrong?"
                        ),
                        "options": [
                            "Nothing -- this is a valid rewrite that keeps the same intent",
                            "The rewrite changed the user's actual intent, so retrieval will now find the wrong documents",
                            "The rewrite is too similar to the original to be useful",
                            "The rewrite made the query too short for BM25",
                        ],
                        "correct": 1,
                        "explanation": (
                            "The rewritten query asks a fundamentally different question than the "
                            "original, violating the core rule that rewriting should improve "
                            "clarity without changing intent."
                        ),
                    },
                    {
                        "question": "Why shouldn't every query automatically be sent through an LLM rewriter?",
                        "options": [
                            "LLMs cannot process short queries",
                            "Rewriting an already-clear query adds unnecessary latency, cost, and risk of failure with little benefit",
                            "Rewriting is illegal in production RAG systems",
                            "Only Arabic queries benefit from rewriting",
                        ],
                        "correct": 1,
                        "explanation": (
                            "If a query is already a good search query, rewriting it may not "
                            "improve retrieval at all, while still incurring extra cost, latency, "
                            "and another possible point of failure."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 9
            # ------------------------------------------------------------
            "title": "Query Expansion",
            "slug": "ai-developer-advanced-rag-query-expansion",
            "description": (
                "Broadening a query with related terms to bridge vocabulary "
                "gaps between users and documents -- and the query-drift risk "
                "that makes over-expansion dangerous."
            ),
            "order": 9,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "query-expansion", "retrieval", "llm"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Query Expansion",
                "content": """# Query Expansion

Query Rewriting made a question *clearer* while keeping the same intent. **Query Expansion** goes a step further: it adds related terms or concepts to increase the chance of retrieving relevant documents.

## The Basic Idea

*"How do I graduate?"* is a short query. The knowledge base might phrase the same idea with terms like `graduation`, `graduation requirements`, `degree completion`, `credit hours`, `academic requirements`. The user's query only contains `graduate`. Expansion can add the related terminology directly: `graduate, graduation, graduation requirements, degree completion, credit hours, academic requirements` -- giving retrieval far more ways to find the relevant content.

## Rewriting vs. Expansion

**Rewriting**: one query → a better version of the *same* query. `"What do I need before taking it?" → "CSE251 prerequisites"`. The original is *replaced*.

**Expansion**: one query → more related information *added on top*. `"CSE251 prerequisites" → "CSE251 prerequisites, required courses, prerequisite subjects, course requirements"`. The original concept is *broadened*.

Mental shortcut: **rewriting → make it clearer. Expansion → make it broader.**

## Why Broaden at All?

Because users and documents often use different vocabulary. If a document says *"Students must satisfy the prerequisite courses before enrollment"* and the user asks *"What classes do I need before registering?"*, there's a real vocabulary gap: *classes/before registering* vs. *courses/prerequisite/enrollment*. A good expansion can bridge exactly that gap.

## Expansion Helps BM25 Directly

`"graduation requirements"` expanded to `"graduation requirements, degree requirements, degree completion, credit hours, graduation criteria"` gives a lexical retriever like BM25 far more useful terms to match against.

## It Can Help Dense Retrieval Too

This isn't only a BM25 technique. `"How many credits do I need?"` expanded to include `credit hours, graduation requirements, degree completion, academic credits, required credits` gives the embedding more surrounding context about the user's actual intent, which can improve semantic retrieval as well.

## LLM-Generated Expansion

```python
prompt = \"\"\"
Generate related search terms for this query.

Query:
What are the requirements for graduating?

Return 5 relevant terms.
\"\"\"
```

The model might return: `graduation requirements, degree requirements, credit hours, degree completion, graduation criteria` -- terms that can then be folded into the retrieval query.

## A Related but Distinct Approach: Multiple Queries

Instead of packing extra terms into *one* query, you can generate several *separate* queries: `"How can I graduate?"` becomes `graduation requirements`, `required credit hours for graduation`, `degree completion requirements`, `courses required for graduation` -- each searched independently. This is edging toward **Multi-Query Retrieval**, a related but distinct technique.

**Expansion**: `Original → Expanded Query → one retrieval operation`.
**Multi-query retrieval**: `Original → Q1, Q2, Q3, Q4 → separate retrievals → combine results`.

Expansion broadens *one* search; multi-query performs *multiple* searches.

## In a Bilingual RAG System

*"عايز أعرف شروط التخرج"* could be expanded into `شروط التخرج, متطلبات التخرج, الساعات المعتمدة المطلوبة للتخرج, شروط الحصول على الدرجة, متطلبات إتمام البرنامج` -- giving the retrieval system considerably more vocabulary to match against a knowledge base that may phrase the same requirements differently.

## Especially Useful for BM25

If a document says *"The student must complete the required academic credits"* and the user asks *"How many units do I need?"*, there may be almost no lexical overlap at all. Expansion introducing `academic credits, required credits, credit hours, degree requirements` gives BM25 real opportunities to match that it otherwise wouldn't have had.

## The Risk: Query Drift

More terms are not automatically better. Expand `"What is CSE251?"` into `CSE251, Machine Learning, Deep Learning, Artificial Intelligence, Computer Vision, Data Science, program requirements, course prerequisites`, and the query has become far too broad -- retrieval may now return anything loosely related to AI or university courses. This gradual drift away from what the user actually asked is called **query drift**, and it's dangerous precisely because it looks like "more thorough" search while actually degrading relevance. The rule: **expand the query, but stay close to the original intent.**

## The Hallucination Risk

If a user asks *"What are the prerequisites for CSE251?"* and an LLM incorrectly generates `CSE201, MATH201, STAT201` as expansion terms -- but STAT201 isn't actually a prerequisite -- using those generated terms for retrieval has quietly introduced incorrect information into the search. Query expansion should generate **search concepts**, not invent **factual claims**. Safer: `CSE251 prerequisites, required courses, prerequisite subjects, course enrollment requirements`. Riskier (because it asserts unverified facts): `CSE251 requires CSE201, MATH201, STAT201`.

## In a Production Pipeline

```
                     User Query
                          ↓
                   Query Analysis
                          ↓
                  Query Expansion
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
         Dense Retrieval          BM25
              ↓                       ↓
              └───────────┬───────────┘
                          ↓
                         RRF
                          ↓
                    Candidate Docs
                          ↓
                    Cross-Encoder
                          ↓
                     Top Context
                          ↓
                         LLM
```

## When Expansion Helps

It's especially valuable when users use informal language while documents use formal terminology (*"How do I finish uni?"* vs. *graduation requirements*), when there are many synonyms (*car/automobile/vehicle*), when the domain has specialized vocabulary (*authentication/OAuth/OAuth2/JWT/access token*), or generally wherever documents and users describe the same thing differently -- common in legal, medical, academic, and enterprise/technical documentation.

## When to Avoid It

Don't expand aggressively when the query is already precise (`"CSE251"`), when the user is asking for an exact identifier (`"REG-2025-17A"`), or when the query is already very specific (*"What is the deadline for registration in Fall 2026?"*). Adding related concepts in these cases can actively hurt retrieval.

## A Practical Strategy

Rather than expanding every query unconditionally:

```
Query
  ↓
Is query ambiguous or too short?
  │
 ┌┴──────────────┐
No              Yes
 │                │
 ↓                ↓
Normal          Expand
Retrieval          │
 └────────┬────────┘
          ↓
       Retrieval
```

This conditional approach reduces unnecessary LLM calls, latency, cost, and query drift.

## The Bigger Picture

```
                           User
                            ↓
                       Query
                            ↓
                  ┌─────────┴─────────┐
                  ↓                   ↓
              Rewriting            Expansion
                  └─────────┬─────────┘
                            ↓
                   Retrieval Pipeline
                            ↓
               ┌────────────┴────────────┐
               ↓                         ↓
           Dense Search               BM25
               ↓                         ↓
               └────────────┬────────────┘
                            ↓
                           RRF
                            ↓
                     Candidate Docs
                            ↓
                     Cross-Encoder
                            ↓
                      Top Documents
                            ↓
                           LLM
```

*The single idea to keep:* expansion trades precision for recall by adding related terms -- valuable when there's a real vocabulary gap between users and documents, dangerous when it drifts the search away from the user's actual intent or invents facts that were never verified.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Expand vs. Don't",
                    "description": (
                        "User asks: \"How do I finish university?\" Your knowledge base uses "
                        "the terms: graduation requirements, degree completion, required credit "
                        "hours, graduation criteria.\n\n"
                        "Answer: (1) Why might query expansion help here? "
                        "(2) Give 3 useful expanded terms. "
                        "(3) Why would this be useful for BM25? "
                        "(4) What is query drift? "
                        "(5) Would you aggressively expand the query \"CSE251\"? Why or why not?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "query-expansion", "critical-thinking"],
                },
                {
                    "title": "Safe vs. Risky Expansion",
                    "description": (
                        "For the query \"What are the prerequisites for CSE251?\", one expansion "
                        "produces \"CSE251 prerequisites, required courses, prerequisite "
                        "subjects, course enrollment requirements\" and another produces \"CSE251 "
                        "requires CSE201, MATH201, STAT201\". Explain which is safer and why, "
                        "specifically in terms of what each expansion is asserting."
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "query-expansion", "critical-thinking"],
                },
            ],
            "quiz": {
                "title": "Query Expansion — Knowledge Check",
                "questions": [
                    {
                        "question": "What does query expansion do to a search query?",
                        "options": [
                            "Replaces it with a completely different question",
                            "Adds related terms or concepts to increase the chance of matching relevant documents",
                            "Shortens it to a single keyword for speed",
                            "Translates it into the language of the document collection",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Query expansion broadens a query by adding related vocabulary, "
                            "rather than replacing or shortening it."
                        ),
                    },
                    {
                        "question": "What is the key difference between query rewriting and query expansion?",
                        "options": [
                            "Rewriting adds new terms; expansion clarifies existing ones",
                            "Rewriting makes the query clearer while keeping the same scope; expansion makes it broader by adding related terms",
                            "They are the same technique with different names",
                            "Rewriting only works for Arabic queries; expansion only works for English",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Rewriting replaces the query with a clearer version of the same "
                            "question; expansion adds related terms on top to broaden retrieval "
                            "coverage."
                        ),
                    },
                    {
                        "question": "Why might expanding 'How many units do I need?' with terms like 'academic credits' and 'credit hours' help BM25?",
                        "options": [
                            "BM25 ignores the original query entirely once expanded",
                            "It introduces terms that may actually appear in the documents, giving BM25 more chances to find a lexical match",
                            "BM25 cannot process queries shorter than 5 words",
                            "Expansion converts the query into an embedding automatically",
                        ],
                        "correct": 1,
                        "explanation": (
                            "BM25 relies on literal term overlap, so adding terms that likely "
                            "appear in the target documents gives it more opportunities to match, "
                            "bridging a vocabulary gap."
                        ),
                    },
                    {
                        "question": "What is 'query drift'?",
                        "options": [
                            "When a query is automatically translated into another language",
                            "When excessive expansion gradually moves the search away from the user's actual intent, returning increasingly irrelevant results",
                            "When a retriever's index becomes outdated over time",
                            "When a user changes their question mid-conversation",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Query drift happens when too many related-but-tangential terms are "
                            "added, broadening the search so much that it no longer reflects what "
                            "the user actually asked."
                        ),
                    },
                    {
                        "question": (
                            "Why is it risky for an LLM to expand 'What are the prerequisites for "
                            "CSE251?' into 'CSE251 requires CSE201, MATH201, STAT201' if STAT201 "
                            "isn't actually a prerequisite?"
                        ),
                        "options": [
                            "It isn't risky -- more specific terms always improve retrieval",
                            "The expansion asserts an unverified fact rather than just generating related search concepts, which can inject incorrect information into retrieval",
                            "The query becomes too short for effective retrieval",
                            "STAT201 will be automatically filtered out by the retriever",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Good expansion generates plausible search concepts, not factual "
                            "claims -- asserting specific prerequisites that may be wrong "
                            "introduces hallucinated information into the retrieval process."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 10
            # ------------------------------------------------------------
            "title": "Multi-Query Retrieval",
            "slug": "ai-developer-advanced-rag-multi-query-retrieval",
            "description": (
                "Generating several different search queries from one user "
                "question and retrieving with each of them, to improve recall "
                "when a single query can't capture every relevant angle."
            ),
            "order": 10,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "multi-query", "retrieval", "recall", "rrf"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Multi-Query Retrieval",
                "content": """# Multi-Query Retrieval

So far: **Query Rewriting** makes one query clearer, and **Query Expansion** adds related terms to that one query. **Multi-Query Retrieval** goes further still -- it creates *multiple different queries* and searches with all of them. It's especially useful when a single query can't capture every way relevant information might be expressed.

## The Core Idea

Normally: `User Query → One Search → Documents`. With multi-query retrieval:

```
                 User Query
                     ↓
              Query Generator
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
       Q1           Q2           Q3
        ↓            ↓            ↓
    Retrieval    Retrieval    Retrieval
        ↓            ↓            ↓
        └────────────┼────────────┘
                     ↓
               Combine Results
                     ↓
                  Rerank
```

Instead of betting everything on one search formulation, you run several searches from different angles.

## Why Multiple Queries?

*"What do I need to graduate from the AI Engineering program?"* could mean required credit hours, graduation requirements, required courses, academic conditions, or degree completion requirements. A single query might catch some of these and miss others. So you generate several: `AI Engineering graduation requirements`, `AI Engineering required credit hours`, `AI Engineering required courses for graduation`, `AI Engineering degree completion requirements` -- and search the knowledge base with each one separately.

## Different Queries Find Different Documents

Query 1 (*"graduation requirements"*) retrieves `A, B, C`. Query 2 (*"required credit hours"*) retrieves `B, D, E`. Query 3 (*"degree completion requirements"*) retrieves `A, E, F`. Combined: `A, B, C, D, E, F` -- candidate recall has increased simply by asking the question multiple ways.

## The Main Reason It Exists

The goal is almost always: **improve recall by searching for the same underlying information from multiple query formulations.** Recall, as covered earlier, is how much of the relevant information you actually managed to retrieve -- multi-query retrieval gives the system more independent chances to find it.

## In a Bilingual RAG System

*"إيه شروط التخرج من هندسة الذكاء الاصطناعي؟"* could generate several Arabic query variants -- `شروط التخرج من برنامج هندسة الذكاء الاصطناعي`, `متطلبات الحصول على درجة هندسة الذكاء الاصطناعي`, `الساعات المعتمدة المطلوبة للتخرج`, `المقررات المطلوبة لإتمام برنامج هندسة الذكاء الاصطناعي` -- each run through Dense + BM25, with the results merged afterward.

## Multi-Query Is Not Query Expansion

This is the key distinction to hold onto. **Expansion** turns one query into a broader *single* query: `"CSE251 prerequisites" → "CSE251 prerequisites required courses enrollment"` -- still one search. **Multi-query** turns one query into *several separate* queries: `"CSE251 prerequisites" → Q1: CSE251 prerequisites, Q2: courses required before CSE251, Q3: CSE251 enrollment requirements` -- three separate searches. **Expansion broadens one search; multi-query performs multiple searches.**

## Different Perspectives, Not Just Synonyms

For *"How can I register for CSE251?"*, useful generated queries might be `CSE251 registration requirements`, `CSE251 prerequisites`, `requirements for enrolling in CSE251`, `CSE251 registration conditions`. These aren't just synonyms of each other -- they're genuinely different interpretations of what information is needed. One document might use "registration requirements," another "prerequisite courses," another "enrollment conditions." Multiple queries raise the odds of hitting whichever phrasing the right document actually uses.

## The Retrieval Architecture

```
User Query
    ↓
LLM generates 4 queries
    ↓
┌───────┬───────┬───────┬───────┐
↓       ↓       ↓       ↓
Q1      Q2      Q3      Q4
↓       ↓       ↓       ↓
Search  Search  Search  Search
└───────┴───────┴───────┴───────┘
             ↓
       Merge Documents
             ↓
           RRF
             ↓
        Cross-Encoder
             ↓
          Top-K
             ↓
            LLM
```

RRF is a natural fit here, because you now have *multiple* ranked lists to combine, not just two (dense and sparse).

## Multi-Query + RRF

If `Q1 → A, B, C`, `Q2 → B, D, E`, and `Q3 → C, B, F`, then Document `B` appears in *all three* result lists and receives strong combined support from RRF -- documents that keep showing up near the top across multiple query formulations are exactly the ones RRF is designed to surface.

## Why This Can Outperform a Single Search

If one document uses *"degree completion criteria,"* another uses *"minimum required credit hours,"* and another uses *"courses required for degree completion,"* a single query like *"How do I graduate?"* has to rely on dense retrieval catching all three phrasings at once. Multiple queries give the system multiple independent retrieval *paths* -- one query, one path; multiple queries, multiple paths, more chances to discover relevant documents.

## LLM-Generated Queries

```python
prompt = \"\"\"
Generate 4 different search queries that help retrieve
documents needed to answer the user's question.

User question:
{question}

Each query should focus on a different aspect.
Return only the queries.
\"\"\"
```

For *"What are the requirements to graduate?"*, the LLM might generate: `graduation requirements`, `required credit hours for graduation`, `required courses for degree completion`, `academic conditions for graduation` -- and your retriever searches all four.

## The Queries Should Share a Goal

Don't let the generator drift: `Q1 → graduation requirements`, `Q2 → university admission requirements`, `Q3 → tuition fees`, `Q4 → dormitory requirements` are four *different topics*, not four angles on the same question. The generated queries should represent different ways of finding information relevant to *the same* underlying question.

## The Danger of Too Many Queries

Generating 100 queries sounds thorough but creates real problems: 100 retrieval operations means higher latency, higher compute cost, more irrelevant documents pulled in, more deduplication work, and more reranking work. A small number of *good* queries beats a huge number of mediocre ones -- **3-5 queries** is a reasonable starting point, though the right number depends on the application and should be evaluated, not fixed blindly.

## Another Danger: Duplicates

If `Q1 → A, B, C, D`, `Q2 → A, B, E, F`, and `Q3 → A, B, G, H`, you don't want `A, B, A, B, A, B, ...` sent downstream. After multi-query retrieval you typically: combine results, **deduplicate documents**, fuse rankings (RRF), then rerank the deduplicated candidates.

## Multi-Query Doesn't Replace Reranking

Each component has a distinct job. **Multi-query** finds more potentially useful documents. **RRF** combines multiple rankings into one. **Cross-Encoder** carefully judges candidate relevance. The chain: `Multi-query → more candidates → RRF → unified ranking → Cross-Encoder → best candidates`.

## The Pipeline So Far

```
                              User
                               ↓
                              Query
                               ↓
                    Query Rewriting / Analysis
                               ↓
                      Multi-Query Generation
                               ↓
             ┌─────────────────┼─────────────────┐
             ↓                 ↓                 ↓
            Q1                Q2                Q3
             ↓                 ↓                 ↓
       Dense + BM25      Dense + BM25      Dense + BM25
             ↓                 ↓                 ↓
             └─────────────────┼─────────────────┘
                               ↓
                              RRF
                               ↓
                         Candidate Docs
                               ↓
                        Cross-Encoder
                               ↓
                         Top Documents
                               ↓
                              LLM
```

This is a considerably more advanced architecture than a basic `Query → Vector DB → LLM` pipeline.

## When to Use It

Multi-query retrieval helps when the question is genuinely complex (*"What courses, credit requirements, and academic conditions do I need to graduate?"*), when vocabulary varies significantly between users and documents, or when a question naturally has multiple valid interpretations worth exploring separately.

## When Not to Bother

For a very precise question like *"What is the credit-hour value of CSE251?"*, one good query is likely enough -- generating four variants adds latency without adding value. As always: **Advanced RAG doesn't mean applying every technique to every query; a good AI Engineer picks the technique that fits the problem.**

*The single idea to keep:* multi-query retrieval trades extra retrieval calls for higher recall by asking the same underlying question from several angles -- valuable when phrasing genuinely varies across documents, wasteful when the question is already precise and unambiguous.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Generate Multi-Query Variants",
                    "description": (
                        "User asks: \"What are the requirements for graduating from the AI "
                        "Engineering program?\"\n\n"
                        "Create 3 useful search queries that could be generated for Multi-Query "
                        "Retrieval, then answer: "
                        "(1) Why are these queries better than simply repeating the original "
                        "question three times? "
                        "(2) Why could RRF be useful after running these searches? "
                        "(3) Why shouldn't we generate 100 queries? "
                        "(4) What's the difference between Multi-Query Retrieval and Query Rewriting?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "multi-query", "critical-thinking"],
                },
                {
                    "title": "Merge and Deduplicate Multi-Query Results",
                    "description": (
                        "Given the retrieval results for three separate queries (each a list of "
                        "document IDs, possibly with overlaps), write a function that returns a "
                        "deduplicated list of all documents that appeared in at least one query's "
                        "results, preserving first-seen order."
                    ),
                    "starter_code": (
                        "q1_results = [\"A\", \"B\", \"C\", \"D\"]\n"
                        "q2_results = [\"A\", \"B\", \"E\", \"F\"]\n"
                        "q3_results = [\"A\", \"B\", \"G\", \"H\"]\n\n"
                        "def merge_and_dedupe(*result_lists):\n"
                        "    # TODO: return a single list of unique document IDs across all\n"
                        "    # result_lists, preserving the order each ID first appears in.\n"
                        "    pass\n\n"
                        "print(merge_and_dedupe(q1_results, q2_results, q3_results))\n"
                    ),
                    "solution_code": (
                        "def merge_and_dedupe(*result_lists):\n"
                        "    seen = set()\n"
                        "    merged = []\n"
                        "    for results in result_lists:\n"
                        "        for doc in results:\n"
                        "            if doc not in seen:\n"
                        "                seen.add(doc)\n"
                        "                merged.append(doc)\n"
                        "    return merged\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "multi-query", "python"],
                },
            ],
            "quiz": {
                "title": "Multi-Query Retrieval — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the primary purpose of Multi-Query Retrieval?",
                        "options": [
                            "To translate the query into multiple languages",
                            "To improve recall by searching for the same underlying information using several different query formulations",
                            "To replace the reranking stage entirely",
                            "To reduce the number of documents retrieved",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Multi-query retrieval generates several queries targeting the same "
                            "underlying question to increase the chance of finding relevant "
                            "documents phrased differently across the corpus."
                        ),
                    },
                    {
                        "question": "How does Multi-Query Retrieval differ from Query Expansion?",
                        "options": [
                            "They are the same technique with different names",
                            "Expansion broadens one query into one search; multi-query generates several separate queries and performs multiple searches",
                            "Multi-query only works with BM25, while expansion only works with dense retrieval",
                            "Expansion always produces more queries than multi-query",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Query expansion adds related terms to a single query for one "
                            "retrieval operation; multi-query retrieval produces multiple distinct "
                            "queries, each searched separately."
                        ),
                    },
                    {
                        "question": (
                            "If Document B appears in the top results of three separate "
                            "multi-query searches, what does RRF do with that signal?"
                        ),
                        "options": [
                            "It discards B because it appeared multiple times",
                            "It accumulates B's rank-based contributions across all three lists, giving it strong combined support",
                            "It averages B's position down to the lowest of the three ranks",
                            "RRF cannot be used when there are more than two ranked lists",
                        ],
                        "correct": 1,
                        "explanation": (
                            "RRF sums rank-based contributions across every list a document "
                            "appears in, so a document that ranks well across multiple query "
                            "variants accumulates strong combined support."
                        ),
                    },
                    {
                        "question": "Why is generating 100 queries for multi-query retrieval generally a bad idea?",
                        "options": [
                            "LLMs are physically incapable of generating more than 10 queries",
                            "It significantly increases latency, compute cost, irrelevant documents, and reranking work without proportional benefit",
                            "Vector databases reject more than 5 simultaneous queries",
                            "BM25 cannot process more than 10 queries per session",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A small number of well-chosen queries (often 3-5) is typically more "
                            "effective than a huge number of queries, which adds cost, latency, "
                            "and noise without a proportional recall benefit."
                        ),
                    },
                    {
                        "question": (
                            "For the query 'What is the credit-hour value of CSE251?', why might "
                            "multi-query retrieval add little value?"
                        ),
                        "options": [
                            "Multi-query retrieval only works for Arabic queries",
                            "The question is already precise and unambiguous, so generating several variants adds latency without meaningfully improving recall",
                            "CSE251 is not a valid search term",
                            "Precise queries cannot be processed by BM25",
                        ],
                        "correct": 1,
                        "explanation": (
                            "When a query is already specific and unambiguous, one good search "
                            "is typically sufficient -- generating multiple variants mainly adds "
                            "cost and latency in that case."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 11
            # ------------------------------------------------------------
            "title": "Parent-Child Retrieval",
            "slug": "ai-developer-advanced-rag-parent-child-retrieval",
            "description": (
                "Retrieving with small, precise child chunks while returning "
                "their larger parent section as context -- getting precise "
                "matching and rich context at the same time."
            ),
            "order": 11,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "parent-child-retrieval", "chunking", "retrieval"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Parent-Child Retrieval",
                "content": """# Parent-Child Retrieval

Here's a common tension in RAG: **small chunks are good for retrieval, but larger chunks are often better for understanding.** Parent-Child Retrieval is how you get both at once.

## The Problem With Normal Chunking

A document on CSE251 has sections: Description, Prerequisites, Learning Outcomes, Assessment. Split into chunks: `Chunk 1 → Description`, `Chunk 2 → Prerequisites`, `Chunk 3 → Learning Outcomes`, `Chunk 4 → Assessment`. A small chunk is great for a specific question -- *"What are the prerequisites?"* finds Chunk 2's `"CSE201 and MATH201..."` directly. But sometimes the answer really needs more surrounding context than one small chunk provides.

## The Core Idea

Parent-Child Retrieval creates two levels:

```
Parent Document / Section
        ↓
   ┌────┼────┐
   ↓    ↓    ↓
 Child Child Child
```

**Child chunks are used for retrieval. The parent chunk is returned as context.** In short: **search small, return large.**

## Why Do This?

Small chunks give precise retrieval, less irrelevant information, better matching, and easier ranking -- but they can lose surrounding context, split an important explanation across pieces, or contain incomplete information on their own. Large chunks give more context and more complete explanations for generation -- but retrieval on them becomes less precise, and you send more irrelevant text to the LLM along with the useful part. Parent-Child Retrieval is a direct answer to that tradeoff.

## A Worked Example

Parent: *"CSE251 Registration Information"*, containing Child 1 (course description), Child 2 (prerequisites), Child 3 (registration conditions), Child 4 (credit hours). Query: *"What are the prerequisites for CSE251?"* Retrieval searches the children and matches Child 2. Instead of sending only Child 2's text (`"CSE201 and MATH201"`) to the LLM, you return its **parent** -- the full CSE251 Registration Information section, description and credit hours included -- giving the LLM meaningfully richer context to work with.

## The Architecture

```
                 Document
                    ↓
                 Parent
                    ↓
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       Child 1   Child 2   Child 3
          ↓         ↓         ↓
          └─────────┬─────────┘
                    ↓
               Embeddings
                    ↓
               Vector DB
```

At query time: `Query → Search child chunks → Find relevant child → Identify parent → Retrieve parent → LLM`.

## Why Not Just Store the Parent?

Because retrieval often works better on smaller pieces. If a parent is 2,000 words covering course description, prerequisites, grading, learning outcomes, registration, and assessment all at once, its embedding represents *all* of those concepts simultaneously -- the specific "prerequisite" signal gets diluted across everything else in the section. A small child like *"Prerequisites: CSE201 and MATH201"* has a much stronger, sharper relationship to a prerequisite query. **Small child → precise retrieval. Large parent → rich context.**

## Connecting to Embeddings

Only the children need to be embedded and searched:

```
Child text → Embedding → Vector DB
```

The parent doesn't need its own embedding for retrieval purposes -- instead, you store a relationship: `child_42 → parent_7`, `child_43 → parent_7`, `child_44 → parent_7`. When `child_42` is retrieved, you look up `parent_7` and pull its full content.

## A Concrete Data Model

```python
parent = {
    "id": "course_251",
    "text": "...full CSE251 section..."
}

children = [
    {"id": "chunk_1", "parent_id": "course_251", "text": "CSE251 is a Machine Learning course..."},
    {"id": "chunk_2", "parent_id": "course_251", "text": "Prerequisites: CSE201 and MATH201."},
    {"id": "chunk_3", "parent_id": "course_251", "text": "Students will learn..."},
]
```

The vector database holds embeddings for `chunk_1`, `chunk_2`, `chunk_3` -- each remembering `parent_id = course_251`.

## The Query Process

*"What are the prerequisites for CSE251?"* → embedding search finds `chunk_2` → look up `chunk_2.parent_id = course_251` → retrieve the full parent → pass that parent context to the LLM → generate the answer.

## More Than Two Levels

The hierarchy doesn't have to stop at parent/child. It can go `Document → Section → Subsection → Chunk`, and you can retrieve at the smallest level while returning any larger level as context -- `Parent: Chapter 4, Child: Section 4.2, Grandchild: Paragraph 4.2.3`, for instance. The exact hierarchy depends entirely on your data's natural structure.

## A Real-World Example

A 100-page university regulation document might be structured as `University Regulation → Admission / Registration / Graduation / Course Descriptions`, each with their own subsections (e.g. Graduation → Credit Requirements, GPA Requirements, Graduation Conditions), with small child chunks under each. A query like *"What GPA do I need to graduate?"* retrieves the "GPA requirements" child, then returns the "Graduation Requirements" parent -- giving the LLM enough surrounding context without needing to embed the whole document as one giant chunk.

## Combined With Hybrid Search

```
                    Query
                      ↓
             ┌────────┴────────┐
             ↓                 ↓
         Dense Child         BM25 Child
             ↓                 ↓
             └────────┬────────┘
                      ↓
                     RRF
                      ↓
                Child Results
                      ↓
               Parent Lookup
                      ↓
                Parent Context
                      ↓
                 Cross-Encoder
                      ↓
                     LLM
```

Parent-Child Retrieval isn't tied to dense search alone -- it composes cleanly with everything else built up in this level.

## Deduplicate Parents

If `child_1 → parent_A`, `child_2 → parent_A`, and `child_3 → parent_B` are all retrieved, you don't want to send `parent_A` twice just because two of its children matched. The flow is: `Retrieve children → map to parents → deduplicate parents → build context`.

## Parent-Child vs. Normal Retrieval

Normal: `Query → small chunk → LLM`. Parent-Child: `Query → small child → find parent → larger context → LLM`. The second approach helps most where meaning depends heavily on surrounding context.

## Where It Shines

Legal documents (a clause depending on its surrounding section), academic regulations (a rule depending on nearby definitions or exceptions), technical documentation (a config parameter depending on the larger API section), manuals (a single instruction needing its surrounding procedure), and long structured documents generally (books, policies, reports, specifications).

## The Main Tradeoff

Parent-Child Retrieval isn't automatically better. If the parent is itself 10,000 words, you've simply recreated the original context problem one level up -- the LLM now receives too much irrelevant information again. The engineering target: **child small enough to retrieve precisely, parent large enough to provide context, but not unnecessarily huge.**

## The Full Pipeline

```
                         Query
                           ↓
                  Query Rewriting
                           ↓
                    Multi-Query
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
         Dense Search                BM25
              ↓                         ↓
              └────────────┬────────────┘
                           ↓
                          RRF
                           ↓
                     Child Chunks
                           ↓
                    Parent Lookup
                           ↓
                      Parent Docs
                           ↓
                    Cross-Encoder
                           ↓
                     Best Context
                           ↓
                          LLM
```

Every technique in this level has a distinct, non-overlapping job.

## The Key Mental Model

**Retrieval unit** (child): *"Which small piece matches my query?"* **Context unit** (parent): *"What larger piece should the LLM understand?"* Separating those two questions is what makes Parent-Child Retrieval powerful.

*The single idea to keep:* retrieve on small, precise children; deliver their larger parent as context -- and deduplicate parents before they reach the LLM, since multiple matching children often point to the same parent.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Trace the Parent-Child Lookup",
                    "description": (
                        "Parent A: CSE251 Course Information, with children A1 (course "
                        "description), A2 (prerequisites), A3 (learning outcomes), A4 "
                        "(assessment). Parent B: CSE252 Course Information, with children B1 "
                        "(course description), B2 (prerequisites), B3 (learning outcomes).\n\n"
                        "User asks: \"What are the prerequisites for CSE251?\"\n\n"
                        "Answer: (1) Which child should ideally be retrieved? "
                        "(2) Which parent should then be returned? "
                        "(3) Why might retrieving the child be better than embedding only the "
                        "entire parent? "
                        "(4) If A2 and A3 are both retrieved, should you send Parent A twice to the LLM?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "parent-child-retrieval", "critical-thinking"],
                },
                {
                    "title": "Map Children to Deduplicated Parents",
                    "description": (
                        "Given a list of retrieved child IDs and a lookup mapping each child ID "
                        "to its parent ID and parent text, return the deduplicated list of full "
                        "parent texts to send to the LLM, preserving first-seen order."
                    ),
                    "starter_code": (
                        "retrieved_children = [\"chunk_1\", \"chunk_2\", \"chunk_5\"]\n\n"
                        "child_to_parent = {\n"
                        "    \"chunk_1\": \"course_251\",\n"
                        "    \"chunk_2\": \"course_251\",\n"
                        "    \"chunk_5\": \"course_252\",\n"
                        "}\n\n"
                        "parents = {\n"
                        "    \"course_251\": \"...full CSE251 section...\",\n"
                        "    \"course_252\": \"...full CSE252 section...\",\n"
                        "}\n\n"
                        "def get_deduplicated_parent_contexts(retrieved_children, child_to_parent, parents):\n"
                        "    # TODO: map each retrieved child to its parent, deduplicate parent\n"
                        "    # IDs preserving first-seen order, then return the list of parent texts.\n"
                        "    pass\n\n"
                        "print(get_deduplicated_parent_contexts(retrieved_children, child_to_parent, parents))\n"
                    ),
                    "solution_code": (
                        "def get_deduplicated_parent_contexts(retrieved_children, child_to_parent, parents):\n"
                        "    seen_parents = []\n"
                        "    for child_id in retrieved_children:\n"
                        "        parent_id = child_to_parent[child_id]\n"
                        "        if parent_id not in seen_parents:\n"
                        "            seen_parents.append(parent_id)\n"
                        "    return [parents[pid] for pid in seen_parents]\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "parent-child-retrieval", "python"],
                },
            ],
            "quiz": {
                "title": "Parent-Child Retrieval — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the core principle of Parent-Child Retrieval?",
                        "options": [
                            "Always embed and search the largest possible chunk",
                            "Search using small child chunks, but return their larger parent as context",
                            "Search using the parent, and return only the matching child text",
                            "Store every chunk twice, once as parent and once as child",
                        ],
                        "correct": 1,
                        "explanation": (
                            "The technique's defining move is 'search small, return large' -- "
                            "retrieving with precise child chunks while delivering richer parent "
                            "context to the LLM."
                        ),
                    },
                    {
                        "question": (
                            "Why does embedding only a large parent chunk (e.g. 2,000 words "
                            "covering many topics) often hurt precise retrieval?"
                        ),
                        "options": [
                            "Large chunks cannot be embedded at all",
                            "The embedding represents many concepts at once, diluting the specific signal a narrow query needs to match",
                            "Vector databases reject documents longer than 500 words",
                            "Large chunks always retrieve faster than small ones",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A large chunk's embedding blends many different concepts together, "
                            "weakening its match strength to any single specific query compared "
                            "to a small, focused child chunk."
                        ),
                    },
                    {
                        "question": (
                            "In the child-to-parent data model, what does a vector database "
                            "typically store embeddings for?"
                        ),
                        "options": [
                            "Only the parent documents",
                            "The child chunks, each remembering a reference (parent_id) to its parent",
                            "Neither parents nor children -- only raw text",
                            "A single averaged embedding representing the whole document",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Children are embedded and searched directly; each stores a "
                            "parent_id reference so the system can look up and return the full "
                            "parent content after a child match."
                        ),
                    },
                    {
                        "question": (
                            "Two retrieved children, A2 and A3, both belong to Parent A. What "
                            "should happen before sending context to the LLM?"
                        ),
                        "options": [
                            "Send Parent A twice, once for each matching child",
                            "Deduplicate so Parent A is only included once in the context",
                            "Discard both children since they share a parent",
                            "Merge A2 and A3 into a new child before retrieval",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Multiple matching children pointing to the same parent should be "
                            "deduplicated at the parent level so the LLM doesn't receive redundant context."
                        ),
                    },
                    {
                        "question": (
                            "What goes wrong if the 'parent' in Parent-Child Retrieval is itself "
                            "10,000 words long?"
                        ),
                        "options": [
                            "Nothing -- bigger parents are always strictly better",
                            "It recreates the original context problem: the LLM again receives too much irrelevant information",
                            "The child chunks become impossible to embed",
                            "Retrieval speed for children is unaffected either way",
                        ],
                        "correct": 1,
                        "explanation": (
                            "If the parent is too large, the benefit of precise child-level "
                            "retrieval is undone once that oversized parent context reaches the "
                            "LLM -- the sizing of parent chunks is itself an engineering tradeoff."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": "Advanced RAG Retrieval Pipeline",
                "description": (
                    "Build a complete Advanced RAG retrieval pipeline for a small academic "
                    "knowledge base (course descriptions, prerequisites, and graduation "
                    "regulations) that combines every technique covered in this level: dense "
                    "retrieval, BM25, hybrid search with RRF fusion, Cross-Encoder reranking, "
                    "query rewriting for multi-turn conversations, query expansion for short or "
                    "vague queries, multi-query retrieval for complex questions, and "
                    "parent-child chunking so retrieval stays precise while the LLM still "
                    "receives full context."
                ),
                "difficulty": DifficultyLevel.advanced,
                "tech_stack": ["Python", "FastAPI", "Qdrant", "rank_bm25", "sentence-transformers"],
                "objectives": [
                    "Chunk a small academic document set into parent sections and child chunks",
                    "Index child chunks in both a dense vector store and a BM25 index",
                    "Implement RRF to fuse dense and sparse rankings",
                    "Add a Cross-Encoder reranking step (e.g. BAAI/bge-reranker-v2-m3) over fused candidates",
                    "Implement conditional query rewriting for multi-turn conversational queries",
                    "Implement conditional query expansion for short or ambiguous queries",
                    "Implement multi-query retrieval for complex, multi-part questions",
                    "Resolve retrieved children back to deduplicated parent context before generation",
                ],
                "rubric": {
                    "retrieval_correctness": "Dense, BM25, and hybrid fusion each work correctly and independently",
                    "reranking_quality": "Cross-Encoder reranking measurably improves ordering over raw fusion results",
                    "conditional_logic": "Query rewriting/expansion/multi-query are applied conditionally, not on every query",
                    "parent_child_handling": "Parent lookup and deduplication work correctly across overlapping child matches",
                    "code_quality": "Pipeline stages are modular and independently testable",
                },
                "starter_repo_url": None,
                "estimated_hours": 6.0,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 12
            # ------------------------------------------------------------
            "title": "Context Compression",
            "slug": "ai-developer-advanced-rag-context-compression",
            "description": (
                "Reducing retrieved context down to what's actually needed to "
                "answer the query, without inventing or dropping the facts "
                "required for a correct answer."
            ),
            "order": 12,
            "difficulty": DifficultyLevel.intermediate,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "context-compression", "retrieval"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Context Compression",
                "content": """# Context Compression

The pipeline so far: `Query → Dense + BM25 → RRF → Parent-Child Retrieval → Reranking → Documents → LLM`. One problem remains: **what if the retrieved documents contain a lot of information that isn't actually needed to answer the question?** That's what Context Compression addresses.

## The Problem

Query: *"What are the prerequisites for CSE251?"* The retrieval system finds a genuinely useful parent document covering Description, Prerequisites (`CSE201 and MATH201`), Learning Outcomes, Assessment, Credit Hours, and Teaching Methods -- all real, all about CSE251. But the question only needs one line: `Prerequisites: CSE201 and MATH201.` Sending the whole document to the LLM is unnecessary.

## What Is Context Compression?

Context compression means taking retrieved context and reducing it to the information most useful for answering the specific query:

```
Retrieved Documents
       ↓
Context Compressor
       ↓
Relevant Information
       ↓
LLM
```

Instead of sending, say, 5,000 tokens, you might send 800 tokens containing the parts that actually matter.

## Think of It as Filtering

Retrieval returns Documents A, B, C, D, each full of text. Compression asks: *"which parts of these documents actually matter for this query?"* `Documents → remove irrelevant information → keep useful information → LLM`.

## Why It's Useful

Less context means the LLM processes fewer tokens, which typically means lower API cost and lower latency. It also means better focus -- the LLM sees less irrelevant material -- and less noise, reducing the chance that unrelated retrieved content distracts the model from the actual answer.

## Compression Is Not Chunking

These happen at opposite ends of the pipeline. **Chunking** happens during *ingestion*: `Large document → small chunks`, purely to make documents easier to retrieve. **Context compression** happens *after retrieval*: `Retrieved documents → remove irrelevant parts`, purely to make the retrieved context more useful for generation. **Chunking → before retrieval. Compression → after retrieval.**

## A Worked Example

Query: *"What GPA is required for graduation?"* Retrieved document covers required credit hours, minimum cumulative GPA (2.0), required courses, academic regulations, application deadlines, and eligibility review -- all genuinely part of "Graduation Requirements," but the question is specifically about GPA. A compressor might reduce this to just: *"The minimum cumulative GPA required for graduation is 2.0."* Then `Compressed Context → LLM → "Students need a minimum cumulative GPA of 2.0."`

## Compression at Different Levels

**Level 1 -- remove irrelevant documents**: of `A (relevant), B (relevant), C (irrelevant), D (irrelevant)`, keep only `A, B`.

**Level 2 -- remove irrelevant chunks within a document**: of `Chunk 1 (relevant), Chunk 2 (irrelevant), Chunk 3 (relevant), Chunk 4 (irrelevant)`, keep `Chunk 1, Chunk 3`.

**Level 3 -- extract relevant sentences**: from a paragraph mixing course description, learning content, prerequisites, and logistics, for the query *"What is the prerequisite?"* keep only `"Students must complete CSE201 before registration."`

## Compression Using an LLM

```python
prompt = \"\"\"
Given the user question and retrieved context,
keep only the information that is relevant
to answering the question.

Question:
{query}

Context:
{context}

Return only the relevant information.
\"\"\"
```

The LLM acts as a context filter here.

## The Danger

The compressor is itself an AI component, and it can make mistakes. If the original context says *"Students need a GPA of 2.0"* but the compressor mistakenly outputs *"Students need a GPA of 2.5,"* you've just introduced a brand-new error into the pipeline. The safest mental model: **compression should remove unnecessary information, never invent or modify facts.**

## Extractive vs. Generative Compression

**Extractive** compression selects existing pieces of text verbatim -- from `A B C D E`, keep `B D`. Nothing new is generated, which makes it generally safer for factual RAG. **Generative** compression asks a model to summarize the relevant information -- from `A B C D E`, produce a new sentence like *"Requirement is a minimum GPA of 2.0."* This can be more compact, but introduces real risk of hallucination, missing details, or incorrect interpretation, so it needs evaluation before you trust it in production.

## Context Compression + Parent-Child Retrieval

These pair naturally. Parent-Child Retrieval gives you `Query → small child → parent → rich context`, but the parent itself might still be too large. Adding compression: `Query → child retrieval → parent → context compression → relevant parent information → LLM`. Together they give you precise retrieval, rich context, *and* a focused final payload.

## Context Compression vs. Reranking

Don't conflate these. **Reranking** changes the *order* of documents: `A, B, C, D → C, A, D, B`. **Compression** reduces the *content*: `Large Document → only relevant sections`. **Reranking → document-level relevance. Compression → content-level relevance.** In a pipeline they're sequential and complementary: `Dense + BM25 → RRF → Reranker → Top documents → Context Compression → LLM`.

## Why This Matters for Long Documents

Retrieving 10 documents at 2,000 tokens each is 20,000 tokens -- but the actual answer might depend on only 1,500 of them. Sending all 20,000 is wasteful; compression can turn that into `2,000 relevant tokens → LLM`. This matters most with long PDFs, legal contracts, university regulations, technical manuals, research papers, and enterprise documentation.

## An Important Caveat: Preserve the Evidence

In a bilingual RAG system, *"كم ساعة معتمدة مطلوبة للتخرج؟"* might retrieve a large "متطلبات التخرج" (graduation requirements) section covering many separate conditions. Compression might correctly identify the *topic* sentence about credit hours -- but if the actual number (e.g. *"يجب إتمام 144 ساعة معتمدة"*) appears elsewhere in the document, that specific sentence is critical and **must** be preserved. The compressor's job is to preserve the evidence needed to answer the question, not just to summarize the general topic.

## The Governing Principle

The goal is *not* "make the context as short as possible." The goal is **"make the context as small as possible while preserving the information needed to answer correctly."** Too much context creates noise; too little context loses the evidence entirely; the target is relevant *and* sufficient.

## A Practical Pipeline

```
                         User Query
                              ↓
                       Query Rewriting
                              ↓
                      Multi-Query
                              ↓
               ┌──────────────┴──────────────┐
               ↓                             ↓
          Dense Search                    BM25
               ↓                             ↓
               └──────────────┬──────────────┘
                              ↓
                             RRF
                              ↓
                       Candidate Chunks
                              ↓
                         Parent Lookup
                              ↓
                        Cross-Encoder
                              ↓
                       Top Documents
                              ↓
                    Context Compression
                              ↓
                       Final Context
                              ↓
                             LLM
```

## When to Use It

Compression pays off when retrieved documents are long, parent chunks are large, many retrieved documents contain irrelevant sections, your context window is limited, LLM cost matters, or retrieval has good recall but noisy content. If your retrieved context is already 3 small, highly relevant chunks, compression may add little. As always: **don't add a technique just because it exists -- add it because it solves a real problem you actually have.**

*The single idea to keep:* compress to preserve *sufficient* evidence in the *smallest* possible context, favor extractive over generative compression when factual accuracy matters, and never let the compressor summarize away the specific detail the answer depends on.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Compress This Document",
                    "description": (
                        "Retrieved document:\n"
                        "\"CSE251 — Machine Learning. CSE251 is a 3-credit course. The course "
                        "introduces supervised and unsupervised learning. Prerequisites: CSE201 "
                        "and MATH201. Students complete weekly assignments. The final grade "
                        "consists of assignments and an examination. The course is offered in "
                        "the fall semester.\"\n\n"
                        "User asks: \"What are the prerequisites for CSE251?\"\n\n"
                        "Answer: (1) Which sentence is the most important? "
                        "(2) What is context compression doing here? "
                        "(3) What's the difference between reranking and compression? "
                        "(4) Why shouldn't compression generate new facts? "
                        "(5) If the retrieved context is already one short, highly relevant "
                        "sentence, would compression be necessary?"
                    ),
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["rag", "context-compression", "critical-thinking"],
                },
                {
                    "title": "Extractive Sentence Filter",
                    "description": (
                        "Write a simple extractive compressor: given a query and a list of "
                        "candidate sentences, keep only sentences that contain at least one "
                        "word from the query (case-insensitive), preserving original order. "
                        "This is a naive extractive approach, not the only correct method."
                    ),
                    "starter_code": (
                        "query = \"What is the prerequisite for CSE251?\"\n"
                        "sentences = [\n"
                        "    \"CSE251 is a Machine Learning course worth 3 credits.\",\n"
                        "    \"The course introduces supervised and unsupervised learning.\",\n"
                        "    \"Students must complete CSE201 before registration as a prerequisite.\",\n"
                        "    \"The course includes weekly practical sessions.\",\n"
                        "]\n\n"
                        "def extractive_compress(query, sentences):\n"
                        "    # TODO: keep sentences sharing at least one word (case-insensitive)\n"
                        "    # with the query, preserving original order.\n"
                        "    pass\n\n"
                        "print(extractive_compress(query, sentences))\n"
                    ),
                    "solution_code": (
                        "def extractive_compress(query, sentences):\n"
                        "    query_words = set(query.lower().split())\n"
                        "    kept = []\n"
                        "    for sentence in sentences:\n"
                        "        sentence_words = set(sentence.lower().replace('.', '').split())\n"
                        "        if query_words & sentence_words:\n"
                        "            kept.append(sentence)\n"
                        "    return kept\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "context-compression", "python"],
                },
            ],
            "quiz": {
                "title": "Context Compression — Knowledge Check",
                "questions": [
                    {
                        "question": "What does context compression do in a RAG pipeline?",
                        "options": [
                            "Splits large documents into smaller chunks before indexing",
                            "Reduces retrieved context to the information most useful for answering the query, after retrieval",
                            "Reorders retrieved documents by relevance",
                            "Compresses the vector database to save disk space",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Context compression operates after retrieval, trimming retrieved "
                            "content down to what's actually needed to answer the specific query."
                        ),
                    },
                    {
                        "question": "How does context compression differ from chunking?",
                        "options": [
                            "They are the same technique performed at different times",
                            "Chunking happens during ingestion to aid retrieval; compression happens after retrieval to aid generation",
                            "Chunking only applies to Arabic text; compression only applies to English",
                            "Compression always produces smaller pieces than chunking",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Chunking is a pre-retrieval ingestion step for indexing; compression "
                            "is a post-retrieval step that reduces already-retrieved context "
                            "before it reaches the LLM."
                        ),
                    },
                    {
                        "question": "Why is extractive compression generally considered safer than generative compression for factual RAG?",
                        "options": [
                            "Extractive compression is always shorter",
                            "Extractive compression only selects existing text verbatim, while generative compression can introduce hallucinated or altered facts",
                            "Generative compression cannot process more than one document",
                            "Extractive compression requires no computation at all",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Because extractive compression selects text that already exists, it "
                            "cannot invent new claims the way a generative summarizer might."
                        ),
                    },
                    {
                        "question": (
                            "A compressor summarizes a graduation-requirements section but drops "
                            "the specific number of required credit hours mentioned in it. What "
                            "principle did it violate?"
                        ),
                        "options": [
                            "Compression should always produce the shortest possible output regardless of content",
                            "Compression should preserve the evidence needed to answer the question, not just summarize the general topic",
                            "Compression should never be used on Arabic documents",
                            "Compression must always double the length of the retrieved context",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Dropping the specific number needed to answer the question means "
                            "the compression removed necessary evidence -- the goal is the "
                            "smallest *sufficient* context, not the shortest one."
                        ),
                    },
                    {
                        "question": "What is the key distinction between reranking and context compression?",
                        "options": [
                            "Reranking changes document order (document-level relevance); compression reduces document content (content-level relevance)",
                            "Reranking and compression both only reorder documents",
                            "Compression happens before retrieval; reranking happens after generation",
                            "Reranking removes irrelevant sentences; compression reorders documents",
                        ],
                        "correct": 0,
                        "explanation": (
                            "Reranking decides which whole documents matter most and in what "
                            "order; compression decides which parts of those documents are "
                            "actually needed."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 13
            # ------------------------------------------------------------
            "title": "Corrective RAG",
            "slug": "ai-developer-advanced-rag-corrective-rag",
            "description": (
                "A retrieval decision loop that evaluates whether retrieved "
                "documents are actually good enough, and takes corrective "
                "action -- rewriting, expanding, or searching elsewhere -- "
                "when they aren't."
            ),
            "order": 13,
            "difficulty": DifficultyLevel.advanced,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "corrective-rag", "retrieval", "evaluation"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Corrective RAG",
                "content": """# Corrective RAG

Every technique so far quietly assumes *"the retriever will probably find useful documents."* But in real applications, retrieval can simply fail: `User Query → Retriever → Bad documents → LLM → Bad answer`. **Corrective RAG (CRAG)** adds a mechanism that checks retrieved information and decides what to do when it isn't good enough.

## The Core Idea

Normal RAG: `Query → Retrieve → Generate`. Corrective RAG:

```
Query
 ↓
Retrieve
 ↓
Evaluate Retrieval
 ↓
┌───────────────┬───────────────┐
↓               ↓               ↓
Good            Uncertain       Bad
↓               ↓               ↓
Use it       Improve search   Search again
↓               ↓               ↓
LLM             LLM           LLM
```

The new component is **retrieval evaluation** -- a step that didn't exist in any earlier lesson.

## Why We Need It

Query: *"What are the prerequisites for CSE251?"* Retrieval returns three documents all genuinely about CSE251 -- credit value, learning outcomes, semester offered -- but **none of them actually answers the prerequisite question**. A normal RAG system would still hand these to the LLM, which might guess, admit it doesn't know, or produce an incomplete answer. Corrective RAG instead flags: *"wait, these retrieved documents aren't sufficient."*

## Retrieval Evaluation

After retrieval, an evaluator asks: *"are these documents relevant enough to actually answer the query?"* and classifies the result as roughly **GOOD**, **AMBIGUOUS**, or **BAD**.

**Correct/Good**: retrieved documents clearly contain the needed information -- `Query → good documents → LLM`, no correction needed. **Ambiguous/Weak**: documents are somewhat related but may not be sufficient -- `Query → weak documents → improve retrieval → LLM`. **Incorrect/Bad**: documents aren't relevant at all -- `Query → bad documents → alternative retrieval → LLM`.

## What "Corrective" Actually Means

The system doesn't just report *"retrieval failed"* -- it tries to *fix* the retrieval process. Example: *"How do I finish university?"* → poor retrieval → rewritten to *"AI Engineering graduation requirements"* → retrieve again → better documents. Corrective RAG can lean on techniques already covered: query rewriting, query expansion, web search, alternate retrieval strategies, additional searches.

## Composed With the Rest of the Pipeline

```
                         User Query
                              ↓
                     Query Rewriting
                              ↓
                     Dense + BM25
                              ↓
                             RRF
                              ↓
                          Reranking
                              ↓
                     Retrieval Evaluation
                              ↓
                 ┌────────────┼────────────┐
                 ↓            ↓            ↓
               Good       Uncertain       Bad
                 ↓            ↓            ↓
                LLM       Rewrite       Alternative
                              ↓           Search
                              └─────┬─────┘
                                    ↓
                                   LLM
```

Corrective RAG is a **control strategy around retrieval** -- not a separate retriever competing with dense/sparse/hybrid search.

## In a Bilingual RAG System

*"ما هي شروط التخرج؟"* retrieves documents about registration info, a Machine Learning course description, and exam dates -- none actually about graduation requirements. The evaluator marks this `BAD`, and the system corrects by rewriting to `متطلبات التخرج من برنامج هندسة الذكاء الاصطناعي` and searching again, this time finding documents about graduation requirements, required credit hours, and GPA conditions -- a much better retrieval outcome.

## Corrective RAG vs. Query Rewriting

Don't confuse these. **Query Rewriting** is a *technique*: `bad/unclear query → better query`. **Corrective RAG** is a *strategy*: `retrieve → check retrieval → if bad, take corrective action`. Query rewriting is just one of the tools Corrective RAG might reach for. **Query rewriting is a tool. Corrective RAG is a decision process.**

## How Do You Evaluate Retrieval?

**Approach 1 -- similarity scores.** If Document A scores 0.91, you might set a rule like `if top_score >= 0.80: good else: weak`. But there's a real flaw here.

## Why Similarity Alone Isn't Enough

Query: *"What are the prerequisites for CSE251?"* Retrieved: *"CSE251 is a Machine Learning course worth 3 credits."* This can have high semantic similarity to the query -- it's strongly about CSE251 -- while still **not answering the prerequisite question at all**. **Semantic similarity ≠ answer relevance.** This is one of the most important lessons in this whole level.

## LLM-Based Retrieval Evaluation

A more capable approach asks an LLM directly: given the question and the retrieved context, *"does the context contain enough information to answer the question?"* If the answer is `NO`, the system corrects and searches again. This is smarter than similarity thresholds alone, but adds its own latency, cost, and the risk that the evaluator itself makes mistakes -- another engineering tradeoff to weigh.

## Corrective Actions Can Vary

Bad retrieval doesn't demand one fixed response. Depending on the situation, you might rewrite the query, expand the query, run a web search, try BM25 specifically, try dense retrieval with different settings, or search an entirely different data source. The right correction depends on the application.

## Corrective RAG With External Search

If an internal company knowledge base doesn't have current information -- e.g. *"What is the latest version of our API?"* -- Corrective RAG could detect insufficient internal retrieval and fall back to an external search for current information. This is one of the more compelling real-world use cases for the pattern.

## But Don't Blindly Trust External Search

Reaching outside your own knowledge base introduces **source reliability** questions: which sources are trusted, are they current, are they authoritative, can their content be manipulated, and should external information ever be allowed to override internal documents? Corrective RAG expands your system-design surface, not just your retrieval robustness.

## A Simple Implementation Sketch

```python
documents = retriever.invoke(query)
quality = evaluate_retrieval(query, documents)

if quality == "good":
    context = documents
elif quality == "weak":
    new_query = rewrite_query(query)
    context = retriever.invoke(new_query)
else:
    new_query = expand_query(query)
    context = retriever.invoke(new_query)

answer = llm.invoke(build_prompt(query, context))
```

The exact Python matters less than the logic: `retrieve → evaluate → decide → correct if necessary → generate`.

## Corrective RAG Is a Feedback Loop

Normal RAG: `Query → Retrieve → Generate`. Corrective RAG:

```
Query
 ↓
Retrieve
 ↓
Evaluate
 ↓
Is retrieval good?
 ↓
 ├── Yes → Generate
 │
 └── No → Correct → Retrieve again
                         ↓
                      Evaluate
                         ↓
                      Generate
```

RAG becomes adaptive rather than a fixed one-shot pipeline.

## Don't Create Infinite Loops

A production system must never do `retrieve → bad → retry → bad → retry → bad → retry → ...` indefinitely. Set a hard limit -- e.g. maximum 2 retrieval corrections -- after which, if still insufficient, the system should say something like *"I couldn't find enough reliable information"* rather than looping forever. This bounds cost and latency and prevents runaway behavior.

## Corrective RAG and Hallucination

This pattern can meaningfully reduce hallucinations, because it gives the system a chance to recognize *"I don't have sufficient evidence"* instead of guessing. Rather than `no useful context → LLM guesses`, you get `no useful context → detect failure → try better retrieval`, and if that still fails: `no reliable evidence → don't fabricate an answer`. This fits especially well with a strict, evidence-grounded RAG approach.

## Corrective RAG Doesn't Guarantee Correctness

Important caveat: this is one layer of defense, not a guarantee. Failures can still happen at every stage -- a bad *evaluation* might wrongly conclude retrieval was good; a bad *correction* might search the wrong rewritten query; even genuinely correct documents can still be *misinterpreted* by the LLM. Corrective RAG improves robustness; it doesn't eliminate errors.

## The Accumulated Architecture

```
                              User
                               ↓
                         Query Analysis
                               ↓
                       Query Rewriting
                               ↓
                        Multi-Query
                               ↓
                 ┌─────────────┴─────────────┐
                 ↓                           ↓
            Dense Search                  BM25
                 ↓                           ↓
                 └─────────────┬─────────────┘
                               ↓
                              RRF
                               ↓
                         Candidate Docs
                               ↓
                          Reranking
                               ↓
                      Parent Retrieval
                               ↓
                    Retrieval Evaluation
                               ↓
                 ┌─────────────┴─────────────┐
                 ↓                           ↓
              Sufficient                 Insufficient
                 ↓                           ↓
          Context Compression        Correct Retrieval
                 ↓                           ↓
                 └─────────────┬─────────────┘
                               ↓
                              LLM
```

You won't need every one of these components in every application -- what matters is understanding exactly what problem each one solves, so you can reach for the right ones deliberately.

*The single idea to keep:* Corrective RAG turns retrieval from a one-shot bet into a checked, correctable step -- but it's a defense layer that reduces the odds of a bad answer, not a guarantee that removes them, and it always needs a hard retry limit to stay safe in production.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Evaluate This Retrieval",
                    "description": (
                        "Query: \"What are the prerequisites for CSE251?\" Retrieved: "
                        "(1) \"CSE251 is a Machine Learning course.\" (2) \"CSE251 is worth 3 "
                        "credit hours.\" (3) \"CSE251 is offered in the fall semester.\"\n\n"
                        "Answer: (1) Is this retrieval sufficient? "
                        "(2) What should the retrieval evaluator conclude? "
                        "(3) Give one possible corrective action. "
                        "(4) How is Corrective RAG different from Query Rewriting? "
                        "(5) Why shouldn't the system retry retrieval forever? "
                        "(6) What should the system do if retrieval is still insufficient "
                        "after correction?"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "corrective-rag", "critical-thinking"],
                },
                {
                    "title": "Implement a Bounded Correction Loop",
                    "description": (
                        "Implement the Corrective RAG control loop: call retrieve() and "
                        "evaluate_quality() (both provided as stubs), and if quality is not "
                        "'good', attempt query rewriting and retry, up to a maximum number of "
                        "corrections. If still not good after the limit, return a fallback "
                        "message instead of looping forever."
                    ),
                    "starter_code": (
                        "def retrieve(query):\n"
                        "    # stub: pretend this calls the real retriever\n"
                        "    raise NotImplementedError\n\n"
                        "def evaluate_quality(query, documents):\n"
                        "    # stub: returns 'good', 'weak', or 'bad'\n"
                        "    raise NotImplementedError\n\n"
                        "def rewrite_query(query):\n"
                        "    # stub: returns an improved query string\n"
                        "    raise NotImplementedError\n\n"
                        "def corrective_retrieve(query, max_corrections=2):\n"
                        "    # TODO: retrieve, evaluate, and rewrite+retry up to max_corrections\n"
                        "    # times. If still not 'good' after the limit, return None to signal\n"
                        "    # 'insufficient evidence' rather than looping forever.\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def corrective_retrieve(query, max_corrections=2):\n"
                        "    current_query = query\n"
                        "    for attempt in range(max_corrections + 1):\n"
                        "        documents = retrieve(current_query)\n"
                        "        quality = evaluate_quality(current_query, documents)\n"
                        "        if quality == \"good\":\n"
                        "            return documents\n"
                        "        if attempt < max_corrections:\n"
                        "            current_query = rewrite_query(current_query)\n"
                        "    return None\n"
                    ),
                    "difficulty": DifficultyLevel.advanced,
                    "skill_tested": ["rag", "corrective-rag", "python"],
                },
            ],
            "quiz": {
                "title": "Corrective RAG — Knowledge Check",
                "questions": [
                    {
                        "question": "What new component does Corrective RAG add compared to normal RAG?",
                        "options": [
                            "A step that generates the final answer twice for verification",
                            "A retrieval evaluation step that checks whether retrieved documents are good enough before generation",
                            "A larger embedding model",
                            "A second LLM that only translates queries",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Corrective RAG's defining addition is evaluating retrieval quality "
                            "after retrieval and before generation, then acting on that evaluation."
                        ),
                    },
                    {
                        "question": "Why is a high similarity score alone not sufficient to judge retrieval quality?",
                        "options": [
                            "Similarity scores are always inaccurate",
                            "A document can be highly similar to the query topic without actually containing the answer to the specific question asked",
                            "Similarity scores only work for BM25, not dense retrieval",
                            "High similarity always means the document is irrelevant",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Semantic similarity measures topical relatedness, not whether the "
                            "specific question is actually answered -- a document can score high "
                            "on one while failing the other."
                        ),
                    },
                    {
                        "question": "What is the key difference between Query Rewriting and Corrective RAG?",
                        "options": [
                            "They are identical techniques",
                            "Query Rewriting is a specific technique for improving a query; Corrective RAG is a decision loop that evaluates retrieval and can use rewriting (among other actions) as a fix",
                            "Corrective RAG only works with Arabic queries",
                            "Query Rewriting always requires an LLM, while Corrective RAG never does",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Query rewriting is one tool; Corrective RAG is the broader strategy "
                            "of checking retrieval quality and deciding whether and how to correct it."
                        ),
                    },
                    {
                        "question": "Why must a Corrective RAG system set a maximum number of correction attempts?",
                        "options": [
                            "To comply with a fixed industry standard of exactly 2 retries",
                            "To prevent infinite retry loops that would drive up cost and latency without guaranteeing success",
                            "Because LLMs can only be called twice per conversation",
                            "Because retrieval evaluators can only run once per query",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Without a limit, a persistently bad retrieval could trigger endless "
                            "correction attempts, so systems cap corrections and fall back to an "
                            "honest 'insufficient evidence' response."
                        ),
                    },
                    {
                        "question": "Does Corrective RAG guarantee a correct final answer?",
                        "options": [
                            "Yes, because it always retries until retrieval is perfect",
                            "No -- it reduces certain failure modes but the evaluator, the correction, or the LLM's interpretation can still go wrong",
                            "Yes, because it always falls back to external search",
                            "No -- Corrective RAG never improves answer quality in practice",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Corrective RAG is one layer of defense that improves robustness -- "
                            "it does not eliminate the possibility of a bad evaluation, a bad "
                            "correction, or LLM misinterpretation of correct documents."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 14
            # ------------------------------------------------------------
            "title": "Agentic RAG",
            "slug": "ai-developer-advanced-rag-agentic-rag",
            "description": (
                "Letting an AI agent dynamically decide how to retrieve -- which "
                "tools to use, whether to search again, when to stop -- instead "
                "of following one fixed retrieval pipeline."
            ),
            "order": 14,
            "difficulty": DifficultyLevel.advanced,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "agentic-rag", "agents", "retrieval"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Agentic RAG",
                "content": """# Agentic RAG

Everything up to this point has mostly followed a fixed sequence: `Query → Retrieve → Rerank → Compress → Generate`. **What if the system needs to decide what to do next?** That's Agentic RAG -- one of the most important ideas in modern RAG.

## What Is Agentic RAG?

Agentic RAG is a RAG system where an AI agent can **decide** how to retrieve information, which tools to use, and whether it needs additional retrieval before answering. Instead of `Query → Retriever → LLM`, you get:

```
User
 ↓
Agent
 ↓
Decide what to do
 ↓
Use retrieval/tool
 ↓
Inspect result
 ↓
Decide again
 ↓
Retrieve more if necessary
 ↓
Answer
```

The key word is **decision-making**.

## Traditional RAG vs. Agentic RAG

**Traditional RAG** follows a predetermined workflow: `Query → Retriever → Context → LLM → Answer`. The system doesn't decide anything -- it just follows the pipeline. **Agentic RAG** actively decides at each step: `Query → Agent → "Do I need retrieval?" → Yes → Search → "Is this enough?" → No → Rewrite query → Search again → "Is this enough?" → Yes → Answer`. **Traditional RAG follows a retrieval pipeline. Agentic RAG dynamically controls the retrieval process.**

## The Mental Model

Think of traditional RAG as a **machine** -- you give it a query, it follows predefined steps. Think of Agentic RAG as an **AI researcher** -- you give it a question, and it decides what to search, which source to use, whether it needs another search, whether to change its query, whether it has enough evidence, and when to stop.

## A Worked Example

*"Compare the graduation requirements of the AI Engineering and Computer Engineering programs."* This is meaningfully more complex than *"What is CSE251?"* A simple RAG pipeline might retrieve some documents and hope they cover everything. An agentic system can reason through the task: `Agent → need AI Engineering info → search → need Computer Engineering info → search → compare results → are requirements complete? → yes → generate comparison`. The agent **decomposes** the retrieval task into pieces it can handle separately.

## Agentic RAG Introduces a Loop

Traditional RAG: `A → B → C → D`, straight through. Agentic RAG: `A → B → Evaluate → Decide → B again / C / D → Evaluate → Decide → Stop`. Conceptually, the agent can repeatedly interact with tools:

```
                 ┌──────────────┐
                 │              ↓
User → Agent → Tool → Result → Agent
                 ↑              │
                 └──────────────┘
```

## What Tools Can an Agentic RAG System Use?

An agent might have access to vector search, BM25 search, a database, web search, document search, a calculator, or an external API -- and it decides which one fits the current sub-question. *"What is the current price of this product?"* points toward a web/API tool. *"What does our company policy say about vacation?"* points toward internal document search. *"What are the prerequisites for CSE251?"* points toward the academic knowledge base.

## Agentic RAG Doesn't Mean "The LLM Does Everything"

A common misconception. A good Agentic RAG architecture still has specialized components -- a Query Rewriter, a Retriever, a Reranker, a Context Compressor -- with the agent sitting on top: `Agent → Query Rewriter → Retriever → Reranker → Context Compressor → Agent → LLM`. The agent's job is specifically **deciding what action should happen next**, not doing every step's work itself.

## Example: Failed Retrieval, Handled Dynamically

*"What are the prerequisites for CSE251?"* → Agent searches the knowledge base → retriever returns poor documents → agent evaluates: *not enough evidence* → agent decides to rewrite the query → new query `"CSE251 prerequisite courses enrollment requirements"` → search again → relevant document found → agent evaluates: *enough evidence* → answer. This connects directly to the previous lesson -- **Agentic RAG can turn Corrective RAG into a more dynamic system.**

## Corrective RAG vs. Agentic RAG

These are related but distinct. **Corrective RAG** usually has a *predefined* correction strategy: `retrieve → evaluate → if bad → rewrite → retrieve again`. **Agentic RAG** lets the agent *decide* what correction to perform: `retrieve → evaluate → agent decides: rewrite / expand / BM25 / vector search / another source / stop`. **Corrective RAG can be implemented as a fixed correction workflow. Agentic RAG gives the system more autonomy over that workflow.**

## In a Bilingual RAG System

*"هل أقدر أسجل CSE251 وأنا لسه مخلصتش المتطلبات السابقة؟"* might require the agent to work out what the CSE251 prerequisites are, whether prerequisites are mandatory, whether exceptions exist, and what the registration policy says. Rather than one search, the agent can chain: `search CSE251 prerequisites → inspect → search registration policy → inspect → search prerequisite exceptions → combine evidence → answer` -- much closer to how a human researcher would actually approach the question.

## Decomposing Complex Questions

*"Which AI Engineering courses require CSE251, and what are their prerequisites?"* can be broken into: Task 1 -- find courses that require CSE251; Task 2 -- for each of those courses, find its prerequisites; Task 3 -- combine the information. The agent then performs multiple retrieval operations to satisfy each sub-task -- something fixed RAG pipelines often genuinely struggle with.

## Agent State

Because the agent takes multiple steps, it needs to remember what's happened so far:

```python
state = {
    "question": "...",
    "queries": [],
    "retrieved_docs": [],
    "sources": [],
    "steps": [],
    "final_answer": None,
}
```

The state evolves as the agent works -- the question stays fixed, `queries` accumulates each search attempt (`"CSE251 prerequisites"`, then `"CSE251 enrollment requirements"`), and `retrieved_docs` grows with each round. This concept becomes especially important later when working with frameworks like LangGraph.

## Agentic RAG Is a Workflow With Decisions

```
                   Start
                     ↓
                  Analyze
                     ↓
               Need retrieval?
                ↙        ↘
              Yes         No
               ↓           ↓
             Search      Answer
               ↓
             Inspect
               ↓
          Enough evidence?
            ↙        ↘
          Yes         No
           ↓           ↓
        Answer      Choose action
                       ↓
              ┌────────┼────────┐
              ↓        ↓        ↓
            Rewrite  Search    Other
                       ↓
                    Inspect
                       ↓
                     ...
```

## Autonomy Has a Cost

More autonomy is not automatically better. Agentic RAG can introduce **higher latency** (multiple searches take time), **higher cost** (every LLM/tool call has a price), **more complexity** (more moving parts to build and maintain), **unpredictability** (the agent may choose an inefficient path), and **failure loops** (the agent may keep searching without ever reaching a useful result). The rule: **use agents when the problem actually requires dynamic decision-making.**

## Don't Use an Agent for Everything

For *"What is CSE251?"*, a full agent doing `analyze → search → evaluate → search again → compare → answer` is excessive overhead for a question a simple `Query → Retriever → LLM` pipeline already answers well. Agents earn their cost on tasks that are genuinely complex, multi-step, uncertain, multi-source, decision-heavy, or require iterative retrieval.

## A Practical Architecture

```
                         User
                           ↓
                         Agent
                           ↓
                    Analyze Question
                           ↓
                  Choose Retrieval Tool
                           ↓
              ┌────────────┼────────────┐
              ↓            ↓            ↓
          Vector DB       BM25      Web/API
              ↓            ↓            ↓
              └────────────┼────────────┘
                           ↓
                     Retrieved Data
                           ↓
                        Agent
                           ↓
                   Enough evidence?
                      ↙        ↘
                    Yes         No
                     ↓           ↓
                 Generate    New Action
                     ↓           │
                   Answer ←──────┘
```

## Agentic RAG vs. a Fixed Workflow

A **fixed workflow** is `Step 1 → Step 2 → Step 3 → Step 4`, defined in advance, and the system just follows it. An **agent** is instead given available tools, available state, and available rules, and *decides* what to do next at each point. **Workflow → predetermined path. Agent → dynamic path.** This distinction matters a great deal once you start building agent systems more broadly.

## The Key Engineering Principle

Don't ask *"can I turn this RAG system into an agent?"* Ask **"does this problem require dynamic decisions?"** If no: simple RAG. If yes: Agentic RAG. This mindset saves a great deal of unnecessary complexity in real AI engineering projects.

*The single idea to keep:* Agentic RAG hands decision-making -- what to search, whether to search again, when to stop -- to the agent itself, which is genuinely powerful for complex, multi-step, uncertain questions, but pure overhead for questions a fixed pipeline already answers well. RAG provides the knowledge; the agent controls the retrieval process.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design an Agentic Approach",
                    "description": (
                        "User question: \"Compare the graduation requirements of AI Engineering "
                        "and Computer Engineering, including required credit hours and GPA "
                        "conditions.\"\n\n"
                        "Answer: (1) Why might simple RAG struggle with this question? "
                        "(2) What could an Agentic RAG system do differently? "
                        "(3) Give 3 possible tools the agent could use. "
                        "(4) What should the agent do if the first retrieval doesn't contain "
                        "the GPA requirements? "
                        "(5) Why would using an agent be unnecessary for a simple question like "
                        "\"What is CSE251?\""
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "agentic-rag", "critical-thinking"],
                },
                {
                    "title": "Simulate an Agent Decision Loop",
                    "description": (
                        "Implement a simplified agent loop: given stub functions search(query) "
                        "and has_enough_evidence(docs), repeatedly search and evaluate, "
                        "rewriting the query on insufficient evidence, until evidence is "
                        "sufficient or a maximum number of steps is reached. Track and return "
                        "the full state (all queries tried and all documents collected)."
                    ),
                    "starter_code": (
                        "def search(query):\n"
                        "    # stub: pretend this calls the real retriever\n"
                        "    raise NotImplementedError\n\n"
                        "def has_enough_evidence(docs):\n"
                        "    # stub: returns True/False\n"
                        "    raise NotImplementedError\n\n"
                        "def rewrite_query(query, previous_docs):\n"
                        "    # stub: returns an improved query string\n"
                        "    raise NotImplementedError\n\n"
                        "def agent_loop(question, max_steps=3):\n"
                        "    # TODO: build state = {\"queries\": [], \"retrieved_docs\": []},\n"
                        "    # search, check evidence, rewrite and retry up to max_steps,\n"
                        "    # then return the final state.\n"
                        "    pass\n"
                    ),
                    "solution_code": (
                        "def agent_loop(question, max_steps=3):\n"
                        "    state = {\"queries\": [question], \"retrieved_docs\": []}\n"
                        "    current_query = question\n"
                        "    for step in range(max_steps):\n"
                        "        docs = search(current_query)\n"
                        "        state[\"retrieved_docs\"].extend(docs)\n"
                        "        if has_enough_evidence(state[\"retrieved_docs\"]):\n"
                        "            break\n"
                        "        current_query = rewrite_query(current_query, state[\"retrieved_docs\"])\n"
                        "        state[\"queries\"].append(current_query)\n"
                        "    return state\n"
                    ),
                    "difficulty": DifficultyLevel.advanced,
                    "skill_tested": ["rag", "agentic-rag", "python"],
                },
            ],
            "quiz": {
                "title": "Agentic RAG — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the defining difference between traditional RAG and Agentic RAG?",
                        "options": [
                            "Agentic RAG always uses a larger embedding model",
                            "Traditional RAG follows a fixed retrieval pipeline; Agentic RAG lets an agent dynamically decide what to do next at each step",
                            "Agentic RAG never uses a vector database",
                            "Traditional RAG cannot use reranking",
                        ],
                        "correct": 1,
                        "explanation": (
                            "The core distinction is decision-making: traditional RAG runs a "
                            "predetermined sequence of steps, while an agent in Agentic RAG "
                            "actively decides what action to take next based on what it's found so far."
                        ),
                    },
                    {
                        "question": "How does Agentic RAG relate to Corrective RAG?",
                        "options": [
                            "They are unrelated techniques",
                            "Corrective RAG typically uses a fixed correction strategy; Agentic RAG lets the agent decide which correction (or other action) to take, making the workflow more dynamic",
                            "Agentic RAG replaces the need for retrieval evaluation entirely",
                            "Corrective RAG can only be used inside an agent",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Corrective RAG's evaluate-and-correct loop can be implemented as a "
                            "fixed workflow, or an agent can be given the autonomy to choose "
                            "among several possible corrective actions -- that added autonomy is "
                            "what makes it 'agentic.'"
                        ),
                    },
                    {
                        "question": (
                            "For the question 'Compare the graduation requirements of AI "
                            "Engineering and Computer Engineering,' why might Agentic RAG "
                            "outperform a single fixed retrieval pass?"
                        ),
                        "options": [
                            "Agentic RAG always uses a bigger context window",
                            "The agent can decompose the task into separate searches for each program and combine the results, which a single retrieval pass over one query might miss",
                            "Agentic RAG skips retrieval entirely and answers from memory",
                            "Fixed retrieval pipelines cannot process comparison questions at all",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Complex, multi-part questions often benefit from being broken into "
                            "sub-tasks with separate retrieval steps -- exactly the kind of "
                            "decomposition an agent can perform that a single fixed query cannot."
                        ),
                    },
                    {
                        "question": "What is a real cost of adding agent autonomy to a RAG system?",
                        "options": [
                            "Agents always reduce cost and latency compared to fixed pipelines",
                            "Higher latency and cost from multiple tool/LLM calls, more system complexity, and the risk of inefficient or looping behavior",
                            "Agents cannot use vector search or BM25 as tools",
                            "Agentic RAG requires no evaluation of retrieved evidence",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Autonomy isn't free -- more decision points mean more calls, more "
                            "latency, more complexity, and a real risk of the agent choosing an "
                            "inefficient path or looping without converging."
                        ),
                    },
                    {
                        "question": "Why would using a full agentic pipeline for 'What is CSE251?' likely be unnecessary?",
                        "options": [
                            "Agents cannot answer simple factual questions",
                            "The question is simple and well-served by a single retrieval pass, so the added decision-making overhead provides little benefit for real added cost",
                            "CSE251 is not a valid search term for an agent",
                            "Simple questions cannot be represented as agent state",
                        ],
                        "correct": 1,
                        "explanation": (
                            "For simple, single-step questions, a fixed 'Query → Retriever → "
                            "LLM' pipeline already works well, so the extra latency and "
                            "complexity of an agent isn't justified by the problem's actual difficulty."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 15
            # ------------------------------------------------------------
            "title": "Graph RAG Concepts",
            "slug": "ai-developer-advanced-rag-graph-rag-concepts",
            "description": (
                "Retrieving through explicit entities and relationships rather "
                "than isolated chunks, for multi-hop questions that depend on "
                "chains like course prerequisites."
            ),
            "order": 15,
            "difficulty": DifficultyLevel.advanced,
            "estimated_hours": 1.0,
            "skill_tags": ["rag", "graph-rag", "knowledge-graph", "retrieval"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Graph RAG Concepts",
                "content": """# Graph RAG Concepts

Everything so far has focused on improving retrieval *within* documents. Today's question is different: **what if the important information isn't just inside individual documents, but in the relationships between entities?** That's the motivation behind Graph RAG.

## The Problem With Normal RAG

Suppose your knowledge base encodes: `CSE251 → prerequisite → CSE201`, `CSE301 → prerequisite → CSE251`, `CSE302 → prerequisite → CSE301`. A normal vector search can find the document about CSE301. But if the user asks *"What courses do I need to take before CSE302?"*, the answer requires following a chain: `CSE302 → CSE301 → CSE251 → CSE201`. That's fundamentally a **relationship** problem, not a similarity problem.

## What Is a Graph?

A graph has **nodes** (entities -- `CSE302, CSE301, CSE251, CSE201`) and **edges** (relationships between them -- `CSE302 --requires--> CSE301`, `CSE301 --requires--> CSE251`, `CSE251 --requires--> CSE201`). **Graph = Nodes + Relationships.**

## Traditional RAG vs. Graph RAG

Traditional RAG asks *"which chunks are semantically similar to my question?"*: `Query → Embedding → Vector Search → Relevant Chunks`. Graph-based retrieval asks *"which entities and relationships are connected to the question?"*: `Query → Identify entities → Traverse relationships → Relevant nodes/subgraph → LLM`.

## A Simple Example

`(Mohamed) --enrolled_in--> (CSE251)`, `(CSE251) --prerequisite--> (CSE201)`. For the question *"What prerequisite does Mohamed need for his course?"*, the system follows `Mohamed → CSE251 → CSE201` -- relationship-based reasoning rather than similarity matching.

## Why This Is Useful

Graph-based retrieval shines for questions about relationships, dependencies, hierarchies, networks, multiple entities, and **multi-hop** questions -- *"Which courses depend on CSE251?"*, *"Who manages the team that owns Project X?"*, *"Which products depend on this component?"*, *"Which drugs interact with medications in this category?"*, *"What papers cite research from this author?"* These are all fundamentally about connections.

## What Is a "Hop"?

A hop is one relationship traversal. `CSE302 → CSE301` is one hop. `CSE302 → CSE301 → CSE251` is two hops. `CSE302 → CSE301 → CSE251 → CSE201` is three hops. A question requiring several connected relationships is called a **multi-hop question**.

## Where Normal Retrieval Misses the Chain

Document A says *"CSE302 requires CSE301,"* Document B says *"CSE301 requires CSE251,"* Document C says *"CSE251 requires CSE201."* If the user asks *"What is the earliest prerequisite in the CSE302 prerequisite chain?"*, the answer is `CSE201` -- but **no single document says that directly**. You have to connect `CSE302 → CSE301 → CSE251 → CSE201` across three separate documents. A graph naturally represents exactly this structure.

## Building a Knowledge Graph

*"CSE301 requires CSE251"* can be extracted into a **triple**: `(Subject: CSE301, Relationship: requires, Object: CSE251)`, or simply `(CSE301, requires, CSE251)`. A graph accumulates many such triples -- `(CSE302, requires, CSE301)`, `(CSE301, requires, CSE251)`, `(CSE251, requires, CSE201)` -- forming a structured representation of relationships.

## Graph + RAG, Combined

Graph RAG doesn't have to replace your vector database -- the two combine naturally:

```
                    User Query
                         ↓
                 Query Understanding
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
         Vector Search         Graph Search
              ↓                     ↓
         Semantic chunks       Relationships
              └──────────┬──────────┘
                         ↓
                    Combine Context
                         ↓
                         LLM
```

**Vector search** is good at *"find text that means something similar."* **Graph search** is good at *"follow relationships."* `Vector → semantic similarity. Graph → relationships.`

## A Worked Example

*"Which courses are indirectly dependent on CSE201?"* A vector database might retrieve documents that merely *mention* CSE201. A graph can instead traverse `CSE201 ← CSE251 ← CSE301 ← CSE302`, identifying the entire dependency chain based on relationship direction. The graph provides structure that isn't obvious from isolated chunks alone.

## Graph RAG Beyond Courses

An enterprise knowledge base might have `Employee → works_on → Project → owned_by → Department → managed_by → Manager`. A technical system might have `Service A → depends_on → Service B → uses → Database C`. A research corpus might have `Researcher → authored → Paper → cites → Paper → studies → Topic`. The graph's shape depends entirely on the domain.

## Graph RAG vs. Knowledge Graph

These are related but distinct. A **Knowledge Graph** is the structured data itself -- `Entity → relationship → Entity`. **Graph RAG** is the retrieval/application *architecture* that uses that graph structure during retrieval and reasoning. `Knowledge Graph → data structure. Graph RAG → retrieval architecture using graph information.`

## You Don't Need a Graph for Everything

For *"What is CSE251?"*, a simple vector search is almost certainly sufficient -- there's no need to construct a graph just to retrieve one definition. Graph approaches earn their complexity when questions genuinely require chains like `A related to B, B related to C, C related to D`.

## In a Bilingual Academic RAG System

Given `CSE201 ← CSE251 ← CSE301 ← CSE401` as a prerequisite chain, a student asking *"إيه المواد اللي محتاج أخلصها قبل CSE401؟"* benefits from the graph traversing `CSE401 → CSE301 → CSE251 → CSE201` directly -- far more structured than retrieving four loosely related, unconnected chunks and hoping the LLM reconstructs the chain correctly.

## Reverse Traversal Example

*"What courses become available after I complete CSE251?"* is essentially asking: *find all nodes where `prerequisite → CSE251`.* Given `CSE301 --prerequisite--> CSE251`, `CSE302 --prerequisite--> CSE251`, `CSE401 --prerequisite--> CSE301`, the graph directly identifies `CSE301` and `CSE302` as the answer.

## Graph Traversal

The basic operation is simply walking edges: from `A → B → C → D`, traverse sequentially, or explore multiple neighbors at once (`A` connecting to `B`, `C`, and `D`). This lets you retrieve a relevant *subgraph* for a given question rather than one isolated fact.

## Alongside the Existing Pipeline

```
                         Query
                           ↓
                    Query Analysis
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
       Text Retrieval              Graph Retrieval
              ↓                         ↓
       Dense + BM25                Graph Traversal
              ↓                         ↓
             RRF?                       ↓
              ↓                         ↓
              └────────────┬────────────┘
                           ↓
                       Context
                           ↓
                          LLM
```

Graph retrieval becomes another retrieval *path*, not a replacement for the others -- the exact combination depends on the application.

## The Biggest Advantage

Graph RAG **makes relationships explicit**. Instead of isolated `Chunk A, Chunk B, Chunk C`, you get `A --depends_on--> B --depends_on--> C` -- structure that makes complex relational questions far easier to answer correctly.

## The Biggest Disadvantage

Building and maintaining a graph is not free. It requires extracting entities, extracting relationships, resolving duplicate entities, storing the graph, keeping it updated, handling incorrect relationships, and designing graph schemas. `"Machine Learning"`, `"ML"`, `"Machine Learning Course"`, and `"CSE251"` might all refer to the same entity -- resolving that requires real **entity resolution** work. Graph RAG can introduce significant engineering complexity.

## Don't Use It Just Because It's Advanced

If your application mostly asks *"find the paragraph that explains X,"* Vector Search + BM25 + Reranking is probably sufficient. If it asks *"how is X connected to Y through multiple relationships?"*, a graph becomes genuinely valuable. `Simple semantic question → Vector RAG. Relationship-heavy question → Graph RAG.`

## The Level 6 Toolkit, in Full

```
Dense Retrieval → BM25 → Sparse Retrieval → Hybrid Search → RRF →
Reranking → Cross-Encoders → Query Rewriting → Query Expansion →
Multi-Query Retrieval → Parent-Child Retrieval → Context Compression →
Corrective RAG → Graph RAG
```

*The single idea to keep:* a production system typically uses a carefully selected *subset* of this toolkit, chosen for the actual problem, not the entire list -- vector retrieval answers "what's similar," graph retrieval answers "what's connected," and multi-hop, relationship-heavy questions are the clear signal to reach for the latter.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Trace the Prerequisite Chain",
                    "description": (
                        "Given: CSE251 → prerequisite → CSE201, CSE301 → prerequisite → "
                        "CSE251, CSE401 → prerequisite → CSE301.\n\n"
                        "User asks: \"What courses are in the prerequisite chain for CSE401?\"\n\n"
                        "Answer: (1) Why is this a good Graph RAG problem? "
                        "(2) What nodes exist in the graph? "
                        "(3) What relationships exist? "
                        "(4) What is the path starting from CSE401? "
                        "(5) Why might vector search alone be less natural for this question? "
                        "(6) Would you use Graph RAG for the simple question \"What is CSE401?\" Why?"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "graph-rag", "critical-thinking"],
                },
                {
                    "title": "Traverse a Prerequisite Graph",
                    "description": (
                        "Given a graph represented as an adjacency dict mapping each course to "
                        "its direct prerequisite, write a function that returns the full "
                        "prerequisite chain for a given course, from most immediate to earliest."
                    ),
                    "starter_code": (
                        "prerequisites = {\n"
                        "    \"CSE401\": \"CSE301\",\n"
                        "    \"CSE301\": \"CSE251\",\n"
                        "    \"CSE251\": \"CSE201\",\n"
                        "}\n\n"
                        "def prerequisite_chain(course, prerequisites):\n"
                        "    # TODO: follow the chain starting from `course` until there is no\n"
                        "    # further prerequisite, returning the list of prerequisites in order.\n"
                        "    pass\n\n"
                        "print(prerequisite_chain(\"CSE401\", prerequisites))\n"
                        "# expected: ['CSE301', 'CSE251', 'CSE201']\n"
                    ),
                    "solution_code": (
                        "def prerequisite_chain(course, prerequisites):\n"
                        "    chain = []\n"
                        "    current = course\n"
                        "    while current in prerequisites:\n"
                        "        current = prerequisites[current]\n"
                        "        chain.append(current)\n"
                        "    return chain\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["rag", "graph-rag", "python"],
                },
            ],
            "quiz": {
                "title": "Graph RAG Concepts — Knowledge Check",
                "questions": [
                    {
                        "question": "What core problem does Graph RAG address that vector search alone struggles with?",
                        "options": [
                            "Finding text that is semantically similar to a query",
                            "Answering questions that depend on chains of relationships across multiple entities (multi-hop questions)",
                            "Reducing the number of tokens sent to the LLM",
                            "Speeding up embedding generation",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Graph RAG is specifically suited to multi-hop, relationship-based "
                            "questions where the answer requires connecting several linked "
                            "entities rather than finding one similar chunk."
                        ),
                    },
                    {
                        "question": "What are the two basic building blocks of a graph?",
                        "options": [
                            "Chunks and embeddings",
                            "Nodes (entities) and edges (relationships between them)",
                            "Documents and vectors",
                            "Queries and answers",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A graph is fundamentally nodes representing entities connected by "
                            "edges representing relationships between them."
                        ),
                    },
                    {
                        "question": (
                            "Why can normal document-based RAG miss the answer to 'What is the "
                            "earliest prerequisite in the CSE302 prerequisite chain?' even if "
                            "each individual link (CSE302→CSE301, CSE301→CSE251, etc.) is "
                            "documented separately?"
                        ),
                        "options": [
                            "The documents contain factual errors",
                            "No single document states the full chain -- the answer requires connecting several separate relationship facts together, which a graph represents naturally but isolated chunks do not",
                            "Vector databases cannot store numbers",
                            "BM25 cannot process course codes",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Each prerequisite link may be documented in a separate chunk with no "
                            "single chunk stating the full chain -- a graph explicitly represents "
                            "and can traverse that chain, while isolated chunk retrieval cannot."
                        ),
                    },
                    {
                        "question": "What is the difference between a Knowledge Graph and Graph RAG?",
                        "options": [
                            "They are the same concept with different names",
                            "A Knowledge Graph is the structured data (entities and relationships); Graph RAG is the retrieval architecture that uses that graph during retrieval and reasoning",
                            "A Knowledge Graph only stores numbers; Graph RAG only stores text",
                            "Graph RAG replaces the need for a Knowledge Graph entirely",
                        ],
                        "correct": 1,
                        "explanation": (
                            "The Knowledge Graph is the underlying data structure; Graph RAG is "
                            "the application-level pattern of using that structure to retrieve "
                            "and reason over connected information."
                        ),
                    },
                    {
                        "question": "When is Graph RAG NOT worth the added complexity?",
                        "options": [
                            "When questions require following multi-hop relationships between many entities",
                            "When most questions are simple lookups like 'What is CSE251?' that a plain vector search already answers well",
                            "When the domain has clear hierarchical relationships",
                            "When entities have many interconnected dependencies",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Building and maintaining a graph (entity extraction, relationship "
                            "extraction, entity resolution) is significant overhead that isn't "
                            "justified when simple semantic retrieval already answers most questions well."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # ------------------------------------------------------------
            # Topic 16 (Level 6 capstone)
            # ------------------------------------------------------------
            "title": "Production RAG Project",
            "slug": "ai-developer-advanced-rag-production-rag-project",
            "description": (
                "Capstone: assembling the Advanced RAG toolkit into a realistic, "
                "phased production architecture -- with citations, guardrails, "
                "observability, and evaluation -- instead of using every "
                "technique at once."
            ),
            "order": 16,
            "difficulty": DifficultyLevel.advanced,
            "estimated_hours": 2.0,
            "skill_tags": ["rag", "production", "system-design", "capstone"],
            "prerequisite_ids": [],
            "lesson": {
                "title": "Production RAG Project",
                "content": """# Production RAG Project

🎉 The final lesson of Level 6. Here, instead of learning a new technique, we stop and put everything together into a production-style RAG architecture. The goal isn't to use every technique you've learned -- it's to understand **how an AI Engineer chooses the right components for the actual problem.**

## From "RAG Demo" to Production RAG

A basic RAG project looks like `Documents → Chunks → Embeddings → Vector DB → Retriever → LLM → Answer`. That's fine for learning. A production system needs considerably more: `User → API → Query Processing → Retrieval → Reranking → Context Management → Generation → Citations → Validation → Response`, all surrounded by logging, evaluation, monitoring, security, caching, and error handling.

## A Realistic Production Architecture

```
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    └──────┬──────┘
                           │
                           ▼
                   Query Processing
                           │
                           ▼
                ┌─────────────────────┐
                │ Query Rewriting     │
                │ Query Expansion     │
                │ Intent Detection    │
                └──────────┬──────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │    Hybrid Retrieval     │
              │                         │
              │ Dense + BM25 + RRF      │
              └────────────┬────────────┘
                           │
                           ▼
                      Reranking
                           │
                           ▼
                   Parent Retrieval
                           │
                           ▼
                 Context Compression
                           │
                           ▼
                Retrieval Evaluation
                           │
                    ┌──────┴──────┐
                    │             │
                  Good          Bad
                    │             │
                    ▼             ▼
                  LLM       Correct Retrieval
                    │
                    ▼
                 Citations
                    │
                    ▼
                Validation
                    │
                    ▼
                 Response
```

## Don't Build Everything at Once

Starting with Dense + BM25 + RRF + Reranker + Query Rewriting + Multi-query + Corrective RAG + Graph RAG all at once is a maintenance nightmare. Build in phases instead:

**Phase 1**: `Documents → Chunks → Embeddings → Qdrant → Retriever → LLM`. Get it working, end to end.
**Phase 2**: improve retrieval -- add `Dense + BM25 → Hybrid → RRF`.
**Phase 3**: improve precision -- add a `Reranker`.
**Phase 4**: improve context -- add `Parent Retrieval` and `Compression`.
**Phase 5**: handle failures -- add retrieval `Evaluate → Correct if necessary`.
**Phase 6**: only if actually needed -- Graph RAG, and other more specialized techniques.

## The Capstone Project: Production-Grade Arabic Academic RAG Assistant

Given your existing experience with Arabic RAG, Qdrant, BM25, RRF, rerankers, and LLMs, this is a natural project to consolidate everything from this level.

**Backend**: FastAPI, Qdrant (vector DB), BM25 (sparse retrieval), a multilingual embedding model (dense retrieval), hybrid retrieval (`Dense + BM25 → RRF`), a Cross-Encoder reranker, and an LLM for generation. **Optional advanced components, added only where evaluation shows a real need**: query rewriting, context compression, corrective RAG, graph retrieval for prerequisite-chain questions.

## Data Ingestion Pipeline

```
PDF / DOCX
    ↓
Document Loader
    ↓
Parsing
    ↓
Cleaning
    ↓
Chunking
    ↓
Metadata
    ↓
Embeddings
    ↓
Qdrant
```

```python
document = load_document(path)
cleaned = clean_text(document)
chunks = chunk_document(cleaned)

for chunk in chunks:
    vector = embed(chunk.text)
    qdrant.upsert(
        vector=vector,
        payload={
            "text": chunk.text,
            "course": chunk.course,
            "section": chunk.section,
            "page": chunk.page,
        }
    )
```

Preserving **metadata** (course, section, page) at ingestion time is what makes filtering and citations possible later.

## The Query Pipeline

For *"ما هي متطلبات التخرج؟"*: `FastAPI → Query Processing → Retrieval`. Optionally, the query is first rewritten -- e.g. into `"متطلبات التخرج لبرنامج هندسة الذكاء الاصطناعي"` -- then run through `Dense Search + BM25 → RRF → Candidate Docs`.

## Reranking in Practice

If RRF produces candidates A through E, the Cross-Encoder scores each: `Query + A → 0.94`, `Query + B → 0.91`, `Query + C → 0.52`, `Query + D → 0.34`, `Query + E → 0.21`. Keeping only A and B gives the LLM meaningfully better context than passing all five through.

## Context Construction

```
SYSTEM:
You are an academic assistant.
Answer only using the provided context.

CONTEXT:

[Source 1]
متطلبات التخرج...

[Source 2]
يشترط إتمام...

QUESTION:
ما هي متطلبات التخرج؟
```

The LLM receives the question plus relevant evidence -- never the entire database.

## Citations

A production system should tell the user *where the answer came from*:

```
متطلبات التخرج تشمل إتمام الساعات المعتمدة المطلوبة
وتحقيق الحد الأدنى للمعدل التراكمي.

Sources:
- Academic Regulations — Page 42
- Graduation Requirements — Page 45
```

This matters enormously for academic, legal, enterprise, medical, and financial systems -- anywhere users need to *verify* an answer, not just receive one.

## Metadata Powers Filtering

If each chunk carries `{"text": ..., "course_code": "CSE251", "department": "AI", "section": "Prerequisites", "page": 37, "document": "Academic_Regulations.pdf"}`, a query like *"Give me information about CSE251"* can filter Qdrant on `course_code = CSE251` before running vector search -- dramatically improving retrieval quality by narrowing the search space up front.

## Production Guardrails

The LLM shouldn't just get `Question + Documents` and be left to its own judgment. Define explicit rules: use only provided evidence, don't invent facts, say so explicitly if evidence is insufficient, preserve numbers exactly, cite supporting sources, and answer in the language the user asked in. This is especially important for an academic assistant where precision matters.

## Handling Retrieval Failure

If retrieval finds no useful evidence, the system should never immediately hallucinate an answer. Instead: `Retrieval → Evaluate → Insufficient → Corrective retrieval → Search again`, and if that still fails: *"I couldn't find sufficient information in the available academic documents."* That's a far better outcome than a confident, fabricated answer.

## Observability

Production AI systems need to answer *"what happened when this answer was generated?"* Log the request ID, the user's query, the rewritten query, retrieved documents, retrieval scores, reranker scores, the final context, model used, latency, token usage, and the final answer. If a user reports a wrong answer, you can inspect exactly where things went wrong -- e.g. discovering "wrong documents were retrieved" tells you the problem is in retrieval, not generation.

## Evaluation

Build an evaluation dataset pairing questions with expected evidence -- e.g. `"What are CSE251 prerequisites?" → CSE251 prerequisite section`, `"What GPA is required?" → Graduation requirements`, `"How many credits?" → Program requirements`. Then measure retrieval accuracy, context relevance, answer relevance, faithfulness, and citation accuracy -- letting you compare Version 1 against Version 2 with actual numbers instead of "it seems better."

## RAG Is an Engineering System

This is the most important lesson of the entire level: **RAG isn't simply `LLM + Vector DB`.** A serious RAG system is `Data + Retrieval + Ranking + Context Management + Generation + Evaluation + Monitoring + Security` -- and each layer can fail independently.

## Debugging in Failure Layers

When the final answer is wrong, don't immediately blame the LLM. Work backward through the pipeline: was the document loaded correctly (ingestion)? Parsed correctly (parsing)? Chunked correctly (chunking)? Retrieved at all (retrieval)? Ranked correctly (reranking)? Was useful context preserved (compression/context)? Did the LLM actually use the evidence correctly (generation/prompt)? This layered debugging mindset is one of the most valuable habits an AI Engineer can build.

## The Full Architecture

```
                         ┌──────────────┐
                         │   Documents  │
                         └──────┬───────┘
                                ↓
                    ┌────────────────────┐
                    │ Ingestion Pipeline │
                    └─────────┬──────────┘
                              ↓
                    Cleaning + Chunking
                              ↓
                         Embeddings
                              ↓
                         ┌────────┐
                         │ Qdrant │
                         └────────┘


USER
 ↓
FastAPI
 ↓
Query Processing
 ↓
Query Rewriting
 ↓
 ┌─────────────────────────────┐
 │ Dense Search + BM25         │
 │             ↓               │
 │            RRF              │
 └──────────────┬──────────────┘
                ↓
            Reranking
                ↓
        Parent Retrieval
                ↓
       Context Compression
                ↓
       Retrieval Evaluation
                ↓
          ┌─────┴─────┐
          ↓           ↓
        Good         Bad
          ↓           ↓
         LLM      Corrective RAG
          ↓
       Citations
          ↓
      Validation
          ↓
       Response
```

With logging, monitoring, evaluation, caching, and security wrapped around the whole system.

## One Important Warning

Knowing many advanced RAG techniques doesn't mean your next project should contain all of them. A better default is `Dense + BM25 → RRF → Reranker → LLM`, adding query rewriting, compression, corrective RAG, or graph retrieval **only when your evaluation shows a real problem** those techniques would actually fix. That shift -- from *"I know RAG techniques"* to *"I can engineer a RAG system"* -- is exactly what this level has been building toward.

## Level 6 Achievement

You've moved from individual retrieval concepts to a full architecture, understanding the distinct role of Dense Retrieval, BM25, Sparse Retrieval, Hybrid Search, RRF, Reranking, Cross-Encoders, Query Rewriting, Query Expansion, Multi-Query Retrieval, Parent-Child Retrieval, Context Compression, Corrective RAG, and Graph RAG.

*The single idea to keep:* the real skill was never memorizing technique names -- it's being able to say **"my RAG system has problem X, therefore I should consider technique Y,"** build in phases, evaluate honestly, and only add complexity where the evaluation proves it's needed. There is no single "best RAG" -- there's diagnosing the failure, choosing the technique, evaluating, and improving.
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design the Full Pipeline",
                    "description": (
                        "You're building an Arabic university RAG assistant. A user asks: "
                        "\"ما هي المواد التي يجب أن أنجح فيها قبل تسجيل CSE401؟\" Your system "
                        "currently retrieves poor results.\n\n"
                        "Design the pipeline, addressing: "
                        "(1) Would you use Dense Retrieval, BM25, or both? "
                        "(2) Why might RRF help? "
                        "(3) Would you use a reranker? "
                        "(4) Could Parent-Child Retrieval help? "
                        "(5) What would Context Compression do? "
                        "(6) What happens if retrieval is still poor? "
                        "(7) Would Graph RAG be useful for the prerequisite chain? "
                        "(8) At what point should the LLM generate the final answer? "
                        "(9) What should happen if the system cannot find reliable evidence?"
                    ),
                    "difficulty": DifficultyLevel.advanced,
                    "skill_tested": ["rag", "system-design", "critical-thinking"],
                },
                {
                    "title": "Diagnose the Failure Layer",
                    "description": (
                        "A user asks \"What are CSE251 prerequisites?\" and receives a wrong "
                        "answer. For each scenario below, identify which failure layer "
                        "(ingestion, parsing, chunking, retrieval, reranking, "
                        "compression/context, or generation/prompt) is responsible:\n\n"
                        "1. The retrieved documents are entirely about CSE252, not CSE251.\n"
                        "2. The correct CSE251 prerequisites document was retrieved and ranked "
                        "first, but the LLM's answer states the wrong prerequisite courses.\n"
                        "3. The prerequisites section exists in the source PDF but was never "
                        "indexed at all.\n"
                        "4. The correct chunk was retrieved and reranked to the top, but "
                        "compression accidentally dropped the sentence containing the actual "
                        "prerequisite codes."
                    ),
                    "difficulty": DifficultyLevel.advanced,
                    "skill_tested": ["rag", "debugging", "system-design"],
                },
            ],
            "quiz": {
                "title": "Production RAG Project — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the recommended approach to building a production RAG system's components?",
                        "options": [
                            "Implement every advanced technique (rewriting, multi-query, graph RAG, etc.) from day one",
                            "Build in phases -- start with a basic working pipeline, then add hybrid search, reranking, context handling, and failure handling incrementally as evaluation shows a need",
                            "Only ever use a single embedding model with no retrieval enhancements",
                            "Always start with Graph RAG since it's the most powerful technique",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A phased approach -- basic pipeline first, then hybrid retrieval, "
                            "then reranking, then context handling, then failure handling -- "
                            "avoids building unnecessary complexity that evaluation hasn't justified."
                        ),
                    },
                    {
                        "question": "Why does preserving metadata (course_code, section, page) at ingestion time matter for a production RAG system?",
                        "options": [
                            "It has no practical use beyond storage bookkeeping",
                            "It enables filtered retrieval (e.g. searching only within a specific course) and supports citations back to specific sources",
                            "It replaces the need for embeddings entirely",
                            "It is required for BM25 to function at all",
                        ],
                        "correct": 1,
                        "explanation": (
                            "Metadata lets you filter the search space before or during "
                            "retrieval and lets you cite exactly where an answer's evidence came "
                            "from, both of which matter a great deal in production."
                        ),
                    },
                    {
                        "question": "What should a production RAG system do when retrieval evaluation determines there's insufficient reliable evidence, even after correction attempts?",
                        "options": [
                            "Have the LLM generate its best guess anyway",
                            "Return an honest response stating that sufficient information could not be found, rather than fabricating an answer",
                            "Repeat the same failed query indefinitely until it succeeds",
                            "Silently return an empty response with no explanation",
                        ],
                        "correct": 1,
                        "explanation": (
                            "A well-designed system prefers admitting insufficient evidence over "
                            "hallucinating a confident but unsupported answer, especially in "
                            "domains like academic or legal information."
                        ),
                    },
                    {
                        "question": (
                            "A user reports a wrong answer. Debugging shows the correct document "
                            "was retrieved and ranked first, but the LLM's final answer "
                            "contradicts that document. Which failure layer is implicated?"
                        ),
                        "options": [
                            "Ingestion",
                            "Retrieval",
                            "Generation/prompt -- the LLM failed to use the correct evidence properly",
                            "Chunking",
                        ],
                        "correct": 2,
                        "explanation": (
                            "Since the right document was successfully retrieved and ranked "
                            "first, the failure must be downstream in how the LLM used (or "
                            "ignored) that evidence -- a generation or prompt-design issue."
                        ),
                    },
                    {
                        "question": "What is the central engineering lesson of Level 6, according to the production RAG lesson?",
                        "options": [
                            "Every production RAG system should use all available techniques simultaneously for maximum accuracy",
                            "RAG is a full engineering system (data, retrieval, ranking, context, generation, evaluation, monitoring, security) where each layer can fail independently, and techniques should be chosen based on diagnosed problems, not applied by default",
                            "Vector databases are no longer necessary once you know BM25",
                            "Graph RAG should replace vector search in all production systems",
                        ],
                        "correct": 1,
                        "explanation": (
                            "The core lesson is that RAG is an engineered system with many "
                            "independently-failing layers, and the right technique is the one "
                            "that fixes a diagnosed, evaluated problem -- not a default checklist "
                            "to apply everywhere."
                        ),
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": "Production-Grade Arabic Academic RAG Assistant",
                "description": (
                    "Design and build a phased, production-style RAG system for an Arabic "
                    "academic advisor use case, covering ingestion, hybrid retrieval, "
                    "reranking, context construction with citations, guardrails, retrieval "
                    "evaluation with corrective fallback, and basic observability -- following "
                    "the six-phase build order rather than implementing every technique at once."
                ),
                "difficulty": DifficultyLevel.advanced,
                "tech_stack": ["Python", "FastAPI", "Qdrant", "rank_bm25", "sentence-transformers"],
                "objectives": [
                    "Phase 1: build a basic working pipeline (chunk, embed, store in Qdrant, retrieve, generate)",
                    "Phase 2: add BM25 and combine with dense retrieval via RRF",
                    "Phase 3: add a Cross-Encoder reranking step over fused candidates",
                    "Phase 4: add parent-lookup context and, if needed, context compression",
                    "Phase 5: add a retrieval evaluation step with a bounded corrective-retry loop",
                    "Preserve chunk metadata (course_code, section, page, document) for filtering and citations",
                    "Construct prompts with explicit guardrails: evidence-only answers, no invented facts, cite sources, preserve numbers exactly",
                    "Log request ID, query, rewritten query, retrieved documents and scores, final context, and latency for each request",
                    "Build a small evaluation dataset (question -> expected evidence) to measure retrieval and answer quality",
                ],
                "rubric": {
                    "phased_build": "Components were added incrementally and each phase is independently functional",
                    "retrieval_quality": "Hybrid retrieval with RRF measurably outperforms single-method retrieval on the evaluation set",
                    "citations_and_guardrails": "Responses include source citations and refuse to answer beyond available evidence",
                    "failure_handling": "Retrieval evaluation and corrective retry are implemented with a hard retry limit and honest fallback message",
                    "observability": "Logs capture enough detail to diagnose which pipeline layer caused a wrong answer",
                },
                "starter_repo_url": None,
                "estimated_hours": 10.0,
            },
        },
    ],
}
