LESSON_ID = 'L010-001'
MODULE_ID = 'M010-01'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-001',
 'module_id': 'M010-01',
 'module_title': 'AI Service Architecture & FastAPI Foundations',
 'curriculum_role': 'REVISION + CORE FRAMING',
 'source': {'source_id': 'BOOK-010',
            'chapter': 1,
            'sections': ['Introduction'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['model vs service',
              'API wrapper',
              'service layer',
              'external systems',
              'validation',
              'routing'],
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

TOPIC = {'title': 'From Generative Models to AI Services',
 'slug': 'course-010-l010-001-from-generative-models-to-ai-services',
 'description': 'Intermediate AI Service Engineering with FastAPI lesson: From Generative Models '
                'to AI Services.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.5,
 'skill_tags': ['ai-service-engineering',
                'ai-service-architecture-and-fastapi-foundations',
                'model-vs-service',
                'api-wrapper',
                'service-layer',
                'external-systems',
                'validation'],
 'prerequisite_ids': [],
 'lesson': {'title': 'From Generative Models to AI Services',
            'content': '# From Generative Models to AI Services\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **explain how a '
                       'generative model becomes a controlled service that clients and other '
                       'systems can safely consume.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. **From '
                       'Generative Models to AI Services** gives you a concrete engineering '
                       'technique for making one of those boundaries explicit, testable, and '
                       'observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **model vs service**\n'
                       '- **API wrapper**\n'
                       '- **service layer**\n'
                       '- **external systems**\n'
                       '- **validation**\n'
                       '- **routing**\n'
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
                       'For this lesson specifically, watch for mistakes around **model vs '
                       'service**, **API wrapper**, and **service layer**. Prefer explicit failure '
                       'behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Draw the boundary between a model, the application service, clients, '
                       'databases, tools, and external APIs for one realistic AI product.\n'
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
                       '- **Curriculum role:** REVISION + CORE FRAMING\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **From Generative Models to AI Services** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 30,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: From Generative Models to AI Services',
                'description': 'Draw the boundary between a model, the application service, '
                               'clients, databases, tools, and external APIs for one realistic AI '
                               'product. Capture the acceptance evidence and explain one failure '
                               'case.',
                'difficulty': 'intermediate',
                'skill_tested': ['model-vs-service', 'api-wrapper', 'service-layer']},
               {'title': 'Debug or Decide: From Generative Models to AI Services',
                'description': 'Start from an intentionally weak design involving model vs service '
                               'and API wrapper. Identify the failure boundary, apply the smallest '
                               'justified correction, and add a regression check.',
                'difficulty': 'intermediate',
                'skill_tested': ['model-vs-service', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'From Generative Models to AI Services — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for from '
                                     'generative models to ai services?',
                         'options': ['Make model vs service explicit, test the boundary, and '
                                     'verify behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats model vs service as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should API wrapper be handled explicitly in this lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of API wrapper exposes assumptions, '
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
