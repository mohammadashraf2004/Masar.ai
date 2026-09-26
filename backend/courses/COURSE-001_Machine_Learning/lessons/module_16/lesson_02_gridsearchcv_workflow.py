"""M16.L02 — GridSearchCV Workflow.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 263–267. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M16.L02"
MODULE_ORDER = 16
MODULE_TITLE = 'Hyperparameter Optimization'
MODULE_DESCRIPTION = 'Tune models reproducibly and distinguish inner model search from independent assessment.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '263–267'

TOPIC = {'title': 'GridSearchCV Workflow',
 'slug': 'ml-foundations-m16-l02',
 'description': 'GridSearchCV evaluates candidate configurations across CV folds and exposes '
                'best_params_, best_score_ and best_estimator_.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-16'],
 'prerequisite_ids': [],
 'lesson': {'title': 'GridSearchCV Workflow',
            'content': '# GridSearchCV Workflow\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M16.L02 | '
                       '**Module:** Hyperparameter Optimization\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 263–267. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: GridSearchCV evaluates candidate configurations across CV folds '
                       'and exposes best_params_, best_score_ and best_estimator_.\n'
                       '- Apply the principle to: A grid of C and gamma values yields one selected '
                       'fitted pipeline after refit.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Run a '
                       'compact search and interpret its selected configuration.\n'
                       '\n'
                       '## Why this matters\n'
                       'Tune models reproducibly and distinguish inner model search from '
                       'independent assessment. This lesson focuses on **gridsearchcv workflow** '
                       'so you can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'GridSearchCV evaluates candidate configurations across CV folds and '
                       'exposes best_params_, best_score_ and best_estimator_.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A grid of C and gamma values yields one selected fitted pipeline after '
                       'refit. Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Run a compact search and interpret its selected configuration. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Never confuse best_score_ with an independent held-out test score. Explain '
                       'how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.model_selection import GridSearchCV\n'
                       'search = GridSearchCV(model, {"C": [0.1, 1.0, 10.0]}, cv=5)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **gridsearchcv workflow** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** GridSearchCV evaluates candidate configurations '
                       'across CV folds and exposes best_params_, best_score_ and '
                       'best_estimator_.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'GridSearchCV Workflow — hands-on activity',
                'description': 'Run a compact search and interpret its selected configuration. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-16']},
               {'title': 'GridSearchCV Workflow — critical reasoning',
                'description': 'Consider this boundary: Never confuse best_score_ with an '
                               'independent held-out test score. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'GridSearchCV Workflow — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'GridSearchCV Workflow?',
                         'options': ['The maximum cross-validation score is an independent test '
                                     'estimate.',
                                     'Nested validation permits inner folds to include outer '
                                     'validation rows.',
                                     'GridSearchCV evaluates candidate configurations across CV '
                                     'folds and exposes best_params_, best_score_ and '
                                     'best_estimator_.',
                                     'Search size never affects resource use.'],
                         'correct': 2,
                         'explanation': 'GridSearchCV evaluates candidate configurations across CV '
                                        'folds and exposes best_params_, best_score_ and '
                                        'best_estimator_. In the worked scenario: A grid of C and '
                                        'gamma values yields one selected fitted pipeline after '
                                        'refit.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'GridSearchCV Workflow?',
                         'options': ['Run a compact search and interpret its selected '
                                     'configuration.',
                                     'Design a parameter search using CV without viewing test '
                                     'outcomes.',
                                     'Create separate search-grid dictionaries and a mean-score '
                                     'comparison table.',
                                     'Draw inner/outer index ownership and estimate number of '
                                     'model fits.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Run a compact search and '
                                        'interpret its selected configuration.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Never confuse best_score_ with an '
                                     'independent held-out test score.',
                         'type': 'open'}],
          'passing_score': 70}}
