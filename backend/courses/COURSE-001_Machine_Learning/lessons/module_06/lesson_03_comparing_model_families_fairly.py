"""M06.L03 — Comparing Model Families Fairly.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 126–129. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M06.L03"
MODULE_ORDER = 6
MODULE_TITLE = 'Prediction Uncertainty & Model Comparison'
MODULE_DESCRIPTION = 'Interpret estimator outputs without confusing scores, probabilities and independent evaluation.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '126–129'

TOPIC = {'title': 'Comparing Model Families Fairly',
 'slug': 'ml-foundations-m06-l03',
 'description': 'Compare estimators under the same data split, preprocessing policy and metric, '
                'then reserve final test data for reporting.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-06'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Comparing Model Families Fairly',
            'content': '# Comparing Model Families Fairly\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M06.L03 | '
                       '**Module:** Prediction Uncertainty & Model Comparison\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 126–129. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Compare estimators under the same data split, preprocessing '
                       'policy and metric, then reserve final test data for reporting.\n'
                       '- Apply the principle to: Two classifiers tested on different folds cannot '
                       'be compared as cleanly as two under matched CV.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Design a comparison table with baseline, metric and CV setup.\n'
                       '\n'
                       '## Why this matters\n'
                       'Interpret estimator outputs without confusing scores, probabilities and '
                       'independent evaluation. This lesson focuses on **comparing model families '
                       'fairly** so you can make an explicit choice rather than blindly applying a '
                       'library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Compare estimators under the same data split, preprocessing policy and '
                       'metric, then reserve final test data for reporting.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Two classifiers tested on different folds cannot be compared as cleanly as '
                       'two under matched CV. Before claiming that a method works, check what data '
                       'it uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Design a comparison table with baseline, metric and CV setup. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Choosing the best model from repeated test-set checks contaminates the '
                       'test estimate. Explain how your method respects this boundary or avoids '
                       'the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **comparing model families fairly** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Compare estimators under the same data split, '
                       'preprocessing policy and metric, then reserve final test data for '
                       'reporting.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Comparing Model Families Fairly — hands-on activity',
                'description': 'Design a comparison table with baseline, metric and CV setup. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-06']},
               {'title': 'Comparing Model Families Fairly — critical reasoning',
                'description': 'Consider this boundary: Choosing the best model from repeated '
                               'test-set checks contaminates the test estimate. Explain a failure '
                               'mode if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Comparing Model Families Fairly — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Comparing Model Families Fairly?',
                         'options': ['Any decision-function output is a calibrated probability.',
                                     'Compare estimators under the same data split, preprocessing '
                                     'policy and metric, then reserve final test data for '
                                     'reporting.',
                                     'Different test sets make comparisons automatically fair.',
                                     'The class order does not matter when interpreting scores.'],
                         'correct': 1,
                         'explanation': 'Compare estimators under the same data split, '
                                        'preprocessing policy and metric, then reserve final test '
                                        'data for reporting. In the worked scenario: Two '
                                        'classifiers tested on different folds cannot be compared '
                                        'as cleanly as two under matched CV.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Comparing Model Families Fairly?',
                         'options': ['Inspect decision_function and predict_proba where available.',
                                     'Write code or pseudocode mapping an output row to predicted '
                                     'labels.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.',
                                     'Design a comparison table with baseline, metric and CV '
                                     'setup.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Design a comparison table with '
                                        'baseline, metric and CV setup.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Choosing the best model from repeated '
                                     'test-set checks contaminates the test estimate.',
                         'type': 'open'}],
          'passing_score': 70},
 'project': {'title': 'Supervised Model Comparison',
             'description': 'Compare at least two classifiers and one regression model using '
                            'task-correct metrics and consistent data policies.',
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
