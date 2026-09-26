LESSON_ID = 'L010-057'
MODULE_ID = 'M010-06'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-057',
 'module_id': 'M010-06',
 'module_title': 'Authentication, Authorization & Secure Service Boundaries',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 9,
            'sections': ['Input Guardrails'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['input guardrail',
              'direct prompt injection',
              'indirect prompt injection',
              'moderation',
              'size limit',
              'authorization boundary'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'visual_reference': [{'chapter': 9,
                       'figure': 'Figure 9-1',
                       'title': 'Comparison of an LLM system without and with guardrails',
                       'filename': 'fig_09_01_io_guardrails.png'}],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Input Guardrails & Prompt-Injection Boundaries',
 'slug': 'course-010-l010-057-input-guardrails-and-prompt-injection-boundaries',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: Input Guardrails & '
                'Prompt-Injection Boundaries.',
 'order': 10,
 'difficulty': 'advanced',
 'estimated_hours': 0.92,
 'skill_tags': ['ai-service-engineering',
                'authentication-authorization-and-secure-service-boundaries',
                'input-guardrail',
                'direct-prompt-injection',
                'indirect-prompt-injection',
                'moderation',
                'size-limit'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Input Guardrails & Prompt-Injection Boundaries',
            'content': '# Input Guardrails & Prompt-Injection Boundaries\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **layer schema, size, '
                       'moderation, injection-aware, authorization, and tool-policy controls '
                       'before privileged AI work occurs.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. **Input '
                       'Guardrails & Prompt-Injection Boundaries** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **input guardrail**\n'
                       '- **direct prompt injection**\n'
                       '- **indirect prompt injection**\n'
                       '- **moderation**\n'
                       '- **size limit**\n'
                       '- **authorization boundary**\n'
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
                       'For this lesson specifically, watch for mistakes around **input '
                       'guardrail**, **direct prompt injection**, and **indirect prompt '
                       'injection**. Prefer explicit failure behavior and regression protection '
                       'over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Defend a request that asks the model to ignore permissions; ensure '
                       'forbidden data is excluded before the prompt/model stage.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 9\n'
                       '- **Sections:** Input Guardrails\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Input Guardrails & Prompt-Injection Boundaries** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Input Guardrails & Prompt-Injection Boundaries',
                'description': 'Defend a request that asks the model to ignore permissions; ensure '
                               'forbidden data is excluded before the prompt/model stage. Capture '
                               'the acceptance evidence and explain one failure case.',
                'difficulty': 'advanced',
                'skill_tested': ['input-guardrail',
                                 'direct-prompt-injection',
                                 'indirect-prompt-injection']},
               {'title': 'Debug or Decide: Input Guardrails & Prompt-Injection Boundaries',
                'description': 'Start from an intentionally weak design involving input guardrail '
                               'and direct prompt injection. Identify the failure boundary, apply '
                               'the smallest justified correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['input-guardrail', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Input Guardrails & Prompt-Injection Boundaries — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for input '
                                     'guardrails & prompt-injection boundaries?',
                         'options': ['Make input guardrail explicit, test the boundary, and verify '
                                     'behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats input guardrail as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should direct prompt injection be handled explicitly in '
                                     'this lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of direct prompt injection exposes '
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
             'difficulty': 'advanced',
             'tech_stack': [],
             'objectives': [],
             'estimated_hours': None}}
