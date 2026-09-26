"""M12.L02 — Interaction Features.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 224–226. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M12.L02"
MODULE_ORDER = 12
MODULE_TITLE = 'Nonlinear Feature Engineering'
MODULE_DESCRIPTION = 'Create and assess bins, interactions, polynomial terms and monotonic transforms.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '224–226'

TOPIC = {'title': 'Interaction Features',
 'slug': 'ml-foundations-m12-l02',
 'description': "Interaction terms let one feature modify another's contribution, expanding "
                'otherwise additive linear models.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-12'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Interaction Features',
            'content': '# Interaction Features\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M12.L02 | '
                       '**Module:** Nonlinear Feature Engineering\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 224–226. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       "- Explain: Interaction terms let one feature modify another's "
                       'contribution, expanding otherwise additive linear models.\n'
                       '- Apply the principle to: The effect of property area may differ with '
                       'neighborhood through an area-times-neighborhood interaction.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Construct one interaction term and interpret its coefficient '
                       'conditionally.\n'
                       '\n'
                       '## Why this matters\n'
                       'Create and assess bins, interactions, polynomial terms and monotonic '
                       'transforms. This lesson focuses on **interaction features** so you can '
                       'make an explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       "Interaction terms let one feature modify another's contribution, expanding "
                       'otherwise additive linear models.\n'
                       '\n'
                       '## Worked scenario\n'
                       'The effect of property area may differ with neighborhood through an '
                       'area-times-neighborhood interaction. Before claiming that a method works, '
                       'check what data it uses, which predictions or patterns it produces, and '
                       'how those outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Construct one interaction term and interpret its coefficient '
                       'conditionally. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'An interaction term should not be interpreted as a standalone causal '
                       'effect. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **interaction features** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       "**Retain this idea:** Interaction terms let one feature modify another's "
                       'contribution, expanding otherwise additive linear models.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'Interaction Features — hands-on activity',
                'description': 'Construct one interaction term and interpret its coefficient '
                               'conditionally. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-12']},
               {'title': 'Interaction Features — critical reasoning',
                'description': 'Consider this boundary: An interaction term should not be '
                               'interpreted as a standalone causal effect. Explain a failure mode '
                               'if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Interaction Features — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Interaction Features?',
                         'options': ['Polynomial expansion cannot overfit.',
                                     'Input-domain constraints can be ignored when applying '
                                     'logarithms.',
                                     "Interaction terms let one feature modify another's "
                                     'contribution, expanding otherwise additive linear models.',
                                     'Interaction coefficients directly prove causality.'],
                         'correct': 2,
                         'explanation': "Interaction terms let one feature modify another's "
                                        'contribution, expanding otherwise additive linear models. '
                                        'In the worked scenario: The effect of property area may '
                                        'differ with neighborhood through an '
                                        'area-times-neighborhood interaction.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Interaction Features?',
                         'options': ['Construct one interaction term and interpret its coefficient '
                                     'conditionally.',
                                     'Create bins and compare a baseline with a binned '
                                     'representation.',
                                     'Compare degrees 1 and 2 inside a validation-safe pipeline.',
                                     'Inspect before/after distributions and identify invalid '
                                     'values.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Construct one interaction term '
                                        'and interpret its coefficient conditionally.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? An interaction term should not be '
                                     'interpreted as a standalone causal effect.',
                         'type': 'open'}],
          'passing_score': 70}}
