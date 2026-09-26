"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-069'
MODULE_ID = 'M005-10'
LESSON_META = {
    "lesson_id": 'L005-069',
    "module_id": 'M005-10',
    "title": 'Evaluation & Failure Analysis',
    "learning_objective": 'Evaluate component-level and end-to-end behavior and classify failures across retrieval, generation, orchestration, and adaptation.',
    "curriculum_role": 'MASAR ADDITION',
    "concepts": ['end-to-end evaluation', 'failure analysis', 'component metrics', 'latency', 'resource constraints'],
    "source_reference": {'source_id': 'MASAR-ADDITION', 'book_title': 'MASAR ADDITION', 'edition': None, 'chapter': None, 'chapter_title': 'MASAR ADDITION', 'pages': 'N/A'},
    "estimated_minutes": 50,
    "prerequisites": ['L005-068'],
    "modernization": ['Integrate only tested dependencies; document exact versions, model IDs, data, and evaluation setup used by the capstone.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Evaluation & Failure Analysis',
    "slug": 'course-005-evaluation-and-failure-analysis',
    "description": 'Evaluate component-level and end-to-end behavior and classify failures across retrieval, generation, orchestration, and adaptation.',
    "order": 3,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.833,
    "skill_tags": ['applied-llm-engineering', 'end-to-end-evaluation', 'failure-analysis', 'component-metrics', 'latency'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Evaluation & Failure Analysis',
        "content": '# Evaluation & Failure Analysis\n\n## Learning objective\nEvaluate component-level and end-to-end behavior and classify failures across retrieval, generation, orchestration, and adaptation.\n\n## Curriculum role\nMASAR ADDITION\n\n## Source mapping\n- Source: MASAR-ADDITION — MASAR ADDITION\n- Type: MASAR ADDITION\n- Source chapter/pages: N/A\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **end-to-end evaluation**\n- **failure analysis**\n- **component metrics**\n- **latency**\n- **resource constraints**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\n# Integrate the smallest justified LLM system, then evaluate it against explicit acceptance criteria.\n```\n\n## Practice\nProduce one reproducible artifact for **Evaluation & Failure Analysis**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Integrate only tested dependencies; document exact versions, model IDs, data, and evaluation setup used by the capstone.\n',
        "estimated_minutes": 50,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Evaluation & Failure Analysis — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Evaluate component-level and end-to-end behavior and classify failures across retrieval, generation, orchestration, and adaptation.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['end-to-end-evaluation', 'failure-analysis', 'component-metrics'],
        },
        {
            'title': 'Evaluation & Failure Analysis — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Evaluation & Failure Analysis — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Evaluation & Failure Analysis?', 'options': ['Evaluate component-level and end-to-end behavior and classify failures across retrieval, generation, orchestration, and adaptation.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
