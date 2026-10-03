"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-039'
MODULE_ID = 'M008-05'
LESSON_META = {'lesson_id': 'L008-039',
 'module_id': 'M008-05',
 'title': 'LoRA & DoRA for Vision-Language Models',
 'learning_objective': 'Explain, implement where appropriate, and evaluate lora & dora for vision-language models '
                       'within post-training & alignment for vision-language models.',
 'curriculum_role': 'PRACTICAL CORE',
 'concepts': ['PEFT',
              'low-rank matrices',
              'frozen backbone',
              'trainable adapters',
              'magnitude',
              'direction',
              'low-rank adaptation'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 5,
                      'chapter_title': 'Post-Training Vision Language Models',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 60,
 'prerequisites': ['L008-038', 'M008-01'],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'LoRA & DoRA for Vision-Language Models',
 'slug': 'course-008-lora-and-dora-for-vision-language-models',
 'description': 'Explain, implement where appropriate, and evaluate lora & dora for vision-language models within '
                'post-training & alignment for vision-language models.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.0,
 'skill_tags': ['multimodal-ai', 'peft', 'low-rank-matrices', 'frozen-backbone', 'trainable-adapters'],
 'prerequisite_ids': [],
 'lesson': {'title': 'LoRA & DoRA for Vision-Language Models',
            'content': '# LoRA & DoRA for Vision-Language Models\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain, implement where appropriate, and evaluate lora & dora for vision-language models '
                       'within post-training & alignment for vision-language models.\n'
                       '\n'
                       '## Curriculum role\n'
                       'PRACTICAL CORE\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 5: Post-Training Vision Language Models\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Post-Training & Alignment for Vision-Language Models**. It keeps '
                       'prerequisite material concise and focuses on the new multimodal engineering capability: '
                       'connecting representation, data, architecture, training, evaluation, or deployment decisions '
                       'to observable system behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **PEFT**\n'
                       '- **low-rank matrices**\n'
                       '- **frozen backbone**\n'
                       '- **trainable adapters**\n'
                       '- **magnitude**\n'
                       '- **direction**\n'
                       '- **low-rank adaptation**\n'
                       '\n'
                       '{{figure:lora-low-rank-adaptation}}\n'
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
                       '{{figure:dora-weight-decomposition}}\n'
                       '\n'
                       '## Practice\n'
                       'Adapt a small/open VLM with the target post-training method or a faithful miniature '
                       'experiment, then compare base and adapted behavior on a held-out set.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **LoRA & DoRA for Vision-Language Models** with a '
                       'controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Inspect data formatting, trainable-parameter selection, preference labels, reward signals, and '
                       'capability regression.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **LoRA & DoRA for Vision-Language Models**, '
                       'provide evidence from the practice artifact, identify one realistic failure, and state what '
                       'would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 60,
            'has_code_examples': True},
 'exercises': [{'title': 'LoRA & DoRA for Vision-Language Models — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain, implement where appropriate, '
                               'and evaluate lora & dora for vision-language models within post-training & alignment '
                               'for vision-language models.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['peft', 'low-rank-matrices', 'frozen-backbone']},
               {'title': 'LoRA & DoRA for Vision-Language Models — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'LoRA & DoRA for Vision-Language Models — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of LoRA & DoRA for Vision-Language Models?',
                         'options': ['Explain, implement where appropriate, and evaluate lora & dora for '
                                     'vision-language models within post-training & alignment for vision-language '
                                     'models.',
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
