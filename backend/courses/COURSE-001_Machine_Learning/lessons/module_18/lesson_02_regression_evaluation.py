"""M18.L02 — Regression Evaluation.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 299. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M18.L02"
MODULE_ORDER = 18
MODULE_TITLE = 'Multiclass, Regression & Scoring'
MODULE_DESCRIPTION = 'Match scoring rules to task and aggregate appropriately across classes or targets.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '299'

TOPIC = {'title': 'Regression Evaluation',
 'slug': 'ml-foundations-m18-l02',
 'description': 'MAE, MSE and R² characterize different properties of numeric prediction errors; '
                'report metrics in problem-relevant units.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-18'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Regression Evaluation',
            'content': '# Regression Evaluation\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M18.L02 | '
                       '**Module:** Multiclass, Regression & Scoring\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 299. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: MAE, MSE and R² characterize different properties of numeric '
                       'prediction errors; report metrics in problem-relevant units.\n'
                       '- Apply the principle to: One very large miss affects MSE more strongly '
                       'than MAE.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare two regression models using MAE, MSE and a residual example.\n'
                       '\n'
                       '## Why this matters\n'
                       'Match scoring rules to task and aggregate appropriately across classes or '
                       'targets. This lesson focuses on **regression evaluation** so you can make '
                       'an explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'MAE, MSE and R² characterize different properties of numeric prediction '
                       'errors; report metrics in problem-relevant units.\n'
                       '\n'
                       '## Worked scenario\n'
                       'One very large miss affects MSE more strongly than MAE. Before claiming '
                       'that a method works, check what data it uses, which predictions or '
                       'patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare two regression models using MAE, MSE and a residual example. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A positive R² alone does not establish adequate operational performance. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.metrics import mean_absolute_error, mean_squared_error, '
                       'r2_score\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **regression evaluation** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** MAE, MSE and R² characterize different properties of '
                       'numeric prediction errors; report metrics in problem-relevant units.\n',
            'estimated_minutes': 35,
            'has_code_examples': True},
 'exercises': [{'title': 'Regression Evaluation — hands-on activity',
                'description': 'Compare two regression models using MAE, MSE and a residual '
                               'example. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-18']},
               {'title': 'Regression Evaluation — critical reasoning',
                'description': 'Consider this boundary: A positive R² alone does not establish '
                               'adequate operational performance. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Regression Evaluation — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Regression Evaluation?',
                         'options': ['MAE, MSE and R² characterize different properties of numeric '
                                     'prediction errors; report metrics in problem-relevant units.',
                                     'Macro and weighted metrics answer exactly the same question.',
                                     'MAE and MSE penalize outliers identically.',
                                     'Scoring choices can safely be finalized after viewing test '
                                     'results.'],
                         'correct': 0,
                         'explanation': 'MAE, MSE and R² characterize different properties of '
                                        'numeric prediction errors; report metrics in '
                                        'problem-relevant units. In the worked scenario: One very '
                                        'large miss affects MSE more strongly than MAE.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Regression Evaluation?',
                         'options': ['Compute and contrast macro versus weighted F1 on a skewed '
                                     'label set.',
                                     'Configure scoring in CV and explain which outcome determines '
                                     'best_estimator_.',
                                     'Compare two regression models using MAE, MSE and a residual '
                                     'example.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Compare two regression models '
                                        'using MAE, MSE and a residual example.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A positive R² alone does not establish '
                                     'adequate operational performance.',
                         'type': 'open'}],
          'passing_score': 70}}
