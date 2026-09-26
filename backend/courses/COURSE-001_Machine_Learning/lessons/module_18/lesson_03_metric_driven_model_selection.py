"""M18.L03 — Metric-Driven Model Selection.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 299–303. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M18.L03"
MODULE_ORDER = 18
MODULE_TITLE = 'Multiclass, Regression & Scoring'
MODULE_DESCRIPTION = 'Match scoring rules to task and aggregate appropriately across classes or targets.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '299–303'

TOPIC = {'title': 'Metric-Driven Model Selection',
 'slug': 'ml-foundations-m18-l03',
 'description': 'Select the scoring metric before search and align refit and reporting with the '
                'application goal.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-18'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Metric-Driven Model Selection',
            'content': '# Metric-Driven Model Selection\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M18.L03 | '
                       '**Module:** Multiclass, Regression & Scoring\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 299–303. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Select the scoring metric before search and align refit and '
                       'reporting with the application goal.\n'
                       '- Apply the principle to: A high-accuracy classifier may lose to a '
                       'higher-recall one when missing positives is costly.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Configure scoring in CV and explain which outcome determines '
                       'best_estimator_.\n'
                       '\n'
                       '## Why this matters\n'
                       'Match scoring rules to task and aggregate appropriately across classes or '
                       'targets. This lesson focuses on **metric-driven model selection** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Select the scoring metric before search and align refit and reporting with '
                       'the application goal.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A high-accuracy classifier may lose to a higher-recall one when missing '
                       'positives is costly. Before claiming that a method works, check what data '
                       'it uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Configure scoring in CV and explain which outcome determines '
                       'best_estimator_. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Changing the metric after seeing test results is another form of selection '
                       'leakage. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **metric-driven model selection** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Select the scoring metric before search and align '
                       'refit and reporting with the application goal.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'Metric-Driven Model Selection — hands-on activity',
                'description': 'Configure scoring in CV and explain which outcome determines '
                               'best_estimator_. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-18']},
               {'title': 'Metric-Driven Model Selection — critical reasoning',
                'description': 'Consider this boundary: Changing the metric after seeing test '
                               'results is another form of selection leakage. Explain a failure '
                               'mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Metric-Driven Model Selection — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Metric-Driven Model Selection?',
                         'options': ['Macro and weighted metrics answer exactly the same question.',
                                     'Select the scoring metric before search and align refit and '
                                     'reporting with the application goal.',
                                     'MAE and MSE penalize outliers identically.',
                                     'Scoring choices can safely be finalized after viewing test '
                                     'results.'],
                         'correct': 1,
                         'explanation': 'Select the scoring metric before search and align refit '
                                        'and reporting with the application goal. In the worked '
                                        'scenario: A high-accuracy classifier may lose to a '
                                        'higher-recall one when missing positives is costly.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Metric-Driven Model Selection?',
                         'options': ['Compute and contrast macro versus weighted F1 on a skewed '
                                     'label set.',
                                     'Compare two regression models using MAE, MSE and a residual '
                                     'example.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.',
                                     'Configure scoring in CV and explain which outcome determines '
                                     'best_estimator_.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Configure scoring in CV and '
                                        'explain which outcome determines best_estimator_.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Changing the metric after seeing test '
                                     'results is another form of selection leakage.',
                         'type': 'open'}],
          'passing_score': 70},
 'project': {'title': 'Evaluation and Selection Laboratory',
             'description': 'Define a metric, audit splitting, search development folds, tune any '
                            'threshold without test labels and report one final test outcome.',
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
             'estimated_hours': 7.0}}
