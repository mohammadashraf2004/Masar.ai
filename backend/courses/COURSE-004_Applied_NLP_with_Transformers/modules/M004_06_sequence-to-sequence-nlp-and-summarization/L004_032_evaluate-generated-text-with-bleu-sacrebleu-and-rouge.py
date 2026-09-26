"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-032'
MODULE_ID = 'M004-06'
LESSON_META = {
    "lesson_id": "L004-032",
    "module_id": "M004-06",
    "title": "Evaluate Generated Text with BLEU, SacreBLEU & ROUGE",
    "learning_objective": "Explain and compute reference-based generation metrics while recognizing their limitations.",
    "concepts": [
        "BLEU",
        "brevity penalty",
        "SacreBLEU",
        "ROUGE-1/2/L/Lsum",
        "human evaluation"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 6,
        "chapter_title": "Summarization",
        "pages": "148-154"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-031"
    ],
    "modernization": [
        "Use text_target/DataCollatorForSeq2Seq/Seq2SeqTrainer-style modern workflows and current evaluation tooling."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Evaluate Generated Text with BLEU, SacreBLEU & ROUGE',
    "slug": 'course-004-evaluate-generated-text-with-bleu-sacrebleu-and-rouge',
    "description": 'Explain and compute reference-based generation metrics while recognizing their limitations.',
    "order": 3,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'bleu', 'brevity-penalty', 'sacrebleu', 'rouge-1-2-l-lsum'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Evaluate Generated Text with BLEU, SacreBLEU & ROUGE',
        "content": '# Evaluate Generated Text with BLEU, SacreBLEU & ROUGE\n\n## Learning objective\nExplain and compute reference-based generation metrics while recognizing their limitations.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 6\n- Pages: 148-154\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **BLEU**\n- **brevity penalty**\n- **SacreBLEU**\n- **ROUGE-1/2/L/Lsum**\n- **human evaluation**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForTokenClassification\ncheckpoint = "xlm-roberta-base"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForTokenClassification.from_pretrained(checkpoint)\n```\n\n## Practice\nProduce one reproducible artifact for **Evaluate Generated Text with BLEU, SacreBLEU & ROUGE**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use text_target/DataCollatorForSeq2Seq/Seq2SeqTrainer-style modern workflows and current evaluation tooling.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Evaluate Generated Text with BLEU, SacreBLEU & ROUGE — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Explain and compute reference-based generation metrics while recognizing their limitations.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['bleu', 'brevity-penalty', 'sacrebleu'],
                },
        {
                    'title': 'Evaluate Generated Text with BLEU, SacreBLEU & ROUGE — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Evaluate Generated Text with BLEU, SacreBLEU & ROUGE — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Evaluate Generated Text with BLEU, SacreBLEU & ROUGE"?', 'options': ['Explain and compute reference-based generation metrics while recognizing their limitations.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
