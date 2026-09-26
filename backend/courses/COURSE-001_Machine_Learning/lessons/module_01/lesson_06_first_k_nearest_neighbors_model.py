"""M01.L06 — First k-Nearest Neighbors Model.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 1, pages 20–24. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L06"
MODULE_ORDER = 1
MODULE_TITLE = 'ML Fundamentals & First Model'
MODULE_DESCRIPTION = 'Frame a supervised problem and train the first reproducible iris classifier.'
SOURCE_CHAPTER = 1
SOURCE_PAGES = '20–24'

TOPIC = {'title': 'First k-Nearest Neighbors Model',
 'slug': 'ml-foundations-m01-l06',
 'description': 'kNN predicts from nearby labeled examples; call fit on training data and score on '
                'untouched test observations.',
 'order': 6,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-01'],
 'prerequisite_ids': [],
 'lesson': {'title': 'First k-Nearest Neighbors Model',
            'content': '# First k-Nearest Neighbors Model\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M01.L06 | '
                       '**Module:** ML Fundamentals & First Model\n'
                       '> **Source alignment:** BOOK-001, Chapter 1, pages 20–24. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: kNN predicts from nearby labeled examples; call fit on training '
                       'data and score on untouched test observations.\n'
                       '- Apply the principle to: A new iris is assigned the class preferred by '
                       'its k closest measured training flowers.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit '
                       'KNeighborsClassifier, predict a few examples and calculate test accuracy.\n'
                       '\n'
                       '## Why this matters\n'
                       'Frame a supervised problem and train the first reproducible iris '
                       'classifier. This lesson focuses on **first k-nearest neighbors model** so '
                       'you can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'kNN predicts from nearby labeled examples; call fit on training data and '
                       'score on untouched test observations.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A new iris is assigned the class preferred by its k closest measured '
                       'training flowers. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit KNeighborsClassifier, predict a few examples and calculate test '
                       'accuracy. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Accuracy on training examples is not an independent estimate of '
                       'performance. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.neighbors import KNeighborsClassifier\n'
                       'model = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)\n'
                       'print(model.score(X_test, y_test))\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **first k-nearest neighbors model** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** kNN predicts from nearby labeled examples; call fit '
                       'on training data and score on untouched test observations.\n',
            'estimated_minutes': 35,
            'has_code_examples': True},
 'exercises': [{'title': 'First k-Nearest Neighbors Model — hands-on activity',
                'description': 'Fit KNeighborsClassifier, predict a few examples and calculate '
                               'test accuracy. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-01']},
               {'title': 'First k-Nearest Neighbors Model — critical reasoning',
                'description': 'Consider this boundary: Accuracy on training examples is not an '
                               'independent estimate of performance. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'First k-Nearest Neighbors Model — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of First '
                                     'k-Nearest Neighbors Model?',
                         'options': ['Only handcrafted rules can make a useful prediction.',
                                     'A perfect training score guarantees new-data accuracy.',
                                     'Features and labels are interchangeable.',
                                     'kNN predicts from nearby labeled examples; call fit on '
                                     'training data and score on untouched test observations.'],
                         'correct': 3,
                         'explanation': 'kNN predicts from nearby labeled examples; call fit on '
                                        'training data and score on untouched test observations. '
                                        'In the worked scenario: A new iris is assigned the class '
                                        'preferred by its k closest measured training flowers.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'First k-Nearest Neighbors Model?',
                         'options': ['Describe a prediction problem with its input, target and '
                                     'intended user.',
                                     'Fit KNeighborsClassifier, predict a few examples and '
                                     'calculate test accuracy.',
                                     'Classify three scenarios and sketch X and y for each.',
                                     "Inspect an array's shape, dataset labels and Python package "
                                     'imports.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Fit KNeighborsClassifier, '
                                        'predict a few examples and calculate test accuracy.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Accuracy on training examples is not '
                                     'an independent estimate of performance.',
                         'type': 'open'}],
          'passing_score': 70},
 'project': {'title': 'First Iris Model',
             'description': 'Build a small iris classifier with inspectable splits, training, '
                            'predictions and a test report.',
             'difficulty': DifficultyLevel.beginner,
             'tech_stack': ['Python', 'NumPy', 'scikit-learn', 'Jupyter'],
             'objectives': ['State the problem and data assumptions.',
                            'Implement a reproducible baseline and improved workflow.',
                            'Validate honestly and interpret both strengths and limitations.'],
             'rubric': {'problem_definition': 20,
                        'reproducibility': 25,
                        'evaluation_integrity': 30,
                        'interpretation': 25},
             'starter_repo_url': None,
             'estimated_hours': 3.0}}
