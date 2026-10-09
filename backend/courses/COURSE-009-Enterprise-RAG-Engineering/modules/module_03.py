"""M01.L03 — Scaling Your RAG Stack.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 3, pages not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L03"

MODULE_ORDER = 1

MODULE_TITLE = "RAG Foundations"

MODULE_DESCRIPTION = (
    "Scale a base RAG system into a production-ready architecture with resilient ingestion, "
    "advanced retrieval, safety and faithfulness controls, and a trustworthy user experience."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {'title': 'Scaling Your RAG Stack',
 'slug': 'rag-foundations-m01-l03',
 'description': 'A production-focused lesson on scaling RAG ingestion, retrieval, guardrails, '
                'hallucination control, cost/latency trade-offs, and evidence-centered user '
                'experience.',
 'order': 3,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 10.0,
 'skill_tags': ['rag',
                'scaling',
                'distributed-ingestion',
                'idempotency',
                'observability',
                'incremental-indexing',
                'hybrid-search',
                'bm25',
                'rrf',
                'reranking',
                'mmr',
                'guardrails',
                'prompt-injection',
                'hallucination-detection',
                'rag-ux',
                'module-01'],
 'prerequisite_ids': ['M01.L01', 'M01.L02'],
 'lesson': {'title': 'Scaling Your RAG Stack',
            'content': '# Scaling Your RAG Stack\n'
                       '\n'
                       '> **Course:** Retrieval-Augmented Generation (RAG)  \n'
                       '> **Lesson:** M01.L03  \n'
                       '> **Module:** RAG Foundations  \n'
                       '> **Source alignment:** Supplied source, Chapter 3. Page numbers were not '
                       'provided in the supplied source. This lesson is an instructor-authored '
                       'curriculum adaptation rather than a reproduction of the source text.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Learning outcomes\n'
                       '\n'
                       'By the end of this lesson, you should be able to:\n'
                       '\n'
                       '- Explain why document volume, document size, query load, and retrieval '
                       'noise change RAG architecture at scale.\n'
                       '- Design restartable, observable, idempotent ingestion pipelines for large '
                       'and changing corpora.\n'
                       '- Diagnose OCR, boilerplate, encoding, metadata, and very-large-document '
                       'ingestion problems.\n'
                       '- Explain incremental refresh, change detection, asynchronous ingestion, '
                       'and near-real-time indexing.\n'
                       '- Design a two-stage retrieval pipeline and distinguish recall-oriented '
                       'candidate generation from precision-oriented reranking.\n'
                       '- Explain lexical search, BM25, hybrid retrieval, RRF, weighted fusion, '
                       'cross-encoder reranking, MMR, and custom reranking.\n'
                       '- Place guardrails across the query flow and reason about direct and '
                       'indirect prompt-injection risks.\n'
                       '- Diagnose retrieval, data-quality, and generation causes of RAG '
                       'hallucinations.\n'
                       '- Compare LLM-as-a-judge and dedicated faithfulness models, and design '
                       'correction or refusal policies.\n'
                       '- Design RAG interfaces that expose sources, progress, feedback, errors, '
                       'and multimodal evidence clearly.\n'
                       '- Balance response quality, latency, and cost when adding enterprise '
                       'controls.\n'
                       '- Reason about the RAG stack as one interacting production system rather '
                       'than isolated components.\n'
                       '\n'
                       '---\n'
                       '## 1. RAG at scale changes the engineering problem\n'
                       '\n'
                       'A RAG prototype can look convincing with a few documents and a handful of '
                       'users. At enterprise scale, however, the same design is exposed to much '
                       'larger document collections, more document formats, rapidly changing data, '
                       'and many simultaneous queries. Scale therefore changes the problem from '
                       '"can retrieval work?" to "can retrieval remain accurate, fresh, fast, '
                       'observable, safe, and affordable under continuous load?"\n'
                       '\n'
                       'A useful way to think about scale is to separate four pressures:\n'
                       '\n'
                       '```text\n'
                       'data volume      → more documents, chunks, vectors, and metadata\n'
                       'query volume     → more concurrent retrieval and generation work\n'
                       'data complexity  → more formats, OCR, tables, images, and edge cases\n'
                       'quality pressure → harder retrieval, more guardrails, stricter evaluation\n'
                       '```\n'
                       '\n'
                       'The central lesson is that scaling RAG is not achieved by increasing one '
                       'machine size. It requires redesigning ingestion, retrieval, generation '
                       'controls, and user experience as coordinated subsystems.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Enterprise RAG scaling map | Diagram showing data volume, '
                       'query load, data complexity, retrieval quality, guardrails, and UX '
                       'surrounding a central RAG pipeline | Learner should notice that scale '
                       'affects several interacting dimensions, not one component]]\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 2. Document volume, document size, and query load\n'
                       '\n'
                       'Three dimensions grow independently. First, the corpus may contain '
                       'hundreds of thousands or millions of documents. Second, a single document '
                       'may contain thousands of pages, producing huge numbers of chunks. Third, '
                       'query traffic can grow to high queries per second (QPS).\n'
                       '\n'
                       'Each dimension stresses a different part of the stack. More documents '
                       'increase indexing time and search difficulty. Larger files create parsing '
                       'and memory problems. Higher QPS creates concurrency, rate-limiting, '
                       'caching, and horizontal-scaling requirements. A production design must '
                       'identify which dimension is actually limiting the system instead of '
                       'treating "scale" as one generic problem.\n'
                       '\n'
                       '{{exercise:M01.L03.EX01}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 3. Why retrieval becomes harder as the corpus grows\n'
                       '\n'
                       'With a small corpus, the correct chunk has relatively few competitors. As '
                       'the corpus grows, many chunks become superficially similar to the query. A '
                       'top-k search can therefore contain more noise, duplicated information, or '
                       'passages that match the topic but not the actual intent.\n'
                       '\n'
                       'This creates a signal-to-noise problem: the answer-bearing chunk may still '
                       'exist in the index, but it may be pushed below the retrieval cutoff. The '
                       'generator cannot repair evidence that was never retrieved. This is why '
                       'large systems often move beyond a single vector similarity search toward '
                       'metadata filters, hybrid search, candidate generation, and reranking.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 4. Index freshness and incremental updates\n'
                       '\n'
                       'A RAG system is only as current as the searchable index behind it. '
                       'Rebuilding an index from scratch whenever one document changes becomes '
                       'impractical when the corpus contains millions of records.\n'
                       '\n'
                       'The scalable alternative is an incremental update pipeline. It detects '
                       'which sources are new, modified, or deleted, then reprocesses only '
                       'affected documents or chunks. The pipeline must also remove stale vectors '
                       'and metadata when source content is deleted.\n'
                       '\n'
                       'A useful invariant is:\n'
                       '\n'
                       '```text\n'
                       'source state ≈ indexed state\n'
                       '```\n'
                       '\n'
                       'The smaller the delay between those two states, the fresher the RAG '
                       'system. Freshness is therefore an operational property, not merely a '
                       'retrieval algorithm choice.\n'
                       '\n'
                       '{{exercise:M01.L03.EX02}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 5. Understanding RAG cost as a system\n'
                       '\n'
                       'At scale, cost comes from several layers: raw and processed storage, '
                       'embedding generation, vector and lexical indexes, retrieval compute, LLM '
                       'inference, network traffic, monitoring, and operational tooling. Looking '
                       'only at the LLM API price hides much of the total cost.\n'
                       '\n'
                       'The source chapter illustrates this with a large customer-support corpus. '
                       'The important lesson is not the exact dollar amount, which depends on time '
                       'and provider pricing, but the accounting method: estimate total source '
                       'tokens, one-time or refresh embedding cost, per-query prompt and output '
                       'tokens, index infrastructure, and supporting DevOps costs separately.\n'
                       '\n'
                       'A cost model should answer: Which costs scale with corpus size? Which '
                       'scale with query traffic? Which are one-time? Which recur whenever data '
                       'changes?\n'
                       '\n'
                       '{{exercise:M01.L03.EX03}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 6. Token economics, caching, and model routing\n'
                       '\n'
                       'Generation often becomes the dominant recurring expense because every '
                       'query may send thousands of context tokens to an LLM. Two architectural '
                       'controls are especially important.\n'
                       '\n'
                       '**Multilevel caching** can reuse outputs at several stages: query '
                       'embeddings, retrieval results, reranking outputs, or final responses. '
                       '**Dynamic model routing** sends straightforward requests to cheaper and '
                       'faster models while reserving expensive reasoning models for difficult '
                       'cases.\n'
                       '\n'
                       'The general principle is to avoid recomputing work whose inputs have not '
                       'meaningfully changed, and to avoid paying premium inference cost when the '
                       'task does not need premium capability.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 7. Treat ingestion as production data infrastructure\n'
                       '\n'
                       'A script that loops over files is sufficient for experimentation, but a '
                       'large ingestion system behaves more like an ETL platform. It needs '
                       'scheduling, retries, progress tracking, versioning, observability, failure '
                       'isolation, and controlled rollout of parsing or chunking changes.\n'
                       '\n'
                       'This shift matters because ingestion errors are upstream errors. Once '
                       'malformed text, missing metadata, or outdated content is embedded and '
                       'indexed, downstream retrieval operates on corrupted evidence. Production '
                       'ingestion therefore deserves the same engineering discipline as any other '
                       'critical data pipeline.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 8. The large-volume ingestion pipeline\n'
                       '\n'
                       'Large-scale ingestion is a sequence of expensive transformations:\n'
                       '\n'
                       '```text\n'
                       'read source\n'
                       '→ parse / extract\n'
                       '→ clean and normalize\n'
                       '→ chunk\n'
                       '→ extract metadata\n'
                       '→ embed chunks\n'
                       '→ write vectors + text + metadata\n'
                       '→ build or update indexes\n'
                       '```\n'
                       '\n'
                       'The embedding stage is often computationally intensive, while parsing may '
                       'be I/O-heavy and format-specific. Metadata extraction adds additional work '
                       'but is essential for later filtering and citations. Index writes also '
                       'become slower as indexes grow. The pipeline must therefore be measured '
                       'stage by stage rather than timed only as one giant job.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Distributed ingestion pipeline | Source documents fan out '
                       'to parsing, cleaning, chunking, metadata extraction, embedding workers, '
                       'then converge on vector and metadata stores with retries and observability '
                       '| Learner should notice parallel stages, checkpoints, and failure '
                       'isolation]]\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 9. Metadata is part of retrieval quality\n'
                       '\n'
                       'Metadata such as source URL, document ID, page number, author, date, '
                       'department, and section heading is not decorative. It enables structured '
                       'filtering, source attribution, access control, freshness logic, and better '
                       'context during generation.\n'
                       '\n'
                       'A scalable pipeline must preserve the relationship between each chunk and '
                       'its metadata through every transformation. If a chunk loses its source '
                       'identity or page information, the system may still retrieve text but will '
                       'struggle to filter correctly or provide trustworthy citations.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 10. Brittleness: why restart-from-zero is unacceptable\n'
                       '\n'
                       'Suppose an ingestion run processes hundreds of thousands of documents and '
                       'fails near the end because of one corrupt file or network timeout. If the '
                       'pipeline can only restart from the beginning, a small failure can waste '
                       'hours or days of work.\n'
                       '\n'
                       'A scalable pipeline therefore needs checkpoints, durable task state, '
                       'failure isolation, and the ability to resume. The goal is not to design a '
                       'pipeline that never fails. At large scale, some failure is expected. The '
                       'goal is to make failures local, visible, recoverable, and cheap.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 11. Parallel and distributed processing\n'
                       '\n'
                       'Independent documents can often be parsed, chunked, or embedded '
                       'concurrently. Parallel processing reduces wall-clock time by distributing '
                       'work across CPU processes, machines, or GPUs. Frameworks such as Ray, '
                       'Dask, Spark, or similar systems can coordinate this work depending on the '
                       'workload.\n'
                       '\n'
                       'Embedding generation benefits strongly from batching because accelerators '
                       'are more efficient when processing multiple texts together. Parsing and '
                       'metadata extraction can also be parallelized, but care is needed around '
                       'shared resources, API limits, and memory pressure.\n'
                       '\n'
                       'Parallelism improves throughput; it does not remove the need for '
                       'correctness, checkpointing, and retries.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 12. Pipeline orchestration and dependency management\n'
                       '\n'
                       'A workflow orchestrator represents ingestion as dependent stages rather '
                       'than one long script. For example, embedding should not begin until the '
                       'corresponding chunks exist, while independent documents may be processed '
                       'in parallel.\n'
                       '\n'
                       'An orchestrator can schedule tasks, retry failures, isolate problematic '
                       'inputs, trigger alerts, and expose progress. This is especially valuable '
                       'when the same pipeline must run repeatedly for refresh jobs.\n'
                       '\n'
                       'The important mental model is a directed workflow of restartable tasks, '
                       'not a single process with a long call stack.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 13. Idempotency: safe retries without duplication\n'
                       '\n'
                       'A task is **idempotent** when repeating it produces the same intended '
                       'state instead of duplicating side effects. In RAG ingestion, this might '
                       'mean that retrying a chunk-indexing task updates or upserts the same chunk '
                       'identity rather than inserting a second copy.\n'
                       '\n'
                       'Idempotency turns retries from a dangerous emergency mechanism into a '
                       'normal reliability feature. Stable document IDs, stable chunk IDs, version '
                       'fields, and upsert semantics are common building blocks.\n'
                       '\n'
                       'Without idempotency, an automatic retry can silently create duplicate '
                       'chunks, which then pollute retrieval and distort ranking.\n'
                       '\n'
                       '{{exercise:M01.L03.EX04}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 14. Deep observability for ingestion\n'
                       '\n'
                       'A healthy pipeline needs more than exception logs. It should expose '
                       'throughput such as documents per second and chunks per second, resource '
                       'utilization, queue depth, retry counts, failed-document counts, and stage '
                       'latency.\n'
                       '\n'
                       'It should also reveal silent failures: stalled records that never finish, '
                       'documents filtered out unexpectedly, or a stage that succeeds technically '
                       'but emits zero chunks. These problems may not raise exceptions, yet they '
                       'damage the knowledge base.\n'
                       '\n'
                       'Observability should therefore answer both "did the task crash?" and "did '
                       'the task produce the expected data?".\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 15. Inconsistent data quality is a production norm\n'
                       '\n'
                       'Enterprise corpora contain scanned PDFs, repeated boilerplate, malformed '
                       'encodings, inconsistent layouts, old versions, and corrupted files. A '
                       'single universal parser is rarely sufficient.\n'
                       '\n'
                       'Poor input quality propagates: noisy text is chunked, embedded, and '
                       'stored, contaminating retrieval. The correct response is a conditional '
                       'preprocessing pipeline that first inspects the document and then chooses '
                       'an appropriate path.\n'
                       '\n'
                       '```text\n'
                       'inspect document\n'
                       '→ classify format/quality\n'
                       '→ choose parser or OCR path\n'
                       '→ clean / normalize\n'
                       '→ validate output\n'
                       '→ continue ingestion\n'
                       '```\n'
                       '\n'
                       '[[IMAGE_NEEDED: Conditional document triage | Decision tree routing native '
                       'PDFs, scanned PDFs, HTML, and malformed files through parser, OCR, '
                       'boilerplate removal, or quarantine paths | Learner should notice that '
                       'different document qualities require different preprocessing]]\n'
                       '\n'
                       '{{exercise:M01.L03.EX05}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 16. OCR, boilerplate, and encoding failures\n'
                       '\n'
                       'OCR may confuse visually similar characters, which is especially damaging '
                       'for IDs, codes, or exact names. Boilerplate repeated on every page can '
                       'dominate embeddings and cause irrelevant retrieval. Character-encoding '
                       'mistakes can transform readable punctuation or text into corrupted '
                       'symbols.\n'
                       '\n'
                       'These are not cosmetic defects. They alter the strings that chunkers and '
                       'embedding models receive. A quality pipeline therefore needs cleaning '
                       'rules, duplicate or boilerplate suppression, encoding normalization, and '
                       'validation checks before indexing.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 17. Document triage and conditional routing\n'
                       '\n'
                       'A scalable ingestion pipeline can begin with a triage stage. A native PDF '
                       'with extractable text may use a fast parser, while an image-only PDF may '
                       'require OCR. HTML may require navigation and boilerplate stripping. A '
                       'complex form may require a more specialized parser.\n'
                       '\n'
                       'The key idea is **cheapest correct path first**: do not apply the most '
                       'expensive parser to every document. Detect what the file needs, route it '
                       'appropriately, and reserve expensive techniques for difficult cases.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 18. Very large documents require streamed processing\n'
                       '\n'
                       'Loading a multi-thousand-page document into memory is risky and '
                       'unnecessary. A better strategy is incremental processing: read a page or '
                       'page range, extract content, chunk it, persist results, release memory, '
                       'and continue.\n'
                       '\n'
                       'Streaming reduces peak memory and allows useful output to appear before '
                       'the entire file finishes. It also makes checkpoints more natural. The '
                       'design must preserve cross-page structures when needed—for example, a '
                       'table or section that spans a boundary should not be split blindly.\n'
                       '\n'
                       '{{exercise:M01.L03.EX06}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 19. Splitting a large PDF safely\n'
                       '\n'
                       'The chapter demonstrates dividing a large PDF into page-range files. '
                       'Conceptually, the algorithm is straightforward: determine total pages, '
                       'compute the number of ranges, create a new writer for each range, copy '
                       'those pages, and persist each chunk.\n'
                       '\n'
                       '```python\n'
                       'num_parts = ceil(total_pages / pages_per_part)\n'
                       'for part in range(num_parts):\n'
                       '    start = part * pages_per_part\n'
                       '    end = min(start + pages_per_part, total_pages)\n'
                       '    # copy pages[start:end] into a new PDF\n'
                       '```\n'
                       '\n'
                       'The engineering lesson is more important than the exact library: split '
                       'work into bounded units that can be processed and retried independently. '
                       'Boundaries should be chosen carefully so important structures are not '
                       'broken.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 20. Document refresh and near-real-time indexing\n'
                       '\n'
                       'Production knowledge changes. New documents arrive, existing documents are '
                       'revised, and old ones are deleted. A refresh system must propagate those '
                       'changes into the searchable index.\n'
                       '\n'
                       'For some applications, minutes or hours of delay are unacceptable. '
                       'Near-real-time indexing aims to make new knowledge searchable within '
                       'seconds. This requires fast ingestion stages, asynchronous processing, and '
                       'a storage layer that can accept incremental updates efficiently.\n'
                       '\n'
                       'Freshness requirements should be defined explicitly because they strongly '
                       'affect architecture and cost.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 21. Change detection and asynchronous indexing\n'
                       '\n'
                       'Incremental updates begin with detecting change. Change data capture '
                       '(CDC), source events, timestamps, version hashes, or database transaction '
                       'logs can tell the pipeline what changed.\n'
                       '\n'
                       'A common service pattern is:\n'
                       '\n'
                       '```text\n'
                       'source update\n'
                       '→ accept event / upload\n'
                       '→ acknowledge receipt\n'
                       '→ enqueue indexing work\n'
                       '→ parse + chunk + embed asynchronously\n'
                       '→ update index\n'
                       '→ mark version searchable\n'
                       '```\n'
                       '\n'
                       'Acknowledging receipt separately from completing indexing prevents '
                       'long-running ingestion work from blocking user-facing APIs.\n'
                       '\n'
                       '{{exercise:M01.L03.EX07}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 22. Designing for fast index updates\n'
                       '\n'
                       'Instant or near-real-time indexing is not only an ingestion concern. The '
                       'vector database and index type must support frequent inserts or updates '
                       'without forcing long rebuilds. Different systems make different trade-offs '
                       'among update latency, query latency, memory, persistence, and index '
                       'quality.\n'
                       '\n'
                       'Therefore, vector database selection should include update behavior as a '
                       'first-class requirement, not just benchmarked query speed.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 23. Why basic vector search is not enough at scale\n'
                       '\n'
                       'A dense vector search is a strong baseline, but as the number of chunks '
                       'grows it may return semantically related passages that are not '
                       'sufficiently precise. Enterprise retrieval frequently adds filters, '
                       'lexical matching, fusion, and reranking.\n'
                       '\n'
                       'The objective is not maximum algorithmic sophistication. It is to preserve '
                       'both **recall**—not missing useful evidence—and **precision**—not wasting '
                       'the final context window on weak evidence.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 24. The two-stage retrieval architecture\n'
                       '\n'
                       'A two-stage retrieval pipeline separates a cheap broad search from an '
                       'expensive precise ranking step.\n'
                       '\n'
                       '```text\n'
                       'large corpus\n'
                       '→ Stage 1: candidate generation (fast, high recall)\n'
                       '→ tens/hundreds of candidates\n'
                       '→ Stage 2: reranking (slower, high precision)\n'
                       '→ few best chunks\n'
                       '→ LLM context\n'
                       '```\n'
                       '\n'
                       'This structure is common because applying an expensive relevance model to '
                       'every chunk would be impractical. Stage 1 narrows the problem; Stage 2 '
                       'spends more computation where it matters.\n'
                       '\n'
                       '{{image:candidate-generation-reranking}}'
                       '\n'
                       '\n'
                       '{{exercise:M01.L03.EX08}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 25. Stage 1: optimize candidate generation for recall\n'
                       '\n'
                       'The first stage often applies metadata filters, vector search, lexical '
                       'search, or hybrid search. Its main job is to avoid false negatives. Some '
                       'irrelevant candidates are acceptable because the second stage can remove '
                       'them.\n'
                       '\n'
                       'The critical limitation is irreversible: if a relevant chunk is absent '
                       'from the candidate set, reranking cannot recover it. Candidate-generation '
                       'tuning should therefore be evaluated with recall-oriented metrics and '
                       'realistic queries.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 26. Stage 2: reranking for precision\n'
                       '\n'
                       'Reranking receives a much smaller candidate set and evaluates each '
                       'candidate more carefully. Transformer cross-encoders can jointly process '
                       'the query and candidate text, capturing relationships that independent '
                       'embeddings may miss.\n'
                       '\n'
                       'Because this stage is computationally heavier, it is applied only after '
                       'candidate generation. Its goal is to order the final evidence so that the '
                       'most answer-bearing, specific, and useful chunks survive the context '
                       'cutoff.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 27. Hybrid search combines semantic and lexical evidence\n'
                       '\n'
                       'Semantic search is strong when wording differs but meaning is similar. '
                       'Lexical search is strong when exact tokens matter, such as product codes, '
                       'statute numbers, error messages, names, or jargon. Hybrid search runs both '
                       'and combines their results.\n'
                       '\n'
                       'A useful mental model is:\n'
                       '\n'
                       '```text\n'
                       'semantic search → meaning match\n'
                       'lexical search  → exact/term match\n'
                       'hybrid search   → evidence from both views\n'
                       '```\n'
                       '\n'
                       'This makes retrieval more robust because the weaknesses of one method can '
                       'be compensated by the other.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Hybrid retrieval fusion | Parallel semantic vector search '
                       'and lexical BM25 search produce ranked lists that are fused before '
                       'reranking | Learner should notice that semantic meaning and exact-term '
                       'evidence are complementary]]\n'
                       '\n'
                       '{{exercise:M01.L03.EX09}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 28. Inverted indexes and BM25\n'
                       '\n'
                       'Lexical search uses an inverted index: each term points to the documents '
                       'or chunks containing it. A ranking function such as BM25 then scores how '
                       'informative the term matches are.\n'
                       '\n'
                       'Lexical retrieval is fast, relatively inexpensive, and explainable because '
                       'you can identify which terms matched. Its weakness is that surface-form '
                       'matching does not inherently understand semantic equivalence. "Car issues" '
                       'and "automobile problems" may express the same idea but share no important '
                       'token.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 29. Reciprocal Rank Fusion (RRF)\n'
                       '\n'
                       'Semantic and lexical systems often produce scores on incompatible scales. '
                       'RRF avoids score calibration by combining **ranks** instead of raw scores. '
                       'A document that appears near the top of either result list receives a '
                       'strong fused contribution.\n'
                       '\n'
                       'The intuition is:\n'
                       '\n'
                       '```text\n'
                       'high semantic rank + moderate lexical rank → strong candidate\n'
                       'moderate semantic rank + high lexical rank → strong candidate\n'
                       'low in both lists                     → weak candidate\n'
                       '```\n'
                       '\n'
                       'RRF is attractive because it is simple and does not require the two '
                       'retrieval systems to agree on score units.\n'
                       '\n'
                       '{{exercise:M01.L03.EX10}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 30. Weighted score fusion\n'
                       '\n'
                       'Another option is to normalize the semantic and lexical scores to '
                       'comparable ranges and compute a weighted combination, such as giving '
                       'semantic evidence more influence than lexical evidence.\n'
                       '\n'
                       'This provides direct control over the balance, but score normalization '
                       'matters. A poorly calibrated normalization can make one search system '
                       'dominate even when the chosen numeric weights suggest otherwise. Weights '
                       'should therefore be validated on representative retrieval data rather than '
                       'chosen by intuition alone.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 31. When hybrid search matters most\n'
                       '\n'
                       'Hybrid retrieval is especially useful when a query mixes concept-level '
                       'intent with exact identifiers. Technical troubleshooting may contain both '
                       'a natural-language symptom and an error code. Legal research may need a '
                       'statute number and conceptually related case reasoning. Medical retrieval '
                       'may combine a drug name with a symptom description. Enterprise search may '
                       'combine internal project codes with general questions.\n'
                       '\n'
                       'The recurring pattern is: **exact tokens carry important identity, while '
                       'surrounding language carries intent.**\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 32. Relevance reranking with cross-encoders\n'
                       '\n'
                       'A relevance reranker evaluates the query together with each candidate. '
                       'This joint processing is more expensive than comparing independently '
                       'produced embeddings, but it can distinguish a passage that merely mentions '
                       'similar words from one that directly answers the user’s request.\n'
                       '\n'
                       'For example, many HR documents may contain the words "performance" and '
                       '"review," yet only one may contain the actual mid-year review procedure. A '
                       'reranker can promote that procedural guide above loosely related policy or '
                       'blog content.\n'
                       '\n'
                       '{{exercise:M01.L03.EX11}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 33. Practical reranking workflow\n'
                       '\n'
                       'The chapter demonstrates a cross-encoder reranker with Sentence '
                       'Transformers. The general workflow is:\n'
                       '\n'
                       '```python\n'
                       'from sentence_transformers.cross_encoder import CrossEncoder\n'
                       '\n'
                       'model = CrossEncoder("BAAI/bge-reranker-v2-m3")\n'
                       'pairs = [[query, doc] for doc in candidates]\n'
                       'scores = model.predict(pairs)\n'
                       'reranked = sorted(zip(candidates, scores), key=lambda x: x[1], '
                       'reverse=True)\n'
                       '```\n'
                       '\n'
                       'The important idea is that the model scores each **query-document pair** '
                       'directly. This is different from embedding retrieval, where query and '
                       'documents are encoded separately and compared afterward.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 34. Maximum Marginal Relevance: relevance plus diversity\n'
                       '\n'
                       'Top-ranked results can be redundant. If five chunks repeat the same fact, '
                       'sending all five wastes context space. Maximum Marginal Relevance (MMR) '
                       'balances two goals: keep chunks relevant to the query, but penalize chunks '
                       'that are too similar to evidence already selected.\n'
                       '\n'
                       'The trade-off parameter controls how much the selection favors pure '
                       'relevance versus diversity. MMR is especially useful when the answer '
                       'benefits from multiple perspectives, such as summarizing customer feedback '
                       'or comparing several sources.\n'
                       '\n'
                       '{{exercise:M01.L03.EX12}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 35. Custom reranking with business rules\n'
                       '\n'
                       'A RAG application may need ranking criteria that are not purely semantic. '
                       'Recent support solutions may deserve priority over old ones. In ecommerce, '
                       'unavailable products may need to be excluded. A regulated application may '
                       'prioritize approved source types.\n'
                       '\n'
                       'Custom reranking can incorporate metadata and business rules after '
                       'semantic relevance has been estimated. This makes retrieval aligned with '
                       'the application’s operational objectives rather than only language '
                       'similarity.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 36. Chaining rerankers\n'
                       '\n'
                       'Reranking stages can be composed. A pipeline might first use a '
                       'cross-encoder for relevance, then MMR for diversity, then a business rule '
                       'for recency or availability.\n'
                       '\n'
                       '```text\n'
                       'candidates\n'
                       '→ relevance reranker\n'
                       '→ diversity reranker\n'
                       '→ custom business reranker\n'
                       '→ final context\n'
                       '```\n'
                       '\n'
                       'Each stage should have a clear purpose. Adding rerankers blindly increases '
                       'latency and complexity. The chain should be justified by measured '
                       'improvement on the application’s evaluation set.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 37. Guardrails are controls around the whole query flow\n'
                       '\n'
                       'Guardrails are mechanisms that constrain inputs, retrieved evidence, '
                       'generation, or outputs so the system behaves within defined safety and '
                       'policy boundaries. They are not one final filter attached after the LLM.\n'
                       '\n'
                       'A layered design can validate user input, filter retrieved chunks, '
                       'strengthen instructions in the prompt, evaluate generated text, and block '
                       'or transform unsafe output. Different risks are best handled at different '
                       'stages.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 38. Bias, harmful content, and source curation\n'
                       '\n'
                       'RAG can reproduce problematic content from its sources. One defense starts '
                       'before retrieval: curate the corpus so that it is appropriate for the '
                       'application and, where relevant, represents the necessary range of '
                       'perspectives.\n'
                       '\n'
                       'Additional classifiers can score retrieved passages for unsafe or biased '
                       'content and influence filtering or reranking. Post-generation auditors can '
                       'also inspect the final answer. The key lesson is that grounding does not '
                       'automatically make an answer safe; it only makes it grounded in whatever '
                       'data you chose to retrieve.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 39. Where guardrails can be placed\n'
                       '\n'
                       'Think of guardrails as checkpoints:\n'
                       '\n'
                       '```text\n'
                       'user input\n'
                       '→ input validation / sanitization\n'
                       '→ retrieval\n'
                       '→ evidence filtering / policy checks\n'
                       '→ generation prompt\n'
                       '→ LLM response\n'
                       '→ output safety / faithfulness checks\n'
                       '→ user\n'
                       '```\n'
                       '\n'
                       'Placing all responsibility on a single prompt is fragile. A stronger '
                       'system uses multiple controls so that one failure does not automatically '
                       'become a user-visible failure.\n'
                       '\n'
                       '{{exercise:M01.L03.EX13}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 40. Dedicated safety models as output auditors\n'
                       '\n'
                       'The chapter illustrates using a specialized safety model to classify '
                       'generated content against a policy. The production pattern is more '
                       'important than the specific model:\n'
                       '\n'
                       '```text\n'
                       'generate candidate answer\n'
                       '→ evaluate candidate against policy\n'
                       '→ allow, block, or replace\n'
                       '```\n'
                       '\n'
                       'A dedicated auditor can be cheaper and more consistent than using the main '
                       'generative model for every policy check. The policy itself should be '
                       'explicit, versioned, and testable.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 41. Direct and indirect prompt injection\n'
                       '\n'
                       'Prompt injection attempts to make the model treat untrusted text as '
                       'instructions that override the application’s intended rules. **Direct '
                       'injection** comes from the user query. **Indirect injection** is planted '
                       'inside external content that later enters the model as retrieved context.\n'
                       '\n'
                       'RAG increases the attack surface because retrieved documents are untrusted '
                       'inputs too. A document can contain text that looks like an instruction '
                       'even though the application intended it to be evidence. The system must '
                       'maintain a clear trust boundary among system instructions, user requests, '
                       'and retrieved data.\n'
                       '\n'
                       '[[IMAGE_NEEDED: RAG trust boundaries | System instructions separated from '
                       'user query and retrieved documents, with sanitization and output checks '
                       'around the LLM | Learner should notice that retrieved context is untrusted '
                       'data and not an instruction source]]\n'
                       '\n'
                       '{{exercise:M01.L03.EX14}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 42. Input and document sanitization\n'
                       '\n'
                       'Sanitization inspects both user inputs and ingested documents for '
                       'suspicious patterns, hidden instructions, malformed content, or known '
                       'attack signatures. The chapter emphasizes that malicious text can even be '
                       'visually hidden in documents.\n'
                       '\n'
                       'Sanitization is not a complete defense because attackers can rephrase '
                       'instructions endlessly. It is one layer that reduces obvious attacks and '
                       'creates signals for stricter downstream handling.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 43. Instruction defense and explicit delimiters\n'
                       '\n'
                       'A prompt should clearly separate trusted instructions from untrusted '
                       'content. XML-like delimiters or other markers can label the query and '
                       'retrieved context, while the system instruction explicitly tells the model '
                       'that text inside those blocks is data rather than higher-priority '
                       'instructions.\n'
                       '\n'
                       '```text\n'
                       'SYSTEM: follow application policy\n'
                       '<query>untrusted user text</query>\n'
                       '<context>untrusted retrieved evidence</context>\n'
                       'TASK: answer using context while obeying system policy\n'
                       '```\n'
                       '\n'
                       'This does not make prompt injection impossible, but it reduces ambiguity '
                       'and should be combined with restricted tool permissions and monitoring.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 44. Why RAG can still hallucinate\n'
                       '\n'
                       'RAG reduces hallucination risk by supplying evidence, but it does not '
                       'guarantee faithfulness. The model can misread the evidence, blend '
                       'conflicting sources, over-extrapolate, or prefer its parametric knowledge '
                       'over the retrieved text.\n'
                       '\n'
                       'The correct debugging question is therefore not simply "Did the LLM '
                       'hallucinate?" but "At which stage did support for this claim break down?"\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 45. Three major causes of RAG hallucination\n'
                       '\n'
                       'The chapter identifies three broad causes. **Retrieval failure:** the '
                       'needed evidence was missed or noisy/conflicting chunks were selected. '
                       '**Data-quality failure:** retrieval found the indexed content correctly, '
                       'but the indexed content was wrong, stale, incomplete, or duplicated. '
                       '**Generation failure:** correct evidence was present, yet the LLM ignored, '
                       'misinterpreted, or contradicted it.\n'
                       '\n'
                       'These causes require different fixes. Improving the prompt will not repair '
                       'stale data, and improving the vector index will not repair an LLM that '
                       'disregards clear context.\n'
                       '\n'
                       '{{exercise:M01.L03.EX15}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 46. Questionable, benign, and unwanted hallucinations\n'
                       '\n'
                       'Not every unsupported statement has the same impact. The chapter '
                       'distinguishes **questionable** cases where support is ambiguous, '
                       '**benign** additions that are unsupported but harmless or reasonable, and '
                       '**unwanted** hallucinations that misrepresent the source or create '
                       'misleading facts.\n'
                       '\n'
                       'This taxonomy is useful because the action threshold can depend on the '
                       'application. A medical or legal system may reject any unsupported '
                       'addition, while a creative summarization interface may tolerate mild '
                       'benign inference if clearly signaled.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 47. Hallucination detection with an LLM judge\n'
                       '\n'
                       'An LLM can be prompted to compare the generated response with the '
                       'retrieved evidence and assign a faithfulness or consistency score. This is '
                       'easy to integrate because the application already handles LLM calls.\n'
                       '\n'
                       'The trade-offs are additional latency, additional cost, possible judge '
                       'hallucination, and score calibration. A coarse 1–5 score may also hide '
                       'uncertainty. LLM-as-a-judge is therefore useful, but it should itself be '
                       'evaluated rather than assumed to be an oracle.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 48. Dedicated hallucination evaluation models\n'
                       '\n'
                       'A dedicated hallucination or entailment model receives source text and a '
                       'generated claim or summary, then predicts how well the output is '
                       'supported. Such models are usually smaller and cheaper than a general LLM '
                       'judge and can return continuous scores.\n'
                       '\n'
                       'The chapter illustrates this pattern with HHEM. The key operational idea '
                       'is to treat faithfulness checking as a classification problem that can be '
                       'inserted after generation and monitored independently.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 49. From detection to hallucination correction\n'
                       '\n'
                       'Detection only tells you that the answer is risky. A production system '
                       'must decide what to do next. Options include refusing to answer, showing a '
                       'warning, retrying retrieval, regenerating with stricter instructions, or '
                       'invoking a dedicated correction model with both the suspect answer and the '
                       'supporting context.\n'
                       '\n'
                       'A correction flow can be represented as:\n'
                       '\n'
                       '```text\n'
                       'query → RAG answer → faithfulness check\n'
                       '                     ├─ pass → return answer\n'
                       '                     └─ fail → correct / regenerate / refuse\n'
                       '```\n'
                       '\n'
                       'Correction improves reliability but adds latency and compute, so '
                       'thresholds should be chosen according to risk.\n'
                       '\n'
                       '{{image:hallucination-correction-flow}}'
                       '\n'
                       '\n'
                       '{{exercise:M01.L03.EX16}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 50. The quality–latency–cost triangle\n'
                       '\n'
                       'Scaling improvements are rarely free. Hybrid retrieval adds work, '
                       'reranking adds work, safety checks add work, hallucination detection adds '
                       'work, and correction may add another model call.\n'
                       '\n'
                       'This creates a recurring engineering trade-off among quality, latency, and '
                       'cost. The goal is not to maximize every control on every request. It is to '
                       'allocate expensive checks where risk or uncertainty justifies them and '
                       'keep the common path efficient.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 51. User experience is part of RAG quality\n'
                       '\n'
                       'A technically accurate backend can still fail as a product if users cannot '
                       'express their goal, understand the answer, verify its sources, or recover '
                       'from errors. The chapter therefore treats the frontend as part of the RAG '
                       'system rather than a cosmetic layer.\n'
                       '\n'
                       'Latency is especially visible to users. As retrieval and guardrail stages '
                       'multiply, streaming, progress indicators, and careful presentation can '
                       'make waiting understandable without hiding the true state of the system.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 52. Designing the input experience\n'
                       '\n'
                       'Users should be able to express requests naturally. Depending on the '
                       'application, this may include text, file uploads, images, or voice. '
                       'Suggested queries and auto-completion can teach users what the system can '
                       'answer without forcing them to learn a query syntax.\n'
                       '\n'
                       'Multiturn interfaces should preserve conversation history visibly and use '
                       'prior turns appropriately. The interface should help refine ambiguous '
                       'requests rather than forcing the retrieval layer to guess silently.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 53. Query refinement and source scope controls\n'
                       '\n'
                       'Some applications benefit from letting users narrow the retrieval '
                       'scope—for example, selecting only a particular repository or source '
                       'family. This gives the user a direct way to express constraints that would '
                       'otherwise need to be inferred from text.\n'
                       '\n'
                       'Source controls are especially valuable in enterprise knowledge systems '
                       'where the same question may have different answers depending on whether '
                       'the user wants information from project documentation, chat history, '
                       'tickets, or policy documents.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 54. Present generated answers and evidence together\n'
                       '\n'
                       'A RAG response contains more than generated prose. It may also contain '
                       'citations, source snippets, confidence or hallucination signals, and '
                       'process metadata. A good UI integrates these elements rather than dumping '
                       'them into unrelated panels.\n'
                       '\n'
                       'The user should be able to distinguish the generated synthesis from the '
                       'evidence supporting it and move from a claim to its source quickly. This '
                       'reduces the cost of verification and increases trust.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Evidence-first RAG response UI | Answer with inline '
                       'citations, expandable source passages, progress state, '
                       'confidence/faithfulness signal, and feedback controls | Learner should '
                       'notice how provenance and user controls are integrated into the answer '
                       'experience]]\n'
                       '\n'
                       '{{exercise:M01.L03.EX17}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 55. Source attribution and lineage\n'
                       '\n'
                       'Citations reveal where the system obtained its evidence. Good source '
                       'attribution can include document title, link, page or section, and the '
                       'specific supporting passage when available.\n'
                       '\n'
                       'Lineage is useful for more than trust. When an answer looks wrong, the '
                       'user or developer can determine whether the problem came from a bad '
                       'source, a bad retrieval choice, or bad generation. Citations therefore '
                       'support both user verification and system debugging.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 56. Explain enough of the process to build confidence\n'
                       '\n'
                       'Small interface cues can communicate that the application is retrieving '
                       'evidence and generating a response. Progress messages can show retrieval, '
                       'reranking, or generation stages without exposing implementation noise.\n'
                       '\n'
                       'The objective is not to reveal internal chain-of-thought. It is to give '
                       'users a useful operational explanation—what the system is doing, whether '
                       'sources were found, and whether additional checks were applied.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 57. User feedback as evaluation data\n'
                       '\n'
                       'Thumbs-up/down controls, comments, or issue-reporting mechanisms can '
                       'capture which answers users found useful or problematic. That feedback '
                       'becomes valuable only if it is stored with enough context to analyze '
                       'later: query, retrieved sources, answer, model/version, and user signal.\n'
                       '\n'
                       'Feedback can then feed evaluation sets, failure analysis, and '
                       'prioritization. The UI is therefore also a data-collection surface for '
                       'continuous RAG improvement.\n'
                       '\n'
                       '{{exercise:M01.L03.EX18}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 58. Graceful failure is a feature\n'
                       '\n'
                       'When retrieval finds insufficient evidence, a good interface should not '
                       'disguise uncertainty with confident prose. It should communicate that the '
                       'information could not be found, suggest how to refine the request, or '
                       'offer alternative source scopes.\n'
                       '\n'
                       'Likewise, if a safety or faithfulness check blocks an answer, the user '
                       'should receive a clear and useful status rather than a generic application '
                       'error. Good error handling preserves trust precisely when the system '
                       'cannot satisfy the request.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 59. Multimodal evidence in the interface\n'
                       '\n'
                       'If retrieval returns images, diagrams, or other non-text evidence, the '
                       'interface should present those artifacts as part of the answer and '
                       'preserve their citation relationship. A link alone may hide important '
                       'context; showing the relevant visual alongside the generated explanation '
                       'can make the evidence easier to understand.\n'
                       '\n'
                       'The same principle applies to tables and structured artifacts: preserve '
                       'the form that best communicates the evidence instead of flattening '
                       'everything into plain text.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 60. Reference UI approaches and prototyping tools\n'
                       '\n'
                       'The chapter points to several implementation styles. Dedicated chat UI '
                       'libraries can provide polished conversational patterns. Streamlit and '
                       'Gradio make it quick to build Python-centered prototypes and internal '
                       'tools. Purpose-built RAG reference interfaces demonstrate integrated '
                       'citations, progress reporting, feedback, and hallucination indicators.\n'
                       '\n'
                       'The tool choice should match the product stage: rapid experimentation may '
                       'prioritize development speed, while a production customer-facing system '
                       'may require deeper control over accessibility, interaction design, '
                       'telemetry, and branding.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 61. Putting the enterprise RAG stack together\n'
                       '\n'
                       'The scalable design can now be viewed as one continuous system:\n'
                       '\n'
                       '```text\n'
                       'SOURCES\n'
                       '→ resilient ingestion\n'
                       '→ quality triage / parsing\n'
                       '→ chunk + metadata\n'
                       '→ embeddings + indexes\n'
                       '→ incremental refresh\n'
                       '→ candidate generation\n'
                       '→ hybrid fusion\n'
                       '→ reranking\n'
                       '→ grounded generation\n'
                       '→ safety + faithfulness checks\n'
                       '→ correction/refusal when needed\n'
                       '→ citations + transparent UX\n'
                       '→ user feedback\n'
                       '→ evaluation and iteration\n'
                       '```\n'
                       '\n'
                       'No component operates in isolation. Better retrieval depends on good '
                       'ingestion. Good generation depends on retrieval. Trust depends on '
                       'guardrails, provenance, and UX. Scaling RAG therefore means engineering '
                       'the interactions among components, not simply upgrading one model.\n'
                       '\n'
                       '{{exercise:M01.L03.EX19}}\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Important misconceptions\n'
                       '\n'
                       '### Misconception 1: Scaling RAG only means buying a larger vector '
                       'database\n'
                       '\n'
                       'Scaling affects ingestion throughput, document quality, update freshness, '
                       'retrieval accuracy, generation cost, safety controls, and frontend '
                       'latency. Database capacity is only one dimension.\n'
                       '\n'
                       '### Misconception 2: A retryable pipeline is automatically safe\n'
                       '\n'
                       'Retries are dangerous unless tasks are idempotent. Repeating a '
                       'non-idempotent indexing task can create duplicate chunks and degrade '
                       'retrieval.\n'
                       '\n'
                       '### Misconception 3: Hybrid search is simply vector search plus more '
                       'results\n'
                       '\n'
                       'Hybrid search combines different retrieval signals—semantic and '
                       'lexical—and then fuses their rankings or normalized scores. It is not '
                       'merely increasing k.\n'
                       '\n'
                       '### Misconception 4: Reranking can recover a chunk missed by candidate '
                       'generation\n'
                       '\n'
                       'It cannot. Stage 2 only sees candidates produced by stage 1, so '
                       'first-stage recall places an upper bound on the entire retrieval '
                       'pipeline.\n'
                       '\n'
                       '### Misconception 5: RAG eliminates hallucinations\n'
                       '\n'
                       'RAG reduces risk by supplying evidence, but hallucinations can still arise '
                       'from bad retrieval, bad source data, or unfaithful generation.\n'
                       '\n'
                       '### Misconception 6: Prompt injection only comes from the user\n'
                       '\n'
                       'Indirect prompt injection can be hidden inside retrieved documents or '
                       'webpages, so ingested content is also an untrusted input.\n'
                       '\n'
                       '### Misconception 7: A good backend guarantees a good RAG product\n'
                       '\n'
                       'Users also need understandable latency, source attribution, error states, '
                       'feedback controls, and interfaces that help them express and refine their '
                       'intent.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Key terminology\n'
                       '\n'
                       '| Term | Meaning |\n'
                       '|---|---|\n'
                       '| QPS | Queries per second; a measure of query load. |\n'
                       '| Incremental update | Reprocessing only data affected by additions, '
                       'edits, or deletions. |\n'
                       '| Index freshness | How closely the searchable index reflects the current '
                       'source state. |\n'
                       '| Idempotency | Property that allows a task to be safely repeated without '
                       'duplicate side effects. |\n'
                       '| Orchestration | Coordinating dependent data-processing tasks, retries, '
                       'schedules, and state. |\n'
                       '| Checkpoint | Persisted progress that allows a pipeline to resume instead '
                       'of restarting. |\n'
                       '| CDC | Change data capture; mechanisms that detect source changes for '
                       'downstream processing. |\n'
                       '| Near-real-time indexing | Making new or changed data searchable with '
                       'very low delay. |\n'
                       '| Candidate generation | Fast first-stage retrieval intended to produce a '
                       'high-recall candidate set. |\n'
                       '| Recall | Fraction of relevant items that were successfully retrieved. |\n'
                       '| Precision | Fraction of retrieved items that are actually relevant. |\n'
                       '| Lexical search | Retrieval based on words or terms rather than dense '
                       'semantic vectors. |\n'
                       '| Inverted index | Mapping from terms to the documents or chunks that '
                       'contain them. |\n'
                       '| BM25 | A widely used lexical relevance-ranking function. |\n'
                       '| Hybrid search | Combining semantic and lexical retrieval signals. |\n'
                       '| RRF | Reciprocal Rank Fusion; combines result lists using rank positions '
                       'rather than raw scores. |\n'
                       '| Cross-encoder | Model that jointly processes a query and candidate to '
                       'score their relevance. |\n'
                       '| Reranking | Reordering candidate results using a more precise or '
                       'business-aware scoring method. |\n'
                       '| MMR | Maximum Marginal Relevance; balances query relevance with '
                       'diversity among selected results. |\n'
                       '| Guardrail | Control that constrains inputs, retrieval, generation, or '
                       'outputs according to safety or policy. |\n'
                       '| Prompt injection | Attack that tries to make untrusted text override '
                       'intended model instructions. |\n'
                       '| Direct injection | Prompt injection delivered through the user input. |\n'
                       '| Indirect injection | Prompt injection planted in external content later '
                       'retrieved by the system. |\n'
                       '| Faithfulness | Degree to which a generated response is supported by the '
                       'provided evidence. |\n'
                       '| LLM-as-a-judge | Using an LLM to evaluate another model output against '
                       'defined criteria. |\n'
                       '| Hallucination correction | A post-detection process that repairs, '
                       'regenerates, warns, or refuses unsupported output. |\n'
                       '| Lineage | Traceable connection from a generated claim back to its source '
                       'evidence. |\n'
                       '| Multilevel cache | Caching at several RAG stages such as embeddings, '
                       'retrieval results, or final answers. |\n'
                       '| Dynamic model routing | Selecting different models according to request '
                       'complexity, cost, or latency needs. |\n'
                       '| Deep observability | Monitoring both explicit failures and silent '
                       'data-quality or completeness failures. |\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Self-check\n'
                       '\n'
                       'Before continuing, make sure you can answer these without looking back:\n'
                       '\n'
                       '1. Explain the central engineering idea behind **RAG at scale changes the '
                       'engineering problem** in your own words.\n'
                       '2. What failure or trade-off would appear if a production RAG system '
                       'ignored **RAG at scale changes the engineering problem**?\n'
                       '3. Explain the central engineering idea behind **Document volume, document '
                       'size, and query load** in your own words.\n'
                       '4. What failure or trade-off would appear if a production RAG system '
                       'ignored **Document volume, document size, and query load**?\n'
                       '5. Explain the central engineering idea behind **Why retrieval becomes '
                       'harder as the corpus grows** in your own words.\n'
                       '6. What failure or trade-off would appear if a production RAG system '
                       'ignored **Why retrieval becomes harder as the corpus grows**?\n'
                       '7. Explain the central engineering idea behind **Index freshness and '
                       'incremental updates** in your own words.\n'
                       '8. What failure or trade-off would appear if a production RAG system '
                       'ignored **Index freshness and incremental updates**?\n'
                       '9. Explain the central engineering idea behind **Understanding RAG cost as '
                       'a system** in your own words.\n'
                       '10. What failure or trade-off would appear if a production RAG system '
                       'ignored **Understanding RAG cost as a system**?\n'
                       '11. Give a concrete production scenario where **Understanding RAG cost as '
                       'a system** would change your system design.\n'
                       '12. Explain the central engineering idea behind **Token economics, '
                       'caching, and model routing** in your own words.\n'
                       '13. What failure or trade-off would appear if a production RAG system '
                       'ignored **Token economics, caching, and model routing**?\n'
                       '14. Explain the central engineering idea behind **Treat ingestion as '
                       'production data infrastructure** in your own words.\n'
                       '15. What failure or trade-off would appear if a production RAG system '
                       'ignored **Treat ingestion as production data infrastructure**?\n'
                       '16. Explain the central engineering idea behind **The large-volume '
                       'ingestion pipeline** in your own words.\n'
                       '17. What failure or trade-off would appear if a production RAG system '
                       'ignored **The large-volume ingestion pipeline**?\n'
                       '18. Explain the central engineering idea behind **Metadata is part of '
                       'retrieval quality** in your own words.\n'
                       '19. What failure or trade-off would appear if a production RAG system '
                       'ignored **Metadata is part of retrieval quality**?\n'
                       '20. Explain the central engineering idea behind **Brittleness: why '
                       'restart-from-zero is unacceptable** in your own words.\n'
                       '21. What failure or trade-off would appear if a production RAG system '
                       'ignored **Brittleness: why restart-from-zero is unacceptable**?\n'
                       '22. Explain the central engineering idea behind **Parallel and distributed '
                       'processing** in your own words.\n'
                       '23. What failure or trade-off would appear if a production RAG system '
                       'ignored **Parallel and distributed processing**?\n'
                       '24. Explain the central engineering idea behind **Pipeline orchestration '
                       'and dependency management** in your own words.\n'
                       '25. What failure or trade-off would appear if a production RAG system '
                       'ignored **Pipeline orchestration and dependency management**?\n'
                       '26. Explain the central engineering idea behind **Idempotency: safe '
                       'retries without duplication** in your own words.\n'
                       '27. What failure or trade-off would appear if a production RAG system '
                       'ignored **Idempotency: safe retries without duplication**?\n'
                       '28. Give a concrete production scenario where **Idempotency: safe retries '
                       'without duplication** would change your system design.\n'
                       '29. Explain the central engineering idea behind **Deep observability for '
                       'ingestion** in your own words.\n'
                       '30. What failure or trade-off would appear if a production RAG system '
                       'ignored **Deep observability for ingestion**?\n'
                       '31. Give a concrete production scenario where **Deep observability for '
                       'ingestion** would change your system design.\n'
                       '32. Explain the central engineering idea behind **Inconsistent data '
                       'quality is a production norm** in your own words.\n'
                       '33. What failure or trade-off would appear if a production RAG system '
                       'ignored **Inconsistent data quality is a production norm**?\n'
                       '34. Give a concrete production scenario where **Inconsistent data quality '
                       'is a production norm** would change your system design.\n'
                       '35. Explain the central engineering idea behind **OCR, boilerplate, and '
                       'encoding failures** in your own words.\n'
                       '36. What failure or trade-off would appear if a production RAG system '
                       'ignored **OCR, boilerplate, and encoding failures**?\n'
                       '37. Explain the central engineering idea behind **Document triage and '
                       'conditional routing** in your own words.\n'
                       '38. What failure or trade-off would appear if a production RAG system '
                       'ignored **Document triage and conditional routing**?\n'
                       '39. Explain the central engineering idea behind **Very large documents '
                       'require streamed processing** in your own words.\n'
                       '40. What failure or trade-off would appear if a production RAG system '
                       'ignored **Very large documents require streamed processing**?\n'
                       '41. Give a concrete production scenario where **Very large documents '
                       'require streamed processing** would change your system design.\n'
                       '42. Explain the central engineering idea behind **Splitting a large PDF '
                       'safely** in your own words.\n'
                       '43. What failure or trade-off would appear if a production RAG system '
                       'ignored **Splitting a large PDF safely**?\n'
                       '44. Explain the central engineering idea behind **Document refresh and '
                       'near-real-time indexing** in your own words.\n'
                       '45. What failure or trade-off would appear if a production RAG system '
                       'ignored **Document refresh and near-real-time indexing**?\n'
                       '46. Explain the central engineering idea behind **Change detection and '
                       'asynchronous indexing** in your own words.\n'
                       '47. What failure or trade-off would appear if a production RAG system '
                       'ignored **Change detection and asynchronous indexing**?\n'
                       '48. Give a concrete production scenario where **Change detection and '
                       'asynchronous indexing** would change your system design.\n'
                       '49. Explain the central engineering idea behind **Designing for fast index '
                       'updates** in your own words.\n'
                       '50. What failure or trade-off would appear if a production RAG system '
                       'ignored **Designing for fast index updates**?\n'
                       '51. Explain the central engineering idea behind **Why basic vector search '
                       'is not enough at scale** in your own words.\n'
                       '52. What failure or trade-off would appear if a production RAG system '
                       'ignored **Why basic vector search is not enough at scale**?\n'
                       '53. Explain the central engineering idea behind **The two-stage retrieval '
                       'architecture** in your own words.\n'
                       '54. What failure or trade-off would appear if a production RAG system '
                       'ignored **The two-stage retrieval architecture**?\n'
                       '55. Give a concrete production scenario where **The two-stage retrieval '
                       'architecture** would change your system design.\n'
                       '56. Explain the central engineering idea behind **Stage 1: optimize '
                       'candidate generation for recall** in your own words.\n'
                       '57. What failure or trade-off would appear if a production RAG system '
                       'ignored **Stage 1: optimize candidate generation for recall**?\n'
                       '58. Explain the central engineering idea behind **Stage 2: reranking for '
                       'precision** in your own words.\n'
                       '59. What failure or trade-off would appear if a production RAG system '
                       'ignored **Stage 2: reranking for precision**?\n'
                       '60. Explain the central engineering idea behind **Hybrid search combines '
                       'semantic and lexical evidence** in your own words.\n'
                       '61. What failure or trade-off would appear if a production RAG system '
                       'ignored **Hybrid search combines semantic and lexical evidence**?\n'
                       '62. Give a concrete production scenario where **Hybrid search combines '
                       'semantic and lexical evidence** would change your system design.\n'
                       '63. Explain the central engineering idea behind **Inverted indexes and '
                       'BM25** in your own words.\n'
                       '64. What failure or trade-off would appear if a production RAG system '
                       'ignored **Inverted indexes and BM25**?\n'
                       '65. Explain the central engineering idea behind **Reciprocal Rank Fusion '
                       '(RRF)** in your own words.\n'
                       '66. What failure or trade-off would appear if a production RAG system '
                       'ignored **Reciprocal Rank Fusion (RRF)**?\n'
                       '67. Give a concrete production scenario where **Reciprocal Rank Fusion '
                       '(RRF)** would change your system design.\n'
                       '68. Explain the central engineering idea behind **Weighted score fusion** '
                       'in your own words.\n'
                       '69. What failure or trade-off would appear if a production RAG system '
                       'ignored **Weighted score fusion**?\n'
                       '70. Give a concrete production scenario where **Weighted score fusion** '
                       'would change your system design.\n'
                       '71. Explain the central engineering idea behind **When hybrid search '
                       'matters most** in your own words.\n'
                       '72. What failure or trade-off would appear if a production RAG system '
                       'ignored **When hybrid search matters most**?\n'
                       '73. Explain the central engineering idea behind **Relevance reranking with '
                       'cross-encoders** in your own words.\n'
                       '74. What failure or trade-off would appear if a production RAG system '
                       'ignored **Relevance reranking with cross-encoders**?\n'
                       '75. Explain the central engineering idea behind **Practical reranking '
                       'workflow** in your own words.\n'
                       '76. What failure or trade-off would appear if a production RAG system '
                       'ignored **Practical reranking workflow**?\n'
                       '77. Explain the central engineering idea behind **Maximum Marginal '
                       'Relevance: relevance plus diversity** in your own words.\n'
                       '78. What failure or trade-off would appear if a production RAG system '
                       'ignored **Maximum Marginal Relevance: relevance plus diversity**?\n'
                       '79. Give a concrete production scenario where **Maximum Marginal '
                       'Relevance: relevance plus diversity** would change your system design.\n'
                       '80. Explain the central engineering idea behind **Custom reranking with '
                       'business rules** in your own words.\n'
                       '81. What failure or trade-off would appear if a production RAG system '
                       'ignored **Custom reranking with business rules**?\n'
                       '82. Explain the central engineering idea behind **Chaining rerankers** in '
                       'your own words.\n'
                       '83. What failure or trade-off would appear if a production RAG system '
                       'ignored **Chaining rerankers**?\n'
                       '84. Explain the central engineering idea behind **Guardrails are controls '
                       'around the whole query flow** in your own words.\n'
                       '85. What failure or trade-off would appear if a production RAG system '
                       'ignored **Guardrails are controls around the whole query flow**?\n'
                       '86. Explain the central engineering idea behind **Bias, harmful content, '
                       'and source curation** in your own words.\n'
                       '87. What failure or trade-off would appear if a production RAG system '
                       'ignored **Bias, harmful content, and source curation**?\n'
                       '88. Explain the central engineering idea behind **Where guardrails can be '
                       'placed** in your own words.\n'
                       '89. What failure or trade-off would appear if a production RAG system '
                       'ignored **Where guardrails can be placed**?\n'
                       '90. Give a concrete production scenario where **Where guardrails can be '
                       'placed** would change your system design.\n'
                       '91. Explain the central engineering idea behind **Dedicated safety models '
                       'as output auditors** in your own words.\n'
                       '92. What failure or trade-off would appear if a production RAG system '
                       'ignored **Dedicated safety models as output auditors**?\n'
                       '93. Explain the central engineering idea behind **Direct and indirect '
                       'prompt injection** in your own words.\n'
                       '94. What failure or trade-off would appear if a production RAG system '
                       'ignored **Direct and indirect prompt injection**?\n'
                       '95. Give a concrete production scenario where **Direct and indirect prompt '
                       'injection** would change your system design.\n'
                       '96. Explain the central engineering idea behind **Input and document '
                       'sanitization** in your own words.\n'
                       '97. What failure or trade-off would appear if a production RAG system '
                       'ignored **Input and document sanitization**?\n'
                       '98. Explain the central engineering idea behind **Instruction defense and '
                       'explicit delimiters** in your own words.\n'
                       '99. What failure or trade-off would appear if a production RAG system '
                       'ignored **Instruction defense and explicit delimiters**?\n'
                       '100. Explain the central engineering idea behind **Why RAG can still '
                       'hallucinate** in your own words.\n'
                       '101. What failure or trade-off would appear if a production RAG system '
                       'ignored **Why RAG can still hallucinate**?\n'
                       '102. Explain the central engineering idea behind **Three major causes of '
                       'RAG hallucination** in your own words.\n'
                       '103. What failure or trade-off would appear if a production RAG system '
                       'ignored **Three major causes of RAG hallucination**?\n'
                       '104. Give a concrete production scenario where **Three major causes of RAG '
                       'hallucination** would change your system design.\n'
                       '105. Explain the central engineering idea behind **Questionable, benign, '
                       'and unwanted hallucinations** in your own words.\n'
                       '106. What failure or trade-off would appear if a production RAG system '
                       'ignored **Questionable, benign, and unwanted hallucinations**?\n'
                       '107. Explain the central engineering idea behind **Hallucination detection '
                       'with an LLM judge** in your own words.\n'
                       '108. What failure or trade-off would appear if a production RAG system '
                       'ignored **Hallucination detection with an LLM judge**?\n'
                       '109. Explain the central engineering idea behind **Dedicated hallucination '
                       'evaluation models** in your own words.\n'
                       '110. What failure or trade-off would appear if a production RAG system '
                       'ignored **Dedicated hallucination evaluation models**?\n'
                       '111. Explain the central engineering idea behind **From detection to '
                       'hallucination correction** in your own words.\n'
                       '112. What failure or trade-off would appear if a production RAG system '
                       'ignored **From detection to hallucination correction**?\n'
                       '113. Give a concrete production scenario where **From detection to '
                       'hallucination correction** would change your system design.\n'
                       '114. Explain the central engineering idea behind **The '
                       'quality–latency–cost triangle** in your own words.\n'
                       '115. What failure or trade-off would appear if a production RAG system '
                       'ignored **The quality–latency–cost triangle**?\n'
                       '116. Explain the central engineering idea behind **User experience is part '
                       'of RAG quality** in your own words.\n'
                       '117. What failure or trade-off would appear if a production RAG system '
                       'ignored **User experience is part of RAG quality**?\n'
                       '118. Explain the central engineering idea behind **Designing the input '
                       'experience** in your own words.\n'
                       '119. What failure or trade-off would appear if a production RAG system '
                       'ignored **Designing the input experience**?\n'
                       '120. Explain the central engineering idea behind **Query refinement and '
                       'source scope controls** in your own words.\n'
                       '121. What failure or trade-off would appear if a production RAG system '
                       'ignored **Query refinement and source scope controls**?\n'
                       '122. Explain the central engineering idea behind **Present generated '
                       'answers and evidence together** in your own words.\n'
                       '123. What failure or trade-off would appear if a production RAG system '
                       'ignored **Present generated answers and evidence together**?\n'
                       '124. Give a concrete production scenario where **Present generated answers '
                       'and evidence together** would change your system design.\n'
                       '125. Explain the central engineering idea behind **Source attribution and '
                       'lineage** in your own words.\n'
                       '126. What failure or trade-off would appear if a production RAG system '
                       'ignored **Source attribution and lineage**?\n'
                       '127. Explain the central engineering idea behind **Explain enough of the '
                       'process to build confidence** in your own words.\n'
                       '128. What failure or trade-off would appear if a production RAG system '
                       'ignored **Explain enough of the process to build confidence**?\n'
                       '129. Explain the central engineering idea behind **User feedback as '
                       'evaluation data** in your own words.\n'
                       '130. What failure or trade-off would appear if a production RAG system '
                       'ignored **User feedback as evaluation data**?\n'
                       '131. Give a concrete production scenario where **User feedback as '
                       'evaluation data** would change your system design.\n'
                       '132. Explain the central engineering idea behind **Graceful failure is a '
                       'feature** in your own words.\n'
                       '133. What failure or trade-off would appear if a production RAG system '
                       'ignored **Graceful failure is a feature**?\n'
                       '134. Explain the central engineering idea behind **Multimodal evidence in '
                       'the interface** in your own words.\n'
                       '135. What failure or trade-off would appear if a production RAG system '
                       'ignored **Multimodal evidence in the interface**?\n'
                       '136. Explain the central engineering idea behind **Reference UI approaches '
                       'and prototyping tools** in your own words.\n'
                       '137. What failure or trade-off would appear if a production RAG system '
                       'ignored **Reference UI approaches and prototyping tools**?\n'
                       '138. Explain the central engineering idea behind **Putting the enterprise '
                       'RAG stack together** in your own words.\n'
                       '139. What failure or trade-off would appear if a production RAG system '
                       'ignored **Putting the enterprise RAG stack together**?\n'
                       '140. Give a concrete production scenario where **Putting the enterprise '
                       'RAG stack together** would change your system design.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Retain this idea\n'
                       '\n'
                       '**Enterprise RAG succeeds when the entire evidence path is engineered as '
                       'one reliable system.** At scale, you must keep data fresh and clean, make '
                       'ingestion restartable, preserve recall before reranking for precision, '
                       'combine semantic and lexical signals when useful, treat retrieved text as '
                       'untrusted input, verify faithfulness after generation, and present '
                       'evidence clearly to users. Every extra component introduces latency and '
                       'cost, so production quality comes from measured trade-offs and end-to-end '
                       'observability—not from adding sophistication blindly.\n',
            'estimated_minutes': 600,
            'has_code_examples': True,
            'has_manual_image_requests': True,
            'sections': [{'id': 'rag-at-scale',
                          'title': 'RAG at scale changes the engineering problem',
                          'order': 1},
                         {'id': 'scale-dimensions',
                          'title': 'Document volume, document size, and query load',
                          'order': 2},
                         {'id': 'retrieval-degradation',
                          'title': 'Why retrieval becomes harder as the corpus grows',
                          'order': 3},
                         {'id': 'index-freshness',
                          'title': 'Index freshness and incremental updates',
                          'order': 4},
                         {'id': 'cost-model',
                          'title': 'Understanding RAG cost as a system',
                          'order': 5},
                         {'id': 'token-economics',
                          'title': 'Token economics, caching, and model routing',
                          'order': 6},
                         {'id': 'ingestion-infrastructure',
                          'title': 'Treat ingestion as production data infrastructure',
                          'order': 7},
                         {'id': 'large-volume-ingestion',
                          'title': 'The large-volume ingestion pipeline',
                          'order': 8},
                         {'id': 'metadata-at-scale',
                          'title': 'Metadata is part of retrieval quality',
                          'order': 9},
                         {'id': 'brittleness',
                          'title': 'Brittleness: why restart-from-zero is unacceptable',
                          'order': 10},
                         {'id': 'parallel-processing',
                          'title': 'Parallel and distributed processing',
                          'order': 11},
                         {'id': 'orchestration',
                          'title': 'Pipeline orchestration and dependency management',
                          'order': 12},
                         {'id': 'idempotency',
                          'title': 'Idempotency: safe retries without duplication',
                          'order': 13},
                         {'id': 'deep-observability',
                          'title': 'Deep observability for ingestion',
                          'order': 14},
                         {'id': 'data-quality',
                          'title': 'Inconsistent data quality is a production norm',
                          'order': 15},
                         {'id': 'ocr-encoding',
                          'title': 'OCR, boilerplate, and encoding failures',
                          'order': 16},
                         {'id': 'triage-routing',
                          'title': 'Document triage and conditional routing',
                          'order': 17},
                         {'id': 'large-documents',
                          'title': 'Very large documents require streamed processing',
                          'order': 18},
                         {'id': 'pdf-splitting',
                          'title': 'Splitting a large PDF safely',
                          'order': 19},
                         {'id': 'document-refresh',
                          'title': 'Document refresh and near-real-time indexing',
                          'order': 20},
                         {'id': 'cdc-async',
                          'title': 'Change detection and asynchronous indexing',
                          'order': 21},
                         {'id': 'instant-indexing',
                          'title': 'Designing for fast index updates',
                          'order': 22},
                         {'id': 'advanced-retrieval',
                          'title': 'Why basic vector search is not enough at scale',
                          'order': 23},
                         {'id': 'two-stage',
                          'title': 'The two-stage retrieval architecture',
                          'order': 24},
                         {'id': 'candidate-generation',
                          'title': 'Stage 1: optimize candidate generation for recall',
                          'order': 25},
                         {'id': 'rerank-stage',
                          'title': 'Stage 2: reranking for precision',
                          'order': 26},
                         {'id': 'hybrid-search',
                          'title': 'Hybrid search combines semantic and lexical evidence',
                          'order': 27},
                         {'id': 'lexical-search',
                          'title': 'Inverted indexes and BM25',
                          'order': 28},
                         {'id': 'rrf', 'title': 'Reciprocal Rank Fusion (RRF)', 'order': 29},
                         {'id': 'weighted-fusion', 'title': 'Weighted score fusion', 'order': 30},
                         {'id': 'hybrid-use-cases',
                          'title': 'When hybrid search matters most',
                          'order': 31},
                         {'id': 'relevance-reranking',
                          'title': 'Relevance reranking with cross-encoders',
                          'order': 32},
                         {'id': 'reranker-code',
                          'title': 'Practical reranking workflow',
                          'order': 33},
                         {'id': 'mmr',
                          'title': 'Maximum Marginal Relevance: relevance plus diversity',
                          'order': 34},
                         {'id': 'custom-reranking',
                          'title': 'Custom reranking with business rules',
                          'order': 35},
                         {'id': 'chained-reranking', 'title': 'Chaining rerankers', 'order': 36},
                         {'id': 'guardrails',
                          'title': 'Guardrails are controls around the whole query flow',
                          'order': 37},
                         {'id': 'bias-safety',
                          'title': 'Bias, harmful content, and source curation',
                          'order': 38},
                         {'id': 'guardrail-placement',
                          'title': 'Where guardrails can be placed',
                          'order': 39},
                         {'id': 'safety-auditor',
                          'title': 'Dedicated safety models as output auditors',
                          'order': 40},
                         {'id': 'prompt-injection',
                          'title': 'Direct and indirect prompt injection',
                          'order': 41},
                         {'id': 'input-sanitization',
                          'title': 'Input and document sanitization',
                          'order': 42},
                         {'id': 'instruction-defense',
                          'title': 'Instruction defense and explicit delimiters',
                          'order': 43},
                         {'id': 'hallucinations-remain',
                          'title': 'Why RAG can still hallucinate',
                          'order': 44},
                         {'id': 'hallucination-causes',
                          'title': 'Three major causes of RAG hallucination',
                          'order': 45},
                         {'id': 'hallucination-impact',
                          'title': 'Questionable, benign, and unwanted hallucinations',
                          'order': 46},
                         {'id': 'judge-detection',
                          'title': 'Hallucination detection with an LLM judge',
                          'order': 47},
                         {'id': 'hhem',
                          'title': 'Dedicated hallucination evaluation models',
                          'order': 48},
                         {'id': 'hallucination-correction',
                          'title': 'From detection to hallucination correction',
                          'order': 49},
                         {'id': 'quality-latency',
                          'title': 'The quality–latency–cost triangle',
                          'order': 50},
                         {'id': 'ux-matters',
                          'title': 'User experience is part of RAG quality',
                          'order': 51},
                         {'id': 'input-ux', 'title': 'Designing the input experience', 'order': 52},
                         {'id': 'query-refinement-ux',
                          'title': 'Query refinement and source scope controls',
                          'order': 53},
                         {'id': 'result-presentation',
                          'title': 'Present generated answers and evidence together',
                          'order': 54},
                         {'id': 'source-attribution',
                          'title': 'Source attribution and lineage',
                          'order': 55},
                         {'id': 'process-explanation',
                          'title': 'Explain enough of the process to build confidence',
                          'order': 56},
                         {'id': 'feedback-control',
                          'title': 'User feedback as evaluation data',
                          'order': 57},
                         {'id': 'error-handling-ux',
                          'title': 'Graceful failure is a feature',
                          'order': 58},
                         {'id': 'multimodal-ui',
                          'title': 'Multimodal evidence in the interface',
                          'order': 59},
                         {'id': 'ui-tools',
                          'title': 'Reference UI approaches and prototyping tools',
                          'order': 60},
                         {'id': 'end-to-end-design',
                          'title': 'Putting the enterprise RAG stack together',
                          'order': 61}]},
 'exercises': [{'id': 'M01.L03.EX01',
                'title': 'Scale diagnosis',
                'lesson_code': 'M01.L03',
                'section_id': 'scale-dimensions',
                'placement': 'after_section',
                'description': 'Diagnose which scaling dimension is causing each symptom in a '
                               'hypothetical RAG deployment.',
                'instructions': '1. Use these symptoms from one RAG deployment: (a) nightly re-indexing no longer finishes before morning; (b) p95 query latency doubles at lunchtime while off-peak latency is fine; (c) answers about policies added last week are missing; (d) the monthly bill grows faster than usage.\n'
                                '2. For each symptom, name the scaling dimension it points to - corpus size, query volume, freshness, or cost.\n'
                                '3. Write the first measurement you would take to confirm each diagnosis.\n'
                                '4. Propose one remedy per symptom and the trade-off it introduces.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['system-diagnosis', 'scaling']},
               {'id': 'M01.L03.EX02',
                'title': 'Design an incremental refresh plan',
                'lesson_code': 'M01.L03',
                'section_id': 'index-freshness',
                'placement': 'after_section',
                'description': 'Design a refresh workflow for new, updated, and deleted documents '
                               'without full reindexing.',
                'instructions': '1. Define how a changed document is detected (for example a content hash or modified timestamp) and the stable document ID you key it by.\n'
                                '2. Describe what happens to the index for a new document, an updated document, and a deleted document.\n'
                                '3. Explain how old chunks of an updated document are removed so stale text cannot be retrieved.\n'
                                '4. State how you would verify after each run that the index matches the source, and when a full rebuild is still justified.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['incremental-indexing', 'freshness']},
               {'id': 'M01.L03.EX03',
                'title': 'Build a RAG cost model',
                'lesson_code': 'M01.L03',
                'section_id': 'cost-model',
                'placement': 'after_section',
                'description': 'Classify costs into corpus-driven, query-driven, and operational '
                               'categories and identify the likely dominant recurring cost.',
                'instructions': '1. List at least eight cost items of a RAG service (for example parsing, embedding the corpus, vector storage, query embedding, reranking, LLM generation, monitoring, on-call).\n'
                                '2. Label each item corpus-driven, query-driven, or operational.\n'
                                "3. Write the variable that drives each item's cost (documents, chunks, queries per day, tokens per answer, hours).\n"
                                '4. Identify the item most likely to dominate the recurring bill at high query volume, and one lever that reduces it.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['cost-modeling', 'architecture']},
               {'id': 'M01.L03.EX04',
                'title': 'Make ingestion restartable',
                'lesson_code': 'M01.L03',
                'section_id': 'idempotency',
                'placement': 'after_section',
                'description': 'Design stable IDs and retry semantics that prevent duplicate '
                               'chunks after task retries.',
                'instructions': '1. Define a deterministic chunk ID built from stable inputs (for example document ID, version and chunk position) instead of a random UUID.\n'
                                '2. Explain why writing chunks as upserts keyed by that ID makes a retried task safe.\n'
                                '3. Describe what happens when a task fails halfway through a document and is retried.\n'
                                '4. Add one check that would detect duplicate chunks if they ever appear.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['reliability', 'idempotency']},
               {'id': 'M01.L03.EX05',
                'title': 'Route dirty documents',
                'lesson_code': 'M01.L03',
                'section_id': 'data-quality',
                'placement': 'after_section',
                'description': 'Given mixed native PDFs, scans, HTML, and corrupted encodings, '
                               'design a triage and cleaning decision tree.',
                'instructions': '1. Write the first check that separates the four inputs: native PDF, scanned PDF, HTML, and text with a corrupted encoding.\n'
                                '2. For each branch, name the extraction or cleaning step (text extraction, OCR, HTML boilerplate removal, encoding repair).\n'
                                '3. Define a quality gate after extraction (for example the share of readable characters) and what happens when a document fails it.\n'
                                '4. Explain why a document should be quarantined rather than indexed when cleaning fails.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['data-quality', 'document-routing']},
               {'id': 'M01.L03.EX06',
                'title': 'Process a giant document safely',
                'lesson_code': 'M01.L03',
                'section_id': 'large-documents',
                'placement': 'after_section',
                'description': 'Design a streamed ingestion plan that bounds memory while '
                               'preserving cross-page structures.',
                'instructions': '1. Describe how you read a 5,000-page document in bounded page windows instead of loading it whole.\n'
                                '2. Explain how a table or section that spans two windows is kept together (for example overlapping windows or carrying an open section forward).\n'
                                '3. State the memory limit you would enforce and what the pipeline does when a single page exceeds it.\n'
                                '4. Explain how progress is checkpointed so a crash resumes from the last finished window.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['stream-processing', 'memory-management']},
               {'id': 'M01.L03.EX07',
                'title': 'Design near-real-time indexing',
                'lesson_code': 'M01.L03',
                'section_id': 'cdc-async',
                'placement': 'after_section',
                'description': 'Separate upload acknowledgement from background indexing and '
                               'define observable state transitions.',
                'instructions': '1. Split the upload request from the indexing work: what the API returns immediately, and what is placed on a queue.\n'
                                '2. Define the document states (for example uploaded, parsing, embedding, indexed, failed) and what moves a document between them.\n'
                                '3. Explain how the user or client sees the current state without waiting on the upload request.\n'
                                '4. Define what happens on failure and how long a document may stay in each state before an alert fires.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['async-processing', 'near-real-time-indexing']},
               {'id': 'M01.L03.EX08',
                'title': 'Choose stage-1 and stage-2 goals',
                'lesson_code': 'M01.L03',
                'section_id': 'two-stage',
                'placement': 'after_section',
                'description': 'Explain why stage 1 should favor recall and stage 2 should favor '
                               'precision, then select evaluation metrics.',
                'instructions': '1. Explain what stage 1 (candidate retrieval) is optimizing and why a missed document there can never be recovered later.\n'
                                '2. Explain what stage 2 (reranking) is optimizing and why it can afford a slower model.\n'
                                '3. Choose one metric for each stage (for example recall@100 for stage 1 and nDCG@5 or precision@5 for stage 2).\n'
                                '4. State how many candidates stage 1 passes on and the trade-off of making that number larger.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['retrieval-design', 'recall-precision']},
               {'id': 'M01.L03.EX09',
                'title': 'Choose semantic, lexical, or hybrid',
                'lesson_code': 'M01.L03',
                'section_id': 'hybrid-search',
                'placement': 'after_section',
                'description': 'Classify example queries by which retrieval mode they need and '
                               'justify the choice.',
                'instructions': "1. Classify these queries as semantic, lexical, or hybrid: (a) 'error code E-4021'; (b) 'how do I calm an angry customer?'; (c) 'refund policy for SKU 88-B'; (d) 'what is our stance on remote work?'; (e) 'invoice INV-2024-117 late fee'.\n"
                                '2. For each, name the part of the query that exact matching handles and the part that meaning-based matching handles.\n'
                                '3. Explain the failure you would expect if only semantic search were used for (a).\n'
                                '4. State when hybrid retrieval is worth its extra complexity.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['hybrid-search', 'retrieval-reasoning']},
               {'id': 'M01.L03.EX10',
                'title': 'Fuse two ranked lists with RRF',
                'lesson_code': 'M01.L03',
                'section_id': 'rrf',
                'placement': 'after_section',
                'description': 'Compute a small rank-fusion example and explain why rank-based '
                               'fusion avoids raw-score incompatibility.',
                'instructions': '1. Lexical ranking: D1, D2, D3, D4. Semantic ranking: D3, D1, D5, D2.\n'
                                '2. Compute the RRF score of every document with k = 60: score = sum of 1 / (60 + rank) over the lists that contain it.\n'
                                '3. Write the fused ranking from highest to lowest score.\n'
                                '4. Explain why fusing ranks avoids comparing a BM25 score with a cosine similarity directly.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rrf', 'ranking']},
               {'id': 'M01.L03.EX11',
                'title': 'Rerank noisy candidates',
                'lesson_code': 'M01.L03',
                'section_id': 'relevance-reranking',
                'placement': 'after_section',
                'description': 'Reorder a candidate set so the direct answer outranks merely '
                               'topic-related chunks.',
                'instructions': "1. Query: 'How many vacation days do new employees get?' Candidates: (A) the history of the vacation policy; (B) 'New employees receive 15 vacation days per year.'; (C) how to request vacation in the HR portal; (D) the company holiday calendar.\n"
                                '2. Rank the four candidates from most to least useful for answering the question.\n'
                                '3. Explain what a cross-encoder reranker sees that the first-stage embedding similarity does not.\n'
                                '4. State which candidates should reach the generator and why passing all four could hurt the answer.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['reranking', 'relevance']},
               {'id': 'M01.L03.EX12',
                'title': 'Balance relevance and diversity',
                'lesson_code': 'M01.L03',
                'section_id': 'mmr',
                'placement': 'after_section',
                'description': 'Choose between pure relevance and diversity-oriented selection for '
                               'two different RAG tasks.',
                'instructions': "1. Task A: answer a precise question such as 'What is the refund window?'. Task B: summarize 'all known risks of the migration'.\n"
                                '2. Choose pure relevance ranking or a diversity-aware method such as MMR for each task.\n'
                                '3. Explain what goes wrong in Task B when the top five chunks repeat the same risk.\n'
                                '4. Explain how the MMR lambda setting shifts the balance between relevance and diversity.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['mmr', 'diversity']},
               {'id': 'M01.L03.EX13',
                'title': 'Design layered guardrails',
                'lesson_code': 'M01.L03',
                'section_id': 'guardrail-placement',
                'placement': 'after_section',
                'description': 'Place validation, retrieval filtering, generation constraints, and '
                               'output auditing in a query pipeline.',
                'instructions': '1. Draw the query pipeline: input, retrieval, generation, output.\n'
                                '2. Place one guardrail at each point: input validation, retrieval filtering, generation constraints, output auditing.\n'
                                '3. For each guardrail, name the specific failure it stops (for example injection text, unauthorized chunks, unsupported claims, sensitive data in the answer).\n'
                                '4. Explain why a single guardrail at the output is not enough.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['guardrails', 'defense-in-depth']},
               {'id': 'M01.L03.EX14',
                'title': 'Threat-model prompt injection',
                'lesson_code': 'M01.L03',
                'section_id': 'prompt-injection',
                'placement': 'after_section',
                'description': 'Identify direct and indirect injection paths in a RAG application '
                               'and propose non-destructive mitigations.',
                'instructions': '1. Identify one direct injection path (text the user types) and two indirect paths (text hidden in indexed documents or tool results).\n'
                                '2. For each path, describe what the injected text tries to make the model do.\n'
                                '3. Propose a mitigation for each that does not delete or alter the source documents (for example marking retrieved text as data, isolating instructions, filtering at retrieval, limiting tool permissions).\n'
                                '4. State how you would test that the mitigations work.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['prompt-injection', 'threat-modeling']},
               {'id': 'M01.L03.EX15',
                'title': 'Trace a hallucination to its layer',
                'lesson_code': 'M01.L03',
                'section_id': 'hallucination-causes',
                'placement': 'after_section',
                'description': 'Given three bad answers, decide whether the root cause is '
                               'retrieval, data quality, or generation.',
                'instructions': "1. Answer 1 cites a 2021 price list although a 2024 list exists in the corpus. Answer 2 says 'no information found' although the right document exists. Answer 3 cites the right chunk but states a number that chunk does not contain.\n"
                                '2. For each answer, decide whether the root cause is data quality, retrieval, or generation.\n'
                                '3. Name the evidence you would inspect to confirm each diagnosis.\n'
                                '4. Propose one fix per answer at the layer where the failure started.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['hallucination-debugging', 'root-cause-analysis']},
               {'id': 'M01.L03.EX16',
                'title': 'Design a correction policy',
                'lesson_code': 'M01.L03',
                'section_id': 'hallucination-correction',
                'placement': 'after_section',
                'description': 'Define when to return, warn, regenerate, correct, or refuse based '
                               'on faithfulness risk.',
                'instructions': '1. Define three faithfulness-risk levels (low, medium, high) and the signal you use to measure them.\n'
                                '2. Assign one action to each level: return, warn, regenerate, correct, or refuse.\n'
                                '3. Explain when correcting an answer is better than refusing it, and when it is not.\n'
                                '4. State what is logged for every warned, corrected, or refused answer.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['faithfulness', 'risk-policy']},
               {'id': 'M01.L03.EX17',
                'title': 'Design an evidence-first answer card',
                'lesson_code': 'M01.L03',
                'section_id': 'result-presentation',
                'placement': 'after_section',
                'description': 'Sketch a response layout that combines answer, citations, '
                               'provenance, and confidence without overwhelming the user.',
                'instructions': '1. Sketch the card: where the answer goes and where citations, source dates, and a confidence signal appear.\n'
                                '2. Decide what is visible immediately and what is one click away (for example full source passages).\n'
                                '3. Show how each claim links to the passage that supports it.\n'
                                '4. Explain how the card looks when evidence is weak or missing.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['rag-ux', 'citations']},
               {'id': 'M01.L03.EX18',
                'title': 'Turn feedback into evaluation data',
                'lesson_code': 'M01.L03',
                'section_id': 'feedback-control',
                'placement': 'after_section',
                'description': 'Define what backend fields should be saved when a user marks a RAG '
                               'answer as unhelpful.',
                'instructions': '1. List the fields to save when a user marks an answer unhelpful: query, rewritten query, retrieved chunk IDs and scores, prompt and model version, answer, user reason, and timestamp.\n'
                                '2. Mark which fields need redaction or access control before storage.\n'
                                '3. Explain how a saved record becomes a test case in the evaluation set.\n'
                                '4. Describe how you would keep one noisy user from distorting the evaluation data.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['feedback-loops', 'evaluation']},
               {'id': 'M01.L03.EX19',
                'title': 'Architect a production RAG path',
                'lesson_code': 'M01.L03',
                'section_id': 'end-to-end-design',
                'placement': 'after_section',
                'description': 'Draw an end-to-end architecture for a high-volume RAG service and '
                               'justify each major stage.',
                'instructions': '1. Draw the path from user request to answer: query processing, retrieval, reranking, generation, guardrails, response.\n'
                                '2. Add the offline side: ingestion, indexing, and evaluation.\n'
                                '3. For each major stage, write one sentence justifying why it exists at high volume.\n'
                                '4. Mark where caching, monitoring, and access control sit in the diagram.',
                'expected_output': 'A concise design, table, calculation, diagram, or written '
                                   'analysis that applies the section concept and justifies the '
                                   'reasoning.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['system-design', 'rag-architecture']}],
 'quiz': {'id': 'M01.L03.QZ01',
          'title': 'Scaling Your RAG Stack — Knowledge Check',
          'lesson_code': 'M01.L03',
          'placement': 'lesson_end',
          'questions': [{'id': 'M01.L03.Q01',
                         'section_id': 'rag-at-scale',
                         'question': 'Which statement best captures what changes when RAG scales?',
                         'options': ['Only vector dimensions increase.',
                                     'The system must coordinate data volume, query load, '
                                     'retrieval quality, operations, safety, and UX.',
                                     'Only the LLM needs to be larger.',
                                     'Chunking is no longer necessary.'],
                         'correct': 1,
                         'explanation': 'Scale introduces interacting engineering pressures across '
                                        'the whole stack.'},
                        {'id': 'M01.L03.Q02',
                         'section_id': 'index-freshness',
                         'question': 'Why are incremental updates important for a large dynamic '
                                     'corpus?',
                         'options': ['They make every query use more tokens.',
                                     'They avoid reprocessing the entire corpus for every change.',
                                     'They remove the need for metadata.',
                                     'They guarantee zero hallucinations.'],
                         'correct': 1,
                         'explanation': 'Incremental pipelines selectively process changed data, '
                                        'reducing refresh cost and delay.'},
                        {'id': 'M01.L03.Q03',
                         'section_id': 'idempotency',
                         'question': 'What does idempotency protect an ingestion pipeline from?',
                         'options': ['Slow token generation',
                                     'Duplicate or inconsistent side effects when tasks are '
                                     'retried',
                                     'Low embedding dimension',
                                     'Long user prompts'],
                         'correct': 1,
                         'explanation': 'An idempotent task can be repeated safely without '
                                        'corrupting state.'},
                        {'id': 'M01.L03.Q04',
                         'section_id': 'data-quality',
                         'question': 'Why should document triage happen before embedding?',
                         'options': ['Embedding fixes OCR errors automatically.',
                                     'Different source qualities require different parsing and '
                                     'cleaning paths.',
                                     'Vector databases cannot store PDFs.',
                                     'It increases the LLM context window.'],
                         'correct': 1,
                         'explanation': 'Dirty input propagates downstream, so it should be '
                                        'detected and routed before indexing.'},
                        {'id': 'M01.L03.Q05',
                         'section_id': 'large-documents',
                         'question': 'What is the main advantage of streamed processing for a huge '
                                     'document?',
                         'options': ['It guarantees perfect parsing.',
                                     'It bounds memory usage and enables incremental progress.',
                                     'It removes the need for chunking.',
                                     'It converts lexical search to semantic search.'],
                         'correct': 1,
                         'explanation': 'Streaming avoids loading the whole file into memory and '
                                        'supports checkpoints.'},
                        {'id': 'M01.L03.Q06',
                         'section_id': 'two-stage',
                         'question': 'Why does two-stage retrieval scale well?',
                         'options': ['It applies the most expensive model to every chunk.',
                                     'It uses a fast broad stage before applying expensive '
                                     'precision ranking to a small set.',
                                     'It removes candidate generation.',
                                     'It guarantees all answers are correct.'],
                         'correct': 1,
                         'explanation': 'The architecture spends heavy computation only on a '
                                        'narrowed candidate set.'},
                        {'id': 'M01.L03.Q07',
                         'section_id': 'candidate-generation',
                         'question': 'What is the key failure that reranking cannot fix?',
                         'options': ['A relevant chunk omitted by stage 1',
                                     'A duplicated citation in the UI',
                                     'A slow output animation',
                                     'A cached query embedding'],
                         'correct': 0,
                         'explanation': 'Rerankers only operate on candidates they receive.'},
                        {'id': 'M01.L03.Q08',
                         'section_id': 'hybrid-search',
                         'question': 'Why combine semantic and lexical retrieval?',
                         'options': ['To make embeddings larger',
                                     'To capture both conceptual similarity and exact-term '
                                     'evidence',
                                     'To avoid all metadata filters',
                                     'To eliminate the LLM'],
                         'correct': 1,
                         'explanation': 'The two retrieval families compensate for different '
                                        'weaknesses.'},
                        {'id': 'M01.L03.Q09',
                         'section_id': 'rrf',
                         'question': 'What problem does RRF avoid?',
                         'options': ['Tokenization',
                                     'Need to normalize incompatible raw scores from different '
                                     'retrieval systems',
                                     'Chunk creation',
                                     'Index persistence'],
                         'correct': 1,
                         'explanation': 'RRF fuses rank positions, so raw score scales do not need '
                                        'to match.'},
                        {'id': 'M01.L03.Q10',
                         'section_id': 'relevance-reranking',
                         'question': 'How does a cross-encoder differ from embedding similarity?',
                         'options': ['It jointly evaluates the query and candidate text.',
                                     'It never uses transformers.',
                                     'It only works on metadata.',
                                     'It stores documents in SQL.'],
                         'correct': 0,
                         'explanation': 'Joint processing enables more nuanced relevance scoring.'},
                        {'id': 'M01.L03.Q11',
                         'section_id': 'mmr',
                         'question': 'What does MMR add beyond pure relevance?',
                         'options': ['Encryption',
                                     'Diversity among selected chunks',
                                     'Larger embeddings',
                                     'OCR correction'],
                         'correct': 1,
                         'explanation': 'MMR penalizes redundancy while retaining query '
                                        'relevance.'},
                        {'id': 'M01.L03.Q12',
                         'section_id': 'guardrail-placement',
                         'question': 'Which is the strongest guardrail design?',
                         'options': ['One sentence in the prompt only',
                                     'A layered set of controls across input, retrieval, '
                                     'generation, and output',
                                     'No retrieval filtering',
                                     'Only frontend validation'],
                         'correct': 1,
                         'explanation': 'Defense in depth reduces dependence on any single '
                                        'control.'},
                        {'id': 'M01.L03.Q13',
                         'section_id': 'prompt-injection',
                         'question': 'What makes indirect prompt injection distinct?',
                         'options': ['It is always sent as the user query.',
                                     'It is planted in external content and activated when that '
                                     'content is retrieved.',
                                     'It only affects vector dimensions.',
                                     'It is a database outage.'],
                         'correct': 1,
                         'explanation': 'Indirect attacks enter through data that the model later '
                                        'reads as context.'},
                        {'id': 'M01.L03.Q14',
                         'section_id': 'hallucination-causes',
                         'question': 'If the indexed policy is outdated and the model faithfully '
                                     'summarizes it, what failed?',
                         'options': ['Only generation',
                                     'Data quality/freshness',
                                     'Only reranking latency',
                                     'The frontend'],
                         'correct': 1,
                         'explanation': 'Faithful generation from bad source data still produces '
                                        'an incorrect user outcome.'},
                        {'id': 'M01.L03.Q15',
                         'section_id': 'judge-detection',
                         'question': 'What is one drawback of LLM-as-a-judge?',
                         'options': ['It requires no model call.',
                                     'It can add latency, cost, and judgment inconsistency.',
                                     'It cannot read text.',
                                     'It only works with images.'],
                         'correct': 1,
                         'explanation': 'The judge itself is a probabilistic model and consumes '
                                        'inference resources.'},
                        {'id': 'M01.L03.Q16',
                         'section_id': 'hallucination-correction',
                         'question': 'What should happen after a faithfulness check fails?',
                         'options': ['Always return the answer unchanged',
                                     'Apply a policy such as warn, regenerate, correct, or refuse',
                                     'Delete the vector database',
                                     'Increase k indefinitely'],
                         'correct': 1,
                         'explanation': 'Detection must connect to an action policy.'},
                        {'id': 'M01.L03.Q17',
                         'section_id': 'result-presentation',
                         'question': 'Why integrate citations with the generated answer?',
                         'options': ['To hide retrieval',
                                     'To help users verify claims and understand provenance',
                                     'To remove metadata',
                                     'To slow the interface'],
                         'correct': 1,
                         'explanation': 'Evidence-first presentation improves verification and '
                                        'trust.'},
                        {'id': 'M01.L03.Q18',
                         'section_id': 'end-to-end-design',
                         'question': 'Which principle best summarizes production RAG scaling?',
                         'options': ['Optimize each component in isolation.',
                                     'Engineer and measure the interactions across ingestion, '
                                     'retrieval, generation, controls, and UX.',
                                     'Always choose the largest model.',
                                     'Always maximize k.'],
                         'correct': 1,
                         'explanation': 'End-to-end interactions determine the final system '
                                        'behavior.'},
                        {'id': 'M01.L03.Q19',
                         'section_id': 'end-to-end-design',
                         'type': 'open',
                         'question': 'Design a production RAG architecture for a corpus with '
                                     'millions of documents and frequent updates. Explain how you '
                                     'would make ingestion restartable, preserve retrieval recall '
                                     'and precision, defend against prompt injection, check '
                                     'faithfulness, and expose trustworthy results in the UI.'}],
          'passing_score': 70}}
