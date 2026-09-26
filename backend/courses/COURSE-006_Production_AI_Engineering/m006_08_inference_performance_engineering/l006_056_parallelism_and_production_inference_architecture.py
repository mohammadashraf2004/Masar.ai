LESSON = {'lesson_id': 'L006-056',
 'module_id': 'M006-08',
 'title': 'Parallelism & Production Inference Architecture',
 'slug': 'parallelism-and-production-inference-architecture',
 'guided_minutes': 50,
 'classification': 'CORE + REVISION',
 'status': 'finalized_curriculum_seed',
 'source_mapping': {'source_id': 'BOOK-006',
                    'book_title': 'AI Engineering',
                    'edition': 'SOURCE INFORMATION MISSING',
                    'source_type': 'BOOK-006',
                    'chapter': 'Chapter 8 — Dataset Engineering',
                    'pages': 'pp. 363–404'},
 'focus': 'Choose replica, tensor, and pipeline strategies according to model fit, latency, throughput, and '
          'communication overhead.',
 'learning_objectives': ['Explain the production-engineering purpose of parallelism & production inference '
                         'architecture.',
                         'Apply the lesson to a realistic AI-system decision: Choose replica, tensor, and '
                         'pipeline strategies according to model fit, latency, throughput, and communication '
                         'overhead.',
                         'Measure or validate the decision with explicit acceptance criteria rather than '
                         'intuition alone.'],
 'content_outline': [{'type': 'revision_gate',
                      'text': 'Identify prerequisite concepts already taught in COURSE-001..005 and treat '
                              'them as revision.'},
                     {'type': 'production_focus',
                      'text': 'Choose replica, tensor, and pipeline strategies according to model fit, '
                              'latency, throughput, and communication overhead.'},
                     {'type': 'decision_or_system_view',
                      'text': 'Connect the technique to measurable production quality, latency, cost, '
                              'security, reliability, or maintainability.'}],
 'practice': {'title': 'Practice — Parallelism & Production Inference Architecture',
              'instructions': 'Apply this lesson to a small production-AI scenario. Choose replica, tensor, '
                              'and pipeline strategies according to model fit, latency, throughput, and '
                              'communication overhead.',
              'acceptance_criteria': ['The decision or design is explicit and testable.',
                                      'Relevant quality, latency, cost, safety, or reliability trade-offs '
                                      'are identified.',
                                      'Repeated prerequisite material is referenced as revision rather than '
                                      'treated as a new competency.']},
 'quiz': [{'question': 'What is the primary production purpose of Parallelism & Production Inference '
                       'Architecture?',
           'answer': 'To make an explicit, evidence-based engineering decision for a production AI system.',
           'explanation': 'COURSE-006 emphasizes measurable system behavior and production trade-offs.'},
          {'question': 'How should repeated material from COURSE-001 through COURSE-005 be treated?',
           'answer': 'As revision unless the lesson adds genuine production depth.',
           'explanation': 'This prevents duplicated competencies while preserving prerequisite recall.'}]}
