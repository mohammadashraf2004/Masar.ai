"""M08.L03 — NMF: Nonnegative Components.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 155–158. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L03"
MODULE_ORDER = 8
MODULE_TITLE = 'Dimensionality Reduction & Feature Extraction'
MODULE_DESCRIPTION = 'Understand PCA, NMF and t-SNE as tools with distinct goals and constraints.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '155–158'

TOPIC = {'title': 'NMF: Nonnegative Components',
 'slug': 'ml-foundations-m08-l03',
 'description': 'NMF factorizes nonnegative measurements into additive components and nonnegative '
                'weights; representation differs from PCA.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-08'],
 'prerequisite_ids': [],
 'lesson': {'title': 'NMF: Nonnegative Components',
            'content': '# NMF: Nonnegative Components\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M08.L03 | '
                       '**Module:** Dimensionality Reduction & Feature Extraction\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 155–158. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: NMF factorizes nonnegative measurements into additive '
                       'components and nonnegative weights; representation differs from PCA.\n'
                       '- Apply the principle to: A grayscale image can be described by additive '
                       'nonnegative pattern contributions.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Explain why negative input values break standard NMF assumptions.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand PCA, NMF and t-SNE as tools with distinct goals and '
                       'constraints. This lesson focuses on **nmf: nonnegative components** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'NMF factorizes nonnegative measurements into additive components and '
                       'nonnegative weights; representation differs from PCA.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A grayscale image can be described by additive nonnegative pattern '
                       'contributions. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Explain why negative input values break standard NMF assumptions. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'NMF components are not orthogonal PCA axes. Explain how your method '
                       'respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.decomposition import NMF\n'
                       'nmf = NMF(n_components=3, init="nndsvda", random_state=42, max_iter=500)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **nmf: nonnegative components** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** NMF factorizes nonnegative measurements into '
                       'additive components and nonnegative weights; representation differs from '
                       'PCA.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'NMF: Nonnegative Components — hands-on activity',
                'description': 'Explain why negative input values break standard NMF assumptions. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-08']},
               {'title': 'NMF: Nonnegative Components — critical reasoning',
                'description': 'Consider this boundary: NMF components are not orthogonal PCA '
                               'axes. Explain a failure mode if it is ignored and the safeguard '
                               'you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'NMF: Nonnegative Components — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of NMF: '
                                     'Nonnegative Components?',
                         'options': ['Maximum variance always identifies the strongest predictor.',
                                     'NMF accepts arbitrary negative input without preprocessing.',
                                     't-SNE axes are calibrated feature measurements.',
                                     'NMF factorizes nonnegative measurements into additive '
                                     'components and nonnegative weights; representation differs '
                                     'from PCA.'],
                         'correct': 3,
                         'explanation': 'NMF factorizes nonnegative measurements into additive '
                                        'components and nonnegative weights; representation '
                                        'differs from PCA. In the worked scenario: A grayscale '
                                        'image can be described by additive nonnegative pattern '
                                        'contributions.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'NMF: Nonnegative Components?',
                         'options': ['Sketch the first component of an elongated 2D scatterplot.',
                                     'Explain why negative input values break standard NMF '
                                     'assumptions.',
                                     'Fit PCA on training data and transform validation data with '
                                     'the same fitted object.',
                                     'Fit a small NMF and describe how a sample combines '
                                     'components.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Explain why negative input '
                                        'values break standard NMF assumptions.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? NMF components are not orthogonal PCA '
                                     'axes.',
                         'type': 'open'}],
          'passing_score': 70}}
