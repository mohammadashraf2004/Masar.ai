"""Masar COURSE-007 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L007-059'
MODULE_ID = 'M007-10'
LESSON_META = {
    "lesson_id": 'L007-059',
    "module_id": 'M007-10',
    "title": 'Supporting Extension: LMQL & Constrained LLM Programs',
    "learning_objective": 'Express prompts, generation variables, constraints, stopping rules, and control flow as a declarative LLM program.',
    "curriculum_role": 'SUPPORTING EXTENSION',
    "concepts": ['LMQL', 'declarative programming', 'generation constraints', 'output variables', 'stopping conditions', 'program control flow'],
    "source_reference": {"source_id": "BOOK-007", "book_title": "SOURCE INFORMATION MISSING", "edition": "SOURCE INFORMATION MISSING", "chapter": 13, "chapter_title": 'Design Patterns and System Architecture', "pages": "SOURCE INFORMATION MISSING"},
    "estimated_minutes": 30,
    "prerequisites": ['L007-058'],
    "modernization": ["Revalidate model IDs, package APIs, provider interfaces, and framework-specific examples before implementation."],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Supporting Extension: LMQL & Constrained LLM Programs',
    "slug": 'course-007-supporting-extension-lmql-and-constrained-llm-programs',
    "description": 'Express prompts, generation variables, constraints, stopping rules, and control flow as a declarative LLM program.',
    "order": 4,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.5,
    "skill_tags": ['advanced-llm-systems', 'lmql', 'declarative-programming', 'generation-constraints', 'output-variables'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Supporting Extension: LMQL & Constrained LLM Programs',
        "content": "# Supporting Extension: LMQL & Constrained LLM Programs\n\n## Learning objective\nExpress prompts, generation variables, constraints, stopping rules, and control flow as a declarative LLM program.\n\n## Curriculum role\nSUPPORTING EXTENSION\n\n## Source mapping\n- Source: BOOK-007 — SOURCE INFORMATION MISSING\n- Chapter 13: Design Patterns and System Architecture\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson preserves the source chapter's engineering intent while fitting the Masar prerequisite chain. Material already established in COURSE-001 through COURSE-006 is explicitly treated as **revision**; deeper treatment is labeled as extension rather than being presented as a brand-new prerequisite.\n\n## Concepts\n- **LMQL**\n- **declarative programming**\n- **generation constraints**\n- **output variables**\n- **stopping conditions**\n- **program control flow**\n\n## Engineering workflow\n1. Define the task and the measurable constraint before selecting a technique.\n2. Establish a simple baseline and capture its observable behavior.\n3. Apply the lesson technique to the smallest reproducible example that still exposes the real trade-off.\n4. Inspect an intermediate artifact such as logits, retrieved documents, traces, training samples, memory usage, rankings, or verifier decisions.\n5. Compare the result against the baseline and record at least one failure mode.\n6. State what evidence would make you keep, reject, or modify the approach.\n\n## Practice\nBuild a reproducible artifact that demonstrates how to **express prompts, generation variables, constraints, stopping rules, and control flow as a declarative LLM program**. Use a small controlled input set first, then include at least one difficult or adversarial example that exposes a limitation.\n\n## Debug / evaluate\n- Check data, tokenizer, model, retrieval, tool, or state compatibility before interpreting outputs.\n- Separate model failure from retrieval, orchestration, data, or evaluation failure.\n- Never treat a single successful example as sufficient evidence.\n- Record latency, memory, cost, or quality only when actually measured.\n- Preserve source-era concepts while revalidating current APIs and package interfaces before implementation.\n\n## Assessment\nExplain the principal engineering trade-off, provide evidence from the practice artifact, identify one realistic failure, and state what would change your final architecture decision.\n\n## Source / modernization boundary\nThe instructional framing is original Masar curriculum material grounded in BOOK-007. Code and external APIs must be revalidated against the target repository and current package versions before production use.\n",
        "estimated_minutes": 30,
        "has_code_examples": True,
    },
    "exercises": [
        {
            "title": 'Supporting Extension: LMQL & Constrained LLM Programs — Guided Practice',
            "description": 'Build a reproducible artifact that demonstrates: Express prompts, generation variables, constraints, stopping rules, and control flow as a declarative LLM program.',
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ['lmql', 'declarative-programming', 'generation-constraints'],
        },
        {
            "title": 'Supporting Extension: LMQL & Constrained LLM Programs — Debug / Evaluate',
            "description": "Introduce or locate one realistic failure, diagnose it with evidence, compare against the baseline, and document the corrective decision.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["debugging", "evaluation"],
        }
    ],
    "quiz": {
        "title": 'Supporting Extension: LMQL & Constrained LLM Programs — Knowledge Check',
        "questions": [
            {"question": 'What is the primary objective of Supporting Extension: LMQL & Constrained LLM Programs?', "options": ['Express prompts, generation variables, constraints, stopping rules, and control flow as a declarative LLM program.', "Memorize every source paragraph", "Choose the largest model regardless of constraints", "Skip evaluation if the code runs"], "correct": 0, "explanation": "The lesson is organized around the stated engineering learning objective."},
            {"question": "Which practice best matches the Masar learning loop?", "options": ["Learn → Practice → Build → Debug → Evaluate", "Read → Memorize → Stop", "Train once → Deploy without evaluation", "Choose a framework before defining the task"], "correct": 0, "explanation": "COURSE-007 preserves the applied Masar learning loop."},
            {"question": "How should source-era APIs or framework examples be handled?", "options": ["Preserve the concept, revalidate the current API, and label modernization", "Silently copy the old API", "Invent successful output", "Delete the entire lesson"], "correct": 0, "explanation": "Source fidelity and modernization are tracked separately."}
        ],
        "passing_score": 70
    },
    "project": None,
}
