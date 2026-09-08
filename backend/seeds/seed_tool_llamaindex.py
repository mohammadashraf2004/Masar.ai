"""
backend/seeds/seed_tool_llamaindex.py

Adds topic content (lessons/exercises/quiz/project) to the LlamaIndex
tool course, which already exists as a shell (seeded by
seeds/seed_tool_courses.py). Idempotent — safe to re-run.

Run from backend/:
    docker compose exec api python seeds/seed_tool_llamaindex.py
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

TOOL_SLUG = "llamaindex"  # must already exist — created by seed_tool_courses.py

# ---------------------------------------------------------------------------
# Topics (flat — no levels). Add one dict per topic, in the order they
# should appear.
# ---------------------------------------------------------------------------
TOPICS = [
    {
        # ToolTopic fields
        "title":            "What is LlamaIndex?",
        "slug":              "what-is-llamaindex",
        "description":       "Intro to LlamaIndex: connecting LLMs to your own data, how it compares to LangChain, and the five core concepts (Document, Node, Embedding, Index, Query Engine).",
        "order":             1,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["llamaindex", "rag", "llm", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "What is LlamaIndex?",
            "content":              """Let's start with the simplest possible explanation.

Imagine you have a 100-page PDF.

You ask an AI:

"What are the graduation requirements?"

The AI doesn't automatically know what's inside your PDF.

We need a system that can:

PDF → understand/store information → find relevant information → give it to the LLM → generate an answer

That's where LlamaIndex comes in.

## Simple definition

LlamaIndex is a framework for connecting LLMs to your own data.

Your data could be:

- 📄 PDFs
- 📝 Word documents
- 📃 Text files
- 🗄️ Databases
- 🌐 Websites
- 📊 CSV files
- 🔌 APIs
- and more

## 🧠 Think of LlamaIndex like a librarian

Imagine a huge library.

You ask:

"Find me information about Machine Learning courses."

The librarian:

1. Searches the library
2. Finds relevant books/pages
3. Takes the useful information
4. Gives it to you

LlamaIndex does something similar for your AI application.

```
             YOUR DATA
                 ↓
       ┌──────────────────┐
       │    LlamaIndex    │
       └──────────────────┘
                 ↓
        Find relevant data
                 ↓
              LLM
                 ↓
          Final Answer
```

## 🔥 LlamaIndex vs LangChain

Since you're learning LangChain, this is important.

**LangChain**

LangChain is a general framework for building applications around LLMs.

It gives you things like:

```
LLM
 ↓
Prompt
 ↓
Tools
 ↓
Agents
 ↓
Memory
 ↓
Chains
```

**LlamaIndex**

LlamaIndex is especially focused on connecting LLMs with data.

```
Your Documents
      ↓
  LlamaIndex
      ↓
 Retrieval
      ↓
     LLM
      ↓
   Answer
```

A simple way to remember:

- LangChain = build LLM applications
- LlamaIndex = connect LLMs to your data

There is overlap between them, and you can use them together.

## 🟡 What problem does LlamaIndex solve?

Suppose you have:

`university_rules.pdf`

Inside it:

- Registration Rules
- Graduation Requirements
- GPA Rules
- Course Descriptions
- Tuition Fees

You ask:

"What GPA do I need to graduate?"

Instead of sending the entire PDF to the LLM, LlamaIndex can find the relevant section.

```
PDF
 ↓
Split into smaller pieces
 ↓
Create embeddings
 ↓
Store/index them
 ↓
User asks question
 ↓
Search relevant pieces
 ↓
Send relevant pieces to LLM
 ↓
Answer
```

This is essentially RAG.

## 🧩 The 5 most important LlamaIndex concepts

Don't try to memorize everything yet.

For now, remember these five:

**1. Document**

Represents your original data.

```python
Document(text="LlamaIndex is a framework...")
```

**2. Node**

A smaller piece of a document.

For example:

```
PDF
 ↓
Document
 ↓
Node 1
Node 2
Node 3
Node 4
```

Why? Because searching 100 pages at once isn't efficient.

**3. Embedding**

Converts text into numbers representing its meaning.

For example:

```
"How do I graduate?"
          ↓
   [0.21, -0.15, 0.73, ...]
```

These vectors allow us to search for meaning, not just exact words.

**4. Index**

An index organizes your data so that it can be searched efficiently.

Think:

```
Documents
    ↓
  Index
    ↓
Search
```

**5. Query Engine**

The part that lets the user ask questions.

```python
response = query_engine.query(
    "What are the graduation requirements?"
)
```

And you get:

```
The graduation requirements are...
```

## 🚀 The complete picture

Eventually, you'll build something like this:

```
                PDF
                 ↓
            Documents
                 ↓
              Nodes
                 ↓
            Embeddings
                 ↓
              Index
                 ↓
            Retriever
                 ↓
          Relevant Nodes
                 ↓
               LLM
                 ↓
              Answer
```

Don't worry if some of these words are unfamiliar. We'll learn each one separately.

## 📝 Tiny exercise

Before Lesson 2, remember these:

| Concept | Simple meaning |
|---|---|
| LlamaIndex | Connects LLMs to your data |
| Document | Your original data |
| Node | Small piece of a document |
| Embedding | Meaning represented as numbers |
| Index | Organized searchable data |
| Query Engine | Allows you to ask questions |

## ⭐ One sentence to remember

LlamaIndex helps an LLM find and use information from your own data.
""",
            "order":                1,
            "estimated_minutes":    25,
            "has_code_examples":    False,
        },
        "exercises": [
            # No exercises yet — this lesson is conceptual (no hands-on code).
            # Add here once you provide a coding exercise for this topic.
        ],
        "quiz": {
            "title":         "What is LlamaIndex? Quiz",
            "questions":     [
                {
                    "question": "What is LlamaIndex primarily used for?",
                    "options": [
                        "Connecting LLMs to your own data",
                        "Training new LLMs from scratch",
                        "Hosting LLMs on the cloud",
                        "Building user interfaces for chatbots"
                    ],
                    "correct": 0,
                    "explanation": "LlamaIndex is a framework focused on connecting LLMs to your own data (PDFs, docs, databases, etc.) so they can answer questions using that data."
                },
                {
                    "question": "Which analogy is used in the lesson to describe how LlamaIndex works?",
                    "options": [
                        "A translator",
                        "A librarian",
                        "A calculator",
                        "A search engine ad"
                    ],
                    "correct": 1,
                    "explanation": "The lesson compares LlamaIndex to a librarian who searches a library, finds relevant information, and hands it back to you."
                },
                {
                    "question": "What is the main difference between LangChain and LlamaIndex, according to the lesson?",
                    "options": [
                        "LangChain only works with PDFs, LlamaIndex works with any data",
                        "LangChain is for building LLM applications broadly; LlamaIndex focuses on connecting LLMs to data",
                        "LangChain is newer than LlamaIndex",
                        "They are identical and interchangeable"
                    ],
                    "correct": 1,
                    "explanation": "LangChain = build LLM applications (prompts, tools, agents, memory, chains). LlamaIndex = connect LLMs to your data. They can overlap and be used together."
                },
                {
                    "question": "In LlamaIndex, what is a 'Node'?",
                    "options": [
                        "A server that hosts the LLM",
                        "A smaller piece of a larger Document",
                        "A type of embedding model",
                        "A user query"
                    ],
                    "correct": 1,
                    "explanation": "A Node is a smaller chunk of a Document. Splitting documents into nodes makes searching more efficient than scanning an entire large document at once."
                },
                {
                    "question": "What does an Embedding represent?",
                    "options": [
                        "The file size of a document",
                        "A summary of the document written by the LLM",
                        "Text converted into numbers that represent its meaning",
                        "The metadata tags of a document"
                    ],
                    "correct": 2,
                    "explanation": "An embedding converts text into a vector of numbers representing its meaning, which allows searching by semantic similarity rather than exact keyword matches."
                },
                {
                    "question": "What does a Query Engine do?",
                    "options": [
                        "Stores raw PDF files",
                        "Lets the user ask questions and returns an answer using the indexed data",
                        "Converts embeddings back into text",
                        "Trains the LLM on new data"
                    ],
                    "correct": 1,
                    "explanation": "The Query Engine is the component that lets a user ask a question (e.g., query_engine.query(...)) and returns a generated answer based on relevant retrieved data."
                },
                {
                    "question": "The overall retrieval pattern described in this lesson (PDF → chunks → embeddings → index → search → LLM → answer) is essentially known as:",
                    "options": [
                        "Fine-tuning",
                        "RAG (Retrieval-Augmented Generation)",
                        "Prompt chaining",
                        "Reinforcement learning"
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly states: 'This is essentially RAG' — Retrieval-Augmented Generation, where relevant data is retrieved and passed to the LLM to generate an answer."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Installation + Your First LlamaIndex App",
        "slug":              "installation-first-llamaindex-app",
        "description":       "Install LlamaIndex in a virtual environment and build your first tiny program using the Document class.",
        "order":             2,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   0.75,
        "skill_tags":        ["llamaindex", "python", "setup"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Installation + Your First LlamaIndex App",
            "content":              """Today we'll do only two things:

1. Install LlamaIndex
2. Build your first tiny LlamaIndex program

## 1. What are we trying to build?

We want this:

```
Your text
   ↓
LlamaIndex
   ↓
Question
   ↓
Answer
```

For now, we'll keep it extremely simple.

## 2. Install LlamaIndex

Create a virtual environment if you don't already have one:

```bash
python -m venv .venv
```

Activate it on Linux/WSL:

```bash
source .venv/bin/activate
```

Then install LlamaIndex:

```bash
pip install llama-index
```

Check that it works:

```bash
python -c "import llama_index; print('LlamaIndex works!')"
```

You should see:

```
LlamaIndex works!
```

## 3. Your first LlamaIndex program

Create `main.py`. Put this inside:

```python
from llama_index.core import Document

document = Document(
    text="LlamaIndex helps developers build applications using their own data."
)
print(document.text)
```

Run:

```bash
python main.py
```

You should get:

```
LlamaIndex helps developers build applications using their own data.
```

🎉 Congratulations! You just created your first LlamaIndex `Document`.

## 4. What did we just do?

This line:

```python
from llama_index.core import Document
```

imports the `Document` class.

Then:

```python
document = Document(
    text="LlamaIndex helps developers build applications using their own data."
)
```

creates a LlamaIndex document.

Think of it as:

```
Document
   │
   └── Your data
```

For example:

```python
document = Document(text="Python is a programming language.")
```

or:

```python
document = Document(text="Mansoura University offers AI Engineering.")
```

The document can contain your own information.

## 5. Why is `Document` important?

Later, instead of manually putting text into your program, you'll load real data:

```
PDF
Word
Website
CSV
Database
     ↓
  Document
     ↓
  LlamaIndex
```

For example:

```
university_rules.pdf
        ↓
     Document
        ↓
      Nodes
        ↓
      Index
        ↓
    Retriever
        ↓
       LLM
```

That's where LlamaIndex becomes really useful.

## 6. One important idea

Don't confuse:

**Document** — The original piece of data.

**Node** — A smaller piece of that document.

Imagine a 100-page PDF:

```
PDF
 │
 └── Document
       │
       ├── Node 1
       ├── Node 2
       ├── Node 3
       ├── Node 4
       └── ...
```

We'll learn Nodes in Lesson 3.

## 🧠 Remember

For this lesson, you only need to remember:

```
LlamaIndex
    ↓
Document
    ↓
Your data
```

And the basic code:

```python
from llama_index.core import Document

document = Document(text="Hello LlamaIndex!")
print(document.text)
```

That's it. Don't worry about embeddings, vector databases, RAG, agents, or anything else yet.
""",
            "order":                2,
            "estimated_minutes":    20,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Create Your Own Document",
                "description":   "Install llama-index in a virtual environment, then write a script that creates a Document containing a sentence about your own university or field of study, and prints its text.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  """from llama_index.core import Document

# TODO: create a Document with text about your university or field of study
document = ___

# TODO: print the document's text
""",
                "solution_code": """from llama_index.core import Document

document = Document(
    text="Mansoura University offers AI Engineering."
)
print(document.text)
""",
                "skill_tested":  ["llamaindex", "document"],
            },
        ],
        "quiz": {
            "title":         "Installation + Your First LlamaIndex App Quiz",
            "questions":     [
                {
                    "question": "Which pip command installs LlamaIndex?",
                    "options": [
                        "pip install llamaindex-core",
                        "pip install llama-index",
                        "pip install llama_index_sdk",
                        "pip install index-llama"
                    ],
                    "correct": 1,
                    "explanation": "LlamaIndex is installed with `pip install llama-index`."
                },
                {
                    "question": "What class did we import to create our first LlamaIndex program?",
                    "options": [
                        "Node",
                        "Index",
                        "Document",
                        "QueryEngine"
                    ],
                    "correct": 2,
                    "explanation": "We imported `Document` from `llama_index.core` to represent our original piece of data."
                },
                {
                    "question": "What does `document.text` return in the example?",
                    "options": [
                        "A list of Nodes",
                        "The embedding vector of the document",
                        "The raw text string that was passed into the Document",
                        "A query engine object"
                    ],
                    "correct": 2,
                    "explanation": "`document.text` simply returns the raw text string you passed in when creating the Document."
                },
                {
                    "question": "According to the lesson, what's the key difference between a Document and a Node?",
                    "options": [
                        "A Document is a smaller piece of a Node",
                        "A Node is a smaller piece of a Document",
                        "They are the exact same thing",
                        "A Node only exists in databases, not PDFs"
                    ],
                    "correct": 1,
                    "explanation": "A Document is the original piece of data; a Node is a smaller piece of that document. Nodes are covered in Lesson 3."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Documents + Nodes",
        "slug":              "documents-and-nodes",
        "description":       "Understand how large documents are split into smaller, searchable Nodes using SentenceSplitter, chunk_size, and chunk_overlap.",
        "order":             3,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["llamaindex", "nodes", "chunking", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Documents + Nodes",
            "content":              """Today we'll understand one very important idea:

A Document is the whole data. A Node is a smaller piece of that data.

## 1. Why do we need Nodes?

Imagine you have a 100-page PDF.

You don't want to search the entire PDF every time the user asks a question.

Instead:

```
100-page PDF
     ↓
  Document
     ↓
 ┌───────┬───────┬───────┬───────┐
 │ Node1 │ Node2 │ Node3 │ Node4 │ ...
 └───────┴───────┴───────┴───────┘
```

Each Node contains a smaller piece of information.

## 2. Simple example

Suppose our document says:

- Python is a programming language.
- Python is widely used in artificial intelligence.
- Python has libraries such as NumPy and Pandas.
- Python can also be used for web development.

We can split it into:

- Node 1: Python is a programming language.
- Node 2: Python is widely used in artificial intelligence.
- Node 3: Python has libraries such as NumPy and Pandas.
- Node 4: Python can also be used for web development.

Now if someone asks:

"What libraries does Python have?"

We can retrieve Node 3 instead of searching everything.

## 3. Creating Nodes

LlamaIndex provides tools for splitting documents.

First:

```python
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
```

Create a document:

```python
document = Document(
    text=\"\"\"
    Python is a programming language.

    Python is widely used in artificial intelligence.

    Python has libraries such as NumPy and Pandas.

    Python can also be used for web development.
    \"\"\"
)
```

Now create a splitter:

```python
splitter = SentenceSplitter(
    chunk_size=50,
    chunk_overlap=10
)
```

Then create Nodes:

```python
nodes = splitter.get_nodes_from_documents(
    [document]
)
```

Finally:

```python
for node in nodes:
    print(node.text)
    print("-----")
```

## 4. What is chunk_size?

This is important.

`chunk_size=50` means: try to keep each chunk around 50 tokens.

Think:

```
Large document
      ↓
   chunk_size
      ↓
Smaller pieces
```

