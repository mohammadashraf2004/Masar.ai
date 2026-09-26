"""M03.L04 — Multiclass Linear Prediction.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 61–65. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M03.L04"
MODULE_ORDER = 3
MODULE_TITLE = 'Linear & Probabilistic Models'
MODULE_DESCRIPTION = 'Understand linear predictions, regularization, probabilistic baselines and multiclass decision rules.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '61–65'

TOPIC = {'title': 'Multiclass Linear Prediction',
 'slug': 'ml-foundations-m03-l04',
 'description': 'Multiclass linear estimators produce classwise evidence and select a class; '
                'examine decision shapes and label order.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5,
 'skill_tags': ['machine-learning', 'foundations', 'module-03'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Multiclass Linear Prediction',
            'content': '# Multiclass Linear Prediction\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M03.L04 | '
                       '**Module:** Linear & Probabilistic Models\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 61–65. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Multiclass linear estimators produce classwise evidence and '
                       'select a class; examine decision shapes and label order.\n'
                       '- Apply the principle to: Iris predicts among three flowers from several '
                       'competing class scores.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Check '
                       'classes_ and explain how a predicted label relates to scores.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand linear predictions, regularization, probabilistic baselines and '
                       'multiclass decision rules. This lesson focuses on **multiclass linear '
                       'prediction** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Multiclass linear estimators produce classwise evidence and select a '
                       'class; examine decision shapes and label order.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Iris predicts among three flowers from several competing class scores. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Check classes_ and explain how a predicted label relates to scores. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not assume the positive-class column for every classwise output. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **multiclass linear prediction** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Multiclass linear estimators produce classwise '
                       'evidence and select a class; examine decision shapes and label order.\n',
            'estimated_minutes': 30,
            'has_code_examples': False},
 'exercises': [{'title': 'Multiclass Linear Prediction — hands-on activity',
                'description': 'Check classes_ and explain how a predicted label relates to '
                               'scores. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-03']},
               {'title': 'Multiclass Linear Prediction — critical reasoning',
                'description': 'Consider this boundary: Do not assume the positive-class column '
                               'for every classwise output. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Multiclass Linear Prediction — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Multiclass Linear Prediction?',
                         'options': ['Regularization controls only the size of the dataset.',
                                     'All linear-classifier scores are calibrated probabilities.',
                                     'Learned coefficients establish causal relationships.',
                                     'Multiclass linear estimators produce classwise evidence and '
                                     'select a class; examine decision shapes and label order.'],
                         'correct': 3,
                         'explanation': 'Multiclass linear estimators produce classwise evidence '
                                        'and select a class; examine decision shapes and label '
                                        'order. In the worked scenario: Iris predicts among three '
                                        'flowers from several competing class scores.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Multiclass Linear Prediction?',
                         'options': ['Fit LinearRegression and explain one coefficient while '
                                     'holding other features fixed.',
                                     'Check classes_ and explain how a predicted label relates to '
                                     'scores.',
                                     'Compare coefficient patterns and held-out error for several '
                                     'alpha values.',
                                     'Train logistic regression and linear SVM on scaled training '
                                     'data and compare boundaries.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Check classes_ and explain how '
                                        'a predicted label relates to scores.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not assume the positive-class '
                                     'column for every classwise output.',
                         'type': 'open'}],
          'passing_score': 70}}
