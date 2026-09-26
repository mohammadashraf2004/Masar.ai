"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-002'
MODULE_ID = 'M004-01'
LESSON_META = {
    "lesson_id": "L004-002",
    "module_id": "M004-01",
    "title": "Rapid NLP Prototyping with Transformers Pipelines",
    "learning_objective": "Prototype common NLP tasks quickly and inspect pipeline outputs and failure cases.",
    "concepts": [
        "pipeline API",
        "classification",
        "NER",
        "QA",
        "summarization/generation",
        "failure inspection"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 1,
        "chapter_title": "Hello Transformers",
        "pages": "10-16"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-001"
    ],
    "modernization": [
        "Use the current PyTorch-first Transformers ecosystem and current model-card/evaluation workflows."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Rapid NLP Prototyping with Transformers Pipelines',
    "slug": 'course-004-rapid-nlp-prototyping-with-transformers-pipelines',
    "description": 'Prototype common NLP tasks quickly and inspect pipeline outputs and failure cases.',
    "order": 2,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'pipeline-api', 'classification', 'ner', 'qa'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Rapid NLP Prototyping with Transformers Pipelines',
        "content": '# Rapid NLP Prototyping with Transformers Pipelines\n\n## Learning objective\nPrototype common NLP tasks quickly and inspect pipeline outputs and failure cases.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 1\n- Pages: 10-16\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **pipeline API**\n- **classification**\n- **NER**\n- **QA**\n- **summarization/generation**\n- **failure inspection**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Rapid NLP Prototyping with Transformers Pipelines**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use the current PyTorch-first Transformers ecosystem and current model-card/evaluation workflows.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Rapid NLP Prototyping with Transformers Pipelines — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Prototype common NLP tasks quickly and inspect pipeline outputs and failure cases.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['pipeline-api', 'classification', 'ner'],
                },
        {
                    'title': 'Rapid NLP Prototyping with Transformers Pipelines — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Rapid NLP Prototyping with Transformers Pipelines — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Rapid NLP Prototyping with Transformers Pipelines"?', 'options': ['Prototype common NLP tasks quickly and inspect pipeline outputs and failure cases.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