If you make it too large, you may retrieve lots of unnecessary information.

If you make it too small, you may lose important context.

So we normally choose a reasonable chunk size.

## 5. What is chunk_overlap?

Suppose we have:

- Node 1: Python is useful for AI and machine learning.
- Node 2: Machine learning allows computers to learn from data.

There can be some overlap between them.

Why? Because we don't want important information to get cut between two chunks.

## 6. The complete example

Try this:

```python
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


document = Document(
    text=\"\"\"
    Python is a programming language.

    Python is widely used in artificial intelligence.

    Python has libraries such as NumPy and Pandas.

    Python can also be used for web development.
    \"\"\"
)


splitter = SentenceSplitter(
    chunk_size=50,
    chunk_overlap=10
)


nodes = splitter.get_nodes_from_documents([document])


for i, node in enumerate(nodes):
    print(f"Node {i + 1}:")
    print(node.text)
    print("-----")
```

## 🧠 The important picture

Remember this:

```
             DOCUMENT
                 │
                 ↓
           Splitter
                 │
                 ↓
       ┌─────────┼─────────┐
       ↓         ↓         ↓
     Node 1    Node 2    Node 3
       │         │         │
       └─────────┼─────────┘
                 ↓
           Later: Index
```

You don't need to memorize the code yet.

Just understand:

- Document = whole information
- Node = smaller searchable piece
""",
            "order":                3,
            "estimated_minutes":    35,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Split a Document into Nodes",
                "description":   "Create a Document containing three pieces of information about LlamaIndex, split it into Nodes using SentenceSplitter, and print each Node.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  """from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

# TODO: create a document containing these three pieces of information:
# 1. LlamaIndex is used for RAG.
# 2. LlamaIndex can work with documents.
# 3. LlamaIndex can connect LLMs to external data.
document = ___

# TODO: create a splitter with a reasonable chunk_size and chunk_overlap
splitter = ___

# TODO: split the document into nodes
nodes = ___

# TODO: print each node's text
""",
                "solution_code": """from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

document = Document(
    text=\"\"\"
    LlamaIndex is used for RAG.

    LlamaIndex can work with documents.

    LlamaIndex can connect LLMs to external data.
    \"\"\"
)

splitter = SentenceSplitter(
    chunk_size=50,
    chunk_overlap=10
)

nodes = splitter.get_nodes_from_documents([document])

for i, node in enumerate(nodes):
    print(f"Node {i + 1}:")
    print(node.text)
    print("-----")
""",
                "skill_tested":  ["llamaindex", "nodes", "sentencesplitter"],
            },
        ],
        "quiz": {
            "title":         "Documents + Nodes Quiz",
            "questions":     [
                {
                    "question": "What is the relationship between a Document and a Node?",
                    "options": [
                        "A Node contains many Documents",
                        "A Document is a smaller piece of a Node",
                        "A Node is a smaller piece of a Document",
                        "They are unrelated concepts"
                    ],
                    "correct": 2,
                    "explanation": "A Document is the whole data; a Node is a smaller piece of that data, created by splitting the document."
                },
                {
                    "question": "Which class is used in the lesson to split a Document into Nodes?",
                    "options": [
                        "DocumentSplitter",
                        "SentenceSplitter",
                        "NodeBuilder",
                        "TextChunker"
                    ],
                    "correct": 1,
                    "explanation": "`SentenceSplitter` from `llama_index.core.node_parser` is used to split documents into nodes."
                },
                {
                    "question": "What does chunk_size roughly control?",
                    "options": [
                        "How many documents can be loaded at once",
                        "How many tokens are kept in each chunk/node",
                        "The number of LLM calls made",
                        "The embedding model's vector dimensions"
                    ],
                    "correct": 1,
                    "explanation": "chunk_size controls approximately how many tokens are kept in each chunk (node). Too large wastes context; too small loses important context."
                },
                {
                    "question": "Why does chunk_overlap exist?",
                    "options": [
                        "To make indexing slower",
                        "To duplicate the entire document for backup",
                        "To avoid cutting important information between two chunks",
                        "To reduce the number of nodes created"
                    ],
                    "correct": 2,
                    "explanation": "chunk_overlap lets consecutive nodes share a bit of text so important information isn't lost when it falls near a chunk boundary."
                },
                {
                    "question": "Which method is used to actually generate Nodes from a list of Documents?",
                    "options": [
                        "splitter.get_nodes_from_documents([document])",
                        "document.to_nodes()",
                        "Node.create(document)",
                        "splitter.split(document)"
                    ],
                    "correct": 0,
                    "explanation": "The lesson uses `splitter.get_nodes_from_documents([document])` to generate the list of Node objects."
                },
                {
                    "question": "If chunk_size is set far too large for a big document, what's the likely downside?",
                    "options": [
                        "The document will fail to load",
                        "You may retrieve lots of unnecessary information per node",
                        "Nodes will no longer contain any text",
                        "chunk_overlap will be ignored automatically"
                    ],
                    "correct": 1,
                    "explanation": "Very large chunks mean each node holds more (potentially irrelevant) content, reducing the precision of retrieval."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Embeddings + Vector Stores",
        "slug":              "embeddings-and-vector-stores",
        "description":       "How embeddings turn text into vectors of meaning, how vector stores hold them, and how similarity search finds relevant nodes for a question.",
        "order":             4,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["llamaindex", "embeddings", "vector-store", "rag"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Embeddings + Vector Stores",
            "content":              """This is one of the most important concepts in RAG.

Don't worry — I'll make it simple.

## 1. The problem

Suppose your document contains:

"Python is commonly used for artificial intelligence."

The user asks:

"What programming language is popular for AI?"

The words aren't exactly the same.

Document: "Python is commonly used for artificial intelligence."

Question: "What programming language is popular for AI?"

A simple keyword search might struggle.

We want the computer to understand that these two sentences have similar meaning.

That's what embeddings help us do.

## 2. What is an embedding?

An embedding converts text into numbers.

For example:

```
"Python is used for AI"
          ↓
      Embedding
          ↓
[0.21, -0.13, 0.87, 0.42, ...]
```

Another sentence:

```
"Python is popular in artificial intelligence"
          ↓
      Embedding
          ↓
[0.20, -0.12, 0.85, 0.44, ...]
```

The vectors are relatively close because their meanings are similar.

## 3. Think of a map 🗺️

Imagine every sentence gets a location on a giant map.

```
                   AI
                    ↑
                    │
       Python ●     │    ● Machine Learning
                    │
                    │
             ● JavaScript
                    │
                    └──────────────→
```

Similar concepts are placed near each other.

So "Python is used for AI" and "Python is popular for machine learning" might be close together.

But "How to cook pasta" would probably be far away.

## 4. What is a Vector Store?

Now we have lots of embeddings. We need somewhere to store them.

That's a vector store.

Think:

```
Documents
   ↓
Nodes
   ↓
Embeddings
   ↓
Vector Store
```

The vector store allows us to search for vectors that are similar to our question.

## 5. The RAG search process

Suppose we have:

- Node 1 → Python is used for AI
- Node 2 → Cats are mammals
- Node 3 → Cairo is the capital of Egypt
- Node 4 → Python has NumPy and Pandas

We create embeddings:

- Node 1 → [0.2, 0.8, ...]
- Node 2 → [0.9, 0.1, ...]
- Node 3 → [0.7, 0.2, ...]
- Node 4 → [0.3, 0.7, ...]

User asks: "What is Python used for?"

The question also becomes an embedding:

```
Question
   ↓
[0.25, 0.79, ...]
```

Then we compare it with the stored vectors.

The closest nodes might be: Node 1 ⭐ and Node 4 ⭐

Those are sent to the LLM.

## 6. The complete picture

This is extremely important:

```
             DOCUMENT
                 ↓
               NODES
                 ↓
             EMBEDDING
                 ↓
           VECTOR STORE
                 ↓
          ┌─────────────┐
Question →│ Similarity  │
          │   Search    │
          └─────────────┘
                 ↓
        Relevant Nodes
                 ↓
                LLM
                 ↓
              Answer
```

This is the foundation of RAG.

## 7. A simple LlamaIndex example

LlamaIndex can create a vector index for us.

```python
from llama_index.core import VectorStoreIndex
```

Suppose we have:

```python
from llama_index.core import Document

document = Document(
    text=\"\"\"
    Python is widely used in artificial intelligence.
    Python has libraries such as NumPy and Pandas.
    \"\"\"
)
```

Then:

```python
index = VectorStoreIndex.from_documents(
    [document]
)
```

That's it. LlamaIndex handles much of the work:

```
Document
   ↓
Nodes
   ↓
Embeddings
   ↓
Vector Index
```

## 8. But where did the embeddings come from?

Good question. LlamaIndex needs an embedding model.

There are many choices:

- OpenAI embeddings
- Hugging Face embeddings
- Cohere embeddings
- Local embedding models

For example, you might eventually use `intfloat/multilingual-e5-large` — particularly useful when working with multiple languages.

But don't worry about choosing an embedding model yet. We'll handle that when we build the actual RAG system.

## 🧠 Three things to remember

**Embedding** — Converts text into numbers representing its meaning.

**Vector Store** — Stores those numerical representations so we can search them.

**Similarity Search** — Finds the stored vectors that are most similar to the user's question.

## 🎯 Simple analogy

Think about Google Maps:

- Embedding = GPS coordinates
- Vector Store = Map
- Similarity Search = Find places near me

Similarly:

```
Text
 ↓
Embedding
 ↓
Vector Store
 ↓
Find similar text
```

## ⭐ The most important concept

If you remember only one thing from today's lesson:

Embeddings turn text into vectors so we can find text with similar meaning.
""",
            "order":                4,
            "estimated_minutes":    30,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Build a Vector Index from a Document",
                "description":   "Create a Document about Python and AI, then build a VectorStoreIndex from it using LlamaIndex.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  """from llama_index.core import Document, VectorStoreIndex

# TODO: create a document about Python being used in AI, with libraries like NumPy and Pandas
document = ___

# TODO: build a VectorStoreIndex from the document
index = ___
""",
                "solution_code": """from llama_index.core import Document, VectorStoreIndex

document = Document(
    text=\"\"\"
    Python is widely used in artificial intelligence.
    Python has libraries such as NumPy and Pandas.
    \"\"\"
)

index = VectorStoreIndex.from_documents([document])
""",
                "skill_tested":  ["llamaindex", "embeddings", "vectorstoreindex"],
            },
        ],
        "quiz": {
            "title":         "Embeddings + Vector Stores Quiz",
            "questions":     [
                {
                    "question": "Why do we need embeddings when the user's question doesn't use the exact same words as the document?",
                    "options": [
                        "Embeddings fix spelling errors in the question",
                        "Embeddings let us compare meaning rather than exact keywords",
                        "Embeddings translate the question into another language",
                        "Embeddings compress the document to save storage"
                    ],
                    "correct": 1,
                    "explanation": "Embeddings convert text into vectors representing meaning, so semantically similar sentences end up close together even if the wording differs."
                },
                {
                    "question": "What does an embedding model actually output for a piece of text?",
                    "options": [
                        "A shorter summary of the text",
                        "A list/vector of numbers representing meaning",
                        "A translated version of the text",
                        "A yes/no relevance score"
                    ],
                    "correct": 1,
                    "explanation": "An embedding converts text into a vector of numbers (e.g. [0.21, -0.13, 0.87, ...]) that represents its meaning."
                },
                {
                    "question": "What is the purpose of a Vector Store?",
                    "options": [
                        "To store the original raw PDF files only",
                        "To store embeddings so they can be searched for similarity",
                        "To store the final LLM-generated answers",
                        "To store user login credentials"
                    ],
                    "correct": 1,
                    "explanation": "A vector store holds the numerical embeddings so the system can later search for vectors similar to a user's question."
                },
                {
                    "question": "In the Google Maps analogy from the lesson, what does 'Similarity Search' correspond to?",
                    "options": [
                        "The map itself",
                        "The GPS coordinates",
                        "Finding places near me",
                        "The road network"
                    ],
                    "correct": 2,
                    "explanation": "The lesson maps Embedding → GPS coordinates, Vector Store → Map, and Similarity Search → 'Find places near me.'"
                },
                {
                    "question": "Which LlamaIndex class is shown for creating a vector index from documents?",
                    "options": [
                        "EmbeddingIndex",
                        "VectorStoreIndex",
                        "DocumentIndex",
                        "SimilarityIndex"
                    ],
                    "correct": 1,
                    "explanation": "`VectorStoreIndex.from_documents([document])` is used to build the index, handling node splitting and embedding creation internally."
                },
                {
                    "question": "After embedding a question and comparing it to stored node embeddings, what gets sent to the LLM?",
                    "options": [
                        "Every node in the vector store, regardless of relevance",
                        "Only the single closest node, always exactly one",
                        "The most relevant (closest) nodes found via similarity search",
                        "The raw embedding vectors, not the text"
                    ],
                    "correct": 2,
                    "explanation": "The nodes whose embeddings are closest to the question's embedding are considered most relevant and are passed along to the LLM to generate an answer."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Index + Query Engine",
        "slug":              "index-and-query-engine",
        "description":       "Connect Documents, Nodes, and Embeddings via a VectorStoreIndex, and use a Query Engine to ask questions and get answers — your first RAG-style application.",
        "order":             5,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["llamaindex", "index", "query-engine", "rag", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Index + Query Engine",
            "content":              """Great. Now we're going to connect the pieces from the previous lessons.

By the end, you'll have your first LlamaIndex question-answering system. 🎯

## 1. What is an Index?

We already learned that we have:

```
Document
   ↓
Nodes
   ↓
Embeddings
```

Now we need something that organizes all this information for searching.

That's the Index.

Think of an index like the index at the back of a textbook.

```
📖 Book
   ↓
📑 Index
   ↓
Find what you're looking for quickly
```

In LlamaIndex:

```
Documents
    ↓
   Index
    ↓
Searchable information
```

## 2. VectorStoreIndex

The most common index you'll use for RAG is `VectorStoreIndex`.

Import it:

```python
from llama_index.core import VectorStoreIndex
```

Then:

```python
index = VectorStoreIndex.from_documents(
    documents
)
```

LlamaIndex handles a lot of work for you:

```
Documents
    ↓
Split into Nodes
    ↓
Create Embeddings
    ↓
Store in Vector Index
```

## 3. What is a Query Engine?

Now we have our data indexed. But how do we ask questions?

That's where the Query Engine comes in.

Think:

```
Index
  ↓
Query Engine
  ↓
Question
  ↓
Answer
```

Create one:

```python
query_engine = index.as_query_engine()
```

Then ask:

```python
response = query_engine.query(
    "What is Python used for?"
)
print(response)
```

The Query Engine handles the retrieval process for you.

## 4. Your first complete example 🚀

Create a file `rag.py`. Put this inside:

```python
from llama_index.core import Document, VectorStoreIndex


documents = [
    Document(
        text=\"\"\"
        Python is a popular programming language.
        It is widely used in artificial intelligence,
        machine learning, data science, and web development.
        \"\"\"
    ),
    Document(
        text=\"\"\"
        LlamaIndex is a framework for building applications
        that connect large language models with external data.
        \"\"\"
    )
]


index = VectorStoreIndex.from_documents(documents)


query_engine = index.as_query_engine()


response = query_engine.query(
    "What is Python used for?"
)


print(response)
```

## 5. What's happening?

Let's break it down.

**Step 1 — Create documents**

```python
documents = [
    Document(...),
    Document(...)
]
```

We have our data.

**Step 2 — Create the index**

```python
index = VectorStoreIndex.from_documents(documents)
```

LlamaIndex processes the documents. Conceptually:

```
Documents
    ↓
Nodes
    ↓
Embeddings
    ↓
Vector Index
```

**Step 3 — Create Query Engine**

```python
query_engine = index.as_query_engine()
```

