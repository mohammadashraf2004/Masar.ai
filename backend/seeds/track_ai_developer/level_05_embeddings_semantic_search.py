"""
backend/seeds/track_ai_developer/level_05_embeddings_semantic_search.py

Level 5 of the "AI Developer" career track: Embeddings & Semantic Search.

NOTE ON STRUCTURE: I don't yet have your `common.py` or a completed level
file (e.g. level_04_prompt_engineering.py) to mirror exactly, so this module
exposes its data as a single `LEVEL` dict shaped the same way as one entry
of the old `LEVELS` list in seed_track_ai_developer.py (title/description/
order/topics, each topic carrying TOPIC_FIELDS + lesson/exercises/quiz/
project). Once you share common.py, tell me how level files are expected to
plug in (e.g. does seed_track_ai_developer.py import `LEVEL` by name, call a
`get_level()` function, or something else?) and I'll adjust the export
without touching the content below.
"""

from app.models.learning import DifficultyLevel

LEVEL = {
    "title":       "Level 5: Embeddings & Semantic Search",
    "description": "Understand what embeddings are, why they power semantic search and RAG, and how they differ from LLMs and from vector databases like FAISS/Qdrant/Chroma.",
    "order":       5,
    "topics": [
        {
            # Topic fields
            "title":            "What Are Embeddings?",
            "slug":              "embeddings-what-are-embeddings",
            "description":       "The core mental model for this level: an embedding is a numerical representation of meaning, used to compare and search information by similarity rather than exact wording.",
            "order":             1,
            "difficulty":        DifficultyLevel.beginner,
            "estimated_hours":   1.5,
            "skill_tags":        ["embeddings", "semantic-search", "vector-search", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "What Are Embeddings?",
                "content": """# What Are Embeddings?

You have already used embeddings with models like multilingual-e5, FAISS, Qdrant, and Chroma. Now let's understand what an embedding actually is.

## 1. The basic idea

An **embedding** is a way to represent something as a list of numbers so that a computer can understand its meaning and relationships.

For example, the sentence:

> "I love programming"

might become something conceptually like:

```
[0.21, -0.73, 0.15, 0.92, ...]
```

Maybe it has 384 numbers. We call this list a **vector**.

So: **Embedding = numerical representation of meaning.**

## 2. Why do we need this?

Computers don't naturally understand that these two sentences are related:

- "I want to buy a car"
- "I'm looking for a vehicle"

The words are different, but their meaning is similar. An embedding model tries to represent them in a mathematical space where similar meanings are located relatively close together.

```
                    "I want to buy a car"
                              ●
                           /
                         /
                       /
                     ●
             "I'm looking for a vehicle"
```

While something unrelated might be farther away:

```
"How do I cook pasta?"
                    ●


"I want to buy a car"
                    ●
                  /
                ●
"I'm looking for a vehicle"
```

This is the fundamental idea behind **semantic search**.

## 3. Think of embeddings as coordinates

Imagine a simple 2-dimensional world:

```
             ↑
             |
        ● Cat
             |
             |       ● Dog
             |
-------------+----------------→
             |
                    ● Car
             |
```

Each object has coordinates, e.g. Cat → [2, 8], Dog → [3, 7], Car → [9, 2]. Cat and Dog are relatively close; Car is farther away.

Real embedding models don't normally use just 2 dimensions — they might use hundreds or thousands:

```
Sentence
   ↓
Embedding Model
   ↓
[0.12, -0.42, 0.77, 0.03, ...]
```

Common sizes are **384**, **768**, or **1024** dimensions, depending on the model.

## 4. Important: the numbers don't have simple meanings

Suppose we have `[0.2, -0.7, 0.4, 0.9]`. You *cannot* normally say "0.2 = cars, -0.7 = price, 0.4 = location, 0.9 = investment." That's not how embeddings work — the meaning is *distributed* across the entire vector.

Think of it like a fingerprint:

```
Embedding
    ↓
[0.21, -0.13, 0.77, 0.42, ...]
         ↑
    entire pattern matters
```

The *relationship between vectors* is usually more useful than interpreting individual dimensions.

## 5. Where does the embedding come from?

```
Text
 ↓
Embedding Model
 ↓
Vector
```

For example:

```
text = "I want to buy an apartment"
embedding = model.encode(text)
```

The model processes the text and produces something like `[0.123, -0.456, 0.781, ...]`. That vector *is* the embedding.

## 6. Embedding models vs LLMs

This distinction matters. An **LLM** is primarily designed to generate or understand language:

```
Question
   ↓
LLM
   ↓
Answer
```

An **embedding model** is designed to convert information into a vector representation useful for comparing and searching:

```
Text
 ↓
Embedding Model
 ↓
Vector
```

For example:

```
"What are the admission requirements?"
                ↓
        Embedding Model
                ↓
[0.12, -0.44, 0.83, ...]
```

We can then compare that vector against vectors representing documents.

## 7. This is exactly what you were doing with FAISS/Qdrant

Suppose you have these documents:

- Document 1: "Students must complete 160 credit hours to graduate."
- Document 2: "The university library is open from 8 AM to 6 PM."
- Document 3: "The minimum GPA required for graduation is 2.0."

You create embeddings for each (vector A, B, C). Then a user asks:

> "How many hours do I need to finish my degree?"

You create another embedding for the query (vector Q), then compare:

```
             Query
               Q
              / \\
             /   \\
            /     \\
           A       C
        Document 1  Document 3
```

Document 1 should be highly relevant because "How many hours do I need to finish my degree?" and "Students must complete 160 credit hours to graduate." have similar *meaning*, even though the wording differs. This is the foundation of your previous RAG retrieval pipeline.

## 8. What does FAISS actually do?

This is a key mental model: **FAISS doesn't magically understand Arabic or English.** It doesn't understand "شروط التخرج" by itself. You first convert the text into vectors:

```
"شروط التخرج"
       ↓
Embedding Model
       ↓
[0.12, -0.42, ...]
```

Then FAISS works with *those vectors*:

```
             Text
              ↓
       Embedding Model
              ↓
           Vector
              ↓
            FAISS
              ↓
     Similar vectors
```

The same basic idea applies to vector databases such as Qdrant, Chroma, Pinecone, and Weaviate. They store and search vectors, although their capabilities and implementations differ.

## 9. Embeddings are not the database

Another important distinction: the **embedding model** creates the vector. **FAISS / Qdrant / Chroma** stores and searches vectors.

```
Text
 ↓
Embedding Model
 ↓
Vector
 ↓
Vector Database
```

For example:

```
text = "Students need 160 credit hours."
vector = embedding_model.encode(text)
vector_db.add(vector)

# Later:
query = "How many credits are required?"
query_vector = embedding_model.encode(query)
results = vector_db.search(query_vector)
```

## 10. Why embeddings are powerful

Traditional keyword search might look for the exact phrase "credit hours." But the user might ask "How many hours do I need to graduate?" — with no exact match in the query. Semantic embeddings let the system focus on *meaning* rather than exact word matching.

That's why embeddings are one of the most important building blocks for:

```
Semantic Search
       ↓
RAG
       ↓
Advanced RAG
       ↓
AI Agents
       ↓
Knowledge-based AI applications
```

## 11. Your Arabic RAG example

This is especially relevant to systems you've already built. Imagine your database contains:

> "يشترط للتخرج إتمام 160 ساعة معتمدة."

The user asks:

> "أنا محتاج أخلص كام ساعة عشان أتخرج؟"

Different wording, but semantically:

```
"إتمام 160 ساعة معتمدة للتخرج"
             ≈
"كام ساعة عشان أتخرج؟"
```

A good Arabic/multilingual embedding model can represent these texts so they end up relatively close in vector space. That's why *multilingual* embedding models matter for your Arabic RAG systems.

## 12. The complete mental model

```
                TEXT
                  ↓
          Embedding Model
                  ↓
              VECTOR
                  ↓
        Store / Search Vector
                  ↓
          Similarity Search
                  ↓
        Relevant Documents
```

And in RAG:

```
Documents
    ↓
Embeddings
    ↓
Vector Database
    ↓
        ← User Query
              ↓
        Query Embedding
              ↓
       Similarity Search
              ↓
       Relevant Documents
              ↓
             LLM
              ↓
            Answer
```

You have already implemented much of this. The difference now is that we're building the mental model *underneath* the code.

## 🧠 Key Takeaways

1. Embedding = numerical representation of information.
2. An embedding is usually a vector containing many numbers.
3. The individual numbers usually don't have simple human-readable meanings.
4. Similar meanings → vectors that can be compared as similar.
5. Embedding models *create* vectors; FAISS/Qdrant/Chroma *store and search* them.

**One sentence to remember:** An embedding converts meaning into a mathematical representation that allows computers to compare and search information by similarity.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Embeddings vs. Vector Databases — Concept Check",
                    "description": (
                        "Without writing code, answer these:\n\n"
                        "1. What is the difference between an embedding model and FAISS?\n\n"
                        "2. Why could these two sentences have similar embeddings?\n"
                        "   \"I want to purchase an apartment\" / \"I'm looking to buy a flat\"\n\n"
                        "3. In your previous RAG system, which happens first — "
                        "(A) Search Qdrant, or (B) Convert the query into an embedding?"
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["embeddings", "semantic-search", "rag"],
                },
            ],
            "quiz": {
                "title": "What Are Embeddings? — Knowledge Check",
                "questions": [
                    {
                        "question": "What is an embedding?",
                        "options": [
                            "A numerical vector representation of the meaning of a piece of data",
                            "A compressed copy of the original text stored for backup",
                            "A SQL index used to speed up keyword search",
                            "A rule-based dictionary mapping words to synonyms",
                        ],
                        "correct": 0,
                        "explanation": "An embedding is a list of numbers (a vector) that represents the meaning of text (or other data) so it can be compared mathematically.",
                    },
                    {
                        "question": "Why might 'I want to buy a car' and 'I'm looking for a vehicle' end up close together in vector space?",
                        "options": [
                            "Because they contain the same exact words",
                            "Because a good embedding model represents similar meanings with similar vectors, regardless of wording",
                            "Because they are the same length in characters",
                            "Because FAISS forces all English sentences to be close together",
                        ],
                        "correct": 1,
                        "explanation": "Embedding models place semantically similar text near each other in vector space even when the exact words differ.",
                    },
                    {
                        "question": "What does FAISS (or Qdrant/Chroma) actually operate on?",
                        "options": [
                            "Raw text directly, using built-in language understanding",
                            "Vectors that were already produced by an embedding model",
                            "SQL tables of keywords",
                            "The LLM's internal weights",
                        ],
                        "correct": 1,
                        "explanation": "FAISS and similar tools store and search vectors — they don't understand language on their own. Text must be converted into a vector by an embedding model first.",
                    },
                    {
                        "question": "What is the key difference between an embedding model and an LLM?",
                        "options": [
                            "There is no difference, they are the same thing",
                            "An LLM only works with images, an embedding model only works with text",
                            "An embedding model converts information into a vector for comparison/search; an LLM generates or understands language to produce answers",
                            "An embedding model is always larger than an LLM",
                        ],
                        "correct": 2,
                        "explanation": "LLMs generate/understand language (question → answer). Embedding models turn text into vectors used for comparison and search.",
                    },
                    {
                        "question": "In a typical RAG pipeline, what happens immediately after a user submits a query?",
                        "options": [
                            "The LLM generates the final answer directly from the raw query",
                            "The query is converted into an embedding, which is then used to search the vector database",
                            "The vector database is searched using the raw query text with no embedding step",
                            "The documents are re-embedded from scratch for every query",
                        ],
                        "correct": 1,
                        "explanation": "The query is embedded first, and that query vector is compared against stored document vectors to find relevant results.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.beginner,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # Topic fields
            "title":            "Vector Representations",
            "slug":              "embeddings-vector-representations",
            "description":       "What a vector actually is, why embeddings use hundreds or thousands of dimensions, and how documents and queries share the same vector space.",
            "order":             2,
            "difficulty":        DifficultyLevel.beginner,
            "estimated_hours":   1.5,
            "skill_tags":        ["embeddings", "vectors", "semantic-search", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Vector Representations",
                "content": """# Vector Representations

In Lesson 1, we learned: **an embedding is a numerical representation of meaning.** Now let's understand what that numerical representation actually looks like, and why we call it a *vector*.

## 1. What is a vector?

In AI, a vector is simply a list of numbers:

```
vector = [0.2, -0.5, 0.8, 0.1]
```

That's a vector with 4 dimensions. You can think of it as a point in space. With two dimensions, `[3, 4]` means `x = 3, y = 4`:

```
        y
        ↑
    5   |
    4   |       ● [3,4]
    3   |
    2   |
    1   |
    0   +----------------→ x
        0  1  2  3  4
```

That's easy to visualize — but embeddings usually have hundreds of dimensions.

## 2. Embeddings are high-dimensional vectors

Real models might produce **384**, **768**, **1024**, or **1536** dimensions. For example:

```
embedding = model.encode("I want to buy an apartment")
print(len(embedding))
# 384
```

```
"I want to buy an apartment"
             ↓
      Embedding Model
             ↓
[0.12, -0.44, 0.71, 0.08, ..., 0.31]
 ↑
 384 numbers
```

We call this a **384-dimensional vector**.

## 3. Why so many dimensions?

Because language is complicated. Consider "I want to buy an apartment in Cairo." — it contains many things at once:

- Object → apartment
- Action → buy
- Location → Cairo
- Intent → purchase
- Topic → real estate

An embedding model needs a rich representation that captures many relationships at once. You shouldn't think "dimension 1 = location, dimension 2 = price, dimension 3 = apartment." Instead: **the whole vector together represents the information.**

## 4. A useful mental model: coordinates

Imagine a fictional 3-dimensional embedding space for "cat," "kitten," "dog," and "car":

```
cat     → [0.8, 0.7, 0.2]
kitten  → [0.82, 0.72, 0.21]
dog     → [0.75, 0.68, 0.25]
car     → [-0.4, 0.1, 0.9]
```

Notice: cat, kitten, and dog are relatively close, while car is much farther away.

```
Vector space
              Animals
                 ↑

          ● kitten
        ● cat
           ● dog


                              ● car
```

The model has transformed language into a mathematical space where relationships can be *measured*.

## 5. This is why vector databases exist

Suppose you have 100,000 documents. You represent each as a vector and store them in Qdrant:

```
Qdrant
 ├── vector 1
 ├── vector 2
 ├── vector 3
 ├── ...
 └── vector 100000
```

When a user asks "How many credits do I need to graduate?", you create a query vector the same way, and Qdrant searches for stored vectors that are close/similar to it.

## 6. Documents and queries live in the same space

This is one of the most important ideas in semantic search. Suppose:

- Document "Students must complete 160 credit hours to graduate." → `D = [0.21, -0.31, 0.77, ...]`
- Query "How many hours are required for graduation?" → `Q = [0.19, -0.29, 0.75, ...]`

The vectors are similar, so `Q ≈ D` — the document becomes a good search result.

## 7. Why this is different from keyword search

Keyword matching might only notice the words "hours" and "graduation" repeated across query and document. Semantic search can recognize the deeper relationship:

```
required hours
        ≈
credit hours needed
        ≈
credits needed to graduate
```

That's the power of representing language as vectors.

## 8. Let's see it with Python

Using Sentence Transformers, which you've already worked with:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

text = "I want to buy an apartment"

embedding = model.encode(text)

print(embedding)
print(len(embedding))
```

You'll get something conceptually like `[0.012, -0.083, 0.214, ..., 0.041]` with length `384`. The important part isn't memorizing the numbers — it's understanding the pipeline: `text → model.encode() → vector`.

## 9. Multiple texts → multiple vectors

```python
texts = [
    "I want to buy an apartment",
    "I'm looking for a flat",
    "How do I cook pasta?"
]

embeddings = model.encode(texts)
```

Conceptually, Text 1 → Vector 1, Text 2 → Vector 2, Text 3 → Vector 3:

```
embeddings
    ↓
[
    [0.12, -0.43, ...],
    [0.15, -0.41, ...],
    [-0.72, 0.11, ...]
]
```

The first two vectors should be more similar to each other than either is to the pasta sentence.

## 10. A very important distinction

There are two different things:

**Vector representation** — the actual numbers: `[0.12, -0.43, 0.81, ...]`

**Similarity** — a mathematical measurement telling us how related two vectors are:

```
Vector A
   ↘
    Similarity → 0.91
   ↗
Vector B
```

We'll study similarity in the next lesson, and go deeper into the most commonly used measure, cosine similarity, after that.

## 11. Connecting everything you've learned

```
             DOCUMENT
                 ↓
          Embedding Model
                 ↓
             VECTOR
                 ↓
          Qdrant / FAISS
                 ↓
              stored
```

Then:

```
              USER QUERY
                   ↓
            Embedding Model
                   ↓
              QUERY VECTOR
                   ↓
          Similarity Search
                   ↓
        Relevant Documents
                   ↓
                  LLM
                   ↓
                Answer
```

The vector is the bridge between human language and mathematical search.

## 🧠 Key Takeaways

1. Vector = list of numbers.
2. An embedding is a vector representation produced by an embedding model.
3. Embeddings usually have hundreds or thousands of dimensions.
4. The entire vector represents the information; individual dimensions usually aren't directly interpretable.
5. Documents and queries can be represented as vectors *in the same space*.
6. Vector databases such as Qdrant, FAISS, and Chroma work with these vectors to enable similarity search.
7. Similarity tells us how close/related two vectors are.

**Mental model:** Human language → Embedding model → High-dimensional vector → Mathematical comparison → Semantic search.
""",
                "estimated_minutes": 25,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Vectors in the Same Space — Concept Check",
                    "description": (
                        "Without writing code, answer these:\n\n"
                        "1. Why does an embedding model typically output hundreds or thousands "
                        "of numbers instead of just one or two?\n\n"
                        "2. In your own words, why must a document and a user query be embedded "
                        "using the same embedding model in order to compare them meaningfully?\n\n"
                        "3. If `model.encode(\"I want to buy an apartment\")` returns a vector of "
                        "length 384, what would you expect `len(model.encode(\"How do I cook pasta?\"))` "
                        "to be, and why?"
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["embeddings", "vectors", "semantic-search"],
                },
            ],
            "quiz": {
                "title": "Vector Representations — Knowledge Check",
                "questions": [
                    {
                        "question": "What is a vector, in the context of embeddings?",
                        "options": [
                            "A single number representing how important a document is",
                            "A list of numbers representing a point in a (usually high-dimensional) space",
                            "A row in a SQL database table",
                            "A compressed image format",
                        ],
                        "correct": 1,
                        "explanation": "A vector is simply a list of numbers, which can be interpreted as coordinates of a point in space.",
                    },
                    {
                        "question": "Why do real embedding models typically produce hundreds or thousands of dimensions instead of just 2 or 3?",
                        "options": [
                            "To make the vectors take up more storage space on purpose",
                            "Because language captures many overlapping relationships (object, action, location, intent, topic, etc.) that need a rich representation",
                            "Because vector databases require a fixed size of exactly 1536",
                            "Higher dimensions are only used to slow down search on purpose for security",
                        ],
                        "correct": 1,
                        "explanation": "Language is complex, and a rich, high-dimensional space is needed to capture many relationships between concepts simultaneously.",
                    },
                    {
                        "question": "For semantic search to work, what must be true about how documents and queries are embedded?",
                        "options": [
                            "They must be embedded with different models optimized for their own type",
                            "They must be embedded into the same vector space so their vectors can be meaningfully compared",
                            "Queries should never be embedded, only documents",
                            "Documents must be embedded first and queries embedded a year later",
                        ],
                        "correct": 1,
                        "explanation": "Documents and queries need to live in the same vector space (i.e., produced by a consistent embedding model) for similarity comparisons to be meaningful.",
                    },
                    {
                        "question": "If two sentences have very different meanings (e.g., 'I want to buy an apartment' vs. 'How do I cook pasta?'), what would you expect about their embedding vectors?",
                        "options": [
                            "They will always have identical vectors",
                            "They should typically be located farther apart in the embedding space than semantically similar sentences",
                            "They will have a different number of dimensions",
                            "There is no expected relationship between meaning and vector position",
                        ],
                        "correct": 1,
                        "explanation": "Embedding models place semantically dissimilar text farther apart, while similar meanings cluster closer together — the dimensionality itself stays fixed for a given model.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.beginner,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # Topic fields
            "title":            "Similarity",
            "slug":              "embeddings-similarity",
            "description":       "How similarity between vectors is measured and used to rank search results, including the difference between similarity and distance, and why cosine similarity is the standard metric for text embeddings.",
            "order":             3,
            "difficulty":        DifficultyLevel.beginner,
            "estimated_hours":   2.0,
            "skill_tags":        ["embeddings", "similarity", "cosine-similarity", "semantic-search", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Similarity",
                "content": """# Similarity

In the previous lesson, we learned that an embedding is a vector:

```
"I want to buy an apartment"
        ↓
[0.12, -0.43, 0.81, ...]
```

Now we need to answer an important question: **how do we know whether two vectors represent similar meanings?** That's where similarity comes in.

## 1. What is similarity?

Similarity is simply a number that tells us how related two things are. "I want to buy an apartment" and "I'm looking for a flat" have similar meanings, so we want **similarity = HIGH**. But "I want to buy an apartment" and "I like eating pizza" have very different meanings, so **similarity = LOW**.

## 2. The important mental model

Think of embeddings as points in a huge mathematical space:

```
       ● A
      /
     /
    ● B


                         ● C
```

If A and B are close, they are considered more similar. If C is far away, it's less similar to A. So semantic search is basically: **turn text into vectors, then find vectors that are similar to the query vector.**

## 3. Example with your RAG system

Suppose your knowledge base contains:

- D1 = "Students must complete 160 credit hours to graduate."
- D2 = "The university library closes at 6 PM."
- D3 = "The minimum graduation GPA is 2.0."

User asks: Q = "How many credits are needed for graduation?"

We embed everything, then calculate similarity:

```
Similarity(Q, D1) = 0.94
Similarity(Q, D2) = 0.12
Similarity(Q, D3) = 0.71
```

The search system ranks them: 1. D1 (0.94), 2. D3 (0.71), 3. D2 (0.12). Therefore D1 is the best match.

## 4. Similarity is usually represented by a score

With **cosine similarity**, you'll commonly see values between:

- **-1** → completely opposite direction
- **0** → unrelated / orthogonal
- **+1** → same direction

For many modern text embeddings, you'll frequently encounter positive scores like 0.20, 0.45, 0.72, or 0.91. But don't memorize a universal rule like "0.7 always means relevant" — the meaning of a score depends on the embedding model, your dataset, your language, your type of documents, and your similarity metric. We'll study thresholds later.

## 5. Similarity is not the same as distance

**Similarity**: higher usually means *more similar*. **Distance**: lower usually means *closer*.

```
Similarity:

A ───────── B          A ───────────────────────── C
      0.92                          0.31

Distance:

A ─ B                  A ───────────────── C
  0.10                          0.80
```

A and B are highly similar / close in both framings. So: **similarity ↑ → more related**, **distance ↓ → more related**. This distinction matters when working with vector databases, since different indexes/configurations may use different metrics.

## 6. How is similarity calculated?

Suppose we have two small vectors, `A = [1, 2]` and `B = [2, 4]`. They're pointing in exactly the same direction, so we'd expect them to be highly similar. Another vector, `C = [-2, 1]`, points in a very different direction:

```
        A/B
         ↗
        /
       /
------+----------------
       \\
        \\
         ↖ C
```

Therefore `similarity(A, B)` → high, `similarity(A, C)` → lower. Common ways to calculate this include **cosine similarity**, **Euclidean distance**, and **dot product**. For semantic search, cosine similarity is particularly important — that's our focus for the rest of this lesson.

## 7. Why cosine similarity?

`A = [1, 2]` and `B = [2, 4]` — B is basically A scaled by 2. Their *lengths* are different (A is shorter, B is longer), but their *direction* is identical. **Cosine similarity focuses primarily on the angle/direction between vectors**, not their magnitude:

```
A
 ↗
  \\
   \\  same direction
    ↗ B
```

So `cosine_similarity(A, B) ≈ 1`. This is useful because with text embeddings, we're often more interested in the direction/semantic relationship than simply how large the numbers are.

## 8. Practical Python example

```python
from sklearn.metrics.pairwise import cosine_similarity

A = [[1, 2]]
B = [[2, 4]]

score = cosine_similarity(A, B)
print(score)
# [[1.]]  -- vectors point in the same direction
```

```python
A = [[1, 2]]
C = [[-2, 1]]

score = cosine_similarity(A, C)
print(score)
# [[0.]]  -- directions are perpendicular
```

## 9. With real embeddings

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = [
    "I want to buy an apartment",
    "I'm looking for a flat",
    "How do I cook pasta?"
]

embeddings = model.encode(texts)

score = cosine_similarity([embeddings[0]], [embeddings[1]])
print(score)
```

Conceptually, "I want to buy an apartment" and "I'm looking for a flat" should show high similarity, while comparing embedding[0] against the pasta sentence should give a much lower similarity.

## 10. How this connects to Qdrant/FAISS

When you previously wrote something like `results = qdrant.search(query_vector=query_vector)`, underneath the high-level API the system is essentially doing:

```
Query Vector
      ↓
Compare against stored vectors
      ↓
Calculate similarity/distance
      ↓
Rank results
      ↓
Return nearest vectors
```

So when Qdrant returns Document A → 0.91, Document B → 0.73, Document C → 0.28, that score tells you something about the relationship between the query vector and each stored vector. The exact meaning and direction of the score depend on the metric/API being used, so always check the vector database configuration instead of assuming every "score" means cosine similarity.

## 11. Similarity → Ranking

Given Query = "How many credits do I need to graduate?" with Document 1 → 0.93, Document 2 → 0.81, Document 3 → 0.35, Document 4 → 0.22, we sort them and retrieve the top *k*. For example, `top_k = 2` gives Document 1 and Document 2. This is the foundation of **Top-K Retrieval**, which you'll use heavily in RAG.

## 12. The complete mental model

```
             TEXT
               ↓
        Embedding Model
               ↓
             VECTOR
               ↓
       Similarity Metric
               ↓
       Similarity Score
               ↓
            Ranking
               ↓
        Top-K Results
```

And your RAG system becomes:

```
Documents
    ↓
Embeddings
    ↓
Vector Database
    ↓
               Query
                 ↓
            Query Embedding
                 ↓
          Similarity Search
                 ↓
              Ranking
                 ↓
             Top-K Docs
                 ↓
                LLM
                 ↓
              Answer
```

## 🧠 Key Takeaways

1. Similarity measures how related two vectors are.
2. Similar meanings should generally produce vectors that are more similar.
3. Similarity and distance are not the same thing.
4. Cosine similarity compares the direction/angle between vectors.
5. Vector databases use similarity/distance to rank search results.
6. Semantic search is fundamentally: Query → Embedding → Compare → Rank → Retrieve.

**The most important connection to your previous work:** when you used Qdrant + embeddings for your Arabic RAG system, Qdrant wasn't "understanding" the Arabic text directly. It was searching through mathematical vector representations and ranking them according to a configured similarity/distance measure.
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Rank Documents by Similarity",
                    "description": (
                        "Suppose:\n\n"
                        "Query: \"How much does one credit hour cost?\"\n\n"
                        "Document A: \"The cost of a credit hour is 1330 EGP.\"\n"
                        "Document B: \"The university library opens at 8 AM.\"\n"
                        "Document C: \"Students need 160 credit hours to graduate.\"\n\n"
                        "Without running any code:\n\n"
                        "1. Rank Documents A, B, and C from most to least semantically similar "
                        "to the query, and explain your reasoning.\n\n"
                        "2. Which document do you expect to have the lowest similarity score, and why?\n\n"
                        "3. Document C shares the phrase 'credit hours' with the query but answers a "
                        "different question (how many, not how much). Why might a good embedding "
                        "model still rank it above Document B?"
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["embeddings", "similarity", "semantic-search", "rag"],
                },
            ],
            "quiz": {
                "title": "Similarity — Knowledge Check",
                "questions": [
                    {
                        "question": "What does a similarity score tell us?",
                        "options": [
                            "How many words two pieces of text share exactly",
                            "How related two vectors (and therefore two pieces of meaning) are",
                            "The exact number of dimensions in an embedding",
                            "How long a document is compared to the query",
                        ],
                        "correct": 1,
                        "explanation": "Similarity is a number expressing how closely related two vectors are, which reflects how related their underlying meanings are.",
                    },
                    {
                        "question": "With cosine similarity, what does a score near +1 typically indicate?",
                        "options": [
                            "The two vectors are completely unrelated",
                            "The two vectors point in the same direction (highly similar)",
                            "The two vectors are guaranteed to be identical text",
                            "An error occurred during embedding",
                        ],
                        "correct": 1,
                        "explanation": "A cosine similarity near +1 means the vectors point in nearly the same direction, indicating high similarity.",
                    },
                    {
                        "question": "How do similarity and distance relate to each other?",
                        "options": [
                            "They are exactly the same thing with the same scale",
                            "Higher similarity generally corresponds to lower distance, and vice versa",
                            "Higher similarity always corresponds to higher distance",
                            "Distance is only used for images, never for text",
                        ],
                        "correct": 1,
                        "explanation": "Similarity and distance move in opposite directions: more similar/related items tend to have higher similarity scores and lower distance values.",
                    },
                    {
                        "question": "Why is cosine similarity particularly useful for comparing text embeddings?",
                        "options": [
                            "It ignores the content of the vectors entirely",
                            "It focuses on the direction/angle between vectors rather than their magnitude, which matters more for semantic meaning",
                            "It only works when vectors have exactly 2 dimensions",
                            "It guarantees a similarity score of exactly 1 for all related sentences",
                        ],
                        "correct": 1,
                        "explanation": "Cosine similarity measures the angle between vectors, which captures semantic direction/meaning better than raw magnitude for text embeddings.",
                    },
                    {
                        "question": "If Document 1 scores 0.93, Document 2 scores 0.81, Document 3 scores 0.35, and Document 4 scores 0.22 against a query, what would top_k = 2 retrieval return?",
                        "options": [
                            "Document 3 and Document 4",
                            "Document 1 and Document 2",
                            "All four documents",
                            "Only Document 1",
                        ],
                        "correct": 1,
                        "explanation": "Top-K retrieval with k=2 returns the two highest-scoring (most similar) documents: Document 1 (0.93) and Document 2 (0.81).",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.beginner,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # Topic fields
            "title":            "Cosine Similarity",
            "slug":              "embeddings-cosine-similarity",
            "description":       "A deeper look at cosine similarity: how it compares vector direction rather than magnitude, why normalization matters, and how it connects to Qdrant/FAISS distance metrics.",
            "order":             4,
            "difficulty":        DifficultyLevel.beginner,
            "estimated_hours":   2.0,
            "skill_tags":        ["embeddings", "cosine-similarity", "similarity", "vector-search", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Cosine Similarity",
                "content": """# Cosine Similarity

In the previous lesson, we learned that we need a way to compare vectors. One of the most important methods for text embeddings is **cosine similarity**. Don't worry about the name — the idea is actually simple.

## 1. The core idea

Cosine similarity measures the **angle between two vectors**. Think of vectors as arrows:

```
       B
      ↗
     /
    /
   ↗ A
  /
 ●
```

If they point in almost the same direction → similarity is **HIGH**. If they point in completely different directions → similarity is **LOW**. So the mental model is: *cosine similarity asks "Are these two vectors pointing in a similar direction?"*

## 2. Why "cosine"?

You don't need to memorize the trigonometry yet. The formula is:

```
cosine similarity = (A · B) / (||A|| × ||B||)
```

where `A · B` is the dot product, and `||A||`/`||B||` are the lengths (magnitudes) of A and B. The important thing is what the formula *gives us*, not deriving it.

## 3. The score

Cosine similarity normally ranges from:

```
-1 ───────── 0 ───────── +1
opposite     unrelated    same direction
```

```
+1
│
│   Very similar
│
0  ─────────────
│
│   Very different
│
-1
```

For many modern text-embedding applications, you'll often see positive scores rather than values near -1. But don't interpret "0.8 = always good, 0.6 = always bad" — there is no universal threshold. We'll study thresholds later.

## 4. Simple example

`A = [1, 0]`, `B = [2, 0]`:

```
A ─────→

B ─────────────→
```

They point in exactly the same direction, so **cosine similarity = 1** — even though B is twice as long. This is one of the most useful properties of cosine similarity.

## 5. Direction matters more than magnitude

`A = [1, 2]`, `B = [2, 4]` — B is basically A multiplied by 2. Their lengths are different, but their direction is identical. Therefore `cosine_similarity(A, B) = 1`. This is why cosine similarity is useful for embeddings: we often care about the *pattern/direction* of the representation, not simply how large the vector is.

## 6. Completely different direction

`A = [1, 0]`, `B = [0, 1]`:

```
        B
        ↑
        |
        |
        |
        +────────→ A
```

They are perpendicular, so **cosine similarity = 0** — no directional similarity.

## 7. Opposite direction

`A = [1, 0]`, `B = [-1, 0]`:

```
B ←──────── ● ────────→ A
```

They point in opposite directions, so **cosine similarity = -1**. Again, for normal text-embedding applications, don't expect semantic relationships to neatly map to +1, 0, and -1 — real embedding spaces are much more complicated.

## 8. Let's calculate it ourselves

```python
import numpy as np

A = np.array([1, 2])
B = np.array([2, 4])

similarity = np.dot(A, B) / (
    np.linalg.norm(A) * np.linalg.norm(B)
)

print(similarity)
# 1.0
```

Because they point in the same direction.

## 9. Using scikit-learn

You don't normally need to implement the formula yourself:

```python
from sklearn.metrics.pairwise import cosine_similarity

A = [[1, 2]]
B = [[2, 4]]

score = cosine_similarity(A, B)
print(score)
# [[1.]]
```

## 10. Now let's use actual embeddings

This is where it becomes relevant to your previous work:

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = [
    "I want to buy an apartment",
    "I'm looking for a flat",
    "How do I cook pasta?"
]

embeddings = model.encode(texts)

score_1 = cosine_similarity([embeddings[0]], [embeddings[1]])
score_2 = cosine_similarity([embeddings[0]], [embeddings[2]])

print(score_1)
print(score_2)
```

Conceptually: Apartment ↔ Flat → high similarity; Apartment ↔ Pasta → much lower similarity. The exact scores will depend on the model.

## 11. Why normalize?

You'll often encounter **normalized embeddings**. Normalization means converting a vector so that its length becomes 1. For example, `A = [3, 4]` normalizes to `[0.6, 0.8]`, because `sqrt(3² + 4²) = 5` and `[3/5, 4/5] = [0.6, 0.8]`. Now the vector has unit length.

## 12. Why does normalization matter?

When vectors are normalized (`||A|| = 1`, `||B|| = 1`), cosine similarity becomes closely related to the dot product. Specifically, `cosine(A, B) = A · B` for unit-normalized vectors. This matters because many vector-search systems can efficiently perform dot-product-based search.

## 13. Connection to FAISS

This explains something you may have encountered when working with FAISS. Depending on configuration, FAISS can use metrics such as **Inner Product** or **L2 distance**. If your embeddings are normalized, inner product can correspond directly to cosine similarity. So the pipeline can be:

```
Text
 ↓
Embedding Model
 ↓
Normalize vector
 ↓
FAISS
 ↓
Inner Product
 ↓
Similarity ranking
```

This is one reason you may see code like:

```python
embeddings = model.encode(
    texts,
    normalize_embeddings=True
)
```

The normalization isn't just cosmetic — it can make the vector representation compatible with the similarity calculation/search strategy you want.

## 14. Qdrant connection

With Qdrant, you may configure a collection using a distance metric such as **Cosine**:

```
Query
 ↓
Embedding
 ↓
Qdrant
 ↓
Cosine-based comparison
 ↓
Nearest vectors
```

So when you previously configured vector search, you were choosing *how* the vector space should be compared. That's a deeper understanding of what was happening behind the API.

## 15. A real semantic-search example

Your university RAG database contains:

- D1: "Students must complete 160 credit hours to graduate."
- D2: "The minimum GPA for graduation is 2.0."
- D3: "The tuition fee per credit hour is 1330 EGP."

User asks: "How much does a credit hour cost?" Cosine similarity might conceptually produce `Q↔D1 = 0.32`, `Q↔D2 = 0.27`, `Q↔D3 = 0.89` — so D3 gets ranked first. That's the foundation of semantic retrieval.

## 16. One important warning

**High cosine similarity does not automatically mean "correct answer."** This is extremely important for RAG. Suppose the query is "What is the tuition fee?" and retrieval returns "Students must complete 160 credit hours." It might have *some* semantic relationship to university requirements, but that doesn't mean it's the correct information.

So: **Similarity ≠ Correctness.** Similarity helps us retrieve candidates — it doesn't prove that the retrieved document contains the answer. This is one reason you later learned about reranking, retrieval evaluation, context relevance, and faithfulness.

## 🧠 Key Takeaways

1. Cosine similarity compares vector *direction*: same direction → high similarity, different direction → low similarity.
2. Formula: `cos(A,B) = (A · B) / (||A|| ||B||)` — you don't need to memorize it yet.
3. Range: -1 (opposite), 0 (perpendicular), +1 (same direction).
4. Normalization can make cosine similarity equivalent to dot product.
5. In your RAG systems: Query → Query Embedding → Cosine/distance comparison → Rank documents → Top-K retrieval.
6. Most importantly: **similarity helps you find relevant candidates; it does not guarantee correctness.**
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Ranking by Cosine Similarity",
                    "description": (
                        "Suppose we have:\n\n"
                        "A = [1, 0]\nB = [2, 0]\nC = [0, 1]\nD = [-1, 0]\n\n"
                        "Without calculating anything precisely, rank B, C, and D by cosine "
                        "similarity to A — highest, middle, and lowest — and explain your "
                        "reasoning based on direction rather than magnitude."
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["embeddings", "cosine-similarity", "similarity"],
                },
            ],
            "quiz": {
                "title": "Cosine Similarity — Knowledge Check",
                "questions": [
                    {
                        "question": "What does cosine similarity primarily measure between two vectors?",
                        "options": [
                            "The difference in their magnitudes (lengths)",
                            "The angle/direction between them",
                            "The number of dimensions they share",
                            "How many words the original texts have in common",
                        ],
                        "correct": 1,
                        "explanation": "Cosine similarity focuses on the angle between vectors, not their length — vectors pointing in the same direction get a high score even if their magnitudes differ.",
                    },
                    {
                        "question": "If A = [1, 2] and B = [2, 4], what is cosine_similarity(A, B), and why?",
                        "options": [
                            "0, because B is twice as long as A",
                            "-1, because they point in opposite directions",
                            "1, because B is just A scaled by 2 and they point in the same direction",
                            "It cannot be determined without more information",
                        ],
                        "correct": 2,
                        "explanation": "B is a scalar multiple of A, so they point in exactly the same direction, giving a cosine similarity of 1 regardless of the difference in magnitude.",
                    },
                    {
                        "question": "What does normalizing an embedding vector mean?",
                        "options": [
                            "Rounding all values to the nearest integer",
                            "Scaling the vector so its length (magnitude) becomes 1",
                            "Removing dimensions that are close to zero",
                            "Converting the vector back into text",
                        ],
                        "correct": 1,
                        "explanation": "Normalization rescales a vector so its length equals 1, which is why cosine similarity becomes equivalent to the dot product for normalized vectors.",
                    },
                    {
                        "question": "Why might a vector database like FAISS or Qdrant use inner product (dot product) search on normalized embeddings?",
                        "options": [
                            "Because inner product search has nothing to do with cosine similarity",
                            "Because on normalized vectors, inner product search is equivalent to cosine similarity and can be computed efficiently",
                            "Because dot product is always more accurate than cosine similarity regardless of normalization",
                            "Because normalization is required before any vectors can be stored at all",
                        ],
                        "correct": 1,
                        "explanation": "For unit-normalized vectors, the dot product equals the cosine similarity, letting vector search systems use efficient inner-product search to achieve cosine-similarity ranking.",
                    },
                    {
                        "question": "Why is it important to remember that 'similarity ≠ correctness' in a RAG system?",
                        "options": [
                            "Because similarity scores are always wrong and should be ignored",
                            "Because a retrieved document can be semantically related to the query without actually containing the correct answer",
                            "Because cosine similarity can never be computed for real documents",
                            "Because RAG systems don't use similarity at all",
                        ],
                        "correct": 1,
                        "explanation": "A document can be topically or semantically related to a query (giving it a high similarity score) without actually answering it correctly — similarity finds candidates, it doesn't verify correctness.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": None,
                "description": None,
                "difficulty": DifficultyLevel.beginner,
                "tech_stack": [],
                "objectives": [],
                "rubric": {},
                "starter_repo_url": None,
                "estimated_hours": None,
            },
        },
        {
            # Topic fields
            "title":            "Embedding Models",
            "slug":              "embeddings-embedding-models",
            "description":       "What an embedding model actually is, why different models produce incompatible vector spaces, and how to reason about choosing an embedding model — including multilingual models for Arabic RAG.",
            "order":             5,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   2.0,
            "skill_tags":        ["embeddings", "embedding-models", "multilingual", "rag", "model-selection"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Embedding Models",
                "content": """# Embedding Models

Now we move from *what embeddings are* to *what creates them*. You already used models like `multilingual-e5-small`, `multilingual-e5-large`, `paraphrase-multilingual-MiniLM`, and Sentence Transformers. This lesson is about understanding what an embedding model actually does and how to think about choosing one.

## 1. What is an embedding model?

An embedding model is a model specifically trained to convert input into vectors:

```
Text
 ↓
Embedding Model
 ↓
Vector
```

For example:

```python
text = "I want to buy an apartment"
vector = model.encode(text)
# [0.12, -0.43, 0.71, ..., 0.08]
```

**Embedding model = model that converts information into a useful vector representation.**

## 2. An embedding model is different from an LLM

An LLM does: Question → LLM → Generated answer. An embedding model does: Text → Embedding Model → Vector.

```
LLM
"What is RAG?"
       ↓
"RAG stands for Retrieval-Augmented Generation..."

Embedding model
"What is RAG?"
       ↓
[0.12, -0.44, 0.72, ...]
```

The embedding model isn't trying to write an answer. Its job is to create a representation useful for semantic search, retrieval, clustering, recommendations, duplicate detection, and classification.

## 3. What does "trained for embeddings" mean?

An embedding model isn't simply a normal language model where we grab a random internal layer and call it an embedding. It is *trained* so its vector representations have useful relationships. During training, it should learn that "I want to buy a car" and "I'm looking for a vehicle" have related representations, while "I want to buy a car" and "The weather is cold today" are less related.

```
Similar meaning   → Similar vectors
Different meaning → Different vectors
```

That's the property we care about.

## 4. Think of an embedding model as a translator

An embedding model translates *human language* into *mathematical language*:

```
"I need an apartment in Cairo"          "I'm searching for a flat in Cairo"
             ↓                                          ↓
       Embedding Model                            Embedding Model
             ↓                                          ↓
[0.18, -0.42, 0.73, ...]                    [0.20, -0.40, 0.71, ...]
```

Now mathematical operations can tell us that these vectors are similar.

## 5. Not all embedding models are the same

You might think "an embedding is an embedding, why do I care which model I use?" Because different embedding models can produce very different vector spaces. Model A's vector for "apartment" and Model B's vector for "apartment" won't necessarily share dimensions, values, or geometry — e.g., Model A → 384 dimensions, Model B → 768, Model C → 1024. **You generally cannot mix their vectors in the same vector index and expect meaningful comparisons.**

## 6. Embedding dimensions

Every embedding model has an output dimension:

```python
embedding = model.encode("Hello")
print(len(embedding))
# 384
```

This matters when creating a vector database — if your model produces 384 dimensions, your Qdrant collection needs to be configured accordingly:

```
Embedding Model
     ↓
384 dimensions
     ↓
Qdrant collection
     ↓
vector size = 384
```

If you switch to a model producing 768 dimensions, you generally need a different collection/index configuration.

## 7. Model choice affects retrieval quality

Given the same query, "How many credits are required for graduation?", Model A might retrieve "Students must complete 160 credit hours to graduate." very effectively, while Model B might retrieve "The minimum GPA for graduation is 2.0." instead. Better embedding model → potentially better retrieval → potentially better RAG. But **a newer or larger model is not automatically better for your specific dataset** — you need evaluation.

## 8. General-purpose vs specialized embeddings

Embedding models can be designed for different purposes: **general text embeddings** (semantic search, similarity, clustering) vs. **retrieval-focused embeddings** (designed specifically for query → document retrieval). This distinction becomes important when choosing models for RAG.

## 9. Query and document representations

Some modern embedding models are designed around two roles: **query** and **document**. With models such as E5, you'll often see prefixes like `query: how many credits are required?` and `passage: students must complete 160 credit hours to graduate.` The idea is to tell the model "this text is a search query" versus "this text is something that will be searched." This can improve retrieval because the model was trained with this setup in mind — particularly relevant to your previous use of `intfloat/multilingual-e5-small` and `intfloat/multilingual-e5-large`.

## 10. Why multilingual embedding models?

Connecting this to your Arabic RAG experience: if your document is "يشترط للتخرج إتمام 160 ساعة معتمدة." and the user asks "محتاج كام ساعة عشان أتخرج؟", an English-only embedding model isn't the best choice. A **multilingual embedding model** is designed to represent multiple languages in a compatible semantic space:

```
Arabic  → Multilingual Embedding Model → Vector
English → Multilingual Embedding Model → Vector
```

This can even enable cross-language semantic relationships — "How many credits are required for graduation?" and "كام ساعة معتمدة مطلوبة للتخرج؟" can potentially be represented similarly.

## 11. Sentence Transformers

A typical workflow:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

embedding = model.encode("I want to buy an apartment")
print(embedding.shape)
```

**Sentence Transformers** is an ecosystem/library that makes it easy to use many embedding and similarity models — it isn't itself one single embedding model. That's an important distinction: Sentence Transformers = framework/library; an embedding model = the actual model producing vectors.

## 12. Hugging Face connection

You might find models such as `intfloat/multilingual-e5-large` on Hugging Face. The model is the actual trained neural network; libraries such as Sentence Transformers make using compatible models convenient:

```
Hugging Face
    ↓
Model repository
    ↓
Embedding model
    ↓
Sentence Transformers
    ↓
encode()
    ↓
Vector
```

The exact loading path depends on the model.

## 13. Embedding model ≠ vector database

Reinforcing this because it's a common source of confusion: an **embedding model** creates Text → Vector. A **vector database** stores/searches Vector → Similar vectors. You need both for a typical semantic retrieval system.

## 14. Choosing an embedding model

Don't choose a model just because "it has a lot of dimensions" — more dimensions doesn't automatically mean better retrieval. Consider:

1. **Language support** — English? Arabic? Multiple languages?
2. **Retrieval quality** — how well does it retrieve your actual documents?
3. **Vector dimension** — larger vectors mean more storage, more memory, potentially more computation.
4. **Speed** — embedding millions of documents matters at scale.
5. **Hardware** — can your infrastructure run the model efficiently?
6. **Domain** — a model that works well for general text might behave differently on legal, medical, academic, real estate, or code documents.

## 15. A real engineering decision

Testing `multilingual-e5-small` (Model A) vs. `multilingual-e5-large` (Model B) for your Arabic academic RAG system — you shouldn't automatically say "large > small." Instead:

```
Test Dataset → Model A → Retrieval Results → Evaluate
Test Dataset → Model B → Retrieval Results → Evaluate
```

Then compare Recall@K, Precision@K, semantic relevance, latency, memory, and cost. This is AI *engineering*, rather than simply calling a model.

## 16. One more important concept: embedding consistency

Suppose you indexed your documents using Model A, then later search using Model B:

```
Documents → Model A → Vectors A → Qdrant

Query → Model B → Vector B → Compare with Vectors A
```

These vectors come from *different embedding spaces* — the similarity scores generally won't be meaningful. **Use the same compatible embedding model for indexing documents and embedding queries.** If you change the embedding model, you generally need to re-embed your documents.

## 🧠 The complete mental model

```
             EMBEDDING MODEL
                    │
       ┌────────────┴────────────┐
       ↓                         ↓
   Documents                  Queries
       ↓                         ↓
    Vectors                   Vectors
       │                         │
       └──────────┬──────────────┘
                  ↓
            Similarity Search
                  ↓
             Top-K Results
```

And model selection happens *before* all of this: Language → Use case → Embedding model → Vector dimension → Vector database → Similarity search → Evaluation.

## 🧠 Key Takeaways

1. An embedding model converts input into vectors.
2. Different embedding models produce different vector spaces.
3. The model's embedding dimension matters for your vector database.
4. Bigger dimensions don't automatically mean better quality.
5. For RAG, retrieval-focused embedding models can be especially useful.
6. For Arabic/multilingual applications, use an embedding model designed to support the languages you need.
7. Documents and queries should be embedded consistently, usually with the same model.
8. Model choice should be based on evaluation, not popularity or model size alone.

**The key engineering principle:** the best embedding model isn't necessarily the biggest one — it is the one that gives good retrieval quality for your data, language, hardware, latency, and cost requirements.
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Choosing an Embedding Model for Arabic RAG",
                    "description": (
                        "You're building your Arabic RAG system. You have two choices:\n\n"
                        "Model A: English-only, 768 dimensions\n"
                        "Model B: Multilingual, 384 dimensions\n\n"
                        "Your documents are Arabic and your users ask questions in Arabic.\n\n"
                        "1. Which would you initially choose, and why?\n\n"
                        "2. Does the fact that Model A has more dimensions than Model B change "
                        "your answer? Why or why not?\n\n"
                        "3. If you later switch from Model B to a different multilingual model, "
                        "what do you need to do to your existing Qdrant collection, and why?"
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["embeddings", "embedding-models", "multilingual", "rag"],
                },
            ],
            "quiz": {
                "title": "Embedding Models — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the core difference between an embedding model and an LLM?",
                        "options": [
                            "An embedding model generates natural-language answers, while an LLM only produces vectors",
                            "An embedding model converts text into a vector representation; an LLM generates or understands language to produce answers",
                            "There is no meaningful difference between the two",
                            "An LLM is always smaller than an embedding model",
                        ],
                        "correct": 1,
                        "explanation": "Embedding models produce vector representations for comparison/search, while LLMs generate or understand language to produce text answers.",
                    },
                    {
                        "question": "Why can't you generally mix vectors from two different embedding models in the same vector index?",
                        "options": [
                            "You can always mix them freely with no issues",
                            "Different embedding models produce different, generally incompatible vector spaces, so comparisons between them aren't meaningful",
                            "Vector databases only support one dimension size, period, regardless of model",
                            "Embedding models never differ from one another",
                        ],
                        "correct": 1,
                        "explanation": "Different models learn different vector spaces (different dimensions, geometry, and relationships), so mixing their outputs makes similarity comparisons meaningless.",
                    },
                    {
                        "question": "Why might a multilingual embedding model be a better choice than an English-only model for an Arabic RAG system?",
                        "options": [
                            "Multilingual models are always faster than English-only models",
                            "A multilingual model is designed to represent multiple languages in a compatible semantic space, enabling meaningful similarity for Arabic text",
                            "English-only models cannot technically accept Arabic input at all",
                            "Multilingual models always have fewer dimensions, which is inherently better",
                        ],
                        "correct": 1,
                        "explanation": "Multilingual embedding models are trained to place semantically similar text from different languages close together, which is essential for retrieval quality on Arabic documents and queries.",
                    },
                    {
                        "question": "What must you do if you switch the embedding model used for your document index?",
                        "options": [
                            "Nothing — the old vectors remain fully compatible with the new model's queries",
                            "Generally re-embed (re-index) your documents with the new model, since old and new vectors live in different embedding spaces",
                            "Only re-embed the queries, never the documents",
                            "Simply increase the vector database's storage size",
                        ],
                        "correct": 1,
                        "explanation": "Since different models produce different embedding spaces, switching models generally requires re-embedding your documents so that queries and documents remain comparable.",
                    },
                    {
                        "question": "What is the key engineering principle for choosing an embedding model?",
                        "options": [
                            "Always choose the model with the most dimensions",
                            "Always choose the newest model released, regardless of your use case",
                            "Choose the model that gives good retrieval quality for your specific data, language, hardware, latency, and cost — based on evaluation",
                            "Model choice doesn't matter as long as you use Sentence Transformers",
                        ],
                        "correct": 2,
                        "explanation": "The best embedding model is the one that performs well on your actual data and constraints, determined through evaluation rather than assumptions about size or popularity.",
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
            # Topic fields
            "title":            "Multilingual Embeddings",
            "slug":              "embeddings-multilingual-embeddings",
            "description":       "How multilingual embedding models place semantically related text from different languages in a compatible vector space, enabling cross-lingual retrieval — and why Arabic RAG needs careful evaluation rather than assumptions.",
            "order":             6,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   2.0,
            "skill_tags":        ["embeddings", "multilingual", "cross-lingual-retrieval", "arabic-nlp", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Multilingual Embeddings",
                "content": """# Multilingual Embeddings

You already worked with multilingual models such as multilingual-e5, so now let's understand what makes an embedding model *multilingual* and why this matters for your Arabic RAG systems.

## 1. What is a multilingual embedding?

A multilingual embedding model can represent text from multiple languages in a **compatible semantic vector space**. For example:

- English: "How many credits are required for graduation?"
- Arabic: "كم عدد الساعات المطلوبة للتخرج؟"

Different languages, essentially the same meaning. A multilingual embedding model tries to produce vectors that are close to each other:

```
English → Multilingual Embedding Model → Vector A
Arabic  → Multilingual Embedding Model → Vector B

Similarity(A, B) → HIGH
```

This is called **cross-lingual semantic representation**.

## 2. Why is this useful?

Imagine your knowledge base contains the Arabic document "يشترط للتخرج إتمام 160 ساعة معتمدة." but a user asks in English: "How many credit hours do I need to graduate?" If your embedding model handles both languages well, the system can recognize the semantic relationship between them. This can enable **cross-language retrieval** — useful when documents are Arabic but users sometimes ask in English, documents contain multiple languages, users switch languages, or you need multilingual search generally.

## 3. How does the model learn this?

The model is trained on multilingual data so that semantically related texts across languages occupy compatible regions of the vector space:

```
English sentence ──┐
                   │
Arabic sentence ───┼──→ Shared semantic space
                   │
French sentence ───┘
```

Imagine the vector space contains a concept like "buy apartment":

```
             "buy apartment"
                   ●
                 / | \\
                /  |  \\
               /   |   \\
              ●    ●    ●
           English Arabic French
```

Different languages can point toward the same semantic concept.

## 4. This is different from translation

A multilingual embedding model does not necessarily translate the sentence. "أنا أبحث عن شقة" doesn't need to become "I'm looking for an apartment." Instead, each is turned into its own vector, and those vectors can be compared directly. **Multilingual embeddings allow semantic comparison across languages without requiring explicit translation first.**

## 5. Your Arabic RAG example

Document: "يشترط للتخرج إتمام 160 ساعة معتمدة." User (Arabic): "أنا محتاج كام ساعة عشان أتخرج؟" A multilingual embedding model represents both, and `cosine_similarity(Q, D)` can be high. Now suppose the user asks in English instead: "How many credit hours do I need to graduate?" A good multilingual model may also place that English query vector close to the *same* Arabic document vector:

```
                Arabic Document
                      ●
                     / \\
                    /   \\
                   /     \\
              Arabic Q   English Q
                  ●          ●
```

That's the powerful part.

## 6. Multilingual does NOT mean equally good at every language

This is very important. If a model claims to support "100+ languages," that doesn't mean English quality = Arabic quality = Chinese quality = .... Language performance can vary — a model might be excellent at English, very good at Arabic, good at French, and moderate at a low-resource language. **For a real project, test the language that actually matters to you.**

## 7. Arabic has additional challenges

Arabic semantic search can be harder because of:

- **Different forms of the same word** — e.g., التخرج / للتخرج / بالتخرج
- **Diacritics** — عِلْم vs علم
- **Morphology** — Arabic words carry prefixes and suffixes, e.g. والطلاب / فالطلاب / للطلاب
- **Dialects** — a user might write "محتاج كام ساعة عشان أتخرج؟" while the document uses formal Arabic: "يشترط للتخرج إتمام 160 ساعة معتمدة."

A good multilingual embedding model should help bridge some of these differences.

## 8. Multilingual embeddings vs keyword search

Comparing "يشترط للتخرج إتمام 160 ساعة معتمدة." against the query "كام ساعة لازم أخلصها عشان أتخرج؟" — keyword matching may struggle because the wording differs substantially. Semantic embeddings focus more on the underlying concepts (graduation + required hours) rather than exact matching. This is one reason embeddings are valuable for Arabic search.

## 9. E5 and the query/document distinction

This connects directly to `intfloat/multilingual-e5-large`. E5 models are designed for embedding/retrieval tasks, and you may encounter usage such as `query: كام ساعة مطلوبة للتخرج؟` and `passage: يشترط للتخرج إتمام 160 ساعة معتمدة.` The `query:` / `passage:` prefixes aren't random — they tell the model what role the text is playing:

```
              E5
        ┌──────┴──────┐
        ↓             ↓
      query         passage
        ↓             ↓
     vector Q       vector D
        └──────┬──────┘
               ↓
          Retrieval
```

When using a particular embedding model, always follow that model's documented input format — don't assume every embedding model requires these prefixes.

## 10. One of the biggest mistakes in multilingual RAG

Imagine you have Arabic documents but choose an embedding model that works primarily for English. Then: Arabic document → poor representation → poor retrieval, even if Qdrant, chunking, the LLM, and the prompt are all otherwise fine. This connects to a principle from your Prompt Engineering level: **don't try to fix a retrieval problem with a better prompt.** If your embedding model doesn't represent your language/domain well, changing the prompt won't solve the underlying retrieval problem.

## 11. Multilingual embeddings don't solve everything

An Arabic query going through a multilingual embedding into Qdrant is powerful, but retrieval quality can still be affected by bad chunking, noisy documents, poor preprocessing, an inappropriate embedding model, the wrong similarity metric, bad metadata filtering, insufficient top-K, or domain-specific terminology. The embedding model is *one component* of the retrieval system.

## 12. Cross-language search

A more interesting example: your database contains Arabic documents, but the user submits an English query.

```
English Query
      ↓
Multilingual Embedding
      ↓
Query Vector
      ↓
Qdrant
      ↓
Arabic Document Vectors
      ↓
Similarity Search
      ↓
Arabic Documents
```

The user could then receive an answer generated in English or Arabic, depending on your application design. This is called **cross-lingual retrieval**.

## 13. Practical Python example

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-small")

texts = [
    "query: How many credit hours are required for graduation?",
    "passage: يشترط للتخرج إتمام 160 ساعة معتمدة."
]

embeddings = model.encode(texts)
print(embeddings.shape)
# (2, embedding_dimension)
```

```python
from sklearn.metrics.pairwise import cosine_similarity

score = cosine_similarity([embeddings[0]], [embeddings[1]])
print(score)
```

The exact score isn't something to memorize. The important idea: an English query and an Arabic document, both passed through a multilingual embedding model, can be compared for semantic similarity.

## 14. A subtle but important point

Multilingual embeddings don't necessarily mean every language shares exactly the same semantic space perfectly — think of it as an **imperfect alignment**:

```
English ────────┐
                │
Arabic ─────────┼──→ approximately aligned semantic space
                │
French ─────────┘
```

Some concepts and languages may align better than others. **Always evaluate multilingual retrieval on your actual language and data.** For your Arabic projects, that means testing with real Arabic queries rather than assuming the model's language list guarantees excellent Arabic retrieval.

## 15. When should you use multilingual embeddings?

They're especially useful when your application has Arabic + English, multiple languages, cross-language search needs, multilingual documents, or multilingual users. If your application is strictly English-only, a strong English-focused embedding model may be preferable. Again: **choose based on your actual use case and evaluation.**

## 🧠 Key Takeaways

1. Multilingual embeddings represent multiple languages in a compatible semantic space.
2. They can enable cross-language retrieval (e.g., English query → Arabic documents).
3. They don't translate text — they create vectors that can be compared semantically.
4. Multilingual ≠ equally good at every language. Always test your target language.
5. Arabic introduces additional challenges: morphology, spelling variations, dialects, and formal-vs-colloquial wording.
6. Model-specific instructions matter — for models such as E5, query/passage prefixes can be important. Always follow the model's intended usage.
7. For your Arabic RAG: Arabic Query → Multilingual Embedding → Query Vector → Qdrant/FAISS → Arabic Document Vectors → Similarity Search.
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Cross-Lingual Similarity Prediction",
                    "description": (
                        "Suppose you have:\n\n"
                        "Document: \"يشترط للتخرج إتمام 160 ساعة معتمدة.\"\n\n"
                        "Query 1: \"كام ساعة محتاج عشان أتخرج؟\"\n"
                        "Query 2: \"How many credit hours do I need to graduate?\"\n"
                        "Query 3: \"كيف يمكنني حجز موعد في المكتبة؟\"\n\n"
                        "Assuming you use a good multilingual embedding model:\n\n"
                        "1. Rank the three queries by expected semantic similarity to the document, "
                        "from most to least similar.\n\n"
                        "2. Explain why Query 3 should score low despite being in the same language "
                        "as the document.\n\n"
                        "3. Explain why Query 2 can still score reasonably high despite being in a "
                        "different language than the document."
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["embeddings", "multilingual", "cross-lingual-retrieval", "arabic-nlp"],
                },
            ],
            "quiz": {
                "title": "Multilingual Embeddings — Knowledge Check",
                "questions": [
                    {
                        "question": "What does it mean for an embedding model to be 'multilingual'?",
                        "options": [
                            "It automatically translates text between languages before embedding it",
                            "It can represent text from multiple languages in a compatible semantic vector space, so related meanings across languages end up close together",
                            "It only works with one language at a time and must be reloaded to switch",
                            "It converts all input languages into English internally before encoding",
                        ],
                        "correct": 1,
                        "explanation": "A multilingual embedding model places semantically similar text from different languages near each other in vector space, without performing explicit translation.",
                    },
                    {
                        "question": "Why is 'this model supports 100+ languages' not enough information to guarantee good Arabic retrieval?",
                        "options": [
                            "Because supporting many languages always means every language performs equally well",
                            "Because language performance can vary significantly across languages, so the target language should be tested directly",
                            "Because multilingual models cannot process Arabic script at all",
                            "Because the number of supported languages has no relationship to model quality",
                        ],
                        "correct": 1,
                        "explanation": "Multilingual support doesn't guarantee uniform quality — some languages are represented much better than others, so you need to evaluate the specific language you care about.",
                    },
                    {
                        "question": "What is cross-lingual retrieval?",
                        "options": [
                            "Retrieving documents only when the query and document are in the exact same language",
                            "Using a query in one language to retrieve relevant documents written in a different language",
                            "Translating a document into every supported language before storing it",
                            "A technique that only works with keyword search, not embeddings",
                        ],
                        "correct": 1,
                        "explanation": "Cross-lingual retrieval means a query in one language (e.g. English) can retrieve semantically relevant documents in another language (e.g. Arabic), enabled by a shared multilingual vector space.",
                    },
                    {
                        "question": "For a model like E5 that uses 'query:' and 'passage:' prefixes, what is the purpose of these prefixes?",
                        "options": [
                            "They are optional decorations with no effect on the model",
                            "They tell the model what role the text is playing (a search query vs. a piece of content to be searched), matching how the model was trained",
                            "They translate the text into a different language",
                            "They are required by every embedding model regardless of architecture",
                        ],
                        "correct": 1,
                        "explanation": "E5-style prefixes signal to the model whether the input is a query or a passage, aligning with how the model was trained for retrieval — but this convention is model-specific, not universal.",
                    },
                    {
                        "question": "Why can't poor retrieval caused by a mismatched embedding model be fixed simply by improving the prompt?",
                        "options": [
                            "Prompts have no effect on RAG systems at all",
                            "The prompt only shapes how the LLM uses whatever context it receives; if retrieval brought back the wrong or poorly-represented chunks, the LLM never sees the right information to begin with",
                            "Because embedding models and prompts are actually the same component",
                            "Because retrieval always works perfectly regardless of embedding model choice",
                        ],
                        "correct": 1,
                        "explanation": "If the embedding model doesn't represent the language/domain well, retrieval surfaces the wrong chunks, and no amount of prompt engineering can compensate for missing or irrelevant context.",
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
            # Topic fields
            "title":            "Document Embeddings",
            "slug":              "embeddings-document-embeddings",
            "description":       "How documents (or chunks of documents) are turned into vectors during indexing, what gets stored alongside a vector in a vector database, and how indexing time differs from query time.",
            "order":             7,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   2.0,
            "skill_tags":        ["embeddings", "document-embeddings", "indexing", "vector-database", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Document Embeddings",
                "content": """# Document Embeddings

Now we're going to focus on one specific part of semantic search: **how do we turn documents into embeddings so they can be searched later?** This is directly connected to the RAG systems you've already built.

## 1. What is a document embedding?

A document embedding is simply the vector representation of a document or a piece of a document:

```
Document
   ↓
Embedding Model
   ↓
Vector
```

For example, "Students must complete 160 credit hours to graduate." becomes `[0.13, -0.42, 0.77, ..., 0.21]`. That vector is the document embedding.

## 2. Usually, we don't embed an entire large document

This is very important for RAG. Imagine you have a 200-page PDF — you normally don't do `200-page PDF → One embedding`, because one vector would represent too much information. Instead:

```
Large Document
      ↓
Split into chunks
      ↓
Chunk 1, Chunk 2, Chunk 3, ..., Chunk 500
      ↓
Embedding each chunk
```

So Chunk 1 → Vector 1, Chunk 2 → Vector 2, and so on. This is exactly why **chunking** is so important in RAG.

## 3. Example

Suppose your document contains three sections: credit-hour requirements, minimum GPA, and cost per credit hour. Instead of creating one vector for the entire document, we create one embedding per chunk. Now a query about tuition ("How much is one credit hour?") can find exactly the chunk about cost — much more useful than a single blended vector for the whole document.

## 4. Why not just store the text?

Because vector search needs vectors. Your database might contain something conceptually like:

```
┌────────────────────────────────────┐
│ ID: 101                            │
│                                    │
│ Vector: [0.12, -0.42, ...]         │
│                                    │
│ Text: "Students must complete..."  │
│                                    │
│ Metadata:                          │
│   course: "Graduation Rules"       │
│   year: 2025/2026                  │
└────────────────────────────────────┘
```

The **text** is what you'll eventually give to the LLM. The **vector** is what you use for semantic retrieval.

## 5. Vector + payload

With Qdrant, you can think of a stored point as `Point → Vector + Payload`. The vector is used for search; the payload can contain the text, source, page, section, course, document name, language, and so on:

```python
payload = {
    "text": "Students must complete 160 credit hours to graduate.",
    "source": "academic_regulations.pdf",
    "page": 42,
    "section": "Graduation Requirements"
}
```

When Qdrant finds the vector, you retrieve the original text and metadata alongside it.

## 6. The complete document-ingestion pipeline

```
Documents
    ↓
Load
    ↓
Parse
    ↓
Clean
    ↓
Chunk
    ↓
Embed
    ↓
Store
```

For example: PDF → text → 1000 chunks → 1000 embeddings → Qdrant. This process is often called **indexing** or **ingestion**.

## 7. Indexing vs querying

This distinction is extremely important.

**Indexing time** — you prepare your knowledge base once, and it can be reused: Documents → Chunks → Document embeddings → Vector database.

**Query time** — a user asks something: User Query → Query embedding → Vector database search → Relevant document chunks.

```
INDEXING                    QUERYING

Documents                   User Query
    ↓                           ↓
Chunks                    Query Embedding
    ↓                           ↓
Embeddings                  Search
    ↓                           ↓
Vector DB                  Results
```

This distinction becomes very important when we study query embeddings in the next lesson.

## 8. Practical Python example

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-small")

documents = [
    "Students must complete 160 credit hours to graduate.",
    "The minimum GPA required for graduation is 2.0.",
    "The cost of one credit hour is 1330 EGP."
]

embeddings = model.encode(documents)
print(embeddings.shape)
# (3, 384)
```

Meaning: 3 documents × 384 numbers per document.

## 9. What actually gets stored?

If `embeddings.shape` returns `(3, 384)`, you conceptually store each document's vector alongside its text and metadata. The vector database doesn't need to regenerate the embedding every time someone searches — you already created it during indexing.

## 10. Why embedding documents can be expensive

Ten documents is easy. A production system might have 1,000,000 chunks, requiring 1,000,000 embedding operations. This introduces engineering considerations: batching, GPU vs CPU, embedding model size, processing speed, memory, API cost if using a hosted model, caching, and incremental indexing. For example, processing 1,000,000 chunks in batches of 1,000 rather than all at once. You generally don't want to load and process everything inefficiently in one giant operation.

## 11. What happens when a document changes?

Suppose you originally indexed "Students need 160 credit hours." Then the university updates it to "Students need 162 credit hours." The old embedding represents the old text, so you need to update/re-embed the affected chunk: remove/update the old vector, then store a new embedding for the new text. This is part of maintaining a production knowledge base.

## 12. A very important rule: same embedding space

If you indexed your documents using `multilingual-e5-large`, you shouldn't suddenly embed a new document using some other model and put it into the same vector index expecting normal similarity comparisons. Model A produces Vector Space A; Model B produces Vector Space B — these are different spaces. For a given vector collection/index, you generally want all vectors produced consistently by the same compatible embedding setup.

## 13. Document embedding doesn't mean "understanding the whole document"

This is subtle. The vector for "Students must complete 160 credit hours to graduate." is not a database containing every fact in an easily recoverable form — it's a compressed numerical representation useful for similarity/retrieval. The vector helps answer "which other pieces of text are semantically related to this one?" It isn't equivalent to storing the original text. That's why we keep both: **vector → retrieval**, **text → context for LLM**.

## 14. Connecting this to your previous Arabic RAG

You previously worked with a pipeline roughly like: Arabic Document → Arabic normalization → Semantic chunking → Multilingual Embedding → Qdrant/FAISS/Chroma. Now you can see exactly what the embedding stage is doing:

```
Chunk:
"يشترط للتخرج إتمام 160 ساعة معتمدة."
                ↓
       multilingual embedding
                ↓
         [0.18, -0.31, ...]
                ↓
             Qdrant
```

Qdrant stores something conceptually like Vector + Arabic text + metadata. Later, the query embedding will be compared against these document vectors.

## 15. The bigger RAG picture

At indexing time:

```
                 INDEXING

Documents
    ↓
Parse
    ↓
Clean
    ↓
Chunk
    ↓
Document Embeddings
    ↓
Vector Database
```

At query time:

```
                  QUERY

User Question
      ↓
Query Embedding
      ↓
Similarity Search
      ↓
Relevant Chunks
      ↓
LLM
      ↓
Answer
```

Notice something important: **document embeddings are created before the user asks a question.** That is why indexing can be done ahead of time.

## 🧠 Key Takeaways

1. A document embedding is a vector representation of a document or chunk.
2. In RAG, we usually embed chunks, not entire large documents.
3. Vector databases store vector + text + metadata together.
4. Document embeddings are usually created during indexing/ingestion.
5. Query embeddings are created later, when a user searches.
6. Keep your embedding setup consistent: documents and queries should go through the same model.
7. The vector is not a replacement for the original text — the vector helps with retrieval; the original text is what you ultimately pass to the LLM.
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "One Embedding or Many?",
                    "description": (
                        "Imagine you have a 100-page university PDF. Would you choose:\n\n"
                        "A. PDF → 1 embedding\n\n"
                        "or\n\n"
                        "B. PDF → chunks → embedding for each chunk → Qdrant\n\n"
                        "Explain your choice, and describe what would go wrong in practice with "
                        "the option you did *not* choose."
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["embeddings", "document-embeddings", "chunking", "rag"],
                },
            ],
            "quiz": {
                "title": "Document Embeddings — Knowledge Check",
                "questions": [
                    {
                        "question": "Why do RAG systems usually embed chunks rather than an entire large document as a single vector?",
                        "options": [
                            "Because embedding models cannot process more than one sentence at a time",
                            "Because a single vector for a very large document would blend too much information together, making retrieval less precise",
                            "Because chunking is required by law for AI applications",
                            "Because vector databases refuse to store more than one vector per document",
                        ],
                        "correct": 1,
                        "explanation": "A single embedding for an entire large document would represent too much mixed information, making it hard to retrieve the specific relevant part; chunking allows more precise retrieval.",
                    },
                    {
                        "question": "In a typical vector database record (e.g. a Qdrant point), what do the vector and the payload/text each provide?",
                        "options": [
                            "The vector is shown to the user; the payload is used only internally and never retrieved",
                            "The vector is used for similarity search; the text/payload provides the actual content and metadata passed to the LLM",
                            "The vector and the text are exactly the same thing stored twice",
                            "The payload is used for search; the vector is discarded after indexing",
                        ],
                        "correct": 1,
                        "explanation": "The vector enables similarity search, while the payload (text and metadata) is what gets retrieved and ultimately given to the LLM as context.",
                    },
                    {
                        "question": "What is the key difference between 'indexing time' and 'query time' in a RAG pipeline?",
                        "options": [
                            "There is no meaningful difference; both happen simultaneously for every user request",
                            "Indexing time prepares the knowledge base (documents → chunks → embeddings → vector DB) ahead of time; query time embeds the user's question and searches against the already-indexed vectors",
                            "Query time is when documents are first uploaded; indexing time is when users ask questions",
                            "Indexing time only applies to English documents",
                        ],
                        "correct": 1,
                        "explanation": "Indexing happens once (or periodically) to prepare the vector database, while query time happens each time a user asks a question and needs their query embedded and compared against the pre-built index.",
                    },
                    {
                        "question": "Why is embedding 1,000,000 document chunks an engineering challenge rather than a purely conceptual one?",
                        "options": [
                            "Because it introduces practical considerations like batching, hardware (GPU vs CPU), processing speed, memory, and cost",
                            "Because embedding models can only process exactly 10 chunks per day",
                            "Because vector databases cannot store more than 1,000 vectors",
                            "Because larger datasets automatically produce worse embeddings",
                        ],
                        "correct": 0,
                        "explanation": "At scale, embedding large numbers of chunks requires engineering decisions around batching, hardware, throughput, memory, and cost — not just calling encode() once.",
                    },
                    {
                        "question": "If a source document is updated (e.g., '160 credit hours' changes to '162 credit hours'), what needs to happen to the vector index?",
                        "options": [
                            "Nothing — the old vector will automatically update itself to reflect the new text",
                            "The affected chunk's old vector should be removed/updated and replaced with a new embedding of the updated text",
                            "The entire vector database must be deleted and the application restarted",
                            "Only the payload text needs to change; the vector can stay the same",
                        ],
                        "correct": 1,
                        "explanation": "Since a vector represents the meaning of specific text at the time it was embedded, updated content requires re-embedding and updating the stored vector, not just the payload text.",
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
            # Topic fields
            "title":            "Query Embeddings",
            "slug":              "embeddings-query-embeddings",
            "description":       "How a user's question is turned into a query vector at search time, how it differs from a document embedding, and why documents and queries must be embedded with a compatible model.",
            "order":             8,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   2.0,
            "skill_tags":        ["embeddings", "query-embeddings", "semantic-search", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Query Embeddings",
                "content": """# Query Embeddings

So far, we learned how to create document embeddings. Now we need the other half of semantic search: **how do we turn the user's question into a vector that we can compare with our document vectors?** That's a query embedding.

## 1. What is a query embedding?

A query embedding is the vector representation of the user's search question:

```
User Query
    ↓
Embedding Model
    ↓
Query Vector
```

For example, "How many credit hours do I need to graduate?" becomes `[0.18, -0.42, 0.73, ..., 0.11]`. That vector is the query embedding.

## 2. Why do we need it?

During indexing, Document 1 → Vector 1, Document 2 → Vector 2, and so on. Now the user asks "How many credits do I need to graduate?" — we need to convert that question into the *same vector space*:

```
Query Vector
      ↓
Compare against
      ↓
Document Vectors
      ↓
Rank by similarity
```

That's semantic search.

## 3. The complete process

**Step 1 — Index documents:** Document → Embedding Model → Document Vector → Qdrant/FAISS.

**Step 2 — User searches:** User Query → *Same* Embedding Model → Query Vector.

**Step 3 — Search:** Query Vector → Qdrant/FAISS → Similarity/Distance → Top-K Documents.

## 4. A concrete example

Knowledge base: D1 = "Students must complete 160 credit hours to graduate.", D2 = "The minimum GPA required for graduation is 2.0.", D3 = "The university library opens at 8 AM." — each embedded into a vector. The user asks Q = "How many credits are needed to graduate?" → Vector Q. Comparing: Q↔D1 → HIGH, Q↔D2 → MEDIUM, Q↔D3 → LOW. The system retrieves D1, D2, ... depending on your top_k and similarity settings.

## 5. Query embedding is not the answer

This is another important distinction. The vector for "How many credits are needed?" does *not* answer the question — it only helps us find relevant information:

```
Query
 ↓
Query Embedding
 ↓
Find relevant documents
 ↓
Documents
 ↓
LLM
 ↓
Answer
```

**The embedding model retrieves information; the LLM generates the final answer.**

## 6. Python example

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

documents = [
    "Students must complete 160 credit hours to graduate.",
    "The minimum GPA required for graduation is 2.0.",
    "The university library opens at 8 AM."
]

document_embeddings = model.encode(documents)

query = "How many credits are needed to graduate?"
query_embedding = model.encode(query)

scores = cosine_similarity([query_embedding], document_embeddings)
print(scores)
```

Conceptually: Query → [query vector] → D1 → 0.91, D2 → 0.62, D3 → 0.18. Then we select the highest-scoring documents.

## 7. Finding the best document

```python
import numpy as np

best_index = np.argmax(scores[0])
print(documents[best_index])
# "Students must complete 160 credit hours to graduate."
```

Now you've built a very small semantic search engine — no Qdrant, no FAISS, no LangChain. Just embedding + cosine similarity + ranking. This is useful because it lets you understand what's happening underneath the frameworks.

## 8. Query embedding vs document embedding

They are similar but have different roles:

| | Document Embedding | Query Embedding |
|---|---|---|
| Input | Document/chunk | User question |
| Created | During indexing | During search |
| Purpose | Represent searchable content | Represent what user wants |
| Stored permanently? | Usually yes | Usually no |
| Compared with | Query vector | Document vectors |

```
              INDEXING

Documents
   ↓
Document Embeddings
   ↓
Vector DB


              QUERY

User Query
   ↓
Query Embedding
   ↓
Vector DB
   ↓
Compare with document embeddings
```

## 9. The same embedding model matters

This is extremely important. If your documents were embedded with `multilingual-e5-large`, your queries should generally be embedded using the *compatible same model/setup* — not Model A for documents and Model B for queries, because Model A produces Vector Space A and Model B produces Vector Space B, and those vectors aren't necessarily comparable:

```
Documents ──→ Model A ──→ Vectors A
                              ↑
                              │
Query ───────→ Model A ──→ Vector A
```

## 10. E5 example

With an E5 retrieval model, you may format the inputs as `query = "query: كام ساعة محتاج عشان أتخرج؟"` and `document = "passage: يشترط للتخرج إتمام 160 ساعة معتمدة."`, then embed each with E5 to get a Query Vector and a Document Vector, and compare them. The `query:` and `passage:` prefixes are part of *that model's* intended retrieval setup. Again, this is model-specific — don't automatically add these prefixes to every embedding model.

## 11. Why query wording matters

Consider "How many credits do I need to graduate?" (Q1, specific) vs. "Tell me about graduation." (Q2, vague) — both about graduation, but Q1 is much more specific, and the query embedding reflects the information contained in the query. More specific query → potentially better retrieval. This is one reason query formulation can matter. However, remember your Prompt Engineering lesson: **if retrieval is fundamentally bad, endlessly rewriting the prompt isn't the real solution.** Sometimes the problem is the embedding model, chunking, data quality, or retrieval strategy.

## 12. Query embeddings in your Arabic RAG

Your previous architecture probably looked roughly like:

```
                 User
                  ↓
        "كام ساعة للتخرج؟"
                  ↓
          Query Embedding
                  ↓
               Qdrant
                  ↓
        Similarity Search
                  ↓
          Relevant Chunks
                  ↓
                 Reranker
                  ↓
                  LLM
                  ↓
                Answer
```

Now you can identify exactly what "Query Embedding" means: the Arabic question passed through a multilingual embedding model to produce the query vector that Qdrant uses to find relevant stored vectors.

## 13. A useful optimization

If your database contains 1,000,000 document chunks, you don't want to generate new embeddings for all documents every time someone asks a question. That's why document embeddings are precomputed during indexing: 1,000,000 documents → 1,000,000 embeddings → stored in vector DB. Then each query only requires: 1 user question → 1 query embedding → search existing vectors. This is one of the reasons vector databases make semantic search practical.

## 14. Query embedding in a production RAG

```
                 USER
                  │
                  ▼
               Query
                  │
                  ▼
          Query Embedding
                  │
                  ▼
          Vector Database
                  │
                  ▼
           Top-K Retrieval
                  │
                  ▼
             Reranking
                  │
                  ▼
          Context Construction
                  │
                  ▼
                 LLM
                  │
                  ▼
               Answer
```

You've already implemented versions of this. Now you're understanding the individual mathematical components underneath it.

## 🧠 Key Takeaways

1. Query embedding: User Query → Embedding Model → Query Vector.
2. It is used for retrieval, not generation: Query Embedding → find relevant information → LLM → Answer.
3. Documents are embedded during indexing; queries are embedded when users search.
4. Use a compatible embedding setup for both: Documents → Model X, Queries → Model X.
5. Your Qdrant/FAISS retrieval is essentially: Query → Query Vector → Compare with stored Document Vectors → Rank → Top-K.

**Most important mental model:** document embeddings describe what your knowledge base *contains*; query embeddings describe what the user is *looking for*.
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Trace a Query From Question to Retrieval",
                    "description": (
                        "You have these stored documents:\n\n"
                        "D1: \"The tuition fee is 1330 EGP per credit hour.\"\n"
                        "D2: \"Students need 160 credit hours to graduate.\"\n"
                        "D3: \"The minimum GPA for graduation is 2.0.\"\n\n"
                        "The user asks: \"How much does one credit hour cost?\"\n\n"
                        "Explain the process from the user's query until D1 is retrieved. Don't "
                        "worry about code — explain the steps in your own words, and be explicit "
                        "about which embedding model is used for the query versus the documents."
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["embeddings", "query-embeddings", "semantic-search", "rag"],
                },
            ],
            "quiz": {
                "title": "Query Embeddings — Knowledge Check",
                "questions": [
                    {
                        "question": "What is a query embedding?",
                        "options": [
                            "The final natural-language answer returned to the user",
                            "The vector representation of the user's search question, created at search time",
                            "A copy of the document embedding used for indexing",
                            "A special type of vector database index",
                        ],
                        "correct": 1,
                        "explanation": "A query embedding is the vector produced by running the user's question through an embedding model at query time.",
                    },
                    {
                        "question": "What is the key difference in *when* document embeddings and query embeddings are created?",
                        "options": [
                            "Both are always created at the exact same time, during indexing",
                            "Document embeddings are typically created during indexing (ahead of time); query embeddings are created during search, when a user asks a question",
                            "Query embeddings are created during indexing; document embeddings are created during search",
                            "Neither is ever precomputed",
                        ],
                        "correct": 1,
                        "explanation": "Document embeddings are usually precomputed once during indexing and reused, while query embeddings are generated fresh each time a user submits a question.",
                    },
                    {
                        "question": "Why must a query be embedded using a model compatible with the one used to embed the documents?",
                        "options": [
                            "It isn't actually necessary — any embedding model can compare with any other",
                            "Different embedding models produce different, generally incompatible vector spaces, so mixing them makes similarity scores meaningless",
                            "Because query embeddings are always larger than document embeddings",
                            "Because only one embedding model exists in total",
                        ],
                        "correct": 1,
                        "explanation": "If the query and documents come from different embedding spaces, their vectors can't be meaningfully compared, so the same (or a compatible) model must be used for both.",
                    },
                    {
                        "question": "Does the query embedding itself answer the user's question?",
                        "options": [
                            "Yes, the query embedding directly contains the answer text",
                            "No — the query embedding only helps find relevant documents; an LLM (or similar) is needed to generate the final answer from that retrieved context",
                            "Yes, but only for questions under 10 words",
                            "No, query embeddings are never used in retrieval at all",
                        ],
                        "correct": 1,
                        "explanation": "The query embedding is used purely for retrieval — finding relevant documents. Generating a final natural-language answer is a separate step, typically handled by an LLM.",
                    },
                    {
                        "question": "Why is it advantageous to precompute document embeddings during indexing rather than regenerating them on every query?",
                        "options": [
                            "It has no advantage; regenerating them every time is just as fast",
                            "At scale (e.g. millions of documents), regenerating all document embeddings on every query would be extremely wasteful; precomputing once and reusing them makes each query only require embedding the (much smaller) question",
                            "Because document embeddings expire after one use and cannot be reused anyway",
                            "Because query embeddings are impossible to compute quickly",
                        ],
                        "correct": 1,
                        "explanation": "Precomputing document embeddings during indexing avoids redundant, expensive re-embedding of the entire corpus for every single query — only the query needs to be embedded at search time.",
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
            # Topic fields
            "title":            "Semantic Search",
            "slug":              "embeddings-semantic-search",
            "description":       "How embeddings, similarity, and vector search combine into semantic search — searching by meaning rather than exact keywords — and how it differs from full RAG.",
            "order":             9,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   2.0,
            "skill_tags":        ["embeddings", "semantic-search", "vector-search", "top-k", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Semantic Search",
                "content": """# Semantic Search

You now understand embeddings, vectors, similarity, cosine similarity, embedding models, multilingual embeddings, and document embeddings. Now we combine them into one practical concept: **Semantic Search**.

## 1. What is semantic search?

Semantic search means **searching based on the meaning of the query rather than only matching exact words**. Traditional keyword search for "How many credits do I need to graduate?" would look for the literal words "credits" and "graduate." Semantic search instead converts the query into a vector:

```
Query
  ↓
Embedding Model
  ↓
Query Vector
```

Then searches for documents with similar vectors:

```
Query Vector
      ↓
Similarity Search
      ↓
Similar Document Vectors
      ↓
Relevant Documents
```

## 2. Keyword search vs semantic search

Your database contains "Students must complete 160 credit hours to graduate." The user asks "How many hours do I need to finish my degree?"

**Keyword search** looks for matching words — there may be little or no exact overlap between "hours, finish, degree" and "160, credit, graduate," so keyword search may struggle.

**Semantic search** represents both as vectors (`[0.12, -0.43, 0.77, ...]` and `[0.14, -0.41, 0.75, ...]`), finds their similarity is HIGH, and retrieves the document anyway.

## 3. The semantic search pipeline

This is the core pipeline you should memorize:

```
                 INDEXING

Documents
    ↓
Chunking
    ↓
Document Embeddings
    ↓
Vector Database
```

Then:

```
                  SEARCH

User Query
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Ranking
    ↓
Top-K Results
```

That's semantic search.

## 4. A simple example

```python
documents = [
    "Students must complete 160 credit hours to graduate.",
    "The minimum GPA required for graduation is 2.0.",
    "The university library opens at 8 AM."
]

query = "How many credits are needed to graduate?"

document_embeddings = model.encode(documents)
query_embedding = model.encode(query)

scores = cosine_similarity([query_embedding], document_embeddings)
```

Conceptually:

```
Query
 ↓
How many credits are needed?
 ↓
        Similarity
       /    |     \\
      /     |      \\
    0.91   0.63    0.12
     ↓      ↓       ↓
    D1     D2      D3
```

So D1 becomes the best result.

## 5. Ranking is essential

Semantic search doesn't just answer "which documents are relevant?" — it normally produces a ranking: 1. D1 → 0.91, 2. D2 → 0.63, 3. D3 → 0.12. Then we choose the top results, e.g. `top_k = 2` gives D1 and D2. This is called **Top-K retrieval**.

## 6. Why retrieve more than one?

If the user asks "Tell me about graduation requirements," there may not be one single chunk containing everything — you might have separate chunks for required credit hours, minimum GPA, required courses, and the graduation application. A good retrieval system returns several chunks, and the LLM receives all of them as context. This is where semantic search becomes the foundation of RAG.

## 7. Semantic search without an LLM

You do not need an LLM to perform semantic search — you only need an embedding model plus a similarity calculation: Query → Embedding → Compare vectors → Rank → Results. The LLM comes later if you want to generate an answer. So **semantic search and RAG are not the same thing.**

## 8. Semantic Search vs RAG

**Semantic Search**: Query → Embedding → Search → Documents (the system gives you relevant documents).

**RAG**: Query → Embedding → Search → Documents → Context → LLM → Generated Answer.

Semantic search can be a retrieval component *inside* a RAG system.

## 9. Connecting this to your previous RAG system

Your previous architecture included BM25, dense retrieval, RRF, a reranker, Qdrant, and an LLM. Semantic search is essentially the **dense retrieval** part: Query → Embedding → Qdrant → Vector similarity → Top-K. You might combine it with BM25:

```
                 Query
                   ↓
            ┌──────┴──────┐
            ↓             ↓
       Dense Search    BM25
            ↓             ↓
         Results       Results
            └──────┬──────┘
                   ↓
                  RRF
                   ↓
               Reranker
                   ↓
                LLM
```

We'll study these advanced retrieval techniques later — for now, focus on the semantic search foundation.

## 10. Semantic search can understand paraphrases

Query "How much is one credit hour?" vs document "The cost of a credit hour is 1330 EGP." — the wording is different ("how much" ≈ "cost", "one credit hour" ≈ "a credit hour"), but the meaning is related, and embedding-based search can capture this relationship.

## 11. Arabic example

Document: "يشترط للتخرج إتمام 160 ساعة معتمدة." Query: "أنا محتاج كام ساعة عشان أتخرج؟" The pipeline: Arabic Document → Document Embedding → Vector → Qdrant, then Arabic Query → Query Embedding → Query Vector → Qdrant → Similarity Search → Relevant Arabic Document. The exact wording doesn't need to match.

## 12. Semantic search is not magic

Semantic search can fail. Query "What is the tuition fee?" might retrieve "Students must complete 160 credit hours." instead of the tuition information, due to a poor embedding model, an ambiguous query, poor chunking, noisy documents, similar concepts, domain-specific terminology, or bad similarity configuration. **Semantic search ≠ perfect search** — you need evaluation and tuning.

## 13. The importance of chunk quality

If a document blending graduation credits, GPA, tuition, and library hours is stored as *one huge chunk*, its embedding represents many different concepts at once. A query about tuition may retrieve it, but the result contains lots of irrelevant information. Better chunking — separate chunks for graduation credits, GPA, tuition, and library — lets "How much is a credit hour?" retrieve the tuition chunk precisely. Semantic search quality isn't only about the embedding model.

## 14. Metadata can improve search

You can sometimes combine semantic search with metadata filters — e.g., query "How much does a credit hour cost?" with filter `document_type = "tuition"`:

```
Query
 ↓
Query Embedding
 ↓
Metadata Filter
 ↓
Semantic Search
 ↓
Relevant Results
```

This can dramatically reduce irrelevant retrieval.

## 15. Semantic search at scale

Comparing 1 query against 3 documents is easy in Python. But production systems may compare 1 query against 1,000,000 vectors — you don't want to manually calculate cosine similarity against every vector in an inefficient Python loop. That's where systems such as FAISS, Qdrant, Milvus, Pinecone, and Weaviate become useful: they provide efficient vector search/indexing mechanisms.

```
Small experiment: Python → Cosine similarity → Search
Production:       Embedding → Vector database/index → Efficient nearest-neighbor search
```

## 16. Nearest-neighbor search

**Nearest Neighbor Search** means finding vectors that are closest to a given vector according to a chosen metric:

```
                 Query
                   ●
                 /   \\
                /     \\
               ●       ●
             Doc A   Doc B


                         ●
                       Doc C
```

The nearest vectors are likely the most semantically similar. For large datasets, systems often use **Approximate Nearest Neighbor (ANN)** techniques to make search much faster. You don't need to learn the algorithms yet — just remember: Semantic Search → Nearest Neighbor Search.

## 17. The complete mental model

```
                    DOCUMENTS
                        ↓
                     Chunking
                        ↓
                Document Embeddings
                        ↓
                  Vector Database
                        │
                        │
                        ▼
USER QUERY → Query Embedding
                        ↓
                Vector Similarity
                        ↓
                 Nearest Neighbors
                        ↓
                    Ranking
                        ↓
                     Top-K
```

And when used inside RAG:

```
Top-K
  ↓
Context Construction
  ↓
LLM
  ↓
Answer
```

## 🧠 Key Takeaways

Semantic search means searching by meaning rather than exact keywords. Basic pipeline: Query → Embedding → Vector Search → Similarity → Ranking → Top-K Documents.

Remember these distinctions:
- **Embedding** → creates the vector
- **Similarity** → compares vectors
- **Semantic Search** → uses vector similarity to find relevant information
- **Vector Database** → efficiently stores/searches those vectors
- **RAG** → uses retrieved information to help an LLM generate an answer

One very important engineering principle: **good semantic search depends on more than the embedding model — data quality, chunking, similarity configuration, metadata, and retrieval strategy all matter.**
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Tracing a Semantic Search Query",
                    "description": (
                        "You have these documents:\n\n"
                        "D1: \"Students must complete 160 credit hours to graduate.\"\n"
                        "D2: \"The minimum GPA required for graduation is 2.0.\"\n"
                        "D3: \"The tuition fee is 1330 EGP per credit hour.\"\n"
                        "D4: \"The university library opens at 8 AM.\"\n\n"
                        "Query: \"How much do I pay for one credit hour?\"\n\n"
                        "1. Which document should semantic search rank first, and why?\n\n"
                        "2. Explain the semantic-search pipeline step by step, from the user's "
                        "query until D3 is retrieved.\n\n"
                        "3. Is this semantic search alone enough to produce a final answer for "
                        "the user, or is another component needed? Explain."
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["embeddings", "semantic-search", "rag"],
                },
            ],
            "quiz": {
                "title": "Semantic Search — Knowledge Check",
                "questions": [
                    {
                        "question": "What is the core difference between keyword search and semantic search?",
                        "options": [
                            "Keyword search only works in English; semantic search works in every language equally well",
                            "Keyword search matches exact words/phrases; semantic search compares the meaning of the query and documents via embeddings",
                            "There is no real difference between them",
                            "Semantic search never uses vectors, only keyword search does",
                        ],
                        "correct": 1,
                        "explanation": "Keyword search relies on literal word overlap, while semantic search embeds the query and documents into vectors and compares them by meaning.",
                    },
                    {
                        "question": "Is semantic search the same thing as RAG?",
                        "options": [
                            "Yes, they are always identical",
                            "No — semantic search retrieves relevant documents using embeddings and similarity; RAG adds an LLM step that generates an answer from that retrieved context",
                            "No — RAG never uses semantic search at all",
                            "Yes, because both require a vector database",
                        ],
                        "correct": 1,
                        "explanation": "Semantic search is a retrieval technique (query → embedding → search → documents). RAG builds on top of retrieval by feeding the retrieved context to an LLM to generate an answer.",
                    },
                    {
                        "question": "Why might chunk quality affect semantic search results, even with a good embedding model?",
                        "options": [
                            "Chunk quality has no effect on search results, only the embedding model matters",
                            "A chunk that blends many unrelated concepts together produces a vector representing all of them, making it harder to retrieve just the relevant part precisely",
                            "Chunking is only relevant for keyword search, not semantic search",
                            "Smaller chunks always produce worse embeddings than large chunks",
                        ],
                        "correct": 1,
                        "explanation": "If a chunk mixes multiple topics, its embedding becomes a blend of all of them, reducing precision when a query is about just one specific topic within that chunk.",
                    },
                    {
                        "question": "Why do production systems use tools like FAISS, Qdrant, or Pinecone instead of manually computing cosine similarity in a Python loop?",
                        "options": [
                            "Because manual cosine similarity calculations are mathematically incorrect",
                            "Because at scale (e.g. millions of vectors), efficient nearest-neighbor search and indexing are needed for practical performance",
                            "Because these tools eliminate the need for an embedding model entirely",
                            "Because Python cannot compute cosine similarity at all",
                        ],
                        "correct": 1,
                        "explanation": "Comparing a query against millions of vectors with naive Python loops doesn't scale; specialized vector search systems provide efficient (often approximate) nearest-neighbor search.",
                    },
                    {
                        "question": "How can metadata filtering improve semantic search results?",
                        "options": [
                            "It replaces the need for embeddings entirely",
                            "It narrows the candidate set (e.g., only 'tuition' documents) before or alongside similarity search, reducing irrelevant retrieval",
                            "It always makes search slower with no benefit",
                            "It only works for English-language documents",
                        ],
                        "correct": 1,
                        "explanation": "Combining semantic search with metadata filters (like document type) helps constrain results to a relevant subset, improving precision.",
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
            # Topic fields
            "title":            "Similarity Thresholds",
            "slug":              "embeddings-similarity-thresholds",
            "description":       "Why Top-K retrieval always returns something even when nothing is relevant, how similarity thresholds act as a minimum relevance gate, and the precision/recall tradeoff of choosing one.",
            "order":             10,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   2.0,
            "skill_tags":        ["embeddings", "similarity-thresholds", "top-k", "precision-recall", "rag"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Similarity Thresholds",
                "content": """# Similarity Thresholds

So far, we learned how to find the most similar documents. But there's an important problem: **what if nothing is actually relevant?** This is where similarity thresholds become important.

## 1. The problem with Top-K

Your database contains chunks about graduation requirements, tuition fees, course registration, and library hours. The user asks "How do I apply for a passport?" — your university database probably has nothing about passports. But if you use `top_k = 3`, the system will still return three documents, e.g. D1 → 0.31, D2 → 0.27, D3 → 0.22. Why? **Because Top-K always returns something if there are vectors to search.** That's dangerous for RAG.

## 2. The solution: similarity threshold

Instead of "give me the 3 most similar documents," we can say "give me the most similar documents, *but only if they are similar enough*." For example, with `threshold = 0.70`: D1 (0.31) ❌, D2 (0.27) ❌, D3 (0.22) ❌ → result: no sufficiently relevant documents found. This is much safer.

## 3. Simple mental model

Think of a threshold as a minimum quality gate:

```
Similarity Score

0.00 ─────────────── 0.50 ─────────────── 1.00
                       │
                  threshold
                       │
              ┌────────┴────────┐
              │                 │
           Reject             Accept
```

If `score >= threshold`, keep the result. If `score < threshold`, discard it.

## 4. Example

Query "How much is one credit hour?" returns D1 → 0.92, D2 → 0.71, D3 → 0.43, D4 → 0.18. With `threshold = 0.70`, we keep D1 and D2, and reject D3 and D4:

```
Query
 ↓
Vector Search
 ↓
Scores
 ↓
Threshold Filter
 ↓
Relevant Documents
```

## 5. Why this matters in RAG

**Without a threshold:** user asks something unrelated → retriever finds "closest" documents anyway → LLM receives irrelevant context → LLM tries to answer → potential hallucination.

**With a threshold:** user asks something unrelated → retriever searches → scores are too low → no relevant context → system says "I don't have enough information." That's much better production behavior.

## 6. Very important: similarity ≠ relevance

Query "What is the tuition fee?" returns D1 → 0.48, D2 → 0.45, D3 → 0.42. D1 is the most similar — but does that mean D1 is actually relevant? Not necessarily. The system only knows D1 is *more similar than* D2 and D3, not that D1 contains the correct answer. **Similarity is a ranking signal, not a guarantee of correctness.**

## 7. There is no universal "good score"

Don't treat "0.8 = good, 0.5 = bad" as a universal rule. Similarity scores depend on the embedding model, similarity metric, normalization, dataset, language, domain, query type, and chunk quality. A score of 0.65 might be useful for one system and poor for another. **You should determine the threshold experimentally for your specific system.**

## 8. Cosine similarity example

Documents D1 → 0.91, D2 → 0.74, D3 → 0.51, D4 → 0.12. With `threshold = 0.70`: D1 ✓, D2 ✓, D3 ✗, D4 ✗. With `threshold = 0.85`: D1 ✓, D2 ✗, D3 ✗, D4 ✗. **Higher threshold** → more strict retrieval. **Lower threshold** → more permissive retrieval.

## 9. Precision vs recall

**High threshold (0.85):** retrieve fewer documents. Advantage: less irrelevant context. Disadvantage: might miss useful documents.

**Low threshold (0.40):** retrieve more documents. Advantage: less chance of missing relevant information. Disadvantage: more irrelevant documents.

```
High threshold → High precision → Potentially lower recall
Low threshold  → Potentially higher recall → Potentially lower precision
```

We'll study retrieval evaluation much more deeply in Level 10.

## 10. Threshold + Top-K

You can combine them: `top_k = 5`, `threshold = 0.70` means "find up to 5 results, but only keep results whose similarity is at least 0.70." If search returns D1 → 0.94, D2 → 0.88, D3 → 0.79, D4 → 0.61, D5 → 0.42, after thresholding you keep D1, D2, D3 (D4 and D5 fall below 0.70).

## 11. Python example

```python
scores = [0.92, 0.81, 0.63, 0.41]
threshold = 0.70

filtered = [score for score in scores if score >= threshold]
print(filtered)
# [0.92, 0.81]
```

In a real search system, keep the document together with its score:

```python
results = [
    ("D1", 0.92),
    ("D2", 0.81),
    ("D3", 0.63),
    ("D4", 0.41),
]

threshold = 0.70

filtered = [(doc, score) for doc, score in results if score >= threshold]
print(filtered)
# [("D1", 0.92), ("D2", 0.81)]
```

That's essentially the basic idea behind threshold filtering.

## 12. A production RAG example

User asks "كام ساعة محتاج عشان أتخرج؟" — retriever returns Chunk 1 → 0.93, Chunk 2 → 0.87, Chunk 3 → 0.45, Chunk 4 → 0.31. With `threshold = 0.70`, you send only Chunk 1 and Chunk 2 forward. Now the user asks "ما هي مواعيد مباريات الدوري الإنجليزي؟" (English Premier League fixtures) — your academic database returns everything below 0.35. With `threshold = 0.70`, the result is: no relevant documents. Your application can respond appropriately instead of pretending the academic database contains the answer.

## 13. Thresholds are especially useful for "I don't know"

A robust RAG system should be able to say "I don't have enough information to answer that" rather than forcing an answer:

```
User Query
    ↓
Query Embedding
    ↓
Vector Search
    ↓
Similarity Scores
    ↓
Threshold
    ↓
 ┌───────────────┐
 │               │
Pass           Fail
 │               │
 ↓               ↓
Retrieve       No relevant
context        context
 │               │
 ↓               ↓
LLM          "I don't know"
```

This is an important production behavior.

## 14. But don't blindly add a threshold

A threshold is useful, but **a poorly chosen threshold can make your system worse.** If relevant documents usually score around 0.62–0.68, and you choose `threshold = 0.80`, you will reject the correct documents — your RAG may start saying "I don't know" even when the answer exists. Threshold selection is an evaluation problem, not a number you guess.

## 15. How should you choose a threshold?

A simple process, before you learn formal retrieval evaluation later:

1. **Create real queries** — Q1, Q2, Q3, ..., Q100.
2. **Mark which documents are actually relevant** — e.g., Q1 → D4 relevant.
3. **Run your embedding search and record scores** — e.g., Q1 → D4 → 0.73.
4. **Experiment with thresholds** — 0.50, 0.55, 0.60, 0.65, 0.70, 0.75 — and measure which threshold gives you the best retrieval behavior.

This is much better than "I read online that 0.7 is a good threshold."

## 16. One more important issue: different models, different scores

If Model A gives D1 → 0.82 and Model B gives D1 → 0.67, you *cannot* automatically conclude Model A is better just because 0.82 > 0.67 — the scores come from different embedding spaces/models. You need to evaluate retrieval quality using your dataset.

## 17. Your previous Qdrant experience

Your pipeline was: Query → Embedding → Qdrant → Vector similarity → Top-K. Now we're adding a similarity-score and threshold step:

```
Query
 ↓
Embedding
 ↓
Qdrant
 ↓
Top-K Search
 ↓
Threshold Filtering
 ↓
Relevant Context
 ↓
Reranker / LLM
```

This is one of the simplest ways to improve retrieval robustness.

## 🧠 Key Takeaways

1. Top-K always tries to return results, even if the query is completely unrelated.
2. A similarity threshold creates a minimum relevance requirement: `score >= threshold → keep`, `score < threshold → reject`.
3. Similarity does not guarantee relevance — it is primarily a ranking signal.
4. There is no universal threshold — don't blindly use 0.7 because someone recommended it.
5. Threshold selection should be based on your actual data.
6. Threshold and Top-K can work together: Top-K = maximum number, Threshold = minimum similarity.

**Most important mental model:** Top-K asks "What are the closest results?" Threshold asks "Are they close enough to trust/use?"
""",
                "estimated_minutes": 30,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Combining Top-K and Threshold",
                    "description": (
                        "Your semantic search returns:\n\n"
                        "D1 → 0.91\nD2 → 0.76\nD3 → 0.68\nD4 → 0.42\nD5 → 0.21\n\n"
                        "You configure: top_k = 4, threshold = 0.70\n\n"
                        "1. Which documents will finally be returned?\n\n"
                        "2. Why isn't D4 returned even though top_k = 4?\n\n"
                        "3. What could happen if you increase the threshold from 0.70 to 0.85?"
                    ),
                    # theory-only exercise, graded conversationally by AnswerChat
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["embeddings", "similarity-thresholds", "top-k", "rag"],
                },
            ],
            "quiz": {
                "title": "Similarity Thresholds — Knowledge Check",
                "questions": [
                    {
                        "question": "Why is relying only on Top-K retrieval risky for RAG systems?",
                        "options": [
                            "Top-K is always slower than threshold filtering",
                            "Top-K always returns a fixed number of results even if none of them are actually relevant, which can feed irrelevant context to the LLM",
                            "Top-K can only return one document at a time",
                            "Top-K cannot be used together with embeddings",
                        ],
                        "correct": 1,
                        "explanation": "Top-K retrieval returns the k closest vectors regardless of whether they're actually relevant, which is risky when a query has no good match in the knowledge base.",
                    },
                    {
                        "question": "What does a similarity threshold do?",
                        "options": [
                            "It guarantees the retrieved document is factually correct",
                            "It sets a minimum similarity score a result must meet to be kept, filtering out results that aren't similar enough",
                            "It increases the number of documents returned by search",
                            "It replaces the need for an embedding model",
                        ],
                        "correct": 1,
                        "explanation": "A threshold acts as a minimum quality gate: results scoring below it are discarded, regardless of how they rank relative to each other.",
                    },
                    {
                        "question": "Why is it wrong to assume a similarity score like 0.7 is a universally 'good' threshold across all systems?",
                        "options": [
                            "Because 0.7 is always too low for any system",
                            "Because similarity scores depend on the embedding model, metric, normalization, dataset, language, and domain, so a 'good' score varies by system",
                            "Because thresholds can only be integers, not decimals",
                            "Because cosine similarity always produces scores above 0.9 regardless of relevance",
                        ],
                        "correct": 1,
                        "explanation": "Similarity scores are not standardized across systems — what counts as a strong or weak score depends heavily on the specific embedding model and data, so thresholds must be tuned experimentally.",
                    },
                    {
                        "question": "What is the tradeoff between a high similarity threshold and a low one?",
                        "options": [
                            "There is no tradeoff — higher thresholds are always strictly better",
                            "A high threshold tends toward higher precision but potentially lower recall; a low threshold tends toward higher recall but potentially lower precision",
                            "A high threshold always retrieves more documents than a low threshold",
                            "Thresholds have no relationship to precision or recall",
                        ],
                        "correct": 1,
                        "explanation": "Raising the threshold filters out more borderline results (higher precision, possibly missing relevant ones), while lowering it keeps more results (potentially higher recall, but more noise).",
                    },
                    {
                        "question": "Why can setting a threshold too high (e.g. 0.80) actually make a RAG system worse, if relevant documents usually score around 0.62–0.68?",
                        "options": [
                            "It has no negative effect since higher is always safer",
                            "It will reject documents that are actually relevant, causing the system to incorrectly respond 'I don't know' even when the answer exists",
                            "It will cause the embedding model to crash",
                            "It will force the system to always return every document instead of filtering",
                        ],
                        "correct": 1,
                        "explanation": "If the threshold is set above where genuinely relevant documents actually score, correct answers get filtered out, leading to false 'I don't know' responses.",
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
            # Topic fields
            "title":            "Semantic Search Project",
            "slug":              "embeddings-semantic-search-project",
            "description":       "Capstone for Level 5: build a small semantic search engine from scratch (no LangChain/Qdrant/FAISS) to see the full indexing → query → similarity → ranking → threshold pipeline with your own code.",
            "order":             11,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   3.0,
            "skill_tags":        ["embeddings", "semantic-search", "similarity-thresholds", "top-k", "rag", "capstone"],
            "prerequisite_ids":  [],
            # Content
            "lesson": {
                "title": "Semantic Search Project",
                "content": """# Semantic Search Project

This is the final lesson of Level 5. We're going to build a small semantic search engine from scratch so you can connect everything we've learned:

```
Documents
   ↓
Document Embeddings
   ↓
Vector Search

User Query
   ↓
Query Embedding
   ↓
Similarity
   ↓
Ranking
   ↓
Threshold
   ↓
Relevant Documents
```

We'll keep it simple first — no LangChain, Qdrant, or FAISS. The goal is to understand the mechanics *underneath* them.

## 1. Our project

We'll build a tiny **University Semantic Search Engine**. Our knowledge base:

```python
documents = [
    "Students must complete 160 credit hours to graduate.",
    "The minimum GPA required for graduation is 2.0.",
    "The cost of one credit hour is 1330 EGP.",
    "Students must register their courses before the registration deadline.",
    "The university library opens at 8 AM."
]
```

A user can ask "How many credits do I need to finish my degree?" and our system should find "Students must complete 160 credit hours to graduate."

## 2. Step 1 — Load the embedding model

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
```

The model converts text into vectors: Text → Embedding Model → Vector.

## 3. Step 2 — Create document embeddings

```python
document_embeddings = model.encode(documents)
```

If we have 5 documents and the model produces 384-dimensional vectors, `document_embeddings.shape` → `(5, 384)`. These are our stored document vectors.

## 4. Step 3 — Receive a query

```python
query = "How many credits do I need to finish my degree?"
query_embedding = model.encode(query)
```

Conceptually: User Query → Embedding Model → Query Vector.

## 5. Step 4 — Calculate similarity

```python
from sklearn.metrics.pairwise import cosine_similarity

scores = cosine_similarity([query_embedding], document_embeddings)[0]
```

We might get conceptually: D1 → 0.89, D2 → 0.61, D3 → 0.45, D4 → 0.32, D5 → 0.12. The exact numbers aren't important — what matters is the *ranking*: D1 most similar, D2 second, D3 third.

## 6. Step 5 — Rank the results

```python
ranked_indices = scores.argsort()[::-1]

for index in ranked_indices:
    print(documents[index], scores[index])
```

Now we have a semantic ranking.

## 7. Step 6 — Add Top-K

```python
top_k = 3
top_indices = ranked_indices[:top_k]
```

Now we only return the three most similar documents.

## 8. Step 7 — Add a similarity threshold

```python
threshold = 0.60

results = []

for index in ranked_indices:
    score = scores[index]

    if score < threshold:
        continue

    results.append({
        "text": documents[index],
        "score": float(score)
    })

    if len(results) >= top_k:
        break
```

Now our system has both Top-K *and* Threshold.

## 9. Complete simple implementation

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


documents = [
    "Students must complete 160 credit hours to graduate.",
    "The minimum GPA required for graduation is 2.0.",
    "The cost of one credit hour is 1330 EGP.",
    "Students must register their courses before the registration deadline.",
    "The university library opens at 8 AM."
]


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Document embeddings
document_embeddings = model.encode(documents)


def semantic_search(query, top_k=3, threshold=0.60):

    # Query embedding
    query_embedding = model.encode(query)

    # Similarity
    scores = cosine_similarity(
        [query_embedding],
        document_embeddings
    )[0]

    # Rank
    ranked_indices = scores.argsort()[::-1]

    results = []

    # Top-K + threshold
    for index in ranked_indices:

        score = float(scores[index])

        if score < threshold:
            continue

        results.append({
            "text": documents[index],
            "score": score
        })

        if len(results) >= top_k:
            break

    return results
```

Now we can search:

```python
results = semantic_search("How many credits do I need to finish my degree?")

for result in results:
    print(result)
```

You should get the graduation-credit document near the top.

## 10. Try different queries

`semantic_search("What is the tuition price for a credit hour?")` should retrieve "The cost of one credit hour is 1330 EGP." `semantic_search("What GPA do I need to graduate?")` should retrieve "The minimum GPA required for graduation is 2.0." `semantic_search("When can I use the library?")` should retrieve the library document.

## 11. Test an unrelated query

Now try `semantic_search("How do I repair my car?")`. There isn't a car-repair document. Ideally, the similarity scores should be low enough that our threshold prevents irrelevant results. This is exactly why we studied similarity thresholds before building this project.

## 12. What's happening underneath?

```
                    INDEXING

University Documents
        ↓
Embedding Model
        ↓
Document Vectors
        ↓
Stored in Memory
```

Then:

```
                     QUERY

"How many credits?"
        ↓
Embedding Model
        ↓
Query Vector
        ↓
Cosine Similarity
        ↓
Similarity Scores
        ↓
Ranking
        ↓
Top-K
        ↓
Threshold
        ↓
Relevant Documents
```

That's the complete semantic search pipeline.

## 13. Where would Qdrant fit?

Our simple project does: Python list → compare against every vector. Qdrant replaces our simple storage/search mechanism: Documents → Embeddings → Qdrant → Efficient Vector Search. Our project: Query Vector → Compare with all vectors → Rank. Production: Query Vector → Qdrant → Efficient nearest-neighbor search → Rank. **Qdrant isn't the thing creating semantic meaning — the embedding model creates the representation. Qdrant helps you store and efficiently search those representations.**

## 14. Where would FAISS fit?

Same idea. FAISS is primarily a library for efficient similarity search over vectors: Embedding Model → Vectors → FAISS → Nearest vectors. Embedding model → creates vectors. FAISS → searches vectors. This distinction is extremely important.

## 15. Where does RAG fit?

Our project currently ends at: Query → Semantic Search → Relevant Documents. RAG continues: Query → Semantic Search → Relevant Documents → Context Construction → LLM → Answer. For example, semantic search finds "Students must complete 160 credit hours to graduate.", and RAG gives that to the LLM as context alongside the question, producing "You need to complete 160 credit hours to graduate." So: **Semantic Search → Retrieval component → RAG.**

## 16. Important production improvement

Our example embeds the documents *once*: `document_embeddings = model.encode(documents)`. We shouldn't do this every time a user searches.

**Bad:** Every query → re-embed all documents → search.

**Correct:** Indexing: Documents → Embeddings → Store. Query: Query → Query embedding → Search stored embeddings.

This distinction becomes critical when you have thousands or millions of chunks.

## 17. What we intentionally didn't use

Notice we didn't use LangChain, LangGraph, LlamaIndex, Qdrant, FAISS, or Chroma. That's intentional — you've already used these tools practically. The goal of this project was to understand the core mechanism underneath them. Once you understand Text → Embedding → Vector → Similarity → Ranking → Top-K → Threshold, a vector database becomes much easier to understand. It's no longer a mysterious black box.

## 18. What you learned in this level

You've now completed the full progression: What Are Embeddings? (text → numerical representation) → Vector Representations (text → vector in a high-dimensional space) → Similarity (compare vectors to measure semantic closeness) → Cosine Similarity (measure the angle/direction between vectors) → Embedding Models (models that convert text into embeddings) → Multilingual Embeddings (multiple languages → compatible semantic representations) → Document Embeddings (document chunks → stored vectors) → Query Embeddings (user query → query vector) → Semantic Search (query vector → similar document vectors) → Similarity Thresholds (only accept results that are sufficiently similar) → this capstone (all concepts → working semantic search system).

## 🧠 Final Mental Model

If you remember only one diagram from this level, remember this:

```
                 INDEXING

Documents
    ↓
Chunking
    ↓
Document Embeddings
    ↓
Vector Database
    │
    │
    │
    ▼
────────────────────────────────


                  QUERY

User Question
    ↓
Query Embedding
    ↓
Query Vector
    ↓
Similarity Search
    ↓
Ranking
    ↓
Top-K
    ↓
Threshold
    ↓
Relevant Chunks
```

And the next level will add:

```
Relevant Chunks
      ↓
Context
      ↓
LLM
      ↓
Answer
```

That's the bridge from semantic search → RAG.

## 🎯 Level Complete

You now have the conceptual foundation for the embedding/retrieval systems you've already been building with Qdrant, FAISS, Chroma, and RAG.
""",
                "estimated_minutes": 45,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Build and Extend the Semantic Search Engine",
                    "description": (
                        "Using the complete implementation from this lesson:\n\n"
                        "1. Run `semantic_search()` against all the example queries in the lesson "
                        "(tuition, GPA, library) and confirm each retrieves the expected document.\n\n"
                        "2. Run `semantic_search(\"How do I repair my car?\")` with `threshold = 0.60`. "
                        "Report what is returned and whether the threshold behaved as expected.\n\n"
                        "3. Add two more documents to the knowledge base on a topic of your choice "
                        "(e.g. exam schedules, scholarships) and write a query for each that should "
                        "retrieve it. Adjust `top_k` and `threshold` if needed and explain any changes."
                    ),
                    "starter_code": (
                        "from sentence_transformers import SentenceTransformer\n"
                        "from sklearn.metrics.pairwise import cosine_similarity\n\n\n"
                        "documents = [\n"
                        "    \"Students must complete 160 credit hours to graduate.\",\n"
                        "    \"The minimum GPA required for graduation is 2.0.\",\n"
                        "    \"The cost of one credit hour is 1330 EGP.\",\n"
                        "    \"Students must register their courses before the registration deadline.\",\n"
                        "    \"The university library opens at 8 AM.\",\n"
                        "    # TODO: add 2 more documents on a topic of your choice\n"
                        "]\n\n"
                        "model = SentenceTransformer(\"sentence-transformers/all-MiniLM-L6-v2\")\n"
                        "document_embeddings = model.encode(documents)\n\n\n"
                        "def semantic_search(query, top_k=3, threshold=0.60):\n"
                        "    query_embedding = model.encode(query)\n"
                        "    scores = cosine_similarity([query_embedding], document_embeddings)[0]\n"
                        "    ranked_indices = scores.argsort()[::-1]\n\n"
                        "    results = []\n"
                        "    for index in ranked_indices:\n"
                        "        score = float(scores[index])\n"
                        "        if score < threshold:\n"
                        "            continue\n"
                        "        results.append({\"text\": documents[index], \"score\": score})\n"
                        "        if len(results) >= top_k:\n"
                        "            break\n\n"
                        "    return results\n\n\n"
                        "# TODO: run the example queries and the unrelated query, then report results\n"
                    ),
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["embeddings", "semantic-search", "similarity-thresholds", "top-k"],
                },
            ],
            "quiz": {
                "title": "Semantic Search Project — Knowledge Check",
                "questions": [
                    {
                        "question": "In the project's semantic_search() function, why is document_embeddings computed once outside the function rather than inside it?",
                        "options": [
                            "Because Sentence Transformers cannot be called more than once",
                            "Because document embeddings represent the indexing step and shouldn't be recomputed on every query — only the query needs a fresh embedding at search time",
                            "Because it has no effect on performance either way",
                            "Because cosine_similarity requires embeddings to be created outside functions",
                        ],
                        "correct": 1,
                        "explanation": "Document embeddings belong to the indexing stage and should be computed once; recomputing them on every search would be wasteful, especially at scale.",
                    },
                    {
                        "question": "In this project, what role does scikit-learn's cosine_similarity play, and what role does the vector database (Qdrant/FAISS) play in a production system?",
                        "options": [
                            "They are unrelated and solve completely different problems",
                            "cosine_similarity computes similarity directly in Python for a small dataset; a vector database provides an efficient way to do the same kind of comparison at scale",
                            "cosine_similarity replaces the need for an embedding model",
                            "Vector databases compute similarity while cosine_similarity stores vectors",
                        ],
                        "correct": 1,
                        "explanation": "The manual cosine_similarity calculation and a production vector database both perform similarity search — the vector database just does it far more efficiently at scale using indexing and (often) approximate nearest-neighbor techniques.",
                    },
                    {
                        "question": "If semantic_search('How do I repair my car?') returns no results with threshold=0.60, what does that demonstrate?",
                        "options": [
                            "That the embedding model is broken",
                            "That the threshold successfully filtered out results with insufficient similarity, since the knowledge base has no relevant content",
                            "That Top-K retrieval failed to work at all",
                            "That cosine similarity cannot handle unrelated queries",
                        ],
                        "correct": 1,
                        "explanation": "This is the threshold working as intended: since no document is genuinely about car repair, all similarity scores fall below the threshold and are correctly rejected.",
                    },
                    {
                        "question": "How does this project's pipeline connect to a full RAG system?",
                        "options": [
                            "It is identical to RAG; nothing else needs to be added",
                            "It implements the retrieval half of RAG (query → semantic search → relevant documents); RAG adds context construction and an LLM to generate a final answer",
                            "RAG doesn't use semantic search at all, so this project is unrelated",
                            "This project already includes an LLM step",
                        ],
                        "correct": 1,
                        "explanation": "The project stops at 'relevant documents.' A full RAG system takes those retrieved documents, builds a context, and passes it to an LLM to generate the final answer.",
                    },
                    {
                        "question": "Why did this lesson intentionally avoid using LangChain, Qdrant, or FAISS?",
                        "options": [
                            "Because those tools don't actually work for semantic search",
                            "To make sure the underlying mechanism (embed, compare, rank, filter) is understood directly, so those tools become recognizable wrappers around a known process rather than a black box",
                            "Because those tools are being deprecated",
                            "Because Sentence Transformers cannot be combined with vector databases",
                        ],
                        "correct": 1,
                        "explanation": "Building the pipeline manually first demystifies what higher-level tools like LangChain, Qdrant, and FAISS are actually doing internally.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": "University Semantic Search Engine",
                "description": (
                    "Build a small semantic search engine over a university knowledge base, "
                    "without using LangChain, Qdrant, or FAISS. Implement the full pipeline "
                    "yourself: embed documents once at indexing time, embed each incoming "
                    "query, rank documents by cosine similarity, and apply both a top_k limit "
                    "and a similarity threshold so unrelated queries correctly return no results."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "tech_stack": ["python", "sentence-transformers", "scikit-learn", "numpy"],
                "objectives": [
                    "Embed a small set of documents once using a Sentence Transformers model",
                    "Embed an incoming user query at search time",
                    "Rank documents by cosine similarity to the query",
                    "Apply top_k to limit the number of results returned",
                    "Apply a similarity threshold so low-relevance results are excluded",
                    "Demonstrate correct behavior on at least one clearly unrelated query",
                ],
                "rubric": {
                    "correct_ranking": "Retrieves the most semantically relevant document first for at least 3 distinct test queries",
                    "threshold_behavior": "An unrelated query (e.g. about car repair) returns no results given the configured threshold",
                    "top_k_behavior": "Never returns more than top_k results even when more documents exceed the threshold",
                    "code_clarity": "Indexing (document embedding) and querying (query embedding + search) are clearly separated, with documents embedded only once",
                },
                "starter_repo_url": None,
                "estimated_hours": 3.0,
            },
        },
        # Level 5 is now fully contiguous, orders 1-11 (Lessons 1-11 from
        # the source material), matching your progress summary's "10/15
        # topics" style layout — no more gaps.
    ],
}
