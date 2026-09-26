"""M08.L01 — PCA: Variance and Principal Directions.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 140–142. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L01"
MODULE_ORDER = 8
MODULE_TITLE = 'Dimensionality Reduction & Feature Extraction'
MODULE_DESCRIPTION = 'Understand PCA, NMF and t-SNE as tools with distinct goals and constraints.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '140–142'

TOPIC = {'title': 'PCA: Variance and Principal Directions',
 'slug': 'ml-foundations-m08-l01',
 'description': 'PCA learns orthogonal axes of maximal variance without using labels; component '
                'scores define a lower-dimensional representation.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-08'],
 'prerequisite_ids': [],
 'lesson': {'title': 'PCA: Variance and Principal Directions',
            'content': '# PCA: Variance and Principal Directions\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M08.L01 | '
                       '**Module:** Dimensionality Reduction & Feature Extraction\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 140–142. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: PCA learns orthogonal axes of maximal variance without using '
                       'labels; component scores define a lower-dimensional representation.\n'
                       '- Apply the principle to: A diagonal point cloud is summarized by a '
                       'leading direction along its widest spread.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Sketch the first component of an elongated 2D scatterplot.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand PCA, NMF and t-SNE as tools with distinct goals and '
                       'constraints. This lesson focuses on **pca: variance and principal '
                       'directions** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'PCA learns orthogonal axes of maximal variance without using labels; '
                       'component scores define a lower-dimensional representation.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A diagonal point cloud is summarized by a leading direction along its '
                       'widest spread. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Sketch the first component of an elongated 2D scatterplot. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Maximum variance does not guarantee maximum predictive relevance. Explain '
                       'how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **pca: variance and principal directions** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** PCA learns orthogonal axes of maximal variance '
                       'without using labels; component scores define a lower-dimensional '
                       'representation.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'PCA: Variance and Principal Directions — hands-on activity',
                'description': 'Sketch the first component of an elongated 2D scatterplot. Deliver '
                               'a short notebook, annotated example or written calculation with '
                               'your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-08']},
               {'title': 'PCA: Variance and Principal Directions — critical reasoning',
                'description': 'Consider this boundary: Maximum variance does not guarantee '
                               'maximum predictive relevance. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'PCA: Variance and Principal Directions — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of PCA: '
                                     'Variance and Principal Directions?',
                         'options': ['Maximum variance always identifies the strongest predictor.',
                                     'PCA learns orthogonal axes of maximal variance without using '
                                     'labels; component scores define a lower-dimensional '
                                     'representation.',
                                     'NMF accepts arbitrary negative input without preprocessing.',
                                     't-SNE axes are calibrated feature measurements.'],
                         'correct': 1,
                         'explanation': 'PCA learns orthogonal axes of maximal variance without '
                                        'using labels; component scores define a lower-dimensional '
                                        'representation. In the worked scenario: A diagonal point '
                                        'cloud is summarized by a leading direction along its '
                                        'widest spread.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'PCA: Variance and Principal Directions?',
                         'options': ['Fit PCA on training data and transform validation data with '
                                     'the same fitted object.',
                                     'Explain why negative input values break standard NMF '
                                     'assumptions.',
                                     'Fit a small NMF and describe how a sample combines '
                                     'components.',
                                     'Sketch the first component of an elongated 2D scatterplot.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Sketch the first component of '
                                        'an elongated 2D scatterplot.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Maximum variance does not guarantee '
                                     'maximum predictive relevance.',
                         'type': 'open'}],
          'passing_score': 70}}
