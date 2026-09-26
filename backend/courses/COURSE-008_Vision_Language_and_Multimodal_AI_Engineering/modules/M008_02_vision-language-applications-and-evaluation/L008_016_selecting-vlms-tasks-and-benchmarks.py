"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-016'
MODULE_ID = 'M008-02'
LESSON_META = {'lesson_id': 'L008-016',
 'module_id': 'M008-02',
 'title': 'Selecting VLMs, Tasks & Benchmarks',
 'learning_objective': 'Use explicit constraints and measurable evidence to make engineering decisions for selecting '
                       'vlms, tasks & benchmarks.',
 'curriculum_role': 'APPLIED SYNTHESIS',
 'concepts': ['Selecting VLMs', 'Tasks', 'Benchmarks', 'multimodal engineering'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 2,
                      'chapter_title': 'Vision Language Model Applications',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 45,
 'prerequisites': ['L008-015'],
 'visuals': [],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Selecting VLMs, Tasks & Benchmarks',
 'slug': 'course-008-selecting-vlms-tasks-and-benchmarks',
 'description': 'Use explicit constraints and measurable evidence to make engineering decisions for selecting vlms, '
                'tasks & benchmarks.',
 'order': 8,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['multimodal-ai', 'selecting-vlms', 'tasks', 'benchmarks', 'multimodal-engineering'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Selecting VLMs, Tasks & Benchmarks',
            'content': '# Selecting VLMs, Tasks & Benchmarks\n'
                       '\n'
                       '## Learning objective\n'
                       'Use explicit constraints and measurable evidence to make engineering decisions for selecting '
                       'vlms, tasks & benchmarks.\n'
                       '\n'
                       '## Curriculum role\n'
                       'APPLIED SYNTHESIS\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 2: Vision Language Model Applications\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Vision-Language Applications & Evaluation**. It keeps prerequisite '
                       'material concise and focuses on the new multimodal engineering capability: connecting '
                       'representation, data, architecture, training, evaluation, or deployment decisions to '
                       'observable system behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **Selecting VLMs**\n'
                       '- **Tasks**\n'
                       '- **Benchmarks**\n'
                       '- **multimodal engineering**\n'
                       '\n'
                       '## Engineering workflow\n'
                       '1. Define the task, modality inputs/outputs, and measurable constraint.\n'
                       '2. Establish the smallest reproducible baseline before adding complexity.\n'
                       '3. Inspect an intermediate artifact: tensor shapes, visual tokens, masks, embeddings, '
                       'rankings, traces, cache use, or action outputs.\n'
                       '4. Apply the target technique while changing one major variable at a time.\n'
                       '5. Measure the effect on quality plus at least one engineering metric where relevant.\n'
                       '6. Record a realistic failure mode and distinguish where in the multimodal pipeline it '
                       'originates.\n'
                       '7. State the evidence required to keep, reject, or modify the approach.\n'
                       '\n'
                       '## Practice\n'
                       'Run a controlled example of the target VLM task, define an appropriate metric or rubric, then '
                       'compare one successful and one failed prediction.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **Selecting VLMs, Tasks & Benchmarks** with a controlled '
                       'input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Separate perception errors, reasoning errors, metric mismatch, and benchmark leakage.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **Selecting VLMs, Tasks & Benchmarks**, provide '
                       'evidence from the practice artifact, identify one realistic failure, and state what would '
                       'change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Selecting VLMs, Tasks & Benchmarks — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Use explicit constraints and '
                               'measurable evidence to make engineering decisions for selecting vlms, tasks & '
                               'benchmarks.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['selecting-vlms', 'tasks', 'benchmarks']},
               {'title': 'Selecting VLMs, Tasks & Benchmarks — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Selecting VLMs, Tasks & Benchmarks — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Selecting VLMs, Tasks & Benchmarks?',
                         'options': ['Use explicit constraints and measurable evidence to make engineering decisions '
                                     'for selecting vlms, tasks & benchmarks.',
                                     'Memorize the source without testing it',
                                     'Choose the largest model regardless of constraints',
                                     'Skip evaluation if inference succeeds'],
                         'correct': 0,
                         'explanation': 'The lesson is organized around the stated multimodal engineering objective.'},
                        {'question': 'Which workflow best matches the Masar implementation standard?',
                         'options': ['Learn → Practice → Build → Debug → Evaluate',
                                     'Read → Memorize → Stop',
                                     'Train once → Deploy without evaluation',
                                     'Choose a framework before defining the task'],
                         'correct': 0,
                         'explanation': 'COURSE-008 preserves Masar’s implementation-oriented learning loop.'},
                        {'question': 'How should fast-moving model/API examples from the source be handled?',
                         'options': ['Preserve the concept, revalidate the current implementation, and label '
                                     'modernization',
                                     'Silently assume every API is unchanged',
                                     'Invent successful benchmark numbers',
                                     'Remove the architectural concept entirely'],
                         'correct': 0,
                         'explanation': 'Source fidelity and modernization are tracked separately.'}],
          'passing_score': 70},
 'project': {'title': 'VLM Applications & Evaluation Lab',
             'description': 'Implement a compact suite covering representative VLM tasks and evaluate each with '
                            'task-appropriate metrics and failure analysis.',
             'difficulty': DifficultyLevel.intermediate,
             'tech_stack': ['Python', 'Transformers', 'evaluation metrics'],
             'objectives': ['Integrate the core capabilities from Vision-Language Applications & Evaluation',
                            'Build a reproducible artifact rather than a one-off demo',
                            'Measure quality and at least one engineering constraint',
                            'Diagnose at least one realistic multimodal failure',
                            'Document architecture decisions, limitations, and acceptance criteria'],
             'rubric': {'implementation': 30,
                        'evaluation': 25,
                        'debugging': 20,
                        'architecture_tradeoffs': 15,
                        'reproducibility': 10},
             'starter_repo_url': None,
             'estimated_hours': 3.0}}
