LESSON_ID = 'L010-024'
MODULE_ID = 'M010-02'
LESSON_META = {'course_id': 'COURSE-010',
 'lesson_id': 'L010-024',
 'module_id': 'M010-02',
 'module_title': 'Model Integration, Lifecycle & Type-Safe API Contracts',
 'curriculum_role': 'CORE + MASAR ADDITION',
 'source': {'source_id': 'BOOK-010',
            'chapter': 4,
            'sections': ['Type-Safe AI Services'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['adapter',
              'schema evolution',
              'backward compatibility',
              'provider normalization',
              'contract test',
              'change safety'],
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

TOPIC = {'title': 'Contract Evolution & Schema-Change Safety',
 'slug': 'course-010-l010-024-contract-evolution-and-schema-change-safety',
 'description': 'Intermediate AI Service Engineering with FastAPI lesson: Contract Evolution & '
                'Schema-Change Safety.',
 'order': 14,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['ai-service-engineering',
                'model-integration-lifecycle-and-type-safe-api-contracts',
                'adapter',
                'schema-evolution',
                'backward-compatibility',
                'provider-normalization',
                'contract-test'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Contract Evolution & Schema-Change Safety',
            'content': '# Contract Evolution & Schema-Change Safety\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **evolve provider and '
                       'internal schemas while preserving the public API and catching breaking '
                       'changes through types and tests.**\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'AI services fail at boundaries: between HTTP and business logic, '
                       'asynchronous and blocking work, identity and policy, model output and '
                       'downstream execution, or local development and production runtime. '
                       '**Contract Evolution & Schema-Change Safety** gives you a concrete '
                       'engineering technique for making one of those boundaries explicit, '
                       'testable, and observable.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **adapter**\n'
                       '- **schema evolution**\n'
                       '- **backward compatibility**\n'
                       '- **provider normalization**\n'
                       '- **contract test**\n'
                       '- **change safety**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'HTTP contract → validation → service → provider/resource lifecycle → '
                       'normalized response\n'
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
                       'from typing import Protocol\n'
                       'from pydantic import BaseModel\n'
                       '\n'
                       'class GenerationRequest(BaseModel):\n'
                       '    prompt: str\n'
                       '\n'
                       'class ModelProvider(Protocol):\n'
                       '    async def generate(self, request: GenerationRequest) -> str: ...\n'
                       '```\n'
                       '\n'
                       'The snippet is intentionally small. The course capstone grows the same '
                       'boundary through later modules rather than replacing it with unrelated '
                       'demos.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'Leaking provider-specific payloads or loading expensive resources inside '
                       'requests makes contracts unstable and latency unpredictable.\n'
                       '\n'
                       'For this lesson specifically, watch for mistakes around **adapter**, '
                       '**schema evolution**, and **backward compatibility**. Prefer explicit '
                       'failure behavior and regression protection over hidden fallbacks.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Adapt a changed provider payload to the stable internal/public contract '
                       'and add a regression test proving the API response did not change.\n'
                       '\n'
                       'Record both the successful path and one intentionally broken case. Explain '
                       'what signal—test result, status code, trace, database row, metric, or '
                       'deployment check—proves that your fix works.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI*\n'
                       '- **Chapter:** 4\n'
                       '- **Sections:** Type-Safe AI Services\n'
                       '- **Curriculum role:** CORE + MASAR ADDITION\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Contract Evolution & Schema-Change Safety** as a reusable '
                       'service-engineering capability. The exact provider, framework version, '
                       'model, database, or hosting platform can change; the boundary, failure '
                       'mode, and evidence-driven workflow should remain understandable.\n',
            'estimated_minutes': 40,
            'has_code_examples': True},
 'exercises': [{'title': 'Build and Verify: Contract Evolution & Schema-Change Safety',
                'description': 'Adapt a changed provider payload to the stable internal/public '
                               'contract and add a regression test proving the API response did '
                               'not change. Capture the acceptance evidence and explain one '
                               'failure case.',
                'difficulty': 'intermediate',
                'skill_tested': ['adapter', 'schema-evolution', 'backward-compatibility']},
               {'title': 'Debug or Decide: Contract Evolution & Schema-Change Safety',
                'description': 'Start from an intentionally weak design involving adapter and '
                               'schema evolution. Identify the failure boundary, apply the '
                               'smallest justified correction, and add a regression check.',
                'difficulty': 'intermediate',
                'skill_tested': ['adapter', 'debugging', 'regression-testing']}],
 'quiz': {'title': 'Contract Evolution & Schema-Change Safety — Knowledge Check',
          'questions': [{'question': 'What is the strongest engineering approach for contract '
                                     'evolution & schema-change safety?',
                         'options': ['Make adapter explicit, test the boundary, and verify '
                                     'behavior with evidence',
                                     'Choose the newest library feature without defining a '
                                     'contract',
                                     'Put all logic directly in the HTTP route for simplicity',
                                     'Judge success only from one successful manual demo'],
                         'correct': 0,
                         'explanation': 'The lesson treats adapter as an engineering boundary with '
                                        'explicit behavior and verification, not as a one-off '
                                        'implementation detail.'},
                        {'question': 'Why should schema evolution be handled explicitly in this '
                                     'lesson?',
                         'options': ['Because hidden assumptions become production failure modes '
                                     'and make changes harder to test',
                                     'Because it guarantees every provider and deployment '
                                     'environment behaves identically',
                                     'Because it removes the need for monitoring and regression '
                                     'tests',
                                     'Because it makes all AI model outputs deterministic'],
                         'correct': 0,
                         'explanation': 'Explicit treatment of schema evolution exposes '
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
 'project': {'title': 'Pluggable Typed AI Model Gateway',
             'description': 'Build a provider-neutral AI gateway with lifespan-managed resources, '
                            'typed contracts, media responses, settings, and monitoring '
                            'middleware.',
             'objectives': ['Swap providers without changing routes',
                            'Validate requests/responses',
                            'Manage model lifecycle',
                            'Record safe request telemetry'],
             'tech_stack': ['FastAPI', 'Pydantic v2', 'provider adapter', 'pytest'],
             'estimated_hours': 7}}
