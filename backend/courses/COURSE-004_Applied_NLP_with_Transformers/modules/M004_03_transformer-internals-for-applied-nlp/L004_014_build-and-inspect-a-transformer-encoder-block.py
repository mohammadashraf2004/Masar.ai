"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-014'
MODULE_ID = 'M004-03'
LESSON_META = {
    "lesson_id": "L004-014",
    "module_id": "M004-03",
    "title": "Build and Inspect a Transformer Encoder Block",
    "learning_objective": "Connect attention, feed-forward networks, residual connections, and normalization in an encoder block.",
    "concepts": [
        "feed-forward network",
        "residual connections",
        "layer normalization",
        "dropout",
        "encoder block inspection"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 3,
        "chapter_title": "Transformer Anatomy",
        "pages": "70-73"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-013"
    ],
    "modernization": [
        "Treat deep architecture theory as revision; use current PyTorch attention APIs for implementation inspection."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Build and Inspect a Transformer Encoder Block',
    "slug": 'course-004-build-and-inspect-a-transformer-encoder-block',
    "description": 'Connect attention, feed-forward networks, residual connections, and normalization in an encoder block.',
    "order": 3,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'feed-forward-network', 'residual-connections', 'layer-normalization', 'dropout'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Build and Inspect a Transformer Encoder Block',
        "content": '# Build and Inspect a Transformer Encoder Block\n\n## Learning objective\nConnect attention, feed-forward networks, residual connections, and normalization in an encoder block.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 3\n- Pages: 70-73\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **feed-forward network**\n- **residual connections**\n- **layer normalization**\n- **dropout**\n- **encoder block inspection**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Build and Inspect a Transformer Encoder Block**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Treat deep architecture theory as revision; use current PyTorch attention APIs for implementation inspection.\n\n## Prerequisite-depth note\nThis is a concise COURSE-004 revision/application lesson. For full attention mathematics, derivations, and deep architecture theory, return to COURSE-002 — Deep Learning Foundations.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Build and Inspect a Transformer Encoder Block — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Connect attention, feed-forward networks, residual connections, and normalization in an encoder block.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['feed-forward-network', 'residual-connections', 'layer-normalization'],
                },
        {
                    'title': 'Build and Inspect a Transformer Encoder Block — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Build and Inspect a Transformer Encoder Block — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Build and Inspect a Transformer Encoder Block"?', 'options': ['Connect attention, feed-forward networks, residual connections, and normalization in an encoder block.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
