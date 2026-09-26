"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-011'
MODULE_ID = 'M004-02'
LESSON_META = {
    "lesson_id": "L004-011",
    "module_id": "M004-02",
    "title": "Package and Reuse the Fine-Tuned Classifier",
    "learning_objective": "Save, reload, document, and run inference with a fine-tuned classifier.",
    "concepts": [
        "save_pretrained",
        "model/tokenizer pairing",
        "pipeline reload",
        "model documentation",
        "training/inference separation"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 2,
        "chapter_title": "Text Classification",
        "pages": "53-54"
    },
    "estimated_minutes": 20,
    "prerequisites": [
        "L004-010"
    ],
    "modernization": [
        "Use dynamic padding where appropriate, current Trainer APIs, and modern evaluation tooling."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Package and Reuse the Fine-Tuned Classifier',
    "slug": 'course-004-package-and-reuse-the-fine-tuned-classifier',
    "description": 'Save, reload, document, and run inference with a fine-tuned classifier.',
    "order": 7,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.333,
    "skill_tags": ['applied-nlp', 'transformers', 'save-pretrained', 'model-tokenizer-pairing', 'pipeline-reload', 'model-documentation'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Package and Reuse the Fine-Tuned Classifier',
        "content": '# Package and Reuse the Fine-Tuned Classifier\n\n## Learning objective\nSave, reload, document, and run inference with a fine-tuned classifier.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 2\n- Pages: 53-54\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **save_pretrained**\n- **model/tokenizer pairing**\n- **pipeline reload**\n- **model documentation**\n- **training/inference separation**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Package and Reuse the Fine-Tuned Classifier**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use dynamic padding where appropriate, current Trainer APIs, and modern evaluation tooling.\n',
        "estimated_minutes": 20,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Package and Reuse the Fine-Tuned Classifier — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Save, reload, document, and run inference with a fine-tuned classifier.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['save-pretrained', 'model-tokenizer-pairing', 'pipeline-reload'],
                },
        {
                    'title': 'Package and Reuse the Fine-Tuned Classifier — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Package and Reuse the Fine-Tuned Classifier — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Package and Reuse the Fine-Tuned Classifier"?', 'options': ['Save, reload, document, and run inference with a fine-tuned classifier.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": {
            'title': 'Transformer Text Classification Engineering Lab',
            'description': 'Audit data, build baselines, fine-tune, evaluate, diagnose errors, and reload a text classifier.',
            'difficulty': DifficultyLevel.intermediate,
            'tech_stack': ['Python', 'PyTorch', 'Hugging Face Transformers'],
            'objectives': ['Build a reproducible workflow', 'Compare against a baseline', 'Debug concrete failures', 'Evaluate with task-appropriate metrics', 'Document limitations'],
            'rubric': {'correctness': 30, 'evaluation': 25, 'debugging': 20, 'reproducibility': 15, 'documentation': 10},
            'starter_repo_url': None,
            'estimated_hours': 3.0,
        },
}
