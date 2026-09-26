LESSON_ID = 'L010-042'
MODULE_ID = 'M010-05'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-042',
 'module_id': 'M010-05',
 'module_title': 'Persistence & Database Engineering for AI Services',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 7,
            'sections': ['Database Models', 'Pydantic Schemas'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['Mapped',
              'mapped_column',
              'primary key',
              'foreign key',
              'relationship',
              'index',
              'ORM entity',
              'API schema'],
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

TOPIC = {'title': 'ORM Entities, Relationships & API Schemas',
 'slug': 'course-010-l010-042-orm-entities-relationships-and-api-schemas',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: ORM Entities, Relationships '
                '& API Schemas.',
 'order': 3,
 'difficulty': 'advanced',
 'estimated_hours': 0.92,
 'skill_tags': ['ai-service-engineering',
                'persistence-and-database-engineering-for-ai-services',
                'mapped',
                'mapped-column',
                'primary-key',
                'foreign-key',
                'relationship'],
 'prerequisite_ids': [],
 'lesson': {'title': 'ORM Entities, Relationships & API Schemas',
            'content': '# ORM Entities, Relationships & API Schemas\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **model persistent '
                       'entities and relationships while keeping ORM mappings separate from public '
                       'Pydantic API schemas.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. **ORM '
                       'Entities, Relationships & API Schemas** gives you a concrete engineering '
                       'technique for making one of those boundaries explicit, testable, and '
                       'observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **Mapped**\n'
                       '- **mapped_column**\n'
                       '- **primary key**\n'
                       '- **foreign key**\n'
                       '- **relationship**\n'
                       '- **index**\n'
                       '- **ORM entity**\n'
                       '- **API schema**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'Router → service → repository → database, with explicit transactions and '
                       'durable state\n'
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
                       'async def create_conversation(service, payload):\n'
                       '    conversation = await service.create(payload)\n'
                       '    return {"id": str(conversation.id), "title": conversation.title}\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'Request-scoped sessions, migrations, and transaction ownership must be '
                       'explicit or data will become inconsistent and hard to recover.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around **Mapped**, '
                       '**mapped_column**, and **primary key**. Prefer explicit failure behavior '
                       'and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Design Conversation and Message entities plus separate '
                       'create/update/response schemas and explain why database schema != API '
                       'schema.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 7\n'
                       '- **Sections:** Database Models, Pydantic Schemas\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **ORM Entities, Relationships & API Schemas** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: ORM Entities, Relationships & API Schemas',
                'description': 'Design Conversation and Message entities plus separate '
                               'create/update/response schemas and explain why database schema != '
                               'API schema. Capture the acceptance evidence and explain one '
                               'failure case.',
                'difficulty': 'advanced',
                'skill_tested': ['mapped', 'mapped-column', 'primary-key']},
               {'title': 'Debug or Decide: ORM Entities, Relationships & API Schemas',
                'description': 'Start from an intentionally weak design involving Mapped and '
                               'mapped_column. Identify the failure boundary, apply the smallest '
                               'justified correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['mapped', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'ORM Entities, Relationships & API Schemas — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for orm entities, '
                                     'relationships & api schemas?',
                         'options': ['Make Mapped explicit, test the boundary, and verify behavior '
                                     'with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats Mapped as an engineering boundary with '
                                        'explicit behavior and verification, not as a one-off '
                                        'implementation detail.'},
                        {'question': 'Why should mapped_column be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of mapped_column exposes assumptions, '
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
