"""M17.L01 — Imbalanced Classes and Baselines.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 275–279. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M17.L01"
MODULE_ORDER = 17
MODULE_TITLE = 'Binary Classification Evaluation'
MODULE_DESCRIPTION = 'Choose a metric and threshold that reflects the actual costs of different errors.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '275–279'

TOPIC = {'title': 'Imbalanced Classes and Baselines',
 'slug': 'ml-foundations-m17-l01',
 'description': 'Accuracy alone may hide failure on rare classes; compare against a majority-class '
                'dummy baseline and identify false-positive costs.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-17'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Imbalanced Classes and Baselines',
            'content': '# Imbalanced Classes and Baselines\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M17.L01 | '
                       '**Module:** Binary Classification Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 275–279. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Accuracy alone may hide failure on rare classes; compare '
                       'against a majority-class dummy baseline and identify false-positive '
                       'costs.\n'
                       '- Apply the principle to: A 99% negative dataset rewards an '
                       'always-negative classifier with 99% accuracy and zero positive recall.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Construct a confusion scenario and choose an application-appropriate '
                       'goal.\n'
                       '\n'
                       '## Why this matters\n'
                       'Choose a metric and threshold that reflects the actual costs of different '
                       'errors. This lesson focuses on **imbalanced classes and baselines** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Accuracy alone may hide failure on rare classes; compare against a '
                       'majority-class dummy baseline and identify false-positive costs.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A 99% negative dataset rewards an always-negative classifier with 99% '
                       'accuracy and zero positive recall. Before claiming that a method works, '
                       'check what data it uses, which predictions or patterns it produces, and '
                       'how those outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Construct a confusion scenario and choose an application-appropriate goal. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A high accuracy score does not imply detection of the minority class. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **imbalanced classes and baselines** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Accuracy alone may hide failure on rare classes; '
                       'compare against a majority-class dummy baseline and identify '
                       'false-positive costs.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Imbalanced Classes and Baselines — hands-on activity',
                'description': 'Construct a confusion scenario and choose an '
                               'application-appropriate goal. Deliver a short notebook, annotated '
                               'example or written calculation with your result and '
                               'interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-17']},
               {'title': 'Imbalanced Classes and Baselines — critical reasoning',
                'description': 'Consider this boundary: A high accuracy score does not imply '
                               'detection of the minority class. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Imbalanced Classes and Baselines — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Imbalanced Classes and Baselines?',
                         'options': ['Accuracy proves minority-class recall is high.',
                                     'The default threshold is optimal for every business.',
                                     'Accuracy alone may hide failure on rare classes; compare '
                                     'against a majority-class dummy baseline and identify '
                                     'false-positive costs.',
                                     'ROC AUC always determines the right alert threshold.'],
                         'correct': 2,
                         'explanation': 'Accuracy alone may hide failure on rare classes; compare '
                                        'against a majority-class dummy baseline and identify '
                                        'false-positive costs. In the worked scenario: A 99% '
                                        'negative dataset rewards an always-negative classifier '
                                        'with 99% accuracy and zero positive recall.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Imbalanced Classes and Baselines?',
                         'options': ['Construct a confusion scenario and choose an '
                                     'application-appropriate goal.',
                                     'Compute precision, recall and F1 from a small hand-written '
                                     'matrix.',
                                     'Compare two thresholds and document the review capacity they '
                                     'require.',
                                     'Plot precision and recall across decision scores and discuss '
                                     'a practical operating point.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Construct a confusion scenario '
                                        'and choose an application-appropriate goal.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A high accuracy score does not imply '
                                     'detection of the minority class.',
                         'type': 'open'}],
          'passing_score': 70}}
