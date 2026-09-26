"""M16.L01 — Manual Grid Search and Selection Bias.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 260–263. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M16.L01"
MODULE_ORDER = 16
MODULE_TITLE = 'Hyperparameter Optimization'
MODULE_DESCRIPTION = 'Tune models reproducibly and distinguish inner model search from independent assessment.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '260–263'

TOPIC = {'title': 'Manual Grid Search and Selection Bias',
 'slug': 'ml-foundations-m16-l01',
 'description': 'Try predefined settings on development data and understand how repeated checking '
                'biases the selected maximum score.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-16'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Manual Grid Search and Selection Bias',
            'content': '# Manual Grid Search and Selection Bias\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M16.L01 | '
                       '**Module:** Hyperparameter Optimization\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 260–263. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Try predefined settings on development data and understand how '
                       'repeated checking biases the selected maximum score.\n'
                       '- Apply the principle to: Picking the best of forty settings by test '
                       'accuracy turns the test set into validation.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Design a parameter search using CV without viewing test outcomes.\n'
                       '\n'
                       '## Why this matters\n'
                       'Tune models reproducibly and distinguish inner model search from '
                       'independent assessment. This lesson focuses on **manual grid search and '
                       'selection bias** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Try predefined settings on development data and understand how repeated '
                       'checking biases the selected maximum score.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Picking the best of forty settings by test accuracy turns the test set '
                       'into validation. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Design a parameter search using CV without viewing test outcomes. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'The top validation score is not an unbiased estimate of the chosen model. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **manual grid search and selection bias** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Try predefined settings on development data and '
                       'understand how repeated checking biases the selected maximum score.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'Manual Grid Search and Selection Bias — hands-on activity',
                'description': 'Design a parameter search using CV without viewing test outcomes. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-16']},
               {'title': 'Manual Grid Search and Selection Bias — critical reasoning',
                'description': 'Consider this boundary: The top validation score is not an '
                               'unbiased estimate of the chosen model. Explain a failure mode if '
                               'it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Manual Grid Search and Selection Bias — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Manual '
                                     'Grid Search and Selection Bias?',
                         'options': ['The maximum cross-validation score is an independent test '
                                     'estimate.',
                                     'Try predefined settings on development data and understand '
                                     'how repeated checking biases the selected maximum score.',
                                     'Nested validation permits inner folds to include outer '
                                     'validation rows.',
                                     'Search size never affects resource use.'],
                         'correct': 1,
                         'explanation': 'Try predefined settings on development data and '
                                        'understand how repeated checking biases the selected '
                                        'maximum score. In the worked scenario: Picking the best '
                                        'of forty settings by test accuracy turns the test set '
                                        'into validation.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Manual Grid Search and Selection Bias?',
                         'options': ['Run a compact search and interpret its selected '
                                     'configuration.',
                                     'Create separate search-grid dictionaries and a mean-score '
                                     'comparison table.',
                                     'Draw inner/outer index ownership and estimate number of '
                                     'model fits.',
                                     'Design a parameter search using CV without viewing test '
                                     'outcomes.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Design a parameter search using '
                                        'CV without viewing test outcomes.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? The top validation score is not an '
                                     'unbiased estimate of the chosen model.',
                         'type': 'open'}],
          'passing_score': 70}}
