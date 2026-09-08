"""
backend/seeds/seed_tool_qdrant.py

Adds topic content (lessons/exercises/quiz/project) to the Qdrant
tool course, which already exists as a shell (seeded by
seeds/seed_tool_courses.py). Idempotent — safe to re-run.

Run from backend/:
    docker compose exec api python seeds/seed_tool_qdrant.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine, Base
import app.models.user, app.models.learning, app.models.progress    # noqa: F401
import app.models.community, app.models.wallet, app.models.auth_token  # noqa: F401
import app.models.challenge, app.models.exam                         # noqa: F401
from app.models.learning import Lesson, Exercise, Quiz, Project, DifficultyLevel
from app.models.tool_course import ToolCourse, ToolTopic

Base.metadata.create_all(bind=engine)

TOOL_SLUG = "qdrant"  # must already exist — created by seed_tool_courses.py

# ---------------------------------------------------------------------------
# Topics (flat — no levels). Add one dict per topic, in the order they
# should appear.
# ---------------------------------------------------------------------------
TOPICS = [
    {
        # ToolTopic fields
        "title":            "What is Qdrant?",
        "slug":              "what-is-qdrant",
        "description":       "Vectors, embeddings, and semantic similarity search — why Qdrant matters for RAG systems.",
        "order":             1,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["qdrant", "vector-database", "rag", "embeddings"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "What is Qdrant?",
            "content": r"""Imagine you have 100,000 documents.

You ask: "How do I register a course?"

A normal database might search for the exact words: "register", "course".
But what if the document says: "Students must complete the enrollment process before adding subjects."
The words are different, but the meaning is similar. This is where a vector database helps.

## 1. What is a vector?

An AI model can convert text into numbers. For example:

```
"How do I register a course?"
```

might become something like:

```
[0.12, -0.45, 0.87, 0.31, ...]
```

This list of numbers is called a vector or embedding.

The important idea: **similar meanings → similar vectors.**

```
"How do I register a course?"       → [0.12, -0.45, 0.87, ...]
"How can I enroll in a subject?"    → [0.14, -0.43, 0.85, ...]
```

Their vectors should be relatively close.

## 2. So what does Qdrant do?

Qdrant stores these vectors and lets you search for vectors that are similar.

```
                 Qdrant
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
    Vector 1     Vector 2     Vector 3
       │            │            │
    Document A   Document B   Document C
```

You give Qdrant a query vector, e.g. `[0.13, -0.44, 0.86, ...]`, and:

```
Query → Qdrant → Most similar vectors → Their documents
```

## 3. Qdrant in a RAG system

A typical RAG (Retrieval-Augmented Generation) system looks like:

```
User Question
    ↓
Embedding Model
    ↓
Query Vector
    ↓
Qdrant
    ↓
Similarity Search
    ↓
Relevant Documents
    ↓
LLM
    ↓
Answer
```

Example:

```
User: "What are the graduation requirements?"
    ↓ Embedding
    ↓ Qdrant searches thousands of document chunks
    ↓ Returns:
        Chunk 1: Graduation requirements...
        Chunk 2: Credit hour requirements...
        Chunk 3: GPA requirements...
    ↓ LLM uses those chunks to answer.
```

## 4. Qdrant vs normal database

**SQL database** is good for structured queries, e.g.:
- `Find students where GPA > 3.5`
- `Find course where code = "CSE251"`

**Qdrant** is good for semantic similarity, e.g.:
- `Find documents that are semantically similar to "How can I graduate?"`

So: SQL → structured data, Qdrant → vector similarity search. In real applications, you often use both together.

## 5. The 3 most important Qdrant concepts

Don't worry about everything yet — for now, remember only these three:

### ① Collection
A collection is like a table. It contains vectors. Example: `academic_documents`

### ② Point
A point is one stored item. It contains a **Vector** + a **Payload**. For example:

```
Vector: [0.12, -0.45, 0.87, ...]
Payload: {
    "text": "Students must complete...",
    "course": "CSE251"
}
```

### ③ Search
You give Qdrant a `query_vector`, and it returns the most similar points, ranked by similarity:

```
Point 1 → 0.92 similarity
Point 2 → 0.87 similarity
Point 3 → 0.81 similarity
```

Higher similarity generally means more relevant.

## 🧩 The mental model

```
Collection
   │
   ├── Point
   │     ├── Vector
   │     └── Payload
   │
   ├── Point
   │     ├── Vector
   │     └── Payload
   │
   └── Point
         ├── Vector
         └── Payload
```

That's enough for Lesson 1.
""",
            "order":                1,
            "estimated_minutes":    25,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Design a Collection Payload",
                "description":   "You're building a RAG system over a university's academic documents (course descriptions, enrollment policies, graduation requirements). Design the payload structure for a single Point that would be stored in a Qdrant collection called `academic_documents`. Your payload should let a downstream system filter results (e.g. by course code or document type) in addition to the semantic vector search.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  "point = {\n    \"vector\": [0.12, -0.45, 0.87],  # pretend embedding\n    \"payload\": {\n        # TODO: add fields that describe this document chunk\n        # (e.g. text, course code, document type, source)\n    }\n}\n",
                "solution_code": "point = {\n    \"vector\": [0.12, -0.45, 0.87],  # pretend embedding\n    \"payload\": {\n        \"text\": \"Students must complete the enrollment process before adding subjects.\",\n        \"course\": \"CSE251\",\n        \"doc_type\": \"enrollment_policy\",\n        \"source\": \"student_handbook_2025.pdf\",\n        \"chunk_id\": 14\n    }\n}\n",
                "skill_tested":  ["qdrant", "payload-design", "rag"],
            },
        ],
        "quiz": {
            "title":         "What is Qdrant? Quiz",
            "questions": [
                {
                    "question": "What is a vector (embedding) in the context of Qdrant?",
                    "options": [
                        "A list of numbers that represents the meaning of a piece of text",
                        "A row in a SQL table",
                        "A type of database index for exact keyword matches",
                        "A compressed version of a document's raw text"
                    ],
                    "correct": 0,
                    "explanation": "A vector (or embedding) is a list of numbers produced by an AI model that captures the meaning of text — similar meanings produce similar vectors."
                },
                {
                    "question": "What does Qdrant primarily store and search over?",
                    "options": [
                        "Rows with exact string matches",
                        "Vectors (with associated payloads), searchable by similarity",
                        "Only raw text documents",
                        "SQL tables with foreign keys"
                    ],
                    "correct": 1,
                    "explanation": "Qdrant stores vectors, each attached to a payload, and lets you search for the vectors most similar to a given query vector."
                },
                {
                    "question": "In Qdrant, what is a 'Collection'?",
                    "options": [
                        "A single stored vector",
                        "The similarity score between two vectors",
                        "A group of points — conceptually similar to a table in a SQL database",
                        "The embedding model itself"
                    ],
                    "correct": 2,
                    "explanation": "A Collection is like a table — it holds a set of Points (vectors + payloads)."
                },
                {
                    "question": "What is the difference between a Point's vector and its payload?",
                    "options": [
                        "There is no difference, they are the same thing",
                        "The vector is the numeric embedding used for similarity search; the payload is the metadata/original content stored alongside it (e.g. text, course code)",
                        "The payload is used for similarity search; the vector is just metadata",
                        "The vector is optional but the payload is required"
                    ],
                    "correct": 1,
                    "explanation": "The vector is what Qdrant compares during similarity search, while the payload carries the human-readable data (text, tags, IDs, etc.) that gets returned alongside a match."
                },
                {
                    "question": "When would you prefer a SQL database over Qdrant?",
                    "options": [
                        "When you need to find documents that are semantically similar to a question",
                        "When you need exact structured queries, like 'find students where GPA > 3.5'",
                        "When you need to store embeddings",
                        "Never — Qdrant always replaces SQL"
                    ],
                    "correct": 1,
                    "explanation": "SQL databases excel at structured, exact-match queries. Qdrant excels at semantic similarity search. Real applications often use both."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Vectors & Embeddings",
        "slug":              "vectors-and-embeddings",
        "description":       "How text becomes vectors, why embedding dimensions matter, and generating embeddings with Sentence Transformers.",
        "order":             2,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["qdrant", "embeddings", "sentence-transformers", "vector-database"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Vectors & Embeddings",
            "content": r"""This lesson is very important because Qdrant works with vectors. Don't worry—we'll make it simple.

## 1. What is an embedding?

An embedding is a way to convert text into numbers. For example:

```
"machine learning"
    ↓
Embedding Model
    ↓
[0.21, -0.45, 0.73, 0.11, ...]
```

That list of numbers is a vector.

So: **Embedding = the process/result of converting data into a vector that represents its meaning.**

## 2. Why convert text to numbers?

Computers don't understand the meaning of text directly, but they can compare numbers.

Suppose we have:

```
A = "How do I register a course?"
B = "How can I enroll in a subject?"
C = "What is the weather today?"
```

An embedding model might produce:

```
A → [0.12, 0.45, 0.81, ...]
B → [0.15, 0.43, 0.79, ...]
C → [-0.72, 0.11, -0.32, ...]
```

A and B have similar meanings, so their vectors should be relatively close.

## 3. Similarity

Qdrant uses vector similarity to find relevant information.

```
       A
      ●
     /
    /
   ● B
                    ● C
```

A and B are close. C is far away. Therefore:

```
A ↔ B = similar
A ↔ C = not very similar
```

This is the basic idea behind semantic search.

## 4. Embedding dimensions

A vector isn't necessarily just 3 numbers. An embedding model might produce a vector with hundreds of dimensions, e.g.:

```
384 dimensions
768 dimensions
1024 dimensions
1536 dimensions
```

The exact dimension depends on the embedding model.

### Important Qdrant rule

**The vector size in your Qdrant collection must match the embedding model.**

```
Embedding model
    ↓
384 dimensions
    ↓
Qdrant collection
    ↓
vector size = 384
```

You cannot create the collection with `size = 768` and then insert `384-dimensional vectors`. They must match.

## 5. Let's use a real embedding model

We'll use Sentence Transformers because it's easy to understand.

Install:

```bash
pip install sentence-transformers
```

Then:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

Now create an embedding:

```python
text = "How do I register a course?"
vector = model.encode(text)
print(vector)
```

You'll get something similar to:

```
[ 0.021, -0.083, 0.142, ... ]
```

## 6. Check the vector size

```python
print(len(vector))
```

For this model, you'll get:

```
384
```

So: `all-MiniLM-L6-v2` → 384-dimensional vector. Remember this because we'll need it when creating our Qdrant collection.

## 7. Multiple documents

Suppose we have:

```python
documents = [
    "How do I register a course?",
    "Students must complete registration before adding subjects.",
    "The university library is open from 9 AM to 5 PM."
]
```

We can create embeddings:

```python
vectors = model.encode(documents)
```

Now:

```
Document 1 → Vector 1
Document 2 → Vector 2
Document 3 → Vector 3
```

These vectors can then be stored in Qdrant.

## 8. The complete picture

```
Text
 ↓
Embedding Model
 ↓
Vector
 ↓
Qdrant
```

And when searching:

```
User Question
 ↓
Embedding Model
 ↓
Query Vector
 ↓
Qdrant
 ↓
Similar Vectors
 ↓
Relevant Text
```

## 🧠 Very important distinction

Don't confuse these:

**Embedding model** — creates vectors: `Text → Vector`

**Qdrant** — stores and searches vectors: `Vector → Store/Search`

