LESSON = {'lesson_id': 'L006-050',
 'module_id': 'M006-08',
 'title': 'Inference Metrics, SLOs & Goodput',
 'slug': 'inference-metrics-slos-and-goodput',
 'guided_minutes': 50,
 'classification': 'REVISION + PRODUCTION EXTENSION',
 'status': 'finalized_curriculum_seed',
 'source_mapping': {'source_id': 'BOOK-006',
                    'book_title': 'AI Engineering',
                    'edition': 'SOURCE INFORMATION MISSING',
                    'source_type': 'BOOK-006',
                    'chapter': 'Chapter 8 — Dataset Engineering',
                    'pages': 'pp. 363–404'},
 'focus': 'Use percentiles, TTFT, TPOT, throughput, cost, and goodput to optimize for user-visible SLOs.',
 'learning_objectives': ['Explain the production-engineering purpose of inference metrics, slos & goodput.',
                         'Apply the lesson to a realistic AI-system decision: Use percentiles, TTFT, TPOT, '
                         'throughput, cost, and goodput to optimize for user-visible SLOs.',
                         'Measure or validate the decision with explicit acceptance criteria rather than '
                         'intuition alone.'],
 'content_outline': [{'type': 'revision_gate',
                      'text': 'Identify prerequisite concepts already taught in COURSE-001..005 and treat '
                              'them as revision.'},
                     {'type': 'production_focus',
                      'text': 'Use percentiles, TTFT, TPOT, throughput, cost, and goodput to optimize for '
                              'user-visible SLOs.'},
                     {'type': 'decision_or_system_view',
                      'text': 'Connect the technique to measurable production quality, latency, cost, '
                              'security, reliability, or maintainability.'}],
 'practice': {'title': 'Practice — Inference Metrics, SLOs & Goodput',
              'instructions': 'Apply this lesson to a small production-AI scenario. Use percentiles, TTFT, '
                              'TPOT, throughput, cost, and goodput to optimize for user-visible SLOs.',
              'acceptance_criteria': ['The decision or design is explicit and testable.',
                                      'Relevant quality, latency, cost, safety, or reliability trade-offs '
                                      'are identified.',
                                      'Repeated prerequisite material is referenced as revision rather than '
                                      'treated as a new competency.']},
 'quiz': [{'question': 'What is the primary production purpose of Inference Metrics, SLOs & Goodput?',
           'answer': 'To make an explicit, evidence-based engineering decision for a production AI system.',
           'explanation': 'COURSE-006 emphasizes measurable system behavior and production trade-offs.'},
          {'question': 'How should repeated material from COURSE-001 through COURSE-005 be treated?',
           'answer': 'As revision unless the lesson adds genuine production depth.',
           'explanation': 'This prevents duplicated competencies while preserving prerequisite recall.'}]}
