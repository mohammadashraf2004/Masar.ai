"""M11.L01 — Understanding Categorical Features.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 211–213. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M11.L01"
MODULE_ORDER = 11
MODULE_TITLE = 'Categorical Data Representation'
MODULE_DESCRIPTION = 'Encode qualitative variables while preventing category drift and evaluation leakage.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '211–213'

TOPIC = {'title': 'Understanding Categorical Features',
 'slug': 'ml-foundations-m11-l01',
 'description': 'Categorical inputs describe membership, not continuous magnitude; encoding must '
                'reflect whether ordering is meaningful.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-11'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Understanding Categorical Features',
            'content': '# Understanding Categorical Features\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M11.L01 | '
                       '**Module:** Categorical Data Representation\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 211–213. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Categorical inputs describe membership, not continuous '
                       'magnitude; encoding must reflect whether ordering is meaningful.\n'
                       '- Apply the principle to: Apartment type is nominal, whereas an '
                       'intentionally ordered satisfaction scale may be ordinal.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Inspect a mixed table and classify numeric, nominal and ordinal columns.\n'
                       '\n'
                       '## Why this matters\n'
                       'Encode qualitative variables while preventing category drift and '
                       'evaluation leakage. This lesson focuses on **understanding categorical '
                       'features** so you can make an explicit choice rather than blindly applying '
                       'a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Categorical inputs describe membership, not continuous magnitude; encoding '
                       'must reflect whether ordering is meaningful.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Apartment type is nominal, whereas an intentionally ordered satisfaction '
                       'scale may be ordinal. Before claiming that a method works, check what data '
                       'it uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Inspect a mixed table and classify numeric, nominal and ordinal columns. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'An integer category code does not imply meaningful arithmetic distance. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **understanding categorical features** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Categorical inputs describe membership, not '
                       'continuous magnitude; encoding must reflect whether ordering is '
                       'meaningful.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Understanding Categorical Features — hands-on activity',
                'description': 'Inspect a mixed table and classify numeric, nominal and ordinal '
                               'columns. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-11']},
               {'title': 'Understanding Categorical Features — critical reasoning',
                'description': 'Consider this boundary: An integer category code does not imply '
                               'meaningful arithmetic distance. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Understanding Categorical Features — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Understanding Categorical Features?',
                         'options': ['Categorical inputs describe membership, not continuous '
                                     'magnitude; encoding must reflect whether ordering is '
                                     'meaningful.',
                                     'Integer-coded categories inherently have equal numerical '
                                     'spacing.',
                                     'The final test set should define training categories.',
                                     'New categories never appear after deployment.'],
                         'correct': 0,
                         'explanation': 'Categorical inputs describe membership, not continuous '
                                        'magnitude; encoding must reflect whether ordering is '
                                        'meaningful. In the worked scenario: Apartment type is '
                                        'nominal, whereas an intentionally ordered satisfaction '
                                        'scale may be ordinal.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Understanding Categorical Features?',
                         'options': ['One-hot encode a small training table and transform an '
                                     'unseen-category example.',
                                     'Diagnose a numeric-code error and document an inference-time '
                                     'category policy.',
                                     'Inspect a mixed table and classify numeric, nominal and '
                                     'ordinal columns.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Inspect a mixed table and '
                                        'classify numeric, nominal and ordinal columns.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? An integer category code does not '
                                     'imply meaningful arithmetic distance.',
                         'type': 'open'}],
          'passing_score': 70}}
