"""M12.L01 — Binning Continuous Variables.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 220–224. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M12.L01"
MODULE_ORDER = 12
MODULE_TITLE = 'Nonlinear Feature Engineering'
MODULE_DESCRIPTION = 'Create and assess bins, interactions, polynomial terms and monotonic transforms.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '220–224'

TOPIC = {'title': 'Binning Continuous Variables',
 'slug': 'ml-foundations-m12-l01',
 'description': 'Binning replaces continuous values with intervals and can expose threshold-like '
                'effects; bin edges should be established using development data.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-12'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Binning Continuous Variables',
            'content': '# Binning Continuous Variables\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M12.L01 | '
                       '**Module:** Nonlinear Feature Engineering\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 220–224. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Binning replaces continuous values with intervals and can '
                       'expose threshold-like effects; bin edges should be established using '
                       'development data.\n'
                       '- Apply the principle to: Age bands can help a linear model represent a '
                       'non-smooth response.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Create bins and compare a baseline with a binned representation.\n'
                       '\n'
                       '## Why this matters\n'
                       'Create and assess bins, interactions, polynomial terms and monotonic '
                       'transforms. This lesson focuses on **binning continuous variables** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Binning replaces continuous values with intervals and can expose '
                       'threshold-like effects; bin edges should be established using development '
                       'data.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Age bands can help a linear model represent a non-smooth response. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Create bins and compare a baseline with a binned representation. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Binning always loses some within-bin numeric detail. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **binning continuous variables** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Binning replaces continuous values with intervals '
                       'and can expose threshold-like effects; bin edges should be established '
                       'using development data.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Binning Continuous Variables — hands-on activity',
                'description': 'Create bins and compare a baseline with a binned representation. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-12']},
               {'title': 'Binning Continuous Variables — critical reasoning',
                'description': 'Consider this boundary: Binning always loses some within-bin '
                               'numeric detail. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Binning Continuous Variables — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Binning '
                                     'Continuous Variables?',
                         'options': ['Polynomial expansion cannot overfit.',
                                     'Binning replaces continuous values with intervals and can '
                                     'expose threshold-like effects; bin edges should be '
                                     'established using development data.',
                                     'Input-domain constraints can be ignored when applying '
                                     'logarithms.',
                                     'Interaction coefficients directly prove causality.'],
                         'correct': 1,
                         'explanation': 'Binning replaces continuous values with intervals and can '
                                        'expose threshold-like effects; bin edges should be '
                                        'established using development data. In the worked '
                                        'scenario: Age bands can help a linear model represent a '
                                        'non-smooth response.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Binning Continuous Variables?',
                         'options': ['Construct one interaction term and interpret its coefficient '
                                     'conditionally.',
                                     'Compare degrees 1 and 2 inside a validation-safe pipeline.',
                                     'Inspect before/after distributions and identify invalid '
                                     'values.',
                                     'Create bins and compare a baseline with a binned '
                                     'representation.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Create bins and compare a '
                                        'baseline with a binned representation.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Binning always loses some within-bin '
                                     'numeric detail.',
                         'type': 'open'}],
          'passing_score': 70}}
