"""M09.L04 — DBSCAN and Density-Based Groups.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 187–191. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M09.L04"
MODULE_ORDER = 9
MODULE_TITLE = 'Clustering Algorithms'
MODULE_DESCRIPTION = 'Select clustering methods from the geometry and density of the dataset.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '187–191'

TOPIC = {'title': 'DBSCAN and Density-Based Groups',
 'slug': 'ml-foundations-m09-l04',
 'description': 'DBSCAN grows clusters from dense neighborhoods and labels sparse points as noise; '
                'eps and min_samples interact with scaling.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.8333,
 'skill_tags': ['machine-learning', 'foundations', 'module-09'],
 'prerequisite_ids': [],
 'lesson': {'title': 'DBSCAN and Density-Based Groups',
            'content': '# DBSCAN and Density-Based Groups\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M09.L04 | '
                       '**Module:** Clustering Algorithms\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 187–191. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: DBSCAN grows clusters from dense neighborhoods and labels '
                       'sparse points as noise; eps and min_samples interact with scaling.\n'
                       '- Apply the principle to: Two curved moons can be detected as two '
                       'density-connected groups.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Tune '
                       'eps on a standardized toy dataset and count noise points.\n'
                       '\n'
                       '## Why this matters\n'
                       'Select clustering methods from the geometry and density of the dataset. '
                       'This lesson focuses on **dbscan and density-based groups** so you can make '
                       'an explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'DBSCAN grows clusters from dense neighborhoods and labels sparse points as '
                       'noise; eps and min_samples interact with scaling.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Two curved moons can be detected as two density-connected groups. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Tune eps on a standardized toy dataset and count noise points. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A DBSCAN noise label is not proof of an anomalous or harmful real-world '
                       'case. Explain how your method respects this boundary or avoids the '
                       'corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.cluster import DBSCAN\n'
                       'model = DBSCAN(eps=0.5, min_samples=5)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **dbscan and density-based groups** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** DBSCAN grows clusters from dense neighborhoods and '
                       'labels sparse points as noise; eps and min_samples interact with '
                       'scaling.\n',
            'estimated_minutes': 50,
            'has_code_examples': True},
 'exercises': [{'title': 'DBSCAN and Density-Based Groups — hands-on activity',
                'description': 'Tune eps on a standardized toy dataset and count noise points. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-09']},
               {'title': 'DBSCAN and Density-Based Groups — critical reasoning',
                'description': 'Consider this boundary: A DBSCAN noise label is not proof of an '
                               'anomalous or harmful real-world case. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'DBSCAN and Density-Based Groups — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of DBSCAN '
                                     'and Density-Based Groups?',
                         'options': ['Cluster IDs encode an inherent ranking.',
                                     'DBSCAN grows clusters from dense neighborhoods and labels '
                                     'sparse points as noise; eps and min_samples interact with '
                                     'scaling.',
                                     'Every clustering method detects every possible shape equally '
                                     'well.',
                                     'A low inertia alone validates a clustering solution.'],
                         'correct': 1,
                         'explanation': 'DBSCAN grows clusters from dense neighborhoods and labels '
                                        'sparse points as noise; eps and min_samples interact with '
                                        'scaling. In the worked scenario: Two curved moons can be '
                                        'detected as two density-connected groups.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'DBSCAN and Density-Based Groups?',
                         'options': ['Fit k-means for several k values and inspect assignments.',
                                     'Contrast k-means on blobs versus moon-shaped data.',
                                     'Compare linkage settings and explain one dendrogram cut.',
                                     'Tune eps on a standardized toy dataset and count noise '
                                     'points.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Tune eps on a standardized toy '
                                        'dataset and count noise points.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A DBSCAN noise label is not proof of '
                                     'an anomalous or harmful real-world case.',
                         'type': 'open'}],
          'passing_score': 70}}
