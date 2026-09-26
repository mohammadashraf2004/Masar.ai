"""M20.L08 — Topic Modeling with LDA.

One Topic -> one Lesson + two Exercises + a Quiz + optional module Project.
BOOK-001, Chapter 7, pages 347–355. Instructor-authored structured draft.
"""
from app.models.learning import DifficultyLevel

LESSON_CODE = "M20.L08"
MODULE_ORDER = 20
MODULE_TITLE = 'Machine Learning for Text'
MODULE_DESCRIPTION = 'Represent English text and build supervised sentiment and unsupervised topic-analysis workflows.'
SOURCE_CHAPTER = 7
SOURCE_PAGES = '347–355'

TOPIC = {'title': 'Topic Modeling with LDA',
 'slug': 'ml-foundations-m20-l08',
 'description': 'Latent Dirichlet Allocation estimates topic-word patterns and document-topic '
                'mixtures; validate proposed topic names through representative documents.',
 'order': 8,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.9167,
 'skill_tags': ['machine-learning', 'foundations', 'module-20'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Topic Modeling with LDA',
            'content': '# Topic Modeling with LDA\n'
                       '\n'
                       '> **Course:** Machine Learning Foundations | **Lesson:** M20.L08 | '
                       '**Module:** Machine Learning for Text\n'
                       '> **Source alignment:** BOOK-001, Chapter 7, pages 347–355. This is an '
                       'original curriculum adaptation, not an excerpt from the book.\n'
                       '\n'
                       '## Learning outcomes\n'
                       '- Explain: Latent Dirichlet Allocation estimates topic-word patterns and '
                       'document-topic mixtures; validate proposed topic names through '
                       'representative documents.\n'
                       '- Apply the principle to: A topic with musical words should be checked '
                       'against high-weight movie reviews.\n'
                       '- Complete the activity and defend its evaluation or interpretation: Fit a '
                       'compact LDA model and report top words and three representative '
                       'documents.\n'
                       '\n'
                       '## Why this matters\n'
                       'Represent English text and build supervised sentiment and unsupervised '
                       'topic-analysis workflows. This lesson focuses on **topic modeling with '
                       'lda** so you can make an explicit choice rather than blindly applying a '
                       'library default.\n'
                       '\n'
                       '## Core explanation\n'
                       'Latent Dirichlet Allocation estimates topic-word patterns and '
                       'document-topic mixtures; validate proposed topic names through '
                       'representative documents.\n'
                       '\n'
                       '## Worked scenario\n'
                       'A topic with musical words should be checked against high-weight movie '
                       'reviews. Before claiming that a method works, check what data it uses, '
                       'which predictions or patterns it produces, and how those outputs would be '
                       'assessed in the intended application.\n'
                       '\n'
                       '## Guided practice\n'
                       'Fit a compact LDA model and report top words and three representative '
                       'documents. Record your assumptions, relevant parameters and the observed '
                       'result. Explain how the result supports—or fails to support—your '
                       'decision.\n'
                       '\n'
                       '## Important boundary or misconception\n'
                       'Automatically discovered components are not verified human categories. '
                       'Explain how your method respects this boundary or avoids the corresponding '
                       'misconception.\n'
                       '\n'
                       '## Python starting point\n'
                       '\n'
                       'The following is a compact starting example. Run it in a notebook with its '
                       'required variables defined where applicable; adapt it for the exercise.\n'
                       '\n'
                       '```python\n'
                       'from sklearn.decomposition import LatentDirichletAllocation\n'
                       'lda = LatentDirichletAllocation(n_components=10, random_state=42)\n'
                       '```\n'
                       '\n'
                       '## Self-check\n'
                       'Explain **topic modeling with lda** in your own words and answer: what '
                       'would change in the worked scenario if you ignored the boundary above?\n'
                       '\n'
                       '**Retain this idea:** Latent Dirichlet Allocation estimates topic-word '
                       'patterns and document-topic mixtures; validate proposed topic names '
                       'through representative documents.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Topic Modeling with LDA — hands-on activity',
                'description': 'Fit a compact LDA model and report top words and three '
                               'representative documents. Deliver a short notebook, annotated '
                               'example or written calculation with your result and '
                               'interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['machine-learning', 'foundations', 'module-20']},
               {'title': 'Topic Modeling with LDA — critical reasoning',
                'description': 'Consider this boundary: Automatically discovered components are '
                               'not verified human categories. Explain a failure mode if it is '
                               'ignored and the safeguard you would use.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['evaluation', 'reasoning']}],
 'quiz': {'title': 'Topic Modeling with LDA — Knowledge Check',
          'questions': [{'question': 'Which statement accurately captures the main idea of Topic '
                                     'Modeling with LDA?',
                         'options': ['Latent Dirichlet Allocation estimates topic-word patterns '
                                     'and document-topic mixtures; validate proposed topic names '
                                     'through representative documents.',
                                     'Every string column is free-form natural language.',
                                     'The vocabulary should be fitted on all test documents.',
                                     'Topic-model word groups are validated human categories.'],
                         'correct': 0,
                         'explanation': 'Latent Dirichlet Allocation estimates topic-word patterns '
                                        'and document-topic mixtures; validate proposed topic '
                                        'names through representative documents. In the worked '
                                        'scenario: A topic with musical words should be checked '
                                        'against high-weight movie reviews.'},
                        {'question': 'Which activity directly demonstrates the intended skill in '
                                     'Topic Modeling with LDA?',
                         'options': ['Load review examples and describe label balance and '
                                     'formatting problems.',
                                     'Fit CountVectorizer on tiny texts and inspect vocabulary_ '
                                     'and shape.',
                                     'Fit a compact LDA model and report top words and three '
                                     'representative documents.',
                                     'Compare a baseline and filtered word-count pipeline under '
                                     'the same CV.'],
                         'correct': 2,
                         'explanation': 'The intended practice is: Fit a compact LDA model and '
                                        'report top words and three representative documents.'},
                        {'question': 'What risk does this important boundary highlight, and how '
                                     'would you address it? Automatically discovered components '
                                     'are not verified human categories.',
                         'type': 'open'}],
          'passing_score': 70},
 'project': {'title': 'Sentiment and Topic Exploration',
             'description': 'Build a sparse-text sentiment pipeline and independently interpret '
                            'document topics through representative samples.',
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
