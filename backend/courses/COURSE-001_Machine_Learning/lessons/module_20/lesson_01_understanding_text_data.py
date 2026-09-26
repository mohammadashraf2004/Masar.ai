"""M20.L01 — Understanding Text Data.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 7, pages 323–327. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M20.L01"
MODULE_ORDER = 20
MODULE_TITLE = 'Machine Learning for Text'
MODULE_DESCRIPTION = 'Represent English text and build supervised sentiment and unsupervised topic-analysis workflows.'
SOURCE_CHAPTER = 7
SOURCE_PAGES = '323–327'

TOPIC = {'title': 'Understanding Text Data',
 'slug': 'ml-foundations-m20-l01',
 'description': 'Separate fixed categorical strings, messy category responses, structured strings '
                'and free-text documents; inspect labels and encoding.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-20'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Understanding Text Data',
            'content': '# Understanding Text Data\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M20.L01 | '
                       '**Module:** Machine Learning for Text\n'
                       '> **Source alignment:** BOOK-001, Chapter 7, pages 323–327. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Separate fixed categorical strings, messy category responses, '
                       'structured strings and free-text documents; inspect labels and encoding.\n'
                       '- Apply the principle to: An IMDb review is a document; a postal code '
                       'stored as text is not a free-text document.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Load '
                       'review examples and describe label balance and formatting problems.\n'
                       '\n'
                       '## Why this matters\n'
                       'Represent English text and build supervised sentiment and unsupervised '
                       'topic-analysis workflows. This lesson focuses on **understanding text '
                       'data** so you can make an explicit choice rather than blindly applying a '
                       'library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Separate fixed categorical strings, messy category responses, structured '
                       'strings and free-text documents; inspect labels and encoding.\n'
                       '\n'
                       '## Worked scenario\n'
                       'An IMDb review is a document; a postal code stored as text is not a '
                       'free-text document. Before claiming that a method works, check what data '
                       'it uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Load review examples and describe label balance and formatting problems. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not treat every string column as prose. Explain how your method '
                       'respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **understanding text data** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Separate fixed categorical strings, messy category '
                       'responses, structured strings and free-text documents; inspect labels and '
                       'encoding.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Understanding Text Data — hands-on activity',
                'description': 'Load review examples and describe label balance and formatting '
                               'problems. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-20']},
               {'title': 'Understanding Text Data — critical reasoning',
                'description': 'Consider this boundary: Do not treat every string column as prose. '
                               'Explain a failure mode if it is ignored and the safeguard you '
                               'would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Understanding Text Data — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Understanding Text Data?',
                         'options': ['Every string column is free-form natural language.',
                                     'Separate fixed categorical strings, messy category '
                                     'responses, structured strings and free-text documents; '
                                     'inspect labels and encoding.',
                                     'The vocabulary should be fitted on all test documents.',
                                     'Topic-model word groups are validated human categories.'],
                         'correct': 1,
                         'explanation': 'Separate fixed categorical strings, messy category '
                                        'responses, structured strings and free-text documents; '
                                        'inspect labels and encoding. In the worked scenario: An '
                                        'IMDb review is a document; a postal code stored as text '
                                        'is not a free-text document.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Understanding Text Data?',
                         'options': ['Fit CountVectorizer on tiny texts and inspect vocabulary_ '
                                     'and shape.',
                                     'Compare a baseline and filtered word-count pipeline under '
                                     'the same CV.',
                                     'Build TfidfVectorizer plus LogisticRegression and inspect '
                                     'idf_ after fitting.',
                                     'Load review examples and describe label balance and '
                                     'formatting problems.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Load review examples and '
                                        'describe label balance and formatting problems.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not treat every string column as '
                                     'prose.',
                         'type': 'open'}],
          'passing_score': 70}}