Now we have something that can answer questions using the indexed data.

**Step 4 — Ask a question**

```python
response = query_engine.query(
    "What is Python used for?"
)
```

The query engine searches for relevant information.

**Step 5 — Print the answer**

```python
print(response)
```

You should get something similar to:

"Python is used in artificial intelligence, machine learning, data science, and web development."

🎉 You just built a tiny RAG-style application!

## 6. What's happening behind the scenes?

This simple line:

```python
response = query_engine.query("What is Python used for?")
```

actually represents several steps:

```
                  Question
                     ↓
          "What is Python used for?"
                     ↓
                 Embedding
                     ↓
              Similarity Search
                     ↓
             Relevant Nodes
                     ↓
                   LLM
                     ↓
                  Answer
```

You don't have to manually implement all of that. LlamaIndex does much of it for you.

## 7. The big picture 🧠

You've now learned the basic LlamaIndex pipeline:

```
                 YOUR DATA
                     ↓
                 Documents
                     ↓
                   Nodes
                     ↓
                Embeddings
                     ↓
              VectorStoreIndex
                     ↓
                Query Engine
                     ↑
                     │
                  Question
                     ↓
                   Answer
```

This is the foundation for everything we'll do later.

## ⚠️ One important thing

You might run the code and encounter an error related to an LLM API key.

That's normal.

Why? Because LlamaIndex needs an LLM to generate the final answer.

The architecture is:

```
Vector Index
     ↓
Find relevant information
     ↓
LLM
     ↓
Generate answer
```

We'll properly configure the LLM when we build our RAG application.

For now, focus on understanding the architecture.

## 🧠 Remember these two lines

The most important code from today's lesson:

```python
index = VectorStoreIndex.from_documents(documents)
```

and:

```python
query_engine = index.as_query_engine()
```

Then:

```python
response = query_engine.query("Your question")
```

That's the basic LlamaIndex workflow.
""",
            "order":                5,
            "estimated_minutes":    35,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Build a Tiny Question-Answering App",
                "description":   "Create documents about Egypt (country, capital, and Alexandria), build a VectorStoreIndex, create a query engine, and ask 'What is the capital of Egypt?'. Expect an answer mentioning Cairo.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  """from llama_index.core import Document, VectorStoreIndex

# TODO: create three documents:
# 1. "Egypt is a country in North Africa."
# 2. "Cairo is the capital of Egypt."
# 3. "Alexandria is a major city on the Mediterranean coast."
documents = [
    ___,
    ___,
    ___,
]

# TODO: build the index
index = ___

# TODO: create a query engine
query_engine = ___

# TODO: ask "What is the capital of Egypt?" and print the response
""",
                "solution_code": """from llama_index.core import Document, VectorStoreIndex

documents = [
    Document(text="Egypt is a country in North Africa."),
    Document(text="Cairo is the capital of Egypt."),
    Document(text="Alexandria is a major city on the Mediterranean coast."),
]

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

response = query_engine.query("What is the capital of Egypt?")
print(response)
""",
                "skill_tested":  ["llamaindex", "index", "query-engine", "rag"],
            },
        ],
        "quiz": {
            "title":         "Index + Query Engine Quiz",
            "questions":     [
                {
                    "question": "What analogy does the lesson use to explain what an Index does?",
                    "options": [
                        "A GPS system",
                        "The index at the back of a textbook",
                        "A librarian's card catalog drawer",
                        "A search engine homepage"
                    ],
                    "correct": 1,
                    "explanation": "The lesson compares an Index to the index at the back of a textbook — it helps you find what you're looking for quickly."
                },
                {
                    "question": "Which line of code creates a VectorStoreIndex from a list of documents?",
                    "options": [
                        "index = VectorStoreIndex(documents)",
                        "index = VectorStoreIndex.from_documents(documents)",
                        "index = documents.to_index()",
                        "index = build_index(documents)"
                    ],
                    "correct": 1,
                    "explanation": "`VectorStoreIndex.from_documents(documents)` is the method used to build the index, handling node splitting and embedding internally."
                },
                {
                    "question": "How do you create a Query Engine from an index?",
                    "options": [
                        "index.query_engine()",
                        "QueryEngine(index)",
                        "index.as_query_engine()",
                        "index.get_engine()"
                    ],
                    "correct": 2,
                    "explanation": "Calling `index.as_query_engine()` returns a query engine object that can handle retrieval for you."
                },
                {
                    "question": "Behind the scenes, what happens between the question being asked and the answer being generated?",
                    "options": [
                        "The question is embedded, compared via similarity search, relevant nodes are found, then sent to the LLM",
                        "The question is directly matched against document filenames",
                        "The entire document set is re-read from disk each time with no embeddings involved",
                        "The LLM generates an answer with no retrieval step at all"
                    ],
                    "correct": 0,
                    "explanation": "The pipeline is: Question → Embedding → Similarity Search → Relevant Nodes → LLM → Answer."
                },
                {
                    "question": "Why might you get an error related to an LLM API key when running the query engine example?",
                    "options": [
                        "Because VectorStoreIndex requires a paid license",
                        "Because LlamaIndex needs an LLM to generate the final answer, and it isn't configured yet",
                        "Because Documents cannot be created without an API key",
                        "Because embeddings always require an API key by design"
                    ],
                    "correct": 1,
                    "explanation": "The query engine needs an LLM to generate the final answer from the retrieved nodes; the lesson notes this will be properly configured later when building the full RAG app."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Build Your First Real RAG",
        "slug":              "build-your-first-real-rag",
        "description":       "Put Documents, Nodes, Embeddings, Index, and Query Engine together to build a complete Retrieval-Augmented Generation (RAG) pipeline that answers questions from a university knowledge base.",
        "order":             6,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.25,
        "skill_tags":        ["llamaindex", "rag", "query-engine", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Build Your First Real RAG",
            "content":              """Now we put everything together.

By the end of this lesson, you'll understand the complete RAG pipeline in LlamaIndex.

## 1. What is RAG?

RAG stands for: **Retrieval-Augmented Generation**

Don't let the name scare you.

It simply means:

Find relevant information first, then give that information to the LLM to generate an answer.

**Without RAG**

Imagine you ask an LLM:

"What are the rules in my university document?"

The LLM doesn't automatically know your private document.

```
Question
   ↓
LLM
   ↓
"I don't know..."
```

**With RAG**

```
Question
   ↓
Search your documents
   ↓
Find relevant information
   ↓
Give it to LLM
   ↓
Generate answer
```

That's RAG.

## 2. Our example

Let's pretend we have a university document containing:

- The AI Engineering program requires students to complete 160 credit hours.
- Students must complete all required courses before graduation.
- The minimum GPA required for graduation is 2.0.

Our user asks:

"How many credit hours are required?"

Our system should find the credit-hours sentence and use that information to answer.

## 3. Create the document

Create `rag.py`. Start with:

```python
from llama_index.core import Document
```

Then:

```python
document = Document(
    text=\"\"\"
    The AI Engineering program requires students to complete
    160 credit hours.

    Students must complete all required courses before graduation.

    The minimum GPA required for graduation is 2.0.
    \"\"\"
)
```

## 4. Create the index

```python
from llama_index.core import VectorStoreIndex


index = VectorStoreIndex.from_documents(
    [document]
)
```

Remember what happens conceptually:

```
Document
   ↓
Nodes
   ↓
Embeddings
   ↓
Vector Index
```

## 5. Create the Query Engine

```python
query_engine = index.as_query_engine()
```

Now we can ask questions.

## 6. Ask a question

```python
response = query_engine.query(
    "How many credit hours are required?"
)

print(response)
```

The system retrieves the relevant information and generates an answer, something like:

"The AI Engineering program requires 160 credit hours."

🎉 You have built your first RAG application!

## 7. The complete code

```python
from llama_index.core import Document, VectorStoreIndex


document = Document(
    text=\"\"\"
    The AI Engineering program requires students to complete
    160 credit hours.

    Students must complete all required courses before graduation.

    The minimum GPA required for graduation is 2.0.
    \"\"\"
)


index = VectorStoreIndex.from_documents(
    [document]
)


query_engine = index.as_query_engine()


response = query_engine.query(
    "How many credit hours are required?"
)


print(response)
```

## 8. Let's ask different questions

You can reuse the same `query_engine`.

**Question 1**

```python
query_engine.query("What GPA is required for graduation?")
```

Expected idea: "The minimum GPA required is 2.0."

**Question 2**

```python
query_engine.query("What must students complete before graduation?")
```

Expected idea: "Students must complete all required courses."

## 9. What's actually happening?

This is the most important part of today's lesson.

When you ask "What GPA is required for graduation?", LlamaIndex roughly does:

```
                 USER QUESTION
                       ↓
              Create embedding
                       ↓
                 Search index
                       ↓
             Find relevant Node
                       ↓
        "The minimum GPA ... 2.0"
                       ↓
                 Send context
                       ↓
                      LLM
                       ↓
                    Answer
```

This is Retrieval-Augmented Generation.

## 10. Why not just send the whole document?

Imagine your document is 10,000 pages.

Sending all 10,000 pages to the LLM would be inefficient.

Instead:

```
10,000 pages
      ↓
    Nodes
      ↓
Question
      ↓
Retrieve 3 relevant Nodes
      ↓
      LLM
      ↓
    Answer
```

That's one of the main reasons RAG is useful.

## 11. RAG in one picture

Memorize this:

```
                YOUR DATA
                    ↓
                Documents
                    ↓
                  Nodes
                    ↓
                Embeddings
                    ↓
               Vector Index
                    ↓
                  Search
                    ↑
                    │
                 Question
                    ↓
            Relevant Context
                    ↓
                   LLM
                    ↓
                 Answer
```

This diagram will become extremely familiar as we continue.

## 12. Important: RAG ≠ LlamaIndex

Don't confuse them.

**RAG** — A technique/architecture: Retrieve → Augment → Generate

**LlamaIndex** — A framework that helps you implement systems like RAG.

So: RAG = concept, LlamaIndex = tool/framework.

## 🧠 What you've learned so far

You now know:

- Document → your data
- Node → smaller piece of data
- Embedding → numerical representation of meaning
- Vector Store/Index → searchable information
- Query Engine → asks questions
- RAG → retrieve information + generate answer

That's already the core of many RAG applications.
""",
            "order":                6,
            "estimated_minutes":    40,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Build an AI Engineering Knowledge Base",
                "description":   "Create a small knowledge base about Python, machine learning, deep learning, and LlamaIndex. Build an index and query engine, then ask three different questions against it.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  """from llama_index.core import Document, VectorStoreIndex

# TODO: create a document containing these facts:
# 1. Python is commonly used for AI and machine learning.
# 2. Machine learning allows computers to learn patterns from data.
# 3. Deep learning uses neural networks with multiple layers.
# 4. LlamaIndex helps connect LLMs with external data.
document = ___

# TODO: build the index and query engine
index = ___
query_engine = ___

# TODO: ask these three questions and print each response
# "What is deep learning?"
# "What is LlamaIndex used for?"
# "What is Python commonly used for?"
""",
                "solution_code": """from llama_index.core import Document, VectorStoreIndex

document = Document(
    text=\"\"\"
    Python is commonly used for AI and machine learning.

    Machine learning allows computers to learn patterns from data.

    Deep learning uses neural networks with multiple layers.

    LlamaIndex helps connect LLMs with external data.
    \"\"\"
)

index = VectorStoreIndex.from_documents([document])
query_engine = index.as_query_engine()

for question in [
    "What is deep learning?",
    "What is LlamaIndex used for?",
    "What is Python commonly used for?",
]:
    response = query_engine.query(question)
    print(f"Q: {question}")
    print(f"A: {response}")
    print("-----")
""",
                "skill_tested":  ["llamaindex", "rag", "query-engine"],
            },
        ],
        "quiz": {
            "title":         "Build Your First Real RAG Quiz",
            "questions":     [
                {
                    "question": "What does RAG stand for?",
                    "options": [
                        "Retrieval-Augmented Generation",
                        "Rapid AI Generation",
                        "Retrieval and Grading",
                        "Recursive Answer Generation"
                    ],
                    "correct": 0,
                    "explanation": "RAG stands for Retrieval-Augmented Generation: find relevant information first, then give it to the LLM to generate an answer."
                },
                {
                    "question": "Without RAG, why might an LLM fail to answer a question about your private university document?",
                    "options": [
                        "The LLM refuses to answer questions about universities",
                        "The LLM doesn't automatically know the contents of your private document",
                        "The LLM can only answer math questions",
                        "The LLM requires the document to be a PDF specifically"
                    ],
                    "correct": 1,
                    "explanation": "An LLM has no built-in access to your private documents, so without retrieval it simply doesn't know what's inside them."
                },
                {
                    "question": "Why is it inefficient to send an entire 10,000-page document to the LLM for every question?",
                    "options": [
                        "LLMs cannot read more than one page at a time",
                        "It's slower, costlier, and unnecessary when only a few relevant nodes actually answer the question",
                        "Documents longer than 10 pages cause errors",
                        "The LLM would refuse the request entirely"
                    ],
                    "correct": 1,
                    "explanation": "RAG retrieves only a handful of relevant nodes rather than sending everything, which is far more efficient than passing the whole document each time."
                },
                {
                    "question": "Which statement correctly distinguishes RAG from LlamaIndex?",
                    "options": [
                        "RAG and LlamaIndex are the same thing",
                        "RAG is a concept/technique; LlamaIndex is a framework/tool that helps implement it",
                        "LlamaIndex is a concept; RAG is a specific Python library",
                        "RAG only works with LlamaIndex and no other framework"
                    ],
                    "correct": 1,
                    "explanation": "RAG = concept (Retrieve → Augment → Generate). LlamaIndex = tool/framework that helps you build systems like RAG."
                },
                {
                    "question": "In the RAG pipeline diagram, what happens right after the user's question is turned into an embedding?",
                    "options": [
                        "The LLM immediately generates an answer with no search",
                        "The index is searched to find the relevant Node(s)",
                        "The document is deleted and recreated",
                        "A new embedding model is trained from scratch"
                    ],
                    "correct": 1,
                    "explanation": "After the question is embedded, the vector index is searched to find the relevant node(s), whose content is then sent as context to the LLM."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Retrievers — How LlamaIndex Finds the Right Information",
        "slug":              "retrievers",
        "description":       "Understand retrievers, how they differ from query engines, the similarity_top_k setting, and why retrieval quality determines answer quality in RAG.",
        "order":             7,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["llamaindex", "retriever", "rag", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Retrievers — How LlamaIndex Finds the Right Information",
            "content":              """This lesson is very important because retrieval is the heart of RAG.

Don't worry — we'll keep it simple.

## 1. What is a Retriever?

A retriever answers one question:

"Which pieces of my data are relevant to this question?"

Imagine your database contains 1,000 pieces of information.

The user asks:

"What GPA is required for graduation?"

We don't want all 1,000 pieces. We want something like:

- Node 237 ⭐ "The minimum GPA required for graduation is 2.0."
- Node 481 ⭐ "Students must satisfy all graduation requirements."

The retriever finds those relevant Nodes.

## 2. Think of a librarian 📚

Imagine you have a huge library.

You ask: "Find books about machine learning."

The librarian doesn't give you every book. They search and give you the most relevant ones.

```
You
 ↓
Question
 ↓
Librarian
 ↓
Relevant books
```

In LlamaIndex:

```
User
 ↓
Question
 ↓
Retriever
 ↓
Relevant Nodes
```

## 3. Retriever vs Query Engine

This distinction is important.

**Retriever** — Finds information.

```
Question
   ↓
Retriever
   ↓
Relevant Nodes
```

**Query Engine** — Usually does more:

```
Question
   ↓
Retrieve relevant Nodes
   ↓
Give them to LLM
   ↓
Generate answer
```

