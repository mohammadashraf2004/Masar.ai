"""M05.L04 — Training and Tuning an MLP.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 113–119. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M05.L04"
MODULE_ORDER = 5
MODULE_TITLE = 'Nonlinear Models & Neural Network Introduction'
MODULE_DESCRIPTION = 'Use nonlinear kernels and explain a feed-forward neural network without expanding into a deep-learning course.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '113–119'

TOPIC = {'title': 'Training and Tuning an MLP',
 'slug': 'ml-foundations-m05-l04',
 'description': 'MLP training depends on feature scaling, capacity, regularization, optimization '
                'and a validation strategy.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-05'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Training and Tuning an MLP',
            'content': '# Training and Tuning an MLP\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M05.L04 | '
                       '**Module:** Nonlinear Models & Neural Network Introduction\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 113–119. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: MLP training depends on feature scaling, capacity, '
                       'regularization, optimization and a validation strategy.\n'
                       '- Apply the principle to: Changing hidden-layer width alters model '
                       'capacity and runtime.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Train '
                       'a scaled MLP and compare training versus validation scores.\n'
                       '\n'
                       '## Why this matters\n'
                       'Use nonlinear kernels and explain a feed-forward neural network without '
                       'expanding into a deep-learning course. This lesson focuses on **training '
                       'and tuning an mlp** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'MLP training depends on feature scaling, capacity, regularization, '
                       'optimization and a validation strategy.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Changing hidden-layer width alters model capacity and runtime. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Train a scaled MLP and compare training versus validation scores. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not interpret convergence warnings as evidence of good model quality. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.neural_network import MLPClassifier\n'
                       'classifier = MLPClassifier(hidden_layer_sizes=(50,), max_iter=1000, '
                       'random_state=42)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **training and tuning an mlp** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** MLP training depends on feature scaling, capacity, '
                       'regularization, optimization and a validation strategy.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Training and Tuning an MLP — hands-on activity',
                'description': 'Train a scaled MLP and compare training versus validation scores. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-05']},
               {'title': 'Training and Tuning an MLP — critical reasoning',
                'description': 'Consider this boundary: Do not interpret convergence warnings as '
                               'evidence of good model quality. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Training and Tuning an MLP — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Training and Tuning an MLP?',
                         'options': ['Kernel models are unaffected by input feature scale.',
                                     'MLP training depends on feature scaling, capacity, '
                                     'regularization, optimization and a validation strategy.',
                                     'Increasing model complexity cannot cause overfitting.',
                                     'MLPs always outperform classical methods on small data.'],
                         'correct': 1,
                         'explanation': 'MLP training depends on feature scaling, capacity, '
                                        'regularization, optimization and a validation strategy. '
                                        'In the worked scenario: Changing hidden-layer width '
                                        'alters model capacity and runtime.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Training and Tuning an MLP?',
                         'options': ['Compare linear and RBF SVC results on a nonlinear example.',
                                     'Build a scaling-plus-SVC pipeline and compare several '
                                     'C/gamma combinations.',
                                     'Draw a small input-hidden-output network and count '
                                     'connections.',
                                     'Train a scaled MLP and compare training versus validation '
                                     'scores.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Train a scaled MLP and compare '
                                        'training versus validation scores.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not interpret convergence warnings '
                                     'as evidence of good model quality.',
                         'type': 'open'}],
          'passing_score': 70}}
