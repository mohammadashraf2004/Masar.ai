"""MASAR ADDITION — COURSE-008 capstone metadata."""
from app.models.learning import DifficultyLevel

COURSE_PROJECT = {
    "title": "Production Multimodal AI System Capstone",
    "description": "Design and build a production-oriented multimodal AI system with one primary specialization (document, video, visual assistant, or agentic vision), explicit evaluation, failure analysis, and deployment constraints; include an architecture extension plan for any-to-any generation or action-capable behavior.",
    "difficulty": DifficultyLevel.intermediate,
    "tech_stack": ["Python", "PyTorch/Transformers", "multimodal model", "evaluation tooling", "retrieval or serving stack as needed"],
    "objectives": [
        "Integrate perception, representation, inference, and application architecture into one coherent multimodal system",
        "Use grounded evaluation and failure analysis rather than demo-only success",
        "Measure at least one production constraint such as latency, VRAM, throughput, storage, or retrieval cost",
        "Document data, safety, and source-grounding boundaries",
        "Produce a reproducible implementation and architecture handoff"
    ],
    "rubric": {"implementation": 30, "evaluation": 25, "reliability": 20, "architecture": 15, "reproducibility": 10},
    "starter_repo_url": None,
    "estimated_hours": 12.0,
}
