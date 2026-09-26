"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-017'
MODULE_ID = 'M004-04'
LESSON_META = {
    "lesson_id": "L004-017",
    "module_id": "M004-04",
    "title": "Audit a Multilingual Token-Classification Dataset",
    "learning_objective": "Inspect multilingual NER data, label distributions, language coverage, and split quality.",
    "concepts": [
        "PAN-X style data",
        "BIO tags",
        "language splits",
        "class balance",
        "dataset audit"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 4,
        "chapter_title": "Multilingual Named Entity Recognition",
        "pages": "87-92"
    },
    "estimated_minutes": 35,
    "prerequisites": [
        "L004-016"
    ],
    "modernization": [
        "Prefer AutoModelForTokenClassification for production code; custom model-head code is anatomy practice."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Audit a Multilingual Token-Classification Dataset',
    "slug": 'course-004-audit-a-multilingual-token-classification-dataset',
    "description": 'Inspect multilingual NER data, label distributions, language coverage, and split quality.',
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.583,
    "skill_tags": ['applied-nlp', 'transformers', 'pan-x-style-data', 'bio-tags', 'language-splits', 'class-balance'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Audit a Multilingual Token-Classification Dataset',
        "content": '# Audit a Multilingual Token-Classification Dataset\n\n## Learning objective\nInspect multilingual NER data, label distributions, language coverage, and split quality.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 4\n- Pages: 87-92\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **PAN-X style data**\n- **BIO tags**\n- **language splits**\n- **class balance**\n- **dataset audit**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForTokenClassification\ncheckpoint = "xlm-roberta-base"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForTokenClassification.from_pretrained(checkpoint)\n```\n\n## Practice\nProduce one reproducible artifact for **Audit a Multilingual Token-Classification Dataset**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Prefer AutoModelForTokenClassification for production code; custom model-head code is anatomy practice.\n',
        "estimated_minutes": 35,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Audit a Multilingual Token-Classification Dataset — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Inspect multilingual NER data, label distributions, language coverage, and split quality.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['pan-x-style-data', 'bio-tags', 'language-splits'],
                },
        {
                    'title': 'Audit a Multilingual Token-Classification Dataset — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Audit a Multilingual Token-Classification Dataset — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Audit a Multilingual Token-Classification Dataset"?', 'options': ['Inspect multilingual NER data, label distributions, language coverage, and split quality.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
