LESSON_ID = 'L010-069'
MODULE_ID = 'M010-08'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-069',
 'module_id': 'M010-08',
 'module_title': 'Testing & Reliability Engineering for AI APIs',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 11,
            'sections': ['Testing Strategies', 'Testing Boundaries'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['system under test',
              'test boundary',
              'unit test',
              'integration test',
              'E2E',
              'behavioral evaluation',
              'verification vs validation'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Designing an AI Service Test Strategy',
 'slug': 'course-010-l010-069-designing-an-ai-service-test-strategy',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: Designing an AI Service Test '
                'Strategy.',
 'order': 1,
 'difficulty': 'advanced',
 'estimated_hours': 0.83,
 'skill_tags': ['ai-service-engineering',
                'testing-and-reliability-engineering-for-ai-apis',
                'system-under-test',
                'test-boundary',
                'unit-test',
                'integration-test',
                'e2e'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Designing an AI Service Test Strategy',
            'content': '# Designing an AI Service Test Strategy\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **choose static, unit, '
                       'integration, behavioral, and E2E boundaries according to the confidence '
                       'and cost required.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Designing an AI Service Test Strategy** gives you a concrete engineering '
                       'technique for making one of those boundaries explicit, testable, and '
                       'observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **system under test**\n'
                       '- **test boundary**\n'
                       '- **unit test**\n'
                       '- **integration test**\n'
                       '- **E2E**\n'
                       '- **behavioral evaluation**\n'
                       '- **verification vs validation**\n'
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
                       '{{figure:test-boundaries}}\n'
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
                       'For this lesson specifically, watch for mistakes around **system under '
                       'test**, **test boundary**, and **unit test**. Prefer explicit failure '
                       'behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Classify 15 capstone components/workflows into the right testing layer and '
                       'explain the trade-off between confidence, cost, and fragility.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 11\n'
                       '- **Sections:** Testing Strategies, Testing Boundaries\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Designing an AI Service Test Strategy** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 50,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Designing an AI Service Test Strategy',
                'description': 'Classify 15 capstone components/workflows into the right testing '
                               'layer and explain the trade-off between confidence, cost, and '
                               'fragility. Capture the acceptance evidence and explain one failure '
                               'case.',
                'difficulty': 'advanced',
                'skill_tested': ['system-under-test', 'test-boundary', 'unit-test']},
               {'title': 'Debug or Decide: Designing an AI Service Test Strategy',
                'description': 'Start from an intentionally weak design involving system under '
                               'test and test boundary. Identify the failure boundary, apply the '
                               'smallest justified correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['system-under-test', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Designing an AI Service Test Strategy — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for designing an '
                                     'ai service test strategy?',
                         'options': ['Make system under test explicit, test the boundary, and '
                                     'verify behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats system under test as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should test boundary be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of test boundary exposes assumptions, '
                                        'makes failures diagnosable, and supports regression '
                                        'protection; it does not guarantee universal behavior.'},
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
