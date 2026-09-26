"""M03.L01 — Ordinary Least Squares Regression.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 45–48. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M03.L01"
MODULE_ORDER = 3
MODULE_TITLE = 'Linear & Probabilistic Models'
MODULE_DESCRIPTION = 'Understand linear predictions, regularization, probabilistic baselines and multiclass decision rules.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '45–48'

TOPIC = {'title': 'Ordinary Least Squares Regression',
 'slug': 'ml-foundations-m03-l01',
 'description': 'Linear regression chooses coefficients and an intercept that minimize squared '
                'prediction error on training examples.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-03'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Ordinary Least Squares Regression',
            'content': '# Ordinary Least Squares Regression\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M03.L01 | '
                       '**Module:** Linear & Probabilistic Models\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 45–48. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Linear regression chooses coefficients and an intercept that '
                       'minimize squared prediction error on training examples.\n'
                       '- Apply the principle to: A two-feature model adds weighted area and '
                       'room-count contributions to an estimated price.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit '
                       'LinearRegression and explain one coefficient while holding other features '
                       'fixed.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand linear predictions, regularization, probabilistic baselines and '
                       'multiclass decision rules. This lesson focuses on **ordinary least squares '
                       'regression** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Linear regression chooses coefficients and an intercept that minimize '
                       'squared prediction error on training examples.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A two-feature model adds weighted area and room-count contributions to an '
                       'estimated price. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit LinearRegression and explain one coefficient while holding other '
                       'features fixed. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Correlation or a learned coefficient does not establish causality. Explain '
                       'how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.linear_model import LinearRegression\n'
                       'regressor = LinearRegression()\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **ordinary least squares regression** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Linear regression chooses coefficients and an '
                       'intercept that minimize squared prediction error on training examples.\n',
            'estimated_minutes': 35,
            'has_code_examples': True},
 'exercises': [{'title': 'Ordinary Least Squares Regression — hands-on activity',
                'description': 'Fit LinearRegression and explain one coefficient while holding '
                               'other features fixed. Deliver a short notebook, annotated example '
                               'or written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-03']},
               {'title': 'Ordinary Least Squares Regression — critical reasoning',
                'description': 'Consider this boundary: Correlation or a learned coefficient does '
                               'not establish causality. Explain a failure mode if it is ignored '
                               'and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Ordinary Least Squares Regression — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Ordinary Least Squares Regression?',
                         'options': ['Linear regression chooses coefficients and an intercept that '
                                     'minimize squared prediction error on training examples.',
                                     'Regularization controls only the size of the dataset.',
                                     'All linear-classifier scores are calibrated probabilities.',
                                     'Learned coefficients establish causal relationships.'],
                         'correct': 0,
                         'explanation': 'Linear regression chooses coefficients and an intercept '
                                        'that minimize squared prediction error on training '
                                        'examples. In the worked scenario: A two-feature model '
                                        'adds weighted area and room-count contributions to an '
                                        'estimated price.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Ordinary Least Squares Regression?',
                         'options': ['Compare coefficient patterns and held-out error for several '
                                     'alpha values.',
                                     'Train logistic regression and linear SVM on scaled training '
                                     'data and compare boundaries.',
                                     'Fit LinearRegression and explain one coefficient while '
                                     'holding other features fixed.',
                                     'Check classes_ and explain how a predicted label relates to '
                                     'scores.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Fit LinearRegression and '
                                        'explain one coefficient while holding other features '
                                        'fixed.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Correlation or a learned coefficient '
                                     'does not establish causality.',
                         'type': 'open'}],
          'passing_score': 70}}
