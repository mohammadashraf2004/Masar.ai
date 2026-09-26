"""M01.L05 — Prepare and Explore Iris Data.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 1, pages 17–20. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L05"
MODULE_ORDER = 1
MODULE_TITLE = 'ML Fundamentals & First Model'
MODULE_DESCRIPTION = 'Frame a supervised problem and train the first reproducible iris classifier.'
SOURCE_CHAPTER = 1
SOURCE_PAGES = '17–20'

TOPIC = {'title': 'Prepare and Explore Iris Data',
 'slug': 'ml-foundations-m01-l05',
 'description': 'Inspect class frequencies and pairwise feature plots using only development data '
                'before drawing modeling conclusions.',
 'order': 5,
 'difficulty': DifficultyLevel.beginner,
 'estimated_hours': 0.5833,
 'skill_tags': ['machine-learning', 'foundations', 'module-01'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Prepare and Explore Iris Data',
            'content': '# Prepare and Explore Iris Data\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M01.L05 | '
                       '**Module:** ML Fundamentals & First Model\n'
                       '> **Source alignment:** BOOK-001, Chapter 1, pages 17–20. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Inspect class frequencies and pairwise feature plots using only '
                       'development data before drawing modeling conclusions.\n'
                       '- Apply the principle to: A scatter matrix can reveal separability, '
                       'overlap and unusual points without proving generalization.\n'
                       '- Complete the activity and defend its evaluation or interpretation: '
                       'Create a stratified train/test split and explore the training portion.\n'
                       '\n'
                       '## Why this matters\n'
                       'Frame a supervised problem and train the first reproducible iris '
                       'classifier. This lesson focuses on **prepare and explore iris data** so '
                       'you can make an explicit choice rather than blindly applying a library '
                       'default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Inspect class frequencies and pairwise feature plots using only '
                       'development data before drawing modeling conclusions.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A scatter matrix can reveal separability, overlap and unusual points '
                       'without proving generalization. Before claiming that a method works, check '
                       'what data it uses, which predictions or patterns it produces, and how '
                       'those outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Create a stratified train/test split and explore the training portion. '
                       'Record your assumptions, relevant parameters and the observed result. '
                       'Explain how the result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'A plot showing clustered points does not establish predictive accuracy. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.model_selection import train_test_split\n'
                       'X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, '
                       'random_state=42)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **prepare and explore iris data** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** Inspect class frequencies and pairwise feature plots '
                       'using only development data before drawing modeling conclusions.\n',
            'estimated_minutes': 35,
            'has_code_examples': True},
 'exercises': [{'title': 'Prepare and Explore Iris Data — hands-on activity',
                'description': 'Create a stratified train/test split and explore the training '
                               'portion. Deliver a short notebook, annotated example or written '
                               'calculation with your result and interpretation.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['machine-learning', 'foundations', 'module-01']},
               {'title': 'Prepare and Explore Iris Data — critical reasoning',
                'description': 'Consider this boundary: A plot showing clustered points does not '
                               'establish predictive accuracy. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.beginner,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Prepare and Explore Iris Data — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Prepare '
                                     'and Explore Iris Data?',
                         'options': ['Only handcrafted rules can make a useful prediction.',
                                     'A perfect training score guarantees new-data accuracy.',
                                     'Inspect class frequencies and pairwise feature plots using '
                                     'only development data before drawing modeling conclusions.',
                                     'Features and labels are interchangeable.'],
                         'correct': 2,
                         'explanation': 'Inspect class frequencies and pairwise feature plots '
                                        'using only development data before drawing modeling '
                                        'conclusions. In the worked scenario: A scatter matrix can '
                                        'reveal separability, overlap and unusual points without '
                                        'proving generalization.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Prepare and Explore Iris Data?',
                         'options': ['Create a stratified train/test split and explore the '
                                     'training portion.',
                                     'Describe a prediction problem with its input, target and '
                                     'intended user.',
                                     'Classify three scenarios and sketch X and y for each.',
                                     "Inspect an array's shape, dataset labels and Python package "
                                     'imports.'],
                         'correct': 0,
                         'explanation': 'The intended practice is: Create a stratified train/test '
                                        'split and explore the training portion.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? A plot showing clustered points does '
                                     'not establish predictive accuracy.',
                         'type': 'open'}],
          'passing_score': 70}}
