"""M13.L02 — Model-Based Feature Selection.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 4, pages 238–240. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M13.L02"
MODULE_ORDER = 13
MODULE_TITLE = 'Automatic Feature Selection'
MODULE_DESCRIPTION = 'Compare feature selection techniques and fit them within the evaluation process.'
SOURCE_CHAPTER = 4
SOURCE_PAGES = '238–240'

TOPIC = {'title': 'Model-Based Feature Selection',
 'slug': 'ml-foundations-m13-l02',
 'description': 'SelectFromModel uses learned importance or coefficient magnitude to choose '
                'features; rankings depend on model assumptions.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-13'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Model-Based Feature Selection',
            'content': '# Model-Based Feature Selection\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M13.L02 | '
                       '**Module:** Automatic Feature Selection\n'
                       '> **Source alignment:** BOOK-001, Chapter 4, pages 238–240. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: SelectFromModel uses learned importance or coefficient '
                       'magnitude to choose features; rankings depend on model assumptions.\n'
                       '- Apply the principle to: L1 linear regression can zero out weights that a '
                       'selection step removes.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Inspect feature support after model-based selection in a pipeline.\n'
                       '\n'
                       '## Why this matters\n'
                       'Compare feature selection techniques and fit them within the evaluation '
                       'process. This lesson focuses on **model-based feature selection** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'SelectFromModel uses learned importance or coefficient magnitude to choose '
                       'features; rankings depend on model assumptions.\n'
                       '\n'
                       '## Worked scenario\n'
                       'L1 linear regression can zero out weights that a selection step removes. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Inspect feature support after model-based selection in a pipeline. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Importance does not prove a feature caused predictions. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.feature_selection import SelectFromModel\n'
                       'from sklearn.linear_model import LogisticRegression\n'
                       'selector = SelectFromModel(LogisticRegression(penalty="l1", '
                       'solver="liblinear"))\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **model-based feature selection** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** SelectFromModel uses learned importance or '
                       'coefficient magnitude to choose features; rankings depend on model '
                       'assumptions.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Model-Based Feature Selection — hands-on activity',
                'description': 'Inspect feature support after model-based selection in a pipeline. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-13']},
               {'title': 'Model-Based Feature Selection — critical reasoning',
                'description': 'Consider this boundary: Importance does not prove a feature caused '
                               'predictions. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Model-Based Feature Selection — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Model-Based Feature Selection?',
                         'options': ['Feature selection may use all targets before '
                                     'cross-validation.',
                                     'Importance rankings are necessarily stable across folds.',
                                     'Repeated feature-elimination fits have no computational '
                                     'cost.',
                                     'SelectFromModel uses learned importance or coefficient '
                                     'magnitude to choose features; rankings depend on model '
                                     'assumptions.'],
                         'correct': 3,
                         'explanation': 'SelectFromModel uses learned importance or coefficient '
                                        'magnitude to choose features; rankings depend on model '
                                        'assumptions. In the worked scenario: L1 linear regression '
                                        'can zero out weights that a selection step removes.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Model-Based Feature Selection?',
                         'options': ['Select features within a training fold and record selected '
                                     'names.',
                                     'Inspect feature support after model-based selection in a '
                                     'pipeline.',
                                     'Compare RFE selections across training folds and compute '
                                     'budget.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Inspect feature support after '
                                        'model-based selection in a pipeline.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Importance does not prove a feature '
                                     'caused predictions.',
                         'type': 'open'}],
          'passing_score': 70}}
