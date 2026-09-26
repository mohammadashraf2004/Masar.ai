LESSON_ID = "L009-014"
MODULE_ID = "M009-03"
LESSON_META = {'course_id': 'COURSE-009',
 'lesson_id': 'L009-014',
 'module_id': 'M009-03',
 'module_title': 'High-Precision Retrieval: Hybrid Search & Reranking',
 'curriculum_role': 'CORE',
 'source': {'source_id': 'BOOK-009',
            'chapter': 3,
            'sections': ['Hybrid search'],
            'page_range': 'SOURCE INFORMATION MISSING'},
 'concepts': ['score normalization',
              'weighted fusion',
              'rank fusion',
              'RRF',
              'calibration',
              'top-k merging'],
 'stable_prerequisites': ['COURSE-005 — Applied LLM Engineering',
                          'COURSE-006 — Production AI Engineering',
                          'COURSE-007 — Advanced LLM Systems & Application Architecture',
                          'COURSE-008 — Vision-Language & Multimodal AI Engineering (specialized '
                          'supporting background)'],
 'visual_reference': None,
 'code_verification': 'Illustrative / syntax-checked where embedded'}

TOPIC = {'title': 'Fusion Strategies for Hybrid Search',
 'slug': 'course-009-l009-014-fusion-strategies-for-hybrid-search',
 'description': 'Advanced Enterprise RAG Engineering lesson: Fusion Strategies for Hybrid Search.',
 'order': 2,
 'difficulty': 'advanced',
 'estimated_hours': 0.92,
 'skill_tags': ['enterprise-rag',
                'high-precision-retrieval-hybrid-search-reranking',
                'score-normalization',
                'weighted-fusion',
                'rank-fusion',
                'rrf'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Fusion Strategies for Hybrid Search',
            'content': '# Fusion Strategies for Hybrid Search\n'
                       '\n'
                       '## Objective\n'
                       '\n'
                       'By the end of this lesson, you should be able to **design, test, or '
                       'diagnose** the production behavior behind fusion strategies for hybrid '
                       'search instead of treating it as a configuration detail.\n'
                       '\n'
                       '## Why this matters\n'
                       '\n'
                       'Enterprise RAG fails when teams optimize one component in isolation and '
                       'assume the rest of the pipeline will compensate. This lesson treats '
                       '**score normalization** as part of a measurable system. The goal is not to '
                       'memorize a vendor API; it is to understand the engineering contract, the '
                       'failure modes, and the evidence needed to decide whether a change improves '
                       'the application.\n'
                       '\n'
                       '## Core concepts\n'
                       '\n'
                       '- **score normalization**\n'
                       '- **weighted fusion**\n'
                       '- **rank fusion**\n'
                       '- **RRF**\n'
                       '- **calibration**\n'
                       '- **top-k merging**\n'
                       '\n'
                       '## System mental model\n'
                       '\n'
                       '```text\n'
                       'User / source\n'
                       '     ↓\n'
                       'High-Precision Retrieval: Hybrid Search & Reranking\n'
                       '     ↓\n'
                       'Measured evidence\n'
                       '     ↓\n'
                       'Decision / next stage\n'
                       '```\n'
                       '\n'
                       'A production implementation should make the boundaries visible: what '
                       'information enters this stage, what transformation occurs, what evidence '
                       'leaves it, and how failures are surfaced. Hidden fallbacks are dangerous '
                       'because they can make an answer look successful while the retrieval path '
                       'is incomplete or degraded.\n'
                       '\n'
                       '## Engineering workflow\n'
                       '\n'
                       '1. **State the requirement.** Convert a vague goal such as "better '
                       'retrieval" or "fewer hallucinations" into a metric, test, or acceptance '
                       'condition.\n'
                       '2. **Build a baseline.** Capture the current behavior before changing '
                       'configuration.\n'
                       '3. **Change one important variable.** Keep enough of the system fixed that '
                       'the result is interpretable.\n'
                       '4. **Inspect traces, not only final answers.** Record retrieved IDs, '
                       'scores, evidence, model calls, latency, and errors where relevant.\n'
                       '5. **Run regression cases.** Include common queries, difficult queries, '
                       'missing-data cases, and adversarial or permission-sensitive cases.\n'
                       '6. **Decide with evidence.** Keep the change only when its quality gain '
                       'justifies its latency, cost, operational, and security impact.\n'
                       '\n'
                       '## Practical implementation pattern\n'
                       '\n'
                       '```python\n'
                       'def reciprocal_rank_fusion(rankings, k=60):\n'
                       '    scores = {}\n'
                       '    for ranking in rankings:\n'
                       '        for rank, doc_id in enumerate(ranking, start=1):\n'
                       '            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)\n'
                       '    return sorted(scores, key=scores.get, reverse=True)\n'
                       '```\n'
                       '\n'
                       'This code is intentionally small: it exposes the *production invariant* '
                       'you need to preserve. In your application, place the same logic behind '
                       'tests, telemetry, and explicit configuration rather than burying it inside '
                       'a notebook.\n'
                       '\n'
                       '## Production checklist\n'
                       '\n'
                       '- Define the observable input and output of the component.\n'
                       '- Record the assumptions that can fail in production.\n'
                       '- Measure quality before and after the change.\n'
                       '- Capture latency, cost, and provenance where the component affects them.\n'
                       '- Prefer reversible changes and regression tests over one-off tuning.\n'
                       '\n'
                       '## Common failure modes\n'
                       '\n'
                       'A frequent mistake is optimizing the visible output while ignoring the '
                       'underlying stage. For example, a fluent final answer can hide missing '
                       'evidence, stale documents, an authorization-filter failure, or a fallback '
                       'to model memory. Another mistake is treating source-era example values as '
                       'universal thresholds. Production thresholds should come from your own '
                       'benchmark, workload, risk profile, and service objectives.\n'
                       '\n'
                       '## Practice\n'
                       '\n'
                       'Take one real or synthetic RAG query and create a trace that shows:\n'
                       '\n'
                       '- the input to this stage;\n'
                       '- the relevant configuration;\n'
                       '- the intermediate evidence;\n'
                       '- the stage latency;\n'
                       '- the final decision;\n'
                       '- one failure case and how your implementation detects it.\n'
                       '\n'
                       'Then change one variable related to **score normalization** and compare '
                       'the result using the same trace format.\n'
                       '\n'
                       '## Source mapping\n'
                       '\n'
                       '- **Source:** BOOK-009\n'
                       '- **Chapter:** 3\n'
                       '- **Sections:** Hybrid search\n'
                       '- **Curriculum role:** CORE\n'
                       '- **Source page range:** SOURCE INFORMATION MISSING\n'
                       '\n'
                       '## Key takeaway\n'
                       '\n'
                       'Treat **Fusion Strategies for Hybrid Search** as an engineering capability '
                       'with measurable inputs, outputs, failure modes, and regression '
                       'protection—not as a one-time configuration choice.\n'
                       '\n',
            'estimated_minutes': 55,
            'has_code_examples': True},
 'exercises': [{'title': 'Trace and Diagnose: Fusion Strategies for Hybrid Search',
                'description': 'Create a compact trace for a RAG query that exposes score '
                               'normalization, weighted fusion, the resulting evidence, and one '
                               'failure. Explain the root cause and the metric you would use to '
                               'verify the fix.',
                'difficulty': 'advanced',
                'skill_tested': ['score-normalization', 'rag-debugging', 'production-evaluation']},
               {'title': 'Controlled Experiment: Score Normalization',
                'description': 'Build a before/after experiment around score normalization. Keep '
                               'the evaluation set fixed, measure quality and latency, and write '
                               'an acceptance decision that states whether the change should ship.',
                'difficulty': 'advanced',
                'skill_tested': ['score-normalization',
                                 'experiment-design',
                                 'regression-testing']}],
 'quiz': {'title': 'Fusion Strategies for Hybrid Search — Knowledge Check',
          'questions': [{'question': 'What is the strongest production approach when working on '
                                     'fusion strategies for hybrid search?',
                         'options': ['Measure score normalization in the context of the end-to-end '
                                     'RAG objective',
                                     'Choose the newest vendor feature without a baseline',
                                     'Judge success only from one fluent answer',
                                     'Remove tracing to reduce implementation complexity'],
                         'correct': 0,
                         'explanation': 'Production decisions should connect score normalization '
                                        'to measurable end-to-end quality, latency, cost, '
                                        'security, or reliability rather than rely on a single '
                                        'demo.'},
                        {'question': 'Why should a RAG change be evaluated against a fixed '
                                     'baseline?',
                         'options': ['To determine whether the change caused a measurable '
                                     'improvement or regression',
                                     'To make every model deterministic',
                                     'To eliminate the need for user feedback',
                                     'To guarantee that all future data has the same distribution'],
                         'correct': 0,
                         'explanation': 'A baseline makes the effect of a change observable and '
                                        'supports regression protection; it does not guarantee '
                                        'determinism or future data stability.'},
                        {'question': 'Which artifact is most useful for debugging a production RAG '
                                     'failure?',
                         'options': ['A trace linking the query, retrieved evidence, '
                                     'configuration, model calls, and final answer',
                                     'Only the final generated answer',
                                     'Only the application homepage',
                                     'A list of model marketing benchmarks'],
                         'correct': 0,
                         'explanation': 'A stage-level trace lets you attribute failures to '
                                        'ingestion, retrieval, ranking, generation, permissions, '
                                        'or other system components.'}],
          'passing_score': 70},
 'project': {'title': None,
             'description': None,
             'difficulty': 'advanced',
             'tech_stack': [],
             'objectives': [],
             'rubric': {},
             'starter_repo_url': None,
             'estimated_hours': None}}
