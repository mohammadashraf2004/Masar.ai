"""M06.L01 — Decision Scores and Predictive Probabilities.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 119–123. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M06.L01"
MODULE_ORDER = 6
MODULE_TITLE = 'Prediction Uncertainty & Model Comparison'
MODULE_DESCRIPTION = 'Interpret estimator outputs without confusing scores, probabilities and independent evaluation.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '119–123'

TOPIC = {'title': 'Decision Scores and Predictive Probabilities',
 'slug': 'ml-foundations-m06-l01',
 'description': 'Decision functions express signed or classwise confidence scores; predict_proba '
                'expresses model-provided probabilities when supported.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-06'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Decision Scores and Predictive Probabilities',
            'content': '# Decision Scores and Predictive Probabilities\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M06.L01 | '
                       '**Module:** Prediction Uncertainty & Model Comparison\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 119–123. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Decision functions express signed or classwise confidence '
                       'scores; predict_proba expresses model-provided probabilities when '
                       'supported.\n'
                       '- Apply the principle to: A score above zero can determine a binary '
                       'decision without being a 0–1 probability.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Inspect decision_function and predict_proba where available.\n'
                       '\n'
                       '## Why this matters\n'
                       'Interpret estimator outputs without confusing scores, probabilities and '
                       'independent evaluation. This lesson focuses on **decision scores and '
                       'predictive probabilities** so you can make an explicit choice rather than '
                       'blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Decision functions express signed or classwise confidence scores; '
                       'predict_proba expresses model-provided probabilities when supported.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A score above zero can determine a binary decision without being a 0–1 '
                       'probability. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Inspect decision_function and predict_proba where available. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A decision score of 2.3 is not a 230 percent probability. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **decision scores and predictive probabilities** in your own words '
                       'and answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Decision functions express signed or classwise '
                       'confidence scores; predict_proba expresses model-provided probabilities '
                       'when supported.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 'Decision Scores and Predictive Probabilities — hands-on activity',
                'description': 'Inspect decision_function and predict_proba where available. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-06']},
               {'title': 'Decision Scores and Predictive Probabilities — critical reasoning',
                'description': 'Consider this boundary: A decision score of 2.3 is not a 230 '
                               'percent probability. Explain a failure mode if it is ignored and '
                               'the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Decision Scores and Predictive Probabilities — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Decision Scores and Predictive Probabilities?',
                         'options': ['Any decision-function output is a calibrated probability.',
                                     'Different test sets make comparisons automatically fair.',
                                     'The class order does not matter when interpreting scores.',
                                     'Decision functions express signed or classwise confidence '
                                     'scores; predict_proba expresses model-provided probabilities '
                                     'when supported.'],
                         'correct': 3,
                         'explanation': 'Decision functions express signed or classwise confidence '
                                        'scores; predict_proba expresses model-provided '
                                        'probabilities when supported. In the worked scenario: A '
                                        'score above zero can determine a binary decision without '
                                        'being a 0–1 probability.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Decision Scores and Predictive Probabilities?',
                         'options': ['Write code or pseudocode mapping an output row to predicted '
                                     'labels.',
                                     'Inspect decision_function and predict_proba where available.',
                                     'Design a comparison table with baseline, metric and CV '
                                     'setup.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Inspect decision_function and '
                                        'predict_proba where available.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A decision score of 2.3 is not a 230 '
                                     'percent probability.',
                         'type': 'open'}],
          'passing_score': 70}}
