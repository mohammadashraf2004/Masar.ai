"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-028'
MODULE_ID = 'M004-05'
LESSON_META = {
    "lesson_id": "L004-028",
    "module_id": "M004-05",
    "title": "Top-k and Nucleus Sampling",
    "learning_objective": "Apply top-k and top-p sampling and reason about static versus dynamic candidate sets.",
    "concepts": [
        "top-k",
        "top-p",
        "nucleus sampling",
        "candidate truncation",
        "sampling controls"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 5,
        "chapter_title": "Text Generation",
        "pages": "136-140"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-027"
    ],
    "modernization": [
        "Use GenerationConfig/current generate() controls; do not present one decoding strategy as universally best."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Top-k and Nucleus Sampling',
    "slug": 'course-004-top-k-and-nucleus-sampling',
    "description": 'Apply top-k and top-p sampling and reason about static versus dynamic candidate sets.',
    "order": 5,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'top-k', 'top-p', 'nucleus-sampling', 'candidate-truncation'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Top-k and Nucleus Sampling',
        "content": '# Top-k and Nucleus Sampling\n\n## Learning objective\nApply top-k and top-p sampling and reason about static versus dynamic candidate sets.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 5\n- Pages: 136-140\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **top-k**\n- **top-p**\n- **nucleus sampling**\n- **candidate truncation**\n- **sampling controls**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForCausalLM\ncheckpoint = "gpt2"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForCausalLM.from_pretrained(checkpoint)\ninputs = tokenizer("Masar", return_tensors="pt")\noutput = model.generate(**inputs, max_new_tokens=32)\n```\n\n## Practice\nProduce one reproducible artifact for **Top-k and Nucleus Sampling**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use GenerationConfig/current generate() controls; do not present one decoding strategy as universally best.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Top-k and Nucleus Sampling — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Apply top-k and top-p sampling and reason about static versus dynamic candidate sets.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['top-k', 'top-p', 'nucleus-sampling'],
                },
        {
                    'title': 'Top-k and Nucleus Sampling — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Top-k and Nucleus Sampling — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Top-k and Nucleus Sampling"?', 'options': ['Apply top-k and top-p sampling and reason about static versus dynamic candidate sets.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
