"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-024'
MODULE_ID = 'M008-03'
LESSON_META = {'lesson_id': 'L008-024',
 'module_id': 'M008-03',
 'title': 'Packed Multi-Image Training with Placeholder Tokens',
 'learning_objective': 'Implement and reason about packed multi-image training with placeholder tokens while tracking '
                       'data, optimization, memory, and quality trade-offs.',
 'curriculum_role': 'ADVANCED PRACTICAL',
 'concepts': ['Packed Multi-Image Training with Placeholder Tokens',
              'multimodal engineering',
              'controlled experiments',
              'failure analysis'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 3,
                      'chapter_title': 'Vision Language Model Training',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 65,
 'prerequisites': ['L008-023', 'M008-01'],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Packed Multi-Image Training with Placeholder Tokens',
 'slug': 'course-008-packed-multi-image-training-with-placeholder-tokens',
 'description': 'Implement and reason about packed multi-image training with placeholder tokens while tracking data, '
                'optimization, memory, and quality trade-offs.',
 'order': 8,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.08,
 'skill_tags': ['multimodal-ai',
                'packed-multi-image-training-with-placeholder-tokens',
                'multimodal-engineering',
                'controlled-experiments',
                'failure-analysis'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Packed Multi-Image Training with Placeholder Tokens',
            'content': '# Packed Multi-Image Training with Placeholder Tokens\n'
                       '\n'
                       '## Learning objective\n'
                       'Implement and reason about packed multi-image training with placeholder tokens while tracking '
                       'data, optimization, memory, and quality trade-offs.\n'
                       '\n'
                       '## Curriculum role\n'
                       'ADVANCED PRACTICAL\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 3: Vision Language Model Training\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Training Vision-Language Models from First Principles**. It keeps '
                       'prerequisite material concise and focuses on the new multimodal engineering capability: '
                       'connecting representation, data, architecture, training, evaluation, or deployment decisions '
                       'to observable system behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **Packed Multi-Image Training with Placeholder Tokens**\n'
                       '- **multimodal engineering**\n'
                       '- **controlled experiments**\n'
                       '- **failure analysis**\n'
                       '\n'
                       '{{figure:packed-training-loss}}\n'
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
                       'Implement the smallest training artifact that exposes the relevant tensor, batching, loss, '
                       'packing, or generation behavior; compare against a baseline.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **Packed Multi-Image Training with Placeholder Tokens** '
                       'with a controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Check label shifts, masking, padding, image-token placement, EOS handling, and gradient flow '
                       'before blaming the model.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **Packed Multi-Image Training with Placeholder '
                       'Tokens**, provide evidence from the practice artifact, identify one realistic failure, and '
                       'state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 65,
            'has_code_examples': True},
 'exercises': [{'title': 'Packed Multi-Image Training with Placeholder Tokens — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Implement and reason about packed '
                               'multi-image training with placeholder tokens while tracking data, optimization, '
                               'memory, and quality trade-offs.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['packed-multi-image-training-with-placeholder-tokens',
                                 'multimodal-engineering',
                                 'controlled-experiments']},
               {'title': 'Packed Multi-Image Training with Placeholder Tokens — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Packed Multi-Image Training with Placeholder Tokens — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Packed Multi-Image Training with Placeholder '
                                     'Tokens?',
                         'options': ['Implement and reason about packed multi-image training with placeholder tokens '
                                     'while tracking data, optimization, memory, and quality trade-offs.',
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
