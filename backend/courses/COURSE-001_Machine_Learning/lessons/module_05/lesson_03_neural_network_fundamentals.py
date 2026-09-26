"""M05.L03 — Neural Network Fundamentals.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 105–113. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M05.L03"
MODULE_ORDER = 5
MODULE_TITLE = 'Nonlinear Models & Neural Network Introduction'
MODULE_DESCRIPTION = 'Use nonlinear kernels and explain a feed-forward neural network without expanding into a deep-learning course.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '105–113'

TOPIC = {'title': 'Neural Network Fundamentals',
 'slug': 'ml-foundations-m05-l03',
 'description': 'An MLP combines layers of weighted transformations and nonlinear activations to '
                'learn flexible patterns.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-05'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Neural Network Fundamentals',
            'content': '# Neural Network Fundamentals\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M05.L03 | '
                       '**Module:** Nonlinear Models & Neural Network Introduction\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 105–113. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: An MLP combines layers of weighted transformations and '
                       'nonlinear activations to learn flexible patterns.\n'
                       '- Apply the principle to: A hidden layer can represent nonlinear '
                       'interactions unavailable to a single linear boundary.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Draw '
                       'a small input-hidden-output network and count connections.\n'
                       '\n'
                       '## Why this matters\n'
                       'Use nonlinear kernels and explain a feed-forward neural network without '
                       'expanding into a deep-learning course. This lesson focuses on **neural '
                       'network fundamentals** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'An MLP combines layers of weighted transformations and nonlinear '
                       'activations to learn flexible patterns.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A hidden layer can represent nonlinear interactions unavailable to a '
                       'single linear boundary. Before claiming that a method works, check what '
                       'data it uses, which predictions or patterns it produces, and how those '
                       'outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Draw a small input-hidden-output network and count connections. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A neural network is not inherently better for every small tabular dataset. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **neural network fundamentals** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** An MLP combines layers of weighted transformations '
                       'and nonlinear activations to learn flexible patterns.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Neural Network Fundamentals — hands-on activity',
                'description': 'Draw a small input-hidden-output network and count connections. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-05']},
               {'title': 'Neural Network Fundamentals — critical reasoning',
                'description': 'Consider this boundary: A neural network is not inherently better '
                               'for every small tabular dataset. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Neural Network Fundamentals — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Neural '
                                     'Network Fundamentals?',
                         'options': ['An MLP combines layers of weighted transformations and '
                                     'nonlinear activations to learn flexible patterns.',
                                     'Kernel models are unaffected by input feature scale.',
                                     'Increasing model complexity cannot cause overfitting.',
                                     'MLPs always outperform classical methods on small data.'],
                         'correct': 0,
                         'explanation': 'An MLP combines layers of weighted transformations and '
                                        'nonlinear activations to learn flexible patterns. In the '
                                        'worked scenario: A hidden layer can represent nonlinear '
                                        'interactions unavailable to a single linear boundary.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Neural Network Fundamentals?',
                         'options': ['Compare linear and RBF SVC results on a nonlinear example.',
                                     'Build a scaling-plus-SVC pipeline and compare several '
                                     'C/gamma combinations.',
                                     'Draw a small input-hidden-output network and count '
                                     'connections.',
                                     'Train a scaled MLP and compare training versus validation '
                                     'scores.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Draw a small '
                                        'input-hidden-output network and count connections.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A neural network is not inherently '
                                     'better for every small tabular dataset.',
                         'type': 'open'}],
          'passing_score': 70}}
