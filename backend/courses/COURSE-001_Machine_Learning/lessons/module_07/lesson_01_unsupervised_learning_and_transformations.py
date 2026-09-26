"""M07.L01 — Unsupervised Learning and Transformations.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 131–132. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M07.L01"
MODULE_ORDER = 7
MODULE_TITLE = 'Unsupervised Learning & Preprocessing'
MODULE_DESCRIPTION = 'Learn transformer behavior and how data leakage affects scaled unsupervised representations.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '131–132'

TOPIC = {'title': 'Unsupervised Learning and Transformations',
 'slug': 'ml-foundations-m07-l01',
 'description': 'Unsupervised algorithms reveal structure or transform representations without '
                'supervised target labels; their patterns still need interpretation.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5,
 'skill_tags': ['machine-learning', 'foundations', 'module-07'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Unsupervised Learning and Transformations',
            'content': '# Unsupervised Learning and Transformations\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M07.L01 | '
                       '**Module:** Unsupervised Learning & Preprocessing\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 131–132. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Unsupervised algorithms reveal structure or transform '
                       'representations without supervised target labels; their patterns still '
                       'need interpretation.\n'
                       '- Apply the principle to: Clustering finds groups, while scaling and PCA '
                       'produce new representations.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Differentiate clustering, dimensionality reduction and preprocessing in '
                       'three cases.\n'
                       '\n'
                       '## Why this matters\n'
                       'Learn transformer behavior and how data leakage affects scaled '
                       'unsupervised representations. This lesson focuses on **unsupervised '
                       'learning and transformations** so you can make an explicit choice rather '
                       'than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Unsupervised algorithms reveal structure or transform representations '
                       'without supervised target labels; their patterns still need '
                       'interpretation.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Clustering finds groups, while scaling and PCA produce new '
                       'representations. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Differentiate clustering, dimensionality reduction and preprocessing in '
                       'three cases. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Unsupervised clusters are not automatically meaningful or labeled classes. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **unsupervised learning and transformations** in your own words '
                       'and answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Unsupervised algorithms reveal structure or '
                       'transform representations without supervised target labels; their patterns '
                       'still need interpretation.\n',
            'estimated_minutes': 30,
            'has_code_examples': False},
 'exercises': [{'title': 'Unsupervised Learning and Transformations — hands-on activity',
                'description': 'Differentiate clustering, dimensionality reduction and '
                               'preprocessing in three cases. Deliver a short notebook, annotated '
                               'example or written calculation with your result and '
                               'interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-07']},
               {'title': 'Unsupervised Learning and Transformations — critical reasoning',
                'description': 'Consider this boundary: Unsupervised clusters are not '
                               'automatically meaningful or labeled classes. Explain a failure '
                               'mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Unsupervised Learning and Transformations — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Unsupervised Learning and Transformations?',
                         'options': ['Unsupervised algorithms reveal structure or transform '
                                     'representations without supervised target labels; their '
                                     'patterns still need interpretation.',
                                     'It is safe to fit scalers on the test set.',
                                     'Unsupervised methods require a supervised target.',
                                     'All scaling methods guarantee that future values stay within '
                                     'training bounds.'],
                         'correct': 0,
                         'explanation': 'Unsupervised algorithms reveal structure or transform '
                                        'representations without supervised target labels; their '
                                        'patterns still need interpretation. In the worked '
                                        'scenario: Clustering finds groups, while scaling and PCA '
                                        'produce new representations.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Unsupervised Learning and Transformations?',
                         'options': ['Scale a small numeric array using two methods and inspect '
                                     'resulting distributions.',
                                     'Demonstrate train-fit then test-transform and identify '
                                     'leaked alternative code.',
                                     'Differentiate clustering, dimensionality reduction and '
                                     'preprocessing in three cases.',
                                     'Compare a scaled versus unscaled SVM using a held-out '
                                     'development split.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Differentiate clustering, '
                                        'dimensionality reduction and preprocessing in three '
                                        'cases.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Unsupervised clusters are not '
                                     'automatically meaningful or labeled classes.',
                         'type': 'open'}],
          'passing_score': 70}}
