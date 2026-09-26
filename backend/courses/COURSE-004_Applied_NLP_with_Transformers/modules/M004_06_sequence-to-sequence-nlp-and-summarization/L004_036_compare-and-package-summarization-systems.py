"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-036'
MODULE_ID = 'M004-06'
LESSON_META = {
    "lesson_id": "L004-036",
    "module_id": "M004-06",
    "title": "Compare and Package Summarization Systems",
    "learning_objective": "Compare baselines and fine-tuned systems, select a model, and package reproducible inference.",
    "concepts": [
        "baseline comparison",
        "metric table",
        "generation config",
        "model packaging",
        "model card",
        "acceptance criteria"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 6,
        "chapter_title": "Summarization",
        "pages": "141-163"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-035"
    ],
    "modernization": [
        "Use text_target/DataCollatorForSeq2Seq/Seq2SeqTrainer-style modern workflows and current evaluation tooling."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Compare and Package Summarization Systems',
    "slug": 'course-004-compare-and-package-summarization-systems',
    "description": 'Compare baselines and fine-tuned systems, select a model, and package reproducible inference.',
    "order": 7,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'baseline-comparison', 'metric-table', 'generation-config', 'model-packaging'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Compare and Package Summarization Systems',
        "content": '# Compare and Package Summarization Systems\n\n## Learning objective\nCompare baselines and fine-tuned systems, select a model, and package reproducible inference.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 6\n- Pages: 141-163\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **baseline comparison**\n- **metric table**\n- **generation config**\n- **model packaging**\n- **model card**\n- **acceptance criteria**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForSeq2SeqLM\ncheckpoint = "google-t5/t5-small"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)\n```\n\n## Practice\nProduce one reproducible artifact for **Compare and Package Summarization Systems**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use text_target/DataCollatorForSeq2Seq/Seq2SeqTrainer-style modern workflows and current evaluation tooling.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Compare and Package Summarization Systems — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Compare baselines and fine-tuned systems, select a model, and package reproducible inference.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['baseline-comparison', 'metric-table', 'generation-config'],
                },
        {
                    'title': 'Compare and Package Summarization Systems — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Compare and Package Summarization Systems — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Compare and Package Summarization Systems"?', 'options': ['Compare baselines and fine-tuned systems, select a model, and package reproducible inference.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": {
            'title': 'Summarization Engineering Lab',
            'description': 'Build baselines, fine-tune a summarizer, evaluate with ROUGE plus human checks, and diagnose domain shift.',
            'difficulty': DifficultyLevel.intermediate,
            'tech_stack': ['Python', 'PyTorch', 'Hugging Face Transformers'],
            'objectives': ['Build a reproducible workflow', 'Compare against a baseline', 'Debug concrete failures', 'Evaluate with task-appropriate metrics', 'Document limitations'],
            'rubric': {'correctness': 30, 'evaluation': 25, 'debugging': 20, 'reproducibility': 15, 'documentation': 10},
            'starter_repo_url': None,
            'estimated_hours': 3.0,
        },
}
