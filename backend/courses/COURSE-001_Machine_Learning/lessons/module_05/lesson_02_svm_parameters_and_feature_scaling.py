"""M05.L02 — SVM Parameters and Feature Scaling.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 100–105. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M05.L02"
MODULE_ORDER = 5
MODULE_TITLE = 'Nonlinear Models & Neural Network Introduction'
MODULE_DESCRIPTION = 'Use nonlinear kernels and explain a feed-forward neural network without expanding into a deep-learning course.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '100–105'

TOPIC = {'title': 'SVM Parameters and Feature Scaling',
 'slug': 'ml-foundations-m05-l02',
 'description': 'SVC C governs regularization and gamma controls RBF locality; distance-based '
                'kernels depend on comparable feature scales.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-05'],
 'prerequisite_ids': [],
 'lesson': {'title': 'SVM Parameters and Feature Scaling',
            'content': '# SVM Parameters and Feature Scaling\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M05.L02 | '
                       '**Module:** Nonlinear Models & Neural Network Introduction\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 100–105. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: SVC C governs regularization and gamma controls RBF locality; '
                       'distance-based kernels depend on comparable feature scales.\n'
                       '- Apply the principle to: One feature measured in thousands can dominate '
                       'an unscaled distance.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Build '
                       'a scaling-plus-SVC pipeline and compare several C/gamma combinations.\n'
                       '\n'
                       '## Why this matters\n'
                       'Use nonlinear kernels and explain a feed-forward neural network without '
                       'expanding into a deep-learning course. This lesson focuses on **svm '
                       'parameters and feature scaling** so you can make an explicit choice rather '
                       'than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'SVC C governs regularization and gamma controls RBF locality; '
                       'distance-based kernels depend on comparable feature scales.\n'
                       '\n'
                       '## Worked scenario\n'
                       'One feature measured in thousands can dominate an unscaled distance. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Build a scaling-plus-SVC pipeline and compare several C/gamma '
                       'combinations. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Never fit a scaler on the entire dataset before CV. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **svm parameters and feature scaling** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** SVC C governs regularization and gamma controls RBF '
                       'locality; distance-based kernels depend on comparable feature scales.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'SVM Parameters and Feature Scaling — hands-on activity',
                'description': 'Build a scaling-plus-SVC pipeline and compare several C/gamma '
                               'combinations. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-05']},
               {'title': 'SVM Parameters and Feature Scaling — critical reasoning',
                'description': 'Consider this boundary: Never fit a scaler on the entire dataset '
                               'before CV. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'SVM Parameters and Feature Scaling — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of SVM '
                                     'Parameters and Feature Scaling?',
                         'options': ['Kernel models are unaffected by input feature scale.',
                                     'Increasing model complexity cannot cause overfitting.',
                                     'MLPs always outperform classical methods on small data.',
                                     'SVC C governs regularization and gamma controls RBF '
                                     'locality; distance-based kernels depend on comparable '
                                     'feature scales.'],
                         'correct': 3,
                         'explanation': 'SVC C governs regularization and gamma controls RBF '
                                        'locality; distance-based kernels depend on comparable '
                                        'feature scales. In the worked scenario: One feature '
                                        'measured in thousands can dominate an unscaled distance.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'SVM Parameters and Feature Scaling?',
                         'options': ['Compare linear and RBF SVC results on a nonlinear example.',
                                     'Build a scaling-plus-SVC pipeline and compare several '
                                     'C/gamma combinations.',
                                     'Draw a small input-hidden-output network and count '
                                     'connections.',
                                     'Train a scaled MLP and compare training versus validation '
                                     'scores.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Build a scaling-plus-SVC '
                                        'pipeline and compare several C/gamma combinations.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Never fit a scaler on the entire '
                                     'dataset before CV.',
                         'type': 'open'}],
          'passing_score': 70}}
