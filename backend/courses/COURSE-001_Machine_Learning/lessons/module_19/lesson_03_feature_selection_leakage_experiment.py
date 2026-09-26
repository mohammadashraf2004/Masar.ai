"""M19.L03 — Feature Selection Leakage Experiment.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 6, pages 310–311. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M19.L03"
MODULE_ORDER = 19
MODULE_TITLE = 'Machine Learning Pipelines'
MODULE_DESCRIPTION = 'Combine all fitted transformations with models inside robust selection and evaluation workflows.'
SOURCE_CHAPTER = 6
SOURCE_PAGES = '310–311'

TOPIC = {'title': 'Feature Selection Leakage Experiment',
 'slug': 'ml-foundations-m19-l03',
 'description': 'Selecting features against all labels before CV can create falsely strong '
                'predictions even from random independent data.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-19'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Feature Selection Leakage Experiment',
            'content': '# Feature Selection Leakage Experiment\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M19.L03 | '
                       '**Module:** Machine Learning Pipelines\n'
                       '> **Source alignment:** BOOK-001, Chapter 6, pages 310–311. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Selecting features against all labels before CV can create '
                       'falsely strong predictions even from random independent data.\n'
                       "- Apply the principle to: The book's synthetic random-label example "
                       'reports 0.91 R² with leakage versus -0.25 with a proper pipeline.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Write '
                       'a reproducible paired experiment and explain why the two setups differ.\n'
                       '\n'
                       '## Why this matters\n'
                       'Combine all fitted transformations with models inside robust selection and '
                       'evaluation workflows. This lesson focuses on **feature selection leakage '
                       'experiment** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Selecting features against all labels before CV can create falsely strong '
                       'predictions even from random independent data.\n'
                       '\n'
                       '## Worked scenario\n'
                       "The book's synthetic random-label example reports 0.91 R² with leakage "
                       'versus -0.25 with a proper pipeline. Before claiming that a method works, '
                       'check what data it uses, which predictions or patterns it produces, and '
                       'how those outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Write a reproducible paired experiment and explain why the two setups '
                       'differ. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A strong cross-validation score does not validate a pipeline that leaked '
                       'labels. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **feature selection leakage experiment** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Selecting features against all labels before CV can '
                       'create falsely strong predictions even from random independent data.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Feature Selection Leakage Experiment — hands-on activity',
                'description': 'Write a reproducible paired experiment and explain why the two '
                               'setups differ. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-19']},
               {'title': 'Feature Selection Leakage Experiment — critical reasoning',
                'description': 'Consider this boundary: A strong cross-validation score does not '
                               'validate a pipeline that leaked labels. Explain a failure mode if '
                               'it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Feature Selection Leakage Experiment — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Feature '
                                     'Selection Leakage Experiment?',
                         'options': ['All fitted preprocessing should happen before '
                                     'cross-validation.',
                                     'A pipeline makes group and time leakage impossible '
                                     'automatically.',
                                     'Selecting features against all labels before CV can create '
                                     'falsely strong predictions even from random independent '
                                     'data.',
                                     'Search parameters do not need to identify their pipeline '
                                     'step.'],
                         'correct': 2,
                         'explanation': 'Selecting features against all labels before CV can '
                                        'create falsely strong predictions even from random '
                                        "independent data. In the worked scenario: The book's "
                                        'synthetic random-label example reports 0.91 R² with '
                                        'leakage versus -0.25 with a proper pipeline.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Feature Selection Leakage Experiment?',
                         'options': ['Write a reproducible paired experiment and explain why the '
                                     'two setups differ.',
                                     'Illustrate which rows a scaler sees in one five-fold '
                                     'iteration.',
                                     'Build and grid-search an SVC pipeline on raw training '
                                     'features.',
                                     'Build explicit and automatically named pipelines and inspect '
                                     'steps.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Write a reproducible paired '
                                        'experiment and explain why the two setups differ.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A strong cross-validation score does '
                                     'not validate a pipeline that leaked labels.',
                         'type': 'open'}],
          'passing_score': 70}}
