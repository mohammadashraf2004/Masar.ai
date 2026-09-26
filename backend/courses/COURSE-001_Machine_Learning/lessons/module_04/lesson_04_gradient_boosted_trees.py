"""M04.L04 — Gradient Boosted Trees.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 88–92. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M04.L04"
MODULE_ORDER = 4
MODULE_TITLE = 'Decision Trees & Ensembles'
MODULE_DESCRIPTION = 'Interpret tree decisions, compare ensemble methods, and recognize non-extrapolation and attribution limits.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '88–92'

TOPIC = {'title': 'Gradient Boosted Trees',
 'slug': 'ml-foundations-m04-l04',
 'description': 'Gradient boosting adds trees sequentially to reduce remaining predictive error; '
                'learning rate and depth affect fit and compute.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-04'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Gradient Boosted Trees',
            'content': '# Gradient Boosted Trees\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M04.L04 | '
                       '**Module:** Decision Trees & Ensembles\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 88–92. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Gradient boosting adds trees sequentially to reduce remaining '
                       'predictive error; learning rate and depth affect fit and compute.\n'
                       '- Apply the principle to: A small new tree adjusts errors left by earlier '
                       'ensemble stages.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare boosted-tree settings with a forest on validation data.\n'
                       '\n'
                       '## Why this matters\n'
                       'Interpret tree decisions, compare ensemble methods, and recognize '
                       'non-extrapolation and attribution limits. This lesson focuses on '
                       '**gradient boosted trees** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Gradient boosting adds trees sequentially to reduce remaining predictive '
                       'error; learning rate and depth affect fit and compute.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A small new tree adjusts errors left by earlier ensemble stages. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare boosted-tree settings with a forest on validation data. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'More boosting iterations can eventually overfit and cost more time. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.ensemble import GradientBoostingClassifier\n'
                       'classifier = GradientBoostingClassifier(random_state=42)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **gradient boosted trees** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Gradient boosting adds trees sequentially to reduce '
                       'remaining predictive error; learning rate and depth affect fit and '
                       'compute.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Gradient Boosted Trees — hands-on activity',
                'description': 'Compare boosted-tree settings with a forest on validation data. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-04']},
               {'title': 'Gradient Boosted Trees — critical reasoning',
                'description': 'Consider this boundary: More boosting iterations can eventually '
                               'overfit and cost more time. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Gradient Boosted Trees — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Gradient Boosted Trees?',
                         'options': ['Gradient boosting adds trees sequentially to reduce '
                                     'remaining predictive error; learning rate and depth affect '
                                     'fit and compute.',
                                     'Feature importance proves causal influence.',
                                     'A single unrestricted tree cannot overfit.',
                                     'Trees automatically extrapolate continuous trends.'],
                         'correct': 0,
                         'explanation': 'Gradient boosting adds trees sequentially to reduce '
                                        'remaining predictive error; learning rate and depth '
                                        'affect fit and compute. In the worked scenario: A small '
                                        'new tree adjusts errors left by earlier ensemble stages.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Gradient Boosted Trees?',
                         'options': ['Fit a small tree, visualize paths and explain a prediction.',
                                     'Compare feature importances with a held-out performance and '
                                     'extrapolation check.',
                                     'Compare boosted-tree settings with a forest on validation '
                                     'data.',
                                     'Fit a forest and compare it with a single tree using the '
                                     'same split.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Compare boosted-tree settings '
                                        'with a forest on validation data.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? More boosting iterations can '
                                     'eventually overfit and cost more time.',
                         'type': 'open'}],
          'passing_score': 70}}
