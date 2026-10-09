"""M01.L04 — Deploying RAG to Production.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 4, pages not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L04"

MODULE_ORDER = 1

MODULE_TITLE = "RAG Foundations"

MODULE_DESCRIPTION = (
    "Move a RAG proof of concept into a production-ready system with measurable quality, "
    "low latency, strong security, scalable architecture, cost controls, and continuous operations."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {'title': 'Deploying RAG to Production',
 'slug': 'rag-foundations-m01-l04',
 'description': 'A production-engineering lesson on moving RAG from a proof of concept to a '
                'scalable, secure, low-latency, observable, cost-controlled, continuously '
                'evaluated enterprise system.',
 'order': 4,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 11.5,
 'skill_tags': ['rag',
                'production-rag',
                'microservices',
                'latency',
                'autoscaling',
                'semantic-cache',
                'cache-invalidation',
                'security',
                'privacy',
                'rbac',
                'pii-redaction',
                'observability',
                'vendor-management',
                'tco',
                'model-routing',
                'rag-evaluation',
                'production-architecture',
                'deployment',
                'module-01'],
 'prerequisite_ids': ['M01.L01', 'M01.L02', 'M01.L03'],
 'lesson': {'title': 'Deploying RAG to Production',
            'content': '# Deploying RAG to Production\n'
                       '\n'
                       '> **Course:** Retrieval-Augmented Generation (RAG)  \n'
                       '\n'
                       '> **Lesson:** M01.L04  \n'
                       '\n'
                       '> **Module:** RAG Foundations  \n'
                       '\n'
                       '> **Source alignment:** Supplied source, Chapter 4. Page numbers were not '
                       'provided in the supplied source. This lesson is an instructor-authored '
                       'curriculum adaptation rather than a reproduction of the source text.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Learning outcomes\n'
                       '\n'
                       'By the end of this lesson, you should be able to:\n'
                       '\n'
                       '- Explain why a successful RAG proof of concept still requires major '
                       'architectural work before production.\n'
                       '\n'
                       '- Diagnose poor RAG responses by separating data-coverage, retrieval, '
                       'generation, and prompt failures.\n'
                       '\n'
                       '- Design staging verification for safe knowledge-base updates.\n'
                       '\n'
                       '- Build an end-to-end latency budget and reason about tail latency.\n'
                       '\n'
                       '- Explain fan-out/gather retrieval and independent microservice '
                       'auto-scaling.\n'
                       '\n'
                       '- Choose among model, indexing, inference, and caching strategies for '
                       'reducing latency.\n'
                       '\n'
                       '- Design exact and semantic caching with safe invalidation, eviction, and '
                       'horizontal scaling.\n'
                       '\n'
                       '- Apply defense-in-depth security across ingestion, data stores, '
                       'retrieval, and generation.\n'
                       '\n'
                       '- Explain typed masking, RBAC filtering, provider data-leakage risks, and '
                       'on-premises generation choices.\n'
                       '\n'
                       '- Evaluate vendor integrations using API, security, performance, SLA, '
                       'monitoring, and support criteria.\n'
                       '\n'
                       '- Map the interdisciplinary team skills required to operate RAG in '
                       'production.\n'
                       '\n'
                       '- Build a total-cost-of-ownership model and implement cost alerts, rate '
                       'limits, and model routing.\n'
                       '\n'
                       '- Interpret a reference production architecture for both ingestion and '
                       'query flow.\n'
                       '\n'
                       '- Translate POC lessons into measurable production KPIs and readiness '
                       'requirements.\n'
                       '\n'
                       '- Use monitoring, tracing, user feedback, and evaluation to operate and '
                       'continuously improve a deployed RAG system.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 1. From a RAG proof of concept to a production system\n'
                       '\n'
                       'A proof of concept answers a narrow question: **can this idea work well '
                       'enough to be useful?** A production system must answer a much harder set '
                       'of questions at the same time: can it stay accurate when the corpus grows, '
                       'remain responsive under load, protect private data, recover from failures, '
                       'integrate with enterprise systems, and stay affordable over months or '
                       'years?\n'
                       '\n'
                       'That difference changes the engineering mindset. A POC may be a notebook '
                       'or a small service with one vector database and one LLM endpoint. A '
                       'production RAG application is usually a distributed system with explicit '
                       'operational responsibilities.\n'
                       '\n'
                       '```text\n'
                       'POC mindset\n'
                       '    retrieve → generate → demo\n'
                       '\n'
                       'Production mindset\n'
                       '    ingest safely\n'
                       '        ↓\n'
                       '    retrieve accurately\n'
                       '        ↓\n'
                       '    generate faithfully\n'
                       '        ↓\n'
                       '    enforce security + guardrails\n'
                       '        ↓\n'
                       '    observe latency + quality + cost\n'
                       '        ↓\n'
                       '    recover, upgrade, and scale continuously\n'
                       '```\n'
                       '\n'
                       "The chapter's core message is that production readiness comes mostly from "
                       'rigorous system design, software engineering, DevOps/MLOps, security, and '
                       'organizational discipline—not from adding one more RAG trick.\n'
                       '\n'
                       '[[IMAGE_NEEDED: POC-to-production RAG transition | A side-by-side diagram '
                       'showing a small POC stack on the left and a distributed production stack '
                       'with security, monitoring, scaling, staging, and CI/CD on the right | '
                       'Learner should notice that production adds operational systems around the '
                       'same core RAG logic]]\n'
                       '\n'
                       '{{exercise:M01.L04.EX01}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 2. The production quality pillars\n'
                       '\n'
                       'The chapter groups the production challenge into several recurring '
                       'concerns: response quality, hallucinations, latency, security and privacy, '
                       'integration complexity, team expertise, total cost of ownership, '
                       'evaluation, and ongoing operations.\n'
                       '\n'
                       'These concerns interact. Improving response quality may require a reranker '
                       'or a larger LLM, which can increase latency and cost. Increasing security '
                       'may require redaction or stricter filtering, which can remove useful '
                       'context. Caching may reduce latency but create freshness problems if '
                       'invalidation is weak.\n'
                       '\n'
                       'A production architecture therefore needs explicit priorities and '
                       'measurable constraints. Instead of saying “make the RAG system better,” '
                       'define which quality dimensions matter and what acceptable operating '
                       'bounds look like.\n'
                       '\n'
                       'A useful mental model is:\n'
                       '\n'
                       '```text\n'
                       'response quality\n'
                       '↕\n'
                       'latency ↔ cost\n'
                       '↕\n'
                       'security / privacy\n'
                       '↕\n'
                       'availability / maintainability\n'
                       '```\n'
                       '\n'
                       'No production decision is isolated from the rest of the system.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 3. Diagnosing poor response quality\n'
                       '\n'
                       'When a RAG response is poor, the final LLM is not automatically the '
                       'culprit. The chapter identifies four major failure sources:\n'
                       '\n'
                       '1. the knowledge base does not contain the needed information;\n'
                       '2. the retrieval pipeline fails to select the right evidence;\n'
                       '3. the LLM generates unfaithfully even when the evidence is correct;\n'
                       '4. the prompt does not sufficiently constrain or guide the model.\n'
                       '\n'
                       'This creates a practical debugging order. First ask whether the answer is '
                       'present in the source data. Then inspect what was retrieved. Only after '
                       'that should you focus on the generator and prompt.\n'
                       '\n'
                       '```text\n'
                       'bad answer\n'
                       '   |\n'
                       '   +-- Is the required source data present?\n'
                       '   |      └─ no → data coverage problem\n'
                       '   |\n'
                       '   +-- Was the right evidence retrieved?\n'
                       '   |      └─ no → retrieval problem\n'
                       '   |\n'
                       '   +-- Did the LLM use the evidence faithfully?\n'
                       '   |      └─ no → generation / hallucination problem\n'
                       '   |\n'
                       '   └-- Did the prompt clearly define behavior?\n'
                       '          └─ no → prompt design problem\n'
                       '```\n'
                       '\n'
                       'This failure tree prevents teams from wasting time tuning prompts when the '
                       'real issue is missing or badly retrieved data.\n'
                       '\n'
                       '[[IMAGE_NEEDED: RAG response-quality failure tree | Decision tree from a '
                       'bad answer through data coverage, retrieval, generation faithfulness, and '
                       'prompt design | Learner should notice the recommended debugging order and '
                       'that not every bad answer is an LLM problem]]\n'
                       '\n'
                       '{{exercise:M01.L04.EX02}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 4. Failure reason 1: the system has no relevant data\n'
                       '\n'
                       'A RAG system cannot ground an answer in knowledge that does not exist in '
                       'its corpus. The chapter illustrates this with two examples: a TV support '
                       'system missing a manual for a particular model, and an investment research '
                       'system that has evidence for one company but no filings or internal '
                       'research for another company in a comparative question.\n'
                       '\n'
                       'The danger is subtle. Retrieval usually returns *something* even when the '
                       'correct information is absent. Those chunks can look topically related, '
                       'and the LLM may still produce a fluent answer from irrelevant evidence.\n'
                       '\n'
                       'Production systems therefore need a way to distinguish:\n'
                       '\n'
                       '- “the retriever found relevant evidence,” from\n'
                       '- “the retriever merely found the closest available chunks.”\n'
                       '\n'
                       'This is why query logging, response-quality monitoring, and corpus '
                       'coverage analysis matter. Missing-data failures should become ingestion '
                       'tasks rather than prompt-tuning tasks.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 5. Promote new knowledge through a staging index\n'
                       '\n'
                       'In a POC, it may be tempting to rerun an ingestion script directly against '
                       'the live vector database whenever new documents arrive. In production, '
                       "that can damage every user's results if the new ingestion introduces "
                       'malformed text, broken encoding, incorrect metadata, or other processing '
                       'defects.\n'
                       '\n'
                       'The chapter recommends a staging-verification workflow:\n'
                       '\n'
                       '```text\n'
                       'new / updated documents\n'
                       '        ↓\n'
                       'staging collection\n'
                       '        ↓\n'
                       'retrieval tests + format checks\n'
                       '        ↓ pass\n'
                       'production collection\n'
                       '```\n'
                       '\n'
                       'The staging collection can be a subset or a clone of production. Automated '
                       'retrieval tests should verify that newly ingested documents are searchable '
                       'and represented correctly before promotion.\n'
                       '\n'
                       'This is the retrieval equivalent of validating a software release before '
                       'deploying it to production.\n'
                       '\n'
                       '{{exercise:M01.L04.EX03}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 6. Subject-matter experts and source-of-truth control\n'
                       '\n'
                       'Document presence alone is not enough. Enterprise repositories often '
                       'contain old policies, duplicates, drafts, superseded versions, or '
                       'documents whose authority is unclear.\n'
                       '\n'
                       'Subject-matter experts (SMEs) are important because they can identify '
                       'which documents are valid sources of truth and which should be excluded or '
                       'removed. This is especially important when old and new versions conflict: '
                       'a technically perfect retriever can still return the wrong policy if both '
                       'versions remain available without adequate metadata or governance.\n'
                       '\n'
                       'Production data quality therefore includes **semantic governance**: '
                       'knowing not only how to parse a file, but whether the organization should '
                       'trust that file at all.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 7. Failure reason 2: the retrieval pipeline is too weak\n'
                       '\n'
                       'A simple semantic vector search often performs well in a small POC because '
                       'there are relatively few competing chunks. Production corpora are larger '
                       'and noisier, which makes accurate top-k retrieval harder.\n'
                       '\n'
                       'At scale, the retrieval layer may need metadata filters, hybrid '
                       'semantic-plus-lexical search, relevance reranking, diversity reranking, '
                       'and distributed storage. The more data grows, the more important index '
                       'design, consistency, fault tolerance, and low-latency access become.\n'
                       '\n'
                       'The chapter summarizes this with a familiar principle: **garbage in, '
                       'garbage out**. If the evidence sent to the LLM is incomplete or '
                       'misleading, generation quality will decline even if the LLM itself is '
                       'strong.\n'
                       '\n'
                       '{{exercise:M01.L04.EX04}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 8. Failure reason 3: the LLM is not faithful to good evidence\n'
                       '\n'
                       'Even when retrieval is correct, the generator can still produce '
                       'unsupported claims. The model may misunderstand evidence, combine facts '
                       'incorrectly, use internal parametric knowledge instead of the retrieved '
                       'context, or fill gaps when the retrieved evidence only partially answers '
                       'the query.\n'
                       '\n'
                       'This means factual quality is not binary. A response can contain a mixture '
                       'of supported and unsupported statements—a spectrum of factuality.\n'
                       '\n'
                       'A production design should therefore consider both:\n'
                       '\n'
                       '- choosing an LLM with strong grounded-generation behavior; and\n'
                       '- implementing hallucination detection or correction controls when the '
                       'application requires high trust.\n'
                       '\n'
                       'The key diagnostic question is: **does each important factual claim follow '
                       'from the retrieved evidence?**\n'
                       '\n'
                       '{{exercise:M01.L04.EX05}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 9. Failure reason 4: production prompt engineering\n'
                       '\n'
                       'A minimal RAG prompt may simply insert context and ask the model to '
                       'answer. The chapter shows how a small instruction can materially improve '
                       'behavior: explicitly tell the model to admit when the answer cannot be '
                       'found rather than inventing one.\n'
                       '\n'
                       'An adapted production-oriented prompt might look like:\n'
                       '\n'
                       '```text\n'
                       "Use the supplied context to answer the user's question.\n"
                       'If the context does not support an answer, say that you do not know.\n'
                       'Do not invent missing facts.\n'
                       '\n'
                       '<context>\n'
                       '{context}\n'
                       '</context>\n'
                       '\n'
                       '<question>\n'
                       '{question}\n'
                       '</question>\n'
                       '```\n'
                       '\n'
                       'The important point is not one exact wording. It is that production '
                       'prompts define behavior for uncertainty and edge cases. Prompt changes '
                       'should be evaluated over many representative queries because an '
                       'instruction that helps one case can affect others.\n'
                       '\n'
                       'Prompt engineering also contributes to prompt-injection defense, so prompt '
                       'design belongs to both quality engineering and security engineering.\n'
                       '\n'
                       '{{exercise:M01.L04.EX06}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 10. Designing an end-to-end latency budget\n'
                       '\n'
                       'Production users expect a response within a small number of seconds. The '
                       'chapter suggests a retrieval target on the order of a few hundred '
                       'milliseconds, while generation can take several seconds depending on the '
                       'model and whether additional reasoning or hallucination checks are used.\n'
                       '\n'
                       'The exact values are less important than the budgeting method. Break the '
                       'request into stages:\n'
                       '\n'
                       '```text\n'
                       'query embedding\n'
                       '+ vector / lexical retrieval\n'
                       '+ result fusion\n'
                       '+ reranking\n'
                       '+ context fetch\n'
                       '+ LLM generation\n'
                       '+ optional guardrails / hallucination checks\n'
                       '= end-to-end latency\n'
                       '```\n'
                       '\n'
                       'If every stage is optimized independently without an end-to-end budget, '
                       'total latency can still become unacceptable.\n'
                       '\n'
                       'The production team should measure each component separately and trace '
                       'individual requests through the full pipeline.\n'
                       '\n'
                       '{{exercise:M01.L04.EX07}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 11. Average latency is not enough: watch the tail\n'
                       '\n'
                       'A system can have a reasonable average response time while still '
                       'frustrating many users. The chapter therefore emphasizes tail latency, '
                       'such as the 95th percentile.\n'
                       '\n'
                       'If the average request takes three seconds but a meaningful fraction takes '
                       'ten or more, users experience the slow tail directly. Tail latency often '
                       'reveals overload, slow database paths, large candidate sets, cold model '
                       'instances, or unusually expensive queries.\n'
                       '\n'
                       'Production monitoring should therefore include a latency distribution '
                       'rather than a single mean:\n'
                       '\n'
                       '```text\n'
                       'P50 → typical request\n'
                       'P95 → slow experience seen by a significant minority\n'
                       'P99 → extreme tail / incident signal\n'
                       '```\n'
                       '\n'
                       'The chapter uses P95/P99 latency as an important criterion when evaluating '
                       'vendors as well.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 12. Parallel fan-out/gather retrieval\n'
                       '\n'
                       'Sequentially running semantic search and lexical search makes their '
                       'latencies add together. The chapter recommends a decoupled architecture '
                       'with a stateless orchestrator that fans out independent work in parallel.\n'
                       '\n'
                       '```text\n'
                       '                    ┌─ vector search ─┐\n'
                       'query → orchestrator                  ├→ gather → reranker → LLM\n'
                       '                    └─ lexical search ┘\n'
                       '```\n'
                       '\n'
                       'With this pattern, retrieval time is approximately controlled by the '
                       'slower branch rather than the sum of both branches.\n'
                       '\n'
                       'The orchestrator coordinates the request but does not need to perform '
                       'every heavy operation itself. This keeps orchestration lightweight and '
                       'allows retrieval services, model services, and databases to evolve '
                       'independently.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Fan-out/gather RAG query architecture | Diagram showing an '
                       'orchestrator calling semantic and lexical search in parallel, gathering '
                       'candidates, reranking, then calling the LLM | Learner should notice that '
                       'parallel independent work reduces additive latency]]\n'
                       '\n'
                       '{{exercise:M01.L04.EX08}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 13. Scale each microservice according to its bottleneck\n'
                       '\n'
                       'A major advantage of decoupled services is independent auto-scaling. '
                       'Different parts of RAG consume different resources:\n'
                       '\n'
                       '- the orchestrator is primarily CPU/API work;\n'
                       '- databases are I/O and memory intensive;\n'
                       '- embedding and reranking models may need accelerators;\n'
                       '- LLM inference can be GPU intensive and expensive.\n'
                       '\n'
                       'Scaling every component together wastes resources. Instead, each service '
                       'should scale based on the metric that reflects its bottleneck—for example '
                       'CPU utilization, database connections, queue depth, or in-flight GPU '
                       'requests.\n'
                       '\n'
                       'This architecture turns RAG scaling into several smaller capacity-planning '
                       'problems rather than one monolithic deployment problem.\n'
                       '\n'
                       '{{exercise:M01.L04.EX09}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 14. Using smaller or alternative LLMs in production\n'
                       '\n'
                       'A POC may use a frontier LLM because it is easy to access and maximizes '
                       'initial quality. Production requirements can change that choice. A smaller '
                       'or faster model may reduce latency and cost enough to be preferable if it '
                       'preserves required answer quality.\n'
                       '\n'
                       'The chapter warns that changing the model can alter output quality, so the '
                       'decision must be validated with RAG evaluation rather than intuition.\n'
                       '\n'
                       'This gives a general rule:\n'
                       '\n'
                       '> **Model selection is an empirical system decision, not a prestige '
                       'decision.**\n'
                       '\n'
                       'Choose the smallest/fastest option that still satisfies the production '
                       'quality requirement for the target workload.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 15. Software and hardware acceleration for model services\n'
                       '\n'
                       'When embedding, reranking, or generation models are hosted by your own '
                       'infrastructure, production performance depends on both hardware and '
                       'serving software.\n'
                       '\n'
                       'The chapter points to powerful GPUs and optimized inference servers such '
                       'as vLLM, TensorRT-LLM, and Text Generation Inference. The important '
                       'production idea is that the serving layer implements optimizations needed '
                       'for concurrency and long-context workloads, such as batching and '
                       'memory-efficient attention handling.\n'
                       '\n'
                       'A raw model checkpoint is not a production inference service. Production '
                       'model serving needs scheduling, concurrency handling, resource '
                       'utilization, and observability around the model.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 16. Efficient indexing is a latency prerequisite\n'
                       '\n'
                       'Fast query orchestration cannot compensate for poorly indexed storage.\n'
                       '\n'
                       'For semantic retrieval, the chapter recommends approximate '
                       'nearest-neighbor indexes such as HNSW or IVFPQ when running a local vector '
                       'database. For lexical retrieval, systems such as Elasticsearch or '
                       'OpenSearch need suitable sharding and analyzers.\n'
                       '\n'
                       'The core design principle is straightforward: **index design determines '
                       'whether storage can satisfy the latency budget under production scale.**\n'
                       '\n'
                       'Index configuration must be validated on the real corpus size and query '
                       'load. A design that appears fast in memory on POC data may perform very '
                       'differently with the production corpus.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 17. Caching at multiple layers of the RAG pipeline\n'
                       '\n'
                       'Caching can bypass expensive computation, but the best cache location '
                       'depends on what work is repeated.\n'
                       '\n'
                       'The chapter identifies three layers:\n'
                       '\n'
                       '| Cache | Key idea | Work avoided |\n'
                       '|---|---|---|\n'
                       '| Full response cache | reuse a prior final answer | almost the entire RAG '
                       'pipeline |\n'
                       '| Retrieval cache | reuse the candidate chunks for a similar query | '
                       'vector/lexical retrieval and fusion |\n'
                       '| Chunk cache | reuse chunk text after IDs are known | slower '
                       'document-store reads |\n'
                       '\n'
                       'These layers are complementary rather than mutually exclusive.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Multi-level RAG caching | Layered diagram showing '
                       'full-response, retrieval, and chunk caches around the orchestrator and '
                       'retrieval services | Learner should notice that each cache skips a '
                       'different amount of downstream work]]\n'
                       '\n'
                       '{{exercise:M01.L04.EX10}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 18. Why semantic caching fits natural-language queries\n'
                       '\n'
                       'Exact string caching works poorly when users ask the same question with '
                       'different wording. The chapter therefore introduces semantic caching: '
                       'embed the incoming query, compare it with embeddings of cached queries, '
                       'and reuse a result if similarity exceeds a threshold.\n'
                       '\n'
                       'Conceptually:\n'
                       '\n'
                       '```text\n'
                       'incoming query\n'
                       '   ↓ embed\n'
                       'query vector\n'
                       '   ↓ similarity search over cached query vectors\n'
                       'similar enough?\n'
                       '   ├─ yes → reuse cached result\n'
                       '   └─ no  → run retrieval and cache result\n'
                       '```\n'
                       '\n'
                       'This can increase cache hit rates for natural-language systems because '
                       'meaning, not exact wording, determines reuse.\n'
                       '\n'
                       'The similarity threshold is important. A threshold that is too low can '
                       'reuse an answer for a meaningfully different question. A threshold that is '
                       'too high behaves more like exact matching and loses much of the benefit.\n'
                       '\n'
                       '{{exercise:M01.L04.EX11}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 19. Worked implementation: a semantic cached retriever\n'
                       '\n'
                       'The source includes a retriever wrapper that stores previous query '
                       'embeddings and retrieval results. The core logic can be reduced to three '
                       'operations:\n'
                       '\n'
                       '```python\n'
                       'def retrieve(query):\n'
                       '    q_vec = embeddings.embed_query(query)\n'
                       '\n'
                       '    match = find_cached_vector_above_threshold(q_vec)\n'
                       '    if match:\n'
                       '        return match.documents\n'
                       '\n'
                       '    docs = base_retriever.invoke(query)\n'
                       '    cache.store(query_vector=q_vec, documents=docs)\n'
                       '    return docs\n'
                       '```\n'
                       '\n'
                       'The production lesson is in the control flow, not the exact class '
                       'implementation:\n'
                       '\n'
                       '1. embed once;\n'
                       '2. search the semantic cache;\n'
                       '3. return immediately on a safe hit;\n'
                       '4. otherwise execute retrieval;\n'
                       '5. persist enough information to serve future equivalent queries.\n'
                       '\n'
                       'The cache must also record enough lineage to know which documents a cached '
                       'result depended on; otherwise targeted invalidation becomes difficult.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 20. Cache invalidation is the hard part\n'
                       '\n'
                       'A cache can make a RAG system fast and wrong at the same time.\n'
                       '\n'
                       'If a policy document changes but a cached answer still reflects the old '
                       'policy, the cache defeats the freshness guarantees of the retrieval '
                       'system. The chapter recommends event-driven invalidation rather than '
                       'relying only on time-to-live expiration.\n'
                       '\n'
                       'A robust pattern is:\n'
                       '\n'
                       '```text\n'
                       'document update\n'
                       '     ↓\n'
                       'ingestion pipeline\n'
                       '     ↓ publish change event\n'
                       'Redis Pub/Sub / Kafka\n'
                       '     ↓\n'
                       'cache subscriber\n'
                       '     ↓\n'
                       'purge entries affected by that document\n'
                       '```\n'
                       '\n'
                       'This requires cache entries to carry dependency information or other '
                       'identifiers that make targeted invalidation possible.\n'
                       '\n'
                       '{{exercise:M01.L04.EX12}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 21. Eviction and horizontal scaling for production caches\n'
                       '\n'
                       'Two additional cache problems appear at scale.\n'
                       '\n'
                       '**Eviction:** RAM is finite, so the cache needs a policy such as least '
                       'recently used (LRU) to remove older entries.\n'
                       '\n'
                       '**Horizontal scaling:** one cache server may not provide enough memory or '
                       'throughput, so production systems may need clustering or sharding.\n'
                       '\n'
                       'The production lesson is that a semantic cache is a distributed data '
                       'system, not just a Python dictionary. Capacity, consistency, invalidation, '
                       'and failure behavior all need explicit design.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 22. Security and privacy require defense in depth\n'
                       '\n'
                       'The chapter organizes production RAG security around three major attack '
                       'surfaces:\n'
                       '\n'
                       '1. ingestion;\n'
                       '2. vector/lexical/graph data stores;\n'
                       '3. generation and output.\n'
                       '\n'
                       'Security controls must protect data both while it is moving and while it '
                       'is stored. Permissions must survive the transformation from source '
                       'documents to chunks, vectors, metadata, prompts, and generated answers.\n'
                       '\n'
                       '[[IMAGE_NEEDED: RAG defense-in-depth security layers | Diagram showing '
                       'ingestion security, encrypted data stores with RBAC, permission-filtered '
                       'retrieval, protected LLM generation, and monitored output | Learner should '
                       'notice that security constraints must persist across every '
                       'transformation]]\n'
                       '\n'
                       '{{exercise:M01.L04.EX13}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 23. Secure the ingestion layer end to end\n'
                       '\n'
                       'The ingestion pipeline is an ETL pipeline and should be treated like '
                       'critical data infrastructure.\n'
                       '\n'
                       'The chapter calls for standard encryption during movement from source '
                       'systems through extraction, specialized table/image handling, chunking, '
                       'embedding, and final storage. A secure architecture should not create an '
                       'unprotected intermediate stage simply because the data is “inside” the RAG '
                       'pipeline.\n'
                       '\n'
                       'This matters because sensitive source content may be duplicated into '
                       'several forms:\n'
                       '\n'
                       '```text\n'
                       'original document\n'
                       '→ extracted text\n'
                       '→ chunks\n'
                       '→ metadata\n'
                       '→ embeddings\n'
                       '→ indexes\n'
                       '```\n'
                       '\n'
                       'Each representation needs appropriate controls.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 24. PII/PHI redaction can damage answer quality\n'
                       '\n'
                       'Masking sensitive data can protect privacy but can also destroy '
                       'relationships that the model needs to understand.\n'
                       '\n'
                       'If every person, medication, and patient name is replaced by an '
                       'undifferentiated placeholder, the sentence structure may remain readable '
                       'while the semantic roles disappear.\n'
                       '\n'
                       'The chapter therefore presents **entity-aware redaction (typed masking)** '
                       'as a stronger strategy. Replace a sensitive value with its category:\n'
                       '\n'
                       '```text\n'
                       'specific doctor name    → [DOCTOR_NAME]\n'
                       'specific medication     → [MEDICATION]\n'
                       'specific patient name   → [PATIENT_NAME]\n'
                       '```\n'
                       '\n'
                       'This hides the value while preserving the fact that a doctor prescribed a '
                       'medication to a patient.\n'
                       '\n'
                       'The engineering goal is not maximum deletion. It is the minimum '
                       "information exposure consistent with the application's purpose.\n"
                       '\n'
                       '{{exercise:M01.L04.EX14}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 25. Worked implementation: entity-aware redaction\n'
                       '\n'
                       'The source demonstrates typed masking with Microsoft Presidio. The adapted '
                       'workflow is:\n'
                       '\n'
                       '```python\n'
                       'from presidio_analyzer import AnalyzerEngine\n'
                       'from presidio_anonymizer import AnonymizerEngine\n'
                       '\n'
                       'analyzer = AnalyzerEngine()\n'
                       'anonymizer = AnonymizerEngine()\n'
                       '\n'
                       'entities = analyzer.analyze(\n'
                       '    text=input_text,\n'
                       '    entities=["PERSON", "PHONE_NUMBER"],\n'
                       '    language="en",\n'
                       ')\n'
                       '\n'
                       'safe_text = anonymizer.anonymize(\n'
                       '    text=input_text,\n'
                       '    analyzer_results=entities,\n'
                       '    # configure replacements such as <PERSON> and <PHONE_NUMBER>\n'
                       ').text\n'
                       '```\n'
                       '\n'
                       'The important design steps are:\n'
                       '\n'
                       '1. detect sensitive entities;\n'
                       '2. classify their type;\n'
                       '3. replace values with typed tokens;\n'
                       '4. verify that downstream retrieval still works;\n'
                       '5. log/redact safely so the privacy control itself does not leak the '
                       'original value.\n'
                       '\n'
                       'Redaction belongs early enough in the pipeline that sensitive content is '
                       'not unnecessarily copied into downstream stores.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 26. Provenance and integrity tracking\n'
                       '\n'
                       'The chapter notes that organizations with provenance requirements may need '
                       'to prove that data was not silently altered.\n'
                       '\n'
                       'Hash-based tracking can create a digital fingerprint of data at important '
                       'stages of the RAG pipeline. The purpose is not retrieval relevance; it is '
                       'auditability.\n'
                       '\n'
                       'A provenance record can answer questions such as:\n'
                       '\n'
                       '- which source document produced this chunk?\n'
                       '- which ingestion version processed it?\n'
                       '- has the content changed since it was approved?\n'
                       '- can an auditor verify the history?\n'
                       '\n'
                       'Production trust includes the ability to explain where data came from and '
                       'whether its lineage is intact.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 27. Data-store safeguards: encryption, minimization, and monitoring\n'
                       '\n'
                       'Vector stores do not contain “harmless math.” They commonly store both '
                       'embeddings and the corresponding text or metadata. Hybrid retrieval may '
                       'add a lexical store, and knowledge-graph systems add another repository.\n'
                       '\n'
                       'The chapter therefore applies normal enterprise data-security requirements '
                       'to all of them:\n'
                       '\n'
                       '- encryption at rest and in transit;\n'
                       '- RBAC;\n'
                       '- network security;\n'
                       '- data minimization;\n'
                       '- regular review and deletion of unnecessary data;\n'
                       '- monitoring and incident-response controls.\n'
                       '\n'
                       'Adding a new retrieval store adds a new security surface that must be '
                       'governed.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 28. Prevent data leaks with permission-aware retrieval\n'
                       '\n'
                       'An enterprise corpus often mixes documents with different access levels. '
                       'If retrieval ignores those permissions, RAG can expose confidential '
                       'information even if the underlying source systems were secure.\n'
                       '\n'
                       'The chapter recommends permission-based filtering in the query flow:\n'
                       '\n'
                       '```text\n'
                       'authenticated user\n'
                       '      ↓ roles / permissions\n'
                       'query → metadata filter\n'
                       '      ↓\n'
                       'only authorized chunks\n'
                       '      ↓\n'
                       'LLM prompt\n'
                       '```\n'
                       '\n'
                       'The important principle is that authorization must be enforced **before** '
                       'sensitive chunks are sent to the generator.\n'
                       '\n'
                       'This also means the ingestion process must preserve permission metadata '
                       'consistently enough for query-time enforcement.\n'
                       '\n'
                       '{{exercise:M01.L04.EX15}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 29. Data leakage risk when calling external LLM providers\n'
                       '\n'
                       'When a production RAG system sends retrieved internal text to an '
                       "externally hosted LLM, sensitive information leaves the organization's "
                       'controlled environment over a network call.\n'
                       '\n'
                       'The chapter treats this as a privacy and governance concern that must be '
                       'evaluated deliberately. Provider logging, retention, temporary caching, '
                       'and metadata handling can matter even when content is partly anonymized.\n'
                       '\n'
                       'For highly sensitive deployments, this requirement can influence '
                       'architecture more than model quality: the organization may prefer an '
                       'on-premises or private-cloud model so that retrieved data never leaves the '
                       'controlled environment.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 30. When on-premises or private-cloud generation becomes necessary\n'
                       '\n'
                       'The source explains that highly sensitive RAG systems may use openly '
                       'deployable models within a data center or VPC to reduce the risk of '
                       'sending proprietary context to an external service.\n'
                       '\n'
                       'This choice moves responsibility inward. The organization gains more '
                       'control over data location, but must now operate the inference stack, '
                       'including hardware, serving software, scaling, patching, and monitoring.\n'
                       '\n'
                       'Privacy architecture therefore changes the cost and operations '
                       'architecture as well.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 31. Generation guardrails in production\n'
                       '\n'
                       'The final LLM can still produce disallowed, biased, harmful, or otherwise '
                       'noncompliant output even when retrieval is protected.\n'
                       '\n'
                       'Production guardrails need logging and monitoring so violations can be '
                       'investigated rather than silently filtered. The chapter also recommends '
                       'giving users a way to report problematic responses, turning user feedback '
                       'into an operational signal.\n'
                       '\n'
                       'A mature guardrail system therefore includes:\n'
                       '\n'
                       '```text\n'
                       'policy\n'
                       '→ detection / filtering\n'
                       '→ logging\n'
                       '→ user reporting\n'
                       '→ incident review\n'
                       '→ rule/model improvement\n'
                       '```\n'
                       '\n'
                       'Safety is a maintained process, not a one-time prompt instruction.\n'
                       '\n'
                       '{{exercise:M01.L04.EX16}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 32. Vendor chaos and integration complexity\n'
                       '\n'
                       'Production RAG often accumulates components for content extraction, '
                       'table/image parsing, advanced retrieval, hallucination controls, security, '
                       'and knowledge graphs. Each additional subsystem introduces another API, '
                       'authentication method, output format, SLA, support channel, and failure '
                       'mode.\n'
                       '\n'
                       'The technical cost of a vendor is therefore larger than the invoice. '
                       'Integration, monitoring, security review, legal review, and support '
                       'coordination all consume engineering effort.\n'
                       '\n'
                       'The chapter describes the DIY result as potentially fragmented and brittle '
                       'when every connection is owned by the internal team.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 33. A disciplined vendor-evaluation checklist\n'
                       '\n'
                       'The chapter proposes evaluating new components across several dimensions.\n'
                       '\n'
                       '| Area | Questions to ask |\n'
                       '|---|---|\n'
                       '| API & integration | Is there a stable API/SDK? What are rate limits and '
                       'batch options? |\n'
                       '| Data & formats | What input/output formats are supported? Is '
                       'transformation required? |\n'
                       '| Security & compliance | How is data protected? How is PII handled? Which '
                       'compliance commitments exist? |\n'
                       '| Performance | What P95/P99 latency and scaling behavior are guaranteed? '
                       '|\n'
                       '| Reliability | What uptime SLA is provided? |\n'
                       '| Monitoring | Can the component integrate with your observability stack? '
                       '|\n'
                       '| Support | How are critical incidents handled and how fast is response? '
                       '|\n'
                       '| Change management | How are versions and upgrades introduced? |\n'
                       '\n'
                       'This checklist turns “does the product work?” into “can this subsystem '
                       'survive inside our production architecture?”\n'
                       '\n'
                       '{{exercise:M01.L04.EX17}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 34. Support coordination is an architectural cost\n'
                       '\n'
                       'A production incident can cross subsystem boundaries. A latency spike '
                       'might be caused by the vector database, reranker, model provider, network, '
                       'or orchestrator. If those pieces come from different vendors, the internal '
                       'team becomes the coordinator among several support organizations.\n'
                       '\n'
                       'This is one reason the chapter presents turnkey platforms as attractive: '
                       'one integrated provider can reduce the number of ownership boundaries.\n'
                       '\n'
                       'The trade-off is not simply DIY versus convenience. It is **internal '
                       'control and customization versus integration and accountability burden**.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 35. Production RAG is an interdisciplinary team problem\n'
                       '\n'
                       'RAG sits at the intersection of machine learning, data engineering, '
                       'software infrastructure, security, and domain knowledge.\n'
                       '\n'
                       'The chapter emphasizes that a successful team needs expertise across all '
                       'of these areas because production failures can originate anywhere in the '
                       'stack. A retriever quality problem, a GPU throughput problem, a broken ETL '
                       'job, and a privacy policy violation require different skills.\n'
                       '\n'
                       'The team must also keep learning because the underlying ecosystem changes '
                       'quickly.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 36. Machine-learning engineering responsibilities\n'
                       '\n'
                       'The chapter associates machine-learning engineering with:\n'
                       '\n'
                       '- embedding and reranking models;\n'
                       '- LLM inference and GPU choices;\n'
                       '- prompt engineering;\n'
                       '- hybrid retrieval;\n'
                       '- retrieval optimization;\n'
                       '- hallucination detection and correction;\n'
                       '- graph-related expertise if knowledge graphs are added.\n'
                       '\n'
                       'This role connects model behavior to measurable application quality and '
                       'performance.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 37. Data-engineering responsibilities\n'
                       '\n'
                       'Data engineering owns the scalable movement and transformation of '
                       'enterprise data: PDFs, databases, websites, collaboration systems, and '
                       'other sources.\n'
                       '\n'
                       'The work includes extraction, normalization, ingestion reliability, '
                       'refresh, and high availability. Poor data engineering creates stale or '
                       'malformed knowledge before the RAG-specific components ever see it.\n'
                       '\n'
                       'In production RAG, the ingestion pipeline is therefore a first-class '
                       'system, not preprocessing glue.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 38. DevOps/MLOps responsibilities\n'
                       '\n'
                       'The chapter highlights containerization, CI/CD, orchestration, GPU '
                       'optimization, auto-scaling, and monitoring as essential production '
                       'skills.\n'
                       '\n'
                       'These capabilities convert a working model pipeline into a service that '
                       'can be deployed repeatedly, observed under load, rolled back, patched, and '
                       'scaled.\n'
                       '\n'
                       'Without this layer, every model or retrieval improvement becomes risky to '
                       'ship.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 39. Security and compliance responsibilities\n'
                       '\n'
                       'Security expertise includes prompt-injection defense, PII redaction, data '
                       'governance, privacy controls, and auditability.\n'
                       '\n'
                       'The important organizational point is that these are not tasks to add '
                       'after development. They constrain architecture from ingestion through '
                       'generation and therefore must be represented in design decisions early.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 40. Build versus buy: spend internal talent on differentiation\n'
                       '\n'
                       'The chapter presents a practical alternative to building every RAG '
                       'component internally: use turnkey or managed services for '
                       'nondifferentiated infrastructure while applying internal expertise to '
                       'domain-specific requirements.\n'
                       '\n'
                       'This is not an automatic recommendation to outsource everything. It is a '
                       'resource-allocation question:\n'
                       '\n'
                       '```text\n'
                       'Is this component a strategic differentiator?\n'
                       '        ├─ yes → internal investment may be justified\n'
                       '        └─ no  → managed/turnkey may reduce integration and maintenance '
                       'burden\n'
                       '```\n'
                       '\n'
                       'The decision should consider quality, security, control, expertise, vendor '
                       'risk, support, and total cost.\n'
                       '\n'
                       '{{exercise:M01.L04.EX18}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 41. Total cost of ownership is larger than API spend\n'
                       '\n'
                       'Production budgeting must include the complete cost of running and '
                       'evolving the system, not only per-token LLM charges.\n'
                       '\n'
                       'The chapter separates direct costs from indirect and ongoing costs, and '
                       'also includes business-continuity and security requirements.\n'
                       '\n'
                       'A useful TCO model includes:\n'
                       '\n'
                       '```text\n'
                       'vendor services\n'
                       '+ retrieval infrastructure\n'
                       '+ CPU/GPU compute\n'
                       '+ storage\n'
                       '+ staging environments\n'
                       '+ monitoring / observability\n'
                       '+ integration work\n'
                       '+ security / compliance\n'
                       '+ support contracts\n'
                       '+ engineering staff\n'
                       '+ HA / disaster-recovery capacity\n'
                       '+ future growth\n'
                       '```\n'
                       '\n'
                       'This makes TCO an architecture input rather than an accounting '
                       'afterthought.\n'
                       '\n'
                       '{{exercise:M01.L04.EX19}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 42. Direct costs: vendors, retrieval, compute, and storage\n'
                       '\n'
                       'Direct expenses include vendor-managed models or services, the operational '
                       'cost of vector/lexical/reranking infrastructure, and compute/storage for '
                       'both staging and production.\n'
                       '\n'
                       'The chapter notes that each additional vendor also creates administrative '
                       'and lock-in risk. Retrieval costs may scale nonlinearly when larger '
                       'datasets also require low latency and high availability.\n'
                       '\n'
                       'The correct question is not “what is the cheapest component?” but “what '
                       'does this component cost at the scale, availability, and latency we '
                       'require?”\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 43. Indirect and ongoing costs\n'
                       '\n'
                       'Production systems require integration with enterprise software, ingestion '
                       'tooling, testing, DevOps, monitoring, privacy controls, maintenance, '
                       'support, and periodic upgrades.\n'
                       '\n'
                       'These costs grow as data volume, use cases, and query traffic grow.\n'
                       '\n'
                       'Because they are distributed across teams, indirect costs are easy to '
                       'underestimate. A system that looks inexpensive from its cloud bill may '
                       'still be costly to operate if it consumes significant engineering time.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 44. High availability and business continuity add real cost\n'
                       '\n'
                       'No production system is completely immune to failure. If the business '
                       'requires continuity during regional or infrastructure outages, the design '
                       'may need redundant deployments and automatic failover.\n'
                       '\n'
                       'The chapter uses multi-region architecture as an example. This improves '
                       'resilience but duplicates infrastructure and operational complexity.\n'
                       '\n'
                       'Availability requirements should therefore be defined before budgeting. '
                       '“Mission critical” is an architectural and financial requirement, not just '
                       'a label.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 45. Cost monitoring, budget alerts, and denial-of-wallet protection\n'
                       '\n'
                       'Auto-scaling compute and pay-per-token APIs can produce unexpectedly large '
                       'bills. The chapter recommends integrating usage and billing telemetry into '
                       'the primary monitoring system.\n'
                       '\n'
                       'Two important controls are:\n'
                       '\n'
                       '- **budget alerts** at predefined thresholds;\n'
                       '- **rate limiting** so a faulty service or malicious user cannot create '
                       'uncontrolled spend.\n'
                       '\n'
                       'The second control also defends against a denial-of-wallet pattern: a '
                       'system remains technically available but becomes financially unsustainable '
                       'because an attacker or bug triggers excessive expensive requests.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 46. Cascading models and LLM routing\n'
                       '\n'
                       'The chapter proposes a cascading model strategy to control cost.\n'
                       '\n'
                       '```text\n'
                       'query\n'
                       '  ↓\n'
                       'router\n'
                       '  ├─ simple / high-confidence → smaller, faster, cheaper model\n'
                       '  └─ complex / low-confidence → stronger, more expensive model\n'
                       '```\n'
                       '\n'
                       'The goal is to reserve expensive reasoning capacity for queries that need '
                       'it.\n'
                       '\n'
                       'A router must be observable. The production team should know how often '
                       'each route is selected, what quality each route achieves, and how much '
                       'each route costs. Otherwise the router becomes an invisible source of '
                       'quality or cost regressions.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Cascading LLM router | Diagram showing a query router '
                       'sending simple requests to a low-cost model and difficult requests to a '
                       'more powerful expensive model, with both paths feeding monitoring | '
                       'Learner should notice the quality-cost trade-off and the need to observe '
                       'routing decisions]]\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 47. RAG evaluation is a production control loop\n'
                       '\n'
                       'A production system changes: data changes, models are upgraded, prompts '
                       'evolve, traffic shifts, and retrieval indexes grow. Without continuous '
                       'evaluation, quality can degrade without an obvious outage.\n'
                       '\n'
                       'The chapter therefore treats evaluation as essential to operating the '
                       'system. Relevant measurements include retrieval quality, generation '
                       'quality, hallucination/faithfulness, response relevance, latency, and '
                       'availability.\n'
                       '\n'
                       'The production principle is:\n'
                       '\n'
                       '> **You cannot reliably improve or protect a dimension you do not '
                       'measure.**\n'
                       '\n'
                       'Evaluation is not only for model selection. It is also a regression '
                       'detector for every future change.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 48. Reference architecture: production ingestion flow\n'
                       '\n'
                       "The chapter's reference architecture decomposes ingestion into services.\n"
                       '\n'
                       'A document-extraction service handles source-specific parsing, '
                       'tables/images, and metadata. A separate chunking service can support more '
                       'flexible strategies. An embedding service converts both documents and '
                       'queries into vectors.\n'
                       '\n'
                       'The resulting artifacts are distributed to the appropriate stores: vectors '
                       'to vector search, text and metadata to lexical search, with security '
                       'controls throughout.\n'
                       '\n'
                       '```text\n'
                       'source systems\n'
                       '    ↓\n'
                       'document extraction\n'
                       '    ↓\n'
                       'chunking\n'
                       '    ↓\n'
                       'document embedding\n'
                       '    ├─ vectors → vector DB\n'
                       '    └─ text/metadata → lexical system\n'
                       '```\n'
                       '\n'
                       'Separating these capabilities makes each independently deployable and '
                       'scalable.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 49. Reference architecture: production query flow\n'
                       '\n'
                       'On the query side, the query string is embedded for semantic search while '
                       'the same text can be sent to lexical search in parallel.\n'
                       '\n'
                       'The two candidate lists are combined and reranked. Sensitive data may be '
                       'masked before the final context enters the generative service. The '
                       'generation service applies the prompt and guardrails to produce the '
                       'answer.\n'
                       '\n'
                       '```text\n'
                       'query\n'
                       ' ├─ query embedding → vector search ─┐\n'
                       ' └────────────────→ lexical search ──┤\n'
                       '                                     ↓\n'
                       '                              combine + rerank\n'
                       '                                     ↓\n'
                       '                              optional masking\n'
                       '                                     ↓\n'
                       '                             LLM + guardrails\n'
                       '                                     ↓\n'
                       '                                  answer\n'
                       '```\n'
                       '\n'
                       '{{image:production-rag-architecture}}'
                       '\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 50. Logging, monitoring, and observability are a cross-cutting plane\n'
                       '\n'
                       'The reference architecture diagram does not show every operational system. '
                       'The chapter explicitly calls out logging, monitoring, and observability as '
                       'MLOps concerns that must be integrated into every service.\n'
                       '\n'
                       'These capabilities answer different operational questions:\n'
                       '\n'
                       '- **logs:** what happened?\n'
                       '- **metrics/monitoring:** is the system healthy?\n'
                       '- **traces/observability:** where did time or failure occur in this '
                       'specific request?\n'
                       '\n'
                       'For RAG, request traces should connect retrieval candidates, reranker '
                       'outcomes, model calls, latency, and final quality signals where '
                       'appropriate.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Observability plane across RAG microservices | Production '
                       'RAG pipeline with a horizontal logging-metrics-tracing layer connected to '
                       'every service | Learner should notice that observability is cross-cutting '
                       'rather than a separate final component]]\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 51. Start production planning with a POC retrospective\n'
                       '\n'
                       'Before redesigning the system, document what the proof of concept actually '
                       'taught you.\n'
                       '\n'
                       'The chapter suggests reviewing:\n'
                       '\n'
                       '- which vector DB, embedding model, reranker, and LLM were used;\n'
                       '- how data was collected and ingested;\n'
                       '- whether tables/images needed special treatment;\n'
                       '- which prompt was used;\n'
                       '- which advanced RAG features were tested;\n'
                       '- whether response quality was good enough;\n'
                       '- how latency and evaluation were measured;\n'
                       '- which unexpected issues occurred;\n'
                       '- what functionality was missing.\n'
                       '\n'
                       'This report converts an informal experiment into evidence for production '
                       'requirements.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 52. Translate production goals into measurable requirements\n'
                       '\n'
                       'Once lessons from the POC are documented, define explicit production '
                       'goals. Where possible, use quantitative KPIs.\n'
                       '\n'
                       "The chapter's example requirement table includes dimensions such as:\n"
                       '\n'
                       '- mean/median query latency;\n'
                       '- uptime and availability;\n'
                       '- context precision and recall;\n'
                       '- hallucination rate and answer relevance;\n'
                       '- supported file types and data sources;\n'
                       '- refresh requirements;\n'
                       '- retrieval techniques;\n'
                       '- chunking strategies;\n'
                       '- supported LLMs and embedding models.\n'
                       '\n'
                       'The exact sample numbers are illustrative. The important practice is to '
                       'replace vague goals like “fast” or “high quality” with measurable '
                       'acceptance criteria.\n'
                       '\n'
                       '{{exercise:M01.L04.EX20}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 53. Production-readiness considerations beyond model quality\n'
                       '\n'
                       'The chapter expands production planning beyond RAG algorithms.\n'
                       '\n'
                       '**Hardware:** CPU/GPU, memory, networking, staging, and HA capacity.\n'
                       '\n'
                       '**Development process:** source control, CI/CD, '
                       'unit/integration/regression tests.\n'
                       '\n'
                       '**Data connectivity:** source systems, credentials, and permission '
                       'propagation.\n'
                       '\n'
                       '**Security/governance:** audit needs, relevant compliance obligations, and '
                       'end-to-end encryption.\n'
                       '\n'
                       '**Monitoring:** uptime, latency, quality, and user satisfaction.\n'
                       '\n'
                       '**Budget:** monthly operating limits and behavior when usage exceeds '
                       'assumptions.\n'
                       '\n'
                       'A production plan is incomplete if it specifies the LLM and vector '
                       'database but leaves these areas undefined.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 54. Successful launch includes user training\n'
                       '\n'
                       'A technically correct system can still fail if users do not understand '
                       'when or how to use it.\n'
                       '\n'
                       'The chapter recommends training employees or customers on the '
                       "application's capabilities and appropriate use. This is important because "
                       'user behavior affects the query distribution, perceived usefulness, and '
                       'feedback data the team receives.\n'
                       '\n'
                       'Production success therefore includes adoption design, not only backend '
                       'readiness.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 55. Treat usage changes as diagnostic signals\n'
                       '\n'
                       'The chapter gives an important operational example: query volume may spike '
                       'after launch and then fall sharply after a few weeks.\n'
                       '\n'
                       'That drop can indicate that users are abandoning the tool because answers '
                       'are not useful, latency is too high, or another experience problem '
                       'exists.\n'
                       '\n'
                       'Usage metrics should therefore be interpreted together with quality and '
                       'latency data. A falling request count is not necessarily a capacity '
                       'success; it may be an adoption failure.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 56. Use per-query feedback to localize failures\n'
                       '\n'
                       'A thumbs-up/thumbs-down signal becomes much more valuable when it is '
                       'connected to the rest of the request trace.\n'
                       '\n'
                       'For a negative response, the team should be able to inspect:\n'
                       '\n'
                       '```text\n'
                       'user query\n'
                       '→ retrieved chunks\n'
                       '→ reranked chunks\n'
                       '→ prompt/context\n'
                       '→ generated answer\n'
                       '→ latency\n'
                       '→ user feedback\n'
                       '```\n'
                       '\n'
                       'This helps distinguish missing data, poor retrieval, hallucination, and '
                       'performance problems.\n'
                       '\n'
                       'Feedback is most useful when it leads to a reproducible investigation, not '
                       'when it is stored as an isolated satisfaction number.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 57. The first production weeks require active observation\n'
                       '\n'
                       'The chapter expects unexpected issues after launch. Pre-launch testing '
                       'cannot reproduce every real query, load pattern, document, or user '
                       'behavior.\n'
                       '\n'
                       'The first weeks therefore require close attention to metrics and fast '
                       "remediation. Strong observability increases the team's ability to identify "
                       'and fix problems before users permanently lose trust.\n'
                       '\n'
                       'Production launch is not the end of development; it is the beginning of '
                       'real-world evidence collection.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 58. Ongoing maintenance is part of the product\n'
                       '\n'
                       'After a successful launch, routine operational work continues: patching '
                       'infrastructure, handling uptime incidents, scaling compute, and upgrading '
                       'components when vulnerabilities are discovered.\n'
                       '\n'
                       'This work is easy to overlook during a POC because the prototype exists '
                       'for a short period. A production service must be maintainable for the full '
                       'lifetime of the application.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 59. Upgrading embeddings, LLMs, retrieval, and guardrails safely\n'
                       '\n'
                       'The chapter uses a new embedding model as an example. Even if a benchmark '
                       'suggests better quality, production adoption still requires:\n'
                       '\n'
                       '1. implementing the model for both ingestion and query time;\n'
                       '2. rebuilding or migrating compatible representations when needed;\n'
                       '3. testing dependencies;\n'
                       '4. evaluating the full RAG pipeline against the old version;\n'
                       '5. checking latency and hardware impact;\n'
                       '6. deploying with monitoring.\n'
                       '\n'
                       'The same logic applies to new LLMs, rerankers, hybrid search methods, or '
                       'hallucination controls.\n'
                       '\n'
                       'A component improvement is not a system improvement until end-to-end '
                       'evaluation confirms it.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 60. Plan for continuous improvement and new use cases\n'
                       '\n'
                       'The chapter closes by emphasizing that production RAG requires ongoing '
                       'investment. Data sources must remain clean, deduplicated, and current. '
                       'Models and infrastructure evolve. New techniques appear. More business '
                       'teams may request additional RAG or agentic-RAG use cases.\n'
                       '\n'
                       'The long-term architecture should therefore support change rather than '
                       'assume the first production stack will remain fixed.\n'
                       '\n'
                       'A durable lifecycle is:\n'
                       '\n'
                       '```text\n'
                       'plan → test → deploy → monitor → learn → upgrade\n'
                       '  ↑                                  ↓\n'
                       '  └──────────── repeat ──────────────┘\n'
                       '```\n'
                       '\n'
                       '[[IMAGE_NEEDED: Continuous RAG production lifecycle | Circular lifecycle '
                       'showing plan, test, deploy, monitor, learn, and upgrade, with data hygiene '
                       'and evaluation surrounding the loop | Learner should notice that '
                       'production RAG is continuously maintained and improved]]\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 61. Why POC retrieval quality often degrades in production\n'
                       '\n'
                       'The production dataset is usually much larger than the POC dataset. More '
                       'chunks means more near-neighbors competing for top positions, larger '
                       'indexes to maintain, and greater pressure on ranking quality.\n'
                       '\n'
                       'The chapter links this directly to both quality and latency. You may need '
                       'to retrieve more candidates to preserve recall, but then reranking and '
                       'generation become more expensive. This is why scaling data volume can '
                       'indirectly increase the cost of the query path.\n'
                       '\n'
                       'Production retrieval design therefore balances three linked variables:\n'
                       '\n'
                       '```text\n'
                       'candidate count ↔ retrieval recall ↔ reranking / generation cost\n'
                       '```\n'
                       '\n'
                       'The correct operating point must be measured on production-like data.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 62. More retrieved chunks are not automatically better\n'
                       '\n'
                       'When retrieval becomes difficult, a common instinct is to send more chunks '
                       'to the LLM. The chapter warns that this increases generation input size, '
                       'latency, and cost, and can still reduce answer quality if the additional '
                       'context is noisy.\n'
                       '\n'
                       'The production objective is not maximum context volume. It is **maximum '
                       'useful evidence per token**.\n'
                       '\n'
                       'This reinforces the need for stronger ranking rather than blindly '
                       'expanding top-k.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 63. Choose microservice boundaries around scaling and ownership\n'
                       '\n'
                       "The chapter's reference design separates extraction, chunking, embedding, "
                       'retrieval, reranking, and generation because these components have '
                       'different resource and scaling profiles.\n'
                       '\n'
                       'A boundary is useful when it enables independent deployment, scaling, '
                       'hardware choice, security policy, or ownership. A boundary that only adds '
                       'network hops without those benefits can make the system harder to '
                       'operate.\n'
                       '\n'
                       'The source does not prescribe one mandatory decomposition. It presents '
                       'decoupling as a strategy for controlling complexity and allowing '
                       'independent scaling.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 64. Staging is useful only when it tests production assumptions\n'
                       '\n'
                       'The staging-verification pattern is valuable because ingestion changes can '
                       'damage live retrieval. For staging to be meaningful, it should exercise '
                       'the same parsing, chunking, metadata, indexing, and retrieval logic that '
                       'production uses.\n'
                       '\n'
                       'A tiny hand-crafted test path that bypasses production processing will not '
                       'catch the kinds of ingestion defects the chapter warns about.\n'
                       '\n'
                       'The goal is to validate a candidate knowledge change under realistic '
                       'processing before promotion.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 65. Security controls must be evaluated for quality impact\n'
                       '\n'
                       "The chapter's redaction discussion illustrates a broader principle: "
                       'security transformations can change retrieval and generation quality.\n'
                       '\n'
                       'Typed masking attempts to preserve semantic roles while hiding values, but '
                       'any redaction can still change embeddings, lexical matches, and '
                       'answerability. Therefore privacy controls should be included in end-to-end '
                       'RAG evaluation rather than tested only by the security team.\n'
                       '\n'
                       'A secure system that cannot answer its intended questions is not '
                       'successful; neither is an accurate system that exposes protected data.\n'
                       '\n'
                       '---\n'
                       '\n'
                       "## 66. SLAs should match the dependency's role in the RAG path\n"
                       '\n'
                       "A vendor's availability and latency commitments matter most when that "
                       'service sits directly on the critical request path.\n'
                       '\n'
                       'If an external reranker or generation API has weak P95/P99 performance or '
                       'poor support response, it can dominate the end-to-end experience '
                       'regardless of how fast the rest of the stack is.\n'
                       '\n'
                       'The vendor checklist is therefore architectural: it asks whether the '
                       "external dependency's guarantees are compatible with the system's own "
                       'production KPI.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 67. Cost should be observable at component level\n'
                       '\n'
                       'The chapter connects cost control with observability. If all spend is '
                       'viewed only as one monthly cloud total, the team cannot identify whether '
                       'embeddings, retrieval infrastructure, generation, monitoring, or another '
                       'component is driving a change.\n'
                       '\n'
                       'Component-level cost telemetry allows questions such as:\n'
                       '\n'
                       '- cost per query;\n'
                       '- cost per model route;\n'
                       '- cost of ingestion refresh;\n'
                       '- cost by retrieval path;\n'
                       '- cost change after an upgrade.\n'
                       '\n'
                       'This makes cost a measurable system behavior rather than an accounting '
                       'surprise.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 68. Data hygiene remains a source-system responsibility\n'
                       '\n'
                       'The conclusion emphasizes that keeping RAG healthy requires clean, '
                       'deduplicated, and regularly updated source documents.\n'
                       '\n'
                       'A production pipeline cannot fully compensate for an organization that '
                       'continuously feeds it conflicting, obsolete, or duplicated knowledge. '
                       'Retrieval and generation quality depend on upstream governance.\n'
                       '\n'
                       'This is why RAG production work extends beyond the AI team into content '
                       'ownership and data-management processes.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Important misconceptions\n'
                       '\n'
                       '### Misconception: If the POC works, production is mostly deployment '
                       'packaging.\n'
                       '\n'
                       '\n'
                       'The chapter shows that production adds scale, latency, security, '
                       'observability, staging, support, cost, and organizational requirements '
                       'that a POC usually does not exercise.\n'
                       '\n'
                       '\n'
                       '### Misconception: A bad RAG answer means the LLM is weak.\n'
                       '\n'
                       '\n'
                       'Poor answers can originate from missing source data, weak retrieval, '
                       'unfaithful generation, or prompt design. Debug the evidence path before '
                       'changing the model.\n'
                       '\n'
                       '\n'
                       '### Misconception: Adding more retrieved chunks always improves answer '
                       'quality.\n'
                       '\n'
                       '\n'
                       'More chunks can increase noise, latency, and cost. Stronger ranking is '
                       'often preferable to blindly expanding context.\n'
                       '\n'
                       '\n'
                       '### Misconception: Caching is only a performance optimization.\n'
                       '\n'
                       '\n'
                       'In RAG, caching also creates a correctness problem because stale cached '
                       'results can outlive the documents they were derived from.\n'
                       '\n'
                       '\n'
                       '### Misconception: Embeddings are safe to expose because they are just '
                       'numbers.\n'
                       '\n'
                       '\n'
                       'The vector store often includes associated text and metadata, and all RAG '
                       'stores remain part of the security boundary.\n'
                       '\n'
                       '\n'
                       '### Misconception: Redacting every sensitive value as XXXX is always '
                       'safest.\n'
                       '\n'
                       '\n'
                       'Generic masking can destroy semantic relationships. Typed masking can '
                       'preserve useful roles while still hiding specific values.\n'
                       '\n'
                       '\n'
                       '### Misconception: RBAC in the source system is enough.\n'
                       '\n'
                       '\n'
                       'Permissions must be propagated and enforced during retrieval so '
                       'unauthorized chunks are never sent to the generator.\n'
                       '\n'
                       '\n'
                       '### Misconception: A managed vendor reduces engineering work to zero.\n'
                       '\n'
                       '\n'
                       'Managed services reduce some operational burden but still introduce '
                       'integration, security, SLA, monitoring, and support dependencies.\n'
                       '\n'
                       '\n'
                       '### Misconception: The monthly LLM API bill is the TCO.\n'
                       '\n'
                       '\n'
                       'TCO also includes retrieval infrastructure, staging, monitoring, security, '
                       'integration, support, engineering staff, and high availability.\n'
                       '\n'
                       '\n'
                       '### Misconception: Once production launches, the architecture can remain '
                       'stable.\n'
                       '\n'
                       '\n'
                       'The chapter treats production RAG as a continuous lifecycle of monitoring, '
                       'maintenance, evaluation, upgrades, and new use cases.\n'
                       '\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Key terminology\n'
                       '\n'
                       '\n'
                       '| Term | Meaning |\n'
                       '|---|---|\n'
                       '\n'
                       '| Proof of concept (POC) | A limited implementation used to validate '
                       'feasibility and value before full production engineering. |\n'
                       '\n'
                       '| Production-grade | Able to satisfy defined requirements for quality, '
                       'latency, security, availability, scalability, and maintainability. |\n'
                       '\n'
                       '| Staging collection | A nonproduction index used to validate new or '
                       'changed ingested data before promotion. |\n'
                       '\n'
                       '| Source of truth | The authoritative document or data source that the '
                       'organization considers current and valid. |\n'
                       '\n'
                       '| Tail latency | Slow-request behavior near the high percentiles of the '
                       'latency distribution, such as P95 or P99. |\n'
                       '\n'
                       '| Fan-out/gather | Running independent requests in parallel, then '
                       'gathering their results for the next processing stage. |\n'
                       '\n'
                       '| Auto-scaling | Automatically changing the number of service replicas '
                       'according to workload or resource metrics. |\n'
                       '\n'
                       '| Semantic cache | A cache that matches new queries to prior queries by '
                       'embedding similarity rather than exact text. |\n'
                       '\n'
                       '| Cache invalidation | Removing or updating cached data when the '
                       'underlying source data changes. |\n'
                       '\n'
                       '| Eviction policy | A rule for deciding which cache entries to remove when '
                       'memory is limited. |\n'
                       '\n'
                       '| Defense in depth | Using multiple security controls across different '
                       'layers instead of relying on one protection. |\n'
                       '\n'
                       '| PII | Personally identifiable information. |\n'
                       '\n'
                       '| PHI | Protected health information. |\n'
                       '\n'
                       '| Typed masking | Replacing a sensitive value with its entity category so '
                       'semantic roles remain visible. |\n'
                       '\n'
                       '| Data provenance | Traceable information about the origin and history of '
                       'data. |\n'
                       '\n'
                       '| RBAC | Role-based access control used to restrict data or actions '
                       'according to user roles. |\n'
                       '\n'
                       '| Guardrail | A control that checks, blocks, or modifies unsafe or '
                       'disallowed model behavior. |\n'
                       '\n'
                       '| SLA | A service-level agreement defining commitments such as uptime, '
                       'support response, or latency. |\n'
                       '\n'
                       '| Total cost of ownership (TCO) | The full cost of operating and evolving '
                       'a system, including direct and indirect expenses. |\n'
                       '\n'
                       '| Denial of wallet | Excessive expensive requests that create financially '
                       'damaging usage. |\n'
                       '\n'
                       '| Cascading model routing | Sending simple requests to cheaper models and '
                       'escalating harder requests to stronger models. |\n'
                       '\n'
                       '| High availability (HA) | Architecture designed to continue service '
                       'despite component failures. |\n'
                       '\n'
                       '| Failover | Redirecting work from a failed component or region to a '
                       'healthy alternative. |\n'
                       '\n'
                       '| Observability | Using logs, metrics, and traces to understand internal '
                       'system behavior. |\n'
                       '\n'
                       '| Regression test | A test that verifies a new change did not degrade '
                       'previously acceptable behavior. |\n'
                       '\n'
                       '| Data hygiene | Keeping source data clean, current, deduplicated, and '
                       'suitable for ingestion. |\n'
                       '\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Self-check\n'
                       '\n'
                       '\n'
                       'Before continuing, make sure you can answer the following without looking '
                       'back at the lesson:\n'
                       '\n'
                       '\n'
                       '1. What makes a production RAG system fundamentally different from a proof '
                       'of concept?\n'
                       '\n'
                       '2. Why does the chapter say much of production RAG work is standard '
                       'software engineering and DevOps?\n'
                       '\n'
                       '3. Which quality dimensions can conflict with each other in a production '
                       'RAG design?\n'
                       '\n'
                       '4. What four major failure sources should you investigate when a response '
                       'is poor?\n'
                       '\n'
                       '5. Why can a retriever still return plausible-looking chunks when the '
                       'correct data is absent?\n'
                       '\n'
                       '6. How should a missing-data failure be handled differently from a prompt '
                       'failure?\n'
                       '\n'
                       '7. What is the purpose of a staging collection?\n'
                       '\n'
                       '8. Which ingestion defects can a staging-verification workflow catch '
                       'before production promotion?\n'
                       '\n'
                       '9. Why are subject-matter experts important for determining the source of '
                       'truth?\n'
                       '\n'
                       '10. How can duplicate old and new policies create bad RAG answers even '
                       'with technically correct retrieval?\n'
                       '\n'
                       '11. Why does retrieval become more difficult when the corpus grows?\n'
                       '\n'
                       '12. Which advanced retrieval techniques does the chapter recommend as '
                       'systems scale?\n'
                       '\n'
                       '13. Why is garbage-in-garbage-out a useful principle for RAG retrieval?\n'
                       '\n'
                       '14. How can an LLM hallucinate even when the correct evidence was '
                       'retrieved?\n'
                       '\n'
                       '15. What does a spectrum of factuality mean in generated answers?\n'
                       '\n'
                       '16. Why should production prompts explicitly define what to do when '
                       'evidence is missing?\n'
                       '\n'
                       '17. How can prompt design contribute to prompt-injection defense?\n'
                       '\n'
                       '18. What stages belong in an end-to-end latency budget?\n'
                       '\n'
                       '19. Why can a low average latency hide a poor user experience?\n'
                       '\n'
                       '20. What do P50, P95, and P99 latency tell you?\n'
                       '\n'
                       '21. Why is fan-out/gather faster than sequential semantic and lexical '
                       'search?\n'
                       '\n'
                       "22. What is the role of the stateless orchestrator in the chapter's "
                       'architecture?\n'
                       '\n'
                       '23. Why should vector search and lexical search be able to scale '
                       'independently?\n'
                       '\n'
                       '24. Which resource bottlenecks differ between orchestrator, database, and '
                       'LLM services?\n'
                       '\n'
                       '25. Why might a smaller LLM be preferable in production?\n'
                       '\n'
                       '26. What must be re-evaluated when the production LLM is changed?\n'
                       '\n'
                       '27. Why is optimized inference software important for self-hosted model '
                       'services?\n'
                       '\n'
                       '28. What is the purpose of batching in a production inference server?\n'
                       '\n'
                       '29. Why are ANN indexes important for production vector retrieval?\n'
                       '\n'
                       '30. What production concerns apply to lexical search indexing?\n'
                       '\n'
                       '31. What work does a full-response cache avoid?\n'
                       '\n'
                       '32. What work does a retrieval cache avoid?\n'
                       '\n'
                       '33. What work does a chunk cache avoid?\n'
                       '\n'
                       '34. Why does natural-language input reduce the effectiveness of '
                       'exact-string caching?\n'
                       '\n'
                       '35. How does semantic caching decide whether to reuse a prior result?\n'
                       '\n'
                       '36. What happens if a semantic-cache threshold is too low?\n'
                       '\n'
                       '37. What happens if a semantic-cache threshold is too high?\n'
                       '\n'
                       '38. Why can a semantic cache return a fast but incorrect answer?\n'
                       '\n'
                       '39. Why is event-driven invalidation stronger than relying only on TTL?\n'
                       '\n'
                       '40. What information must a cache entry retain to support targeted '
                       'invalidation?\n'
                       '\n'
                       '41. Why does a production cache need an eviction policy?\n'
                       '\n'
                       '42. Why might a cache require sharding or clustering?\n'
                       '\n'
                       '43. What are the three major security surfaces identified in the chapter?\n'
                       '\n'
                       '44. Why must encryption continue across intermediate ingestion stages?\n'
                       '\n'
                       '45. What different representations of sensitive data can an ingestion '
                       'pipeline create?\n'
                       '\n'
                       '46. Why can generic PII masking reduce RAG answer quality?\n'
                       '\n'
                       '47. How does typed masking preserve more useful semantics?\n'
                       '\n'
                       '48. What are the main steps in entity-aware redaction?\n'
                       '\n'
                       '49. Why should redaction controls be tested with end-to-end retrieval and '
                       'generation?\n'
                       '\n'
                       '50. What problem does hash-based provenance tracking address?\n'
                       '\n'
                       '51. What should an audit trail tell you about a chunk?\n'
                       '\n'
                       '52. Why must vector, lexical, and graph stores all be treated as sensitive '
                       'data stores?\n'
                       '\n'
                       '53. What is data minimization in the context of production RAG?\n'
                       '\n'
                       '54. Why must permission checks happen before retrieved chunks enter the '
                       'LLM prompt?\n'
                       '\n'
                       '55. What metadata is required to enforce permission-aware retrieval?\n'
                       '\n'
                       '56. What additional risk is introduced by external LLM API calls?\n'
                       '\n'
                       '57. Why can anonymized data still create privacy concerns?\n'
                       '\n'
                       '58. What operational responsibilities move in-house when an organization '
                       'self-hosts an LLM?\n'
                       '\n'
                       '59. Why are generation guardrails required even when retrieval is '
                       'protected?\n'
                       '\n'
                       '60. How does user reporting contribute to production safety?\n'
                       '\n'
                       '61. What extra integration burden is introduced by each new RAG vendor?\n'
                       '\n'
                       '62. Which API questions should be asked before adopting a vendor '
                       'component?\n'
                       '\n'
                       '63. Why are P95/P99 latency guarantees important in vendor assessment?\n'
                       '\n'
                       '64. What should you ask a vendor about compliance and PII handling?\n'
                       '\n'
                       '65. Why can support coordination become difficult in a multi-vendor RAG '
                       'stack?\n'
                       '\n'
                       '66. What trade-off does a turnkey platform make relative to DIY '
                       'integration?\n'
                       '\n'
                       '67. Why does production RAG require an interdisciplinary team?\n'
                       '\n'
                       '68. Which tasks fall under machine-learning engineering in the chapter?\n'
                       '\n'
                       '69. Which tasks fall under data engineering?\n'
                       '\n'
                       '70. Which tasks fall under DevOps/MLOps?\n'
                       '\n'
                       '71. Which tasks fall under security/compliance?\n'
                       '\n'
                       '72. Why is rapid change in the RAG ecosystem itself an organizational '
                       'challenge?\n'
                       '\n'
                       '73. What question helps decide whether a component is worth building '
                       'internally?\n'
                       '\n'
                       '74. Why is the LLM API bill only one part of TCO?\n'
                       '\n'
                       '75. Which direct costs should appear in a RAG budget?\n'
                       '\n'
                       '76. Which indirect costs are easy to underestimate?\n'
                       '\n'
                       '77. How does high availability increase TCO?\n'
                       '\n'
                       '78. Why should availability requirements be defined before final '
                       'budgeting?\n'
                       '\n'
                       '79. Why does the chapter recommend budget-based alerts?\n'
                       '\n'
                       '80. What is a denial-of-wallet attack?\n'
                       '\n'
                       '81. How can rate limiting reduce financial risk?\n'
                       '\n'
                       '82. How does cascading model routing reduce average cost?\n'
                       '\n'
                       '83. What signals should a model router expose to observability?\n'
                       '\n'
                       '84. Why must router quality be evaluated instead of assumed?\n'
                       '\n'
                       '85. Why is continuous RAG evaluation needed after launch?\n'
                       '\n'
                       '86. What kinds of regressions can evaluation detect?\n'
                       '\n'
                       '87. What services appear in the reference ingestion architecture?\n'
                       '\n'
                       '88. Why might chunking be separated from document extraction?\n'
                       '\n'
                       '89. How can one embedding service support both ingestion and queries?\n'
                       '\n'
                       '90. Where are vectors stored in the reference architecture?\n'
                       '\n'
                       '91. Where are text and metadata commonly stored?\n'
                       '\n'
                       '92. How do semantic and lexical search execute in the reference query '
                       'flow?\n'
                       '\n'
                       '93. What happens after the two retrieval result sets are collected?\n'
                       '\n'
                       '94. Where can PII masking be applied in the query path?\n'
                       '\n'
                       '95. Why are security controls needed in every microservice?\n'
                       '\n'
                       '96. What are the three cross-cutting MLOps aspects named in the chapter?\n'
                       '\n'
                       '97. What is the difference between a log, a metric, and a trace?\n'
                       '\n'
                       '98. Why should a request trace include retrieval and model stages?\n'
                       '\n'
                       '99. What should a POC retrospective record about the components used?\n'
                       '\n'
                       '100. What should it record about data ingestion?\n'
                       '\n'
                       '101. What should it record about prompts and hallucinations?\n'
                       '\n'
                       '102. What should it record about latency and response quality?\n'
                       '\n'
                       '103. Why should unexpected POC issues be documented before production '
                       'planning?\n'
                       '\n'
                       "104. Why are numeric KPIs stronger than goals such as 'fast' or "
                       "'accurate'?\n"
                       '\n'
                       "105. Which latency measures does the chapter's example KPI table include?\n"
                       '\n'
                       '106. Which response-quality dimensions appear in the example KPI table?\n'
                       '\n'
                       '107. Which ingestion capabilities should be specified in production '
                       'requirements?\n'
                       '\n'
                       '108. Which retrieval techniques can be listed as production requirements?\n'
                       '\n'
                       '109. Why should staging and HA hardware be included in capacity planning?\n'
                       '\n'
                       '110. What questions belong under development environment and process?\n'
                       '\n'
                       '111. What questions belong under data connectivity?\n'
                       '\n'
                       '112. What questions belong under security and governance?\n'
                       '\n'
                       '113. What questions belong under monitoring?\n'
                       '\n'
                       '114. What questions belong under budget planning?\n'
                       '\n'
                       '115. Why is user training part of a successful production launch?\n'
                       '\n'
                       '116. What might a post-launch drop in query volume indicate?\n'
                       '\n'
                       '117. Why should adoption metrics be interpreted with quality and latency '
                       'metrics?\n'
                       '\n'
                       '118. How can thumbs-up/thumbs-down feedback become diagnostically useful?\n'
                       '\n'
                       '119. What request information should be attached to negative feedback?\n'
                       '\n'
                       '120. Why should the team expect new issues during the first weeks after '
                       'launch?\n'
                       '\n'
                       '121. How does observability improve remediation speed?\n'
                       '\n'
                       '122. What kinds of routine maintenance remain after launch?\n'
                       '\n'
                       '123. Why can a new embedding model require changes at both ingest and '
                       'query time?\n'
                       '\n'
                       '124. Why can a quality-improving model still be a bad production upgrade?\n'
                       '\n'
                       '125. What additional hardware or latency constraints can appear after a '
                       'model upgrade?\n'
                       '\n'
                       '126. What process should be followed for new LLMs, rerankers, and '
                       'hallucination controls?\n'
                       '\n'
                       '127. Why is end-to-end evaluation required for every component upgrade?\n'
                       '\n'
                       '128. Why does the chapter emphasize source data hygiene?\n'
                       '\n'
                       '129. How can duplicate or outdated source documents undermine production '
                       'quality?\n'
                       '\n'
                       '130. Why should the architecture expect new RAG and agentic-RAG use '
                       'cases?\n'
                       '\n'
                       '131. What is the continuous production lifecycle described in this '
                       'lesson?\n'
                       '\n'
                       '132. Why is production launch the beginning rather than the end of '
                       'learning?\n'
                       '\n'
                       '133. How do latency and cost pressures interact with retrieval candidate '
                       'count?\n'
                       '\n'
                       '134. Why is maximum useful evidence per token a better goal than maximum '
                       'context size?\n'
                       '\n'
                       '135. What benefit does a service boundary provide when components have '
                       'different scaling profiles?\n'
                       '\n'
                       '136. Why can too many microservices also create operational cost?\n'
                       '\n'
                       '137. Why should staging use the same processing logic as production?\n'
                       '\n'
                       '138. How can a redaction strategy create a retrieval regression?\n'
                       '\n'
                       "139. Why should vendor SLAs align with the system's own KPI?\n"
                       '\n'
                       '140. Why is component-level cost telemetry more useful than one monthly '
                       'total?\n'
                       '\n'
                       '141. Which cost-per-unit metrics can help locate waste?\n'
                       '\n'
                       '142. Why must source-system owners participate in RAG data hygiene?\n'
                       '\n'
                       '143. Why is a secure RAG system still incomplete if it cannot answer its '
                       'intended questions?\n'
                       '\n'
                       '144. Why is an accurate RAG system still unacceptable if it exposes '
                       'protected data?\n'
                       '\n'
                       '145. How does caching connect the latency problem to the freshness '
                       'problem?\n'
                       '\n'
                       '146. How does model routing connect the cost problem to the evaluation '
                       'problem?\n'
                       '\n'
                       '147. How does permission filtering connect identity management to '
                       'retrieval?\n'
                       '\n'
                       '148. How does staging connect ingestion engineering to response quality?\n'
                       '\n'
                       '149. What is the single most important mental model for moving from POC to '
                       'production RAG?\n'
                       '\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Retain this idea\n'
                       '\n'
                       '\n'
                       '**A production RAG system is not a bigger prototype. It is a continuously '
                       'operated distributed system whose answer quality depends on the '
                       'coordinated health of data, retrieval, generation, security, latency, '
                       'cost, and observability. Every change should move through a disciplined '
                       'cycle of staging, evaluation, deployment, monitoring, and improvement.**\n',
            'estimated_minutes': 690,
            'has_code_examples': True,
            'has_manual_image_requests': True,
            'sections': [{'id': 'poc-vs-production',
                          'title': 'From a RAG proof of concept to a production system',
                          'order': 1},
                         {'id': 'production-quality-pillars',
                          'title': 'The production quality pillars',
                          'order': 2},
                         {'id': 'quality-failure-tree',
                          'title': 'Diagnosing poor response quality',
                          'order': 3},
                         {'id': 'missing-data',
                          'title': 'Failure reason 1: the system has no relevant data',
                          'order': 4},
                         {'id': 'staging-index',
                          'title': 'Promote new knowledge through a staging index',
                          'order': 5},
                         {'id': 'source-of-truth',
                          'title': 'Subject-matter experts and source-of-truth control',
                          'order': 6},
                         {'id': 'weak-retrieval',
                          'title': 'Failure reason 2: the retrieval pipeline is too weak',
                          'order': 7},
                         {'id': 'llm-hallucination',
                          'title': 'Failure reason 3: the LLM is not faithful to good evidence',
                          'order': 8},
                         {'id': 'production-prompts',
                          'title': 'Failure reason 4: production prompt engineering',
                          'order': 9},
                         {'id': 'latency-budget',
                          'title': 'Designing an end-to-end latency budget',
                          'order': 10},
                         {'id': 'tail-latency',
                          'title': 'Average latency is not enough: watch the tail',
                          'order': 11},
                         {'id': 'fanout-gather',
                          'title': 'Parallel fan-out/gather retrieval',
                          'order': 12},
                         {'id': 'independent-autoscaling',
                          'title': 'Scale each microservice according to its bottleneck',
                          'order': 13},
                         {'id': 'alternative-llms',
                          'title': 'Using smaller or alternative LLMs in production',
                          'order': 14},
                         {'id': 'inference-acceleration',
                          'title': 'Software and hardware acceleration for model services',
                          'order': 15},
                         {'id': 'indexing-for-latency',
                          'title': 'Efficient indexing is a latency prerequisite',
                          'order': 16},
                         {'id': 'cache-layers',
                          'title': 'Caching at multiple layers of the RAG pipeline',
                          'order': 17},
                         {'id': 'semantic-cache',
                          'title': 'Why semantic caching fits natural-language queries',
                          'order': 18},
                         {'id': 'semantic-cache-code',
                          'title': 'Worked implementation: a semantic cached retriever',
                          'order': 19},
                         {'id': 'cache-invalidation',
                          'title': 'Cache invalidation is the hard part',
                          'order': 20},
                         {'id': 'cache-capacity',
                          'title': 'Eviction and horizontal scaling for production caches',
                          'order': 21},
                         {'id': 'security-overview',
                          'title': 'Security and privacy require defense in depth',
                          'order': 22},
                         {'id': 'ingestion-security',
                          'title': 'Secure the ingestion layer end to end',
                          'order': 23},
                         {'id': 'redaction-tradeoff',
                          'title': 'PII/PHI redaction can damage answer quality',
                          'order': 24},
                         {'id': 'presidio-redaction',
                          'title': 'Worked implementation: entity-aware redaction',
                          'order': 25},
                         {'id': 'provenance-integrity',
                          'title': 'Provenance and integrity tracking',
                          'order': 26},
                         {'id': 'datastore-security',
                          'title': 'Data-store safeguards: encryption, minimization, and '
                                   'monitoring',
                          'order': 27},
                         {'id': 'permission-filtering',
                          'title': 'Prevent data leaks with permission-aware retrieval',
                          'order': 28},
                         {'id': 'external-provider-risk',
                          'title': 'Data leakage risk when calling external LLM providers',
                          'order': 29},
                         {'id': 'onprem-models',
                          'title': 'When on-premises or private-cloud generation becomes necessary',
                          'order': 30},
                         {'id': 'generation-guardrails',
                          'title': 'Generation guardrails in production',
                          'order': 31},
                         {'id': 'vendor-chaos',
                          'title': 'Vendor chaos and integration complexity',
                          'order': 32},
                         {'id': 'vendor-checklist',
                          'title': 'A disciplined vendor-evaluation checklist',
                          'order': 33},
                         {'id': 'support-complexity',
                          'title': 'Support coordination is an architectural cost',
                          'order': 34},
                         {'id': 'team-overview',
                          'title': 'Production RAG is an interdisciplinary team problem',
                          'order': 35},
                         {'id': 'ml-engineering-skills',
                          'title': 'Machine-learning engineering responsibilities',
                          'order': 36},
                         {'id': 'data-engineering-skills',
                          'title': 'Data-engineering responsibilities',
                          'order': 37},
                         {'id': 'devops-skills',
                          'title': 'DevOps/MLOps responsibilities',
                          'order': 38},
                         {'id': 'security-skills',
                          'title': 'Security and compliance responsibilities',
                          'order': 39},
                         {'id': 'build-vs-buy',
                          'title': 'Build versus buy: spend internal talent on differentiation',
                          'order': 40},
                         {'id': 'tco-overview',
                          'title': 'Total cost of ownership is larger than API spend',
                          'order': 41},
                         {'id': 'direct-costs',
                          'title': 'Direct costs: vendors, retrieval, compute, and storage',
                          'order': 42},
                         {'id': 'indirect-costs',
                          'title': 'Indirect and ongoing costs',
                          'order': 43},
                         {'id': 'ha-costs',
                          'title': 'High availability and business continuity add real cost',
                          'order': 44},
                         {'id': 'cost-monitoring',
                          'title': 'Cost monitoring, budget alerts, and denial-of-wallet '
                                   'protection',
                          'order': 45},
                         {'id': 'model-router',
                          'title': 'Cascading models and LLM routing',
                          'order': 46},
                         {'id': 'rag-evaluation',
                          'title': 'RAG evaluation is a production control loop',
                          'order': 47},
                         {'id': 'reference-architecture-ingestion',
                          'title': 'Reference architecture: production ingestion flow',
                          'order': 48},
                         {'id': 'reference-architecture-query',
                          'title': 'Reference architecture: production query flow',
                          'order': 49},
                         {'id': 'observability-plane',
                          'title': 'Logging, monitoring, and observability are a cross-cutting '
                                   'plane',
                          'order': 50},
                         {'id': 'poc-retrospective',
                          'title': 'Start production planning with a POC retrospective',
                          'order': 51},
                         {'id': 'requirements-kpis',
                          'title': 'Translate production goals into measurable requirements',
                          'order': 52},
                         {'id': 'production-readiness-checklist',
                          'title': 'Production-readiness considerations beyond model quality',
                          'order': 53},
                         {'id': 'launch-training',
                          'title': 'Successful launch includes user training',
                          'order': 54},
                         {'id': 'adoption-signals',
                          'title': 'Treat usage changes as diagnostic signals',
                          'order': 55},
                         {'id': 'user-feedback-loop',
                          'title': 'Use per-query feedback to localize failures',
                          'order': 56},
                         {'id': 'early-operations',
                          'title': 'The first production weeks require active observation',
                          'order': 57},
                         {'id': 'maintenance',
                          'title': 'Ongoing maintenance is part of the product',
                          'order': 58},
                         {'id': 'component-upgrades',
                          'title': 'Upgrading embeddings, LLMs, retrieval, and guardrails safely',
                          'order': 59},
                         {'id': 'continuous-improvement',
                          'title': 'Plan for continuous improvement and new use cases',
                          'order': 60},
                         {'id': 'retrieval-growth-effects',
                          'title': 'Why POC retrieval quality often degrades in production',
                          'order': 61},
                         {'id': 'retrieval-context-size',
                          'title': 'More retrieved chunks are not automatically better',
                          'order': 62},
                         {'id': 'microservice-boundaries',
                          'title': 'Choose microservice boundaries around scaling and ownership',
                          'order': 63},
                         {'id': 'staging-production-parity',
                          'title': 'Staging is useful only when it tests production assumptions',
                          'order': 64},
                         {'id': 'quality-vs-security',
                          'title': 'Security controls must be evaluated for quality impact',
                          'order': 65},
                         {'id': 'vendor-sla',
                          'title': "SLAs should match the dependency's role in the RAG path",
                          'order': 66},
                         {'id': 'observability-cost',
                          'title': 'Cost should be observable at component level',
                          'order': 67},
                         {'id': 'production-data-hygiene',
                          'title': 'Data hygiene remains a source-system responsibility',
                          'order': 68}]},
 'exercises': [{'id': 'M01.L04.EX01',
                'title': 'POC-to-production gap analysis',
                'lesson_code': 'M01.L04',
                'section_id': 'poc-vs-production',
                'placement': 'after_section',
                'description': 'Given a small notebook-based RAG POC, identify the production '
                               'capabilities that are missing and group them by quality, '
                               'operations, security, and scale.',
                'instructions': '1. Assume the POC is one notebook: it loads a folder of PDFs, embeds them in memory, and answers questions with one prompt.\n'
                                '2. List at least eight capabilities a production version needs that the notebook lacks.\n'
                                '3. Group them under quality, operations, security, and scale.\n'
                                '4. Pick the three gaps you would close first and explain why.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['architecture', 'production-readiness']},
               {'id': 'M01.L04.EX02',
                'title': 'Diagnose a bad answer',
                'lesson_code': 'M01.L04',
                'section_id': 'quality-failure-tree',
                'placement': 'after_section',
                'description': 'Trace a low-quality answer through the four-part failure tree and '
                               'identify the first evidence you would inspect.',
                'instructions': '1. Take one low-quality answer and list the four branches of the failure tree from the lesson.\n'
                                '2. For each branch, write the first piece of evidence you would inspect (for example the retrieved chunks, the source document, the prompt, the raw model output).\n'
                                '3. Order the checks from cheapest and most likely to most expensive.\n'
                                '4. State what result in each check would rule that branch out.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['debugging', 'response-quality']},
               {'id': 'M01.L04.EX03',
                'title': 'Design a staging promotion workflow',
                'lesson_code': 'M01.L04',
                'section_id': 'staging-index',
                'placement': 'after_section',
                'description': 'Design tests and promotion gates for adding a new document batch '
                               'without polluting the live index.',
                'instructions': '1. Describe how a new document batch is indexed into a staging index first, never directly into the live one.\n'
                                '2. Define the tests the batch must pass (parsing quality, duplicate check, access labels, a regression set of known questions).\n'
                                '3. Define the promotion gate: who or what approves the switch, and how it is performed.\n'
                                '4. Explain how you roll back if problems appear after promotion.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['staging', 'ingestion-validation']},
               {'id': 'M01.L04.EX04',
                'title': 'Strengthen a weak retriever',
                'lesson_code': 'M01.L04',
                'section_id': 'weak-retrieval',
                'placement': 'after_section',
                'description': 'Given noisy production retrieval, choose which retrieval upgrades '
                               'you would test and explain what failure each addresses.',
                'instructions': '1. Describe two symptoms of noisy retrieval you might see in production logs (for example relevant documents ranked below 20, or near-duplicate chunks filling the top results).\n'
                                '2. Choose up to three upgrades to test (for example hybrid search, a reranker, better chunking, query rewriting, metadata filters).\n'
                                '3. For each upgrade, name the failure it addresses.\n'
                                '4. Define the offline metric and query set you would use to compare each upgrade with the current retriever.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['retrieval', 'system-design']},
               {'id': 'M01.L04.EX05',
                'title': 'Audit generator faithfulness',
                'lesson_code': 'M01.L04',
                'section_id': 'llm-hallucination',
                'placement': 'after_section',
                'description': 'Given retrieved evidence and a partially supported answer, '
                               'identify which claims are grounded and which require refusal or '
                               'correction.',
                'instructions': "1. Evidence: 'Plan B includes 50 GB storage and email support. Price: $20 per month.' Answer: 'Plan B costs $20 per month, includes 50 GB storage, 24/7 phone support, and a free trial.'\n"
                                '2. Split the answer into individual claims.\n'
                                '3. Mark each claim supported, unsupported, or contradicted by the evidence.\n'
                                '4. Rewrite the answer so it keeps only supported claims and says what the evidence does not cover.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['faithfulness', 'hallucination']},
               {'id': 'M01.L04.EX06',
                'title': 'Write an uncertainty-aware RAG prompt',
                'lesson_code': 'M01.L04',
                'section_id': 'production-prompts',
                'placement': 'after_section',
                'description': 'Create a prompt that uses retrieved context, defines uncertainty '
                               'behavior, and avoids inventing missing facts.',
                'instructions': '1. Write a prompt with placeholders for the question and the retrieved context.\n'
                                '2. Instruct the model to answer only from the context and to cite the chunk it used.\n'
                                '3. Define the exact behavior when the context is incomplete or conflicting (for example a fixed sentence and what to ask next).\n'
                                '4. Test the prompt mentally against one question the context cannot answer and show the expected response.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['prompt-engineering', 'grounded-generation']},
               {'id': 'M01.L04.EX07',
                'title': 'Create a latency budget',
                'lesson_code': 'M01.L04',
                'section_id': 'latency-budget',
                'placement': 'after_section',
                'description': 'Allocate an end-to-end latency target across embedding, retrieval, '
                               'reranking, generation, and guardrails, then identify the dominant '
                               'path.',
                'instructions': '1. Take an end-to-end target of 2,000 ms at p95.\n'
                                '2. Allocate milliseconds to query embedding, retrieval, reranking, generation (time to first token and full answer), and guardrails, so they add up to the target.\n'
                                '3. Identify the stage that dominates the budget and explain why.\n'
                                '4. Propose one change that would reduce the dominant stage and the quality risk it carries.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['latency', 'performance']},
               {'id': 'M01.L04.EX08',
                'title': 'Parallelize the query path',
                'lesson_code': 'M01.L04',
                'section_id': 'fanout-gather',
                'placement': 'after_section',
                'description': 'Redesign a sequential semantic-plus-lexical retrieval path into '
                               'fan-out/gather form and explain the latency effect.',
                'instructions': '1. Start from the sequential path: semantic search (120 ms), then lexical search (80 ms), then merge (10 ms).\n'
                                '2. Redraw it as fan-out/gather: both searches start together and a merge step waits for both.\n'
                                '3. Compute the new latency of the retrieval step and compare it with the sequential version.\n'
                                '4. Explain what the merge step must do when one search is slow or fails (timeout, partial results).',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['parallelization', 'orchestration']},
               {'id': 'M01.L04.EX09',
                'title': 'Choose auto-scaling signals',
                'lesson_code': 'M01.L04',
                'section_id': 'independent-autoscaling',
                'placement': 'after_section',
                'description': 'Assign an appropriate scaling signal to orchestrator, retrieval, '
                               'and GPU model services.',
                'instructions': '1. List the three services: the orchestrator API, the retrieval/vector service, and the GPU model server.\n'
                                '2. Choose a scaling signal for each (for example request concurrency, query latency, GPU utilization or queue depth).\n'
                                '3. Explain why CPU utilization alone is a poor signal for the GPU model server.\n'
                                '4. State the cold-start risk for each service and how you would soften it.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['autoscaling', 'microservices']},
               {'id': 'M01.L04.EX10',
                'title': 'Design a cache hierarchy',
                'lesson_code': 'M01.L04',
                'section_id': 'cache-layers',
                'placement': 'after_section',
                'description': 'Choose full-response, retrieval, and chunk caches for a support '
                               'assistant and explain which expensive work each cache avoids.',
                'instructions': '1. Define a full-response cache, a retrieval-results cache, and a chunk/embedding cache for a support assistant.\n'
                                '2. For each cache, write the key, what it stores, and the expensive work it avoids.\n'
                                '3. Choose a time-to-live for each and explain the staleness risk.\n'
                                '4. State which requests must never be served from the full-response cache (for example personalized or permission-dependent answers).',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['caching', 'latency']},
               {'id': 'M01.L04.EX11',
                'title': 'Tune a semantic cache threshold',
                'lesson_code': 'M01.L04',
                'section_id': 'semantic-cache',
                'placement': 'after_section',
                'description': 'Reason about the failure modes of a semantic similarity threshold '
                               'that is too high or too low and propose an evaluation plan.',
                'instructions': '1. Describe what goes wrong when the similarity threshold is too low (wrong cached answers served to different questions).\n'
                                '2. Describe what goes wrong when it is too high (almost no cache hits, no savings).\n'
                                '3. Write two question pairs that look similar but need different answers.\n'
                                '4. Propose an evaluation: a labeled set of question pairs, the hit rate and false-hit rate you measure, and how you choose the threshold.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['semantic-cache', 'evaluation']},
               {'id': 'M01.L04.EX12',
                'title': 'Design event-driven invalidation',
                'lesson_code': 'M01.L04',
                'section_id': 'cache-invalidation',
                'placement': 'after_section',
                'description': 'Create a document-change-to-cache-purge workflow that prevents '
                               'stale policy answers.',
                'instructions': '1. Define the event emitted when a policy document changes, including the document ID and version.\n'
                                '2. List every cache entry that depends on that document (responses, retrieval results, chunks) and how you find them.\n'
                                '3. Describe the purge and re-index order so that no stale answer is served in between.\n'
                                '4. State how you verify that the next question about the policy returns the new answer.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['cache-invalidation', 'freshness']},
               {'id': 'M01.L04.EX13',
                'title': 'Build a defense-in-depth map',
                'lesson_code': 'M01.L04',
                'section_id': 'security-overview',
                'placement': 'after_section',
                'description': 'Map controls to ingestion, storage, retrieval, generation, and '
                               'monitoring for a sensitive enterprise RAG system.',
                'instructions': '1. Create a table with rows for ingestion, storage, retrieval, generation, and monitoring.\n'
                                '2. Put at least one control in each row (for example malware and PII scanning, encryption, permission filtering, output redaction, audit alerts).\n'
                                '3. For each control, name the threat it addresses.\n'
                                '4. Explain which control still protects the system if the one before it fails.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['security', 'defense-in-depth']},
               {'id': 'M01.L04.EX14',
                'title': 'Preserve meaning while redacting',
                'lesson_code': 'M01.L04',
                'section_id': 'redaction-tradeoff',
                'placement': 'after_section',
                'description': 'Compare generic masking with typed masking for a sensitive '
                               'sentence and explain the impact on RAG usefulness.',
                'instructions': "1. Sentence: 'Maria Lopez (account 4417) disputed a $1,200 charge on 3 May.'\n"
                                '2. Mask it generically (every sensitive span becomes [REDACTED]).\n'
                                '3. Mask it with typed placeholders (for example [PERSON], [ACCOUNT_ID], [AMOUNT], [DATE]).\n'
                                "4. Explain which version still lets RAG answer questions such as 'what kinds of disputes happen?' and why.",
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['privacy', 'redaction']},
               {'id': 'M01.L04.EX15',
                'title': 'Enforce authorization before generation',
                'lesson_code': 'M01.L04',
                'section_id': 'permission-filtering',
                'placement': 'after_section',
                'description': 'Design a metadata and query-time filtering scheme that prevents '
                               "confidential chunks from reaching an unauthorized user's prompt.",
                'instructions': '1. Define the access metadata stored on every chunk (for example department, sensitivity, allowed groups).\n'
                                "2. Show how the user's groups become a filter applied inside the retrieval query, before any chunk is returned.\n"
                                '3. Explain why filtering after generation is too late.\n'
                                "4. Describe a test that proves a confidential chunk never reaches an unauthorized user's prompt.",
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rbac', 'access-control']},
               {'id': 'M01.L04.EX16',
                'title': 'Operationalize guardrails',
                'lesson_code': 'M01.L04',
                'section_id': 'generation-guardrails',
                'placement': 'after_section',
                'description': 'Define the logging, reporting, and incident-review loop for unsafe '
                               'or noncompliant generated outputs.',
                'instructions': '1. Define what is logged when a guardrail blocks or flags an output (input, output, rule triggered, model version, user, time).\n'
                                '2. Define the regular report: which counts and trends are reviewed and by whom.\n'
                                '3. Describe the incident-review steps for one serious unsafe output, from detection to fix.\n'
                                '4. Explain how a reviewed incident becomes a new test case or rule.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['guardrails', 'operations']},
               {'id': 'M01.L04.EX17',
                'title': 'Evaluate a new vendor',
                'lesson_code': 'M01.L04',
                'section_id': 'vendor-checklist',
                'placement': 'after_section',
                'description': "Use the chapter's vendor checklist to assess a hypothetical "
                               'managed reranker and identify unresolved risks.',
                'instructions': '1. Take a hypothetical managed reranker API and apply the vendor checklist from the lesson.\n'
                                '2. For each checklist item, write what you would ask the vendor and what evidence would satisfy you.\n'
                                '3. Mark the items that are still unresolved.\n'
                                '4. Decide whether you would run a pilot, and state the exit plan if the vendor fails.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['vendor-management', 'architecture']},
               {'id': 'M01.L04.EX18',
                'title': 'Make a build-versus-buy decision',
                'lesson_code': 'M01.L04',
                'section_id': 'build-vs-buy',
                'placement': 'after_section',
                'description': 'Classify several RAG components as differentiating or '
                               'nondifferentiating and justify which should be built internally.',
                'instructions': '1. List the components: document parsing, embedding model, vector database, reranker, prompt and answer logic, evaluation suite, and access control.\n'
                                '2. Mark each component differentiating (it makes your product better than competitors) or nondifferentiating.\n'
                                '3. Decide build or buy for each and justify the decision.\n'
                                '4. Name one component where buying now and building later makes sense.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['build-vs-buy', 'strategy']},
               {'id': 'M01.L04.EX19',
                'title': 'Construct a TCO model',
                'lesson_code': 'M01.L04',
                'section_id': 'tco-overview',
                'placement': 'after_section',
                'description': 'Build a cost table that separates direct, indirect, HA, security, '
                               'and staffing costs for a production RAG deployment.',
                'instructions': '1. Create a table with rows for direct costs (compute, storage, API calls), indirect costs, high availability, security, and staffing.\n'
                                '2. Fill in one estimate per row for a year, writing the assumption behind each number.\n'
                                '3. Mark which costs grow with query volume and which stay fixed.\n'
                                '4. Identify the largest cost and one assumption that would change the total the most if it were wrong.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['tco', 'cost-modeling']},
               {'id': 'M01.L04.EX20',
                'title': 'Turn POC results into production KPIs',
                'lesson_code': 'M01.L04',
                'section_id': 'requirements-kpis',
                'placement': 'after_section',
                'description': 'Translate vague goals such as fast, reliable, and accurate into '
                               'measurable production requirements and acceptance tests.',
                'instructions': '1. Take three vague goals: fast, reliable, and accurate.\n'
                                '2. Turn each into a measurable KPI with a number (for example p95 latency under 2 s, 99.9% monthly availability, 90% of answers supported by citations on the evaluation set).\n'
                                '3. Write one acceptance test per KPI that must pass before launch.\n'
                                '4. Explain how each KPI is monitored after launch and who acts when it is breached.',
                'expected_output': 'A concise but technically justified design, table, workflow, '
                                   'calculation, prompt, or written analysis that could be '
                                   'reviewed by an engineering team.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['kpi', 'production-planning']}],
 'quiz': {'id': 'M01.L04.QZ01',
          'title': 'Deploying RAG to Production — Knowledge Check',
          'lesson_code': 'M01.L04',
          'placement': 'lesson_end',
          'questions': [{'id': 'M01.L04.Q01',
                         'section_id': 'quality-failure-tree',
                         'question': 'A production RAG answer is wrong. What should you verify '
                                     "first according to the lesson's debugging order?",
                         'options': ['Whether the LLM temperature is zero',
                                     'Whether the required information exists in the source data',
                                     'Whether the UI uses streaming',
                                     'Whether the vector database is self-hosted'],
                         'correct': 1,
                         'explanation': 'The first diagnostic step is to verify data coverage. '
                                        'Prompt or model tuning cannot recover knowledge that is '
                                        'absent from the corpus.'},
                        {'id': 'M01.L04.Q02',
                         'section_id': 'staging-index',
                         'question': 'What is the main purpose of a staging collection before '
                                     'promoting new RAG data?',
                         'options': ['To reduce the embedding dimension',
                                     'To validate ingestion and retrieval before touching the live '
                                     'index',
                                     'To replace the production vector database permanently',
                                     'To cache final LLM responses'],
                         'correct': 1,
                         'explanation': 'Staging protects production from malformed text, '
                                        'metadata, or indexing changes by providing a place to run '
                                        'retrieval and formatting checks first.'},
                        {'id': 'M01.L04.Q03',
                         'section_id': 'tail-latency',
                         'question': 'Why is P95 latency useful in production monitoring?',
                         'options': ['It shows only the fastest requests',
                                     'It measures storage size',
                                     'It reveals the slow experience affecting a meaningful '
                                     'minority of users',
                                     'It replaces end-to-end tracing'],
                         'correct': 2,
                         'explanation': 'Averages can hide slow tails. P95 makes the slower user '
                                        'experience visible and helps expose overload or expensive '
                                        'query paths.'},
                        {'id': 'M01.L04.Q04',
                         'section_id': 'fanout-gather',
                         'question': 'What is the latency advantage of running semantic and '
                                     'lexical search in parallel?',
                         'options': ['Their latencies are multiplied',
                                     'Total retrieval time is driven roughly by the slower branch '
                                     'rather than the sum',
                                     'Reranking becomes unnecessary',
                                     'The query no longer needs an embedding'],
                         'correct': 1,
                         'explanation': 'Fan-out/gather overlaps independent work, so semantic and '
                                        'lexical search do not add their full latencies '
                                        'sequentially.'},
                        {'id': 'M01.L04.Q05',
                         'section_id': 'independent-autoscaling',
                         'question': 'Why should RAG microservices scale independently?',
                         'options': ['Every component uses exactly the same resources',
                                     'Different services have different bottlenecks such as CPU, '
                                     'I/O, memory, or GPU load',
                                     'It prevents any need for monitoring',
                                     'It guarantees zero downtime'],
                         'correct': 1,
                         'explanation': "Independent scaling matches capacity to each service's "
                                        'actual resource pressure instead of duplicating the '
                                        'entire stack.'},
                        {'id': 'M01.L04.Q06',
                         'section_id': 'semantic-cache',
                         'question': 'What distinguishes semantic caching from exact-string '
                                     'caching?',
                         'options': ['It stores only images',
                                     'It uses embedding similarity to match differently worded '
                                     'queries with similar meaning',
                                     'It disables cache invalidation',
                                     'It can only cache final responses'],
                         'correct': 1,
                         'explanation': 'Semantic caching embeds queries and reuses prior results '
                                        'when the meanings are sufficiently close, even if wording '
                                        'differs.'},
                        {'id': 'M01.L04.Q07',
                         'section_id': 'cache-invalidation',
                         'question': 'Why can TTL-only cache expiration be insufficient for a '
                                     'frequently updated knowledge base?',
                         'options': ['TTL increases embedding dimensions',
                                     'A stale answer can remain available until expiry even after '
                                     'its source document changes',
                                     'TTL prevents horizontal scaling',
                                     'TTL removes all cached entries immediately'],
                         'correct': 1,
                         'explanation': 'Event-driven invalidation can purge affected entries as '
                                        'soon as documents change instead of waiting for an '
                                        'arbitrary expiration time.'},
                        {'id': 'M01.L04.Q08',
                         'section_id': 'redaction-tradeoff',
                         'question': 'What advantage does typed masking have over replacing every '
                                     'sensitive value with the same generic token?',
                         'options': ['It exposes the original secret value',
                                     'It preserves semantic roles such as doctor, medication, and '
                                     'patient while hiding identities',
                                     'It makes encryption unnecessary',
                                     'It guarantees perfect retrieval'],
                         'correct': 1,
                         'explanation': 'Typed masking keeps role information that may be '
                                        'important to retrieval and generation while removing '
                                        'specific sensitive values.'},
                        {'id': 'M01.L04.Q09',
                         'section_id': 'permission-filtering',
                         'question': 'Where should permission filtering be enforced to prevent '
                                     'data leakage?',
                         'options': ['Only after the final answer is displayed',
                                     'Before unauthorized chunks are included in the LLM prompt',
                                     'Only in the browser UI',
                                     'Only when documents are uploaded'],
                         'correct': 1,
                         'explanation': 'The key protection is to ensure chunks the user is not '
                                        'authorized to see never enter the generation context.'},
                        {'id': 'M01.L04.Q10',
                         'section_id': 'vendor-checklist',
                         'question': 'Which vendor metric is especially important for '
                                     'understanding slow production requests?',
                         'options': ['Logo size',
                                     'P95/P99 latency',
                                     'Number of marketing pages',
                                     'Embedding color'],
                         'correct': 1,
                         'explanation': 'High-percentile latency reveals tail behavior that can '
                                        'dominate real user experience even when averages look '
                                        'acceptable.'},
                        {'id': 'M01.L04.Q11',
                         'section_id': 'tco-overview',
                         'question': 'Which item belongs in production RAG total cost of ownership '
                                     'but may be missed if you look only at API invoices?',
                         'options': ['Engineering support, staging, monitoring, and security work',
                                     "Only the user's browser cache",
                                     'Only the model name',
                                     'Only document filenames'],
                         'correct': 0,
                         'explanation': 'TCO includes direct and indirect operational costs such '
                                        'as staff, environments, observability, security, support, '
                                        'and HA.'},
                        {'id': 'M01.L04.Q12',
                         'section_id': 'cost-monitoring',
                         'question': 'How does rate limiting help with cost control?',
                         'options': ["It increases every query's token count",
                                     'It prevents a faulty or malicious source from generating '
                                     'unbounded expensive requests',
                                     'It removes the need for budgets',
                                     'It guarantees answer correctness'],
                         'correct': 1,
                         'explanation': 'Rate limiting limits how quickly usage and spend can '
                                        'grow, reducing denial-of-wallet risk.'},
                        {'id': 'M01.L04.Q13',
                         'section_id': 'model-router',
                         'question': 'What is the purpose of a cascading model router?',
                         'options': ['Send every request to the most expensive model',
                                     'Route simple queries to cheaper models and escalate harder '
                                     'queries when needed',
                                     'Eliminate retrieval',
                                     'Replace all monitoring'],
                         'correct': 1,
                         'explanation': 'Routing aims to preserve quality on difficult queries '
                                        'while lowering average cost and latency for simpler '
                                        'ones.'},
                        {'id': 'M01.L04.Q14',
                         'section_id': 'rag-evaluation',
                         'question': 'Why is evaluation still required after a RAG system reaches '
                                     'production?',
                         'options': ['Because data, prompts, models, indexes, and traffic continue '
                                     'to change',
                                     'Because production systems never need monitoring',
                                     'Because evaluation replaces security',
                                     'Because every query must be manually graded'],
                         'correct': 0,
                         'explanation': 'Continuous changes can introduce regressions, so '
                                        'evaluation becomes an ongoing production control rather '
                                        'than a one-time experiment.'},
                        {'id': 'M01.L04.Q15',
                         'section_id': 'reference-architecture-query',
                         'question': 'What normally happens after semantic and lexical candidates '
                                     'are collected in the reference query flow?',
                         'options': ['They are discarded',
                                     'They are combined and reranked before generation',
                                     'They are written back into the source documents',
                                     'They bypass authorization'],
                         'correct': 1,
                         'explanation': 'The reference architecture combines candidate sets, '
                                        'reranks them, and then prepares the selected context for '
                                        'generation.'},
                        {'id': 'M01.L04.Q16',
                         'section_id': 'requirements-kpis',
                         'question': 'Why should production goals be expressed as measurable KPIs?',
                         'options': ['To make requirements testable and comparable against POC '
                                     'performance',
                                     'To avoid monitoring',
                                     'To hide system trade-offs',
                                     'To guarantee all vendors use the same technology'],
                         'correct': 0,
                         'explanation': "Numeric targets convert vague objectives such as 'fast' "
                                        "and 'accurate' into acceptance criteria that can be "
                                        'measured.'},
                        {'id': 'M01.L04.Q17',
                         'section_id': 'adoption-signals',
                         'question': 'A newly launched RAG app sees a large usage spike followed '
                                     'by a sharp decline. What is a reasonable interpretation?',
                         'options': ['The system is definitely successful',
                                     'Users may be abandoning it because of quality, latency, or '
                                     'usability problems',
                                     'The vector dimensions are too high by definition',
                                     'No further investigation is needed'],
                         'correct': 1,
                         'explanation': 'The chapter treats falling usage as a diagnostic signal '
                                        'that should be investigated together with quality and '
                                        'latency telemetry.'},
                        {'id': 'M01.L04.Q18',
                         'section_id': 'component-upgrades',
                         'question': 'A new embedding model scores better on a benchmark. What '
                                     'should happen before production adoption?',
                         'options': ['Replace the old model immediately',
                                     'Run end-to-end RAG evaluation and check latency, hardware, '
                                     'dependencies, and ingest/query compatibility',
                                     'Change only the UI',
                                     'Disable staging'],
                         'correct': 1,
                         'explanation': 'A component benchmark improvement does not prove a '
                                        'production system improvement; end-to-end impact must be '
                                        'validated.'},
                        {'id': 'M01.L04.Q19',
                         'section_id': 'production-data-hygiene',
                         'question': 'Why can the RAG team not solve all data-quality problems '
                                     'inside the retrieval pipeline?',
                         'options': ['Source systems may contain obsolete, conflicting, or '
                                     'duplicate documents that require organizational ownership '
                                     'and governance',
                                     'Vector databases cannot store text',
                                     'LLMs cannot read documents',
                                     'Monitoring prevents data updates'],
                         'correct': 0,
                         'explanation': 'Upstream data hygiene and source-of-truth governance '
                                        'require participation from content owners; downstream '
                                        'retrieval cannot fully repair bad authoritative data.'},
                        {'id': 'M01.L04.Q20',
                         'section_id': 'continuous-improvement',
                         'type': 'open',
                         'question': 'You are moving a successful internal RAG POC into '
                                     'production. Propose an end-to-end plan covering quality, '
                                     'latency, security, cost, architecture, monitoring, launch, '
                                     'and future upgrades. Explain the dependencies among your '
                                     'choices.'}],
          'passing_score': 70}}
