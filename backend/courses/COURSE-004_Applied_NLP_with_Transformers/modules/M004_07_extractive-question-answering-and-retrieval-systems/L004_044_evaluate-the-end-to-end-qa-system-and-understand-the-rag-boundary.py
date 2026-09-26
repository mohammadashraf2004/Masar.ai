"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-044'
MODULE_ID = 'M004-07'
LESSON_META = {
    "lesson_id": "L004-044",
    "module_id": "M004-07",
    "title": "Evaluate the End-to-End QA System & Understand the RAG Boundary",
    "learning_objective": "Evaluate retriever and reader jointly and distinguish extractive QA from modern generative RAG systems.",
    "concepts": [
        "pipeline evaluation",
        "retrieval bottleneck",
        "reader bottleneck",
        "generative QA",
        "RAG boundary",
        "search-first hierarchy"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 7,
        "chapter_title": "Question Answering",
        "pages": "203-207"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-043"
    ],
    "modernization": [
        "Treat the book's Haystack code as historical; preserve retriever-reader architecture and evaluation concepts, not obsolete APIs."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Evaluate the End-to-End QA System & Understand the RAG Boundary',
    "slug": 'course-004-evaluate-the-end-to-end-qa-system-and-understand-the-rag-boundary',
    "description": 'Evaluate retriever and reader jointly and distinguish extractive QA from modern generative RAG systems.',
    "order": 8,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'pipeline-evaluation', 'retrieval-bottleneck', 'reader-bottleneck', 'generative-qa'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Evaluate the End-to-End QA System & Understand the RAG Boundary',
        "content": '# Evaluate the End-to-End QA System & Understand the RAG Boundary\n\n## Learning objective\nEvaluate retriever and reader jointly and distinguish extractive QA from modern generative RAG systems.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 7\n- Pages: 203-207\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **pipeline evaluation**\n- **retrieval bottleneck**\n- **reader bottleneck**\n- **generative QA**\n- **RAG boundary**\n- **search-first hierarchy**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\nqa = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")\nresult = qa(question="What is Masar?", context="Masar is an Arabic-first AI learning platform.")\n```\n\n## Practice\nProduce one reproducible artifact for **Evaluate the End-to-End QA System & Understand the RAG Boundary**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Treat the book\'s Haystack code as historical; preserve retriever-reader architecture and evaluation concepts, not obsolete APIs.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Evaluate the End-to-End QA System & Understand the RAG Boundary — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Evaluate retriever and reader jointly and distinguish extractive QA from modern generative RAG systems.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['pipeline-evaluation', 'retrieval-bottleneck', 'reader-bottleneck'],
                },
        {
                    'title': 'Evaluate the End-to-End QA System & Understand the RAG Boundary — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Evaluate the End-to-End QA System & Understand the RAG Boundary — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Evaluate the End-to-End QA System & Understand the RAG Boundary"?', 'options': ['Evaluate retriever and reader jointly and distinguish extractive QA from modern generative RAG systems.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": {
            'title': 'Retriever-Reader QA System',
            'description': 'Build and evaluate retrieval plus extractive QA, measuring retrieval and answer extraction separately.',
            'difficulty': DifficultyLevel.intermediate,
            'tech_stack': ['Python', 'PyTorch', 'Hugging Face Transformers'],
            'objectives': ['Build a reproducible workflow', 'Compare against a baseline', 'Debug concrete failures', 'Evaluate with task-appropriate metrics', 'Document limitations'],
            'rubric': {'correctness': 30, 'evaluation': 25, 'debugging': 20, 'reproducibility': 15, 'documentation': 10},
            'starter_repo_url': None,
            'estimated_hours': 3.0,
        },
}
