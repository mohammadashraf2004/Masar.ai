LESSON = {'lesson_id': 'L006-049',
 'module_id': 'M006-08',
 'title': 'Diagnosing Production Inference Bottlenecks',
 'slug': 'diagnosing-production-inference-bottlenecks',
 'guided_minutes': 50,
 'classification': 'CORE + REVISION',
 'status': 'finalized_curriculum_seed',
 'source_mapping': {'source_id': 'BOOK-006',
                    'book_title': 'AI Engineering',
                    'edition': 'SOURCE INFORMATION MISSING',
                    'source_type': 'BOOK-006',
                    'chapter': 'Chapter 8 — Dataset Engineering',
                    'pages': 'pp. 363–404'},
 'focus': 'Profile workload characteristics and determine whether prefill, decode, compute, memory, or '
          'traffic is limiting performance.',
 'learning_objectives': ['Explain the production-engineering purpose of diagnosing production inference '
                         'bottlenecks.',
                         'Apply the lesson to a realistic AI-system decision: Profile workload '
                         'characteristics and determine whether prefill, decode, compute, memory, or traffic '
                         'is limiting performance.',
                         'Measure or validate the decision with explicit acceptance criteria rather than '
                         'intuition alone.'],
 'content_outline': [{'type': 'revision_gate',
                      'text': 'Identify prerequisite concepts already taught in COURSE-001..005 and treat '
                              'them as revision.'},
                     {'type': 'production_focus',
                      'text': 'Profile workload characteristics and determine whether prefill, decode, '
                              'compute, memory, or traffic is limiting performance.'},
                     {'type': 'decision_or_system_view',
                      'text': 'Connect the technique to measurable production quality, latency, cost, '
                              'security, reliability, or maintainability.'}],
 'practice': {'title': 'Practice — Diagnosing Production Inference Bottlenecks',
              'instructions': 'Apply this lesson to a small production-AI scenario. Profile workload '
                              'characteristics and determine whether prefill, decode, compute, memory, or '
                              'traffic is limiting performance.',
              'acceptance_criteria': ['The decision or design is explicit and testable.',
                                      'Relevant quality, latency, cost, safety, or reliability trade-offs '
                                      'are identified.',
                                      'Repeated prerequisite material is referenced as revision rather than '
                                      'treated as a new competency.']},
 'quiz': [{'question': 'What is the primary production purpose of Diagnosing Production Inference '
                       'Bottlenecks?',
           'answer': 'To make an explicit, evidence-based engineering decision for a production AI system.',
           'explanation': 'COURSE-006 emphasizes measurable system behavior and production trade-offs.'},
          {'question': 'How should repeated material from COURSE-001 through COURSE-005 be treated?',
           'answer': 'As revision unless the lesson adds genuine production depth.',
           'explanation': 'This prevents duplicated competencies while preserving prerequisite recall.'}]}
