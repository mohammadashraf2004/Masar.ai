"""M15.L04 — Group-Aware Validation.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 258–260. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M15.L04"
MODULE_ORDER = 15
MODULE_TITLE = 'Reliable Model Evaluation'
MODULE_DESCRIPTION = 'Separate evaluation roles and choose cross-validation consistent with the sampling process.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '258–260'

TOPIC = {'title': 'Group-Aware Validation',
 'slug': 'ml-foundations-m15-l04',
 'description': 'Use group-based splitting when several observations originate from the same '
                'patient, speaker or other entity.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-15'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Group-Aware Validation',
            'content': '# Group-Aware Validation\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M15.L04 | '
                       '**Module:** Reliable Model Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 258–260. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Use group-based splitting when several observations originate '
                       'from the same patient, speaker or other entity.\n'
                       '- Apply the principle to: A patient with five records must not appear in '
                       'both train and validation folds.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Audit '
                       'overlap of group IDs across folds and document the constraint.\n'
                       '\n'
                       '## Why this matters\n'
                       'Separate evaluation roles and choose cross-validation consistent with the '
                       'sampling process. This lesson focuses on **group-aware validation** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Use group-based splitting when several observations originate from the '
                       'same patient, speaker or other entity.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A patient with five records must not appear in both train and validation '
                       'folds. Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Audit overlap of group IDs across folds and document the constraint. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'StratifiedKFold alone does not enforce group separation. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.model_selection import GroupKFold\n'
                       'cv = GroupKFold(n_splits=5)\n'
                       '# Provide groups to the CV-enabled estimator using the API supported by '
                       'your environment.\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **group-aware validation** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Use group-based splitting when several observations '
                       'originate from the same patient, speaker or other entity.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Group-Aware Validation — hands-on activity',
                'description': 'Audit overlap of group IDs across folds and document the '
                               'constraint. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-15']},
               {'title': 'Group-Aware Validation — critical reasoning',
                'description': 'Consider this boundary: StratifiedKFold alone does not enforce '
                               'group separation. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Group-Aware Validation — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Group-Aware Validation?',
                         'options': ['The final test set is appropriate for repeated tuning.',
                                     'Stratification prevents all forms of leakage.',
                                     'Group identity can be ignored when rows are correlated.',
                                     'Use group-based splitting when several observations '
                                     'originate from the same patient, speaker or other entity.'],
                         'correct': 3,
                         'explanation': 'Use group-based splitting when several observations '
                                        'originate from the same patient, speaker or other entity. '
                                        'In the worked scenario: A patient with five records must '
                                        'not appear in both train and validation folds.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Group-Aware Validation?',
                         'options': ['Draw data-flow boundaries for training, tuning and final '
                                     'reporting.',
                                     'Audit overlap of group IDs across folds and document the '
                                     'constraint.',
                                     'Run cross_val_score and report mean and individual fold '
                                     'scores.',
                                     'Choose a splitter for a small imbalanced dataset and justify '
                                     'it.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Audit overlap of group IDs '
                                        'across folds and document the constraint.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? StratifiedKFold alone does not enforce '
                                     'group separation.',
                         'type': 'open'}],
          'passing_score': 70}}