So: Retriever = Find. Query Engine = Find + Answer.

## 4. The default retriever

When we previously wrote:

```python
query_engine = index.as_query_engine()
```

LlamaIndex created retrieval behavior for us automatically.

But we can access the retriever directly.

```python
retriever = index.as_retriever()
```

Then:

```python
nodes = retriever.retrieve(
    "What GPA is required for graduation?"
)
```

Now `nodes` contains the relevant Nodes.

## 5. Let's see the retrieved information

Example:

```python
from llama_index.core import Document, VectorStoreIndex


document = Document(
    text=\"\"\"
    The AI Engineering program requires 160 credit hours.

    Students must complete all required courses.

    The minimum GPA required for graduation is 2.0.

    Python is commonly used for artificial intelligence.
    \"\"\"
)


index = VectorStoreIndex.from_documents([document])


retriever = index.as_retriever()


nodes = retriever.retrieve(
    "What GPA is required for graduation?"
)


for node in nodes:
    print(node.text)
```

You should see information related to: "The minimum GPA required for graduation is 2.0."

## 6. Why is this useful?

Previously, you only saw:

```python
response = query_engine.query(question)
```

You got an answer. But now we can inspect the retrieval step itself:

```
Question
   ↓
Retriever
   ↓
What did it find?
   ↓
Nodes
```

This is extremely useful when debugging RAG.

## 7. similarity_top_k

One important setting is `similarity_top_k`.

It controls approximately how many relevant Nodes you want retrieved.

For example:

```python
retriever = index.as_retriever(
    similarity_top_k=3
)
```

This means: try to retrieve the top 3 most similar Nodes.

Think:

- similarity_top_k = 1 → Best 1 Node
- similarity_top_k = 3 → Best 3 Nodes
- similarity_top_k = 10 → Best 10 Nodes

## 8. Why not retrieve 100 Nodes?

Good question. More isn't always better.

Suppose you retrieve 100 Nodes and pass them all to the LLM — it receives lots of irrelevant information. That can:

- increase cost
- increase latency
- confuse the model
- reduce answer quality

Instead, we usually want a small number of highly relevant Nodes.

## 9. Retriever in a real RAG system

The pipeline becomes:

```
                 USER QUESTION
                       ↓
                   Retriever
                       ↓
              ┌────────┼────────┐
              ↓        ↓        ↓
            Node 1   Node 2   Node 3
              └────────┼────────┘
                       ↓
                    Context
                       ↓
                       LLM
                       ↓
                    Answer
```

## 10. Retriever is NOT the LLM

This is another important distinction.

The retriever doesn't normally answer "What GPA is required?"

Instead, it finds: "The minimum GPA required is 2.0."

Then the LLM can turn that retrieved information into a natural response:

Retriever: "The minimum GPA required is 2.0."

↓

LLM: "The minimum GPA required for graduation is 2.0."

## 11. A very important RAG concept

Your final answer can only be as good as the information retrieved.

Imagine: Excellent LLM + Bad Retrieval → Bad Answer

But: Good Retrieval + Good LLM → Good Answer

That's why RAG engineers spend a lot of time improving retrieval.

## 🧠 Remember

**Retriever** — Finds relevant Nodes.

**similarity_top_k** — Controls how many Nodes are retrieved.

**Query Engine** — Uses retrieval and then generates an answer.

## ⭐ One sentence to remember

The retriever is the part of RAG that searches your data and brings back the most relevant information.
""",
            "order":                7,
            "estimated_minutes":    35,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Inspect Retrieved Nodes",
                "description":   "Use the AI Engineering example, create a retriever with similarity_top_k=2, retrieve nodes for 'What is machine learning?', and print each node's text.",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  """from llama_index.core import Document, VectorStoreIndex

document = Document(
    text=\"\"\"
    Python is commonly used for AI and machine learning.

    Machine learning allows computers to learn patterns from data.

    Deep learning uses neural networks with multiple layers.

    LlamaIndex helps connect LLMs with external data.
    \"\"\"
)

index = VectorStoreIndex.from_documents([document])

# TODO: create a retriever with similarity_top_k=2
retriever = ___

# TODO: retrieve nodes for "What is machine learning?"
nodes = ___

# TODO: print each node's text, separated by "-----"
""",
                "solution_code": """from llama_index.core import Document, VectorStoreIndex

document = Document(
    text=\"\"\"
    Python is commonly used for AI and machine learning.

    Machine learning allows computers to learn patterns from data.

    Deep learning uses neural networks with multiple layers.

    LlamaIndex helps connect LLMs with external data.
    \"\"\"
)

index = VectorStoreIndex.from_documents([document])

retriever = index.as_retriever(similarity_top_k=2)

nodes = retriever.retrieve("What is machine learning?")

for node in nodes:
    print(node.text)
    print("-----")
""",
                "skill_tested":  ["llamaindex", "retriever", "similarity_top_k"],
            },
        ],
        "quiz": {
            "title":         "Retrievers Quiz",
            "questions":     [
                {
                    "question": "What question does a Retriever answer?",
                    "options": [
                        "Which pieces of my data are relevant to this question?",
                        "What is the final natural-language answer?",
                        "How should the LLM be fine-tuned?",
                        "What is the total cost of this query?"
                    ],
                    "correct": 0,
                    "explanation": "A retriever's job is to find which pieces (Nodes) of your data are relevant to a given question."
                },
                {
                    "question": "How does a Retriever differ from a Query Engine?",
                    "options": [
                        "They are exactly the same thing",
                        "A Retriever only finds relevant Nodes; a Query Engine finds Nodes AND generates an answer via the LLM",
                        "A Query Engine only finds Nodes; a Retriever generates the final answer",
                        "A Retriever requires an API key while a Query Engine does not"
                    ],
                    "correct": 1,
                    "explanation": "Retriever = Find. Query Engine = Find + Answer (it uses the LLM to generate a response from retrieved nodes)."
                },
                {
                    "question": "How do you create a retriever directly from an index?",
                    "options": [
                        "index.get_retriever()",
                        "index.as_retriever()",
                        "Retriever.from_index(index)",
                        "index.retrieve_engine()"
                    ],
                    "correct": 1,
                    "explanation": "`index.as_retriever()` returns a retriever object that can be used to call `.retrieve(question)`."
                },
                {
                    "question": "What does the similarity_top_k parameter control?",
                    "options": [
                        "The number of documents you're allowed to upload",
                        "Approximately how many of the most similar Nodes are retrieved",
                        "The embedding model's vector dimensionality",
                        "The maximum length of the final LLM answer"
                    ],
                    "correct": 1,
                    "explanation": "similarity_top_k controls how many top relevant Nodes the retriever tries to return, e.g. similarity_top_k=3 retrieves the best 3 Nodes."
                },
                {
                    "question": "Why is retrieving too many Nodes (e.g. 100) usually a bad idea?",
                    "options": [
                        "It's actually always better to retrieve as many as possible",
                        "It can increase cost and latency, and confuse the model with irrelevant information",
                        "LlamaIndex has a hard limit of 10 Nodes maximum",
                        "It causes the vector store to delete itself"
                    ],
                    "correct": 1,
                    "explanation": "Passing too many, often less-relevant, nodes to the LLM increases cost and latency and can reduce answer quality by diluting the relevant context."
                },
                {
                    "question": "According to the lesson, what determines the ceiling on your final RAG answer quality?",
                    "options": [
                        "Only the LLM's raw intelligence, regardless of retrieval",
                        "The quality of the information retrieved — good retrieval is necessary for a good answer",
                        "The number of documents uploaded, regardless of relevance",
                        "The programming language used to build the app"
                    ],
                    "correct": 1,
                    "explanation": "The lesson states: Excellent LLM + Bad Retrieval → Bad Answer, but Good Retrieval + Good LLM → Good Answer. Retrieval quality caps overall answer quality."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Metadata + Filtering",
        "slug":              "metadata-and-filtering",
        "description":       "Attach metadata to Documents/Nodes and use it to narrow retrieval to a relevant subset of data before semantic search runs.",
        "order":             8,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.0,
        "skill_tags":        ["llamaindex", "metadata", "filtering", "rag", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Metadata + Filtering",
            "content":              """Today we'll learn how to make retrieval more precise.

Imagine you have thousands of documents:

- Course 1 → AI → 2025
- Course 2 → CS → 2025
- Course 3 → AI → 2024
- Course 4 → Mathematics → 2025

A normal similarity search might search everything.

But what if you want: "Search only AI courses from 2025."

That's where metadata and filtering help.

## 1. What is Metadata?

Metadata is simply extra information about a document or Node.

For example:

Document: "Introduction to Machine Learning"

Metadata: `department = "AI"`, `year = 2025`, `course_code = "AI301"`

Think of it like a label attached to your data.

```
┌──────────────────────────────┐
│ Introduction to ML           │
│                              │
│ department: AI               │
│ year: 2025                   │
│ course_code: AI301           │
└──────────────────────────────┘
```

## 2. Why do we need Metadata?

Suppose we have 1000 documents, and the user asks:

"What are the AI courses in 2025?"

Instead of searching everything, we can narrow it:

```
1000 documents
      ↓
year = 2025
      ↓
AI department
      ↓
Search
```

This can make retrieval much more useful.

## 3. Adding Metadata to a Document

LlamaIndex allows us to add metadata.

```python
from llama_index.core import Document


document = Document(
    text="Machine Learning is a course about learning patterns from data.",
    metadata={
        "department": "AI",
        "year": 2025,
        "course_code": "AI301"
    }
)
```

Now our document has Text ("Machine Learning is...") and Metadata (department=AI, year=2025, course_code=AI301).

## 4. Multiple Documents

Let's create three courses:

```python
from llama_index.core import Document


documents = [
    Document(
        text="Machine Learning teaches algorithms that learn from data.",
        metadata={
            "department": "AI",
            "year": 2025,
            "course_code": "AI301"
        }
    ),

    Document(
        text="Database Systems teaches SQL and database design.",
        metadata={
            "department": "CS",
            "year": 2025,
            "course_code": "CS302"
        }
    ),

    Document(
        text="Deep Learning teaches neural networks.",
        metadata={
            "department": "AI",
            "year": 2024,
            "course_code": "AI401"
        }
    )
]
```

Now we have:

- Machine Learning → AI → 2025
- Database Systems → CS → 2025
- Deep Learning → AI → 2024

## 5. Metadata Filtering

The idea is:

```
Question
   ↓
Filter metadata
   ↓
Search remaining data
   ↓
Relevant Nodes
```

For example, `department = AI` and `year = 2025` would leave only:

Machine Learning ✅ (because Database Systems is CS, and Deep Learning is 2024)

## 6. Why this is powerful

Imagine your academic RAG system with metadata such as:

```python
metadata={
    "faculty": "Engineering",
    "department": "AI",
    "academic_year": "2025/2026",
    "topic": "GPA"
}
```

Then you can narrow searches based on those properties. For example, "What is the GPA requirement?" could search only `topic = GPA` instead of searching your entire university regulation document.

## 7. Metadata vs Text

This distinction is important.

**Text** — Contains the actual information: "The minimum GPA required for graduation is 2.0."

**Metadata** — Describes the information: `topic = "graduation"`, `year = "2025"`, `source = "university_rules"`

## 8. Metadata becomes extremely useful with large datasets

With a small project of 20 documents, you might not notice much difference. But imagine 100,000 documents with metadata like `country = Egypt`, `year = 2026`, `department = AI`, `document_type = regulation` — retrieval can then focus on the correct subset.

## 9. A real-world example

Imagine your academic advisor system contains: GPA rules, Registration rules, Graduation rules, Course descriptions, Tuition fees, Academic calendar.

You can attach metadata like `topic = GPA`, `topic = registration`, `topic = graduation`, `topic = courses`, `topic = tuition`.

Then "How much is the credit hour?" can focus on `topic = tuition`, while "What GPA do I need?" can focus on `topic = GPA`.

This is a very common pattern in production RAG.

## 10. Important warning ⚠️

Metadata doesn't replace semantic search. You usually combine them.

```
                 Question
                    ↓
             Metadata Filter
                    ↓
            Semantic Retrieval
                    ↓
             Relevant Nodes
                    ↓
                   LLM
                    ↓
                 Answer
```

So: Metadata = narrow the search. Embeddings = find similar meaning.

## 🧠 Remember

**Metadata** — Extra information describing your data.

**Filtering** — Restrict retrieval to data matching specific metadata.

## ⭐ One sentence to remember

Metadata tells LlamaIndex what a piece of data is, while filtering lets us restrict retrieval to the data we want.
""",
            "order":                8,
            "estimated_minutes":    35,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Tag Courses with Metadata",
                "description":   "Create three course documents (Python/AI/2025, Databases/CS/2025, Deep Learning/AI/2024) each with department, year, and course_code metadata. Then identify which one matches department=AI and year=2025.",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  """from llama_index.core import Document

# TODO: create three documents with metadata:
# 1. "Python teaches programming for AI applications." -> department=AI, year=2025, course_code="AI201"
# 2. "Databases teaches SQL and database design." -> department=CS, year=2025, course_code="CS302"
# 3. "Deep Learning teaches neural networks." -> department=AI, year=2024, course_code="AI401"
documents = [
    ___,
    ___,
    ___,
]

# TODO: print the text of any document where metadata["department"] == "AI"
# and metadata["year"] == 2025
""",
                "solution_code": """from llama_index.core import Document

documents = [
    Document(
        text="Python teaches programming for AI applications.",
        metadata={"department": "AI", "year": 2025, "course_code": "AI201"}
    ),
    Document(
        text="Databases teaches SQL and database design.",
        metadata={"department": "CS", "year": 2025, "course_code": "CS302"}
    ),
    Document(
        text="Deep Learning teaches neural networks.",
        metadata={"department": "AI", "year": 2024, "course_code": "AI401"}
    ),
]

for doc in documents:
    if doc.metadata["department"] == "AI" and doc.metadata["year"] == 2025:
        print(doc.text)
""",
                "skill_tested":  ["llamaindex", "metadata", "filtering"],
            },
        ],
        "quiz": {
            "title":         "Metadata + Filtering Quiz",
            "questions":     [
                {
                    "question": "What is metadata in the context of a LlamaIndex Document?",
                    "options": [
                        "The embedding vector of the document",
                        "Extra information describing the document, such as department or year",
                        "The LLM's generated answer",
                        "A copy of the document's text in another language"
                    ],
                    "correct": 1,
                    "explanation": "Metadata is extra information (like department, year, course_code) attached to a document or node, separate from its actual text content."
                },
                {
                    "question": "How do you attach metadata when creating a Document?",
                    "options": [
                        "Document(text=..., tags=...)",
                        "Document(text=..., metadata={...})",
                        "Document.set_metadata(text=..., ...)",
                        "Metadata is attached automatically and cannot be customized"
                    ],
                    "correct": 1,
                    "explanation": "The `metadata` parameter accepts a dictionary of key-value pairs when constructing a Document, e.g. `metadata={'department': 'AI', 'year': 2025}`."
                },
                {
                    "question": "Given three documents tagged (AI, 2025), (CS, 2025), and (AI, 2024), which one matches a filter of department=AI AND year=2025?",
                    "options": [
                        "The CS, 2025 document",
                        "The AI, 2024 document",
                        "The AI, 2025 document",
                        "All three documents match"
                    ],
                    "correct": 2,
                    "explanation": "Only the document tagged department=AI and year=2025 satisfies both filter conditions simultaneously."
                },
                {
                    "question": "According to the lesson, does metadata filtering replace semantic (embedding-based) search?",
                    "options": [
                        "Yes, metadata filtering makes embeddings unnecessary",
                        "No — metadata narrows the search space, while embeddings still find similar meaning within it",
                        "Yes, but only for documents larger than 100 pages",
                        "Metadata and embeddings can never be used together"
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly warns that metadata doesn't replace semantic search — the two are typically combined: metadata filters the pool, embeddings find semantically relevant results within it."
                },
                {
                    "question": "Why does metadata become especially valuable as a dataset grows (e.g. to 100,000 documents)?",
                    "options": [
                        "Because embeddings stop working past a certain dataset size",
                        "Because it lets retrieval focus on the correct subset instead of searching everything",
                        "Because metadata reduces the storage size of each document to zero",
                        "Because LlamaIndex requires metadata for datasets over 1,000 documents"
                    ],
                    "correct": 1,
                    "explanation": "With large datasets, filtering by metadata (e.g. country, year, department) lets the system narrow the search space to the relevant subset before or alongside semantic search."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Reranking — Getting the Best Results",
        "slug":              "reranking",
        "description":       "Understand rerankers, how they differ from retrievers, why reranking improves relevance ordering, and how to plug a reranker into a query engine as a node postprocessor.",
        "order":             9,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.0,
        "skill_tags":        ["llamaindex", "reranking", "rag", "retriever"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Reranking — Getting the Best Results",
            "content":              """We're now getting into an important RAG improvement technique.

