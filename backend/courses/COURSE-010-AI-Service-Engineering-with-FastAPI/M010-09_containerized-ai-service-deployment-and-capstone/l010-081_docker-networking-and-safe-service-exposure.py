LESSON_ID = 'L010-081'
MODULE_ID = 'M010-09'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-081',
 'module_id': 'M010-09',
 'module_title': 'Containerized AI Service Deployment & Capstone',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 12,
            'sections': ['Docker Networking', 'Bridge Network Driver', 'Publishing Ports'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['bridge network',
              'embedded DNS',
              'service name',
              'port publishing',
              '127.0.0.1 binding',
              'network isolation'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Docker Networking & Safe Service Exposure',
 'slug': 'course-010-l010-081-docker-networking-and-safe-service-exposure',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: Docker Networking & Safe '
                'Service Exposure.',
 'order': 5,
 'difficulty': 'advanced',
 'estimated_hours': 1.0,
 'skill_tags': ['ai-service-engineering',
                'containerized-ai-service-deployment-and-capstone',
                'bridge-network',
                'embedded-dns',
                'service-name',
                'port-publishing',
                '127-0-0-1-binding'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Docker Networking & Safe Service Exposure',
            'content': '# Docker Networking & Safe Service Exposure\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **connect containers '
                       'through user-defined bridge networks and embedded DNS while exposing only '
                       'intended host ports.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Docker Networking & Safe Service Exposure** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **bridge network**\n'
                       '- **embedded DNS**\n'
                       '- **service name**\n'
                       '- **port publishing**\n'
                       '- **127.0.0.1 binding**\n'
                       '- **network isolation**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'Tested source → reproducible image → registry/runtime config → container '
                       'stack → smoke-tested release\n'
                       '```\n'
                       '\n'
                       'Use the mental model to identify what enters the component, what '
                       'responsibility it owns, what it must not own, and what evidence you need '
                       'when it fails.\n'
                       '\n'
                       '{{figure:isolated-bridge-networks}}\n'
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
                       '```text\n'
                       '# Deployment artifact mental model\n'
                       'source → build → image → registry → runtime → health/smoke checks\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'A container that runs locally is not automatically production-ready; '
                       'runtime identity, network exposure, secrets, storage, and health all '
                       'matter.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around **bridge '
                       'network**, **embedded DNS**, and **service name**. Prefer explicit failure '
                       'behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Create API+DB+Redis on a private bridge, publish only the API, and prove '
                       'the database/cache are not directly reachable from outside the network.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 12\n'
                       '- **Sections:** Docker Networking, Bridge Network Driver, Publishing '
                       'Ports\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Docker Networking & Safe Service Exposure** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 60,
            'has_code_examples': False},
 'exercises': [{'title': 'Build and Verify: Docker Networking & Safe Service Exposure',
                'description': 'Create API+DB+Redis on a private bridge, publish only the API, and '
                               'prove the database/cache are not directly reachable from outside '
                               'the network. Capture the acceptance evidence and explain one '
                               'failure case.',
                'difficulty': 'advanced',
                'skill_tested': ['bridge-network', 'embedded-dns', 'service-name']},
               {'title': 'Debug or Decide: Docker Networking & Safe Service Exposure',
                'description': 'Start from an intentionally weak design involving bridge network '
                               'and embedded DNS. Identify the failure boundary, apply the '
                               'smallest justified correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['bridge-network', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Docker Networking & Safe Service Exposure — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for docker '
                                     'networking & safe service exposure?',
                         'options': ['Make bridge network explicit, test the boundary, and verify '
                                     'behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats bridge network as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should embedded DNS be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of embedded DNS exposes assumptions, '
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
