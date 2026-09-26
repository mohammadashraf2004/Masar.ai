"""M09.L02 — k-Means Limitations and Vector Quantization.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 173–181. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M09.L02"
MODULE_ORDER = 9
MODULE_TITLE = 'Clustering Algorithms'
MODULE_DESCRIPTION = 'Select clustering methods from the geometry and density of the dataset.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '173–181'

TOPIC = {'title': 'k-Means Limitations and Vector Quantization',
 'slug': 'ml-foundations-m09-l02',
 'description': 'k-means assumes distance to centroids is meaningful; it struggles with nonconvex '
                'shapes and unequal densities, but centroids can compress signals.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-09'],
 'prerequisite_ids': [],
 'lesson': {'title': 'k-Means Limitations and Vector Quantization',
            'content': '# k-Means Limitations and Vector Quantization\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M09.L02 | '
                       '**Module:** Clustering Algorithms\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 173–181. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: k-means assumes distance to centroids is meaningful; it '
                       'struggles with nonconvex shapes and unequal densities, but centroids can '
                       'compress signals.\n'
                       '- Apply the principle to: Two concentric rings are poorly represented as '
                       'two centroid-based clusters.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Contrast k-means on blobs versus moon-shaped data.\n'
                       '\n'
                       '## Why this matters\n'
                       'Select clustering methods from the geometry and density of the dataset. '
                       'This lesson focuses on **k-means limitations and vector quantization** so '
                       'you can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'k-means assumes distance to centroids is meaningful; it struggles with '
                       'nonconvex shapes and unequal densities, but centroids can compress '
                       'signals.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Two concentric rings are poorly represented as two centroid-based '
                       'clusters. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Contrast k-means on blobs versus moon-shaped data. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Low within-cluster inertia does not prove the discovered clusters are '
                       'useful. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **k-means limitations and vector quantization** in your own words '
                       'and answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** k-means assumes distance to centroids is meaningful; '
                       'it struggles with nonconvex shapes and unequal densities, but centroids '
                       'can compress signals.\n',
            'estimated_minutes': 40,
            'has_code_examples': False},
 'exercises': [{'title': 'k-Means Limitations and Vector Quantization — hands-on activity',
                'description': 'Contrast k-means on blobs versus moon-shaped data. Deliver a short '
                               'notebook, annotated example or written calculation with your '
                               'result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-09']},
               {'title': 'k-Means Limitations and Vector Quantization — critical reasoning',
                'description': 'Consider this boundary: Low within-cluster inertia does not prove '
                               'the discovered clusters are useful. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'k-Means Limitations and Vector Quantization — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of k-Means '
                                     'Limitations and Vector Quantization?',
                         'options': ['Cluster IDs encode an inherent ranking.',
                                     'Every clustering method detects every possible shape equally '
                                     'well.',
                                     'A low inertia alone validates a clustering solution.',
                                     'k-means assumes distance to centroids is meaningful; it '
                                     'struggles with nonconvex shapes and unequal densities, but '
                                     'centroids can compress signals.'],
                         'correct': 3,
                         'explanation': 'k-means assumes distance to centroids is meaningful; it '
                                        'struggles with nonconvex shapes and unequal densities, '
                                        'but centroids can compress signals. In the worked '
                                        'scenario: Two concentric rings are poorly represented as '
                                        'two centroid-based clusters.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'k-Means Limitations and Vector Quantization?',
                         'options': ['Fit k-means for several k values and inspect assignments.',
                                     'Contrast k-means on blobs versus moon-shaped data.',
                                     'Compare linkage settings and explain one dendrogram cut.',
                                     'Tune eps on a standardized toy dataset and count noise '
                                     'points.'],
                         'correct': 1,
                         'explanation': 'The intended practice is: Contrast k-means on blobs '
                                        'versus moon-shaped data.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Low within-cluster inertia does not '
                                     'prove the discovered clusters are useful.',
                         'type': 'open'}],
          'passing_score': 70}}
