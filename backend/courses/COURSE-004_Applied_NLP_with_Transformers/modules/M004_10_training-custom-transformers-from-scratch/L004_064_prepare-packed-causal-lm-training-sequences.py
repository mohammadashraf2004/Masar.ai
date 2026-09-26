"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-064'
MODULE_ID = 'M004-10'
LESSON_META = {
    "lesson_id": "L004-064",
    "module_id": "M004-10",
    "title": "Prepare Packed Causal-LM Training Sequences",
    "learning_objective": "Create efficient fixed-length training sequences by packing many examples with document boundaries.",
    "concepts": [
        "EOS separator",
        "sequence packing",
        "constant length",
        "IterableDataset",
        "shuffle buffer",
        "loss labels"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 10,
        "chapter_title": "Training Transformers from Scratch",
        "pages": "326-330"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-063"
    ],
    "modernization": [
        "Keep the chapter as optional advanced practice; use current Accelerate/DDP/sharded-training and governance practices."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Prepare Packed Causal-LM Training Sequences',
    "slug": 'course-004-prepare-packed-causal-lm-training-sequences',
    "description": 'Create efficient fixed-length training sequences by packing many examples with document boundaries.',
    "order": 5,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'eos-separator', 'sequence-packing', 'constant-length', 'iterabledataset'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Prepare Packed Causal-LM Training Sequences',
        "content": '# Prepare Packed Causal-LM Training Sequences\n\n## Learning objective\nCreate efficient fixed-length training sequences by packing many examples with document boundaries.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 10\n- Pages: 326-330\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **EOS separator**\n- **sequence packing**\n- **constant length**\n- **IterableDataset**\n- **shuffle buffer**\n- **loss labels**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Prepare Packed Causal-LM Training Sequences**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Keep the chapter as optional advanced practice; use current Accelerate/DDP/sharded-training and governance practices.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Prepare Packed Causal-LM Training Sequences — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Create efficient fixed-length training sequences by packing many examples with document boundaries.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['eos-separator', 'sequence-packing', 'constant-length'],
                },
        {
                    'title': 'Prepare Packed Causal-LM Training Sequences — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Prepare Packed Causal-LM Training Sequences — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Prepare Packed Causal-LM Training Sequences"?', 'options': ['Create efficient fixed-length training sequences by packing many examples with document boundaries.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
