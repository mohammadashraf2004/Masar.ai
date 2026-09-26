"""M10.L01 — ARI and NMI with Reference Labels.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 191–193. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M10.L01"
MODULE_ORDER = 10
MODULE_TITLE = 'Clustering Evaluation & Applications'
MODULE_DESCRIPTION = 'Evaluate unlabeled structure carefully and translate patterns into inspectable applications.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '191–193'

TOPIC = {'title': 'ARI and NMI with Reference Labels',
 'slug': 'ml-foundations-m10-l01',
 'description': 'Adjusted Rand and normalized mutual information compare cluster assignments '
                'against known reference labels; labels are optional external information.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-10'],
 'prerequisite_ids': [],
 'lesson': {'title': 'ARI and NMI with Reference Labels',
            'content': '# ARI and NMI with Reference Labels\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M10.L01 | '
                       '**Module:** Clustering Evaluation & Applications\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 191–193. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Adjusted Rand and normalized mutual information compare cluster '
                       'assignments against known reference labels; labels are optional external '
                       'information.\n'
                       '- Apply the principle to: Cluster ID 0 may correspond to reference class 2 '
                       'with no penalty for renaming.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Evaluate clustering under two permuted cluster-label encodings.\n'
                       '\n'
                       '## Why this matters\n'
                       'Evaluate unlabeled structure carefully and translate patterns into '
                       'inspectable applications. This lesson focuses on **ari and nmi with '
                       'reference labels** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Adjusted Rand and normalized mutual information compare cluster '
                       'assignments against known reference labels; labels are optional external '
                       'information.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Cluster ID 0 may correspond to reference class 2 with no penalty for '
                       'renaming. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Evaluate clustering under two permuted cluster-label encodings. Record '
                       'your assumptions, relevant parameters and the observed result. Explain how '
                       'the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'ARI can be negative; cluster IDs should not be compared by numeric '
                       'equality. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.metrics import adjusted_rand_score, '
                       'normalized_mutual_info_score\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **ari and nmi with reference labels** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Adjusted Rand and normalized mutual information '
                       'compare cluster assignments against known reference labels; labels are '
                       'optional external information.\n',
            'estimated_minutes': 35,
            'has_code_examples': True},
 'exercises': [{'title': 'ARI and NMI with Reference Labels — hands-on activity',
                'description': 'Evaluate clustering under two permuted cluster-label encodings. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-10']},
               {'title': 'ARI and NMI with Reference Labels — critical reasoning',
                'description': 'Consider this boundary: ARI can be negative; cluster IDs should '
                               'not be compared by numeric equality. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'ARI and NMI with Reference Labels — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of ARI and '
                                     'NMI with Reference Labels?',
                         'options': ['An internal clustering metric proves business relevance.',
                                     'Cluster IDs must numerically match reference-label IDs.',
                                     'Unsupervised cluster names should be treated as ground '
                                     'truth.',
                                     'Adjusted Rand and normalized mutual information compare '
                                     'cluster assignments against known reference labels; labels '
                                     'are optional external information.'],
                         'correct': 3,
                         'explanation': 'Adjusted Rand and normalized mutual information compare '
                                        'cluster assignments against known reference labels; '
                                        'labels are optional external information. In the worked '
                                        'scenario: Cluster ID 0 may correspond to reference class '
                                        '2 with no penalty for renaming.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'ARI and NMI with Reference Labels?',
                         'options': ['Evaluate silhouette on two structures and explain a '
                                     'disagreement with visual evidence.',
                                     'Evaluate clustering under two permuted cluster-label '
                                     'encodings.',
                                     'Build cluster profiles from features and sample examples '
                                     'without assigning unsupported labels.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Evaluate clustering under two '
                                        'permuted cluster-label encodings.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? ARI can be negative; cluster IDs '
                                     'should not be compared by numeric equality.',
                         'type': 'open'}],
          'passing_score': 70}}
