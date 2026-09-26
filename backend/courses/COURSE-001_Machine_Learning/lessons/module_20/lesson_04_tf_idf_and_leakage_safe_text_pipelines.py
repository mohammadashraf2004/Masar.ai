"""M20.L04 — TF–IDF and Leakage-Safe Text Pipelines.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 7, pages 336–338. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M20.L04"
MODULE_ORDER = 20
MODULE_TITLE = 'Machine Learning for Text'
MODULE_DESCRIPTION = 'Represent English text and build supervised sentiment and unsupervised topic-analysis workflows.'
SOURCE_CHAPTER = 7
SOURCE_PAGES = '336–338'

TOPIC = {'title': 'TF–IDF and Leakage-Safe Text Pipelines',
 'slug': 'ml-foundations-m20-l04',
 'description': 'TF–IDF weights terms by document-specific frequency and corpus-wide rarity; fit '
                'vectorization within cross-validation.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.8333,
 'skill_tags': ['machine-learning', 'foundations', 'module-20'],
 'prerequisite_ids': [],
 'lesson': {'title': 'TF–IDF and Leakage-Safe Text Pipelines',
            'content': '# TF–IDF and Leakage-Safe Text Pipelines\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M20.L04 | '
                       '**Module:** Machine Learning for Text\n'
                       '> **Source alignment:** BOOK-001, Chapter 7, pages 336–338. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: TF–IDF weights terms by document-specific frequency and '
                       'corpus-wide rarity; fit vectorization within cross-validation.\n'
                       '- Apply the principle to: A word used in one review collection gets a '
                       'different IDF weight than in another.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Build '
                       'TfidfVectorizer plus LogisticRegression and inspect idf_ after fitting.\n'
                       '\n'
                       '## Why this matters\n'
                       'Represent English text and build supervised sentiment and unsupervised '
                       'topic-analysis workflows. This lesson focuses on **tf–idf and leakage-safe '
                       'text pipelines** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'TF–IDF weights terms by document-specific frequency and corpus-wide '
                       'rarity; fit vectorization within cross-validation.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A word used in one review collection gets a different IDF weight than in '
                       'another. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Build TfidfVectorizer plus LogisticRegression and inspect idf_ after '
                       'fitting. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'IDF is fitted corpus statistics and must not include CV validation '
                       'documents. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.pipeline import make_pipeline\n'
                       'from sklearn.feature_extraction.text import TfidfVectorizer\n'
                       'from sklearn.linear_model import LogisticRegression\n'
                       'pipe = make_pipeline(TfidfVectorizer(min_df=2), '
                       'LogisticRegression(max_iter=1000))\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **tf–idf and leakage-safe text pipelines** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** TF–IDF weights terms by document-specific frequency '
                       'and corpus-wide rarity; fit vectorization within cross-validation.\n',
            'estimated_minutes': 50,
            'has_code_examples': True},
 'exercises': [{'title': 'TF–IDF and Leakage-Safe Text Pipelines — hands-on activity',
                'description': 'Build TfidfVectorizer plus LogisticRegression and inspect idf_ '
                               'after fitting. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-20']},
               {'title': 'TF–IDF and Leakage-Safe Text Pipelines — critical reasoning',
                'description': 'Consider this boundary: IDF is fitted corpus statistics and must '
                               'not include CV validation documents. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'TF–IDF and Leakage-Safe Text Pipelines — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of TF–IDF '
                                     'and Leakage-Safe Text Pipelines?',
                         'options': ['TF–IDF weights terms by document-specific frequency and '
                                     'corpus-wide rarity; fit vectorization within '
                                     'cross-validation.',
                                     'Every string column is free-form natural language.',
                                     'The vocabulary should be fitted on all test documents.',
                                     'Topic-model word groups are validated human categories.'],
                         'correct': 0,
                         'explanation': 'TF–IDF weights terms by document-specific frequency and '
                                        'corpus-wide rarity; fit vectorization within '
                                        'cross-validation. In the worked scenario: A word used in '
                                        'one review collection gets a different IDF weight than in '
                                        'another.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'TF–IDF and Leakage-Safe Text Pipelines?',
                         'options': ['Load review examples and describe label balance and '
                                     'formatting problems.',
                                     'Fit CountVectorizer on tiny texts and inspect vocabulary_ '
                                     'and shape.',
                                     'Build TfidfVectorizer plus LogisticRegression and inspect '
                                     'idf_ after fitting.',
                                     'Compare a baseline and filtered word-count pipeline under '
                                     'the same CV.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Build TfidfVectorizer plus '
                                        'LogisticRegression and inspect idf_ after fitting.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? IDF is fitted corpus statistics and '
                                     'must not include CV validation documents.',
                         'type': 'open'}],
          'passing_score': 70}}
