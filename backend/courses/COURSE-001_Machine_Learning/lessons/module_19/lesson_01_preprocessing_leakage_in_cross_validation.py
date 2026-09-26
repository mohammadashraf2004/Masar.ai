"""M19.L01 — Preprocessing Leakage in Cross-Validation.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 6, pages 305–307. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M19.L01"
MODULE_ORDER = 19
MODULE_TITLE = 'Machine Learning Pipelines'
MODULE_DESCRIPTION = 'Combine all fitted transformations with models inside robust selection and evaluation workflows.'
SOURCE_CHAPTER = 6
SOURCE_PAGES = '305–307'

TOPIC = {'title': 'Preprocessing Leakage in Cross-Validation',
 'slug': 'ml-foundations-m19-l01',
 'description': 'Preprocessing before CV reveals validation fold statistics to model development; '
                'validation must surround every data-dependent fitting step.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-19'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Preprocessing Leakage in Cross-Validation',
            'content': '# Preprocessing Leakage in Cross-Validation\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M19.L01 | '
                       '**Module:** Machine Learning Pipelines\n'
                       '> **Source alignment:** BOOK-001, Chapter 6, pages 305–307. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Preprocessing before CV reveals validation fold statistics to '
                       'model development; validation must surround every data-dependent fitting '
                       'step.\n'
                       '- Apply the principle to: MinMaxScaler fitted on all development rows can '
                       'use validation minima and maxima.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Illustrate which rows a scaler sees in one five-fold iteration.\n'
                       '\n'
                       '## Why this matters\n'
                       'Combine all fitted transformations with models inside robust selection and '
                       'evaluation workflows. This lesson focuses on **preprocessing leakage in '
                       'cross-validation** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Preprocessing before CV reveals validation fold statistics to model '
                       'development; validation must surround every data-dependent fitting step.\n'
                       '\n'
                       '## Worked scenario\n'
                       'MinMaxScaler fitted on all development rows can use validation minima and '
                       'maxima. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Illustrate which rows a scaler sees in one five-fold iteration. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A separate final test set does not repair leakage inside CV. Explain how '
                       'your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **preprocessing leakage in cross-validation** in your own words '
                       'and answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Preprocessing before CV reveals validation fold '
                       'statistics to model development; validation must surround every '
                       'data-dependent fitting step.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Preprocessing Leakage in Cross-Validation — hands-on activity',
                'description': 'Illustrate which rows a scaler sees in one five-fold iteration. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-19']},
               {'title': 'Preprocessing Leakage in Cross-Validation — critical reasoning',
                'description': 'Consider this boundary: A separate final test set does not repair '
                               'leakage inside CV. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Preprocessing Leakage in Cross-Validation — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Preprocessing Leakage in Cross-Validation?',
                         'options': ['Preprocessing before CV reveals validation fold statistics '
                                     'to model development; validation must surround every '
                                     'data-dependent fitting step.',
                                     'All fitted preprocessing should happen before '
                                     'cross-validation.',
                                     'A pipeline makes group and time leakage impossible '
                                     'automatically.',
                                     'Search parameters do not need to identify their pipeline '
                                     'step.'],
                         'correct': 0,
                         'explanation': 'Preprocessing before CV reveals validation fold '
                                        'statistics to model development; validation must surround '
                                        'every data-dependent fitting step. In the worked '
                                        'scenario: MinMaxScaler fitted on all development rows can '
                                        'use validation minima and maxima.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Preprocessing Leakage in Cross-Validation?',
                         'options': ['Build and grid-search an SVC pipeline on raw training '
                                     'features.',
                                     'Write a reproducible paired experiment and explain why the '
                                     'two setups differ.',
                                     'Illustrate which rows a scaler sees in one five-fold '
                                     'iteration.',
                                     'Build explicit and automatically named pipelines and inspect '
                                     'steps.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Illustrate which rows a scaler '
                                        'sees in one five-fold iteration.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A separate final test set does not '
                                     'repair leakage inside CV.',
                         'type': 'open'}],
          'passing_score': 70}}
