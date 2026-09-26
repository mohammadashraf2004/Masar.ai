LESSON_ID = 'L010-004'
MODULE_ID = 'M010-01'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-004',
 'module_id': 'M010-01',
 'module_title': 'AI Service Architecture & FastAPI Foundations',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 2,
            'sections': ['Getting Started with FastAPI'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['FastAPI app',
              'path operation',
              'route handler',
              'Uvicorn',
              'FastAPI CLI',
              'health endpoint'],
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

TOPIC = {'title': 'Build Your First FastAPI AI Service',
 'slug': 'course-010-l010-004-build-your-first-fastapi-ai-service',
 'description': 'Intermediate AI Service Engineering with FastAPI lesson: Build Your First FastAPI '
                'AI Service.',
 'order': 4,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['ai-service-engineering',
                'ai-service-architecture-and-fastapi-foundations',
                'fastapi-app',
                'path-operation',
                'route-handler',
                'uvicorn',
                'fastapi-cli'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Build Your First FastAPI AI Service',
            'content': '# Build Your First FastAPI AI Service\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **create, run, and '
                       'inspect a minimal FastAPI AI service with health, information, and '
                       'generation endpoints.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. **Build '
                       'Your First FastAPI AI Service** gives you a concrete engineering technique '
                       'for making one of those boundaries explicit, testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **FastAPI app**\n'
                       '- **path operation**\n'
                       '- **route handler**\n'
                       '- **Uvicorn**\n'
                       '- **FastAPI CLI**\n'
                       '- **health endpoint**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'Client → FastAPI transport → service/control layer → provider/data/tool → '
                       'validated response\n'
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
                       'from fastapi import FastAPI\n'
                       '\n'
                       'app = FastAPI()\n'
                       '\n'
                       '@app.get("/health")\n'
                       'async def health() -> dict[str, str]:\n'
                       '    return {"status": "ok"}\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'Mixing transport, provider, persistence, and policy code in one route '
                       'makes the backend hard to test and change.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around **FastAPI app**, '
                       '**path operation**, and **route handler**. Prefer explicit failure '
                       'behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Build /health, /api/v1/info, and a fake /api/v1/generate endpoint, then '
                       'verify JSON responses and /docs.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 2\n'
                       '- **Sections:** Getting Started with FastAPI\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Build Your First FastAPI AI Service** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Build Your First FastAPI AI Service',
                'description': 'Build /health, /api/v1/info, and a fake /api/v1/generate endpoint, '
                               'then verify JSON responses and /docs. Capture the acceptance '
                               'evidence and explain one failure case.',
                'difficulty': 'intermediate',
                'skill_tested': ['fastapi-app', 'path-operation', 'route-handler']},
               {'title': 'Debug or Decide: Build Your First FastAPI AI Service',
                'description': 'Start from an intentionally weak design involving FastAPI app and '
                               'path operation. Identify the failure boundary, apply the smallest '
                               'justified correction, and add a regression check.',
                'difficulty': 'intermediate',
                'skill_tested': ['fastapi-app', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Build Your First FastAPI AI Service — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for build your '
                                     'first fastapi ai service?',
                         'options': ['Make FastAPI app explicit, test the boundary, and verify '
                                     'behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats FastAPI app as an engineering boundary '
                                        'with explicit behavior and verification, not as a one-off '
                                        'implementation detail.'},
                        {'question': 'Why should path operation be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of path operation exposes assumptions, '
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
             'difficulty': 'intermediate',
             'tech_stack': [],
             'objectives': [],
             'estimated_hours': None}}
