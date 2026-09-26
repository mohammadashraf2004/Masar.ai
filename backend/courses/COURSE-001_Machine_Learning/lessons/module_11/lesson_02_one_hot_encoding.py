"""M11.L02 — One-Hot Encoding.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 213–217. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M11.L02"
MODULE_ORDER = 11
MODULE_TITLE = 'Categorical Data Representation'
MODULE_DESCRIPTION = 'Encode qualitative variables while preventing category drift and evaluation leakage.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '213–217'

TOPIC = {'title': 'One-Hot Encoding',
 'slug': 'ml-foundations-m11-l02',
 'description': 'One-hot encoding creates indicator columns for nominal categories; fit the '
                'encoder on training categories and handle unseen values explicitly.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-11'],
 'prerequisite_ids': [],
 'lesson': {'title': 'One-Hot Encoding',
            'content': '# One-Hot Encoding\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M11.L02 | '
                       '**Module:** Categorical Data Representation\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 213–217. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: One-hot encoding creates indicator columns for nominal '
                       'categories; fit the encoder on training categories and handle unseen '
                       'values explicitly.\n'
                       '- Apply the principle to: Three neighborhoods become three separate binary '
                       'indicator columns.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'One-hot encode a small training table and transform an unseen-category '
                       'example.\n'
                       '\n'
                       '## Why this matters\n'
                       'Encode qualitative variables while preventing category drift and '
                       'evaluation leakage. This lesson focuses on **one-hot encoding** so you can '
                       'make an explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'One-hot encoding creates indicator columns for nominal categories; fit the '
                       'encoder on training categories and handle unseen values explicitly.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Three neighborhoods become three separate binary indicator columns. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'One-hot encode a small training table and transform an unseen-category '
                       'example. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not fit category vocabulary from the held-out test set. Explain how '
                       'your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.preprocessing import OneHotEncoder\n'
                       'encoder = OneHotEncoder(handle_unknown="ignore")\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **one-hot encoding** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** One-hot encoding creates indicator columns for '
                       'nominal categories; fit the encoder on training categories and handle '
                       'unseen values explicitly.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'One-Hot Encoding — hands-on activity',
                'description': 'One-hot encode a small training table and transform an '
                               'unseen-category example. Deliver a short notebook, annotated '
                               'example or written calculation with your result and '
                               'interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-11']},
               {'title': 'One-Hot Encoding — critical reasoning',
                'description': 'Consider this boundary: Do not fit category vocabulary from the '
                               'held-out test set. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'One-Hot Encoding — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of One-Hot '
                                     'Encoding?',
                         'options': ['Integer-coded categories inherently have equal numerical '
                                     'spacing.',
                                     'One-hot encoding creates indicator columns for nominal '
                                     'categories; fit the encoder on training categories and '
                                     'handle unseen values explicitly.',
                                     'The final test set should define training categories.',
                                     'New categories never appear after deployment.'],
                         'correct': 1,
                         'explanation': 'One-hot encoding creates indicator columns for nominal '
                                        'categories; fit the encoder on training categories and '
                                        'handle unseen values explicitly. In the worked scenario: '
                                        'Three neighborhoods become three separate binary '
                                        'indicator columns.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'One-Hot Encoding?',
                         'options': ['Inspect a mixed table and classify numeric, nominal and '
                                     'ordinal columns.',
                                     'Diagnose a numeric-code error and document an inference-time '
                                     'category policy.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.',
                                     'One-hot encode a small training table and transform an '
                                     'unseen-category example.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: One-hot encode a small training '
                                        'table and transform an unseen-category example.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not fit category vocabulary from '
                                     'the held-out test set.',
                         'type': 'open'}],
          'passing_score': 70}}
