"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-062'
MODULE_ID = 'M004-10'
LESSON_META = {
    "lesson_id": "L004-062",
    "module_id": "M004-10",
    "title": "Train & Evaluate a Domain Tokenizer",
    "learning_objective": "Train a domain-specific tokenizer and evaluate efficiency, coverage, and downstream suitability.",
    "concepts": [
        "BPE",
        "byte-level BPE",
        "train_new_from_iterator",
        "vocabulary size",
        "fertility",
        "coverage",
        "domain tokens"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 10,
        "chapter_title": "Training Transformers from Scratch",
        "pages": "310-322"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-061"
    ],
    "modernization": [
        "Keep the chapter as optional advanced practice; use current Accelerate/DDP/sharded-training and governance practices."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Train & Evaluate a Domain Tokenizer',
    "slug": 'course-004-train-and-evaluate-a-domain-tokenizer',
    "description": 'Train a domain-specific tokenizer and evaluate efficiency, coverage, and downstream suitability.',
    "order": 3,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'bpe', 'byte-level-bpe', 'train-new-from-iterator', 'vocabulary-size'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Train & Evaluate a Domain Tokenizer',
        "content": '# Train & Evaluate a Domain Tokenizer\n\n## Learning objective\nTrain a domain-specific tokenizer and evaluate efficiency, coverage, and downstream suitability.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 10\n- Pages: 310-322\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **BPE**\n- **byte-level BPE**\n- **train_new_from_iterator**\n- **vocabulary size**\n- **fertility**\n- **coverage**\n- **domain tokens**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForTokenClassification\ncheckpoint = "xlm-roberta-base"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForTokenClassification.from_pretrained(checkpoint)\n```\n\n## Practice\nProduce one reproducible artifact for **Train & Evaluate a Domain Tokenizer**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Keep the chapter as optional advanced practice; use current Accelerate/DDP/sharded-training and governance practices.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Train & Evaluate a Domain Tokenizer — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Train a domain-specific tokenizer and evaluate efficiency, coverage, and downstream suitability.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['bpe', 'byte-level-bpe', 'train-new-from-iterator'],
                },
        {
                    'title': 'Train & Evaluate a Domain Tokenizer — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Train & Evaluate a Domain Tokenizer — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Train & Evaluate a Domain Tokenizer"?', 'options': ['Train a domain-specific tokenizer and evaluate efficiency, coverage, and downstream suitability.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
