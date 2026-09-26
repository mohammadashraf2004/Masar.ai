"""Masar COURSE-007 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L007-060'
MODULE_ID = 'M007-10'
LESSON_META = {
    "lesson_id": 'L007-060',
    "module_id": 'M007-10',
    "title": 'Synthesis: Designing a Production LLM System',
    "learning_objective": 'Compose model selection, RAG, tools, agents, memory, guardrails, verifiers, optimization, routing, and fallbacks into one production architecture.',
    "curriculum_role": 'MASAR SYNTHESIS + SYSTEM DESIGN',
    "concepts": ['system architecture', 'model selection', 'routing', 'RAG', 'tools', 'agents', 'memory', 'guardrails', 'verifiers', 'fallbacks', 'latency', 'cost', 'reliability'],
    "source_reference": {"source_id": "BOOK-007", "book_title": "SOURCE INFORMATION MISSING", "edition": "SOURCE INFORMATION MISSING", "chapter": 13, "chapter_title": 'Design Patterns and System Architecture', "pages": "SOURCE INFORMATION MISSING"},
    "estimated_minutes": 45,
    "prerequisites": ['L007-059'],
    "modernization": ["Revalidate model IDs, package APIs, provider interfaces, and framework-specific examples before implementation."],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Synthesis: Designing a Production LLM System',
    "slug": 'course-007-synthesis-designing-a-production-llm-system',
    "description": 'Compose model selection, RAG, tools, agents, memory, guardrails, verifiers, optimization, routing, and fallbacks into one production architecture.',
    "order": 5,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['advanced-llm-systems', 'system-architecture', 'model-selection', 'routing', 'rag'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Synthesis: Designing a Production LLM System',
        "content": "# Synthesis: Designing a Production LLM System\n\n## Learning objective\nCompose model selection, RAG, tools, agents, memory, guardrails, verifiers, optimization, routing, and fallbacks into one production architecture.\n\n## Curriculum role\nMASAR SYNTHESIS + SYSTEM DESIGN\n\n## Source mapping\n- Source: BOOK-007 — SOURCE INFORMATION MISSING\n- Chapter 13: Design Patterns and System Architecture\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson preserves the source chapter's engineering intent while fitting the Masar prerequisite chain. Material already established in COURSE-001 through COURSE-006 is explicitly treated as **revision**; deeper treatment is labeled as extension rather than being presented as a brand-new prerequisite.\n\n## Concepts\n- **system architecture**\n- **model selection**\n- **routing**\n- **RAG**\n- **tools**\n- **agents**\n- **memory**\n- **guardrails**\n- **verifiers**\n- **fallbacks**\n- **latency**\n- **cost**\n- **reliability**\n\n## Engineering workflow\n1. Define the task and the measurable constraint before selecting a technique.\n2. Establish a simple baseline and capture its observable behavior.\n3. Apply the lesson technique to the smallest reproducible example that still exposes the real trade-off.\n4. Inspect an intermediate artifact such as logits, retrieved documents, traces, training samples, memory usage, rankings, or verifier decisions.\n5. Compare the result against the baseline and record at least one failure mode.\n6. State what evidence would make you keep, reject, or modify the approach.\n\n## Practice\nBuild a reproducible artifact that demonstrates how to **compose model selection, RAG, tools, agents, memory, guardrails, verifiers, optimization, routing, and fallbacks into one production architecture**. Use a small controlled input set first, then include at least one difficult or adversarial example that exposes a limitation.\n\n## Debug / evaluate\n- Check data, tokenizer, model, retrieval, tool, or state compatibility before interpreting outputs.\n- Separate model failure from retrieval, orchestration, data, or evaluation failure.\n- Never treat a single successful example as sufficient evidence.\n- Record latency, memory, cost, or quality only when actually measured.\n- Preserve source-era concepts while revalidating current APIs and package interfaces before implementation.\n\n## Assessment\nExplain the principal engineering trade-off, provide evidence from the practice artifact, identify one realistic failure, and state what would change your final architecture decision.\n\n## Source / modernization boundary\nThe instructional framing is original Masar curriculum material grounded in BOOK-007. Code and external APIs must be revalidated against the target repository and current package versions before production use.\n",
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
            "title": 'Synthesis: Designing a Production LLM System — Guided Practice',
            "description": 'Build a reproducible artifact that demonstrates: Compose model selection, RAG, tools, agents, memory, guardrails, verifiers, optimization, routing, and fallbacks into one production architecture.',
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ['system-architecture', 'model-selection', 'routing'],
        },
        {
            "title": 'Synthesis: Designing a Production LLM System — Debug / Evaluate',
            "description": "Introduce or locate one realistic failure, diagnose it with evidence, compare against the baseline, and document the corrective decision.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["debugging", "evaluation"],
        }
    ],
    "quiz": {
        "title": 'Synthesis: Designing a Production LLM System — Knowledge Check',
        "questions": [
            {"question": 'What is the primary objective of Synthesis: Designing a Production LLM System?', "options": ['Compose model selection, RAG, tools, agents, memory, guardrails, verifiers, optimization, routing, and fallbacks into one production architecture.', "Memorize every source paragraph", "Choose the largest model regardless of constraints", "Skip evaluation if the code runs"], "correct": 0, "explanation": "The lesson is organized around the stated engineering learning objective."},
            {"question": "Which practice best matches the Masar learning loop?", "options": ["Learn → Practice → Build → Debug → Evaluate", "Read → Memorize → Stop", "Train once → Deploy without evaluation", "Choose a framework before defining the task"], "correct": 0, "explanation": "COURSE-007 preserves the applied Masar learning loop."},
            {"question": "How should source-era APIs or framework examples be handled?", "options": ["Preserve the concept, revalidate the current API, and label modernization", "Silently copy the old API", "Invent successful output", "Delete the entire lesson"], "correct": 0, "explanation": "Source fidelity and modernization are tracked separately."}
        ],
        "passing_score": 70
    },
    "project": {'title': 'Production LLM System Architecture Capstone', 'description': 'Produce a production-ready architecture specification for an LLM application with routing, RAG, tools, memory, reliability controls, observability points, and measurable acceptance criteria.', 'difficulty': DifficultyLevel.intermediate, 'tech_stack': ['Python', 'LLM / NLP tooling', 'evaluation artifacts'], 'objectives': ['Build a reproducible workflow', 'Compare against a baseline', 'Debug concrete failures', 'Evaluate with task-appropriate evidence', 'Document limitations and trade-offs'], 'rubric': {'correctness': 25, 'evaluation': 25, 'debugging': 20, 'reproducibility': 15, 'documentation': 15}, 'starter_repo_url': None, 'estimated_hours': 8.0},
}
