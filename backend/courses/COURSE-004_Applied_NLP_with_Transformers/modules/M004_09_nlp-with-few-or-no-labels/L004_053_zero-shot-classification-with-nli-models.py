"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-053'
MODULE_ID = 'M004-09'
LESSON_META = {
    "lesson_id": "L004-053",
    "module_id": "M004-09",
    "title": "Zero-Shot Classification with NLI Models",
    "learning_objective": "Use NLI-based zero-shot classification and tune label names, templates, and thresholds.",
    "concepts": [
        "MNLI/NLI",
        "candidate labels",
        "hypothesis template",
        "multi_label",
        "thresholding",
        "calibration"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 9,
        "chapter_title": "Dealing with Few to No Labels",
        "pages": "263-271"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-052"
    ],
    "modernization": [
        "Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Zero-Shot Classification with NLI Models',
    "slug": 'course-004-zero-shot-classification-with-nli-models',
    "description": 'Use NLI-based zero-shot classification and tune label names, templates, and thresholds.',
    "order": 2,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'mnli-nli', 'candidate-labels', 'hypothesis-template', 'multi-label'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Zero-Shot Classification with NLI Models',
        "content": '# Zero-Shot Classification with NLI Models\n\n## Learning objective\nUse NLI-based zero-shot classification and tune label names, templates, and thresholds.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 9\n- Pages: 263-271\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **MNLI/NLI**\n- **candidate labels**\n- **hypothesis template**\n- **multi_label**\n- **thresholding**\n- **calibration**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForSequenceClassification\ncheckpoint = "distilbert-base-uncased"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForSequenceClassification.from_pretrained(checkpoint)\n```\n\n## Practice\nProduce one reproducible artifact for **Zero-Shot Classification with NLI Models**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Zero-Shot Classification with NLI Models — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Use NLI-based zero-shot classification and tune label names, templates, and thresholds.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['mnli-nli', 'candidate-labels', 'hypothesis-template'],
                },
        {
                    'title': 'Zero-Shot Classification with NLI Models — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Zero-Shot Classification with NLI Models — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Zero-Shot Classification with NLI Models"?', 'options': ['Use NLI-based zero-shot classification and tune label names, templates, and thresholds.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
