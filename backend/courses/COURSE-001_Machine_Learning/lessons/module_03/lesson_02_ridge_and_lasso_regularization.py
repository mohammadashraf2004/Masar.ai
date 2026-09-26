"""M03.L02 — Ridge and Lasso Regularization.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 48–54. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M03.L02"
MODULE_ORDER = 3
MODULE_TITLE = 'Linear & Probabilistic Models'
MODULE_DESCRIPTION = 'Understand linear predictions, regularization, probabilistic baselines and multiclass decision rules.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '48–54'

TOPIC = {'title': 'Ridge and Lasso Regularization',
 'slug': 'ml-foundations-m03-l02',
 'description': 'Ridge penalizes squared coefficients and Lasso penalizes absolute coefficients; '
                'alpha controls the strength of these constraints.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-03'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Ridge and Lasso Regularization',
            'content': '# Ridge and Lasso Regularization\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M03.L02 | '
                       '**Module:** Linear & Probabilistic Models\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 48–54. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Ridge penalizes squared coefficients and Lasso penalizes '
                       'absolute coefficients; alpha controls the strength of these constraints.\n'
                       '- Apply the principle to: On correlated features, Ridge shrinks weights '
                       'while Lasso may drive some to zero.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare coefficient patterns and held-out error for several alpha values.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand linear predictions, regularization, probabilistic baselines and '
                       'multiclass decision rules. This lesson focuses on **ridge and lasso '
                       'regularization** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Ridge penalizes squared coefficients and Lasso penalizes absolute '
                       'coefficients; alpha controls the strength of these constraints.\n'
                       '\n'
                       '## Worked scenario\n'
                       'On correlated features, Ridge shrinks weights while Lasso may drive some '
                       'to zero. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare coefficient patterns and held-out error for several alpha values. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Large alpha is not guaranteed to improve generalization. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.linear_model import Ridge, Lasso\n'
                       'ridge = Ridge(alpha=1.0)\n'
                       'lasso = Lasso(alpha=1.0)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **ridge and lasso regularization** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Ridge penalizes squared coefficients and Lasso '
                       'penalizes absolute coefficients; alpha controls the strength of these '
                       'constraints.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Ridge and Lasso Regularization — hands-on activity',
                'description': 'Compare coefficient patterns and held-out error for several alpha '
                               'values. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-03']},
               {'title': 'Ridge and Lasso Regularization — critical reasoning',
                'description': 'Consider this boundary: Large alpha is not guaranteed to improve '
                               'generalization. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Ridge and Lasso Regularization — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Ridge '
                                     'and Lasso Regularization?',
                         'options': ['Regularization controls only the size of the dataset.',
                                     'Ridge penalizes squared coefficients and Lasso penalizes '
                                     'absolute coefficients; alpha controls the strength of these '
                                     'constraints.',
                                     'All linear-classifier scores are calibrated probabilities.',
                                     'Learned coefficients establish causal relationships.'],
                         'correct': 1,
                         'explanation': 'Ridge penalizes squared coefficients and Lasso penalizes '
                                        'absolute coefficients; alpha controls the strength of '
                                        'these constraints. In the worked scenario: On correlated '
                                        'features, Ridge shrinks weights while Lasso may drive '
                                        'some to zero.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Ridge and Lasso Regularization?',
                         'options': ['Fit LinearRegression and explain one coefficient while '
                                     'holding other features fixed.',
                                     'Train logistic regression and linear SVM on scaled training '
                                     'data and compare boundaries.',
                                     'Check classes_ and explain how a predicted label relates to '
                                     'scores.',
                                     'Compare coefficient patterns and held-out error for several '
                                     'alpha values.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Compare coefficient patterns '
                                        'and held-out error for several alpha values.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Large alpha is not guaranteed to '
                                     'improve generalization.',
                         'type': 'open'}],
          'passing_score': 70}}
