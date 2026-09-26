"""M17.L03 — Decision Scores and Thresholds.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 285–289. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M17.L03"
MODULE_ORDER = 17
MODULE_TITLE = 'Binary Classification Evaluation'
MODULE_DESCRIPTION = 'Choose a metric and threshold that reflects the actual costs of different errors.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '285–289'

TOPIC = {'title': 'Decision Scores and Thresholds',
 'slug': 'ml-foundations-m17-l03',
 'description': 'Changing a decision threshold trades precision for recall; select it with '
                'development data, not the final test set.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-17'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Decision Scores and Thresholds',
            'content': '# Decision Scores and Thresholds\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M17.L03 | '
                       '**Module:** Binary Classification Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 285–289. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Changing a decision threshold trades precision for recall; '
                       'select it with development data, not the final test set.\n'
                       '- Apply the principle to: Lowering a fraud alert threshold catches more '
                       'cases but also sends more false alarms.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare two thresholds and document the review capacity they require.\n'
                       '\n'
                       '## Why this matters\n'
                       'Choose a metric and threshold that reflects the actual costs of different '
                       'errors. This lesson focuses on **decision scores and thresholds** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Changing a decision threshold trades precision for recall; select it with '
                       'development data, not the final test set.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Lowering a fraud alert threshold catches more cases but also sends more '
                       'false alarms. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare two thresholds and document the review capacity they require. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'The default threshold is not universally optimal. Explain how your method '
                       'respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **decision scores and thresholds** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Changing a decision threshold trades precision for '
                       'recall; select it with development data, not the final test set.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Decision Scores and Thresholds — hands-on activity',
                'description': 'Compare two thresholds and document the review capacity they '
                               'require. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-17']},
               {'title': 'Decision Scores and Thresholds — critical reasoning',
                'description': 'Consider this boundary: The default threshold is not universally '
                               'optimal. Explain a failure mode if it is ignored and the safeguard '
                               'you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Decision Scores and Thresholds — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Decision Scores and Thresholds?',
                         'options': ['Changing a decision threshold trades precision for recall; '
                                     'select it with development data, not the final test set.',
                                     'Accuracy proves minority-class recall is high.',
                                     'The default threshold is optimal for every business.',
                                     'ROC AUC always determines the right alert threshold.'],
                         'correct': 0,
                         'explanation': 'Changing a decision threshold trades precision for '
                                        'recall; select it with development data, not the final '
                                        'test set. In the worked scenario: Lowering a fraud alert '
                                        'threshold catches more cases but also sends more false '
                                        'alarms.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Decision Scores and Thresholds?',
                         'options': ['Construct a confusion scenario and choose an '
                                     'application-appropriate goal.',
                                     'Compute precision, recall and F1 from a small hand-written '
                                     'matrix.',
                                     'Compare two thresholds and document the review capacity they '
                                     'require.',
                                     'Plot precision and recall across decision scores and discuss '
                                     'a practical operating point.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Compare two thresholds and '
                                        'document the review capacity they require.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? The default threshold is not '
                                     'universally optimal.',
                         'type': 'open'}],
          'passing_score': 70}}
