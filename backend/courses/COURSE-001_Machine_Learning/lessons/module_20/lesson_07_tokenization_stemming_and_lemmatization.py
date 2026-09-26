"""M20.L07 — Tokenization, Stemming and Lemmatization.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 7, pages 344–347. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M20.L07"
MODULE_ORDER = 20
MODULE_TITLE = 'Machine Learning for Text'
MODULE_DESCRIPTION = 'Represent English text and build supervised sentiment and unsupervised topic-analysis workflows.'
SOURCE_CHAPTER = 7
SOURCE_PAGES = '344–347'

TOPIC = {'title': 'Tokenization, Stemming and Lemmatization',
 'slug': 'ml-foundations-m20-l07',
 'description': 'Stemming trims forms heuristically and lemmatization maps context-sensitive '
                'variants to base forms; assess their effect empirically.',
 'order': 7,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.8333,
 'skill_tags': ['machine-learning', 'foundations', 'module-20'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Tokenization, Stemming and Lemmatization',
            'content': '# Tokenization, Stemming and Lemmatization\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M20.L07 | '
                       '**Module:** Machine Learning for Text\n'
                       '> **Source alignment:** BOOK-001, Chapter 7, pages 344–347. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Stemming trims forms heuristically and lemmatization maps '
                       'context-sensitive variants to base forms; assess their effect '
                       'empirically.\n'
                       '- Apply the principle to: Meeting as noun versus verb can have different '
                       'lemmas even when a stemmer collapses them.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare a small set of words and audit custom tokenizer behavior.\n'
                       '\n'
                       '## Why this matters\n'
                       'Represent English text and build supervised sentiment and unsupervised '
                       'topic-analysis workflows. This lesson focuses on **tokenization, stemming '
                       'and lemmatization** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Stemming trims forms heuristically and lemmatization maps '
                       'context-sensitive variants to base forms; assess their effect '
                       'empirically.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Meeting as noun versus verb can have different lemmas even when a stemmer '
                       'collapses them. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare a small set of words and audit custom tokenizer behavior. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Older spaCy model names and methods in the source need adaptation before '
                       'coding. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **tokenization, stemming and lemmatization** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Stemming trims forms heuristically and lemmatization '
                       'maps context-sensitive variants to base forms; assess their effect '
                       'empirically.\n',
            'estimated_minutes': 50,
            'has_code_examples': False},
 'exercises': [{'title': 'Tokenization, Stemming and Lemmatization — hands-on activity',
                'description': 'Compare a small set of words and audit custom tokenizer behavior. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-20']},
               {'title': 'Tokenization, Stemming and Lemmatization — critical reasoning',
                'description': 'Consider this boundary: Older spaCy model names and methods in the '
                               'source need adaptation before coding. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Tokenization, Stemming and Lemmatization — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Tokenization, Stemming and Lemmatization?',
                         'options': ['Every string column is free-form natural language.',
                                     'The vocabulary should be fitted on all test documents.',
                                     'Topic-model word groups are validated human categories.',
                                     'Stemming trims forms heuristically and lemmatization maps '
                                     'context-sensitive variants to base forms; assess their '
                                     'effect empirically.'],
                         'correct': 3,
                         'explanation': 'Stemming trims forms heuristically and lemmatization maps '
                                        'context-sensitive variants to base forms; assess their '
                                        'effect empirically. In the worked scenario: Meeting as '
                                        'noun versus verb can have different lemmas even when a '
                                        'stemmer collapses them.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Tokenization, Stemming and Lemmatization?',
                         'options': ['Load review examples and describe label balance and '
                                     'formatting problems.',
                                     'Compare a small set of words and audit custom tokenizer '
                                     'behavior.',
                                     'Fit CountVectorizer on tiny texts and inspect vocabulary_ '
                                     'and shape.',
                                     'Compare a baseline and filtered word-count pipeline under '
                                     'the same CV.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Compare a small set of words '
                                        'and audit custom tokenizer behavior.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Older spaCy model names and methods in '
                                     'the source need adaptation before coding.',
                         'type': 'open'}],
          'passing_score': 70}}
