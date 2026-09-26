"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-071'
MODULE_ID = 'M004-11'
LESSON_META = {
    "lesson_id": "L004-071",
    "module_id": "M004-11",
    "title": "Beyond Text: Multimodal Transformer Systems",
    "learning_objective": "Understand how Transformers extend to vision, audio, tables, documents, and multimodal systems without turning this NLP course into a multimodal implementation course.",
    "concepts": [
        "ViT",
        "TAPAS",
        "wav2vec 2.0",
        "LayoutLM",
        "CLIP",
        "vision-language models",
        "multimodal processors"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 11,
        "chapter_title": "Future Directions",
        "pages": "354-369"
    },
    "estimated_minutes": 50,
    "prerequisites": [
        "L004-070"
    ],
    "modernization": [
        "Treat 2021 frontier examples as foundations; connect to compute-optimal scaling, efficient exact attention kernels, and modern multimodal systems."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Beyond Text: Multimodal Transformer Systems',
    "slug": 'course-004-beyond-text-multimodal-transformer-systems',
    "description": 'Understand how Transformers extend to vision, audio, tables, documents, and multimodal systems without turning this NLP course into a multimodal implementation course.',
    "order": 3,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.833,
    "skill_tags": ['applied-nlp', 'transformers', 'vit', 'tapas', 'wav2vec-2-0', 'layoutlm'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Beyond Text: Multimodal Transformer Systems',
        "content": '# Beyond Text: Multimodal Transformer Systems\n\n## Learning objective\nUnderstand how Transformers extend to vision, audio, tables, documents, and multimodal systems without turning this NLP course into a multimodal implementation course.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 11\n- Pages: 354-369\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **ViT**\n- **TAPAS**\n- **wav2vec 2.0**\n- **LayoutLM**\n- **CLIP**\n- **vision-language models**\n- **multimodal processors**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Beyond Text: Multimodal Transformer Systems**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Treat 2021 frontier examples as foundations; connect to compute-optimal scaling, efficient exact attention kernels, and modern multimodal systems.\n',
        "estimated_minutes": 50,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Beyond Text: Multimodal Transformer Systems — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Understand how Transformers extend to vision, audio, tables, documents, and multimodal systems without turning this NLP course into a multimodal implementation course.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['vit', 'tapas', 'wav2vec-2-0'],
                },
        {
                    'title': 'Beyond Text: Multimodal Transformer Systems — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Beyond Text: Multimodal Transformer Systems — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Beyond Text: Multimodal Transformer Systems"?', 'options': ['Understand how Transformers extend to vision, audio, tables, documents, and multimodal systems without turning this NLP course into a multimodal implementation course.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
