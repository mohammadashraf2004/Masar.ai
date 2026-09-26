"""M03.L05 — Naive Bayes Classifiers.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 65–70. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M03.L05"
MODULE_ORDER = 3
MODULE_TITLE = 'Linear & Probabilistic Models'
MODULE_DESCRIPTION = 'Understand linear predictions, regularization, probabilistic baselines and multiclass decision rules.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '65–70'

TOPIC = {'title': 'Naive Bayes Classifiers',
 'slug': 'ml-foundations-m03-l05',
 'description': 'Naive Bayes combines class priors with feature evidence under a '
                'conditional-independence assumption; model variants depend on features.',
 'order': 5,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5,
 'skill_tags': ['machine-learning', 'foundations', 'module-03'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Naive Bayes Classifiers',
            'content': '# Naive Bayes Classifiers\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M03.L05 | '
                       '**Module:** Linear & Probabilistic Models\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 65–70. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Naive Bayes combines class priors with feature evidence under a '
                       'conditional-independence assumption; model variants depend on features.\n'
                       '- Apply the principle to: MultinomialNB can model document counts while '
                       'GaussianNB fits continuous-feature assumptions.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Choose a suitable Naive Bayes variant for counts versus continuous '
                       'measurements.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand linear predictions, regularization, probabilistic baselines and '
                       'multiclass decision rules. This lesson focuses on **naive bayes '
                       'classifiers** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Naive Bayes combines class priors with feature evidence under a '
                       'conditional-independence assumption; model variants depend on features.\n'
                       '\n'
                       '## Worked scenario\n'
                       'MultinomialNB can model document counts while GaussianNB fits '
                       'continuous-feature assumptions. Before claiming that a method works, check '
                       'what data it uses, which predictions or patterns it produces, and how '
                       'those outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Choose a suitable Naive Bayes variant for counts versus continuous '
                       'measurements. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Feature independence is a model assumption, not proof about the data. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.naive_bayes import GaussianNB, MultinomialNB\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **naive bayes classifiers** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Naive Bayes combines class priors with feature '
                       'evidence under a conditional-independence assumption; model variants '
                       'depend on features.\n',
            'estimated_minutes': 30,
            'has_code_examples': True},
 'exercises': [{'title': 'Naive Bayes Classifiers — hands-on activity',
                'description': 'Choose a suitable Naive Bayes variant for counts versus continuous '
                               'measurements. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-03']},
               {'title': 'Naive Bayes Classifiers — critical reasoning',
                'description': 'Consider this boundary: Feature independence is a model '
                               'assumption, not proof about the data. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Naive Bayes Classifiers — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Naive '
                                     'Bayes Classifiers?',
                         'options': ['Naive Bayes combines class priors with feature evidence '
                                     'under a conditional-independence assumption; model variants '
                                     'depend on features.',
                                     'Regularization controls only the size of the dataset.',
                                     'All linear-classifier scores are calibrated probabilities.',
                                     'Learned coefficients establish causal relationships.'],
                         'correct': 0,
                         'explanation': 'Naive Bayes combines class priors with feature evidence '
                                        'under a conditional-independence assumption; model '
                                        'variants depend on features. In the worked scenario: '
                                        'MultinomialNB can model document counts while GaussianNB '
                                        'fits continuous-feature assumptions.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Naive Bayes Classifiers?',
                         'options': ['Fit LinearRegression and explain one coefficient while '
                                     'holding other features fixed.',
                                     'Compare coefficient patterns and held-out error for several '
                                     'alpha values.',
                                     'Choose a suitable Naive Bayes variant for counts versus '
                                     'continuous measurements.',
                                     'Train logistic regression and linear SVM on scaled training '
                                     'data and compare boundaries.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Choose a suitable Naive Bayes '
                                        'variant for counts versus continuous measurements.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Feature independence is a model '
                                     'assumption, not proof about the data.',
                         'type': 'open'}],
          'passing_score': 70}}
