"""M07.L02 — Comparing Data Scalers.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 132–134. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M07.L02"
MODULE_ORDER = 7
MODULE_TITLE = 'Unsupervised Learning & Preprocessing'
MODULE_DESCRIPTION = 'Learn transformer behavior and how data leakage affects scaled unsupervised representations.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '132–134'

TOPIC = {'title': 'Comparing Data Scalers',
 'slug': 'ml-foundations-m07-l02',
 'description': 'StandardScaler centers and rescales features, while MinMaxScaler uses training '
                'minima and maxima; choice depends on model and distribution.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-07'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Comparing Data Scalers',
            'content': '# Comparing Data Scalers\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M07.L02 | '
                       '**Module:** Unsupervised Learning & Preprocessing\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 132–134. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: StandardScaler centers and rescales features, while '
                       'MinMaxScaler uses training minima and maxima; choice depends on model and '
                       'distribution.\n'
                       '- Apply the principle to: A 0–10000 feature overwhelms a 0–1 feature in '
                       'Euclidean distance without scaling.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Scale '
                       'a small numeric array using two methods and inspect resulting '
                       'distributions.\n'
                       '\n'
                       '## Why this matters\n'
                       'Learn transformer behavior and how data leakage affects scaled '
                       'unsupervised representations. This lesson focuses on **comparing data '
                       'scalers** so you can make an explicit choice rather than blindly applying '
                       'a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'StandardScaler centers and rescales features, while MinMaxScaler uses '
                       'training minima and maxima; choice depends on model and distribution.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A 0–10000 feature overwhelms a 0–1 feature in Euclidean distance without '
                       'scaling. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Scale a small numeric array using two methods and inspect resulting '
                       'distributions. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'MinMaxScaler cannot guarantee future values stay in the 0–1 interval. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.preprocessing import StandardScaler, MinMaxScaler\n'
                       'scaler = StandardScaler()\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **comparing data scalers** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** StandardScaler centers and rescales features, while '
                       'MinMaxScaler uses training minima and maxima; choice depends on model and '
                       'distribution.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Comparing Data Scalers — hands-on activity',
                'description': 'Scale a small numeric array using two methods and inspect '
                               'resulting distributions. Deliver a short notebook, annotated '
                               'example or written calculation with your result and '
                               'interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-07']},
               {'title': 'Comparing Data Scalers — critical reasoning',
                'description': 'Consider this boundary: MinMaxScaler cannot guarantee future '
                               'values stay in the 0–1 interval. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Comparing Data Scalers — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Comparing Data Scalers?',
                         'options': ['It is safe to fit scalers on the test set.',
                                     'StandardScaler centers and rescales features, while '
                                     'MinMaxScaler uses training minima and maxima; choice depends '
                                     'on model and distribution.',
                                     'Unsupervised methods require a supervised target.',
                                     'All scaling methods guarantee that future values stay within '
                                     'training bounds.'],
                         'correct': 1,
                         'explanation': 'StandardScaler centers and rescales features, while '
                                        'MinMaxScaler uses training minima and maxima; choice '
                                        'depends on model and distribution. In the worked '
                                        'scenario: A 0–10000 feature overwhelms a 0–1 feature in '
                                        'Euclidean distance without scaling.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Comparing Data Scalers?',
                         'options': ['Differentiate clustering, dimensionality reduction and '
                                     'preprocessing in three cases.',
                                     'Demonstrate train-fit then test-transform and identify '
                                     'leaked alternative code.',
                                     'Compare a scaled versus unscaled SVM using a held-out '
                                     'development split.',
                                     'Scale a small numeric array using two methods and inspect '
                                     'resulting distributions.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Scale a small numeric array '
                                        'using two methods and inspect resulting distributions.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? MinMaxScaler cannot guarantee future '
                                     'values stay in the 0–1 interval.',
                         'type': 'open'}],
          'passing_score': 70}}
