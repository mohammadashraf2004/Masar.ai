"""M01.L01 — Introduction to Retrieval-Augmented Generation (RAG).

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 1, pages not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = 'RAG Foundations'

MODULE_DESCRIPTION = ('Build the mental model for retrieval-augmented generation: why it is needed, how ingestion and query flows work, how a basic implementation is assembled, and how RAG compares with long-context prompting and fine-tuning.')

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": 'Introduction to Retrieval-Augmented Generation (RAG)',

    "slug": "rag-foundations-m01-l01",

    "description": (
        "Learn why retrieval-augmented generation is needed, how ingestion and query "
        "flows work, how a basic RAG pipeline is assembled, and how RAG compares "
        "with long-context prompting, fine-tuning, and advanced RAG approaches."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        'rag',
        'retrieval',
        'embeddings',
        'vector-search',
        'langchain',
        'production-rag',
    ],

    "prerequisite_ids": [],

    "lesson": {
        "title": 'Introduction to Retrieval-Augmented Generation (RAG)',

        "content": '# Introduction to Retrieval-Augmented Generation (RAG)\n\n> **Course:** Retrieval-Augmented Generation (RAG)  \n> **Lesson:** M01.L01  \n> **Module:** RAG Foundations  \n> **Source alignment:** Supplied source, Chapter 1. Page numbers were not provided in the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n\n---\n\n## Learning outcomes\n\nBy the end of this lesson, you should be able to:\n\n- Explain why a capable LLM can still fail on private, current, or niche information.\n- Describe RAG as a retrieval step followed by grounded generation.\n- Distinguish parametric knowledge from knowledge retrieved at query time.\n- Explain the difference between a dataset, corpus, and search index.\n- Trace a RAG ingestion flow from source documents to stored embeddings and text.\n- Trace a RAG query flow from a user question to retrieval, prompting, generation, citations, and guardrails.\n- Compare semantic, lexical, hybrid search, and reranking at a high level.\n- Explain why production RAG requires evaluation, monitoring, security, and operational controls.\n- Read a simple LangChain RAG implementation and explain the role of each component.\n- Compare RAG with full-document prompting and fine-tuning.\n- Identify major benefits and enterprise use cases of RAG.\n- Explain the basic ideas behind agentic RAG, multimodal RAG, and knowledge-graph-enhanced RAG.\n\n---\n\n## 1. Why RAG Exists\n\nA large language model can be excellent at language while still being blind to the facts your application actually needs.\n\nImagine an internal company assistant. The base LLM may write fluent answers, summarize documents, and produce code. But a question such as:\n\n```text\nWhat is our refund policy after January next year?\n```\n\ndepends on company-specific and time-sensitive information. That information may never have appeared in the model\'s training data, and even if an older version did, the policy may have changed.\n\nThis exposes a fundamental limitation: an LLM\'s training cannot contain every public fact, every private document, every database row, and every future update. Training is a snapshot. Real organizations are constantly changing.\n\nWhen the model lacks the needed evidence, it may still generate a confident answer. The chapter uses the term **hallucination** for generated content that is unsupported by real data available to justify it.\n\nA useful mental model is:\n\n```text\nFluency is not the same as factual access.\n\nA model may know how to answer\nwithout knowing the facts required for this answer.\n```\n\nRAG addresses this gap by giving the model a way to obtain relevant external information at the time the question is asked.\n\n{{exercise:M01.L01.EX01}}\n\n---\n\n## 2. The Core RAG Loop: Retrieve, Augment, Generate\n\nRetrieval-augmented generation has two essential stages:\n\n1. **Retrieval (R):** find information that is relevant to the user\'s query.\n2. **Generation (G):** give the query and retrieved information to an LLM so it can produce a grounded answer.\n\nThe word **augmented** captures the bridge between them: retrieved facts are added to the model\'s prompt, augmenting what the model can use during generation.\n\nA basic flow looks like this:\n\n```text\nUser question\n    |\n    v\nRetrieve relevant facts\n    |\n    v\nAdd facts to the prompt\n    |\n    v\nLLM generates an answer grounded in those facts\n```\n\n[[IMAGE_NEEDED: Basic RAG architecture | A user query flowing first to a retrieval component that fetches relevant information from a private knowledge source, then to an LLM that receives both the query and retrieved context and produces the final answer | Learner should notice that retrieval happens before generation and that the LLM is grounded by external context]]\n\n### Example: a grounded medical question\n\nSuppose a RAG system is connected to a private collection of medical books and journal papers. A user asks:\n\n```text\nWhat are the effective treatments for diabetes?\n```\n\nThe system should not ask the LLM to rely only on its internal memory. Instead:\n\n```text\nQuestion\n  -> retrieve passages about diabetes treatment\n  -> place those passages in the prompt\n  -> ask the LLM to answer from that evidence\n```\n\nA minimal prompt pattern can be expressed as:\n\n```text\nYou are answering a question from retrieved evidence.\n\nQuestion:\n{question}\n\nRetrieved context:\n{context}\n\nAnswer using the context. If the context does not contain the answer,\nsay that you do not know.\n```\n\nThis is the central RAG idea. Retrieval supplies evidence; generation turns that evidence into a useful response.\n\n---\n\n## 3. Parametric Knowledge vs Retrieved Knowledge\n\nThe chapter compares ordinary LLM use with a **closed-book test**, and RAG with an **open-book test**.\n\n### Closed-book: parametric knowledge\n\nA model\'s training changes the values of its neural-network parameters, or **weights**. Information represented through those learned parameters is called **parametric knowledge**.\n\nIn closed-book use:\n\n```text\nQuestion -> LLM weights -> Answer\n```\n\nThe model can only rely on what its training and post-training made available through those parameters.\n\n### Open-book: retrieved knowledge\n\nIn RAG:\n\n```text\nQuestion\n   -> retrieve external evidence\n   -> Question + evidence\n   -> LLM\n   -> Answer\n```\n\nThe model receives additional information in real time. This means the application can use facts that are private, recently updated, or too specialized to expect from the base model.\n\nThe distinction matters because RAG does not require every fact to be memorized inside the model. The model can remain a general language-and-reasoning engine while the external knowledge system supplies task-specific evidence.\n\n---\n\n## 4. The Blueprint of a RAG Stack\n\nA practical RAG system has two different flows:\n\n```text\nINGESTION FLOW\nSource data\n  -> extract / parse\n  -> prepare\n  -> chunk\n  -> embed / index\n  -> store searchable representations + original text\n\nQUERY FLOW\nUser query\n  -> represent / search\n  -> retrieve candidate facts\n  -> optionally improve ranking\n  -> build prompt\n  -> LLM generation\n  -> citations / guardrails\n  -> final response\n```\n\n{{image:rag-stack}}\n\nThe two flows solve different problems. Ingestion asks, **"How do we make our knowledge searchable?"** Query processing asks, **"How do we find the right evidence for this question and turn it into an answer?"**\n\n---\n\n## 5. The Ingestion Flow\n\nIngestion prepares source data for retrieval.\n\nSources might include databases, PDF files, object storage, or knowledge-management systems. The exact source is less important than the transformation:\n\n```text\nRaw source\n  -> extract usable content\n  -> clean / prepare\n  -> split into manageable pieces\n  -> create representations for search\n  -> store representations and original text\n```\n\n### Embeddings and indexing\n\nAn **embedding** is a vector representation intended to capture semantic meaning. During ingestion, text can be converted into embeddings and stored in a **vector database**.\n\nThe system also needs the actual text associated with each vector. A vector alone is useful for matching, but the generation step needs readable facts to place into the LLM prompt.\n\nA simplified stored record is conceptually:\n\n```text\n{\n  vector: [ ... semantic representation ... ],\n  text:   "The policy states that ...",\n  metadata: { ... optional source or permission fields ... }\n}\n```\n\nThe chapter notes that production ingestion becomes much more involved. Important concerns include:\n\n- document preprocessing,\n- chunking,\n- embedding,\n- data validation,\n- multimodal inputs,\n- incremental updates.\n\n### Dataset, corpus, and index\n\nThese terms are sometimes used loosely, but the chapter gives a useful distinction:\n\n| Term | Precise mental model |\n|---|---|\n| Dataset / document set | The initial raw collection of source files or records |\n| Corpus | The curated, cleaned, and organized body of content |\n| Index | A search-optimized data structure built from the corpus |\n\nSo an **index** is not merely "all the documents." It is the structure created to make retrieval fast and effective.\n\n{{exercise:M01.L01.EX02}}\n\n---\n\n## 6. Retrieval: Embeddings, Semantic Search, and Better Search\n\nAt query time, retrieval tries to find the facts most useful for answering the user\'s question.\n\nA basic semantic retrieval path is:\n\n```text\nUser query\n  -> query embedding\n  -> similarity search in the vector database\n  -> top matching text chunks\n```\n\n### Semantic search\n\n**Semantic search** uses embeddings to match meaning rather than relying only on exact wording.\n\nFor example, a query such as:\n\n```text\nHow can an employee get reimbursed for travel?\n```\n\nmay still match a passage headed:\n\n```text\nBusiness expense repayment procedure\n```\n\neven though the exact words differ, because the representations can capture related meaning.\n\n[[IMAGE_NEEDED: Semantic retrieval in embedding space | A conceptual diagram with one query point and several document-chunk points, highlighting nearby semantically related chunks and distant unrelated chunks | Learner should notice that semantic similarity is based on vector proximity rather than exact word overlap]]\n\n### Lexical search\n\n**Lexical search** matches based more directly on written forms, words, and terms. It can be useful when exact terminology matters.\n\n### Hybrid search and reranking\n\nThe chapter emphasizes that semantic vector search is only a basic retrieval method and may be insufficient for high-quality production RAG.\n\nTwo important improvements are:\n\n- **Hybrid search:** combine semantic search with lexical search.\n- **Reranking:** take candidate results and reorder them so the most relevant evidence rises to the top.\n\nThe goal is not to retrieve a lot of text. The goal is to retrieve the **right facts**.\n\nA better retrieval pipeline can be summarized as:\n\n```text\nQuery\n  -> retrieve candidates\n  -> combine complementary search signals\n  -> rerank candidates\n  -> keep the strongest evidence\n```\n\n---\n\n## 7. Generation: Grounding the LLM in Retrieved Facts\n\nAfter retrieval, the system constructs a prompt containing:\n\n- the user\'s original query,\n- the retrieved facts,\n- instructions describing how the LLM should answer.\n\nThis is where retrieval becomes **augmented generation**.\n\nThe model is not merely asked:\n\n```text\nAnswer this question.\n```\n\nIt is asked something closer to:\n\n```text\nAnswer this question using the retrieved evidence below.\nIf the evidence does not support an answer, say so.\n```\n\nThe grounding instruction matters because simply attaching context does not guarantee good behavior. The prompt should make the relationship between the question, evidence, and answer explicit.\n\n### A useful generation contract\n\nThink of the generation step as a contract:\n\n```text\nInput:\n  question + retrieved evidence\n\nExpected behavior:\n  synthesize an answer from that evidence\n\nFailure behavior:\n  if evidence is insufficient, do not invent missing facts\n```\n\nThis shifts the task from "recall anything you know" toward "reason over the evidence supplied for this query."\n\n{{exercise:M01.L01.EX03}}\n\n---\n\n## 8. Citations, Hallucination Detection, and Guardrails\n\nA production-quality RAG answer should often expose where its claims came from.\n\n### Citations\n\nCitations let the user trace an answer back to the retrieved sources. This improves explainability in two ways:\n\n1. A user can verify a claim.\n2. A team can distinguish a model-generation problem from a source-data problem.\n\nIf a cited document itself contains incorrect information, the failure is different from an LLM inventing content with no supporting source.\n\n### Hallucination detection\n\nAfter generation, a RAG pipeline can check whether the answer is consistent with the retrieved facts. This is a form of **hallucination detection**.\n\nConceptually:\n\n```text\nRetrieved facts + generated answer\n          |\n          v\nCheck whether claims are supported\n          |\n          +--> acceptable -> return\n          |\n          +--> unsupported -> block, revise, or flag\n```\n\n### Other guardrails\n\nThe chapter also names guardrails for:\n\n- bias,\n- toxic or harmful responses,\n- disallowed content.\n\nThe key lesson is that generation is not necessarily the last step. A robust system can validate and filter the response before it reaches the user.\n\n---\n\n## 9. From Prototype to Production RAG\n\nA proof of concept can be small. A mission-critical RAG system must also be operable, measurable, secure, and scalable.\n\nThe chapter groups these concerns into several areas.\n\n### 9.1 Better retrieval and broader data\n\nProduction systems may need:\n\n- hybrid retrieval,\n- reranking,\n- multimodal information such as tables, images, and flowcharts,\n- knowledge graphs,\n- agentic workflows.\n\n### 9.2 Continuous evaluation\n\nYou need to measure more than whether one demo question "looks good." Evaluation can cover:\n\n```text\nretrieval quality\ngeneration quality\nhallucination / faithfulness\ncitation quality\n```\n\nEvaluation should continue as the system changes.\n\n### 9.3 CI/CD and automated data refresh\n\nWhen source data changes, an event-driven ingestion process can update the RAG knowledge base:\n\n```text\nSource update\n  -> ETL trigger\n  -> preprocess / chunk\n  -> embed\n  -> index\n  -> refreshed searchable knowledge\n```\n\nAutomated RAG evaluation can also be integrated into CI/CD so that a model, prompt, or data change that degrades quality is caught before deployment.\n\n### 9.4 Version control and reproducibility\n\nPrompts should be treated as versioned artifacts. The chapter also recommends versioning components such as:\n\n- embedding models,\n- chunking logic,\n- the generative LLM.\n\nThis supports reproducibility and rollback.\n\n### 9.5 Observability and cost monitoring\n\nTracing a single request across the RAG pipeline helps explain why a bad response occurred.\n\nUseful measurements include:\n\n- ingestion performance,\n- retrieval performance,\n- LLM generation performance,\n- token usage,\n- total cost per query.\n\n### 9.6 Performance and scalability\n\nThe chapter highlights:\n\n- database indexing strategies,\n- sharding,\n- caching,\n- optimized inference,\n- autoscaling inference endpoints.\n\nIt also makes an important distinction: a retrieval algorithm may scale efficiently, but the overall system can still be limited by database concurrency, network latency, or other engineering bottlenecks.\n\n### 9.7 Security and governance\n\nSecurity must apply to the data path, not only to the user interface.\n\nThe chapter calls out:\n\n- granular role-based access controls at the data level,\n- encryption at rest,\n- encryption in motion,\n- prompt/input sanitization,\n- output filtering,\n- redaction of personally identifiable information (PII).\n\nA critical rule is:\n\n```text\nThe retriever should not return a document\nthat the current user is not authorized to access.\n```\n\nPermission-aware retrieval is part of the architecture.\n\n{{exercise:M01.L01.EX04}}\n\n---\n\n## 10. Worked Example: Ingesting Documents with LangChain\n\nThe chapter demonstrates a small RAG pipeline grounded in *Alice\'s Adventures in Wonderland*. The purpose is not to present a production architecture; it is to make the ingestion/query pattern concrete.\n\nThe ingestion stages are:\n\n```text\nPDF\n -> parse pages\n -> split text into chunks\n -> embed chunks\n -> store chunks + embeddings in LanceDB\n```\n\nThe source example uses these LangChain components:\n\n- `PyPDFLoader`\n- `RecursiveCharacterTextSplitter`\n- `OpenAIEmbeddings`\n- `LanceDB`\n\nAn adapted version of the same idea is:\n\n```python\nfrom langchain_community.document_loaders import PyPDFLoader\nfrom langchain_text_splitters import RecursiveCharacterTextSplitter\nfrom langchain_openai import OpenAIEmbeddings\nfrom langchain_community.vectorstores import LanceDB\n\nloader = PyPDFLoader("path/to/document.pdf")\npages = loader.load()\n\nsplitter = RecursiveCharacterTextSplitter(\n    chunk_size=1000,\n    chunk_overlap=200,\n    length_function=len,\n)\nchunks = splitter.split_documents(pages)\n\nembedding_model = OpenAIEmbeddings(model="text-embedding-3-small")\nvector_store = LanceDB.from_documents(chunks, embedding_model)\n```\n\n### What each part does\n\n`PyPDFLoader` turns the PDF into document objects that can be processed.\n\n`RecursiveCharacterTextSplitter` breaks long material into chunks. The example uses a chunk size of `1000` and overlap of `200`.\n\n`OpenAIEmbeddings` converts each chunk into an embedding.\n\n`LanceDB.from_documents(...)` creates a searchable vector store from the chunks and their embeddings.\n\nThis is the ingestion half of the system. No user answer has been generated yet.\n\n---\n\n## 11. Worked Example: Building the Query Chain\n\nThe source then constructs a query-time chain.\n\nIts main pieces are:\n\n- an LLM,\n- a retriever configured to return the top three chunks,\n- a formatting function that joins retrieved document text,\n- a prompt containing `context` and `question`,\n- a runnable chain,\n- a string output parser.\n\nAn adapted version is:\n\n```python\nfrom langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\nfrom langchain_core.runnables import RunnablePassthrough\n\nllm = ChatOpenAI(model="gpt-4o-mini", temperature=0)\nretriever = vector_store.as_retriever(search_kwargs={"k": 3})\n\ndef format_docs(docs):\n    return "\\n\\n".join(doc.page_content for doc in docs)\n\nprompt = ChatPromptTemplate.from_template(\n    "Answer the question using only the following context:\\n\\n"\n    "{context}\\n\\nQuestion: {question}"\n)\n\nrag_chain = (\n    {\n        "context": retriever | format_docs,\n        "question": RunnablePassthrough(),\n    }\n    | prompt\n    | llm\n    | StrOutputParser()\n)\n```\n\nThe data movement is more important than the syntax:\n\n```text\nquestion\n   |------------------------------+\n   |                              |\n   v                              v\nretriever                      pass through\n   |                              |\ntop chunks                        |\n   |                              |\nformat_docs                       |\n   +-----------> prompt <---------+\n                    |\n                    v\n                   LLM\n                    |\n                    v\n              string output\n```\n\n[[IMAGE_NEEDED: LangChain RAG query chain | A flow diagram showing the incoming question splitting into two paths: one to the retriever and document formatter for context, and one passed through unchanged as the question; both enter the prompt, then the LLM, then the string output parser | Learner should notice that the same user question drives retrieval and is also preserved as the question supplied to the LLM]]\n\nThe source demonstrates invoking the chain with a question about the Mad Hatter\'s tea party and receiving a synthesized answer from the retrieved text.\n\nOne small implementation detail is visible directly in the supplied code: the sample assigns the text to a variable named `Query` but invokes the chain using `q`. In an implementation, the variable passed to `invoke(...)` must be the variable that actually holds the question.\n\n{{exercise:M01.L01.EX05}}\n\n---\n\n## 12. RAG vs "Chat with PDF" and Long-Context Prompting\n\nRAG can look similar to "chat with PDF," but the underlying strategy may be very different.\n\nA simple document-chat system can place the entire document into the prompt:\n\n```text\nFull PDF text\n+ question\n-> LLM\n```\n\nThe chapter notes that very large context windows can make this practical for small or moderate collections. But the approach becomes problematic at enterprise scale.\n\n### Limitation 1: cost\n\nIf the prompt includes everything, the model processes large amounts of text that may be irrelevant to the question.\n\nRAG instead tries to send only the most relevant evidence.\n\n### Limitation 2: latency\n\nLong prompts take more processing. Even when they technically fit in the model\'s context window, they can increase response latency.\n\n### Limitation 3: document selection\n\nIf an organization has data spread across Google Drive, Notion, SharePoint, PDFs, and other systems, somebody or something still has to decide which content belongs in the prompt.\n\nOnce the system automatically selects relevant documents, you have reintroduced retrieval.\n\n### The core comparison\n\n| Full-context approach | RAG |\n|---|---|\n| Sends large amounts of available text | Selects relevant evidence |\n| Can work well for small collections | Designed to scale to large collections |\n| Pays processing cost for irrelevant context | Tries to reduce unnecessary context |\n| Requires a way to choose documents at scale | Retrieval is the selection mechanism |\n\n{{exercise:M01.L01.EX06}}\n\n---\n\n## 13. RAG vs Fine-Tuning\n\nFine-tuning adapts a pre-trained model by continuing training on additional data. This changes the model\'s internal parameters.\n\nRAG takes a different approach: keep the knowledge externally retrievable and provide relevant facts at query time.\n\n### 13.1 Expertise gap\n\nThe chapter warns that fine-tuning requires careful data preparation and deep learning expertise. Risks include:\n\n- overfitting,\n- regression in general model capabilities,\n- importing bias from the new data,\n- safety regressions.\n\nIt also notes that modern models usually undergo post-training such as supervised fine-tuning (SFT) and reinforcement learning with human feedback (RLHF). Additional fine-tuning can interfere with those behaviors if handled poorly.\n\n### 13.2 Cost and changing data\n\nFine-tuning has training cost. The update frequency creates another challenge:\n\n```text\nIf the enterprise data changes every day,\nhow often would you retrain?\n```\n\nRAG can instead update the external knowledge store.\n\n### 13.3 Access control\n\nThis is one of the chapter\'s strongest distinctions.\n\nSuppose training data mixes:\n\n```text\nEngineering\nHR\nFinance\nLegal\n```\n\nAfter fine-tuning, learned information is blended into model weights. It is difficult to separate "knowledge allowed for HR" from "knowledge allowed for everyone" at answer time.\n\nWith RAG, permission metadata can be stored with documents and used as a retrieval filter.\n\n```text\nUser query + user permissions\n          |\n          v\npermission-aware retrieval\n          |\n          v\nonly authorized evidence\n```\n\n### 13.4 They are not mutually exclusive\n\nThe chapter explicitly notes that a fine-tuned LLM can still be used inside a RAG system.\n\nThe choice is not:\n\n```text\nRAG XOR fine-tuning\n```\n\nA system may use fine-tuning for model behavior or domain adaptation while still using RAG to provide fresh, controllable external knowledge.\n\n{{exercise:M01.L01.EX07}}\n\n---\n\n## 14. Key Benefits of RAG\n\nThe chapter highlights several benefits.\n\n### 14.1 Scalability and efficiency\n\nA retrieval engine can search collections containing very large numbers of documents without placing the whole collection into every LLM prompt.\n\nThe chapter contrasts this with an LLM\'s self-attention cost, which grows quadratically with sequence length.\n\nHowever, retrieval efficiency does not automatically guarantee whole-system scalability. Database concurrency, network latency, and other production bottlenecks still matter.\n\n### 14.2 Reduced hallucination\n\nRAG provides relevant facts for the model to use.\n\nIf the application is designed to respond with "I don\'t know" when evidence is absent, it can avoid forcing an unsupported answer.\n\nRAG **reduces** hallucination risk; it does not logically guarantee that hallucinations disappear. Retrieval can be wrong, source data can be wrong, and the model can still misuse context. That is why evaluation and guardrails remain necessary.\n\n### 14.3 Explainability\n\nBecause retrieved evidence can be cited, users can inspect the source behind claims.\n\nThis is much more traceable than trying to reconstruct which training examples caused a particular fact to be represented in model weights.\n\n### 14.4 Fast knowledge updates\n\nExternal RAG data can be updated using ordinary ETL-style processes.\n\n```text\nChange document\n -> reprocess affected knowledge\n -> update index\n -> new queries can retrieve the new version\n```\n\nThe LLM does not need to memorize the update.\n\n### 14.5 Access controls\n\nPermission information can be attached to documents during ingestion and applied during retrieval.\n\nThis makes RAG attractive for enterprise systems that need both grounding and data-level authorization.\n\n{{exercise:M01.L01.EX08}}\n\n---\n\n## 15. Virtual Assistants, Chatbots, and Education\n\nRAG is useful whenever an assistant needs to answer from organization-specific knowledge.\n\n### Customer support\n\nAn airline, for example, might connect a RAG assistant to:\n\n- support logs,\n- FAQs,\n- website information,\n- internal policies.\n\nThe assistant can be internal, supporting customer-service staff, or external, speaking directly with customers.\n\n### Education\n\nA school or university can ground an AI tutor in teacher-approved course materials.\n\nThe chapter describes two modes:\n\n```text\nTutor mode:\nstudent asks -> RAG retrieves course evidence -> assistant answers\n\nExaminer mode:\nagent asks questions -> student answers -> system evaluates\n                                  |\n                                  +-> new questions target weak areas\n```\n\n[[IMAGE_NEEDED: RAG-powered tutor and examiner | Course materials flowing through ingestion into a vector database, then an AI agent interacting with a student in two modes: tutor mode answering student questions and examiner mode asking and grading questions | Learner should notice that both tutoring and assessment are grounded in the same approved course knowledge]]\n\nThe important pattern is not "chatbot" by itself. It is a chatbot whose answers are constrained by a defined knowledge base.\n\n---\n\n## 16. Enterprise Search and Grounded Content Creation\n\n### Enterprise knowledge management\n\nOrganizations often spread information across many systems. Traditional search may return a list of documents that the employee must open, read, and mentally combine.\n\nRAG adds a generation layer:\n\n```text\nEmployee question\n -> retrieve relevant passages across enterprise sources\n -> synthesize the passages\n -> produce a direct answer\n```\n\nThis can reduce the time spent manually reading many search results.\n\n### Automated content creation and summarization\n\nEnterprise writing often requires research and fact-checking.\n\nA RAG workflow can:\n\n```text\nContent request\n -> retrieve recent relevant information\n -> generate a draft or summary\n -> human review when needed\n```\n\nThe value comes from grounding generation in the latest available enterprise material rather than relying only on the LLM\'s parametric knowledge.\n\n---\n\n## 17. Question Answering, Healthcare, and Legal Research\n\n### Question-answering systems\n\nA RAG question-answering system may be simpler in interaction style than a chatbot:\n\n```text\none question -> one grounded answer\n```\n\nThe chapter gives requests for proposals (RFPs) and requests for information (RFIs) as an example. A system can retrieve:\n\n- historical responses,\n- product specifications,\n- pricing,\n- customer interactions,\n\nand synthesize a tailored response.\n\n### Healthcare\n\nA healthcare RAG system may combine:\n\n- patient medical records,\n- physician notes,\n- treatment guidelines,\n- research articles.\n\nThe chapter emphasizes two non-negotiable conditions for life-critical use:\n\n- privacy/compliance requirements such as HIPAA in the context described,\n- **human-in-the-loop (HITL)** validation by a qualified clinician.\n\nThe AI output is not a substitute for clinical validation.\n\n### Legal and compliance research\n\nRAG can help retrieve:\n\n- case law,\n- statutes,\n- internal compliance documents.\n\nThe goal is to accelerate research while keeping answers connected to source material, which is important when precision and traceability matter.\n\n---\n\n## 18. Personalized Advertising with Retrieval\n\nThe chapter also presents RAG as a retrieval-and-generation pattern for personalized advertising.\n\nConceptually:\n\n```text\nUser context\n   +\nproduct catalog in searchable knowledge base\n   |\n   v\nretrieve relevant products / facts\n   |\n   v\ngenerate ad copy tailored to the context\n```\n\n[[IMAGE_NEEDED: Retrieval-powered personalized advertising | User context such as current interests and prior purchases flowing alongside a searchable product knowledge base into retrieval, followed by an LLM generating a personalized advertisement | Learner should notice that retrieval chooses relevant product information while generation adapts the message to the user\'s context]]\n\nThe same product can be described differently depending on what is relevant to the user. The retrieval stage selects applicable product information; the generation stage turns it into contextualized language.\n\nThe architectural lesson is broader than advertising: RAG can support **selection plus generation**, not only factual question answering.\n\n---\n\n## 19. Agentic RAG\n\nBasic RAG is often presented as a one-shot pipeline:\n\n```text\nretrieve once -> generate once\n```\n\n**Agentic RAG** allows an AI agent to orchestrate retrieval more dynamically.\n\n### Iterative and multi-step retrieval\n\nIf the first retrieval is insufficient, the agent can reformulate or retrieve again.\n\n```text\nQuestion\n -> retrieve\n -> evidence insufficient?\n      | yes\n      v\n   refine query\n      |\n      +-> retrieve again\n```\n\n### Dynamic tool integration\n\nRetrieval itself can become a tool that the model calls when needed. The agent may also use other tools, such as web search or APIs, rather than relying only on pre-ingested knowledge.\n\n### Advanced reasoning and adaptability\n\nThe chapter describes agents that can:\n\n- decompose complex queries,\n- plan retrieval strategies,\n- validate information,\n- coordinate specialized subagents.\n\n[[IMAGE_NEEDED: Agentic RAG loop | An agent receiving a complex question, planning, calling retrieval as a tool, evaluating returned evidence, optionally reformulating the query and retrieving again, then producing a final response | Learner should notice the feedback loop and that retrieval can occur multiple times rather than only once]]\n\nAgentic RAG is useful when a single retrieval step cannot reliably gather everything required for a multi-part problem.\n\n{{exercise:M01.L01.EX09}}\n\n---\n\n## 20. Multimodal RAG\n\nRAG began primarily with text, but useful enterprise knowledge also lives in:\n\n- tables,\n- diagrams,\n- charts,\n- images,\n- whole document pages.\n\nThe chapter presents two broad approaches.\n\n### Approach 1: convert modalities to text\n\nFor example:\n\n```text\nimage -> caption / extracted text -> text RAG pipeline\n```\n\nThis keeps the downstream pipeline text-based.\n\n### Approach 2: keep the original modality\n\nMultimodal embedding models and vision-language or multimodal language models can work with non-text data more directly.\n\n```text\ntext + image/table/page\n -> multimodal representations / retrieval\n -> multimodal model at query time\n```\n\nA newer end-to-end direction described in the chapter is to embed entire pages and send relevant pages to a multimodal LLM.\n\n[[IMAGE_NEEDED: Two multimodal RAG strategies | Side-by-side comparison: left converts images/tables/diagrams into text before retrieval and generation; right preserves original modalities, retrieves multimodal content, and sends it to a vision-language or multimodal LLM | Learner should notice the trade-off between normalizing everything into text and preserving the original modality]]\n\n---\n\n## 21. RAG with Knowledge Graphs\n\nFlat text retrieval can struggle when answering requires connecting facts across multiple documents.\n\nA **knowledge graph (KG)** represents entities and the relationships between them.\n\nA simplified graph might look like:\n\n```text\n[Customer A] --owns--> [Account 17]\n[Account 17] --belongs_to--> [Region East]\n[Region East] --managed_by--> [Team Delta]\n```\n\nA question may require following several relationships. This is **multi-hop reasoning**.\n\nThe chapter describes a pipeline in which unstructured documents are processed to extract entities and relationships, which are then used to construct a knowledge graph.\n\n[[IMAGE_NEEDED: Knowledge-graph-enhanced RAG | A small graph of entities connected by labeled relationships, with a query requiring two or more hops across the graph before evidence is supplied to an LLM | Learner should notice how explicit relationships help connect facts that may be scattered across different documents]]\n\nIt also introduces **GraphRAG**, popularized by Microsoft, as an approach that processes unstructured documents to extract entities and relationships and constructs a graph capturing connections in the data.\n\nThe purpose is not simply to replace vector search. It is to add structured relationships that can help with questions where "connecting the dots" matters.\n\n{{exercise:M01.L01.EX10}}\n\n---\n\n## 22. The System Mental Model to Carry Forward\n\nThe chapter\'s most important shift is to stop thinking of an LLM application as "a model that knows things" and start thinking of it as a **system that must supply evidence**.\n\nA useful end-to-end mental model is:\n\n```text\nKNOWLEDGE PREPARATION\nsources\n -> extraction\n -> cleaning / organization\n -> chunking\n -> embeddings / indexes\n -> searchable stores\n\nQUESTION PROCESSING\nuser question\n -> retrieval\n -> optional hybrid search / reranking\n -> authorized evidence\n -> prompt construction\n -> LLM generation\n -> citations\n -> guardrails\n -> final response\n\nOPERATIONS AROUND BOTH FLOWS\nevaluation\nmonitoring\nsecurity\nversioning\ncost control\nscaling\ncontinuous data refresh\n```\n\nRAG is therefore not only a prompt pattern. At production scale, it is a data system, search system, LLM system, security boundary, and operational pipeline working together.\n\n---\n\n## Important misconceptions\n\n### Misconception 1\n\n> If an LLM is large enough, it should already know my organization\'s private and current data.\n\n### Why this is wrong\n\nTraining cannot include information that was private, unavailable, or created after training. RAG exists specifically to supply such external information at query time.\n\n### Misconception 2\n\n> RAG means placing every available document into the prompt.\n\n### Why this is wrong\n\nThe retrieval step is designed to select relevant evidence. Sending all documents is closer to full-context prompting and creates cost, latency, and scaling problems.\n\n### Misconception 3\n\n> Vector search and RAG are the same thing.\n\n### Why this is wrong\n\nVector search is one retrieval technique. A RAG system also includes generation, and production retrieval may use lexical search, hybrid search, reranking, or other methods.\n\n### Misconception 4\n\n> If I use RAG, hallucinations are impossible.\n\n### Why this is wrong\n\nRAG can reduce hallucinations by supplying evidence, but poor retrieval, incorrect source data, or generation errors can still produce bad answers. Evaluation and guardrails are still required.\n\n### Misconception 5\n\n> Fine-tuning and RAG are mutually exclusive.\n\n### Why this is wrong\n\nA fine-tuned model can be used as the generative LLM inside a RAG pipeline. The techniques solve different aspects of the problem.\n\n### Misconception 6\n\n> Updating RAG knowledge means retraining the LLM.\n\n### Why this is wrong\n\nThe retrieved knowledge is stored outside the LLM and can be refreshed through ingestion and indexing workflows.\n\n### Misconception 7\n\n> Access control can be handled only after the LLM generates the answer.\n\n### Why this is wrong\n\nSensitive documents should be filtered during retrieval so unauthorized evidence is not supplied to the model in the first place.\n\n### Misconception 8\n\n> RAG is only for question-answering chatbots.\n\n### Why this is wrong\n\nThe chapter describes enterprise search, content creation, personalized advertising, education, healthcare, legal research, and other applications that combine retrieval with generation.\n\n---\n\n## Key terminology\n\n| Term | Meaning |\n|---|---|\n| Retrieval-augmented generation (RAG) | A pattern that retrieves external information and supplies it to an LLM for grounded generation |\n| Retrieval | Finding information relevant to the user\'s query |\n| Generation | Producing the final response with an LLM using the query and retrieved evidence |\n| Augmentation | Adding retrieved information to the LLM\'s prompt or working context |\n| Hallucination | Generated content unsupported by the evidence or knowledge available to justify it |\n| Parametric knowledge | Knowledge represented through the learned parameters or weights of a model |\n| Embedding | A vector representation used to capture semantic properties of content |\n| Vector database | A database designed to store and search vector representations, commonly alongside source text and metadata |\n| Indexing | Building search-oriented representations or structures from source content |\n| Dataset / document set | The initial raw collection of source data |\n| Corpus | A curated, cleaned, organized body of content |\n| Index | A high-performance structure optimized for search and retrieval |\n| Semantic search | Retrieval based on meaning similarity represented in embedding space |\n| Lexical search | Retrieval based on similarity in words or written form |\n| Hybrid search | Retrieval that combines semantic and lexical methods |\n| Reranking | Reordering retrieved candidates to place the most relevant evidence first |\n| Grounding | Constraining or supporting generation with retrieved evidence |\n| Citation | A reference connecting an answer claim to its source evidence |\n| Guardrail | A validation or filtering step used to enforce quality, safety, or policy expectations |\n| RBAC | Role-based access control used to limit data access according to authorization |\n| ETL | Extract, transform, load processes used to move and prepare data |\n| LLMOps / MLOps | Operational practices for deploying, evaluating, monitoring, and maintaining model-based systems |\n| Agentic RAG | RAG in which an agent can plan, call retrieval/tools, and perform iterative or multi-step retrieval |\n| Multimodal RAG | RAG that includes non-text information such as images, tables, diagrams, or pages |\n| Knowledge graph | A structured representation of entities and relationships |\n| Multi-hop reasoning | Connecting multiple related facts or graph edges to answer a question |\n| GraphRAG | A graph-oriented RAG approach that builds entity-and-relationship structures from unstructured data |\n| HITL | Human-in-the-loop validation in which a qualified person reviews or controls important AI-assisted decisions |\n\n---\n\n## Self-check\n\nBefore continuing, make sure you can answer these without looking back:\n\n1. Why can an LLM be fluent yet still fail on a company\'s private policy?\n2. Why does a larger training dataset not permanently solve freshness and private-data problems?\n3. What are the two core stages represented by the letters R and G in RAG?\n4. What does "augmented" mean in retrieval-augmented generation?\n5. What information normally enters the LLM during the generation stage of RAG?\n6. Why is the closed-book/open-book analogy useful for understanding RAG?\n7. What is parametric knowledge?\n8. How is retrieved knowledge different from parametric knowledge?\n9. What is the purpose of the ingestion flow?\n10. What is the purpose of the query flow?\n11. Why does a vector store need the original text in addition to embeddings?\n12. What is an embedding used for in the chapter\'s basic RAG design?\n13. Distinguish a dataset, corpus, and index.\n14. What happens when a user query is converted into an embedding?\n15. What is semantic search?\n16. How does lexical search differ from semantic search?\n17. Why might semantic search alone be insufficient in production?\n18. What does hybrid search combine?\n19. What does reranking do?\n20. What makes retrieved evidence "good" for RAG generation?\n21. What should a RAG prompt tell the LLM to do when the evidence does not contain an answer?\n22. Why are citations useful to an end user?\n23. How can citations help an engineering team debug an incorrect answer?\n24. What is hallucination detection checking after generation?\n25. Name two guardrails other than hallucination detection mentioned in the chapter.\n26. Why should RAG quality be evaluated continuously rather than only at launch?\n27. What role can automated data refresh play in CI/CD for RAG?\n28. Why should prompts and model components be versioned?\n29. What can request tracing tell you about a bad RAG response?\n30. Which costs or performance measurements can be monitored per RAG component?\n31. How can database concurrency or network latency limit a system even if retrieval is efficient?\n32. Why should permissions be applied at retrieval time?\n33. What is the purpose of encryption at rest and in motion in a RAG system?\n34. Why are prompt sanitization and output filtering part of production RAG?\n35. In the LangChain ingestion example, what are the roles of the PDF loader, text splitter, embedding model, and LanceDB?\n36. Why does the example split documents before embedding them?\n37. In the query chain, why does the question travel both to the retriever and into the prompt?\n38. What is the purpose of `format_docs()` in the source example?\n39. Why can placing an entire PDF collection into a long prompt be wasteful?\n40. How can long-context prompting create a document-selection problem at enterprise scale?\n41. What expertise risks does the chapter associate with fine-tuning?\n42. Why can frequently changing enterprise data make repeated fine-tuning unattractive?\n43. Why is permission control harder when sensitive knowledge is blended into model weights?\n44. Can a fine-tuned model still be used in RAG? Explain.\n45. List the five major benefits of RAG described in the chapter.\n46. Why does RAG improve explainability compared with relying only on parametric knowledge?\n47. How does external knowledge storage make addition or removal of knowledge easier?\n48. What is the difference between a multiturn chatbot and the single-question QA form factor described in the chapter?\n49. How can RAG support a university tutor?\n50. What additional role can an examiner-style educational RAG agent perform?\n51. How does RAG change enterprise search compared with reading a list of top search results manually?\n52. Why is retrieval useful for automated reports and summaries?\n53. What is the architectural pattern behind personalized RAG-generated advertisements?\n54. What two production requirements does the chapter emphasize for healthcare RAG?\n55. Why are citations and source traceability especially relevant in legal/compliance research?\n56. How does agentic RAG differ from one-shot RAG?\n57. What can an agent do if the first retrieval does not provide enough evidence?\n58. What does it mean to make retrieval a tool available to an agent?\n59. What are the two broad strategies for multimodal RAG described in the chapter?\n60. When might preserving an image or page in its original modality be useful?\n61. What problem do knowledge graphs address that flat text retrieval can struggle with?\n62. What is multi-hop reasoning?\n63. At a high level, how does GraphRAG create graph structure from unstructured documents?\n64. Why is RAG better understood as a system architecture rather than only a prompt trick?\n65. If a RAG answer is wrong, what separate failure locations would you investigate across retrieval, source data, generation, and guardrails?\n\n---\n\n## Retain this idea\n\n**RAG turns an LLM from a closed-book generator into one component of an evidence-driven system: prepare external knowledge so it can be searched, retrieve the right authorized facts for each question, give those facts to the model for grounded generation, and then verify, cite, monitor, and operate the result. The quality of a RAG application therefore depends not only on the LLM, but on the entire chain from data ingestion and retrieval through security, prompting, generation, evaluation, and production operations.**\n',

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": 'why-rag-exists',
                "title": 'Why RAG Exists',
                "order": 1,
            },
            {
                "id": 'core-rag-loop',
                "title": 'The Core RAG Loop: Retrieve, Augment, Generate',
                "order": 2,
            },
            {
                "id": 'parametric-vs-retrieved',
                "title": 'Parametric Knowledge vs Retrieved Knowledge',
                "order": 3,
            },
            {
                "id": 'rag-stack-blueprint',
                "title": 'The Blueprint of a RAG Stack',
                "order": 4,
            },
            {
                "id": 'ingestion-flow',
                "title": 'The Ingestion Flow',
                "order": 5,
            },
            {
                "id": 'retrieval-flow',
                "title": 'Retrieval: Embeddings, Semantic Search, and Better Search',
                "order": 6,
            },
            {
                "id": 'generation-flow',
                "title": 'Generation: Grounding the LLM in Retrieved Facts',
                "order": 7,
            },
            {
                "id": 'citations-and-guardrails',
                "title": 'Citations, Hallucination Detection, and Guardrails',
                "order": 8,
            },
            {
                "id": 'production-rag',
                "title": 'From Prototype to Production RAG',
                "order": 9,
            },
            {
                "id": 'langchain-ingestion',
                "title": 'Worked Example: Ingesting Documents with LangChain',
                "order": 10,
            },
            {
                "id": 'langchain-query',
                "title": 'Worked Example: Building the Query Chain',
                "order": 11,
            },
            {
                "id": 'rag-vs-long-context',
                "title": 'RAG vs "Chat with PDF" and Long-Context Prompting',
                "order": 12,
            },
            {
                "id": 'rag-vs-finetuning',
                "title": 'RAG vs Fine-Tuning',
                "order": 13,
            },
            {
                "id": 'rag-benefits',
                "title": 'Key Benefits of RAG',
                "order": 14,
            },
            {
                "id": 'assistants-and-education',
                "title": 'Virtual Assistants, Chatbots, and Education',
                "order": 15,
            },
            {
                "id": 'enterprise-search-content',
                "title": 'Enterprise Search and Grounded Content Creation',
                "order": 16,
            },
            {
                "id": 'question-answering-health-legal',
                "title": 'Question Answering, Healthcare, and Legal Research',
                "order": 17,
            },
            {
                "id": 'personalized-ads',
                "title": 'Personalized Advertising with Retrieval',
                "order": 18,
            },
            {
                "id": 'agentic-rag',
                "title": 'Agentic RAG',
                "order": 19,
            },
            {
                "id": 'multimodal-rag',
                "title": 'Multimodal RAG',
                "order": 20,
            },
            {
                "id": 'knowledge-graph-rag',
                "title": 'RAG with Knowledge Graphs',
                "order": 21,
            },
            {
                "id": 'rag-system-mental-model',
                "title": 'The System Mental Model to Carry Forward',
                "order": 22,
            },
        ],
    },

    "exercises": [
        {
            "id": 'M01.L01.EX01',

            "title": 'Diagnose the Knowledge Gap',

            "lesson_code": "M01.L01",

            "section_id": 'why-rag-exists',

            "placement": "after_section",

            "description": 'Decide which questions require external organizational knowledge rather than relying only on a base LLM.',

            "instructions": '1. Write four example questions for an internal company assistant.\n2. Make two questions answerable from broad world knowledge and two dependent on private or recently updated company data.\n3. For each question, state whether RAG is needed and why.\n4. Identify the risk if the model answers a private-data question without retrieval.',

            "expected_output": 'A four-row table containing the question, knowledge source needed, whether retrieval is required, and the main failure risk.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'rag-problem-framing',
                'knowledge-boundary-analysis',
            ],
        },

        {
            "id": 'M01.L01.EX02',

            "title": 'Design an Ingestion Flow',

            "lesson_code": "M01.L01",

            "section_id": 'ingestion-flow',

            "placement": "after_section",

            "description": 'Translate a small private document collection into the stages of a RAG ingestion pipeline.',

            "instructions": '1. Assume the source is a folder of company policy PDFs.\n2. Describe the path from raw PDFs to searchable records.\n3. State what should be stored alongside each embedding.\n4. Label which artifact is the dataset, which is the corpus, and which is the index.',

            "expected_output": 'A text diagram of the ingestion pipeline plus a short explanation distinguishing dataset, corpus, and index.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'ingestion-design',
                'rag-data-modeling',
            ],
        },

        {
            "id": 'M01.L01.EX03',

            "title": 'Write a Grounded Generation Contract',

            "lesson_code": "M01.L01",

            "section_id": 'generation-flow',

            "placement": "after_section",

            "description": 'Create prompt instructions that make retrieved evidence the basis of the answer.',

            "instructions": '1. Write a short prompt template with placeholders for a question and retrieved context.\n2. Require the answer to use the supplied context.\n3. Specify what the model should do when the context is insufficient.\n4. Explain why each instruction reduces unsupported generation.',

            "expected_output": 'A compact prompt template followed by a four-to-six sentence explanation of its grounding behavior.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'prompt-grounding',
                'failure-behavior-design',
            ],
        },

        {
            "id": 'M01.L01.EX04',

            "title": 'Production RAG Failure Review',

            "lesson_code": "M01.L01",

            "section_id": 'production-rag',

            "placement": "after_section",

            "description": 'Map production failures to evaluation, monitoring, scalability, or security controls.',

            "instructions": '1. Consider these failures: stale documents, slow vector search, an unauthorized HR document retrieved for a general employee, and quality regression after a prompt change.\n2. Classify each failure as primarily data-refresh, performance, security, or evaluation/versioning.\n3. Propose one control from the chapter for each failure.\n4. Explain why the control belongs at that layer.',

            "expected_output": 'A four-row incident table with failure, category, proposed control, and reasoning.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'production-rag',
                'security-and-observability',
            ],
        },

        {
            "id": 'M01.L01.EX05',

            "title": 'Trace the LangChain Data Flow',

            "lesson_code": "M01.L01",

            "section_id": 'langchain-query',

            "placement": "after_section",

            "description": 'Explain how a question moves through the retriever, formatter, prompt, LLM, and output parser.',

            "instructions": "1. Draw the query chain as a text diagram.\n2. Mark where retrieval happens.\n3. Mark where the original question is preserved.\n4. Explain how retrieved documents become the `{context}` field.\n5. Identify the variable-name mismatch visible in the supplied source's invocation example.",

            "expected_output": 'A labeled data-flow diagram and a short explanation of each stage, including the observed invocation-variable mismatch.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'langchain-reading',
                'rag-pipeline-tracing',
            ],
        },

        {
            "id": 'M01.L01.EX06',

            "title": 'Choose Between Full Context and Retrieval',

            "lesson_code": "M01.L01",

            "section_id": 'rag-vs-long-context',

            "placement": "after_section",

            "description": 'Compare a full-document prompt with a retrieval-based design.',

            "instructions": "1. Scenario A has one short policy PDF used occasionally.\n2. Scenario B has hundreds of thousands of documents across several enterprise systems.\n3. For each scenario, discuss cost, latency, document selection, and scalability.\n4. State which design is more appropriate in each scenario and justify the choice using the chapter's reasoning.",

            "expected_output": 'A comparison table for the two scenarios with a justified architecture choice for each.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'architecture-selection',
                'tradeoff-analysis',
            ],
        },

        {
            "id": 'M01.L01.EX07',

            "title": 'RAG or Fine-Tuning?',

            "lesson_code": "M01.L01",

            "section_id": 'rag-vs-finetuning',

            "placement": "after_section",

            "description": 'Separate knowledge freshness and access-control needs from model-adaptation needs.',

            "instructions": '1. Consider a company with daily policy changes and department-specific confidential documents.\n2. Explain which problems RAG directly addresses.\n3. List the fine-tuning challenges described in the chapter for this case.\n4. Explain one situation in which a fine-tuned LLM could still be used inside the RAG stack.',

            "expected_output": 'A reasoned architecture note comparing RAG and fine-tuning without treating them as mutually exclusive.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'rag-vs-finetuning',
                'enterprise-security',
            ],
        },

        {
            "id": 'M01.L01.EX08',

            "title": 'Benefit-to-Mechanism Mapping',

            "lesson_code": "M01.L01",

            "section_id": 'rag-benefits',

            "placement": "after_section",

            "description": 'Connect each RAG benefit to the mechanism that produces it.',

            "instructions": "1. Create rows for scalability, hallucination reduction, explainability, knowledge updates, and access control.\n2. For each, identify the RAG mechanism responsible for the benefit.\n3. Add one limitation or condition that prevents the benefit from being automatic.\n4. Explain why 'RAG eliminates hallucinations' is too strong a claim.",

            "expected_output": 'A five-row table with benefit, enabling mechanism, and limitation/condition.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'rag-benefits',
                'critical-reasoning',
            ],
        },

        {
            "id": 'M01.L01.EX09',

            "title": 'Turn One-Shot RAG into Agentic RAG',

            "lesson_code": "M01.L01",

            "section_id": 'agentic-rag',

            "placement": "after_section",

            "description": 'Redesign a simple retrieve-once pipeline for a complex multi-part question.',

            "instructions": '1. Start with `question -> retrieve -> generate`.\n2. Add a decision for insufficient evidence.\n3. Add query reformulation and a second retrieval attempt.\n4. Add one optional external tool call.\n5. Explain which steps make the design agentic according to the chapter.',

            "expected_output": 'A text flowchart showing an iterative agentic retrieval loop and a short explanation.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'agentic-rag',
                'iterative-retrieval',
            ],
        },

        {
            "id": 'M01.L01.EX10',

            "title": 'Model a Multi-Hop Knowledge Question',

            "lesson_code": "M01.L01",

            "section_id": 'knowledge-graph-rag',

            "placement": "after_section",

            "description": 'Show why explicit entity relationships can help answer a question that spans several facts.',

            "instructions": '1. Invent four neutral entities such as a customer, account, region, and team.\n2. Connect them with labeled relationships.\n3. Write one question that requires following at least two relationships.\n4. Explain why retrieving one isolated text chunk may be insufficient and how graph structure can help.',

            "expected_output": 'A small text knowledge graph, one multi-hop question, and a short explanation of the graph advantage.',

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                'knowledge-graphs',
                'multi-hop-reasoning',
            ],
        },

    ],

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": 'Introduction to Retrieval-Augmented Generation (RAG) — Knowledge Check',

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": 'M01.L01.Q01',
                "section_id": 'why-rag-exists',
                "question": "Why can a strong general-purpose LLM still fail on a company's newly updated internal policy?",
                "options": [
                    'Its tokenizer cannot process policy language.',
                    "The policy may be private or newer than the model's training knowledge.",
                    'LLMs cannot generate fluent text about organizations.',
                    'RAG is required for every question, including general world knowledge.',
                ],
                "correct": 1,
                "explanation": 'A model can be fluent without having access to private or newly updated facts. RAG supplies such external evidence at query time.',
            },

            {
                "id": 'M01.L01.Q02',
                "section_id": 'core-rag-loop',
                "question": 'What happens during the augmentation part of retrieval-augmented generation?',
                "options": [
                    'The model is retrained on every retrieved document.',
                    "Retrieved information is added to the model's query-time context or prompt.",
                    'The vector database generates the final answer.',
                    "The user's query is removed before generation.",
                ],
                "correct": 1,
                "explanation": 'Augmentation means giving retrieved facts to the LLM along with the question so generation can be grounded in them.',
            },

            {
                "id": 'M01.L01.Q03',
                "section_id": 'parametric-vs-retrieved',
                "question": 'Which description best matches parametric knowledge?',
                "options": [
                    "Information represented in the model's learned weights.",
                    'Documents stored in a vector database.',
                    'Only facts returned by lexical search.',
                    'Metadata attached to a retrieved chunk.',
                ],
                "correct": 0,
                "explanation": 'Parametric knowledge is represented through learned model parameters; retrieved knowledge is supplied externally at query time.',
            },

            {
                "id": 'M01.L01.Q04',
                "section_id": 'ingestion-flow',
                "question": "Which sequence best represents the chapter's basic ingestion idea?",
                "options": [
                    'Question -> LLM -> answer -> embed answer',
                    'Raw source -> prepare/split -> embed/index -> store searchable representation and text',
                    'Vector DB -> fine-tune model -> delete source',
                    'Prompt -> rerank -> ETL -> source document',
                ],
                "correct": 1,
                "explanation": 'Ingestion turns raw source content into search-ready structures, commonly chunks with embeddings plus the original text.',
            },

            {
                "id": 'M01.L01.Q05',
                "section_id": 'retrieval-flow',
                "question": 'Why might a production system combine semantic and lexical search?',
                "options": [
                    'Because embeddings cannot be stored in databases.',
                    'Because semantic search is always slower than generation.',
                    'Because complementary retrieval signals can improve candidate quality.',
                    'Because lexical search performs LLM generation.',
                ],
                "correct": 2,
                "explanation": 'The chapter presents hybrid search as a way to combine semantic meaning with written-form matching to improve retrieval.',
            },

            {
                "id": 'M01.L01.Q06',
                "section_id": 'citations-and-guardrails',
                "question": 'What is one major engineering benefit of citations in RAG?',
                "options": [
                    'They make embeddings unnecessary.',
                    'They let users and engineers trace claims back to retrieved sources.',
                    'They guarantee that every source document is correct.',
                    'They replace access controls.',
                ],
                "correct": 1,
                "explanation": 'Citations improve traceability and help distinguish generation failures from problems in source data.',
            },

            {
                "id": 'M01.L01.Q07',
                "section_id": 'production-rag',
                "question": 'Where should document permissions ideally affect a RAG pipeline?',
                "options": [
                    'Only after the final answer is shown.',
                    'During retrieval so unauthorized documents are excluded from evidence.',
                    'Only during model pre-training.',
                    "Only inside the user's browser.",
                ],
                "correct": 1,
                "explanation": 'The chapter emphasizes data-level access control: the retriever should return only documents the user is authorized to see.',
            },

            {
                "id": 'M01.L01.Q08',
                "section_id": 'langchain-query',
                "question": "In the chapter's LangChain query chain, what is the retriever responsible for?",
                "options": [
                    'Formatting the final answer as a string.',
                    'Returning relevant chunks from the vector store.',
                    'Fine-tuning the chat model.',
                    'Encrypting the source PDF.',
                ],
                "correct": 1,
                "explanation": 'The retriever queries the vector store and returns relevant document chunks; later stages format, prompt, generate, and parse.',
            },

            {
                "id": 'M01.L01.Q09',
                "section_id": 'rag-vs-long-context',
                "question": 'Why can putting every enterprise document into a long prompt be inefficient?',
                "options": [
                    'It prevents the LLM from receiving any text.',
                    'It processes large amounts of irrelevant content, increasing cost and latency.',
                    'It automatically converts all documents into knowledge graphs.',
                    'It provides stronger document-level permissions than retrieval.',
                ],
                "correct": 1,
                "explanation": 'The chapter argues that full-context prompting wastes computation on irrelevant information and does not scale well to large collections.',
            },

            {
                "id": 'M01.L01.Q10',
                "section_id": 'rag-vs-finetuning',
                "question": 'Which access-control problem does the chapter associate with fine-tuning on mixed confidential data?',
                "options": [
                    'The vector store cannot store metadata.',
                    'Knowledge becomes blended into model weights and is difficult to separate by user permission at query time.',
                    'Fine-tuned models cannot generate text.',
                    'Fine-tuning forces every document to remain public.',
                ],
                "correct": 1,
                "explanation": 'When knowledge is absorbed into model weights, document-level segmentation is much harder than filtering external documents during RAG retrieval.',
            },

            {
                "id": 'M01.L01.Q11',
                "section_id": 'rag-benefits',
                "question": 'Which statement about hallucinations is most consistent with the chapter?',
                "options": [
                    'RAG makes hallucinations mathematically impossible.',
                    'RAG can reduce hallucinations by supplying relevant facts, but validation still matters.',
                    'Only fine-tuning can reduce hallucinations.',
                    'Citations remove the need for retrieved evidence.',
                ],
                "correct": 1,
                "explanation": 'Grounding helps, but retrieval quality, source correctness, and generation behavior can still fail; guardrails and evaluation remain important.',
            },

            {
                "id": 'M01.L01.Q12',
                "section_id": 'assistants-and-education',
                "question": 'What distinguishes the educational examiner mode described in the chapter?',
                "options": [
                    'It only retrieves answers to questions asked by the student.',
                    'It proactively asks questions, grades responses, and can target weak areas.',
                    'It removes the need for course materials.',
                    'It fine-tunes a separate model for every student.',
                ],
                "correct": 1,
                "explanation": 'The examiner mode is proactive: it generates questions, evaluates answers, and can reinforce areas needing improvement.',
            },

            {
                "id": 'M01.L01.Q13',
                "section_id": 'agentic-rag',
                "question": 'What is a defining capability of agentic RAG?',
                "options": [
                    'It must retrieve exactly once.',
                    'It can iteratively retrieve, reformulate queries, and use tools as needed.',
                    'It cannot use pre-ingested knowledge.',
                    'It removes generation from RAG.',
                ],
                "correct": 1,
                "explanation": 'Agentic RAG allows dynamic orchestration, including multiple retrieval steps, query reformulation, and external tool use.',
            },

            {
                "id": 'M01.L01.Q14',
                "section_id": 'multimodal-rag',
                "question": 'Which pair matches the two multimodal strategies described in the chapter?',
                "options": [
                    'Convert all modalities to text, or preserve modalities and use multimodal models.',
                    'Use only lexical search, or use no retrieval.',
                    'Fine-tune every image, or discard all images.',
                    'Store pages only as SQL rows, or send no context.',
                ],
                "correct": 0,
                "explanation": 'The chapter contrasts text-normalization approaches with approaches that preserve non-text modalities for multimodal retrieval and generation.',
            },

            {
                "id": 'M01.L01.Q15',
                "section_id": 'rag-system-mental-model',
                "type": "open",
                "question": 'You are designing an internal assistant over rapidly changing company documents with department-specific permissions. Describe the ingestion flow, query flow, security control point, evaluation/monitoring needs, and explain why you would not simply place all documents into every prompt.',
            },
        ],

        "passing_score": 70,
    },
}
