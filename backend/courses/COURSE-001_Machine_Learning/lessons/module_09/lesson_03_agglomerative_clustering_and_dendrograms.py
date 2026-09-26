"""M09.L03 — Agglomerative Clustering and Dendrograms.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 181–187. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M09.L03"
MODULE_ORDER = 9
MODULE_TITLE = 'Clustering Algorithms'
MODULE_DESCRIPTION = 'Select clustering methods from the geometry and density of the dataset.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '181–187'

TOPIC = {'title': 'Agglomerative Clustering and Dendrograms',
 'slug': 'ml-foundations-m09-l03',
 'description': 'Agglomerative clustering merges nearby groups into a hierarchy; linkage choices '
                'and dendrogram cuts define final groups.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-09'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Agglomerative Clustering and Dendrograms',
            'content': '# Agglomerative Clustering and Dendrograms\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M09.L03 | '
                       '**Module:** Clustering Algorithms\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 181–187. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Agglomerative clustering merges nearby groups into a hierarchy; '
                       'linkage choices and dendrogram cuts define final groups.\n'
                       '- Apply the principle to: A dendrogram records successive merges rather '
                       'than forcing one fixed k immediately.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Compare linkage settings and explain one dendrogram cut.\n'
                       '\n'
                       '## Why this matters\n'
                       'Select clustering methods from the geometry and density of the dataset. '
                       'This lesson focuses on **agglomerative clustering and dendrograms** so you '
                       'can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Agglomerative clustering merges nearby groups into a hierarchy; linkage '
                       'choices and dendrogram cuts define final groups.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A dendrogram records successive merges rather than forcing one fixed k '
                       'immediately. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Compare linkage settings and explain one dendrogram cut. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       "Do not read the dendrogram's visual spacing as a universal probability. "
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.cluster import AgglomerativeClustering\n'
                       'model = AgglomerativeClustering(n_clusters=3)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **agglomerative clustering and dendrograms** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Agglomerative clustering merges nearby groups into a '
                       'hierarchy; linkage choices and dendrogram cuts define final groups.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Agglomerative Clustering and Dendrograms — hands-on activity',
                'description': 'Compare linkage settings and explain one dendrogram cut. Deliver a '
                               'short notebook, annotated example or written calculation with your '
                               'result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-09']},
               {'title': 'Agglomerative Clustering and Dendrograms — critical reasoning',
                'description': "Consider this boundary: Do not read the dendrogram's visual "
                               'spacing as a universal probability. Explain a failure mode if it '
                               'is ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Agglomerative Clustering and Dendrograms — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Agglomerative Clustering and Dendrograms?',
                         'options': ['Agglomerative clustering merges nearby groups into a '
                                     'hierarchy; linkage choices and dendrogram cuts define final '
                                     'groups.',
                                     'Cluster IDs encode an inherent ranking.',
                                     'Every clustering method detects every possible shape equally '
                                     'well.',
                                     'A low inertia alone validates a clustering solution.'],
                         'correct': 0,
                         'explanation': 'Agglomerative clustering merges nearby groups into a '
                                        'hierarchy; linkage choices and dendrogram cuts define '
                                        'final groups. In the worked scenario: A dendrogram '
                                        'records successive merges rather than forcing one fixed k '
                                        'immediately.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Agglomerative Clustering and Dendrograms?',
                         'options': ['Fit k-means for several k values and inspect assignments.',
                                     'Contrast k-means on blobs versus moon-shaped data.',
                                     'Compare linkage settings and explain one dendrogram cut.',
                                     'Tune eps on a standardized toy dataset and count noise '
                                     'points.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Compare linkage settings and '
                                        'explain one dendrogram cut.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     "would you address it? Do not read the dendrogram's visual "
                                     'spacing as a universal probability.',
                         'type': 'open'}],
          'passing_score': 70}}
