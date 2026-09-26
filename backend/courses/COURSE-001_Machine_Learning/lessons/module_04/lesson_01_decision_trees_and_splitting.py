"""M04.L01 — Decision Trees and Splitting.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 2, pages 70–77. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M04.L01"
MODULE_ORDER = 4
MODULE_TITLE = 'Decision Trees & Ensembles'
MODULE_DESCRIPTION = 'Interpret tree decisions, compare ensemble methods, and recognize non-extrapolation and attribution limits.'
SOURCE_CHAPTER = 2
SOURCE_PAGES = '70–77'

TOPIC = {'title': 'Decision Trees and Splitting',
 'slug': 'ml-foundations-m04-l01',
 'description': 'A decision tree partitions feature space through successive threshold questions; '
                'depth controls expressiveness.',
 'order': 1,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.6667,
 'skill_tags': ['machine-learning', 'foundations', 'module-04'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Decision Trees and Splitting',
            'content': '# Decision Trees and Splitting\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M04.L01 | '
                       '**Module:** Decision Trees & Ensembles\n'
                       '> **Source alignment:** BOOK-001, Chapter 2, pages 70–77. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: A decision tree partitions feature space through successive '
                       'threshold questions; depth controls expressiveness.\n'
                       '- Apply the principle to: One branch asks whether petal length exceeds a '
                       'learned threshold before asking another question.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit a '
                       'small tree, visualize paths and explain a prediction.\n'
                       '\n'
                       '## Why this matters\n'
                       'Interpret tree decisions, compare ensemble methods, and recognize '
                       'non-extrapolation and attribution limits. This lesson focuses on '
                       '**decision trees and splitting** so you can make an explicit choice rather '
                       'than blindly applying a library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'A decision tree partitions feature space through successive threshold '
                       'questions; depth controls expressiveness.\n'
                       '\n'
                       '## Worked scenario\n'
                       'One branch asks whether petal length exceeds a learned threshold before '
                       'asking another question. Before claiming that a method works, check what '
                       'data it uses, which predictions or patterns it produces, and how those '
                       'outputs would be assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit a small tree, visualize paths and explain a prediction. Record your '
                       'assumptions, relevant parameters and the observed result. Explain how the '
                       'result supports—or fails to support—your decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Unrestricted trees can overfit a small training set. Explain how your '
                       'method respects this boundary or avoids the corresponding misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.tree import DecisionTreeClassifier\n'
                       'classifier = DecisionTreeClassifier(max_depth=3, random_state=42)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **decision trees and splitting** in your own words and answer: '
                       'what would change in the worked scenario if you ignored the boundary '
                       'above?\n'
                       '\n'
                       '**Retain this idea:** A decision tree partitions feature space through '
                       'successive threshold questions; depth controls expressiveness.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Decision Trees and Splitting — hands-on activity',
                'description': 'Fit a small tree, visualize paths and explain a prediction. '
                               'Deliver a short notebook, annotated example or written calculation '
                               'with your result and interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-04']},
               {'title': 'Decision Trees and Splitting — critical reasoning',
                'description': 'Consider this boundary: Unrestricted trees can overfit a small '
                               'training set. Explain a failure mode if it is ignored and the '
                               'safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Decision Trees and Splitting — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of '
                                     'Decision Trees and Splitting?',
                         'options': ['Feature importance proves causal influence.',
                                     'A decision tree partitions feature space through successive '
                                     'threshold questions; depth controls expressiveness.',
                                     'A single unrestricted tree cannot overfit.',
                                     'Trees automatically extrapolate continuous trends.'],
                         'correct': 1,
                         'explanation': 'A decision tree partitions feature space through '
                                        'successive threshold questions; depth controls '
                                        'expressiveness. In the worked scenario: One branch asks '
                                        'whether petal length exceeds a learned threshold before '
                                        'asking another question.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Decision Trees and Splitting?',
                         'options': ['Compare feature importances with a held-out performance and '
                                     'extrapolation check.',
                                     'Fit a forest and compare it with a single tree using the '
                                     'same split.',
                                     'Compare boosted-tree settings with a forest on validation '
                                     'data.',
                                     'Fit a small tree, visualize paths and explain a prediction.'],
                         'correct': 3,
                         'explanation': 'The intended practice is: Fit a small tree, visualize '
                                        'paths and explain a prediction.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Unrestricted trees can overfit a small '
                                     'training set.',
                         'type': 'open'}],
          'passing_score': 70}}
