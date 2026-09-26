LESSON_ID = 'L010-025'
MODULE_ID = 'M010-03'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-025',
 'module_id': 'M010-03',
 'module_title': 'Async AI Workloads, Concurrency & Background Processing',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 5,
            'sections': ['Blocking Operations'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['blocking operation',
              'I/O-bound',
              'CPU-bound',
              'GPU-bound',
              'memory-bound',
              'workload classification'],
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

TOPIC = {'title': 'Blocking Workloads in AI Services',
 'slug': 'course-010-l010-025-blocking-workloads-in-ai-services',
 'description': 'Intermediate AI Service Engineering with FastAPI lesson: Blocking Workloads in AI '
                'Services.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['ai-service-engineering',
                'async-ai-workloads-concurrency-and-background-processing',
                'blocking-operation',
                'i-o-bound',
                'cpu-bound',
                'gpu-bound',
                'memory-bound'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Blocking Workloads in AI Services',
            'content': '# Blocking Workloads in AI Services\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **classify AI-service '
                       'work as I/O-, CPU-, GPU-, memory-bound, or long-running before choosing a '
                       'concurrency strategy.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Blocking Workloads in AI Services** gives you a concrete engineering '
                       'technique for making one of those boundaries explicit, testable, and '
                       'observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **blocking operation**\n'
                       '- **I/O-bound**\n'
                       '- **CPU-bound**\n'
                       '- **GPU-bound**\n'
                       '- **memory-bound**\n'
                       '- **workload classification**\n'
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
                       'For this lesson specifically, watch for mistakes around **blocking '
                       'operation**, **I/O-bound**, and **CPU-bound**. Prefer explicit failure '
                       'behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Classify database, HTTP, tokenization, embedding, local LLM, and '
                       'image-generation operations and defend the execution strategy for each.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 5\n'
                       '- **Sections:** Blocking Operations\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Blocking Workloads in AI Services** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Blocking Workloads in AI Services',
                'description': 'Classify database, HTTP, tokenization, embedding, local LLM, and '
                               'image-generation operations and defend the execution strategy for '
                               'each. Capture the acceptance evidence and explain one failure '
                               'case.',
                'difficulty': 'intermediate',
                'skill_tested': ['blocking-operation', 'i-o-bound', 'cpu-bound']},
               {'title': 'Debug or Decide: Blocking Workloads in AI Services',
                'description': 'Start from an intentionally weak design involving blocking '
                               'operation and I/O-bound. Identify the failure boundary, apply the '
                               'smallest justified correction, and add a regression check.',
                'difficulty': 'intermediate',
                'skill_tested': ['blocking-operation', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Blocking Workloads in AI Services — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for blocking '
                                     'workloads in ai services?',
                         'options': ['Make blocking operation explicit, test the boundary, and '
                                     'verify behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats blocking operation as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should I/O-bound be handled explicitly in this lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of I/O-bound exposes assumptions, '
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
