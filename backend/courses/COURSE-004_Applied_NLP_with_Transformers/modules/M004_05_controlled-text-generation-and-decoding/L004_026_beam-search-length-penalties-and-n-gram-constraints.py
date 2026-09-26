"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-026'
MODULE_ID = 'M004-05'
LESSON_META = {
    "lesson_id": "L004-026",
    "module_id": "M004-05",
    "title": "Beam Search, Length Penalties & N-Gram Constraints",
    "learning_objective": "Use beam search and constraints while understanding probability/quality trade-offs.",
    "concepts": [
        "beam search",
        "num_beams",
        "length penalty",
        "no-repeat n-grams",
        "sequence scores"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 5,
        "chapter_title": "Text Generation",
        "pages": "130-134"
    },
    "estimated_minutes": 45,
    "prerequisites": [
        "L004-025"
    ],
    "modernization": [
        "Use GenerationConfig/current generate() controls; do not present one decoding strategy as universally best."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Beam Search, Length Penalties & N-Gram Constraints',
    "slug": 'course-004-beam-search-length-penalties-and-n-gram-constraints',
    "description": 'Use beam search and constraints while understanding probability/quality trade-offs.',
    "order": 3,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 0.75,
    "skill_tags": ['applied-nlp', 'transformers', 'beam-search', 'num-beams', 'length-penalty', 'no-repeat-n-grams'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Beam Search, Length Penalties & N-Gram Constraints',
        "content": '# Beam Search, Length Penalties & N-Gram Constraints\n\n## Learning objective\nUse beam search and constraints while understanding probability/quality trade-offs.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 5\n- Pages: 130-134\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **beam search**\n- **num_beams**\n- **length penalty**\n- **no-repeat n-grams**\n- **sequence scores**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import AutoTokenizer, AutoModelForCausalLM\ncheckpoint = "gpt2"\ntokenizer = AutoTokenizer.from_pretrained(checkpoint)\nmodel = AutoModelForCausalLM.from_pretrained(checkpoint)\ninputs = tokenizer("Masar", return_tensors="pt")\noutput = model.generate(**inputs, max_new_tokens=32)\n```\n\n## Practice\nProduce one reproducible artifact for **Beam Search, Length Penalties & N-Gram Constraints**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use GenerationConfig/current generate() controls; do not present one decoding strategy as universally best.\n',
        "estimated_minutes": 45,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Beam Search, Length Penalties & N-Gram Constraints — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Use beam search and constraints while understanding probability/quality trade-offs.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['beam-search', 'num-beams', 'length-penalty'],
                },
        {
                    'title': 'Beam Search, Length Penalties & N-Gram Constraints — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.intermediate,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Beam Search, Length Penalties & N-Gram Constraints — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Beam Search, Length Penalties & N-Gram Constraints"?', 'options': ['Use beam search and constraints while understanding probability/quality trade-offs.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
