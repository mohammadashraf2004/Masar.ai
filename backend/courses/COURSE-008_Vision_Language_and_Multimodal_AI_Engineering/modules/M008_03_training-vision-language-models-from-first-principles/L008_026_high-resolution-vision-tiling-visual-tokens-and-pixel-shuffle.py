"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-026'
MODULE_ID = 'M008-03'
LESSON_META = {'lesson_id': 'L008-026',
 'module_id': 'M008-03',
 'title': 'High-Resolution Vision: Tiling, Visual Tokens & Pixel Shuffle',
 'learning_objective': 'Explain and compare high-resolution vision: tiling, visual tokens & pixel shuffle and connect '
                       'architectural choices to compute, memory, quality, and implementation complexity.',
 'curriculum_role': 'CORE EXTENSION',
 'concepts': ['High-Resolution Vision', 'Tiling', 'Visual Tokens', 'Pixel Shuffle'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 3,
                      'chapter_title': 'Vision Language Model Training',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 65,
 'prerequisites': ['L008-025', 'M008-01'],
 'visuals': [],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'High-Resolution Vision: Tiling, Visual Tokens & Pixel Shuffle',
 'slug': 'course-008-high-resolution-vision-tiling-visual-tokens-and-pixel-shuffle',
 'description': 'Explain and compare high-resolution vision: tiling, visual tokens & pixel shuffle and connect '
                'architectural choices to compute, memory, quality, and implementation complexity.',
 'order': 10,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.08,
 'skill_tags': ['multimodal-ai', 'high-resolution-vision', 'tiling', 'visual-tokens', 'pixel-shuffle'],
 'prerequisite_ids': [],
 'lesson': {'title': 'High-Resolution Vision: Tiling, Visual Tokens & Pixel Shuffle',
            'content': '# High-Resolution Vision: Tiling, Visual Tokens & Pixel Shuffle\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain and compare high-resolution vision: tiling, visual tokens & pixel shuffle and connect '
                       'architectural choices to compute, memory, quality, and implementation complexity.\n'
                       '\n'
                       '## Curriculum role\n'
                       'CORE EXTENSION\n'
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
                       '- **High-Resolution Vision**\n'
                       '- **Tiling**\n'
                       '- **Visual Tokens**\n'
                       '- **Pixel Shuffle**\n'
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
                       '**Lesson-specific goal:** demonstrate **High-Resolution Vision: Tiling, Visual Tokens & Pixel '
                       'Shuffle** with a controlled input set and at least one difficult example.\n'
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
                       'Explain the principal engineering trade-off in **High-Resolution Vision: Tiling, Visual Tokens '
                       '& Pixel Shuffle**, provide evidence from the practice artifact, identify one realistic '
                       'failure, and state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 65,
            'has_code_examples': True},
 'exercises': [{'title': 'High-Resolution Vision: Tiling, Visual Tokens & Pixel Shuffle — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain and compare high-resolution '
                               'vision: tiling, visual tokens & pixel shuffle and connect architectural choices to '
                               'compute, memory, quality, and implementation complexity.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['high-resolution-vision', 'tiling', 'visual-tokens']},
               {'title': 'High-Resolution Vision: Tiling, Visual Tokens & Pixel Shuffle — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'High-Resolution Vision: Tiling, Visual Tokens & Pixel Shuffle — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of High-Resolution Vision: Tiling, Visual Tokens & '
                                     'Pixel Shuffle?',
                         'options': ['Explain and compare high-resolution vision: tiling, visual tokens & pixel '
                                     'shuffle and connect architectural choices to compute, memory, quality, and '
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
 'project': {'title': 'Train and Debug a Small Vision-Language Model',
             'description': 'Train and debug a small VLM, including multimodal loss masking, batching/packing, '
                            'generation, and an inference optimization experiment.',
             'difficulty': DifficultyLevel.intermediate,
             'tech_stack': ['Python', 'PyTorch', 'Transformers'],
             'objectives': ['Integrate the core capabilities from Training Vision-Language Models from First '
                            'Principles',
                            'Build a reproducible artifact rather than a one-off demo',
                            'Measure quality and at least one engineering constraint',
                            'Diagnose at least one realistic multimodal failure',
                            'Document architecture decisions, limitations, and acceptance criteria'],
             'rubric': {'implementation': 30,
                        'evaluation': 25,
                        'debugging': 20,
                        'architecture_tradeoffs': 15,
                        'reproducibility': 10},
             'starter_repo_url': None,
             'estimated_hours': 6.0}}
