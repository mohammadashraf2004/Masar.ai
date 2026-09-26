"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-069'
MODULE_ID = 'M004-11'
LESSON_META = {
    "lesson_id": "L004-069",
    "module_id": "M004-11",
    "title": "Scaling Laws & Compute-Optimal Transformer Training",
    "learning_objective": "Reason jointly about model parameters, training tokens, compute, quality, and inference cost.",
    "concepts": [
        "scaling laws",
        "compute-optimal training",
        "model/data balance",
        "data quality",
        "inference cost"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 11,
        "chapter_title": "Future Directions",
        "pages": "345-350"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-068"
    ],
    "modernization": [
        "Treat 2021 frontier examples as foundations; connect to compute-optimal scaling, efficient exact attention kernels, and modern multimodal systems."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Scaling Laws & Compute-Optimal Transformer Training',
    "slug": 'course-004-scaling-laws-and-compute-optimal-transformer-training',
    "description": 'Reason jointly about model parameters, training tokens, compute, quality, and inference cost.',
    "order": 1,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'scaling-laws', 'compute-optimal-training', 'model-data-balance', 'data-quality'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Scaling Laws & Compute-Optimal Transformer Training',
        "content": '# Scaling Laws & Compute-Optimal Transformer Training\n\n## Learning objective\nReason jointly about model parameters, training tokens, compute, quality, and inference cost.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 11\n- Pages: 345-350\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **scaling laws**\n- **compute-optimal training**\n- **model/data balance**\n- **data quality**\n- **inference cost**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Scaling Laws & Compute-Optimal Transformer Training**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Treat 2021 frontier examples as foundations; connect to compute-optimal scaling, efficient exact attention kernels, and modern multimodal systems.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Scaling Laws & Compute-Optimal Transformer Training — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Reason jointly about model parameters, training tokens, compute, quality, and inference cost.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['scaling-laws', 'compute-optimal-training', 'model-data-balance'],
                },
        {
                    'title': 'Scaling Laws & Compute-Optimal Transformer Training — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Scaling Laws & Compute-Optimal Transformer Training — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Scaling Laws & Compute-Optimal Transformer Training"?', 'options': ['Reason jointly about model parameters, training tokens, compute, quality, and inference cost.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
