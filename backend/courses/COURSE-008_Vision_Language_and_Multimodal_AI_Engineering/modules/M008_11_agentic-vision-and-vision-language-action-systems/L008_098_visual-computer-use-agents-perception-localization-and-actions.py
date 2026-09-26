"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-098'
MODULE_ID = 'M008-11'
LESSON_META = {'lesson_id': 'L008-098',
 'module_id': 'M008-11',
 'title': 'Visual Computer-Use Agents: Perception, Localization & Actions',
 'learning_objective': 'Explain, implement where appropriate, and evaluate visual computer-use agents: perception, '
                       'localization & actions within agentic vision & vision-language-action systems.',
 'curriculum_role': 'CORE',
 'concepts': ['observation', 'policy', 'action space', 'verification', 'control loop', 'observe-act loop', 'tools'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 11,
                      'chapter_title': 'Advanced Topics and Cutting-Edge Research',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 60,
 'prerequisites': ['L008-097', 'M008-01', 'M008-03', 'COURSE-007 — Agent/tool prerequisite concepts'],
 'visuals': [],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Visual Computer-Use Agents: Perception, Localization & Actions',
 'slug': 'course-008-visual-computer-use-agents-perception-localization-and-actions',
 'description': 'Explain, implement where appropriate, and evaluate visual computer-use agents: perception, '
                'localization & actions within agentic vision & vision-language-action systems.',
 'order': 2,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.0,
 'skill_tags': ['multimodal-ai', 'observation', 'policy', 'action-space', 'verification'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Visual Computer-Use Agents: Perception, Localization & Actions',
            'content': '# Visual Computer-Use Agents: Perception, Localization & Actions\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain, implement where appropriate, and evaluate visual computer-use agents: perception, '
                       'localization & actions within agentic vision & vision-language-action systems.\n'
                       '\n'
                       '## Curriculum role\n'
                       'CORE\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 11: Advanced Topics and Cutting-Edge Research\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Agentic Vision & Vision-Language-Action Systems**. It keeps '
                       'prerequisite material concise and focuses on the new multimodal engineering capability: '
                       'connecting representation, data, architecture, training, evaluation, or deployment decisions '
                       'to observable system behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **observation**\n'
                       '- **policy**\n'
                       '- **action space**\n'
                       '- **verification**\n'
                       '- **control loop**\n'
                       '- **observe-act loop**\n'
                       '- **tools**\n'
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
                       'Use a sandboxed GUI, simulator, or offline trace to build an observe-decide-act experiment '
                       'with bounded actions, explicit verification, and failure recovery.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **Visual Computer-Use Agents: Perception, Localization & '
                       'Actions** with a controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Validate action schemas and end states, bound permissions/actions, and separate localization '
                       'failure from planning or execution failure.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **Visual Computer-Use Agents: Perception, '
                       'Localization & Actions**, provide evidence from the practice artifact, identify one realistic '
                       'failure, and state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 60,
            'has_code_examples': True},
 'exercises': [{'title': 'Visual Computer-Use Agents: Perception, Localization & Actions — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain, implement where appropriate, '
                               'and evaluate visual computer-use agents: perception, localization & actions within '
                               'agentic vision & vision-language-action systems.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['observation', 'policy', 'action-space']},
               {'title': 'Visual Computer-Use Agents: Perception, Localization & Actions — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Visual Computer-Use Agents: Perception, Localization & Actions — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Visual Computer-Use Agents: Perception, '
                                     'Localization & Actions?',
                         'options': ['Explain, implement where appropriate, and evaluate visual computer-use agents: '
                                     'perception, localization & actions within agentic vision & '
                                     'vision-language-action systems.',
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
