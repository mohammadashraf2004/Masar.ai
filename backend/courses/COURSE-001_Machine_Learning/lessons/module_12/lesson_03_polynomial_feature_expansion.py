"""M12.L03 — Polynomial Feature Expansion.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 226–232. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M12.L03"
MODULE_ORDER = 12
MODULE_TITLE = 'Nonlinear Feature Engineering'
MODULE_DESCRIPTION = 'Create and assess bins, interactions, polynomial terms and monotonic transforms.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '226–232'

TOPIC = {'title': 'Polynomial Feature Expansion',
 'slug': 'ml-foundations-m12-l03',
 'description': 'PolynomialFeatures expands numerical variables to powers and interactions; use '
                'regularization and CV to control complexity.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-12'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Polynomial Feature Expansion',
            'content': '# Polynomial Feature Expansion\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M12.L03 | '
                       '**Module:** Nonlinear Feature Engineering\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 226–232. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: PolynomialFeatures expands numerical variables to powers and '
                       'interactions; use regularization and CV to control complexity.\n'
                       '- Apply the principle to: An x-squared term allows a linear regressor to '
                       'fit a curved relation.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare degrees 1 and 2 inside a validation-safe pipeline.\n'
                       '\n'
                       '## Why this matters\n'
                       'Create and assess bins, interactions, polynomial terms and monotonic '
                       'transforms. This lesson focuses on **polynomial feature expansion** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'PolynomialFeatures expands numerical variables to powers and interactions; '
                       'use regularization and CV to control complexity.\n'
                       '\n'
                       '## Worked scenario\n'
                       'An x-squared term allows a linear regressor to fit a curved relation. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare degrees 1 and 2 inside a validation-safe pipeline. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'High degrees can increase feature count and overfitting dramatically. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.preprocessing import PolynomialFeatures\n'
                       'features = PolynomialFeatures(degree=2, include_bias=False)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **polynomial feature expansion** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** PolynomialFeatures expands numerical variables to '
                       'powers and interactions; use regularization and CV to control '
                       'complexity.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Polynomial Feature Expansion — hands-on activity',
                'description': 'Compare degrees 1 and 2 inside a validation-safe pipeline. Deliver '
                               'a short notebook, annotated example or written calculation with '
                               'your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-12']},
               {'title': 'Polynomial Feature Expansion — critical reasoning',
                'description': 'Consider this boundary: High degrees can increase feature count '
                               'and overfitting dramatically. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Polynomial Feature Expansion — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Polynomial Feature Expansion?',
                         'options': ['Polynomial expansion cannot overfit.',
                                     'Input-domain constraints can be ignored when applying '
                                     'logarithms.',
                                     'Interaction coefficients directly prove causality.',
                                     'PolynomialFeatures expands numerical variables to powers and '
                                     'interactions; use regularization and CV to control '
                                     'complexity.'],
                         'correct': 3,
                         'explanation': 'PolynomialFeatures expands numerical variables to powers '
                                        'and interactions; use regularization and CV to control '
                                        'complexity. In the worked scenario: An x-squared term '
                                        'allows a linear regressor to fit a curved relation.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Polynomial Feature Expansion?',
                         'options': ['Create bins and compare a baseline with a binned '
                                     'representation.',
                                     'Compare degrees 1 and 2 inside a validation-safe pipeline.',
                                     'Construct one interaction term and interpret its coefficient '
                                     'conditionally.',
                                     'Inspect before/after distributions and identify invalid '
                                     'values.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Compare degrees 1 and 2 inside '
                                        'a validation-safe pipeline.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? High degrees can increase feature '
                                     'count and overfitting dramatically.',
                         'type': 'open'}],
          'passing_score': 70}}
