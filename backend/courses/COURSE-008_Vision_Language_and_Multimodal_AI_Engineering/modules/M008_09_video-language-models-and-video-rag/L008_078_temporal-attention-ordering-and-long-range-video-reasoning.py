"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-078'
MODULE_ID = 'M008-09'
LESSON_META = {'lesson_id': 'L008-078',
 'module_id': 'M008-09',
 'title': 'Temporal Attention, Ordering & Long-Range Video Reasoning',
 'learning_objective': 'Explain and compare temporal attention, ordering & long-range video reasoning and connect '
                       'architectural choices to compute, memory, quality, and implementation complexity.',
 'curriculum_role': 'CORE ARCHITECTURE',
 'concepts': ['frames', 'temporal modeling', 'frame sampling', 'video tokens', 'temporal context'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 9,
                      'chapter_title': 'Video-Language Models',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 60,
 'prerequisites': ['L008-077', 'M008-01', 'M008-03', 'COURSE-007 — Advanced RAG prerequisite concepts'],
 'visuals': [],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Temporal Attention, Ordering & Long-Range Video Reasoning',
 'slug': 'course-008-temporal-attention-ordering-and-long-range-video-reasoning',
 'description': 'Explain and compare temporal attention, ordering & long-range video reasoning and connect '
                'architectural choices to compute, memory, quality, and implementation complexity.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.0,
 'skill_tags': ['multimodal-ai', 'frames', 'temporal-modeling', 'frame-sampling', 'video-tokens'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Temporal Attention, Ordering & Long-Range Video Reasoning',
            'content': '# Temporal Attention, Ordering & Long-Range Video Reasoning\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain and compare temporal attention, ordering & long-range video reasoning and connect '
                       'architectural choices to compute, memory, quality, and implementation complexity.\n'
                       '\n'
                       '## Curriculum role\n'
                       'CORE ARCHITECTURE\n'
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
                       '- **frames**\n'
                       '- **temporal modeling**\n'
                       '- **frame sampling**\n'
                       '- **video tokens**\n'
                       '- **temporal context**\n'
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
                       '**Lesson-specific goal:** demonstrate **Temporal Attention, Ordering & Long-Range Video '
                       'Reasoning** with a controlled input set and at least one difficult example.\n'
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
                       'Explain the principal engineering trade-off in **Temporal Attention, Ordering & Long-Range '
                       'Video Reasoning**, provide evidence from the practice artifact, identify one realistic '
                       'failure, and state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 60,
            'has_code_examples': True},
 'exercises': [{'title': 'Temporal Attention, Ordering & Long-Range Video Reasoning — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain and compare temporal '
                               'attention, ordering & long-range video reasoning and connect architectural choices to '
                               'compute, memory, quality, and implementation complexity.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['frames', 'temporal-modeling', 'frame-sampling']},
               {'title': 'Temporal Attention, Ordering & Long-Range Video Reasoning — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Temporal Attention, Ordering & Long-Range Video Reasoning — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Temporal Attention, Ordering & Long-Range Video '
                                     'Reasoning?',
                         'options': ['Explain and compare temporal attention, ordering & long-range video reasoning '
                                     'and connect architectural choices to compute, memory, quality, and '
                                     'implementation complexity.',
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
