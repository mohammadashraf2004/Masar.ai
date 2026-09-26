"""M11.L03 — Numeric Codes and Consistent Schema.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 217–219. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M11.L03"
MODULE_ORDER = 11
MODULE_TITLE = 'Categorical Data Representation'
MODULE_DESCRIPTION = 'Encode qualitative variables while preventing category drift and evaluation leakage.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '217–219'

TOPIC = {'title': 'Numeric Codes and Consistent Schema',
 'slug': 'ml-foundations-m11-l03',
 'description': 'Numeric-looking categorical values still require semantic inspection; maintain '
                'stable feature order across train and inference.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-11'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Numeric Codes and Consistent Schema',
            'content': '# Numeric Codes and Consistent Schema\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M11.L03 | '
                       '**Module:** Categorical Data Representation\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 217–219. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Numeric-looking categorical values still require semantic '
                       'inspection; maintain stable feature order across train and inference.\n'
                       '- Apply the principle to: A postal code is an identifier rather than a '
                       'continuous geographic measurement.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Diagnose a numeric-code error and document an inference-time category '
                       'policy.\n'
                       '\n'
                       '## Why this matters\n'
                       'Encode qualitative variables while preventing category drift and '
                       'evaluation leakage. This lesson focuses on **numeric codes and consistent '
                       'schema** so you can make an explicit choice rather than blindly applying a '
                       'library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Numeric-looking categorical values still require semantic inspection; '
                       'maintain stable feature order across train and inference.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A postal code is an identifier rather than a continuous geographic '
                       'measurement. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Diagnose a numeric-code error and document an inference-time category '
                       'policy. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Treating city code 10 as twice city code 5 creates fake numerical meaning. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **numeric codes and consistent schema** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Numeric-looking categorical values still require '
                       'semantic inspection; maintain stable feature order across train and '
                       'inference.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Numeric Codes and Consistent Schema — hands-on activity',
                'description': 'Diagnose a numeric-code error and document an inference-time '
                               'category policy. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-11']},
               {'title': 'Numeric Codes and Consistent Schema — critical reasoning',
                'description': 'Consider this boundary: Treating city code 10 as twice city code 5 '
                               'creates fake numerical meaning. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Numeric Codes and Consistent Schema — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Numeric '
                                     'Codes and Consistent Schema?',
                         'options': ['Integer-coded categories inherently have equal numerical '
                                     'spacing.',
                                     'The final test set should define training categories.',
                                     'Numeric-looking categorical values still require semantic '
                                     'inspection; maintain stable feature order across train and '
                                     'inference.',
                                     'New categories never appear after deployment.'],
                         'correct': 2,
                         'explanation': 'Numeric-looking categorical values still require semantic '
                                        'inspection; maintain stable feature order across train '
                                        'and inference. In the worked scenario: A postal code is '
                                        'an identifier rather than a continuous geographic '
                                        'measurement.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Numeric Codes and Consistent Schema?',
                         'options': ['Diagnose a numeric-code error and document an inference-time '
                                     'category policy.',
                                     'Inspect a mixed table and classify numeric, nominal and '
                                     'ordinal columns.',
                                     'One-hot encode a small training table and transform an '
                                     'unseen-category example.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Diagnose a numeric-code error '
                                        'and document an inference-time category policy.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Treating city code 10 as twice city '
                                     'code 5 creates fake numerical meaning.',
                         'type': 'open'}],
          'passing_score': 70}}
