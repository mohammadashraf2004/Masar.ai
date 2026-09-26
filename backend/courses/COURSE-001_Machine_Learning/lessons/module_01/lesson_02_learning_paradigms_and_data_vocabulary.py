"""M01.L02 — Learning Paradigms and Data Vocabulary.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 1, pages 2–6. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L02"
MODULE_ORDER = 1
MODULE_TITLE = 'ML Fundamentals & First Model'
MODULE_DESCRIPTION = 'Frame a supervised problem and train the first reproducible iris classifier.'
SOURCE_CHAPTER = 1
SOURCE_PAGES = '2–6'

TOPIC = {'title': 'Learning Paradigms and Data Vocabulary',
 'slug': 'ml-foundations-m01-l02',
 'description': 'Supervised tasks have labeled examples; unsupervised tasks search for structure '
                'without known targets. Samples are rows and features are columns.',
 'order': 2,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-01'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Learning Paradigms and Data Vocabulary',
            'content': '# Learning Paradigms and Data Vocabulary\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M01.L02 | '
                       '**Module:** ML Fundamentals & First Model\n'
                       '> **Source alignment:** BOOK-001, Chapter 1, pages 2–6. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Supervised tasks have labeled examples; unsupervised tasks '
                       'search for structure without known targets. Samples are rows and features '
                       'are columns.\n'
                       '- Apply the principle to: Spam classification uses labeled messages; '
                       'customer grouping starts without predefined groups.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Classify three scenarios and sketch X and y for each.\n'
                       '\n'
                       '## Why this matters\n'
                       'Frame a supervised problem and train the first reproducible iris '
                       'classifier. This lesson focuses on **learning paradigms and data '
                       'vocabulary** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Supervised tasks have labeled examples; unsupervised tasks search for '
                       'structure without known targets. Samples are rows and features are '
                       'columns.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Spam classification uses labeled messages; customer grouping starts '
                       'without predefined groups. Before claiming that a method works, check what '
                       'data it uses, which predictions or patterns it produces, and how those '
                       'outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Classify three scenarios and sketch X and y for each. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not mistake a clustering group for an established ground-truth class. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **learning paradigms and data vocabulary** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Supervised tasks have labeled examples; unsupervised '
                       'tasks search for structure without known targets. Samples are rows and '
                       'features are columns.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Learning Paradigms and Data Vocabulary — hands-on activity',
                'description': 'Classify three scenarios and sketch X and y for each. Deliver a '
                               'short notebook, annotated example or written calculation with your '
                               'result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-01']},
               {'title': 'Learning Paradigms and Data Vocabulary — critical reasoning',
                'description': 'Consider this boundary: Do not mistake a clustering group for an '
                               'established ground-truth class. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Learning Paradigms and Data Vocabulary — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Learning Paradigms and Data Vocabulary?',
                         'options': ['Only handcrafted rules can make a useful prediction.',
                                     'A perfect training score guarantees new-data accuracy.',
                                     'Features and labels are interchangeable.',
                                     'Supervised tasks have labeled examples; unsupervised tasks '
                                     'search for structure without known targets. Samples are rows '
                                     'and features are columns.'],
                         'correct': 3,
                         'explanation': 'Supervised tasks have labeled examples; unsupervised '
                                        'tasks search for structure without known targets. Samples '
                                        'are rows and features are columns. In the worked '
                                        'scenario: Spam classification uses labeled messages; '
                                        'customer grouping starts without predefined groups.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Learning Paradigms and Data Vocabulary?',
                         'options': ['Describe a prediction problem with its input, target and '
                                     'intended user.',
                                     'Classify three scenarios and sketch X and y for each.',
                                     "Inspect an array's shape, dataset labels and Python package "
                                     'imports.',
                                     'Load Iris, report the feature names and identify its three '
                                     'classes.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Classify three scenarios and '
                                        'sketch X and y for each.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not mistake a clustering group for '
                                     'an established ground-truth class.',
                         'type': 'open'}],
          'passing_score': 70}}
