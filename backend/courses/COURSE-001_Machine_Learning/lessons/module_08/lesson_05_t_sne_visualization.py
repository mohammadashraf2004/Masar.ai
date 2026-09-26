"""M08.L05 — t-SNE Visualization.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 3, pages 163–168. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L05"
MODULE_ORDER = 8
MODULE_TITLE = 'Dimensionality Reduction & Feature Extraction'
MODULE_DESCRIPTION = 'Understand PCA, NMF and t-SNE as tools with distinct goals and constraints.'
SOURCE_CHAPTER = 3
SOURCE_PAGES = '163–168'

TOPIC = {'title': 't-SNE Visualization',
 'slug': 'ml-foundations-m08-l05',
 'description': 't-SNE is a nonlinear visualization method preserving local neighborhoods '
                'approximately; plot coordinates should not be treated as measurements.',
 'order': 5,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-08'],
 'prerequisite_ids': [],
 'lesson': {'title': 't-SNE Visualization',
            'content': '# t-SNE Visualization\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M08.L05 | '
                       '**Module:** Dimensionality Reduction & Feature Extraction\n'
                       '> **Source alignment:** BOOK-001, Chapter 3, pages 163–168. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: t-SNE is a nonlinear visualization method preserving local '
                       'neighborhoods approximately; plot coordinates should not be treated as '
                       'measurements.\n'
                       '- Apply the principle to: Nearby points in a 2D embedding may share '
                       'structure, but apparent cluster sizes can mislead.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Contrast a PCA scatter with a t-SNE plot and record caveats.\n'
                       '\n'
                       '## Why this matters\n'
                       'Understand PCA, NMF and t-SNE as tools with distinct goals and '
                       'constraints. This lesson focuses on **t-sne visualization** so you can '
                       'make an explicit choice rather than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       't-SNE is a nonlinear visualization method preserving local neighborhoods '
                       'approximately; plot coordinates should not be treated as measurements.\n'
                       '\n'
                       '## Worked scenario\n'
                       'Nearby points in a 2D embedding may share structure, but apparent cluster '
                       'sizes can mislead. Before claiming that a method works, check what data it '
                       'uses, which predictions or patterns it produces, and how those outputs '
                       'would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Contrast a PCA scatter with a t-SNE plot and record caveats. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Standard scikit-learn TSNE has no transform for unseen samples. Explain '
                       'how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **t-sne visualization** in your own words and answer: what would '
                       'change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** t-SNE is a nonlinear visualization method preserving '
                       'local neighborhoods approximately; plot coordinates should not be treated '
                       'as measurements.\n',
            'estimated_minutes': 35,
            'has_code_examples': False},
 'exercises': [{'title': 't-SNE Visualization — hands-on activity',
                'description': 'Contrast a PCA scatter with a t-SNE plot and record caveats. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-08']},
               {'title': 't-SNE Visualization — critical reasoning',
                'description': 'Consider this boundary: Standard scikit-learn TSNE has no '
                               'transform for unseen samples. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 't-SNE Visualization — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of t-SNE '
                                     'Visualization?',
                         'options': ['Maximum variance always identifies the strongest predictor.',
                                     't-SNE is a nonlinear visualization method preserving local '
                                     'neighborhoods approximately; plot coordinates should not be '
                                     'treated as measurements.',
                                     'NMF accepts arbitrary negative input without preprocessing.',
                                     't-SNE axes are calibrated feature measurements.'],
                         'correct': 1,
                         'explanation': 't-SNE is a nonlinear visualization method preserving '
                                        'local neighborhoods approximately; plot coordinates '
                                        'should not be treated as measurements. In the worked '
                                        'scenario: Nearby points in a 2D embedding may share '
                                        'structure, but apparent cluster sizes can mislead.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     't-SNE Visualization?',
                         'options': ['Sketch the first component of an elongated 2D scatterplot.',
                                     'Fit PCA on training data and transform validation data with '
                                     'the same fitted object.',
                                     'Explain why negative input values break standard NMF '
                                     'assumptions.',
                                     'Contrast a PCA scatter with a t-SNE plot and record '
                                     'caveats.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Contrast a PCA scatter with a '
                                        't-SNE plot and record caveats.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Standard scikit-learn TSNE has no '
                                     'transform for unseen samples.',
                         'type': 'open'}],
          'passing_score': 70}}
