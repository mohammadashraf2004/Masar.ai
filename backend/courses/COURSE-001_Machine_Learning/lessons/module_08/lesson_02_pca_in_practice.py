"""M08.L02 — PCA in Practice.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 142–155. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L02"
MODULE_ORDER = 8
MODULE_TITLE = 'Dimensionality Reduction & Feature Extraction'
MODULE_DESCRIPTION = 'Understand PCA, NMF and t-SNE as tools with distinct goals and constraints.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '142–155'

TOPIC = {'title': 'PCA in Practice',
 'slug': 'ml-foundations-m08-l02',
 'description': 'Fit PCA after suitable training-only scaling, inspect explained variance and '
                'components, and evaluate reconstruction carefully.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-08'],
 'prerequisite_ids': [],
 'lesson': {'title': 'PCA in Practice',
            'content': '# PCA in Practice\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M08.L02 | '
                       '**Module:** Dimensionality Reduction & Feature Extraction\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 142–155. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Fit PCA after suitable training-only scaling, inspect explained '
                       'variance and components, and evaluate reconstruction carefully.\n'
                       '- Apply the principle to: Thirty numeric columns can be projected to two '
                       'components for visualization.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit '
                       'PCA on training data and transform validation data with the same fitted '
                       'object.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand PCA, NMF and t-SNE as tools with distinct goals and '
                       'constraints. This lesson focuses on **pca in practice** so you can make an '
                       'explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Fit PCA after suitable training-only scaling, inspect explained variance '
                       'and components, and evaluate reconstruction carefully.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Thirty numeric columns can be projected to two components for '
                       'visualization. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit PCA on training data and transform validation data with the same '
                       'fitted object. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not use test-set structure to choose principal components during '
                       'evaluation. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.decomposition import PCA\n'
                       'pca = PCA(n_components=2, random_state=42)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **pca in practice** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Fit PCA after suitable training-only scaling, '
                       'inspect explained variance and components, and evaluate reconstruction '
                       'carefully.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'PCA in Practice — hands-on activity',
                'description': 'Fit PCA on training data and transform validation data with the '
                               'same fitted object. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-08']},
               {'title': 'PCA in Practice — critical reasoning',
                'description': 'Consider this boundary: Do not use test-set structure to choose '
                               'principal components during evaluation. Explain a failure mode if '
                               'it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'PCA in Practice — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of PCA in '
                                     'Practice?',
                         'options': ['Maximum variance always identifies the strongest predictor.',
                                     'NMF accepts arbitrary negative input without preprocessing.',
                                     'Fit PCA after suitable training-only scaling, inspect '
                                     'explained variance and components, and evaluate '
                                     'reconstruction carefully.',
                                     't-SNE axes are calibrated feature measurements.'],
                         'correct': 2,
                         'explanation': 'Fit PCA after suitable training-only scaling, inspect '
                                        'explained variance and components, and evaluate '
                                        'reconstruction carefully. In the worked scenario: Thirty '
                                        'numeric columns can be projected to two components for '
                                        'visualization.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'PCA in Practice?',
                         'options': ['Fit PCA on training data and transform validation data with '
                                     'the same fitted object.',
                                     'Sketch the first component of an elongated 2D scatterplot.',
                                     'Explain why negative input values break standard NMF '
                                     'assumptions.',
                                     'Fit a small NMF and describe how a sample combines '
                                     'components.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Fit PCA on training data and '
                                        'transform validation data with the same fitted object.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not use test-set structure to '
                                     'choose principal components during evaluation.',
                         'type': 'open'}],
          'passing_score': 70}}
