"""M01.L03 — Python Machine Learning Toolchain.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 1, pages 6–13. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L03"
MODULE_ORDER = 1
MODULE_TITLE = 'ML Fundamentals & First Model'
MODULE_DESCRIPTION = 'Frame a supervised problem and train the first reproducible iris classifier.'
SOURCE_CHAPTER = 1
SOURCE_PAGES = '6–13'

TOPIC = {'title': 'Python Machine Learning Toolchain',
 'slug': 'ml-foundations-m01-l03',
 'description': 'Use NumPy arrays, pandas tables, matplotlib plots, and scikit-learn estimators '
                'for distinct parts of a workflow.',
 'order': 3,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.5,
 'skill_tags': ['machine-learning', 'foundations', 'module-01'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Python Machine Learning Toolchain',
            'content': '# Python Machine Learning Toolchain\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M01.L03 | '
                       '**Module:** ML Fundamentals & First Model\n'
                       '> **Source alignment:** BOOK-001, Chapter 1, pages 6–13. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Use NumPy arrays, pandas tables, matplotlib plots, and '
                       'scikit-learn estimators for distinct parts of a workflow.\n'
                       '- Apply the principle to: Check X.shape before fitting and plot '
                       'distributions to detect unusual feature ranges.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       "Inspect an array's shape, dataset labels and Python package imports.\n"
                       '\n'
                       '## Why this matters\n'
                       'Frame a supervised problem and train the first reproducible iris '
                       'classifier. This lesson focuses on **python machine learning toolchain** '
                       'so you can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Use NumPy arrays, pandas tables, matplotlib plots, and scikit-learn '
                       'estimators for distinct parts of a workflow.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Check X.shape before fitting and plot distributions to detect unusual '
                       'feature ranges. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       "Inspect an array's shape, dataset labels and Python package imports. "
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not treat the historic version numbers printed in the book as '
                       'installation instructions. Explain how your method respects this boundary '
                       'or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **python machine learning toolchain** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Use NumPy arrays, pandas tables, matplotlib plots, '
                       'and scikit-learn estimators for distinct parts of a workflow.\n',
            'estimated_minutes': 30,
            'has_code_examples': False},
 'exercises': [{'title': 'Python Machine Learning Toolchain — hands-on activity',
                'description': "Inspect an array's shape, dataset labels and Python package "
                               'imports. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-01']},
               {'title': 'Python Machine Learning Toolchain — critical reasoning',
                'description': 'Consider this boundary: Do not treat the historic version numbers '
                               'printed in the book as installation instructions. Explain a '
                               'failure mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Python Machine Learning Toolchain — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Python '
                                     'Machine Learning Toolchain?',
                         'options': ['Use NumPy arrays, pandas tables, matplotlib plots, and '
                                     'scikit-learn estimators for distinct parts of a workflow.',
                                     'Only handcrafted rules can make a useful prediction.',
                                     'A perfect training score guarantees new-data accuracy.',
                                     'Features and labels are interchangeable.'],
                         'correct': 0,
                         'explanation': 'Use NumPy arrays, pandas tables, matplotlib plots, and '
                                        'scikit-learn estimators for distinct parts of a workflow. '
                                        'In the worked scenario: Check X.shape before fitting and '
                                        'plot distributions to detect unusual feature ranges.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Python Machine Learning Toolchain?',
                         'options': ['Describe a prediction problem with its input, target and '
                                     'intended user.',
                                     'Classify three scenarios and sketch X and y for each.',
                                     "Inspect an array's shape, dataset labels and Python package "
                                     'imports.',
                                     'Load Iris, report the feature names and identify its three '
                                     'classes.'],
                         'correct': 2,
                         'explanation': "The intended practice is: Inspect an array's shape, "
                                        'dataset labels and Python package imports.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not treat the historic version '
                                     'numbers printed in the book as installation instructions.',
                         'type': 'open'}],
          'passing_score': 70}}
