"""M20.L03 — Build a Text Classification Baseline.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 7, pages 332–335. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M20.L03"
MODULE_ORDER = 20
MODULE_TITLE = 'Machine Learning for Text'
MODULE_DESCRIPTION = 'Represent English text and build supervised sentiment and unsupervised topic-analysis workflows.'
SOURCE_CHAPTER = 7
SOURCE_PAGES = '332–335'

TOPIC = {'title': 'Build a Text Classification Baseline',
 'slug': 'ml-foundations-m20-l03',
 'description': 'A linear model on word counts provides a baseline; min_df, max_df and stopword '
                'choices change sparsity and coverage.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-20'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Build a Text Classification Baseline',
            'content': '# Build a Text Classification Baseline\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M20.L03 | '
                       '**Module:** Machine Learning for Text\n'
                       '> **Source alignment:** BOOK-001, Chapter 7, pages 332–335. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: A linear model on word counts provides a baseline; min_df, '
                       'max_df and stopword choices change sparsity and coverage.\n'
                       '- Apply the principle to: Filtering words that occur in fewer than five '
                       "documents shrinks the book's vocabulary.\n"
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare a baseline and filtered word-count pipeline under the same CV.\n'
                       '\n'
                       '## Why this matters\n'
                       'Represent English text and build supervised sentiment and unsupervised '
                       'topic-analysis workflows. This lesson focuses on **build a text '
                       'classification baseline** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'A linear model on word counts provides a baseline; min_df, max_df and '
                       'stopword choices change sparsity and coverage.\n'
                       '\n'
                       '## Worked scenario\n'
                       "Filtering words that occur in fewer than five documents shrinks the book's "
                       'vocabulary. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare a baseline and filtered word-count pipeline under the same CV. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Removing stopwords does not always increase validation performance. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.pipeline import make_pipeline\n'
                       'from sklearn.feature_extraction.text import CountVectorizer\n'
                       'from sklearn.linear_model import LogisticRegression\n'
                       'pipe = make_pipeline(CountVectorizer(min_df=2), '
                       'LogisticRegression(max_iter=1000))\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **build a text classification baseline** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** A linear model on word counts provides a baseline; '
                       'min_df, max_df and stopword choices change sparsity and coverage.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Build a Text Classification Baseline — hands-on activity',
                'description': 'Compare a baseline and filtered word-count pipeline under the same '
                               'CV. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-20']},
               {'title': 'Build a Text Classification Baseline — critical reasoning',
                'description': 'Consider this boundary: Removing stopwords does not always '
                               'increase validation performance. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Build a Text Classification Baseline — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Build a '
                                     'Text Classification Baseline?',
                         'options': ['Every string column is free-form natural language.',
                                     'The vocabulary should be fitted on all test documents.',
                                     'Topic-model word groups are validated human categories.',
                                     'A linear model on word counts provides a baseline; min_df, '
                                     'max_df and stopword choices change sparsity and coverage.'],
                         'correct': 3,
                         'explanation': 'A linear model on word counts provides a baseline; '
                                        'min_df, max_df and stopword choices change sparsity and '
                                        'coverage. In the worked scenario: Filtering words that '
                                        "occur in fewer than five documents shrinks the book's "
                                        'vocabulary.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Build a Text Classification Baseline?',
                         'options': ['Load review examples and describe label balance and '
                                     'formatting problems.',
                                     'Compare a baseline and filtered word-count pipeline under '
                                     'the same CV.',
                                     'Fit CountVectorizer on tiny texts and inspect vocabulary_ '
                                     'and shape.',
                                     'Build TfidfVectorizer plus LogisticRegression and inspect '
                                     'idf_ after fitting.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Compare a baseline and filtered '
                                        'word-count pipeline under the same CV.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Removing stopwords does not always '
                                     'increase validation performance.',
                         'type': 'open'}],
          'passing_score': 70}}
