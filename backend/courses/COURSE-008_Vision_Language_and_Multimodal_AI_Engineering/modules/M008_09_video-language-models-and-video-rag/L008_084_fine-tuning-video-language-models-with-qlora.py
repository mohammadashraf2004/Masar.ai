"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-084'
MODULE_ID = 'M008-09'
LESSON_META = {'lesson_id': 'L008-084',
 'module_id': 'M008-09',
 'title': 'Fine-Tuning Video-Language Models with QLoRA',
 'learning_objective': 'Implement and reason about fine-tuning video-language models with qlora while tracking data, '
                       'optimization, memory, and quality trade-offs.',
 'curriculum_role': 'ADVANCED PRACTICAL',
 'concepts': ['PEFT',
              'low-rank matrices',
              'frozen backbone',
              'trainable adapters',
              'frames',
              'temporal modeling',
              'frame sampling'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 9,
                      'chapter_title': 'Video-Language Models',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 70,
 'prerequisites': ['L008-083', 'M008-01', 'M008-03', 'COURSE-007 — Advanced RAG prerequisite concepts'],
 'visuals': [],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Fine-Tuning Video-Language Models with QLoRA',
 'slug': 'course-008-fine-tuning-video-language-models-with-qlora',
 'description': 'Implement and reason about fine-tuning video-language models with qlora while tracking data, '
                'optimization, memory, and quality trade-offs.',
 'order': 9,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.17,
 'skill_tags': ['multimodal-ai', 'peft', 'low-rank-matrices', 'frozen-backbone', 'trainable-adapters'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Fine-Tuning Video-Language Models with QLoRA',
            'content': '# Fine-Tuning Video-Language Models with QLoRA\n'
                       '\n'
                       '## Learning objective\n'
                       'Implement and reason about fine-tuning video-language models with qlora while tracking data, '
                       'optimization, memory, and quality trade-offs.\n'
                       '\n'
                       '## Curriculum role\n'
                       'ADVANCED PRACTICAL\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 9: Video-Language Models\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Video-Language Models & Video-RAG**. It keeps prerequisite material '
                       'concise and focuses on the new multimodal engineering capability: connecting representation, '
                       'data, architecture, training, evaluation, or deployment decisions to observable system '
                       'behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **PEFT**\n'
                       '- **low-rank matrices**\n'
                       '- **frozen backbone**\n'
                       '- **trainable adapters**\n'
                       '- **frames**\n'
                       '- **temporal modeling**\n'
                       '- **frame sampling**\n'
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
                       'Process a short video corpus or clip set, vary frame/segment strategy, and evaluate temporal '
                       'retrieval or generation quality alongside token/latency cost.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **Fine-Tuning Video-Language Models with QLoRA** with a '
                       'controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Check timestamps, segment boundaries, frame sampling, retrieval relevance, and temporal '
                       'evidence before interpreting answers.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **Fine-Tuning Video-Language Models with '
                       'QLoRA**, provide evidence from the practice artifact, identify one realistic failure, and '
                       'state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 70,
            'has_code_examples': True},
 'exercises': [{'title': 'Fine-Tuning Video-Language Models with QLoRA — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Implement and reason about '
                               'fine-tuning video-language models with qlora while tracking data, optimization, '
                               'memory, and quality trade-offs.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['peft', 'low-rank-matrices', 'frozen-backbone']},
               {'title': 'Fine-Tuning Video-Language Models with QLoRA — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Fine-Tuning Video-Language Models with QLoRA — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Fine-Tuning Video-Language Models with QLoRA?',
                         'options': ['Implement and reason about fine-tuning video-language models with qlora while '
                                     'tracking data, optimization, memory, and quality trade-offs.',
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
