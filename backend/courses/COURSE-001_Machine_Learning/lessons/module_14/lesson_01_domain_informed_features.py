"""M14.L01 — Domain-Informed Features.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 242–243. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M14.L01"
MODULE_ORDER = 14
MODULE_TITLE = 'Domain Knowledge & Temporal Features'
MODULE_DESCRIPTION = 'Use domain transformations while respecting information availability and chronology.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '242–243'

TOPIC = {'title': 'Domain-Informed Features',
 'slug': 'ml-foundations-m14-l01',
 'description': 'Useful representations can require domain understanding; derive features from '
                'information genuinely available at prediction time.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-14'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Domain-Informed Features',
            'content': '# Domain-Informed Features\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M14.L01 | '
                       '**Module:** Domain Knowledge & Temporal Features\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 242–243. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Useful representations can require domain understanding; derive '
                       'features from information genuinely available at prediction time.\n'
                       '- Apply the principle to: Price per area is invalid as an input when '
                       'predicting that same price, but floor area itself may help.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Propose features for a problem and document their availability at '
                       'inference.\n'
                       '\n'
                       '## Why this matters\n'
                       'Use domain transformations while respecting information availability and '
                       'chronology. This lesson focuses on **domain-informed features** so you can '
                       'make an explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Useful representations can require domain understanding; derive features '
                       'from information genuinely available at prediction time.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Price per area is invalid as an input when predicting that same price, but '
                       'floor area itself may help. Before claiming that a method works, check '
                       'what data it uses, which predictions or patterns it produces, and how '
                       'those outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Propose features for a problem and document their availability at '
                       'inference. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A convenient column measured only after the outcome is target leakage. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **domain-informed features** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Useful representations can require domain '
                       'understanding; derive features from information genuinely available at '
                       'prediction time.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Domain-Informed Features — hands-on activity',
                'description': 'Propose features for a problem and document their availability at '
                               'inference. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-14']},
               {'title': 'Domain-Informed Features — critical reasoning',
                'description': 'Consider this boundary: A convenient column measured only after '
                               'the outcome is target leakage. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Domain-Informed Features — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Domain-Informed Features?',
                         'options': ['Features measured after an outcome are always valid '
                                     'predictors.',
                                     'Shuffling all time series is always safe.',
                                     'Periodicity cannot be represented with engineered features.',
                                     'Useful representations can require domain understanding; '
                                     'derive features from information genuinely available at '
                                     'prediction time.'],
                         'correct': 3,
                         'explanation': 'Useful representations can require domain understanding; '
                                        'derive features from information genuinely available at '
                                        'prediction time. In the worked scenario: Price per area '
                                        'is invalid as an input when predicting that same price, '
                                        'but floor area itself may help.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Domain-Informed Features?',
                         'options': ['Engineer time features and compare chronological with '
                                     'shuffled split behavior.',
                                     'Propose features for a problem and document their '
                                     'availability at inference.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.',
                                     'Ignore the source data and report a score without fitting a '
                                     'model.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Propose features for a problem '
                                        'and document their availability at inference.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A convenient column measured only '
                                     'after the outcome is target leakage.',
                         'type': 'open'}],
          'passing_score': 70}}
