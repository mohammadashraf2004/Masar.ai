LESSON_ID = 'L010-078'
MODULE_ID = 'M010-09'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-078',
 'module_id': 'M010-09',
 'module_title': 'Containerized AI Service Deployment & Capstone',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 12,
            'sections': ['Deploying with Containers', 'Building Docker Images'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['Dockerfile', 'base image', 'WORKDIR', 'COPY', 'RUN', 'CMD', 'EXPOSE', 'container'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'visual_reference': [{'chapter': 12,
                       'figure': 'Figure 12-4',
                       'title': 'Docker platform system architecture',
                       'filename': 'fig_12_04_docker_platform.png'}],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Containerizing a FastAPI AI Service',
 'slug': 'course-010-l010-078-containerizing-a-fastapi-ai-service',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: Containerizing a FastAPI AI '
                'Service.',
 'order': 2,
 'difficulty': 'advanced',
 'estimated_hours': 1.0,
 'skill_tags': ['ai-service-engineering',
                'containerized-ai-service-deployment-and-capstone',
                'dockerfile',
                'base-image',
                'workdir',
                'copy',
                'run'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Containerizing a FastAPI AI Service',
            'content': '# Containerizing a FastAPI AI Service\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **package the capstone '
                       'into a reproducible Docker image with a clear base, dependency layer, app '
                       'layer, runtime user, and startup command.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Containerizing a FastAPI AI Service** gives you a concrete engineering '
                       'technique for making one of those boundaries explicit, testable, and '
                       'observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **Dockerfile**\n'
                       '- **base image**\n'
                       '- **WORKDIR**\n'
                       '- **COPY**\n'
                       '- **RUN**\n'
                       '- **CMD**\n'
                       '- **EXPOSE**\n'
                       '- **container**\n'
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
                       'For this lesson specifically, watch for mistakes around **Dockerfile**, '
                       '**base image**, and **WORKDIR**. Prefer explicit failure behavior and '
                       'regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Write and build a Dockerfile for the API, run it locally, verify lifespan '
                       'startup/shutdown, and confirm /health is reachable.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 12\n'
                       '- **Sections:** Deploying with Containers, Building Docker Images\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Containerizing a FastAPI AI Service** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 60,
            'has_code_examples': False},
 'exercises': [{'title': 'Build and Verify: Containerizing a FastAPI AI Service',
                'description': 'Write and build a Dockerfile for the API, run it locally, verify '
                               'lifespan startup/shutdown, and confirm /health is reachable. '
                               'Capture the acceptance evidence and explain one failure case.',
                'difficulty': 'advanced',
                'skill_tested': ['dockerfile', 'base-image', 'workdir']},
               {'title': 'Debug or Decide: Containerizing a FastAPI AI Service',
                'description': 'Start from an intentionally weak design involving Dockerfile and '
                               'base image. Identify the failure boundary, apply the smallest '
                               'justified correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['dockerfile', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Containerizing a FastAPI AI Service — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for '
                                     'containerizing a fastapi ai service?',
                         'options': ['Make Dockerfile explicit, test the boundary, and verify '
                                     'behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats Dockerfile as an engineering boundary '
                                        'with explicit behavior and verification, not as a one-off '
                                        'implementation detail.'},
                        {'question': 'Why should base image be handled explicitly in this lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of base image exposes assumptions, '
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
