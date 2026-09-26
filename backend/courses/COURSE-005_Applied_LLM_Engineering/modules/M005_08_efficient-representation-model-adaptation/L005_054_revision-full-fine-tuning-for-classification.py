"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-054'
MODULE_ID = 'M005-08'
LESSON_META = {
    "lesson_id": 'L005-054',
    "module_id": 'M005-08',
    "title": 'Revision: Full Fine-Tuning for Classification',
    "learning_objective": 'Refresh full-model supervised classification fine-tuning as the baseline for comparing more efficient adaptation strategies.',
    "curriculum_role": 'REVISION → BASELINE',
    "concepts": ['BERT classification', 'full fine-tuning', 'classification head', 'Trainer', 'F1'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 11, 'chapter_title': 'Fine-Tuning Representation Models for Classification', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 30,
    "prerequisites": [],
    "modernization": ['Revalidate Transformers, SetFit, evaluate, data-collator, and Trainer APIs before implementation.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Revision: Full Fine-Tuning for Classification',
    "slug": 'course-005-revision-full-fine-tuning-for-classification',
    "description": 'Refresh full-model supervised classification fine-tuning as the baseline for comparing more efficient adaptation strategies.',
    "order": 1,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.5,
    "skill_tags": ['applied-llm-engineering', 'bert-classification', 'full-fine-tuning', 'classification-head', 'trainer'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Revision: Full Fine-Tuning for Classification',
        "content": '# Revision: Full Fine-Tuning for Classification\n\n## Learning objective\nRefresh full-model supervised classification fine-tuning as the baseline for comparing more efficient adaptation strategies.\n\n## Curriculum role\nREVISION → BASELINE\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 11: Fine-Tuning Representation Models for Classification\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **BERT classification**\n- **full fine-tuning**\n- **classification head**\n- **Trainer**\n- **F1**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom transformers import AutoModelForSequenceClassification, AutoTokenizer\n# Compare adaptation strategies on the same held-out evaluation data.\n```\n\n## Practice\nProduce one reproducible artifact for **Revision: Full Fine-Tuning for Classification**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate Transformers, SetFit, evaluate, data-collator, and Trainer APIs before implementation.\n',
        "estimated_minutes": 30,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Revision: Full Fine-Tuning for Classification — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Refresh full-model supervised classification fine-tuning as the baseline for comparing more efficient adaptation strategies.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['bert-classification', 'full-fine-tuning', 'classification-head'],
        },
        {
            'title': 'Revision: Full Fine-Tuning for Classification — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Revision: Full Fine-Tuning for Classification — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Revision: Full Fine-Tuning for Classification?', 'options': ['Refresh full-model supervised classification fine-tuning as the baseline for comparing more efficient adaptation strategies.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
