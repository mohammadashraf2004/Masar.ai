"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-037'
MODULE_ID = 'M004-07'
LESSON_META = {
    "lesson_id": "L004-037",
    "module_id": "M004-07",
    "title": "Frame Extractive QA and Audit QA Data",
    "learning_objective": "Frame extractive QA, inspect answer spans and unanswerable examples, and understand domain constraints.",
    "concepts": [
        "extractive QA",
        "question/context/answer",
        "answer_start",
        "unanswerable questions",
        "closed/open domain"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 7,
        "chapter_title": "Question Answering",
        "pages": "165-173"
    },
    "estimated_minutes": 35,
    "prerequisites": [
        "L004-036"
    ],
    "modernization": [
        "Treat the book's Haystack code as historical; preserve retriever-reader architecture and evaluation concepts, not obsolete APIs."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Frame Extractive QA and Audit QA Data',
    "slug": 'course-004-frame-extractive-qa-and-audit-qa-data',
    "description": 'Frame extractive QA, inspect answer spans and unanswerable examples, and understand domain constraints.',
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.583,
    "skill_tags": ['applied-nlp', 'transformers', 'extractive-qa', 'question-context-answer', 'answer-start', 'unanswerable-questions'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Frame Extractive QA and Audit QA Data',
        "content": '# Frame Extractive QA and Audit QA Data\n\n## Learning objective\nFrame extractive QA, inspect answer spans and unanswerable examples, and understand domain constraints.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 7\n- Pages: 165-173\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **extractive QA**\n- **question/context/answer**\n- **answer_start**\n- **unanswerable questions**\n- **closed/open domain**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\nqa = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")\nresult = qa(question="What is Masar?", context="Masar is an Arabic-first AI learning platform.")\n```\n\n## Practice\nProduce one reproducible artifact for **Frame Extractive QA and Audit QA Data**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Treat the book\'s Haystack code as historical; preserve retriever-reader architecture and evaluation concepts, not obsolete APIs.\n',
        "estimated_minutes": 35,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Frame Extractive QA and Audit QA Data — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Frame extractive QA, inspect answer spans and unanswerable examples, and understand domain constraints.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['extractive-qa', 'question-context-answer', 'answer-start'],
                },
        {
                    'title': 'Frame Extractive QA and Audit QA Data — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Frame Extractive QA and Audit QA Data — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Frame Extractive QA and Audit QA Data"?', 'options': ['Frame extractive QA, inspect answer spans and unanswerable examples, and understand domain constraints.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
