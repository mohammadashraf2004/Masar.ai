"""M20.L06 — N-grams and Context.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 7, pages 339–343. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M20.L06"
MODULE_ORDER = 20
MODULE_TITLE = 'Machine Learning for Text'
MODULE_DESCRIPTION = 'Represent English text and build supervised sentiment and unsupervised topic-analysis workflows.'
SOURCE_CHAPTER = 7
SOURCE_PAGES = '339–343'

TOPIC = {'title': 'N-grams and Context',
 'slug': 'ml-foundations-m20-l06',
 'description': 'Word bigrams and trigrams recover limited phrase order and negation context while '
                'expanding the feature space.',
 'order': 6,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.8333,
 'skill_tags': ['machine-learning', 'foundations', 'module-20'],
 'prerequisite_ids': [],
 'lesson': {'title': 'N-grams and Context',
            'content': '# N-grams and Context\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M20.L06 | '
                       '**Module:** Machine Learning for Text\n'
                       '> **Source alignment:** BOOK-001, Chapter 7, pages 339–343. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Word bigrams and trigrams recover limited phrase order and '
                       'negation context while expanding the feature space.\n'
                       "- Apply the principle to: The phrases 'not worth' and 'well worth' differ "
                       "although they share 'worth'.\n"
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Grid-search ngram_range on a pipeline and inspect useful phrases.\n'
                       '\n'
                       '## Why this matters\n'
                       'Represent English text and build supervised sentiment and unsupervised '
                       'topic-analysis workflows. This lesson focuses on **n-grams and context** '
                       'so you can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Word bigrams and trigrams recover limited phrase order and negation '
                       'context while expanding the feature space.\n'
                       '\n'
                       '## Worked scenario\n'
                       "The phrases 'not worth' and 'well worth' differ although they share "
                       "'worth'. Before claiming that a method works, check what data it uses, "
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Grid-search ngram_range on a pipeline and inspect useful phrases. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Adding longer n-grams always increases cost and may overfit. Explain how '
                       'your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.feature_extraction.text import TfidfVectorizer\n'
                       'vect = TfidfVectorizer(ngram_range=(1, 2))\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **n-grams and context** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Word bigrams and trigrams recover limited phrase '
                       'order and negation context while expanding the feature space.\n',
            'estimated_minutes': 50,
            'has_code_examples': True},
 'exercises': [{'title': 'N-grams and Context — hands-on activity',
                'description': 'Grid-search ngram_range on a pipeline and inspect useful phrases. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-20']},
               {'title': 'N-grams and Context — critical reasoning',
                'description': 'Consider this boundary: Adding longer n-grams always increases '
                               'cost and may overfit. Explain a failure mode if it is ignored and '
                               'the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'N-grams and Context — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of N-grams '
                                     'and Context?',
                         'options': ['Every string column is free-form natural language.',
                                     'The vocabulary should be fitted on all test documents.',
                                     'Word bigrams and trigrams recover limited phrase order and '
                                     'negation context while expanding the feature space.',
                                     'Topic-model word groups are validated human categories.'],
                         'correct': 2,
                         'explanation': 'Word bigrams and trigrams recover limited phrase order '
                                        'and negation context while expanding the feature space. '
                                        "In the worked scenario: The phrases 'not worth' and 'well "
                                        "worth' differ although they share 'worth'."},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'N-grams and Context?',
                         'options': ['Grid-search ngram_range on a pipeline and inspect useful '
                                     'phrases.',
                                     'Load review examples and describe label balance and '
                                     'formatting problems.',
                                     'Fit CountVectorizer on tiny texts and inspect vocabulary_ '
                                     'and shape.',
                                     'Compare a baseline and filtered word-count pipeline under '
                                     'the same CV.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Grid-search ngram_range on a '
                                        'pipeline and inspect useful phrases.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Adding longer n-grams always increases '
                                     'cost and may overfit.',
                         'type': 'open'}],
          'passing_score': 70}}
