"""
backend/seeds/seed_tool_courses.py

Seeds the 15 tool-course catalog entries across 4 sections. This creates
the browsable/enrollable ToolCourse shells only — no ToolTopic content yet.
Run backend/seeds/seed_tool_<name>.py scripts (following the pattern in
TOOL_COURSES_HANDOFF.md) per tool to add actual lessons/exercises/quizzes/
projects once content is drafted.

Run from backend/:
    python seeds/seed_tool_courses.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine, Base
import app.models.user         # noqa: F401
import app.models.learning     # noqa: F401
import app.models.progress     # noqa: F401
import app.models.community    # noqa: F401
import app.models.wallet       # noqa: F401
import app.models.auth_token   # noqa: F401
import app.models.challenge    # noqa: F401
import app.models.exam         # noqa: F401
from app.models.tool_course import ToolCourse
from app.models.learning import DifficultyLevel

Base.metadata.create_all(bind=engine)

# related_track_ids reference career_tracks.id seeded by seed_tracks.py:
#   1 data-analyst, 2 ml-engineer, 3 ai-developer, 4 mlops-engineer, 5 ai-engineer

TOOL_COURSES = [
    # ── LLM & AI Application Layer ──────────────────────────────────────
    {
        "slug": "langchain", "title": "LangChain", "icon": "🦜",
        "category": "LLM & AI Application Layer",
        "description": "Build LLM pipelines with chains, prompts, models, and output parsers — the most-asked framework in AI Developer interviews.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 12.0,
        "related_track_ids": [3],
    },
    {
        "slug": "langgraph", "title": "LangGraph", "icon": "🕸️",
        "category": "LLM & AI Application Layer",
        "description": "Build agents and multi-step workflows as stateful graphs — the natural next step after LangChain.",
        "difficulty": DifficultyLevel.advanced, "estimated_hours": 10.0,
        "related_track_ids": [3],
    },
    {
        "slug": "llamaindex", "title": "LlamaIndex", "icon": "🦙",
        "category": "LLM & AI Application Layer",
        "description": "A RAG-focused alternative to LangChain, purpose-built for indexing and querying your own documents.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 10.0,
        "related_track_ids": [3],
    },
    {
        "slug": "openai-api", "title": "OpenAI API", "icon": "🤖",
        "category": "LLM & AI Application Layer",
        "description": "Function calling, Assistants, vision, and practical patterns for building on the OpenAI API in production.",
        "difficulty": DifficultyLevel.beginner, "estimated_hours": 8.0,
        "related_track_ids": [3],
    },
    {
        "slug": "hugging-face", "title": "Hugging Face", "icon": "🤗",
        "category": "LLM & AI Application Layer",
        "description": "The model hub, Inference API, and Spaces — finding, running, and deploying open models.",
        "difficulty": DifficultyLevel.beginner, "estimated_hours": 8.0,
        "related_track_ids": [2, 3],
    },

    # ── Vector Databases ─────────────────────────────────────────────────
    {
        "slug": "pinecone", "title": "Pinecone", "icon": "🌲",
        "category": "Vector Databases",
        "description": "The most popular managed vector database — indexing, querying, and scaling semantic search.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 6.0,
        "related_track_ids": [3],
    },
    {
        "slug": "qdrant", "title": "Qdrant", "icon": "🔺",
        "category": "Vector Databases",
        "description": "An open-source vector database built for self-hosted setups, with a strong filtering and payload model.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 6.0,
        "related_track_ids": [3, 4],
    },
    {
        "slug": "weaviate", "title": "Weaviate", "icon": "🕷️",
        "category": "Vector Databases",
        "description": "A vector database built for multimodal search — text, images, and hybrid search in one system.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 6.0,
        "related_track_ids": [3],
    },

    # ── MLOps & Infrastructure ───────────────────────────────────────────
    {
        "slug": "mlflow", "title": "MLflow", "icon": "📊",
        "category": "MLOps & Infrastructure",
        "description": "Experiment tracking and model registry — the standard way ML teams track what they trained and why.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 8.0,
        "related_track_ids": [2, 4],
    },
    {
        "slug": "dvc", "title": "DVC", "icon": "🗃️",
        "category": "MLOps & Infrastructure",
        "description": "Data version control for ML projects — Git-like workflows for datasets and model artifacts.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 6.0,
        "related_track_ids": [2, 4],
    },
    {
        "slug": "wandb", "title": "Weights & Biases (W&B)", "icon": "📈",
        "category": "MLOps & Infrastructure",
        "description": "Training monitoring, experiment comparison, and hyperparameter sweeps for serious model development.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 6.0,
        "related_track_ids": [2],
    },
    {
        "slug": "fastapi-serving", "title": "FastAPI", "icon": "⚡",
        "category": "MLOps & Infrastructure",
        "description": "Serving ML models over HTTP — request validation, async inference, and production-grade API design.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 10.0,
        "related_track_ids": [3, 4],
    },
    {
        "slug": "airflow", "title": "Airflow", "icon": "🌀",
        "category": "MLOps & Infrastructure",
        "description": "Pipeline orchestration — scheduling, retries, and dependency graphs for data and ML workflows.",
        "difficulty": DifficultyLevel.advanced, "estimated_hours": 10.0,
        "related_track_ids": [4],
    },

    # ── Data Tools ───────────────────────────────────────────────────────
    {
        "slug": "dbt", "title": "dbt", "icon": "🔧",
        "category": "Data Tools",
        "description": "Data transformation as SQL + version control — a huge skill in Egyptian fintech and analytics roles.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 8.0,
        "related_track_ids": [1],
    },
    {
        "slug": "great-expectations", "title": "Great Expectations", "icon": "✅",
        "category": "Data Tools",
        "description": "Data quality and validation — catching broken pipelines before they reach a dashboard or a model.",
        "difficulty": DifficultyLevel.intermediate, "estimated_hours": 6.0,
        "related_track_ids": [1, 2],
    },
    {
        "slug": "streamlit", "title": "Streamlit", "icon": "🎈",
        "category": "Data Tools",
        "description": "Rapid ML demo apps — turn a model or a dataset into a shareable interface in an afternoon.",
        "difficulty": DifficultyLevel.beginner, "estimated_hours": 5.0,
        "related_track_ids": [1, 2],
    },
]


def seed_tool_courses(db):
    for data in TOOL_COURSES:
        existing = db.query(ToolCourse).filter(ToolCourse.slug == data["slug"]).first()
        if existing:
            print(f"- {data['slug']} already exists, skipping")
            continue
        db.add(ToolCourse(is_active=True, **data))
        print(f"+ {data['slug']} created")
    db.commit()
    print("Done.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_tool_courses(db)
    finally:
        db.close()
