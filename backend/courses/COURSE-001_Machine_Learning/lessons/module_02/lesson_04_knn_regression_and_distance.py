"""M02.L04 — kNN Regression and Distance.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 40–44. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M02.L04"
MODULE_ORDER = 2
MODULE_TITLE = 'Supervised Learning & Generalization'
MODULE_DESCRIPTION = 'Distinguish tasks and learn how flexibility, data volume and representation affect generalization.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '40–44'

TOPIC = {'title': 'kNN Regression and Distance',
 'slug': 'ml-foundations-m02-l04',
 'description': 'kNN regression averages nearby targets; distance and neighborhood selection '
                'determine how locally predictions respond.',
 'order': 4,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-02'],
 'prerequisite_ids': [],
 'lesson': {'title': 'kNN Regression and Distance',
            'content': '# kNN Regression and Distance\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M02.L04 | '
                       '**Module:** Supervised Learning & Generalization\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 40–44. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: kNN regression averages nearby targets; distance and '
                       'neighborhood selection determine how locally predictions respond.\n'
                       '- Apply the principle to: Predict a house value by averaging values of '
                       'comparable houses.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit a '
                       'kNN regressor and compare train and validation R² across k.\n'
                       '\n'
                       '## Why this matters\n'
                       'Distinguish tasks and learn how flexibility, data volume and '
                       'representation affect generalization. This lesson focuses on **knn '
                       'regression and distance** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'kNN regression averages nearby targets; distance and neighborhood '
                       'selection determine how locally predictions respond.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Predict a house value by averaging values of comparable houses. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit a kNN regressor and compare train and validation R² across k. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Nearest-neighbor regressors do not automatically extrapolate beyond known '
                       'target ranges. Explain how your method respects this boundary or avoids '
                       'the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.neighbors import KNeighborsRegressor\n'
                       'regressor = KNeighborsRegressor(n_neighbors=5)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **knn regression and distance** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** kNN regression averages nearby targets; distance and '
                       'neighborhood selection determine how locally predictions respond.\n',
            'estimated_minutes': 35,
            'has_code_examples': True},
 'exercises': [{'title': 'kNN Regression and Distance — hands-on activity',
                'description': 'Fit a kNN regressor and compare train and validation R² across k. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-02']},
               {'title': 'kNN Regression and Distance — critical reasoning',
                'description': 'Consider this boundary: Nearest-neighbor regressors do not '
                               'automatically extrapolate beyond known target ranges. Explain a '
                               'failure mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'kNN Regression and Distance — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of kNN '
                                     'Regression and Distance?',
                         'options': ['The most flexible model always predicts unseen examples '
                                     'best.',
                                     'Every numeric target should be handled as classification.',
                                     'kNN regression averages nearby targets; distance and '
                                     'neighborhood selection determine how locally predictions '
                                     'respond.',
                                     'The neighborhood size never changes a kNN prediction.'],
                         'correct': 2,
                         'explanation': 'kNN regression averages nearby targets; distance and '
                                        'neighborhood selection determine how locally predictions '
                                        'respond. In the worked scenario: Predict a house value by '
                                        'averaging values of comparable houses.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'kNN Regression and Distance?',
                         'options': ['Fit a kNN regressor and compare train and validation R² '
                                     'across k.',
                                     'Write X, y and a sensible metric for both situations.',
                                     'Sketch underfit, balanced and overfit train/test error '
                                     'patterns.',
                                     'Compare several k values using a development split or CV.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Fit a kNN regressor and compare '
                                        'train and validation R² across k.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Nearest-neighbor regressors do not '
                                     'automatically extrapolate beyond known target ranges.',
                         'type': 'open'}],
          'passing_score': 70}}
