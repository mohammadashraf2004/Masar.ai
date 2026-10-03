LESSON_ID = 'L010-071'
MODULE_ID = 'M010-08'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-071',
 'module_id': 'M010-08',
 'module_title': 'Testing & Reliability Engineering for AI APIs',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 11,
            'sections': ['Unit Tests', 'Test Doubles', 'Mocking and Patching'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['dummy', 'stub', 'spy', 'mock', 'fake', 'dependency override', 'provider interface'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Unit Tests, Test Doubles & Dependency Injection',
 'slug': 'course-010-l010-071-unit-tests-test-doubles-and-dependency-injection',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: Unit Tests, Test Doubles & '
                'Dependency Injection.',
 'order': 3,
 'difficulty': 'advanced',
 'estimated_hours': 0.92,
 'skill_tags': ['ai-service-engineering',
                'testing-and-reliability-engineering-for-ai-apis',
                'dummy',
                'stub',
                'spy',
                'mock',
                'fake'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Unit Tests, Test Doubles & Dependency Injection',
            'content': '# Unit Tests, Test Doubles & Dependency Injection\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **use fakes, stubs, '
                       'spies, mocks, and FastAPI dependency overrides to isolate business logic '
                       'from expensive/external systems.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. **Unit '
                       'Tests, Test Doubles & Dependency Injection** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **dummy**\n'
                       '- **stub**\n'
                       '- **spy**\n'
                       '- **mock**\n'
                       '- **fake**\n'
                       '- **dependency override**\n'
                       '- **provider interface**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'Static checks → unit → integration → behavioral/regression → focused E2E → '
                       'release decision\n'
                       '```\n'
                       '\n'
                       'Use the mental model to identify what enters the component, what '
                       'responsibility it owns, what it must not own, and what evidence you need '
                       'when it fails.\n'
                       '\n'
                       '{{figure:test-doubles}}\n'
                       '\n'
                       '## Engineering workflow\n'
                       '\n'
                       '1. **State the contract.** Write down the expected input, output, side '
                       'effects, and failure behavior before selecting a library feature.\n'
                       '2. **Keep responsibilities local.** Put transport, business rules, '
                       'provider access, persistence, policy, and deployment concerns behind clear '
                       'interfaces.\n'
                       '3. **Build the smallest realistic implementation.** Use fakes or local '
                       'resources when external providers or GPUs would distract from the service '
                       'competency.\n'
                       '4. **Exercise the failure path.** Test malformed input, unavailable '
                       'dependencies, timeout/cancellation, permission problems, or incompatible '
                       'state where relevant.\n'
                       '5. **Measure or verify the outcome.** Use tests, traces, timings, database '
                       'state, security decisions, or deployment smoke checks instead of relying '
                       'on a visually successful demo.\n'
                       '\n'
                       '## Practical implementation pattern\n'
                       '\n'
                       '```python\n'
                       'def test_health(client):\n'
                       '    response = client.get("/health")\n'
                       '    assert response.status_code == 200\n'
                       '    assert response.json()["status"] == "ok"\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'Tests that are broad, slow, network-dependent, or exact-string based in '
                       'the wrong places become flaky and stop protecting releases.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around **dummy**, '
                       '**stub**, and **spy**. Prefer explicit failure behavior and regression '
                       'protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Test GenerationService with a FakeProvider and use '
                       'app.dependency_overrides rather than patching nested provider SDK '
                       'internals.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 11\n'
                       '- **Sections:** Unit Tests, Test Doubles, Mocking and Patching\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Unit Tests, Test Doubles & Dependency Injection** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Unit Tests, Test Doubles & Dependency Injection',
                'description': 'Test GenerationService with a FakeProvider and use '
                               'app.dependency_overrides rather than patching nested provider SDK '
                               'internals. Capture the acceptance evidence and explain one failure '
                               'case.',
                'difficulty': 'advanced',
                'skill_tested': ['dummy', 'stub', 'spy']},
               {'title': 'Debug or Decide: Unit Tests, Test Doubles & Dependency Injection',
                'description': 'Start from an intentionally weak design involving dummy and stub. '
                               'Identify the failure boundary, apply the smallest justified '
                               'correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['dummy', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Unit Tests, Test Doubles & Dependency Injection — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for unit tests, '
                                     'test doubles & dependency injection?',
                         'options': ['Make dummy explicit, test the boundary, and verify behavior '
                                     'with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats dummy as an engineering boundary with '
                                        'explicit behavior and verification, not as a one-off '
                                        'implementation detail.'},
                        {'question': 'Why should stub be handled explicitly in this lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of stub exposes assumptions, makes '
                                        'failures diagnosable, and supports regression protection; '
                                        'it does not guarantee universal behavior.'},
                        {'question': 'Which evidence best supports a production decision after '
                                     'changing this part of the service?',
                         'options': ['A repeatable test, trace, metric, state check, or smoke test '
                                     'tied to the requirement',
                                     'A screenshot of one successful response only',
                                     'A provider marketing benchmark with a different workload',
                                     'The fact that the code runs without a syntax error'],
                         'correct': 0,
                         'explanation': 'Production decisions need evidence tied to the actual '
                                        'contract and workload. Syntax and isolated demos are '
                                        'necessary but insufficient.'}],
          'passing_score': 70},
 'project': {'title': None,
             'description': None,
             'difficulty': 'advanced',
             'tech_stack': [],
             'objectives': [],
             'estimated_hours': None}}
