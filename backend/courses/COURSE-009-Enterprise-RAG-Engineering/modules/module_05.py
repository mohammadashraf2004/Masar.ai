"""M01.L05 — The RAG Platform.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 5, pages not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L05"
MODULE_ORDER = 1
MODULE_TITLE = "RAG Foundations"
MODULE_DESCRIPTION = (
    "Evaluate managed RAG platforms and use platform APIs while retaining a clear mental model "
    "of ingestion, retrieval, generation, governance, deployment, quality, and operational trade-offs."
)
SOURCE_CHAPTER = 5
SOURCE_PAGES = "Not provided in supplied source"


TOPIC = {'title': 'The RAG Platform',
 'slug': 'rag-foundations-m01-l05',
 'description': 'A study-ready guide to managed RAG platforms: DIY versus platform trade-offs, '
                'core RAG capabilities, connectors, governance, deployment models, cost, and an '
                'API-level Vectara example.',
 'order': 5,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 9.5,
 'skill_tags': ['rag',
                'rag-platform',
                'rag-as-a-service',
                'turnkey-rag',
                'platform-selection',
                'vector-database',
                'embeddings',
                'hybrid-search',
                'reranking',
                'prompt-governance',
                'data-connectors',
                'rag-governance',
                'shadow-ai',
                'tco',
                'saas',
                'vpc',
                'on-premises',
                'api-security',
                'vectara',
                'hallucination-correction',
                'module-01'],
 'prerequisite_ids': ['M01.L01', 'M01.L02', 'M01.L03', 'M01.L04'],
 'lesson': {'title': 'The RAG Platform',
            'content': '# The RAG Platform\n'
                       '\n'
                       '> **Course:** Retrieval-Augmented Generation (RAG)  \n'
                       '> **Lesson:** M01.L05  \n'
                       '> **Module:** RAG Foundations  \n'
                       '> **Source alignment:** Supplied source, Chapter 5. Page numbers were not '
                       'provided in the supplied source. This lesson is an instructor-authored '
                       'curriculum adaptation rather than a reproduction of the source text.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Learning outcomes\n'
                       '\n'
                       'By the end of this lesson, you should be able to:\n'
                       '\n'
                       '- Explain the ownership boundary between DIY RAG and a managed RAG '
                       'platform.\n'
                       '- Evaluate platform capabilities across ingestion, embeddings, vector '
                       'storage, retrieval, generation, and hallucination controls.\n'
                       '- Reason about embedding-model portability, re-indexing, and vector '
                       'dimensionality trade-offs.\n'
                       '- Assess hybrid search, reranking, prompt governance, and multi-LLM '
                       'support.\n'
                       '- Evaluate enterprise data connectors for refresh, permissions, '
                       'reliability, and observability.\n'
                       '- Explain RAG sprawl, policy drift, shadow AI, and the value of a governed '
                       'golden path.\n'
                       '- Compare DIY and platform total cost of ownership rather than only direct '
                       'API fees.\n'
                       '- Select among SaaS, VPC, and on-premises/air-gapped deployment from '
                       'requirements.\n'
                       '- Explain how a platform API can abstract ingestion and query '
                       'orchestration without removing the underlying RAG stages.\n'
                       '- Design corpora, metadata, API-key scopes, structured ingestion, and '
                       'query configuration.\n'
                       '- Interpret factual-consistency and hallucination-correction features '
                       'correctly.\n'
                       '- Evaluate administrative APIs, operational automation, and portability '
                       'before choosing a long-term platform.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 1. Why a RAG platform exists\n'
                       '\n'
                       'A do-it-yourself RAG stack gives you control over every layer, but that '
                       'control also creates an engineering obligation. You must choose and '
                       'operate the parser, chunker, embedding model, vector database, lexical '
                       'search system, reranker, generative LLM, safety mechanisms, observability, '
                       'and the glue connecting them. A **RAG platform** moves much of that '
                       'machinery behind a managed API.\n'
                       '\n'
                       'The important mental model is not “platform = RAG with fewer features.” A '
                       'platform changes **who owns the operational complexity**. Your application '
                       'still decides what data should ground answers, who can use the '
                       'application, what the user experience should be, and how RAG fits into the '
                       'business workflow. The platform provider takes responsibility for a large '
                       'portion of the underlying RAG infrastructure.\n'
                       '\n'
                       '```text\n'
                       'DIY RAG\n'
                       'application\n'
                       '   ↓\n'
                       'team owns parsing → chunking → embedding → indexes → retrieval → '
                       'generation → guardrails\n'
                       '\n'
                       'RAG platform\n'
                       'application\n'
                       '   ↓\n'
                       'standardized RAG API\n'
                       '   ↓\n'
                       'provider-managed parsing → chunking → embedding → retrieval → generation → '
                       'quality controls\n'
                       '```\n'
                       '\n'
                       'This abstraction is attractive because the expensive part of a mature RAG '
                       'system is often not writing the first query call. It is maintaining '
                       'quality, scaling infrastructure, updating models, handling security fixes, '
                       'supporting many data sources, and keeping the entire pipeline observable '
                       'over time.\n'
                       '\n'
                       '[[IMAGE_NEEDED: DIY RAG versus RAG platform | Show an application '
                       'connected either to many individually managed RAG components or to one '
                       'standardized platform API backed by managed components | Notice that the '
                       'main difference is ownership of infrastructure complexity, not the '
                       'disappearance of the RAG stages]]\n'
                       '\n'
                       '{{exercise:M01.L05.EX01}}\n'
                       '\n'
                       '\n'
                       '## 2. DIY control comes with responsibility\n'
                       '\n'
                       'The strongest argument for DIY RAG is **granular control**. You can select '
                       'a vector database, choose exactly which embedding model to serve, '
                       'implement your own chunking logic, control reranking, and decide precisely '
                       'how generation is performed. This is valuable when your use case requires '
                       'unusual algorithms, proprietary infrastructure, or deep optimization.\n'
                       '\n'
                       'But every customized component becomes something your organization must '
                       'provision, integrate, secure, monitor, scale, patch, and eventually '
                       'replace. Open source does not remove that responsibility. It may remove a '
                       'license fee, but it does not remove engineering effort, infrastructure '
                       'costs, failure handling, or operational ownership.\n'
                       '\n'
                       'A useful way to think about the trade-off is:\n'
                       '\n'
                       '| Dimension | DIY tendency | Platform tendency |\n'
                       '|---|---|---|\n'
                       '| Component control | Maximum | Constrained to platform options |\n'
                       '| Time to first production deployment | Longer | Often shorter |\n'
                       '| Operational burden | Internal team | Shifted toward vendor |\n'
                       '| Ability to customize internals | High | Depends on exposed '
                       'API/configuration |\n'
                       '| Vendor dependence | Distributed across components | Concentrated in '
                       'platform |\n'
                       '| Standardization across teams | Must be built | Often built in |\n'
                       '\n'
                       'Neither side is automatically superior. The correct choice depends on '
                       'which capabilities are strategically differentiating for your organization '
                       'and which are merely infrastructure that must work reliably.\n'
                       '\n'
                       '\n'
                       '## 3. The platform as a central control plane\n'
                       '\n'
                       'A major platform advantage appears when an organization has more than one '
                       'RAG application. Instead of every team creating a separate stack, the '
                       'platform can become a **central control plane** for security, accuracy, '
                       'cost, performance, and common policies.\n'
                       '\n'
                       'The application teams still build different products, but they consume a '
                       'standardized RAG service. Central IT can then define approved models, '
                       'governance rules, access controls, logging, and operational standards once '
                       'rather than reproducing them independently in every project.\n'
                       '\n'
                       'This is especially important because RAG is not only an ML problem. It '
                       'touches identity, sensitive data, auditability, infrastructure, cost '
                       'management, and software release processes. A central platform can make '
                       'those concerns consistent across applications.\n'
                       '\n'
                       'The source presents this as one of the defining properties of platform '
                       'RAG: a standardized RAG API combined with centralized management. The '
                       'value therefore grows with organizational scale, because each new '
                       'application can reuse an existing “golden path” instead of creating '
                       'another isolated stack.\n'
                       '\n'
                       '{{image:rag-platform-governance}}'
                       '\n'
                       '\n'
                       '\n'
                       '## 4. A decision framework: control, speed, operations, and lock-in\n'
                       '\n'
                       'Choosing DIY or platform RAG is a strategic architecture decision rather '
                       'than a feature checklist. Four questions organize the decision well.\n'
                       '\n'
                       '**1. How much control do you truly need?** If your competitive advantage '
                       'depends on custom retrieval algorithms, unusual model serving, or '
                       'proprietary infrastructure, DIY flexibility may matter. If your business '
                       'value is mainly in the application and its data, infrastructure control '
                       'may be less important.\n'
                       '\n'
                       '**2. How quickly must you ship?** A platform can compress the path from '
                       'idea to production because ingestion, search, generation, monitoring, and '
                       'administrative APIs are already present.\n'
                       '\n'
                       '**3. Who will operate the system?** A DIY choice implicitly commits the '
                       'organization to vector infrastructure, model operations, security updates, '
                       'observability, and continual upgrades.\n'
                       '\n'
                       '**4. What happens if you want to leave?** Platform convenience '
                       'concentrates dependency. Data may be portable, but embeddings, metadata '
                       'schemas, query parameters, platform-specific prompts, and administrative '
                       'automation can make migration costly. This is the **platform lock-in** '
                       'risk highlighted in the chapter.\n'
                       '\n'
                       'A good architecture review therefore asks not only “Can this platform meet '
                       'today’s requirements?” but also “Which assumptions would make migration '
                       'difficult later?”\n'
                       '\n'
                       '{{exercise:M01.L05.EX02}}\n'
                       '\n'
                       '\n'
                       '## 5. Evaluate a platform from the RAG pipeline outward\n'
                       '\n'
                       'The first platform-selection criterion is still **RAG quality**. '
                       'Operational convenience is useless if retrieval and generation are poor. A '
                       'platform should therefore be evaluated by walking through the RAG pipeline '
                       'itself:\n'
                       '\n'
                       '```text\n'
                       'data sources\n'
                       '   ↓\n'
                       'ingestion / extraction / chunking\n'
                       '   ↓\n'
                       'embedding + indexing\n'
                       '   ↓\n'
                       'vector / lexical retrieval\n'
                       '   ↓\n'
                       'reranking\n'
                       '   ↓\n'
                       'generation + prompt controls\n'
                       '   ↓\n'
                       'hallucination detection/correction\n'
                       '   ↓\n'
                       'answer + citations / metadata\n'
                       '```\n'
                       '\n'
                       'At each layer, ask what is fixed, what is configurable, what is '
                       'bring-your-own, what is observable, and what can be replaced later. This '
                       'avoids choosing a platform based only on a polished API or a long list of '
                       'integrations.\n'
                       '\n'
                       'The chapter focuses on embedding models, vector databases, advanced '
                       'retrieval, prompt engineering, multiple LLM support, hallucination '
                       'controls, data connectors, governance, deployment, cost, and '
                       'administrative APIs. Together these dimensions reveal whether the platform '
                       'is merely convenient for a demo or suitable as long-term enterprise '
                       'infrastructure.\n'
                       '\n'
                       '\n'
                       '## 6. Default embedding models and multilingual requirements\n'
                       '\n'
                       'Many RAG platforms provide a default embedding model. That simplifies '
                       'onboarding because the developer does not need to deploy an encoder or '
                       'configure an embedding service. But the default should not be treated as '
                       'universally appropriate.\n'
                       '\n'
                       'If your application works across languages, evaluate whether the embedding '
                       'model supports those languages well. The embedding model defines the '
                       'vector representation used for retrieval, so weak multilingual behavior '
                       'can cause relevant chunks to become difficult to find even when the rest '
                       'of the pipeline is well engineered.\n'
                       '\n'
                       'The correct evaluation question is therefore not “Does the platform have '
                       'embeddings?” but “Does its embedding capability match my retrieval domain '
                       'and language requirements?” This must be tested with your own queries and '
                       'corpus rather than assumed from model size alone.\n'
                       '\n'
                       'A platform that hides model operations can still expose meaningful '
                       'choices: default model, alternate supported models, dimensionality '
                       'settings, or bring-your-own embeddings. The breadth of those choices '
                       'determines how much future flexibility you retain.\n'
                       '\n'
                       '\n'
                       '## 7. Bring-your-own embeddings and the re-indexing consequence\n'
                       '\n'
                       'Bring-your-own (BYO) embedding support reduces long-term model risk. If a '
                       'built-in embedder is inadequate for a new language, domain, or quality '
                       'target, you can replace it with a better one.\n'
                       '\n'
                       'However, embedding models are not interchangeable at query time. Your '
                       'stored vectors were produced by one model in one vector space. Switching '
                       'the model normally means **re-encoding the corpus** and rebuilding the '
                       'corresponding vector index. That has three practical consequences:\n'
                       '\n'
                       '1. **Migration time** — large corpora may take substantial time to '
                       're-embed.\n'
                       '2. **Migration cost** — model inference, storage, and index rebuilds '
                       'consume resources.\n'
                       '3. **Release risk** — old and new retrieval behavior should be compared '
                       'before cutover.\n'
                       '\n'
                       'This is why BYO support is valuable but not free. The feature gives you an '
                       'escape route; it does not eliminate the cost of taking that route.\n'
                       '\n'
                       'A mature platform selection should ask how model replacement is performed, '
                       'whether multiple indexes can coexist during migration, and how retrieval '
                       'quality is evaluated before the new embedding representation becomes '
                       'production default. The chapter does not prescribe a specific migration '
                       'mechanism, but it makes the need for re-encoding explicit.\n'
                       '\n'
                       '{{exercise:M01.L05.EX03}}\n'
                       '\n'
                       '\n'
                       '## 8. Embedding dimensions: quality versus compute and storage\n'
                       '\n'
                       'Embedding dimensionality affects both retrieval representation and '
                       'infrastructure. Higher-dimensional vectors can capture more nuanced '
                       'information, but they require more memory, more storage, and more '
                       'arithmetic during similarity search.\n'
                       '\n'
                       'In DIY RAG, those costs appear directly in your infrastructure: larger '
                       'indexes, more memory pressure, longer indexing, and potentially greater '
                       'query latency. In a managed platform, the vendor absorbs the '
                       'implementation complexity, but the resource cost still exists and is '
                       'typically reflected in pricing or service limits.\n'
                       '\n'
                       'An important insight from the chapter is that **larger embeddings do not '
                       'guarantee a proportionally better end-to-end RAG system**. A strong '
                       'second-stage reranker may produce larger quality gains than increasing '
                       'embedding dimension. Therefore, you should evaluate the entire retrieval '
                       'pipeline, not optimize one representation in isolation.\n'
                       '\n'
                       '```text\n'
                       'higher dimension\n'
                       '   ├─ potentially richer semantic representation\n'
                       '   ├─ more storage\n'
                       '   ├─ more memory\n'
                       '   ├─ more similarity-search work\n'
                       '   └─ possibly higher cost / latency\n'
                       '```\n'
                       '\n'
                       'Platform due diligence should include both the supported dimensions and '
                       'the commercial consequences of using them.\n'
                       '\n'
                       '\n'
                       '## 9. What DIY vector-database ownership really includes\n'
                       '\n'
                       'A DIY stack lets you choose a specialized vector database, an open-source '
                       'option, a managed service, or vector search inside an existing database. '
                       'That choice gives you control over index configuration, sharding, '
                       'hardware, failure isolation, and scaling strategy.\n'
                       '\n'
                       'But operating the vector layer means owning much more than the '
                       '`similarity_search()` call. You need to manage:\n'
                       '\n'
                       '- index creation and rebuilds,\n'
                       '- memory and storage planning,\n'
                       '- replication and high availability,\n'
                       '- capacity growth,\n'
                       '- security patches,\n'
                       '- backup and recovery,\n'
                       '- query latency under load,\n'
                       '- metadata and filtering behavior,\n'
                       '- upgrades without unacceptable downtime.\n'
                       '\n'
                       'These responsibilities can create substantial hidden costs even when the '
                       'database software itself is free.\n'
                       '\n'
                       'A platform hides most of these details. The trade-off is that you accept '
                       'the platform provider’s capabilities and limits. If your application '
                       'requires a specific index strategy, special filtering semantics, or '
                       'unusual deployment constraints, verify those explicitly rather than '
                       'assuming that “managed vector search” covers them.\n'
                       '\n'
                       '{{exercise:M01.L05.EX04}}\n'
                       '\n'
                       '\n'
                       '## 10. Managed vector storage: abstraction with constraints\n'
                       '\n'
                       'When the vector database is bundled into a RAG platform, you no longer '
                       'spend engineering time selecting nodes, tuning storage, configuring '
                       'shards, or patching the database. For teams whose goal is to build a RAG '
                       'application rather than database infrastructure, this can remove a large '
                       'operational burden.\n'
                       '\n'
                       'The cost of abstraction is reduced visibility and control. The provider '
                       'determines much of the vector-store architecture, and you interact through '
                       'the capabilities it exposes. Your evaluation should therefore focus on '
                       'behavior that matters to the application: supported corpus size, '
                       'filtering, latency, scaling, metadata, update behavior, and the effect of '
                       'embedding dimensions.\n'
                       '\n'
                       'A useful rule from the chapter is:\n'
                       '\n'
                       '> Choose DIY when deep customization and internal infrastructure expertise '
                       'are important; choose a platform when speed to market and offloading '
                       'operational burden matter more, provided the platform capabilities satisfy '
                       'your requirements.\n'
                       '\n'
                       'That is a trade-off statement, not a universal recommendation.\n'
                       '\n'
                       '\n'
                       '## 11. Advanced retrieval is a quality and safety boundary\n'
                       '\n'
                       'The retrieval pipeline is one of the highest-leverage parts of RAG. Vector '
                       'search provides a strong baseline, but production systems often improve '
                       'quality using hybrid search and reranking.\n'
                       '\n'
                       'A platform should therefore be judged not only on whether it “supports '
                       'search,” but on how much retrieval control it exposes. Can you combine '
                       'semantic and lexical retrieval? Can you configure the blend? Can you '
                       'select a reranker? Can you change the number of candidates? Can you attach '
                       'metadata filters?\n'
                       '\n'
                       'Retrieval also acts as a **safety boundary**. The generator can only '
                       'ground itself in the context you give it. Better retrieval narrows that '
                       'context toward relevant and verified information, reducing the chance that '
                       'the LLM is distracted by unrelated passages or forced to fill gaps.\n'
                       '\n'
                       'A platform whose ingestion API is excellent but whose retrieval pipeline '
                       'is weak may still produce disappointing answers. Conversely, a provider '
                       'that continually improves retrieval can deliver value to every application '
                       'consuming the platform.\n'
                       '\n'
                       '\n'
                       '## 12. Hybrid search and reranking: build them or consume them\n'
                       '\n'
                       'In DIY RAG, vector search becomes easy once embeddings and a vector '
                       'database are available. The more difficult work begins when you add '
                       'lexical indexes, hybrid fusion, and rerankers. Those components introduce '
                       'additional models, services, data structures, tuning parameters, and '
                       'monitoring requirements.\n'
                       '\n'
                       'A RAG platform can package these capabilities as query parameters or '
                       'presets. That can dramatically reduce implementation effort, but it also '
                       'means the platform’s retrieval roadmap becomes strategically important to '
                       'you.\n'
                       '\n'
                       'When evaluating a vendor, ask:\n'
                       '\n'
                       '- Is hybrid search built in or external?\n'
                       '- Can its balance be configured?\n'
                       '- Which rerankers are available?\n'
                       '- Are multilingual rerankers supported if needed?\n'
                       '- Can retrieval settings differ by application or corpus?\n'
                       '- Are search results and scores visible for debugging?\n'
                       '\n'
                       'The chapter emphasizes that this is where many of the largest '
                       'retrieval-relevance gains occur. A platform should not be selected only '
                       'because it abstracts infrastructure; it should also provide a retrieval '
                       'stack that is strong enough for your use cases.\n'
                       '\n'
                       '{{exercise:M01.L05.EX05}}\n'
                       '\n'
                       '\n'
                       '## 13. Prompt engineering is a maintained component, not a one-time '
                       'string\n'
                       '\n'
                       'The final RAG prompt tells the generative model how to use retrieved '
                       'context. It can instruct the model to answer the user, avoid unsupported '
                       'claims, follow a desired style, and treat retrieved text and user input '
                       'safely.\n'
                       '\n'
                       'A common mistake is to view this prompt as a one-time template. The '
                       'chapter points out that different LLMs can respond differently to the same '
                       'instructions. When the underlying model changes—or when a new application '
                       'has different constraints—the prompt may require adaptation and '
                       'retesting.\n'
                       '\n'
                       'Prompt engineering therefore behaves like application logic:\n'
                       '\n'
                       '```text\n'
                       'model version changes\n'
                       '      ↓\n'
                       'prompt behavior may change\n'
                       '      ↓\n'
                       'run evaluation\n'
                       '      ↓\n'
                       'refine instructions if needed\n'
                       '      ↓\n'
                       'release through controlled process\n'
                       '```\n'
                       '\n'
                       'In DIY systems, each team owns this lifecycle. In platform systems, some '
                       'of that expertise can be centralized.\n'
                       '\n'
                       '\n'
                       '## 14. Centralized prompt governance and consistent safety posture\n'
                       '\n'
                       'Prompt governance becomes an organizational problem when many teams build '
                       'RAG applications independently. One application may use strong grounding '
                       'instructions; another may omit them. One may include prompt-injection '
                       'defenses; another may not. Over time, this creates an inconsistent safety '
                       'posture.\n'
                       '\n'
                       'A platform can centralize prompt presets, supported model configurations, '
                       'and common safety behavior. This allows an organization to update a shared '
                       'policy once and apply it broadly, rather than auditing every application’s '
                       'custom prompt manually.\n'
                       '\n'
                       'Centralization does not mean every application must have the same prompt. '
                       'It means there is a controlled mechanism for defining, testing, and '
                       'deploying prompt behavior.\n'
                       '\n'
                       'This is a subtle but important platform benefit: a RAG platform is not '
                       'only infrastructure abstraction; it can also become a **governance layer '
                       'for model interaction**.\n'
                       '\n'
                       '{{exercise:M01.L05.EX06}}\n'
                       '\n'
                       '\n'
                       '## 15. Support for multiple LLMs protects application flexibility\n'
                       '\n'
                       'A DIY stack can call commercial LLM APIs or host open-weight models. This '
                       'gives the engineering team direct control over model choice. A platform '
                       'should offer comparable flexibility if model choice is important to the '
                       'application.\n'
                       '\n'
                       'Why does this matter? LLM performance characteristics can change over '
                       'time, and different models have different quality, cost, latency, '
                       'language, privacy, and hosting properties. A platform that permanently '
                       'ties every application to one generator creates a strategic dependency.\n'
                       '\n'
                       'Support for multiple LLMs lets you adapt as requirements change. A '
                       'lightweight application may use a fast model, while a complex domain '
                       'application may use a more capable model. A sensitive deployment may '
                       'require a self-hosted model. A domain application may eventually use a '
                       'fine-tuned model.\n'
                       '\n'
                       'The platform-selection question is therefore not just “Which model do you '
                       'use?” but “How much control do I retain over model choice now and later?”\n'
                       '\n'
                       '\n'
                       '## 16. Model behavior can change even when your application code does not\n'
                       '\n'
                       'The chapter highlights a less obvious risk: an LLM service may change '
                       'behavior over time. Even if your own application code is unchanged, a '
                       'model update can alter instruction following, tone, safety behavior, or '
                       'answer quality.\n'
                       '\n'
                       'For a DIY system, your team must track these changes, run regression '
                       'evaluation, and decide when to migrate. A platform provider can take on '
                       'part of this burden by testing supported models and updating platform '
                       'defaults or presets.\n'
                       '\n'
                       'This does not eliminate the need for your own evaluation. Your application '
                       'has domain-specific requirements that a vendor cannot fully know. But a '
                       'strong provider can reduce the amount of model surveillance your team '
                       'performs alone.\n'
                       '\n'
                       'Treat model selection as a versioned dependency, not as a permanent '
                       'constant. A platform is valuable when it helps manage that dependency '
                       'without hiding the quality impact from you.\n'
                       '\n'
                       '{{exercise:M01.L05.EX07}}\n'
                       '\n'
                       '\n'
                       '## 17. Bring-your-own LLM for specialized or self-hosted generation\n'
                       '\n'
                       'Some applications benefit from a fine-tuned or self-hosted generative '
                       'model. DIY RAG naturally allows this because you own the generation '
                       'endpoint. With a platform, you should verify whether **bring-your-own '
                       'LLM** is supported if this is part of your roadmap.\n'
                       '\n'
                       'BYO LLM capability is particularly relevant when:\n'
                       '\n'
                       '- a domain-specific fine-tuned model is required,\n'
                       '- data cannot be sent to a public model endpoint,\n'
                       '- an organization already operates an internal inference service,\n'
                       '- cost or latency policy favors a particular model family.\n'
                       '\n'
                       'The decision should be made early because generation integration touches '
                       'prompt formats, streaming, authentication, observability, and potentially '
                       'data-governance requirements.\n'
                       '\n'
                       'The broader lesson is that managed RAG does not have to mean zero model '
                       'flexibility—but the flexibility must be exposed deliberately by the '
                       'platform.\n'
                       '\n'
                       '\n'
                       '## 18. Hallucination detection and correction belong in the platform '
                       'evaluation\n'
                       '\n'
                       'RAG reduces hallucination risk by grounding the LLM in retrieved evidence, '
                       'but the generator can still produce statements that are not supported by '
                       'that evidence. The chapter therefore treats **hallucination detection and '
                       'correction** as first-class platform capabilities.\n'
                       '\n'
                       'Detection answers: *How factually consistent is this generated response '
                       'with the retrieved context?* Correction goes further: *Can unsupported '
                       'spans be revised using the source evidence?*\n'
                       '\n'
                       'A platform may provide these functions directly, whereas a DIY system '
                       'requires you to select models, host or call them, define thresholds, add '
                       'latency and cost controls, and decide what happens when a response is '
                       'flagged.\n'
                       '\n'
                       'When evaluating a platform, ask whether factual-consistency information is '
                       'exposed programmatically, whether it is available per response, and '
                       'whether correction produces an auditable explanation of what changed.\n'
                       '\n'
                       '{{exercise:M01.L05.EX08}}\n'
                       '\n'
                       '\n'
                       '## 19. Data connectors are part of the RAG product, not a peripheral '
                       'feature\n'
                       '\n'
                       'A RAG system is only useful when it can ingest the information users need. '
                       'Enterprise knowledge often lives across email, cloud drives, document '
                       'systems, wikis, issue trackers, CRMs, databases, and web pages. Therefore, '
                       'data connectivity can become as important as model quality.\n'
                       '\n'
                       'A platform may provide managed connectors to many of these sources. In a '
                       'DIY architecture, your team must build connectors, use open-source '
                       'connector projects, or purchase a separate commercial integration layer.\n'
                       '\n'
                       'The important point is that a connector is not simply “Can I read from '
                       'system X?” It must also support the operational lifecycle: authentication, '
                       'incremental refresh, deletions, permission synchronization, partial '
                       'failures, monitoring, and recovery.\n'
                       '\n'
                       'A long connector list can be misleading if the connector does not import '
                       'the specific content you need. An email connector might support one '
                       'provider but not another; a project-management connector might ingest '
                       'tickets but not attachments.\n'
                       '\n'
                       '\n'
                       '## 20. A connector due-diligence checklist\n'
                       '\n'
                       'Evaluate each required connector with concrete questions:\n'
                       '\n'
                       '| Area | Questions |\n'
                       '|---|---|\n'
                       '| Coverage | Which file types, objects, attachments, comments, or nested '
                       'items are imported? |\n'
                       '| Refresh | Can the connector incrementally ingest additions, edits, and '
                       'deletions? |\n'
                       '| Reliability | Are partial failures visible? Can failed items be retried? '
                       '|\n'
                       '| Permissions | Are source-system permissions synchronized into RAG '
                       'retrieval? |\n'
                       '| Deployment | Can it run inside your IT/network constraints? |\n'
                       '| Observability | Are logs, metrics, progress, and skipped items visible? '
                       '|\n'
                       '\n'
                       'This checklist prevents a common failure mode: selecting a connector '
                       'because the source name appears on a marketing page, then discovering '
                       'during implementation that the exact object types or refresh semantics are '
                       'unsupported.\n'
                       '\n'
                       'The platform should make incomplete ingestion visible. If files are '
                       'silently skipped, the RAG system may look healthy while its knowledge base '
                       'is actually missing important data.\n'
                       '\n'
                       '{{exercise:M01.L05.EX09}}\n'
                       '\n'
                       '\n'
                       '## 21. DIY connector options: build, open source, or commercial\n'
                       '\n'
                       'For DIY RAG, the chapter describes three broad ways to connect external '
                       'sources:\n'
                       '\n'
                       '1. **Build and maintain connectors yourself.** Maximum control, maximum '
                       'ownership.\n'
                       '2. **Use open-source connector or orchestration projects.** This reduces '
                       'initial implementation effort but still leaves integration and operation '
                       'to your team.\n'
                       '3. **Use a commercial connector service.** This shifts more maintenance to '
                       'another provider but adds another dependency and cost center.\n'
                       '\n'
                       'The supplied chapter lists ecosystems with large connector catalogs, '
                       'illustrating that data integration is already a substantial software '
                       'category. The precise connector counts change over time, so the strategic '
                       'takeaway is more important than any single number: evaluate coverage and '
                       'behavior for your required sources, not the size of the catalog alone.\n'
                       '\n'
                       'A platform that integrates connectors, indexing, retrieval, and '
                       'permissions into one service can reduce integration boundaries. But it '
                       'should still expose enough monitoring to prove that synchronization is '
                       'correct.\n'
                       '\n'
                       '\n'
                       '## 22. Refresh and permission synchronization are correctness features\n'
                       '\n'
                       'Two connector behaviors directly affect answer correctness and data '
                       'safety: **refresh** and **permissions**.\n'
                       '\n'
                       'Without reliable refresh, the platform may answer from outdated documents '
                       'even though the source system has newer information. Without permission '
                       'synchronization, retrieval may surface content that the user is not '
                       'authorized to see.\n'
                       '\n'
                       'A production connector therefore needs to do more than copy data once:\n'
                       '\n'
                       '```text\n'
                       'source change\n'
                       '   ↓\n'
                       'detect addition / edit / deletion\n'
                       '   ↓\n'
                       'update indexed representation\n'
                       '   ↓\n'
                       'update metadata and access controls\n'
                       '   ↓\n'
                       'verify synchronization / surface failures\n'
                       '```\n'
                       '\n'
                       'This is why connector quality should be evaluated as part of the RAG '
                       'system’s correctness model. A perfect retriever over stale or unauthorized '
                       'data is still a failed system.\n'
                       '\n'
                       '\n'
                       '## 23. RAG sprawl: when every team builds a different stack\n'
                       '\n'
                       'DIY freedom can create **RAG sprawl**: many independently managed RAG '
                       'applications across the same organization, each with different vector '
                       'stores, models, ingestion flows, security controls, and monitoring '
                       'practices.\n'
                       '\n'
                       'At first this may look like healthy experimentation. At enterprise scale '
                       'it becomes operational fragmentation. Central IT must support many '
                       'technology combinations, security teams must audit many independent attack '
                       'surfaces, and data governance policies may be implemented differently in '
                       'each stack.\n'
                       '\n'
                       'The result can be duplicated infrastructure, inconsistent access control, '
                       'uneven patching, incompatible monitoring, and rising support costs.\n'
                       '\n'
                       'RAG sprawl is therefore not simply “too many AI apps.” It is the '
                       'multiplication of **independent RAG infrastructure and policy '
                       'implementations** that central teams must somehow govern.\n'
                       '\n'
                       '[[IMAGE_NEEDED: RAG sprawl versus centralized platform | Left side shows '
                       'departments each running their own vector DB, embedding model, LLM and '
                       'ingestion pipeline; right side shows the same departments sharing a '
                       'governed platform | Notice duplicated infrastructure and inconsistent '
                       'controls on the sprawl side]]\n'
                       '\n'
                       '\n'
                       '## 24. Policy drift and shadow AI\n'
                       '\n'
                       'When separate teams update their own RAG stacks, controls can slowly '
                       'diverge from organizational policy. This is **policy drift**. One '
                       'application may preserve a privacy rule; another may remove it while '
                       'changing its ingestion pipeline. One may use an approved datastore; '
                       'another may introduce a new component without central review.\n'
                       '\n'
                       'The chapter connects this to **shadow AI**, the AI-era counterpart of '
                       'shadow IT. An application built without the knowledge of IT or security '
                       'can expose more than infrastructure risk: it may process sensitive '
                       'enterprise data, call external models, store embeddings in unapproved '
                       'systems, or bypass permission policies.\n'
                       '\n'
                       'Centralized governance reduces this risk by giving teams an approved path '
                       'for building applications. Security controls, redaction, approved models, '
                       'encryption, audit trails, and release processes can be provided once at '
                       'the platform level.\n'
                       '\n'
                       'The key architectural principle is **make the secure path the easy '
                       'path**.\n'
                       '\n'
                       '\n'
                       '## 25. A platform “golden path” for governance\n'
                       '\n'
                       'A platform can provide a preconfigured path that satisfies organizational '
                       'requirements by default. The chapter illustrates this with the idea of '
                       'enforcing approved vector storage and applying PII-handling rules '
                       'consistently across applications.\n'
                       '\n'
                       'A golden path can centralize:\n'
                       '\n'
                       '- approved compute and storage,\n'
                       '- identity and role-based access,\n'
                       '- encryption,\n'
                       '- observability and audit trails,\n'
                       '- release processes,\n'
                       '- model and prompt policies,\n'
                       '- common data-governance transformations.\n'
                       '\n'
                       'This does not prevent specialized applications. It creates a safe baseline '
                       'from which exceptions can be reviewed deliberately.\n'
                       '\n'
                       'From a software-platform perspective, the goal is to turn policy from a '
                       'document teams must remember into **infrastructure behavior teams inherit '
                       'automatically**.\n'
                       '\n'
                       '{{exercise:M01.L05.EX10}}\n'
                       '\n'
                       '\n'
                       '## 26. Centralization can reduce duplicated infrastructure and effort\n'
                       '\n'
                       'RAG sprawl can duplicate the same expensive work. Two teams may embed '
                       'overlapping data with the same model, maintain separate vector stores, '
                       'allocate separate GPU capacity, and each build monitoring and deployment '
                       'pipelines.\n'
                       '\n'
                       'A shared platform can reuse infrastructure and central expertise. One '
                       'embedding service or approved model configuration can support many '
                       'applications; one security patch can protect the shared component; one '
                       'observability layer can cover multiple workloads.\n'
                       '\n'
                       'This is an economies-of-scale argument. It does not mean every workload '
                       'should share every index or every model. Isolation may still be required. '
                       'The benefit is that the underlying operational capabilities are '
                       'implemented once and reused systematically rather than recreated ad hoc.\n'
                       '\n'
                       'Centralization also improves discoverability: IT can see which '
                       'applications exist, what resources they consume, and which policies they '
                       'use.\n'
                       '\n'
                       '\n'
                       '## 27. DIY cost is more than API tokens\n'
                       '\n'
                       'DIY RAG often appears inexpensive during prototyping because the visible '
                       'bill may consist mostly of model API usage. That view ignores much of the '
                       'total cost of ownership.\n'
                       '\n'
                       'The chapter calls attention to costs from:\n'
                       '\n'
                       '- infrastructure setup and configuration,\n'
                       '- vector, lexical, and model-serving resources,\n'
                       '- research and testing of components,\n'
                       '- engineering time for integration,\n'
                       '- continuous maintenance and security patching,\n'
                       '- prompt and retrieval improvements,\n'
                       '- hallucination controls,\n'
                       '- observability and scaling,\n'
                       '- specialist staffing.\n'
                       '\n'
                       'These costs are persistent. A RAG stack is not “finished” after the first '
                       'production deployment; models and algorithms evolve, vulnerabilities '
                       'appear, data volumes grow, and new applications create new requirements.\n'
                       '\n'
                       'When comparing DIY with a platform, compare **total operational '
                       'ownership**, not just the vendor subscription line item.\n'
                       '\n'
                       '{{exercise:M01.L05.EX11}}\n'
                       '\n'
                       '\n'
                       '## 28. Two platform pricing patterns\n'
                       '\n'
                       'The supplied chapter describes two broad platform pricing patterns.\n'
                       '\n'
                       '**Developer-centric consumption model.** These services encourage '
                       'bottom-up adoption with free or relatively low initial subscriptions, then '
                       'charge usage-based overages. This lowers the entry barrier but makes total '
                       'cost more variable as ingestion and query volume grow.\n'
                       '\n'
                       '**All-in-one enterprise model.** These offerings are designed for larger '
                       'organizations and often use annual subscriptions or bundled credit '
                       'systems. The intent is greater TCO predictability by packaging storage, '
                       'compute, API activity, retrieval, and related services into a simpler '
                       'commercial unit.\n'
                       '\n'
                       'Neither pricing model automatically means “cheaper.” The important '
                       'questions are: Which resources are metered? How does cost scale with '
                       'corpus size and query volume? Are model choices priced differently? What '
                       'happens when usage exceeds committed capacity? Which operational tasks are '
                       'included?\n'
                       '\n'
                       'Cost predictability is itself a platform feature.\n'
                       '\n'
                       '\n'
                       '## 29. Upgrades and platform evolution shift ongoing work to the vendor\n'
                       '\n'
                       'A managed platform vendor is responsible for keeping core infrastructure '
                       'current: updating supported models, improving retrieval, patching '
                       'vulnerabilities, and evolving the service. This can reduce the internal '
                       'maintenance burden significantly.\n'
                       '\n'
                       'The trade-off is dependency on the vendor’s roadmap. If a new technique is '
                       'strategically important but the platform does not support it, you may need '
                       'to wait, integrate an external component, or move away from the platform.\n'
                       '\n'
                       'Platform selection should therefore evaluate not only today’s feature list '
                       'but also the provider’s **ability and willingness to evolve the RAG '
                       'stack**. Retrieval innovation, model support, security practices, and '
                       'deployment options all change quickly.\n'
                       '\n'
                       'A platform is a long-term technical partner, not just an API endpoint.\n'
                       '\n'
                       '\n'
                       '## 30. Deployment is a spectrum: SaaS, VPC, and on-premises\n'
                       '\n'
                       'A RAG platform may be delivered in different deployment models, each '
                       'moving the boundary between vendor responsibility and customer control.\n'
                       '\n'
                       '| Model | Primary strength | Primary trade-off |\n'
                       '|---|---|---|\n'
                       '| SaaS | Fastest adoption and least infrastructure ownership | Least '
                       'environmental control; data leaves your environment |\n'
                       '| Customer VPC | Stronger network/data control with managed platform '
                       'software | More cloud and MLOps responsibility |\n'
                       '| On-premises / air-gapped | Maximum data isolation and control | Maximum '
                       'hardware and operational responsibility |\n'
                       '\n'
                       'The decision affects security, compliance, support SLAs, staffing, '
                       'hardware, model availability, and speed of deployment.\n'
                       '\n'
                       'There is no universal best option. The chapter frames SaaS as prioritizing '
                       'convenience, on-premises as prioritizing control and isolation, and VPC as '
                       'a middle ground.\n'
                       '\n'
                       '[[IMAGE_NEEDED: SaaS VPC on-premises responsibility spectrum | Show three '
                       'deployment columns with increasing customer responsibility and increasing '
                       'control from SaaS to VPC to on-premises | Notice that greater control also '
                       'transfers more infrastructure and operations back to the customer]]\n'
                       '\n'
                       '{{exercise:M01.L05.EX12}}\n'
                       '\n'
                       '\n'
                       '## 31. DIY deployment flexibility is limited by component availability\n'
                       '\n'
                       'DIY RAG can theoretically run almost anywhere, but individual component '
                       'choices may constrain that freedom. A managed vector database or external '
                       'model API cannot simply be moved into an air-gapped environment. If your '
                       'policy requires on-premises processing, you may need to replace those '
                       'components with locally deployable alternatives.\n'
                       '\n'
                       'This applies across the stack:\n'
                       '\n'
                       '- generative LLM,\n'
                       '- embedding model,\n'
                       '- reranker,\n'
                       '- OCR and parsing,\n'
                       '- vector database,\n'
                       '- lexical search,\n'
                       '- multimodal processing.\n'
                       '\n'
                       'Therefore, “DIY means unlimited deployment flexibility” is only partly '
                       'true. You control the architecture, but you must choose components that '
                       'can actually operate in the target environment.\n'
                       '\n'
                       '\n'
                       '## 32. SaaS platform: operational simplicity with external trust\n'
                       '\n'
                       'In the SaaS model, the vendor manages the stack and underlying cloud '
                       'infrastructure. This minimizes your operational burden and often provides '
                       'the fastest route to deployment.\n'
                       '\n'
                       'The central question is whether your organization is allowed to send the '
                       'relevant data into the vendor-managed environment. Security controls and '
                       'compliance certifications can make SaaS acceptable for many workloads, but '
                       'an air-gapped requirement immediately rules it out.\n'
                       '\n'
                       'When assessing SaaS, consider:\n'
                       '\n'
                       '- data residency and privacy expectations,\n'
                       '- authentication and authorization,\n'
                       '- encryption,\n'
                       '- supported compliance requirements,\n'
                       '- service availability and SLA,\n'
                       '- data retention behavior,\n'
                       '- vendor access to operational data.\n'
                       '\n'
                       'The chapter’s key point is that security and governance requirements must '
                       'drive the deployment choice rather than convenience alone.\n'
                       '\n'
                       '\n'
                       '## 33. VPC deployment: a middle ground\n'
                       '\n'
                       'A VPC deployment places the platform within an isolated segment of a '
                       'public cloud environment controlled more directly by the customer. This '
                       'can provide stronger network and data controls than SaaS while retaining '
                       'many platform benefits.\n'
                       '\n'
                       'The trade-off is that your team now needs more cloud-architecture and '
                       'MLOps expertise. Networking, identity integration, resource planning, and '
                       'parts of operations may become shared responsibilities.\n'
                       '\n'
                       'VPC deployment is useful when the organization already runs regulated or '
                       'sensitive workloads in a controlled cloud environment and wants tighter '
                       'boundaries than a public multi-tenant SaaS service can provide.\n'
                       '\n'
                       'Think of VPC deployment as moving the platform **closer to your security '
                       'perimeter** without necessarily taking full ownership of every RAG '
                       'component.\n'
                       '\n'
                       '\n'
                       '## 34. On-premises and air-gapped platform deployment\n'
                       '\n'
                       'On-premises deployment offers the highest degree of data isolation because '
                       'the RAG stack runs inside infrastructure controlled by the organization. '
                       'It is attractive for highly sensitive data and environments where internet '
                       'access is restricted or forbidden.\n'
                       '\n'
                       'But control transfers responsibility back to your team. You may need '
                       'enterprise GPUs, enough VRAM for model weights, local inference servers, '
                       'local embedding and reranking, local OCR/parsing, container orchestration, '
                       'logging, monitoring, security patching, and manual model updates.\n'
                       '\n'
                       'An important insight is that air-gapping affects **every cloud '
                       'dependency**, not just the generative LLM. A pipeline that used cloud OCR '
                       'or a hosted embedding endpoint in development must replace those services '
                       'locally.\n'
                       '\n'
                       'On-premises platform software can reduce application-layer integration '
                       'work, but it cannot remove the physical and operational reality of running '
                       'the infrastructure yourself.\n'
                       '\n'
                       '\n'
                       '## 35. Selecting a deployment model from requirements\n'
                       '\n'
                       'The chapter recommends treating deployment as a requirements decision. A '
                       'practical selection sequence is:\n'
                       '\n'
                       '```text\n'
                       'Does data have to remain physically inside the organization?\n'
                       '  ├─ yes → on-premises / air-gapped is likely required\n'
                       '  └─ no\n'
                       '      ↓\n'
                       'Do policy or network controls require customer-managed cloud isolation?\n'
                       '  ├─ yes → consider VPC deployment\n'
                       '  └─ no → SaaS may be suitable\n'
                       '```\n'
                       '\n'
                       'Then validate the result against expertise, budget, performance, support '
                       'expectations, and speed of deployment.\n'
                       '\n'
                       'The important discipline is to identify **hard constraints** first. If '
                       'policy prohibits external processing, no amount of SaaS convenience can '
                       'compensate. If rapid deployment with a small operations team is the '
                       'primary requirement, a fully self-managed stack may be an unnecessarily '
                       'expensive choice.\n'
                       '\n'
                       '\n'
                       '## 36. Cloud “platforms of services” versus end-to-end RAG platforms\n'
                       '\n'
                       'The chapter distinguishes between a complete DIY stack, a collection of '
                       'managed cloud services, and a true end-to-end RAG platform.\n'
                       '\n'
                       'Major cloud providers can simplify DIY by offering managed search, model, '
                       'and knowledge-base services. This reduces infrastructure work, but '
                       'developers may still need to select, configure, and orchestrate multiple '
                       'components.\n'
                       '\n'
                       'A true end-to-end RAG platform goes further by exposing ingestion, '
                       'extraction, chunking, embedding, storage, retrieval, generation, and '
                       'hallucination controls through a unified API.\n'
                       '\n'
                       '```text\n'
                       'DIY                    Managed service toolkit           End-to-end '
                       'platform\n'
                       'many self-run parts →  many managed parts to wire  →     one standardized '
                       'RAG surface\n'
                       '```\n'
                       '\n'
                       'The distinction matters because integration boundaries create operational '
                       'work. Fewer boundaries can reduce failure modes and simplify '
                       'accountability, but they also increase dependence on the platform '
                       'provider.\n'
                       '\n'
                       '\n'
                       '## 37. Vectara as the chapter’s concrete platform example\n'
                       '\n'
                       'The chapter uses Vectara to make platform concepts concrete. The goal is '
                       'not to argue that one vendor is universally correct; it is to show what an '
                       'end-to-end RAG platform API can look like.\n'
                       '\n'
                       'The example demonstrates four major workflows:\n'
                       '\n'
                       '1. create and configure a corpus,\n'
                       '2. ingest files or structured text,\n'
                       '3. execute a query with retrieval and generation settings,\n'
                       '4. inspect or correct hallucinations and perform administrative '
                       'operations.\n'
                       '\n'
                       'As you study the example, focus on what the API **abstracts**. A file '
                       'upload does not merely store bytes. It triggers extraction, chunking, '
                       'embedding, and indexing. A query request does not merely run vector '
                       'similarity. It can configure hybrid search, reranking, generation, and '
                       'factual consistency.\n'
                       '\n'
                       'That is the platform pattern you should learn, even if you later use a '
                       'different provider.\n'
                       '\n'
                       '\n'
                       '## 38. Corpus and document: the platform’s data model\n'
                       '\n'
                       'In the chapter’s Vectara example, a **corpus** is a virtual container '
                       'holding a prepared body of data for retrieval. Separate corpora can '
                       'represent separate applications or knowledge domains—for example internal '
                       'documentation, support information, or reviews.\n'
                       '\n'
                       'A **document** is an individual information unit inside the corpus. '
                       'Documents may come from uploaded files or structured text ingestion.\n'
                       '\n'
                       'This data model gives applications an isolation boundary. Instead of '
                       'putting every enterprise document into one undifferentiated index, you can '
                       'design corpora around ownership, application scope, access, or retrieval '
                       'behavior.\n'
                       '\n'
                       'Corpus design should therefore be intentional. Ask:\n'
                       '\n'
                       '- Which application owns this corpus?\n'
                       '- Which users may query it?\n'
                       '- Which metadata fields will be filtered?\n'
                       '- Which embedding model should represent the content?\n'
                       '- How will documents be refreshed or deleted?\n'
                       '\n'
                       'Those questions turn corpus creation from a console task into '
                       'architecture.\n'
                       '\n'
                       '{{exercise:M01.L05.EX13}}\n'
                       '\n'
                       '\n'
                       '## 39. Corpus configuration: identity, embedding, and filter attributes\n'
                       '\n'
                       'The example corpus configuration includes a human-friendly name, a stable '
                       'corpus key for API requests, an optional description, an embedding model, '
                       'and optional filter attributes.\n'
                       '\n'
                       'Filter attributes deserve special attention. They define metadata you '
                       'expect to use in retrieval constraints, such as document type, department, '
                       'author, date, or another structured property. Thinking about these fields '
                       'before ingestion improves query-time control later.\n'
                       '\n'
                       'Metadata can exist at document level or at a finer-grained document-part '
                       'level, depending on the platform representation. The central design lesson '
                       'is the same as in DIY RAG: **metadata is part of retrieval architecture**, '
                       'not decorative information.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Corpus configuration anatomy | Show corpus name/key, '
                       'embedding model, document content and filter attributes feeding a '
                       'searchable corpus | Notice that metadata and embedding configuration are '
                       'designed before large-scale ingestion]]\n'
                       '\n'
                       '\n'
                       '## 40. API keys and least-privilege access\n'
                       '\n'
                       'The source describes several API-key scopes: a personal key with broad '
                       'access, a query-only key, and a query-plus-index key. This illustrates a '
                       'general security principle: applications should receive only the '
                       'permissions they need.\n'
                       '\n'
                       'A public-facing search application may only require query access. An '
                       'ingestion worker needs write/index permission. An administrative service '
                       'may need broader privileges. Reusing one all-powerful credential '
                       'everywhere makes compromise more damaging.\n'
                       '\n'
                       '```text\n'
                       'frontend / query service       → query-only capability\n'
                       'indexing worker                → index + query if required\n'
                       'administration automation      → broader scoped credential\n'
                       '```\n'
                       '\n'
                       'The specific key types are platform-specific, but the lesson is portable: '
                       '**separate identities by responsibility and follow least privilege**.\n'
                       '\n'
                       '{{exercise:M01.L05.EX14}}\n'
                       '\n'
                       '\n'
                       '## 41. File upload: one API call, many hidden stages\n'
                       '\n'
                       'The file-upload example shows the core platform abstraction. The client '
                       'sends a document to a corpus endpoint along with authentication. The '
                       'response includes a document identifier, extracted metadata, and storage '
                       'information.\n'
                       '\n'
                       'An adapted request shape looks like this:\n'
                       '\n'
                       '```python\n'
                       'import os, requests\n'
                       '\n'
                       'corpus_key = "RAGBOOK"\n'
                       'headers = {"x-api-key": os.getenv("VECTARA_API_KEY")}\n'
                       '\n'
                       'with open("pet_policy.pdf", "rb") as f:\n'
                       '    response = requests.post(\n'
                       '        f"https://api.vectara.io/v2/corpora/{corpus_key}/upload_file",\n'
                       '        headers=headers,\n'
                       '        files={"file": ("pet_policy.pdf", f, "application/pdf")},\n'
                       '    )\n'
                       '\n'
                       'result = response.json()\n'
                       'print(result["id"])\n'
                       '```\n'
                       '\n'
                       'The educational value is not the HTTP syntax. It is what happens behind '
                       'the call: the platform extracts content, chunks it, embeds chunks, stores '
                       'vectors, stores text, and preserves metadata needed later.\n'
                       '\n'
                       '{{exercise:M01.L05.EX15}}\n'
                       '\n'
                       '\n'
                       '## 42. Tracing the hidden ingestion pipeline\n'
                       '\n'
                       'A managed upload can be expanded conceptually into familiar RAG stages:\n'
                       '\n'
                       '```text\n'
                       'uploaded file\n'
                       '   ↓\n'
                       'content extraction\n'
                       '   ↓\n'
                       'chunking\n'
                       '   ↓\n'
                       'embedding\n'
                       '   ↓\n'
                       'vector storage\n'
                       '   +\n'
                       'text / metadata storage\n'
                       '   ↓\n'
                       'queryable corpus\n'
                       '```\n'
                       '\n'
                       'The platform hides implementation details, not the underlying logic. '
                       'Understanding this is critical for debugging. If a query fails to retrieve '
                       'an expected fact, you still need to reason about extraction, chunking, '
                       'embeddings, metadata, and indexing even if you do not operate those '
                       'components directly.\n'
                       '\n'
                       'A platform therefore changes the debugging interface. Instead of '
                       'inspecting your own parser process or database node, you inspect platform '
                       'metadata, API responses, logs, retrieval results, and vendor '
                       'observability.\n'
                       '\n'
                       'Abstraction reduces operational work, but it does not remove the need to '
                       'understand the RAG pipeline.\n'
                       '\n'
                       '\n'
                       '## 43. Configurable ingestion: chunking, tables, images, and metadata\n'
                       '\n'
                       'A strong RAG platform does not force one ingestion path for every '
                       'document. The source example describes optional controls such as selecting '
                       'a chunking strategy, enabling table or image extraction, and attaching '
                       'document metadata.\n'
                       '\n'
                       'This illustrates an important platform design principle: **common advanced '
                       'capabilities should be configuration, not custom infrastructure**.\n'
                       '\n'
                       'For example, the application might specify that a document should use '
                       'fixed-size rather than sentence-oriented chunking, or request table '
                       'extraction because the document contains important structured data. In DIY '
                       'RAG, those choices might require new libraries or pipeline branches. In a '
                       'platform, they can be API parameters.\n'
                       '\n'
                       'This is a major source of developer productivity—but only when the '
                       'provided options match the application’s real needs.\n'
                       '\n'
                       '\n'
                       '## 44. Direct structured ingestion for non-file data\n'
                       '\n'
                       'Not all knowledge arrives as files. Data may come from databases, '
                       'collaboration tools, issue trackers, CRM systems, or APIs. The chapter’s '
                       'direct-ingestion example shows how structured text can be posted to the '
                       'platform as a document object.\n'
                       '\n'
                       'An adapted shape is:\n'
                       '\n'
                       '```python\n'
                       'payload = {\n'
                       '    "id": "selected-works",\n'
                       '    "type": "structured",\n'
                       '    "title": "Selected Works",\n'
                       '    "metadata": {"author": "William Shakespeare"},\n'
                       '    "sections": [\n'
                       '        {\n'
                       '            "title": "King Lear",\n'
                       '            "text": "Synopsis and selected text...",\n'
                       '            "sections": [\n'
                       '                {"title": "Act I", "text": "...", "metadata": {"stage": '
                       '"..."}}\n'
                       '            ],\n'
                       '        }\n'
                       '    ],\n'
                       '}\n'
                       '```\n'
                       '\n'
                       'The important design idea is that the source structure does not have to be '
                       'flattened into one giant string. Hierarchy and metadata can remain '
                       'explicit, giving downstream retrieval more context.\n'
                       '\n'
                       '{{exercise:M01.L05.EX16}}\n'
                       '\n'
                       '\n'
                       '## 45. Nested sections preserve document structure\n'
                       '\n'
                       'The structured-ingestion example allows sections inside sections, and '
                       'metadata at multiple levels. That supports documents whose internal '
                       'organization matters.\n'
                       '\n'
                       'A flat representation might lose the relationship between an act, chapter, '
                       'subsection, and its local text. A hierarchical representation can preserve '
                       'those relationships so the platform can carry context into indexing and '
                       'retrieval.\n'
                       '\n'
                       '```text\n'
                       'document\n'
                       ' ├─ document metadata\n'
                       ' ├─ section A\n'
                       ' │   ├─ text\n'
                       ' │   └─ subsection A.1\n'
                       ' │       ├─ text\n'
                       ' │       └─ local metadata\n'
                       ' └─ section B\n'
                       '```\n'
                       '\n'
                       'This is a reminder that ingestion quality depends on **representation**, '
                       'not merely on getting text into an index. A platform can make structured '
                       'representation easier, but application developers must still decide what '
                       'structure and metadata are meaningful.\n'
                       '\n'
                       '\n'
                       '## 46. The platform query API collapses the RAG query flow\n'
                       '\n'
                       'A DIY query path may require separate calls for query embedding, vector '
                       'retrieval, lexical retrieval, fusion, reranking, prompt construction, LLM '
                       'generation, and hallucination scoring. A platform can collapse much of '
                       'that into one request.\n'
                       '\n'
                       'The source’s Vectara example configures search and generation in a single '
                       'payload. Conceptually:\n'
                       '\n'
                       '```python\n'
                       'payload = {\n'
                       '    "query": "Are pets allowed in the office?",\n'
                       '    "search": {\n'
                       '        "lexical_interpolation": 0.025,\n'
                       '        "limit": 50,\n'
                       '        "context_configuration": {"sentences_before": 2, '
                       '"sentences_after": 2},\n'
                       '        "reranker": {"reranker_name": "Rerank_Multilingual_v1"},\n'
                       '    },\n'
                       '    "generation": {\n'
                       '        "max_used_search_results": 7,\n'
                       '        "response_language": "eng",\n'
                       '        "enable_factual_consistency_score": True,\n'
                       '    },\n'
                       '}\n'
                       '```\n'
                       '\n'
                       'One call still represents multiple RAG operations. The platform simply '
                       'exposes them as a coherent query contract.\n'
                       '\n'
                       '[[IMAGE_NEEDED: One query API expanding into the RAG query pipeline | Show '
                       'a single client request expanding inside the platform into hybrid search, '
                       'context expansion, reranking, generation and factual-consistency scoring | '
                       'Notice that the API hides orchestration while preserving configurable '
                       'controls]]\n'
                       '\n'
                       '\n'
                       '## 47. Reading query parameters as retrieval architecture\n'
                       '\n'
                       'The query example is valuable because each parameter maps to a retrieval '
                       'design choice.\n'
                       '\n'
                       '- **Lexical interpolation** controls the lexical-versus-semantic mixture '
                       'and therefore whether hybrid retrieval contributes to ranking.\n'
                       '- **Limit** controls the number of initial search results considered.\n'
                       '- **Context configuration** expands a matched passage with nearby '
                       'sentences to recover local context.\n'
                       '- **Reranker selection** chooses a second-stage ranking model.\n'
                       '\n'
                       'These are not merely API fields. They correspond to concepts from the '
                       'previous chapters. A learner who understands the RAG stack can look at the '
                       'payload and reconstruct the retrieval architecture.\n'
                       '\n'
                       'This is exactly what a good platform should enable: abstract '
                       'infrastructure details while still exposing meaningful quality controls.\n'
                       '\n'
                       '{{exercise:M01.L05.EX17}}\n'
                       '\n'
                       '\n'
                       '## 48. Generation controls: how much context, which prompt, and factual '
                       'consistency\n'
                       '\n'
                       'The generation part of the query controls how retrieval output becomes an '
                       'answer. The source example includes:\n'
                       '\n'
                       '- how many retrieved results are used by the generator,\n'
                       '- the response language,\n'
                       '- a named prompt or generation preset,\n'
                       '- factual-consistency scoring.\n'
                       '\n'
                       'The parameter controlling maximum used search results is especially '
                       'important. Retrieval may produce dozens of candidates, but sending every '
                       'one to the LLM can increase noise, token cost, and latency. The platform '
                       'lets the application separate **candidate retrieval depth** from '
                       '**generation context depth**.\n'
                       '\n'
                       'A named generation preset also illustrates centralized prompt/model '
                       'governance: instead of embedding a long prompt string in every '
                       'application, the platform can refer to a managed configuration.\n'
                       '\n'
                       'Factual-consistency scoring turns hallucination detection into a '
                       'query-level output that the application can inspect and act upon.\n'
                       '\n'
                       '\n'
                       '## 49. Streaming changes perceived latency, not retrieval quality\n'
                       '\n'
                       'The source notes a streaming-response option. With streaming enabled, the '
                       'user interface can display generated text incrementally rather than '
                       'waiting for the full response.\n'
                       '\n'
                       'This is primarily a **user-experience latency** improvement. It does not '
                       'make retrieval more accurate and does not necessarily reduce total '
                       'generation time. It reduces the delay before the user begins seeing useful '
                       'output.\n'
                       '\n'
                       '```text\n'
                       'non-streaming: query ───────────────> complete answer appears\n'
                       'streaming:     query ───> first tokens → more tokens → complete answer\n'
                       '```\n'
                       '\n'
                       'A platform that supports streaming simplifies frontend integration because '
                       'the application does not need to design a custom streaming layer around '
                       'the underlying model provider.\n'
                       '\n'
                       '\n'
                       '## 50. Use factual-consistency scores as signals, not magic truth\n'
                       '\n'
                       'The example query returns both a generated summary and a '
                       'factual-consistency score. This turns hallucination detection into a '
                       'machine-readable signal that downstream application logic can use.\n'
                       '\n'
                       'Possible application behavior includes flagging low-confidence answers, '
                       'sending them for additional checking, or presenting a warning. The exact '
                       'threshold and action must be validated for the application rather than '
                       'copied blindly.\n'
                       '\n'
                       'A factual-consistency score does not replace retrieval evaluation or human '
                       'judgment. If the retrieved context itself is wrong or incomplete, a '
                       'perfectly faithful answer can still be wrong for the user. The score '
                       'measures consistency with the supplied evidence, not universal truth.\n'
                       '\n'
                       'That distinction should remain clear when using platform-provided quality '
                       'metrics.\n'
                       '\n'
                       '\n'
                       '## 51. Hallucination correction as a separate platform operation\n'
                       '\n'
                       'The chapter goes beyond detection by showing a hallucination-correction '
                       'endpoint. The application provides the generated text and the source '
                       'documents or retrieved chunks. The corrector returns revised text grounded '
                       'in those sources.\n'
                       '\n'
                       'An adapted request shape is:\n'
                       '\n'
                       '```python\n'
                       'payload = {\n'
                       '    "generated_text": candidate_answer,\n'
                       '    "documents": [{"text": r["text"]} for r in search_results],\n'
                       '    "model": "vhc-large-1.0",\n'
                       '}\n'
                       '```\n'
                       '\n'
                       'The important pattern is **evidence-aware post-processing**:\n'
                       '\n'
                       '```text\n'
                       'retrieved evidence + generated answer\n'
                       '              ↓\n'
                       '      hallucination corrector\n'
                       '              ↓\n'
                       '       corrected answer\n'
                       '```\n'
                       '\n'
                       'This can be especially useful when the generator produced an answer that '
                       'is mostly good but contains a few unsupported details.\n'
                       '\n'
                       '{{exercise:M01.L05.EX18}}\n'
                       '\n'
                       '\n'
                       '## 52. Corrections should be auditable\n'
                       '\n'
                       'The source example returns more than a corrected paragraph. It also '
                       'returns specific corrections containing the original span, corrected span, '
                       'and an explanation of why the change was made.\n'
                       '\n'
                       'That structure is operationally valuable. It allows developers to answer:\n'
                       '\n'
                       '- What exactly changed?\n'
                       '- Which claim was unsupported?\n'
                       '- Which source evidence justified the correction?\n'
                       '- Is the correction mechanism behaving sensibly?\n'
                       '\n'
                       'A correction system that silently rewrites text is harder to trust and '
                       'debug. Structured explanations make it possible to log corrections, '
                       'inspect recurring failure patterns, and decide whether the real problem '
                       'belongs in generation, retrieval, or source data.\n'
                       '\n'
                       'This is another example of a broader principle: **platform abstraction '
                       'should not eliminate observability**.\n'
                       '\n'
                       '\n'
                       '## 53. Administrative APIs turn a platform into manageable infrastructure\n'
                       '\n'
                       'Production platforms need more than ingest and query endpoints. The '
                       'chapter highlights administrative APIs for corpora, documents, API keys, '
                       'users, and query history.\n'
                       '\n'
                       'These APIs matter because enterprise RAG must be automated. Central IT may '
                       'need to create or retire corpora, delete documents, rotate credentials, '
                       'provision users, inspect activity, and integrate RAG operations into '
                       'existing workflows.\n'
                       '\n'
                       'An adapted document-list request might be as simple as:\n'
                       '\n'
                       '```python\n'
                       'response = requests.get(\n'
                       '    f"https://api.vectara.io/v2/corpora/{corpus_key}/documents",\n'
                       '    headers={"x-api-key": api_key},\n'
                       ')\n'
                       'documents = response.json()["documents"]\n'
                       '```\n'
                       '\n'
                       'The specific endpoint is less important than the requirement: **every '
                       'important console operation should ideally be automatable** if the '
                       'platform is going to serve many applications.\n'
                       '\n'
                       '\n'
                       '## 54. Why central IT needs automation and query visibility\n'
                       '\n'
                       'Administrative automation allows a platform to fit into enterprise '
                       'lifecycle management. Employees join and leave. Data must be deleted. '
                       'Credentials expire. Applications are created and retired. Security teams '
                       'need audit information. Operations teams need usage history.\n'
                       '\n'
                       'A platform that can only be managed manually through a web console becomes '
                       'difficult to govern at scale. APIs let you integrate RAG with existing '
                       'identity, provisioning, compliance, and monitoring processes.\n'
                       '\n'
                       'Query history is particularly useful for understanding activity across '
                       'applications. It can support troubleshooting, quality analysis, cost '
                       'attribution, and governance—subject to the organization’s own privacy '
                       'policies.\n'
                       '\n'
                       'Platform selection should therefore include an **operations API** review, '
                       'not only an inference API review.\n'
                       '\n'
                       '\n'
                       '## 55. Build a platform-selection scorecard\n'
                       '\n'
                       'A structured scorecard helps prevent vendor selection from being dominated '
                       'by one attractive feature. Evaluate the platform across the full '
                       'lifecycle.\n'
                       '\n'
                       '| Category | Questions to answer |\n'
                       '|---|---|\n'
                       '| Ingestion | Formats, tables/images, chunking, refresh, connectors, '
                       'failures? |\n'
                       '| Embeddings | Default quality, multilingual, BYO, dimensions, migration? '
                       '|\n'
                       '| Retrieval | Hybrid search, filters, rerankers, result visibility? |\n'
                       '| Generation | Multiple LLMs, BYO LLM, prompts, streaming? |\n'
                       '| Quality | Hallucination detection, correction, citations/evidence? |\n'
                       '| Governance | RBAC, permission sync, auditability, centralized policies? '
                       '|\n'
                       '| Deployment | SaaS, VPC, on-premises/air-gapped? |\n'
                       '| Operations | Monitoring, admin APIs, query history, support SLA? |\n'
                       '| Economics | Pricing unit, scale behavior, overages, migration cost? |\n'
                       '| Portability | Data export, metadata portability, model/index migration '
                       'path? |\n'
                       '\n'
                       'The best platform is the one that satisfies your actual constraints and '
                       'reduces nondifferentiating engineering work without blocking capabilities '
                       'that are strategically important.\n'
                       '\n'
                       '\n'
                       '## 56. Design for platform portability before you need it\n'
                       '\n'
                       'The chapter warns that platform convenience can create lock-in and '
                       'migration costs. You can reduce—not eliminate—that risk by keeping '
                       'application boundaries clear.\n'
                       '\n'
                       'Useful design habits include keeping your own canonical source data, '
                       'maintaining stable document IDs and metadata definitions, separating '
                       'business logic from vendor-specific request construction, and documenting '
                       'which platform features are essential versus replaceable.\n'
                       '\n'
                       'Think in terms of an adapter boundary:\n'
                       '\n'
                       '```text\n'
                       'business application\n'
                       '      ↓\n'
                       'internal RAG service interface\n'
                       '      ↓\n'
                       'platform-specific adapter\n'
                       '      ↓\n'
                       'RAG platform API\n'
                       '```\n'
                       '\n'
                       'The chapter does not prescribe this exact software pattern, but it follows '
                       'directly from the migration-risk problem it identifies: avoid scattering '
                       'vendor-specific assumptions throughout the application.\n'
                       '\n'
                       'Portability planning is easier before the platform becomes deeply embedded '
                       'in every workflow.\n'
                       '\n'
                       '\n'
                       '## 57. Important misconceptions\n'
                       '\n'
                       '### Misconception 1: “A RAG platform means I no longer need to understand '
                       'RAG.”\n'
                       'Wrong. The platform hides operations, but retrieval quality still depends '
                       'on chunking, metadata, embeddings, filters, reranking, and context '
                       'selection. You need the conceptual model to configure and debug it.\n'
                       '\n'
                       '### Misconception 2: “Managed means no operational responsibility.”\n'
                       'Wrong. You still own application requirements, data quality, access '
                       'policy, evaluation, integration, user experience, and vendor governance.\n'
                       '\n'
                       '### Misconception 3: “The platform with the most connectors is '
                       'automatically best.”\n'
                       'Wrong. Connector depth, refresh behavior, permission synchronization, and '
                       'failure visibility matter more than a raw count.\n'
                       '\n'
                       '### Misconception 4: “BYO embeddings make model switching easy.”\n'
                       'Incomplete. BYO support enables the switch, but the corpus normally must '
                       'be re-embedded and re-indexed.\n'
                       '\n'
                       '### Misconception 5: “A factual-consistency score proves the answer is '
                       'true.”\n'
                       'Wrong. It indicates support from the retrieved context. If the context is '
                       'stale or incorrect, the answer can be faithful yet still wrong for the '
                       'user.\n'
                       '\n'
                       '### Misconception 6: “SaaS is less secure and on-premises is automatically '
                       'secure.”\n'
                       'Too simplistic. Deployment changes the security boundary and '
                       'responsibility. On-premises increases control but also increases the '
                       'customer’s responsibility to configure and operate security correctly.\n'
                       '\n'
                       '\n'
                       '## 58. Key terminology\n'
                       '\n'
                       '| Term | Meaning in this lesson |\n'
                       '|---|---|\n'
                       '| RAG platform | Managed service that packages much of the RAG pipeline '
                       'behind developer APIs |\n'
                       '| RAG-as-a-service | Another name for a managed RAG platform |\n'
                       '| Turnkey RAG | End-to-end managed RAG intended to reduce integration and '
                       'operations work |\n'
                       '| DIY RAG | RAG architecture assembled and operated from individually '
                       'selected components |\n'
                       '| Control plane | Central layer used to manage policy, security, '
                       'performance, cost, and shared platform settings |\n'
                       '| BYO embedding | Ability to use an embedding model selected by the '
                       'customer |\n'
                       '| BYO LLM | Ability to use a customer-selected or customer-hosted '
                       'generative model |\n'
                       '| Re-indexing | Rebuilding searchable representations, commonly required '
                       'after changing embedding models |\n'
                       '| Hybrid search | Retrieval combining semantic/vector and lexical/keyword '
                       'signals |\n'
                       '| Reranker | Second-stage model or algorithm that reorders retrieved '
                       'candidates |\n'
                       '| Connector | Integration that ingests and refreshes data from an external '
                       'source system |\n'
                       '| Permission sync | Propagation of source-system access rules into '
                       'retrieval authorization |\n'
                       '| RAG sprawl | Proliferation of separately managed RAG stacks across an '
                       'organization |\n'
                       '| Policy drift | Gradual divergence of individual systems from centralized '
                       'governance standards |\n'
                       '| Shadow AI | AI systems deployed outside normal IT/security visibility '
                       'and governance |\n'
                       '| Golden path | Preapproved platform path that automatically applies '
                       'organizational standards |\n'
                       '| SaaS | Vendor-hosted deployment where infrastructure is primarily '
                       'managed by the provider |\n'
                       '| VPC | Isolated cloud-network deployment providing more customer control '
                       'than typical SaaS |\n'
                       '| On-premises | Deployment inside organization-controlled infrastructure '
                       '|\n'
                       '| Air-gapped | Environment with no external network connectivity |\n'
                       '| Corpus | Logical container holding prepared data for retrieval in the '
                       'platform example |\n'
                       '| Filter attribute | Structured metadata field used to constrain retrieval '
                       '|\n'
                       '| Factual consistency | Degree to which generated statements are supported '
                       'by retrieved context |\n'
                       '| Hallucination correction | Post-generation step that revises unsupported '
                       'claims using source evidence |\n'
                       '| Streaming response | Incremental delivery of generated output as tokens '
                       'become available |\n'
                       '| Platform lock-in | Cost or difficulty of moving applications and data '
                       'away from a provider |\n'
                       '| TCO | Total cost of ownership, including direct and indirect operational '
                       'costs |\n'
                       '\n'
                       '\n'
                       '## 59. Retain this idea\n'
                       '\n'
                       'The most useful mental model from this chapter is: **a RAG platform does '
                       'not replace the RAG stack; it changes the ownership boundary around it**. '
                       'The same conceptual stages—ingestion, representation, retrieval, '
                       'reranking, generation, quality control, governance, and operations—still '
                       'exist. The platform’s value is that many of them become standardized, '
                       'managed capabilities instead of separate systems your team must build and '
                       'operate. Your job shifts from wiring every component to deciding which '
                       'data, policies, quality controls, deployment model, and platform '
                       'capabilities your application actually needs.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Self-check\n'
                       '\n'
                       '1. What problem is a RAG platform trying to abstract for developers?\n'
                       '2. Which parts of the RAG application remain the customer’s responsibility '
                       'even when infrastructure is managed?\n'
                       '3. How does a standardized RAG API change the ownership boundary compared '
                       'with DIY RAG?\n'
                       '4. Why can a platform reduce time to production?\n'
                       '5. What operational obligations come with the flexibility of DIY RAG?\n'
                       '6. Why does open-source software not imply zero operational cost?\n'
                       '7. What is a central control plane in the context of RAG?\n'
                       '8. Which policies can benefit from being applied centrally across many RAG '
                       'applications?\n'
                       '9. Why does the value of central governance tend to increase as the number '
                       'of applications grows?\n'
                       '10. Which four broad questions should be asked when choosing between DIY '
                       'and a platform?\n'
                       '11. What does platform lock-in mean?\n'
                       '12. Which platform-specific choices could make migration expensive?\n'
                       '13. Why should platform selection start from the RAG pipeline rather than '
                       'from vendor marketing features?\n'
                       '14. Which ingestion capabilities should be examined during platform '
                       'evaluation?\n'
                       '15. Which retrieval capabilities should be examined during platform '
                       'evaluation?\n'
                       '16. Why can a default embedding model be problematic for multilingual '
                       'applications?\n'
                       '17. What does BYO embedding support protect you against?\n'
                       '18. Why must a corpus usually be re-embedded when the embedding model '
                       'changes?\n'
                       '19. What quality checks should happen before cutting over to a new '
                       'embedding model?\n'
                       '20. How does embedding dimensionality affect storage?\n'
                       '21. How does embedding dimensionality affect similarity-search '
                       'computation?\n'
                       '22. Why does a larger embedding dimension not guarantee a better '
                       'end-to-end RAG application?\n'
                       '23. How can a reranker change the importance of embedding-model choices?\n'
                       '24. What responsibilities are hidden behind the phrase “operate a vector '
                       'database”?\n'
                       '25. Why can an open-source vector database still have a high TCO?\n'
                       '26. What application-visible properties should be evaluated when the '
                       'platform manages the vector database?\n'
                       '27. When might deep vector-database customization justify DIY ownership?\n'
                       '28. Why is retrieval considered one of the highest-leverage RAG '
                       'components?\n'
                       '29. How can retrieval act as a safety boundary before generation?\n'
                       '30. What is the difference between basic vector search and a richer '
                       'production retrieval pipeline?\n'
                       '31. Why should a vendor’s retrieval roadmap matter to a platform '
                       'customer?\n'
                       '32. Which questions would you ask about hybrid search support?\n'
                       '33. Which questions would you ask about reranker support?\n'
                       '34. Why is prompt engineering not a set-and-forget activity?\n'
                       '35. How can changing the underlying LLM alter prompt behavior?\n'
                       '36. What is centralized prompt governance?\n'
                       '37. How can centralized prompt governance reduce inconsistent safety '
                       'behavior across teams?\n'
                       '38. Why is support for multiple LLMs useful over the lifetime of a RAG '
                       'system?\n'
                       '39. Which dimensions besides raw answer quality can influence LLM choice?\n'
                       '40. Why should changes in model behavior be treated as a '
                       'dependency-management problem?\n'
                       '41. What should be regression-tested when a platform changes its default '
                       'LLM?\n'
                       '42. When might BYO LLM capability be necessary?\n'
                       '43. How is hallucination detection different from hallucination '
                       'correction?\n'
                       '44. What information should a platform expose to make hallucination '
                       'controls auditable?\n'
                       '45. Why is a long list of connectors not enough to prove strong data '
                       'integration?\n'
                       '46. What does connector object coverage mean?\n'
                       '47. Why should attachment support be verified explicitly?\n'
                       '48. How can partial connector failures create hidden RAG quality '
                       'problems?\n'
                       '49. What should a connector do when a source document is deleted?\n'
                       '50. Why does incremental refresh matter for production RAG?\n'
                       '51. Why does permission synchronization matter for security?\n'
                       '52. What are the three broad DIY approaches to external data connectors '
                       'described in the chapter?\n'
                       '53. What is RAG sprawl?\n'
                       '54. How can RAG sprawl increase security risk?\n'
                       '55. How can RAG sprawl increase cost?\n'
                       '56. What is policy drift?\n'
                       '57. What is shadow AI?\n'
                       '58. Why does shadow AI create more than a simple infrastructure-management '
                       'problem?\n'
                       '59. What is a platform golden path?\n'
                       '60. How can a golden path enforce data-governance controls by default?\n'
                       '61. Which resources can be shared or standardized to reduce duplication '
                       'across RAG teams?\n'
                       '62. Why can duplicate embedding pipelines waste money?\n'
                       '63. What direct costs are easy to see in DIY RAG?\n'
                       '64. Which indirect or ongoing costs are easy to overlook?\n'
                       '65. Why should engineering and maintenance effort be included in TCO?\n'
                       '66. How does the developer-centric consumption pricing model behave as '
                       'usage grows?\n'
                       '67. How does an enterprise bundled-credit or subscription model aim to '
                       'improve predictability?\n'
                       '68. Which pricing questions should be asked beyond the advertised monthly '
                       'fee?\n'
                       '69. How does a platform shift the burden of future model and security '
                       'upgrades?\n'
                       '70. Why should the vendor roadmap be considered during platform '
                       'selection?\n'
                       '71. What are the three deployment models emphasized in the chapter?\n'
                       '72. What is the main operational advantage of SaaS?\n'
                       '73. What is the main security/control limitation of SaaS for some '
                       'organizations?\n'
                       '74. When is SaaS a nonstarter?\n'
                       '75. What additional expertise does a VPC deployment usually require?\n'
                       '76. Why can VPC be considered a middle ground?\n'
                       '77. What is the principal benefit of on-premises deployment?\n'
                       '78. What responsibilities return to the customer in on-premises '
                       'deployment?\n'
                       '79. Why does air-gapping affect OCR, embeddings, reranking, and multimodal '
                       'processing—not only the LLM?\n'
                       '80. How should hard security constraints influence deployment selection?\n'
                       '81. How do managed cloud service toolkits differ from an end-to-end RAG '
                       'platform?\n'
                       '82. Why do integration boundaries matter operationally?\n'
                       '83. Why does the chapter use Vectara as an example rather than as a '
                       'universal recommendation?\n'
                       '84. What is a corpus in the platform example?\n'
                       '85. Why might an organization use more than one corpus?\n'
                       '86. What is a document in the platform example?\n'
                       '87. Which metadata should be considered when designing a corpus?\n'
                       '88. What are filter attributes used for?\n'
                       '89. Why should metadata design happen before large-scale ingestion?\n'
                       '90. What API-key scopes are described in the source example?\n'
                       '91. How does least privilege apply to query, ingestion, and administration '
                       'services?\n'
                       '92. Why is reusing one full-access API key everywhere risky?\n'
                       '93. What hidden RAG stages can occur after a single file upload?\n'
                       '94. Why can an upload succeed while future retrieval quality is still '
                       'poor?\n'
                       '95. What kinds of ingestion behavior can be exposed as platform '
                       'configuration?\n'
                       '96. Why is table extraction a meaningful RAG ingestion option?\n'
                       '97. Why is direct structured ingestion needed in addition to file upload?\n'
                       '98. What benefits come from preserving nested sections?\n'
                       '99. How can local metadata on a section improve later retrieval?\n'
                       '100. Which major RAG stages can a single query API orchestrate?\n'
                       '101. What does lexical interpolation represent conceptually?\n'
                       '102. Why might a query API retrieve more candidates than it ultimately '
                       'sends to generation?\n'
                       '103. What is the purpose of context expansion around a matched passage?\n'
                       '104. What is the purpose of a reranker parameter?\n'
                       '105. What does max-used-search-results control?\n'
                       '106. Why can named generation presets support governance?\n'
                       '107. What user-experience problem does streaming solve?\n'
                       '108. Why does streaming not automatically improve retrieval accuracy?\n'
                       '109. What does a factual-consistency score measure?\n'
                       '110. Why can a factually consistent answer still be wrong for the user?\n'
                       '111. What evidence is needed for hallucination correction?\n'
                       '112. Why should a correction service expose the original and corrected '
                       'spans?\n'
                       '113. How can correction explanations help diagnose systemic RAG problems?\n'
                       '114. Which administrative resources should a mature RAG platform expose '
                       'through APIs?\n'
                       '115. Why is document deletion an important administrative capability?\n'
                       '116. How can query history help operations and quality teams?\n'
                       '117. Why should enterprise management functions be automatable rather than '
                       'console-only?\n'
                       '118. Which categories belong in a platform-selection scorecard?\n'
                       '119. How should retrieval capability be weighted relative to connector '
                       'count?\n'
                       '120. Why should deployment options be part of the selection scorecard?\n'
                       '121. Why should portability be considered before signing with a platform?\n'
                       '122. Which application boundaries can reduce platform-specific coupling?\n'
                       '123. Why should canonical source data remain under your control?\n'
                       '124. Why is it useful to maintain stable document IDs independent of the '
                       'platform?\n'
                       '125. How can an internal RAG interface reduce vendor-specific code '
                       'spread?\n'
                       '126. What is the central misconception behind saying that a platform '
                       'removes the need to understand RAG?\n'
                       '127. What is the central misconception behind saying that “managed” means '
                       'no responsibility?\n'
                       '128. What is the difference between source truth and factual consistency '
                       'with retrieved evidence?\n'
                       '129. In one sentence, what is the ownership-boundary mental model for RAG '
                       'platforms?\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Final mental model\n'
                       '\n'
                       '**Platform RAG is not a different kind of RAG. It is the same pipeline '
                       'with a different ownership boundary.** Understand the stages, decide which '
                       'controls your application must retain, and use the platform to remove '
                       'nondifferentiating operational work without giving up the quality, '
                       'security, governance, deployment, or portability properties your '
                       'organization actually needs.',
            'estimated_minutes': 570,
            'has_code_examples': True,
            'has_manual_image_requests': True,
            'sections': [{'id': 'platform-purpose',
                          'title': 'Why a RAG platform exists',
                          'order': 1},
                         {'id': 'diy-control-responsibility',
                          'title': 'DIY control comes with responsibility',
                          'order': 2},
                         {'id': 'central-control-plane',
                          'title': 'The platform as a central control plane',
                          'order': 3},
                         {'id': 'decision-framework',
                          'title': 'A decision framework: control, speed, operations, and lock-in',
                          'order': 4},
                         {'id': 'core-capabilities',
                          'title': 'Evaluate a platform from the RAG pipeline outward',
                          'order': 5},
                         {'id': 'embedding-defaults',
                          'title': 'Default embedding models and multilingual requirements',
                          'order': 6},
                         {'id': 'byo-embeddings',
                          'title': 'Bring-your-own embeddings and the re-indexing consequence',
                          'order': 7},
                         {'id': 'embedding-dimensions',
                          'title': 'Embedding dimensions: quality versus compute and storage',
                          'order': 8},
                         {'id': 'vector-db-diy',
                          'title': 'What DIY vector-database ownership really includes',
                          'order': 9},
                         {'id': 'managed-vector-db',
                          'title': 'Managed vector storage: abstraction with constraints',
                          'order': 10},
                         {'id': 'retrieval-quality-boundary',
                          'title': 'Advanced retrieval is a quality and safety boundary',
                          'order': 11},
                         {'id': 'hybrid-reranking-platform',
                          'title': 'Hybrid search and reranking: build them or consume them',
                          'order': 12},
                         {'id': 'prompt-engineering',
                          'title': 'Prompt engineering is a maintained component, not a one-time '
                                   'string',
                          'order': 13},
                         {'id': 'prompt-governance',
                          'title': 'Centralized prompt governance and consistent safety posture',
                          'order': 14},
                         {'id': 'multiple-llms',
                          'title': 'Support for multiple LLMs protects application flexibility',
                          'order': 15},
                         {'id': 'model-behavior-change',
                          'title': 'Model behavior can change even when your application code does '
                                   'not',
                          'order': 16},
                         {'id': 'byo-llm',
                          'title': 'Bring-your-own LLM for specialized or self-hosted generation',
                          'order': 17},
                         {'id': 'hallucination-controls',
                          'title': 'Hallucination detection and correction belong in the platform '
                                   'evaluation',
                          'order': 18},
                         {'id': 'data-connectors',
                          'title': 'Data connectors are part of the RAG product, not a peripheral '
                                   'feature',
                          'order': 19},
                         {'id': 'connector-due-diligence',
                          'title': 'A connector due-diligence checklist',
                          'order': 20},
                         {'id': 'connector-options',
                          'title': 'DIY connector options: build, open source, or commercial',
                          'order': 21},
                         {'id': 'refresh-permissions',
                          'title': 'Refresh and permission synchronization are correctness '
                                   'features',
                          'order': 22},
                         {'id': 'rag-sprawl',
                          'title': 'RAG sprawl: when every team builds a different stack',
                          'order': 23},
                         {'id': 'policy-drift-shadow-ai',
                          'title': 'Policy drift and shadow AI',
                          'order': 24},
                         {'id': 'golden-path',
                          'title': 'A platform “golden path” for governance',
                          'order': 25},
                         {'id': 'resource-duplication',
                          'title': 'Centralization can reduce duplicated infrastructure and effort',
                          'order': 26},
                         {'id': 'true-diy-cost',
                          'title': 'DIY cost is more than API tokens',
                          'order': 27},
                         {'id': 'platform-pricing-models',
                          'title': 'Two platform pricing patterns',
                          'order': 28},
                         {'id': 'platform-evolution',
                          'title': 'Upgrades and platform evolution shift ongoing work to the '
                                   'vendor',
                          'order': 29},
                         {'id': 'deployment-spectrum',
                          'title': 'Deployment is a spectrum: SaaS, VPC, and on-premises',
                          'order': 30},
                         {'id': 'diy-deployment',
                          'title': 'DIY deployment flexibility is limited by component '
                                   'availability',
                          'order': 31},
                         {'id': 'saas-platform',
                          'title': 'SaaS platform: operational simplicity with external trust',
                          'order': 32},
                         {'id': 'vpc-platform',
                          'title': 'VPC deployment: a middle ground',
                          'order': 33},
                         {'id': 'onprem-platform',
                          'title': 'On-premises and air-gapped platform deployment',
                          'order': 34},
                         {'id': 'deployment-selection',
                          'title': 'Selecting a deployment model from requirements',
                          'order': 35},
                         {'id': 'middle-ground-cloud-services',
                          'title': 'Cloud “platforms of services” versus end-to-end RAG platforms',
                          'order': 36},
                         {'id': 'vectara-role',
                          'title': 'Vectara as the chapter’s concrete platform example',
                          'order': 37},
                         {'id': 'corpus-document-model',
                          'title': 'Corpus and document: the platform’s data model',
                          'order': 38},
                         {'id': 'corpus-configuration',
                          'title': 'Corpus configuration: identity, embedding, and filter '
                                   'attributes',
                          'order': 39},
                         {'id': 'api-key-scope',
                          'title': 'API keys and least-privilege access',
                          'order': 40},
                         {'id': 'file-upload',
                          'title': 'File upload: one API call, many hidden stages',
                          'order': 41},
                         {'id': 'upload-hidden-pipeline',
                          'title': 'Tracing the hidden ingestion pipeline',
                          'order': 42},
                         {'id': 'ingestion-options',
                          'title': 'Configurable ingestion: chunking, tables, images, and metadata',
                          'order': 43},
                         {'id': 'direct-ingestion',
                          'title': 'Direct structured ingestion for non-file data',
                          'order': 44},
                         {'id': 'hierarchical-sections',
                          'title': 'Nested sections preserve document structure',
                          'order': 45},
                         {'id': 'single-query-api',
                          'title': 'The platform query API collapses the RAG query flow',
                          'order': 46},
                         {'id': 'search-parameters',
                          'title': 'Reading query parameters as retrieval architecture',
                          'order': 47},
                         {'id': 'generation-parameters',
                          'title': 'Generation controls: how much context, which prompt, and '
                                   'factual consistency',
                          'order': 48},
                         {'id': 'streaming',
                          'title': 'Streaming changes perceived latency, not retrieval quality',
                          'order': 49},
                         {'id': 'factual-consistency-output',
                          'title': 'Use factual-consistency scores as signals, not magic truth',
                          'order': 50},
                         {'id': 'hallucination-correction',
                          'title': 'Hallucination correction as a separate platform operation',
                          'order': 51},
                         {'id': 'correction-audit',
                          'title': 'Corrections should be auditable',
                          'order': 52},
                         {'id': 'admin-apis',
                          'title': 'Administrative APIs turn a platform into manageable '
                                   'infrastructure',
                          'order': 53},
                         {'id': 'central-it-automation',
                          'title': 'Why central IT needs automation and query visibility',
                          'order': 54},
                         {'id': 'platform-selection-scorecard',
                          'title': 'Build a platform-selection scorecard',
                          'order': 55},
                         {'id': 'lockin-mitigation',
                          'title': 'Design for platform portability before you need it',
                          'order': 56},
                         {'id': 'misconceptions', 'title': 'Important misconceptions', 'order': 57},
                         {'id': 'terminology', 'title': 'Key terminology', 'order': 58},
                         {'id': 'retain-idea', 'title': 'Retain this idea', 'order': 59}]},
 'exercises': [{'id': 'M01.L05.EX01',
                'title': 'Platform or DIY?',
                'lesson_code': 'M01.L05',
                'section_id': 'platform-purpose',
                'placement': 'after_section',
                'description': 'Compare ownership boundaries',
                'instructions': 'You are designing an internal support assistant. Draw two '
                                'architectures: DIY and managed platform. Mark which team owns '
                                'parsing, embedding, storage, retrieval, generation, security '
                                'updates, and observability in each.',
                'expected_output': 'A side-by-side architecture with explicit ownership for each '
                                   'RAG stage.',
                'difficulty': 'intermediate',
                'skill_tested': 'architecture trade-offs'},
               {'id': 'M01.L05.EX02',
                'title': 'Lock-in review',
                'lesson_code': 'M01.L05',
                'section_id': 'decision-framework',
                'placement': 'after_section',
                'description': 'Identify migration risks',
                'instructions': 'List five platform-specific decisions that could make a future '
                                'migration difficult. For each, state one design choice that could '
                                'reduce the dependency.',
                'expected_output': 'A risk table pairing platform dependency with a portability '
                                   'mitigation.',
                'difficulty': 'intermediate',
                'skill_tested': 'platform portability'},
               {'id': 'M01.L05.EX03',
                'title': 'Embedding migration plan',
                'lesson_code': 'M01.L05',
                'section_id': 'byo-embeddings',
                'placement': 'after_section',
                'description': 'Plan a model replacement',
                'instructions': 'Assume the current embedding model is weak in a new language. '
                                'Design a safe migration plan that accounts for re-embedding, '
                                'index rebuild, quality comparison, and cutover.',
                'expected_output': 'A staged migration plan from old embedding space to new '
                                   'embedding space.',
                'difficulty': 'intermediate',
                'skill_tested': 'embedding lifecycle'},
               {'id': 'M01.L05.EX04',
                'title': 'Vector ownership inventory',
                'lesson_code': 'M01.L05',
                'section_id': 'vector-db-diy',
                'placement': 'after_section',
                'description': 'Expose hidden operations',
                'instructions': 'For a DIY vector database, enumerate the operational '
                                'responsibilities beyond vector search itself. Classify each as '
                                'deployment, reliability, security, performance, or maintenance.',
                'expected_output': 'A categorized operations inventory.',
                'difficulty': 'beginner',
                'skill_tested': 'vector infrastructure'},
               {'id': 'M01.L05.EX05',
                'title': 'Retrieval capability scorecard',
                'lesson_code': 'M01.L05',
                'section_id': 'hybrid-reranking-platform',
                'placement': 'after_section',
                'description': 'Evaluate retrieval controls',
                'instructions': 'Create a vendor scorecard for semantic search, lexical search, '
                                'fusion, metadata filtering, reranking, multilingual support, and '
                                'result observability.',
                'expected_output': 'A retrieval-focused platform evaluation scorecard.',
                'difficulty': 'intermediate',
                'skill_tested': 'retrieval evaluation'},
               {'id': 'M01.L05.EX06',
                'title': 'Prompt governance design',
                'lesson_code': 'M01.L05',
                'section_id': 'prompt-governance',
                'placement': 'after_section',
                'description': 'Centralize prompt policy',
                'instructions': 'Design a process in which teams can customize application prompts '
                                'while central security controls mandatory grounding and '
                                'injection-defense instructions.',
                'expected_output': 'A governance workflow separating mandatory policy from '
                                   'application customization.',
                'difficulty': 'intermediate',
                'skill_tested': 'prompt governance'},
               {'id': 'M01.L05.EX07',
                'title': 'Model-change regression plan',
                'lesson_code': 'M01.L05',
                'section_id': 'model-behavior-change',
                'placement': 'after_section',
                'description': 'Test model drift',
                'instructions': 'A platform upgrades its default LLM. Define what you would '
                                'evaluate before accepting the change, including quality, '
                                'instruction following, latency, and domain-specific failures.',
                'expected_output': 'A regression checklist and acceptance criteria.',
                'difficulty': 'intermediate',
                'skill_tested': 'model lifecycle'},
               {'id': 'M01.L05.EX08',
                'title': 'Hallucination response policy',
                'lesson_code': 'M01.L05',
                'section_id': 'hallucination-controls',
                'placement': 'after_section',
                'description': 'Design an application response policy',
                'instructions': 'Define how an application should react to high, medium, and low '
                                'factual-consistency signals. Include when to return, warn, '
                                'correct, or escalate.',
                'expected_output': 'A decision table for factual-consistency handling.',
                'difficulty': 'intermediate',
                'skill_tested': 'hallucination controls'},
               {'id': 'M01.L05.EX09',
                'title': 'Connector due diligence',
                'lesson_code': 'M01.L05',
                'section_id': 'connector-due-diligence',
                'placement': 'after_section',
                'description': 'Inspect connector depth',
                'instructions': 'Choose one enterprise source and write ten questions covering '
                                'object coverage, attachments, refresh, deletions, permissions, '
                                'failure recovery, deployment, and monitoring.',
                'expected_output': 'A connector acceptance checklist grounded in operational '
                                   'behavior.',
                'difficulty': 'intermediate',
                'skill_tested': 'data integration'},
               {'id': 'M01.L05.EX10',
                'title': 'Stop RAG sprawl',
                'lesson_code': 'M01.L05',
                'section_id': 'golden-path',
                'placement': 'after_section',
                'description': 'Design a golden path',
                'instructions': 'Your company has five teams using different vector stores and '
                                'LLMs. Design a minimum platform policy that standardizes security '
                                'and governance without forcing all teams into identical '
                                'applications.',
                'expected_output': 'A platform baseline defining shared controls and allowed '
                                   'customization.',
                'difficulty': 'intermediate',
                'skill_tested': 'governance'},
               {'id': 'M01.L05.EX11',
                'title': 'TCO comparison',
                'lesson_code': 'M01.L05',
                'section_id': 'true-diy-cost',
                'placement': 'after_section',
                'description': 'Compare direct and indirect cost',
                'instructions': 'Build a TCO worksheet comparing DIY and managed platform RAG. '
                                'Include engineering, infrastructure, model APIs, monitoring, '
                                'support, security, and ongoing upgrades.',
                'expected_output': 'A cost model that does not compare only subscription fees.',
                'difficulty': 'intermediate',
                'skill_tested': 'TCO analysis'},
               {'id': 'M01.L05.EX12',
                'title': 'Choose a deployment model',
                'lesson_code': 'M01.L05',
                'section_id': 'deployment-spectrum',
                'placement': 'after_section',
                'description': 'Map requirements to SaaS/VPC/on-prem',
                'instructions': 'For three organizations—a startup with public documentation, a '
                                'regulated bank, and an air-gapped defense environment—choose a '
                                'plausible deployment model and justify it from constraints.',
                'expected_output': 'Three requirement-based deployment decisions without assuming '
                                   'one model fits all.',
                'difficulty': 'intermediate',
                'skill_tested': 'deployment architecture'},
               {'id': 'M01.L05.EX13',
                'title': 'Design corpora',
                'lesson_code': 'M01.L05',
                'section_id': 'corpus-document-model',
                'placement': 'after_section',
                'description': 'Partition knowledge intentionally',
                'instructions': 'You have HR policies, public product docs, and support tickets. '
                                'Propose corpus boundaries and explain access, metadata, and '
                                'application reasons for your design.',
                'expected_output': 'A corpus architecture with clear isolation rationale.',
                'difficulty': 'intermediate',
                'skill_tested': 'knowledge architecture'},
               {'id': 'M01.L05.EX14',
                'title': 'Least-privilege keys',
                'lesson_code': 'M01.L05',
                'section_id': 'api-key-scope',
                'placement': 'after_section',
                'description': 'Scope platform credentials',
                'instructions': 'Assign credentials to a query API, an ingestion worker, and an '
                                'administrative automation job. Explain why they should not share '
                                'one full-access key.',
                'expected_output': 'A least-privilege credential map.',
                'difficulty': 'beginner',
                'skill_tested': 'API security'},
               {'id': 'M01.L05.EX15',
                'title': 'Trace a file upload',
                'lesson_code': 'M01.L05',
                'section_id': 'file-upload',
                'placement': 'after_section',
                'description': 'Explain platform abstraction',
                'instructions': 'Starting from an uploaded PDF, trace the hidden stages until the '
                                'document becomes retrievable. For each stage, name one possible '
                                'failure symptom visible at query time.',
                'expected_output': 'An ingestion trace connecting hidden platform stages to '
                                   'observable failures.',
                'difficulty': 'intermediate',
                'skill_tested': 'ingestion debugging'},
               {'id': 'M01.L05.EX16',
                'title': 'Model structured ingestion',
                'lesson_code': 'M01.L05',
                'section_id': 'direct-ingestion',
                'placement': 'after_section',
                'description': 'Preserve hierarchy and metadata',
                'instructions': 'Represent a policy manual with chapters, sections, dates, '
                                'departments, and sensitivity labels using nested sections and '
                                'metadata.',
                'expected_output': 'A structured document object that preserves hierarchy and '
                                   'useful retrieval metadata.',
                'difficulty': 'intermediate',
                'skill_tested': 'structured ingestion'},
               {'id': 'M01.L05.EX17',
                'title': 'Tune the query payload',
                'lesson_code': 'M01.L05',
                'section_id': 'search-parameters',
                'placement': 'after_section',
                'description': 'Reason about retrieval knobs',
                'instructions': 'For a query with an exact product code plus a natural-language '
                                'problem description, explain how you would think about lexical '
                                'interpolation, candidate limit, context expansion, and reranking.',
                'expected_output': 'A justified query configuration based on retrieval behavior.',
                'difficulty': 'intermediate',
                'skill_tested': 'query tuning'},
               {'id': 'M01.L05.EX18',
                'title': 'Correct and audit',
                'lesson_code': 'M01.L05',
                'section_id': 'hallucination-correction',
                'placement': 'after_section',
                'description': 'Use correction safely',
                'instructions': 'A generated answer contains two unsupported claims. Define the '
                                'data you would send to a correction service and the correction '
                                'information you would log for later analysis.',
                'expected_output': 'An evidence-aware correction and audit record design.',
                'difficulty': 'intermediate',
                'skill_tested': 'hallucination correction'}],
 'quiz': {'id': 'M01.L05.QZ01',
          'title': 'The RAG Platform — Lesson Quiz',
          'lesson_code': 'M01.L05',
          'placement': 'lesson_end',
          'questions': [{'id': 'M01.L05.Q01',
                         'section_id': 'platform-purpose',
                         'question': 'What is the most important architectural change introduced '
                                     'by a RAG platform?',
                         'options': ['The RAG pipeline no longer needs retrieval',
                                     'Operational ownership of many RAG components shifts toward '
                                     'the platform provider',
                                     'Embeddings are replaced by keyword search',
                                     'Every application must use the same corpus'],
                         'correct': 1,
                         'explanation': 'A platform still contains the familiar RAG stages; its '
                                        'key value is packaging and operating many of those stages '
                                        'behind managed APIs.'},
                        {'id': 'M01.L05.Q02',
                         'section_id': 'decision-framework',
                         'question': 'Which concern is most directly associated with platform '
                                     'lock-in?',
                         'options': ['The inability to use any metadata',
                                     'Migration cost caused by platform-specific APIs, '
                                     'representations, and workflows',
                                     'The requirement to use only small language models',
                                     'The impossibility of running hybrid search'],
                         'correct': 1,
                         'explanation': 'Lock-in is about dependence that makes switching '
                                        'providers expensive or difficult, not about one universal '
                                        'missing feature.'},
                        {'id': 'M01.L05.Q03',
                         'section_id': 'byo-embeddings',
                         'question': 'Why does changing embedding models usually require '
                                     're-encoding the corpus?',
                         'options': ['Embedding models create vectors in model-specific '
                                     'representation spaces',
                                     'Vector databases only accept one document at a time',
                                     'Rerankers cannot read old chunks',
                                     'Prompts contain the old model name'],
                         'correct': 0,
                         'explanation': 'Stored vectors and query vectors must inhabit a '
                                        'compatible representation space, so a new embedding model '
                                        'normally requires new document embeddings and an updated '
                                        'index.'},
                        {'id': 'M01.L05.Q04',
                         'section_id': 'embedding-dimensions',
                         'question': 'What is a likely cost of using higher-dimensional '
                                     'embeddings?',
                         'options': ['Lower storage and less computation',
                                     'More storage and similarity-search computation',
                                     'Elimination of reranking',
                                     'Guaranteed higher end-to-end RAG accuracy'],
                         'correct': 1,
                         'explanation': 'Higher-dimensional vectors generally consume more storage '
                                        'and compute. They may improve representation, but they do '
                                        'not guarantee better overall RAG quality.'},
                        {'id': 'M01.L05.Q05',
                         'section_id': 'hybrid-reranking-platform',
                         'question': 'Why should retrieval capabilities be a major '
                                     'platform-selection criterion?',
                         'options': ['Retrieval determines which evidence reaches the generator',
                                     'Retrieval only affects billing dashboards',
                                     'Retrieval is irrelevant when the LLM is large enough',
                                     'Retrieval is used only during ingestion'],
                         'correct': 0,
                         'explanation': 'The generator depends on retrieved evidence. Strong '
                                        'hybrid search and reranking can materially improve '
                                        'relevance and reliability.'},
                        {'id': 'M01.L05.Q06',
                         'section_id': 'prompt-governance',
                         'question': 'What is one organizational benefit of centralized prompt '
                                     'governance?',
                         'options': ['It guarantees every application has identical business logic',
                                     'It can apply shared safety and grounding policies '
                                     'consistently across applications',
                                     'It removes the need for RAG evaluation',
                                     'It prevents any team from changing its user interface'],
                         'correct': 1,
                         'explanation': 'Central governance can standardize mandatory prompt and '
                                        'safety behavior while still allowing application-level '
                                        'customization.'},
                        {'id': 'M01.L05.Q07',
                         'section_id': 'multiple-llms',
                         'question': 'Why is support for multiple LLMs strategically useful?',
                         'options': ['All LLMs behave identically',
                                     'Different applications and future conditions may require '
                                     'different quality, cost, latency, privacy, or hosting '
                                     'properties',
                                     'It removes the need for prompts',
                                     'It prevents model updates'],
                         'correct': 1,
                         'explanation': 'Model requirements change across workloads and over time, '
                                        'so a platform that supports multiple LLMs preserves '
                                        'flexibility.'},
                        {'id': 'M01.L05.Q08',
                         'section_id': 'connector-due-diligence',
                         'question': 'Which connector property is most important for preventing '
                                     'silent knowledge gaps?',
                         'options': ['A colorful configuration screen',
                                     'Visibility into partial failures and skipped content',
                                     'A high marketing connector count',
                                     'Using only PDF files'],
                         'correct': 1,
                         'explanation': 'If skipped or failed items are invisible, the knowledge '
                                        'base can be incomplete without operators realizing it.'},
                        {'id': 'M01.L05.Q09',
                         'section_id': 'refresh-permissions',
                         'question': 'Why is permission synchronization part of RAG correctness?',
                         'options': ['It makes embeddings shorter',
                                     'It helps ensure retrieval does not surface content the user '
                                     'is unauthorized to access',
                                     'It replaces reranking',
                                     'It is only needed for public documents'],
                         'correct': 1,
                         'explanation': 'RAG retrieval must respect source access controls; '
                                        'otherwise the system can leak confidential content.'},
                        {'id': 'M01.L05.Q10',
                         'section_id': 'rag-sprawl',
                         'question': 'What best describes RAG sprawl?',
                         'options': ['A single corpus containing many documents',
                                     'Many independently managed RAG stacks with duplicated '
                                     'components and inconsistent policies',
                                     'Using more than one chunk per answer',
                                     'Serving responses to many users'],
                         'correct': 1,
                         'explanation': 'RAG sprawl refers to fragmented stacks across teams, '
                                        'creating duplicated infrastructure and governance '
                                        'complexity.'},
                        {'id': 'M01.L05.Q11',
                         'section_id': 'true-diy-cost',
                         'question': 'Why can a DIY RAG system appear cheaper than it really is?',
                         'options': ['Teams may count only visible API or license fees and ignore '
                                     'engineering and operations',
                                     'Vector databases are always free to operate',
                                     'Platforms never charge for usage',
                                     'LLMs do not incur token costs'],
                         'correct': 0,
                         'explanation': 'A realistic TCO includes staffing, infrastructure, '
                                        'security, testing, maintenance, observability, and '
                                        'upgrades.'},
                        {'id': 'M01.L05.Q12',
                         'section_id': 'deployment-spectrum',
                         'question': 'Which deployment model generally transfers the most '
                                     'infrastructure responsibility to the customer?',
                         'options': ['SaaS',
                                     'On-premises / air-gapped',
                                     'A public web demo',
                                     'Query-only API access'],
                         'correct': 1,
                         'explanation': 'On-premises provides maximum control and isolation but '
                                        'requires the customer to operate hardware, software, '
                                        'model serving, and security.'},
                        {'id': 'M01.L05.Q13',
                         'section_id': 'middle-ground-cloud-services',
                         'question': 'How does an end-to-end RAG platform differ from a collection '
                                     'of managed cloud services?',
                         'options': ['It typically presents a more unified API over multiple RAG '
                                     'stages',
                                     'It never uses vector search',
                                     'It cannot support managed infrastructure',
                                     'It only provides a user interface'],
                         'correct': 0,
                         'explanation': 'Managed service toolkits simplify individual parts, while '
                                        'an end-to-end platform aims to unify the RAG workflow '
                                        'behind a standardized surface.'},
                        {'id': 'M01.L05.Q14',
                         'section_id': 'api-key-scope',
                         'question': 'Which credential design best follows least privilege?',
                         'options': ['Use one personal full-access key in every component',
                                     'Give the query service query-only access and grant '
                                     'ingestion/admin rights only where required',
                                     'Store all keys in frontend JavaScript',
                                     'Disable authentication inside the organization'],
                         'correct': 1,
                         'explanation': 'Least privilege scopes each identity to the smallest set '
                                        'of actions needed for its responsibility.'},
                        {'id': 'M01.L05.Q15',
                         'section_id': 'upload-hidden-pipeline',
                         'question': 'Why must developers still understand parsing and chunking '
                                     'when using a managed upload API?',
                         'options': ['Because managed platforms never parse files',
                                     'Because retrieval failures can still originate in hidden '
                                     'ingestion stages and need conceptual debugging',
                                     'Because APIs cannot store metadata',
                                     'Because chunking happens only in the browser'],
                         'correct': 1,
                         'explanation': 'Abstraction changes how the stage is operated, but the '
                                        'stage still affects retrieval quality and failure '
                                        'diagnosis.'},
                        {'id': 'M01.L05.Q16',
                         'section_id': 'search-parameters',
                         'question': 'What does lexical interpolation represent in the source '
                                     'query example?',
                         'options': ['The balance between lexical and semantic retrieval signals',
                                     'The number of API keys',
                                     'The embedding vector dimension',
                                     'The number of corpora in the account'],
                         'correct': 0,
                         'explanation': 'The parameter controls the hybrid-search balance between '
                                        'lexical and semantic retrieval.'},
                        {'id': 'M01.L05.Q17',
                         'section_id': 'factual-consistency-output',
                         'question': 'A response receives a high factual-consistency score but '
                                     'cites an outdated policy. What does this show?',
                         'options': ['The answer must be current and correct',
                                     'Faithfulness to retrieved context is different from '
                                     'correctness of the underlying source data',
                                     'The vector database is unavailable',
                                     'Streaming should be disabled'],
                         'correct': 1,
                         'explanation': 'A model can faithfully summarize stale evidence. Factual '
                                        'consistency is evidence support, not a guarantee that the '
                                        'evidence itself is current.'},
                        {'id': 'M01.L05.Q18',
                         'section_id': 'platform-selection-scorecard',
                         'type': 'open',
                         'question': 'You are comparing two RAG platforms. One has stronger '
                                     'retrieval and governance but fewer connectors; the other has '
                                     'many connectors but weak permission synchronization and '
                                     'limited reranking. Explain how you would decide using the '
                                     'chapter’s framework.',
                         'explanation': 'A strong answer prioritizes actual requirements and '
                                        'examines connector depth, permission correctness, '
                                        'retrieval quality, governance, deployment constraints, '
                                        'TCO, operations, and portability rather than choosing '
                                        'from a single feature count.'}],
          'passing_score': 70}}
