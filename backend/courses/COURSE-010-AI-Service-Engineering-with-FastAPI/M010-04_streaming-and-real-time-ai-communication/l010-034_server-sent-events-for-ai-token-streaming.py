LESSON_ID = 'L010-034'
MODULE_ID = 'M010-04'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-034',
 'module_id': 'M010-04',
 'module_title': 'Streaming & Real-Time AI Communication',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-010',
            'chapter': 6,
            'sections': ['Server-Sent Events'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['text/event-stream',
              'EventSource',
              'async generator',
              'StreamingResponse',
              'event ID',
              'retry',
              'done event'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture '
                          '(specialized supporting background)',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)',
                          'COURSE-009 — Enterprise RAG Engineering (specialized supporting '
                          'background)'],
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Server-Sent Events for AI Token Streaming',
 'slug': 'course-010-l010-034-server-sent-events-for-ai-token-streaming',
 'description': 'Intermediate AI Service Engineering with FastAPI lesson: Server-Sent Events for '
                'AI Token Streaming.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['ai-service-engineering',
                'streaming-and-real-time-ai-communication',
                'text-event-stream',
                'eventsource',
                'async-generator',
                'streamingresponse',
                'event-id'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Server-Sent Events for AI Token Streaming',
            'content': '# Server-Sent Events for AI Token Streaming\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **stream incremental '
                       'model output over a server-to-client event stream with explicit event '
                       'types and completion semantics.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Server-Sent Events for AI Token Streaming** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **text/event-stream**\n'
                       '- **EventSource**\n'
                       '- **async generator**\n'
                       '- **StreamingResponse**\n'
                       '- **event ID**\n'
                       '- **retry**\n'
                       '- **done event**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'Provider event stream → streaming service → SSE/WebSocket adapter → '
                       'connected client\n'
                       '```\n'
                       '\n'
                       'Use the mental model to identify what enters the component, what '
                       'responsibility it owns, what it must not own, and what evidence you need '
                       'when it fails.\n'
                       '\n'
                       '{{figure:sse}}\n'
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
                       'from collections.abc import AsyncIterator\n'
                       '\n'
                       'async def stream_events() -> AsyncIterator[dict[str, str]]:\n'
                       '    for token in ["Fast", "API", " streaming"]:\n'
                       '        yield {"type": "token", "text": token}\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'A live connection can outlive requests, fail halfway, or slow down; '
                       'cleanup and cancellation are part of correctness.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around '
                       '**text/event-stream**, **EventSource**, and **async generator**. Prefer '
                       'explicit failure behavior and regression protection over hidden '
                       'fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Implement a provider-independent token generator and expose it as an SSE '
                       'endpoint with token, usage, and done events.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 6\n'
                       '- **Sections:** Server-Sent Events\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Server-Sent Events for AI Token Streaming** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 50,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Server-Sent Events for AI Token Streaming',
                'description': 'Implement a provider-independent token generator and expose it as '
                               'an SSE endpoint with token, usage, and done events. Capture the '
                               'acceptance evidence and explain one failure case.',
                'difficulty': 'intermediate',
                'skill_tested': ['text-event-stream', 'eventsource', 'async-generator']},
               {'title': 'Debug or Decide: Server-Sent Events for AI Token Streaming',
                'description': 'Start from an intentionally weak design involving '
                               'text/event-stream and EventSource. Identify the failure boundary, '
                               'apply the smallest justified correction, and add a regression '
                               'check.',
                'difficulty': 'intermediate',
                'skill_tested': ['text-event-stream', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Server-Sent Events for AI Token Streaming — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for server-sent '
                                     'events for ai token streaming?',
                         'options': ['Make text/event-stream explicit, test the boundary, and '
                                     'verify behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats text/event-stream as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should EventSource be handled explicitly in this lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of EventSource exposes assumptions, '
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
