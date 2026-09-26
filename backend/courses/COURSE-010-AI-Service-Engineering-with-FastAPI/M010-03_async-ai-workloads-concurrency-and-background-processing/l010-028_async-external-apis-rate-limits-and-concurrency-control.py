LESSON_ID = 'L010-028'
MODULE_ID = 'M010-03'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-028',
 'module_id': 'M010-03',
 'module_title': 'Async AI Workloads, Concurrency & Background Processing',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 5,
            'sections': ['External APIs', 'Async Model Providers'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['async HTTP',
              'connection reuse',
              'timeout',
              'retry',
              'backoff',
              'Semaphore',
              'provider rate limit'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'visual_reference': None,
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Async External APIs, Rate Limits & Concurrency Control',
 'slug': 'course-010-l010-028-async-external-apis-rate-limits-and-concurrency-control',
 'description': 'Intermediate AI Service Engineering with FastAPI lesson: Async External APIs, '
                'Rate Limits & Concurrency Control.',
 'order': 4,
 'difficulty': 'intermediate',
 'estimated_hours': 0.92,
 'skill_tags': ['ai-service-engineering',
                'async-ai-workloads-concurrency-and-background-processing',
                'async-http',
                'connection-reuse',
                'timeout',
                'retry',
                'backoff'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Async External APIs, Rate Limits & Concurrency Control',
            'content': '# Async External APIs, Rate Limits & Concurrency Control\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **call remote '
                       'AI/providers concurrently while applying timeouts, retries, and bounded '
                       'concurrency.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. **Async '
                       'External APIs, Rate Limits & Concurrency Control** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **async HTTP**\n'
                       '- **connection reuse**\n'
                       '- **timeout**\n'
                       '- **retry**\n'
                       '- **backoff**\n'
                       '- **Semaphore**\n'
                       '- **provider rate limit**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'Classify workload → choose async/thread/process/external job boundary → '
                       'measure responsiveness\n'
                       '```\n'
                       '\n'
                       'Use the mental model to identify what enters the component, what '
                       'responsibility it owns, what it must not own, and what evidence you need '
                       'when it fails.\n'
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
                       'import asyncio\n'
                       '\n'
                       'async def bounded_call(name: str, semaphore: asyncio.Semaphore) -> str:\n'
                       '    async with semaphore:\n'
                       '        await asyncio.sleep(0.01)\n'
                       '        return name\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'Adding async syntax around blocking compute does not make the event loop '
                       'safe; classify the workload first.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around **async HTTP**, '
                       '**connection reuse**, and **timeout**. Prefer explicit failure behavior '
                       'and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Send multiple mock provider requests concurrently, then protect the '
                       'provider with a semaphore and timeout/retry policy.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 5\n'
                       '- **Sections:** External APIs, Async Model Providers\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Async External APIs, Rate Limits & Concurrency Control** as a '
                       'reusable service-engineering capability. The exact provider, framework '
                       'version, model, database, or hosting platform can change; the boundary, '
                       'failure mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Async External APIs, Rate Limits & Concurrency Control',
                'description': 'Send multiple mock provider requests concurrently, then protect '
                               'the provider with a semaphore and timeout/retry policy. Capture '
                               'the acceptance evidence and explain one failure case.',
                'difficulty': 'intermediate',
                'skill_tested': ['async-http', 'connection-reuse', 'timeout']},
               {'title': 'Debug or Decide: Async External APIs, Rate Limits & Concurrency Control',
                'description': 'Start from an intentionally weak design involving async HTTP and '
                               'connection reuse. Identify the failure boundary, apply the '
                               'smallest justified correction, and add a regression check.',
                'difficulty': 'intermediate',
                'skill_tested': ['async-http', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Async External APIs, Rate Limits & Concurrency Control — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for async '
                                     'external apis, rate limits & concurrency control?',
                         'options': ['Make async HTTP explicit, test the boundary, and verify '
                                     'behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats async HTTP as an engineering boundary '
                                        'with explicit behavior and verification, not as a one-off '
                                        'implementation detail.'},
                        {'question': 'Why should connection reuse be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of connection reuse exposes '
                                        'assumptions, makes failures diagnosable, and supports '
                                        'regression protection; it does not guarantee universal '
                                        'behavior.'},
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
             'difficulty': 'intermediate',
             'tech_stack': [],
             'objectives': [],
             'estimated_hours': None}}
