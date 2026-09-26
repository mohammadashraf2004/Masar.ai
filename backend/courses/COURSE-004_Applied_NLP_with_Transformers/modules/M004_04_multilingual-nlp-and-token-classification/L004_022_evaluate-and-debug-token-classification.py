"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-022'
MODULE_ID = 'M004-04'
LESSON_META = {
    "lesson_id": "L004-022",
    "module_id": "M004-04",
    "title": "Evaluate and Debug Token Classification",
    "learning_objective": "Evaluate entities correctly and use per-token error analysis to reveal model and data failures.",
    "concepts": [
        "precision/recall/F1",
        "entity-level metrics",
        "per-token loss",
        "error slicing",
        "majority O class"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 4,
        "chapter_title": "Multilingual Named Entity Recognition",
        "pages": "105-115"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-021"
    ],
    "modernization": [
        "Prefer AutoModelForTokenClassification for production code; custom model-head code is anatomy practice."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Evaluate and Debug Token Classification',
    "slug": 'course-004-evaluate-and-debug-token-classification',
    "description": 'Evaluate entities correctly and use per-token error analysis to reveal model and data failures.',
    "order": 6,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'precision-recall-f1', 'entity-level-metrics', 'per-token-loss', 'error-slicing'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Evaluate and Debug Token Classification',
        "content": '# Evaluate and Debug Token Classification\n\n## Learning objective\nEvaluate entities correctly and use per-token error analysis to reveal model and data failures.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 4\n- Pages: 105-115\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **precision/recall/F1**\n- **entity-level metrics**\n- **per-token loss**\n- **error slicing**\n- **majority O class**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForTokenClassification\ncheckpoint = "xlm-roberta-base"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForTokenClassification.from_pretrained(checkpoint)\n```\n\n## Practice\nProduce one reproducible artifact for **Evaluate and Debug Token Classification**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Prefer AutoModelForTokenClassification for production code; custom model-head code is anatomy practice.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Evaluate and Debug Token Classification — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Evaluate entities correctly and use per-token error analysis to reveal model and data failures.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['precision-recall-f1', 'entity-level-metrics', 'per-token-loss'],
                },
        {
                    'title': 'Evaluate and Debug Token Classification — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Evaluate and Debug Token Classification — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Evaluate and Debug Token Classification"?', 'options': ['Evaluate entities correctly and use per-token error analysis to reveal model and data failures.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
