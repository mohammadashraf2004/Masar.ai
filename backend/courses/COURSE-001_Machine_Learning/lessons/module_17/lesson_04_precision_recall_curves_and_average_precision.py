"""M17.L04 — Precision–Recall Curves and Average Precision.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 289–292. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M17.L04"
MODULE_ORDER = 17
MODULE_TITLE = 'Binary Classification Evaluation'
MODULE_DESCRIPTION = 'Choose a metric and threshold that reflects the actual costs of different errors.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '289–292'

TOPIC = {'title': 'Precision–Recall Curves and Average Precision',
 'slug': 'ml-foundations-m17-l04',
 'description': 'A PR curve summarizes positive-class retrieval across thresholds; average '
                'precision weights precision changes by recall increments.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-17'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Precision–Recall Curves and Average Precision',
            'content': '# Precision–Recall Curves and Average Precision\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M17.L04 | '
                       '**Module:** Binary Classification Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 289–292. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: A PR curve summarizes positive-class retrieval across '
                       'thresholds; average precision weights precision changes by recall '
                       'increments.\n'
                       '- Apply the principle to: An alerting system may need high precision at a '
                       'minimum workable recall.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Plot '
                       'precision and recall across decision scores and discuss a practical '
                       'operating point.\n'
                       '\n'
                       '## Why this matters\n'
                       'Choose a metric and threshold that reflects the actual costs of different '
                       'errors. This lesson focuses on **precision–recall curves and average '
                       'precision** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'A PR curve summarizes positive-class retrieval across thresholds; average '
                       'precision weights precision changes by recall increments.\n'
                       '\n'
                       '## Worked scenario\n'
                       'An alerting system may need high precision at a minimum workable recall. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Plot precision and recall across decision scores and discuss a practical '
                       'operating point. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Average precision is not necessarily identical to trapezoidal PR area. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.metrics import precision_recall_curve, '
                       'average_precision_score\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **precision–recall curves and average precision** in your own '
                       'words and answer: what would change in the worked scenario if you ignored '
                       'the boundary above?\n'
                       '\n'
                       '**Retain this idea:** A PR curve summarizes positive-class retrieval '
                       'across thresholds; average precision weights precision changes by recall '
                       'increments.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Precision–Recall Curves and Average Precision — hands-on activity',
                'description': 'Plot precision and recall across decision scores and discuss a '
                               'practical operating point. Deliver a short notebook, annotated '
                               'example or written calculation with your result and '
                               'interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-17']},
               {'title': 'Precision–Recall Curves and Average Precision — critical reasoning',
                'description': 'Consider this boundary: Average precision is not necessarily '
                               'identical to trapezoidal PR area. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Precision–Recall Curves and Average Precision — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Precision–Recall Curves and Average Precision?',
                         'options': ['Accuracy proves minority-class recall is high.',
                                     'A PR curve summarizes positive-class retrieval across '
                                     'thresholds; average precision weights precision changes by '
                                     'recall increments.',
                                     'The default threshold is optimal for every business.',
                                     'ROC AUC always determines the right alert threshold.'],
                         'correct': 1,
                         'explanation': 'A PR curve summarizes positive-class retrieval across '
                                        'thresholds; average precision weights precision changes '
                                        'by recall increments. In the worked scenario: An alerting '
                                        'system may need high precision at a minimum workable '
                                        'recall.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Precision–Recall Curves and Average Precision?',
                         'options': ['Construct a confusion scenario and choose an '
                                     'application-appropriate goal.',
                                     'Compute precision, recall and F1 from a small hand-written '
                                     'matrix.',
                                     'Compare two thresholds and document the review capacity they '
                                     'require.',
                                     'Plot precision and recall across decision scores and discuss '
                                     'a practical operating point.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Plot precision and recall '
                                        'across decision scores and discuss a practical operating '
                                        'point.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Average precision is not necessarily '
                                     'identical to trapezoidal PR area.',
                         'type': 'open'}],
          'passing_score': 70}}
