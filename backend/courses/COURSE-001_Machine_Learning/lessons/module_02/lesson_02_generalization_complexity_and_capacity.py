"""M02.L02 — Generalization, Complexity and Capacity.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 29–35. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M02.L02"
MODULE_ORDER = 2
MODULE_TITLE = 'Supervised Learning & Generalization'
MODULE_DESCRIPTION = 'Distinguish tasks and learn how flexibility, data volume and representation affect generalization.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '29–35'

TOPIC = {'title': 'Generalization, Complexity and Capacity',
 'slug': 'ml-foundations-m02-l02',
 'description': 'Training error can decrease while unseen-data error rises when a model fits '
                'noise; compare learning and validation behavior.',
 'order': 2,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-02'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Generalization, Complexity and Capacity',
            'content': '# Generalization, Complexity and Capacity\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M02.L02 | '
                       '**Module:** Supervised Learning & Generalization\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 29–35. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Training error can decrease while unseen-data error rises when '
                       'a model fits noise; compare learning and validation behavior.\n'
                       '- Apply the principle to: A highly flexible boundary perfectly fits the '
                       'samples yet misses new points.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Sketch underfit, balanced and overfit train/test error patterns.\n'
                       '\n'
                       '## Why this matters\n'
                       'Distinguish tasks and learn how flexibility, data volume and '
                       'representation affect generalization. This lesson focuses on '
                       '**generalization, complexity and capacity** so you can make an explicit '
                       'choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Training error can decrease while unseen-data error rises when a model '
                       'fits noise; compare learning and validation behavior.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A highly flexible boundary perfectly fits the samples yet misses new '
                       'points. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Sketch underfit, balanced and overfit train/test error patterns. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Never select model complexity by minimum training error alone. Explain how '
                       'your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **generalization, complexity and capacity** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Training error can decrease while unseen-data error '
                       'rises when a model fits noise; compare learning and validation behavior.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Generalization, Complexity and Capacity — hands-on activity',
                'description': 'Sketch underfit, balanced and overfit train/test error patterns. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-02']},
               {'title': 'Generalization, Complexity and Capacity — critical reasoning',
                'description': 'Consider this boundary: Never select model complexity by minimum '
                               'training error alone. Explain a failure mode if it is ignored and '
                               'the safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Generalization, Complexity and Capacity — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Generalization, Complexity and Capacity?',
                         'options': ['Training error can decrease while unseen-data error rises '
                                     'when a model fits noise; compare learning and validation '
                                     'behavior.',
                                     'The most flexible model always predicts unseen examples '
                                     'best.',
                                     'Every numeric target should be handled as classification.',
                                     'The neighborhood size never changes a kNN prediction.'],
                         'correct': 0,
                         'explanation': 'Training error can decrease while unseen-data error rises '
                                        'when a model fits noise; compare learning and validation '
                                        'behavior. In the worked scenario: A highly flexible '
                                        'boundary perfectly fits the samples yet misses new '
                                        'points.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Generalization, Complexity and Capacity?',
                         'options': ['Write X, y and a sensible metric for both situations.',
                                     'Compare several k values using a development split or CV.',
                                     'Sketch underfit, balanced and overfit train/test error '
                                     'patterns.',
                                     'Fit a kNN regressor and compare train and validation R² '
                                     'across k.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Sketch underfit, balanced and '
                                        'overfit train/test error patterns.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Never select model complexity by '
                                     'minimum training error alone.',
                         'type': 'open'}],
          'passing_score': 70}}
