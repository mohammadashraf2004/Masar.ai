"""M08.L04 — NMF for Pattern Extraction.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 158–163. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L04"
MODULE_ORDER = 8
MODULE_TITLE = 'Dimensionality Reduction & Feature Extraction'
MODULE_DESCRIPTION = 'Understand PCA, NMF and t-SNE as tools with distinct goals and constraints.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '158–163'

TOPIC = {'title': 'NMF for Pattern Extraction',
 'slug': 'ml-foundations-m08-l04',
 'description': 'Inspect learned NMF components and their sample weights to understand recurring '
                'additive patterns.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-08'],
 'prerequisite_ids': [],
 'lesson': {'title': 'NMF for Pattern Extraction',
            'content': '# NMF for Pattern Extraction\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M08.L04 | '
                       '**Module:** Dimensionality Reduction & Feature Extraction\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 158–163. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Inspect learned NMF components and their sample weights to '
                       'understand recurring additive patterns.\n'
                       '- Apply the principle to: Faces may be approximated by weighted '
                       'nonnegative image parts.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit a '
                       'small NMF and describe how a sample combines components.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand PCA, NMF and t-SNE as tools with distinct goals and '
                       'constraints. This lesson focuses on **nmf for pattern extraction** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Inspect learned NMF components and their sample weights to understand '
                       'recurring additive patterns.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Faces may be approximated by weighted nonnegative image parts. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit a small NMF and describe how a sample combines components. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Changing the component count changes the interpretation of extracted '
                       'patterns. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **nmf for pattern extraction** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Inspect learned NMF components and their sample '
                       'weights to understand recurring additive patterns.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'NMF for Pattern Extraction — hands-on activity',
                'description': 'Fit a small NMF and describe how a sample combines components. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-08']},
               {'title': 'NMF for Pattern Extraction — critical reasoning',
                'description': 'Consider this boundary: Changing the component count changes the '
                               'interpretation of extracted patterns. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'NMF for Pattern Extraction — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of NMF for '
                                     'Pattern Extraction?',
                         'options': ['Inspect learned NMF components and their sample weights to '
                                     'understand recurring additive patterns.',
                                     'Maximum variance always identifies the strongest predictor.',
                                     'NMF accepts arbitrary negative input without preprocessing.',
                                     't-SNE axes are calibrated feature measurements.'],
                         'correct': 0,
                         'explanation': 'Inspect learned NMF components and their sample weights '
                                        'to understand recurring additive patterns. In the worked '
                                        'scenario: Faces may be approximated by weighted '
                                        'nonnegative image parts.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'NMF for Pattern Extraction?',
                         'options': ['Sketch the first component of an elongated 2D scatterplot.',
                                     'Fit PCA on training data and transform validation data with '
                                     'the same fitted object.',
                                     'Fit a small NMF and describe how a sample combines '
                                     'components.',
                                     'Explain why negative input values break standard NMF '
                                     'assumptions.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Fit a small NMF and describe '
                                        'how a sample combines components.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Changing the component count changes '
                                     'the interpretation of extracted patterns.',
                         'type': 'open'}],
          'passing_score': 70}}