```
Sentence Transformer
    ↓
   creates vector
    ↓
      Qdrant
        ↓
stores/searches vector
```
""",
            "order":                2,
            "estimated_minutes":    30,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Check the Embedding Dimension",
                "description":   "Use Sentence Transformers to embed a sentence with the `all-MiniLM-L6-v2` model, then print the vector's length. Confirm it matches the dimension you'd need to configure for a Qdrant collection storing these embeddings.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  "from sentence_transformers import SentenceTransformer\n\nmodel = SentenceTransformer(\"all-MiniLM-L6-v2\")\ntext = \"I want to enroll in a course\"\nvector = model.encode(text)\n\n# TODO: print the length of the vector\n",
                "solution_code": "from sentence_transformers import SentenceTransformer\n\nmodel = SentenceTransformer(\"all-MiniLM-L6-v2\")\ntext = \"I want to enroll in a course\"\nvector = model.encode(text)\n\nprint(len(vector))  # 384 — this model produces 384-dimensional vectors\n",
                "skill_tested":  ["embeddings", "sentence-transformers"],
            },
        ],
        "quiz": {
            "title":         "Vectors & Embeddings Quiz",
            "questions": [
                {
                    "question": "What is an embedding?",
                    "options": [
                        "A SQL query that filters exact text matches",
                        "The process/result of converting data into a vector that represents its meaning",
                        "A compressed image format",
                        "A type of Qdrant collection"
                    ],
                    "correct": 1,
                    "explanation": "An embedding converts text (or other data) into a numeric vector that captures its meaning, so texts with similar meaning end up with similar vectors."
                },
                {
                    "question": "Why do we convert text into numbers before storing it in Qdrant?",
                    "options": [
                        "Because computers can compare numbers to determine similarity, but can't compare raw text meaning directly",
                        "To save disk space",
                        "Because Qdrant only accepts JSON",
                        "To encrypt the text"
                    ],
                    "correct": 0,
                    "explanation": "Computers can't directly grasp the meaning of text, but they can compare numeric vectors, which is what makes semantic search possible."
                },
                {
                    "question": "The all-MiniLM-L6-v2 Sentence Transformer model produces vectors of what dimension?",
                    "options": [
                        "128",
                        "384",
                        "768",
                        "1536"
                    ],
                    "correct": 1,
                    "explanation": "all-MiniLM-L6-v2 produces 384-dimensional vectors — this is confirmed by calling len(vector) on its output."
                },
                {
                    "question": "What must be true about the vector size when creating a Qdrant collection?",
                    "options": [
                        "It can be any size regardless of the embedding model",
                        "It must match the dimension produced by the embedding model you plan to use",
                        "It must always be 1536",
                        "It is auto-detected from the first inserted vector and can change later"
                    ],
                    "correct": 1,
                    "explanation": "The vector size configured in the Qdrant collection must match the embedding model's output dimension — you can't mix a 384-dim model with a 768-dim collection."
                },
                {
                    "question": "In the pipeline 'Text → Embedding Model → Vector → Qdrant', what is Qdrant's role?",
                    "options": [
                        "It creates the embeddings from raw text",
                        "It stores and searches the vectors that were already created by the embedding model",
                        "It trains the embedding model",
                        "It converts vectors back into the original text"
                    ],
                    "correct": 1,
                    "explanation": "The embedding model's job is to create vectors from text; Qdrant's job is to store those vectors and search them for similarity. These are two distinct roles."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Install Qdrant",
        "slug":              "install-qdrant",
        "description":       "Install the Qdrant Python client, run Qdrant in local in-memory mode, and create your first collection.",
        "order":             3,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["qdrant", "python", "setup", "vector-database"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Install Qdrant",
            "content": r"""Now we're going to actually run Qdrant and connect to it using Python. Don't worry about Docker or complicated configuration yet — we'll start with the easiest method.

## 1. Install the Python client

Run:

```bash
pip install qdrant-client
```

Then test it:

```python
from qdrant_client import QdrantClient
print("Qdrant installed!")
```

If you see `Qdrant installed!` you're ready. ✅

## 2. Run Qdrant locally

The easiest way for learning is to use Qdrant's local/in-memory mode.

```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
```

Think of `client` as your connection to Qdrant.

```
Python
   │
   ▼
QdrantClient
   │
   ▼
Qdrant
```

## 3. Why `:memory:`?

When we write `QdrantClient(":memory:")`, Qdrant runs inside your Python process. It's excellent for learning because:

- No Docker
- No server setup
- No configuration
- Very fast
- Perfect for experiments

⚠️ But the data disappears when the Python program stops. Later we'll learn how to run a persistent Qdrant database.

## 4. Create your first collection

Remember from Lesson 1: a collection is like a table that stores vectors. Let's create one.

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="my_documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
```

Congratulations! 🎉 You've created your first Qdrant collection.

## 5. What does this code mean?

**Collection name** — `collection_name="my_documents"`. You can name it whatever you want, e.g. `courses`, `documents`, `products`, `articles`.

**Vector size** — `size=384`. Remember Lesson 2? We used `all-MiniLM-L6-v2`, which produces 384 dimensions. Therefore: Embedding size = 384 → Qdrant vector size = 384. They must match.

## 6. What is `Distance.COSINE`?

This tells Qdrant how to compare vectors. `Distance.COSINE` means: compare vectors based on their cosine similarity. For semantic search, cosine similarity is very commonly used.

You may also encounter `Distance.EUCLID` and `Distance.DOT` — don't worry about those yet. For now: COSINE = 👍

## 7. Check your collection

You can see your collections:

```python
collections = client.get_collections()
print(collections)
```

You'll see something similar to:

```
collections=[
    CollectionDescription(name='my_documents')
]
```

## 8. Complete example

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Create Qdrant client
client = QdrantClient(":memory:")

# Create collection
client.create_collection(
    collection_name="my_documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

# Show collections
print(client.get_collections())
```

## 🧠 Understand the architecture

Right now we have:

```
                    Qdrant
                      │
              ┌───────┴───────┐
              │               │
          Collection      Collection
              │
        my_documents
              │
           Vectors
```

Later we'll put actual vectors inside it.

## ⚠️ One important thing

You might see tutorials using:

```python
QdrantClient("http://localhost:6333")
```

That's different — it means connecting to a running Qdrant Server at `localhost:6333`. We'll learn that later. For now, `QdrantClient(":memory:")` is much easier.
""",
            "order":                3,
            "estimated_minutes":    25,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Create Your First Collection",
                "description":   "Connect to an in-memory Qdrant instance, confirm it starts with no collections, then create a collection named `test` with the right vector size and distance metric for an all-MiniLM-L6-v2 embedding model. Confirm it now appears in the collection list.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  "from qdrant_client import QdrantClient\nfrom qdrant_client.models import Distance, VectorParams\n\nclient = QdrantClient(\":memory:\")\nprint(client.get_collections())  # expect: no collections yet\n\n# TODO: create a collection named \"test\" sized for all-MiniLM-L6-v2 embeddings\n# using cosine distance\n\nprint(client.get_collections())  # expect: \"test\" now listed\n",
                "solution_code": "from qdrant_client import QdrantClient\nfrom qdrant_client.models import Distance, VectorParams\n\nclient = QdrantClient(\":memory:\")\nprint(client.get_collections())  # no collections yet\n\nclient.create_collection(\n    collection_name=\"test\",\n    vectors_config=VectorParams(\n        size=384,\n        distance=Distance.COSINE\n    )\n)\n\nprint(client.get_collections())  # collections=[CollectionDescription(name='test')]\n",
                "skill_tested":  ["qdrant", "qdrant-client", "collections"],
            },
        ],
        "quiz": {
            "title":         "Install Qdrant Quiz",
            "questions": [
                {
                    "question": "Which package do you install to connect to Qdrant from Python?",
                    "options": [
                        "sentence-transformers",
                        "qdrant-client",
                        "vector-db",
                        "pyqdrant"
                    ],
                    "correct": 1,
                    "explanation": "`pip install qdrant-client` installs the official Python client used to connect to and interact with Qdrant."
                },
                {
                    "question": "What does `QdrantClient(\":memory:\")` do?",
                    "options": [
                        "Connects to a remote Qdrant server on the cloud",
                        "Runs Qdrant inside your Python process with no persistence — great for learning and experiments",
                        "Deletes all existing collections",
                        "Encrypts stored vectors in memory"
                    ],
                    "correct": 1,
                    "explanation": "The `:memory:` mode runs Qdrant in-process with no Docker or server setup required, but the data disappears once the Python program stops."
                },
                {
                    "question": "When creating a collection with `size=384`, what determines this number?",
                    "options": [
                        "It's arbitrary and can be any number",
                        "It must match the output dimension of the embedding model you plan to use, e.g. all-MiniLM-L6-v2",
                        "It's always fixed at 384 for every Qdrant collection",
                        "It represents the number of documents you plan to store"
                    ],
                    "correct": 1,
                    "explanation": "The vector size must match the embedding model's dimension — all-MiniLM-L6-v2 produces 384-dimensional vectors, so the collection is configured with size=384."
                },
                {
                    "question": "What does `Distance.COSINE` configure in a Qdrant collection?",
                    "options": [
                        "How Qdrant compresses vectors on disk",
                        "The metric Qdrant uses to compare vector similarity",
                        "The maximum number of vectors allowed",
                        "The embedding model used to generate vectors"
                    ],
                    "correct": 1,
                    "explanation": "The distance metric (COSINE, EUCLID, or DOT) tells Qdrant how to measure similarity between vectors. Cosine similarity is the common default for semantic search."
                },
                {
                    "question": "What's the difference between `QdrantClient(\":memory:\")` and `QdrantClient(\"http://localhost:6333\")`?",
                    "options": [
                        "There is no difference",
                        "`:memory:` runs Qdrant in-process with no persistence; `localhost:6333` connects to a separately running Qdrant server",
                        "`:memory:` is for production; `localhost:6333` is only for testing",
                        "`localhost:6333` is used only for embeddings, not vector storage"
                    ],
                    "correct": 1,
                    "explanation": "`:memory:` mode embeds Qdrant directly in your Python process (non-persistent), while connecting to `localhost:6333` talks to an actual running Qdrant server instance."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Points",
        "slug":              "points",
        "description":       "Store data in Qdrant using Points — ID, vector, and payload — and insert them with upsert.",
        "order":             4,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["qdrant", "points", "python", "vector-database"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Points",
            "content": r"""Now we're going to put actual data inside Qdrant. The most important concept in this lesson is the **Point**.

## 1. What is a Point?

In Qdrant, a Point is one stored item. A point contains:

```
Point
├── ID
├── Vector
└── Payload
```

Think of it like this:

```
ID       → Who is this?
Vector   → What does it mean?
Payload  → What information belongs to it?
```

## 2. Example

Suppose we have: `"Machine learning is a branch of AI."`

We create an embedding: `[0.12, -0.44, 0.73, ...]`

Then store it in Qdrant:

```
Point
├── ID: 1
├── Vector: [0.12, -0.44, 0.73, ...]
└── Payload:
      text: "Machine learning is a branch of AI."
```

## 3. Create a collection

Let's start from scratch:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
```

Now we have: `Qdrant → documents`

## 4. Create a Point

Qdrant uses `PointStruct`.

```python
from qdrant_client.models import PointStruct

point = PointStruct(
    id=1,
    vector=[0.1] * 384,
    payload={
        "text": "Machine learning is a branch of AI."
    }
)
```

Notice: `vector=[0.1] * 384` creates `[0.1, 0.1, 0.1, 0.1, ...]` with 384 numbers. We're using a fake vector for now — later we'll use a real embedding model.

## 5. Insert the Point

```python
client.upsert(
    collection_name="documents",
    points=[point]
)
```

`upsert` basically means: **insert this point, or update it if the ID already exists.**

## 6. What did we just do?

We went from: `Python → Point → Qdrant`, and Qdrant now contains:

```
documents
  Point 1
  ├── ID
  ├── Vector
  └── Payload
```

🎉 You just stored your first point.

## 7. Why do we need Payload?

The vector contains numbers like `[0.1, 0.2, -0.4, ...]` — humans can't read that. So we store the original information in the payload.

```python
payload={
    "text": "Machine learning is a branch of AI.",
    "course": "AI",
    "chapter": 1
}
```

Now the point looks like:

```
Point
├── ID: 1
├── Vector
│   └── [0.1, 0.2, -0.4, ...]
└── Payload
    ├── text: "Machine learning..."
    ├── course: "AI"
    └── chapter: 1
```

This is extremely useful for RAG.

## 8. Store multiple points

```python
points = [
    PointStruct(
        id=1,
        vector=[0.1] * 384,
        payload={"text": "Machine learning is a branch of AI."}
    ),
    PointStruct(
        id=2,
        vector=[0.2] * 384,
        payload={"text": "Deep learning uses neural networks."}
    ),
    PointStruct(
        id=3,
        vector=[0.3] * 384,
        payload={"text": "Python is widely used in AI."}
    )
]

client.upsert(
    collection_name="documents",
    points=points
)
```

Now:

```
Qdrant
└── documents
     ├── Point 1
     ├── Point 2
     └── Point 3
```

## 9. Important: IDs

Every point needs an ID, e.g. `id=1`, `id=2`, `id=3`. You can also use UUIDs — for now, simple integers are easier.

## 10. The RAG connection

Imagine your university document contains:

```
Chunk 1
"Students must complete 140 credit hours..."
```

We create: `Chunk → Embedding → Vector`, then store:

```
Point
├── ID: 1
├── Vector: embedding
└── Payload:
      text: "Students must complete 140 credit hours..."
```

So Qdrant becomes:

```
                Qdrant
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      Point 1    Point 2    Point 3
        │          │          │
      Chunk 1    Chunk 2    Chunk 3
```

That's the foundation of a Qdrant-powered RAG system.

## 🧪 Complete example

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. Create client
client = QdrantClient(":memory:")

# 2. Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

# 3. Create points
points = [
    PointStruct(
        id=1,
        vector=[0.1] * 384,
        payload={"text": "Machine learning is a branch of AI."}
    ),
    PointStruct(
        id=2,
        vector=[0.2] * 384,
        payload={"text": "Deep learning uses neural networks."}
    )
]

# 4. Insert points
client.upsert(
    collection_name="documents",
    points=points
)

print("Points inserted!")
```

## 🧠 Remember this

The most important Qdrant structure is:

```
Collection
   ↓
Points
   ↓
┌───────────────┐
│ ID            │
│ Vector        │
│ Payload       │
└───────────────┘
```

And for RAG:

