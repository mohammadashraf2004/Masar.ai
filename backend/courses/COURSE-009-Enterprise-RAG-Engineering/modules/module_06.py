"""M01.L06 — Evaluating Your RAG Application.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 6, pages not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L06"
MODULE_ORDER = 1
MODULE_TITLE = "RAG Foundations"
MODULE_DESCRIPTION = (
    "Build, evaluate, and operate RAG systems by measuring ingestion quality, retrieval relevance, "
    "generation faithfulness, user outcomes, safety, latency, reliability, and cost."
)
SOURCE_CHAPTER = 6
SOURCE_PAGES = "Not provided in supplied source"


TOPIC = {'title': 'Evaluating Your RAG Application',
 'slug': 'rag-foundations-m01-l06',
 'description': 'A study-ready guide to diagnosing RAG failures and evaluating ingestion, '
                'retrieval, generation, user outcomes, safety, and production system health.',
 'order': 6,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 10.5,
 'skill_tags': ['rag',
                'rag-evaluation',
                'retrieval-evaluation',
                'generation-evaluation',
                'llm-as-a-judge',
                'precision',
                'recall',
                'f1',
                'mrr',
                'map',
                'ndcg',
                'umbrela',
                'autonuggetizer',
                'faithfulness',
                'citations',
                'human-feedback',
                'offline-evaluation',
                'online-evaluation',
                'mlops',
                'observability',
                ],
 'prerequisite_ids': ['M01.L01', 'M01.L02', 'M01.L03', 'M01.L04', 'M01.L05'],
 'lesson': {'title': 'Evaluating Your RAG Application',
            'content': '# Evaluating Your RAG Application\n'
                       '\n'
                       '> **Course:** Retrieval-Augmented Generation (RAG)  \n'
                       '> **Lesson:** M01.L06  \n'
                       '> **Module:** RAG Foundations  \n'
                       '> **Source alignment:** Supplied source, Chapter 6. Page numbers were not '
                       'provided. This lesson is an instructor-authored study adaptation rather '
                       'than a reproduction of the source text.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Learning outcomes\n'
                       '\n'
                       'By the end of this lesson, you should be able to:\n'
                       '\n'
                       '- Separate **offline** evaluation from **online** evaluation and explain '
                       'when each is useful.\n'
                       '- Diagnose failures in ingestion, retrieval, and generation instead of '
                       'treating RAG quality as one number.\n'
                       '- Explain precision@k, recall@k, F1@k, MRR, MAP, and nDCG and choose among '
                       'them deliberately.\n'
                       '- Explain what golden chunks and golden answers are, why they are '
                       'expensive to maintain, and when reference-free evaluation helps.\n'
                       '- Use the LLM-as-a-judge pattern while accounting for model bias, '
                       'instability, cost, and latency.\n'
                       '- Explain UMBRELA and AutoNuggetizer as reference-free evaluation '
                       'approaches.\n'
                       '- Evaluate generation with context utilization, answer similarity, answer '
                       'relevance, faithfulness, citation accuracy, and response consistency.\n'
                       '- Add safety, bias, and red-team checks to a RAG evaluation program.\n'
                       '- Compare Open RAG Eval, Ragas, DeepEval, and managed evaluation '
                       'approaches conceptually.\n'
                       '- Use explicit user feedback as a first-class quality signal.\n'
                       '- Design CI/CD evaluation gates that prevent quality regression when RAG '
                       'components change.\n'
                       '- Build online evaluation with asynchronous judging, sampling, A/B '
                       'testing, and feedback loops.\n'
                       '- Treat latency, throughput, uptime, error rate, cost, CPU, GPU, and '
                       'memory as part of RAG quality.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 1. Why RAG evaluation is a system requirement\n'
                       '\n'
                       'A RAG application can appear impressive during a demo and still fail badly '
                       'in production. The reason is that RAG quality is produced by a '
                       '**pipeline**. The final answer depends on the quality of the source data, '
                       'ingestion, retrieval, ranking, prompting, generation, and the surrounding '
                       'production system. A single impressive answer tells you almost nothing '
                       'about whether the system is reliable.\n'
                       '\n'
                       'RAG evaluation is therefore the discipline of **measuring where the system '
                       'succeeds and where it fails**. At minimum, you want to answer two '
                       'questions:\n'
                       '\n'
                       '1. **Retrieval quality:** Did the system find the chunks that actually '
                       'contain the information needed for this query?\n'
                       '2. **Generation quality:** Given the retrieved evidence, did the LLM '
                       'produce a useful answer that is faithful, complete, and relevant?\n'
                       '\n'
                       'Production teams should go further and include system behavior such as '
                       'latency, uptime, throughput, and cost. A RAG application that is highly '
                       'accurate but takes thirty seconds for every request is still a poor '
                       'production system. Likewise, a fast system that regularly retrieves the '
                       'wrong evidence is not useful.\n'
                       '\n'
                       'The most useful mental model is **evaluation as diagnosis**, not '
                       'evaluation as a leaderboard. A metric is valuable when it tells you *which '
                       'component to improve next*.\n'
                       '\n'
                       '[[IMAGE_NEEDED: RAG evaluation layers | Show ingestion → retrieval → '
                       'generation → user/system outcomes with metrics attached to each layer | '
                       'Notice that final answer quality is downstream of multiple independently '
                       'measurable stages]]\n'
                       '\n'
                       '## 2. Offline evaluation versus online evaluation\n'
                       '\n'
                       'The chapter distinguishes two evaluation modes.\n'
                       '\n'
                       '**Offline evaluation** happens during development or before release. You '
                       'control the test queries, system configuration, and usually the evaluation '
                       'dataset. Because it is not on the critical user path, offline evaluation '
                       'can be expensive and slow. This is where you can run large benchmark sets, '
                       'compare several embedding models, change chunking strategies, test '
                       'rerankers, or invoke expensive LLM judges repeatedly.\n'
                       '\n'
                       '**Online evaluation** observes the live system. Its advantage is realism: '
                       'the queries come from actual users rather than from a hand-designed '
                       'benchmark. Its challenge is that live evaluation must not make the user '
                       'experience unacceptably slow or expensive.\n'
                       '\n'
                       'A mature system needs both. Offline evaluation is the main **tuning '
                       'engine**; online evaluation is the main **early-warning system**.\n'
                       '\n'
                       '```text\n'
                       'Development change\n'
                       '     ↓\n'
                       'offline benchmark\n'
                       '     ↓\n'
                       'evaluation gate\n'
                       '     ↓\n'
                       'production\n'
                       '     ↓\n'
                       'online telemetry + sampled evaluation + human feedback\n'
                       '     ↓\n'
                       'new failure cases promoted into offline benchmark\n'
                       '```\n'
                       '\n'
                       'This cycle is one of the most important ideas in the lesson: evaluation '
                       'should become a continuous process, not a one-time activity performed '
                       'before launch.\n'
                       '\n'
                       '## 3. Evaluate the pipeline, not only the final answer\n'
                       '\n'
                       'Suppose a user receives a wrong answer. There are several very different '
                       'explanations:\n'
                       '\n'
                       '- The required information was never ingested.\n'
                       '- The data exists, but parsing destroyed its structure.\n'
                       '- The retriever missed the right chunk.\n'
                       '- The retriever found the right chunk but also returned too much noise.\n'
                       '- The generator ignored an important retrieved chunk.\n'
                       '- The generator fabricated a claim that is unsupported by the context.\n'
                       '- The answer is faithful but does not actually address the user’s intent.\n'
                       '- The system is correct but too slow or unavailable.\n'
                       '\n'
                       'These failures require different fixes. Prompt engineering cannot repair '
                       'missing documents. A stronger LLM cannot recover a chunk the retriever '
                       'never supplied. Increasing `top_k` may improve recall but also inject more '
                       'irrelevant context.\n'
                       '\n'
                       'For that reason, do not build a dashboard with only one “RAG score.” Keep '
                       'stage-specific metrics so that a quality change can be localized. This is '
                       'the foundation for scientific tuning.\n'
                       '\n'
                       '{{exercise:M01.L06.EX01}}\n'
                       '\n'
                       '## 4. Retrieval failure: low recall\n'
                       '\n'
                       '**Low recall** means useful information exists in the indexed corpus, but '
                       'the retrieval stage fails to return it within the candidate set used '
                       'downstream.\n'
                       '\n'
                       'There are two common forms:\n'
                       '\n'
                       '- **Complete miss:** none of the required evidence is retrieved.\n'
                       '- **Partial miss:** some evidence appears, but other facts required for a '
                       'complete answer are absent.\n'
                       '\n'
                       'The second case is particularly dangerous because the answer may look '
                       'plausible. Consider a question asking for both a final approval step and a '
                       'filing deadline. If retrieval returns only the approval chunk, the '
                       'generator may answer the first half correctly and fail on the deadline.\n'
                       '\n'
                       'The chapter emphasizes a practical priority: **optimize retrieval before '
                       'trying to rescue the system through generation**. If relevant evidence is '
                       'rarely retrieved, no prompt can reliably compensate for it.\n'
                       '\n'
                       'Typical levers for recall include the retrieval method, `k`, hybrid '
                       'search, reranking candidate depth, query formulation, metadata filters, '
                       'and the quality of the indexed representation.\n'
                       '\n'
                       '{{exercise:M01.L06.EX02}}\n'
                       '\n'
                       '## 5. Retrieval failure: low precision\n'
                       '\n'
                       '**Low precision** means the retriever returns too much irrelevant '
                       'material. The system may still retrieve the correct chunk, but it '
                       'surrounds that evidence with distracting or misleading chunks.\n'
                       '\n'
                       'Noise matters for two reasons. First, irrelevant chunks consume the '
                       'context budget. Second, they can influence the generator, especially if '
                       'they contain vocabulary that looks related to the query.\n'
                       '\n'
                       'For example, a query about a project launch approval process should not '
                       'receive a chunk about a post-launch celebration just because both contain '
                       'the words “project” and “launch.” Keyword overlap alone is not enough to '
                       'establish relevance.\n'
                       '\n'
                       'Low precision can often be improved with stronger first-stage retrieval, '
                       'metadata filtering, hybrid retrieval, or a reranker. But remember the '
                       'precision–recall tension: aggressively filtering noise can accidentally '
                       'remove relevant evidence. Evaluation exists to measure that trade-off '
                       'instead of guessing.\n'
                       '\n'
                       '## 6. Some retrieval failures are architectural\n'
                       '\n'
                       'Standard top-k RAG works best when the needed answer can be located in one '
                       'or a few passages that are semantically similar to the query. Some '
                       'questions violate that assumption.\n'
                       '\n'
                       'A **multi-hop** question may require retrieving one fact, using it to '
                       'identify a second entity, then retrieving another fact. A **sensemaking** '
                       'question may require combining evidence across many documents to summarize '
                       'a collective pattern.\n'
                       '\n'
                       'If evaluation shows that ordinary semantic or hybrid retrieval repeatedly '
                       'fails on these classes of queries, the problem may not be a bad threshold '
                       'or a weak prompt. The retrieval architecture itself may be insufficient. '
                       'The chapter points forward to agentic RAG and knowledge graphs as '
                       'approaches better suited to these tasks.\n'
                       '\n'
                       'This is an important diagnostic lesson: do not endlessly tune a component '
                       'when the evaluation evidence says the underlying method does not fit the '
                       'query class.\n'
                       '\n'
                       '## 7. Generation can fail even with good retrieval\n'
                       '\n'
                       'Once retrieval succeeds, the generator still has several responsibilities: '
                       'it must respect the evidence, use the important evidence, and answer the '
                       'actual user request.\n'
                       '\n'
                       'The chapter highlights three major generation failures:\n'
                       '\n'
                       '1. **Faithfulness failure** — the answer contains claims not supported by '
                       'the retrieved context or contradicts it.\n'
                       '2. **Context-utilization failure** — the relevant evidence was supplied, '
                       'but the model failed to use all important pieces.\n'
                       '3. **Answer-relevance failure** — the answer is grounded and perhaps '
                       'complete, but does not resolve the user’s actual question.\n'
                       '\n'
                       'These distinctions matter because a single similarity score between a '
                       'generated answer and a reference answer cannot explain all three. Good '
                       'generation evaluation therefore needs several complementary metrics.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Generation failure map | Show retrieved context feeding an '
                       'LLM, with branches for hallucination, ignored evidence, and off-target '
                       'answer | Notice that all three failures can occur even when retrieval '
                       'itself is correct]]\n'
                       '\n'
                       '## 8. Faithfulness and hallucination\n'
                       '\n'
                       'A response is **faithful** when its factual claims are supported by the '
                       'retrieved chunks. A faithfulness failure occurs when the model introduces '
                       'unsupported or contradictory claims.\n'
                       '\n'
                       'For RAG, faithfulness is central because the promise of the architecture '
                       'is grounding. If the retrieved context says a deadline is July 31 and the '
                       'answer changes it to early August, the system has broken that grounding '
                       'contract.\n'
                       '\n'
                       'The chapter also makes an important troubleshooting distinction:\n'
                       '\n'
                       '- **Unfaithful incorrectness:** the source chunks were correct, but the '
                       'generator departed from them.\n'
                       '- **Faithful incorrectness:** the generator accurately reflected retrieved '
                       'evidence, but the evidence itself was stale or wrong.\n'
                       '\n'
                       'The first points toward the generator, prompt, or hallucination controls. '
                       'The second points upstream toward ingestion, versioning, source '
                       'governance, or retrieval of obsolete content. This distinction prevents '
                       'teams from blaming the LLM for a data-management failure.\n'
                       '\n'
                       '{{exercise:M01.L06.EX03}}\n'
                       '\n'
                       '## 9. Context utilization: did the model use all necessary evidence?\n'
                       '\n'
                       'A generator can be faithful to one chunk while ignoring another critical '
                       'chunk. That produces an answer that is technically grounded yet '
                       'dangerously incomplete.\n'
                       '\n'
                       'Imagine a question asking for both the risks and benefits of a project. '
                       'The retriever correctly supplies one chunk describing expected revenue and '
                       'another describing market volatility. If the generator discusses only '
                       'revenue, the response has a **context-utilization failure**.\n'
                       '\n'
                       'This failure can arise from ordering effects, long prompts, uneven '
                       'attention to chunks, or prompt design. The “lost in the middle” phenomenon '
                       'is one reason a model may underuse evidence placed in particular '
                       'positions.\n'
                       '\n'
                       'Context utilization therefore asks a different question from faithfulness. '
                       'Faithfulness asks, “Is what the model said supported?” Context utilization '
                       'asks, “Did the model include the important things it should have said?”\n'
                       '\n'
                       '## 10. Answer relevance: did the response solve the user’s problem?\n'
                       '\n'
                       'A response can be factually correct and fully grounded but still be '
                       'unhelpful.\n'
                       '\n'
                       'If a user asks, “Is it safe to push the new update?” and the system merely '
                       'lists three features of the update, the response may be accurate yet fail '
                       'to answer the decision-oriented question. The burden of interpretation has '
                       'been returned to the user.\n'
                       '\n'
                       'This illustrates why answer relevance is not the same as factual '
                       'consistency. Relevance requires understanding the **intent of the '
                       'question**.\n'
                       '\n'
                       'Reference-answer metrics such as ROUGE-L or BERTScore may miss this kind '
                       'of failure because lexical or semantic similarity to a reference does not '
                       'always capture whether the assistant fulfilled the intended task. A '
                       'well-designed LLM-as-a-judge rubric can be more useful when the criterion '
                       'is inherently semantic and task-specific.\n'
                       '\n'
                       '## 11. Evaluation must reach back into ingestion\n'
                       '\n'
                       'RAG follows the familiar rule **garbage in, garbage out**. If parsing, '
                       'cleaning, or document lifecycle management is wrong, downstream retrieval '
                       'and generation metrics will suffer.\n'
                       '\n'
                       'Two ingestion failures receive special attention in the chapter:\n'
                       '\n'
                       '- **Structural parsing errors:** tables, images, headings, or layout '
                       'relationships are lost. The raw words may exist, but the meaning encoded '
                       'by structure disappears.\n'
                       '- **Content staleness:** old documents remain searchable after newer '
                       'versions exist.\n'
                       '\n'
                       'These problems can masquerade as retrieval or generation failures. For '
                       'example, a retriever cannot return a correctly structured table row if the '
                       'ingestion pipeline flattened it into nonsense. Likewise, a generator can '
                       'be perfectly faithful to the wrong version of a policy.\n'
                       '\n'
                       'Evaluation should therefore include data-quality checks, ingestion logs, '
                       'and version-aware tests—not just query-time metrics.\n'
                       '\n'
                       '## 12. Entity IDs and versioning as evaluation enablers\n'
                       '\n'
                       'A practical strategy for staleness is to assign each logical document a '
                       'stable **entity ID** and maintain explicit versions. When a newer version '
                       'is ingested, chunks from the superseded version can be removed or '
                       'excluded.\n'
                       '\n'
                       'This design supports a useful proactive test: if multiple active versions '
                       'of the same entity are present when only one should be current, the '
                       'ingestion pipeline is unhealthy.\n'
                       '\n'
                       'This illustrates a broader point: some “evaluation metrics” are not model '
                       'scores at all. They are **invariants** about your data and system. A '
                       'strong RAG quality program includes both statistical metrics and '
                       'deterministic checks.\n'
                       '\n'
                       '## 13. Build a failure matrix before choosing metrics\n'
                       '\n'
                       'Before selecting tools, write down the failure classes you care about and '
                       'the measurement that can reveal each one.\n'
                       '\n'
                       '| Stage | Failure | Useful signal |\n'
                       '|---|---|---|\n'
                       '| Ingestion | Lost table/layout information | parser tests, targeted '
                       'retrieval tests |\n'
                       '| Ingestion | Stale versions | entity/version invariant checks |\n'
                       '| Retrieval | Missing relevant chunks | recall@k, rank-aware metrics |\n'
                       '| Retrieval | Too much noise | precision@k, relevance judging |\n'
                       '| Generation | Unsupported claims | faithfulness / hallucination score |\n'
                       '| Generation | Ignored facts | context-utilization / nugget coverage |\n'
                       '| Generation | Off-target answer | answer relevance rubric |\n'
                       '| System | Slow responses | latency, P95/P99 |\n'
                       '| System | Instability | uptime, error rate, response consistency |\n'
                       '| Economics | Unsustainable cost | per-component cost and resource usage '
                       '|\n'
                       '\n'
                       'This mapping prevents “metric collecting” without a diagnostic purpose.\n'
                       '\n'
                       '## 14. LLM-as-a-judge: the core idea\n'
                       '\n'
                       '**LLM-as-a-judge** uses a language model as an evaluator rather than as '
                       'the user-facing generator. The judge receives evidence such as the user '
                       'query, retrieved context, generated answer, and an explicit rubric. It '
                       'then returns a score, category, or critique.\n'
                       '\n'
                       'The main strength is flexibility. Natural-language rubrics let you '
                       'evaluate criteria that are difficult to encode with simple formulas: '
                       'faithfulness, usefulness, concision, persona adherence, reasoning quality, '
                       'or domain-specific requirements.\n'
                       '\n'
                       'A judge is therefore best understood as a **programmable semantic '
                       'evaluator**. But it is still a model, with biases, cost, latency, and '
                       'randomness. Its output should not be treated as unquestionable ground '
                       'truth.\n'
                       '\n'
                       '## 15. Pointwise versus pairwise judging\n'
                       '\n'
                       'A **pointwise** judge scores one response independently, for example from '
                       '1 to 5. This is simple and useful when you need absolute thresholds.\n'
                       '\n'
                       'A **pairwise** judge compares two responses and chooses which better '
                       'satisfies a rubric. The chapter notes that pairwise comparisons often '
                       'produce more stable alignment with human preferences because the judge has '
                       'an explicit anchor.\n'
                       '\n'
                       'The trade-off is interpretability: a pointwise score can be tracked as a '
                       'time series, while pairwise evaluation is naturally suited to A/B '
                       'comparisons such as “current reranker versus candidate reranker.”\n'
                       '\n'
                       'In practice, use pointwise judging when you need an operational threshold '
                       'and pairwise judging when comparing two system versions.\n'
                       '\n'
                       '## 16. Judge biases: style, verbosity, and self-reference\n'
                       '\n'
                       'LLM judges may reward characteristics that correlate poorly with '
                       'correctness.\n'
                       '\n'
                       'The chapter discusses **self-referential bias**, where a judge prefers '
                       'outputs that resemble styles it was trained to produce. This can manifest '
                       'as:\n'
                       '\n'
                       '- **Style over substance:** polished AI-like wording receives a higher '
                       'score despite weaker facts.\n'
                       '- **Verbosity bias:** longer responses are rewarded simply because they '
                       'appear more comprehensive.\n'
                       '- **Systemic blind spots:** the judge shares a reasoning weakness with the '
                       'model under evaluation and therefore fails to penalize it.\n'
                       '\n'
                       'The antidote is calibration against a **human-verified golden set**. If '
                       'judge scores do not align with trusted human judgments on representative '
                       'examples, the judge should not be used as a quality oracle.\n'
                       '\n'
                       '{{exercise:M01.L06.EX05}}\n'
                       '\n'
                       '## 17. Judge cost and latency are part of the evaluation design\n'
                       '\n'
                       'Every LLM judge call consumes inference capacity and time. This matters '
                       'even offline when you evaluate thousands of queries, and it becomes '
                       'critical online.\n'
                       '\n'
                       'A production evaluation design should therefore answer:\n'
                       '\n'
                       '- Which metrics truly require a judge?\n'
                       '- Can a smaller model provide acceptable evaluation quality?\n'
                       '- Should only a sample of traffic be judged?\n'
                       '- Can judging run asynchronously after the user receives the answer?\n'
                       '- Should some deterministic metrics be computed first and expensive judge '
                       'calls reserved for uncertain cases?\n'
                       '\n'
                       'Evaluation has its own **budget**. Treat that budget explicitly rather '
                       'than allowing evaluation costs to hide inside general LLM spend.\n'
                       '\n'
                       '## 18. Stochastic judges can change their minds\n'
                       '\n'
                       'LLMs are stochastic. Even with temperature set to zero, identical inputs '
                       'can sometimes produce different outputs. A judge may therefore score the '
                       'same answer differently across runs.\n'
                       '\n'
                       'Practical mitigations from the chapter include:\n'
                       '\n'
                       '- run the judge multiple times and average or aggregate results;\n'
                       '- prefer structured rubrics;\n'
                       '- use pairwise comparisons when appropriate;\n'
                       '- log the full judge input and output;\n'
                       '- calibrate against human judgments;\n'
                       '- version the judge model and prompt.\n'
                       '\n'
                       'The lesson is subtle but important: the evaluation system itself must be '
                       'evaluated and monitored.\n'
                       '\n'
                       '## 19. Walkthrough: a factuality and relevance judge\n'
                       '\n'
                       'A compact implementation uses an LLM with a prompt that defines the rubric '
                       'and requests structured JSON output.\n'
                       '\n'
                       '```python\n'
                       'from openai import OpenAI\n'
                       'import json\n'
                       'import re\n'
                       '\n'
                       'client = OpenAI()\n'
                       '\n'
                       'def evaluate_answer(query, context, answer, model="gpt-4o"):\n'
                       '    prompt = f"""\n'
                       '    Evaluate this RAG answer on two criteria from 1 to 5.\n'
                       '\n'
                       '    Factuality: Is every factual claim grounded in the context?\n'
                       '    Answer relevance: Does the answer directly help with the query?\n'
                       '\n'
                       '    Query: {query}\n'
                       '    Context: {context}\n'
                       '    Answer: {answer}\n'
                       '\n'
                       '    Return only JSON with:\n'
                       '    factuality_score, factuality_reasoning,\n'
                       '    relevance_score, relevance_reasoning\n'
                       '    """\n'
                       '\n'
                       '    response = client.chat.completions.create(\n'
                       '        model=model,\n'
                       '        messages=[\n'
                       '            {"role": "system", "content": "Return valid JSON only."},\n'
                       '            {"role": "user", "content": prompt},\n'
                       '        ],\n'
                       '        temperature=0,\n'
                       '    )\n'
                       '\n'
                       '    text = response.choices[0].message.content\n'
                       '    match = re.search(r"\\{.*\\}", text, re.DOTALL)\n'
                       '    return json.loads(match.group(0)) if match else None\n'
                       '```\n'
                       '\n'
                       'The important part is not the API syntax. It is the **rubric**. The '
                       'evaluator must know exactly what factuality means, what relevance means, '
                       'and what output format is required.\n'
                       '\n'
                       'A judge result should normally include reasoning during offline analysis '
                       'so humans can inspect why a score changed. In automated pipelines, you may '
                       'additionally reduce the result to numeric fields for dashboards and '
                       'gates.\n'
                       '\n'
                       '{{exercise:M01.L06.EX04}}\n'
                       '\n'
                       '## 20. Golden chunks and golden answers\n'
                       '\n'
                       'Many traditional metrics require a trusted reference.\n'
                       '\n'
                       'A **golden chunk set** identifies which chunks should be considered '
                       'relevant for a query. It enables recall, precision, MRR, MAP, and nDCG.\n'
                       '\n'
                       'A **golden answer** is a trusted target answer used when comparing '
                       'generated output through answer-similarity metrics or correctness '
                       'rubrics.\n'
                       '\n'
                       'Golden data is powerful because it anchors evaluation in explicit human '
                       'expectations. Its weakness is maintenance cost. In a dynamic enterprise '
                       'corpus, documents change, chunk boundaries change, and the “correct” chunk '
                       'IDs may become obsolete.\n'
                       '\n'
                       'This creates a practical split:\n'
                       '\n'
                       '- Use curated golden sets when the application is stable enough and the '
                       'highest confidence is required.\n'
                       '- Use reference-free methods when the corpus is too large or changes too '
                       'rapidly for continuous manual labeling.\n'
                       '\n'
                       'Neither approach is universally superior; they solve different operational '
                       'problems.\n'
                       '\n'
                       '## 21. Precision@k: how clean is the retrieved context?\n'
                       '\n'
                       '**Precision@k** measures the fraction of the top `k` retrieved chunks that '
                       'are relevant.\n'
                       '\n'
                       '\\[\n'
                       'Precision@k = \x0c'
                       'rac{\text{relevant chunks in top k}}{k}\n'
                       '\\]\n'
                       '\n'
                       'If the retriever returns five chunks and four are relevant, precision@5 is '
                       '`4/5 = 0.8`.\n'
                       '\n'
                       'High precision means the generator receives a high signal-to-noise ratio. '
                       'This is especially valuable when context windows are limited or when '
                       'irrelevant text easily distracts the model.\n'
                       '\n'
                       'Precision does **not** tell you whether the retriever missed other '
                       'relevant chunks elsewhere in the corpus. That is recall’s job.\n'
                       '\n'
                       '{{exercise:M01.L06.EX06}}\n'
                       '\n'
                       '## 22. Recall@k: did the retriever find the evidence that exists?\n'
                       '\n'
                       '**Recall@k** measures the fraction of all relevant chunks that appear '
                       'within the top `k` results.\n'
                       '\n'
                       '\\[\n'
                       'Recall@k = \x0c'
                       'rac{\text{relevant chunks in top k}}{\text{all relevant chunks for the '
                       'query}}\n'
                       '\\]\n'
                       '\n'
                       'Suppose the corpus contains four chunks that a human considers relevant, '
                       'but only three appear in the top ten. Recall@10 is `3/4 = 0.75`.\n'
                       '\n'
                       'Recall is crucial when answers require several pieces of evidence. A '
                       'retriever with low recall can cause incomplete answers even if every '
                       'returned chunk is high quality.\n'
                       '\n'
                       'Computing recall requires knowing the complete relevant set, which is why '
                       'it becomes expensive at scale.\n'
                       '\n'
                       '{{exercise:M01.L06.EX07}}\n'
                       '\n'
                       '## 23. The precision–recall trade-off\n'
                       '\n'
                       'Increasing `k` often raises recall because more candidates are returned, '
                       'but it can lower precision because extra results include more noise. '
                       'Reducing `k` may create clean context while missing necessary facts.\n'
                       '\n'
                       'This means `k` is not merely a latency parameter. It participates in a '
                       'quality trade-off.\n'
                       '\n'
                       'A simple tuning experiment is to evaluate several values of `k` against '
                       'the same query set and plot precision and recall. You may then choose the '
                       'operating point that fits the application. For compliance or research use '
                       'cases, recall may deserve more weight; for highly focused FAQ retrieval, '
                       'precision may dominate.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Precision recall trade-off in RAG | Show top-k retrieval '
                       'expanding from a small clean set to a larger noisier set, with recall '
                       'rising and precision potentially falling | Notice that selecting k changes '
                       'both context completeness and context noise]]\n'
                       '\n'
                       '## 24. F1@k: one score when precision and recall both matter\n'
                       '\n'
                       'The **F1-score** is the harmonic mean of precision and recall:\n'
                       '\n'
                       '\\[\n'
                       'F1 = 2 \times \x0c'
                       'rac{Precision \times Recall}{Precision + Recall}\n'
                       '\\]\n'
                       '\n'
                       'The harmonic mean penalizes an imbalanced system. A retriever with '
                       'precision 1.0 but recall 0.1 will not receive a strong F1 score.\n'
                       '\n'
                       'F1 is useful when the use case values both coverage and cleanliness. But '
                       'it also hides the underlying trade-off, so keep precision and recall '
                       'visible in your dashboard instead of reporting F1 alone.\n'
                       '\n'
                       '## 25. Why rank matters in RAG\n'
                       '\n'
                       'Precision@k and recall@k treat every position in the top `k` equally. Yet '
                       'rank matters in practice.\n'
                       '\n'
                       'A chunk at position 1 may influence the generator more than one at '
                       'position 10. Long prompts can also suffer from ordering effects such as '
                       '“lost in the middle.” Therefore, retrieval evaluation should sometimes '
                       'reward systems that place the best evidence near the top.\n'
                       '\n'
                       'Rank-aware metrics answer this need. The chapter discusses **MRR, MAP, and '
                       'nDCG**.\n'
                       '\n'
                       '## 26. Mean Reciprocal Rank (MRR)\n'
                       '\n'
                       'MRR focuses on the rank of the **first relevant result**.\n'
                       '\n'
                       'For one query:\n'
                       '\n'
                       '\\[\n'
                       'RR = \x0c'
                       'rac{1}{rank_{first\\ relevant}}\n'
                       '\\]\n'
                       '\n'
                       'If the first relevant chunk is rank 1, the score is 1. If it is rank 4, '
                       'the score is 0.25. If no relevant chunk appears, the score is 0.\n'
                       '\n'
                       'MRR is then the mean of reciprocal rank over all evaluation queries.\n'
                       '\n'
                       'MRR is excellent when one strong result is enough to answer the question. '
                       'It is less informative when the answer requires several relevant chunks.\n'
                       '\n'
                       '{{exercise:M01.L06.EX08}}\n'
                       '\n'
                       '## 27. Mean Average Precision (MAP)\n'
                       '\n'
                       '**Average Precision (AP)** rewards systems that retrieve *multiple* '
                       'relevant chunks and place them high in the ranking. Conceptually, you '
                       'compute precision each time a relevant item is encountered and average '
                       'those precision values for the query. **MAP** is the mean AP over the '
                       'evaluation query set.\n'
                       '\n'
                       'MAP therefore captures more of the ranking than MRR. It is useful when '
                       'several relevant passages exist and you care about retrieving many of them '
                       'near the top.\n'
                       '\n'
                       'Unlike nDCG, traditional MAP treats relevance as binary: relevant or not '
                       'relevant.\n'
                       '\n'
                       '## 28. Normalized Discounted Cumulative Gain (nDCG)\n'
                       '\n'
                       '**nDCG** supports **graded relevance**. Instead of saying a chunk is '
                       'simply relevant or irrelevant, you can assign levels such as 0, 1, 2, and '
                       '3.\n'
                       '\n'
                       'DCG rewards high relevance and discounts items that appear later. nDCG '
                       'divides the system’s DCG by the ideal possible DCG for that query:\n'
                       '\n'
                       '\\[\n'
                       'nDCG@k = \x0c'
                       'rac{DCG@k}{IDCG@k}\n'
                       '\\]\n'
                       '\n'
                       'This makes scores comparable across queries with different relevance '
                       'distributions.\n'
                       '\n'
                       'nDCG is powerful when ranking quality is nuanced. It can be unnecessary '
                       'overhead for tiny retrieval sets where you only care whether one or two '
                       'correct chunks appear.\n'
                       '\n'
                       '[[IMAGE_NEEDED: MRR MAP and nDCG comparison | Show the same ranked list '
                       'annotated with how MRR looks only at the first relevant result, MAP '
                       'rewards every relevant position, and nDCG additionally uses graded '
                       'relevance | Notice that the metrics answer different ranking questions]]\n'
                       '\n'
                       '{{exercise:M01.L06.EX09}}\n'
                       '\n'
                       '## 29. Choosing a retrieval metric\n'
                       '\n'
                       'Use the metric that matches the retrieval objective.\n'
                       '\n'
                       '| Goal | Useful metric |\n'
                       '|---|---|\n'
                       '| Keep irrelevant context out | Precision@k |\n'
                       '| Ensure all important evidence is found | Recall@k |\n'
                       '| Balance precision and recall | F1@k |\n'
                       '| Get one good answer very high | MRR |\n'
                       '| Rank several relevant chunks well | MAP |\n'
                       '| Rank chunks with graded relevance | nDCG |\n'
                       '| Avoid maintaining golden chunk labels | UMBRELA-style judging |\n'
                       '\n'
                       'A mature evaluation suite may use several because no single metric '
                       'captures all retrieval behavior.\n'
                       '\n'
                       '## 30. UMBRELA: reference-free retrieval relevance\n'
                       '\n'
                       'The chapter introduces **UMBRELA** as a way to evaluate retrieved chunks '
                       'without a manually curated golden chunk set.\n'
                       '\n'
                       'An LLM judge receives a query and one retrieved passage, then assigns an '
                       'integer relevance score:\n'
                       '\n'
                       '- `0` — irrelevant;\n'
                       '- `1` — topically related but does not answer the query;\n'
                       '- `2` — contains useful answer information but with ambiguity or extra '
                       'material;\n'
                       '- `3` — directly and precisely answers the query.\n'
                       '\n'
                       'This turns retrieval relevance into a scalable semantic judging task. It '
                       'is particularly attractive in dynamic corpora where hand-maintained golden '
                       'chunks would become stale quickly.\n'
                       '\n'
                       'The trade is clear: you replace human labeling effort with inference cost '
                       'and judge uncertainty.\n'
                       '\n'
                       '{{exercise:M01.L06.EX10}}\n'
                       '\n'
                       '## 31. How to use UMBRELA scores\n'
                       '\n'
                       'A UMBRELA score can be inspected directly as a relevance signal for each '
                       'returned chunk. You can also use graded scores as input to ranking metrics '
                       'such as nDCG.\n'
                       '\n'
                       'What UMBRELA does **not** solve cheaply is recall over the entire corpus. '
                       'To know that the retriever found all relevant chunks, you would need '
                       'relevance judgments for every potentially relevant chunk, which is '
                       'infeasible for large collections.\n'
                       '\n'
                       'So reference-free retrieval judging is excellent for answering “How good '
                       'are the chunks I retrieved?” but not automatically “Did I retrieve every '
                       'relevant chunk that exists?”\n'
                       '\n'
                       '[[IMAGE_NEEDED: UMBRELA scoring workflow | Show query + retrieved chunk → '
                       'LLM judge → 0/1/2/3 relevance score for each candidate | Notice that no '
                       'human-labeled golden chunk is required for the returned candidates]]\n'
                       '\n'
                       '## 32. Generation evaluation asks a different question\n'
                       '\n'
                       'Retrieval metrics tell you whether the generator was given good '
                       'ingredients. Generation metrics ask whether the model **used those '
                       'ingredients correctly**.\n'
                       '\n'
                       'A strong generation evaluation suite looks at multiple dimensions:\n'
                       '\n'
                       '- context utilization;\n'
                       '- answer accuracy or similarity;\n'
                       '- answer relevance;\n'
                       '- faithfulness / factual consistency;\n'
                       '- citation accuracy;\n'
                       '- response consistency;\n'
                       '- safety and bias.\n'
                       '\n'
                       'These dimensions overlap but are not interchangeable.\n'
                       '\n'
                       '## 33. Context utilization with AutoNuggetizer\n'
                       '\n'
                       'The chapter describes **AutoNuggetizer** as a structured approach to '
                       'measuring whether a response covers the important facts available in the '
                       'evidence.\n'
                       '\n'
                       'The process begins by generating atomic **nuggets** from the query and '
                       'relevant chunks. Nuggets are then classified by importance:\n'
                       '\n'
                       '- **Vital** — necessary for a complete and correct answer.\n'
                       '- **OK** — useful supporting detail but not essential.\n'
                       '\n'
                       'The generated answer is then checked against each nugget and labeled as '
                       'supported, partially supported, or not supported. These judgments are '
                       'aggregated into an overall context-utilization assessment.\n'
                       '\n'
                       'This directly targets a weakness that faithfulness alone cannot detect. A '
                       'response may contain no hallucinations while still omitting half the vital '
                       'facts.\n'
                       '\n'
                       '[[IMAGE_NEEDED: AutoNuggetizer concept | Show retrieved evidence '
                       'decomposed into vital and optional nuggets, then compare the generated '
                       'answer against each nugget for coverage | Notice that this evaluates '
                       'completeness of evidence use rather than only hallucination]]\n'
                       '\n'
                       '{{exercise:M01.L06.EX11}}\n'
                       '\n'
                       '## 34. Answer similarity and golden answers\n'
                       '\n'
                       '**Answer similarity** compares the generated answer with a trusted '
                       'reference answer. The chapter mentions approaches such as **ROUGE-L** and '
                       '**BERTScore**.\n'
                       '\n'
                       'A surface-oriented metric such as ROUGE-L looks at overlap in sequences, '
                       'while semantic approaches such as BERTScore compare meaning using learned '
                       'representations. These methods can be useful when acceptable answers have '
                       'a relatively stable form.\n'
                       '\n'
                       'But similarity has a limitation: two answers can be semantically similar '
                       'while one fails an important instruction, and two equally correct answers '
                       'can use very different wording. Treat similarity as one signal, not a '
                       'complete measure of answer quality.\n'
                       '\n'
                       '## 35. Answer relevancy as a task-fulfillment metric\n'
                       '\n'
                       'Answer relevancy asks whether the response directly addresses the original '
                       'query. It penalizes responses that are tangential, incomplete, or filled '
                       'with unnecessary detail.\n'
                       '\n'
                       'Because relevance depends on intent, LLM-as-a-judge can be a natural fit. '
                       'A domain-specific rubric can ask whether the response reaches the '
                       'requested conclusion, includes required elements, and avoids unrelated '
                       'content.\n'
                       '\n'
                       'For example, an incident-response assistant may require a response to '
                       'state the severity, recommended action, and escalation path. Generic '
                       'semantic similarity would not necessarily enforce that rubric.\n'
                       '\n'
                       '## 36. Faithfulness as factual consistency\n'
                       '\n'
                       'Faithfulness measures whether the generated claims are supported by the '
                       'retrieved context.\n'
                       '\n'
                       'You can estimate faithfulness using:\n'
                       '\n'
                       '- a specialized hallucination detection model such as HHEM;\n'
                       '- an LLM-as-a-judge prompt that checks claims against the provided '
                       'evidence.\n'
                       '\n'
                       'The key rule is that the evaluator should judge against the **retrieved '
                       'source text**, not its own world knowledge. Otherwise it stops measuring '
                       'RAG grounding and starts evaluating external factuality.\n'
                       '\n'
                       '## 37. Citation accuracy: can the user verify the claim?\n'
                       '\n'
                       'Inline citations are valuable only when they truly support the statement '
                       'they are attached to.\n'
                       '\n'
                       '**Citation precision** asks whether a cited source actually substantiates '
                       'the associated claim. A high-quality RAG answer lets the user follow the '
                       'citation and easily locate the supporting evidence.\n'
                       '\n'
                       'Misattributed citations can be worse than no citations because they create '
                       'a false appearance of verification. Citation evaluation should therefore '
                       'be part of production testing whenever citations are a user-facing trust '
                       'feature.\n'
                       '\n'
                       '{{exercise:M01.L06.EX12}}\n'
                       '\n'
                       '## 38. Response consistency and repeatability\n'
                       '\n'
                       'Run the same query several times. Does the factual substance remain '
                       'stable?\n'
                       '\n'
                       'LLMs are probabilistic, so minor wording differences are expected. The '
                       'concern is **semantic instability**: different conclusions, different '
                       'numbers, or different recommendations for the same evidence.\n'
                       '\n'
                       'Consistency is especially important in finance, healthcare, legal, and '
                       'other regulated domains. The chapter recommends measuring it '
                       'systematically rather than assuming temperature zero guarantees '
                       'deterministic behavior.\n'
                       '\n'
                       'One practical method is to run a query `N` times and measure the '
                       'distribution of other evaluation metrics—such as faithfulness or '
                       'relevance—across the runs.\n'
                       '\n'
                       '## 39. Safety and bias belong in evaluation\n'
                       '\n'
                       'A RAG system can be relevant and faithful yet still produce unsafe or '
                       'discriminatory content. Evaluation should therefore include safety checks '
                       'on both retrieved evidence and generated output.\n'
                       '\n'
                       'The chapter mentions specialized models such as **Llama Guard** and '
                       '**ShieldGemma**. These models can classify unsafe or policy-violating '
                       'content. The exact safety policy depends on the application.\n'
                       '\n'
                       'For multimodal RAG, safety evaluation may need to inspect both text and '
                       'images. This is why safety should be designed as a broader evaluation '
                       'dimension rather than a single text-only filter.\n'
                       '\n'
                       '## 40. Red teaming finds failures your benchmark did not imagine\n'
                       '\n'
                       'Automated metrics are strongest on failure modes you already know how to '
                       'measure. **Red teaming** deliberately searches for failures outside those '
                       'comfortable paths.\n'
                       '\n'
                       'Human testers craft adversarial, culturally nuanced, ambiguous, or '
                       'ethically difficult prompts to expose bias, unsafe behavior, retrieval '
                       'weaknesses, or harmful combinations of otherwise innocent evidence.\n'
                       '\n'
                       'The most valuable outcome of red teaming is not merely a report. '
                       'Successful attacks should be transformed into:\n'
                       '\n'
                       '- new safety rules;\n'
                       '- improved prompts;\n'
                       '- data curation changes;\n'
                       '- regression tests;\n'
                       '- new benchmark cases.\n'
                       '\n'
                       'This turns one discovered weakness into a permanent improvement in the '
                       'evaluation suite.\n'
                       '\n'
                       '## 41. Evaluation frameworks solve different workflow problems\n'
                       '\n'
                       'The chapter surveys several evaluation offerings. Their value is not only '
                       'the metrics they compute but the **workflow** they encourage.\n'
                       '\n'
                       '- **Open RAG Eval** emphasizes reference-free evaluation such as UMBRELA '
                       'and AutoNuggetizer.\n'
                       '- **Ragas** provides a broad LLM-based metric ecosystem and integrates '
                       'with common RAG frameworks.\n'
                       '- **DeepEval** frames LLM evaluation like software unit testing and '
                       'integrates tightly with pytest-style workflows.\n'
                       '- **Amazon Bedrock evaluation** provides a managed approach integrated '
                       'into the AWS ecosystem.\n'
                       '\n'
                       'Do not choose a framework solely by the number of metrics in its '
                       'documentation. Choose based on transparency, required ground truth, '
                       'extensibility, CI/CD integration, managed infrastructure needs, and the '
                       'types of failures your application must detect.\n'
                       '\n'
                       '## 42. Open RAG Eval and reference-free workflows\n'
                       '\n'
                       'Open RAG Eval is presented as an open source approach designed around the '
                       'difficulty of maintaining ground-truth labels at enterprise scale.\n'
                       '\n'
                       'Its metrics include:\n'
                       '\n'
                       '- UMBRELA for retrieval relevance;\n'
                       '- AutoNuggetizer for fact/nugget coverage;\n'
                       '- hallucination scoring;\n'
                       '- citation evaluation;\n'
                       '- consistency measurement.\n'
                       '\n'
                       'A practical advantage is that evaluation can start from a query list '
                       'rather than requiring golden answers for every query. Connectors can '
                       'obtain the query, contexts, and responses from a RAG system, after which '
                       'the configured metrics are computed.\n'
                       '\n'
                       '## 43. Ragas\n'
                       '\n'
                       'Ragas is an open source RAG evaluation framework with strong integrations '
                       'into the broader LLM ecosystem. A common workflow builds an evaluation '
                       'dataset containing questions, generated answers, and retrieved contexts; a '
                       'ground-truth answer can also be included.\n'
                       '\n'
                       'Ragas can additionally generate synthetic test cases from source '
                       'documents. Synthetic data is useful for bootstrapping, but the chapter '
                       'cautions that generated queries may not reflect real user behavior '
                       'accurately.\n'
                       '\n'
                       'The general lesson is to inspect how a metric is defined instead of '
                       'treating a library score as self-explanatory. A low score is only '
                       'actionable when you understand what evidence the metric used and what '
                       'behavior it penalized.\n'
                       '\n'
                       '## 44. DeepEval and evaluation as unit testing\n'
                       '\n'
                       'DeepEval is developer-oriented. It encourages defining individual test '
                       'cases and asserting that metrics exceed required thresholds, similar to '
                       'conventional `pytest` workflows.\n'
                       '\n'
                       'That mental model is valuable because it moves RAG evaluation into the '
                       'same discipline as software regression testing. A newly changed prompt or '
                       'reranker should not be released merely because the code compiles; it '
                       'should satisfy quality assertions.\n'
                       '\n'
                       'DeepEval also supports custom criteria-based evaluation, useful when the '
                       'application has requirements that generic metrics do not capture.\n'
                       '\n'
                       '## 45. Managed evaluation with Amazon Bedrock\n'
                       '\n'
                       'A managed service can remove much of the infrastructure required to '
                       'orchestrate judge models and aggregate evaluation jobs. The chapter uses '
                       'Amazon Bedrock as an example.\n'
                       '\n'
                       'Managed evaluation can cover retrieval and generation metrics, and may '
                       'include responsible-AI dimensions such as harmfulness or refusal '
                       'behavior.\n'
                       '\n'
                       'The trade-off is the familiar platform trade-off: easier operations and '
                       'ecosystem integration in exchange for vendor cost and less visibility into '
                       'some underlying evaluation details compared with fully open source '
                       'tooling.\n'
                       '\n'
                       '## 46. Human feedback is not optional telemetry\n'
                       '\n'
                       'Automated evaluation approximates user value. Actual user feedback '
                       'measures it more directly.\n'
                       '\n'
                       'A simple thumbs-up/thumbs-down mechanism can produce a powerful production '
                       'signal if it is connected to the full interaction trace. For each '
                       'interaction, log fields such as:\n'
                       '\n'
                       '- interaction ID;\n'
                       '- query;\n'
                       '- retrieved chunks;\n'
                       '- generated answer;\n'
                       '- user feedback;\n'
                       '- timestamp;\n'
                       '- user/session metadata where appropriate.\n'
                       '\n'
                       'The useful part is not merely computing a global thumbs-up percentage. You '
                       'can segment satisfaction by topic, correlate satisfaction with automated '
                       'metrics, and inspect the worst-rated interactions for root-cause '
                       'analysis.\n'
                       '\n'
                       '{{exercise:M01.L06.EX13}}\n'
                       '\n'
                       '## 47. Turn feedback into diagnosis\n'
                       '\n'
                       'Human feedback supports several analyses:\n'
                       '\n'
                       '**Overall satisfaction rate** gives a simple high-level KPI.\n'
                       '\n'
                       '**Satisfaction by topic** can reveal that one knowledge domain is healthy '
                       'while another is failing. For example, feature questions may perform well '
                       'while billing questions fail because the billing corpus is incomplete.\n'
                       '\n'
                       '**Correlation analysis** compares human ratings with metrics such as '
                       'faithfulness or answer relevance. If low faithfulness strongly predicts '
                       'thumbs-down feedback, that metric is a useful proxy. If there is no '
                       'relationship, the metric may not reflect what users value.\n'
                       '\n'
                       '**Failure analysis** investigates badly rated queries and classifies the '
                       'root cause: missing data, poor retrieval, hallucination, irrelevant '
                       'answer, formatting, latency, or another issue.\n'
                       '\n'
                       '## 48. Measurement and tuning are two different jobs\n'
                       '\n'
                       'A mature evaluation program supports both **measurement** and **tuning**.\n'
                       '\n'
                       'Measurement asks: *How healthy is the current RAG system?* It provides '
                       'baselines, dashboards, release comparisons, and production alerts.\n'
                       '\n'
                       'Tuning asks: *Which configuration improves the system?* You deliberately '
                       'vary chunking, embedding model, retrieval method, `k`, reranker, prompt, '
                       'or LLM and use the evaluation suite to compare alternatives.\n'
                       '\n'
                       'Without measurement, tuning becomes guesswork. Without tuning, metrics '
                       'become passive reporting. The system improves when both are connected.\n'
                       '\n'
                       '## 49. Operate the judge like a production component\n'
                       '\n'
                       'If LLM judges influence release decisions or quality dashboards, they need '
                       'operational discipline.\n'
                       '\n'
                       'Log the query, retrieved context, generated answer, judge prompt, judge '
                       'model/version, score, and textual reasoning. This lets you audit why a '
                       'score changed.\n'
                       '\n'
                       'Version judge prompts. If the rubric changes from one release to another '
                       'without versioning, you create **evaluation drift**: the measured score '
                       'changes even though the RAG system did not.\n'
                       '\n'
                       'Sampling and batching can keep judge cost under control. Online judges '
                       'should usually run outside the synchronous user path unless the result is '
                       'itself a safety gate that must block delivery.\n'
                       '\n'
                       '## 50. Offline evaluation as a CI/CD quality gate\n'
                       '\n'
                       'Before deploying a changed embedding model, reranker, prompt, LLM, or '
                       'chunking strategy, run the fixed evaluation suite.\n'
                       '\n'
                       'A production team can define a **no-regression policy**, for example:\n'
                       '\n'
                       '```text\n'
                       'faithfulness >= required threshold\n'
                       'retrieval relevance >= required threshold\n'
                       'critical safety tests = 100% pass\n'
                       'P95 latency increase <= allowed budget\n'
                       '```\n'
                       '\n'
                       'The exact thresholds are application-specific. The important idea is that '
                       'quality criteria become release requirements rather than informal '
                       'observations.\n'
                       '\n'
                       'The benchmark should be a **living dataset**. When real users discover a '
                       'difficult query, add it to the benchmark so the same failure cannot '
                       'silently reappear.\n'
                       '\n'
                       'Version the benchmark alongside code and configuration so evaluation '
                       'history remains auditable.\n'
                       '\n'
                       '{{exercise:M01.L06.EX14}}\n'
                       '\n'
                       '## 51. Online evaluation should be asynchronous by default\n'
                       '\n'
                       'Live traffic is valuable because it contains query patterns your offline '
                       'benchmark did not anticipate. But expensive evaluation should not force '
                       'the user to wait.\n'
                       '\n'
                       'The chapter recommends an **out-of-band** architecture:\n'
                       '\n'
                       '```text\n'
                       'User → RAG → response returned immediately\n'
                       '              ↓\n'
                       '       log query/context/answer\n'
                       '              ↓\n'
                       '       background evaluation worker\n'
                       '              ↓\n'
                       '       quality store / alerts / dashboards\n'
                       '```\n'
                       '\n'
                       'This design allows reference-free judges or other expensive metrics to run '
                       'without adding user-perceived latency.\n'
                       '\n'
                       'You also do not need to evaluate every request. Sampling a representative '
                       'fraction of traffic can provide a strong health signal while keeping cost '
                       'manageable.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Offline and online evaluation flywheel | Show offline '
                       'benchmark and CI gate feeding production, production sampled '
                       'asynchronously, failures and user feedback returning to the benchmark | '
                       'Notice how real-world failures continuously improve the offline test '
                       'set]]\n'
                       '\n'
                       '{{exercise:M01.L06.EX15}}\n'
                       '\n'
                       '## 52. Champion–challenger A/B evaluation\n'
                       '\n'
                       'For a candidate improvement, route a controlled subset of traffic to a '
                       '**challenger** pipeline while the current production system remains the '
                       '**champion**.\n'
                       '\n'
                       'Compare automated quality metrics, user feedback, latency, and cost. This '
                       'directly tests whether an apparently better offline configuration helps '
                       'actual users.\n'
                       '\n'
                       'A/B testing is most useful when both variants are safe enough to expose to '
                       'users. High-risk changes should first pass offline gates and staged '
                       'testing.\n'
                       '\n'
                       '{{exercise:M01.L06.EX16}}\n'
                       '\n'
                       '## 53. Latency and throughput are quality metrics too\n'
                       '\n'
                       'A production RAG system must be both correct and responsive.\n'
                       '\n'
                       'Track end-to-end latency as well as per-component latency for retrieval, '
                       'reranking, and generation. Average latency alone can hide poor '
                       'experiences, so also track **tail latency** such as P95 or P99.\n'
                       '\n'
                       '**Throughput**, often expressed as queries per second (QPS), measures how '
                       'much concurrent workload the service can support.\n'
                       '\n'
                       'Decomposing latency is essential for diagnosis. If P95 grows after adding '
                       'a reranker, you should know whether the reranker itself is responsible or '
                       'whether the candidate set made generation slower.\n'
                       '\n'
                       '## 54. Reliability: uptime and error rate\n'
                       '\n'
                       '**Uptime** measures the fraction of time the application is available. '
                       'Enterprise services often target values such as 99.9% or higher, depending '
                       'on their requirements.\n'
                       '\n'
                       'Track **error rate** alongside uptime. HTTP 5xx responses, timeouts, '
                       'dependency failures, and model-provider errors may reveal a system that '
                       'technically remains “up” but is unhealthy.\n'
                       '\n'
                       'RAG has many external dependencies—vector DB, reranker, LLM, evaluator, '
                       'document store—so reliability dashboards should identify which component '
                       'generated each failure.\n'
                       '\n'
                       '## 55. Cost and resource efficiency\n'
                       '\n'
                       'Track spend by component rather than only total monthly cost:\n'
                       '\n'
                       '- vector database;\n'
                       '- lexical search;\n'
                       '- embedding service;\n'
                       '- reranker;\n'
                       '- generation LLM;\n'
                       '- evaluation judge models;\n'
                       '- compute and storage.\n'
                       '\n'
                       'Also observe CPU, GPU, and memory utilization. Evaluation itself adds a '
                       'second cost layer because LLM judges consume tokens and compute.\n'
                       '\n'
                       'This is why the chapter recommends an **evaluation budget** alongside the '
                       'production budget. Use expensive metrics where they create decision value, '
                       'and sample traffic when full coverage is unnecessary.\n'
                       '\n'
                       '## 56. Design a layered RAG quality dashboard\n'
                       '\n'
                       'A useful dashboard groups metrics by what they diagnose.\n'
                       '\n'
                       '**Ingestion health**\n'
                       '- parsing failures;\n'
                       '- stale/duplicate document versions;\n'
                       '- ingestion lag.\n'
                       '\n'
                       '**Retrieval quality**\n'
                       '- precision/recall or reference-free relevance;\n'
                       '- rank-aware metrics;\n'
                       '- retrieval latency.\n'
                       '\n'
                       '**Generation quality**\n'
                       '- faithfulness;\n'
                       '- context utilization;\n'
                       '- answer relevance;\n'
                       '- citation accuracy;\n'
                       '- consistency.\n'
                       '\n'
                       '**User outcomes**\n'
                       '- satisfaction rate;\n'
                       '- feedback by topic;\n'
                       '- failure categories.\n'
                       '\n'
                       '**System health**\n'
                       '- average/P95/P99 latency;\n'
                       '- QPS;\n'
                       '- uptime;\n'
                       '- errors;\n'
                       '- cost and resource usage.\n'
                       '\n'
                       '[[IMAGE_NEEDED: RAG evaluation dashboard | Show five groups for ingestion, '
                       'retrieval, generation, user outcomes, and system health with '
                       'representative metrics | Notice that model quality and operational quality '
                       'are monitored together]]\n'
                       '\n'
                       '{{exercise:M01.L06.EX17}}\n'
                       '\n'
                       '## 57. A practical end-to-end evaluation workflow\n'
                       '\n'
                       'A disciplined evaluation cycle can look like this:\n'
                       '\n'
                       '1. Define business-critical query classes.\n'
                       '2. Build a representative offline query set.\n'
                       '3. Create golden chunks/answers where feasible.\n'
                       '4. Select stage-specific metrics tied to known failure modes.\n'
                       '5. Establish the baseline system.\n'
                       '6. Change **one major variable at a time** when possible.\n'
                       '7. Re-run evaluation and inspect both aggregate and per-query results.\n'
                       '8. Check latency and cost so quality gains are not economically '
                       'unacceptable.\n'
                       '9. Gate releases on non-regression criteria.\n'
                       '10. Sample production interactions asynchronously.\n'
                       '11. Combine automated metrics with human feedback.\n'
                       '12. Promote important failures into the offline benchmark.\n'
                       '\n'
                       'The final step closes the loop: production experience continuously '
                       'strengthens future evaluation.\n'
                       '\n'
                       '{{exercise:M01.L06.EX18}}\n'
                       '\n'
                       '## 58. Common misconceptions\n'
                       '\n'
                       '**Misconception 1: “A good LLM can compensate for weak retrieval.”**  \n'
                       'It cannot reliably answer from evidence it never received.\n'
                       '\n'
                       '**Misconception 2: “High faithfulness means the answer is correct.”**  \n'
                       'A model can be perfectly faithful to stale or incorrect source documents.\n'
                       '\n'
                       '**Misconception 3: “Precision is enough.”**  \n'
                       'A clean context can still omit critical evidence; recall matters too.\n'
                       '\n'
                       '**Misconception 4: “One aggregate RAG score is sufficient.”**  \n'
                       'Aggregate scores hide the component that failed.\n'
                       '\n'
                       '**Misconception 5: “Temperature zero makes judging deterministic.”**  \n'
                       'LLM behavior can remain nondeterministic.\n'
                       '\n'
                       '**Misconception 6: “Reference-free means ground-truth quality is '
                       'unnecessary forever.”**  \n'
                       'Human-calibrated examples are still valuable for validating judge '
                       'behavior.\n'
                       '\n'
                       '**Misconception 7: “Online evaluation should block every answer.”**  \n'
                       'Most quality evaluation can run asynchronously on sampled traffic.\n'
                       '\n'
                       '**Misconception 8: “Evaluation cost is negligible.”**  \n'
                       'LLM judging can become a meaningful secondary token/compute expense.\n'
                       '\n'
                       '## 59. Key terminology\n'
                       '\n'
                       '| Term | Meaning in this lesson |\n'
                       '|---|---|\n'
                       '| Offline evaluation | Evaluation during development, usually against a '
                       'controlled benchmark |\n'
                       '| Online evaluation | Evaluation of live production interactions |\n'
                       '| Golden chunk | Human-curated chunk considered relevant to a query |\n'
                       '| Golden answer | Trusted reference answer |\n'
                       '| Precision@k | Fraction of returned top-k chunks that are relevant |\n'
                       '| Recall@k | Fraction of all relevant chunks found in top-k |\n'
                       '| F1 | Harmonic mean of precision and recall |\n'
                       '| MRR | Rank-sensitive metric focused on the first relevant result |\n'
                       '| MAP | Ranking metric rewarding multiple relevant results placed high |\n'
                       '| nDCG | Rank-aware metric supporting graded relevance |\n'
                       '| LLM-as-a-judge | Using an LLM to score output against a rubric |\n'
                       '| UMBRELA | Reference-free LLM-based relevance scoring for retrieved '
                       'passages |\n'
                       '| Nugget | Atomic fact used in context-utilization evaluation |\n'
                       '| Faithfulness | Degree to which generated claims are supported by '
                       'retrieved context |\n'
                       '| Citation precision | Degree to which cited evidence really supports '
                       'associated claims |\n'
                       '| Evaluation drift | Score changes caused by changed evaluation '
                       'criteria/model rather than changed RAG quality |\n'
                       '| Evaluation gate | CI/CD quality threshold a candidate release must pass '
                       '|\n'
                       '| Tail latency | High-percentile latency such as P95/P99 |\n'
                       '| QPS | Queries per second, a throughput measure |\n'
                       '\n'
                       '## 60. Retain this mental model\n'
                       '\n'
                       'Think of RAG evaluation as a **measurement stack that mirrors the RAG '
                       'stack**.\n'
                       '\n'
                       '```text\n'
                       'SOURCE / INGESTION\n'
                       'Is the right information present, clean, structured, and current?\n'
                       '        ↓\n'
                       'RETRIEVAL\n'
                       'Did we find the right evidence and rank it well?\n'
                       '        ↓\n'
                       'GENERATION\n'
                       'Did we use that evidence faithfully, completely, and relevantly?\n'
                       '        ↓\n'
                       'USER\n'
                       'Was the result useful and trusted?\n'
                       '        ↓\n'
                       'SYSTEM\n'
                       'Was it fast, available, scalable, and affordable?\n'
                       '```\n'
                       '\n'
                       'When a metric gets worse, ask which layer it belongs to before changing '
                       'anything. That habit prevents random tuning and turns evaluation into an '
                       'engineering discipline.\n'
                       '\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Comprehensive self-check\n'
                       '\n'
                       '1. Why should RAG evaluation be treated as diagnosis rather than a single '
                       'leaderboard score?\n'
                       '2. What is the difference between offline and online RAG evaluation?\n'
                       '3. Why is offline evaluation especially useful for tuning?\n'
                       '4. Why is online evaluation valuable even when offline benchmarks are '
                       'strong?\n'
                       '5. Why can a good generator not compensate reliably for low retrieval '
                       'recall?\n'
                       '6. What is a complete retrieval miss?\n'
                       '7. What is a partial retrieval miss?\n'
                       '8. How can low precision harm generation even if the correct chunk is '
                       'present?\n'
                       '9. Why can increasing top-k improve recall but reduce precision?\n'
                       '10. What kind of query may reveal an architectural limit of standard RAG?\n'
                       '11. What is a faithfulness failure?\n'
                       '12. What is faithful incorrectness?\n'
                       '13. What is unfaithful incorrectness?\n'
                       '14. Why does distinguishing faithful incorrectness from unfaithful '
                       'incorrectness matter?\n'
                       '15. What is a context-utilization failure?\n'
                       '16. How is context utilization different from faithfulness?\n'
                       '17. What is an answer-relevance failure?\n'
                       '18. Why can answer similarity miss an answer-relevance failure?\n'
                       '19. How can structural parsing errors affect retrieval?\n'
                       '20. How can stale content produce a faithful but wrong answer?\n'
                       '21. Why are stable entity IDs useful for document versioning?\n'
                       '22. What is an example of a deterministic ingestion quality invariant?\n'
                       '23. What information does an LLM-as-a-judge receive?\n'
                       '24. Why is natural-language rubric flexibility useful?\n'
                       '25. What is pointwise judging?\n'
                       '26. What is pairwise judging?\n'
                       '27. Why may pairwise judging be more stable?\n'
                       '28. What is self-referential bias in an LLM judge?\n'
                       '29. What is verbosity bias?\n'
                       '30. How can a human-verified golden set calibrate a judge?\n'
                       '31. Why is judge cost part of evaluation architecture?\n'
                       '32. Why can an LLM judge produce different scores for identical input?\n'
                       '33. Name two ways to reduce judge instability.\n'
                       '34. Why should judge prompts be versioned?\n'
                       '35. What is evaluation drift?\n'
                       '36. What is a golden chunk?\n'
                       '37. What is a golden answer?\n'
                       '38. Why are golden chunks difficult to maintain in dynamic corpora?\n'
                       '39. What does precision@k measure?\n'
                       '40. What does recall@k measure?\n'
                       '41. If top-5 contains four relevant chunks, what is precision@5?\n'
                       '42. If six relevant chunks exist and top-5 contains three, what is '
                       'recall@5?\n'
                       '43. Why is F1 useful?\n'
                       '44. Why should precision and recall remain visible even when F1 is '
                       'reported?\n'
                       '45. Why do rank-aware metrics matter for RAG?\n'
                       '46. What does MRR focus on?\n'
                       '47. When is MRR a good choice?\n'
                       '48. How does MAP differ from MRR?\n'
                       '49. What additional capability does nDCG provide over MAP?\n'
                       '50. What is graded relevance?\n'
                       '51. Why can nDCG be unnecessary for very small top-k sets?\n'
                       '52. What problem does UMBRELA try to solve?\n'
                       '53. What do UMBRELA scores 0 and 3 mean?\n'
                       '54. Why does UMBRELA not automatically give corpus-wide recall?\n'
                       '55. What is the key trade-off of reference-free LLM judging?\n'
                       '56. What does context utilization measure?\n'
                       '57. What is a nugget in AutoNuggetizer?\n'
                       '58. What is the difference between a vital nugget and an OK nugget?\n'
                       "59. What does 'partially supported' mean in nugget evaluation?\n"
                       '60. What does answer similarity compare?\n'
                       '61. Why can two correct answers have low lexical overlap?\n'
                       '62. What does answer relevancy measure?\n'
                       '63. What does faithfulness measure?\n'
                       '64. Why should a faithfulness evaluator judge against retrieved context '
                       'rather than world knowledge?\n'
                       '65. What is citation precision?\n'
                       '66. Why can a wrong citation be more damaging than no citation?\n'
                       '67. What does response consistency measure?\n'
                       '68. Why is consistency important in regulated domains?\n'
                       '69. Why is temperature zero not a complete determinism guarantee?\n'
                       '70. Why should safety and bias be part of RAG evaluation?\n'
                       '71. What role can Llama Guard or ShieldGemma play?\n'
                       '72. What is red teaming?\n'
                       '73. How should successful red-team failures improve the evaluation suite?\n'
                       '74. What is the main appeal of Open RAG Eval?\n'
                       '75. What kind of workflow does DeepEval encourage?\n'
                       '76. What is one caution about synthetic test generation?\n'
                       '77. What is one advantage of managed RAG evaluation services?\n'
                       '78. What fields should be logged with user feedback?\n'
                       '79. Why is satisfaction by topic more useful than one overall satisfaction '
                       'rate?\n'
                       '80. How can human feedback validate automated metrics?\n'
                       '81. What is measurement in the RAG evaluation lifecycle?\n'
                       '82. What is tuning?\n'
                       '83. Why does tuning without measurement become guesswork?\n'
                       '84. Why should LLM judge reasoning be logged?\n'
                       '85. What is a no-regression release policy?\n'
                       '86. Why should benchmark datasets evolve over time?\n'
                       '87. Why should benchmark data be versioned?\n'
                       '88. Why is asynchronous evaluation useful online?\n'
                       '89. Why might evaluating only a sample of live traffic be sufficient?\n'
                       '90. What is a champion pipeline?\n'
                       '91. What is a challenger pipeline?\n'
                       '92. What should an A/B evaluation compare besides answer quality?\n'
                       '93. Why should average latency not be the only latency metric?\n'
                       '94. What do P95 and P99 describe?\n'
                       '95. What is QPS?\n'
                       '96. What does uptime measure?\n'
                       '97. What does error rate reveal that uptime alone may hide?\n'
                       '98. Why should RAG evaluation cost itself be monitored?\n'
                       '99. Which compute-resource metrics should accompany monetary cost?\n'
                       '100. Why should retrieval and generation metrics appear on separate '
                       'dashboard groups?\n'
                       '101. Why should ingestion health appear on the same quality dashboard as '
                       'model metrics?\n'
                       '102. What is the role of user outcomes in an evaluation dashboard?\n'
                       '103. What is the role of system-health metrics?\n'
                       '104. What is the first step when a metric regresses: tune randomly or '
                       'localize the failure layer?\n'
                       '105. Why should only one major variable be changed at a time when '
                       'practical?\n'
                       '106. How do real-world failures improve future offline evaluation?\n'
                       '107. How can evaluation become a business lever rather than a reporting '
                       'task?\n'
                       '108. Why is RAG evaluation not one-size-fits-all?\n'
                       '109. Give an example of a use case that might prioritize recall over '
                       'precision.\n'
                       '110. Give an example of a use case that might prioritize faithfulness over '
                       'stylistic similarity.\n'
                       "111. Why should latency and cost be considered when selecting the 'best' "
                       'model configuration?\n'
                       '112. What does it mean to mirror the RAG stack with an evaluation stack?\n'
                       '113. How does a layered metric suite prevent misdiagnosis?\n'
                       '114. Why can a high aggregate score hide dangerous edge cases?\n'
                       '115. Why are per-query results important during debugging?\n'
                       '116. How would you turn a user thumbs-down into a regression test?\n'
                       '117. How can stale source data be detected proactively?\n'
                       '118. What metrics would you inspect first if users complain that answers '
                       'omit key details?\n'
                       '119. What metrics would you inspect first if answers contain unsupported '
                       'facts?\n'
                       '120. What metrics would you inspect first if answers are correct but too '
                       'slow?\n'
                       '121. What metrics would you inspect first if retrieval returns many '
                       'related but useless chunks?\n'
                       '122. What would you inspect if the same question produces materially '
                       'different answers?\n'
                       '123. How can sampling reduce online evaluation cost?\n'
                       '124. Why should a judge model change trigger re-calibration?\n'
                       '125. Why should evaluation prompts be treated like code?\n'
                       '126. How do citations support user trust only when citation accuracy is '
                       'high?\n'
                       '127. How can feedback-topic clustering expose corpus gaps?\n'
                       '128. Why is evaluation required after changing the embedding model?\n'
                       '129. Why is evaluation required after changing only the prompt?\n'
                       '130. Why should a new reranker be tested for latency as well as '
                       'relevance?\n'
                       '131. Why can a reference-free metric still benefit from human '
                       'calibration?\n'
                       '132. What is the central mental model you should retain from this lesson?\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Lesson summary\n'
                       '\n'
                       'RAG evaluation is a continuous engineering discipline. Diagnose ingestion, '
                       'retrieval, generation, user outcomes, and system health separately; use '
                       'metrics that match the failure you are trying to detect; combine '
                       'golden-data evaluation with scalable reference-free techniques when '
                       'appropriate; calibrate LLM judges instead of blindly trusting them; '
                       'integrate offline evaluation into CI/CD; sample and evaluate production '
                       'traffic asynchronously; and close the loop by converting real failures and '
                       'human feedback into new regression tests.\n',
            'estimated_minutes': 630,
            'has_code_examples': True,
            'has_manual_image_requests': True,
            'sections': [{'id': 'evaluation-purpose',
                          'title': 'Why RAG evaluation is a system requirement',
                          'order': 1},
                         {'id': 'offline-vs-online',
                          'title': 'Offline evaluation versus online evaluation',
                          'order': 2},
                         {'id': 'failure-localization',
                          'title': 'Evaluate the pipeline, not only the final answer',
                          'order': 3},
                         {'id': 'retrieval-failure-low-recall',
                          'title': 'Retrieval failure: low recall',
                          'order': 4},
                         {'id': 'retrieval-failure-low-precision',
                          'title': 'Retrieval failure: low precision',
                          'order': 5},
                         {'id': 'architectural-retrieval-limits',
                          'title': 'Some retrieval failures are architectural',
                          'order': 6},
                         {'id': 'generation-failure-map',
                          'title': 'Generation can fail even with good retrieval',
                          'order': 7},
                         {'id': 'faithfulness-failure',
                          'title': 'Faithfulness and hallucination',
                          'order': 8},
                         {'id': 'context-utilization-failure',
                          'title': 'Context utilization: did the model use all necessary evidence?',
                          'order': 9},
                         {'id': 'answer-relevance-failure',
                          'title': 'Answer relevance: did the response solve the user’s problem?',
                          'order': 10},
                         {'id': 'ingestion-failures',
                          'title': 'Evaluation must reach back into ingestion',
                          'order': 11},
                         {'id': 'document-versioning',
                          'title': 'Entity IDs and versioning as evaluation enablers',
                          'order': 12},
                         {'id': 'failure-matrix',
                          'title': 'Build a failure matrix before choosing metrics',
                          'order': 13},
                         {'id': 'judge-concept',
                          'title': 'LLM-as-a-judge: the core idea',
                          'order': 14},
                         {'id': 'judge-pointwise-pairwise',
                          'title': 'Pointwise versus pairwise judging',
                          'order': 15},
                         {'id': 'judge-biases',
                          'title': 'Judge biases: style, verbosity, and self-reference',
                          'order': 16},
                         {'id': 'judge-cost-latency',
                          'title': 'Judge cost and latency are part of the evaluation design',
                          'order': 17},
                         {'id': 'judge-instability',
                          'title': 'Stochastic judges can change their minds',
                          'order': 18},
                         {'id': 'judge-code',
                          'title': 'Walkthrough: a factuality and relevance judge',
                          'order': 19},
                         {'id': 'golden-data',
                          'title': 'Golden chunks and golden answers',
                          'order': 20},
                         {'id': 'precision-at-k',
                          'title': 'Precision@k: how clean is the retrieved context?',
                          'order': 21},
                         {'id': 'recall-at-k',
                          'title': 'Recall@k: did the retriever find the evidence that exists?',
                          'order': 22},
                         {'id': 'precision-recall-tradeoff',
                          'title': 'The precision–recall trade-off',
                          'order': 23},
                         {'id': 'f1-score',
                          'title': 'F1@k: one score when precision and recall both matter',
                          'order': 24},
                         {'id': 'rank-awareness', 'title': 'Why rank matters in RAG', 'order': 25},
                         {'id': 'mrr', 'title': 'Mean Reciprocal Rank (MRR)', 'order': 26},
                         {'id': 'map', 'title': 'Mean Average Precision (MAP)', 'order': 27},
                         {'id': 'ndcg',
                          'title': 'Normalized Discounted Cumulative Gain (nDCG)',
                          'order': 28},
                         {'id': 'retrieval-metric-selection',
                          'title': 'Choosing a retrieval metric',
                          'order': 29},
                         {'id': 'umbrela',
                          'title': 'UMBRELA: reference-free retrieval relevance',
                          'order': 30},
                         {'id': 'umbrela-interpretation',
                          'title': 'How to use UMBRELA scores',
                          'order': 31},
                         {'id': 'generation-metrics-overview',
                          'title': 'Generation evaluation asks a different question',
                          'order': 32},
                         {'id': 'autonuggetizer',
                          'title': 'Context utilization with AutoNuggetizer',
                          'order': 33},
                         {'id': 'answer-similarity',
                          'title': 'Answer similarity and golden answers',
                          'order': 34},
                         {'id': 'answer-relevancy',
                          'title': 'Answer relevancy as a task-fulfillment metric',
                          'order': 35},
                         {'id': 'faithfulness-metric',
                          'title': 'Faithfulness as factual consistency',
                          'order': 36},
                         {'id': 'citation-accuracy',
                          'title': 'Citation accuracy: can the user verify the claim?',
                          'order': 37},
                         {'id': 'response-consistency',
                          'title': 'Response consistency and repeatability',
                          'order': 38},
                         {'id': 'safety-bias',
                          'title': 'Safety and bias belong in evaluation',
                          'order': 39},
                         {'id': 'red-teaming',
                          'title': 'Red teaming finds failures your benchmark did not imagine',
                          'order': 40},
                         {'id': 'evaluation-tools-map',
                          'title': 'Evaluation frameworks solve different workflow problems',
                          'order': 41},
                         {'id': 'open-rag-eval',
                          'title': 'Open RAG Eval and reference-free workflows',
                          'order': 42},
                         {'id': 'ragas', 'title': 'Ragas', 'order': 43},
                         {'id': 'deepeval',
                          'title': 'DeepEval and evaluation as unit testing',
                          'order': 44},
                         {'id': 'bedrock-eval',
                          'title': 'Managed evaluation with Amazon Bedrock',
                          'order': 45},
                         {'id': 'human-feedback',
                          'title': 'Human feedback is not optional telemetry',
                          'order': 46},
                         {'id': 'feedback-analysis',
                          'title': 'Turn feedback into diagnosis',
                          'order': 47},
                         {'id': 'measurement-vs-tuning',
                          'title': 'Measurement and tuning are two different jobs',
                          'order': 48},
                         {'id': 'judge-production',
                          'title': 'Operate the judge like a production component',
                          'order': 49},
                         {'id': 'offline-gates',
                          'title': 'Offline evaluation as a CI/CD quality gate',
                          'order': 50},
                         {'id': 'online-eval',
                          'title': 'Online evaluation should be asynchronous by default',
                          'order': 51},
                         {'id': 'ab-testing',
                          'title': 'Champion–challenger A/B evaluation',
                          'order': 52},
                         {'id': 'latency-throughput',
                          'title': 'Latency and throughput are quality metrics too',
                          'order': 53},
                         {'id': 'uptime-errors',
                          'title': 'Reliability: uptime and error rate',
                          'order': 54},
                         {'id': 'cost-resource',
                          'title': 'Cost and resource efficiency',
                          'order': 55},
                         {'id': 'quality-dashboard',
                          'title': 'Design a layered RAG quality dashboard',
                          'order': 56},
                         {'id': 'evaluation-workflow',
                          'title': 'A practical end-to-end evaluation workflow',
                          'order': 57},
                         {'id': 'common-misconceptions',
                          'title': 'Common misconceptions',
                          'order': 58},
                         {'id': 'terminology', 'title': 'Key terminology', 'order': 59},
                         {'id': 'retain-mental-model',
                          'title': 'Retain this mental model',
                          'order': 60}]},
 'exercises': [{'id': 'M01.L06.EX01',
                'title': 'Diagnose a RAG failure',
                'lesson_code': 'M01.L06',
                'section_id': 'failure-localization',
                'placement': 'after_section',
                'description': 'Given five bad RAG outputs, classify each failure as ingestion, '
                               'retrieval, generation, or system-level and justify the '
                               'classification.',
                'instructions': '1. Use these five bad outputs from one HR assistant: (a) it cites a PDF page whose table was extracted as scrambled text; (b) the right policy exists in the index but is ranked 40th; (c) the correct chunk is retrieved, yet the answer contradicts it; (d) half the requests time out after a model-provider outage; (e) answers quote a 2022 policy that was replaced in 2024.\n'
                                '2. Classify each failure as ingestion, retrieval, generation, or system-level.\n'
                                '3. Write the evidence in the output that supports each classification.\n'
                                '4. Name the first component you would inspect for each one.',
                'expected_output': 'A table with failure category, evidence, and first component '
                                   'to inspect.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX02',
                'title': 'Design a low-recall test',
                'lesson_code': 'M01.L06',
                'section_id': 'retrieval-failure-low-recall',
                'placement': 'after_section',
                'description': 'Create a query that requires two distinct chunks and describe how '
                               'you would detect a partial retrieval failure.',
                'instructions': '1. Write a question whose full answer needs facts from two different chunks (for example a leave-policy chunk and a payroll-calendar chunk).\n'
                                '2. List the evidence each chunk must contribute.\n'
                                '3. Describe what a partial retrieval looks like: only one of the two chunks appears in the top-k.\n'
                                '4. Write a pass/fail rule, such as: pass only if both required chunks appear in the top 5.',
                'expected_output': 'A query, required evidence list, and a pass/fail retrieval '
                                   'rule.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX03',
                'title': 'Separate faithful from correct',
                'lesson_code': 'M01.L06',
                'section_id': 'faithfulness-failure',
                'placement': 'after_section',
                'description': 'Write one example of a faithful-but-wrong answer caused by stale '
                               'source data and one unfaithful answer caused by the generator.',
                'instructions': '1. Write a question and an answer that faithfully repeats its retrieved source, but the source itself is out of date, so the answer is wrong.\n'
                                '2. Write a second answer where the retrieved source is correct but the generator adds or changes a fact.\n'
                                '3. For each answer, state the root cause in one sentence.\n'
                                '4. Propose a different fix for each: one for the data, one for generation.',
                'expected_output': 'Two examples with different root causes and remediation paths.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX04',
                'title': 'Design an LLM judge rubric',
                'lesson_code': 'M01.L06',
                'section_id': 'judge-code',
                'placement': 'after_section',
                'description': 'Write a 1–5 rubric for factuality and answer relevance with '
                               'explicit definitions for scores 1, 3, and 5.',
                'instructions': '1. Write a 1-5 scale for factuality and a separate 1-5 scale for answer relevance.\n'
                                '2. Define scores 1, 3 and 5 for each scale with observable criteria, not adjectives alone.\n'
                                '3. Add one short example answer for score 3 on each scale.\n'
                                '4. Check that another evaluator could apply the definitions without asking you questions.',
                'expected_output': 'A rubric precise enough that another evaluator could apply it '
                                   'consistently.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX05',
                'title': 'Audit a judge for verbosity bias',
                'lesson_code': 'M01.L06',
                'section_id': 'judge-biases',
                'placement': 'after_section',
                'description': 'Create a concise correct answer and a verbose partially wrong '
                               'answer, then describe how you would test whether a judge rewards '
                               'verbosity.',
                'instructions': '1. Write one question, a concise correct answer, and a long answer that contains one wrong fact.\n'
                                '2. Describe how you would send both answers to the judge, swapping their order between runs.\n'
                                '3. Define the result that would show verbosity bias.\n'
                                '4. Propose one change to the judge prompt or rubric that reduces the bias.',
                'expected_output': 'A controlled judge-calibration experiment.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX06',
                'title': 'Calculate precision@k',
                'lesson_code': 'M01.L06',
                'section_id': 'precision-at-k',
                'placement': 'after_section',
                'description': 'For a top-5 relevance pattern [R, I, R, R, I], compute '
                               'precision@5.',
                'instructions': '1. Count the relevant results (R) among the top 5: [R, I, R, R, I].\n'
                                '2. Divide that count by k = 5.\n'
                                '3. Write the result as a fraction and as a decimal.\n'
                                '4. Explain in one sentence what the number says about the results a user sees.',
                'expected_output': 'Precision@5 as a fraction and a decimal, with a one-sentence interpretation.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX07',
                'title': 'Calculate recall@k',
                'lesson_code': 'M01.L06',
                'section_id': 'recall-at-k',
                'placement': 'after_section',
                'description': 'If five relevant chunks exist and top-5 retrieval contains three '
                               'of them, compute recall@5.',
                'instructions': '1. Note how many relevant chunks exist in total (5).\n'
                                '2. Note how many of them appear in the top 5 results (3).\n'
                                '3. Compute recall@5 as found divided by total relevant, as a fraction and a decimal.\n'
                                '4. Explain what the missing chunks could mean for the completeness of the answer.',
                'expected_output': 'Recall@5 as a fraction and a decimal, with an interpretation of completeness.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX08',
                'title': 'Calculate reciprocal rank',
                'lesson_code': 'M01.L06',
                'section_id': 'mrr',
                'placement': 'after_section',
                'description': 'If the first relevant result is at rank 4, calculate reciprocal '
                               'rank.',
                'instructions': '1. Find the rank of the first relevant result (rank 4).\n'
                                '2. Compute the reciprocal rank as 1 divided by that rank, as a fraction and a decimal.\n'
                                '3. Explain what MRR (the mean of reciprocal ranks over many queries) rewards.',
                'expected_output': 'The reciprocal rank as a fraction and a decimal, and an explanation of what MRR rewards.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX09',
                'title': 'Choose a rank-aware metric',
                'lesson_code': 'M01.L06',
                'section_id': 'ndcg',
                'placement': 'after_section',
                'description': 'For a search problem where passages have relevance grades 0–3, '
                               'explain why nDCG is more suitable than MRR.',
                'instructions': '1. Describe what MRR measures: only the position of the first relevant result.\n'
                                '2. Describe what nDCG measures: graded relevance (0-3) across the whole ranking.\n'
                                '3. Give a two-ranking example where MRR is the same but nDCG differs.\n'
                                '4. Conclude which metric fits graded passages and why.',
                'expected_output': 'A comparison that references graded relevance and full ranking '
                                   'quality.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX10',
                'title': 'Score passages with UMBRELA',
                'lesson_code': 'M01.L06',
                'section_id': 'umbrela',
                'placement': 'after_section',
                'description': 'Create four passages for one query and assign expected UMBRELA '
                               'scores 0, 1, 2, and 3.',
                'instructions': '1. Write one query, for example: "How many vacation days do new employees get?"\n'
                                '2. Write four short passages: one unrelated (0), one on the topic but without the answer (1), one with a partial answer (2), and one that fully answers it (3).\n'
                                '3. Assign each passage its UMBRELA score.\n'
                                '4. Justify each score in one sentence.',
                'expected_output': 'Four passages with justified relevance levels.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX11',
                'title': 'Build a nugget set',
                'lesson_code': 'M01.L06',
                'section_id': 'autonuggetizer',
                'placement': 'after_section',
                'description': 'For a two-part policy question, create vital and optional nuggets '
                               'and evaluate whether a sample answer covers them.',
                'instructions': '1. Use a two-part question, for example: "Can I carry over unused leave, and until when?"\n'
                                '2. List the vital nuggets (facts any correct answer must contain) and the optional nuggets (helpful extras).\n'
                                '3. Write a short sample answer.\n'
                                '4. Mark each nugget as supported, partially supported, or missing in that answer.',
                'expected_output': 'A nugget table with importance and support status.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX12',
                'title': 'Audit citation precision',
                'lesson_code': 'M01.L06',
                'section_id': 'citation-accuracy',
                'placement': 'after_section',
                'description': 'Write three claims with citations, including one misattribution, '
                               'then define how your evaluator should flag it.',
                'instructions': '1. Write three short source passages, each with an ID such as [S1].\n'
                                '2. Write three claims that cite them, making one claim cite a source that does not support it.\n'
                                '3. Define how your evaluator checks each citation against its source.\n'
                                '4. Write the pass/fail rule for citation precision.',
                'expected_output': 'A small citation-audit dataset and pass/fail rule.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX13',
                'title': 'Design feedback logging',
                'lesson_code': 'M01.L06',
                'section_id': 'human-feedback',
                'placement': 'after_section',
                'description': 'Define a production interaction event schema that supports '
                               'satisfaction, topic analysis, and failure debugging.',
                'instructions': '1. List the fields of one interaction event: query, retrieved context IDs, answer, model version and timestamp.\n'
                                '2. Add feedback fields: a rating and an optional comment.\n'
                                '3. Add the metadata you need for topic analysis and debugging (for example a topic label and latency).\n'
                                '4. Mark which fields contain personal data and how they are protected.',
                'expected_output': 'A JSON-like schema containing query, contexts, answer, '
                                   'feedback, and metadata.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX14',
                'title': 'Create a release gate',
                'lesson_code': 'M01.L06',
                'section_id': 'offline-gates',
                'placement': 'after_section',
                'description': 'Define four quality and system thresholds that a changed reranker '
                               'must meet before deployment.',
                'instructions': '1. Choose two quality metrics the new reranker must not make worse (for example nDCG@10 and faithfulness).\n'
                                '2. Choose two system metrics with limits (for example p95 latency and cost per 1,000 queries).\n'
                                '3. Write a numeric threshold for each of the four metrics.\n'
                                '4. State what happens when one threshold is missed.',
                'expected_output': 'A no-regression policy including quality and latency '
                                   'requirements.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX15',
                'title': 'Design asynchronous online evaluation',
                'lesson_code': 'M01.L06',
                'section_id': 'online-eval',
                'placement': 'after_section',
                'description': 'Sketch the components required to evaluate 10% of live traffic '
                               'without delaying user responses.',
                'instructions': '1. Show where each interaction is logged after the answer has already been sent to the user.\n'
                                '2. Describe how 10% of interactions are sampled.\n'
                                '3. Add a queue and a background worker that runs the evaluator.\n'
                                '4. Show where the scores are stored and displayed on a dashboard.',
                'expected_output': 'A flow containing logging, sampling, queue/background worker, '
                                   'evaluator, and dashboard.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX16',
                'title': 'Plan a champion–challenger experiment',
                'lesson_code': 'M01.L06',
                'section_id': 'ab-testing',
                'placement': 'after_section',
                'description': 'Design an A/B test for a new reranker including primary quality '
                               'metric, latency metric, and user-feedback metric.',
                'instructions': '1. Describe how traffic is split between the current reranker (champion) and the new one (challenger).\n'
                                '2. Choose the primary quality metric, a latency metric and a user-feedback metric.\n'
                                '3. Write a success criterion for each metric.\n'
                                '4. State how long the test runs and when you would stop it early.',
                'expected_output': 'An experiment plan with success criteria.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX17',
                'title': 'Build a metric dashboard',
                'lesson_code': 'M01.L06',
                'section_id': 'quality-dashboard',
                'placement': 'after_section',
                'description': 'Choose at least two metrics each for retrieval, generation, user '
                               'outcomes, and system health.',
                'instructions': '1. Choose at least two retrieval metrics.\n'
                                '2. Choose at least two generation metrics.\n'
                                '3. Choose at least two user-outcome metrics and two system-health metrics.\n'
                                '4. For each metric, write one sentence on the problem it would reveal.',
                'expected_output': 'A grouped dashboard specification and rationale.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']},
               {'id': 'M01.L06.EX18',
                'title': 'Create your RAG evaluation plan',
                'lesson_code': 'M01.L06',
                'section_id': 'evaluation-workflow',
                'placement': 'after_section',
                'description': 'Design an evaluation lifecycle for a production internal knowledge '
                               'assistant.',
                'instructions': '1. Describe the offline benchmark: which questions it contains and how answers are scored.\n'
                                '2. Define the release gate a change must pass before deployment.\n'
                                '3. Describe online sampling and how user feedback is collected.\n'
                                '4. Explain how and how often the benchmark is updated with new failures.',
                'expected_output': 'A concise plan covering offline benchmark, release gate, '
                                   'online sampling, feedback, and benchmark updates.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-evaluation', 'analysis']}],
 'quiz': {'id': 'M01.L06.QUIZ',
          'title': 'Evaluating Your RAG Application — Lesson Quiz',
          'lesson_code': 'M01.L06',
          'placement': 'lesson_end',
          'questions': [{'type': 'mcq',
                         'section_id': 'offline-vs-online',
                         'question': 'Which statement best describes offline RAG evaluation?',
                         'options': ['It runs only after a user complains',
                                     'It is development-time evaluation used for deeper tuning and '
                                     'comparison',
                                     'It must evaluate every production request synchronously',
                                     'It measures only uptime'],
                         'correct': 1,
                         'explanation': 'Offline evaluation is primarily used during development '
                                        'and can afford deeper, more expensive analysis.'},
                        {'type': 'mcq',
                         'section_id': 'retrieval-failure-low-recall',
                         'question': 'A required chunk exists in the corpus but is not returned in '
                                     'top-k. What failure is this?',
                         'options': ['Low recall',
                                     'Low latency',
                                     'High precision',
                                     'Citation failure'],
                         'correct': 0,
                         'explanation': 'The retriever failed to surface relevant evidence that '
                                        'exists.'},
                        {'type': 'mcq',
                         'section_id': 'faithfulness-failure',
                         'question': 'A model accurately repeats a deadline from an outdated '
                                     'policy. Which diagnosis is most precise?',
                         'options': ['Unfaithful incorrectness',
                                     'Faithful incorrectness',
                                     'Low precision only',
                                     'Citation precision failure only'],
                         'correct': 1,
                         'explanation': 'The answer can be faithful to retrieved evidence while '
                                        'still being wrong because the source data is stale.'},
                        {'type': 'mcq',
                         'section_id': 'judge-pointwise-pairwise',
                         'question': 'Which judging setup directly compares two candidate '
                                     'responses?',
                         'options': ['Pointwise', 'Pairwise', 'Recall@k', 'HNSW'],
                         'correct': 1,
                         'explanation': 'Pairwise judging compares alternatives against one '
                                        'another.'},
                        {'type': 'mcq',
                         'section_id': 'judge-biases',
                         'question': 'What is verbosity bias in an LLM judge?',
                         'options': ['Preferring shorter answers regardless of quality',
                                     'Rewarding length or polished detail even when it does not '
                                     'improve correctness',
                                     'Failing to parse JSON',
                                     'Confusing recall with precision'],
                         'correct': 1,
                         'explanation': 'Judges may mistakenly associate longer answers with '
                                        'higher quality.'},
                        {'type': 'mcq',
                         'section_id': 'precision-at-k',
                         'question': 'Top-5 retrieval contains 4 relevant chunks. What is '
                                     'precision@5?',
                         'options': ['0.2', '0.4', '0.8', '1.25'],
                         'correct': 2,
                         'explanation': '4 relevant results divided by 5 retrieved results equals '
                                        '0.8.'},
                        {'type': 'mcq',
                         'section_id': 'recall-at-k',
                         'question': 'Five relevant chunks exist, and 3 appear in top-k. What is '
                                     'recall@k?',
                         'options': ['0.3', '0.5', '0.6', '1.67'],
                         'correct': 2,
                         'explanation': 'Recall is 3/5 = 0.6.'},
                        {'type': 'mcq',
                         'section_id': 'mrr',
                         'question': 'Which retrieval metric focuses on the rank of the first '
                                     'relevant result?',
                         'options': ['MRR', 'F1', 'Recall@k', 'Citation precision'],
                         'correct': 0,
                         'explanation': 'MRR is built from the reciprocal rank of the first '
                                        'relevant result.'},
                        {'type': 'mcq',
                         'section_id': 'ndcg',
                         'question': 'Which metric naturally supports graded relevance levels?',
                         'options': ['MRR', 'nDCG', 'Exact-match accuracy', 'Uptime'],
                         'correct': 1,
                         'explanation': 'nDCG can use multi-level relevance judgments and '
                                        'discounts lower ranks.'},
                        {'type': 'mcq',
                         'section_id': 'umbrela',
                         'question': 'What is the central benefit of UMBRELA-style retrieval '
                                     'evaluation?',
                         'options': ['It guarantees full-corpus recall',
                                     'It can score returned passage relevance without manually '
                                     'maintained golden chunks',
                                     'It removes all LLM cost',
                                     'It measures only latency'],
                         'correct': 1,
                         'explanation': 'UMBRELA replaces static relevance labels for returned '
                                        'chunks with LLM-based relevance judging.'},
                        {'type': 'mcq',
                         'section_id': 'autonuggetizer',
                         'question': 'What problem does AutoNuggetizer primarily help measure?',
                         'options': ['GPU utilization',
                                     'Context utilization and coverage of important facts',
                                     'Vector index memory only',
                                     'API authentication'],
                         'correct': 1,
                         'explanation': 'It decomposes evidence into nuggets and checks whether '
                                        'the generated answer covers them.'},
                        {'type': 'mcq',
                         'section_id': 'citation-accuracy',
                         'question': 'What does citation precision ask?',
                         'options': ['How many citations fit in the prompt',
                                     'Whether the cited source actually supports the associated '
                                     'claim',
                                     'Whether retrieval latency is below 300 ms',
                                     'Whether users click citations'],
                         'correct': 1,
                         'explanation': 'Citation precision measures correct attribution of claims '
                                        'to supporting evidence.'},
                        {'type': 'mcq',
                         'section_id': 'offline-gates',
                         'question': 'What is the purpose of an evaluation gate in CI/CD?',
                         'options': ['To make every model deterministic',
                                     'To stop releases that regress critical quality or system '
                                     'metrics',
                                     'To remove human feedback',
                                     'To increase top-k automatically'],
                         'correct': 1,
                         'explanation': 'An evaluation gate converts minimum quality requirements '
                                        'into release criteria.'},
                        {'type': 'mcq',
                         'section_id': 'online-eval',
                         'question': 'Why is asynchronous online evaluation attractive?',
                         'options': ['It eliminates all evaluation cost',
                                     'It avoids adding judge latency to the user response path',
                                     'It guarantees golden answers exist',
                                     'It makes retrieval deterministic'],
                         'correct': 1,
                         'explanation': 'Out-of-band evaluation preserves the user experience '
                                        'while still measuring production behavior.'},
                        {'type': 'mcq',
                         'section_id': 'latency-throughput',
                         'question': 'Why track P95 latency in addition to average latency?',
                         'options': ['P95 measures retrieval precision',
                                     'Average latency can hide a bad tail experienced by some '
                                     'users',
                                     'P95 replaces uptime',
                                     'P95 is always lower than average'],
                         'correct': 1,
                         'explanation': 'Tail latency reveals slow experiences hidden by the '
                                        'mean.'},
                        {'type': 'mcq',
                         'section_id': 'human-feedback',
                         'question': 'Which is the strongest use of thumbs-up/down feedback?',
                         'options': ['Store only the global percentage',
                                     'Connect it to the full interaction trace and analyze '
                                     'failures by topic and root cause',
                                     'Use it instead of all automated evaluation',
                                     'Delete low-rated queries'],
                         'correct': 1,
                         'explanation': 'Feedback becomes actionable when linked to query, '
                                        'contexts, answer, and metadata.'},
                        {'type': 'mcq',
                         'section_id': 'judge-production',
                         'question': 'What is evaluation drift?',
                         'options': ['A vector moving in embedding space',
                                     'Scores changing because the evaluation model/rubric changed '
                                     'rather than because the RAG system changed',
                                     'A cache miss',
                                     'A document version update'],
                         'correct': 1,
                         'explanation': 'Changing the yardstick can create apparent quality '
                                        'changes unrelated to the evaluated system.'},
                        {'type': 'open',
                         'section_id': 'evaluation-workflow',
                         'question': 'Design a minimal but production-ready RAG evaluation program '
                                     'for an internal enterprise assistant. Explain the offline '
                                     'benchmark, retrieval and generation metrics, CI/CD gate, '
                                     'online sampling strategy, user-feedback loop, and system '
                                     'metrics you would track.',
                         'expected_points': ['stage-specific diagnosis',
                                             'offline and online evaluation',
                                             'retrieval and generation metrics',
                                             'release gate',
                                             'sampled asynchronous production evaluation',
                                             'human feedback',
                                             'latency uptime and cost']}],
          'passing_score': 70}}
