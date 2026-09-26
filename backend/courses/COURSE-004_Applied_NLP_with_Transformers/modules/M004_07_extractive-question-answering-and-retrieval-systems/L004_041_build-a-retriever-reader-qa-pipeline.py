"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-041'
MODULE_ID = 'M004-07'
LESSON_META = {
    "lesson_id": "L004-041",
    "module_id": "M004-07",
    "title": "Build a Retriever-Reader QA Pipeline",
    "learning_objective": "Combine retrieval with extractive reading to answer questions over a document collection.",
    "concepts": [
        "retriever-reader",
        "BM25",
        "dense retrieval",
        "document store",
        "reader",
        "reranking awareness"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 7,
        "chapter_title": "Question Answering",
        "pages": "181-189"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-040"
    ],
    "modernization": [
        "Treat the book's Haystack code as historical; preserve retriever-reader architecture and evaluation concepts, not obsolete APIs."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Build a Retriever-Reader QA Pipeline',
    "slug": 'course-004-build-a-retriever-reader-qa-pipeline',
    "description": 'Combine retrieval with extractive reading to answer questions over a document collection.',
    "order": 5,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'retriever-reader', 'bm25', 'dense-retrieval', 'document-store'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Build a Retriever-Reader QA Pipeline',
        "content": '# Build a Retriever-Reader QA Pipeline\n\n## Learning objective\nCombine retrieval with extractive reading to answer questions over a document collection.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 7\n- Pages: 181-189\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **retriever-reader**\n- **BM25**\n- **dense retrieval**\n- **document store**\n- **reader**\n- **reranking awareness**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\nqa = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")\nresult = qa(question="What is Masar?", context="Masar is an Arabic-first AI learning platform.")\n```\n\n## Practice\nProduce one reproducible artifact for **Build a Retriever-Reader QA Pipeline**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Treat the book\'s Haystack code as historical; preserve retriever-reader architecture and evaluation concepts, not obsolete APIs.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Build a Retriever-Reader QA Pipeline — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Combine retrieval with extractive reading to answer questions over a document collection.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['retriever-reader', 'bm25', 'dense-retrieval'],
                },
        {
                    'title': 'Build a Retriever-Reader QA Pipeline — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Build a Retriever-Reader QA Pipeline — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Build a Retriever-Reader QA Pipeline"?', 'options': ['Combine retrieval with extractive reading to answer questions over a document collection.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
