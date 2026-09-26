"""M19.L06 — Search Across Models and Custom Transformers.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapters 6 (pp. 319–321) and 8 (pp. 360–361). Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M19.L06"
MODULE_ORDER = 19
MODULE_TITLE = 'Machine Learning Pipelines'
MODULE_DESCRIPTION = 'Combine all fitted transformations with models inside robust selection and evaluation workflows.'
SOURCE_CHAPTER = 6
SOURCE_PAGES = '319–321, 360–361'
SOURCE_CHAPTERS = (6, 8)

TOPIC = {'title': 'Search Across Models and Custom Transformers',
 'slug': 'ml-foundations-m19-l06',
 'description': 'Use conditional grids to compare estimators and preprocessing options; implement '
                'custom data-dependent steps with a compatible fit/transform interface.',
 'order': 6,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-19'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Search Across Models and Custom Transformers',
            'content': '# Search Across Models and Custom Transformers\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M19.L06 | '
                       '**Module:** Machine Learning Pipelines\n'
                       '> **Source alignment:** BOOK-001, Chapters 6 (pp. 319–321) and 8 (pp. '
                       '360–361). This is an original curriculum adaptation, not an excerpt from '
                       'the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Use conditional grids to compare estimators and preprocessing '
                       'options; implement custom data-dependent steps with a compatible '
                       'fit/transform interface.\n'
                       '- Apply the principle to: Compare SVC with scaling against a forest '
                       'without scaling using separate parameter grids.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Draft '
                       'a BaseEstimator plus TransformerMixin step and place it in a pipeline.\n'
                       '\n'
                       '## Why this matters\n'
                       'Combine all fitted transformations with models inside robust selection and '
                       'evaluation workflows. This lesson focuses on **search across models and '
                       'custom transformers** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Use conditional grids to compare estimators and preprocessing options; '
                       'implement custom data-dependent steps with a compatible fit/transform '
                       'interface.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Compare SVC with scaling against a forest without scaling using separate '
                       'parameter grids. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Draft a BaseEstimator plus TransformerMixin step and place it in a '
                       'pipeline. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A custom transform must retain constructor parameter values and fit using '
                       'training-fold data only. Explain how your method respects this boundary or '
                       'avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.base import BaseEstimator, TransformerMixin\n'
                       '\n'
                       'class AddConstant(BaseEstimator, TransformerMixin):\n'
                       '    def __init__(self, amount=1.0):\n'
                       '        self.amount = amount\n'
                       '\n'
                       '    def fit(self, X, y=None):\n'
                       '        return self\n'
                       '\n'
                       '    def transform(self, X):\n'
                       '        return X + self.amount\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **search across models and custom transformers** in your own words '
                       'and answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Use conditional grids to compare estimators and '
                       'preprocessing options; implement custom data-dependent steps with a '
                       'compatible fit/transform interface.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Search Across Models and Custom Transformers — hands-on activity',
                'description': 'Draft a BaseEstimator plus TransformerMixin step and place it in a '
                               'pipeline. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-19']},
               {'title': 'Search Across Models and Custom Transformers — critical reasoning',
                'description': 'Consider this boundary: A custom transform must retain constructor '
                               'parameter values and fit using training-fold data only. Explain a '
                               'failure mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Search Across Models and Custom Transformers — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Search '
                                     'Across Models and Custom Transformers?',
                         'options': ['All fitted preprocessing should happen before '
                                     'cross-validation.',
                                     'Use conditional grids to compare estimators and '
                                     'preprocessing options; implement custom data-dependent steps '
                                     'with a compatible fit/transform interface.',
                                     'A pipeline makes group and time leakage impossible '
                                     'automatically.',
                                     'Search parameters do not need to identify their pipeline '
                                     'step.'],
                         'correct': 1,
                         'explanation': 'Use conditional grids to compare estimators and '
                                        'preprocessing options; implement custom data-dependent '
                                        'steps with a compatible fit/transform interface. In the '
                                        'worked scenario: Compare SVC with scaling against a '
                                        'forest without scaling using separate parameter grids.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Search Across Models and Custom Transformers?',
                         'options': ['Illustrate which rows a scaler sees in one five-fold '
                                     'iteration.',
                                     'Build and grid-search an SVC pipeline on raw training '
                                     'features.',
                                     'Write a reproducible paired experiment and explain why the '
                                     'two setups differ.',
                                     'Draft a BaseEstimator plus TransformerMixin step and place '
                                     'it in a pipeline.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Draft a BaseEstimator plus '
                                        'TransformerMixin step and place it in a pipeline.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A custom transform must retain '
                                     'constructor parameter values and fit using training-fold '
                                     'data only.',
                         'type': 'open'}],
          'passing_score': 70},
 'project': {'title': 'Leakage-Safe Training Pipeline',
             'description': 'Compare preprocessing and estimator alternatives inside CV, inspect '
                            'the selected pipeline and test a custom transformer.',
             'difficulty': DifficultyLevel.intermediate,
             'tech_stack': ['Python', 'NumPy', 'scikit-learn', 'Jupyter'],
             'objectives': ['State the problem and data assumptions.',
                            'Implement a reproducible baseline and improved workflow.',
                            'Validate honestly and interpret both strengths and limitations.'],
             'rubric': {'problem_definition': 20,
                        'reproducibility': 25,
                        'evaluation_integrity': 30,
                        'interpretation': 25},
             'starter_repo_url': None,
             'estimated_hours': 5.0}}
