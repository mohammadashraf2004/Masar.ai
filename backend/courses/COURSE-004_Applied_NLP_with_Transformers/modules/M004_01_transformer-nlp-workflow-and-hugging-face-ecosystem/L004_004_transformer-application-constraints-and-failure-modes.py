"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-004'
MODULE_ID = 'M004-01'
LESSON_META = {
    "lesson_id": "L004-004",
    "module_id": "M004-01",
    "title": "Transformer Application Constraints & Failure Modes",
    "learning_objective": "Identify constraints that can invalidate an otherwise good Transformer prototype.",
    "concepts": [
        "language coverage",
        "labels",
        "context limits",
        "bias",
        "latency",
        "error analysis"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 1,
        "chapter_title": "Hello Transformers",
        "pages": "19-20"
    },
    "estimated_minutes": 30,
    "prerequisites": [
        "L004-003"
    ],
    "modernization": [
        "Use the current PyTorch-first Transformers ecosystem and current model-card/evaluation workflows."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Transformer Application Constraints & Failure Modes',
    "slug": 'course-004-transformer-application-constraints-and-failure-modes',
    "description": 'Identify constraints that can invalidate an otherwise good Transformer prototype.',
    "order": 4,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.5,
    "skill_tags": ['applied-nlp', 'transformers', 'language-coverage', 'labels', 'context-limits', 'bias'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Transformer Application Constraints & Failure Modes',
        "content": '# Transformer Application Constraints & Failure Modes\n\n## Learning objective\nIdentify constraints that can invalidate an otherwise good Transformer prototype.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 1\n- Pages: 19-20\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **language coverage**\n- **labels**\n- **context limits**\n- **bias**\n- **latency**\n- **error analysis**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Transformer Application Constraints & Failure Modes**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use the current PyTorch-first Transformers ecosystem and current model-card/evaluation workflows.\n',
        "estimated_minutes": 30,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Transformer Application Constraints & Failure Modes — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Identify constraints that can invalidate an otherwise good Transformer prototype.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['language-coverage', 'labels', 'context-limits'],
                },
        {
                    'title': 'Transformer Application Constraints & Failure Modes — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Transformer Application Constraints & Failure Modes — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Transformer Application Constraints & Failure Modes"?', 'options': ['Identify constraints that can invalidate an otherwise good Transformer prototype.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": {
            'title': 'Transformer Task Explorer',
            'description': 'Prototype at least four NLP tasks, inspect model cards and failure cases, and document limitations.',
            'difficulty': DifficultyLevel.intermediate,
            'tech_stack': ['Python', 'PyTorch', 'Hugging Face Transformers'],
            'objectives': ['Build a reproducible workflow', 'Compare against a baseline', 'Debug concrete failures', 'Evaluate with task-appropriate metrics', 'Document limitations'],
            'rubric': {'correctness': 30, 'evaluation': 25, 'debugging': 20, 'reproducibility': 15, 'documentation': 10},
            'starter_repo_url': None,
            'estimated_hours': 3.0,
        },
}