```
Document → Chunk → Embedding → Vector → Point → Qdrant
```
""",
            "order":                4,
            "estimated_minutes":    30,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Build and Insert Multiple Points",
                "description":   "Create a Qdrant collection called `courses` (384-dim, cosine distance). Then build three PointStructs — using fake vectors like `[0.1] * 384` — for three course descriptions of your choice, each with a payload containing `text` and a `course_code` field. Upsert all three points into the collection.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  "from qdrant_client import QdrantClient\nfrom qdrant_client.models import Distance, VectorParams, PointStruct\n\nclient = QdrantClient(\":memory:\")\n\n# TODO: create a \"courses\" collection (size=384, cosine distance)\n\n# TODO: build 3 PointStructs with fake vectors and payloads containing\n# \"text\" and \"course_code\"\n\n# TODO: upsert the points into the collection\n",
                "solution_code": "from qdrant_client import QdrantClient\nfrom qdrant_client.models import Distance, VectorParams, PointStruct\n\nclient = QdrantClient(\":memory:\")\n\nclient.create_collection(\n    collection_name=\"courses\",\n    vectors_config=VectorParams(size=384, distance=Distance.COSINE)\n)\n\npoints = [\n    PointStruct(\n        id=1,\n        vector=[0.1] * 384,\n        payload={\"text\": \"Intro to programming with Python.\", \"course_code\": \"CSE101\"}\n    ),\n    PointStruct(\n        id=2,\n        vector=[0.2] * 384,\n        payload={\"text\": \"Data structures and algorithms.\", \"course_code\": \"CSE201\"}\n    ),\n    PointStruct(\n        id=3,\n        vector=[0.3] * 384,\n        payload={\"text\": \"Introduction to machine learning.\", \"course_code\": \"CSE310\"}\n    ),\n]\n\nclient.upsert(collection_name=\"courses\", points=points)\nprint(\"Points inserted!\")\n",
                "skill_tested":  ["qdrant", "points", "upsert"],
            },
        ],
        "quiz": {
            "title":         "Points Quiz",
            "questions": [
                {
                    "question": "What are the three main components of a Qdrant Point?",
                    "options": [
                        "Collection, Distance, Payload",
                        "ID, Vector, Payload",
                        "ID, Collection, Distance",
                        "Vector, Distance, Client"
                    ],
                    "correct": 1,
                    "explanation": "A Point is made up of an ID (identifier), a Vector (the embedding), and a Payload (the original/metadata information)."
                },
                {
                    "question": "What does `client.upsert()` do?",
                    "options": [
                        "Deletes a point by ID",
                        "Only inserts new points, and errors if the ID already exists",
                        "Inserts a point, or updates it if the ID already exists",
                        "Creates a new collection"
                    ],
                    "correct": 2,
                    "explanation": "Upsert inserts a new point, or updates the existing point if one with that ID is already stored."
                },
                {
                    "question": "Why do we store a payload alongside the vector in a Point?",
                    "options": [
                        "Because Qdrant requires payloads to run similarity search",
                        "Because vectors are just numbers — the payload holds the human-readable original text/metadata",
                        "To make the vector smaller",
                        "Payloads are optional and rarely used in practice"
                    ],
                    "correct": 1,
                    "explanation": "Vectors are lists of numbers that aren't human-readable. The payload stores the original text and any metadata so it can be retrieved alongside search results."
                },
                {
                    "question": "In `PointStruct(id=5, vector=[0.3]*384, payload={\"text\": \"Qdrant is a vector database.\"})`, what does `id=5` represent?",
                    "options": [
                        "The similarity score of the point",
                        "The dimension of the vector",
                        "The unique identifier for this point",
                        "The collection name"
                    ],
                    "correct": 2,
                    "explanation": "Every point needs a unique ID (an integer or UUID) so it can be referenced, retrieved, or updated later."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Insert Real Embeddings",
        "slug":              "insert-real-embeddings",
        "description":       "Replace fake vectors with real Sentence Transformer embeddings and insert them into Qdrant as Points.",
        "order":             5,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["qdrant", "sentence-transformers", "embeddings", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Insert Real Embeddings",
            "content": r"""So far we used fake vectors like `[0.1] * 384`. Now we're going to do the real thing:

```
Text → Embedding Model → Real Vector → Qdrant
```

## 1. Install Sentence Transformers

If you haven't already:

```bash
pip install sentence-transformers
```

Then:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

Remember: `all-MiniLM-L6-v2` → 384 dimensions.

## 2. Create some documents

```python
documents = [
    "Machine learning is a branch of artificial intelligence.",
    "Deep learning uses neural networks to learn patterns.",
    "Python is a popular programming language for AI."
]
```

## 3. Create embeddings

```python
vectors = model.encode(documents)

print(len(vectors))     # 3 — because we have 3 documents
print(len(vectors[0]))  # 384 — each vector has 384 numbers
```

So: 3 documents → 3 vectors → each vector has 384 numbers.

## 4. Create Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
```

## 5. Convert vectors into Points

```python
from qdrant_client.models import PointStruct

points = []

for i, (document, vector) in enumerate(zip(documents, vectors)):
    point = PointStruct(
        id=i,
        vector=vector.tolist(),
        payload={
            "text": document
        }
    )
    points.append(point)
```

Now we have three Points, each with an ID, a real embedding, and the original text.

## 6. Insert them into Qdrant

```python
client.upsert(
    collection_name="documents",
    points=points
)
```

Done! 🎉 Our real embeddings are now inside Qdrant.

## 7. Let's verify the data

We can retrieve points using:

```python
result = client.retrieve(
    collection_name="documents",
    ids=[0, 1, 2]
)

print(result)
```

You'll see the stored points, with payloads like `"Machine learning is a branch of artificial intelligence."`

## 8. Why is this better than our previous example?

Previously, `vector=[0.1] * 384` was just fake data. Now, `vector=model.encode(document)` creates a vector that represents the *meaning* of the document. That's what makes semantic search possible.

## 9. Complete example

```python
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Documents
documents = [
    "Machine learning is a branch of artificial intelligence.",
    "Deep learning uses neural networks to learn patterns.",
    "Python is a popular programming language for AI."
]

# 3. Create embeddings
vectors = model.encode(documents)

# 4. Create Qdrant client
client = QdrantClient(":memory:")

# 5. Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

# 6. Create points
points = []
for i, (document, vector) in enumerate(zip(documents, vectors)):
    points.append(
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={"text": document}
        )
    )

# 7. Insert points
client.upsert(
    collection_name="documents",
    points=points
)

print("Documents inserted successfully!")
```

## 🧠 The important pipeline

```
                 DOCUMENT
                    │
                    ▼
            Embedding Model
                    │
                    ▼
                 VECTOR
                    │
                    ▼
                 POINT
              ┌─────┴─────┐
              │           │
           Vector       Payload
              │           │
              └─────┬─────┘
                    ▼
                 QDRANT
