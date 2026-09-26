"""M07.L04 — Scaling for a Kernel SVM.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 138–140. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M07.L04"
MODULE_ORDER = 7
MODULE_TITLE = 'Unsupervised Learning & Preprocessing'
MODULE_DESCRIPTION = 'Learn transformer behavior and how data leakage affects scaled unsupervised representations.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '138–140'

TOPIC = {'title': 'Scaling for a Kernel SVM',
 'slug': 'ml-foundations-m07-l04',
 'description': 'SVM performance depends on distances across feature dimensions; assess scaling as '
                'part of a full modeling workflow.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5,
 'skill_tags': ['machine-learning', 'foundations', 'module-07'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Scaling for a Kernel SVM',
            'content': '# Scaling for a Kernel SVM\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M07.L04 | '
                       '**Module:** Unsupervised Learning & Preprocessing\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 138–140. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: SVM performance depends on distances across feature dimensions; '
                       'assess scaling as part of a full modeling workflow.\n'
                       '- Apply the principle to: Scaling changes which points count as similar '
                       'for an RBF kernel.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare a scaled versus unscaled SVM using a held-out development split.\n'
                       '\n'
                       '## Why this matters\n'
                       'Learn transformer behavior and how data leakage affects scaled '
                       'unsupervised representations. This lesson focuses on **scaling for a '
                       'kernel svm** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'SVM performance depends on distances across feature dimensions; assess '
                       'scaling as part of a full modeling workflow.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Scaling changes which points count as similar for an RBF kernel. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare a scaled versus unscaled SVM using a held-out development split. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A scaling choice should not be made by repeatedly inspecting the final '
                       'test score. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **scaling for a kernel svm** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** SVM performance depends on distances across feature '
                       'dimensions; assess scaling as part of a full modeling workflow.\n',
            'estimated_minutes': 30,
            'has_code_examples': False},
 'exercises': [{'title': 'Scaling for a Kernel SVM — hands-on activity',
                'description': 'Compare a scaled versus unscaled SVM using a held-out development '
                               'split. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-07']},
               {'title': 'Scaling for a Kernel SVM — critical reasoning',
                'description': 'Consider this boundary: A scaling choice should not be made by '
                               'repeatedly inspecting the final test score. Explain a failure mode '
                               'if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Scaling for a Kernel SVM — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Scaling '
                                     'for a Kernel SVM?',
                         'options': ['It is safe to fit scalers on the test set.',
                                     'Unsupervised methods require a supervised target.',
                                     'All scaling methods guarantee that future values stay within '
                                     'training bounds.',
                                     'SVM performance depends on distances across feature '
                                     'dimensions; assess scaling as part of a full modeling '
                                     'workflow.'],
                         'correct': 3,
                         'explanation': 'SVM performance depends on distances across feature '
                                        'dimensions; assess scaling as part of a full modeling '
                                        'workflow. In the worked scenario: Scaling changes which '
                                        'points count as similar for an RBF kernel.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Scaling for a Kernel SVM?',
                         'options': ['Differentiate clustering, dimensionality reduction and '
                                     'preprocessing in three cases.',
                                     'Compare a scaled versus unscaled SVM using a held-out '
                                     'development split.',
                                     'Scale a small numeric array using two methods and inspect '
                                     'resulting distributions.',
                                     'Demonstrate train-fit then test-transform and identify '
                                     'leaked alternative code.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Compare a scaled versus '
                                        'unscaled SVM using a held-out development split.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A scaling choice should not be made by '
                                     'repeatedly inspecting the final test score.',
                         'type': 'open'}],
          'passing_score': 70}}