Don't worry — the idea is simple.

## 1. The problem

Suppose the user asks:

"What is the minimum GPA required for graduation?"

Our retriever searches 1,000 Nodes and returns the top 5:

1. GPA calculation
2. Course registration
3. Graduation requirements ⭐
4. Academic calendar
5. Credit hours

The correct information is Node 3. But the retriever put it in position 3. That's not ideal.

## 2. What does a Reranker do?

A reranker looks at the retrieved results again and tries to put the most relevant results first.

```
Retriever
    ↓
5 results
    ↓
Reranker
    ↓
Reordered results
    ↓
Best results
```

Before:

1. GPA calculation
2. Registration
3. Graduation requirements ⭐
4. Academic calendar
5. Credit hours

After reranking:

1. Graduation requirements ⭐
2. GPA calculation
3. Credit hours
4. Registration
5. Academic calendar

## 3. Retriever vs Reranker

This is very important.

**Retriever** — Fast and broad: "Give me some potentially relevant results."

**Reranker** — More precise: "Now carefully decide which of these results are actually the most relevant."

Think:

```
Retriever
    ↓
100 candidates
    ↓
Reranker
    ↓
Top 5
```

## 4. Simple analogy 🕵️

Imagine you're hiring someone.

**Step 1 — Recruiter**: Looks through 10,000 CVs → 100 possible candidates.

**Step 2 — Hiring manager**: Carefully evaluates those 100 → 5 best candidates.

The recruiter is like the retriever. The hiring manager is like the reranker.

## 5. Why do we need reranking?

Semantic similarity isn't perfect.

Question: "What GPA is required for graduation?"

These two texts may both look relevant:

A: "Students must maintain a good academic GPA."

B: "The minimum GPA required for graduation is 2.0."

But B is much more useful. A reranker can help distinguish them.

## 6. Reranking in a RAG pipeline

Our pipeline now becomes:

```
                  QUESTION
                     ↓
                 Retriever
                     ↓
              10–20 candidates
                     ↓
                 Reranker
                     ↓
                Top 3–5
                     ↓
                    LLM
                     ↓
                  Answer
```

This is a very common production RAG architecture.

## 7. LlamaIndex and reranking

LlamaIndex supports reranking through postprocessors.

One commonly used approach is a Sentence Transformer reranker.

Conceptually:

```python
reranker = ...
```

Then:

```python
query_engine = index.as_query_engine(
    node_postprocessors=[reranker]
)
```

The exact model and package depend on your setup. For example, `BAAI/bge-reranker-v2-m3` is a strong multilingual reranking model and can be useful for Arabic + English RAG.

## 8. Don't confuse reranking with embeddings

They are different.

**Embedding** — Turns text into vectors: Text → [0.21, 0.72, ...]. Used for fast similarity search.

**Reranker** — Examines Question + Retrieved Text and produces a relevance score.

For example:

- Result A → 0.31
- Result B → 0.94 ⭐
- Result C → 0.52

Then B gets placed first.

## 9. Why don't we rerank everything?

Because reranking is generally more expensive than initial retrieval.

Imagine 1,000,000 documents — we don't want to rerank all 1,000,000.

Instead:

```
1,000,000 documents
        ↓
Fast Retriever
        ↓
50 candidates
        ↓
Reranker
        ↓
5 best
```

This gives us a good balance between speed + accuracy.

## 10. The RAG architecture we're building

You've now learned:

```
                 Documents
                     ↓
                   Nodes
                     ↓
                 Embeddings
                     ↓
                Vector Index
                     ↓
                 Retriever
                     ↓
              Candidate Nodes
                     ↓
                 Reranker
                     ↓
                Best Nodes
                     ↓
                    LLM
                     ↓
                  Answer
```

This is getting close to a production-quality RAG architecture.

## 🧠 Important terminology

**Retriever** — Finds potentially relevant information.

**Reranker** — Reorders those results according to relevance.

**Top-K** — The number of results you keep. For example: Retriever → top 20, Reranker → top 5, LLM → receives 5.

## 🎯 Simple example

Question: "What courses are required for graduation?"

Retriever returns: Course registration, Required courses ⭐, Tuition fees, GPA rules, Academic calendar.

Reranker: Required courses ⭐, GPA rules, Course registration, Academic calendar, Tuition fees.

Then perhaps we only send "Required courses" and "GPA rules" to the LLM.

## ⭐ One sentence to remember

Retrieval finds possible answers; reranking puts the best answers first.
""",
            "order":                9,
            "estimated_minutes":    35,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Wire a Reranker into a Query Engine",
                "description":   "Given a retriever that returns candidate nodes, write the query engine setup that would plug a reranker in as a node postprocessor.",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  """from llama_index.core import Document, VectorStoreIndex

document = Document(
    text=\"\"\"
    Students must maintain a good academic GPA.

    The minimum GPA required for graduation is 2.0.

    Course registration opens every semester.
    \"\"\"
)

index = VectorStoreIndex.from_documents([document])

# Assume `reranker` is already created (e.g. a SentenceTransformerRerank instance)
reranker = ...

# TODO: create a query engine that uses `reranker` as a node postprocessor
query_engine = ___
""",
                "solution_code": """from llama_index.core import Document, VectorStoreIndex

document = Document(
    text=\"\"\"
    Students must maintain a good academic GPA.

    The minimum GPA required for graduation is 2.0.

    Course registration opens every semester.
    \"\"\"
)

index = VectorStoreIndex.from_documents([document])

# Assume `reranker` is already created (e.g. a SentenceTransformerRerank instance)
reranker = ...

query_engine = index.as_query_engine(
    node_postprocessors=[reranker]
)
""",
                "skill_tested":  ["llamaindex", "reranking", "node_postprocessors"],
            },
        ],
        "quiz": {
            "title":         "Reranking Quiz",
            "questions":     [
                {
                    "question": "What is the main job of a reranker?",
                    "options": [
                        "To generate embeddings for new documents",
                        "To reorder retrieved results so the most relevant ones come first",
                        "To translate the user's question into another language",
                        "To replace the LLM entirely"
                    ],
                    "correct": 1,
                    "explanation": "A reranker takes the results the retriever already found and reorders them so the most relevant results appear first."
                },
                {
                    "question": "In the hiring analogy, who does the reranker correspond to?",
                    "options": [
                        "The recruiter who screens 10,000 CVs",
                        "The hiring manager who carefully evaluates the 100 shortlisted candidates",
                        "The job applicant",
                        "The HR software system"
                    ],
                    "correct": 1,
                    "explanation": "The recruiter (broad, fast screening) is like the retriever; the hiring manager (careful, precise evaluation) is like the reranker."
                },
                {
                    "question": "How does a reranker fundamentally differ from an embedding model?",
                    "options": [
                        "A reranker converts text into vectors; an embedding model scores relevance",
                        "A reranker examines the question plus retrieved text together and produces a relevance score, rather than just embedding text independently",
                        "There is no difference between the two",
                        "A reranker is only used for images, not text"
                    ],
                    "correct": 1,
                    "explanation": "Embeddings turn text into vectors independently for fast similarity search. A reranker jointly examines the question and each candidate text to produce a relevance score."
                },
                {
                    "question": "Why isn't reranking applied to the entire dataset (e.g. all 1,000,000 documents) directly?",
                    "options": [
                        "Reranking only works on datasets smaller than 10 documents",
                        "Reranking is generally more expensive, so it's applied only to a smaller set of candidates from a fast retriever first",
                        "Rerankers cannot process more than one document at a time",
                        "It's actually recommended to rerank everything for best results"
                    ],
                    "correct": 1,
                    "explanation": "Reranking is costlier than initial retrieval, so a fast retriever first narrows millions of documents to a smaller candidate set (e.g. 50), which the reranker then refines."
                },
                {
                    "question": "In LlamaIndex, how is a reranker typically plugged into a query engine?",
                    "options": [
                        "As a `node_postprocessors` argument when creating the query engine",
                        "By replacing the VectorStoreIndex entirely",
                        "It cannot be integrated with a query engine",
                        "By modifying the Document's metadata directly"
                    ],
                    "correct": 0,
                    "explanation": "The lesson shows `query_engine = index.as_query_engine(node_postprocessors=[reranker])` as the way to plug a reranker into the pipeline."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Chat Engine + Memory",
        "slug":              "chat-engine-and-memory",
        "description":       "Move from single-shot Q&A to conversational RAG using a Chat Engine that maintains conversation history, and understand the difference between conversation history and long-term memory.",
        "order":             10,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.0,
        "skill_tags":        ["llamaindex", "chat-engine", "memory", "rag", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Chat Engine + Memory",
            "content":              """Now we're going to make our RAG system conversational.

So instead of:

```
Question → Answer
```

we'll have:

```
User → Question
       ↓
     AI Answer
       ↓
User → Follow-up question
       ↓
     AI understands context
```

## 1. The problem

Imagine you ask: "What is LlamaIndex?"

AI: "LlamaIndex is a framework for building applications with LLMs and external data."

Then you ask: "What can I use it for?"

A normal question-answer system might not know what "it" means.

A chat system remembers:

```
User: What is LlamaIndex?
        ↓
AI: LlamaIndex is...
        ↓
User: What can I use it for?
        ↓
AI: You can use LlamaIndex for...
```

That's conversation context.

## 2. Query Engine vs Chat Engine

You already know `query_engine.query(...)`. This is great for individual questions.

```
Question
   ↓
Query Engine
   ↓
Answer
```

A **Chat Engine** is designed for conversations.

```
Conversation
     ↓
 Chat Engine
     ↓
 Context-aware Answer
```

## 3. Creating a Chat Engine

Suppose we have our index:

```python
index = VectorStoreIndex.from_documents(documents)
```

We can create a chat engine:

```python
chat_engine = index.as_chat_engine()
```

Then:

```python
response = chat_engine.chat(
    "What is LlamaIndex?"
)

print(response)
```

## 4. Continue the conversation

Now:

```python
response = chat_engine.chat(
    "What can I use it for?"
)

print(response)
```

The chat engine can use the conversation history to understand that "it" = LlamaIndex.

## 5. Chat history

Think about the conversation as a list:

- User: "What is LlamaIndex?"
- AI: "LlamaIndex is a framework..."
- User: "What can I use it for?"
- AI: "You can use it for RAG..."

The previous messages provide context.

## 6. Memory

Now we need another concept: **Memory**.

Memory allows the application to maintain information from the conversation.

Think:

```
Conversation
     ↓
   Memory
     ↓
Previous messages
     ↓
Current question
     ↓
Better answer
```

For example:

- User: "My name is Mohammad."
- AI: "Nice to meet you, Mohammad."
- User: "What is my name?"
- AI: "Your name is Mohammad."

The system needs some mechanism to retain that information.

## 7. Important distinction ⚠️

There are different types of "memory."

**Conversation history** — Remembers messages from the current conversation (User → message 1, AI → response 1, User → message 2, AI → response 2...).

**Long-term memory** — Can store information beyond the current conversation, e.g. "User prefers Arabic responses." This is a more advanced topic.

For now, focus on conversation history.

## 8. Chat + RAG

Here's where things get interesting. We can combine Chat + Retrieval + LLM:

```
                 User Question
                       ↓
                Conversation
                  Context
                       ↓
                   Retriever
                       ↓
                Relevant Nodes
                       ↓
                     LLM
                       ↓
                    Answer
```

Now we have a conversational RAG system.

## 9. Example: University Advisor

Imagine your academic advisor.

User: "What GPA do I need to graduate?"

AI: "The minimum GPA is 2.0."

Then user: "What about credit hours?" — the system understands that we're still talking about graduation requirements.

Then: "And what courses do I need?" — again, the conversation context helps.

This is much closer to a real AI assistant.

## 10. A simple example

```python
from llama_index.core import Document, VectorStoreIndex


documents = [
    Document(
        text=\"\"\"
        LlamaIndex is a framework for connecting
        large language models with external data.
        \"\"\"
    ),
    Document(
        text=\"\"\"
        LlamaIndex can be used to build RAG systems,
        chatbots, question-answering systems, and agents.
        \"\"\"
    )
]


index = VectorStoreIndex.from_documents(documents)


chat_engine = index.as_chat_engine()


response = chat_engine.chat(
    "What is LlamaIndex?"
)

print(response)


response = chat_engine.chat(
    "What can I use it for?"
)

print(response)
```

The important part is `chat_engine = index.as_chat_engine()` and `chat_engine.chat(...)`.

## 11. Query Engine vs Chat Engine

Remember this table:

| | Query Engine | Chat Engine |
|---|---|---|
| Single questions | ⭐⭐⭐ | ⭐⭐⭐ |
| Conversation | ⭐ | ⭐⭐⭐ |
| Context | Limited | Stronger |
| RAG | ✅ | ✅ |
| Follow-up questions | Less natural | Better |

Simple rule: Question-answering → Query Engine. Conversation → Chat Engine.

## 🧠 The big picture

You've now moved from:

```
             RAG
              ↓
       Question → Answer
```

to:

```
          Conversational RAG

              User
               ↓
        Conversation History
               ↓
           Retriever
               ↓
        Relevant Documents
               ↓
              LLM
               ↓
             Answer
```

## ⭐ One sentence to remember

A Chat Engine lets your LlamaIndex application have a conversation instead of answering isolated questions.
""",
            "order":                10,
            "estimated_minutes":    35,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Have a Multi-Turn Conversation",
                "description":   "Build an index from documents about LlamaIndex, create a chat engine, and have a two-turn conversation: ask what LlamaIndex is, then ask a follow-up using 'it' to refer to LlamaIndex.",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  """from llama_index.core import Document, VectorStoreIndex

documents = [
    Document(
        text=\"\"\"
        LlamaIndex is a framework for connecting
        large language models with external data.
        \"\"\"
    ),
    Document(
        text=\"\"\"
        LlamaIndex can be used to build RAG systems,
        chatbots, question-answering systems, and agents.
        \"\"\"
    )
]

index = VectorStoreIndex.from_documents(documents)

# TODO: create a chat engine
chat_engine = ___

# TODO: ask "What is LlamaIndex?" and print the response

# TODO: ask the follow-up "What can I use it for?" and print the response
""",
                "solution_code": """from llama_index.core import Document, VectorStoreIndex

documents = [
    Document(
        text=\"\"\"
        LlamaIndex is a framework for connecting
        large language models with external data.
        \"\"\"
    ),
    Document(
        text=\"\"\"
        LlamaIndex can be used to build RAG systems,
        chatbots, question-answering systems, and agents.
        \"\"\"
    )
]

index = VectorStoreIndex.from_documents(documents)

chat_engine = index.as_chat_engine()

response = chat_engine.chat("What is LlamaIndex?")
print(response)

