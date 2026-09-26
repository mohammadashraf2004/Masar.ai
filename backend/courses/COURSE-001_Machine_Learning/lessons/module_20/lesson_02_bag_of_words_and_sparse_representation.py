"""M20.L02 — Bag-of-Words and Sparse Representation.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 7, pages 327–332. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M20.L02"
MODULE_ORDER = 20
MODULE_TITLE = 'Machine Learning for Text'
MODULE_DESCRIPTION = 'Represent English text and build supervised sentiment and unsupervised topic-analysis workflows.'
SOURCE_CHAPTER = 7
SOURCE_PAGES = '327–332'

TOPIC = {'title': 'Bag-of-Words and Sparse Representation',
 'slug': 'ml-foundations-m20-l02',
 'description': 'Tokenization yields tokens, a training vocabulary assigns feature columns, and '
                'counts form sparse document-term matrices.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.8333,
 'skill_tags': ['machine-learning', 'foundations', 'module-20'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Bag-of-Words and Sparse Representation',
            'content': '# Bag-of-Words and Sparse Representation\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M20.L02 | '
                       '**Module:** Machine Learning for Text\n'
                       '> **Source alignment:** BOOK-001, Chapter 7, pages 327–332. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Tokenization yields tokens, a training vocabulary assigns '
                       'feature columns, and counts form sparse document-term matrices.\n'
                       '- Apply the principle to: Two short sentences become a two-row matrix with '
                       'a column per training word.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit '
                       'CountVectorizer on tiny texts and inspect vocabulary_ and shape.\n'
                       '\n'
                       '## Why this matters\n'
                       'Represent English text and build supervised sentiment and unsupervised '
                       'topic-analysis workflows. This lesson focuses on **bag-of-words and sparse '
                       'representation** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Tokenization yields tokens, a training vocabulary assigns feature columns, '
                       'and counts form sparse document-term matrices.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Two short sentences become a two-row matrix with a column per training '
                       'word. Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit CountVectorizer on tiny texts and inspect vocabulary_ and shape. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not densify a huge real-world document-term matrix. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.feature_extraction.text import CountVectorizer\n'
                       'vect = CountVectorizer()\n'
                       'X_counts = vect.fit_transform(["a useful review", "another useful '
                       'review"])\n'
                       'print(X_counts.shape)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **bag-of-words and sparse representation** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Tokenization yields tokens, a training vocabulary '
                       'assigns feature columns, and counts form sparse document-term matrices.\n',
            'estimated_minutes': 50,
            'has_code_examples': True},
 'exercises': [{'title': 'Bag-of-Words and Sparse Representation — hands-on activity',
                'description': 'Fit CountVectorizer on tiny texts and inspect vocabulary_ and '
                               'shape. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-20']},
               {'title': 'Bag-of-Words and Sparse Representation — critical reasoning',
                'description': 'Consider this boundary: Do not densify a huge real-world '
                               'document-term matrix. Explain a failure mode if it is ignored and '
                               'the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Bag-of-Words and Sparse Representation — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Bag-of-Words and Sparse Representation?',
                         'options': ['Every string column is free-form natural language.',
                                     'The vocabulary should be fitted on all test documents.',
                                     'Tokenization yields tokens, a training vocabulary assigns '
                                     'feature columns, and counts form sparse document-term '
                                     'matrices.',
                                     'Topic-model word groups are validated human categories.'],
                         'correct': 2,
                         'explanation': 'Tokenization yields tokens, a training vocabulary assigns '
                                        'feature columns, and counts form sparse document-term '
                                        'matrices. In the worked scenario: Two short sentences '
                                        'become a two-row matrix with a column per training word.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Bag-of-Words and Sparse Representation?',
                         'options': ['Fit CountVectorizer on tiny texts and inspect vocabulary_ '
                                     'and shape.',
                                     'Load review examples and describe label balance and '
                                     'formatting problems.',
                                     'Compare a baseline and filtered word-count pipeline under '
                                     'the same CV.',
                                     'Build TfidfVectorizer plus LogisticRegression and inspect '
                                     'idf_ after fitting.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Fit CountVectorizer on tiny '
                                        'texts and inspect vocabulary_ and shape.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not densify a huge real-world '
                                     'document-term matrix.',
                         'type': 'open'}],
          'passing_score': 70}}
