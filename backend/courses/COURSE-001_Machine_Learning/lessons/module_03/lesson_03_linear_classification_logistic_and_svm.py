"""M03.L03 — Linear Classification: Logistic and SVM.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 54–61. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M03.L03"
MODULE_ORDER = 3
MODULE_TITLE = 'Linear & Probabilistic Models'
MODULE_DESCRIPTION = 'Understand linear predictions, regularization, probabilistic baselines and multiclass decision rules.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '54–61'

TOPIC = {'title': 'Linear Classification: Logistic and SVM',
 'slug': 'ml-foundations-m03-l03',
 'description': 'Linear classifiers learn a weighted decision boundary; logistic regression can '
                'provide class probabilities, while linear SVM produces decision scores.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-03'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Linear Classification: Logistic and SVM',
            'content': '# Linear Classification: Logistic and SVM\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M03.L03 | '
                       '**Module:** Linear & Probabilistic Models\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 54–61. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Linear classifiers learn a weighted decision boundary; logistic '
                       'regression can provide class probabilities, while linear SVM produces '
                       'decision scores.\n'
                       '- Apply the principle to: In two dimensions the boundary separates the '
                       'plane with a straight line.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Train '
                       'logistic regression and linear SVM on scaled training data and compare '
                       'boundaries.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand linear predictions, regularization, probabilistic baselines and '
                       'multiclass decision rules. This lesson focuses on **linear classification: '
                       'logistic and svm** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Linear classifiers learn a weighted decision boundary; logistic regression '
                       'can provide class probabilities, while linear SVM produces decision '
                       'scores.\n'
                       '\n'
                       '## Worked scenario\n'
                       'In two dimensions the boundary separates the plane with a straight line. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Train logistic regression and linear SVM on scaled training data and '
                       'compare boundaries. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Logistic regression is a classifier despite its name. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.linear_model import LogisticRegression\n'
                       'classifier = LogisticRegression(max_iter=1000)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **linear classification: logistic and svm** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Linear classifiers learn a weighted decision '
                       'boundary; logistic regression can provide class probabilities, while '
                       'linear SVM produces decision scores.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Linear Classification: Logistic and SVM — hands-on activity',
                'description': 'Train logistic regression and linear SVM on scaled training data '
                               'and compare boundaries. Deliver a short notebook, annotated '
                               'example or written calculation with your result and '
                               'interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-03']},
               {'title': 'Linear Classification: Logistic and SVM — critical reasoning',
                'description': 'Consider this boundary: Logistic regression is a classifier '
                               'despite its name. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Linear Classification: Logistic and SVM — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Linear '
                                     'Classification: Logistic and SVM?',
                         'options': ['Regularization controls only the size of the dataset.',
                                     'All linear-classifier scores are calibrated probabilities.',
                                     'Linear classifiers learn a weighted decision boundary; '
                                     'logistic regression can provide class probabilities, while '
                                     'linear SVM produces decision scores.',
                                     'Learned coefficients establish causal relationships.'],
                         'correct': 2,
                         'explanation': 'Linear classifiers learn a weighted decision boundary; '
                                        'logistic regression can provide class probabilities, '
                                        'while linear SVM produces decision scores. In the worked '
                                        'scenario: In two dimensions the boundary separates the '
                                        'plane with a straight line.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Linear Classification: Logistic and SVM?',
                         'options': ['Train logistic regression and linear SVM on scaled training '
                                     'data and compare boundaries.',
                                     'Fit LinearRegression and explain one coefficient while '
                                     'holding other features fixed.',
                                     'Compare coefficient patterns and held-out error for several '
                                     'alpha values.',
                                     'Check classes_ and explain how a predicted label relates to '
                                     'scores.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Train logistic regression and '
                                        'linear SVM on scaled training data and compare '
                                        'boundaries.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Logistic regression is a classifier '
                                     'despite its name.',
                         'type': 'open'}],
          'passing_score': 70}}
