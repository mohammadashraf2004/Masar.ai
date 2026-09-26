"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-015'
MODULE_ID = 'M005-01'
LESSON_META = {
    "lesson_id": 'L005-015',
    "module_id": 'M005-01',
    "title": 'Choosing an LLM Classification Strategy',
    "learning_objective": 'Choose among task-specific models, embeddings plus lightweight classifiers, zero-shot embeddings, and generative classification.',
    "curriculum_role": 'REVISION → DECISION EXTENSION',
    "concepts": ['task-specific models', 'embedding classifiers', 'zero-shot classification', 'generative classification', 'latency-cost tradeoffs'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 4, 'chapter_title': 'Text Classification', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 45,
    "prerequisites": ['L005-014'],
    "modernization": ['Revalidate model IDs, tokenizer compatibility, context limits, and generation APIs before implementation.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Choosing an LLM Classification Strategy',
    "slug": 'course-005-choosing-an-llm-classification-strategy',
    "description": 'Choose among task-specific models, embeddings plus lightweight classifiers, zero-shot embeddings, and generative classification.',
    "order": 10,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-llm-engineering', 'task-specific-models', 'embedding-classifiers', 'zero-shot-classification', 'generative-classification'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Choosing an LLM Classification Strategy',
        "content": '# Choosing an LLM Classification Strategy\n\n## Learning objective\nChoose among task-specific models, embeddings plus lightweight classifiers, zero-shot embeddings, and generative classification.\n\n## Curriculum role\nREVISION → DECISION EXTENSION\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 4: Text Classification\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **task-specific models**\n- **embedding classifiers**\n- **zero-shot classification**\n- **generative classification**\n- **latency-cost tradeoffs**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForCausalLM\n# Inspect a compatible causal model/tokenizer pair; validate the checkpoint before use.\n```\n\n## Practice\nProduce one reproducible artifact for **Choosing an LLM Classification Strategy**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate model IDs, tokenizer compatibility, context limits, and generation APIs before implementation.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Choosing an LLM Classification Strategy — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Choose among task-specific models, embeddings plus lightweight classifiers, zero-shot embeddings, and generative classification.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['task-specific-models', 'embedding-classifiers', 'zero-shot-classification'],
        },
        {
            'title': 'Choosing an LLM Classification Strategy — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Choosing an LLM Classification Strategy — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Choosing an LLM Classification Strategy?', 'options': ['Choose among task-specific models, embeddings plus lightweight classifiers, zero-shot embeddings, and generative classification.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": {
            'title': 'LLM Execution & Model Selection Lab',
            'description': 'Inspect and compare candidate LLM execution paths, model architecture signals, resource constraints, and classification choices.',
            'difficulty': DifficultyLevel.intermediate,
            'tech_stack': ['Python', 'PyTorch', 'Hugging Face ecosystem'],
            'objectives': ['Build a reproducible workflow', 'Compare against a baseline', 'Debug concrete failures', 'Evaluate with task-appropriate evidence', 'Document limitations'],
            'rubric': {'correctness': 30, 'evaluation': 25, 'debugging': 20, 'reproducibility': 15, 'documentation': 10},
            'starter_repo_url': None,
            'estimated_hours': 4.0,
        },
}
