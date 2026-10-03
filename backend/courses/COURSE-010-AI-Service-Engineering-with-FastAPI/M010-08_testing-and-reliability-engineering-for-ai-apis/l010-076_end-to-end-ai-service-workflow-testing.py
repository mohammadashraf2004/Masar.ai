LESSON_ID = 'L010-076'
MODULE_ID = 'M010-08'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-076',
 'module_id': 'M010-08',
 'module_title': 'Testing & Reliability Engineering for AI APIs',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 11,
            'sections': ['End-to-End Testing', 'Vertical E2E Tests', 'Horizontal E2E Tests'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['vertical E2E',
              'horizontal E2E',
              'critical journey',
              'smoke flow',
              'workflow side effect',
              'test client'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'End-to-End AI Service Workflow Testing',
 'slug': 'course-010-l010-076-end-to-end-ai-service-workflow-testing',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: End-to-End AI Service '
                'Workflow Testing.',
 'order': 8,
 'difficulty': 'advanced',
 'estimated_hours': 0.92,
 'skill_tags': ['ai-service-engineering',
                'testing-and-reliability-engineering-for-ai-apis',
                'vertical-e2e',
                'horizontal-e2e',
                'critical-journey',
                'smoke-flow',
                'workflow-side-effect'],
 'prerequisite_ids': [],
 'lesson': {'title': 'End-to-End AI Service Workflow Testing',
            'content': '# End-to-End AI Service Workflow Testing\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **automate a small set of '
                       'critical user journeys across authentication, API, persistence, streaming, '
                       'security, and model-provider boundaries.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**End-to-End AI Service Workflow Testing** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **vertical E2E**\n'
                       '- **horizontal E2E**\n'
                       '- **critical journey**\n'
                       '- **smoke flow**\n'
                       '- **workflow side effect**\n'
                       '- **test client**\n'
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
                       '{{figure:e2e-boundaries}}\n'
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
                       'For this lesson specifically, watch for mistakes around **vertical E2E**, '
                       '**horizontal E2E**, and **critical journey**. Prefer explicit failure '
                       'behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Automate login -> conversation -> streamed generation -> persistence plus '
                       'an unauthorized/security failure workflow.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 11\n'
                       '- **Sections:** End-to-End Testing, Vertical E2E Tests, Horizontal E2E '
                       'Tests\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **End-to-End AI Service Workflow Testing** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: End-to-End AI Service Workflow Testing',
                'description': 'Automate login -> conversation -> streamed generation -> '
                               'persistence plus an unauthorized/security failure workflow. '
                               'Capture the acceptance evidence and explain one failure case.',
                'difficulty': 'advanced',
                'skill_tested': ['vertical-e2e', 'horizontal-e2e', 'critical-journey']},
               {'title': 'Debug or Decide: End-to-End AI Service Workflow Testing',
                'description': 'Start from an intentionally weak design involving vertical E2E and '
                               'horizontal E2E. Identify the failure boundary, apply the smallest '
                               'justified correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['vertical-e2e', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'End-to-End AI Service Workflow Testing — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for end-to-end ai '
                                     'service workflow testing?',
                         'options': ['Make vertical E2E explicit, test the boundary, and verify '
                                     'behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats vertical E2E as an engineering boundary '
                                        'with explicit behavior and verification, not as a one-off '
                                        'implementation detail.'},
                        {'question': 'Why should horizontal E2E be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of horizontal E2E exposes assumptions, '
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
 'project': {'title': 'Release Reliability Test Suite',
             'description': 'Create the release gate with unit, integration, async, '
                            'behavioral/regression, and focused E2E tests.',
             'objectives': ['Isolate deterministic logic',
                            'Test real integration contracts',
                            'Evaluate probabilistic behavior',
                            'Automate critical workflows'],
             'tech_stack': ['pytest', 'HTTPX', 'AnyIO/pytest-asyncio', 'test DB/cache'],
             'estimated_hours': 8}}
