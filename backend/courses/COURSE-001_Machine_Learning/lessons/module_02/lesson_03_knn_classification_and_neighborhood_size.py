"""M02.L03 — kNN Classification and Neighborhood Size.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 35–40. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M02.L03"
MODULE_ORDER = 2
MODULE_TITLE = 'Supervised Learning & Generalization'
MODULE_DESCRIPTION = 'Distinguish tasks and learn how flexibility, data volume and representation affect generalization.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '35–40'

TOPIC = {'title': 'kNN Classification and Neighborhood Size',
 'slug': 'ml-foundations-m02-l03',
 'description': 'kNN classification uses local labeled examples; k determines boundary smoothness '
                'and must be chosen using validation.',
 'order': 3,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-02'],
 'prerequisite_ids': [],
 'lesson': {'title': 'kNN Classification and Neighborhood Size',
            'content': '# kNN Classification and Neighborhood Size\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M02.L03 | '
                       '**Module:** Supervised Learning & Generalization\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 35–40. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: kNN classification uses local labeled examples; k determines '
                       'boundary smoothness and must be chosen using validation.\n'
                       '- Apply the principle to: k=1 creates a very local boundary while larger k '
                       'averages over wider neighborhoods.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare several k values using a development split or CV.\n'
                       '\n'
                       '## Why this matters\n'
                       'Distinguish tasks and learn how flexibility, data volume and '
                       'representation affect generalization. This lesson focuses on **knn '
                       'classification and neighborhood size** so you can make an explicit choice '
                       'rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'kNN classification uses local labeled examples; k determines boundary '
                       'smoothness and must be chosen using validation.\n'
                       '\n'
                       '## Worked scenario\n'
                       'k=1 creates a very local boundary while larger k averages over wider '
                       'neighborhoods. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare several k values using a development split or CV. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Feature scale can distort nearest-neighbor distances. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.neighbors import KNeighborsClassifier\n'
                       'model = KNeighborsClassifier(n_neighbors=5)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **knn classification and neighborhood size** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** kNN classification uses local labeled examples; k '
                       'determines boundary smoothness and must be chosen using validation.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'kNN Classification and Neighborhood Size — hands-on activity',
                'description': 'Compare several k values using a development split or CV. Deliver '
                               'a short notebook, annotated example or written calculation with '
                               'your result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-02']},
               {'title': 'kNN Classification and Neighborhood Size — critical reasoning',
                'description': 'Consider this boundary: Feature scale can distort nearest-neighbor '
                               'distances. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'kNN Classification and Neighborhood Size — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of kNN '
                                     'Classification and Neighborhood Size?',
                         'options': ['The most flexible model always predicts unseen examples '
                                     'best.',
                                     'kNN classification uses local labeled examples; k determines '
                                     'boundary smoothness and must be chosen using validation.',
                                     'Every numeric target should be handled as classification.',
                                     'The neighborhood size never changes a kNN prediction.'],
                         'correct': 1,
                         'explanation': 'kNN classification uses local labeled examples; k '
                                        'determines boundary smoothness and must be chosen using '
                                        'validation. In the worked scenario: k=1 creates a very '
                                        'local boundary while larger k averages over wider '
                                        'neighborhoods.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'kNN Classification and Neighborhood Size?',
                         'options': ['Write X, y and a sensible metric for both situations.',
                                     'Sketch underfit, balanced and overfit train/test error '
                                     'patterns.',
                                     'Fit a kNN regressor and compare train and validation R² '
                                     'across k.',
                                     'Compare several k values using a development split or CV.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Compare several k values using '
                                        'a development split or CV.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Feature scale can distort '
                                     'nearest-neighbor distances.',
                         'type': 'open'}],
          'passing_score': 70}}
