"""M04.L02 — Feature Importance and Extrapolation.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 77–83. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M04.L02"
MODULE_ORDER = 4
MODULE_TITLE = 'Decision Trees & Ensembles'
MODULE_DESCRIPTION = 'Interpret tree decisions, compare ensemble methods, and recognize non-extrapolation and attribution limits.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '77–83'

TOPIC = {'title': 'Feature Importance and Extrapolation',
 'slug': 'ml-foundations-m04-l02',
 'description': 'Tree importance summarizes training split usage, not causation; ordinary trees '
                'and forests predict using observed target patterns and extrapolate poorly.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-04'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Feature Importance and Extrapolation',
            'content': '# Feature Importance and Extrapolation\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M04.L02 | '
                       '**Module:** Decision Trees & Ensembles\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 77–83. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Tree importance summarizes training split usage, not causation; '
                       'ordinary trees and forests predict using observed target patterns and '
                       'extrapolate poorly.\n'
                       '- Apply the principle to: A tree trained on earlier price levels cannot '
                       'simply extend a trend indefinitely.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare feature importances with a held-out performance and extrapolation '
                       'check.\n'
                       '\n'
                       '## Why this matters\n'
                       'Interpret tree decisions, compare ensemble methods, and recognize '
                       'non-extrapolation and attribution limits. This lesson focuses on **feature '
                       'importance and extrapolation** so you can make an explicit choice rather '
                       'than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Tree importance summarizes training split usage, not causation; ordinary '
                       'trees and forests predict using observed target patterns and extrapolate '
                       'poorly.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A tree trained on earlier price levels cannot simply extend a trend '
                       'indefinitely. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare feature importances with a held-out performance and extrapolation '
                       'check. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'High impurity importance does not prove a feature causes the outcome. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **feature importance and extrapolation** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Tree importance summarizes training split usage, not '
                       'causation; ordinary trees and forests predict using observed target '
                       'patterns and extrapolate poorly.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Feature Importance and Extrapolation — hands-on activity',
                'description': 'Compare feature importances with a held-out performance and '
                               'extrapolation check. Deliver a short notebook, annotated example '
                               'or written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-04']},
               {'title': 'Feature Importance and Extrapolation — critical reasoning',
                'description': 'Consider this boundary: High impurity importance does not prove a '
                               'feature causes the outcome. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Feature Importance and Extrapolation — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Feature '
                                     'Importance and Extrapolation?',
                         'options': ['Feature importance proves causal influence.',
                                     'A single unrestricted tree cannot overfit.',
                                     'Tree importance summarizes training split usage, not '
                                     'causation; ordinary trees and forests predict using observed '
                                     'target patterns and extrapolate poorly.',
                                     'Trees automatically extrapolate continuous trends.'],
                         'correct': 2,
                         'explanation': 'Tree importance summarizes training split usage, not '
                                        'causation; ordinary trees and forests predict using '
                                        'observed target patterns and extrapolate poorly. In the '
                                        'worked scenario: A tree trained on earlier price levels '
                                        'cannot simply extend a trend indefinitely.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Feature Importance and Extrapolation?',
                         'options': ['Compare feature importances with a held-out performance and '
                                     'extrapolation check.',
                                     'Fit a small tree, visualize paths and explain a prediction.',
                                     'Fit a forest and compare it with a single tree using the '
                                     'same split.',
                                     'Compare boosted-tree settings with a forest on validation '
                                     'data.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Compare feature importances '
                                        'with a held-out performance and extrapolation check.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? High impurity importance does not '
                                     'prove a feature causes the outcome.',
                         'type': 'open'}],
          'passing_score': 70}}