```

## 🔥 One important distinction

There are two different operations here.

**Insert:** `Document → Embedding → Qdrant`

**Search:** `Question → Embedding → Qdrant → Similar Documents`

We've now learned the first one.
""",
            "order":                5,
            "estimated_minutes":    30,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Embed and Insert Real Documents",
                "description":   "Using Sentence Transformers, embed a list of at least 4 short documents about a topic of your choice, create a Qdrant collection sized for the model's output dimension, convert the embeddings into PointStructs (with the original text in the payload), upsert them, and retrieve them back by ID to confirm they were stored correctly.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  "from sentence_transformers import SentenceTransformer\nfrom qdrant_client import QdrantClient\nfrom qdrant_client.models import Distance, VectorParams, PointStruct\n\nmodel = SentenceTransformer(\"all-MiniLM-L6-v2\")\n\ndocuments = [\n    # TODO: add at least 4 short documents\n]\n\n# TODO: create embeddings, a Qdrant collection, PointStructs, upsert, then retrieve\n",
                "solution_code": "from sentence_transformers import SentenceTransformer\nfrom qdrant_client import QdrantClient\nfrom qdrant_client.models import Distance, VectorParams, PointStruct\n\nmodel = SentenceTransformer(\"all-MiniLM-L6-v2\")\n\ndocuments = [\n    \"Students must complete 140 credit hours to graduate.\",\n    \"The registration period opens two weeks before the semester.\",\n    \"A minimum GPA of 2.0 is required to remain enrolled.\",\n    \"Course withdrawals must be submitted before the deadline.\",\n]\n\nvectors = model.encode(documents)\n\nclient = QdrantClient(\":memory:\")\nclient.create_collection(\n    collection_name=\"documents\",\n    vectors_config=VectorParams(size=384, distance=Distance.COSINE)\n)\n\npoints = [\n    PointStruct(id=i, vector=vector.tolist(), payload={\"text\": document})\n    for i, (document, vector) in enumerate(zip(documents, vectors))\n]\n\nclient.upsert(collection_name=\"documents\", points=points)\n\nresult = client.retrieve(collection_name=\"documents\", ids=[0, 1, 2, 3])\nprint(result)\n",
                "skill_tested":  ["qdrant", "sentence-transformers", "embeddings", "points"],
            },
        ],
        "quiz": {
            "title":         "Insert Real Embeddings Quiz",
            "questions": [
                {
                    "question": "What does `model.encode(documents)` return when `documents` is a list of 3 strings?",
                    "options": [
                        "A single 384-dimensional vector representing all 3 documents combined",
                        "3 vectors, one per document, each 384-dimensional (for all-MiniLM-L6-v2)",
                        "A single number representing similarity",
                        "A Qdrant collection"
                    ],
                    "correct": 1,
                    "explanation": "Encoding a list of documents returns one vector per document — for all-MiniLM-L6-v2, each vector has 384 dimensions."
                },
                {
                    "question": "Why is `vector.tolist()` used when building a PointStruct from a Sentence Transformer embedding?",
                    "options": [
                        "To reduce the vector's dimensions",
                        "Sentence Transformers returns NumPy arrays, and PointStruct expects a plain Python list",
                        "It's optional and has no effect",
                        "To convert the vector into a payload"
                    ],
                    "correct": 1,
                    "explanation": "model.encode() returns NumPy arrays; PointStruct's vector field expects a plain Python list, so .tolist() converts it."
                },
                {
                    "question": "What is the key difference between a fake vector like `[0.1] * 384` and a real embedding from a model?",
                    "options": [
                        "There is no real difference",
                        "The real embedding represents the actual meaning of the text, enabling meaningful semantic search; the fake vector does not",
                        "Fake vectors are faster to search",
                        "Real embeddings must always be integers"
                    ],
                    "correct": 1,
                    "explanation": "A real embedding captures the semantic meaning of the text, so similarity search actually reflects meaning. A fake, constant vector carries no real semantic information."
                },
                {
                    "question": "What does `client.retrieve(collection_name=\"documents\", ids=[0, 1, 2])` do?",
                    "options": [
                        "Performs a similarity search using a query vector",
                        "Fetches the stored points with those specific IDs, including their vectors and payloads",
                        "Deletes the points with those IDs",
                        "Creates new points with those IDs"
                    ],
                    "correct": 1,
                    "explanation": "retrieve() fetches points directly by their IDs, letting you verify what was actually stored (vector and payload)."
                },
                {
                    "question": "Which pipeline correctly describes the 'Insert' operation covered in this lesson?",
                    "options": [
                        "Question → Embedding → Qdrant → Similar Documents",
                        "Document → Embedding → Qdrant",
                        "Qdrant → Embedding → Document",
                        "Vector → Payload → Question"
                    ],
                    "correct": 1,
                    "explanation": "Insert takes a document, embeds it into a vector, and stores it in Qdrant. Search (covered in a later lesson) goes the other direction: Question → Embedding → Qdrant → Similar Documents."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Similarity Search",
        "slug":              "similarity-search",
        "description":       "Search Qdrant by meaning — embed a query, run query_points(), and understand similarity scores.",
        "order":             6,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["qdrant", "semantic-search", "python", "rag"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Similarity Search",
            "content": r"""This is the most important lesson so far.

We already know how to go: `Document → Embedding → Vector → Qdrant`. Now we'll do the reverse:

```
Question → Embedding → Query Vector → Qdrant → Similar Documents
```

## 1. Our documents

We'll use the same documents:

```python
documents = [
    "Machine learning is a branch of artificial intelligence.",
    "Deep learning uses neural networks to learn patterns.",
    "Python is a popular programming language for AI."
]
```

They are already stored in Qdrant.

## 2. User asks a question

Suppose the user asks: `"What is deep learning?"`

We need to convert this question into a vector.

```python
query = "What is deep learning?"
query_vector = model.encode(query)
```

Now: `"What is deep learning?" → Embedding Model → Query Vector`

## 3. Search Qdrant

Now we give the vector to Qdrant. With current qdrant-client versions, use the `query_points()` API:

```python
results = client.query_points(
    collection_name="documents",
    query=query_vector.tolist(),
    limit=2
)
```

`limit=2` means: give me the 2 most similar points.

## 4. See the results

```python
for result in results.points:
    print(result.score)
    print(result.payload)
```

You might get something conceptually like:

```
0.82
{'text': 'Deep learning uses neural networks to learn patterns.'}

0.51
{'text': 'Machine learning is a branch of artificial intelligence.'}
```

The exact scores can vary by model/version. The important part is: a more similar document gets a higher score.

## 5. What is the score?

Remember our collection uses `distance=Distance.COSINE`. So Qdrant calculates cosine similarity between the Query Vector and each Document Vector. Higher similarity means more relevant.

For example:

```
Document A → 0.90
Document B → 0.72
Document C → 0.31
```

The ranking is: A > B > C

## 6. The complete search

```python
query = "What is deep learning?"
query_vector = model.encode(query)

results = client.query_points(
    collection_name="documents",
    query=query_vector.tolist(),
    limit=2
)

for result in results.points:
    print("Score:", result.score)
    print("Text:", result.payload["text"])
    print()
```

You'll get something similar to:

```
Score: 0.8...
Text: Deep learning uses neural networks to learn patterns.

Score: 0.5...
Text: Machine learning is a branch of artificial intelligence.
```

## 7. Why is this powerful?

The question was `"What is deep learning?"`. The document says `"Deep learning uses neural networks to learn patterns."` They don't need to be exact matches — Qdrant is comparing their vectors. That's called **Semantic Search**.

Instead of asking "Do these texts contain the same words?", we're asking "Do these texts have similar meanings?"

## 8. Another example

Try: `query = "What programming language is useful for artificial intelligence?"`

Qdrant should find: `"Python is a popular programming language for AI."` — even though the wording is different. That's the power of embeddings + vector search.

## 9. Qdrant is NOT creating the embeddings

This is very important. Qdrant doesn't do `Text → Embedding` — your embedding model does that. Qdrant does: `Vector → Store → Search → Return similar vectors`

So the architecture is:

```
                 User Question
                       │
                       ▼
               Embedding Model
                       │
                       ▼
                  Query Vector
                       │
                       ▼
                    Qdrant
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
           Point     Point     Point
             │
             ▼
       Relevant Payload
```

## 10. This is exactly what RAG needs

Suppose we have a university document split into chunks about credit hours, GPA requirements, and registration. We embed and store all chunks. Then the user asks: `"What are the graduation requirements?"`

```
Question → Embedding → Qdrant → Top 3 relevant chunks → LLM → Answer
```

This is the retrieval part of RAG.

## 🧪 Try different questions

After running the code, experiment with:

```
query = "What is machine learning?"
query = "What are neural networks?"
query = "Which language can I use for AI?"
```

Watch which documents Qdrant returns.

## 🧠 The 3 lines to remember

```python
query_vector = model.encode(query)

results = client.query_points(
    collection_name="documents",
    query=query_vector.tolist(),
    limit=3
)
```

That's the basic Qdrant semantic search.
""",
            "order":                6,
            "estimated_minutes":    30,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Run and Compare Semantic Queries",
                "description":   "Using the `documents` collection you built with real embeddings, run three different queries — one clearly about machine learning, one about neural networks, and one about programming languages for AI. For each, print the top result's score and text, and confirm the returned document makes semantic sense even when the wording differs from the query.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  "queries = [\n    \"What is machine learning?\",\n    \"What are neural networks?\",\n    \"Which language can I use for AI?\",\n]\n\n# TODO: for each query, encode it, call client.query_points(), and print\n# the top result's score and payload text\n",
                "solution_code": "queries = [\n    \"What is machine learning?\",\n    \"What are neural networks?\",\n    \"Which language can I use for AI?\",\n]\n\nfor query in queries:\n    query_vector = model.encode(query)\n    results = client.query_points(\n        collection_name=\"documents\",\n        query=query_vector.tolist(),\n        limit=1\n    )\n    top = results.points[0]\n    print(f\"Query: {query}\")\n    print(\"Score:\", top.score)\n    print(\"Text:\", top.payload[\"text\"])\n    print()\n",
                "skill_tested":  ["qdrant", "semantic-search", "query_points"],
            },
        ],
        "quiz": {
            "title":         "Similarity Search Quiz",
            "questions": [
                {
                    "question": "What is the correct pipeline for searching Qdrant with a natural-language question?",
                    "options": [
                        "Question → Qdrant → Embedding Model → Answer",
                        "Question → Embedding Model → Query Vector → Qdrant → Similar Documents",
                        "Question → Payload → Qdrant",
                        "Question → Distance.COSINE → Answer"
                    ],
                    "correct": 1,
                    "explanation": "You embed the question into a query vector using the same embedding model, then pass that vector to Qdrant, which returns the most similar stored documents."
                },
                {
                    "question": "In `client.query_points(collection_name=\"documents\", query=query_vector.tolist(), limit=2)`, what does `limit=2` control?",
                    "options": [
                        "The maximum vector dimension allowed",
                        "The number of most similar points returned",
                        "The number of collections searched",
                        "The minimum similarity score required"
                    ],
                    "correct": 1,
                    "explanation": "limit controls how many of the most similar points Qdrant returns, ranked by similarity score."
                },
                {
                    "question": "What does a higher `result.score` mean when using Distance.COSINE?",
                    "options": [
                        "The document is less relevant to the query",
                        "The document is more similar/relevant to the query",
                        "The document was inserted more recently",
                        "The document has a longer payload"
                    ],
                    "correct": 1,
                    "explanation": "With cosine similarity, a higher score means the query vector and document vector are more similar, i.e. more relevant."
                },
                {
                    "question": "Why can Qdrant match \"What is deep learning?\" to a document that says \"Deep learning uses neural networks to learn patterns\" even though the wording differs?",
                    "options": [
                        "Qdrant performs exact keyword matching after all",
                        "Because it compares the semantic meaning of the vectors, not the literal words",
                        "Because the payload text was manually linked to the query",
                        "It's a coincidence and not reliable"
                    ],
                    "correct": 1,
                    "explanation": "Semantic search compares vector meaning rather than exact words, so differently-worded but similar-meaning text can still match closely."
                },
                {
                    "question": "Which statement correctly describes the division of labor between the embedding model and Qdrant?",
                    "options": [
                        "Qdrant creates the embeddings; the embedding model only stores them",
                        "The embedding model creates vectors from text; Qdrant stores and searches those vectors",
                        "Both do the same job redundantly",
                        "Qdrant creates embeddings only during search, not during insert"
                    ],
                    "correct": 1,
                    "explanation": "The embedding model (e.g. Sentence Transformers) is responsible for turning text into vectors; Qdrant's job is purely to store and search vectors, not create them."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Payloads & Filtering",
        "slug":              "payloads-and-filtering",
        "description":       "Combine semantic search with metadata filters using Filter, FieldCondition, and MatchValue for more controlled RAG retrieval.",
        "order":             7,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["qdrant", "filtering", "rag", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Payloads & Filtering",
            "content": r"""Now we're going to learn something very useful in real projects: 🔎 **search by meaning AND apply conditions.**

For example: "Find documents about machine learning, but only from the AI course." This is called filtering.

## 1. What is a Payload?

We've already seen payloads:

```python
payload={
    "text": "Deep learning uses neural networks.",
    "course": "AI",
    "chapter": 3
}
```

The payload is simply extra information stored with the vector.

```
Point
├── ID
├── Vector
└── Payload
     ├── text
     ├── course
     └── chapter
```

## 2. Why do we need payloads?

Imagine we have 1,000 documents across courses: AI, Machine Learning, Computer Vision, NLP. A user asks "What is a neural network?" — but maybe we only want results from `course = "Deep Learning"`. The payload lets us do that.

## 3. Example documents

```python
documents = [
    {
        "text": "Machine learning learns patterns from data.",
        "course": "Machine Learning"
    },
    {
        "text": "Deep learning uses neural networks.",
        "course": "Deep Learning"
    },
    {
        "text": "Python is commonly used in AI.",
        "course": "Programming"
    }
]
```

Notice each document has `text` and `course`.

## 4. Store the payload

```python
points = []

for i, (document, vector) in enumerate(zip(documents, vectors)):
    points.append(
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={
                "text": document["text"],
                "course": document["course"]
            }
        )
    )
```

## 5. Search without filtering

Normally:

```python
results = client.query_points(
    collection_name="documents",
    query=query_vector.tolist(),
    limit=5
)
```

Qdrant searches everything: All documents → Similarity Search → Top results.

## 6. Search WITH a filter

Now suppose we only want `course = "Deep Learning"`. We can use a Qdrant filter.

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

query = "What are neural networks?"
query_vector = model.encode(query)

results = client.query_points(
    collection_name="documents",
    query=query_vector.tolist(),
    query_filter=Filter(
        must=[
            FieldCondition(
                key="course",
                match=MatchValue(value="Deep Learning")
            )
        ]
    ),
    limit=3
)
```

Now Qdrant searches only documents where `course == "Deep Learning"`.

## 7. Understand `must`

`must=[...]` means: **this condition must be true.** For example:

```python
must=[
    FieldCondition(
        key="course",
        match=MatchValue(value="Deep Learning")
    )
]
```

means: `course` MUST equal `"Deep Learning"`.

## 8. Multiple filters

Suppose your payload is:

```python
payload={
    "text": "...",
    "course": "AI",
    "year": 3,
    "language": "English"
}
```

You could filter `course = AI AND year = 3`:

```python
query_filter=Filter(
    must=[
        FieldCondition(key="course", match=MatchValue(value="AI")),
        FieldCondition(key="year", match=MatchValue(value=3))
    ]
)
```

So Qdrant finds: similar meaning + course = AI + year = 3.

## 9. Why filtering is powerful for RAG

Imagine your academic advisor RAG system with payload:

```python
payload={
    "text": "...",
    "department": "AI",
    "course_code": "CSE251",
    "academic_year": "2025/2026",
    "topic": "registration"
}
```

User asks: "What are the registration requirements for CSE251?" Instead of searching the entire database, you can filter `course_code = CSE251`, then perform semantic search inside those documents. That's much more controlled.

## 10. Semantic search + filtering

This is the key idea:

```
                  User Question
                       ↓
                  Query Vector
                       ↓
              ┌─────────────────┐
              │     Qdrant      │
              │                 │
              │ Filter          │
              │      ↓          │
              │ Similarity      │
              │ Search          │
              └────────┬────────┘
                       ↓
                Relevant Results
```

So you're combining a **Semantic condition** ("What is registration?") with a **Metadata condition** (`course_code = CSE251`).

## 🧪 Simple example

```python
payload={
    "text": "Students register courses before the semester.",
    "course": "CSE251"
}
```

You can search `query = "How do students register?"` and filter `course = "CSE251"`. The result is much more targeted.

## ⚠️ Important distinction

Don't confuse:

- **Payload** — information stored with a point: text, course, year, topic
- **Vector** — the numerical representation: `[0.12, -0.34, 0.78, ...]`
- **Filter** — a condition applied to payload: `course = CSE251`

```
Point
│
├── Vector → semantic meaning
│
└── Payload → metadata
          │
          └── Filter → restrict results
```

## 🧠 Remember this formula

```
Qdrant Search = Semantic Similarity + Metadata Filtering
```

For example: `"What is registration?" + course_code = "CSE251" + year = 3 → Qdrant → Relevant documents.`
""",
            "order":                7,
            "estimated_minutes":    35,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Filtered Semantic Search",
                "description":   "Insert the three example documents (with `course` metadata) into a fresh Qdrant collection. Then run a semantic search for \"What are neural networks?\" twice: once unfiltered, and once filtered to only `course = \"Deep Learning\"`. Compare the two result sets and confirm the filtered version only returns documents from that course.",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  "from qdrant_client.models import Filter, FieldCondition, MatchValue\n\nquery = \"What are neural networks?\"\nquery_vector = model.encode(query)\n\n# TODO: run an unfiltered query_points() search, print results\n\n# TODO: run a filtered query_points() search where course == \"Deep Learning\", print results\n",
                "solution_code": "from qdrant_client.models import Filter, FieldCondition, MatchValue\n\nquery = \"What are neural networks?\"\nquery_vector = model.encode(query)\n\n# Unfiltered\nunfiltered = client.query_points(\n    collection_name=\"documents\",\n    query=query_vector.tolist(),\n    limit=3\n)\nprint(\"Unfiltered:\")\nfor r in unfiltered.points:\n    print(r.score, r.payload)\n\n# Filtered to course = Deep Learning\nfiltered = client.query_points(\n    collection_name=\"documents\",\n    query=query_vector.tolist(),\n    query_filter=Filter(\n        must=[FieldCondition(key=\"course\", match=MatchValue(value=\"Deep Learning\"))]\n    ),\n    limit=3\n)\nprint(\"Filtered (Deep Learning only):\")\nfor r in filtered.points:\n    print(r.score, r.payload)\n",
                "skill_tested":  ["qdrant", "filtering", "query_points", "rag"],
            },
        ],
        "quiz": {
            "title":         "Payloads & Filtering Quiz",
            "questions": [
                {
                    "question": "What does the `must` keyword mean inside a Qdrant `Filter`?",
                    "options": [
                        "The condition is optional and only applied if space allows",
                        "The condition must be true for a point to be included in the results",
                        "It sorts the results by that field",
                        "It excludes points that match the condition"
                    ],
                    "correct": 1,
                    "explanation": "`must` specifies conditions that have to be true — points that don't satisfy every `must` condition are excluded from the results."
                },
                {
                    "question": "In `FieldCondition(key=\"course\", match=MatchValue(value=\"Deep Learning\"))`, what is being filtered?",
                    "options": [
                        "Only points where the vector's first dimension equals 'Deep Learning'",
                        "Only points where the payload's 'course' field equals exactly 'Deep Learning'",
                        "All points, sorted by course name",
                        "The embedding model to use"
                    ],
                    "correct": 1,
                    "explanation": "FieldCondition with MatchValue restricts results to points whose payload field ('course') exactly matches the given value."
                },
                {
                    "question": "What does combining a query_filter with a semantic query achieve?",
                    "options": [
                        "It replaces semantic search with pure keyword search",
                        "It restricts the semantic similarity search to only the subset of points matching the metadata condition(s)",
                        "It has no effect on which results are returned",
                        "It disables the vector search entirely"
                    ],
                    "correct": 1,
                    "explanation": "The filter narrows the candidate pool by metadata (e.g. course_code), and then Qdrant runs similarity search only within that filtered subset."
                },
                {
                    "question": "If you add two FieldConditions inside the same `must` list, how are they combined?",
                    "options": [
                        "As an OR — either condition can be true",
                        "As an AND — both conditions must be true",
                        "Only the first condition is applied",
                        "They cancel each other out"
                    ],
                    "correct": 1,
                    "explanation": "Multiple conditions inside `must` are combined with AND logic — every condition in the list has to be satisfied."
                },
                {
                    "question": "Why is filtering especially useful for a RAG system like an academic advisor bot?",
                    "options": [
                        "It removes the need for an embedding model",
                        "It lets you narrow retrieval to relevant metadata (e.g. a specific course code) before running semantic search, giving more targeted results",
                        "It automatically improves the accuracy of the LLM's language generation",
                        "It stores documents more efficiently on disk"
                    ],
                    "correct": 1,
                    "explanation": "Filtering by metadata (like course_code or department) lets you scope semantic search to the relevant subset of documents, producing more targeted and controlled retrieval for RAG."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Advanced Filtering",
        "slug":              "advanced-filtering",
        "description":       "Combine AND, OR, NOT, and numeric range conditions in Qdrant filters for more precise, controlled RAG retrieval.",
        "order":             8,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["qdrant", "filtering", "rag", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Advanced Filtering",
            "content": r"""Now let's make filtering a little more powerful. Don't worry — there are only a few ideas you need. The main operators are: **AND**, **OR**, **NOT**, **Range**.

## 1. AND — All conditions must match

Suppose each point has:

```python
payload = {
    "course": "AI",
    "year": 3,
    "language": "English"
}
```

We want: AI AND Year 3. Use `must`:

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

query_filter = Filter(
    must=[
        FieldCondition(key="course", match=MatchValue(value="AI")),
        FieldCondition(key="year", match=MatchValue(value=3))
    ]
)
```

This means `course = AI AND year = 3`. Only points satisfying both conditions are returned.

## 2. OR — At least one condition

Suppose you want: Course is AI OR Machine Learning. Use `should`:

```python
query_filter = Filter(
    should=[
        FieldCondition(key="course", match=MatchValue(value="AI")),
        FieldCondition(key="course", match=MatchValue(value="Machine Learning"))
    ]
)
```

A point can match either one.

## 3. NOT — Exclude something

Suppose you want: search everything except AI documents. Use `must_not`:

```python
query_filter = Filter(
    must_not=[
        FieldCondition(key="course", match=MatchValue(value="AI"))
    ]
)
```

Meaning `course ≠ AI`. So AI documents are excluded, everything else passes.

## 4. Combining AND + OR

A realistic example: `Year 3 AND (AI OR Machine Learning)`.

```
                    year = 3
                       │
                       AND
                       │
              ┌────────┴────────┐
              │                 │
          course = AI     course = ML
              │                 │
              └────── OR ───────┘
```

The filter can be built using nested filter conditions. For learning purposes, the important thing is understanding the logic.

## 5. Numeric ranges

Suppose your payload contains:

```python
payload = {
    "course": "AI",
    "credits": 3
}
```

You could ask: find courses with at least 3 credits. Qdrant supports range conditions:

```python
from qdrant_client.models import Range

query_filter = Filter(
    must=[
        FieldCondition(
            key="credits",
            range=Range(gte=3)
        )
    ]
)
```

`gte` means "greater than or equal": `3 → ✅, 4 → ✅, 5 → ✅, 2 → ❌`

## 6. Other range operators

| Operator | Meaning |
|---|---|
| gt | greater than |
| gte | greater than or equal |
| lt | less than |
| lte | less than or equal |

Example: `range=Range(gte=3, lte=5)` means `3 ≤ credits ≤ 5`.

## 7. Real academic example

Imagine your Qdrant payload contains:

```python
payload = {
    "text": "...",
    "course_code": "CSE251",
    "credits": 3,
    "year": 3,
    "department": "AI"
}
```

A user asks: "Find information about third-year AI courses worth at least 3 credits." You could conceptually filter `department = AI AND year = 3 AND credits >= 3`, then Qdrant performs semantic search inside those matching points.

## 8. Filtering + similarity search

This is the important part — we don't use filtering *instead of* vector search, we combine them:

```
                 User Question
                       ↓
                  Query Vector
                       ↓
                ┌─────────────┐
                │   Qdrant    │
                │             │
                │   Filter    │
                │      ↓      │
                │   Search    │
                └──────┬──────┘
                       ↓
                 Top K Results
```

```python
results = client.query_points(
    collection_name="documents",
    query=query_vector.tolist(),
    query_filter=query_filter,
    limit=5
)
```

So: `query + query_filter + limit`.

## 9. Why this matters for RAG

Imagine your database contains 100,000 chunks — you don't necessarily want to search all of them. Suppose the user asks: "What are the registration rules for AI students in 2026?" You could use metadata: `department = AI`, `academic_year = 2026`, `topic = registration`. Then Qdrant searches semantically among the relevant data. This can make your retrieval much more controlled.

## 🧠 The four operators to remember

```
must      → AND
should    → OR
must_not  → NOT
range     → numbers
```

That's enough for now.
""",
            "order":                8,
            "estimated_minutes":    35,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Build a Compound Filter",
                "description":   "Given points with payloads containing `course`, `year`, and `credits`, build a Qdrant filter that finds points where `year = 3` AND `credits >= 3` AND the course is either `\"AI\"` or `\"Machine Learning\"`. You don't need to run this against real data — just construct the `Filter` object correctly and print it.",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  "from qdrant_client.models import Filter, FieldCondition, MatchValue, Range\n\n# TODO: build a Filter for:\n# year == 3 AND credits >= 3 AND (course == \"AI\" OR course == \"Machine Learning\")\n",
                "solution_code": "from qdrant_client.models import Filter, FieldCondition, MatchValue, Range\n\nquery_filter = Filter(\n    must=[\n        FieldCondition(key=\"year\", match=MatchValue(value=3)),\n        FieldCondition(key=\"credits\", range=Range(gte=3)),\n        Filter(\n            should=[\n                FieldCondition(key=\"course\", match=MatchValue(value=\"AI\")),\n                FieldCondition(key=\"course\", match=MatchValue(value=\"Machine Learning\")),\n            ]\n        ),\n    ]\n)\n\nprint(query_filter)\n",
                "skill_tested":  ["qdrant", "filtering", "must", "should", "range"],
            },
        ],
        "quiz": {
            "title":         "Advanced Filtering Quiz",
            "questions": [
                {
                    "question": "Which Qdrant filter keyword implements 'OR' logic?",
                    "options": [
                        "must",
                        "should",
                        "must_not",
                        "range"
                    ],
                    "correct": 1,
                    "explanation": "`should` means at least one of the listed conditions can match — this implements OR logic."
                },
                {
                    "question": "What does `must_not=[FieldCondition(key=\"course\", match=MatchValue(value=\"AI\"))]` do?",
                    "options": [
                        "Returns only points where course equals AI",
                        "Excludes points where course equals AI, returning everything else",
                        "Sorts results with AI courses first",
                        "Has no effect on the results"
                    ],
                    "correct": 1,
                    "explanation": "must_not excludes any point matching the condition — here, all points with course = AI are filtered out."
                },
                {
                    "question": "Given payload `credits: 3` and a filter `range=Range(gte=3)`, does this point match?",
                    "options": [
                        "Yes, because 3 is greater than or equal to 3",
                        "No, because 3 is not strictly greater than 3",
                        "It depends on the course field",
                        "Range conditions can't be applied to integers"
                    ],
                    "correct": 0,
                    "explanation": "gte means 'greater than or equal to', so a value of exactly 3 satisfies range=Range(gte=3)."
                },
                {
                    "question": "How would you express 'year = 3 AND (course = AI OR course = Machine Learning)' using Qdrant filters?",
                    "options": [
                        "A single must_not condition",
                        "A must condition for year=3, combined with a nested should for the two course options",
                        "Two separate must conditions for course, with no way to combine with year",
                        "This logic isn't supported by Qdrant filters"
                    ],
                    "correct": 1,
                    "explanation": "You combine a must condition (year=3) with a nested filter using should (OR) for the two course options, achieving AND(year=3, OR(course=AI, course=ML))."
                },
                {
                    "question": "Why do we combine filtering with vector similarity search instead of using filtering alone?",
                    "options": [
                        "Filtering alone is always faster and just as accurate",
                        "Filtering narrows the candidate set by metadata, while similarity search finds the most semantically relevant results within that set — together they give more precise, controlled retrieval",
                        "Vector search cannot run at all without a filter",
                        "Filters replace the need for an embedding model"
                    ],
                    "correct": 1,
                    "explanation": "Filtering restricts the pool of candidates by exact metadata conditions, while similarity search ranks by semantic relevance — combining both gives more targeted RAG retrieval than either alone."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Persistent Storage & Docker",
        "slug":              "persistent-storage-and-docker",
        "description":       "Move beyond in-memory Qdrant — use local disk persistence or run Qdrant as a Docker server for real applications.",
        "order":             9,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.0,
        "skill_tags":        ["qdrant", "docker", "persistence", "deployment"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Persistent Storage & Docker",
            "content": r"""Until now we've used `client = QdrantClient(":memory:")`. That's great for learning, but there's one big problem: **everything disappears when the Python program stops.** ❌

Now we'll learn how to keep our data.

## 1. Two ways to keep Qdrant data

**Option A — Local persistent mode.** Qdrant stores its data on your disk: `Python → Qdrant → Disk`

**Option B — Qdrant server.** Run Qdrant as a separate service, commonly with Docker: `Python → Qdrant Server → Disk`

For real projects, the second approach is very common.

## 2. Local persistent mode

For learning, we can use:

```python
from qdrant_client import QdrantClient

client = QdrantClient(path="./qdrant_data")
```

Instead of `QdrantClient(":memory:")`, we use `QdrantClient(path="./qdrant_data")`. Now Qdrant stores the local data in `qdrant_data/`.

## 3. Why is this useful?

With `QdrantClient(":memory:")`:

```
Run Python → Data exists → Stop Python → 💥 Data disappears
```

With `QdrantClient(path="./qdrant_data")`:

```
Run Python → Store data → Stop Python → Data remains → Run Python again → Data is still there
```

Much better. ✅

## 4. Example

```python
from qdrant_client import QdrantClient

client = QdrantClient(path="./qdrant_data")

print(client.get_collections())
```

Now your Qdrant data is associated with that local directory.

## 5. When should you use this?

For learning, small experiments, local applications, and testing — it's convenient. But for a larger application, you may want a real Qdrant server.

## 6. Qdrant with Docker

Docker lets you run Qdrant as a separate service. The architecture becomes:

```
┌──────────────────┐
│   Your Python    │
│    Application   │
└────────┬─────────┘
         │
         │ HTTP
         ▼
┌──────────────────┐
│ Qdrant Container │
│                  │
│    Qdrant DB     │
└──────────────────┘
```

## 7. Start Qdrant with Docker

If Docker is installed, run:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Qdrant will run on `localhost:6333`.

## 8. Connect Python to it

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
```

Now: `Python → localhost:6333 → Qdrant`

## 9. Three Qdrant setups you should remember

**🟢 Setup 1 — Memory:** `QdrantClient(":memory:")` — use for quick experiments, learning, tests. Data disappears when the process ends.

**🟡 Setup 2 — Local disk:** `QdrantClient(path="./qdrant_data")` — use for local projects, persistent development, small applications. Data stays on disk.

**🔵 Setup 3 — Qdrant server:** `QdrantClient(url="http://localhost:6333")` — use for real applications, backend services, multiple clients, Docker deployments.

## 10. Important: Don't confuse the client and server

This is a common beginner mistake.

**Qdrant Client** — your Python code, `QdrantClient(...)`. It lets your application communicate with Qdrant.

**Qdrant Server** — the actual database service running at e.g. `localhost:6333`.

```
Python Application
       │
       │ Qdrant Client
       ▼
   Qdrant Server
       │
       ▼
     Storage
```

## 11. What should YOU use?

For our lessons, I recommend `QdrantClient(":memory:")` now, because it's simple. Then for projects, `QdrantClient(path="./qdrant_data")` or Docker with `QdrantClient(url="http://localhost:6333")`.

## 🧠 One important real-world concept

Suppose you're building your academic RAG system. You don't want to load 10,000 documents and create embeddings every single time you start the application. Instead:

```
First setup → Create embeddings → Store in Qdrant → Persistent storage
```

Then later:

```
Start application → Connect to existing Qdrant → Search immediately
```

That's the advantage of persistence.

## 🎯 Quick recap

| Mode | Example | Data survives? | Good for |
|---|---|---|---|
| Memory | `:memory:` | ❌ | Learning |
| Local | `path="./qdrant_data"` | ✅ | Local projects |
| Server | `url="http://localhost:6333"` | ✅ | Real applications |
""",
            "order":                9,
            "estimated_minutes":    30,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Switch Between Qdrant Modes",
                "description":   "Write the three lines of client-initialization code corresponding to the three Qdrant setups discussed in this lesson (memory, local disk, and server), and add a one-line comment next to each explaining when you'd use it.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  "from qdrant_client import QdrantClient\n\n# TODO: memory-mode client\n\n# TODO: local-disk persistent client\n\n# TODO: server-mode client connecting to a Dockerized Qdrant instance\n",
                "solution_code": "from qdrant_client import QdrantClient\n\n# Memory mode — quick experiments, learning, tests (data disappears on exit)\nmemory_client = QdrantClient(\":memory:\")\n\n# Local disk mode — local projects, persistent development (data stays on disk)\nlocal_client = QdrantClient(path=\"./qdrant_data\")\n\n# Server mode — real applications, backend services, multiple clients (requires a running Qdrant server, e.g. via Docker)\nserver_client = QdrantClient(url=\"http://localhost:6333\")\n",
                "skill_tested":  ["qdrant", "deployment", "docker"],
            },
        ],
        "quiz": {
            "title":         "Persistent Storage & Docker Quiz",
            "questions": [
                {
                    "question": "What happens to data stored with `QdrantClient(\":memory:\")` when the Python program stops?",
                    "options": [
                        "It's automatically saved to disk",
                        "It disappears completely",
                        "It's uploaded to a Qdrant cloud server",
                        "It's cached and restored on the next run"
                    ],
                    "correct": 1,
                    "explanation": "In-memory mode keeps all data inside the running Python process — once the process stops, the data is gone."
                },
                {
                    "question": "What does `QdrantClient(path=\"./qdrant_data\")` do differently from `:memory:` mode?",
                    "options": [
                        "Nothing, they behave identically",
                        "It stores Qdrant's data on local disk so it survives after the program stops",
                        "It connects to a remote Qdrant server",
                        "It disables vector search"
                    ],
                    "correct": 1,
                    "explanation": "Local persistent mode saves data to a local directory on disk, so it's still there the next time you start the program."
                },
                {
                    "question": "What command starts a Qdrant server using Docker on the default port?",
                    "options": [
                        "docker run -p 6333:6333 qdrant/qdrant",
                        "pip install qdrant-server",
                        "qdrant --start",
                        "docker build qdrant"
                    ],
                    "correct": 0,
                    "explanation": "`docker run -p 6333:6333 qdrant/qdrant` runs the Qdrant server container, exposing it on port 6333."
                },
                {
                    "question": "What's the difference between the 'Qdrant Client' and the 'Qdrant Server'?",
                    "options": [
                        "They are the same thing",
                        "The Client is your Python code that communicates with Qdrant; the Server is the actual database service (e.g. running at localhost:6333)",
                        "The Client stores data; the Server only searches it",
                        "The Server is only used in memory mode"
                    ],
                    "correct": 1,
                    "explanation": "The client is the library your application uses to talk to Qdrant, while the server is the actual running database service that stores and processes the data."
                },
                {
                    "question": "Which setup would be most appropriate for a real backend application serving multiple clients in production?",
                    "options": [
                        "QdrantClient(\":memory:\")",
                        "QdrantClient(path=\"./qdrant_data\")",
                        "QdrantClient(url=\"http://localhost:6333\") connecting to a running Qdrant server",
                        "None of these are appropriate for production"
                    ],
                    "correct": 2,
                    "explanation": "For real applications, backend services, and multiple clients, running Qdrant as a server (e.g. via Docker) and connecting via URL is the recommended setup."
                }
            ],
            "passing_score": 70,
        },
        "project": None,
    },
    {
        # ToolTopic fields
        "title":            "Qdrant + Sentence Transformers",
        "slug":              "qdrant-plus-sentence-transformers",
        "description":       "Put it all together — build a small end-to-end semantic search engine using Sentence Transformers and Qdrant.",
        "order":             10,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   2.0,
        "skill_tags":        ["qdrant", "sentence-transformers", "semantic-search", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Qdrant + Sentence Transformers",
            "content": r"""Now we put everything together. We're going to build a small semantic search engine using:

🧠 Sentence Transformers → creates embeddings
🗄️ Qdrant → stores/searches vectors
🔎 Semantic search → finds relevant documents

## 1. The complete architecture

```
Documents
    ↓
Sentence Transformer
    ↓
Embeddings
    ↓
Qdrant
    ↓
        User Question
             ↓
      Sentence Transformer
             ↓
        Query Embedding
             ↓
           Qdrant
             ↓
       Similar Documents
```

This is basically the retrieval part of RAG.

## 2. Install the libraries

```bash
pip install qdrant-client sentence-transformers
```

## 3. Load the embedding model

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

Remember: `all-MiniLM-L6-v2` → 384 dimensions.

## 4. Create our documents

```python
documents = [
    "Machine learning allows computers to learn patterns from data.",
    "Deep learning is based on neural networks with multiple layers.",
    "Python is widely used for artificial intelligence and machine learning.",
    "Qdrant is a vector database designed for similarity search.",
    "RAG combines information retrieval with large language models."
]
```

## 5. Create embeddings

```python
vectors = model.encode(documents)
```

Each of the 5 vectors has 384 numbers.

## 6. Create Qdrant

```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
```

## 7. Create a collection

```python
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="knowledge",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
```

## 8. Create points

```python
from qdrant_client.models import PointStruct

points = []
for i, (document, vector) in enumerate(zip(documents, vectors)):
    points.append(
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={"text": document}
        )
    )
```

## 9. Insert the points

```python
client.upsert(
    collection_name="knowledge",
    points=points
)
```

## 10. Ask a question

```python
query = "What is a vector database?"
query_vector = model.encode(query)
```

## 11. Search Qdrant

```python
results = client.query_points(
    collection_name="knowledge",
    query=query_vector.tolist(),
    limit=3
)
```

Qdrant finds the three most similar points.

## 12. Display the results

```python
for result in results.points:
    print("Score:", result.score)
    print("Text:", result.payload["text"])
    print()
```

You should see the Qdrant document near the top: `"Qdrant is a vector database designed for similarity search."` — that's exactly what we wanted. 🎯

## 13. Let's try another question

```python
query = "How does deep learning work?"
```

Qdrant should find something like: `"Deep learning is based on neural networks with multiple layers."`

## 14. Another question

```python
query = "Which programming language is popular for AI?"
```

The relevant result should be: `"Python is widely used for artificial intelligence and machine learning."` Notice the question doesn't have to exactly match the document — that's semantic search.

## 15. Complete mini-project

```python
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Machine learning allows computers to learn patterns from data.",
    "Deep learning is based on neural networks with multiple layers.",
    "Python is widely used for artificial intelligence and machine learning.",
    "Qdrant is a vector database designed for similarity search.",
    "RAG combines information retrieval with large language models."
]

vectors = model.encode(documents)
client = QdrantClient(":memory:")

client.create_collection(
    collection_name="knowledge",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

points = []
for i, (document, vector) in enumerate(zip(documents, vectors)):
    points.append(
        PointStruct(id=i, vector=vector.tolist(), payload={"text": document})
    )

client.upsert(collection_name="knowledge", points=points)

query = "What is a vector database?"
query_vector = model.encode(query)

results = client.query_points(
    collection_name="knowledge",
    query=query_vector.tolist(),
    limit=3
)

for result in results.points:
    print("Score:", result.score)
    print("Text:", result.payload["text"])
    print()
```

## 🧠 Understand what is happening

Don't memorize the whole code — understand this pipeline:

```
                DOCUMENTS
                    │
                    ▼
          Sentence Transformer
                    │
                    ▼
                 VECTORS
                    │
                    ▼
                 QDRANT
                    │
                    │
             User Question
                    │
                    ▼
          Sentence Transformer
                    │
                    ▼
              Query Vector
                    │
                    ▼
                 QDRANT
                    │
                    ▼
          Similar Documents
```

## 🔥 This is almost RAG

Currently: `Question → Qdrant → Relevant documents`

A RAG system adds one more step: `Question → Qdrant → Relevant documents → LLM → Final Answer`

For example, given the question "What is Qdrant?", Qdrant retrieves "Qdrant is a vector database designed for similarity search," and the LLM turns that into: "Qdrant is a vector database used to store and search embeddings."
""",
            "order":                10,
            "estimated_minutes":    45,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Mini Semantic Search Challenge",
                "description":   "Using the `knowledge` collection from this lesson, search for \"What is RAG?\" with `limit=2` and confirm the RAG-related document ranks near the top. Then try \"How do neural networks help AI?\" and observe which document Qdrant considers most similar, even though the wording doesn't exactly match any document.",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  "queries = [\n    (\"What is RAG?\", 2),\n    (\"How do neural networks help AI?\", 2),\n]\n\n# TODO: for each (query, limit) pair, encode the query, run query_points(),\n# and print the score + text of each result\n",
                "solution_code": "queries = [\n    (\"What is RAG?\", 2),\n    (\"How do neural networks help AI?\", 2),\n]\n\nfor query, limit in queries:\n    query_vector = model.encode(query)\n    results = client.query_points(\n        collection_name=\"knowledge\",\n        query=query_vector.tolist(),\n        limit=limit\n    )\n    print(f\"Query: {query}\")\n    for r in results.points:\n        print(\" Score:\", r.score, \"| Text:\", r.payload[\"text\"])\n    print()\n",
                "skill_tested":  ["qdrant", "sentence-transformers", "semantic-search"],
            },
        ],
        "quiz": {
            "title":         "Qdrant + Sentence Transformers Quiz",
            "questions": [
                {
                    "question": "In this lesson's architecture, what role does Sentence Transformers play?",
                    "options": [
                        "It stores and searches vectors",
                        "It converts both documents and user questions into embeddings",
                        "It generates the final natural-language answer",
                        "It applies metadata filters"
                    ],
                    "correct": 1,
                    "explanation": "Sentence Transformers is the embedding model — it turns both the knowledge base documents and incoming queries into vectors."
                },
                {
                    "question": "Why does asking \"Which programming language is popular for AI?\" still correctly retrieve the Python document, even though the wording differs?",
                    "options": [
                        "Qdrant does exact keyword matching by default",
                        "Because semantic search compares vector meaning rather than literal wording",
                        "The documents were manually tagged with keywords",
                        "It's random chance"
                    ],
                    "correct": 1,
                    "explanation": "Semantic search matches based on the meaning captured by the embeddings, so differently worded but semantically related questions and documents can still match well."
                },
                {
                    "question": "What's the difference between the pipeline in this lesson and a full RAG system?",
                    "options": [
                        "There is no difference — they're identical",
                        "This lesson stops at retrieving relevant documents; RAG adds a final step where an LLM generates an answer from those documents",
                        "RAG doesn't use embeddings",
                        "This lesson uses a real LLM, but RAG doesn't"
                    ],
                    "correct": 1,
                    "explanation": "This lesson covers Question → Qdrant → Relevant documents. A full RAG system adds Relevant documents → LLM → Final Answer."
                },
                {
                    "question": "Why must the same embedding model (all-MiniLM-L6-v2) be used for both the documents and the query?",
                    "options": [
                        "It doesn't matter which model is used for each",
                        "Different models produce vectors in different, incompatible spaces — for similarity comparison to be meaningful, both sides must use the same model",
                        "Only the query needs an embedding model; documents don't",
                        "Using different models makes search faster"
                    ],
                    "correct": 1,
                    "explanation": "Vectors from different embedding models aren't comparable — cosine similarity is only meaningful when both the query and documents were embedded with the same model."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Build a Mini Semantic Search Engine",
            "description":      "Build a small, self-contained semantic search engine over a knowledge base of your choosing (at least 8-10 short documents on a topic you're interested in — e.g. university policies, cooking tips, or programming concepts). Use Sentence Transformers to embed the documents, store them in an in-memory Qdrant collection, and implement a `search(query, top_k=3)` function that embeds a query and returns the top matching documents with their similarity scores. Test it with at least 5 different queries, including some that use different wording than the source documents, and write a short summary of how well semantic search performed compared to what a keyword search would have found.",
            "difficulty":       DifficultyLevel.intermediate,
            "tech_stack":       ["Qdrant", "Sentence Transformers", "Python"],
            "objectives": [
                "Build a knowledge base of at least 8-10 short text documents",
                "Generate real embeddings using Sentence Transformers (all-MiniLM-L6-v2)",
                "Create and populate a Qdrant collection with the correct vector size and distance metric",
                "Implement a reusable search(query, top_k) function using query_points()",
                "Test the search function with at least 5 varied queries, including reworded/paraphrased ones",
                "Summarize how semantic search results compare to what keyword matching would return"
            ],
            "rubric": {
                "correctness": "Embeddings, collection, and points are created correctly with matching vector dimensions",
                "functionality": "search() function reliably returns relevant top-k results with scores",
                "testing": "At least 5 varied queries tested, including paraphrased wording",
                "reflection": "Clear written comparison of semantic vs. keyword search behavior"
            },
            "starter_repo_url": None,
            "estimated_hours":  3.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Qdrant + RAG",
        "slug":              "qdrant-plus-rag",
        "description":       "Connect Qdrant to a full Retrieval-Augmented Generation pipeline — retrieve relevant chunks, build context, and pass it to an LLM.",
        "order":             11,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   2.0,
        "skill_tags":        ["qdrant", "rag", "llm", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Qdrant + RAG",
            "content": r"""Now we're connecting Qdrant to something you've already learned: **RAG (Retrieval-Augmented Generation)**. This is where Qdrant becomes really useful.

## 1. What is RAG?

RAG is basically:

```
User Question → Retrieve relevant information → Give information to LLM → LLM generates answer
```

With Qdrant:

```
                 User Question
                       ↓
                 Embedding Model
                       ↓
                  Query Vector
                       ↓
                    Qdrant
                       ↓
                Relevant Chunks
                       ↓
                     LLM
                       ↓
                    Answer
```

## 2. Why do we need Qdrant?

Imagine you have 10,000 document chunks. The user asks "What are the graduation requirements?" We don't want to send all 10,000 chunks to the LLM. Instead:

```
10,000 chunks → Qdrant → Top 5 relevant chunks → LLM
```

That's the retrieval part.

## 3. Our simple knowledge base

```python
documents = [
    "Students need 140 credit hours to graduate.",
    "Students must maintain the required minimum GPA.",
    "Course registration takes place before the beginning of each semester.",
    "Students can drop courses according to university regulations.",
    "Artificial intelligence courses include machine learning and deep learning."
]
```

In a real project, these would come from PDFs, Word files, websites, etc.

## 4. Create embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(documents)
```

## 5. Store them in Qdrant

```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
```

Create collection:

```python
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="university",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
```

## 6. Insert the documents

```python
from qdrant_client.models import PointStruct

points = []
for i, (text, vector) in enumerate(zip(documents, vectors)):
    points.append(
        PointStruct(id=i, vector=vector.tolist(), payload={"text": text})
    )

client.upsert(collection_name="university", points=points)
```

Now Qdrant contains our knowledge.

## 7. User asks a question

```python
question = "How many credit hours are needed for graduation?"
query_vector = model.encode(question)
```

## 8. Retrieve relevant documents

```python
results = client.query_points(
    collection_name="university",
    query=query_vector.tolist(),
    limit=3
)
```

Now Qdrant might return: "Students need 140 credit hours to graduate.", "Students must maintain the required minimum GPA.", and "Course registration takes place before...". The first one is the most relevant.

## 9. Build the context

```python
context = "\n".join(
    result.payload["text"]
    for result in results.points
)

print(context)
```

This is our context.

## 10. Give the context to an LLM

```python
prompt = f'''
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Answer:
'''
```

Then send this prompt to your LLM. Conceptually: `Context + Question → LLM → Answer`

For example, the question "How many credit hours are needed for graduation?" produces the answer "Students need 140 credit hours to graduate."

## 11. The complete RAG pipeline

```
                  DOCUMENTS
                     ↓
                Embeddings
                     ↓
                   Qdrant
                     ↓
              ┌─────────────┐
              │             │
              │  Retriever  │
              │             │
              └──────┬──────┘
                     ↑
                     │
               User Question
                     │
                     ↓
                 Embedding
                     │
                     ↓
                  Qdrant
                     │
                     ↓
              Relevant Chunks
                     │
                     ↓
                   LLM
                     │
                     ↓
                  Answer
```

That's RAG.

## 12. Qdrant's role

This is very important: **Qdrant is not the LLM.** Qdrant doesn't generate the answer.

Qdrant does: `STORE → SEARCH → RETRIEVE`

The LLM does: `UNDERSTAND CONTEXT → GENERATE ANSWER`

So: `Qdrant = Retrieval`, `LLM = Generation`. That's why it's called Retrieval-Augmented Generation.

## 13. Why this is useful for your projects

For an academic assistant: `University Documents → Chunking → Embeddings → Qdrant`. Then a student asks "What are the requirements for graduation?", Qdrant retrieves the relevant chunks, and the LLM answers using those chunks. This is exactly the type of architecture used in many production RAG systems.

## 🧠 Important RAG vocabulary

| Term | Meaning |
|---|---|
| Embedding | Text → vector |
| Vector DB | Stores/searches vectors |
| Qdrant | Vector database |
| Point | Vector + payload + ID |
| Retriever | Finds relevant documents |
| Context | Retrieved information given to LLM |
| LLM | Generates final answer |
| RAG | Retrieval + generation |

## 🏆 You've reached an important point

You now understand the complete relationship:

```
Sentence Transformer → Embeddings → Qdrant → Retrieval → LLM → Answer
```
""",
            "order":                11,
            "estimated_minutes":    45,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Assemble the RAG Context and Prompt",
                "description":   "Given the `university` collection and a question, retrieve the top 3 relevant chunks with query_points(), join their payload text into a single `context` string, and build the final prompt string following the template from the lesson (Context + Question + Answer). Print the final prompt so you can see exactly what would be sent to an LLM.",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  "question = \"How many credit hours are needed for graduation?\"\n\n# TODO: embed the question, retrieve top 3 chunks, build context string,\n# and construct the final prompt using the lesson's template. Print the prompt.\n",
                "solution_code": "question = \"How many credit hours are needed for graduation?\"\nquery_vector = model.encode(question)\n\nresults = client.query_points(\n    collection_name=\"university\",\n    query=query_vector.tolist(),\n    limit=3\n)\n\ncontext = \"\\n\".join(result.payload[\"text\"] for result in results.points)\n\nprompt = f\"\"\"\nAnswer the question using only the context below.\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:\n\"\"\"\n\nprint(prompt)\n",
                "skill_tested":  ["qdrant", "rag", "prompt-construction"],
            },
        ],
        "quiz": {
            "title":         "Qdrant + RAG Quiz",
            "questions": [
                {
                    "question": "In the RAG pipeline, what is Qdrant's role versus the LLM's role?",
                    "options": [
                        "Qdrant generates answers; the LLM stores and searches vectors",
                        "Qdrant handles store/search/retrieve; the LLM understands context and generates the answer",
                        "They do the exact same job redundantly",
                        "Qdrant replaces the need for an LLM entirely"
                    ],
                    "correct": 1,
                    "explanation": "Qdrant is responsible for retrieval (store, search, retrieve), while the LLM is responsible for generation (understanding context and producing the final answer)."
                },
                {
                    "question": "Why don't we send all 10,000 document chunks directly to the LLM for every question?",
                    "options": [
                        "LLMs can't process text at all",
                        "It would be inefficient and often exceed context limits — Qdrant retrieval narrows it down to only the most relevant chunks first",
                        "Qdrant doesn't allow more than 3 documents to be stored",
                        "The LLM would refuse to answer"
                    ],
                    "correct": 1,
                    "explanation": "Sending the entire knowledge base to the LLM every time is inefficient and impractical; Qdrant's retrieval step narrows things down to the small set of most relevant chunks."
                },
                {
                    "question": "What does the 'context' in a RAG prompt consist of?",
                    "options": [
                        "The entire original knowledge base",
                        "The text payloads of the top-k documents retrieved from Qdrant for this specific question",
                        "The embedding vectors themselves",
                        "The LLM's previous answers"
                    ],
                    "correct": 1,
                    "explanation": "The context is built by joining together the payload text of the documents Qdrant returned as most relevant to the current question."
                },
                {
                    "question": "What does 'RAG' stand for and reflect about the architecture?",
                    "options": [
                        "Random Answer Generation — the LLM answers without any retrieval step",
                        "Retrieval-Augmented Generation — retrieval (via Qdrant) augments the LLM's generation with relevant, specific context",
                        "Ranked Answer Grouping — Qdrant ranks multiple LLM answers",
                        "Real-time Answer Gateway — a caching layer for LLM responses"
                    ],
                    "correct": 1,
                    "explanation": "RAG stands for Retrieval-Augmented Generation: the LLM's generation step is augmented (improved/grounded) using documents retrieved by a system like Qdrant."
                },
                {
                    "question": "In the RAG prompt template used in this lesson, what two things is the LLM given besides its instructions?",
                    "options": [
                        "The vector embeddings and the collection name",
                        "The retrieved context and the original user question",
                        "The Qdrant client code and the payload schema",
                        "Only the question — context is not included"
                    ],
                    "correct": 1,
                    "explanation": "The prompt template includes the retrieved context (joined document text) and the user's original question, instructing the LLM to answer using only that context."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Build a Mini RAG Assistant",
            "description":      "Build an end-to-end mini RAG pipeline over a small knowledge base (at least 8-10 short chunks) on a topic of your choice — e.g. a university's academic policies, a product FAQ, or your own notes on a subject. Use Sentence Transformers to embed the chunks, store and retrieve them via Qdrant, assemble retrieved chunks into a context string, and build the final prompt that would be sent to an LLM. If you have access to an LLM API, actually send the prompt and print the generated answer; otherwise, print the assembled prompt and write out what you'd expect a good answer to look like. Test with at least 4 questions, including at least one that should NOT be answerable from the knowledge base, and show how you'd instruct the LLM to say so rather than hallucinate.",
            "difficulty":       DifficultyLevel.intermediate,
            "tech_stack":       ["Qdrant", "Sentence Transformers", "Python", "LLM API (optional)"],
            "objectives": [
                "Build a knowledge base of at least 8-10 short chunks on a chosen topic",
                "Embed and store the chunks in Qdrant with correct vector configuration",
                "Implement a retrieve(question, top_k) function returning relevant chunks",
                "Assemble retrieved chunks into a context string and build a grounded prompt",
                "Test with at least 4 questions, including one unanswerable from the knowledge base",
                "Handle the unanswerable case explicitly (e.g. instruct the LLM to say it doesn't know rather than hallucinate)"
            ],
            "rubric": {
                "correctness": "Embeddings, Qdrant collection, and retrieval work correctly end-to-end",
                "prompt_design": "Context + question are combined into a clear, grounded prompt",
                "edge_case_handling": "Unanswerable question is handled explicitly rather than producing a hallucinated answer",
                "testing": "At least 4 varied test questions with results shown"
            },
            "starter_repo_url": None,
            "estimated_hours":  4.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Final Project",
        "slug":              "final-project",
        "description":       "Build a complete Qdrant-powered RAG system from scratch, tying together embeddings, storage, retrieval, and LLM prompting.",
        "order":             12,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   3.0,
        "skill_tags":        ["qdrant", "rag", "sentence-transformers", "llm", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Final Project",
            "content": r"""Congratulations! 🎉 This is the final lesson of our basic Qdrant course. We're going to build a small Qdrant RAG system from scratch. The goal is to understand how all the pieces connect.

## 🏗️ What we're building

Our application will answer questions about a small collection of documents.

```
📄 Documents
     ↓
✂️ Split into chunks
     ↓
🧠 Create embeddings
     ↓
🗄️ Store in Qdrant
     ↓
❓ User asks question
     ↓
🧠 Embed question
     ↓
🔎 Search Qdrant
     ↓
📚 Get relevant chunks
     ↓
🤖 LLM
     ↓
💬 Answer
```

## Step 1 — Install packages

```bash
pip install qdrant-client sentence-transformers
```

For the basic project, that's enough.

## Step 2 — Create our documents

We'll start with simple text.

```python
documents = [
    '''
    Students need 140 credit hours to graduate.
    The required credit hours must be completed
    according to the university study plan.
    ''',

    '''
    Students must maintain the required minimum GPA
    throughout their academic program.
    ''',

    '''
    Course registration takes place before the beginning
    of each semester according to university regulations.
    ''',

    '''
    Students can drop courses according to the
    university's academic regulations.
    ''',

    '''
    Artificial intelligence courses include machine
    learning, deep learning, computer vision,
    and natural language processing.
    '''
]
```

For a real application, these could come from a PDF, Word document, website, or database.

## Step 3 — Load the embedding model

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

Remember: `all-MiniLM-L6-v2` → 384 dimensions.

## Step 4 — Create embeddings

```python
vectors = model.encode(documents)
```

Now each of the 5 documents has a corresponding vector.

## Step 5 — Create Qdrant

For this project we'll use local memory:

```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
```

## Step 6 — Create collection

```python
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="university",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
```

Our structure is now: `Qdrant → university`

## Step 7 — Create Points

```python
from qdrant_client.models import PointStruct

points = []
for i, (text, vector) in enumerate(zip(documents, vectors)):
    points.append(
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={"text": text}
        )
    )
```

Each point contains: `ID`, `Vector`, `Payload`.

## Step 8 — Insert into Qdrant

```python
client.upsert(
    collection_name="university",
    points=points
)
```

Now our knowledge base is stored.

```
                Qdrant
                   │
             university
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    Point 1     Point 2     Point 3
       ↓           ↓           ↓
    Chunk       Chunk       Chunk
```

## Step 9 — Ask a question

```python
question = "How many credit hours do I need to graduate?"
query_vector = model.encode(question)
```

## Step 10 — Search Qdrant

```python
results = client.query_points(
    collection_name="university",
    query=query_vector.tolist(),
    limit=3
)
```

Qdrant returns the most relevant points.

## Step 11 — Extract the context

```python
context = "\n\n".join(
    result.payload["text"]
    for result in results.points
)
```

Now `context` contains the retrieved information, e.g. the credit-hours and GPA requirements text.

## Step 12 — Build the LLM prompt

Now we combine Context + Question:

```python
prompt = f'''
Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Answer:
'''
```

## Step 13 — Send it to an LLM

This part depends on which LLM provider/model you're using. Conceptually:

```python
answer = llm.invoke(prompt)
print(answer)
```

The final answer might be: "Students need 140 credit hours to graduate."

## 🎯 Complete retrieval code

The most important part of the project — retrieval, context-building, and prompt construction — comes together like this:

```python
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Documents
documents = [
    "Students need 140 credit hours to graduate.",
    "Students must maintain the required minimum GPA.",
    "Course registration takes place before the beginning of each semester.",
    "Students can drop courses according to university regulations.",
    "Artificial intelligence courses include machine learning and deep learning.",
]

# 3. Embeddings
vectors = model.encode(documents)

# 4. Qdrant client + collection
client = QdrantClient(":memory:")
client.create_collection(
    collection_name="university",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# 5. Points
points = []
for i, (text, vector) in enumerate(zip(documents, vectors)):
    points.append(PointStruct(id=i, vector=vector.tolist(), payload={"text": text}))

# 6. Insert
client.upsert(collection_name="university", points=points)

# 7. User question
question = "How many credit hours do I need to graduate?"

# 8. Embed question
query_vector = model.encode(question)

# 9. Search
results = client.query_points(
    collection_name="university",
    query=query_vector.tolist(),
    limit=3
)

# 10. Build context
context = "\n\n".join(result.payload["text"] for result in results.points)

# 11. Prompt
prompt = f'''
Answer the question using only the context.

Context:
{context}

Question:
{question}

Answer:
'''

print(prompt)
```

The only missing piece is the LLM call itself.

## 🧠 Now understand the entire system

This is the most important diagram of the whole course:

```
                    DOCUMENTS
                       │
                       ▼
                  CHUNKING
                       │
                       ▼
                EMBEDDING MODEL
                       │
                       ▼
                    VECTORS
                       │
                       ▼
                 ┌──────────┐
                 │  QDRANT  │
                 └────┬─────┘
                      │
                      │
              USER QUESTION
                      │
                      ▼
                EMBEDDING MODEL
                      │
                      ▼
                 QUERY VECTOR
                      │
                      ▼
                   QDRANT
                      │
                      ▼
               TOP-K DOCUMENTS
                      │
                      ▼
                   CONTEXT
                      │
                      ▼
                     LLM
                      │
                      ▼
                  ANSWER
```

## 🏆 Your Qdrant knowledge now

You've learned the core Qdrant concepts:

**Fundamentals:** Vector, Embedding, Collection, Point, Payload

**Qdrant operations:** Create collection, Insert points, Upsert, Retrieve points, Similarity search, Top-K search

**Filtering:** must, should, must_not, Range filters, Metadata filtering

**Storage:** In-memory Qdrant, Persistent local storage, Qdrant server, Docker

**RAG:** Retrieval, Context creation, Qdrant + embeddings, Qdrant + LLM, Complete RAG architecture

## 🎓 The one thing I want you to remember

If someone asks you "What is Qdrant?", your simple answer should be:

> Qdrant is a vector database that stores embeddings and performs similarity search so applications can quickly retrieve information that is semantically relevant to a user's query.

And the basic workflow is:

```
Text → Embedding → Qdrant → Similarity Search → Relevant Text
```
""",
            "order":                12,
            "estimated_minutes":    50,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Trace the Full RAG Pipeline",
                "description":   "Without running any code, write out — in your own words or as comments — each of the 13 steps of the pipeline described in this lesson, from installing packages through sending the prompt to an LLM. For each step, note which Python object or variable it produces (e.g. Step 4 produces `vectors`, Step 10 produces `results`).",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  "# Write one comment per step (1-13) describing what happens and what\n# variable/object it produces. Example:\n# Step 1: Install qdrant-client and sentence-transformers -> no variable, just setup\n",
                "solution_code": "# Step 1: Install qdrant-client and sentence-transformers -> no variable, setup only\n# Step 2: Define the documents list -> `documents`\n# Step 3: Load the embedding model -> `model`\n# Step 4: Encode documents into vectors -> `vectors`\n# Step 5: Create a Qdrant client -> `client`\n# Step 6: Create the \"university\" collection on `client` -> no new variable, side effect on client\n# Step 7: Build PointStruct objects from documents+vectors -> `points`\n# Step 8: Upsert points into Qdrant -> no new variable, side effect (data stored)\n# Step 9: Define the user's question -> `question`\n# Step 10: Embed the question -> `query_vector`\n# Step 11: Search Qdrant with query_points() -> `results`\n# Step 12: Join retrieved payload text into a single string -> `context`\n# Step 13: Build the final prompt combining context + question -> `prompt`\n# (Optional) Step 14: Send `prompt` to an LLM -> `answer`\n",
                "skill_tested":  ["qdrant", "rag", "pipeline-design"],
            },
        ],
        "quiz": {
            "title":         "Final Project Quiz",
            "questions": [
                {
                    "question": "In the complete pipeline, what comes immediately after 'Create embeddings' and before 'Create Qdrant collection'?",
                    "options": [
                        "Send the prompt to the LLM",
                        "Create a Qdrant client",
                        "Build the context string",
                        "Ask the user a question"
                    ],
                    "correct": 1,
                    "explanation": "The pipeline order is: load model → create embeddings → create a Qdrant client → create the collection → create points → insert them."
                },
                {
                    "question": "What does `context = \"\\n\\n\".join(result.payload[\"text\"] for result in results.points)` produce?",
                    "options": [
                        "A single embedding vector combining all results",
                        "A single string joining the text of all retrieved documents, separated by blank lines",
                        "A new Qdrant collection",
                        "A filtered version of the query"
                    ],
                    "correct": 1,
                    "explanation": "This line concatenates the payload 'text' field of every retrieved point into one string, which becomes the context passed to the LLM."
                },
                {
                    "question": "According to the final summary, what is Qdrant's core purpose?",
                    "options": [
                        "To generate natural-language answers directly",
                        "To store embeddings and perform similarity search so applications can retrieve semantically relevant information",
                        "To train embedding models from scratch",
                        "To replace the need for any database"
                    ],
                    "correct": 1,
                    "explanation": "The lesson's summary defines Qdrant as a vector database for storing embeddings and performing similarity search — retrieval, not generation."
                },
                {
                    "question": "Which of these is NOT one of the core Qdrant concepts covered across this course?",
                    "options": [
                        "Point, Payload, Collection",
                        "must, should, must_not filters",
                        "In-memory, local disk, and server storage modes",
                        "Training a custom transformer model from scratch"
                    ],
                    "correct": 3,
                    "explanation": "The course covered Qdrant fundamentals, operations, filtering, storage modes, and RAG integration — it did not cover training a transformer model, which is outside Qdrant's scope entirely."
                },
                {
                    "question": "What is the one missing piece in the 'complete retrieval code' shown in this lesson?",
                    "options": [
                        "The embedding model",
                        "The Qdrant collection creation",
                        "The actual call to an LLM to generate the final answer",
                        "The similarity search step"
                    ],
                    "correct": 2,
                    "explanation": "The lesson builds everything up through constructing the final prompt — the only remaining step is actually calling an LLM with that prompt to get the generated answer."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Capstone: End-to-End Qdrant RAG System",
            "description":      "Build a complete, working RAG system from scratch using everything learned in this course. Choose a real knowledge domain you care about (e.g. your own project's documentation, a set of university policies, a product FAQ, or notes on a technical topic) and build at least 10-15 chunks of source content. Implement the full pipeline: chunk your content, embed it with Sentence Transformers, store it in a Qdrant collection (choose memory, local-disk, or Docker-server mode and justify your choice), implement retrieval with at least one metadata filter in addition to semantic search, build the context + prompt construction step, and connect it to an LLM (a real API if you have one, or a clearly mocked/stubbed call if not) to produce final answers. Test the complete system with at least 6 questions, including at least one that requires the metadata filter to return the right answer and one that should be correctly identified as unanswerable from your knowledge base. Write a short README explaining your architecture choices.",
            "difficulty":       DifficultyLevel.intermediate,
            "tech_stack":       ["Qdrant", "Sentence Transformers", "Python", "LLM API (or mocked)"],
            "objectives": [
                "Chunk and prepare at least 10-15 pieces of real source content",
                "Embed all chunks and store them in a Qdrant collection with justified storage mode (memory/local/server)",
                "Attach meaningful metadata to each chunk's payload (e.g. topic, category, date)",
                "Implement retrieval combining semantic search with at least one metadata filter",
                "Build context assembly and LLM prompt construction following the course's pattern",
                "Connect to a real or mocked LLM call to produce a final generated answer",
                "Test with at least 6 questions, including one requiring the filter and one unanswerable question",
                "Write a short README documenting architecture decisions and trade-offs"
            ],
            "rubric": {
                "correctness": "Full pipeline runs end-to-end without errors, from raw content to generated answer",
                "retrieval_quality": "Semantic search and metadata filtering both work correctly and are demonstrated together",
                "prompt_design": "Context and question are combined into a clear, grounded, hallucination-resistant prompt",
                "edge_cases": "Unanswerable questions are handled explicitly rather than producing a fabricated answer",
                "documentation": "README clearly explains storage mode choice and overall architecture"
            },
            "starter_repo_url": None,
            "estimated_hours":  6.0,
        },
    },
    # ... more topics
]

# ---------------------------------------------------------------------------
# Seed logic — do not modify below this line
# ---------------------------------------------------------------------------
TOPIC_FIELDS = ("title", "slug", "description", "order", "difficulty",
                 "estimated_hours", "skill_tags", "prerequisite_ids")


def seed(db):
    course = db.query(ToolCourse).filter(ToolCourse.slug == TOOL_SLUG).first()
    if not course:
        print(f"✗ ToolCourse '{TOOL_SLUG}' not found — run seed_tool_courses.py first")
        return

    for t in TOPICS:
        topic = db.query(ToolTopic).filter(
            ToolTopic.tool_course_id == course.id,
            ToolTopic.order == t["order"],
        ).first()
        if not topic:
            topic = ToolTopic(tool_course_id=course.id, **{k: t[k] for k in TOPIC_FIELDS})
            db.add(topic)
            db.flush()
            print(f"  + ToolTopic: {topic.title}")
        else:
            print(f"  - ToolTopic exists: {topic.title}, skipping")

        if not db.query(Lesson).filter(Lesson.tool_topic_id == topic.id).first():
            db.add(Lesson(tool_topic_id=topic.id, **t["lesson"]))
            print("    + Lesson added")
        else:
            print("    - Lesson exists, skipping")

        if db.query(Exercise).filter(Exercise.tool_topic_id == topic.id).count() == 0:
            for ex in t["exercises"]:
                db.add(Exercise(tool_topic_id=topic.id, **ex))
            print(f"    + {len(t['exercises'])} exercise(s) added")
        else:
            print("    - Exercises exist, skipping")

        if not db.query(Quiz).filter(Quiz.tool_topic_id == topic.id).first():
            db.add(Quiz(tool_topic_id=topic.id, **t["quiz"]))
            print("    + Quiz added")
        else:
            print("    - Quiz exists, skipping")

        if t.get("project") and not db.query(Project).filter(Project.tool_topic_id == topic.id).first():
            db.add(Project(tool_topic_id=topic.id, **t["project"]))
            print("    + Project added")
        else:
            print("    - Project exists or none for this topic, skipping")

    db.commit()
    print("Done.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
