LESSON_ID = 'L010-061'
MODULE_ID = 'M010-06'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-061',
 'module_id': 'M010-06',
 'module_title': 'Authentication, Authorization & Secure Service Boundaries',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 9,
            'sections': ['Distributed Rate Limiting', 'Streaming Throttling'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['distributed limiter',
              'Redis',
              'user key',
              'organization key',
              'connection limit',
              'message rate',
              'stream duration'],
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

TOPIC = {'title': 'Distributed Rate Limiting & Streaming Abuse Controls',
 'slug': 'course-010-l010-061-distributed-rate-limiting-and-streaming-abuse-controls',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: Distributed Rate Limiting & '
                'Streaming Abuse Controls.',
 'order': 14,
 'difficulty': 'advanced',
 'estimated_hours': 0.75,
 'skill_tags': ['ai-service-engineering',
                'authentication-authorization-and-secure-service-boundaries',
                'distributed-limiter',
                'redis',
                'user-key',
                'organization-key',
                'connection-limit'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Distributed Rate Limiting & Streaming Abuse Controls',
            'content': '# Distributed Rate Limiting & Streaming Abuse Controls\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **apply shared limiter '
                       'state and long-lived connection controls consistently across multiple API '
                       'instances.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Distributed Rate Limiting & Streaming Abuse Controls** gives you a '
                       'concrete engineering technique for making one of those boundaries '
                       'explicit, testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **distributed limiter**\n'
                       '- **Redis**\n'
                       '- **user key**\n'
                       '- **organization key**\n'
                       '- **connection limit**\n'
                       '- **message rate**\n'
                       '- **stream duration**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'Authenticate → authorize → usage/input controls → AI/tool operation → '
                       'output controls\n'
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
                       'async def authorize(principal, action: str, resource) -> None:\n'
                       '    allowed = await resource.policy.allows(principal, action)\n'
                       '    if not allowed:\n'
                       '        raise PermissionError("forbidden")\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'The model is not a policy engine. Privileged data/actions must be '
                       'constrained by deterministic application controls.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around **distributed '
                       'limiter**, **Redis**, and **user key**. Prefer explicit failure behavior '
                       'and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Design limits for requests, active streams, messages, duration, and output '
                       'budget across three API replicas sharing limiter state.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 9\n'
                       '- **Sections:** Distributed Rate Limiting, Streaming Throttling\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Distributed Rate Limiting & Streaming Abuse Controls** as a '
                       'reusable service-engineering capability. The exact provider, framework '
                       'version, model, database, or hosting platform can change; the boundary, '
                       'failure mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Distributed Rate Limiting & Streaming Abuse Controls',
                'description': 'Design limits for requests, active streams, messages, duration, '
                               'and output budget across three API replicas sharing limiter state. '
                               'Capture the acceptance evidence and explain one failure case.',
                'difficulty': 'advanced',
                'skill_tested': ['distributed-limiter', 'redis', 'user-key']},
               {'title': 'Debug or Decide: Distributed Rate Limiting & Streaming Abuse Controls',
                'description': 'Start from an intentionally weak design involving distributed '
                               'limiter and Redis. Identify the failure boundary, apply the '
                               'smallest justified correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['distributed-limiter', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Distributed Rate Limiting & Streaming Abuse Controls — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for distributed '
                                     'rate limiting & streaming abuse controls?',
                         'options': ['Make distributed limiter explicit, test the boundary, and '
                                     'verify behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats distributed limiter as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should Redis be handled explicitly in this lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of Redis exposes assumptions, makes '
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
 'project': {'title': 'Hardened Identity & Security Boundary',
             'description': 'Add identity, authorization, OAuth/JWT-aware flows, guardrails, '
                            'quotas, distributed rate limits, and tool/output validation.',
             'objectives': ['Authenticate principals',
                            'Enforce ownership/roles/attributes',
                            'Block unsafe input/output paths',
                            'Protect service capacity'],
             'tech_stack': ['FastAPI security', 'JWT/OIDC concepts', 'Redis', 'Pydantic'],
             'estimated_hours': 9}}
