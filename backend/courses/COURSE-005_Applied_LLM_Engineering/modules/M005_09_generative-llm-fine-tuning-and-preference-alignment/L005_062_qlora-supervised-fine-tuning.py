"""Masar COURSE-005 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L005-062'
MODULE_ID = 'M005-09'
LESSON_META = {
    "lesson_id": 'L005-062',
    "module_id": 'M005-09',
    "title": 'QLoRA Supervised Fine-Tuning',
    "learning_objective": 'Combine quantized base-model loading with LoRA adapters to instruction-tune a causal language model under limited memory.',
    "curriculum_role": 'NEW CORE PRACTICAL',
    "concepts": ['QLoRA', '4-bit quantization', 'LoRA adapters', 'SFT', 'gradient accumulation', 'adapter merging'],
    "source_reference": {'source_id': 'BOOK-005', 'book_title': 'SOURCE INFORMATION MISSING', 'edition': 'SOURCE INFORMATION MISSING', 'chapter': 12, 'chapter_title': 'Fine-Tuning Generation Models', 'pages': 'SOURCE INFORMATION MISSING'},
    "estimated_minutes": 60,
    "prerequisites": ['L005-061'],
    "modernization": ['Revalidate Transformers, PEFT, TRL, bitsandbytes, chat-template, SFT, and DPO APIs before training.'],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'QLoRA Supervised Fine-Tuning',
    "slug": 'course-005-qlora-supervised-fine-tuning',
    "description": 'Combine quantized base-model loading with LoRA adapters to instruction-tune a causal language model under limited memory.',
    "order": 4,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 1.0,
    "skill_tags": ['applied-llm-engineering', 'qlora', '4-bit-quantization', 'lora-adapters', 'sft'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'QLoRA Supervised Fine-Tuning',
        "content": '# QLoRA Supervised Fine-Tuning\n\n## Learning objective\nCombine quantized base-model loading with LoRA adapters to instruction-tune a causal language model under limited memory.\n\n## Curriculum role\nNEW CORE PRACTICAL\n\n## Source mapping\n- Source: BOOK-005 — SOURCE INFORMATION MISSING\n- Chapter 12: Fine-Tuning Generation Models\n- Pages: SOURCE INFORMATION MISSING\n\n## Why this matters\nThis lesson converts the finalized COURSE-005 curriculum into an applied Masar competency. Repeated prerequisite material is treated as revision; new material is used to make, implement, debug, or evaluate a concrete LLM-engineering decision.\n\n## Concepts\n- **QLoRA**\n- **4-bit quantization**\n- **LoRA adapters**\n- **SFT**\n- **gradient accumulation**\n- **adapter merging**\n\n## Applied workflow\n1. Establish the task, constraints, and baseline.\n2. Inspect inputs, outputs, state, retrieval results, model behavior, or metrics before changing the system.\n3. Implement the smallest useful experiment supported by the lesson.\n4. Record realistic failures instead of hiding them.\n5. Evaluate against an explicit acceptance criterion and document what would change the decision.\n\n## Code orientation\n```python\nfrom transformers import AutoModelForCausalLM, AutoTokenizer\n# Revalidate PEFT/TRL/bitsandbytes APIs and checkpoint compatibility before training.\n```\n\n## Practice\nProduce one reproducible artifact for **QLoRA Supervised Fine-Tuning**: executable code, an evaluation table, an error-analysis note, a trace, a dataset sample, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data / tokenizer / model / tool / retrieval compatibility as applicable.\n- Inspect at least one real intermediate artifact rather than only the final prose output.\n- Check evaluation data and metric logic before interpreting results.\n- Record at least one plausible failure mode and how you would detect it.\n- Never fabricate benchmark, latency, quality, or training results.\n\n## Assessment\nExplain the main engineering trade-off in this lesson, show evidence from your practice artifact, and state what would make you choose a different approach.\n\n## Modernization note\n- Revalidate Transformers, PEFT, TRL, bitsandbytes, chat-template, SFT, and DPO APIs before training.\n',
        "estimated_minutes": 60,
        "has_code_examples": True,
    },
    "exercises": [
        {
            'title': 'QLoRA Supervised Fine-Tuning — Guided Practice',
            'description': 'Complete a reproducible task that demonstrates: Combine quantized base-model loading with LoRA adapters to instruction-tune a causal language model under limited memory.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['qlora', '4-bit-quantization', 'lora-adapters'],
        },
        {
            'title': 'QLoRA Supervised Fine-Tuning — Debug / Evaluate',
            'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
            'difficulty': DifficultyLevel.advanced,
            'skill_tested': ['debugging', 'evaluation'],
        }
    ],
    "quiz": {
        'title': 'QLoRA Supervised Fine-Tuning — Knowledge Check',
        'questions': [
            {'question': 'What is the primary objective of QLoRA Supervised Fine-Tuning?', 'options': ['Combine quantized base-model loading with LoRA adapters to instruction-tune a causal language model under limited memory.', 'Memorize every source paragraph', 'Choose the largest model regardless of constraints', 'Skip evaluation if the code runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'},
            {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose a framework before defining the task'], 'correct': 0, 'explanation': 'COURSE-005 preserves the applied Masar learning loop.'},
            {'question': 'How should outdated source APIs be handled?', 'options': ['Preserve the concept, revalidate the current API, and label modernization', 'Silently copy the old API', 'Invent successful output', 'Delete the entire lesson'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}
        ],
        'passing_score': 70
    },
    "project": None,
}
