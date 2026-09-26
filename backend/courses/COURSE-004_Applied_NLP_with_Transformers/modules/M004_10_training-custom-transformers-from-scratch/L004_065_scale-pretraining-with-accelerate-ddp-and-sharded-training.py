"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-065'
MODULE_ID = 'M004-10'
LESSON_META = {
    "lesson_id": "L004-065",
    "module_id": "M004-10",
    "title": "Scale Pretraining with Accelerate, DDP & Sharded Training",
    "learning_objective": "Scale training across devices using Accelerate and understand when DDP or sharded approaches are required.",
    "concepts": [
        "Accelerate",
        "mixed precision",
        "DDP",
        "gradient accumulation",
        "gradient checkpointing",
        "FSDP/DeepSpeed awareness"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 10,
        "chapter_title": "Training Transformers from Scratch",
        "pages": "330-337"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-064"
    ],
    "modernization": [
        "Keep the chapter as optional advanced practice; use current Accelerate/DDP/sharded-training and governance practices."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Scale Pretraining with Accelerate, DDP & Sharded Training',
    "slug": 'course-004-scale-pretraining-with-accelerate-ddp-and-sharded-training',
    "description": 'Scale training across devices using Accelerate and understand when DDP or sharded approaches are required.',
    "order": 6,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'accelerate', 'mixed-precision', 'ddp', 'gradient-accumulation'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Scale Pretraining with Accelerate, DDP & Sharded Training',
        "content": '# Scale Pretraining with Accelerate, DDP & Sharded Training\n\n## Learning objective\nScale training across devices using Accelerate and understand when DDP or sharded approaches are required.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 10\n- Pages: 330-337\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **Accelerate**\n- **mixed precision**\n- **DDP**\n- **gradient accumulation**\n- **gradient checkpointing**\n- **FSDP/DeepSpeed awareness**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\n# Keep the experiment small first; validate data, tokenization,\n# checkpointing, and evaluation before scaling compute.\n```\n\n## Practice\nProduce one reproducible artifact for **Scale Pretraining with Accelerate, DDP & Sharded Training**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Keep the chapter as optional advanced practice; use current Accelerate/DDP/sharded-training and governance practices.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Scale Pretraining with Accelerate, DDP & Sharded Training — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Scale training across devices using Accelerate and understand when DDP or sharded approaches are required.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['accelerate', 'mixed-precision', 'ddp'],
                },
        {
                    'title': 'Scale Pretraining with Accelerate, DDP & Sharded Training — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Scale Pretraining with Accelerate, DDP & Sharded Training — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Scale Pretraining with Accelerate, DDP & Sharded Training"?', 'options': ['Scale training across devices using Accelerate and understand when DDP or sharded approaches are required.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
