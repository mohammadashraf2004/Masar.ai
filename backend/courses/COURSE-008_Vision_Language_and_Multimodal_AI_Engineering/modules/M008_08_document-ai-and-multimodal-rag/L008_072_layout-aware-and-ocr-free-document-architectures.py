"""Masar COURSE-008 lesson seed.

Generated from the finalized COURSE-008 curriculum design based on BOOK-008.
The file uses only fields demonstrated by the supplied Masar Topic/Lesson/Exercise/Quiz/Project seed schema.
Repository integration and end-to-end lesson execution must still be validated in the target application.
"""
from app.models.learning import DifficultyLevel

LESSON_ID = 'L008-072'
MODULE_ID = 'M008-08'
LESSON_META = {'lesson_id': 'L008-072',
 'module_id': 'M008-08',
 'title': 'Layout-Aware & OCR-Free Document Architectures',
 'learning_objective': 'Explain and compare layout-aware & ocr-free document architectures and connect architectural '
                       'choices to compute, memory, quality, and implementation complexity.',
 'curriculum_role': 'ARCHITECTURE CORE',
 'concepts': ['OCR', 'layout', 'document VQA', 'tables', 'page images'],
 'source_reference': {'source_id': 'BOOK-008',
                      'book_title': 'Vision Language Models',
                      'edition': 'SOURCE INFORMATION MISSING',
                      'chapter': 8,
                      'chapter_title': 'Document AI',
                      'pages': 'SOURCE INFORMATION MISSING'},
 'estimated_minutes': 55,
 'prerequisites': ['L008-071', 'M008-01', 'M008-03', 'COURSE-007 — Advanced RAG prerequisite concepts'],
 'visuals': [{'filename': 'funsd-form-fields.png',
              'path': '../../assets/funsd-form-fields.png',
              'caption': 'Form-field annotations for layout-aware document understanding.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'},
             {'filename': 'layoutlmv3-architecture.png',
              'path': '../../assets/layoutlmv3-architecture.png',
              'caption': 'LayoutLMv3 text, 1D/2D position, and image-patch representations.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'},
             {'filename': 'donut-document-model.png',
              'path': '../../assets/donut-document-model.png',
              'caption': 'OCR-free Donut encoder-decoder producing task-specific structured sequences.',
              'publication_note': 'Verify publication/reuse rights before public distribution; redraw as an original '
                                  'Masar figure if required.'}],
 'modernization': ['Revalidate model IDs, package APIs, training/serving interfaces, and hardware-specific examples '
                   'before production implementation.'],
 'status': 'Curriculum finalized / lesson seed export'}

TOPIC = {'title': 'Layout-Aware & OCR-Free Document Architectures',
 'slug': 'course-008-layout-aware-and-ocr-free-document-architectures',
 'description': 'Explain and compare layout-aware & ocr-free document architectures and connect architectural choices '
                'to compute, memory, quality, and implementation complexity.',
 'order': 7,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 0.92,
 'skill_tags': ['multimodal-ai', 'ocr', 'layout', 'document-vqa', 'tables'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Layout-Aware & OCR-Free Document Architectures',
            'content': '# Layout-Aware & OCR-Free Document Architectures\n'
                       '\n'
                       '## Learning objective\n'
                       'Explain and compare layout-aware & ocr-free document architectures and connect architectural '
                       'choices to compute, memory, quality, and implementation complexity.\n'
                       '\n'
                       '## Curriculum role\n'
                       'ARCHITECTURE CORE\n'
                       '\n'
                       '## Source mapping\n'
                       '- Source: BOOK-008 — Vision Language Models\n'
                       '- Chapter 8: Document AI\n'
                       '- Edition/pages: SOURCE INFORMATION MISSING / SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Why this matters\n'
                       'This lesson is part of **Document AI & Multimodal RAG**. It keeps prerequisite material '
                       'concise and focuses on the new multimodal engineering capability: connecting representation, '
                       'data, architecture, training, evaluation, or deployment decisions to observable system '
                       'behavior.\n'
                       '\n'
                       '## Concepts\n'
                       '- **OCR**\n'
                       '- **layout**\n'
                       '- **document VQA**\n'
                       '- **tables**\n'
                       '- **page images**\n'
                       '\n'
                       '## Visual assets\n'
                       '- **funsd-form-fields.png** — Form-field annotations for layout-aware document understanding. '
                       '(package path: `../../assets/funsd-form-fields.png`)\n'
                       '- **layoutlmv3-architecture.png** — LayoutLMv3 text, 1D/2D position, and image-patch '
                       'representations. (package path: `../../assets/layoutlmv3-architecture.png`)\n'
                       '- **donut-document-model.png** — OCR-free Donut encoder-decoder producing task-specific '
                       'structured sequences. (package path: `../../assets/donut-document-model.png`)\n'
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
                       'Build a document-processing or visual-retrieval experiment over several pages and evaluate '
                       'both retrieval/extraction quality and grounding failures.\n'
                       '\n'
                       '**Lesson-specific goal:** demonstrate **Layout-Aware & OCR-Free Document Architectures** with '
                       'a controlled input set and at least one difficult example.\n'
                       '\n'
                       '## Debug / evaluate\n'
                       'Separate OCR/parsing, representation, retrieval, and answer-generation failure; preserve '
                       'page/source grounding.\n'
                       '\n'
                       '- Do not treat one successful sample as sufficient evidence.\n'
                       '- Record latency, memory, cost, ranking quality, task accuracy, or other metrics only when '
                       'actually measured.\n'
                       '- Preserve source-era architectural concepts while revalidating fast-moving model IDs and APIs '
                       'before implementation.\n'
                       '\n'
                       '## Assessment\n'
                       'Explain the principal engineering trade-off in **Layout-Aware & OCR-Free Document '
                       'Architectures**, provide evidence from the practice artifact, identify one realistic failure, '
                       'and state what would change your final design decision.\n'
                       '\n'
                       '## Source / modernization boundary\n'
                       'The instructional framing, exercises, quiz, and project integration are original Masar '
                       'curriculum material grounded in BOOK-008. Model checkpoints, APIs, package versions, and '
                       'hardware-specific behavior must be revalidated in the target repository before production '
                       'use.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Layout-Aware & OCR-Free Document Architectures — Guided Practice',
                'description': 'Build a reproducible artifact that demonstrates: Explain and compare layout-aware & '
                               'ocr-free document architectures and connect architectural choices to compute, memory, '
                               'quality, and implementation complexity.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ocr', 'layout', 'document-vqa']},
               {'title': 'Layout-Aware & OCR-Free Document Architectures — Debug / Evaluate',
                'description': 'Introduce or locate one realistic multimodal failure, diagnose it with evidence, '
                               'compare against the baseline, and document the corrective decision.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'evaluation']}],
 'quiz': {'title': 'Layout-Aware & OCR-Free Document Architectures — Knowledge Check',
          'questions': [{'question': 'What is the primary objective of Layout-Aware & OCR-Free Document Architectures?',
                         'options': ['Explain and compare layout-aware & ocr-free document architectures and connect '
                                     'architectural choices to compute, memory, quality, and implementation '
                                     'complexity.',
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
