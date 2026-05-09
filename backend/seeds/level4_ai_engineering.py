from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Project


def seed_level4(db, track: CareerTrack):
    level = TrackLevel(
        track_id=track.id,
        title="AI Engineering",
        description="RAG, Vector DBs, LangChain, FastAPI, Deployment",
        order=4,
    )
    db.add(level)
    db.flush()

    topic = Topic(
        level_id=level.id,
        title="RAG Systems",
        slug="rag-systems",
        description="Retrieval-Augmented Generation: build production AI apps with real knowledge",
        order=1,
        difficulty="advanced",
        estimated_hours=20,
        prerequisite_ids=[],
        skill_tags=["rag", "vector-db", "embeddings", "langchain", "llm"],
    )
    db.add(topic)
    db.flush()

    db.add(Lesson(
        topic_id=topic.id,
        title="RAG Architecture Deep Dive",
        order=1,
        estimated_minutes=35,
        has_code_examples=True,
        content="""## RAG: Retrieval-Augmented Generation

RAG solves LLMs' biggest limitation: they can't access your private data.

### The Flow

```
Query → Embed → Search Vector DB → Retrieve Chunks → LLM → Answer
```

### Implementation

```python
from anthropic import Anthropic
import chromadb

client     = Anthropic()
chroma     = chromadb.Client()
collection = chroma.create_collection("docs")

def add_documents(texts: list[str]):
    collection.add(documents=texts, ids=[f"doc_{i}" for i in range(len(texts))])

def rag_query(question: str) -> str:
    results = collection.query(query_texts=[question], n_results=3)
    context = "\\n\\n".join(results["documents"][0])

    prompt = f\"\"\"Use this context to answer the question.

Context:
{context}

Question: {question}\"\"\"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
```

### Key Concepts
- **Chunking** — split docs into ~500 token segments with overlap
- **Embeddings** — dense vector representations of text meaning
- **Similarity search** — find chunks closest to query vector
- **Context window** — feed top-k chunks to LLM
""",
    ))

    db.add(Project(
        topic_id=topic.id,
        title="PDF Knowledge Base Chatbot",
        description=(
            "Build a full RAG system that ingests PDFs, stores embeddings in pgvector, "
            "and answers questions via a chat API. Deploy with Docker."
        ),
        difficulty="advanced",
        tech_stack=["Python", "FastAPI", "pgvector", "Claude API", "Docker", "PyPDF2"],
        objectives=[
            "Parse and chunk PDF documents",
            "Generate and store embeddings in pgvector",
            "Implement semantic search retrieval",
            "Build conversational chat API with context",
            "Containerise with Docker",
            "Handle edge cases: no relevant context, long docs",
        ],
        rubric={
            "rag_correctness": 35,
            "retrieval_quality": 25,
            "api_design": 20,
            "docker_deployment": 10,
            "documentation": 10,
        },
        estimated_hours=16,
    ))

    print(f"  ✓ Level 4: {level.title} — topic: {topic.title}")
