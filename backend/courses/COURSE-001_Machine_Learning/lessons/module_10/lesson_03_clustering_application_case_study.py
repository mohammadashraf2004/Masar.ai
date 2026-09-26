"""M10.L03 — Clustering Application Case Study.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 195–209. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M10.L03"
MODULE_ORDER = 10
MODULE_TITLE = 'Clustering Evaluation & Applications'
MODULE_DESCRIPTION = 'Evaluate unlabeled structure carefully and translate patterns into inspectable applications.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '195–209'

TOPIC = {'title': 'Clustering Application Case Study',
 'slug': 'ml-foundations-m10-l03',
 'description': 'Turn clustering outputs into descriptive summaries, inspect representative '
                'samples and record what a domain expert would validate.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['machine-learning', 'foundations', 'module-10'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Clustering Application Case Study',
            'content': '# Clustering Application Case Study\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M10.L03 | '
                       '**Module:** Clustering Evaluation & Applications\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 195–209. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Turn clustering outputs into descriptive summaries, inspect '
                       'representative samples and record what a domain expert would validate.\n'
                       '- Apply the principle to: A cluster of face images may reflect lighting '
                       'rather than identity.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Build '
                       'cluster profiles from features and sample examples without assigning '
                       'unsupported labels.\n'
                       '\n'
                       '## Why this matters\n'
                       'Evaluate unlabeled structure carefully and translate patterns into '
                       'inspectable applications. This lesson focuses on **clustering application '
                       'case study** so you can make an explicit choice rather than blindly '
                       'applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Turn clustering outputs into descriptive summaries, inspect representative '
                       'samples and record what a domain expert would validate.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A cluster of face images may reflect lighting rather than identity. Before '
                       'claiming that a method works, check what data it uses, which predictions '
                       'or patterns it produces, and how those outputs would be assessed in the '
                       'intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Build cluster profiles from features and sample examples without assigning '
                       'unsupported labels. Record your assumptions, relevant parameters and the '
                       'observed result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Do not name unsupervised groups as if they were validated categories. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **clustering application case study** in your own words and '
                       'answer: what would change in the worked scenario if you ignored the '
                       'boundary above?\n'
                       '\n'
                       '**Retain this idea:** Turn clustering outputs into descriptive summaries, '
                       'inspect representative samples and record what a domain expert would '
                       'validate.\n',
            'estimated_minutes': 45,
            'has_code_examples': False},
 'exercises': [{'title': 'Clustering Application Case Study — hands-on activity',
                'description': 'Build cluster profiles from features and sample examples without '
                               'assigning unsupported labels. Deliver a short notebook, annotated '
                               'example or written calculation with your result and '
                               'interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-10']},
               {'title': 'Clustering Application Case Study — critical reasoning',
                'description': 'Consider this boundary: Do not name unsupervised groups as if they '
                               'were validated categories. Explain a failure mode if it is ignored '
                               'and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Clustering Application Case Study — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Clustering Application Case Study?',
                         'options': ['An internal clustering metric proves business relevance.',
                                     'Turn clustering outputs into descriptive summaries, inspect '
                                     'representative samples and record what a domain expert would '
                                     'validate.',
                                     'Cluster IDs must numerically match reference-label IDs.',
                                     'Unsupervised cluster names should be treated as ground '
                                     'truth.'],
                         'correct': 1,
                         'explanation': 'Turn clustering outputs into descriptive summaries, '
                                        'inspect representative samples and record what a domain '
                                        'expert would validate. In the worked scenario: A cluster '
                                        'of face images may reflect lighting rather than '
                                        'identity.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Clustering Application Case Study?',
                         'options': ['Evaluate clustering under two permuted cluster-label '
                                     'encodings.',
                                     'Evaluate silhouette on two structures and explain a '
                                     'disagreement with visual evidence.',
                                     'Inspect only the final test labels to choose every training '
                                     'decision.',
                                     'Build cluster profiles from features and sample examples '
                                     'without assigning unsupported labels.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Build cluster profiles from '
                                        'features and sample examples without assigning '
                                        'unsupported labels.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Do not name unsupervised groups as if '
                                     'they were validated categories.',
                         'type': 'open'}],
          'passing_score': 70},
 'project': {'title': 'Unsupervised Discovery Laboratory',
             'description': 'Compare PCA or NMF representations with clustering, validate '
                            'structure and inspect representative samples.',
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
