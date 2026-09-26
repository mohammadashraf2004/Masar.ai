"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-017'
MODULE_ID = 'M005-03'
LESSON_META = {
    "lesson_id": 'L005-017',
    "module_id": 'M005-03',
    "title": 'Revision: From Embeddings to Unsupervised Text Discovery',
    "learning_objective": 'Connect embedding and clustering foundations to discovering latent structure in unlabeled text collections.',
    "curriculum_role": 'REVISION → APPLICATION BRIDGE',
    "concepts": ['unsupervised learning', 'semantic embeddings', 'clustering', 'outliers', 'dimensionality reduction'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 5, 'chapter_title': 'Text Clustering and Topic Modeling', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 30,
    "prerequisites": [],
    "modernization": ['Revalidate UMAP, HDBSCAN, BERTopic, topic-representation, and embedding-model APIs.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Revision: From Embeddings to Unsupervised Text Discovery',
    "slug": 'course-005-revision-from-embeddings-to-unsupervised-text-discovery',
    "description": 'Connect embedding and clustering foundations to discovering latent structure in unlabeled text collections.',
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.5,
    "skill_tags": ['applied-llm-engineering', 'unsupervised-learning', 'semantic-embeddings', 'clustering', 'outliers'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Revision: From Embeddings to Unsupervised Text Discovery',
        "content": '# Revision: From Embeddings to Unsupervised Text Discovery\n\n## Learning objective\nConnect embedding and clustering foundations to discovering latent structure in unlabeled text collections.\n\n## Curriculum role\nREVISION → APPLICATION BRIDGE\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 5: Text Clustering and Topic Modeling\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **unsupervised learning**\n- **semantic embeddings**\n- **clustering**\n- **outliers**\n- **dimensionality reduction**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom sentence_transformers import SentenceTransformer\n# Pair embeddings with current UMAP/HDBSCAN/BERTopic APIs during implementation.\n```\n\n## Practice\nProduce one reproducible artifact for **Revision: From Embeddings to Unsupervised Text Discovery**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate UMAP, HDBSCAN, BERTopic, topic-representation, and embedding-model APIs.\n',
        "estimated_minutes": 30,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Revision: From Embeddings to Unsupervised Text Discovery — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Connect embedding and clustering foundations to discovering latent structure in unlabeled text collections.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['unsupervised-learning', 'semantic-embeddings', 'clustering'],
        },
        {
            'title': 'Revision: From Embeddings to Unsupervised Text Discovery — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Revision: From Embeddings to Unsupervised Text Discovery — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Revision: From Embeddings to Unsupervised Text Discovery?', 'options': ['Connect embedding and clustering foundations to discovering latent structure in unlabeled text collections.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
