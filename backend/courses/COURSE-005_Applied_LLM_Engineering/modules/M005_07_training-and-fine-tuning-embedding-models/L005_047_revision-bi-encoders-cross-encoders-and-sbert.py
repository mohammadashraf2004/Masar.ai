"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-047'
MODULE_ID = 'M005-07'
LESSON_META = {
    "lesson_id": 'L005-047',
    "module_id": 'M005-07',
    "title": 'Revision: Bi-Encoders, Cross-Encoders & SBERT',
    "learning_objective": 'Refresh bi-encoder and cross-encoder architectures and connect them to sentence-embedding training.',
    "curriculum_role": 'REVISION → TRAINING BRIDGE',
    "concepts": ['bi-encoder', 'cross-encoder', 'SBERT', 'Siamese network', 'pooling', 'retrieval efficiency'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 10, 'chapter_title': 'Creating Text Embedding Models', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 40,
    "prerequisites": [],
    "modernization": ['Revalidate SentenceTransformers trainer, loss, evaluator, MTEB, and dataset APIs before training.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Revision: Bi-Encoders, Cross-Encoders & SBERT',
    "slug": 'course-005-revision-bi-encoders-cross-encoders-and-sbert',
    "description": 'Refresh bi-encoder and cross-encoder architectures and connect them to sentence-embedding training.',
    "order": 1,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-llm-engineering', 'bi-encoder', 'cross-encoder', 'sbert', 'siamese-network'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Revision: Bi-Encoders, Cross-Encoders & SBERT',
        "content": '# Revision: Bi-Encoders, Cross-Encoders & SBERT\n\n## Learning objective\nRefresh bi-encoder and cross-encoder architectures and connect them to sentence-embedding training.\n\n## Curriculum role\nREVISION → TRAINING BRIDGE\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 10: Creating Text Embedding Models\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **bi-encoder**\n- **cross-encoder**\n- **SBERT**\n- **Siamese network**\n- **pooling**\n- **retrieval efficiency**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom sentence_transformers import SentenceTransformer\n# Revalidate current trainer/loss APIs before running expensive training jobs.\n```\n\n## Practice\nProduce one reproducible artifact for **Revision: Bi-Encoders, Cross-Encoders & SBERT**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate SentenceTransformers trainer, loss, evaluator, MTEB, and dataset APIs before training.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Revision: Bi-Encoders, Cross-Encoders & SBERT — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Refresh bi-encoder and cross-encoder architectures and connect them to sentence-embedding training.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['bi-encoder', 'cross-encoder', 'sbert'],
        },
        {
            'title': 'Revision: Bi-Encoders, Cross-Encoders & SBERT — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Revision: Bi-Encoders, Cross-Encoders & SBERT — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Revision: Bi-Encoders, Cross-Encoders & SBERT?', 'options': ['Refresh bi-encoder and cross-encoder architectures and connect them to sentence-embedding training.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