response = chat_engine.chat("What can I use it for?")
print(response)
""",
                "skill_tested":  ["llamaindex", "chat-engine", "conversation"],
            },
        ],
        "quiz": {
            "title":         "Chat Engine + Memory Quiz",
            "questions":     [
                {
                    "question": "What problem does a Chat Engine solve that a plain Query Engine struggles with?",
                    "options": [
                        "It makes retrieval faster",
                        "It understands follow-up questions by using conversation context (e.g. resolving 'it')",
                        "It removes the need for an index entirely",
                        "It eliminates the need for an LLM"
                    ],
                    "correct": 1,
                    "explanation": "A Query Engine typically treats each question independently, while a Chat Engine uses conversation history to understand references like 'it' in follow-up questions."
                },
                {
                    "question": "Which method creates a Chat Engine from an index?",
                    "options": [
                        "index.as_query_engine()",
                        "index.as_chat_engine()",
                        "ChatEngine.from_index(index)",
                        "index.chat_mode()"
                    ],
                    "correct": 1,
                    "explanation": "`index.as_chat_engine()` returns a chat engine, similar to how `as_query_engine()` returns a query engine."
                },
                {
                    "question": "How do you send a message to a chat engine and get a response?",
                    "options": [
                        "chat_engine.query(message)",
                        "chat_engine.ask(message)",
                        "chat_engine.chat(message)",
                        "chat_engine.send(message)"
                    ],
                    "correct": 2,
                    "explanation": "The lesson uses `response = chat_engine.chat(\"What is LlamaIndex?\")` to interact with the chat engine."
                },
                {
                    "question": "What's the difference between conversation history and long-term memory, per the lesson?",
                    "options": [
                        "They are the same thing with different names",
                        "Conversation history covers only the current conversation; long-term memory can persist information beyond it",
                        "Long-term memory only works with Query Engines",
                        "Conversation history is stored in the vector index"
                    ],
                    "correct": 1,
                    "explanation": "Conversation history remembers messages within the current conversation, while long-term memory (a more advanced topic) can retain information like user preferences across conversations."
                },
                {
                    "question": "According to the comparison table, when is a Query Engine generally preferred over a Chat Engine?",
                    "options": [
                        "When handling multi-turn conversations with follow-up questions",
                        "When answering a single, independent question",
                        "When retrieval isn't needed at all",
                        "Query Engines can never be used for RAG"
                    ],
                    "correct": 1,
                    "explanation": "The rule of thumb given is: question-answering → Query Engine, conversation → Chat Engine. Both support RAG, but conversation context is stronger in the Chat Engine."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Tools + Agents",
        "slug":              "tools-and-agents",
        "description":       "Move from RAG (retrieving information) to Agents (deciding and acting): understand Tools, FunctionTool, how agents choose between multiple tools, and when an agent is actually needed versus plain RAG.",
        "order":             11,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.25,
        "skill_tags":        ["llamaindex", "agents", "tools", "function-tool"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Tools + Agents",
            "content":              """We're now moving from RAG to AI Agents.

The main idea is very simple:

A RAG system finds information. An Agent can decide what action to take.

## 1. What is a Tool?

A tool is a function that an AI can use.

For example:

```python
def add(a, b):
    return a + b
```

This is a normal Python function. We can turn it into a tool that an AI agent can use.

Think:

```
AI
 ↓
"I need to calculate 25 + 30"
 ↓
Calculator Tool
 ↓
55
```

## 2. Examples of Tools

An agent could have tools like:

- 🔢 Calculator
- 🔎 Search
- 🌐 Web API
- 🗄️ Database
- 📄 Document search
- 📧 Email
- 📅 Calendar

For example: User: "What is 25 × 40?" → Agent → Calculator Tool → 1000 → Answer.

## 3. What is an Agent?

An Agent is an AI system that can:

1. Understand the user's request
2. Decide what it needs to do
3. Choose a tool
4. Use the tool
5. Look at the result
6. Give the final answer

Simple picture:

```
              User
                ↓
              Agent
                ↓
       "Which tool do I need?"
          ↙           ↘
   Calculator       Search
          ↘           ↙
             Result
                ↓
              Agent
                ↓
              Answer
```

## 4. RAG vs Agent

This is extremely important.

**RAG** — The main job is: Question → Retrieve information → Answer.

**Agent** — The AI can decide: Question → Think about task → Choose tool → Use tool → Maybe use another tool → Answer.

So: RAG = retrieve information. Agent = decide and act.

## 5. Simple Tool Example

Let's create a calculator.

```python
def multiply(a: int, b: int) -> int:
    return a * b
```

We want the agent to be able to use it. LlamaIndex provides tool abstractions such as `FunctionTool`.

```python
from llama_index.core.tools import FunctionTool


multiply_tool = FunctionTool.from_defaults(
    fn=multiply
)
```

Now we have: `multiply()` → `FunctionTool` → AI can use it.

## 6. Why use a tool instead of letting the LLM calculate?

LLMs aren't always reliable calculators. For example: `1234567 × 9876543`.

A calculator is much better at this. So we give the AI a tool.

```
LLM
 ↓
"I need exact arithmetic"
 ↓
Calculator
 ↓
Correct result
```

This is one of the fundamental ideas behind agents.

## 7. Multiple Tools

Imagine we give an agent three tools: Calculator, Course Search, Weather API.

- "What is the weather today?" → agent chooses Weather API
- "What GPA is required?" → agent chooses Course/Document Search
- "What is 25 × 8?" → agent chooses Calculator

The agent decides which tool is appropriate.

## 8. Agent + RAG

This is where LlamaIndex becomes very powerful.

Imagine your university AI assistant has: 📚 University RAG, 🔢 Calculator, 📊 GPA Calculator, 📄 Course Database.

User: "If I have 120 completed credit hours and my GPA is 2.8, what happens if I complete these courses?"

The agent could potentially route through: Question → Agent → Course Database → GPA Calculator → RAG → Answer, instead of forcing one pipeline to handle everything.

## 9. Agent decision-making

Think of an agent as a manager. You give the manager: Calculator, Database, Search.

Then: "Find the AI courses and calculate their total credit hours." → Agent coordinates Course Search (→ Courses) and Calculator (→ Total hours) → Answer.

## 10. Important warning ⚠️

Don't use agents for everything.

If the task is simply "Search my PDF and answer my question," you probably don't need an agent. A normal RAG pipeline is simpler: Question → Retriever → LLM → Answer.

Use an agent when the AI needs to choose between actions/tools.

## 11. When should you use an Agent?

- Simple document question → Use RAG
- Need calculation → Use RAG + Calculator Tool
- Need API + database + RAG → An Agent may be useful

## 🧠 Remember this

**Tool** — A function the AI can use.

**Agent** — An AI system that decides which tools to use and in what order.

## ⭐ One sentence to remember

An Agent is an AI that can choose and use tools to accomplish a task.
""",
            "order":                11,
            "estimated_minutes":    40,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Wrap a Function as a Tool",
                "description":   "Write a multiply function and wrap it as a LlamaIndex FunctionTool so it can be used by an agent.",
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code":  """from llama_index.core.tools import FunctionTool

# TODO: define a function `multiply(a: int, b: int) -> int` that returns a * b
def multiply(a: int, b: int) -> int:
    ___

# TODO: wrap it as a FunctionTool
multiply_tool = ___
""",
                "solution_code": """from llama_index.core.tools import FunctionTool

def multiply(a: int, b: int) -> int:
    return a * b

multiply_tool = FunctionTool.from_defaults(
    fn=multiply
)
""",
                "skill_tested":  ["llamaindex", "tools", "functiontool", "agents"],
            },
        ],
        "quiz": {
            "title":         "Tools + Agents Quiz",
            "questions":     [
                {
                    "question": "What is the core difference between RAG and an Agent, according to the lesson?",
                    "options": [
                        "RAG retrieves information; an Agent decides and acts (possibly using multiple tools)",
                        "RAG and Agents are identical concepts",
                        "Agents can only retrieve documents, nothing else",
                        "RAG requires an LLM while Agents never use an LLM"
                    ],
                    "correct": 0,
                    "explanation": "RAG's job is Question → Retrieve information → Answer. An Agent's job is Question → Think → Choose tool → Use tool → Answer, i.e. it can decide and act."
                },
                {
                    "question": "What is a 'Tool' in the context of an agent?",
                    "options": [
                        "A type of embedding model",
                        "A function that the AI can use to perform an action, like a calculator or search",
                        "A synonym for the LLM itself",
                        "A vector store index"
                    ],
                    "correct": 1,
                    "explanation": "A tool is a function (like calculator, search, database, email) that an AI agent can call upon to accomplish part of a task."
                },
                {
                    "question": "Which LlamaIndex class is used to wrap a plain Python function so an agent can use it?",
                    "options": [
                        "AgentFunction",
                        "FunctionTool",
                        "ToolWrapper",
                        "CallableAgent"
                    ],
                    "correct": 1,
                    "explanation": "`FunctionTool.from_defaults(fn=my_function)` from `llama_index.core.tools` wraps a Python function as a usable tool."
                },
                {
                    "question": "Why might you give an agent a calculator tool instead of letting the LLM compute the answer directly?",
                    "options": [
                        "LLMs are always faster than calculators",
                        "LLMs aren't always reliable at exact arithmetic, especially with large numbers",
                        "Calculators are required by LlamaIndex to function at all",
                        "It's purely a stylistic choice with no practical benefit"
                    ],
                    "correct": 1,
                    "explanation": "The lesson notes that LLMs aren't always reliable calculators (e.g. large multiplications), so an exact calculator tool produces more reliable results."
                },
                {
                    "question": "According to the lesson's warning, when should you avoid using an agent?",
                    "options": [
                        "When the task is a simple 'search my PDF and answer my question' — plain RAG is simpler and sufficient",
                        "Whenever more than one document exists",
                        "Agents should always be used regardless of task complexity",
                        "Only when working with metadata filtering"
                    ],
                    "correct": 0,
                    "explanation": "The lesson explicitly warns not to use agents for everything — a simple document Q&A task is better served by a normal RAG pipeline. Agents are for when the AI needs to choose between multiple actions/tools."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Workflows",
        "slug":              "workflows",
        "description":       "Organize an AI application into multiple connected steps using LlamaIndex Workflows — Events, Steps, and branching logic — and understand how workflows relate to agents.",
        "order":             12,
        "difficulty":        DifficultyLevel.advanced,
        "estimated_hours":   1.25,
        "skill_tags":        ["llamaindex", "workflows", "agents", "architecture"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Workflows",
            "content":              """We're now at one of the more advanced parts of LlamaIndex.

But the idea is actually very simple:

A Workflow lets you organize an AI application into multiple steps.

## 1. The problem

Imagine your AI assistant needs to do this:

```
User asks question
       ↓
Search documents
       ↓
Check if information was found
       ↓
If found → Generate answer
       ↓
If not found → Say "I don't know"
```

That's a workflow. Instead of putting everything into one giant function, we divide it into steps.

## 2. Think of a Workflow like a recipe 🍳

A recipe might say: Get ingredients → Cut vegetables → Cook vegetables → Add sauce → Serve.

Each step has a specific job.

An AI workflow is similar: Receive question → Retrieve information → Check results → Generate answer → Return answer.

## 3. Workflow vs normal RAG

A simple RAG system:

```
Question
   ↓
Retriever
   ↓
LLM
   ↓
Answer
```

A workflow can be more complex:

```
Question
   ↓
Retrieve
   ↓
Check relevance
   ↓
 ┌───────────────┐
 │               │
Good            Bad
 │               │
 ↓               ↓
LLM          Search Again
 │
 ↓
Answer
```

This is why workflows are useful.

## 4. The three words you need

LlamaIndex workflows are built around concepts such as:

**Event** — Information passed between steps. Think: Event = Message.

**Step** — A piece of work, e.g. `retrieve()`, `generate()`.

**Workflow** — Connects the steps: Workflow → Step 1 → Step 2 → Step 3.

## 5. A simple workflow

Conceptually:

```python
class MyWorkflow:

    def step_1():
        ...

    def step_2():
        ...

    def step_3():
        ...
```

The important idea isn't memorizing the syntax yet. Understand the architecture first.

## 6. Example AI workflow

Suppose our user asks: "What is the minimum GPA?"

Our workflow could be:

```
             Question
                ↓
         ┌──────────────┐
         │   Retrieve   │
         └──────────────┘
                ↓
         Relevant Nodes
                ↓
         ┌──────────────┐
         │ Check Result │
         └──────────────┘
             ↙      ↘
          Found    Not Found
            ↓          ↓
          LLM       Search Again
            ↓
         Answer
```

Each box is a step.

## 7. Why not just use normal Python functions?

You can. For a small application, `retrieve()` and `generate()` might be enough.

But workflows become useful when you have: multiple steps, branching, loops, tool calls, retries, asynchronous operations, complex agent behavior.

For example:

```
Question
   ↓
Retrieve
   ↓
Is result good?
 ↙       ↘
No       Yes
 ↓         ↓
Retry     Generate
 ↓         ↓
Retrieve  Answer
```

That becomes easier to manage as a workflow.

## 8. Workflow + Agent

Now combine what we've learned. An advanced application might look like:

```
                  User
                   ↓
                Workflow
                   ↓
                 Agent
                   ↓
        ┌──────────┼──────────┐
        ↓          ↓          ↓
       RAG      Calculator   API
        ↓          ↓          ↓
        └──────────┼──────────┘
                   ↓
                 Check
                   ↓
                Response
```

This is getting close to production AI systems.

## 9. A university advisor example 🎓

Imagine your academic assistant receives: "What is the cost of 15 credit hours and what GPA do I need to graduate?"

This is actually two tasks. A workflow could do:

```
User Question
      ↓
Analyze Question
      ↓
 ┌──────────────┬──────────────┐
 ↓              ↓
Tuition         GPA
 ↓              ↓
Calculator      RAG
 ↓              ↓
 └───────┬──────┘
         ↓
      Combine
         ↓
       Answer
```

This is much more flexible than a simple RAG pipeline.

## 10. Workflow vs Agent

These concepts can be confusing.

**Workflow** — You define the general process: Step A → Step B → Step C.

**Agent** — The AI can decide what action/tool to take: "Should I use Search?" "Should I use Calculator?" "Should I use Database?"

So: Workflow = organize the process. Agent = make decisions/actions. And they can work together.

## 🧠 Remember

**Event** — Information passed between workflow steps.

**Step** — One operation in the workflow.

**Workflow** — A sequence/graph of operations that controls how your application runs.

## ⭐ One sentence to remember

A Workflow organizes multiple AI operations into a controlled sequence of steps.
""",
            "order":                12,
            "estimated_minutes":    40,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Design a Workflow (Conceptual)",
                "description":   "Given the question 'What are the required AI courses, and how many total credit hours are they?', write out the workflow steps as a Python list of strings representing each stage in order.",
                "difficulty":    DifficultyLevel.advanced,
                "starter_code":  """# TODO: represent the workflow steps as an ordered list of strings, e.g.
