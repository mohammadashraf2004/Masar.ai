"""M14.L02 — Time Features and Chronological Evaluation.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 243–250. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M14.L02"
MODULE_ORDER = 14
MODULE_TITLE = 'Domain Knowledge & Temporal Features'
MODULE_DESCRIPTION = 'Use domain transformations while respecting information availability and chronology.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '243–250'

TOPIC = {'title': 'Time Features and Chronological Evaluation',
 'slug': 'ml-foundations-m14-l02',
 'description': 'Derive calendar and periodic features when warranted; evaluate past-to-future '
                'tasks chronologically to avoid future information.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-14'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Time Features and Chronological Evaluation',
            'content': '# Time Features and Chronological Evaluation\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M14.L02 | '
                       '**Module:** Domain Knowledge & Temporal Features\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 243–250. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Derive calendar and periodic features when warranted; evaluate '
                       'past-to-future tasks chronologically to avoid future information.\n'
                       '- Apply the principle to: Hour of day can be represented cyclically to '
                       'connect 23:00 and 00:00.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Engineer time features and compare chronological with shuffled split '
                       'behavior.\n'
                       '\n'
                       '## Why this matters\n'
                       'Use domain transformations while respecting information availability and '
                       'chronology. This lesson focuses on **time features and chronological '
                       'evaluation** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Derive calendar and periodic features when warranted; evaluate '
                       'past-to-future tasks chronologically to avoid future information.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Hour of day can be represented cyclically to connect 23:00 and 00:00. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Engineer time features and compare chronological with shuffled split '
                       'behavior. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A random shuffle can give inflated estimates when observations depend on '
                       'time. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **time features and chronological evaluation** in your own words '
                       'and answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Derive calendar and periodic features when '
                       'warranted; evaluate past-to-future tasks chronologically to avoid future '
                       'information.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'Time Features and Chronological Evaluation — hands-on activity',
                'description': 'Engineer time features and compare chronological with shuffled '
                               'split behavior. Deliver a short notebook, annotated example or '
                               'written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-14']},
               {'title': 'Time Features and Chronological Evaluation — critical reasoning',
                'description': 'Consider this boundary: A random shuffle can give inflated '
                               'estimates when observations depend on time. Explain a failure mode '
                               'if it is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Time Features and Chronological Evaluation — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Time '
                                     'Features and Chronological Evaluation?',
                         'options': ['Derive calendar and periodic features when warranted; '
                                     'evaluate past-to-future tasks chronologically to avoid '
                                     'future information.',
                                     'Features measured after an outcome are always valid '
                                     'predictors.',
                                     'Shuffling all time series is always safe.',
                                     'Periodicity cannot be represented with engineered features.'],
                         'correct': 0,
                         'explanation': 'Derive calendar and periodic features when warranted; '
                                        'evaluate past-to-future tasks chronologically to avoid '
                                        'future information. In the worked scenario: Hour of day '
                                        'can be represented cyclically to connect 23:00 and '
                                        '00:00.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Time Features and Chronological Evaluation?',
                         'options': ['Propose features for a problem and document their '
                                     'availability at inference.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.',
                                     'Engineer time features and compare chronological with '
                                     'shuffled split behavior.',
                                     'Ignore the source data and report a score without fitting a '
                                     'model.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Engineer time features and '
                                        'compare chronological with shuffled split behavior.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A random shuffle can give inflated '
                                     'estimates when observations depend on time.',
                         'type': 'open'}],
          'passing_score': 70},
 'project': {'title': 'Feature Engineering Laboratory',
             'description': 'Compare categorical, nonlinear and domain-derived features with '
                            'train-only transforms and a fixed metric.',
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
             'estimated_hours': 6.0}}
