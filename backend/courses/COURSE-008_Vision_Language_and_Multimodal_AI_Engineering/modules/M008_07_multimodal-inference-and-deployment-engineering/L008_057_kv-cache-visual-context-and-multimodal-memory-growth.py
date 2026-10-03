"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-057'
MODULE_ID = 'M008-07'
LESSON_META = {'lesson_id': 'L008-057',
 'module_id': 'M008-07',
 'title': 'KV Cache, Visual Context & Multimodal Memory Growth',
 'learning_objective': 'Explain, implement where appropriate, and evaluate kv cache, visual context & multimodal '
                       'memory growth within multimodal inference & deployment engineering.',
 'curriculum_role': 'CORE ENGINEERING',
 'concepts': ['prefill', 'decode', 'keys and values', 'cache memory', 'autoregressive generation', 'latency', 'memory'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 7,
                      'chapter_title': 'Deploying Models for Inference at Scale',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 60,
 'prerequisites': ['L008-056', 'M008-01', 'M008-03'],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'KV Cache, Visual Context & Multimodal Memory Growth',
 'slug': 'course-008-kv-cache-visual-context-and-multimodal-memory-growth',
 'description': 'Explain, implement where appropriate, and evaluate kv cache, visual context & multimodal memory '
                'growth within multimodal inference & deployment engineering.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.0,
 'skill_tags': ['multimodal-ai', 'prefill', 'decode', 'keys-and-values', 'cache-memory'],
 'prerequisite_ids': [],
 'lesson': {'title': 'KV Cache, Visual Context & Multimodal Memory Growth',
            'content': '# KV Cache, Visual Context & Multimodal Memory Growth\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain, implement where appropriate, and evaluate kv cache, visual context & multimodal '
                       'memory growth within multimodal inference & deployment engineering.\n'
                       '\n'
                       '## Curriculum role\n'
                       'CORE ENGINEERING\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 7: Deploying Models for Inference at Scale\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Multimodal Inference & Deployment Engineering**. It keeps '
                       'prerequisite material concise and focuses on the new multimodal engineering capability: '
                       'connecting representation, data, architecture, training, evaluation, or deployment decisions '
                       'to observable system behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **prefill**\n'
                       '- **decode**\n'
                       '- **keys and values**\n'
                       '- **cache memory**\n'
                       '- **autoregressive generation**\n'
                       '- **latency**\n'
                       '- **memory**\n'
                       '\n'
                       '{{figure:visual-token-kv-growth}}\n'
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
                       '{{figure:kv-cache-prefill-decode}}\n'
                       '\n'
                       '## Practice\n'
                       'Profile a VLM inference path, change one optimization variable, and record TTFT, throughput, '
                       'VRAM, or another directly measured production metric.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **KV Cache, Visual Context & Multimodal Memory Growth** '
                       'with a controlled input set and at least one difficult example.\n'
                       '\n'
                       '{{figure:mha-gqa-mqa}}\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Warm up devices, synchronize measurements, separate prefill from decode, and distinguish '
                       'memory savings from real speedups.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **KV Cache, Visual Context & Multimodal Memory '
                       'Growth**, provide evidence from the practice artifact, identify one realistic failure, and '
                       'state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 60,
            'has_code_examples': True},
 'exercises': [{'title': 'KV Cache, Visual Context & Multimodal Memory Growth — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain, implement where appropriate, '
                               'and evaluate kv cache, visual context & multimodal memory growth within multimodal '
                               'inference & deployment engineering.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['prefill', 'decode', 'keys-and-values']},
               {'title': 'KV Cache, Visual Context & Multimodal Memory Growth — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'KV Cache, Visual Context & Multimodal Memory Growth — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of KV Cache, Visual Context & Multimodal Memory '
                                     'Growth?',
                         'options': ['Explain, implement where appropriate, and evaluate kv cache, visual context & '
                                     'multimodal memory growth within multimodal inference & deployment engineering.',
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
