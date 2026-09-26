"""M09.L01 — k-Means Clustering.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 168–173. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M09.L01"
MODULE_ORDER = 9
MODULE_TITLE = 'Clustering Algorithms'
MODULE_DESCRIPTION = 'Select clustering methods from the geometry and density of the dataset.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '168–173'

TOPIC = {'title': 'k-Means Clustering',
 'slug': 'ml-foundations-m09-l01',
 'description': 'k-means iteratively assigns points to nearest centers and updates centers; k must '
                'be chosen and results depend on initialization.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-09'],
 'prerequisite_ids': [],
 'lesson': {'title': 'k-Means Clustering',
            'content': '# k-Means Clustering\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M09.L01 | '
                       '**Module:** Clustering Algorithms\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 168–173. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: k-means iteratively assigns points to nearest centers and '
                       'updates centers; k must be chosen and results depend on initialization.\n'
                       '- Apply the principle to: Three compact round point clouds can be '
                       'summarized by three centroids.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit '
                       'k-means for several k values and inspect assignments.\n'
                       '\n'
                       '## Why this matters\n'
                       'Select clustering methods from the geometry and density of the dataset. '
                       'This lesson focuses on **k-means clustering** so you can make an explicit '
                       'choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'k-means iteratively assigns points to nearest centers and updates centers; '
                       'k must be chosen and results depend on initialization.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Three compact round point clouds can be summarized by three centroids. '
                       'Before claiming that a method works, check what data it uses, which '
                       'predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit k-means for several k values and inspect assignments. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Cluster labels such as 0 and 1 have no intrinsic semantic order. Explain '
                       'how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.cluster import KMeans\n'
                       'model = KMeans(n_clusters=3, random_state=42, n_init=10)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **k-means clustering** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** k-means iteratively assigns points to nearest '
                       'centers and updates centers; k must be chosen and results depend on '
                       'initialization.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'k-Means Clustering — hands-on activity',
                'description': 'Fit k-means for several k values and inspect assignments. Deliver '
                               'a short notebook, annotated example or written calculation with '
                               'your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-09']},
               {'title': 'k-Means Clustering — critical reasoning',
                'description': 'Consider this boundary: Cluster labels such as 0 and 1 have no '
                               'intrinsic semantic order. Explain a failure mode if it is ignored '
                               'and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'k-Means Clustering — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of k-Means '
                                     'Clustering?',
                         'options': ['Cluster IDs encode an inherent ranking.',
                                     'Every clustering method detects every possible shape equally '
                                     'well.',
                                     'k-means iteratively assigns points to nearest centers and '
                                     'updates centers; k must be chosen and results depend on '
                                     'initialization.',
                                     'A low inertia alone validates a clustering solution.'],
                         'correct': 2,
                         'explanation': 'k-means iteratively assigns points to nearest centers and '
                                        'updates centers; k must be chosen and results depend on '
                                        'initialization. In the worked scenario: Three compact '
                                        'round point clouds can be summarized by three centroids.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'k-Means Clustering?',
                         'options': ['Fit k-means for several k values and inspect assignments.',
                                     'Contrast k-means on blobs versus moon-shaped data.',
                                     'Compare linkage settings and explain one dendrogram cut.',
                                     'Tune eps on a standardized toy dataset and count noise '
                                     'points.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Fit k-means for several k '
                                        'values and inspect assignments.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Cluster labels such as 0 and 1 have no '
                                     'intrinsic semantic order.',
                         'type': 'open'}],
          'passing_score': 70}}
