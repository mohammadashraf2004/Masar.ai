"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-058'
MODULE_ID = 'M004-09'
LESSON_META = {
    "lesson_id": "L004-058",
    "module_id": "M004-09",
    "title": "Semi-Supervised Learning with Consistency Training",
    "learning_objective": "Understand and prototype consistency-based semi-supervised learning such as UDA/teacher methods.",
    "concepts": [
        "UDA",
        "consistency loss",
        "augmentation",
        "Mean Teacher awareness",
        "unlabeled data"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 9,
        "chapter_title": "Dealing with Few to No Labels",
        "pages": "294-296"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-057"
    ],
    "modernization": [
        "Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Semi-Supervised Learning with Consistency Training',
    "slug": 'course-004-semi-supervised-learning-with-consistency-training',
    "description": 'Understand and prototype consistency-based semi-supervised learning such as UDA/teacher methods.',
    "order": 7,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'uda', 'consistency-loss', 'augmentation', 'mean-teacher-awareness'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Semi-Supervised Learning with Consistency Training',
        "content": '# Semi-Supervised Learning with Consistency Training\n\n## Learning objective\nUnderstand and prototype consistency-based semi-supervised learning such as UDA/teacher methods.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 9\n- Pages: 294-296\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **UDA**\n- **consistency loss**\n- **augmentation**\n- **Mean Teacher awareness**\n- **unlabeled data**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Semi-Supervised Learning with Consistency Training**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Semi-Supervised Learning with Consistency Training — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Understand and prototype consistency-based semi-supervised learning such as UDA/teacher methods.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['uda', 'consistency-loss', 'augmentation'],
                },
        {
                    'title': 'Semi-Supervised Learning with Consistency Training — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Semi-Supervised Learning with Consistency Training — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Semi-Supervised Learning with Consistency Training"?', 'options': ['Understand and prototype consistency-based semi-supervised learning such as UDA/teacher methods.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
