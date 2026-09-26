"""M17.L05 — ROC Curves and AUC.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 292–296. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M17.L05"
MODULE_ORDER = 17
MODULE_TITLE = 'Binary Classification Evaluation'
MODULE_DESCRIPTION = 'Choose a metric and threshold that reflects the actual costs of different errors.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '292–296'

TOPIC = {'title': 'ROC Curves and AUC',
 'slug': 'ml-foundations-m17-l05',
 'description': 'ROC plots true-positive rate against false-positive rate across thresholds; AUC '
                'describes ranking discrimination, not a deployment threshold.',
 'order': 5,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-17'],
 'prerequisite_ids': [],
 'lesson': {'title': 'ROC Curves and AUC',
            'content': '# ROC Curves and AUC\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M17.L05 | '
                       '**Module:** Binary Classification Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 292–296. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: ROC plots true-positive rate against false-positive rate across '
                       'thresholds; AUC describes ranking discrimination, not a deployment '
                       'threshold.\n'
                       '- Apply the principle to: Two classifiers can have similar ROC AUC but '
                       'different precision under rare positives.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare ROC AUC and PR evidence on imbalanced data.\n'
                       '\n'
                       '## Why this matters\n'
                       'Choose a metric and threshold that reflects the actual costs of different '
                       'errors. This lesson focuses on **roc curves and auc** so you can make an '
                       'explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'ROC plots true-positive rate against false-positive rate across '
                       'thresholds; AUC describes ranking discrimination, not a deployment '
                       'threshold.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Two classifiers can have similar ROC AUC but different precision under '
                       'rare positives. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare ROC AUC and PR evidence on imbalanced data. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'ROC AUC alone does not identify a suitable action threshold. Explain how '
                       'your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.metrics import roc_curve, roc_auc_score\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **roc curves and auc** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** ROC plots true-positive rate against false-positive '
                       'rate across thresholds; AUC describes ranking discrimination, not a '
                       'deployment threshold.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'ROC Curves and AUC — hands-on activity',
                'description': 'Compare ROC AUC and PR evidence on imbalanced data. Deliver a '
                               'short notebook, annotated example or written calculation with your '
                               'result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-17']},
               {'title': 'ROC Curves and AUC — critical reasoning',
                'description': 'Consider this boundary: ROC AUC alone does not identify a suitable '
                               'action threshold. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'ROC Curves and AUC — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of ROC '
                                     'Curves and AUC?',
                         'options': ['Accuracy proves minority-class recall is high.',
                                     'The default threshold is optimal for every business.',
                                     'ROC plots true-positive rate against false-positive rate '
                                     'across thresholds; AUC describes ranking discrimination, not '
                                     'a deployment threshold.',
                                     'ROC AUC always determines the right alert threshold.'],
                         'correct': 2,
                         'explanation': 'ROC plots true-positive rate against false-positive rate '
                                        'across thresholds; AUC describes ranking discrimination, '
                                        'not a deployment threshold. In the worked scenario: Two '
                                        'classifiers can have similar ROC AUC but different '
                                        'precision under rare positives.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'ROC Curves and AUC?',
                         'options': ['Compare ROC AUC and PR evidence on imbalanced data.',
                                     'Construct a confusion scenario and choose an '
                                     'application-appropriate goal.',
                                     'Compute precision, recall and F1 from a small hand-written '
                                     'matrix.',
                                     'Compare two thresholds and document the review capacity they '
                                     'require.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Compare ROC AUC and PR evidence '
                                        'on imbalanced data.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? ROC AUC alone does not identify a '
                                     'suitable action threshold.',
                         'type': 'open'}],
          'passing_score': 70}}
