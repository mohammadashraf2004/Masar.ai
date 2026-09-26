"""M02.L01 — Classification Versus Regression.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 25–29. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M02.L01"
MODULE_ORDER = 2
MODULE_TITLE = 'Supervised Learning & Generalization'
MODULE_DESCRIPTION = 'Distinguish tasks and learn how flexibility, data volume and representation affect generalization.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '25–29'

TOPIC = {'title': 'Classification Versus Regression',
 'slug': 'ml-foundations-m02-l01',
 'description': 'Classification predicts discrete labels and regression predicts numeric '
                'quantities; choose the target type before selecting an estimator.',
 'order': 1,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.5,
 'skill_tags': ['machine-learning', 'foundations', 'module-02'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Classification Versus Regression',
            'content': '# Classification Versus Regression\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M02.L01 | '
                       '**Module:** Supervised Learning & Generalization\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 25–29. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Classification predicts discrete labels and regression predicts '
                       'numeric quantities; choose the target type before selecting an estimator.\n'
                       '- Apply the principle to: Predicting an iris species is classification; '
                       'predicting a house price is regression.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Write '
                       'X, y and a sensible metric for both situations.\n'
                       '\n'
                       '## Why this matters\n'
                       'Distinguish tasks and learn how flexibility, data volume and '
                       'representation affect generalization. This lesson focuses on '
                       '**classification versus regression** so you can make an explicit choice '
                       'rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Classification predicts discrete labels and regression predicts numeric '
                       'quantities; choose the target type before selecting an estimator.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Predicting an iris species is classification; predicting a house price is '
                       'regression. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Write X, y and a sensible metric for both situations. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A number-coded class label does not turn a classification task into '
                       'regression. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **classification versus regression** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Classification predicts discrete labels and '
                       'regression predicts numeric quantities; choose the target type before '
                       'selecting an estimator.\n',
            'estimated_minutes': 30,
            'has_code_examples': False},
 'exercises': [{'title': 'Classification Versus Regression — hands-on activity',
                'description': 'Write X, y and a sensible metric for both situations. Deliver a '
                               'short notebook, annotated example or written calculation with your '
                               'result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-02']},
               {'title': 'Classification Versus Regression — critical reasoning',
                'description': 'Consider this boundary: A number-coded class label does not turn a '
                               'classification task into regression. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Classification Versus Regression — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Classification Versus Regression?',
                         'options': ['The most flexible model always predicts unseen examples '
                                     'best.',
                                     'Every numeric target should be handled as classification.',
                                     'The neighborhood size never changes a kNN prediction.',
                                     'Classification predicts discrete labels and regression '
                                     'predicts numeric quantities; choose the target type before '
                                     'selecting an estimator.'],
                         'correct': 3,
                         'explanation': 'Classification predicts discrete labels and regression '
                                        'predicts numeric quantities; choose the target type '
                                        'before selecting an estimator. In the worked scenario: '
                                        'Predicting an iris species is classification; predicting '
                                        'a house price is regression.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Classification Versus Regression?',
                         'options': ['Sketch underfit, balanced and overfit train/test error '
                                     'patterns.',
                                     'Write X, y and a sensible metric for both situations.',
                                     'Compare several k values using a development split or CV.',
                                     'Fit a kNN regressor and compare train and validation R² '
                                     'across k.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Write X, y and a sensible '
                                        'metric for both situations.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A number-coded class label does not '
                                     'turn a classification task into regression.',
                         'type': 'open'}],
          'passing_score': 70}}
