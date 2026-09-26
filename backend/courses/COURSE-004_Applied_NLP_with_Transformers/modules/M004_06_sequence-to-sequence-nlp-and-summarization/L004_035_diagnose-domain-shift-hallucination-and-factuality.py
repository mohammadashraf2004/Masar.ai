"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-035'
MODULE_ID = 'M004-06'
LESSON_META = {
    "lesson_id": "L004-035",
    "module_id": "M004-06",
    "title": "Diagnose Domain Shift, Hallucination & Factuality",
    "learning_objective": "Diagnose why a summarizer can fail when domain or discourse style changes.",
    "concepts": [
        "domain shift",
        "extractive bias",
        "hallucination",
        "factuality",
        "human review",
        "long-document limits"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 6,
        "chapter_title": "Summarization",
        "pages": "157-163"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-034"
    ],
    "modernization": [
        "Use text_target/DataCollatorForSeq2Seq/Seq2SeqTrainer-style modern workflows and current evaluation tooling."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Diagnose Domain Shift, Hallucination & Factuality',
    "slug": 'course-004-diagnose-domain-shift-hallucination-and-factuality',
    "description": 'Diagnose why a summarizer can fail when domain or discourse style changes.',
    "order": 6,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'domain-shift', 'extractive-bias', 'hallucination', 'factuality'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Diagnose Domain Shift, Hallucination & Factuality',
        "content": '# Diagnose Domain Shift, Hallucination & Factuality\n\n## Learning objective\nDiagnose why a summarizer can fail when domain or discourse style changes.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 6\n- Pages: 157-163\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **domain shift**\n- **extractive bias**\n- **hallucination**\n- **factuality**\n- **human review**\n- **long-document limits**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Diagnose Domain Shift, Hallucination & Factuality**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use text_target/DataCollatorForSeq2Seq/Seq2SeqTrainer-style modern workflows and current evaluation tooling.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Diagnose Domain Shift, Hallucination & Factuality — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Diagnose why a summarizer can fail when domain or discourse style changes.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['domain-shift', 'extractive-bias', 'hallucination'],
                },
        {
                    'title': 'Diagnose Domain Shift, Hallucination & Factuality — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Diagnose Domain Shift, Hallucination & Factuality — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Diagnose Domain Shift, Hallucination & Factuality"?', 'options': ['Diagnose why a summarizer can fail when domain or discourse style changes.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
