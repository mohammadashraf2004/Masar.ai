"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-031'
MODULE_ID = 'M005-06'
LESSON_META = {
    "lesson_id": 'L005-031',
    "module_id": 'M005-06',
    "title": 'Revision: From Prompt Chains to LLM Workflows',
    "learning_objective": 'Formalize prompt chains as reusable LLM workflows with explicit inputs, outputs, intermediate state, and debuggability.',
    "curriculum_role": 'REVISION → EXTENSION',
    "concepts": ['chains', 'workflow composition', 'state', 'intermediate outputs', 'deterministic pipelines'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 7, 'chapter_title': 'Advanced Text Generation Techniques and Tools', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 35,
    "prerequisites": [],
    "modernization": ['Keep orchestration concepts framework-independent; revalidate current LangChain/LangGraph or equivalent state/tool APIs.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Revision: From Prompt Chains to LLM Workflows',
    "slug": 'course-005-revision-from-prompt-chains-to-llm-workflows',
    "description": 'Formalize prompt chains as reusable LLM workflows with explicit inputs, outputs, intermediate state, and debuggability.',
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.583,
    "skill_tags": ['applied-llm-engineering', 'chains', 'workflow-composition', 'state', 'intermediate-outputs'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Revision: From Prompt Chains to LLM Workflows',
        "content": '# Revision: From Prompt Chains to LLM Workflows\n\n## Learning objective\nFormalize prompt chains as reusable LLM workflows with explicit inputs, outputs, intermediate state, and debuggability.\n\n## Curriculum role\nREVISION → EXTENSION\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 7: Advanced Text Generation Techniques and Tools\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **chains**\n- **workflow composition**\n- **state**\n- **intermediate outputs**\n- **deterministic pipelines**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\ndef tool(input_data):\n    """Bounded external capability."""\n    raise NotImplementedError\n# Keep state, tool calls, observations, and stopping explicit.\n```\n\n## Practice\nProduce one reproducible artifact for **Revision: From Prompt Chains to LLM Workflows**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Keep orchestration concepts framework-independent; revalidate current LangChain/LangGraph or equivalent state/tool APIs.\n',
        "estimated_minutes": 35,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Revision: From Prompt Chains to LLM Workflows — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Formalize prompt chains as reusable LLM workflows with explicit inputs, outputs, intermediate state, and debuggability.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['chains', 'workflow-composition', 'state'],
        },
        {
            'title': 'Revision: From Prompt Chains to LLM Workflows — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.intermediate,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Revision: From Prompt Chains to LLM Workflows — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Revision: From Prompt Chains to LLM Workflows?', 'options': ['Formalize prompt chains as reusable LLM workflows with explicit inputs, outputs, intermediate state, and debuggability.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
