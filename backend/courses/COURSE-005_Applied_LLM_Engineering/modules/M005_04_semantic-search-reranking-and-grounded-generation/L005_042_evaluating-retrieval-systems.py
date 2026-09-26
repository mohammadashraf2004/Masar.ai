"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-042'
MODULE_ID = 'M005-04'
LESSON_META = {
    "lesson_id": 'L005-042',
    "module_id": 'M005-04',
    "title": 'Evaluating Retrieval Systems',
    "learning_objective": 'Evaluate retrieval systems with query/relevance judgments and ranking metrics instead of anecdotal examples.',
    "curriculum_role": 'NEW CORE',
    "concepts": ['relevance judgments', 'average precision', 'MAP', 'nDCG', 'Recall@k', 'MRR'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 8, 'chapter_title': 'Semantic Search and Retrieval-Augmented Generation', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 50,
    "prerequisites": ['L005-041'],
    "modernization": ['Revalidate embedding/reranker checkpoints, ANN/vector-index APIs, provider APIs, and RAG evaluation tooling.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Evaluating Retrieval Systems',
    "slug": 'course-005-evaluating-retrieval-systems',
    "description": 'Evaluate retrieval systems with query/relevance judgments and ranking metrics instead of anecdotal examples.',
    "order": 5,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.833,
    "skill_tags": ['applied-llm-engineering', 'relevance-judgments', 'average-precision', 'map', 'ndcg'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Evaluating Retrieval Systems',
        "content": '# Evaluating Retrieval Systems\n\n## Learning objective\nEvaluate retrieval systems with query/relevance judgments and ranking metrics instead of anecdotal examples.\n\n## Curriculum role\nNEW CORE\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 8: Semantic Search and Retrieval-Augmented Generation\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **relevance judgments**\n- **average precision**\n- **MAP**\n- **nDCG**\n- **Recall@k**\n- **MRR**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom sentence_transformers import SentenceTransformer, CrossEncoder\n# Build retrieval in explicit stages: chunk → embed → retrieve → rerank → evaluate.\n```\n\n## Practice\nProduce one reproducible artifact for **Evaluating Retrieval Systems**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate embedding/reranker checkpoints, ANN/vector-index APIs, provider APIs, and RAG evaluation tooling.\n',
        "estimated_minutes": 50,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Evaluating Retrieval Systems — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Evaluate retrieval systems with query/relevance judgments and ranking metrics instead of anecdotal examples.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['relevance-judgments', 'average-precision', 'map'],
        },
        {
            'title': 'Evaluating Retrieval Systems — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Evaluating Retrieval Systems — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Evaluating Retrieval Systems?', 'options': ['Evaluate retrieval systems with query/relevance judgments and ranking metrics instead of anecdotal examples.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
