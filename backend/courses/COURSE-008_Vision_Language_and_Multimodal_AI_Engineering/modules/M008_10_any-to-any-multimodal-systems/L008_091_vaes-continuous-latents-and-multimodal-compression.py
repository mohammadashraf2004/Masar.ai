"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-091'
MODULE_ID = 'M008-10'
LESSON_META = {'lesson_id': 'L008-091',
 'module_id': 'M008-10',
 'title': 'VAEs, Continuous Latents & Multimodal Compression',
 'learning_objective': 'Explain, implement where appropriate, and evaluate vaes, continuous latents & multimodal '
                       'compression within any-to-any multimodal systems.',
 'curriculum_role': 'CORE EXTENSION',
 'concepts': ['encoder',
              'latent space',
              'decoder',
              'compression',
              'reconstruction',
              'multimodal input',
              'multimodal output'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 10,
                      'chapter_title': 'Any-to-Any Models',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 55,
 'prerequisites': ['L008-090', 'M008-01', 'M008-03'],
 'visuals': [{'filename': 'multimodal-vae-comparison.png',
              'path': '../../assets/multimodal-vae-comparison.png',
              'caption': 'Image, video, and audio latent-compression examples.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'},
             {'filename': 'multimodal-vae.png',
              'path': '../../assets/multimodal-vae.png',
              'caption': 'VAE compression and reconstruction across image, audio, and action modalities.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'}],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'VAEs, Continuous Latents & Multimodal Compression',
 'slug': 'course-008-vaes-continuous-latents-and-multimodal-compression',
 'description': 'Explain, implement where appropriate, and evaluate vaes, continuous latents & multimodal compression '
                'within any-to-any multimodal systems.',
 'order': 6,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.92,
 'skill_tags': ['multimodal-ai', 'encoder', 'latent-space', 'decoder', 'compression'],
 'prerequisite_ids': [],
 'lesson': {'title': 'VAEs, Continuous Latents & Multimodal Compression',
            'content': '# VAEs, Continuous Latents & Multimodal Compression\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain, implement where appropriate, and evaluate vaes, continuous latents & multimodal '
                       'compression within any-to-any multimodal systems.\n'
                       '\n'
                       '## Curriculum role\n'
                       'CORE EXTENSION\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 10: Any-to-Any Models\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Any-to-Any Multimodal Systems**. It keeps prerequisite material '
                       'concise and focuses on the new multimodal engineering capability: connecting representation, '
                       'data, architecture, training, evaluation, or deployment decisions to observable system '
                       'behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **encoder**\n'
                       '- **latent space**\n'
                       '- **decoder**\n'
                       '- **compression**\n'
                       '- **reconstruction**\n'
                       '- **multimodal input**\n'
                       '- **multimodal output**\n'
                       '\n'
                       '## Visual assets\n'
                       '- **multimodal-vae-comparison.png** — Image, video, and audio latent-compression examples. '
                       '(package path: `../../assets/multimodal-vae-comparison.png`)\n'
                       '- **multimodal-vae.png** — VAE compression and reconstruction across image, audio, and action '
                       'modalities. (package path: `../../assets/multimodal-vae.png`)\n'
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
                       'Prototype the architecture with pretrained components or simplified modules, explicitly '
                       'marking the boundary between discrete tokens, continuous latents, connectors, and generators.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **VAEs, Continuous Latents & Multimodal Compression** '
                       'with a controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Check representation interfaces, modality triggers, connector dimensions, loss routing, and '
                       'staged-training boundaries.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **VAEs, Continuous Latents & Multimodal '
                       'Compression**, provide evidence from the practice artifact, identify one realistic failure, '
                       'and state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'VAEs, Continuous Latents & Multimodal Compression — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain, implement where appropriate, '
                               'and evaluate vaes, continuous latents & multimodal compression within any-to-any '
                               'multimodal systems.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['encoder', 'latent-space', 'decoder']},
               {'title': 'VAEs, Continuous Latents & Multimodal Compression — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'VAEs, Continuous Latents & Multimodal Compression — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of VAEs, Continuous Latents & Multimodal '
                                     'Compression?',
                         'options': ['Explain, implement where appropriate, and evaluate vaes, continuous latents & '
                                     'multimodal compression within any-to-any multimodal systems.',
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
