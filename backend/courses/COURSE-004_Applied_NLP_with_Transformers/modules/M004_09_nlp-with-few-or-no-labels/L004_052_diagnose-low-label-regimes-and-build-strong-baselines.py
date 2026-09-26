"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-052'
MODULE_ID = 'M004-09'
LESSON_META = {
    "lesson_id": "L004-052",
    "module_id": "M004-09",
    "title": "Diagnose Low-Label Regimes & Build Strong Baselines",
    "learning_objective": "Characterize the label budget and establish robust multilabel baselines and learning curves.",
    "concepts": [
        "label budget",
        "multilabel classification",
        "micro/macro F1",
        "balanced splits",
        "learning curves",
        "Naive Bayes baseline"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 9,
        "chapter_title": "Dealing with Few to No Labels",
        "pages": "249-263"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-051"
    ],
    "modernization": [
        "Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Diagnose Low-Label Regimes & Build Strong Baselines',
    "slug": 'course-004-diagnose-low-label-regimes-and-build-strong-baselines',
    "description": 'Characterize the label budget and establish robust multilabel baselines and learning curves.',
    "order": 1,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'label-budget', 'multilabel-classification', 'micro-macro-f1', 'balanced-splits'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Diagnose Low-Label Regimes & Build Strong Baselines',
        "content": '# Diagnose Low-Label Regimes & Build Strong Baselines\n\n## Learning objective\nCharacterize the label budget and establish robust multilabel baselines and learning curves.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 9\n- Pages: 249-263\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **label budget**\n- **multilabel classification**\n- **micro/macro F1**\n- **balanced splits**\n- **learning curves**\n- **Naive Bayes baseline**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Diagnose Low-Label Regimes & Build Strong Baselines**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Diagnose Low-Label Regimes & Build Strong Baselines — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Characterize the label budget and establish robust multilabel baselines and learning curves.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['label-budget', 'multilabel-classification', 'micro-macro-f1'],
                },
        {
                    'title': 'Diagnose Low-Label Regimes & Build Strong Baselines — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Diagnose Low-Label Regimes & Build Strong Baselines — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Diagnose Low-Label Regimes & Build Strong Baselines"?', 'options': ['Characterize the label budget and establish robust multilabel baselines and learning curves.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
