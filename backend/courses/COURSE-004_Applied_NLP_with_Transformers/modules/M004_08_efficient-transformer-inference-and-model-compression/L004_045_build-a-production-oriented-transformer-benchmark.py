"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-045'
MODULE_ID = 'M004-08'
LESSON_META = {
    "lesson_id": "L004-045",
    "module_id": "M004-08",
    "title": "Build a Production-Oriented Transformer Benchmark",
    "learning_objective": "Create a benchmark that measures task quality, latency, and model size under realistic conditions.",
    "concepts": [
        "accuracy/F1",
        "latency warmup",
        "variance",
        "model size",
        "hardware context",
        "benchmark protocol"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 8,
        "chapter_title": "Making Transformers Efficient in Production",
        "pages": "209-217"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-044"
    ],
    "modernization": [
        "Use current PyTorch/torchao, ONNX Runtime/Optimum-style export paths where available; benchmark on target hardware."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Build a Production-Oriented Transformer Benchmark',
    "slug": 'course-004-build-a-production-oriented-transformer-benchmark',
    "description": 'Create a benchmark that measures task quality, latency, and model size under realistic conditions.',
    "order": 1,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'accuracy-f1', 'latency-warmup', 'variance', 'model-size'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Build a Production-Oriented Transformer Benchmark',
        "content": '# Build a Production-Oriented Transformer Benchmark\n\n## Learning objective\nCreate a benchmark that measures task quality, latency, and model size under realistic conditions.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 8\n- Pages: 209-217\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **accuracy/F1**\n- **latency warmup**\n- **variance**\n- **model size**\n- **hardware context**\n- **benchmark protocol**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom time import perf_counter\nstart = perf_counter()\n# prediction = model_or_pipeline(sample)\nelapsed_ms = (perf_counter() - start) * 1000\nprint({"latency_ms": elapsed_ms})\n```\n\n## Practice\nProduce one reproducible artifact for **Build a Production-Oriented Transformer Benchmark**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use current PyTorch/torchao, ONNX Runtime/Optimum-style export paths where available; benchmark on target hardware.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Build a Production-Oriented Transformer Benchmark — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Create a benchmark that measures task quality, latency, and model size under realistic conditions.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['accuracy-f1', 'latency-warmup', 'variance'],
                },
        {
                    'title': 'Build a Production-Oriented Transformer Benchmark — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Build a Production-Oriented Transformer Benchmark — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Build a Production-Oriented Transformer Benchmark"?', 'options': ['Create a benchmark that measures task quality, latency, and model size under realistic conditions.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
