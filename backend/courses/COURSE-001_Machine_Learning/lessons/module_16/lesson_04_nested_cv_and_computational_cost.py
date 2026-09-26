"""M16.L04 — Nested CV and Computational Cost.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 272–275. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M16.L04"
MODULE_ORDER = 16
MODULE_TITLE = 'Hyperparameter Optimization'
MODULE_DESCRIPTION = 'Tune models reproducibly and distinguish inner model search from independent assessment.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '272–275'

TOPIC = {'title': 'Nested CV and Computational Cost',
 'slug': 'ml-foundations-m16-l04',
 'description': 'Nested CV uses inner folds to select hyperparameters and outer folds to assess '
                'selection procedures; monitor fit counts and resources.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-16'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Nested CV and Computational Cost',
            'content': '# Nested CV and Computational Cost\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M16.L04 | '
                       '**Module:** Hyperparameter Optimization\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 272–275. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Nested CV uses inner folds to select hyperparameters and outer '
                       'folds to assess selection procedures; monitor fit counts and resources.\n'
                       '- Apply the principle to: Outer fold A tunes only on outer training data '
                       'before measuring outer validation performance.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Draw '
                       'inner/outer index ownership and estimate number of model fits.\n'
                       '\n'
                       '## Why this matters\n'
                       'Tune models reproducibly and distinguish inner model search from '
                       'independent assessment. This lesson focuses on **nested cv and '
                       'computational cost** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Nested CV uses inner folds to select hyperparameters and outer folds to '
                       'assess selection procedures; monitor fit counts and resources.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Outer fold A tunes only on outer training data before measuring outer '
                       'validation performance. Before claiming that a method works, check what '
                       'data it uses, which predictions or patterns it produces, and how those '
                       'outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Draw inner/outer index ownership and estimate number of model fits. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not apply inner fold indices directly to the full dataset in a '
                       'hand-written nested loop. Explain how your method respects this boundary '
                       'or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **nested cv and computational cost** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Nested CV uses inner folds to select hyperparameters '
                       'and outer folds to assess selection procedures; monitor fit counts and '
                       'resources.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'Nested CV and Computational Cost — hands-on activity',
                'description': 'Draw inner/outer index ownership and estimate number of model '
                               'fits. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-16']},
               {'title': 'Nested CV and Computational Cost — critical reasoning',
                'description': 'Consider this boundary: Do not apply inner fold indices directly '
                               'to the full dataset in a hand-written nested loop. Explain a '
                               'failure mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Nested CV and Computational Cost — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Nested '
                                     'CV and Computational Cost?',
                         'options': ['Nested CV uses inner folds to select hyperparameters and '
                                     'outer folds to assess selection procedures; monitor fit '
                                     'counts and resources.',
                                     'The maximum cross-validation score is an independent test '
                                     'estimate.',
                                     'Nested validation permits inner folds to include outer '
                                     'validation rows.',
                                     'Search size never affects resource use.'],
                         'correct': 0,
                         'explanation': 'Nested CV uses inner folds to select hyperparameters and '
                                        'outer folds to assess selection procedures; monitor fit '
                                        'counts and resources. In the worked scenario: Outer fold '
                                        'A tunes only on outer training data before measuring '
                                        'outer validation performance.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Nested CV and Computational Cost?',
                         'options': ['Design a parameter search using CV without viewing test '
                                     'outcomes.',
                                     'Run a compact search and interpret its selected '
                                     'configuration.',
                                     'Draw inner/outer index ownership and estimate number of '
                                     'model fits.',
                                     'Create separate search-grid dictionaries and a mean-score '
                                     'comparison table.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Draw inner/outer index '
                                        'ownership and estimate number of model fits.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not apply inner fold indices '
                                     'directly to the full dataset in a hand-written nested loop.',
                         'type': 'open'}],
          'passing_score': 70}}
