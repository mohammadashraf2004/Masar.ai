"""M07.L03 — Fit and Transform Without Leakage.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 134–138. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M07.L03"
MODULE_ORDER = 7
MODULE_TITLE = 'Unsupervised Learning & Preprocessing'
MODULE_DESCRIPTION = 'Learn transformer behavior and how data leakage affects scaled unsupervised representations.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '134–138'

TOPIC = {'title': 'Fit and Transform Without Leakage',
 'slug': 'ml-foundations-m07-l03',
 'description': 'Fit preprocessing on training observations only, then reuse fitted parameters on '
                'validation and test inputs.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-07'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Fit and Transform Without Leakage',
            'content': '# Fit and Transform Without Leakage\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M07.L03 | '
                       '**Module:** Unsupervised Learning & Preprocessing\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 134–138. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Fit preprocessing on training observations only, then reuse '
                       'fitted parameters on validation and test inputs.\n'
                       '- Apply the principle to: The test maximum must not influence the scaler '
                       'used to train a classifier.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Demonstrate train-fit then test-transform and identify leaked alternative '
                       'code.\n'
                       '\n'
                       '## Why this matters\n'
                       'Learn transformer behavior and how data leakage affects scaled '
                       'unsupervised representations. This lesson focuses on **fit and transform '
                       'without leakage** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Fit preprocessing on training observations only, then reuse fitted '
                       'parameters on validation and test inputs.\n'
                       '\n'
                       '## Worked scenario\n'
                       'The test maximum must not influence the scaler used to train a classifier. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Demonstrate train-fit then test-transform and identify leaked alternative '
                       'code. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Never call fit_transform independently on the test set. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'scaler.fit(X_train)  # learn training-only statistics\n'
                       'X_train_scaled = scaler.transform(X_train)\n'
                       'X_test_scaled = scaler.transform(X_test)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **fit and transform without leakage** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Fit preprocessing on training observations only, '
                       'then reuse fitted parameters on validation and test inputs.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Fit and Transform Without Leakage — hands-on activity',
                'description': 'Demonstrate train-fit then test-transform and identify leaked '
                               'alternative code. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-07']},
               {'title': 'Fit and Transform Without Leakage — critical reasoning',
                'description': 'Consider this boundary: Never call fit_transform independently on '
                               'the test set. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Fit and Transform Without Leakage — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Fit and '
                                     'Transform Without Leakage?',
                         'options': ['It is safe to fit scalers on the test set.',
                                     'Unsupervised methods require a supervised target.',
                                     'Fit preprocessing on training observations only, then reuse '
                                     'fitted parameters on validation and test inputs.',
                                     'All scaling methods guarantee that future values stay within '
                                     'training bounds.'],
                         'correct': 2,
                         'explanation': 'Fit preprocessing on training observations only, then '
                                        'reuse fitted parameters on validation and test inputs. In '
                                        'the worked scenario: The test maximum must not influence '
                                        'the scaler used to train a classifier.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Fit and Transform Without Leakage?',
                         'options': ['Demonstrate train-fit then test-transform and identify '
                                     'leaked alternative code.',
                                     'Differentiate clustering, dimensionality reduction and '
                                     'preprocessing in three cases.',
                                     'Scale a small numeric array using two methods and inspect '
                                     'resulting distributions.',
                                     'Compare a scaled versus unscaled SVM using a held-out '
                                     'development split.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Demonstrate train-fit then '
                                        'test-transform and identify leaked alternative code.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Never call fit_transform independently '
                                     'on the test set.',
                         'type': 'open'}],
          'passing_score': 70}}
