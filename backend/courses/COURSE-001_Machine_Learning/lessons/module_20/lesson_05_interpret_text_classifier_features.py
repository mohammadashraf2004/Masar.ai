"""M20.L05 — Interpret Text Classifier Features.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 7, pages 337–339. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M20.L05"
MODULE_ORDER = 20
MODULE_TITLE = 'Machine Learning for Text'
MODULE_DESCRIPTION = 'Represent English text and build supervised sentiment and unsupervised topic-analysis workflows.'
SOURCE_CHAPTER = 7
SOURCE_PAGES = '337–339'

TOPIC = {'title': 'Interpret Text Classifier Features',
 'slug': 'ml-foundations-m20-l05',
 'description': 'Inspect vocabulary alignment, model coefficients and their signs; distinguish '
                'frequent corpus terms from learned label associations.',
 'order': 5,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-20'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Interpret Text Classifier Features',
            'content': '# Interpret Text Classifier Features\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M20.L05 | '
                       '**Module:** Machine Learning for Text\n'
                       '> **Source alignment:** BOOK-001, Chapter 7, pages 337–339. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Inspect vocabulary alignment, model coefficients and their '
                       'signs; distinguish frequent corpus terms from learned label associations.\n'
                       '- Apply the principle to: A high-IDF film title is not necessarily an '
                       'indicator of positive sentiment.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Pair '
                       'the largest positive and negative coefficients with feature names.\n'
                       '\n'
                       '## Why this matters\n'
                       'Represent English text and build supervised sentiment and unsupervised '
                       'topic-analysis workflows. This lesson focuses on **interpret text '
                       'classifier features** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Inspect vocabulary alignment, model coefficients and their signs; '
                       'distinguish frequent corpus terms from learned label associations.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A high-IDF film title is not necessarily an indicator of positive '
                       'sentiment. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Pair the largest positive and negative coefficients with feature names. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A word coefficient is a model association, not evidence of a cause. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **interpret text classifier features** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Inspect vocabulary alignment, model coefficients and '
                       'their signs; distinguish frequent corpus terms from learned label '
                       'associations.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Interpret Text Classifier Features — hands-on activity',
                'description': 'Pair the largest positive and negative coefficients with feature '
                               'names. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-20']},
               {'title': 'Interpret Text Classifier Features — critical reasoning',
                'description': 'Consider this boundary: A word coefficient is a model association, '
                               'not evidence of a cause. Explain a failure mode if it is ignored '
                               'and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Interpret Text Classifier Features — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Interpret Text Classifier Features?',
                         'options': ['Every string column is free-form natural language.',
                                     'Inspect vocabulary alignment, model coefficients and their '
                                     'signs; distinguish frequent corpus terms from learned label '
                                     'associations.',
                                     'The vocabulary should be fitted on all test documents.',
                                     'Topic-model word groups are validated human categories.'],
                         'correct': 1,
                         'explanation': 'Inspect vocabulary alignment, model coefficients and '
                                        'their signs; distinguish frequent corpus terms from '
                                        'learned label associations. In the worked scenario: A '
                                        'high-IDF film title is not necessarily an indicator of '
                                        'positive sentiment.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Interpret Text Classifier Features?',
                         'options': ['Load review examples and describe label balance and '
                                     'formatting problems.',
                                     'Fit CountVectorizer on tiny texts and inspect vocabulary_ '
                                     'and shape.',
                                     'Compare a baseline and filtered word-count pipeline under '
                                     'the same CV.',
                                     'Pair the largest positive and negative coefficients with '
                                     'feature names.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Pair the largest positive and '
                                        'negative coefficients with feature names.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A word coefficient is a model '
                                     'association, not evidence of a cause.',
                         'type': 'open'}],
          'passing_score': 70}}
