"""M18.L01 — Multiclass Evaluation.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 5, pages 296–299. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M18.L01"
MODULE_ORDER = 18
MODULE_TITLE = 'Multiclass, Regression & Scoring'
MODULE_DESCRIPTION = 'Match scoring rules to task and aggregate appropriately across classes or targets.'
SOURCE_CHAPTER = 5
SOURCE_PAGES = '296–299'

TOPIC = {'title': 'Multiclass Evaluation',
 'slug': 'ml-foundations-m18-l01',
 'description': 'Inspect per-class precision and recall; macro, micro and weighted averaging '
                'answer different aggregation questions.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-18'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Multiclass Evaluation',
            'content': '# Multiclass Evaluation\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M18.L01 | '
                       '**Module:** Multiclass, Regression & Scoring\n'
                       '> **Source alignment:** BOOK-001, Chapter 5, pages 296–299. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Inspect per-class precision and recall; macro, micro and '
                       'weighted averaging answer different aggregation questions.\n'
                       '- Apply the principle to: A rare class with poor recall can disappear '
                       'behind a high weighted mean.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compute and contrast macro versus weighted F1 on a skewed label set.\n'
                       '\n'
                       '## Why this matters\n'
                       'Match scoring rules to task and aggregate appropriately across classes or '
                       'targets. This lesson focuses on **multiclass evaluation** so you can make '
                       'an explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Inspect per-class precision and recall; macro, micro and weighted '
                       'averaging answer different aggregation questions.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A rare class with poor recall can disappear behind a high weighted mean. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compute and contrast macro versus weighted F1 on a skewed label set. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Weighted F1 is not a direct guarantee of minority-class quality. Explain '
                       'how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.metrics import classification_report\n'
                       'print(classification_report(y_test, predictions, zero_division=0))\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **multiclass evaluation** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Inspect per-class precision and recall; macro, micro '
                       'and weighted averaging answer different aggregation questions.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Multiclass Evaluation — hands-on activity',
                'description': 'Compute and contrast macro versus weighted F1 on a skewed label '
                               'set. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-18']},
               {'title': 'Multiclass Evaluation — critical reasoning',
                'description': 'Consider this boundary: Weighted F1 is not a direct guarantee of '
                               'minority-class quality. Explain a failure mode if it is ignored '
                               'and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Multiclass Evaluation — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Multiclass Evaluation?',
                         'options': ['Macro and weighted metrics answer exactly the same question.',
                                     'MAE and MSE penalize outliers identically.',
                                     'Scoring choices can safely be finalized after viewing test '
                                     'results.',
                                     'Inspect per-class precision and recall; macro, micro and '
                                     'weighted averaging answer different aggregation questions.'],
                         'correct': 3,
                         'explanation': 'Inspect per-class precision and recall; macro, micro and '
                                        'weighted averaging answer different aggregation '
                                        'questions. In the worked scenario: A rare class with poor '
                                        'recall can disappear behind a high weighted mean.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Multiclass Evaluation?',
                         'options': ['Compare two regression models using MAE, MSE and a residual '
                                     'example.',
                                     'Compute and contrast macro versus weighted F1 on a skewed '
                                     'label set.',
                                     'Configure scoring in CV and explain which outcome determines '
                                     'best_estimator_.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Compute and contrast macro '
                                        'versus weighted F1 on a skewed label set.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Weighted F1 is not a direct guarantee '
                                     'of minority-class quality.',
                         'type': 'open'}],
          'passing_score': 70}}
