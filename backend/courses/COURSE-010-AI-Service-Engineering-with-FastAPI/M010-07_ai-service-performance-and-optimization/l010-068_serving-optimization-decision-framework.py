LESSON_ID = 'L010-068'
MODULE_ID = 'M010-07'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-068',
 'module_id': 'M010-07',
 'module_title': 'AI Service Performance & Optimization',
 'curriculum_role': 'CORE + REVISION SYNTHESIS',
 'source': {'source_id': 'BOOK-010',
            'chapter': 10,
            'sections': ['Performance Optimization', 'Quantization', 'Fine-Tuning'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['optimization ladder',
              'model choice',
              'context reduction',
              'caching',
              'batching',
              'quantization awareness',
              'fine-tuning boundary'],
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

TOPIC = {'title': 'Serving Optimization Decision Framework',
 'slug': 'course-010-l010-068-serving-optimization-decision-framework',
 'description': 'Advanced AI Service Engineering with FastAPI lesson: Serving Optimization '
                'Decision Framework.',
 'order': 7,
 'difficulty': 'advanced',
 'estimated_hours': 0.75,
 'skill_tags': ['ai-service-engineering',
                'ai-service-performance-and-optimization',
                'optimization-ladder',
                'model-choice',
                'context-reduction',
                'caching',
                'batching'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Serving Optimization Decision Framework',
            'content': '# Serving Optimization Decision Framework\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **choose service-, '
                       'serving-, or model-level optimizations only after evidence shows they '
                       'address the actual bottleneck.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Serving Optimization Decision Framework** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **optimization ladder**\n'
                       '- **model choice**\n'
                       '- **context reduction**\n'
                       '- **caching**\n'
                       '- **batching**\n'
                       '- **quantization awareness**\n'
                       '- **fine-tuning boundary**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'Measure → identify bottleneck → apply least-invasive optimization → '
                       'benchmark again\n'
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
                       'def cache_key(*, tenant: str, model: str, prompt_version: str, '
                       'request_hash: str) -> str:\n'
                       '    return f"{tenant}:{model}:{prompt_version}:{request_hash}"\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'Optimization that improves one metric while violating correctness, '
                       'privacy, or quality is a regression, not a win.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around **optimization '
                       'ladder**, **model choice**, and **context reduction**. Prefer explicit '
                       'failure behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Given three benchmark profiles, choose the least invasive optimization '
                       'that meets latency/cost/quality targets and justify why deeper model '
                       'changes are or are not needed.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 10\n'
                       '- **Sections:** Performance Optimization, Quantization, Fine-Tuning\n'
                       '- **Curriculum role:** CORE + REVISION SYNTHESIS\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Serving Optimization Decision Framework** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 45,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Serving Optimization Decision Framework',
                'description': 'Given three benchmark profiles, choose the least invasive '
                               'optimization that meets latency/cost/quality targets and justify '
                               'why deeper model changes are or are not needed. Capture the '
                               'acceptance evidence and explain one failure case.',
                'difficulty': 'advanced',
                'skill_tested': ['optimization-ladder', 'model-choice', 'context-reduction']},
               {'title': 'Debug or Decide: Serving Optimization Decision Framework',
                'description': 'Start from an intentionally weak design involving optimization '
                               'ladder and model choice. Identify the failure boundary, apply the '
                               'smallest justified correction, and add a regression check.',
                'difficulty': 'advanced',
                'skill_tested': ['optimization-ladder', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Serving Optimization Decision Framework — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for serving '
                                     'optimization decision framework?',
                         'options': ['Make optimization ladder explicit, test the boundary, and '
                                     'verify behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats optimization ladder as an engineering '
                                        'boundary with explicit behavior and verification, not as '
                                        'a one-off implementation detail.'},
                        {'question': 'Why should model choice be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of model choice exposes assumptions, '
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
 'project': {'title': 'Performance & Cost Optimization Lab',
             'description': 'Benchmark the service and apply batching, cache strategies, context '
                            'reuse, and structured outputs without breaking correctness.',
             'objectives': ['Establish baseline metrics',
                            'Implement safe caching',
                            'Move bulk work offline',
                            'Prove optimization with before/after evidence'],
             'tech_stack': ['Python',
                            'Redis',
                            'vector cache optional',
                            'provider batch/context cache'],
             'estimated_hours': 6}}
