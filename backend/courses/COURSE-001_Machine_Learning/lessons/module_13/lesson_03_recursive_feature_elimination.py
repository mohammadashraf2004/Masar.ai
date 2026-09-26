"""M13.L03 — Recursive Feature Elimination.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 240–241. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M13.L03"
MODULE_ORDER = 13
MODULE_TITLE = 'Automatic Feature Selection'
MODULE_DESCRIPTION = 'Compare feature selection techniques and fit them within the evaluation process.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '240–241'

TOPIC = {'title': 'Recursive Feature Elimination',
 'slug': 'ml-foundations-m13-l03',
 'description': 'RFE repeatedly fits an estimator and prunes features; repeated fitting creates '
                'computation and stability trade-offs.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-13'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Recursive Feature Elimination',
            'content': '# Recursive Feature Elimination\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M13.L03 | '
                       '**Module:** Automatic Feature Selection\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 240–241. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: RFE repeatedly fits an estimator and prunes features; repeated '
                       'fitting creates computation and stability trade-offs.\n'
                       '- Apply the principle to: Start with ten features and iteratively remove '
                       'low-scored variables.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare RFE selections across training folds and compute budget.\n'
                       '\n'
                       '## Why this matters\n'
                       'Compare feature selection techniques and fit them within the evaluation '
                       'process. This lesson focuses on **recursive feature elimination** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'RFE repeatedly fits an estimator and prunes features; repeated fitting '
                       'creates computation and stability trade-offs.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Start with ten features and iteratively remove low-scored variables. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare RFE selections across training folds and compute budget. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A single selected subset is not guaranteed stable across resamples. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.feature_selection import RFE\n'
                       'from sklearn.linear_model import LogisticRegression\n'
                       'selector = RFE(LogisticRegression(max_iter=1000), n_features_to_select=5)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **recursive feature elimination** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** RFE repeatedly fits an estimator and prunes '
                       'features; repeated fitting creates computation and stability trade-offs.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Recursive Feature Elimination — hands-on activity',
                'description': 'Compare RFE selections across training folds and compute budget. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-13']},
               {'title': 'Recursive Feature Elimination — critical reasoning',
                'description': 'Consider this boundary: A single selected subset is not guaranteed '
                               'stable across resamples. Explain a failure mode if it is ignored '
                               'and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Recursive Feature Elimination — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Recursive Feature Elimination?',
                         'options': ['RFE repeatedly fits an estimator and prunes features; '
                                     'repeated fitting creates computation and stability '
                                     'trade-offs.',
                                     'Feature selection may use all targets before '
                                     'cross-validation.',
                                     'Importance rankings are necessarily stable across folds.',
                                     'Repeated feature-elimination fits have no computational '
                                     'cost.'],
                         'correct': 0,
                         'explanation': 'RFE repeatedly fits an estimator and prunes features; '
                                        'repeated fitting creates computation and stability '
                                        'trade-offs. In the worked scenario: Start with ten '
                                        'features and iteratively remove low-scored variables.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Recursive Feature Elimination?',
                         'options': ['Select features within a training fold and record selected '
                                     'names.',
                                     'Inspect feature support after model-based selection in a '
                                     'pipeline.',
                                     'Compare RFE selections across training folds and compute '
                                     'budget.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Compare RFE selections across '
                                        'training folds and compute budget.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A single selected subset is not '
                                     'guaranteed stable across resamples.',
                         'type': 'open'}],
          'passing_score': 70}}
