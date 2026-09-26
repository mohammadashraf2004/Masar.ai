"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-055'
MODULE_ID = 'M008-06'
LESSON_META = {'lesson_id': 'L008-055',
 'module_id': 'M008-06',
 'title': 'Choosing and Reviewing a VLM Architecture',
 'learning_objective': 'Use explicit constraints and measurable evidence to make engineering decisions for choosing '
                       'and reviewing a vlm architecture.',
 'curriculum_role': 'SYSTEM DESIGN',
 'concepts': ['Choosing and Reviewing a VLM Architecture',
              'multimodal engineering',
              'controlled experiments',
              'failure analysis'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 6,
                      'chapter_title': 'Core Architectures of Vision Language Models',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 55,
 'prerequisites': ['L008-054', 'M008-01', 'M008-03'],
 'visuals': [{'filename': 'vlm-architecture-comparison.png',
              'path': '../../assets/vlm-architecture-comparison.png',
              'caption': 'Show-and-Tell, Flamingo, and unified-sequence VLM architecture comparison.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'}],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Choosing and Reviewing a VLM Architecture',
 'slug': 'course-008-choosing-and-reviewing-a-vlm-architecture',
 'description': 'Use explicit constraints and measurable evidence to make engineering decisions for choosing and '
                'reviewing a vlm architecture.',
 'order': 9,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.92,
 'skill_tags': ['multimodal-ai',
                'choosing-and-reviewing-a-vlm-architecture',
                'multimodal-engineering',
                'controlled-experiments',
                'failure-analysis'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Choosing and Reviewing a VLM Architecture',
            'content': '# Choosing and Reviewing a VLM Architecture\n'
                       '\n'
                       '## Learning objective\n'
                       'Use explicit constraints and measurable evidence to make engineering decisions for choosing '
                       'and reviewing a vlm architecture.\n'
                       '\n'
                       '## Curriculum role\n'
                       'SYSTEM DESIGN\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 6: Core Architectures of Vision Language Models\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Core Architectures of Vision-Language Models**. It keeps prerequisite '
                       'material concise and focuses on the new multimodal engineering capability: connecting '
                       'representation, data, architecture, training, evaluation, or deployment decisions to '
                       'observable system behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **Choosing and Reviewing a VLM Architecture**\n'
                       '- **multimodal engineering**\n'
                       '- **controlled experiments**\n'
                       '- **failure analysis**\n'
                       '\n'
                       '## Visual assets\n'
                       '- **vlm-architecture-comparison.png** — Show-and-Tell, Flamingo, and unified-sequence VLM '
                       'architecture comparison. (package path: `../../assets/vlm-architecture-comparison.png`)\n'
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
                       'Implement or diagram the architecture boundary precisely, measure parameter/token differences '
                       'where possible, and compare two fusion or compression choices under controlled conditions.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **Choosing and Reviewing a VLM Architecture** with a '
                       'controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Control token budgets and trainable parameters before attributing differences to the fusion '
                       'architecture.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **Choosing and Reviewing a VLM Architecture**, '
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
 'exercises': [{'title': 'Choosing and Reviewing a VLM Architecture — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Use explicit constraints and '
                               'measurable evidence to make engineering decisions for choosing and reviewing a vlm '
                               'architecture.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['choosing-and-reviewing-a-vlm-architecture',
                                 'multimodal-engineering',
                                 'controlled-experiments']},
               {'title': 'Choosing and Reviewing a VLM Architecture — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Choosing and Reviewing a VLM Architecture — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Choosing and Reviewing a VLM Architecture?',
                         'options': ['Use explicit constraints and measurable evidence to make engineering decisions '
                                     'for choosing and reviewing a vlm architecture.',
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
 'project': {'title': 'Build & Compare Two VLM Architectures',
             'description': 'Implement and compare unified-sequence and cross-attention VLM designs under matched '
                            'data, token budget, and optimization settings.',
             'difficulty': DifficultyLevel.intermediate,
             'tech_stack': ['Python', 'PyTorch', 'Transformers'],
             'objectives': ['Integrate the core capabilities from Core Architectures of Vision-Language Models',
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
             'estimated_hours': 5.0}}
