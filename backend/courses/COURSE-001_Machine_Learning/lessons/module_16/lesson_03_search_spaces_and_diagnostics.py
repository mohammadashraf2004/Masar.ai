"""M16.L03 — Search Spaces and Diagnostics.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 267–272. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M16.L03"
MODULE_ORDER = 16
MODULE_TITLE = 'Hyperparameter Optimization'
MODULE_DESCRIPTION = 'Tune models reproducibly and distinguish inner model search from independent assessment.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '267–272'

TOPIC = {'title': 'Search Spaces and Diagnostics',
 'slug': 'ml-foundations-m16-l03',
 'description': 'Build valid conditional grids and inspect cv_results_ for ranking, variability '
                'and computational cost.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-16'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Search Spaces and Diagnostics',
            'content': '# Search Spaces and Diagnostics\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M16.L03 | '
                       '**Module:** Hyperparameter Optimization\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 267–272. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Build valid conditional grids and inspect cv_results_ for '
                       'ranking, variability and computational cost.\n'
                       "- Apply the principle to: A polynomial kernel's degree parameter is "
                       'irrelevant to a linear SVM grid.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Create separate search-grid dictionaries and a mean-score comparison '
                       'table.\n'
                       '\n'
                       '## Why this matters\n'
                       'Tune models reproducibly and distinguish inner model search from '
                       'independent assessment. This lesson focuses on **search spaces and '
                       'diagnostics** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Build valid conditional grids and inspect cv_results_ for ranking, '
                       'variability and computational cost.\n'
                       '\n'
                       '## Worked scenario\n'
                       "A polynomial kernel's degree parameter is irrelevant to a linear SVM grid. "
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Create separate search-grid dictionaries and a mean-score comparison '
                       'table. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A Cartesian product may include incompatible parameter combinations. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **search spaces and diagnostics** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Build valid conditional grids and inspect '
                       'cv_results_ for ranking, variability and computational cost.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'Search Spaces and Diagnostics — hands-on activity',
                'description': 'Create separate search-grid dictionaries and a mean-score '
                               'comparison table. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-16']},
               {'title': 'Search Spaces and Diagnostics — critical reasoning',
                'description': 'Consider this boundary: A Cartesian product may include '
                               'incompatible parameter combinations. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Search Spaces and Diagnostics — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Search '
                                     'Spaces and Diagnostics?',
                         'options': ['The maximum cross-validation score is an independent test '
                                     'estimate.',
                                     'Nested validation permits inner folds to include outer '
                                     'validation rows.',
                                     'Search size never affects resource use.',
                                     'Build valid conditional grids and inspect cv_results_ for '
                                     'ranking, variability and computational cost.'],
                         'correct': 3,
                         'explanation': 'Build valid conditional grids and inspect cv_results_ for '
                                        'ranking, variability and computational cost. In the '
                                        "worked scenario: A polynomial kernel's degree parameter "
                                        'is irrelevant to a linear SVM grid.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Search Spaces and Diagnostics?',
                         'options': ['Design a parameter search using CV without viewing test '
                                     'outcomes.',
                                     'Create separate search-grid dictionaries and a mean-score '
                                     'comparison table.',
                                     'Run a compact search and interpret its selected '
                                     'configuration.',
                                     'Draw inner/outer index ownership and estimate number of '
                                     'model fits.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Create separate search-grid '
                                        'dictionaries and a mean-score comparison table.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A Cartesian product may include '
                                     'incompatible parameter combinations.',
                         'type': 'open'}],
          'passing_score': 70}}
