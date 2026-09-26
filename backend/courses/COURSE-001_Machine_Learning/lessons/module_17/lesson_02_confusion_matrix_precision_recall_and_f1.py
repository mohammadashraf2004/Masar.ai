"""M17.L02 — Confusion Matrix, Precision, Recall and F1.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 279–285. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M17.L02"
MODULE_ORDER = 17
MODULE_TITLE = 'Binary Classification Evaluation'
MODULE_DESCRIPTION = 'Choose a metric and threshold that reflects the actual costs of different errors.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '279–285'

TOPIC = {'title': 'Confusion Matrix, Precision, Recall and F1',
 'slug': 'ml-foundations-m17-l02',
 'description': 'A confusion matrix separates TP, FP, TN and FN; precision, recall and F1 '
                'summarize different trade-offs.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-17'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Confusion Matrix, Precision, Recall and F1',
            'content': '# Confusion Matrix, Precision, Recall and F1\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M17.L02 | '
                       '**Module:** Binary Classification Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 279–285. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: A confusion matrix separates TP, FP, TN and FN; precision, '
                       'recall and F1 summarize different trade-offs.\n'
                       '- Apply the principle to: Missed disease cases and false alarms correspond '
                       'to distinct matrix cells.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compute precision, recall and F1 from a small hand-written matrix.\n'
                       '\n'
                       '## Why this matters\n'
                       'Choose a metric and threshold that reflects the actual costs of different '
                       'errors. This lesson focuses on **confusion matrix, precision, recall and '
                       'f1** so you can make an explicit choice rather than blindly applying a '
                       'library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'A confusion matrix separates TP, FP, TN and FN; precision, recall and F1 '
                       'summarize different trade-offs.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Missed disease cases and false alarms correspond to distinct matrix cells. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compute precision, recall and F1 from a small hand-written matrix. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'F1 does not directly encode arbitrary business costs. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.metrics import confusion_matrix, classification_report\n'
                       'print(confusion_matrix(y_test, predictions))\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **confusion matrix, precision, recall and f1** in your own words '
                       'and answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** A confusion matrix separates TP, FP, TN and FN; '
                       'precision, recall and F1 summarize different trade-offs.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Confusion Matrix, Precision, Recall and F1 — hands-on activity',
                'description': 'Compute precision, recall and F1 from a small hand-written matrix. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-17']},
               {'title': 'Confusion Matrix, Precision, Recall and F1 — critical reasoning',
                'description': 'Consider this boundary: F1 does not directly encode arbitrary '
                               'business costs. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Confusion Matrix, Precision, Recall and F1 — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Confusion Matrix, Precision, Recall and F1?',
                         'options': ['Accuracy proves minority-class recall is high.',
                                     'The default threshold is optimal for every business.',
                                     'ROC AUC always determines the right alert threshold.',
                                     'A confusion matrix separates TP, FP, TN and FN; precision, '
                                     'recall and F1 summarize different trade-offs.'],
                         'correct': 3,
                         'explanation': 'A confusion matrix separates TP, FP, TN and FN; '
                                        'precision, recall and F1 summarize different trade-offs. '
                                        'In the worked scenario: Missed disease cases and false '
                                        'alarms correspond to distinct matrix cells.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Confusion Matrix, Precision, Recall and F1?',
                         'options': ['Construct a confusion scenario and choose an '
                                     'application-appropriate goal.',
                                     'Compute precision, recall and F1 from a small hand-written '
                                     'matrix.',
                                     'Compare two thresholds and document the review capacity they '
                                     'require.',
                                     'Plot precision and recall across decision scores and discuss '
                                     'a practical operating point.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Compute precision, recall and '
                                        'F1 from a small hand-written matrix.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? F1 does not directly encode arbitrary '
                                     'business costs.',
                         'type': 'open'}],
          'passing_score': 70}}
