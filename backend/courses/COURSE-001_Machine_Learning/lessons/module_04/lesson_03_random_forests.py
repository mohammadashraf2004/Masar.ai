"""M04.L03 — Random Forests.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 83–88. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M04.L03"
MODULE_ORDER = 4
MODULE_TITLE = 'Decision Trees & Ensembles'
MODULE_DESCRIPTION = 'Interpret tree decisions, compare ensemble methods, and recognize non-extrapolation and attribution limits.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '83–88'

TOPIC = {'title': 'Random Forests',
 'slug': 'ml-foundations-m04-l03',
 'description': 'Random forests average randomized decision trees to reduce variance while '
                'retaining nonlinear interactions.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-04'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Random Forests',
            'content': '# Random Forests\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M04.L03 | '
                       '**Module:** Decision Trees & Ensembles\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 83–88. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Random forests average randomized decision trees to reduce '
                       'variance while retaining nonlinear interactions.\n'
                       '- Apply the principle to: Bootstrap samples and feature subsampling make '
                       'individual trees less correlated.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit a '
                       'forest and compare it with a single tree using the same split.\n'
                       '\n'
                       '## Why this matters\n'
                       'Interpret tree decisions, compare ensemble methods, and recognize '
                       'non-extrapolation and attribution limits. This lesson focuses on **random '
                       'forests** so you can make an explicit choice rather than blindly applying '
                       'a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Random forests average randomized decision trees to reduce variance while '
                       'retaining nonlinear interactions.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Bootstrap samples and feature subsampling make individual trees less '
                       'correlated. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit a forest and compare it with a single tree using the same split. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A larger forest does not fix invalid splits or test leakage. Explain how '
                       'your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.ensemble import RandomForestClassifier\n'
                       'classifier = RandomForestClassifier(n_estimators=100, random_state=42)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **random forests** in your own words and answer: what would change '
                       'in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Random forests average randomized decision trees to '
                       'reduce variance while retaining nonlinear interactions.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Random Forests — hands-on activity',
                'description': 'Fit a forest and compare it with a single tree using the same '
                               'split. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-04']},
               {'title': 'Random Forests — critical reasoning',
                'description': 'Consider this boundary: A larger forest does not fix invalid '
                               'splits or test leakage. Explain a failure mode if it is ignored '
                               'and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Random Forests — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Random '
                                     'Forests?',
                         'options': ['Feature importance proves causal influence.',
                                     'A single unrestricted tree cannot overfit.',
                                     'Trees automatically extrapolate continuous trends.',
                                     'Random forests average randomized decision trees to reduce '
                                     'variance while retaining nonlinear interactions.'],
                         'correct': 3,
                         'explanation': 'Random forests average randomized decision trees to '
                                        'reduce variance while retaining nonlinear interactions. '
                                        'In the worked scenario: Bootstrap samples and feature '
                                        'subsampling make individual trees less correlated.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Random Forests?',
                         'options': ['Fit a small tree, visualize paths and explain a prediction.',
                                     'Fit a forest and compare it with a single tree using the '
                                     'same split.',
                                     'Compare feature importances with a held-out performance and '
                                     'extrapolation check.',
                                     'Compare boosted-tree settings with a forest on validation '
                                     'data.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Fit a forest and compare it '
                                        'with a single tree using the same split.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A larger forest does not fix invalid '
                                     'splits or test leakage.',
                         'type': 'open'}],
          'passing_score': 70}}
