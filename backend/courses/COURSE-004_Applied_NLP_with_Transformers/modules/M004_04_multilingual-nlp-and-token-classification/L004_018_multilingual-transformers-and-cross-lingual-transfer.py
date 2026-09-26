"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-018'
MODULE_ID = 'M004-04'
LESSON_META = {
    "lesson_id": "L004-018",
    "module_id": "M004-04",
    "title": "Multilingual Transformers & Cross-Lingual Transfer",
    "learning_objective": "Explain multilingual pretraining and when cross-lingual transfer can reduce labeling requirements.",
    "concepts": [
        "XLM-R",
        "multilingual pretraining",
        "zero-shot transfer",
        "language families",
        "code-switching"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 4,
        "chapter_title": "Multilingual Named Entity Recognition",
        "pages": "92-93"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-017"
    ],
    "modernization": [
        "Prefer AutoModelForTokenClassification for production code; custom model-head code is anatomy practice."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Multilingual Transformers & Cross-Lingual Transfer',
    "slug": 'course-004-multilingual-transformers-and-cross-lingual-transfer',
    "description": 'Explain multilingual pretraining and when cross-lingual transfer can reduce labeling requirements.',
    "order": 2,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'xlm-r', 'multilingual-pretraining', 'zero-shot-transfer', 'language-families'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Multilingual Transformers & Cross-Lingual Transfer',
        "content": '# Multilingual Transformers & Cross-Lingual Transfer\n\n## Learning objective\nExplain multilingual pretraining and when cross-lingual transfer can reduce labeling requirements.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 4\n- Pages: 92-93\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **XLM-R**\n- **multilingual pretraining**\n- **zero-shot transfer**\n- **language families**\n- **code-switching**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Multilingual Transformers & Cross-Lingual Transfer**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Prefer AutoModelForTokenClassification for production code; custom model-head code is anatomy practice.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Multilingual Transformers & Cross-Lingual Transfer — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Explain multilingual pretraining and when cross-lingual transfer can reduce labeling requirements.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['xlm-r', 'multilingual-pretraining', 'zero-shot-transfer'],
                },
        {
                    'title': 'Multilingual Transformers & Cross-Lingual Transfer — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Multilingual Transformers & Cross-Lingual Transfer — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Multilingual Transformers & Cross-Lingual Transfer"?', 'options': ['Explain multilingual pretraining and when cross-lingual transfer can reduce labeling requirements.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
