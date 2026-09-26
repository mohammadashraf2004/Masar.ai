"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-077'
MODULE_ID = 'M008-09'
LESSON_META = {'lesson_id': 'L008-077',
 'module_id': 'M008-09',
 'title': 'From 3D CNNs to Temporal Factorization',
 'learning_objective': 'Explain the transition captured by “From 3D CNNs to Temporal Factorization” and apply it to '
                       'architecture or implementation decisions in modern multimodal systems.',
 'curriculum_role': 'FOUNDATIONS + REVISION',
 'concepts': ['frames', 'temporal modeling', 'frame sampling', 'video tokens', 'temporal context'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 9,
                      'chapter_title': 'Video-Language Models',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 55,
 'prerequisites': ['L008-076', 'M008-01', 'M008-03', 'COURSE-007 — Advanced RAG prerequisite concepts'],
 'visuals': [{'filename': 'factorized-3d-convolution.png',
              'path': '../../assets/factorized-3d-convolution.png',
              'caption': 'Factorizing 3D convolution into spatial and temporal stages.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'},
             {'filename': 'two-stream-video-cnn.png',
              'path': '../../assets/two-stream-video-cnn.png',
              'caption': 'Spatial RGB and temporal optical-flow streams for video understanding.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'}],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'From 3D CNNs to Temporal Factorization',
 'slug': 'course-008-from-3d-cnns-to-temporal-factorization',
 'description': 'Explain the transition captured by “From 3D CNNs to Temporal Factorization” and apply it to '
                'architecture or implementation decisions in modern multimodal systems.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.92,
 'skill_tags': ['multimodal-ai', 'frames', 'temporal-modeling', 'frame-sampling', 'video-tokens'],
 'prerequisite_ids': [],
 'lesson': {'title': 'From 3D CNNs to Temporal Factorization',
            'content': '# From 3D CNNs to Temporal Factorization\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain the transition captured by “From 3D CNNs to Temporal Factorization” and apply it to '
                       'architecture or implementation decisions in modern multimodal systems.\n'
                       '\n'
                       '## Curriculum role\n'
                       'FOUNDATIONS + REVISION\n'
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
                       '## Visual assets\n'
                       '- **factorized-3d-convolution.png** — Factorizing 3D convolution into spatial and temporal '
                       'stages. (package path: `../../assets/factorized-3d-convolution.png`)\n'
                       '- **two-stream-video-cnn.png** — Spatial RGB and temporal optical-flow streams for video '
                       'understanding. (package path: `../../assets/two-stream-video-cnn.png`)\n'
                       '\n'
                       '> These are user-provided reference assets. Verify reuse rights before public publication; '
                       'replace with an original Masar redraw where needed.\n'
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
                       '**Lesson-specific goal:** demonstrate **From 3D CNNs to Temporal Factorization** with a '
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
                       'Explain the principal engineering trade-off in **From 3D CNNs to Temporal Factorization**, '
                       'provide evidence from the practice artifact, identify one realistic failure, and state what '
                       'would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'From 3D CNNs to Temporal Factorization — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain the transition captured by '
                               '“From 3D CNNs to Temporal Factorization” and apply it to architecture or '
                               'implementation decisions in modern multimodal systems.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['frames', 'temporal-modeling', 'frame-sampling']},
               {'title': 'From 3D CNNs to Temporal Factorization — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'From 3D CNNs to Temporal Factorization — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of From 3D CNNs to Temporal Factorization?',
                         'options': ['Explain the transition captured by “From 3D CNNs to Temporal Factorization” and '
                                     'apply it to architecture or implementation decisions in modern multimodal '
                                     'systems.',
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
