"""M01.L04 — Iris Classification Problem.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 1, pages 13–18. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L04"
MODULE_ORDER = 1
MODULE_TITLE = 'ML Fundamentals & First Model'
MODULE_DESCRIPTION = 'Frame a supervised problem and train the first reproducible iris classifier.'
SOURCE_CHAPTER = 1
SOURCE_PAGES = '13–18'

TOPIC = {'title': 'Iris Classification Problem',
 'slug': 'ml-foundations-m01-l04',
 'description': 'The iris task predicts a species from four flower measurements; identify dataset '
                'fields and a clearly held-out test subset.',
 'order': 4,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.5,
 'skill_tags': ['machine-learning', 'foundations', 'module-01'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Iris Classification Problem',
            'content': '# Iris Classification Problem\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M01.L04 | '
                       '**Module:** ML Fundamentals & First Model\n'
                       '> **Source alignment:** BOOK-001, Chapter 1, pages 13–18. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: The iris task predicts a species from four flower measurements; '
                       'identify dataset fields and a clearly held-out test subset.\n'
                       '- Apply the principle to: A row of four measurements is one sample, not '
                       'four separate samples.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Load '
                       'Iris, report the feature names and identify its three classes.\n'
                       '\n'
                       '## Why this matters\n'
                       'Frame a supervised problem and train the first reproducible iris '
                       'classifier. This lesson focuses on **iris classification problem** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'The iris task predicts a species from four flower measurements; identify '
                       'dataset fields and a clearly held-out test subset.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A row of four measurements is one sample, not four separate samples. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Load Iris, report the feature names and identify its three classes. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Never use test labels when fitting the classifier. Explain how your method '
                       'respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.datasets import load_iris\n'
                       'X, y = load_iris(return_X_y=True)\n'
                       'print(X.shape, y.shape)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **iris classification problem** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** The iris task predicts a species from four flower '
                       'measurements; identify dataset fields and a clearly held-out test '
                       'subset.\n',
            'estimated_minutes': 30,
            'has_code_examples': True},
 'exercises': [{'title': 'Iris Classification Problem — hands-on activity',
                'description': 'Load Iris, report the feature names and identify its three '
                               'classes. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-01']},
               {'title': 'Iris Classification Problem — critical reasoning',
                'description': 'Consider this boundary: Never use test labels when fitting the '
                               'classifier. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Iris Classification Problem — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Iris '
                                     'Classification Problem?',
                         'options': ['Only handcrafted rules can make a useful prediction.',
                                     'The iris task predicts a species from four flower '
                                     'measurements; identify dataset fields and a clearly held-out '
                                     'test subset.',
                                     'A perfect training score guarantees new-data accuracy.',
                                     'Features and labels are interchangeable.'],
                         'correct': 1,
                         'explanation': 'The iris task predicts a species from four flower '
                                        'measurements; identify dataset fields and a clearly '
                                        'held-out test subset. In the worked scenario: A row of '
                                        'four measurements is one sample, not four separate '
                                        'samples.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Iris Classification Problem?',
                         'options': ['Describe a prediction problem with its input, target and '
                                     'intended user.',
                                     'Classify three scenarios and sketch X and y for each.',
                                     "Inspect an array's shape, dataset labels and Python package "
                                     'imports.',
                                     'Load Iris, report the feature names and identify its three '
                                     'classes.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Load Iris, report the feature '
                                        'names and identify its three classes.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Never use test labels when fitting the '
                                     'classifier.',
                         'type': 'open'}],
          'passing_score': 70}}
