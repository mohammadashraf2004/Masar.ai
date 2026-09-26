"""M19.L05 — Inspect and Jointly Tune Pipeline Steps.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 6, pages 314–318. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M19.L05"
MODULE_ORDER = 19
MODULE_TITLE = 'Machine Learning Pipelines'
MODULE_DESCRIPTION = 'Combine all fitted transformations with models inside robust selection and evaluation workflows.'
SOURCE_CHAPTER = 6
SOURCE_PAGES = '314–318'

TOPIC = {'title': 'Inspect and Jointly Tune Pipeline Steps',
 'slug': 'ml-foundations-m19-l05',
 'description': 'Inspect named_steps and best_estimator_; jointly tune preprocessing and model '
                'parameters while monitoring expansion costs.',
 'order': 5,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-19'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Inspect and Jointly Tune Pipeline Steps',
            'content': '# Inspect and Jointly Tune Pipeline Steps\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M19.L05 | '
                       '**Module:** Machine Learning Pipelines\n'
                       '> **Source alignment:** BOOK-001, Chapter 6, pages 314–318. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Inspect named_steps and best_estimator_; jointly tune '
                       'preprocessing and model parameters while monitoring expansion costs.\n'
                       '- Apply the principle to: Search polynomial degree and Ridge alpha within '
                       'a single regression pipeline.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Inspect selected parameters and a fitted model attribute after CV.\n'
                       '\n'
                       '## Why this matters\n'
                       'Combine all fitted transformations with models inside robust selection and '
                       'evaluation workflows. This lesson focuses on **inspect and jointly tune '
                       'pipeline steps** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Inspect named_steps and best_estimator_; jointly tune preprocessing and '
                       'model parameters while monitoring expansion costs.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Search polynomial degree and Ridge alpha within a single regression '
                       'pipeline. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Inspect selected parameters and a fitted model attribute after CV. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Fitting polynomial features outside CV can leak feature-selection '
                       'decisions. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **inspect and jointly tune pipeline steps** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Inspect named_steps and best_estimator_; jointly '
                       'tune preprocessing and model parameters while monitoring expansion '
                       'costs.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'Inspect and Jointly Tune Pipeline Steps — hands-on activity',
                'description': 'Inspect selected parameters and a fitted model attribute after CV. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-19']},
               {'title': 'Inspect and Jointly Tune Pipeline Steps — critical reasoning',
                'description': 'Consider this boundary: Fitting polynomial features outside CV can '
                               'leak feature-selection decisions. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Inspect and Jointly Tune Pipeline Steps — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Inspect '
                                     'and Jointly Tune Pipeline Steps?',
                         'options': ['Inspect named_steps and best_estimator_; jointly tune '
                                     'preprocessing and model parameters while monitoring '
                                     'expansion costs.',
                                     'All fitted preprocessing should happen before '
                                     'cross-validation.',
                                     'A pipeline makes group and time leakage impossible '
                                     'automatically.',
                                     'Search parameters do not need to identify their pipeline '
                                     'step.'],
                         'correct': 0,
                         'explanation': 'Inspect named_steps and best_estimator_; jointly tune '
                                        'preprocessing and model parameters while monitoring '
                                        'expansion costs. In the worked scenario: Search '
                                        'polynomial degree and Ridge alpha within a single '
                                        'regression pipeline.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Inspect and Jointly Tune Pipeline Steps?',
                         'options': ['Illustrate which rows a scaler sees in one five-fold '
                                     'iteration.',
                                     'Build and grid-search an SVC pipeline on raw training '
                                     'features.',
                                     'Inspect selected parameters and a fitted model attribute '
                                     'after CV.',
                                     'Write a reproducible paired experiment and explain why the '
                                     'two setups differ.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Inspect selected parameters and '
                                        'a fitted model attribute after CV.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Fitting polynomial features outside CV '
                                     'can leak feature-selection decisions.',
                         'type': 'open'}],
          'passing_score': 70}}