# ["Receive question", "Find AI courses", ...]
workflow_steps = [
    ___,
]
""",
                "solution_code": """workflow_steps = [
    "Receive question",
    "Find AI courses",
    "Extract credit hours",
    "Calculate total",
    "Return answer",
]
""",
                "skill_tested":  ["llamaindex", "workflows", "system-design"],
            },
        ],
        "quiz": {
            "title":         "Workflows Quiz",
            "questions":     [
                {
                    "question": "What is a Workflow in LlamaIndex, at a high level?",
                    "options": [
                        "A single Python function that does everything",
                        "A way to organize an AI application into multiple connected steps",
                        "A type of embedding model",
                        "A synonym for VectorStoreIndex"
                    ],
                    "correct": 1,
                    "explanation": "A Workflow lets you organize an AI application into multiple steps, rather than putting everything into one giant function."
                },
                {
                    "question": "In LlamaIndex Workflow terminology, what is an 'Event'?",
                    "options": [
                        "A scheduled calendar reminder",
                        "Information passed between workflow steps",
                        "An error that stops the workflow",
                        "A type of vector store"
                    ],
                    "correct": 1,
                    "explanation": "An Event is information passed between steps in a workflow — think of it as a message."
                },
                {
                    "question": "When do workflows become especially useful compared to plain Python functions?",
                    "options": [
                        "Only when there is exactly one step",
                        "When you need branching, loops, retries, tool calls, or complex agent behavior",
                        "Workflows are never more useful than plain functions",
                        "Only for very small, single-document RAG apps"
                    ],
                    "correct": 1,
                    "explanation": "The lesson notes workflows become useful with multiple steps, branching, loops, tool calls, retries, async operations, and complex agent behavior."
                },
                {
                    "question": "How does the lesson distinguish Workflow from Agent?",
                    "options": [
                        "They are identical and interchangeable",
                        "Workflow organizes the general process (Step A → B → C); Agent makes decisions about which actions/tools to use",
                        "Agent organizes the process; Workflow makes decisions",
                        "Workflows can only be used without agents"
                    ],
                    "correct": 1,
                    "explanation": "Workflow = organize the process. Agent = make decisions/actions. The lesson notes they can work together."
                },
                {
                    "question": "In the branching retrieval example (Retrieve → Check relevance → Good/Bad), what happens on the 'Bad' branch?",
                    "options": [
                        "The system immediately returns an answer anyway",
                        "The workflow searches again",
                        "The workflow deletes the document",
                        "The workflow stops entirely with no fallback"
                    ],
                    "correct": 1,
                    "explanation": "In the example workflow, if the retrieved result is judged 'Bad', the flow branches to 'Search Again' rather than proceeding straight to the LLM."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Evaluation — Is Your RAG Actually Good?",
        "slug":              "evaluation",
        "description":       "Measure RAG quality by separately evaluating retrieval (did we find the right information?) and answer generation (is the answer correct, relevant, grounded, and free of hallucination?).",
        "order":             13,
        "difficulty":        DifficultyLevel.advanced,
        "estimated_hours":   1.25,
        "skill_tags":        ["llamaindex", "evaluation", "rag", "hallucination"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Evaluation — Is Your RAG Actually Good?",
            "content":              """You can build a RAG system that runs perfectly... but that doesn't mean it gives good answers.

Today we'll learn how to measure its quality.

## 1. The problem

Suppose your user asks: "What is the minimum GPA required for graduation?"

Your RAG answers: "The minimum GPA is 3.5."

But your document says: "The minimum GPA is 2.0."

The application works technically, but the answer is wrong. So we need evaluation.

## 2. What is Evaluation?

Evaluation means: testing how well your AI system performs.

Think of it like an exam.

```
RAG System
    ↓
Test Questions
    ↓
Answers
    ↓
Compare with Expected Results
    ↓
Score
```

## 3. What should we evaluate?

For a RAG system, there are two major areas:

1. **Retrieval quality** — Did we retrieve the right information?
2. **Answer quality** — Did the LLM give a correct answer based on that information?

```
              RAG
               ↓
        ┌──────┴──────┐
        ↓             ↓
    Retrieval       Answer
     Quality         Quality
```

## 4. Retrieval Evaluation

Suppose our document has: Node 1 → Registration, Node 2 → GPA, Node 3 → Tuition, Node 4 → Courses.

Question: "What is the minimum GPA?" — the correct Node is Node 2 → GPA.

If our retriever returns Node 3 → Tuition and Node 1 → Registration instead, retrieval is bad.

Even with a very good LLM, it may not be able to answer correctly.

## 5. Retrieval Accuracy

One simple measurement is: Did the correct information appear in the retrieved results?

For example, top 5 retrieved Nodes: Node 1 ❌, Node 2 ❌, Node 3 ✅, Node 4 ❌, Node 5 ❌.

The relevant information was retrieved. That's good.

## 6. Top-K Retrieval

Remember `similarity_top_k`?

```python
retriever = index.as_retriever(
    similarity_top_k=5
)
```

We're asking: "Is the correct answer somewhere in these top 5 results?"

We can evaluate different values: Top-1 (did we find it immediately?), Top-3, Top-5, Top-10. This helps us understand retrieval performance.

## 7. Answer Evaluation

Now suppose retrieval found the correct information: "The minimum GPA is 2.0."

But the LLM says: "The minimum GPA is 3.0." That's still bad.

So we also need to evaluate the final answer.

## 8. What makes a good answer?

A good RAG answer should generally be:

✅ **Correct** — It matches the source.

✅ **Relevant** — It answers the user's actual question.

✅ **Grounded** — It is supported by retrieved information.

❌ **No hallucination** — It shouldn't invent facts.

## 9. Hallucination

This is one of the biggest problems with LLM applications.

Suppose your document says: "The minimum GPA is 2.0." But the AI says: "The minimum GPA is 2.5 according to the university regulations."

That's a hallucination if 2.5 isn't supported by your data.

A good RAG system should behave more like:

```
If information exists:
    Answer using the source.

If information doesn't exist:
    Say "I don't have enough information."
```

## 10. Evaluation Dataset

The best way to evaluate a RAG system is to create a set of questions. For example:

- Question 1: "What is the minimum GPA?" → Expected: 2.0
- Question 2: "How many credit hours are required?" → Expected: 160
- Question 3: "What are the graduation requirements?" → Expected: "Complete required courses..."

Then run your RAG system against these questions.

## 11. Simple evaluation process

```
          Evaluation Dataset
                  ↓
            Question 1
                  ↓
              RAG System
                  ↓
               Answer
                  ↓
             Evaluate
                  ↓
                Score
```

Repeat for Question 1, Question 2, Question 3... Question 100. Then calculate your overall performance.

## 12. Metrics you may encounter

You may see metrics such as:

**Retrieval metrics** — Recall, Precision, Hit Rate, MRR

**Answer metrics** — Faithfulness, Relevance, Correctness, BERTScore, BLEU, ROUGE

Don't worry about memorizing all of these now. The most important concept is: measure retrieval separately from answer generation.

## 13. A simple mental model

Imagine a restaurant.

**Retriever** — Finds the ingredients: 🥩 🥕 🧅

**LLM** — Cooks the meal: 🍲

Evaluation asks: Were the right ingredients retrieved? And: Did the chef prepare the correct meal?

If the wrong ingredients were retrieved, improving the chef won't solve the problem.

## 14. Your academic RAG example

For your academic advisor system, you could create 100 test questions, e.g.:

- Q: What is the minimum GPA required for graduation?
- Q: How many credit hours are required?
- Q: How much does one credit hour cost?
- Q: What are the registration rules?
- Q: What is the description of CSE 251?

Then measure: Retrieval Accuracy + Answer Correctness + Faithfulness.

This is how you know whether your RAG system is actually improving.

## 🧠 Remember

**Evaluation** — Testing the quality of your AI system.

**Retrieval evaluation** — Did we retrieve the correct information?

**Answer evaluation** — Did the LLM produce a correct, relevant, grounded answer?

**Hallucination** — The model generates information that isn't supported by the available data.

## ⭐ One sentence to remember

A RAG system isn't good just because it runs; evaluation tells us whether it retrieves the right information and produces trustworthy answers.
""",
            "order":                13,
            "estimated_minutes":    40,
            "has_code_examples":    False,
        },
        "exercises": [
            {
                "title":         "Score Retrieval Hit Rate",
                "description":   "Given an evaluation dataset of questions with their expected correct node IDs, and the retriever's actual top-k results per question, compute the hit rate (fraction of questions where the correct node appeared in the retrieved results).",
                "difficulty":    DifficultyLevel.advanced,
                "starter_code":  """# Each entry: (correct_node_id, [retrieved_node_ids])
eval_data = [
    ("node_2", ["node_1", "node_2", "node_3"]),
    ("node_4", ["node_1", "node_3", "node_5"]),
    ("node_2", ["node_2", "node_5", "node_1"]),
]

# TODO: compute hit_rate = fraction of questions where correct_node_id is in retrieved_node_ids
hit_rate = ___

print(f"Hit rate: {hit_rate:.2f}")
""",
                "solution_code": """# Each entry: (correct_node_id, [retrieved_node_ids])
eval_data = [
    ("node_2", ["node_1", "node_2", "node_3"]),
    ("node_4", ["node_1", "node_3", "node_5"]),
    ("node_2", ["node_2", "node_5", "node_1"]),
]

hits = sum(1 for correct, retrieved in eval_data if correct in retrieved)
hit_rate = hits / len(eval_data)

print(f"Hit rate: {hit_rate:.2f}")
""",
                "skill_tested":  ["llamaindex", "evaluation", "retrieval-metrics"],
            },
        ],
        "quiz": {
            "title":         "Evaluation Quiz",
            "questions":     [
                {
                    "question": "Why is evaluation necessary even if a RAG system runs without errors?",
                    "options": [
                        "Because running without errors guarantees correct answers",
                        "Because a system can run perfectly and still give wrong or ungrounded answers",
                        "Evaluation is only needed for embeddings, not RAG",
                        "Evaluation is optional and rarely useful"
                    ],
                    "correct": 1,
                    "explanation": "The lesson opens with exactly this point: a RAG system can run perfectly but still produce incorrect answers, so evaluation is needed to measure actual quality."
                },
                {
                    "question": "What are the two major areas evaluated in a RAG system?",
                    "options": [
                        "Cost and latency only",
                        "Retrieval quality and answer quality",
                        "Embedding size and index size",
                        "Number of documents and number of nodes"
                    ],
                    "correct": 1,
                    "explanation": "RAG evaluation splits into retrieval quality (did we find the right information?) and answer quality (did the LLM use it correctly?)."
                },
                {
                    "question": "What does 'Top-K retrieval evaluation' measure?",
                    "options": [
                        "Whether the correct information appears within the top K retrieved results",
                        "How many kilobytes each node takes up",
                        "The number of tools an agent has access to",
                        "How fast the LLM generates a response"
                    ],
                    "correct": 0,
                    "explanation": "Top-K evaluation checks whether the correct/expected information shows up within the top K results returned by the retriever (e.g. Top-1, Top-3, Top-5)."
                },
                {
                    "question": "What is a hallucination in the context of RAG?",
                    "options": [
                        "When the retriever returns zero results",
                        "When the model generates information that isn't supported by the retrieved/available data",
                        "When the embedding model fails to load",
                        "When a Node is split into too many chunks"
                    ],
                    "correct": 1,
                    "explanation": "Hallucination is when the LLM generates a fact or claim (like a wrong GPA number) that isn't actually supported by the source data."
                },
                {
                    "question": "In the restaurant analogy, what does the lesson say happens if the wrong ingredients are retrieved?",
                    "options": [
                        "Improving the chef (LLM) will still fix the meal completely",
                        "Improving the chef (LLM) won't solve the problem — the ingredients (retrieval) need to be right first",
                        "The meal will still turn out correct regardless of ingredients",
                        "It has no effect on the final meal"
                    ],
                    "correct": 1,
                    "explanation": "If the retriever finds the wrong ingredients (information), even a great LLM ('chef') can't produce a correct answer — retrieval quality is foundational."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "LlamaIndex + FastAPI",
        "slug":              "llamaindex-and-fastapi",
        "description":       "Expose a LlamaIndex RAG system as a FastAPI backend with a /ask endpoint, understand the frontend/backend architecture, and load the index once at startup instead of per-request.",
        "order":             14,
        "difficulty":        DifficultyLevel.advanced,
        "estimated_hours":   1.5,
        "skill_tags":        ["llamaindex", "fastapi", "backend", "rag", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "LlamaIndex + FastAPI",
            "content":              """We're almost finished!

Today we'll connect: LlamaIndex + FastAPI

This is important because a real AI application usually needs a backend API that a frontend can communicate with.

## 1. What is FastAPI?

FastAPI is a Python framework for creating APIs.

Think of an API as a bridge:

```
Frontend
   ↓
  API
   ↓
Python / LlamaIndex
   ↓
  AI
```

For example, your frontend might send "What is the minimum GPA?" to your backend. FastAPI receives it and sends it to LlamaIndex.

## 2. The architecture

Our application will look like:

```
             User
               ↓
        React / Frontend
               ↓
            FastAPI
               ↓
          LlamaIndex
               ↓
        Retriever / RAG
               ↓
              LLM
               ↓
            Answer
               ↓
            FastAPI
               ↓
           Frontend
```

This is a very common architecture for AI applications.

## 3. Install FastAPI

Inside your virtual environment:

```bash
pip install fastapi uvicorn
```

## 4. Create a simple LlamaIndex backend

Create `app.py`. Start with:

```python
from fastapi import FastAPI
from llama_index.core import Document, VectorStoreIndex


app = FastAPI()


document = Document(
    text=\"\"\"
    The AI Engineering program requires 160 credit hours.
    The minimum GPA required for graduation is 2.0.
    \"\"\"
)


index = VectorStoreIndex.from_documents([document])


query_engine = index.as_query_engine()
```

Now our LlamaIndex system exists inside our API.

## 5. Create an API endpoint

Add:

```python
@app.get("/ask")
def ask(question: str):
    response = query_engine.query(question)

    return {
        "answer": str(response)
    }
```

Now our application has `GET /ask`. The user can send `/ask?question=What%20is%20the%20minimum%20GPA?` and the API returns something like:

```json
{
    "answer": "The minimum GPA required for graduation is 2.0."
}
```

## 6. Run the server

Run:

```bash
uvicorn app:app --reload
```

You should see something similar to: `Uvicorn running on http://127.0.0.1:8000`

Now your LlamaIndex application is running as an API.

## 7. Test it

Open `http://127.0.0.1:8000/docs`.

FastAPI automatically gives you an interactive API documentation page. You'll see `GET /ask`. You can click it, enter "What is the minimum GPA?", and execute it.

## 8. Why is /docs useful?

FastAPI automatically generates API documentation. So instead of manually creating documentation, you get an interface where you can test your endpoints.

```
FastAPI
   ↓
/docs
   ↓
Test your API
```

## 9. Frontend connection

Now imagine you have a React frontend. The frontend sends `POST /ask` with `{"question": "What is the minimum GPA?"}`.

FastAPI: Request → LlamaIndex → RAG → Answer.

Then returns `{"answer": "The minimum GPA is 2.0."}`.

The frontend displays: "AI: The minimum GPA required for graduation is 2.0."

## 10. Why this matters

You can now separate your application into two parts:

**Frontend** — Responsible for UI, Chat window, Buttons, User experience.

**Backend** — Responsible for LlamaIndex, RAG, LLM, Database, Authentication, Business logic.

```
┌──────────────────┐
│     Frontend     │
│                  │
│   💬 Chat UI     │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│     FastAPI      │
│                  │
│    LlamaIndex    │
│       RAG        │
│       LLM        │
└──────────────────┘
```

## 11. One important production improvement

In a real application, don't rebuild the index every time a user sends a question.

**Bad architecture:** Request → Create documents → Create index → Ask question → Answer. That is inefficient.

**Instead:** Application starts → Load index once → Wait for requests → Question → Query existing index → Answer. This is much better.

## 12. Your future architecture

Eventually, your project can look like:

```
                   React
                     ↓
                  FastAPI
                     ↓
              ┌──────┴──────┐
              ↓             ↓
         LlamaIndex       Tools
              ↓
         ┌────┴────┐
         ↓         ↓
      Retriever  Reranker
         ↓
    Vector Database
         ↓
         LLM
         ↓
       Answer
```

That's a real AI application architecture.

## 🧠 Remember

**FastAPI** — Creates an API around your LlamaIndex application.

**Endpoint** — A URL where your application accepts requests, e.g. `GET /ask`.

