"""M15.L01 — Training, Validation, Test and Generalization.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 251–252, 261–263. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M15.L01"
MODULE_ORDER = 15
MODULE_TITLE = 'Reliable Model Evaluation'
MODULE_DESCRIPTION = 'Separate evaluation roles and choose cross-validation consistent with the sampling process.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '251–252, 261–263'

TOPIC = {'title': 'Training, Validation, Test and Generalization',
 'slug': 'ml-foundations-m15-l01',
 'description': 'Train parameters on training data, choose configurations on validation data, and '
                'use an untouched test set for final assessment.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-15'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Training, Validation, Test and Generalization',
            'content': '# Training, Validation, Test and Generalization\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M15.L01 | '
                       '**Module:** Reliable Model Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 251–252, 261–263. This '
                       'is an original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Train parameters on training data, choose configurations on '
                       'validation data, and use an untouched test set for final assessment.\n'
                       '- Apply the principle to: Trying twenty models on the test labels makes '
                       'that set part of development.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Draw '
                       'data-flow boundaries for training, tuning and final reporting.\n'
                       '\n'
                       '## Why this matters\n'
                       'Separate evaluation roles and choose cross-validation consistent with the '
                       'sampling process. This lesson focuses on **training, validation, test and '
                       'generalization** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Train parameters on training data, choose configurations on validation '
                       'data, and use an untouched test set for final assessment.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Trying twenty models on the test labels makes that set part of '
                       'development. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Draw data-flow boundaries for training, tuning and final reporting. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A test set is not a hyperparameter tuning set. Explain how your method '
                       'respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **training, validation, test and generalization** in your own '
                       'words and answer: what would change in the worked scenario if you ignored '
                       'the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Train parameters on training data, choose '
                       'configurations on validation data, and use an untouched test set for final '
                       'assessment.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Training, Validation, Test and Generalization — hands-on activity',
                'description': 'Draw data-flow boundaries for training, tuning and final '
                               'reporting. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-15']},
               {'title': 'Training, Validation, Test and Generalization — critical reasoning',
                'description': 'Consider this boundary: A test set is not a hyperparameter tuning '
                               'set. Explain a failure mode if it is ignored and the safeguard you '
                               'would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Training, Validation, Test and Generalization — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Training, Validation, Test and Generalization?',
                         'options': ['Train parameters on training data, choose configurations on '
                                     'validation data, and use an untouched test set for final '
                                     'assessment.',
                                     'The final test set is appropriate for repeated tuning.',
                                     'Stratification prevents all forms of leakage.',
                                     'Group identity can be ignored when rows are correlated.'],
                         'correct': 0,
                         'explanation': 'Train parameters on training data, choose configurations '
                                        'on validation data, and use an untouched test set for '
                                        'final assessment. In the worked scenario: Trying twenty '
                                        'models on the test labels makes that set part of '
                                        'development.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Training, Validation, Test and Generalization?',
                         'options': ['Run cross_val_score and report mean and individual fold '
                                     'scores.',
                                     'Choose a splitter for a small imbalanced dataset and justify '
                                     'it.',
                                     'Draw data-flow boundaries for training, tuning and final '
                                     'reporting.',
                                     'Audit overlap of group IDs across folds and document the '
                                     'constraint.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Draw data-flow boundaries for '
                                        'training, tuning and final reporting.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A test set is not a hyperparameter '
                                     'tuning set.',
                         'type': 'open'}],
          'passing_score': 70}}
