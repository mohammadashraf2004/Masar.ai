LESSON_ID = 'L010-031'
MODULE_ID = 'M010-03'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-031',
 'module_id': 'M010-03',
 'module_title': 'Async AI Workloads, Concurrency & Background Processing',
 'curriculum_role': 'CORE / PRODUCTION AWARENESS',
 'source': {'source_id': 'BOOK-010',
            'chapter': 5,
            'sections': ['Optimizing Model Inference'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['inference server',
              'latency',
              'throughput',
              'batching',
              'continuous batching',
              'KV cache',
              'GPU utilization'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'visual_reference': [{'chapter': 5,
                       'figure': 'Figure 5-16',
                       'title': 'Dynamic/continuous batching with variable batch size',
                       'filename': 'fig_05_16_continuous_batching.png'}],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'External Inference, Throughput & Request Batching',
 'slug': 'course-010-l010-031-external-inference-throughput-and-request-batching',
 'description': 'Intermediate AI Service Engineering with FastAPI lesson: External Inference, '
                'Throughput & Request Batching.',
 'order': 7,
 'difficulty': 'intermediate',
 'estimated_hours': 1.0,
 'skill_tags': ['ai-service-engineering',
                'async-ai-workloads-concurrency-and-background-processing',
                'inference-server',
                'latency',
                'throughput',
                'batching',
                'continuous-batching'],
 'prerequisite_ids': [],
 'lesson': {'title': 'External Inference, Throughput & Request Batching',
            'content': '# External Inference, Throughput & Request Batching\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **explain why dedicated '
                       'inference servers use scheduling, batching, KV-cache management, and GPU '
                       'execution separately from the FastAPI tier.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**External Inference, Throughput & Request Batching** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **inference server**\n'
                       '- **latency**\n'
                       '- **throughput**\n'
                       '- **batching**\n'
                       '- **continuous batching**\n'
                       '- **KV cache**\n'
                       '- **GPU utilization**\n'
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
                       'For this lesson specifically, watch for mistakes around **inference '
                       'server**, **latency**, and **throughput**. Prefer explicit failure '
                       'behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Draw FastAPI -> inference server flow and compare static versus continuous '
                       'batching under variable request lengths.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 5\n'
                       '- **Sections:** Optimizing Model Inference\n'
                       '- **Curriculum role:** CORE / PRODUCTION AWARENESS\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **External Inference, Throughput & Request Batching** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 60,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: External Inference, Throughput & Request Batching',
                'description': 'Draw FastAPI -> inference server flow and compare static versus '
                               'continuous batching under variable request lengths. Capture the '
                               'acceptance evidence and explain one failure case.',
                'difficulty': 'intermediate',
                'skill_tested': ['inference-server', 'latency', 'throughput']},
               {'title': 'Debug or Decide: External Inference, Throughput & Request Batching',
                'description': 'Start from an intentionally weak design involving inference server '
                               'and latency. Identify the failure boundary, apply the smallest '
                               'justified correction, and add a regression check.',
                'difficulty': 'intermediate',
                'skill_tested': ['inference-server', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'External Inference, Throughput & Request Batching — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for external '
                                     'inference, throughput & request batching?',
                         'options': ['Make inference server explicit, test the boundary, and '
                                     'verify behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats inference server as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should latency be handled explicitly in this lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of latency exposes assumptions, makes '
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
 'project': {'title': None,
             'description': None,
             'difficulty': 'intermediate',
             'tech_stack': [],
             'objectives': [],
             'estimated_hours': None}}
