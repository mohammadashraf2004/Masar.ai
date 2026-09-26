"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-061'
MODULE_ID = 'M005-09'
LESSON_META = {
    "lesson_id": 'L005-061',
    "module_id": 'M005-09',
    "title": 'Preparing Instruction Data & Chat Templates for SFT',
    "learning_objective": 'Prepare system/user/assistant examples in the exact conversation format expected by the target model.',
    "curriculum_role": 'NEW CORE',
    "concepts": ['instruction data', 'chat templates', 'role formatting', 'EOS/BOS boundaries', 'sequence length'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 12, 'chapter_title': 'Fine-Tuning Generation Models', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 40,
    "prerequisites": ['L005-060'],
    "modernization": ['Revalidate Transformers, PEFT, TRL, bitsandbytes, chat-template, SFT, and DPO APIs before training.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Preparing Instruction Data & Chat Templates for SFT',
    "slug": 'course-005-preparing-instruction-data-and-chat-templates-for-sft',
    "description": 'Prepare system/user/assistant examples in the exact conversation format expected by the target model.',
    "order": 3,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-llm-engineering', 'instruction-data', 'chat-templates', 'role-formatting', 'eos-bos-boundaries'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Preparing Instruction Data & Chat Templates for SFT',
        "content": '# Preparing Instruction Data & Chat Templates for SFT\n\n## Learning objective\nPrepare system/user/assistant examples in the exact conversation format expected by the target model.\n\n## Curriculum role\nNEW CORE\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 12: Fine-Tuning Generation Models\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **instruction data**\n- **chat templates**\n- **role formatting**\n- **EOS/BOS boundaries**\n- **sequence length**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom transformers import AutoModelForCausalLM, AutoTokenizer\n# Revalidate PEFT/TRL/bitsandbytes APIs and checkpoint compatibility before training.\n```\n\n## Practice\nProduce one reproducible artifact for **Preparing Instruction Data & Chat Templates for SFT**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate Transformers, PEFT, TRL, bitsandbytes, chat-template, SFT, and DPO APIs before training.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'Preparing Instruction Data & Chat Templates for SFT — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Prepare system/user/assistant examples in the exact conversation format expected by the target model.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['instruction-data', 'chat-templates', 'role-formatting'],
        },
        {
            'title': 'Preparing Instruction Data & Chat Templates for SFT — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'Preparing Instruction Data & Chat Templates for SFT — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of Preparing Instruction Data & Chat Templates for SFT?', 'options': ['Prepare system/user/assistant examples in the exact conversation format expected by the target model.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
