"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-023'
MODULE_ID = 'M005-03'
LESSON_META = {
    "lesson_id": 'L005-023',
    "module_id": 'M005-03',
    "title": 'Improving Topic Representations with Embeddings & LLMs',
    "learning_objective": 'Refine topic representations with embedding reranking, MMR diversity, and LLM-generated labels while validating faithfulness.',
    "curriculum_role": 'NEW LLM PIPELINE SKILL',
    "concepts": ['KeyBERT-inspired refinement', 'MMR', 'topic labels', 'representative documents', 'LLM-assisted labeling'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 5, 'chapter_title': 'Text Clustering and Topic Modeling', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 50,
    "prerequisites": ['L005-022'],
    "modernization": ['Revalidate UMAP, HDBSCAN, BERTopic, topic-representation, and embedding-model APIs.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Improving Topic Representations with Embeddings & LLMs',
    "slug": 'course-005-improving-topic-representations-with-embeddings-and-llms',
    "description": 'Refine topic representations with embedding reranking, MMR diversity, and LLM-generated labels while validating faithfulness.',
    "order": 7,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.833,
    "skill_tags": ['applied-llm-engineering', 'keybert-inspired-refinement', 'mmr', 'topic-labels', 'representative-documents'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Improving Topic Representations with Embeddings & LLMs',
        "content": '# Improving Topic Representations with Embeddings & LLMs\n\n## Learning objective\nRefine topic representations with embedding reranking, MMR diversity, and LLM-generated labels while validating faithfulness.\n\n## Curriculum role\nNEW LLM PIPELINE SKILL\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 5: Text Clustering and Topic Modeling\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **KeyBERT-inspired refinement**\n- **MMR**\n- **topic labels**\n- **representative documents**\n- **LLM-assisted labeling**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom sentence_transformers import SentenceTransformer\n# Pair embeddings with current UMAP/HDBSCAN/BERTopic APIs during implementation.\n```\n\n## Practice\nProduce one reproducible artifact for **Improving Topic Representations with Embeddings & LLMs**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate UMAP, HDBSCAN, BERTopic, topic-representation, and embedding-model APIs.\n',
        "estimated_minutes": 50,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Improving Topic Representations with Embeddings & LLMs — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Refine topic representations with embedding reranking, MMR diversity, and LLM-generated labels while validating faithfulness.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['keybert-inspired-refinement', 'mmr', 'topic-labels'],
        },
        {
            'title': 'Improving Topic Representations with Embeddings & LLMs — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Improving Topic Representations with Embeddings & LLMs — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Improving Topic Representations with Embeddings & LLMs?', 'options': ['Refine topic representations with embedding reranking, MMR diversity, and LLM-generated labels while validating faithfulness.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": {
            'title': 'Unstructured Corpus Discovery Pipeline',
            'description': 'Discover, validate, represent, and label latent topics in an unlabeled corpus with human-inspected failure cases.',
            'difficulty': DifficultyLevel.intermediate,
            'tech_stack': ['Python', 'Sentence Transformers', 'UMAP', 'HDBSCAN', 'BERTopic'],
            'objectives': ['Build a reproducible workflow', 'Compare against a baseline', 'Debug concrete failures', 'Evaluate with task-appropriate evidence', 'Document limitations'],
            'rubric': {'correctness': 30, 'evaluation': 25, 'debugging': 20, 'reproducibility': 15, 'documentation': 10},
            'starter_repo_url': None,
            'estimated_hours': 4.0,
        },
}
