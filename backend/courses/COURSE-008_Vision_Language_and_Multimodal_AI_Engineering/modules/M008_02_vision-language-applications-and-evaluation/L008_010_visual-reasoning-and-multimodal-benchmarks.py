"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-010'
MODULE_ID = 'M008-02'
LESSON_META = {'lesson_id': 'L008-010',
 'module_id': 'M008-02',
 'title': 'Visual Reasoning & Multimodal Benchmarks',
 'learning_objective': 'Measure and interpret visual reasoning & multimodal benchmarks with task-appropriate metrics, '
                       'controlled baselines, and failure analysis.',
 'curriculum_role': 'CORE',
 'concepts': ['Visual Reasoning', 'Multimodal Benchmarks', 'multimodal engineering', 'controlled experiments'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 2,
                      'chapter_title': 'Vision Language Model Applications',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 50,
 'prerequisites': ['L008-009'],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Visual Reasoning & Multimodal Benchmarks',
 'slug': 'course-008-visual-reasoning-and-multimodal-benchmarks',
 'description': 'Measure and interpret visual reasoning & multimodal benchmarks with task-appropriate metrics, '
                'controlled baselines, and failure analysis.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.83,
 'skill_tags': ['multimodal-ai',
                'visual-reasoning',
                'multimodal-benchmarks',
                'multimodal-engineering',
                'controlled-experiments'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Visual Reasoning & Multimodal Benchmarks',
            'content': '# Visual Reasoning & Multimodal Benchmarks\n'
                       '\n'
                       '## Learning objective\n'
                       'Measure and interpret visual reasoning & multimodal benchmarks with task-appropriate metrics, '
                       'controlled baselines, and failure analysis.\n'
                       '\n'
                       '## Curriculum role\n'
                       'CORE\n'
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
                       '- **Visual Reasoning**\n'
                       '- **Multimodal Benchmarks**\n'
                       '- **multimodal engineering**\n'
                       '- **controlled experiments**\n'
                       '\n'
                       '{{figure:visual-reasoning-example}}\n'
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
                       '**Lesson-specific goal:** demonstrate **Visual Reasoning & Multimodal Benchmarks** with a '
                       'controlled input set and at least one difficult example.\n'
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
                       'Explain the principal engineering trade-off in **Visual Reasoning & Multimodal Benchmarks**, '
                       'provide evidence from the practice artifact, identify one realistic failure, and state what '
                       'would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 50,
            'has_code_examples': True},
 'exercises': [{'title': 'Visual Reasoning & Multimodal Benchmarks — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Measure and interpret visual '
                               'reasoning & multimodal benchmarks with task-appropriate metrics, controlled baselines, '
                               'and failure analysis.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['visual-reasoning', 'multimodal-benchmarks', 'multimodal-engineering']},
               {'title': 'Visual Reasoning & Multimodal Benchmarks — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Visual Reasoning & Multimodal Benchmarks — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Visual Reasoning & Multimodal Benchmarks?',
                         'options': ['Measure and interpret visual reasoning & multimodal benchmarks with '
                                     'task-appropriate metrics, controlled baselines, and failure analysis.',
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
 'project': None}
