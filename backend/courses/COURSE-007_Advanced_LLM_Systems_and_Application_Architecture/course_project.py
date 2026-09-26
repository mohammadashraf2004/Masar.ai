"""MASAR ADDITION — COURSE-007 capstone metadata."""
from app.models.learning import DifficultyLevel

COURSE_PROJECT = {
    "title": 'Production LLM System Architecture Capstone',
    "description": 'Produce a production-ready architecture specification for an LLM application with routing, RAG, tools, memory, reliability controls, observability points, and measurable acceptance criteria.',
    "difficulty": DifficultyLevel.intermediate,
    "tech_stack": ["Python", "LLM provider or open model", "retrieval stack", "evaluation tooling"],
    "objectives": [
        "Compose an end-to-end LLM system architecture",
        "Define routing, RAG, tools, memory, and reliability boundaries",
        "Specify measurable latency, cost, and quality acceptance criteria",
        "Document failure modes, verification points, and fallbacks",
        "Produce a reproducible architecture and evaluation handoff",
    ],
    "rubric": {"architecture": 25, "reliability": 25, "evaluation": 20, "tradeoffs": 15, "reproducibility": 15},
    "starter_repo_url": None,
    "estimated_hours": 8.0,
}
