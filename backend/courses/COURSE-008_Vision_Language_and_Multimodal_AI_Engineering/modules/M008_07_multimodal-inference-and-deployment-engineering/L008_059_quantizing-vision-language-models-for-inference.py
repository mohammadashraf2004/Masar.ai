"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-059'
MODULE_ID = 'M008-07'
LESSON_META = {'lesson_id': 'L008-059',
 'module_id': 'M008-07',
 'title': 'Quantizing Vision-Language Models for Inference',
 'learning_objective': 'Explain, implement where appropriate, and evaluate quantizing vision-language models for '
                       'inference within multimodal inference & deployment engineering.',
 'curriculum_role': 'CORE + VLM EXTENSION',
 'concepts': ['low precision', 'INT8', 'INT4', 'NF4', 'memory efficiency', 'latency', 'memory'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 7,
                      'chapter_title': 'Deploying Models for Inference at Scale',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 65,
 'prerequisites': ['L008-058', 'M008-01', 'M008-03'],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Quantizing Vision-Language Models for Inference',
 'slug': 'course-008-quantizing-vision-language-models-for-inference',
 'description': 'Explain, implement where appropriate, and evaluate quantizing vision-language models for inference '
                'within multimodal inference & deployment engineering.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.08,
 'skill_tags': ['multimodal-ai', 'low-precision', 'int8', 'int4', 'nf4'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Quantizing Vision-Language Models for Inference',
            'content': '# Quantizing Vision-Language Models for Inference\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain, implement where appropriate, and evaluate quantizing vision-language models for '
                       'inference within multimodal inference & deployment engineering.\n'
                       '\n'
                       '## Curriculum role\n'
                       'CORE + VLM EXTENSION\n'
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
                       '- **low precision**\n'
                       '- **INT8**\n'
                       '- **INT4**\n'
                       '- **NF4**\n'
                       '- **memory efficiency**\n'
                       '- **latency**\n'
                       '- **memory**\n'
                       '\n'
                       '{{figure:linear-quantization-scaling}}\n'
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
                       'Profile a VLM inference path, change one optimization variable, and record TTFT, throughput, '
                       'VRAM, or another directly measured production metric.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **Quantizing Vision-Language Models for Inference** with '
                       'a controlled input set and at least one difficult example.\n'
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
                       'Explain the principal engineering trade-off in **Quantizing Vision-Language Models for '
                       'Inference**, provide evidence from the practice artifact, identify one realistic failure, and '
                       'state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 65,
            'has_code_examples': True},
 'exercises': [{'title': 'Quantizing Vision-Language Models for Inference — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain, implement where appropriate, '
                               'and evaluate quantizing vision-language models for inference within multimodal '
                               'inference & deployment engineering.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['low-precision', 'int8', 'int4']},
               {'title': 'Quantizing Vision-Language Models for Inference — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Quantizing Vision-Language Models for Inference — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Quantizing Vision-Language Models for '
                                     'Inference?',
                         'options': ['Explain, implement where appropriate, and evaluate quantizing vision-language '
                                     'models for inference within multimodal inference & deployment engineering.',
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
