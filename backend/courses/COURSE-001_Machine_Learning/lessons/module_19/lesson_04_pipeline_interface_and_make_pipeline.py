"""M19.L04 — Pipeline Interface and make_pipeline.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 6, pages 312–314. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M19.L04"
MODULE_ORDER = 19
MODULE_TITLE = 'Machine Learning Pipelines'
MODULE_DESCRIPTION = 'Combine all fitted transformations with models inside robust selection and evaluation workflows.'
SOURCE_CHAPTER = 6
SOURCE_PAGES = '312–314'

TOPIC = {'title': 'Pipeline Interface and make_pipeline',
 'slug': 'ml-foundations-m19-l04',
 'description': 'Intermediate pipeline steps transform inputs, the final step implements fitting; '
                'make_pipeline assigns class-derived step names automatically.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-19'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Pipeline Interface and make_pipeline',
            'content': '# Pipeline Interface and make_pipeline\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M19.L04 | '
                       '**Module:** Machine Learning Pipelines\n'
                       '> **Source alignment:** BOOK-001, Chapter 6, pages 312–314. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Intermediate pipeline steps transform inputs, the final step '
                       'implements fitting; make_pipeline assigns class-derived step names '
                       'automatically.\n'
                       '- Apply the principle to: An ordered scaler-PCA-classifier chain uses '
                       'fitted transformations for prediction.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Build '
                       'explicit and automatically named pipelines and inspect steps.\n'
                       '\n'
                       '## Why this matters\n'
                       'Combine all fitted transformations with models inside robust selection and '
                       'evaluation workflows. This lesson focuses on **pipeline interface and '
                       'make_pipeline** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Intermediate pipeline steps transform inputs, the final step implements '
                       'fitting; make_pipeline assigns class-derived step names automatically.\n'
                       '\n'
                       '## Worked scenario\n'
                       'An ordered scaler-PCA-classifier chain uses fitted transformations for '
                       'prediction. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Build explicit and automatically named pipelines and inspect steps. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not assume every final estimator provides predict or every pipeline has '
                       'the same methods. Explain how your method respects this boundary or avoids '
                       'the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.pipeline import make_pipeline\n'
                       'from sklearn.preprocessing import StandardScaler\n'
                       'from sklearn.decomposition import PCA\n'
                       'pipe = make_pipeline(StandardScaler(), PCA(n_components=2))\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **pipeline interface and make_pipeline** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Intermediate pipeline steps transform inputs, the '
                       'final step implements fitting; make_pipeline assigns class-derived step '
                       'names automatically.\n',
            'estimated_minutes': 35,
            'has_code_examples': True},
 'exercises': [{'title': 'Pipeline Interface and make_pipeline — hands-on activity',
                'description': 'Build explicit and automatically named pipelines and inspect '
                               'steps. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-19']},
               {'title': 'Pipeline Interface and make_pipeline — critical reasoning',
                'description': 'Consider this boundary: Do not assume every final estimator '
                               'provides predict or every pipeline has the same methods. Explain a '
                               'failure mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Pipeline Interface and make_pipeline — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Pipeline Interface and make_pipeline?',
                         'options': ['All fitted preprocessing should happen before '
                                     'cross-validation.',
                                     'A pipeline makes group and time leakage impossible '
                                     'automatically.',
                                     'Search parameters do not need to identify their pipeline '
                                     'step.',
                                     'Intermediate pipeline steps transform inputs, the final step '
                                     'implements fitting; make_pipeline assigns class-derived step '
                                     'names automatically.'],
                         'correct': 3,
                         'explanation': 'Intermediate pipeline steps transform inputs, the final '
                                        'step implements fitting; make_pipeline assigns '
                                        'class-derived step names automatically. In the worked '
                                        'scenario: An ordered scaler-PCA-classifier chain uses '
                                        'fitted transformations for prediction.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Pipeline Interface and make_pipeline?',
                         'options': ['Illustrate which rows a scaler sees in one five-fold '
                                     'iteration.',
                                     'Build explicit and automatically named pipelines and inspect '
                                     'steps.',
                                     'Build and grid-search an SVC pipeline on raw training '
                                     'features.',
                                     'Write a reproducible paired experiment and explain why the '
                                     'two setups differ.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Build explicit and '
                                        'automatically named pipelines and inspect steps.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not assume every final estimator '
                                     'provides predict or every pipeline has the same methods.',
                         'type': 'open'}],
          'passing_score': 70}}
