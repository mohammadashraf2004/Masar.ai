"""M01.L01 — What Is Machine Learning?.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 1, pages 1–4. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L01"
MODULE_ORDER = 1
MODULE_TITLE = 'ML Fundamentals & First Model'
MODULE_DESCRIPTION = 'Frame a supervised problem and train the first reproducible iris classifier.'
SOURCE_CHAPTER = 1
SOURCE_PAGES = '1–4'

TOPIC = {'title': 'What Is Machine Learning?',
 'slug': 'ml-foundations-m01-l01',
 'description': 'Machine learning learns patterns from examples instead of relying only on '
                'hand-written decision rules; define inputs, outputs and available evidence.',
 'order': 1,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.4167,
 'skill_tags': ['machine-learning', 'foundations', 'module-01'],
 'prerequisite_ids': [],
 'lesson': {'title': 'What Is Machine Learning?',
            'content': '# What Is Machine Learning?\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M01.L01 | '
                       '**Module:** ML Fundamentals & First Model\n'
                       '> **Source alignment:** BOOK-001, Chapter 1, pages 1–4. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Machine learning learns patterns from examples instead of '
                       'relying only on hand-written decision rules; define inputs, outputs and '
                       'available evidence.\n'
                       '- Apply the principle to: An iris model uses measured petals and sepals to '
                       'infer an unseen flower species.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Describe a prediction problem with its input, target and intended user.\n'
                       '\n'
                       '## Why this matters\n'
                       'Frame a supervised problem and train the first reproducible iris '
                       'classifier. This lesson focuses on **what is machine learning?** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Machine learning learns patterns from examples instead of relying only on '
                       'hand-written decision rules; define inputs, outputs and available '
                       'evidence.\n'
                       '\n'
                       '## Worked scenario\n'
                       'An iris model uses measured petals and sepals to infer an unseen flower '
                       'species. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Describe a prediction problem with its input, target and intended user. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A complex algorithm cannot recover a target that the available features '
                       'cannot reveal. Explain how your method respects this boundary or avoids '
                       'the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **what is machine learning?** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Machine learning learns patterns from examples '
                       'instead of relying only on hand-written decision rules; define inputs, '
                       'outputs and available evidence.\n',
            'estimated_minutes': 25,
            'has_code_examples': False},
 'exercises': [{'title': 'What Is Machine Learning? — hands-on activity',
                'description': 'Describe a prediction problem with its input, target and intended '
                               'user. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-01']},
               {'title': 'What Is Machine Learning? — critical reasoning',
                'description': 'Consider this boundary: A complex algorithm cannot recover a '
                               'target that the available features cannot reveal. Explain a '
                               'failure mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'What Is Machine Learning? — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of What Is '
                                     'Machine Learning?',
                         'options': ['Only handcrafted rules can make a useful prediction.',
                                     'A perfect training score guarantees new-data accuracy.',
                                     'Machine learning learns patterns from examples instead of '
                                     'relying only on hand-written decision rules; define inputs, '
                                     'outputs and available evidence.',
                                     'Features and labels are interchangeable.'],
                         'correct': 2,
                         'explanation': 'Machine learning learns patterns from examples instead of '
                                        'relying only on hand-written decision rules; define '
                                        'inputs, outputs and available evidence. In the worked '
                                        'scenario: An iris model uses measured petals and sepals '
                                        'to infer an unseen flower species.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'What Is Machine Learning?',
                         'options': ['Describe a prediction problem with its input, target and '
                                     'intended user.',
                                     'Classify three scenarios and sketch X and y for each.',
                                     "Inspect an array's shape, dataset labels and Python package "
                                     'imports.',
                                     'Load Iris, report the feature names and identify its three '
                                     'classes.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Describe a prediction problem '
                                        'with its input, target and intended user.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A complex algorithm cannot recover a '
                                     'target that the available features cannot reveal.',
                         'type': 'open'}],
          'passing_score': 70}}
