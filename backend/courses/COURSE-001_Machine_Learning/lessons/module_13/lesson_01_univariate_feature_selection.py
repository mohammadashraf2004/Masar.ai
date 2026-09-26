"""M13.L01 — Univariate Feature Selection.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 235–238. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M13.L01"
MODULE_ORDER = 13
MODULE_TITLE = 'Automatic Feature Selection'
MODULE_DESCRIPTION = 'Compare feature selection techniques and fit them within the evaluation process.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '235–238'

TOPIC = {'title': 'Univariate Feature Selection',
 'slug': 'ml-foundations-m13-l01',
 'description': 'Univariate tests score features separately against the target and keep a '
                'configured subset; they can miss interactions.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-13'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Univariate Feature Selection',
            'content': '# Univariate Feature Selection\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M13.L01 | '
                       '**Module:** Automatic Feature Selection\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 235–238. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Univariate tests score features separately against the target '
                       'and keep a configured subset; they can miss interactions.\n'
                       '- Apply the principle to: Two weak independent marginal features may be '
                       'useful when combined.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Select features within a training fold and record selected names.\n'
                       '\n'
                       '## Why this matters\n'
                       'Compare feature selection techniques and fit them within the evaluation '
                       'process. This lesson focuses on **univariate feature selection** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Univariate tests score features separately against the target and keep a '
                       'configured subset; they can miss interactions.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Two weak independent marginal features may be useful when combined. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Select features within a training fold and record selected names. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Running supervised selection on all data before CV leaks validation '
                       'labels. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.feature_selection import SelectPercentile, f_classif\n'
                       'selector = SelectPercentile(score_func=f_classif, percentile=20)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **univariate feature selection** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Univariate tests score features separately against '
                       'the target and keep a configured subset; they can miss interactions.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Univariate Feature Selection — hands-on activity',
                'description': 'Select features within a training fold and record selected names. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-13']},
               {'title': 'Univariate Feature Selection — critical reasoning',
                'description': 'Consider this boundary: Running supervised selection on all data '
                               'before CV leaks validation labels. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Univariate Feature Selection — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Univariate Feature Selection?',
                         'options': ['Feature selection may use all targets before '
                                     'cross-validation.',
                                     'Importance rankings are necessarily stable across folds.',
                                     'Univariate tests score features separately against the '
                                     'target and keep a configured subset; they can miss '
                                     'interactions.',
                                     'Repeated feature-elimination fits have no computational '
                                     'cost.'],
                         'correct': 2,
                         'explanation': 'Univariate tests score features separately against the '
                                        'target and keep a configured subset; they can miss '
                                        'interactions. In the worked scenario: Two weak '
                                        'independent marginal features may be useful when '
                                        'combined.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Univariate Feature Selection?',
                         'options': ['Select features within a training fold and record selected '
                                     'names.',
                                     'Inspect feature support after model-based selection in a '
                                     'pipeline.',
                                     'Compare RFE selections across training folds and compute '
                                     'budget.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Select features within a '
                                        'training fold and record selected names.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Running supervised selection on all '
                                     'data before CV leaks validation labels.',
                         'type': 'open'}],
          'passing_score': 70}}