**Architecture** — Frontend → FastAPI → LlamaIndex → RAG → LLM.

## ⭐ One sentence to remember

FastAPI lets your frontend communicate with your LlamaIndex/RAG backend through API endpoints.
""",
            "order":                14,
            "estimated_minutes":    45,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Expose a RAG System as a FastAPI Endpoint",
                "description":   "Build a FastAPI app that wraps a LlamaIndex query engine behind a GET /ask endpoint accepting a `question` query parameter and returning a JSON answer.",
                "difficulty":    DifficultyLevel.advanced,
                "starter_code":  """from fastapi import FastAPI
from llama_index.core import Document, VectorStoreIndex

app = FastAPI()

document = Document(
    text=\"\"\"
    The AI Engineering program requires 160 credit hours.
    The minimum GPA required for graduation is 2.0.
    \"\"\"
)

index = VectorStoreIndex.from_documents([document])
query_engine = index.as_query_engine()

# TODO: create a GET /ask endpoint that accepts `question: str`,
# queries query_engine, and returns {"answer": ...}
""",
                "solution_code": """from fastapi import FastAPI
from llama_index.core import Document, VectorStoreIndex

app = FastAPI()

document = Document(
    text=\"\"\"
    The AI Engineering program requires 160 credit hours.
    The minimum GPA required for graduation is 2.0.
    \"\"\"
)

index = VectorStoreIndex.from_documents([document])
query_engine = index.as_query_engine()


@app.get("/ask")
def ask(question: str):
    response = query_engine.query(question)
    return {"answer": str(response)}
""",
                "skill_tested":  ["llamaindex", "fastapi", "backend"],
            },
        ],
        "quiz": {
            "title":         "LlamaIndex + FastAPI Quiz",
            "questions":     [
                {
                    "question": "What is FastAPI used for in this architecture?",
                    "options": [
                        "It replaces the LLM entirely",
                        "It's a Python framework that creates an API bridging the frontend and the LlamaIndex/RAG backend",
                        "It's a vector database",
                        "It's an embedding model"
                    ],
                    "correct": 1,
                    "explanation": "FastAPI is a Python API framework that acts as the bridge between a frontend and the LlamaIndex/RAG backend logic."
                },
                {
                    "question": "Which decorator/route is used to create the example question-answering endpoint?",
                    "options": [
                        "@app.post(\"/answer\")",
                        "@app.get(\"/ask\")",
                        "@app.route(\"/query\")",
                        "@app.query(\"/ask\")"
                    ],
                    "correct": 1,
                    "explanation": "The lesson defines `@app.get(\"/ask\")` with a `question: str` parameter that queries the query engine and returns the answer."
                },
                {
                    "question": "Why is it important to load the VectorStoreIndex once at application startup instead of rebuilding it on every request?",
                    "options": [
                        "FastAPI requires the index to be created exactly once by design",
                        "Rebuilding it every request is inefficient — you want to load once and reuse it for all incoming requests",
                        "The index can only be created a single time ever, across restarts",
                        "It has no effect on performance either way"
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly calls out the 'bad architecture' of rebuilding documents/index per request versus loading the index once at startup and querying it repeatedly."
                },
                {
                    "question": "What does visiting /docs on a running FastAPI app give you?",
                    "options": [
                        "A list of all Python packages installed",
                        "Automatically generated, interactive API documentation you can use to test endpoints",
                        "The raw source code of app.py",
                        "A live chat with the LLM directly, bypassing the API"
                    ],
                    "correct": 1,
                    "explanation": "FastAPI auto-generates interactive documentation at /docs where you can view and test endpoints like GET /ask directly in the browser."
                },
                {
                    "question": "In the frontend/backend separation described, which responsibilities belong to the backend?",
                    "options": [
                        "Chat window UI and buttons",
                        "LlamaIndex, RAG, LLM, database, authentication, and business logic",
                        "Only CSS styling",
                        "Only the visual chat bubble layout"
                    ],
                    "correct": 1,
                    "explanation": "The backend (FastAPI) is responsible for LlamaIndex, RAG, LLM, database, authentication, and business logic, while the frontend handles UI and user experience."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            None,
            "description":      None,
            "difficulty":       None,
            "tech_stack":       [],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  None,
        },
    },
    {
        # ToolTopic fields
        "title":            "Final Project: Build a Complete RAG App",
        "slug":              "final-project-complete-rag-app",
        "description":       "Bring together every concept from the course — Documents, Nodes, Embeddings, Index, Retriever, Reranker, LLM, and FastAPI — into a complete document question-answering RAG application, and take on a capstone Academic Advisor AI project.",
        "order":             15,
        "difficulty":        DifficultyLevel.advanced,
        "estimated_hours":   2.0,
        "skill_tags":        ["llamaindex", "rag", "fastapi", "capstone", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Final Project: Build a Complete RAG App",
            "content":              """Congratulations! 🎉

You've reached the final lesson of our 15-lesson LlamaIndex course.

Now we're going to connect everything you've learned.

## 1. What are we building?

We'll build a simple 📚 Document Question-Answering AI. The user gives us documents and asks questions about them.

```
User:
"What is the minimum GPA required?"
       ↓
     LlamaIndex
       ↓
Search Documents
       ↓
Relevant Information
       ↓
      LLM
       ↓
AI:
"The minimum GPA required is 2.0."
```

## 2. Complete architecture

Here's the system you've learned how to build:

```
                    USER
                      │
                      ↓
                 FastAPI API
                      │
                      ↓
                  LlamaIndex
                      │
                      ↓
                  Documents
                      │
                      ↓
                    Nodes
                      │
                      ↓
                  Embeddings
                      │
                      ↓
                Vector Index
                      │
                      ↓
                  Retriever
                      │
                      ↓
                  Reranker
                      │
                      ↓
                 Relevant Data
                      │
                      ↓
                     LLM
                      │
                      ↓
                   Answer
```

This is the big picture.

## 3. Project structure

A simple project could look like:

```
llamaindex-rag/
│
├── app.py
├── data/
│   ├── document1.txt
│   └── document2.txt
│
├── requirements.txt
└── README.md
```

Later you can expand it:

```
llamaindex-rag/
│
├── app/
│   ├── main.py
│   ├── rag.py
│   ├── tools.py
│   └── config.py
│
├── data/
│
├── tests/
│
└── requirements.txt
```

## 4. Step 1 — Load documents

Instead of manually creating `Document(text="...")`, we can load files.

LlamaIndex has document loaders/readers for many data sources. For example, a directory of documents can be loaded with:

```python
from llama_index.core import SimpleDirectoryReader


documents = SimpleDirectoryReader(
    "data"
).load_data()
```

Now: `data/` (file1.txt, file2.pdf, file3.docx) → `SimpleDirectoryReader` → Documents.

## 5. Step 2 — Create the index

```python
from llama_index.core import VectorStoreIndex


index = VectorStoreIndex.from_documents(
    documents
)
```

Conceptually: Documents → Nodes → Embeddings → Vector Index.

## 6. Step 3 — Create the query engine

```python
query_engine = index.as_query_engine()
```

Now we can ask:

```python
response = query_engine.query(
    "What are the graduation requirements?"
)

print(response)
```

## 7. Step 4 — Add FastAPI

Now expose the system through an API.

```python
from fastapi import FastAPI


app = FastAPI()
```

Create an endpoint:

```python
@app.get("/ask")
def ask(question: str):

    response = query_engine.query(question)

    return {
        "answer": str(response)
    }
```

Now your application looks like: Frontend → GET /ask → FastAPI → LlamaIndex → RAG → Answer.

## 8. Complete basic project

Here's the core idea in one file:

```python
from fastapi import FastAPI
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex
)


app = FastAPI()


# Load documents
documents = SimpleDirectoryReader(
    "data"
).load_data()


# Create index
index = VectorStoreIndex.from_documents(
    documents
)


# Create query engine
query_engine = index.as_query_engine()


@app.get("/ask")
def ask(question: str):

    response = query_engine.query(question)

    return {
        "answer": str(response)
    }
```

Run it:

```bash
uvicorn app:app --reload
```

Then visit `http://127.0.0.1:8000/docs`. You can test your RAG API there.

## 9. What you've learned

Let's connect every lesson:

- **Lesson 1** — What LlamaIndex is (LLM + Your Data)
- **Lesson 2** — Created a Document
- **Lesson 3** — Document → Nodes
- **Lesson 4** — Text → Embeddings → Vector Store
- **Lesson 5** — Index → Query Engine
- **Lesson 6** — Built RAG
- **Lesson 7** — Retriever
- **Lesson 8** — Metadata + Filtering
- **Lesson 9** — Reranking
- **Lesson 10** — Chat + Memory
- **Lesson 11** — Tools + Agents
- **Lesson 12** — Workflows
- **Lesson 13** — Evaluation
- **Lesson 14** — LlamaIndex + FastAPI
- **Lesson 15** — Put the pieces together

## 10. The most important architecture to remember

Don't try to memorize every class and function. Remember this:

```
                 YOUR DATA
                     ↓
                 Documents
                     ↓
                   Nodes
                     ↓
                Embeddings
                     ↓
                Vector Store
                     ↓
                 Retriever
                     ↓
                 Reranker
                     ↓
              Relevant Context
                     ↓
                    LLM
                     ↓
                  Answer
```

And when you need a real application:

```
Frontend
   ↓
FastAPI
   ↓
LlamaIndex
   ↓
   RAG
   ↓
LLM
   ↓
Answer
```

## 🎓 You now understand the LlamaIndex fundamentals

You went from "What is LlamaIndex?" to understanding: Documents, Nodes, Embeddings, Vector Stores, Indexes, Retrievers, Reranking, RAG, Chat, Memory, Tools, Agents, Workflows, Evaluation, FastAPI.

That's a solid foundation.

## 🚀 What I recommend next

Since you already have experience with LangChain, LangGraph, RAG, FAISS/Qdrant, embeddings, rerankers, and FastAPI, don't stop here.

The best next step is to build one serious LlamaIndex project rather than doing another long theory course.

A great project would be:

```
        🎓 Academic Advisor AI
                 │
                 ↓
        University Documents
                 │
                 ↓
             LlamaIndex
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
     Retrieval Reranker  Metadata
        │        │        │
        └────────┼────────┘
                 ↓
                LLM
                 ↓
          Arabic AI Advisor
                 ↓
              FastAPI
                 ↓
          Web Application
```

That project would let you practice almost everything you've learned here while building something close to a real production RAG system.
""",
            "order":                15,
            "estimated_minutes":    50,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Assemble the Complete RAG Pipeline",
                "description":   "Load documents from a data directory, build an index, create a query engine, and expose it via a FastAPI /ask endpoint — combining every piece from the course into one file.",
                "difficulty":    DifficultyLevel.advanced,
                "starter_code":  """from fastapi import FastAPI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

app = FastAPI()

# TODO: load documents from the "data" directory
documents = ___

# TODO: build the index
index = ___

# TODO: create the query engine
query_engine = ___

# TODO: create a GET /ask endpoint that accepts `question: str`
# and returns {"answer": ...}
""",
                "solution_code": """from fastapi import FastAPI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

app = FastAPI()

documents = SimpleDirectoryReader("data").load_data()

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()


@app.get("/ask")
def ask(question: str):
    response = query_engine.query(question)
    return {"answer": str(response)}
""",
                "skill_tested":  ["llamaindex", "rag", "fastapi", "capstone"],
            },
        ],
        "quiz": {
            "title":         "Final Project Quiz",
            "questions":     [
                {
                    "question": "Which class is used to load a whole directory of files (txt, pdf, docx) into Documents?",
                    "options": [
                        "DocumentLoader",
                        "SimpleDirectoryReader",
                        "FileIndex",
                        "BulkDocumentImporter"
                    ],
                    "correct": 1,
                    "explanation": "`SimpleDirectoryReader(\"data\").load_data()` loads all supported files from a directory and converts them into Document objects."
                },
                {
                    "question": "In the complete pipeline diagram, what comes immediately after the Retriever and before the LLM?",
                    "options": [
                        "SimpleDirectoryReader",
                        "Reranker",
                        "FastAPI",
                        "Embeddings"
                    ],
                    "correct": 1,
                    "explanation": "The full architecture shown is: ... Vector Index → Retriever → Reranker → Relevant Data → LLM → Answer."
                },
                {
                    "question": "Which lesson introduced Metadata + Filtering, according to the course recap?",
                    "options": [
                        "Lesson 5",
                        "Lesson 8",
                        "Lesson 11",
                        "Lesson 14"
                    ],
                    "correct": 1,
                    "explanation": "The recap explicitly lists Lesson 8 as Metadata + Filtering."
                },
                {
                    "question": "What is the suggested capstone project to practice most of the course's concepts together?",
                    "options": [
                        "A weather forecasting app",
                        "An Academic Advisor AI using university documents, retrieval, reranker, metadata, LLM, and FastAPI",
                        "A pure calculator agent with no retrieval",
                        "A static HTML landing page"
                    ],
                    "correct": 1,
                    "explanation": "The lesson recommends building an Academic Advisor AI: University Documents → LlamaIndex (Retrieval + Reranker + Metadata) → LLM → Arabic AI Advisor → FastAPI → Web Application."
                },
                {
                    "question": "What is the recommended next step after finishing this course, given prior LangChain/RAG/FastAPI experience?",
                    "options": [
                        "Immediately start a new unrelated theory course",
                        "Build one serious LlamaIndex project rather than another long theory course",
                        "Stop learning about RAG entirely",
                        "Only focus on embeddings from now on"
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly recommends building one serious project (like the Academic Advisor AI) instead of doing another long theory course, given the learner's existing background."
                }
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Academic Advisor AI",
            "description":      "Build a production-style RAG application that answers student questions about university rules (GPA, credit hours, registration, tuition) using real university documents. The system should combine retrieval, reranking, and metadata filtering, generate answers in Arabic, and be exposed through a FastAPI backend suitable for a web frontend.",
            "difficulty":       DifficultyLevel.advanced,
            "tech_stack":       ["LlamaIndex", "Python", "FastAPI", "Vector Database", "Reranker Model"],
            "objectives":       [
                "Load real university documents (rules, GPA policy, tuition, registration) with SimpleDirectoryReader",
                "Build a VectorStoreIndex and attach metadata (e.g. topic, department, year) to documents",
                "Implement a retriever with a sensible similarity_top_k and add a reranker (e.g. BAAI/bge-reranker-v2-m3) as a node postprocessor",
                "Combine metadata filtering with semantic retrieval to narrow searches by topic",
                "Generate grounded answers in Arabic and avoid hallucinating information not present in the source documents",
                "Expose the system through a FastAPI GET/POST endpoint (e.g. /ask) that loads the index once at startup",
                "Create a small evaluation dataset of test questions and measure retrieval hit rate and answer correctness",
            ],
            "rubric":           {
                "retrieval_quality": "Correct information is retrieved for at least 80% of test questions (Top-5 hit rate)",
                "answer_grounding": "Answers are grounded in retrieved documents with no unsupported (hallucinated) claims",
                "reranking": "A reranker is correctly wired into the query pipeline via node_postprocessors",
                "metadata_usage": "Documents are tagged with meaningful metadata and at least one query path uses metadata filtering",
                "api_design": "FastAPI endpoint(s) are functional, the index is loaded once at startup (not rebuilt per request), and /docs works",
                "language_quality": "Generated Arabic answers are clear, natural, and correctly reflect the retrieved source content",
            },
            "starter_repo_url": None,
            "estimated_hours":  10.0,
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

        if t["project"].get("title") is None:
            print("    - No project defined for this topic, skipping")
        elif not db.query(Project).filter(Project.tool_topic_id == topic.id).first():
            db.add(Project(tool_topic_id=topic.id, **t["project"]))
            print("    + Project added")
        else:
            print("    - Project exists, skipping")

    db.commit()
    print("Done.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()