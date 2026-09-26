"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-056'
MODULE_ID = 'M004-09'
LESSON_META = {
    "lesson_id": "L004-056",
    "module_id": "M004-09",
    "title": "Fine-Tune Transformers with Very Few Labels",
    "learning_objective": "Fine-tune a pretrained classifier in a low-data regime and quantify instability across training sizes and seeds.",
    "concepts": [
        "multilabel head",
        "sigmoid/BCE",
        "early stopping",
        "seed variance",
        "partial freezing",
        "overfitting"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 9,
        "chapter_title": "Dealing with Few to No Labels",
        "pages": "284-289"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-055"
    ],
    "modernization": [
        "Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Fine-Tune Transformers with Very Few Labels',
    "slug": 'course-004-fine-tune-transformers-with-very-few-labels',
    "description": 'Fine-tune a pretrained classifier in a low-data regime and quantify instability across training sizes and seeds.',
    "order": 5,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'multilabel-head', 'sigmoid-bce', 'early-stopping', 'seed-variance'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Fine-Tune Transformers with Very Few Labels',
        "content": '# Fine-Tune Transformers with Very Few Labels\n\n## Learning objective\nFine-tune a pretrained classifier in a low-data regime and quantify instability across training sizes and seeds.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 9\n- Pages: 284-289\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **multilabel head**\n- **sigmoid/BCE**\n- **early stopping**\n- **seed variance**\n- **partial freezing**\n- **overfitting**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Fine-Tune Transformers with Very Few Labels**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Fine-Tune Transformers with Very Few Labels — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Fine-tune a pretrained classifier in a low-data regime and quantify instability across training sizes and seeds.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['multilabel-head', 'sigmoid-bce', 'early-stopping'],
                },
        {
                    'title': 'Fine-Tune Transformers with Very Few Labels — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Fine-Tune Transformers with Very Few Labels — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Fine-Tune Transformers with Very Few Labels"?', 'options': ['Fine-tune a pretrained classifier in a low-data regime and quantify instability across training sizes and seeds.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
