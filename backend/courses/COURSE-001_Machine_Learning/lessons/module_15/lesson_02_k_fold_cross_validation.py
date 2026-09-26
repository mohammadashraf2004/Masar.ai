"""M15.L02 — k-Fold Cross-Validation.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 252–254. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M15.L02"
MODULE_ORDER = 15
MODULE_TITLE = 'Reliable Model Evaluation'
MODULE_DESCRIPTION = 'Separate evaluation roles and choose cross-validation consistent with the sampling process.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '252–254'

TOPIC = {'title': 'k-Fold Cross-Validation',
 'slug': 'ml-foundations-m15-l02',
 'description': 'Each fold is held out once for validation and used for training in the other k-1 '
                'rounds; aggregate scores and inspect spread.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-15'],
 'prerequisite_ids': [],
 'lesson': {'title': 'k-Fold Cross-Validation',
            'content': '# k-Fold Cross-Validation\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M15.L02 | '
                       '**Module:** Reliable Model Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 252–254. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Each fold is held out once for validation and used for training '
                       'in the other k-1 rounds; aggregate scores and inspect spread.\n'
                       '- Apply the principle to: Five-fold CV creates five fitted models for five '
                       'validation measurements.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Run '
                       'cross_val_score and report mean and individual fold scores.\n'
                       '\n'
                       '## Why this matters\n'
                       'Separate evaluation roles and choose cross-validation consistent with the '
                       'sampling process. This lesson focuses on **k-fold cross-validation** so '
                       'you can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Each fold is held out once for validation and used for training in the '
                       'other k-1 rounds; aggregate scores and inspect spread.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Five-fold CV creates five fitted models for five validation measurements. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Run cross_val_score and report mean and individual fold scores. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Fold-score variability is not a guarantee of future performance bounds. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.model_selection import cross_val_score\n'
                       'scores = cross_val_score(model, X_train, y_train, cv=5)\n'
                       'print(scores, scores.mean())\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **k-fold cross-validation** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Each fold is held out once for validation and used '
                       'for training in the other k-1 rounds; aggregate scores and inspect '
                       'spread.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'k-Fold Cross-Validation — hands-on activity',
                'description': 'Run cross_val_score and report mean and individual fold scores. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-15']},
               {'title': 'k-Fold Cross-Validation — critical reasoning',
                'description': 'Consider this boundary: Fold-score variability is not a guarantee '
                               'of future performance bounds. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'k-Fold Cross-Validation — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of k-Fold '
                                     'Cross-Validation?',
                         'options': ['The final test set is appropriate for repeated tuning.',
                                     'Each fold is held out once for validation and used for '
                                     'training in the other k-1 rounds; aggregate scores and '
                                     'inspect spread.',
                                     'Stratification prevents all forms of leakage.',
                                     'Group identity can be ignored when rows are correlated.'],
                         'correct': 1,
                         'explanation': 'Each fold is held out once for validation and used for '
                                        'training in the other k-1 rounds; aggregate scores and '
                                        'inspect spread. In the worked scenario: Five-fold CV '
                                        'creates five fitted models for five validation '
                                        'measurements.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'k-Fold Cross-Validation?',
                         'options': ['Draw data-flow boundaries for training, tuning and final '
                                     'reporting.',
                                     'Choose a splitter for a small imbalanced dataset and justify '
                                     'it.',
                                     'Audit overlap of group IDs across folds and document the '
                                     'constraint.',
                                     'Run cross_val_score and report mean and individual fold '
                                     'scores.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Run cross_val_score and report '
                                        'mean and individual fold scores.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Fold-score variability is not a '
                                     'guarantee of future performance bounds.',
                         'type': 'open'}],
          'passing_score': 70}}
