"""M12.L04 — Nonlinear Feature Transformations.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 232–235. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M12.L04"
MODULE_ORDER = 12
MODULE_TITLE = 'Nonlinear Feature Engineering'
MODULE_DESCRIPTION = 'Create and assess bins, interactions, polynomial terms and monotonic transforms.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '232–235'

TOPIC = {'title': 'Nonlinear Feature Transformations',
 'slug': 'ml-foundations-m12-l04',
 'description': 'Log-like and other transformations can change skew and make linear patterns '
                'easier to model; choose a transform valid for the input domain.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-12'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Nonlinear Feature Transformations',
            'content': '# Nonlinear Feature Transformations\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M12.L04 | '
                       '**Module:** Nonlinear Feature Engineering\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 232–235. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Log-like and other transformations can change skew and make '
                       'linear patterns easier to model; choose a transform valid for the input '
                       'domain.\n'
                       '- Apply the principle to: A highly right-skewed positive count may become '
                       'more symmetric after log1p.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Inspect before/after distributions and identify invalid values.\n'
                       '\n'
                       '## Why this matters\n'
                       'Create and assess bins, interactions, polynomial terms and monotonic '
                       'transforms. This lesson focuses on **nonlinear feature transformations** '
                       'so you can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Log-like and other transformations can change skew and make linear '
                       'patterns easier to model; choose a transform valid for the input domain.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A highly right-skewed positive count may become more symmetric after '
                       'log1p. Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Inspect before/after distributions and identify invalid values. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Plain log cannot accept nonpositive values. Explain how your method '
                       'respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **nonlinear feature transformations** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Log-like and other transformations can change skew '
                       'and make linear patterns easier to model; choose a transform valid for the '
                       'input domain.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Nonlinear Feature Transformations — hands-on activity',
                'description': 'Inspect before/after distributions and identify invalid values. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-12']},
               {'title': 'Nonlinear Feature Transformations — critical reasoning',
                'description': 'Consider this boundary: Plain log cannot accept nonpositive '
                               'values. Explain a failure mode if it is ignored and the safeguard '
                               'you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Nonlinear Feature Transformations — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Nonlinear Feature Transformations?',
                         'options': ['Log-like and other transformations can change skew and make '
                                     'linear patterns easier to model; choose a transform valid '
                                     'for the input domain.',
                                     'Polynomial expansion cannot overfit.',
                                     'Input-domain constraints can be ignored when applying '
                                     'logarithms.',
                                     'Interaction coefficients directly prove causality.'],
                         'correct': 0,
                         'explanation': 'Log-like and other transformations can change skew and '
                                        'make linear patterns easier to model; choose a transform '
                                        'valid for the input domain. In the worked scenario: A '
                                        'highly right-skewed positive count may become more '
                                        'symmetric after log1p.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Nonlinear Feature Transformations?',
                         'options': ['Create bins and compare a baseline with a binned '
                                     'representation.',
                                     'Construct one interaction term and interpret its coefficient '
                                     'conditionally.',
                                     'Inspect before/after distributions and identify invalid '
                                     'values.',
                                     'Compare degrees 1 and 2 inside a validation-safe pipeline.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Inspect before/after '
                                        'distributions and identify invalid values.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Plain log cannot accept nonpositive '
                                     'values.',
                         'type': 'open'}],
          'passing_score': 70}}
