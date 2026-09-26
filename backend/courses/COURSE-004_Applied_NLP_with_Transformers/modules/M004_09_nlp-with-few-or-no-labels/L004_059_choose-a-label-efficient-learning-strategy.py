"""Masar COURSE-004 lesson seed.

Generated from the finalized curriculum design. This file uses only fields present
in the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed template. Repository
integration and end-to-end lesson execution must still be validated in the target app.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L004-059'
MODULE_ID = 'M004-09'
LESSON_META = {
    "lesson_id": "L004-059",
    "module_id": "M004-09",
    "title": "Choose a Label-Efficient Learning Strategy",
    "learning_objective": "Choose between zero-shot, embeddings, augmentation, fine-tuning, domain adaptation, and semi-supervised learning based on constraints.",
    "concepts": [
        "decision tree",
        "annotation cost",
        "error cost",
        "active learning awareness",
        "evaluation plan"
    ],
    "source_reference": {
        "source_id": "BOOK-004",
        "book_title": "SOURCE INFORMATION MISSING",
        "edition": "SOURCE INFORMATION MISSING",
        "chapter": 9,
        "chapter_title": "Dealing with Few to No Labels",
        "pages": "249-297"
    },
    "estimated_minutes": 40,
    "prerequisites": [
        "L004-058"
    ],
    "modernization": [
        "Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default."
    ],
    "status": "Draft lesson seed / curriculum finalized"
}

TOPIC = {
    "title": 'Choose a Label-Efficient Learning Strategy',
    "slug": 'course-004-choose-a-label-efficient-learning-strategy',
    "description": 'Choose between zero-shot, embeddings, augmentation, fine-tuning, domain adaptation, and semi-supervised learning based on constraints.',
    "order": 8,
    "difficulty": DifficultyLevel.advanced,
    "estimated_hours": 0.667,
    "skill_tags": ['applied-nlp', 'transformers', 'decision-tree', 'annotation-cost', 'error-cost', 'active-learning-awareness'],
    "prerequisite_ids": [],
    "lesson": {
        "title": 'Choose a Label-Efficient Learning Strategy',
        "content": '# Choose a Label-Efficient Learning Strategy\n\n## Learning objective\nChoose between zero-shot, embeddings, augmentation, fine-tuning, domain adaptation, and semi-supervised learning based on constraints.\n\n## Source mapping\n- Source: BOOK-004 — SOURCE INFORMATION MISSING\n- Chapter 9\n- Pages: 249-297\n\n## Why this matters\nThis lesson converts the chapter material into an applied Masar competency. The focus is not to memorize the book; it is to make a defensible engineering decision, implement or inspect the relevant workflow, and evaluate the result.\n\n## Concepts\n- **decision tree**\n- **annotation cost**\n- **error cost**\n- **active learning awareness**\n- **evaluation plan**\n\n## Applied workflow\n1. Establish the task and the evidence you need.\n2. Inspect the inputs, outputs, shapes, or metrics before changing the model.\n3. Implement the smallest useful experiment.\n4. Record failures instead of hiding them.\n5. Compare the result against a baseline or acceptance criterion.\n\n## Code orientation\n```python\nfrom transformers import pipeline\n# Replace with the task/checkpoint selected in the lesson.\n```\n\n## Practice\nProduce one reproducible artifact for **Choose a Label-Efficient Learning Strategy**: code, an evaluation table, an error-analysis note, or an architecture decision record depending on the lesson.\n\n## Debug checklist\n- Verify data/tokenizer/model compatibility.\n- Inspect at least one batch or model output directly.\n- Check the metric implementation and evaluation split.\n- Record one plausible failure mode and how you would detect it.\n\n## Assessment\nExplain the main trade-off in this lesson, show evidence from your practice artifact, and state what would make you change your implementation decision.\n\n## Modernization note\n- Use modern sentence embeddings and current few-shot/zero-shot tooling rather than relying on old GPT-2 mean pooling as the default.\n',
        "estimated_minutes": 40,
        "has_code_examples": True,
    },
    "exercises": [
        {
                    'title': 'Choose a Label-Efficient Learning Strategy — Guided Practice',
                    'description': 'Complete a small reproducible task that demonstrates: Choose between zero-shot, embeddings, augmentation, fine-tuning, domain adaptation, and semi-supervised learning based on constraints.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['decision-tree', 'annotation-cost', 'error-cost'],
                },
        {
                    'title': 'Choose a Label-Efficient Learning Strategy — Debug / Evaluate',
                    'description': 'Introduce or locate one realistic failure, diagnose it with evidence, and document the corrective decision.',
                    'difficulty': DifficultyLevel.advanced,
                    'skill_tested': ['debugging', 'evaluation'],
                }
    ],
    "quiz": {'title': 'Choose a Label-Efficient Learning Strategy — Knowledge Check', 'questions': [{'question': 'What is the primary objective of "Choose a Label-Efficient Learning Strategy"?', 'options': ['Choose between zero-shot, embeddings, augmentation, fine-tuning, domain adaptation, and semi-supervised learning based on constraints.', 'Memorize every source paragraph', 'Maximize model size regardless of constraints', 'Skip evaluation if inference runs'], 'correct': 0, 'explanation': 'The lesson is organized around the stated engineering learning objective.'}, {'question': 'Which practice best matches the Masar learning loop?', 'options': ['Learn → Practice → Build → Debug → Evaluate', 'Read → Memorize → Stop', 'Train once → Deploy without evaluation', 'Choose the largest model first'], 'correct': 0, 'explanation': 'COURSE-004 preserves the implementation-first Masar loop.'}, {'question': 'What should happen when a source API or recommendation is outdated?', 'options': ['Preserve the concept but modernize the implementation and label the change', 'Silently copy the old API', 'Delete the entire concept', 'Invent a benchmark result'], 'correct': 0, 'explanation': 'Source fidelity and modernization are tracked separately.'}], 'passing_score': 70},
    "project": {
            'title': 'Label-Efficiency Strategy Lab',
            'description': 'Compare at least three low-label approaches across controlled label budgets.',
            'difficulty': DifficultyLevel.advanced,
            'tech_stack': ['Python', 'PyTorch', 'Hugging Face Transformers'],
            'objectives': ['Build a reproducible workflow', 'Compare against a baseline', 'Debug concrete failures', 'Evaluate with task-appropriate metrics', 'Document limitations'],
            'rubric': {'correctness': 30, 'evaluation': 25, 'debugging': 20, 'reproducibility': 15, 'documentation': 10},
            'starter_repo_url': None,
            'estimated_hours': 3.0,
        },
}
