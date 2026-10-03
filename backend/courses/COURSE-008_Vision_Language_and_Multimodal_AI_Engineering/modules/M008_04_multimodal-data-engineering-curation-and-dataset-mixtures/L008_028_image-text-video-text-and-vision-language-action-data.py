"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-028'
MODULE_ID = 'M008-04'
LESSON_META = {'lesson_id': 'L008-028',
 'module_id': 'M008-04',
 'title': 'Image-Text, Video-Text & Vision-Language-Action Data',
 'learning_objective': 'Explain, implement where appropriate, and evaluate image-text, video-text & '
                       'vision-language-action data within multimodal data engineering, curation & dataset mixtures.',
 'curriculum_role': 'CORE',
 'concepts': ['frames',
              'temporal modeling',
              'frame sampling',
              'video tokens',
              'temporal context',
              'observation',
              'policy'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 4,
                      'chapter_title': 'Training Data and Preprocessing for VLMs',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 55,
 'prerequisites': ['L008-027', 'M008-01'],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Image-Text, Video-Text & Vision-Language-Action Data',
 'slug': 'course-008-image-text-video-text-and-vision-language-action-data',
 'description': 'Explain, implement where appropriate, and evaluate image-text, video-text & vision-language-action '
                'data within multimodal data engineering, curation & dataset mixtures.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.92,
 'skill_tags': ['multimodal-ai', 'frames', 'temporal-modeling', 'frame-sampling', 'video-tokens'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Image-Text, Video-Text & Vision-Language-Action Data',
            'content': '# Image-Text, Video-Text & Vision-Language-Action Data\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain, implement where appropriate, and evaluate image-text, video-text & '
                       'vision-language-action data within multimodal data engineering, curation & dataset mixtures.\n'
                       '\n'
                       '## Curriculum role\n'
                       'CORE\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 4: Training Data and Preprocessing for VLMs\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Multimodal Data Engineering, Curation & Dataset Mixtures**. It keeps '
                       'prerequisite material concise and focuses on the new multimodal engineering capability: '
                       'connecting representation, data, architecture, training, evaluation, or deployment decisions '
                       'to observable system behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **frames**\n'
                       '- **temporal modeling**\n'
                       '- **frame sampling**\n'
                       '- **video tokens**\n'
                       '- **temporal context**\n'
                       '- **observation**\n'
                       '- **policy**\n'
                       '\n'
                       '{{figure:vla-dataset-comparison}}\n'
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
                       'Build or transform a small multimodal dataset slice, measure quality/diversity/utilization, '
                       'and document the cost or quality effect of one pipeline decision.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **Image-Text, Video-Text & Vision-Language-Action Data** '
                       'with a controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Audit corruption, filtering bias, annotation hallucinations, distribution imbalance, and '
                       'packaging bottlenecks.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **Image-Text, Video-Text & '
                       'Vision-Language-Action Data**, provide evidence from the practice artifact, identify one '
                       'realistic failure, and state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Image-Text, Video-Text & Vision-Language-Action Data — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain, implement where appropriate, '
                               'and evaluate image-text, video-text & vision-language-action data within multimodal '
                               'data engineering, curation & dataset mixtures.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['frames', 'temporal-modeling', 'frame-sampling']},
               {'title': 'Image-Text, Video-Text & Vision-Language-Action Data — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Image-Text, Video-Text & Vision-Language-Action Data — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Image-Text, Video-Text & Vision-Language-Action '
                                     'Data?',
                         'options': ['Explain, implement where appropriate, and evaluate image-text, video-text & '
                                     'vision-language-action data within multimodal data engineering, curation & '
                                     'dataset mixtures.',
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
