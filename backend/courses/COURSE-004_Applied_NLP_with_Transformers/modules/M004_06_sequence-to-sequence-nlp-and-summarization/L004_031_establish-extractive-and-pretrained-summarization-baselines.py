"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-031'
MODULE_ID = 'M004-06'
LESSON_META = {
    "lesson_id": "L004-031",
    "module_id": "M004-06",
    "title": "Establish Extractive and Pretrained Summarization Baselines",
    "learning_objective": "Build simple and pretrained baselines before fine-tuning a summarizer.",
    "concepts": [
        "lead-3 baseline",
        "summarization pipeline",
        "T5",
        "BART",
        "PEGASUS",
        "qualitative comparison"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 6,
        "chapter_title": "Summarization",
        "pages": "143-147"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-030"
    ],
    "modernization": [
        "Use text_target/DataCollatorForSeq2Seq/Seq2SeqTrainer-style modern workflows and current evaluation tooling."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Establish Extractive and Pretrained Summarization Baselines',
    "slug": 'course-004-establish-extractive-and-pretrained-summarization-baselines',
    "description": 'Build simple and pretrained baselines before fine-tuning a summarizer.',
    "order": 2,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'lead-3-baseline', 'summarization-pipeline', 't5', 'bart'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Establish Extractive and Pretrained Summarization Baselines',
        "content": '# Establish Extractive and Pretrained Summarization Baselines\n\n## Learning objective\nBuild simple and pretrained baselines before fine-tuning a summarizer.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 6\n- Pages: 143-147\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **lead-3 baseline**\n- **summarization pipeline**\n- **T5**\n- **BART**\n- **PEGASUS**\n- **qualitative comparison**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForSeq2SeqLM\ncheckpoint = "google-t5/t5-small"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)\n```\n\n## Practice\nProduce one reproducible artifact for **Establish Extractive and Pretrained Summarization Baselines**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use text_target/DataCollatorForSeq2Seq/Seq2SeqTrainer-style modern workflows and current evaluation tooling.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Establish Extractive and Pretrained Summarization Baselines — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Build simple and pretrained baselines before fine-tuning a summarizer.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['lead-3-baseline', 'summarization-pipeline', 't5'],
                },
        {
                    'title': 'Establish Extractive and Pretrained Summarization Baselines — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Establish Extractive and Pretrained Summarization Baselines — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Establish Extractive and Pretrained Summarization Baselines"?', 'options': ['Build simple and pretrained baselines before fine-tuning a summarizer.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
