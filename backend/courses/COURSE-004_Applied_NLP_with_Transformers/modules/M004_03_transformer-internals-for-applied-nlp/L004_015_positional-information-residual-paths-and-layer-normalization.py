"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-015'
MODULE_ID = 'M004-03'
LESSON_META = {
    "lesson_id": "L004-015",
    "module_id": "M004-03",
    "title": "Positional Information, Residual Paths & Layer Normalization",
    "learning_objective": "Explain how position information and normalization/residual design affect Transformer behavior.",
    "concepts": [
        "positional embeddings",
        "normalization",
        "residual paths",
        "stability",
        "representation flow"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 3,
        "chapter_title": "Transformer Anatomy",
        "pages": "71-76"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-014"
    ],
    "modernization": [
        "Treat deep architecture theory as revision; use current PyTorch attention APIs for implementation inspection."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Positional Information, Residual Paths & Layer Normalization',
    "slug": 'course-004-positional-information-residual-paths-and-layer-normalization',
    "description": 'Explain how position information and normalization/residual design affect Transformer behavior.',
    "order": 4,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'positional-embeddings', 'normalization', 'residual-paths', 'stability'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Positional Information, Residual Paths & Layer Normalization',
        "content": '# Positional Information, Residual Paths & Layer Normalization\n\n## Learning objective\nExplain how position information and normalization/residual design affect Transformer behavior.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 3\n- Pages: 71-76\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **positional embeddings**\n- **normalization**\n- **residual paths**\n- **stability**\n- **representation flow**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Positional Information, Residual Paths & Layer Normalization**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Treat deep architecture theory as revision; use current PyTorch attention APIs for implementation inspection.\n\n## Prerequisite-depth note\nThis is a concise COURSE-004 revision/application lesson. For full attention mathematics, derivations, and deep architecture theory, return to COURSE-002 — Deep Learning Foundations.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Positional Information, Residual Paths & Layer Normalization — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Explain how position information and normalization/residual design affect Transformer behavior.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['positional-embeddings', 'normalization', 'residual-paths'],
                },
        {
                    'title': 'Positional Information, Residual Paths & Layer Normalization — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Positional Information, Residual Paths & Layer Normalization — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Positional Information, Residual Paths & Layer Normalization"?', 'options': ['Explain how position information and normalization/residual design affect Transformer behavior.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
