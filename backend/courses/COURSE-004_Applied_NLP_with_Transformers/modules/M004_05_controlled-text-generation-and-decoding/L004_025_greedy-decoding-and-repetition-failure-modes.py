"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-025'
MODULE_ID = 'M004-05'
LESSON_META = {
    "lesson_id": "L004-025",
    "module_id": "M004-05",
    "title": "Greedy Decoding and Repetition Failure Modes",
    "learning_objective": "Implement greedy decoding and diagnose why locally optimal choices can produce poor text.",
    "concepts": [
        "greedy search",
        "argmax decoding",
        "repetition",
        "degeneration",
        "deterministic generation"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 5,
        "chapter_title": "Text Generation",
        "pages": "127-130"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-024"
    ],
    "modernization": [
        "Use GenerationConfig/current generate() controls; do not present one decoding strategy as universally best."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Greedy Decoding and Repetition Failure Modes',
    "slug": 'course-004-greedy-decoding-and-repetition-failure-modes',
    "description": 'Implement greedy decoding and diagnose why locally optimal choices can produce poor text.',
    "order": 2,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'greedy-search', 'argmax-decoding', 'repetition', 'degeneration'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Greedy Decoding and Repetition Failure Modes',
        "content": '# Greedy Decoding and Repetition Failure Modes\n\n## Learning objective\nImplement greedy decoding and diagnose why locally optimal choices can produce poor text.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 5\n- Pages: 127-130\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **greedy search**\n- **argmax decoding**\n- **repetition**\n- **degeneration**\n- **deterministic generation**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForCausalLM\ncheckpoint = "gpt2"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForCausalLM.from_pretrained(checkpoint)\ninputs = tokenizer("Masar", return_tensors="pt")\noutput = model.generate(**inputs, max_new_tokens=32)\n```\n\n## Practice\nProduce one reproducible artifact for **Greedy Decoding and Repetition Failure Modes**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use GenerationConfig/current generate() controls; do not present one decoding strategy as universally best.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Greedy Decoding and Repetition Failure Modes — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Implement greedy decoding and diagnose why locally optimal choices can produce poor text.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['greedy-search', 'argmax-decoding', 'repetition'],
                },
        {
                    'title': 'Greedy Decoding and Repetition Failure Modes — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Greedy Decoding and Repetition Failure Modes — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Greedy Decoding and Repetition Failure Modes"?', 'options': ['Implement greedy decoding and diagnose why locally optimal choices can produce poor text.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
