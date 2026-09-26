"""M15.L03 — Stratified and Alternative Splitters.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 254–258. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M15.L03"
MODULE_ORDER = 15
MODULE_TITLE = 'Reliable Model Evaluation'
MODULE_DESCRIPTION = 'Separate evaluation roles and choose cross-validation consistent with the sampling process.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '254–258'

TOPIC = {'title': 'Stratified and Alternative Splitters',
 'slug': 'ml-foundations-m15-l03',
 'description': 'Stratification preserves class proportions approximately, while KFold, '
                'leave-one-out and shuffle splits have different costs and assumptions.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-15'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Stratified and Alternative Splitters',
            'content': '# Stratified and Alternative Splitters\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M15.L03 | '
                       '**Module:** Reliable Model Evaluation\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 254–258. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Stratification preserves class proportions approximately, while '
                       'KFold, leave-one-out and shuffle splits have different costs and '
                       'assumptions.\n'
                       '- Apply the principle to: A rare class might disappear from a small '
                       'unstratified validation fold.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Choose a splitter for a small imbalanced dataset and justify it.\n'
                       '\n'
                       '## Why this matters\n'
                       'Separate evaluation roles and choose cross-validation consistent with the '
                       'sampling process. This lesson focuses on **stratified and alternative '
                       'splitters** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Stratification preserves class proportions approximately, while KFold, '
                       'leave-one-out and shuffle splits have different costs and assumptions.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A rare class might disappear from a small unstratified validation fold. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Choose a splitter for a small imbalanced dataset and justify it. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Stratification does not correct label leakage or group dependence. Explain '
                       'how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.model_selection import StratifiedKFold\n'
                       'cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **stratified and alternative splitters** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Stratification preserves class proportions '
                       'approximately, while KFold, leave-one-out and shuffle splits have '
                       'different costs and assumptions.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Stratified and Alternative Splitters — hands-on activity',
                'description': 'Choose a splitter for a small imbalanced dataset and justify it. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-15']},
               {'title': 'Stratified and Alternative Splitters — critical reasoning',
                'description': 'Consider this boundary: Stratification does not correct label '
                               'leakage or group dependence. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Stratified and Alternative Splitters — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Stratified and Alternative Splitters?',
                         'options': ['The final test set is appropriate for repeated tuning.',
                                     'Stratification prevents all forms of leakage.',
                                     'Stratification preserves class proportions approximately, '
                                     'while KFold, leave-one-out and shuffle splits have different '
                                     'costs and assumptions.',
                                     'Group identity can be ignored when rows are correlated.'],
                         'correct': 2,
                         'explanation': 'Stratification preserves class proportions approximately, '
                                        'while KFold, leave-one-out and shuffle splits have '
                                        'different costs and assumptions. In the worked scenario: '
                                        'A rare class might disappear from a small unstratified '
                                        'validation fold.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Stratified and Alternative Splitters?',
                         'options': ['Choose a splitter for a small imbalanced dataset and justify '
                                     'it.',
                                     'Draw data-flow boundaries for training, tuning and final '
                                     'reporting.',
                                     'Run cross_val_score and report mean and individual fold '
                                     'scores.',
                                     'Audit overlap of group IDs across folds and document the '
                                     'constraint.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Choose a splitter for a small '
                                        'imbalanced dataset and justify it.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Stratification does not correct label '
                                     'leakage or group dependence.',
                         'type': 'open'}],
          'passing_score': 70}}
