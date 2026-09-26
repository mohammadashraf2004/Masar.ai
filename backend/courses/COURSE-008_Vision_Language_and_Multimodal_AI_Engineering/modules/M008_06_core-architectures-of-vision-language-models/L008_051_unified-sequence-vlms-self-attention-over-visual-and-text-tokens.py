"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-051'
MODULE_ID = 'M008-06'
LESSON_META = {'lesson_id': 'L008-051',
 'module_id': 'M008-06',
 'title': 'Unified-Sequence VLMs: Self-Attention over Visual and Text Tokens',
 'learning_objective': 'Explain and compare unified-sequence vlms: self-attention over visual and text tokens and '
                       'connect architectural choices to compute, memory, quality, and implementation complexity.',
 'curriculum_role': 'ARCHITECTURE CORE',
 'concepts': ['queries', 'keys', 'values', 'unified sequence', 'token interaction'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 6,
                      'chapter_title': 'Core Architectures of Vision Language Models',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 60,
 'prerequisites': ['L008-050', 'M008-01', 'M008-03'],
 'visuals': [{'filename': 'smolvlm-unified-sequence.png',
              'path': '../../assets/smolvlm-unified-sequence.png',
              'caption': 'Unified-sequence vision-language architecture using projected visual tokens.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'}],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Unified-Sequence VLMs: Self-Attention over Visual and Text Tokens',
 'slug': 'course-008-unified-sequence-vlms-self-attention-over-visual-and-text-tokens',
 'description': 'Explain and compare unified-sequence vlms: self-attention over visual and text tokens and connect '
                'architectural choices to compute, memory, quality, and implementation complexity.',
 'order': 5,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 1.0,
 'skill_tags': ['multimodal-ai', 'queries', 'keys', 'values', 'unified-sequence'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Unified-Sequence VLMs: Self-Attention over Visual and Text Tokens',
            'content': '# Unified-Sequence VLMs: Self-Attention over Visual and Text Tokens\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain and compare unified-sequence vlms: self-attention over visual and text tokens and '
                       'connect architectural choices to compute, memory, quality, and implementation complexity.\n'
                       '\n'
                       '## Curriculum role\n'
                       'ARCHITECTURE CORE\n'
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
                       '- **queries**\n'
                       '- **keys**\n'
                       '- **values**\n'
                       '- **unified sequence**\n'
                       '- **token interaction**\n'
                       '\n'
                       '## Visual assets\n'
                       '- **smolvlm-unified-sequence.png** — Unified-sequence vision-language architecture using '
                       'projected visual tokens. (package path: `../../assets/smolvlm-unified-sequence.png`)\n'
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
                       '**Lesson-specific goal:** demonstrate **Unified-Sequence VLMs: Self-Attention over Visual and '
                       'Text Tokens** with a controlled input set and at least one difficult example.\n'
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
                       'Explain the principal engineering trade-off in **Unified-Sequence VLMs: Self-Attention over '
                       'Visual and Text Tokens**, provide evidence from the practice artifact, identify one realistic '
                       'failure, and state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 60,
            'has_code_examples': True},
 'exercises': [{'title': 'Unified-Sequence VLMs: Self-Attention over Visual and Text Tokens — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain and compare unified-sequence '
                               'vlms: self-attention over visual and text tokens and connect architectural choices to '
                               'compute, memory, quality, and implementation complexity.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['queries', 'keys', 'values']},
               {'title': 'Unified-Sequence VLMs: Self-Attention over Visual and Text Tokens — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Unified-Sequence VLMs: Self-Attention over Visual and Text Tokens — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Unified-Sequence VLMs: Self-Attention over '
                                     'Visual and Text Tokens?',
                         'options': ['Explain and compare unified-sequence vlms: self-attention over visual and text '
                                     'tokens and connect architectural choices to compute, memory, quality, and '
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
