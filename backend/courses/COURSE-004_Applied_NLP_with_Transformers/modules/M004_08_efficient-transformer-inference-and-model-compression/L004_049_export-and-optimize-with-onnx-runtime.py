"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-049'
MODULE_ID = 'M004-08'
LESSON_META = {
    "lesson_id": "L004-049",
    "module_id": "M004-08",
    "title": "Export and Optimize with ONNX Runtime",
    "learning_objective": "Export a Transformer to ONNX/ORT and benchmark graph-optimized inference.",
    "concepts": [
        "ONNX",
        "ONNX Runtime",
        "graph optimization",
        "operator fusion",
        "execution providers",
        "quantized ONNX"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 8,
        "chapter_title": "Making Transformers Efficient in Production",
        "pages": "237-243"
    },
    "estimated_minutes": 50,
    "prerequisites": [
        "L004-048"
    ],
    "modernization": [
        "Use current PyTorch/torchao, ONNX Runtime/Optimum-style export paths where available; benchmark on target hardware."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Export and Optimize with ONNX Runtime',
    "slug": 'course-004-export-and-optimize-with-onnx-runtime',
    "description": 'Export a Transformer to ONNX/ORT and benchmark graph-optimized inference.',
    "order": 5,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.833,
    "skill_tags": ['applied-nlp', 'transformers', 'onnx', 'onnx-runtime', 'graph-optimization', 'operator-fusion'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Export and Optimize with ONNX Runtime',
        "content": '# Export and Optimize with ONNX Runtime\n\n## Learning objective\nExport a Transformer to ONNX/ORT and benchmark graph-optimized inference.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 8\n- Pages: 237-243\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **ONNX**\n- **ONNX Runtime**\n- **graph optimization**\n- **operator fusion**\n- **execution providers**\n- **quantized ONNX**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom time import perf_counter\nstart = perf_counter()\n# prediction = model_or_pipeline(sample)\nelapsed_ms = (perf_counter() - start) * 1000\nprint({"latency_ms": elapsed_ms})\n```\n\n## Practice\nProduce one reproducible artifact for **Export and Optimize with ONNX Runtime**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use current PyTorch/torchao, ONNX Runtime/Optimum-style export paths where available; benchmark on target hardware.\n',
        "estimated_minutes": 50,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Export and Optimize with ONNX Runtime — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Export a Transformer to ONNX/ORT and benchmark graph-optimized inference.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['onnx', 'onnx-runtime', 'graph-optimization'],
                },
        {
                    'title': 'Export and Optimize with ONNX Runtime — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Export and Optimize with ONNX Runtime — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Export and Optimize with ONNX Runtime"?', 'options': ['Export a Transformer to ONNX/ORT and benchmark graph-optimized inference.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": None,
}
