LESSON = {'lesson_id': 'L006-011',
 'module_id': 'M006-02',
 'title': 'Sampling, Test-Time Compute, and Reliability',
 'slug': 'sampling-test-time-compute-and-reliability',
 'guided_minutes': 45,
 'classification': 'REVISION + PRODUCTION EXTENSION',
 'status': 'finalized_curriculum_seed',
 'source_mapping': {'source_id': 'BOOK-006',
                    'book_title': 'AI Engineering',
                    'edition': 'SOURCE INFORMATION MISSING',
                    'source_type': 'BOOK-006',
                    'chapter': 'Chapter 2 — Understanding Foundation Models',
                    'pages': 'pp. 49–111'},
 'focus': 'Connect generation controls and test-time compute to reliability, latency, and cost trade-offs.',
 'learning_objectives': ['Explain the production-engineering purpose of sampling, test-time compute, and '
                         'reliability.',
                         'Apply the lesson to a realistic AI-system decision: Connect generation controls '
                         'and test-time compute to reliability, latency, and cost trade-offs.',
                         'Measure or validate the decision with explicit acceptance criteria rather than '
                         'intuition alone.'],
 'content_outline': [{'type': 'revision_gate',
                      'text': 'Identify prerequisite concepts already taught in COURSE-001..005 and treat '
                              'them as revision.'},
                     {'type': 'production_focus',
                      'text': 'Connect generation controls and test-time compute to reliability, latency, '
                              'and cost trade-offs.'},
                     {'type': 'decision_or_system_view',
                      'text': 'Connect the technique to measurable production quality, latency, cost, '
                              'security, reliability, or maintainability.'}],
 'practice': {'title': 'Practice — Sampling, Test-Time Compute, and Reliability',
              'instructions': 'Apply this lesson to a small production-AI scenario. Connect generation '
                              'controls and test-time compute to reliability, latency, and cost trade-offs.',
              'acceptance_criteria': ['The decision or design is explicit and testable.',
                                      'Relevant quality, latency, cost, safety, or reliability trade-offs '
                                      'are identified.',
                                      'Repeated prerequisite material is referenced as revision rather than '
                                      'treated as a new competency.']},
 'quiz': [{'question': 'What is the primary production purpose of Sampling, Test-Time Compute, and '
                       'Reliability?',
           'answer': 'To make an explicit, evidence-based engineering decision for a production AI system.',
           'explanation': 'COURSE-006 emphasizes measurable system behavior and production trade-offs.'},
          {'question': 'How should repeated material from COURSE-001 through COURSE-005 be treated?',
           'answer': 'As revision unless the lesson adds genuine production depth.',
           'explanation': 'This prevents duplicated competencies while preserving prerequisite recall.'}]}
