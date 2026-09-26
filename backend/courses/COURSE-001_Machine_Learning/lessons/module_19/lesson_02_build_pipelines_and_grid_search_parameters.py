"""M19.L02 — Build Pipelines and Grid-Search Parameters.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 6, pages 307–309. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M19.L02"
MODULE_ORDER = 19
MODULE_TITLE = 'Machine Learning Pipelines'
MODULE_DESCRIPTION = 'Combine all fitted transformations with models inside robust selection and evaluation workflows.'
SOURCE_CHAPTER = 6
SOURCE_PAGES = '307–309'

TOPIC = {'title': 'Build Pipelines and Grid-Search Parameters',
 'slug': 'ml-foundations-m19-l02',
 'description': 'Pipeline chains named transformers and a final estimator; prefix nested search '
                'settings using step__parameter syntax.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-19'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Build Pipelines and Grid-Search Parameters',
            'content': '# Build Pipelines and Grid-Search Parameters\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M19.L02 | '
                       '**Module:** Machine Learning Pipelines\n'
                       '> **Source alignment:** BOOK-001, Chapter 6, pages 307–309. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Pipeline chains named transformers and a final estimator; '
                       'prefix nested search settings using step__parameter syntax.\n'
                       '- Apply the principle to: A scaler-plus-SVC pipeline exposes svm__C and '
                       'svm__gamma for search.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Build '
                       'and grid-search an SVC pipeline on raw training features.\n'
                       '\n'
                       '## Why this matters\n'
                       'Combine all fitted transformations with models inside robust selection and '
                       'evaluation workflows. This lesson focuses on **build pipelines and '
                       'grid-search parameters** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Pipeline chains named transformers and a final estimator; prefix nested '
                       'search settings using step__parameter syntax.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A scaler-plus-SVC pipeline exposes svm__C and svm__gamma for search. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Build and grid-search an SVC pipeline on raw training features. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not pass already scaled full-training features to a CV search. Explain '
                       'how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.pipeline import Pipeline\n'
                       'from sklearn.preprocessing import MinMaxScaler\n'
                       'from sklearn.svm import SVC\n'
                       'pipe = Pipeline([("scaler", MinMaxScaler()), ("svm", SVC())])\n'
                       'param_grid = {"svm__C": [0.1, 1, 10], "svm__gamma": [0.001, 0.01]}\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **build pipelines and grid-search parameters** in your own words '
                       'and answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Pipeline chains named transformers and a final '
                       'estimator; prefix nested search settings using step__parameter syntax.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Build Pipelines and Grid-Search Parameters — hands-on activity',
                'description': 'Build and grid-search an SVC pipeline on raw training features. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-19']},
               {'title': 'Build Pipelines and Grid-Search Parameters — critical reasoning',
                'description': 'Consider this boundary: Do not pass already scaled full-training '
                               'features to a CV search. Explain a failure mode if it is ignored '
                               'and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Build Pipelines and Grid-Search Parameters — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Build '
                                     'Pipelines and Grid-Search Parameters?',
                         'options': ['All fitted preprocessing should happen before '
                                     'cross-validation.',
                                     'Pipeline chains named transformers and a final estimator; '
                                     'prefix nested search settings using step__parameter syntax.',
                                     'A pipeline makes group and time leakage impossible '
                                     'automatically.',
                                     'Search parameters do not need to identify their pipeline '
                                     'step.'],
                         'correct': 1,
                         'explanation': 'Pipeline chains named transformers and a final estimator; '
                                        'prefix nested search settings using step__parameter '
                                        'syntax. In the worked scenario: A scaler-plus-SVC '
                                        'pipeline exposes svm__C and svm__gamma for search.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Build Pipelines and Grid-Search Parameters?',
                         'options': ['Illustrate which rows a scaler sees in one five-fold '
                                     'iteration.',
                                     'Write a reproducible paired experiment and explain why the '
                                     'two setups differ.',
                                     'Build explicit and automatically named pipelines and inspect '
                                     'steps.',
                                     'Build and grid-search an SVC pipeline on raw training '
                                     'features.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Build and grid-search an SVC '
                                        'pipeline on raw training features.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not pass already scaled '
                                     'full-training features to a CV search.',
                         'type': 'open'}],
          'passing_score': 70}}
