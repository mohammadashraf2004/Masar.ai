"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-013'
MODULE_ID = 'M004-03'
LESSON_META = {
    "lesson_id": "L004-013",
    "module_id": "M004-03",
    "title": "Inspect Self-Attention with PyTorch",
    "learning_objective": "Inspect the tensor operations and shapes involved in scaled dot-product and multi-head attention.",
    "concepts": [
        "queries/keys/values",
        "attention scores",
        "masking",
        "softmax",
        "multi-head attention",
        "tensor shapes"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 3,
        "chapter_title": "Transformer Anatomy",
        "pages": "61-70"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-012"
    ],
    "modernization": [
        "Treat deep architecture theory as revision; use current PyTorch attention APIs for implementation inspection."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Inspect Self-Attention with PyTorch',
    "slug": 'course-004-inspect-self-attention-with-pytorch',
    "description": 'Inspect the tensor operations and shapes involved in scaled dot-product and multi-head attention.',
    "order": 2,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'queries-keys-values', 'attention-scores', 'masking', 'softmax'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Inspect Self-Attention with PyTorch',
        "content": '# Inspect Self-Attention with PyTorch\n\n## Learning objective\nInspect the tensor operations and shapes involved in scaled dot-product and multi-head attention.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 3\n- Pages: 61-70\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **queries/keys/values**\n- **attention scores**\n- **masking**\n- **softmax**\n- **multi-head attention**\n- **tensor shapes**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Inspect Self-Attention with PyTorch**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Treat deep architecture theory as revision; use current PyTorch attention APIs for implementation inspection.\n\n## Prerequisite-depth note\nThis is a concise COURSE-004 revision/application lesson. For full attention mathematics, derivations, and deep architecture theory, return to COURSE-002 — Deep Learning Foundations.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Inspect Self-Attention with PyTorch — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Inspect the tensor operations and shapes involved in scaled dot-product and multi-head attention.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['queries-keys-values', 'attention-scores', 'masking'],
                },
        {
                    'title': 'Inspect Self-Attention with PyTorch — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Inspect Self-Attention with PyTorch — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Inspect Self-Attention with PyTorch"?', 'options': ['Inspect the tensor operations and shapes involved in scaled dot-product and multi-head attention.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
