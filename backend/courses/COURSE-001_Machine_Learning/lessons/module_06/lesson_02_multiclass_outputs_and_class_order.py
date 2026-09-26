"""M06.L02 — Multiclass Outputs and Class Order.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 123–126. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M06.L02"
MODULE_ORDER = 6
MODULE_TITLE = 'Prediction Uncertainty & Model Comparison'
MODULE_DESCRIPTION = 'Interpret estimator outputs without confusing scores, probabilities and independent evaluation.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '123–126'

TOPIC = {'title': 'Multiclass Outputs and Class Order',
 'slug': 'ml-foundations-m06-l02',
 'description': 'For multiclass estimators, inspect output dimensions and classes_ before mapping '
                'columns to labels.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5,
 'skill_tags': ['machine-learning', 'foundations', 'module-06'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Multiclass Outputs and Class Order',
            'content': '# Multiclass Outputs and Class Order\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M06.L02 | '
                       '**Module:** Prediction Uncertainty & Model Comparison\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 123–126. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: For multiclass estimators, inspect output dimensions and '
                       'classes_ before mapping columns to labels.\n'
                       '- Apply the principle to: A three-column probability array maps each '
                       'column to a class in classes_.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Write '
                       'code or pseudocode mapping an output row to predicted labels.\n'
                       '\n'
                       '## Why this matters\n'
                       'Interpret estimator outputs without confusing scores, probabilities and '
                       'independent evaluation. This lesson focuses on **multiclass outputs and '
                       'class order** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'For multiclass estimators, inspect output dimensions and classes_ before '
                       'mapping columns to labels.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A three-column probability array maps each column to a class in classes_. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Write code or pseudocode mapping an output row to predicted labels. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not assume the class indices correspond to display names '
                       'alphabetically. Explain how your method respects this boundary or avoids '
                       'the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **multiclass outputs and class order** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** For multiclass estimators, inspect output dimensions '
                       'and classes_ before mapping columns to labels.\n',
            'estimated_minutes': 30,
            'has_code_examples': False},
 'exercises': [{'title': 'Multiclass Outputs and Class Order — hands-on activity',
                'description': 'Write code or pseudocode mapping an output row to predicted '
                               'labels. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-06']},
               {'title': 'Multiclass Outputs and Class Order — critical reasoning',
                'description': 'Consider this boundary: Do not assume the class indices correspond '
                               'to display names alphabetically. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Multiclass Outputs and Class Order — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Multiclass Outputs and Class Order?',
                         'options': ['For multiclass estimators, inspect output dimensions and '
                                     'classes_ before mapping columns to labels.',
                                     'Any decision-function output is a calibrated probability.',
                                     'Different test sets make comparisons automatically fair.',
                                     'The class order does not matter when interpreting scores.'],
                         'correct': 0,
                         'explanation': 'For multiclass estimators, inspect output dimensions and '
                                        'classes_ before mapping columns to labels. In the worked '
                                        'scenario: A three-column probability array maps each '
                                        'column to a class in classes_.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Multiclass Outputs and Class Order?',
                         'options': ['Inspect decision_function and predict_proba where available.',
                                     'Design a comparison table with baseline, metric and CV '
                                     'setup.',
                                     'Write code or pseudocode mapping an output row to predicted '
                                     'labels.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Write code or pseudocode '
                                        'mapping an output row to predicted labels.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not assume the class indices '
                                     'correspond to display names alphabetically.',
                         'type': 'open'}],
          'passing_score': 70}}
