"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-001'
MODULE_ID = 'M005-01'
LESSON_META = {
    "lesson_id": 'L005-001',
    "module_id": 'M005-01',
    "title": 'Revision: Representation Models vs Generative Models',
    "learning_objective": 'Differentiate representation and generative language models and connect each to practical LLM-system roles.',
    "curriculum_role": 'REVISION → APPLICATION FRAMING',
    "concepts": ['representation models', 'generative models', 'encoder-style models', 'decoder-style models', 'application selection'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 1, 'chapter_title': 'An Introduction to Large Language Models', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 30,
    "prerequisites": [],
    "modernization": ['Revalidate model IDs, tokenizer compatibility, context limits, and generation APIs before implementation.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Revision: Representation Models vs Generative Models',
    "slug": 'course-005-revision-representation-models-vs-generative-models',
    "description": 'Differentiate representation and generative language models and connect each to practical LLM-system roles.',
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.5,
    "skill_tags": ['applied-llm-engineering', 'representation-models', 'generative-models', 'encoder-style-models', 'decoder-style-models'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Revision: Representation Models vs Generative Models',
        "content": '# Revision: Representation Models vs Generative Models\n\n## Learning objective\nDifferentiate representation and generative language models and connect each to practical LLM-system roles.\n\n## Curriculum role\nREVISION → APPLICATION FRAMING\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 1: An Introduction to Large Language Models\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **representation models**\n- **generative models**\n- **encoder-style models**\n- **decoder-style models**\n- **application selection**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForCausalLM\n# Inspect a compatible causal model/tokenizer pair; validate the checkpoint before use.\n```\n\n## Practice\nProduce one reproducible artifact for **Revision: Representation Models vs Generative Models**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate model IDs, tokenizer compatibility, context limits, and generation APIs before implementation.\n',
        "estimated_minutes": 30,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Revision: Representation Models vs Generative Models — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Differentiate representation and generative language models and connect each to practical LLM-system roles.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['representation-models', 'generative-models', 'encoder-style-models'],
        },
        {
            'title': 'Revision: Representation Models vs Generative Models — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Revision: Representation Models vs Generative Models — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Revision: Representation Models vs Generative Models?', 'options': ['Differentiate representation and generative language models and connect each to practical LLM-system roles.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
