"""M10.L02 — Silhouette, Stability and Validity.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 193–195. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M10.L02"
MODULE_ORDER = 10
MODULE_TITLE = 'Clustering Evaluation & Applications'
MODULE_DESCRIPTION = 'Evaluate unlabeled structure carefully and translate patterns into inspectable applications.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '193–195'

TOPIC = {'title': 'Silhouette, Stability and Validity',
 'slug': 'ml-foundations-m10-l02',
 'description': 'Silhouette compares within-cluster cohesion and nearest other-cluster separation; '
                'stability and domain usefulness remain distinct.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-10'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Silhouette, Stability and Validity',
            'content': '# Silhouette, Stability and Validity\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M10.L02 | '
                       '**Module:** Clustering Evaluation & Applications\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 193–195. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Silhouette compares within-cluster cohesion and nearest '
                       'other-cluster separation; stability and domain usefulness remain '
                       'distinct.\n'
                       '- Apply the principle to: Round separated blobs can score better than '
                       'meaningful nonconvex density clusters.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Evaluate silhouette on two structures and explain a disagreement with '
                       'visual evidence.\n'
                       '\n'
                       '## Why this matters\n'
                       'Evaluate unlabeled structure carefully and translate patterns into '
                       'inspectable applications. This lesson focuses on **silhouette, stability '
                       'and validity** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Silhouette compares within-cluster cohesion and nearest other-cluster '
                       'separation; stability and domain usefulness remain distinct.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Round separated blobs can score better than meaningful nonconvex density '
                       'clusters. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Evaluate silhouette on two structures and explain a disagreement with '
                       'visual evidence. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'An internal score alone cannot prove the groups solve the application '
                       'problem. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **silhouette, stability and validity** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Silhouette compares within-cluster cohesion and '
                       'nearest other-cluster separation; stability and domain usefulness remain '
                       'distinct.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'Silhouette, Stability and Validity — hands-on activity',
                'description': 'Evaluate silhouette on two structures and explain a disagreement '
                               'with visual evidence. Deliver a short notebook, annotated example '
                               'or written calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-10']},
               {'title': 'Silhouette, Stability and Validity — critical reasoning',
                'description': 'Consider this boundary: An internal score alone cannot prove the '
                               'groups solve the application problem. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Silhouette, Stability and Validity — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Silhouette, Stability and Validity?',
                         'options': ['Silhouette compares within-cluster cohesion and nearest '
                                     'other-cluster separation; stability and domain usefulness '
                                     'remain distinct.',
                                     'An internal clustering metric proves business relevance.',
                                     'Cluster IDs must numerically match reference-label IDs.',
                                     'Unsupervised cluster names should be treated as ground '
                                     'truth.'],
                         'correct': 0,
                         'explanation': 'Silhouette compares within-cluster cohesion and nearest '
                                        'other-cluster separation; stability and domain usefulness '
                                        'remain distinct. In the worked scenario: Round separated '
                                        'blobs can score better than meaningful nonconvex density '
                                        'clusters.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Silhouette, Stability and Validity?',
                         'options': ['Evaluate clustering under two permuted cluster-label '
                                     'encodings.',
                                     'Build cluster profiles from features and sample examples '
                                     'without assigning unsupported labels.',
                                     'Evaluate silhouette on two structures and explain a '
                                     'disagreement with visual evidence.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Evaluate silhouette on two '
                                        'structures and explain a disagreement with visual '
                                        'evidence.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? An internal score alone cannot prove '
                                     'the groups solve the application problem.',
                         'type': 'open'}],
          'passing_score': 70}}
