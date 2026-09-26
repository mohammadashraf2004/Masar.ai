"""M05.L01 — Kernel Support Vector Machines.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 92–100. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M05.L01"
MODULE_ORDER = 5
MODULE_TITLE = 'Nonlinear Models & Neural Network Introduction'
MODULE_DESCRIPTION = 'Use nonlinear kernels and explain a feed-forward neural network without expanding into a deep-learning course.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '92–100'

TOPIC = {'title': 'Kernel Support Vector Machines',
 'slug': 'ml-foundations-m05-l01',
 'description': 'A kernel SVM uses similarity to create nonlinear decision boundaries without '
                'manually constructing all transformed features.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-05'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Kernel Support Vector Machines',
            'content': '# Kernel Support Vector Machines\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M05.L01 | '
                       '**Module:** Nonlinear Models & Neural Network Introduction\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 92–100. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: A kernel SVM uses similarity to create nonlinear decision '
                       'boundaries without manually constructing all transformed features.\n'
                       '- Apply the principle to: An RBF kernel can surround nonlinearly separated '
                       'groups in a two-feature plot.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare linear and RBF SVC results on a nonlinear example.\n'
                       '\n'
                       '## Why this matters\n'
                       'Use nonlinear kernels and explain a feed-forward neural network without '
                       'expanding into a deep-learning course. This lesson focuses on **kernel '
                       'support vector machines** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'A kernel SVM uses similarity to create nonlinear decision boundaries '
                       'without manually constructing all transformed features.\n'
                       '\n'
                       '## Worked scenario\n'
                       'An RBF kernel can surround nonlinearly separated groups in a two-feature '
                       'plot. Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare linear and RBF SVC results on a nonlinear example. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Kernel flexibility does not eliminate overfitting. Explain how your method '
                       'respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.svm import SVC\n'
                       'classifier = SVC(kernel="rbf", C=1.0, gamma="scale")\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **kernel support vector machines** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** A kernel SVM uses similarity to create nonlinear '
                       'decision boundaries without manually constructing all transformed '
                       'features.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Kernel Support Vector Machines — hands-on activity',
                'description': 'Compare linear and RBF SVC results on a nonlinear example. Deliver '
                               'a short notebook, annotated example or written calculation with '
                               'your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-05']},
               {'title': 'Kernel Support Vector Machines — critical reasoning',
                'description': 'Consider this boundary: Kernel flexibility does not eliminate '
                               'overfitting. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Kernel Support Vector Machines — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Kernel '
                                     'Support Vector Machines?',
                         'options': ['Kernel models are unaffected by input feature scale.',
                                     'Increasing model complexity cannot cause overfitting.',
                                     'A kernel SVM uses similarity to create nonlinear decision '
                                     'boundaries without manually constructing all transformed '
                                     'features.',
                                     'MLPs always outperform classical methods on small data.'],
                         'correct': 2,
                         'explanation': 'A kernel SVM uses similarity to create nonlinear decision '
                                        'boundaries without manually constructing all transformed '
                                        'features. In the worked scenario: An RBF kernel can '
                                        'surround nonlinearly separated groups in a two-feature '
                                        'plot.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Kernel Support Vector Machines?',
                         'options': ['Compare linear and RBF SVC results on a nonlinear example.',
                                     'Build a scaling-plus-SVC pipeline and compare several '
                                     'C/gamma combinations.',
                                     'Draw a small input-hidden-output network and count '
                                     'connections.',
                                     'Train a scaled MLP and compare training versus validation '
                                     'scores.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Compare linear and RBF SVC '
                                        'results on a nonlinear example.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Kernel flexibility does not eliminate '
                                     'overfitting.',
                         'type': 'open'}],
          'passing_score': 70}}
