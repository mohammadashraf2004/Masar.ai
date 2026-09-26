LESSON_ID = 'L010-002'
MODULE_ID = 'M010-01'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-002',
 'module_id': 'M010-01',
 'module_title': 'AI Service Architecture & FastAPI Foundations',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 1,
            'sections': ['Introduction'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['service boundary',
              'control layer',
              'provider boundary',
              'database boundary',
              'tool boundary',
              'response validation'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'visual_reference': [{'chapter': 1,
                       'figure': 'Figure 1-4',
                       'title': 'FastAPI web server with data source integrations that serve a '
                                'generative model',
                       'filename': 'fig_01_04_ai_service_architecture.png'}],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Designing the AI Service Boundary',
 'slug': 'course-010-l010-002-designing-the-ai-service-boundary',
 'description': 'Intermediate AI Service Engineering with FastAPI lesson: Designing the AI Service '
                'Boundary.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['ai-service-engineering',
                'ai-service-architecture-and-fastapi-foundations',
                'service-boundary',
                'control-layer',
                'provider-boundary',
                'database-boundary',
                'tool-boundary'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Designing the AI Service Boundary',
            'content': '# Designing the AI Service Boundary\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **design an AI service '
                       'boundary that isolates model/provider details from transport, business '
                       'logic, data access, and policy enforcement.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Designing the AI Service Boundary** gives you a concrete engineering '
                       'technique for making one of those boundaries explicit, testable, and '
                       'observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **service boundary**\n'
                       '- **control layer**\n'
                       '- **provider boundary**\n'
                       '- **database boundary**\n'
                       '- **tool boundary**\n'
                       '- **response validation**\n'
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
                       'For this lesson specifically, watch for mistakes around **service '
                       'boundary**, **control layer**, and **provider boundary**. Prefer explicit '
                       'failure behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Refactor a monolithic AI request flow into explicit client, API, service, '
                       'provider, data, and validation boundaries.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 1\n'
                       '- **Sections:** Introduction\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Designing the AI Service Boundary** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Designing the AI Service Boundary',
                'description': 'Refactor a monolithic AI request flow into explicit client, API, '
                               'service, provider, data, and validation boundaries. Capture the '
                               'acceptance evidence and explain one failure case.',
                'difficulty': 'intermediate',
                'skill_tested': ['service-boundary', 'control-layer', 'provider-boundary']},
               {'title': 'Debug or Decide: Designing the AI Service Boundary',
                'description': 'Start from an intentionally weak design involving service boundary '
                               'and control layer. Identify the failure boundary, apply the '
                               'smallest justified correction, and add a regression check.',
                'difficulty': 'intermediate',
                'skill_tested': ['service-boundary', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Designing the AI Service Boundary — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for designing the '
                                     'ai service boundary?',
                         'options': ['Make service boundary explicit, test the boundary, and '
                                     'verify behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats service boundary as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should control layer be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of control layer exposes assumptions, '
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
