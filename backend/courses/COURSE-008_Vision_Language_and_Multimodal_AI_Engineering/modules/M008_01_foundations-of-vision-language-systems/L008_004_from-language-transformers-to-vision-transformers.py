"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-004'
MODULE_ID = 'M008-01'
LESSON_META = {'lesson_id': 'L008-004',
 'module_id': 'M008-01',
 'title': 'From Language Transformers to Vision Transformers',
 'learning_objective': 'Explain the transition captured by “From Language Transformers to Vision Transformers” and '
                       'apply it to architecture or implementation decisions in modern multimodal systems.',
 'curriculum_role': 'REVISION + MULTIMODAL BRIDGE',
 'concepts': ['image patches', 'patch embeddings', 'positional embeddings', 'self-attention', 'vision backbone'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 1,
                      'chapter_title': 'Introduction to Vision and Language',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 45,
 'prerequisites': ['L008-003'],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'From Language Transformers to Vision Transformers',
 'slug': 'course-008-from-language-transformers-to-vision-transformers',
 'description': 'Explain the transition captured by “From Language Transformers to Vision Transformers” and apply it '
                'to architecture or implementation decisions in modern multimodal systems.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.75,
 'skill_tags': ['multimodal-ai', 'image-patches', 'patch-embeddings', 'positional-embeddings', 'self-attention'],
 'prerequisite_ids': [],
 'lesson': {'title': 'From Language Transformers to Vision Transformers',
            'content': '# From Language Transformers to Vision Transformers\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain the transition captured by “From Language Transformers to Vision Transformers” and '
                       'apply it to architecture or implementation decisions in modern multimodal systems.\n'
                       '\n'
                       '## Curriculum role\n'
                       'REVISION + MULTIMODAL BRIDGE\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 1: Introduction to Vision and Language\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Foundations of Vision-Language Systems**. It keeps prerequisite '
                       'material concise and focuses on the new multimodal engineering capability: connecting '
                       'representation, data, architecture, training, evaluation, or deployment decisions to '
                       'observable system behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **image patches**\n'
                       '- **patch embeddings**\n'
                       '- **positional embeddings**\n'
                       '- **self-attention**\n'
                       '- **vision backbone**\n'
                       '\n'
                       '{{figure:bert-pretraining-finetuning}}\n'
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
                       '{{figure:vision-transformer-vit}}\n'
                       '\n'
                       '## Practice\n'
                       'Inspect a small open VLM or reference implementation, trace image and text representations '
                       'through the model, and record tensor/token shapes at the key modality boundary.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **From Language Transformers to Vision Transformers** '
                       'with a controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Trace shape/token mismatches and distinguish prerequisite-model behavior from genuinely '
                       'multimodal behavior.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **From Language Transformers to Vision '
                       'Transformers**, provide evidence from the practice artifact, identify one realistic failure, '
                       'and state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'From Language Transformers to Vision Transformers — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain the transition captured by '
                               '“From Language Transformers to Vision Transformers” and apply it to architecture or '
                               'implementation decisions in modern multimodal systems.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['image-patches', 'patch-embeddings', 'positional-embeddings']},
               {'title': 'From Language Transformers to Vision Transformers — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'From Language Transformers to Vision Transformers — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of From Language Transformers to Vision '
                                     'Transformers?',
                         'options': ['Explain the transition captured by “From Language Transformers to Vision '
                                     'Transformers” and apply it to architecture or implementation decisions in modern '
                                     'multimodal systems.',
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
